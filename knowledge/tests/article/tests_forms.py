from __future__ import unicode_literals

from django.test import TestCase

from knowledge.forms import ArticleForm


class ArticleFormTestCase(TestCase):

    def test_with_empty_data_should_fail(self):
        form = ArticleForm({})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)
        self.assertEqual(form.errors['title'], ['This field is required.'])
        self.assertEqual(form.errors['content'], ['This field is required.'])
        self.assertEqual(form.errors['slug'], ['This field is required.'])
        self.assertEqual(form.errors['category'], ['This field is required.'])
        self.assertEqual(form.errors['visibility'], ['This field is required.'])
        self.assertEqual(form.errors['publish_state'], ['This field is required.'])

    def test_form_initial_value(self):
        from django.utils.crypto import get_random_string
        from knowledge.base import choices

        form = ArticleForm()

        self.assertEqual(form.fields['visibility'].initial, choices.VisibilityChoice.Public)
        self.assertEqual(form.fields['publish_state'].initial, choices.PublishChoice.Draft)
        self.assertEqual(form.fields['slug'].initial, get_random_string)
