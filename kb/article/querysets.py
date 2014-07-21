from __future__ import unicode_literals

from django.db import models

from ..base import querysets


class ArticleQuerySet(querysets.AuthorableQueryset,
                      querysets.PublishableQueryset):

    def category(self, category):
        if isinstance(category, models.Model):
            qs = self.filter(category=category)

        elif category:
            qs = self.filter(category__slug=category)

        else:
            qs = self.filter()

        return qs
