from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import Client, LiveServerTestCase, RequestFactory, TestCase

from mock import Mock
from splinter import Browser

LoggedUser = Mock()
LoggedUser.is_authenticated = Mock(return_value=True)
LoggedUser.is_anonymous = Mock(return_value=False)
LoggedUser.is_staff = False
LoggedUser.username = 'Logged User'
LoggedUser.id = 1

StaffUser = Mock()
StaffUser.is_authenticated = Mock(return_value=True)
StaffUser.is_anonymous = Mock(return_value=False)
StaffUser.is_staff = True
StaffUser.username = 'Staff User'
StaffUser.id = 1


class StatusCodeAssertionMixin(object):
    def assertHttpCode(self, response, code, code_description):
        self.assertEqual(
            response.status_code, code,
            "Expected an HTTP %s (%s) response, but got HTTP %s" %
            (code, code_description, response.status_code))

    def assertHttpOK(self, response):
        self.assertHttpCode(response, 200, "OK")

    def assertRedirectTo(self, response, expected_url=None):

        self.assertTrue(
            300 <= response.status_code < 400,
            "Expected an HTTP 3XX (redirect) response, but got HTTP %s" %
            response.status_code
        )

        if expected_url:
            location = response._headers.get('location', None)

            self.assertEqual(
                location,
                ('Location', str(expected_url)),
                'Response should redirect to {0}, but it redirects to {1} instead'.format(
                    expected_url,
                    location[1],
                )
            )


class SequenceAssertionMixin(object):

    def assertSeqEqual(self, first, second, msg=None):
        try:
            return super(SequenceAssertionMixin, self).assertCountEqual(first, second, msg)

        except AttributeError:
            return super(SequenceAssertionMixin, self).assertItemsEqual(first, second, msg)


class FormAssertionMixin(object):

    def assertFormInvalid(self, response, form_name='form'):
        try:
            form = response.context_data[form_name]

        except KeyError:
            self.fail("Could not find a form in the response.")

        self.assertFalse(form.is_valid(), "Expected form to be invalid, but it was valid.")

        self.assertEqual(
            response.status_code, 200,
            "Expected HTTP 200, but got HTTP %d. "
            "Looks like the form validated when it shouldn't." % response. status_code)

    def assertFormClass(self, response, form_class, form_name='form'):
        try:
            form = response.context_data[form_name]
        except KeyError:
            self.fail("Could not find a form in the response.")

        self.assertIsInstance(form, form_class)


class AccessAsssertionsMixin(object):

    def assertRedirectToLoginWhenAnonymous(self):
        self.assertRedirectTo(self.get(user=AnonymousUser()),
                              '{0}?next={1}'.format(self.get_login_url(), self.get_view_path()))

    def assertRedirectToLoginWhenAnonymousOnPost(self):
        self.assertRedirectTo(self.post(user=AnonymousUser(), data={}),
                              '{0}?next={1}'.format(self.get_login_url(), self.get_view_path()))

    def get_login_url(self):
        return getattr(settings, 'LOGIN_URL', reverse('login'))

    def assertHttpOkWhenAnonymous(self):
        self.assertHttpOK(self.get(user=AnonymousUser()))

    def assertHttpOkWhenNonStaff(self):
        self.assertHttpOK(self.get(user=LoggedUser))

    def assertRedirectToLoginWhenNonStaff(self):
        self.assertRedirectTo(self.get(user=LoggedUser),
                              '{0}?next={1}'.format(self.get_login_url(), self.get_view_path()))

    def assertRedirectToLoginWhenNonStaffOnPost(self):
        self.assertRedirectTo(self.post(user=LoggedUser, data={}),
                              '{0}?next={1}'.format(self.get_login_url(), self.get_view_path()))


class ContextAssertionsMixin(object):

    def assertObjectInContext(self, response, obj, obj_name='object'):
        self.assertEqual(response.context_data[obj_name], obj)

    def assertObjectListInContext(self, response, obj_list, obj_name='object_list'):
        self.assertSeqEqual(response.context_data[obj_name], obj_list)


class RefreshInstanceMixin(object):

    def refresh(self, instance):
        return instance.__class__._default_manager.get(pk=instance.pk)


