from zope.interface import Interface
from zope.interface import alsoProvides
from zope.app.content.interfaces import IContentType
from eea.facetednavigation.interfaces import IFacetedNavigable as IOriginalFacetedNavigable

class IPossibleFacetedNavigable(Interface):
    """
    A possible heritor that can inherit faceted configuration from a
    faceted navigable object.
    """

class IFacetedNavigable(IOriginalFacetedNavigable):
    """
    A heritor that inherit faceted configuration from a
    faceted navigable object.
    """

alsoProvides(IFacetedNavigable, IContentType)
