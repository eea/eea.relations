""" Various setup
"""
from Products.CMFCore.utils import getToolByName

def importVarious(self):
    if self.readDataFile('eea.relations.txt') is None:
        return

    site = self.getSite()

    # Portal tool
    rtool = getToolByName(site, 'portal_relations')
    rtool.title = 'Possible content relations'
    # remove from portal_catalog
    rtool.unindexObject()
