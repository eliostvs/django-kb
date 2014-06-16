from __future__ import unicode_literals

from ..base import querysets


class CategoryQueryset(querysets.VisibleQueryset,
                       querysets.AuthorableQueryset):
    pass
