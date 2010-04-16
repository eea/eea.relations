from Products.Five.browser import BrowserView
from eea.widget.referencebrowser.component import queryForwardRelations
from Products.CMFCore.utils import getToolByName

class Popup(BrowserView):
    """ Widget popup helper
    """
    _relations = []

    @property
    def relations(self):
        if self._relations:
            return self._relations
        self._relations = queryForwardRelations(self.context)
        return self._relations

    def tabs(self):
        """ Return popup tabs
        """
        rtool = getToolByName(self.context, 'portal_relations')
        for relation in self.relations:
            nto = relation.getField('to').getAccessor(relation)()
            if nto not in rtool.objectIds():
                continue
            yield rtool[nto]
