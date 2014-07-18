from __future__ import unicode_literals

from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
