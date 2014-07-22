from __future__ import unicode_literals

import datetime

from django.test import TestCase

from model_mommy import mommy


class TemplateTagsTestCase(TestCase):

    def test_tag_top_new_articles(self):
        from kb.templatetags.kbtags import top_new_articles

        articles = []

        for i in range(1, 7):
            created = datetime.date.today() + datetime.timedelta(i)
            articles.append(mommy.make_recipe('kb.tests.published_article',
                            created=created))

        articles.reverse()

        mommy.make_recipe('kb.tests.draft_article')

        self.assertSequenceEqual(top_new_articles(), articles[:5])
        self.assertSequenceEqual(top_new_articles(1), [articles[0]])

    def test_tag_top_viewed_articles(self):
        from kb.templatetags.kbtags import top_viewed_articles

        articles = []
        for i in range(1, 7):
            articles.append(mommy.make_recipe('kb.tests.published_article', hits=i))

        articles.reverse()

        mommy.make_recipe('kb.tests.draft_article')

        self.assertSequenceEqual(top_viewed_articles(), articles[:5])
        self.assertSequenceEqual(top_viewed_articles(1), [articles[0]])

    def test_tag_top_rated_articles(self):
        from kb.templatetags.kbtags import top_rated_articles
        from kb.base.choices import VoteChoice

        articles = []
        for a in range(1, 7):
            article = mommy.make_recipe('kb.tests.published_article')
            for v in range(a):
                article.votes.add('%d:%d' % (article.id, v), VoteChoice.Upvote)

            articles.append(article)

        articles.reverse()

        mommy.make_recipe('kb.tests.draft_article')

        self.assertSequenceEqual(top_rated_articles(), articles[:5])
        self.assertSequenceEqual(top_rated_articles(1), [articles[0]])

    def test_tags_filtering_by_category(self):
        from kb.base.choices import VoteChoice
        from kb.models import Article

        c1 = mommy.make_recipe('kb.tests.category_without_articles')
        a1 = mommy.make_recipe('kb.tests.published_article', category=c1)
        a1.votes.add('a1', VoteChoice.Upvote)

        c2 = mommy.make_recipe('kb.tests.category_without_articles')
        a2 = mommy.make_recipe('kb.tests.published_article', category=c2)
        a2.votes.add('a2', VoteChoice.Upvote)

        self.assertEqual(Article.objects.count(), 2)
        self.assertSequenceEqual(Article.objects.top_rated(category=c1), [a1])
        self.assertSequenceEqual(Article.objects.top_rated(category=c2), [a2])

        self.assertSequenceEqual(Article.objects.top_viewed(category=c1), [a1])
        self.assertSequenceEqual(Article.objects.top_viewed(category=c2), [a2])
