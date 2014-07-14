from __future__ import unicode_literals

from model_mommy import mommy

from knowledge.base import choices
from knowledge.base.test import ViewTestCase
from knowledge.models import Article


class HomepageTestCase(ViewTestCase):

    from knowledge.views import Homepage

    view_class = Homepage
    view_name = 'knowledge:homepage'

    def setUp(self):
        self.category = mommy.make_recipe('knowledge.tests.category_with_articles')

        for article in Article.objects.published():
            article.votes.add(token=article.id, rate=choices.VoteChoice.Upvote)

    def test_list_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['categories'], [self.category])

    def test_have_a_search_form_on_context(self):
        from knowledge.forms import SimpleSearchForm

        response = self.get()

        self.assertEqual(response.context_data['search_form'], SimpleSearchForm)

    def test_count_published_articles(self):
        response = self.get()
        category_list = response.context_data['categories']

        self.assertHttpOK(response)
        self.assertEqual(category_list[0].articles_count(), 1)

    def test_list_latest_published_articles(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['new_articles'], Article.objects.published())

    def test_list_top_viewed_published_articles(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['new_articles'], Article.objects.published())

    def test_list_top_rated_published_articles(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['top_viewed_articles'], Article.objects.published())
