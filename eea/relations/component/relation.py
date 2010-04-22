from zope.interface import implements
from interfaces import IRelationsLookUp
from Products.CMFCore.utils import getToolByName

class RelationsLookUp(object):
    """ Lookup for possible relations
    """
    def __init__(self, context):
        self.context = context
        self._relations = []

    @property
    def relations(self):
        if self._relations:
            return self._relations

        rtool = getToolByName(self.context, 'portal_relations')
        brains = rtool.getFolderContents(contentFilter={
            'portal_type': 'EEAPossibleRelation'
        })
        self._relations = [brain.getObject() for brain in brains]
        return self._relations

    def forward(self):
        """ Forward possible relations
        """
        name = self.context.getId()
        for relation in self.relations:
            nfrom = relation.getField('from').getAccessor(relation)()
            if name != nfrom:
                continue
            yield relation

    def backward(self):
        """ Backward possible relations
        """
        name = self.context.getId()
        for relation in self.relations:
            nto = relation.getField('to').getAccessor(relation)()
            if name != nto:
                continue
            yield relation
