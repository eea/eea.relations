from pydot import Node as PyNode
from zope.interface import implements
from interfaces import INode

class Node(object):
    """ Adapter for ContentType to represent it as a pydot.Node
    """
    implements(INode)

    def __init__(self, context):
        self.context = context

    def __call__(self, **kwargs):
        """ Returns a pydot.Node object
        """
        name = self.context.getId()
        label = self.context.title_or_id()
        return PyNode(name, label=label)

    def __repr__(self):
        """ Returns a string representation of the node in dot language.
        """
        return self().to_string()
