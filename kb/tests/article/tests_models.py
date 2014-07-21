from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from kb.base import test
from kb.models import Article


class ArticleModelTest(test.PermalinkTestMixin,
                       test.TimeStampedMixin,
                       test.AuthorTestMixin,
                       test.PublishableTestMixin,
                       test.RefreshInstanceMixin,
                       test.SequenceAssertionMixin,
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
        article = mommy.make_recipe('kb.tests.published_article')
        published = mommy.make_recipe('kb.tests.published_article')
        mommy.make_recipe('kb.tests.draft_article')

        for a in Article.objects.all():
            a.tags.add('Spam')

        self.assertEqual(Article.objects.count(), 3)
        self.assertSeqEqual(article.related(), [published])

    def test_top_new_articles(self):
        articles = mommy.make_recipe('kb.tests.published_article', _quantity=6)
        articles.reverse()
        mommy.make_recipe('kb.tests.draft_article')

        self.assertEqual(Article.objects.count(), 7)
        self.assertSequenceEqual(Article.objects.new(), articles[:5])
        self.assertSequenceEqual(Article.objects.new(1), [articles[0]])

    def test_top_rated_articles(self):
        from kb.base.choices import VoteChoice

        a = mommy.make_recipe('kb.tests.published_article', title='a')
        a.votes.add('a1', VoteChoice.Upvote)
        a.votes.add('a2', VoteChoice.Upvote)
        a.votes.add('a3', VoteChoice.Upvote)

        b = mommy.make_recipe('kb.tests.published_article', title='b')
        b.votes.add('b1', VoteChoice.Upvote)
        b.votes.add('b2', VoteChoice.Upvote)

        c = mommy.make_recipe('kb.tests.published_article', title='c')
        c.votes.add('c1', VoteChoice.Upvote)

        d = mommy.make_recipe('kb.tests.published_article', title='d')
        d.votes.add('d1', VoteChoice.Downvote)

        e = mommy.make_recipe('kb.tests.draft_article', title='e')
        e.votes.add('e1', VoteChoice.Upvote)
        e.votes.add('e2', VoteChoice.Upvote)
        e.votes.add('e3', VoteChoice.Upvote)
        e.votes.add('e4', VoteChoice.Upvote)

        self.assertSequenceEqual(Article.objects.top_rated(), [a, b, c])
