from django.conf.urls import patterns, include, url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from website.models import Event
from website.views import LanguageListView, LanguageDetailView, EventsListView
from datetime import datetime


urlpatterns = patterns('',
    url(r'^$', EventsListView.as_view(
        queryset=Event.objects.filter(end_date__gt=datetime.now()),
        ), name='event_list'),
    url(r'^(?P<slug>[^/]+)/$', LanguageDetailView.as_view(
        queryset=Event.objects.all(),
        ), name='event_detail'),
)