from __future__ import unicode_literals

from django import forms

from haystack.forms import SearchForm

from .article.forms import ArticleForm
from .category.forms import CategoryForm


__all__ = [
    'ArticleForm',
    'CategoryForm',
    'SearchForm',
]


class SearchForm(SearchForm):
    q = forms.CharField(widget=forms.TextInput(attrs={'id': 'search-input'}),
                        required=False,
                        label='')
