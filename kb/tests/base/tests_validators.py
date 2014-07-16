from __future__ import unicode_literals

from unittest import TestCase
from django.core.exceptions import ValidationError


class TestPublishValidator(TestCase):

    def test_publish_choices(self):
        from kb.base.choices import PublishChoice

        self.assertRaises(ValidationError, PublishChoice.validator, 99)
        self.assertEqual(None, PublishChoice.validator(PublishChoice.Draft))
        self.assertEqual(None, PublishChoice.validator(PublishChoice.Published))
