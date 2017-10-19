from django.conf.urls import patterns, include, url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from website.models import NewsItem
from website.views import LanguageListView, LanguageDetailView


urlpatterns = patterns('',
    url(r'^$', LanguageListView.as_view(
        queryset=NewsItem.objects.all(),
    ), name='newsitem_list'),
    url(r'^(?P<slug>[^/]+)/$', LanguageDetailView.as_view(
        queryset=NewsItem.objects.all(),
        ), name='newsitem_detail'),
)