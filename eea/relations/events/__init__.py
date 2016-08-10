""" Custom events
"""
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from eea.relations.events.interfaces import IObjectInitializedEvent

class ObjectInitializedEvent(ObjectModifiedEvent):
    """ An object is being initialised, i.e. populated for the first time
    """
    implements(IObjectInitializedEvent)
