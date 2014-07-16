from __future__ import unicode_literals

from model_mommy import mommy

from kb.base.test import ViewTestCase
from kb.models import Article


class HomepageTestCase(ViewTestCase):

    from kb.views import HomepageView

    view_class = HomepageView
    view_name = 'kb:homepage'

    def setUp(self):
        self.category = mommy.make_recipe('kb.tests.category_with_articles')
        mommy.make_recipe('kb.tests.category_without_articles')

    def test_category_list(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['categories'], [self.category])

    def test_have_a_search_form_on_context(self):
        from kb.forms import SearchForm

        response = self.get()

        self.assertEqual(response.context_data['search_form'], SearchForm)

    def test_latest_articles(self):
        articles = mommy.make_recipe('kb.tests.published_article', _quantity=5)
        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(Article.objects.count(), 7)
        self.assertSeqEqual(response.context_data['top_new'], articles)

    def test_top_viewed_articles(self):
        articles = mommy.make_recipe('kb.tests.published_article', _quantity=5)

        for n, a in enumerate(articles):
            a.hits = n + 1
            a.save()

        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(Article.objects.count(), 7)
        self.assertListEqual(list(response.context_data['top_viewed']), list(reversed(articles)))

    def test_top_rated_articles(self):
        from kb.base.choices import VoteChoice

        d = mommy.make_recipe('kb.tests.published_article', title='d')
        d.votes.add('d1', VoteChoice.Downvote)

        b = mommy.make_recipe('kb.tests.published_article', title='b')
        b.votes.add('b1', VoteChoice.Upvote)
        b.votes.add('b2', VoteChoice.Upvote)

        c = mommy.make_recipe('kb.tests.published_article', title='c')
        c.votes.add('c1', VoteChoice.Upvote)

        a = mommy.make_recipe('kb.tests.published_article', title='a')
        a.votes.add('a1', VoteChoice.Upvote)
        a.votes.add('a2', VoteChoice.Upvote)
        a.votes.add('a3', VoteChoice.Upvote)

        response = self.get()

        self.assertHttpOK(response)
        self.assertListEqual(list(response.context_data['top_rated']), [a, b, c])
