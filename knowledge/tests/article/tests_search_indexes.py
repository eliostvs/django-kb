from __future__ import unicode_literals

from model_mommy import mommy

from knowledge.base.test import LoggedUser, SearchViewTestCase
from knowledge.models import Article
from knowledge.views import search_view


class SearchArticleBaseTestCase(SearchViewTestCase):

    view_function = search_view
    view_name = 'search'

    def make_instance(self):
        mommy.make_recipe('knowledge.tests.public_category_with_articles')
        mommy.make_recipe('knowledge.tests.private_category_with_articles')

        for article in Article.objects.all():
            article.tags.add('bar')


class SearchArticleAsAnonymousUserTestCase(SearchArticleBaseTestCase):

    def test_search_title_should_list_only_public_articles_in_public_categories(self):
        response = self.get({'q': 'title'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertSeqEqual([a.object for a in object_list], Article.objects.get_articles(public_only=True))

    def test_search_content_should_list_only_public_articles_in_public_categories(self):
        response = self.get({'q': 'content'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertSeqEqual([a.object for a in object_list], Article.objects.get_articles(public_only=True))

    def test_search_tag_should_list_only_public_articles_in_public_categories(self):
        response = self.get({'q': 'bar'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertSeqEqual([a.object for a in object_list], Article.objects.get_articles(public_only=True))


class SearchArticleAsAuthenticatedUserTestCase(SearchArticleBaseTestCase):

    view_user = LoggedUser

    def test_search_title_should_list_all_articles_in_all_categories(self):
        response = self.get({'q': 'title'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertSeqEqual([a.object for a in object_list], Article.objects.published())

    def test_search_content_should_list_published_articles(self):
        response = self.get({'q': 'content'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertSeqEqual([a.object for a in object_list], Article.objects.published())

    def test_search_tag_should_list_all_published_articles(self):
        response = self.get({'q': 'bar'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertSeqEqual([a.object for a in object_list], Article.objects.published())
