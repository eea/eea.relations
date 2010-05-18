from zope.interface import implements
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.relations.interfaces import IAutoRelations
from AccessControl import Unauthorized
from interfaces import IBrowserView

class View(BrowserView):
    """ Display auto discovered relations
    """
    implements(IBrowserView)

    def checkPermission(self, brain):
        """ Check document permission
        """
        mtool = getToolByName(self.context, 'portal_membership')
        try:
            obj = brain.getObject()
        except Unauthorized:
            return None
        if mtool.checkPermission('View', obj):
            return obj
        return None

    @property
    def brains(self):
        """ Return brains
        """
        explorer = queryAdapter(self.context, IAutoRelations)
        if not explorer:
            raise StopIteration
        for brain in explorer():
            doc = self.checkPermission(brain)
            if not doc:
                continue
            yield doc
