from __future__ import unicode_literals

from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from model_mommy import mommy

from knowledge.models import Article
from knowledge.base.test import LoggedUser, ViewTestCase


class TestArticleDetailView(ViewTestCase):

    from knowledge.views import ArticleDetailView

    view_class = ArticleDetailView
    view_name = 'knowledge:article_detail'
    view_kwargs = {'slug': 'eggs'}
    view_user = LoggedUser

    def test_view(self):
        from knowledge.forms import SimpleSearchForm

        article = mommy.make_recipe('knowledge.tests.public_published_article', slug='eggs')
        mommy.make_recipe('knowledge.tests.public_draft_article')
        mommy.make_recipe('knowledge.tests.private_draft_article')
        private = mommy.make_recipe('knowledge.tests.private_published_article')
        public = mommy.make_recipe('knowledge.tests.public_published_article')

        for each in Article.objects.all():
            each.tags.add('Spam')

        response = self.get()

        self.assertHttpOK(response)
        self.assertObjectInContext(response, article)
        self.assertEqual(response.context_data['search_form'], SimpleSearchForm)
        self.assertSeqEqual(response.context_data['related_articles'], [public, private])

        response = self.get(user=AnonymousUser())

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['search_form'], SimpleSearchForm)
        self.assertSeqEqual(response.context_data['related_articles'], [public])

    def test_private_article(self):
        mommy.make_recipe('knowledge.tests.private_published_article', slug='eggs')

        self.assertHttpOK(self.get())
        self.assertRaises(Http404, self.get, user=AnonymousUser())

    def test_draft_article(self):
        mommy.make_recipe('knowledge.tests.public_draft_article', slug='eggs')

        self.assertRaises(Http404, self.get, user=LoggedUser())
        self.assertRaises(Http404, self.get, user=AnonymousUser())

    def test_should_list_article_tags(self):
        article = mommy.make_recipe('knowledge.tests.public_published_article', slug='eggs')
        article.tags.add('Spam')
        response = self.get()

        self.assertEqual(len(response.context_data['tags']), 1)
        self.assertEqual(response.context_data['tags'][0].name, 'Spam')

    def test_view_counter(self):
        article = mommy.make_recipe('knowledge.tests.public_published_article', slug='eggs')
        self.assertEqual(article.hits, 0)

        response = self.get()

        self.assertHttpOK(response)
        self.assertEqual(response.context_data['object'].modified, article.modified)

        article = self.refresh(article)

        self.assertEqual(article.hits, 1)


class ArticleCreateViewTestCase(ViewTestCase):

    from knowledge.views import ArticleCreateView

    view_class = ArticleCreateView
    view_name = 'knowledge:article_add'

    def setUp(self):
        category = mommy.make('Category')
        article = mommy.prepare_recipe('knowledge.tests.private_published_article',
                                       category=category,
                                       slug='eggs')

        self.form_data = {
            'title': article.title,
            'content': article.content,
            'slug': article.slug,
            'visibility': article.visibility,
            'publish_state': article.publish_state,
            'category': article.category.id,
        }

    def get_user(self):
        return mommy.make('User')

    def test_view(self):
        from knowledge.forms import ArticleForm
        from knowledge.models import Article

        self.assertHttpOK(self.get())
        self.assertFormClass(self.get(), ArticleForm)

        self.assertFormInvalid(self.post(data={}))

        self.assertEqual(0, Article.objects.count())

        user = self.get_user()
        self.assertRedirectTo(self.post(user=user, data=self.form_data),
                              reverse('knowledge:article_list'))

        self.assertEqual(1, Article.objects.count())

        article = Article.objects.get(pk=1)
        self.assertEqual(article.created_by, user)

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()


class ArticleDeleteViewTestCase(ViewTestCase):

    from knowledge.views import ArticleDeleteView

    view_class = ArticleDeleteView
    view_name = 'knowledge:article_delete'
    view_user = LoggedUser
    view_kwargs = {'slug': 'spam'}

    def test_view(self,):
        from knowledge.models import Article

        mommy.make('Article', slug='spam')

        self.assertEqual(1, Article.objects.count())

        self.assertHttpOK(self.get())
        self.assertRedirectToLoginWhenAnonymous()

        self.assertRedirectTo(self.post(), reverse('knowledge:article_list'))

        self.assertEqual(0, Article.objects.count())


class ArticleListViewTestCase(ViewTestCase):

    from knowledge.views import ArticleListView

    view_class = ArticleListView
    view_name = 'knowledge:article_list'
    view_user = LoggedUser

    def test_view(self):
        articles = mommy.make('Article', _quantity=2)

        self.assertHttpOK(self.get())
        self.assertObjectListInContext(self.get(), articles)
        self.assertRedirectToLoginWhenAnonymous()


class ArticleUpdateViewTestCase(ViewTestCase):

    from knowledge.views import ArticleUpdateView

    view_class = ArticleUpdateView
    view_name = 'knowledge:article_edit'
    view_user = LoggedUser
    view_kwargs = {'slug': 'spam'}

    def setUp(self):
        category = mommy.make('Category')
        self.article = mommy.make_recipe('knowledge.tests.public_published_article',
                                         category=category,
                                         slug='spam')

        self.form_data = {
            'title': 'Bar',
            'slug': self.article.slug,
            'content': self.article.content,
            'visibility': self.article.visibility,
            'publish_state': self.article.publish_state,
            'category': category.pk,
        }

    def test_view(self):
        from knowledge.forms import ArticleForm

        self.assertHttpOK(self.get())

        self.assertRedirectToLoginWhenAnonymous()
        self.assertRedirectToLoginWhenAnonymousOnPost()

        self.assertFormClass(self.get(), ArticleForm)

        self.assertFormInvalid(self.post(data={}))

        self.assertRedirectTo(self.post(data=self.form_data), reverse('knowledge:article_list'))

        article = self.refresh(self.article)

        self.assertEqual(article.title, 'Bar')
