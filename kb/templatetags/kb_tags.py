from __future__ import unicode_literals

from django import template

from ..article.models import Article

register = template.Library()


@register.assignment_tag
def top_new_articles(num=5):
    return Article.objects.new(num)


@register.assignment_tag
def top_viewed_articles(num=5):
    return Article.objects.top_viewed(num)
