""" Related items workflow state changed
"""
import logging

from zope.event import notify
from zope.component import adapter
from zope.formlib import form
from zope.interface import implementer, Interface
from zope import schema
from OFS.SimpleItem import SimpleItem

from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData

from eea.relations.events import ForwardRelatedItemsWorkflowStateChanged
from eea.relations.events import BackwardRelatedItemsWorkflowStateChanged

logger = logging.getLogger('eea.relations')


class IRelatedItemsAction(Interface):
    """ Related Items Action
    """
    transition = schema.Choice(
        title=_(u"Transition"),
        description=_(u"Select the workflow transition to attempt"),
        required=True,
        vocabulary='plone.app.vocabularies.WorkflowTransitions'
    )

    related_items = schema.Bool(
        title=_(u"Related items"),
        required=False,
        description=_("Attempt workflow transition on related items")
    )

    backward_related_items = schema.Bool(
        title=_(u"Backward References"),
        required=False,
        description=_("Attempt workflow transition on backward references")
    )

    asynchronous = schema.Bool(
        title=_(u"Asynchronous"),
        required=False,
        description=_("Perform action asynchronous")
    )


@implementer(IExecutable)
@adapter(Interface, IRelatedItemsAction, Interface)
class RelatedItemsActionExecutor(object):
    """The executor for this action.
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def forward_transition_changed(self):
        """ Forward workflow state changed related items
        """

        obj = self.event.object
        relatedItems = obj.getRelatedItems()
        if not relatedItems:
            return False

        succeeded = set()
        failed = set()

        for item in relatedItems:
            try:
                api.content.transition(
                        obj=item,
                        transition=self.element.transition)
                succeeded.add(item.absolute_url())
            except Exception, err:
                logger.debug("%s: %s", item.absolute_url(), err)
                failed.add(item.absolute_url())
                continue

        event = ForwardRelatedItemsWorkflowStateChanged(
                        obj,
                        succeeded=succeeded,
                        failed=failed,
                        transition=self.element.transition
                )
        notify(event)
        return True

    def backward_transition_changed(self):
        """ Backward workflow state changed related items
        """

        obj = self.event.object
        backRefs = obj.getBRefs()
        if not backRefs:
            return False

        succeeded = set()
        failed = set()

        for item in backRefs:
            try:
                api.content.transition(
                                obj=item,
                                transition=self.element.transition)
                succeeded.add(item.absolute_url())
            except Exception, err:
                logger.debug("%s: %s", item.absolute_url(), err)
                failed.add(item.absolute_url())
                continue
        event = BackwardRelatedItemsWorkflowStateChanged(
                        obj,
                        succeeded=succeeded,
                        failed=failed,
                        transition=self.element.transition
                )
        notify(event)
        return True

    def __call__(self):
        if self.element.related_items:
            self.forward_transition_changed()

        if self.element.backward_related_items:
            self.backward_transition_changed()

        if self.element.asynchronous:
            logger.warn("Not implemented yet")


@implementer(IRelatedItemsAction, IRuleElementData)
class RelatedItemsAction(SimpleItem):
    """ The actual persistent implementation of the action element.
    """

    transition = ''
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
        a = RelatedItemsAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class RelatedItemsEditForm(EditForm):
    """
    An add form for the related items action
    """
    form_fields = form.FormFields(IRelatedItemsAction)
    label = _(u"Add Related Items Action")
    description = _(u"Change workflow state for related items.")
    form_name = _(u"Configure element")
