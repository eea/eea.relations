""" EEA Relation
"""
from zope.interface import implements
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import registerType
from eea.widget.referencebrowser.config import PROJECTNAME

from interfaces import IRelation

class EEAPossibleRelation(ATFolder):
    """ Relation
    """
    implements(IRelation)
    portal_type = meta_type = 'EEAPossibleRelation'
    archetypes_name = 'EEA Possible Relation'
    _at_rename_after_creation = True

registerType(EEAPossibleRelation, PROJECTNAME)
