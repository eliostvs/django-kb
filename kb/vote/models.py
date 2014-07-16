from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils.managers import PassThroughManager

from ..base.choices import VoteChoice
from ..base.querysets import AuthorableQueryset


@python_2_unicode_compatible
class Vote(TimeStampedModel,
           models.Model):

    token = models.CharField(_('Token'),
                             max_length=50)

    rate = models.SmallIntegerField(_('Rate'),
                                    choices=VoteChoice.choices,
                                    validators=[VoteChoice.validator],
                                    db_index=True)

    article = models.ForeignKey('Article',
                                related_name='ratings')

    objects = PassThroughManager.for_queryset_class(AuthorableQueryset)()

    def __str__(self):
        return '%s from %s on %s' % (self.get_rate_display(), self.token, self.article)

    class Meta:
        app_label = 'kb'
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = (('token', 'article'),)
