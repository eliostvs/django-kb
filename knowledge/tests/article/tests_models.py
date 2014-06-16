from __future__ import unicode_literals

from django.test import TestCase
from django.utils.crypto import get_random_string

from model_mommy import mommy

from knowledge.base import choices, test
from knowledge.models import Article


class ArticleModelTest(test.VisibilityTestMixin,
                       test.PermalinkTestMixin,
                       test.TimeStampedMixin,
                       test.AuthorTestMixin,
                       test.PublishableTestMixin,
                       test.RefreshInstanceMixin,
                       test.SeqAssertionMixin,
                       TestCase):

    model = Article

    def create_instance(self, **kwargs):
        return mommy.make('Article', **kwargs)

    def test_create_new_article(self):
        article = self.create_instance()
        self.assertTrue(article.title)
        self.assertTrue(article.title, str(article))
        self.assertTrue(article.content)
        self.assertTrue(article.category)
        self.assertTrue(article.tags)

    def test_increase_hits(self):
        article = self.create_instance()
        modified = article.modified
        article.increase_hits()
        article = self.refresh(article)

        self.assertEqual(article.hits, 1)
        self.assertEqual(article.modified, modified)

    def test_absolute_url(self):
        article = self.create_instance(slug='eggs')
        self.assertEqual(article.get_absolute_url(), '/article/eggs/')


class ArticleModelComplexTestCase(test.SeqAssertionMixin,
                                  TestCase):

    def setUp(self):
        self.pb_category = mommy.make_recipe('knowledge.tests.public_category_with_articles')
        self.pv_category = mommy.make_recipe('knowledge.tests.private_category_with_articles')

    def test_related_articles(self):
        article = mommy.make_recipe('knowledge.tests.public_published_article')

        for a in Article.objects.all():
            a.tags.add('Spam')

        self.assertEqual(article.related().count(), 4)
        self.assertEqual(article.related(public_only=True).count(), 1)

    def test_top_articles(self):
        for a in Article.objects.published():
            a.votes.add(token=get_random_string(), rate=choices.VoteChoice.Upvote)

        for a in Article.objects.public():
            a.votes.add(token=get_random_string(), rate=choices.VoteChoice.Upvote)

        for a in Article.objects.unpublished():
            a.votes.add(token=get_random_string(), rate=choices.VoteChoice.Downvote)

        for a in Article.objects.private():
            a.votes.add(token=get_random_string(), rate=choices.VoteChoice.Downvote)

        self.assertEqual(Article.objects.top_rated().count(), 2)
        self.assertEqual(Article.objects.top_rated(public_only=True).count(), 1)
