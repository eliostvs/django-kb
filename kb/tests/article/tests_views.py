from __future__ import unicode_literals

from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from model_mommy import mommy

from kb.models import Article
from kb.base.test import LoggedUser, ViewTestCase


class TestArticleDetailView(ViewTestCase):

    from kb.views import ArticleDetailView

    view_class = ArticleDetailView
    view_name = 'kb:article_detail'
    view_kwargs = {'slug': 'eggs'}

    def test_view(self):
        from kb.forms import SearchForm

        article = mommy.make_recipe('kb.tests.published_article', slug='eggs')
        published = mommy.make_recipe('kb.tests.published_article')
        mommy.make_recipe('kb.tests.draft_article')

        for each in Article.objects.all():
            each.tags.add('Spam')

        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectInContext(response, article)
        self.assertEqual(response.context_data['search_form'], SearchForm)
        self.assertSeqEqual(response.context_data['related'], [published])

    def test_draft_article(self):
        mommy.make_recipe('kb.tests.draft_article', slug='eggs')

        self.assertRaises(Http404, self.get, user=LoggedUser())
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


class ArticleCreateViewTestCase(ViewTestCase):

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
        return mommy.make('User')

    def test_view(self):
        from kb.forms import ArticleForm
        from kb.models import Article

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), ArticleForm)

        self.assertFormInvalid(self.post(data={}))

        self.assertEqual(0, Article.objects.count())

        user = self.get_user()
        self.assertRedirectTo(self.post(user=user, data=self.form_data),
                              reverse('kb:article_list'))

        self.assertEqual(1, Article.objects.count())

        article = Article.objects.get(pk=1)
        self.assertEqual(article.created_by, user)

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()


class ArticleDeleteViewTestCase(ViewTestCase):

    from kb.views import ArticleDeleteView

    view_class = ArticleDeleteView
    view_name = 'kb:article_delete'
    view_user = LoggedUser
    view_kwargs = {'slug': 'spam'}

    def test_view(self,):
        from kb.models import Article

        mommy.make('Article', slug='spam')

        self.assertEqual(1, Article.objects.count())

        self.assertHttpOK(self.get())
        self.assertRedirectToLoginWhenAnonymous()

        self.assertRedirectTo(self.post(), reverse('kb:article_list'))

        self.assertEqual(0, Article.objects.count())


class ArticleListViewTestCase(ViewTestCase):

    from kb.views import ArticleListView

    view_class = ArticleListView
    view_name = 'kb:article_list'
    view_user = LoggedUser

    def test_view(self):
        articles = mommy.make('Article', _quantity=2)

        self.assertHttpOK(self.get())
        self.assertObjectListInContext(self.get(), articles)
        self.assertRedirectToLoginWhenAnonymous()


class ArticleUpdateViewTestCase(ViewTestCase):

    from kb.views import ArticleUpdateView

    view_class = ArticleUpdateView
    view_name = 'kb:article_edit'
    view_user = LoggedUser
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

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertFormClass(self.get(), ArticleForm)

        self.assertFormInvalid(self.post(data={}))

        self.assertRedirectTo(self.post(data=self.form_data), reverse('kb:article_list'))

        article = self.refresh(self.article)

        self.assertEqual(article.title, 'Bar')
        self.assertEqual(article.content, 'Foo')
