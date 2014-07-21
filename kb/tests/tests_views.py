from __future__ import unicode_literals

from model_mommy import mommy

from kb.base.test import ViewTestCase


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
        self.assertTemplateUsed('kb/index.html')
        self.assertSeqEqual(response.context_data['categories'], [self.category])

    def test_have_a_search_form_on_context(self):
        from kb.forms import SearchForm

        response = self.get()

        self.assertEqual(response.context_data['search_form'], SearchForm)
