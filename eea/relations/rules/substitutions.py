""" Email substitutions
"""

from plone.stringinterp.adapters import BaseSubstitution
from plone.app.contentrules import PloneMessageFactory as _


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
