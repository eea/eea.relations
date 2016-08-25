""" Related items workflow state changed
"""
import logging

from zope.event import notify
from zope.component import adapter
from zope.component import queryUtility
from zope.formlib import form
from zope.interface import implementer, Interface
from OFS.SimpleItem import SimpleItem

from plone import api
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData

from eea.relations.config import EEAMessageFactory as _
from eea.relations.config import IAsyncService
from eea.relations.events import ForwardRelatedItemsWorkflowStateChanged
from eea.relations.events import BackwardRelatedItemsWorkflowStateChanged
from eea.relations.rules.interfaces import IRelatedItemsAction

logger = logging.getLogger('eea.relations')


def forward_transition_change(obj, transition):
    """ Forward workflow state changed related items
    """
    relatedItems = obj.getRelatedItems()
    if not relatedItems:
        return

    succeeded = set()
    failed = set()
    for item in relatedItems:
        try:
            api.content.transition(obj=item, transition=transition)
        except Exception, err:
            logger.debug("%s: %s", item.absolute_url(), err)
            failed.add(item.absolute_url())
        else:
            succeeded.add(item.absolute_url())

    # notify(ForwardRelatedItemsWorkflowStateChanged(
    #     obj, succeeded=succeeded, failed=failed, transition=transition))


def backward_transition_change(obj, transition):
    """ Backward workflow state changed related items
    """
    backRefs = obj.getBRefs()
    if not backRefs:
        return

    succeeded = set()
    failed = set()
    for item in backRefs:
        try:
            api.content.transition(obj=item, transition=transition)
        except Exception, err:
            logger.debug("%s: %s", item.absolute_url(), err)
            failed.add(item.absolute_url())
        else:
            succeeded.add(item.absolute_url())

    # notify(BackwardRelatedItemsWorkflowStateChanged(
    #     obj, succeeded=succeeded, failed=failed, transition=transition))


@implementer(IExecutable)
@adapter(Interface, IRelatedItemsAction, Interface)
class RelatedItemsActionExecutor(object):
    """The executor for this action.
    """
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def forward(self):
        """ Handle related items
        """
        if not self.element.related_items:
            return

        if not self.element.asynchronous:
            return forward_transition_change(
                self.event.object,
                self.element.transition)

        async = queryUtility(IAsyncService)
        job = async.queueJob(
            forward_transition_change,
            self.event.object,
            self.element.transition)

    def backward(self):
        """ Handle back refs
        """
        if not self.element.backward_related_items:
            return

        if not self.element.asynchronous:
            return backward_transition_change(
                self.event.object,
                self.element.transition)

        async = queryUtility(IAsyncService)
        job = async.queueJob(
            backward_transition_change,
            self.event.object,
            self.element.transition)

    def __call__(self):
        self.forward()
        self.backward()


@implementer(IRelatedItemsAction, IRuleElementData)
class RelatedItemsAction(SimpleItem):
    """ The actual persistent implementation of the action element.
    """

    transition = u""
    related_items = False
    backward_related_items = False
    asynchronous = False
    element = "eea.relations.workflow"

    @property
    def summary(self):
        """ Need to access the content rule with the related items action.
        """
        return _(
                u"Execute transition ${transition}",
                mapping=dict(transition=self.transition)
                )


class RelatedItemsAddForm(AddForm):
    """
    An add form for the related items action
    """
    form_fields = form.FormFields(IRelatedItemsAction)
    label = _(u"Add Related Items Action")
    description = _(u"Change workflow state for related items.")
    form_name = _(u"Configure element")

    def create(self, data):
        """ Create action
        """
        action = RelatedItemsAction()
        form.applyChanges(action, self.form_fields, data)
        return action


class RelatedItemsEditForm(EditForm):
    """
    An add form for the related items action
    """
    form_fields = form.FormFields(IRelatedItemsAction)
    label = _(u"Add Related Items Action")
    description = _(u"Change workflow state for related items.")
    form_name = _(u"Configure element")
