from __future__ import unicode_literals

from model_mommy import mommy

from knowledge.base import choices
from knowledge.base.test import LoggedUser, ViewTestCase
from knowledge.models import Article


class HomepageBaseTestCase(ViewTestCase):

    from knowledge.views import Homepage

    view_class = Homepage
    view_name = 'knowledge:homepage'

    def setUp(self):
        self.public = mommy.make_recipe('knowledge.tests.public_category_with_articles')
        self.private = mommy.make_recipe('knowledge.tests.private_category_with_articles')

        for article in Article.objects.published():
            article.votes.add(token=article.id, rate=choices.VoteChoice.Upvote)


class TestHomepageAsAnonymousUser(HomepageBaseTestCase):

    def test_should_list_public_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['categories'], [self.public])

    def test_should_count_published_public_articles_in_public_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['categories'][0].articles_count(True), 1)

    def test_should_list_latest_published_public_articles_in_public_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['new_articles'].count(), 1)

    def test_should_list_top_viewed_published_public_articles_in_public_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['top_viewed_articles'].count(), 1)

    def test_should_list_top_rated_published_public_articles_in_public_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['top_rated_articles'].count(), 1)

    def test_should_have_a_search_form_on_context(self):
        from knowledge.forms import SimpleSearchForm

        response = self.get()

        self.assertEqual(response.context_data['search_form'], SimpleSearchForm)


class TestHomepageAsAuthenticatedUser(HomepageBaseTestCase):

    view_user = LoggedUser

    def test_should_list_all_categories(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['categories'], [self.public, self.private])

    def test_should_count_all_published_articles(self):
        response = self.get()
        category_list = response.context_data['categories']

        self.assertHttpOK(response)
        self.assertEqual(category_list[0].articles_count(), 2)
        self.assertEqual(category_list[1].articles_count(), 2)

    def test_should_list_latest_published_articles(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['new_articles'], Article.objects.published())

    def test_should_list_top_viewed_published_articles(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertSeqEqual(response.context_data['new_articles'], Article.objects.published())

    def test_should_list_top_rated_published_articles(self):
        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['top_viewed_articles'].count(), 4)
