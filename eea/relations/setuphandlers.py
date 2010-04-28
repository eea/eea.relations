from Products.CMFCore.utils import getToolByName

def addObjectProvidesIndex(portal):
    """Add the object_provides index to the portal_catalog.
    """
    catalog = getToolByName(portal, 'portal_catalog')
    if 'object_provides' not in catalog.indexes():
        catalog.addIndex('object_provides', 'KeywordIndex')

def addUIDIndex(portal):
    """Add UID index to the portal_catalog.
    """
    catalog = getToolByName(portal, 'portal_catalog')
    if 'UID' not in catalog.indexes():
        catalog.addIndex('UID', 'FieldIndex')

def importVarious(self):
    if self.readDataFile('eearelations.txt') is None:
        return

    site = self.getSite()

    # Add object_provides index
    addObjectProvidesIndex(site)

    # Add UID index
    addUIDIndex(site)

    # Portal tool
    rtool = getToolByName(site, 'portal_relations')
    rtool.title = 'Possible content relations'
    # remove from portal_catalog
    rtool.unindexObject()

    # Dependencies
    qtool = getToolByName(site, 'portal_quickinstaller')
    installed = [package['id'] for package in qtool.listInstalledProducts()]
    if 'eea.facetednavigation' not in installed:
        qtool.installProduct('eea.facetednavigation')

    # Compatibility
    setup_tool = getToolByName(site, 'portal_setup')
    setup_tool.setImportContext('profile-eea.relations:b')
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext('profile-eea.relations:a')
