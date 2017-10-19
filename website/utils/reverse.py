"""
Third-party application inclusion support.
"""

from email.utils import parsedate
from time import mktime
import re

from django.core import urlresolvers
from django.core.urlresolvers import Resolver404, resolve, reverse as _reverse, NoReverseMatch
from django.db import models
from django.http import HttpResponse
from django.utils.functional import curry as partial, wraps
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from feincms import settings
from feincms.admin.item_editor import ItemEditorForm
from feincms.contrib.fields import JSONField
from feincms.utils import get_object
from feincms.content.application.models import ApplicationContent
from feincms.module.page.models import Page

__author__ = 'maurice'

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_local = local() # Used to store MPTT informations about the currently requested
# page. The information will be used to find the best application
# content instance if a particular application has been added
# more than once to the current website.
# Additionally, we store the page class too, because when we have
# more than one page class, reverse() will want to prefer the page
# class used to render the current page. (See issue #240)


def app_reverse(viewname, urlconf, args=None, kwargs=None, prefix=None, language=None, *vargs, **vkwargs):
    """
    Reverse URLs from application contents

    Works almost like Django's own reverse() method except that it resolves
    URLs from application contents. The second argument, ``urlconf``, has to
    correspond to the URLconf parameter passed in the ``APPLICATIONS`` list
    to ``Page.create_content_type``::

        app_reverse('mymodel-detail', 'myapp.urls', args=...)

        or

        app_reverse('mymodel-detail', 'myapp.urls', kwargs=...)

    The second argument may also be a request object if you want to reverse
    an URL belonging to the current application content.
    """

    # First parameter might be a request instead of an urlconf path, so
    # we'll try to be helpful and extract the current urlconf from it
    appconfig = getattr(urlconf, '_feincms_extra_context', {}).get('app_config', {})
    urlconf = appconfig.get('urlconf_path', urlconf)

    # vargs and vkwargs are used to send through additional parameters which are
    # uninteresting to us (such as current_app)

    # get additional cache keys from the page if available
    # refs https://github.com/feincms/feincms/pull/277/
    fn = getattr(_local, 'page_cache_key_fn', lambda: language if language else '')
    cache_key_prefix = fn()

    app_cache_keys = {
        'none': '%s:app_%s_none' % (cache_key_prefix, urlconf),
        }
    proximity_info = getattr(_local, 'proximity_info', None)
    url_prefix = None

    if proximity_info:
        app_cache_keys.update({
            'all': '%s:app_%s_%s_%s_%s_%s' % ((cache_key_prefix, urlconf,) + proximity_info),
            'tree': '%s:app_%s_%s' % (cache_key_prefix, urlconf, proximity_info[0]),
            })

    for key in ('all', 'tree', 'none'):
        try:
            url_prefix = _local.reverse_cache[app_cache_keys[key]]
            break
        except (AttributeError, KeyError):
            pass
    else:
        try:
            # Take the ApplicationContent class used by the current request
            model_class = _local.page_class.content_type_for(ApplicationContent)
        except AttributeError:
            model_class = None

        if not model_class:
            # Take any
            model_class = ApplicationContent._feincms_content_models[0]

        # TODO: Only active pages? What about multisite support?

        contents = model_class.objects.filter(urlconf_path=urlconf)

        # Helps select ApplicationContent for required language
        if not language is None and 'translations' in Page._feincms_extensions:
            contents = contents.filter(parent__language=language)

        contents = contents.select_related('parent')

        if proximity_info:
            # find the closest match within the same subtree
            tree_contents = contents.filter(parent__tree_id=proximity_info[0])
            if not len(tree_contents):
                # no application contents within the same tree
                cache_key = 'tree'
                try:
                    content = contents[0]
                except IndexError:
                    content = None
            elif len(tree_contents) == 1:
                cache_key = 'tree'
                # just one match within the tree, use it
                content = tree_contents[0]
            else: # len(tree_contents) > 1
                cache_key = 'all'
                try:
                    # select all ancestors and descendants and get the one with
                    # the smallest difference in levels
                    content = (tree_contents.filter(
                        parent__rght__gt=proximity_info[2],
                        parent__lft__lt=proximity_info[1]
                    ) | tree_contents.filter(
                        parent__lft__lte=proximity_info[2],
                        parent__lft__gte=proximity_info[1],
                        )).extra({'level_diff':"abs(level-%d)" % proximity_info[3]}
                    ).order_by('level_diff')[0]
                except IndexError:
                    content = tree_contents[0]
        else:
            cache_key = 'none'
            try:
                content = contents[0]
            except IndexError:
                content = None

        if content:
            if urlconf in model_class.ALL_APPS_CONFIG:
                # We have an overridden URLconf
                urlconf = model_class.ALL_APPS_CONFIG[urlconf]['config'].get(
                    'urls', urlconf)

            if not hasattr(_local, 'reverse_cache'):
                _local.reverse_cache = {}

            # Reimplementation of Page.get_absolute_url because we are quite likely
            # to hit infinite recursion if we call models.permalink because of the
            # reverse monkey patch
            url = content.parent._cached_url[1:-1]
            if url:
                prefix = _reverse('feincms_handler', args=(url,))
                # prefix must always ends with a slash
                prefix += '/' if prefix[-1] != '/' else ''

            else:
                prefix = _reverse('feincms_home')

            _local.reverse_cache[app_cache_keys[cache_key]] = url_prefix = (
                urlconf, prefix)

    if url_prefix:
        return _reverse(viewname,
                        url_prefix[0],
                        args=args,
                        kwargs=kwargs,
                        prefix=url_prefix[1],
                        *vargs, **vkwargs)
    raise NoReverseMatch("Unable to find ApplicationContent for '%s'" % urlconf)


