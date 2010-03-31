from zope.interface import Interface

class IRelationsTool(Interface):
    """ portal_relations tool
    """

class IContentType(Interface):
    """ Content type
    """

class IRelation(Interface):
    """ Relation between 2 content types
    """
