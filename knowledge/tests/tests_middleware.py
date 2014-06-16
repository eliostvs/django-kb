from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase

from knowledge.base.test import LoggedUser


class KnowledgeMiddleareTestCase(TestCase):

    def setUp(self):
        from knowledge.middleware import KnowledgeMiddleware
        self.middleware = KnowledgeMiddleware()
        self.request = HttpRequest()
        self.request.META['REMOTE_ADDR'] = '127.0.0.1'
        self.request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (X11; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0'

    def test_anonymous_user(self):
        from hashlib import md5

        self.request.user = AnonymousUser()
        self.middleware.process_request(self.request)
        s = '127.0.0.1Mozilla/5.0 (X11; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0'
        token = md5(s.encode('utf-8')).hexdigest()

        self.assertEqual(self.request._secret_token, token)

    def test_logged_user(self):
        self.request.user = LoggedUser
        self.middleware.process_request(self.request)

        self.assertEqual(self.request._secret_token, 'Logged User')
