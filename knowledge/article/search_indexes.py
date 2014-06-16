from __future__ import unicode_literals

from ..base.search_indexes import BaseIndex
from ..base.choices import VisibilityChoice
from .models import Article


class ArticleIndex(BaseIndex):

    def get_model(self):
        return Article

    def prepare_visibility(self, obj):
        if obj.category.visibility == VisibilityChoice.Private:
            return VisibilityChoice.Private

        return obj.visibility

    def index_queryset(self, using=None):
        qs = super(ArticleIndex, self).index_queryset(using)
        return qs.published()
