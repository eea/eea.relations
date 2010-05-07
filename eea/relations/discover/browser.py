from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.relations.interfaces import IAutoRelations

class View(BrowserView):
    """ Display auto discovered relations
    """
    @property
    def brains(self):
        """ Return brains
        """
        explorer = queryAdapter(self.context, IAutoRelations)
        if not explorer:
            raise StopIteration
        for brain in explorer():
            yield brain
