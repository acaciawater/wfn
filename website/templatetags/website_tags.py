# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------

import logging
import sys
import traceback
from django import template
from django.conf import settings
from django.http import HttpRequest

from feincms.module.page.models import BasePage, Page
from feincms.utils.templatetags import (SimpleNodeWithVarAndArgs,
    do_simple_node_with_var_and_args_helper,
    SimpleAssignmentNodeWithVarAndArgs,
    do_simple_assignment_node_with_var_and_args_helper)


logger = logging.getLogger('feincms.templatetags.page')

register = template.Library()

@register.simple_tag(takes_context=True)
def fix_lang_url(context, url , **kwargs):
    import re
    p = re.compile(r'^/(?P<lang>[a-zA-Z]+)/.*$')
    lang =  p.search(context['request'].path).group('lang')
    url = url.replace('/nl/', '/'+str(lang)+'/')
    return url


@register.filter
def get_language_name(language):
    return dict((language[0], language[1]) for language in settings.LANGUAGES).get(language, language)

@register.filter
def get_absolute_url(request):
    return request.build_absolute_uri()

# ------------------------------------------------------------------------
# TODO: Belongs in some utility module
def format_exception(e):
    top = traceback.extract_tb(sys.exc_info()[2])[-1]
    return u"'%s' in %s line %d" % (e, top[0], top[1])


# ------------------------------------------------------------------------
@register.assignment_tag(takes_context=True)
def feincms_nav_reverse(context, feincms_page, level=1, depth=1):
    """
    Saves a list of pages into the given context variable.
    """

    if isinstance(feincms_page, HttpRequest):
        try:
            # warning: explicit Page reference here
            feincms_page = Page.objects.for_request(
                feincms_page, best_match=True)
        except Page.DoesNotExist:
            return []

    mptt_opts = feincms_page._mptt_meta

    # mptt starts counting at zero
    mptt_level_range = [level - 1, level + depth - 1]

    queryset = feincms_page.__class__._default_manager.active().filter(in_navigation=False).filter(
        **{
            '%s__gte' % mptt_opts.level_attr: mptt_level_range[0],
            '%s__lt' % mptt_opts.level_attr: mptt_level_range[1],
        }
    )

    page_level = getattr(feincms_page, mptt_opts.level_attr)

    # Used for subset filtering (level>1)
    parent = None

    if level > 1:
        # A subset of the pages is requested. Determine it depending
        # upon the passed page instance

        if level - 2 == page_level:
            # The requested pages start directly below the current page
            parent = feincms_page

        elif level - 2 < page_level:
            # The requested pages start somewhere higher up in the tree
            parent = feincms_page.get_ancestors()[level - 2]

        elif level - 1 > page_level:
            # The requested pages are grandchildren of the current page
            # (or even deeper in the tree). If we would continue processing,
            # this would result in pages from different subtrees being
            # returned directly adjacent to each other.
            queryset = Page.objects.none()

        if parent:
            if getattr(parent, 'navigation_extension', None):
                # Special case for navigation extensions
                return list(parent.extended_navigation(depth=depth,
                    request=context.get('request')))

            # Apply descendant filter
            queryset &= parent.get_descendants()

    if depth > 1:
        # Filter out children with inactive parents
        # None (no parent) is always allowed
        parents = set([None])
        if parent:
            # Subset filtering; allow children of parent as well
            parents.add(parent.id)

        def _parentactive_filter(iterable):
            for elem in iterable:
                if elem.parent_id in parents:
                    yield elem
                parents.add(elem.id)

        queryset = _parentactive_filter(queryset)

    if hasattr(feincms_page, 'navigation_extension'):
        # Filter out children of nodes which have a navigation extension
        def _navext_filter(iterable):
            current_navextension_node = None
            for elem in iterable:
                # Eliminate all subitems of last processed nav extension
                if current_navextension_node is not None and \
                   current_navextension_node.is_ancestor_of(elem):
                    continue

                yield elem
                if getattr(elem, 'navigation_extension', None):
                    current_navextension_node = elem
                    try:
                        for extended in elem.extended_navigation(depth=depth, request=context.get('request')):
                            # Only return items from the extended navigation which
                            # are inside the requested level+depth values. The
                            # "-1" accounts for the differences in MPTT and
                            # navigation level counting
                            this_level = getattr(extended, mptt_opts.level_attr, 0)
                            if this_level < level + depth - 1:
                                yield extended
                    except Exception as e:
                        logger.warn("feincms_nav caught exception in navigation extension for page %d: %s", current_navextension_node.id, format_exception(e))
                else:
                    current_navextension_node = None

        queryset = _navext_filter(queryset)

    # Return a list, not a generator so that it can be consumed
    # several times in a template.
    return list(queryset)


@register.assignment_tag(takes_context=True)
def feincms_breadcrumbs_raw(context, page):

    if not page or not isinstance(page, BasePage):
        raise ValueError("feincms_breadcrumbs must be called with a valid Page object")

    ancs = page.get_ancestors()[1:]

    bc = [(anc.get_absolute_url(), anc.short_title()) for anc in ancs]

    bc.append((page.get_absolute_url(), page.short_title()))

    return bc

@register.assignment_tag(takes_context=True)
def footer_links(context):

    pages = Page._default_manager.active().filter(language=context.get('request').LANGUAGE_CODE, show_in_footer=True)

    return pages