class ViewTestCase(StatusCodeAssertionMixin,
                   FormAssertionMixin,
                   AccessAsssertionsMixin,
                   ContextAssertionsMixin,
                   RefreshInstanceMixin,
                   SequenceAssertionMixin,
                   TestCase):

    view_kwargs = None
    view_name = None
    view_user = None
    view_args = None
    view_class = None
    view_function = None
    request_extra = {}

    def _pre_setup(self, *args, **kwargs):
        super(ViewTestCase, self)._pre_setup(*args, **kwargs)
        self.factory = RequestFactory()
        self.client = Client()

    def get_view_args(self):
        return self.view_args or ()

    def get_view_kwargs(self):
        return self.view_kwargs or {}

    def get_view_path(self):
        return reverse(self.view_name, args=self.get_view_args(), kwargs=self.get_view_kwargs())

    def get_user(self):
        return self.view_user or AnonymousUser()

    def get(self, **kwargs):
        user = kwargs.get('user', None)
        if user is None:
            user = self.get_user()

        request = self.factory.get(path=self.get_view_path(), **kwargs)
        request.user = user

        response = self.view(request)

        if hasattr(response, 'render'):
            return response.render()

        return response

    def post(self, **kwargs):
        user = kwargs.get('user', None)
        if user is None:
            user = self.get_user()

        request = self.factory.post(path=self.get_view_path(), **kwargs)
        request.user = user

        return self.view(request)

    def view(self, request):
        if self.view_class:
            response = self.view_class.as_view()(request,
                                                 *self.get_view_args(),
                                                 **self.get_view_kwargs())

        elif self.view_function:
            response = self.__class__.__dict__['view_function'](request,
                                                                *self.get_view_args(),
                                                                **self.get_view_kwargs())

        return response


class SearchViewTestCase(ViewTestCase):

    def get(self, data):
        request = self.factory.get(self.view_name, data=data)
        request.user = self.get_user()
        response = process_search_response(self.view_function, request)
        return response

    def setUp(self):
        self.make_instance()
        call_command('rebuild_index', interactive=False, verbosity=0)


def process_search_response(view, request):
    view.request = request
    view.form = view.build_form()
    view.query = view.get_query()
    view.results = view.get_results()
    response = view.create_response()
    (paginator, page) = view.build_page()
    response.context = {'query': view.query,
                        'form': view.form,
                        'suggetions': None,
                        'page': page,
                        'paginator': paginator}
    return response


class BehaviorTestCaseMixin(object):
    model = None

    def get_model(self):
        return self.model

    def create_instance(self, **kwargs):
        raise NotImplementedError("Implement me")


class PermalinkTestMixin(BehaviorTestCaseMixin):

    def test_permalink(self):
        obj = self.create_instance()

        self.assertTrue(obj.slug)


class TimeStampedMixin(BehaviorTestCaseMixin):

    def test_timestamped(self):
        obj = self.create_instance()

        self.assertTrue(obj.created)
        self.assertTrue(obj.modified)


class AuthorTestMixin(BehaviorTestCaseMixin):

    def test_author(self):
        obj = self.create_instance()

        self.assertTrue(obj.created_by)

    def test_filter_author(self):
        obj = self.create_instance()
        self.create_instance()

        self.assertSeqEqual(self.get_model()._default_manager.author(obj.created_by), [obj])


class PublishableTestMixin(BehaviorTestCaseMixin):

    from kb.base.choices import PublishChoice

    choice = PublishChoice

    def test_publish_state(self):
        obj = self.create_instance()

        self.assertEqual(obj.publish_state, self.choice.Draft)

    def test_filter_published(self):
        unpublished = self.create_instance()
        published = self.create_instance(publish_state=self.choice.Published)

        self.assertSeqEqual(self.get_model()._default_manager.all(), [unpublished, published])
        self.assertSeqEqual(self.get_model()._default_manager.published(), [published])
        self.assertSeqEqual(self.get_model()._default_manager.unpublished(), [unpublished])


class BaseLiveServer(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseLiveServer, cls).setUpClass()
        cls.browser = Browser('phantomjs')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(BaseLiveServer, cls).tearDownClass()

    def visit(self, url):
        full_url = '{}{}'.format(self.live_server_url, url)
        self.browser.visit(full_url)
