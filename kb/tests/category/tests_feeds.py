from __future__ import unicode_literals

import datetime

from django.http import Http404

from django.utils.timezone import utc
from model_mommy import mommy

from kb.base.test import ViewTestCase
from kb.models import Article


class TestCategoryFeed(ViewTestCase):

    view_name = 'kb:category_feed'
    view_kwargs = {'slug': 'spam'}

    def view(self, request):
        from kb.feeds import CategoryFeed

        return CategoryFeed()(request, slug='spam')

    def test_with_category_without_articles_should_fail(self):
        mommy.make_recipe('kb.tests.category_without_articles', slug='spam')
        self.assertRaises(Http404, self.get)

    def test_view(self):
        category = mommy.make_recipe('kb.tests.category_with_articles', slug='spam')

        mommy.make_recipe('kb.tests.published_article',
                          created=datetime.datetime(2013, 5, 27, tzinfo=utc),
                          created_by=mommy.make('User', username='Guido'),
                          category=category)

        for article in Article.objects.all():
            article.tags.add('Spam', 'Eggs')

        response = self.get()

        self.assertHttpOK(response)
        self.assertContains(response, '<title>Category With Articles Title</title>')
        self.assertContains(response, '<description>Category With Articles Description</description>')

        self.assertContains(response, '<title>Published Article Title</title>')
        self.assertContains(response, '<description>&lt;p&gt;Published Article Content&lt;/p&gt;</description>')
        self.assertContains(response, '<pubDate>Mon, 27 May 2013 00:00:00 +0000</pubDate>')
        self.assertContains(response, '<category>Spam</category>')
        self.assertContains(response, '<category>Eggs</category>')
        self.assertContains(response, '>Guido</dc:creator>')

        self.assertNotContains(response, '<title>Draft Article Title</title>')
        self.assertNotContains(response, '<title>Draft Article Content</title>')
