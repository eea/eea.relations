from Products.CMFCore.utils import getToolByName

def importVarious(self):
    if self.readDataFile('referencebrowser.txt') is None:
        return

    site = self.getSite()

    rtool = getToolByName(site, 'portal_relations')
    rtool.title = 'Possible content relations'
    # remove from portal_catalog
    rtool.unindexObject()
