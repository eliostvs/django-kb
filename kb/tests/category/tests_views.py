from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from model_mommy import mommy

from kb.base import test
from kb.models import Article


class CategoryDetailViewTestCase(test.ViewTestCase):

    from kb.views import CategoryDetailView

    view_class = CategoryDetailView
    view_name = 'kb:category_detail'
    view_kwargs = {'slug': 'spam'}

    def test_view(self):
        from kb.forms import SearchForm

        category = mommy.make_recipe('kb.tests.category_with_articles', slug='spam')

        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectInContext(response, category)
        self.assertSeqEqual(response.context_data['articles'], Article.objects.published())
        self.assertEqual(response.context_data['search_form'], SearchForm)


class CategoryCreateViewTestCase(test.ViewTestCase):

    from kb.views import CategoryCreateView

    view_class = CategoryCreateView
    view_name = 'kb:category_add'

    def get_user(self):
        return self.user

    def setUp(self):
        self.user = mommy.make('User', username='guido', is_staff=True)

        category = mommy.prepare('Category', slug='eggs')

        self.form_data = {
            'name': category.name,
            'slug': category.slug,
        }

    def test_view(self):
        from kb.forms import CategoryForm
        from kb.models import Category

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), CategoryForm)
        self.assertFormInvalid(self.post(data={}))

        self.assertEqual(Category.objects.count(), 0)

        self.assertRedirectTo(self.post(data=self.form_data),
                              reverse('kb:category_list'))

        self.assertEqual(Category.objects.count(), 1)

        category = Category.objects.get(pk=1)
        self.assertEqual(category.created_by, self.user)

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()


class CategoryListViewTestCase(test.ViewTestCase):

    from kb.views import CategoryListView

    view_class = CategoryListView
    view_name = 'kb:category_list'
    view_user = test.StaffUser

    def test_view(self):
        categories = mommy.make('Category', _quantity=2)
        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectListInContext(response, categories)

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()


class CategoryUpdateViewTestCase(test.ViewTestCase):

    from kb.views import CategoryUpdateView

    view_class = CategoryUpdateView
    view_name = 'kb:category_edit'
    view_user = test.StaffUser
    view_kwargs = {'slug': 'spam'}

    def setUp(self):
        self.category = mommy.make_recipe('kb.tests.category_without_articles',
                                          slug='spam')

        self.form_data = {
            'name': 'Eggs',
            'slug': self.category.slug,
        }

    def test_view(self):
        from kb.forms import CategoryForm

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), CategoryForm)
        self.assertFormInvalid(self.post(data={}))

        self.assertRedirectTo(self.post(data=self.form_data),
                              reverse('kb:category_list'))

        category = self.refresh(self.category)
        self.assertEqual(category.name, 'Eggs')

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()


class CategoryDeleteViewTestCase(test.ViewTestCase):

    from kb.views import CategoryDeleteView

    view_class = CategoryDeleteView
    view_name = 'kb:category_delete'
    view_user = test.StaffUser
    view_kwargs = {'slug': 'spam'}

    def setUp(self):
        mommy.make('Category', slug='spam')

    def test_view(self):
        from kb.models import Category

        self.assertHttpOK(self.get())

        self.assertEqual(1, Category.objects.count())
        self.assertRedirectTo(self.post(), reverse('kb:category_list'))
        self.assertEqual(0, Category.objects.count())

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()
