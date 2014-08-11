from __future__ import unicode_literals

from django.contrib import admin


class VoteAdmin(admin.ModelAdmin):
     date_hierarchy = 'created'
     list_display = ['token', 'rate', 'article']
     list_filter = ('rate',)
     search_fields = ['article__title']
