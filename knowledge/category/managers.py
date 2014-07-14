from __future__ import unicode_literals

from django.db import models

from model_utils.managers import PassThroughManagerMixin
from .querysets import CategoryQuerySet


class CategoryManager(PassThroughManagerMixin,
                      models.Manager):

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_categories(self, public_only=False):
        qs = self.exclude(parent__isnull=False)

        if public_only:
            qs = qs.public()

        return qs
