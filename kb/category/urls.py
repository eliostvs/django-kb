from __future__ import unicode_literals

from django.conf.urls import patterns, url

from . import views
from .feeds import CategoryFeed

urlpatterns = patterns(
    'kb.category.views',

    url(r'^(?P<slug>[\w-]+)/$',
        views.CategoryDetailView.as_view(),
        name='category_detail'),

    url(r'^add/$',
        views.CategoryCreateView.as_view(),
        name='category_add'),

    url(r'^$',
        views.CategoryListView.as_view(),
        name='category_list'),

    url(r'^edit/(?P<slug>[\w-]+)/$',
        views.CategoryUpdateView.as_view(),
        name='category_edit'),

    url(r'^delete/(?P<slug>[\w-]+)/$',
        views.CategoryDeleteView.as_view(),
        name='category_delete'),

    url(r'^(?P<slug>[\w-]+)/rss/$',
        CategoryFeed(),
        name='category_feed'),
)
