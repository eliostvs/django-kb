from __future__ import unicode_literals

from hashlib import md5


class KnowledgeMiddleware(object):

    def process_request(self, request):
        request._secret_token = self.generate_token(request)

    def generate_token(self, request):
        if request.user.is_authenticated():
            return request.user.username

        s = ''.join((request.META['REMOTE_ADDR'], request.META.get('HTTP_USER_AGENT', '')))
        return md5(s.encode('utf-8')).hexdigest()
