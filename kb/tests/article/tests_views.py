from __future__ import unicode_literals

from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from model_mommy import mommy

from kb.base import test


class TestArticleDetailView(test.ViewTestCase):

    from kb.views import ArticleDetailView

    view_class = ArticleDetailView
    view_name = 'kb:article_detail'
    view_kwargs = {'slug': 'eggs'}
    view_user = test.StaffUser

    def test_view(self):
        from kb.forms import SearchForm

        article = mommy.make_recipe('kb.tests.published_article', slug='eggs')
        published = mommy.make_recipe('kb.tests.published_article')
        draft = mommy.make_recipe('kb.tests.draft_article')
        mommy.make_recipe('kb.tests.published_article')

        for each in [article, published, draft]:
            each.tags.add('Spam')

        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectInContext(response, article)
        self.assertEqual(response.context_data['search_form'], SearchForm)
        self.assertSeqEqual(response.context_data['related'], [published])

    def test_draft_article(self):
        mommy.make_recipe('kb.tests.draft_article', slug='eggs')

        self.assertHttpOK(self.get())
        self.assertRaises(Http404, self.get, user=test.LoggedUser)
        self.assertRaises(Http404, self.get, user=AnonymousUser())

    def test_should_list_article_tags(self):
        article = mommy.make_recipe('kb.tests.published_article', slug='eggs')
        article.tags.add('Spam')
        response = self.get()

        self.assertEqual(len(response.context_data['tags']), 1)
        self.assertEqual(response.context_data['tags'][0].name, 'Spam')

    def test_view_counter(self):
        article = mommy.make_recipe('kb.tests.published_article', slug='eggs')
        self.assertEqual(article.hits, 0)

        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['object'].modified, article.modified)

        article = self.refresh(article)

        self.assertEqual(article.hits, 1)


class ArticleCreateViewTestCase(test.ViewTestCase):

    from kb.views import ArticleCreateView

    view_class = ArticleCreateView
    view_name = 'kb:article_add'

    def setUp(self):
        category = mommy.make('Category')
        article = mommy.prepare_recipe('kb.tests.published_article',
                                       category=category,
                                       slug='eggs')

        self.form_data = {
            'title': article.title,
            'content': article.content,
            'slug': article.slug,
            'publish_state': article.publish_state,
            'category': article.category.id,
        }

    def get_user(self):
        return mommy.make('User', is_staff=True)

    def test_view(self):
        from kb.forms import ArticleForm
        from kb.models import Article

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), ArticleForm)

        self.assertFormInvalid(self.post(data={}))

        self.assertEqual(0, Article.objects.count())

        self.assertRedirectTo(self.post(data=self.form_data),
                              reverse('kb:article_list'))

        self.assertEqual(1, Article.objects.count())

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()


class ArticleDeleteViewTestCase(test.ViewTestCase):

    from kb.views import ArticleDeleteView

    view_class = ArticleDeleteView
    view_name = 'kb:article_delete'
    view_user = test.StaffUser
    view_kwargs = {'slug': 'spam'}

    def test_view(self,):
        from kb.models import Article

        mommy.make_recipe('kb.tests.draft_article', slug='spam')

        self.assertEqual(1, Article.objects.count())

        self.assertHttpOK(self.get())

        self.assertRedirectTo(self.post(), reverse('kb:article_list'))

        self.assertEqual(0, Article.objects.count())

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()


class ArticleListViewTestCase(test.ViewTestCase):

    from kb.views import ArticleListView

    view_class = ArticleListView
    view_name = 'kb:article_list'
    view_user = test.StaffUser

    def test_view(self):
        articles = mommy.make_recipe('kb.tests.draft_article', _quantity=2)

        self.assertHttpOK(self.get())
        self.assertObjectListInContext(self.get(), articles)

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()


class ArticleUpdateViewTestCase(test.ViewTestCase):

    from kb.views import ArticleUpdateView

    view_class = ArticleUpdateView
    view_name = 'kb:article_edit'
    view_user = test.StaffUser
    view_kwargs = {'slug': 'spam'}

    def setUp(self):
        category = mommy.make('Category')
        self.article = mommy.make_recipe('kb.tests.published_article',
                                         category=category,
                                         slug='spam')

        self.form_data = {
            'title': 'Bar',
            'slug': self.article.slug,
            'content': 'Foo',
            'publish_state': self.article.publish_state,
            'category': category.pk,
        }

    def test_view(self):
        from kb.forms import ArticleForm

        self.assertHttpOK(self.get())

        self.assertFormClass(self.get(), ArticleForm)

        self.assertFormInvalid(self.post(data={}))

        self.assertRedirectTo(self.post(data=self.form_data), reverse('kb:article_list'))

        article = self.refresh(self.article)

        self.assertEqual(article.title, 'Bar')
        self.assertEqual(article.content.raw, 'Foo')
        self.assertEqual(article.content.rendered, '<p>Foo</p>')

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertRedirectToLoginWhenNonStaff()
        self.assertRedirectToLoginWhenNonStaffOnPost()
