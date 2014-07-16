from __future__ import unicode_literals

from django.test import TestCase

from kb.forms import CategoryForm


class CategoryFormTestCase(TestCase):

    def test_with_empty_data_should_fail(self):
        form = CategoryForm({})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['slug'], ['This field is required.'])

    def test_form_initial_value(self):
        from django.utils.crypto import get_random_string

        form = CategoryForm()

        self.assertEqual(form.fields['slug'].initial, get_random_string)
