from __future__ import unicode_literals

from django.core.management import call_command

from model_mommy import mommy

from knowledge.base.test import SearchViewTestCase
from knowledge.views import search_view


class SearchCategoryBaseTestCase(SearchViewTestCase):

    view_function = search_view
    view_name = 'search'

    def setUp(self):
        self.category = mommy.make_recipe('knowledge.tests.category_with_articles')

        call_command('rebuild_index', interactive=False, verbosity=0)

    def test_search_title_should_list_only_public_categories(self):
        response = self.get({'q': 'category with articles title'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.category])

    def test_search_description_should_list_only_public_categories(self):
        response = self.get({'q': 'category with articles description'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.category])
