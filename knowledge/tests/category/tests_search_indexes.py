from __future__ import unicode_literals

from django.core.management import call_command

from model_mommy import mommy

from knowledge.base.test import SearchViewTestCase
from knowledge.views import SearchView


class SearchCategoryBaseTestCase(SearchViewTestCase):

    view_function = SearchView
    view_name = 'search'

    def setUp(self):
        self.category = mommy.make_recipe('knowledge.tests.category_with_articles')
        mommy.make_recipe('knowledge.tests.category_without_articles')
        self.subcategory = mommy.make_recipe('knowledge.tests.subcategory', parent=self.category)
        mommy.make_recipe('knowledge.tests.published_article', category=self.subcategory)

        call_command('rebuild_index', interactive=False, verbosity=0)

    def test_search_title(self):
        response = self.get({'q': 'category with articles title'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.category])

    def test_search_description(self):
        response = self.get({'q': 'category with articles description'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.category])

    def test_search_category_without_articles(self):
        response = self.get({'q': 'category without articles title'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertFalse([o.object for o in object_list])

    def test_search_subcategory(self):
        response = self.get({'q': 'subcategory title'})
        object_list = response.context['page'].object_list

        self.assertHttpOK(response)
        self.assertEqual([o.object for o in object_list], [self.subcategory])
