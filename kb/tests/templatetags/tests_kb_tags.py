from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy


class TemplateTagsTestCase(TestCase):

    def test_tag_top_new_articles(self):
        from kb.templatetags.kb_tags import top_new_articles

        articles = mommy.make_recipe('kb.tests.published_article', _quantity=6)
        articles.reverse()
        mommy.make_recipe('kb.tests.draft_article')

        return self.assertSequenceEqual(top_new_articles(), articles[:-1])
        return self.assertSequenceEqual(top_new_articles(1), articles[-2])
