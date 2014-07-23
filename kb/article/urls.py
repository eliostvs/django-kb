from __future__ import unicode_literals

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    'kb.article.views',

    url(r'^(?P<slug>[\w-]+)/$',
        views.ArticleDetailView.as_view(),
        name='article_detail'),

    url(r'^add/$',
        views.ArticleCreateView.as_view(),
        name='article_add'),

    url(r'^$',
        views.ArticleListView.as_view(),
        name='article_list'),

    url(r'^delete/(?P<slug>[\w-]+)/$',
        views.ArticleDetailView.as_view(),
        name='article_delete'),

    url(r'^edit/(?P<slug>[\w-]+)/$',
        views.ArticleUpdateView.as_view(),
        name='article_edit'),

    url(r'tag/(?P<slug>[\w-]+)/$',
        views.TagListView.as_view(),
        name='search_tag')
)
