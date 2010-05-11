""" Relation vocabularies
"""
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
#
# Object provides
#
class ContentTypesVocabulary(object):
    """Vocabulary factory for object provides index.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """
        rtool = getToolByName(context, 'portal_relations')
        brains = rtool.getFolderContents(contentFilter={
            'portal_type': 'EEARelationsContentType'
        })

        items = [SimpleTerm(brain.getId, brain.getId, brain.Title)
                 for brain in brains]
        return SimpleVocabulary(items)

class WorkflowStatesVocabulary(object):
    """ Vocabulary factory
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ Return all unique states
        """
        wtool = getToolByName(context, 'portal_workflow')
        states = wtool.listWFStatesByTitle(filter_similar=True)
        states.sort()
        items = []
        for title, state in states:
            items.append(SimpleTerm(state, state, title))
        return SimpleVocabulary(items)
