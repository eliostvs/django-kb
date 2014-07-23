from __future__ import unicode_literals

from django.views.generic import TemplateView
from haystack.views import SearchView

from .article.views import (ArticleCreateView, ArticleDeleteView,
                            ArticleDetailView, ArticleListView,
                            ArticleUpdateView, TagListView)
from .base.views import AddSearchFormToContextMixin
from .category.views import (CategoryCreateView, CategoryDeleteView,
                             CategoryDetailView, CategoryListView,
                             CategoryUpdateView)
from .models import Category
from .settings import api_settings

__all__ = [
    'ArticleCreateView',
    'ArticleDeleteView',
    'ArticleDetailView',
    'ArticleListView',
    'ArticleUpdateView',
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryDetailView',
    'CategoryListView',
    'CategoryUpdateView',
    'HomepageView',
    'SearchView',
    'TagListView',
]


class HomepageView(AddSearchFormToContextMixin,
                   TemplateView):

    template_name = 'kb/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.categories()
        return context


SearchView = SearchView(form_class=api_settings.DEFAULT_SEARCH_FORM_CLASS)
