from __future__ import unicode_literals

from django.db import models

from model_utils.managers import PassThroughManagerMixin
from .querysets import CategoryQuerySet
from ..base.choices import PublishChoice


class CategoryManager(PassThroughManagerMixin,
                      models.Manager):

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def available(self):
        qs = self.filter(articles__publish_state=PublishChoice.Published)
        qs = qs.annotate(models.Count('articles'))
        qs = qs.filter(articles__count__gt=0)
        return qs.select_related()
