from __future__ import unicode_literals

from ..base import querysets


class CategoryQuerySet(querysets.VisibleQueryset,
                       querysets.AuthorableQueryset):
    pass
