from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from ..article.models import Article


def vote(request, slug, vote):
    article = get_object_or_404(Article.objects.published(), slug=slug)
    article.votes.add(request._secret_token, vote)

    if request.is_ajax():
        return HttpResponse('{"success": true}', content_type='application/json')

    return HttpResponsePermanentRedirect(article.get_absolute_url())
