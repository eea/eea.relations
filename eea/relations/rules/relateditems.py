import logging
from plone import api
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

from plone.stringinterp.interfaces import IStringSubstitution
from plone.stringinterp.adapters import BaseSubstitution


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

    def forwardWorkflowStateChangedRelatedItems(self):
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if wtool is None:
            return False

        obj = self.event.object
        relatedItems = obj.getRelatedItems()
        if not relatedItems:
            return False
        print relatedItems
        print "a intrat aici"

        succeeded = set()
        failed = set()

        for item in relatedItems:
            try:
                wtool.doActionFor(item, self.element.transition)
                succeeded.add(item.absolute_url())
            except Exception, err:
                logger.warn(
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
        print "sunt in publish related items"
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

    def backwardWorkflowStateChangedRelatedItems(self):
        print "incerc si publish back refs"
        wtool = getToolByName(self.context, 'portal_workflow', None)
        if wtool is None:
            return False

        obj = self.event.object
        backRefs = obj.getBRefs()
        if not backRefs:
            return False

        print backRefs
        print "incerc backrefs"

        succeeded = set()
        failed = set()

        for item in backRefs:
            try:
                wtool.doActionFor(item, self.element.transition)
                succeeded.add(item.absolute_url())
            except Exception, err:
                logger.warn(
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
            self.forwardWorkflowStateChangedRelatedItems()

        if self.element.backward_related_items:
            self.backwardWorkflowStateChangedRelatedItems()

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
    def workflow_transition_changed(self):
        """ All items that changed transition with success.
        """
        if not self.session.get('succeeded'):
            return "Couldn't " + str(self.session.get('transition')) + " none related items.\n"
        succeeded_items = ""
        succeeded_items += str(self.session.get('transition')).title()
        succeeded_items += ' related items:\n'
        for item in self.session.get('succeeded'):
            succeeded_items += '- '
            succeeded_items += str(item)
            succeeded_items += '\n'
        return succeeded_items

    @property
    def workflow_transition_unchanged(self):
        """ All items that unchanged transition.
        """
        if not self.session.get('failed'):
            return "All related items are " + str(self.session.get('transition')) + ".\n"
        failed_items = ""
        failed_items += 'Failed to '
        failed_items += str(self.session.get('transition'))
        failed_items += ' related items:\n'
        for item in self.session.get('failed'):
            failed_items += '- '
            failed_items += str(item)
            failed_items += '\n'
        return failed_items

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
    attribute = u'workflow_transition_changed'


class SubstitutionFailedRelatedItems(CommentSubstitution):
    """
    Add substitution option for workflow transition chnaged with failure.
    """
    category = _(u'All Content')
    description = _(u'All the items that failed to changed transition.')
    attribute = u'workflow_transition_unchanged'
