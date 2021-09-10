""" Archetypes Referenceable patches
"""
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName


def _optimizedGetObject(self, uid):
    tool = getToolByName(self, 'uid_catalog', None)
    if tool is None:  # pragma: no cover
        return ''
    tool = aq_inner(tool)
    traverse = aq_parent(tool).unrestrictedTraverse

    _catalog = tool._catalog
    rids = _catalog.indexes['UID']._index.get(uid, ())
    if isinstance(rids, int):
        rids = (rids,)

    for rid in rids:
        path = _catalog.paths[rid]
        obj = traverse(path, default=None)
        if obj is not None:
            return obj
