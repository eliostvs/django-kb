from __future__ import unicode_literals

from django.http import Http404

from ..base import choices
from ..settings import api_settings


class AddTagsToContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(AddTagsToContextMixin, self).get_context_data(**kwargs)
        context['tags'] = self.object.tags.all()
        return context


class PublishedRequiredMixin(object):

    def get_object(self, queryset=None):
        obj = super(PublishedRequiredMixin, self).get_object(queryset)

        if all([obj.publish_state == choices.PublishChoice.Draft,
                not self.request.user.is_staff]):

            raise Http404

        return obj


class AddSearchFormToContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(AddSearchFormToContextMixin, self).get_context_data(**kwargs)
        context['search_form'] = api_settings.DEFAULT_SEARCH_FORM_CLASS
        return context


class AuthorFormMixin(object):

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AuthorFormMixin, self).form_valid(form)
