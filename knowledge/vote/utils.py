from __future__ import unicode_literals

from .models import Vote
from ..base.choices import VoteChoice


class Votes(object):

    def contribute_to_class(self, cls, name):
        setattr(cls, name, _VoteDescriptor())


class _VoteDescriptor(object):

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.create_manager(instance, Vote._base_manager.__class__)

    def create_manager(self, instance, superclass):

        class VoteManager(superclass):

            def get_queryset(self):
                qs = super(VoteManager, self).get_queryset()
                return qs.filter(article=instance)

            def add(self, token, rate):
                obj, new = self.get_or_create(token=token,
                                              article=instance,
                                              defaults={'rate': rate})

                if not new:
                    obj.rate = rate
                    obj.save()

            def total(self):
                return self.filter().count()

            def downvotes(self):
                return self.filter(rate=VoteChoice.Downvote).count()

            def upvotes(self):
                return self.filter(rate=VoteChoice.Upvote).count()

        manager = VoteManager()
        manager.model = Vote
        return manager
