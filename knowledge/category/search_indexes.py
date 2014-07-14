from __future__ import unicode_literals


from ..base.search_indexes import BaseIndex
from .models import Category


class CategoryIndex(BaseIndex):

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return Category.objects.get_categories(exclude_subcategories=False)
