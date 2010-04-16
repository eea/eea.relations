from zope.interface import Interface

class IContentTypeLookUp(Interface):
    """ Lookup object in portal_relations content-types
    """

class IRelationsLookUp(Interface):
    """ Lookup for possible relations
    """
    def forward():
        """ Forward relations
        """

    def backward():
        """ Backward relations
        """
