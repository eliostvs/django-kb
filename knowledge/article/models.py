from __future__ import unicode_literals

from django.db import models
from django.db.models import F
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

from ..base import behaviours
from ..category.models import Category
from ..vote.utils import Votes
from .managers import ArticleManager


@python_2_unicode_compatible
class Article(behaviours.Visible,
              behaviours.Permalinkable,
              behaviours.Authorable,
              behaviours.Publishable,
              TimeStampedModel):

    title = models.CharField(_('Title'),
                             max_length=100)

    category = models.ForeignKey(Category,
                                 related_name='articles')

    content = models.TextField(_('Content'))

    hits = models.PositiveIntegerField(_('Hits'),
                                       default=0)

    objects = ArticleManager()
    votes = Votes()
    tags = TaggableManager()

    class Meta:
        app_label = 'knowledge'
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title

    def related(self, public_only=False):
        qs = Article.objects.get_articles(public_only)
        qs = qs.filter(tags__in=self.tags.all())
        qs = qs.exclude(pk=self.pk)

        return qs

    def increase_hits(self):
        Article.objects.filter(pk=self.pk).update(hits=F('hits') + 1)
