from __future__ import unicode_literals

from django.db import models

from .choices import PublishChoice


class AuthorableQueryset(models.query.QuerySet):

    def author(self, user):
        return self.filter(created_by__username=user)


class PublishableQueryset(models.query.QuerySet):

    def published(self):
        return self.filter(publish_state=PublishChoice.Published)

    def unpublished(self):
        return self.filter(publish_state=PublishChoice.Draft)
