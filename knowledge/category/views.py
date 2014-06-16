from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces.views import LoginRequiredMixin

from ..base import views
from .forms import CategoryForm
from .models import Category


class CategoryDetailView(views.AddSearchFormToContextMixin,
                         views.LoginRequiredForPrivateObjectMixin,
                         generic.DetailView):

    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['subcategory_list'] = self.subcategory_list()
        context['article_list'] = self.article_list()
        return context

    def subcategory_list(self):
        return self.object.subcategories(self.request.user.is_anonymous())

    def article_list(self):
        qs = self.object.articles.published()

        if self.request.user.is_anonymous():
            qs = qs.public()

        return qs


class CategoryCreateView(LoginRequiredMixin,
                         views.AuthorFormMixin,
                         generic.CreateView):

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('knowledge:category_list')


class CategoryListView(LoginRequiredMixin,
                       generic.ListView):

    model = Category


class CategoryUpdateView(LoginRequiredMixin,
                         generic.UpdateView):

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('knowledge:category_list')


class CategoryDeleteView(LoginRequiredMixin,
                         generic.DeleteView):

    model = Category
    success_url = reverse_lazy('knowledge:category_list')
