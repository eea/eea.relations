from zope.component import getMultiAdapter

def subtype(obj, evt):
    """ Subtype as faceted navigable
    """
    context = obj
    portal_type = getattr(context, 'portal_type', None)
    if portal_type != 'EEARelationsContentType':
        return

    subtyper = getMultiAdapter((context, context.REQUEST),
                               name=u'faceted_subtyper')
    subtyper.enable()
