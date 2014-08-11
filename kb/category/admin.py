from __future__ import unicode_literals

from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['name', 'description']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'description']
