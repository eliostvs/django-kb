from __future__ import unicode_literals

from django.db import models

from model_utils.managers import PassThroughManagerMixin

from .querysets import ArticleQuerySet


class ArticleManager(PassThroughManagerMixin,
                     models.Manager):

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def top_viewed(self, num=5, category=None):
        qs = self.published().category(category)
        return qs.order_by('-hits')[:num]

    def top_new(self, num=5, category=None):
        qs = self.published().category(category)
        return qs.order_by('-created')[:num]

    def top_rated(self, num=5, category=None):
        qs = self.published().category(category)
        qs = qs.annotate(sum=models.Sum('ratings__rate'))
        qs = qs.filter(sum__gt=0)
        return qs.order_by('-sum')[:num]

    def tag(self, tag):
        qs = self.published()
        qs = qs.filter(tags__name__in=[tag])
        return qs.distinct()
