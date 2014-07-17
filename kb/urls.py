from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from . import views
from .settings import api_settings

urlpatterns = patterns(
    '',

    url(r'^$', views.HomepageView.as_view(), name='homepage'),

    url(r'^category/', include('kb.category.urls')),

    url(r'^article/', include('kb.article.urls')),

    url(r'^search/', api_settings.DEFAULT_SEARCH_VIEW_CLASS, name='search'),

    url(r'^vote/', include('kb.vote.urls'))
)
