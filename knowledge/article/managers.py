from __future__ import unicode_literals

from django.db import models

from model_utils.managers import PassThroughManagerMixin

from ..base.choices import VisibilityChoice
from .querysets import ArticleQuerySet


class ArticleManager(PassThroughManagerMixin,
                     models.Manager):

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def top_viewed(self, public_only=False):
        return self.get_articles(public_only).order_by('-hits')[:5]

    def new(self, public_only=False):
        return self.get_articles(public_only).order_by('-created')[:5]

    def top_rated(self, public_only=False):
        qs = self.get_articles(public_only)
        qs = qs.annotate(sum=models.Sum('ratings__rate'))
        qs = qs.filter(sum__gt=0)
        return qs.order_by('-sum')[:5]

    def get_articles(self, public_only=False):
        qs = self.published()

        if public_only:
            qs = qs.filter(category__visibility=VisibilityChoice.Public,
                           visibility=VisibilityChoice.Public)

        return qs
