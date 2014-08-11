from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _

from kb.base.choices import PublishChoice


class ArticleAdmin(admin.ModelAdmin):
    actions = ('make_published', 'make_draft')
    date_hierarchy = 'created'
    list_display = ('title', 'category', 'created_by', 'publish_state', 'hits')
    list_filter = ('publish_state',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'content', 'category__name']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(publish_state=PublishChoice.Published)

        if rows_updated == 1:
            message_bit = _("1 article was")

        else:
            message_bit = ("%s articles were") % rows_updated

        self.message_user(request, _("%s successfully marked as published.") % message_bit)

    make_published.short_description = "Mark selected articles as published"

    def make_draft(self, request, queryset):
        rows_updated = queryset.update(publish_state=PublishChoice.Draft)

        if rows_updated == 1:
            message_bit = _("1 article was")

        else:
            message_bit = ("%s articles were") % rows_updated

        self.message_user(request, _("%s successfully marked as draft.") % message_bit)

    make_draft.short_description = "Mark selected articles as draft"
