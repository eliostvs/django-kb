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


class ArticleTagListView(generic.ListView):

    slug_url_kwarg = 'tag'
    pk_url_kwarg = 'pk'
    queryset = Article.objects.published()

    def get_queryset(self):
        queryset = super(ArticleTagListView, self).get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if pk is not None:
            queryset = queryset.filter(tags__pk__in=[pk])

        elif slug is not None:
            queryset = queryset.filter(tags__name__in=[slug])

        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        return queryset
