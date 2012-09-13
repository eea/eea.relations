""" Browser view for bad relations listing
"""
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IVocabularyFactory
from sets import Set
try:
    from Products.EEAContentTypes.interfaces import IRelations
except:
    NOT_INSTALLED = True

import logging

logger = logging.getLogger('eea.relations.browser.badrelations')

class View(BrowserView):
    """ Views
    """
    @property
    def object_provides_vocabulary(self):
        """ Object provides vocabulary
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u'eea.relations.voc.ObjectProvides')
        return voc(self.context)

    @property
    def portal_types_vocabulary(self):
        """ Portal types vocabulary
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u'eea.relations.voc.PortalTypesVocabulary')
        return voc(self.context)

    @property
    def bad_relations_report(self):
        """ All relations
        """
        res = []
        catalog = getToolByName(self.context, 'portal_catalog')
        ct_type = self.request.get('ct_type', '')
        ct_interface = self.request.get('ct_interface', '')

        if ct_type or ct_interface:
            query = {'portal_type': ct_type}
            res = catalog(**query)

        report = {}

        for brain in res:
            obj = brain.getObject()
            try:
                backreferences = Set(IRelations(obj).backReferences())
                fwdreferences = Set(IRelations(obj).forwardReferences())
                report[brain.getURL()] = backreferences | fwdreferences
            except (TypeError, ValueError):
                # The catalog expects AttributeErrors when a value can't be found
                raise AttributeError
            except:
                logger.info('ERROR: %s' % brain.getURL())

        return report
