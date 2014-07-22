from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces.views import StaffuserRequiredMixin

from ..base import views
from .forms import ArticleForm
from .models import Article


class ArticleDetailView(views.AddSearchFormToContextMixin,
                        views.AddTagsToContextMixin,
                        views.PublishedRequiredMixin,
                        generic.DetailView):

    model = Article

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object(queryset)
        obj.increase_hits()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['related'] = self.object.related()
        return context


class ArticleCreateView(StaffuserRequiredMixin,
                        views.AuthorFormMixin,
                        generic.CreateView):

    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('kb:article_list')


class ArticleListView(StaffuserRequiredMixin,
                      generic.ListView):

    model = Article


class ArticleDeleteView(StaffuserRequiredMixin,
                        generic.DeleteView):

    model = Article
    success_url = reverse_lazy('kb:article_list')


class ArticleUpdateView(StaffuserRequiredMixin,
                        generic.UpdateView):

    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('kb:article_list')
