from __future__ import unicode_literals

from hashlib import md5

import six

from knowledge.base.choices import VoteChoice
from knowledge.base.test import ViewTestCase
from model_mommy import mommy


class VoteViewTestCase(ViewTestCase):
    from knowledge.vote.views import vote

    view_function = vote
    view_name = 'knowledge:vote'

    def setUp(self):
        from knowledge.middleware import KnowledgeMiddleware

        self.vote = VoteChoice.Upvote
        self.middleware = KnowledgeMiddleware()

    def view(self, request):
        self.middleware.process_request(request)
        return super(VoteViewTestCase, self).view(request)

    def test_view_upvote(self):
        article = mommy.make_recipe('knowledge.tests.published_article', slug='eggs')
        response = self.get()

        self.assertRedirectTo(response, '/article/eggs/')
        self.assertEqual(article.votes.total(), 1)
        self.assertEqual(article.votes.upvotes(), 1)
        self.assertEqual(article.votes.downvotes(), 0)

    def test_view_downvote(self):
        article = mommy.make_recipe('knowledge.tests.published_article', slug='eggs')
        self.vote = VoteChoice.Downvote
        response = self.get()

        self.assertRedirectTo(response, '/article/eggs/')
        self.assertEqual(article.votes.total(), 1)
        self.assertEqual(article.votes.upvotes(), 0)
        self.assertEqual(article.votes.downvotes(), 1)

        token = md5('127.0.0.1'.encode('utf-8')).hexdigest()
        self.assertEqual(article.votes.get(pk=1).token, token)

    def test_view_should_raise_404(self):
        from django.http import Http404

        mommy.make_recipe('knowledge.tests.draft_article', slug='eggs')

        self.assertRaises(Http404, self.get)

    def test_ajax_request(self):
        mommy.make_recipe('knowledge.tests.published_article', slug='eggs')
        response = self.get(HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.content, six.b('{"success": true}'))

    def get_view_args(self):
        return 'eggs', self.vote
