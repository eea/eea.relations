from zope import schema
from zope.interface import Interface

class IBrowserView(Interface):
    """ Interface
    """
    brains = schema.Iterable(u'Iterable brains', readonly=True)

class IAutoRelations(Interface):
    """ Adapter to auto discover relations
    """
    def __call__():
        """ Return an iterable of catalog brains
        """
