from __future__ import unicode_literals

from django.contrib import admin

from .article.admin import ArticleAdmin
from .category.admin import CategoryAdmin
from .vote.admin import VoteAdmin

from .models import Article, Category, Vote

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vote, VoteAdmin)
