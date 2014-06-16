from __future__ import unicode_literals

from django.test import TestCase

from knowledge.forms import CategoryForm


class CategoryFormTestCase(TestCase):

    def test_with_empty_data_should_fail(self):
        form = CategoryForm({})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['slug'], ['This field is required.'])
        self.assertEqual(form.errors['visibility'], ['This field is required.'])

    def test_with_a_invalid_visibility_should_fail(self):
        form = CategoryForm({
            'name': 'eggs',
            'visibility': 88,
            'slug': 'eggs',
        })

        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['visibility'],
                         ['Select a valid choice. 88 is not one of the available choices.'])

    def test_form_initial_value(self):
        from django.utils.crypto import get_random_string
        from knowledge.base.choices import VisibilityChoice

        form = CategoryForm()

        self.assertEqual(form.fields['visibility'].initial, VisibilityChoice.Public)
        self.assertEqual(form.fields['slug'].initial, get_random_string)
