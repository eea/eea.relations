from Products.Five.browser import BrowserView

class View(BrowserView):
    """ Views
    """
    @property
    def content_types(self):
        """ Content types
        """
        brains = self.context.getFolderContents(contentFilter={
            'portal_type': 'EEARelationsContentType'
        })
        for brain in brains:
            yield brain

    @property
    def relations(self):
        """ Relations
        """
        brains = self.context.getFolderContents(contentFilter={
            'portal_type': 'EEAPossibleRelation'
        })
        for brain in brains:
            yield brain
