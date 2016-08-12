""" Custom events
"""
from zope.interface import implements, implementer
from zope.lifecycleevent import ObjectModifiedEvent
from eea.relations.events.interfaces import IObjectInitializedEvent
from eea.relations.events.interfaces import IRelatedItemsWorkflowStateChanged
from eea.relations.events.interfaces import IForwardRelatedItemsWSC
from eea.relations.events.interfaces import IBackwardRelatedItemsWSC

class ObjectInitializedEvent(ObjectModifiedEvent):
    """ An object is being initialised, i.e. populated for the first time
    """
    implements(IObjectInitializedEvent)

@implementer(IRelatedItemsWorkflowStateChanged)
class RelatedItemsWorkflowStateChanged(object):
    """ Related Items Workflow State Changed
    """
    def __init__(self, context):
        self.object = context

@implementer(IForwardRelatedItemsWSC)
class ForwardRelatedItemsWorkflowStateChanged(RelatedItemsWorkflowStateChanged):
    """ Related Items Workflow State Changed
    """
@implementer(IBackwardRelatedItemsWSC)
class BackwardRelatedItemsWorkflowStateChanged(RelatedItemsWorkflowStateChanged):
    """ Related Items Workflow State Changed
    """
