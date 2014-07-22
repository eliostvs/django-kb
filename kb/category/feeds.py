from __future__ import unicode_literals

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from .models import Category


class CategoryFeed(Feed):

    def get_object(self, request, slug):
        return get_object_or_404(Category.objects.categories(), slug=slug)

    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        return obj.name

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return obj.articles.published()

    def item_description(self, item):
        return item.content.rendered

    def item_pubdate(self, item):
        return item.created

    def item_categories(self, item):
        return item.tags.all()

    def item_author_name(self, item):
        return item.created_by.username
