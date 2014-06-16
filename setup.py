#!/usr/bin/env python
# -*- coding: utf-8 -*-

import knowledge

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

version = knowledge.__version__

readme = open('README.rst').read()
history = open('HISTORY.rst').read()

setup(
    name='dj-knowledge',
    version=version,
    description="""Simple knowledge base made with django""",
    long_description=readme + '\n\n' + history,
    author='Elio Esteves Duarte',
    author_email='elio.esteves.duarte@gmail.com',
    url='https://github.com/eliostvs/dj-knowledge',
    packages=[
        'knowledge',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='dj-knowledge',
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
