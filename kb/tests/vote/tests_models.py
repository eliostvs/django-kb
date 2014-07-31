from __future__ import unicode_literals

from django.test import TestCase
from model_mommy import mommy

from kb.base import choices
from kb.tests import test


class VoteManagerTestCase(test.TimeStampedMixin,
                          test.SequenceAssertionMixin,
                          TestCase):

    def create_instance(self, **kwargs):
        return mommy.make_recipe('kb.tests.vote', **kwargs)

    def create_article(self, **kwargs):
        return mommy.make_recipe('kb.tests.draft_article')

    def test_create_new_vote(self):
        article = self.create_article()
        instance = self.create_instance(rate=choices.VoteChoice.Upvote,
                                        article=article)

        self.assertIn(instance.rate, choices.VoteChoice.values)
        self.assertTrue(instance.token)
        self.assertEqual(instance.article, article)
        self.assertEqual('Upvote from %s on Draft Article Title' % instance.token, str(instance))

    def test_model_constraint(self):
        from django.db import IntegrityError
        article = self.create_article()

        self.create_instance(article=article, token='a')
        self.assertRaises(IntegrityError, self.create_instance, article=article, token='a')

    def test_total_votes(self):
        article = self.create_article()
        article.votes.add('a', choices.VoteChoice.Upvote)

        self.assertEqual(article.votes.total(), 1)

        article.votes.add('b', choices.VoteChoice.Downvote)

        self.assertEqual(article.votes.total(), 2)

    def test_change_vote(self):
        article = self.create_article()
        article.votes.add('a', choices.VoteChoice.Upvote)

        self.assertEqual(article.votes.upvotes(), 1)
        self.assertEqual(article.votes.downvotes(), 0)
        self.assertEqual(article.votes.total(), 1)

        article.votes.add('a', choices.VoteChoice.Downvote)

        self.assertEqual(article.votes.upvotes(), 0)
        self.assertEqual(article.votes.downvotes(), 1)
        self.assertEqual(article.votes.total(), 1)
