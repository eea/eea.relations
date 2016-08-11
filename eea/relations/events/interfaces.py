""" Events
"""
from zope.component.interfaces import IObjectEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

class IObjectInitializedEvent(IObjectModifiedEvent):
    """An object is being initialised, i.e. populated for the first time
    """

class IEvent(IObjectEvent):
    """ Base Event Interface for all export events
    """

class IRelatedItemsWorkflowStateChanged(IEvent):
    """ Base Event Interface for all Async events
    """


