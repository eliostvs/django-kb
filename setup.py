#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = open('README.rst').read()
history = open('HISTORY.rst').read()

setup(
    name='django-kb',
    version='0.2.0',
    description='Simple knowledge base made with django',
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
        "django-choices>=1.3.0",
        "django-haystack>=2.2.0",
        "django-model-utils>=2.2.0",
        "django-taggit>=0.12.1",
        "django-markupfield==1.2.1",
        "pytz>=2014.4",
    ],
    license='BSD',
    zip_safe=False,
    keywords='django,knowledge base',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
