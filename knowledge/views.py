from __future__ import unicode_literals

from django.views.generic import TemplateView

from haystack.views import SearchView

from .article.views import (ArticleCreateView, ArticleDeleteView,
                            ArticleDetailView, ArticleListView,
                            ArticleUpdateView)
from .base.views import AddSearchFormToContextMixin
from .category.views import (CategoryCreateView, CategoryDeleteView,
                             CategoryDetailView, CategoryListView,
                             CategoryUpdateView)
from .settings import api_settings
from .models import Article, Category

__all__ = [
    'ArticleListView',
    'ArticleDetailView',
    'ArticleCreateView',
    'ArticleDeleteView',
    'ArticleUpdateView',
    'CategoryListView',
    'CategoryDetailView',
    'CategoryCreateView',
    'CategoryUpdateView',
    'CategoryDeleteView',
    'HomepageView',
    'SearchView',
]


class HomepageView(AddSearchFormToContextMixin,
                   TemplateView):

    template_name = 'knowledge/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.categories()
        context['top_new'] = Article.objects.new()
        context['top_viewed'] = Article.objects.top_viewed()
        context['top_rated'] = Article.objects.top_rated()
        return context


class SearchView(SearchView):
    form = api_settings.DEFAULT_SEARCH_FORM_CLASS

    def extra_context(self):
        return {'search_form': api_settings.DEFAULT_SEARCH_FORM_CLASS}
