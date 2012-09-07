""" Browser view for bad relations listing
"""
from Products.EEAContentTypes.interfaces import IRelations
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IVocabularyFactory
from sets import Set
import logging

logger = logging.getLogger('eea.relations.browser.badrelations')

class View(BrowserView):
    """ Views
    """
    @property
    def object_provides_vocabulary(self):
        """ Object provides vocabulary
        """
        voc = queryUtility(IVocabularyFactory, name=u'eea.relations.voc.ObjectProvides')
        return voc(self.context)

    @property
    def content_types_vocabulary(self):
        """ Content types vocabulary
        """
        voc = queryUtility(IVocabularyFactory, name=u'eea.relations.voc.ContentTypes')
        return voc(self.context)

    @property
    def all_relations(self):
        """ All relations
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        query = {'portal_type': 'Specification'}
        res = catalog(**query)

        res_res = {}

        for brain in res:
            obj = brain.getObject()
#            try:
#                backreferences = Set(IRelations(obj).backReferences())
#                fwdreferences = Set(IRelations(obj).forwardReferences())
#                res_res[brain.getURL()] = backreferences | fwdreferences
#            except (TypeError, ValueError):
#                # The catalog expects AttributeErrors when a value can't be found
#                raise AttributeError
#            except:
#                logger.info('ERROR: %s' % brain.getURL())

        return len(res)
