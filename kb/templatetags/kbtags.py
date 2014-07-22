from __future__ import unicode_literals

from django import template

from ..article.models import Article

register = template.Library()


@register.assignment_tag
def top_new_articles(num=5, category=None):
    return Article.objects.top_new(num, category)


@register.assignment_tag
def top_viewed_articles(num=5, category=None):
    return Article.objects.top_viewed(num, category)


@register.assignment_tag
def top_rated_articles(num=5, category=None):
    return Article.objects.top_rated(num, category)
