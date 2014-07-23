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


class TagListView(generic.ListView):

    slug_url_kwarg = 'tag'
    queryset = Article.objects.published()
    template_name = 'kb/tag_list.html'

    def get_queryset(self):
        queryset = super(TagListView, self).get_queryset()
        tag = self.kwargs.get(self.slug_url_kwarg, None)

        return queryset.filter(tags__name__in=[tag]).distinct()

    def get_template_names(self):
        return [self.template_name]
