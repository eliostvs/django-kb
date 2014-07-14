from __future__ import unicode_literals

from django.db import models

from model_utils.managers import PassThroughManagerMixin
from .querysets import CategoryQuerySet


class CategoryManager(PassThroughManagerMixin,
                      models.Manager):

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_categories(self, exclude_subcategories=True):
        qs = self.filter()

        if exclude_subcategories:
            qs = self.exclude(parent__isnull=False)

        qs = qs.annotate(sum=models.Sum('articles'))
        qs = qs.filter(sum__gt=0)
        return qs
