""" View macro utils
"""
from Products.Five.browser import BrowserView
from eea.relations.component import checkForwardContentType
from eea.relations.component import checkBackwardContentType
from Products.CMFCore.utils import getToolByName
from AccessControl import Unauthorized

class Macro(BrowserView):
    """ Categorize relations
    """
    def checkPermission(self, doc):
        """ Check document permission
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission('View', doc):
            return doc
        return None

    def forward(self, **kwargs):
        """ Return forward relations by category
        """
        tabs = {}
        relations = self.context.getRelatedItems()
        for relation in relations:
            if not self.checkPermission(relation):
                continue
            ctype = checkForwardContentType(relation, self.context)
            if not ctype:
                continue
            name = ctype.title_or_id()
            if name not in tabs:
                tabs[name] = []
            tabs[name].append(relation)
        tabs = tabs.items()
        tabs.sort()
        return tabs

    def backward(self, **kwargs):
        """ Return backward relations by category
        """
        tabs = {}
        relations = self.context.getBRefs('relatesTo')
        for relation in relations:
            if not self.checkPermission(relation):
                continue
            ctype = checkBackwardContentType(relation, self.context)
            if not ctype:
                continue
            name = ctype.title_or_id()
            if name not in tabs:
                tabs[name] = []
            tabs[name].append(relation)
        tabs = tabs.items()
        tabs.sort()
        return tabs
