from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem


class BaseChoice(DjangoChoices):

    @classmethod
    def validator(cls, value):
        if value not in cls.values:
            raise ValidationError('Select a valid choice. %(value)s is not '
                                  'one of the available choices.')


class PublishChoice(BaseChoice):
    Draft = ChoiceItem(1, _('Draft'))
    Published = ChoiceItem(2, _('Publish'))


class VoteChoice(BaseChoice):
    Upvote = ChoiceItem(1, _('Upvote'))
    Downvote = ChoiceItem(-1, _('Downvote'))
