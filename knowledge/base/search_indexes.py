from __future__ import unicode_literals

from haystack import indexes


class BaseIndex(indexes.Indexable,
                indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
