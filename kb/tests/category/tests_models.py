from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from kb.base import test
from kb.models import Category


class CategoryModelTestCase(test.PermalinkTestMixin,
                            test.TimeStampedMixin,
                            test.AuthorTestMixin,
                            test.SequenceAssertionMixin,
                            TestCase):

    model = Category

    def create_instance(self, **kwargs):
        return mommy.make('Category', **kwargs)

    def test_create_new_category(self):
        category = self.create_instance(description='foo')

        self.assertTrue(category.name)
        self.assertTrue(category.name, str(category))
        self.assertTrue(category.description, 'foo')

    def test_categories_with_published_articles(self):
        c1 = mommy.make_recipe('kb.tests.category_with_articles')
        c2 = mommy.make_recipe('kb.tests.category_without_articles')
        mommy.make_recipe('kb.tests.draft_article', category=c2)

        self.assertSeqEqual(Category.objects.all(), [c1, c2])
        self.assertSeqEqual(Category.objects.categories(), [c1])

    def test_absolute_url(self):
        category = self.create_instance(slug='spam')
        self.assertEqual(category.get_absolute_url(), '/category/spam/')

    def test_count_category_articles(self):
        category = mommy.make_recipe('kb.tests.category_with_articles')

        self.assertEqual(category.articles.count(), 2)
        self.assertEqual(Category.objects.categories()[0].count_articles, 1)

    def test_category_published_articles(self):
        category = mommy.make_recipe('kb.tests.category_without_articles')

        self.assertSeqEqual(category.published_articles(), [])

        articles = [mommy.make_recipe('kb.tests.published_article',
                                      title='Article %d' % _,
                                      category=category)
                    for _ in range(1, 5)]

        articles.reverse()
        mommy.make_recipe('kb.tests.draft_article', _quantity=2, category=category)

        self.assertSequenceEqual(category.published_articles(), articles)
        self.assertSequenceEqual(category.published_articles(1), [articles[0]])
