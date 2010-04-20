from Products.Five.browser import BrowserView
from eea.widget.referencebrowser.component import queryForwardRelations
from Products.CMFCore.utils import getToolByName

class Popup(BrowserView):
    """ Widget popup helper
    """
    _relations = []
    _field = ''

    @property
    def field(self):
        return self._field

    @property
    def relations(self):
        if self._relations:
            return self._relations
        self._relations = queryForwardRelations(self.context)
        return self._relations

    def tabs(self):
        """ Return popup tabs
        """
        rtool = getToolByName(self.context, 'portal_relations')
        for relation in self.relations:
            nto = relation.getField('to').getAccessor(relation)()
            if nto not in rtool.objectIds():
                continue
            yield rtool[nto]

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        field = kwargs.get('field', '')
        if field:
            self._field = field
        return self.index()

class PopupSelectedItems(BrowserView):
    """ Widget popup selected items helper
    """
    _field = ''

    @property
    def field(self):
        return self._field

    @property
    def items(self):
        """ Return selected items
        """
        for_field = self.context.getField(self.field)
        if not for_field:
            raise StopIteration

        value = for_field.getAccessor(self.context)()
        if not value:
            raise StopIteration

        for brain in value:
            yield brain

    def __call__(self, **kwargs):
        """ Render
        """
        if self.request:
            kwargs.update(self.request.form)

        field = kwargs.get('field', '')
        if not field:
            return 'No field specified'
        self._field = field
        return self.index()
