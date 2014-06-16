from __future__ import unicode_literals

from ..base import querysets


class ArticleQuerySet(querysets.VisibleQueryset,
                      querysets.AuthorableQueryset,
                      querysets.PublishableQueryset):
    pass
