import logging
from zope.component import queryAdapter
from interfaces import IContentTypeLookUp
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
