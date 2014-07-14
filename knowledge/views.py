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
from .forms import SimpleSearchForm
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
    'Homepage',
    'search_view',
]


class Homepage(AddSearchFormToContextMixin,
               TemplateView):

    template_name = 'knowledge/index.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.categories()
        context['new_articles'] = Article.objects.new()
        context['top_viewed_articles'] = Article.objects.top_viewed()
        context['top_rated_articles'] = Article.objects.top_rated()
        return context

search_view = SearchView(form_class=SimpleSearchForm)
