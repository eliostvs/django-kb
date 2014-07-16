#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kb

from setuptools import setup, find_packages

version = kb.__version__

readme = open('README.rst').read()
history = open('HISTORY.rst').read()

setup(
    name='django-kb',
    version=version,
    description='Simple kb base made with django',
    long_description=readme + '\n\n' + history,
    author='Elio Esteves Duarte',
    author_email='elio.esteves.duarte@gmail.com',
    url='https://github.com/eliostvs/django-kb',
    packages=find_packages(exclude=['*tests*']),
    include_package_data=True,
    install_requires=[
        "Django>=1.6, <1.7",
        "South>=0.8.4, <1.0",
        "django-braces>=1.4.0",
        "django-choices>=1.1.12",
        "django-haystack>=2.1.0",
        "django-model-utils>=2.0.3",
        "django-taggit>=0.12",
    ],
    license="BSD",
    zip_safe=False,
    keywords=['django', 'kb', 'knowledge base'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
