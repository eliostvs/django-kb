from __future__ import unicode_literals

from model_mommy import mommy

from knowledge.base.test import LoggedUser, SearchViewTestCase
from knowledge.views import search_view


class SearchCategoryBaseTestCase(SearchViewTestCase):

    view_function = search_view
    view_name = 'search'

    def make_instance(self):
        self.public = mommy.make_recipe('knowledge.tests.public_category')
        self.private = mommy.make_recipe('knowledge.tests.private_category')


class SearchCategoryTestCaseAsAnonymousUser(SearchCategoryBaseTestCase):

    def test_search_title_should_list_only_public_categories(self):
        response = self.get({'q': 'public'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.public])

    def test_search_description_should_list_only_public_categories(self):
        response = self.get({'q': 'description'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.public])


class SearchCategoryTestCaseAsAuthenticatedUser(SearchCategoryBaseTestCase):

    view_user = LoggedUser

    def test_search_title_should_list_public_and_private_categories(self):
        response = self.get({'q': 'name'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.public, self.private])

    def test_search_description_should_list_public_and_private_categories(self):
        response = self.get({'q': 'description'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.public, self.private])
