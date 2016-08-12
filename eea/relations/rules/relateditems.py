import logging
from zope.event import notify
from eea.relations.events import ForwardRelatedItemsWorkflowStateChanged
from eea.relations.events import BackwardRelatedItemsWorkflowStateChanged
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface
from zope import schema

from OFS.SimpleItem import SimpleItem
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from ZODB.POSException import ConflictError
from Products.CMFPlone import utils

from plone.app.contentrules import PloneMessageFactory
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm


logger = logging.getLogger('eea.relations')


class IRelatedItemsAction(Interface):
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


class RelatedItemsActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IRelatedItemsAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def publishRelatedItems(self):
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if wtool is None:
            return False

        obj = self.event.object
        relatedItems = obj.getRelatedItems()
        print relatedItems
        print "a intrat aici"
        for item in relatedItems:
            try:
                wtool.doActionFor(item, self.element.transition)
            except Exception, err:
                logger.warn(
                        "%s: %s",
                        err.message.format(action_id=self.element.transition),
                        item.absolute_url()
                )
                continue
        event = ForwardRelatedItemsWorkflowStateChanged(self.context)
        notify(event)
        return True

    def error(self, obj, error):
        request = getattr(self.context, 'REQUEST', None)
        if request is not None:
            title = utils.pretty_title_or_id(obj, obj)
            message = _(
                    u"Unable to change state of ${name} as part of content "
                    u"rule 'workflow' action: ${error}",
                    mapping={'name': title, 'error': error}
                    )
            IStatusMessage(request).addStatusMessage(message, type="error")

    def publishBackRefs(self):
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if wtool is None:
            return False

        obj = self.event.object
        backRefs = obj.getBRefs()
        print backRefs
        print "incerc backrefs"
        for item in backRefs:
            try:
                wtool.doActionFor(item, self.element.transition)
            except Exception, err:
                logger.warn(
                        "%s: %s",
                        err.message.format(action_id=self.element.transition),
                        item.absolute_url()
                )
                continue
        event = BackwardRelatedItemsWorkflowStateChanged(self.context)
        notify(event)
        return True

    def __call__(self):
        if self.element.related_items:
            self.publishRelatedItems()

        if self.element.backward_related_items:
            self.publishBackRefs()

        if self.element.asynchronous:
            pass


class RelatedItemsAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IRelatedItemsAction, IRuleElementData)

    transition = ''
    related_items = False
    backward_related_items = False
    asynchronous = False

    element = "plone.actions.Workflow"

    @property
    def summary(self):
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
