from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from model_mommy import mommy

from knowledge.base.test import LoggedUser, ViewTestCase
from knowledge.models import Article


class CategoryDetailViewTestCase(ViewTestCase):

    from knowledge.views import CategoryDetailView

    view_class = CategoryDetailView
    view_name = 'knowledge:category_detail'
    view_kwargs = {'slug': 'spam'}

    def test_view(self):
        from knowledge.forms import SimpleSearchForm

        category = mommy.make_recipe('knowledge.tests.category_with_articles', slug='spam')
        subcategory = mommy.make_recipe('knowledge.tests.subcategory', parent=category)

        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectInContext(response, category)
        self.assertSeqEqual(response.context_data['subcategory_list'], [subcategory])
        self.assertSeqEqual(response.context_data['article_list'], Article.objects.published())
        self.assertEqual(response.context_data['search_form'], SimpleSearchForm)


class CategoryCreateViewTestCase(ViewTestCase):

    from knowledge.views import CategoryCreateView

    view_class = CategoryCreateView
    view_name = 'knowledge:category_add'

    def get_user(self):
        return self.user

    def setUp(self):
        self.user = mommy.make('User', username='guido')

        category = mommy.prepare('Category', slug='eggs')

        self.form_data = {
            'name': category.name,
            'slug': category.slug,
        }

    def test_view(self):
        from knowledge.forms import CategoryForm
        from knowledge.models import Category

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), CategoryForm)
        self.assertFormInvalid(self.post(data={}))

        self.assertEqual(Category.objects.count(), 0)

        self.assertRedirectTo(self.post(data=self.form_data),
                              reverse('knowledge:category_list'))

        self.assertEqual(Category.objects.count(), 1)

        category = Category.objects.get(pk=1)
        self.assertEqual(category.created_by, self.user)

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()


class CategoryListViewTestCase(ViewTestCase):

    from knowledge.views import CategoryListView

    view_class = CategoryListView
    view_name = 'knowledge:category_list'
    view_user = LoggedUser

    def test_view(self):
        categories = mommy.make('Category', _quantity=2)
        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectListInContext(response, categories)
        self.assertRedirectToLoginWhenAnonymous()


class CategoryUpdateViewTestCase(ViewTestCase):

    from knowledge.views import CategoryUpdateView

    view_class = CategoryUpdateView
    view_name = 'knowledge:category_edit'
    view_user = LoggedUser
    view_kwargs = {'slug': 'spam'}

    def setUp(self):
        self.category = mommy.make_recipe('knowledge.tests.category_without_articles',
                                          slug='spam')

        self.form_data = {
            'name': 'Eggs',
            'slug': self.category.slug,
        }

    def test_view(self):
        from knowledge.forms import CategoryForm

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), CategoryForm)
        self.assertFormInvalid(self.post(data={}))

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectTo(self.post(data=self.form_data),
                              reverse('knowledge:category_list'))

        category = self.refresh(self.category)
        self.assertEqual(category.name, 'Eggs')


class CategoryDeleteViewTestCase(ViewTestCase):

    from knowledge.views import CategoryDeleteView

    view_class = CategoryDeleteView
    view_name = 'knowledge:category_delete'
    view_user = LoggedUser
    view_kwargs = {'slug': 'spam'}

    def setUp(self):
        mommy.make('Category', slug='spam')

    def test_view(self):
        from knowledge.models import Category

        self.assertHttpOK(self.get())

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertEqual(1, Category.objects.count())
        self.assertRedirectTo(self.post(), reverse('knowledge:category_list'))
        self.assertEqual(0, Category.objects.count())
