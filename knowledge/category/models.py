from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from ..base import behaviours
from .managers import CategoryManager


@python_2_unicode_compatible
class Category(behaviours.Permalinkable,
               behaviours.Authorable,
               TimeStampedModel):

    name = models.CharField(_('Name'),
                            max_length=100)

    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='subcategories')

    description = models.TextField(_('Description'),
                                   null=True,
                                   blank=True)

    objects = CategoryManager()

    class Meta:
        app_label = 'knowledge'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def count(self):
        return self.articles.published().count()
