from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from website.util import xsendfileserve
from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.contrib.auth import views as auth_views
from website.views import logout, mc_subscribe
from django.views.generic import TemplateView
from registration.backends.simple.views import RegistrationView
from website.forms import UserRegForm, LoginForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/reload/', 'website.views.reload_uwsgi', name='reload_uwsgi'),

    url(r'^accounts/login/$',
       auth_views.login,
       {
           'template_name': 'registration/login.html',
           'authentication_form': LoginForm,

           },
       name='auth_login'),
    url(r'^accounts/logout/$', 'website.views.logout', name="logout"),
    url(r'^accounts/partner-login/$', auth_views.login, {
        'template_name': 'registration/partner_login.html',
        'authentication_form': LoginForm,
    }, name="partner_login"),
    url(r'^accounts/', include('website.registration_urls')),
    url(r'^accounts/logged-in/$', TemplateView.as_view(template_name="registration/logged_in.html"), name='logged_in'),

    url(r'^404test$', TemplateView.as_view(template_name="404.html"), name='404test'),



    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # mailchimp
    url(r'^subscribe/$', mc_subscribe, name='mc_subscribe'),



)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)
