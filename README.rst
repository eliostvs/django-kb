=============================
Django KB
=============================

.. image:: https://pypip.in/version/django-kb/badge.svg
    :target: https://pypi.python.org/pypi/django-kb/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/django-kb/badge.svg
    :target: https://pypi.python.org/pypi/django-kb/
    :alt: Supported Python versions

.. image:: https://pypip.in/format/django-kb/badge.svg
    :target: https://pypi.python.org/pypi/django-kb/
    :alt: Download format

.. image:: https://travis-ci.org/eliostvs/django-kb.png?branch=master
    :target: https://travis-ci.org/eliostvs/django-kb

.. image:: https://coveralls.io/repos/eliostvs/django-kb/badge.png?branch=master
    :target: https://coveralls.io/r/eliostvs/django-kb?branch=master

Simple knowledge base made with django

Installation
-------------

#. Install or add ``django-kb`` to your Python path, i.e.:

.. code:: sh

    $ pip install django-kb

#. Configure django-taggit as described `here http://django-taggit.readthedocs.org/en/latest/getting_started.html`_.

#. Configure django-haystack as described `here http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration`_.

#. Configure django-markupfield as described `here https://github.com/jamesturk/django-markupfield#settings`_.

#. Add ``kb`` to your ``INSTALLED_APPS`` setting.

#. Add kb url include to your project's ``urls.py`` file with namespaece ``kb``::

    (r'^', include('kb.urls', namespace='kb')),

#. Add ``kb.middleware.KnowledgeMiddleware`` to your ``MIDDLEWARE_CLASSES`` setting, i.e.::

    MIDDLEWARE_CLASSES = (
        ...
        "kb.middleware.KnowledgeMiddleware",
    )

Usage
-----

Template Tags
~~~~~~~~~~~~~

Loading the tags, i.e.::

    {% load kbtags %}

{% top_new_articles %}
++++++++++++++++++++++

Return the new published articles.

{% top_viewed_articles %}
+++++++++++++++++++++++++

Return the most viewed articles.

{% top_rated_articles %}
++++++++++++++++++++++++

Return the most rated articles.

All this tags accept two optional parameters, ``num`` and ``category``.
``num`` is the number of the articles that will return, by default to 5.
``category`` can be a ``model`` or ``slug`` that will be used to filter the articles.

{% feedback %}
++++++++++++++

This is an inclusion tag which renders links to upvote or downvote the article.

To support AJAX you need to load jQuery and the ``feedback.js`` in your template, i.e.::

    {% load staticfiles %}
    <script type="text/javascript" src="http://code.jquery.com/jquery.min.js"></script>
    <script type="text/javascript" src="{% static "kb/js/feedback.js" %}"></script>


Example
-------

Example of the app django-kb running on Openshift `here <https://github.com/eliostvs/django-kb-example>`_.
