from model_mommy import mommy

from kb.tests import test


class LiveTestArticleDetailView(test.BaseLiveServer):

    def test_upvote_and_downvote_article(self):
        article = mommy.make_recipe('kb.tests.published_article', slug='eggs')
        url = '/article/eggs/'

        self.visit(url)

        self.assertEqual(article.votes.total(), 0)
        self.assertTrue(self.browser.find_by_id('votes'))
        self.assertEqual(len(self.browser.find_by_css('.voter')), 2)

        upvote_link = self.browser.find_by_id('upvote')

        self.assertTrue(upvote_link)
        self.assertTrue(self.browser.is_text_not_present('Thank you for your feedback.'))

        upvote_link.click()

        self.assertTrue(self.browser.is_text_present('Thank you for your feedback.'))
        self.assertEqual(article.votes.total(), 1)
        self.assertEqual(article.votes.upvotes(), 1)

        self.visit(url)
        downvote_link = self.browser.find_by_id('downvote')

        self.assertTrue(downvote_link)
        self.assertTrue(self.browser.is_text_not_present('Thank you for your feedback.'))

        downvote_link.click()

        self.assertTrue(self.browser.is_text_present('Thank you for your feedback.'))
        self.assertEqual(article.votes.total(), 1)
        self.assertEqual(article.votes.downvotes(), 1)
