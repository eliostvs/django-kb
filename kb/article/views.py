from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces.views import StaffuserRequiredMixin

from taggit.models import Tag

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

    form_class = ArticleForm
    model = Article
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

    form_class = ArticleForm
    model = Article
    success_url = reverse_lazy('kb:article_list')


class TagListView(views.AddSearchFormToContextMixin,
                  generic.ListView):

    paginate_by = 10
    queryset = Article.objects.published()
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super(TagListView, self).get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        return queryset.filter(tags__slug__in=[slug]).distinct()

    def get_template_names(self):
        return ['kb/tag_list.html']

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        context['tag'] = Tag.objects.get(slug__iexact=slug)
        return context
