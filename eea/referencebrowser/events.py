from zope.interface import implements
try:
    from zope.lifecycleevent.interfaces import IObjectModifiedEvent
    from zope.lifecycleevent import ObjectModifiedEvent
except ImportError:
    #BBB Plone 2.5
    from zope.app.event.interfaces import IObjectModifiedEvent
    from zope.app.event.objectevent import ObjectModifiedEvent

class IObjectInitializedEvent(IObjectModifiedEvent):
    """An object is being initialised, i.e. populated for the first time
    """

class ObjectInitializedEvent(ObjectModifiedEvent):
    """ An object is being initialised, i.e. populated for the first time
    """
    implements(IObjectInitializedEvent)
