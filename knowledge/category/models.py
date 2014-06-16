from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel

from ..base import behaviours
from .querysets import CategoryQueryset


@python_2_unicode_compatible
class Category(behaviours.Permalinkable,
               behaviours.Visible,
               behaviours.Authorable,
               TimeStampedModel):

    name = models.CharField(_('Name'),
                            max_length=100)

    parent = models.ForeignKey('self',
                               null=True,
                               blank=True)

    description = models.TextField(_('Description'),
                                   null=True,
                                   blank=True)

    objects = PassThroughManager.for_queryset_class(CategoryQueryset)()

    class Meta:
        app_label = 'knowledge'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def subcategories(self, public_only=False):
        qs = self.category_set.all()

        if public_only:
            qs = qs.public()

        return qs

    def articles_count(self, public_only=False):
        qs = self.articles.published()

        if public_only:
            qs = qs.public()

        return qs.count()
