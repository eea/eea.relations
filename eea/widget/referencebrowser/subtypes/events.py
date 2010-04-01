from p4a.subtyper.interfaces import ISubtyper
from zope.component import getUtility
SUBTYPE = 'eea.widget.referencebrowser.facetednavigation.ContentTypeFacetedNavigable'

def subtype(obj, evt):
    """ Subtype as faceted navigable
    """
    context = obj
    portal_type = getattr(context, 'portal_type', None)
    if portal_type != 'EEARelationsContentType':
        return

    subtyper = getUtility(ISubtyper)
    possible_types = [x.name for x in subtyper.possible_types(context)]
    if SUBTYPE not in possible_types:
        return

    if subtyper.existing_type(context) != SUBTYPE:
        subtyper.change_type(context, SUBTYPE)
