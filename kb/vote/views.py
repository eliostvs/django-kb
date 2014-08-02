from __future__ import unicode_literals

import json

from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from ..article.models import Article


def vote(request, slug, vote):
    article = get_object_or_404(Article.objects.published(), slug=slug)
    article.votes.add(request._secret_token, vote)

    if request.is_ajax():
        response = {'response': _('Thank you for your feedback.')}
        return HttpResponse(json.dumps(response), content_type='application/json')

    return HttpResponsePermanentRedirect(article.get_absolute_url())
