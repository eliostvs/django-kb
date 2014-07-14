from __future__ import unicode_literals

import datetime

from django.http import Http404

from django.utils.timezone import utc
from model_mommy import mommy

from knowledge.base.test import ViewTestCase
from knowledge.models import Article


class TestCategoryFeed(ViewTestCase):

    view_name = 'knowledge:category_feed'
    view_kwargs = {'slug': 'spam'}

    def view(self, request):
        from knowledge.feeds import CategoryFeed

        return CategoryFeed()(request, slug='spam')

    def test_with_private_category_should_fail(self):
        mommy.make_recipe('knowledge.tests.private_category', slug='spam')

        self.assertRaises(Http404, self.get)

    def test_view(self):
        category = mommy.make_recipe('knowledge.tests.public_category_with_articles',
                                     slug='spam')

        mommy.make_recipe('knowledge.tests.public_published_article',
                          created=datetime.datetime(2013, 5, 27, tzinfo=utc),
                          created_by=mommy.make('User', username='Guido'),
                          category=category)

        for article in Article.objects.all():
            article.tags.add('Spam', 'Eggs')

        response = self.get()

        self.assertHttpOK(response)
        self.assertContains(response, '<title>Public Category Name</title>')
        self.assertContains(response, '<description>Public Category Description</description>')

        self.assertContains(response, '<title>Title Public and Published</title>')
        self.assertContains(response, '<description>Content Public and Published</description>')
        self.assertContains(response, '<pubDate>Mon, 27 May 2013 00:00:00 +0000</pubDate>')
        self.assertContains(response, '<category>Spam</category>')
        self.assertContains(response, '<category>Eggs</category>')
        self.assertContains(response, '>Guido</dc:creator>')

        self.assertNotContains(response, '<title>Title Private and Published</title>')
        self.assertNotContains(response, '<title>Title Public and Draft</title>')
        self.assertNotContains(response, '<title>Title Private and Draft</title>')
