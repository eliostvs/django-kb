from __future__ import unicode_literals

from django.http import Http404

from ..base import choices
from ..forms import SimpleSearchForm


class AddTagsToContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(AddTagsToContextMixin, self).get_context_data(**kwargs)
        context['tags'] = self.object.tags.all()
        return context


class LoginRequiredForPrivateObjectMixin(object):

    def get_object(self, queryset=None):
        obj = super(LoginRequiredForPrivateObjectMixin, self).get_object(queryset)

        if all([obj.visibility == choices.VisibilityChoice.Private,
                self.request.user.is_anonymous()]):
            raise Http404

        return obj


class PublishedRequiredMixin(object):

    def get_object(self, queryset=None):
        obj = super(PublishedRequiredMixin, self).get_object(queryset)

        if obj.publish_state == choices.PublishChoice.Draft:
            raise Http404

        return obj


class AddSearchFormToContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(AddSearchFormToContextMixin, self).get_context_data(**kwargs)
        context['search_form'] = SimpleSearchForm
        return context


class AuthorFormMixin(object):

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(AuthorFormMixin, self).form_valid(form)
