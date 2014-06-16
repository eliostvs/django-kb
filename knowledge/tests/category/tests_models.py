from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from knowledge.base import test


class CategoryModelTestCase(test.VisibilityTestMixin,
                            test.PermalinkTestMixin,
                            test.TimeStampedMixin,
                            test.AuthorTestMixin,
                            test.SeqAssertionMixin,
                            TestCase):

    from knowledge.models import Category

    model = Category

    def create_instance(self, **kwargs):
        return mommy.make('Category', **kwargs)

    def test_create_new_category(self):
        category = self.create_instance()

        self.assertTrue(category.name)
        self.assertTrue(category.name, str(category))

    def test_subcategory_list(self):
        parent = self.create_instance()

        public = mommy.make_recipe('knowledge.tests.public_category',
                                   parent=parent)

        private = mommy.make_recipe('knowledge.tests.private_category',
                                    parent=parent)

        self.assertSeqEqual(parent.subcategories(), [public, private])

        self.assertSeqEqual(parent.subcategories(public_only=True), [public])

    def test_absolute_url(self):
        category = self.create_instance(slug='spam')
        self.assertEqual(category.get_absolute_url(), '/category/spam/')
