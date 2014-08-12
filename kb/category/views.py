from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.list import MultipleObjectMixin

from braces.views import StaffuserRequiredMixin

from ..base import views
from .forms import CategoryForm
from .models import Category


class CategoryDetailView(views.AddSearchFormToContextMixin,
                         MultipleObjectMixin,
                         generic.DetailView):

    model = Category
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        return context

    @property
    def object_list(self):
        return self.object.articles.published()


class CategoryCreateView(StaffuserRequiredMixin,
                         views.AuthorFormMixin,
                         generic.CreateView):

    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('kb:category_list')


class CategoryListView(StaffuserRequiredMixin,
                       generic.ListView):

    model = Category


class CategoryUpdateView(StaffuserRequiredMixin,
                         generic.UpdateView):

    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('kb:category_list')


class CategoryDeleteView(StaffuserRequiredMixin,
                         generic.DeleteView):

    model = Category
    success_url = reverse_lazy('kb:category_list')
