from __future__ import unicode_literals


from ..base.search_indexes import BaseIndex
from .models import Category


class CategoryIndex(BaseIndex):

    def get_model(self):
        return Category
