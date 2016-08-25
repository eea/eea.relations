""" Custom events
"""
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from eea.relations.events.interfaces import IObjectInitializedEvent
from eea.relations.events.interfaces import IRelatedItemsWorkflowStateChanged
from eea.relations.events.interfaces import IForwardRelatedItemsWSC
from eea.relations.events.interfaces import IBackwardRelatedItemsWSC


@implementer(IObjectInitializedEvent)
class ObjectInitializedEvent(ObjectModifiedEvent):
    """ An object is being initialised, i.e. populated for the first time
    """


@implementer(IRelatedItemsWorkflowStateChanged)
class RelatedItemsWorkflowStateChanged(object):
    """ Related Items Workflow State Changed
    """
    def __init__(self, context, **kwargs):
        self.object = context
        sdm = getattr(context, 'session_data_manager', None)
        session = sdm.getSessionData(create=True) if sdm else None

        for key, value in kwargs.items():
            setattr(self, key, value)
            if not session:
                continue
            session.set(key, value)


@implementer(IForwardRelatedItemsWSC)
class ForwardRelatedItemsWorkflowStateChanged(
        RelatedItemsWorkflowStateChanged):
    """ Related Items Workflow State Changed
    """


@implementer(IBackwardRelatedItemsWSC)
class BackwardRelatedItemsWorkflowStateChanged(
        RelatedItemsWorkflowStateChanged):
    """ Related Items Workflow State Changed
    """
