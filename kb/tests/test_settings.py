from __future__ import unicode_literals

from django.test import TestCase


class SettingsTestCase(TestCase):

    def setUp(self):
        from kb.settings import api_settings
        self.settings = api_settings

    def test_default_form_search_class(self):
        from kb.forms import SearchForm
        self.assertEqual(self.settings.DEFAULT_SEARCH_FORM_CLASS, SearchForm)

    def test_default_option(self):
        from kb.settings import APISettings
        api_settings = APISettings(None, {'FOO': 'BAR'}, None)

        self.assertEqual(api_settings.FOO, 'BAR')

    def test_non_exists_option_should_fail(self):
        self.assertRaises(AttributeError, getattr, self.settings, 'FOO')

    def test_import_non_exist_class_should_fail(self):
        from kb import settings
        api_settings = settings.APISettings({'DEFAULT_SEARCH_FORM_CLASS': 'path.to.non.exist.class'},
                                            settings.DEFAULTS, settings.IMPORT_STRINGS)
        self.assertRaises(ImportError, getattr, api_settings, 'DEFAULT_SEARCH_FORM_CLASS')
