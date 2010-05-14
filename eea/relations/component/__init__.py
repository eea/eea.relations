import logging
from zope.component import queryAdapter
from eea.relations.interfaces import IContentType
from interfaces import IContentTypeLookUp
from interfaces import IRelationsLookUp

logger = logging.getLogger('eea.relations.queryContentType')

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

def checkForwardContentType(ctype, context):
    """ Check contenttype if is a forward relation for context.

    Returns None if False or portal relations content-type if true
    """
    if not IContentType.providedBy(ctype):
        ctype = queryContentType(ctype)
    if not ctype:
        return None

    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        return None

    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s' % context)

    if connecter.isForward(ctype):
        return ctype
    return None

def checkBackwardContentType(ctype, context):
    """ Check document who if is a forward relation for second parameter.

    Returns None if False or portal relations content-type if true
    """
    if not IContentType.providedBy(ctype):
        ctype = queryContentType(ctype)
    if not ctype:
        return None

    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        return None

    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s' % context)

    if connecter.isBackward(ctype):
        return ctype
    return None
