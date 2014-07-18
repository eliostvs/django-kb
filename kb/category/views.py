from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic

from braces.views import StaffuserRequiredMixin

from ..base import views
from .forms import CategoryForm
from .models import Category


class CategoryDetailView(views.AddSearchFormToContextMixin,
                         generic.DetailView):

    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['articles'] = self.object.articles.published()
        return context


class CategoryCreateView(StaffuserRequiredMixin,
                         views.AuthorFormMixin,
                         generic.CreateView):

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('kb:category_list')


class CategoryListView(StaffuserRequiredMixin,
                       generic.ListView):

    model = Category


class CategoryUpdateView(StaffuserRequiredMixin,
                         generic.UpdateView):

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('kb:category_list')


class CategoryDeleteView(StaffuserRequiredMixin,
                         generic.DeleteView):

    model = Category
    success_url = reverse_lazy('kb:category_list')
