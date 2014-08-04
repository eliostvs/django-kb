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


@register.inclusion_tag('kb/inclusion_tags/feedback_extender.html', takes_context=True)
def feedback(context, template_name=None):
    if template_name is None:
        template_name = 'kb/inclusion_tags/feedback.html'

    context.update({'vote_template': template_name})
    return context
