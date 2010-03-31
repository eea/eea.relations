""" EEA Relations Content Type
"""
from zope.interface import implements
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import registerType
from eea.widget.referencebrowser.config import PROJECTNAME

from interfaces import IContentType

class EEARelationsContentType(ATFolder):
    """ Relation node
    """
    implements(IContentType)
    portal_type = meta_type = 'EEARelationsContentType'
    archetypes_name = 'EEA Relation Content Type'
    _at_rename_after_creation = True

registerType(EEARelationsContentType, PROJECTNAME)
