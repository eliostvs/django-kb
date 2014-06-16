from __future__ import unicode_literals

from unittest import TestCase
from django.core.exceptions import ValidationError


class TestVisibilityValidator(TestCase):

    def test_visibility_choices(self):
        from knowledge.base.choices import VisibilityChoice

        self.assertRaises(ValidationError, VisibilityChoice.validator, 99)
        self.assertEqual(None, VisibilityChoice.validator(VisibilityChoice.Public))
        self.assertEqual(None, VisibilityChoice.validator(VisibilityChoice.Private))


class TestPublishValidator(TestCase):

    def test_publish_choices(self):
        from knowledge.base.choices import PublishChoice

        self.assertRaises(ValidationError, PublishChoice.validator, 99)
        self.assertEqual(None, PublishChoice.validator(PublishChoice.Draft))
        self.assertEqual(None, PublishChoice.validator(PublishChoice.Published))
