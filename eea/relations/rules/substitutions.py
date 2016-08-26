""" Email substitutions
"""
from plone.stringinterp.adapters import BaseSubstitution
from plone.app.contentrules import PloneMessageFactory as _


class RelatedItemsSubstitution(BaseSubstitution):
    """In line comment string substitution
    """
    category = _(u'Related items')
    description = _(u'Related items')

    @property
    def related_items_changed(self):
        """ All items that changed transition with success.
        """
        succeeded = getattr(self.context, "succeeded", [])
        return u"\n".join(succeeded)

    @property
    def related_items_unchanged(self):
        """ All items that unchanged transition.
        """
        failed = getattr(self.context, "failed", [])
        return u"\n".join(failed)

    @property
    def related_items_transition(self):
        """ Workflow transition.
        """
        return getattr(self.context, "transition", "")

    def safe_call(self):
        """ Safe call
        """
        return getattr(self, self.attribute, u'')


class RelatedItemsSucceeded(RelatedItemsSubstitution):
    """ Add substitution option for workflow transition changed with success.
    """
    category = _(u'Related items')
    description = _(u'Related items that changed transition with success.')
    attribute = u'related_items_changed'


class RelatedItemsFailed(RelatedItemsSubstitution):
    """ Add substitution option for workflow transition chnaged with failure.
    """
    category = _(u'Related items')
    description = _(u'Related items items that failed to changed transition.')
    attribute = u'related_items_unchanged'


class RelatedItemsTransition(RelatedItemsSubstitution):
    """ Add substitution option to find the workflow transition.
    """
    category = _(u'Related items')
    description = _(u'Workflow transition attempted on the related items.')
    attribute = u'related_items_transition'
