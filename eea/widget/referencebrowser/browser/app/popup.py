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

class BaseView(BrowserView):
    """ Base view for selected item
    """
    _field = ''
    _mode = 'view'

    @property
    def field(self):
        return self._field

    @property
    def mode(self):
        return self._mode

    def setup(self, **kwargs):
        """ Setup view
        """
        if self.request:
            kwargs.update(self.request.form)

        # Set mode
        mode = kwargs.get('mode', 'view')
        self._mode = mode

        # Set field
        field = kwargs.get('field', '')
        self._field = field

class PopupSelectedItems(BaseView):
    """ Widget popup selected items helper
    """
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
        self.setup(**kwargs)
        return self.index()

class PopupSelectedItem(BaseView):
    """ Display an item
    """
    def __call__(self, **kwargs):
        self.setup(**kwargs)
        return self.index()
