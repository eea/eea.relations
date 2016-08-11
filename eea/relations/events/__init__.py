""" Custom events
"""
from zope.interface import implements, implementer
from zope.lifecycleevent import ObjectModifiedEvent
from eea.relations.events.interfaces import IObjectInitializedEvent
from eea.relations.events.interfaces import IEvent, IRelatedItemsWorkflowStateChanged

class ObjectInitializedEvent(ObjectModifiedEvent):
    """ An object is being initialised, i.e. populated for the first time
    """
    implements(IObjectInitializedEvent)

@implementer(IEvent)
class Event(object):
    """ Abstract event
    """
    def __init__(self, context, **kwargs):
        self.object = context

@implementer(IRelatedItemsWorkflowStateChanged)
class AsyncEvent(Event):
    """ Abstract event for all async events
    """
