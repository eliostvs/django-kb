from __future__ import unicode_literals


from django.test import TestCase


class SettingsTestCase(TestCase):

    def setUp(self):
        from knowledge.settings import api_settings
        self.settings = api_settings

    def test_default_form_search_class(self):
        from knowledge.forms import SearchForm
        self.assertEqual(self.settings.DEFAULT_SEARCH_FORM_CLASS, SearchForm)
