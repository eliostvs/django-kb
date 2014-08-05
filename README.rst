=============================
Django KB
=============================

.. image:: https://badge.fury.io/py/django-kb.png
    :target: https://badge.fury.io/py/django-kb

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

To support AJAX you need to load jQuery and the ``vote.js`` in your template, i.e.::

    {% load staticfiles %}
    <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script type="text/javascript" src="{% static "kb/js/votes.js" %}"></script>
