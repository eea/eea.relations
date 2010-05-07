from zope.interface import Interface

class IAutoRelations(Interface):
    """ Adapter to auto discover relations
    """
    def __call__():
        """ Return an iterable of catalog brains
        """
