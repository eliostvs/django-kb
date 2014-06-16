from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns(
    '',

    url(r'^$', views.Homepage.as_view(), name='homepage'),

    url(r'^category/', include('knowledge.category.urls')),

    url(r'^article/', include('knowledge.article.urls')),

    url(r'^search/', views.search_view, name='search'),

    url(r'^vote/', include('knowledge.vote.urls'))
)
