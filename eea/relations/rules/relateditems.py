""" Related items workflow state changed
"""
import logging

from zope.event import notify
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface
from zope import schema
from OFS.SimpleItem import SimpleItem

from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.stringinterp.adapters import BaseSubstitution
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData

from eea.relations.events import ForwardRelatedItemsWorkflowStateChanged
from eea.relations.events import BackwardRelatedItemsWorkflowStateChanged

from Products.CMFCore.utils import getToolByName

LOGGER = logging.getLogger('eea.relations')


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

    def forward_transition_changed(self):
        """ Forward workflow state changed related items
        """
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if wtool is None:
            return False

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
                LOGGER.warn(
                        "%s: %s",
                        err.message.format(action_id=self.element.transition),
                        item.absolute_url()
                )
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
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if wtool is None:
            return False

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
                LOGGER.warn(
                        "%s: %s",
                        err.message.format(action_id=self.element.transition),
                        item.absolute_url()
                )
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


class CommentSubstitution(BaseSubstitution):
    """In line comment string substitution
    """
    def __init__(self, context, **kwargs):
        super(CommentSubstitution, self).__init__(context, **kwargs)
        self._session = None

    @property
    def session(self):
        """ User session
        """
        if self._session is None:
            sdm = getattr(self.context, 'session_data_manager', None)
            self._session = sdm.getSessionData(create=False) if sdm else {}
        return self._session

    @property
    def workflow_transition_items_changed(self):
        """ All items that changed transition with success.
        """
        succeeded_items = ""
        for item in self.session.get('succeeded'):
            succeeded_items += item.format()
            succeeded_items += '\n'
        return succeeded_items

    @property
    def workflow_transition_items_unchanged(self):
        """ All items that unchanged transition.
        """
        failed_items = ""
        for item in self.session.get('failed'):
            failed_items += item.format()
            failed_items += '\n'
        return failed_items

    @property
    def workflow_transition(self):
        """ Workflow transition.
        """
        return self.session.get('transition')

    def safe_call(self):
        """ Safe call
        """
        return getattr(self, self.attribute, u'')


class SubstitutionSucceededRelatedItems(CommentSubstitution):
    """
    Add substitution option for workflow transition changed with success.
    """
    category = _(u'All Content')
    description = _(u'All the items that changed transition with success.')
    attribute = u'workflow_transition_items_changed'


class SubstitutionFailedRelatedItems(CommentSubstitution):
    """
    Add substitution option for workflow transition chnaged with failure.
    """
    category = _(u'All Content')
    description = _(u'All the items that failed to changed transition.')
    attribute = u'workflow_transition_items_unchanged'


class SubstitutionWorkflowTransitionRelatedItems(CommentSubstitution):
    """
    Add substitution option to find the workflow transition.
    """
    category = _(u'All Content')
    description = _(u'Workflow transition of the related items.')
    attribute = u'workflow_transition'
