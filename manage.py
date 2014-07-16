#!/usr/bin/env python
import os
import sys

from django.conf import settings
from django.conf.urls import patterns, include, url

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(here, 'kb'))

settings.configure(
    SECRET_KEY='placerandomsecretkeyhere',
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ":memory:",
        }
    },
    INSTALLED_APPS=(
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'taggit',
        'haystack',
        'kb',
        'kb.tests',
    ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    ROOT_URLCONF=sys.modules[__name__],
    SITE_ID=1,
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',),
    SOUTH_TESTS_MIGRATE=False,
    SOUTH_MIGRATION_MODULES={
        'taggit': 'taggit.south_migrations',
    },
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(here, 'whoosh_index'),
        },
    },
    USE_TZ=True,
)

urlpatterns = patterns(
    '',
    url(r'', include('kb.urls', namespace='kb')),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
