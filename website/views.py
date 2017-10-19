import os
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import logout as auth_logout
from website.util import get_mailchimp_api
import mailchimp
from django.contrib import messages
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login


class RegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        next_page = request.POST.get('next')
        if not next_page:
            next_page = '/%s/' % request.LANGUAGE_CODE
        return next_page


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('previous-page', '/%s/' % request.LANGUAGE_CODE))


class LanguageListView(ListView):
    def get_queryset(self):
        import re
        p = re.compile(r'^/(?P<lang>[a-zA-Z]+)/.*$')
        lang =  p.search(self.request.path_info).group('lang')

        return self.queryset.filter(language=lang)


class EventsListView(LanguageListView):
    def get_queryset(self):
        from datetime import datetime
        return self.queryset.filter(end_date__gt=datetime.now())


class LanguageDetailView(DetailView):
    def get_object(self, queryset=None):
        import re
        p = re.compile(r'^/(?P<lang>[a-zA-Z]+)/.*$')
        lang =  p.search(self.request.path_info).group('lang')

        return super(LanguageDetailView, self).get_object(
            self.queryset.filter(language=lang)
        )


def homepage(request):
    return render(request, 'homepage.html', {})


def mc_index(request):
    try:
        m = get_mailchimp_api()
        lists = m.lists.list()
    except mailchimp.Error, e:
        messages.error(request,  'An error occurred: %s - %s' % (e.__class__, e))
        return redirect('/')

    return render_to_response('mailchimp/index.html', {'lists':lists['data']}, context_instance=RequestContext(request))



def mc_subscribe(request):
    list_id = settings.MAILCHIMP_NEWSLETTER_ID
    next_page = '/%s/' % request.LANGUAGE_CODE
    try:
        m = get_mailchimp_api()
        next_page = request.POST['next_page']
        m.lists.subscribe(list_id, {'email': request.POST['email']})
        messages.add_message(request, messages.INFO, _("The email has been successfully subscribed"), extra_tags='newsletter')
    except mailchimp.ListAlreadySubscribedError:
        messages.add_message(request, messages.INFO,  _("That email is already subscribed to the list"), extra_tags='newsletter')
        return redirect(next_page)
    except mailchimp.Error, e:
        messages.error(request,  'An error occurred: %s - %s' % (e.__class__, e))
        return redirect(next_page)

    return redirect(next_page)


def reload_uwsgi(request):
    wsgi = 'website/wsgi.py'
    os.utime(os.path.join(settings.BASE_PATH, wsgi), None)
    messages.success(request, 'WSGI server reloaded successfully.')
    return HttpResponseRedirect(reverse('admin:index'))
