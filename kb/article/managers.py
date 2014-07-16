from __future__ import unicode_literals

from django.db import models

from model_utils.managers import PassThroughManagerMixin

from .querysets import ArticleQuerySet


class ArticleManager(PassThroughManagerMixin,
                     models.Manager):

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def top_viewed(self):
        return self.published().order_by('-hits')[:5]

    def new(self):
        return self.published().order_by('-created')[:5]

    def top_rated(self):
        qs = self.published()
        qs = qs.annotate(sum=models.Sum('ratings__rate'))
        qs = qs.filter(sum__gt=0)
        return qs.order_by('-sum')[:5]