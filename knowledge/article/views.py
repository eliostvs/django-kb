from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces.views import LoginRequiredMixin

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
        context['related_articles'] = self.related_articles()
        return context

    def related_articles(self):
        return self.object.related(self.request.user.is_anonymous())


class ArticleCreateView(LoginRequiredMixin,
                        views.AuthorFormMixin,
                        generic.CreateView):

    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('knowledge:article_list')


class ArticleListView(LoginRequiredMixin,
                      generic.ListView):

    model = Article


class ArticleDeleteView(LoginRequiredMixin,
                        generic.DeleteView):

    model = Article
    success_url = reverse_lazy('knowledge:article_list')


class ArticleUpdateView(LoginRequiredMixin,
                        generic.UpdateView):

    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('knowledge:article_list')
