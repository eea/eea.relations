""" Custom events
"""
import logging
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from eea.relations.events.interfaces import IObjectInitializedEvent
from eea.relations.events.interfaces import IRelatedItemsWorkflowStateChanged
from eea.relations.events.interfaces import IForwardRelatedItemsWSC
from eea.relations.events.interfaces import IBackwardRelatedItemsWSC
logger = logging.getLogger("eea.relations")

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
        session = None
        # import ipdb; ipdb.set_trace()
        # sdm = getattr(context, 'session_data_manager', None)
        # try:
        #     session = sdm.getSessionData(create=True) if sdm else None
        # except Exception, err:
        #     logger.exception(err)
        #     session = None

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
