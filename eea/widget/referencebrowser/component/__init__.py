import logging
from zope.component import queryAdapter
from eea.widget.referencebrowser.interfaces import IContentType
from interfaces import IContentTypeLookUp
from interfaces import IRelationsLookUp

logger = logging.getLogger('eea.widget.referencebrowser.queryContentType')

def queryContentType(context):
    """ Lookup for context related content-type in portal_relations
    """
    connecter = queryAdapter(context, IContentTypeLookUp)
    if not connecter:
        logger.exception('No IContentTypeLookUp adapter found for '
                         '%s' % context)
        return None
    return connecter()

def queryForwardRelations(context):
    """ Lookup for context possible forward relations
    """
    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        raise StopIteration
    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s' % context)
        raise StopIteration
    for relation in connecter.forward():
        yield relation

def queryBackwardRelations(context):
    """ Lookup for context possible backward relations
    """
    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        raise StopIteration
    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s' % context)
        raise StopIteration
    for relation in connecter.backward():
        yield relation
