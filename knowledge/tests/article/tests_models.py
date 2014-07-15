from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from knowledge.base import test
from knowledge.models import Article


class ArticleModelTest(test.PermalinkTestMixin,
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

    def test_related_articles(self):
        article = mommy.make_recipe('knowledge.tests.published_article')
        published = mommy.make_recipe('knowledge.tests.published_article')
        mommy.make_recipe('knowledge.tests.draft_article')

        for a in Article.objects.all():
            a.tags.add('Spam')

        self.assertEqual(Article.objects.count(), 3)
        self.assertSeqEqual(article.related(), [published])
