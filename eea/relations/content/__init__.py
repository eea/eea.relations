""" Content
"""
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types, listTypes
from eea.widget.referencebrowser.config import (
    PROJECTNAME,
    ADD_CONTENT_PERMISSION
)

from Products.Archetypes.atapi import registerType
from tool import EEARelationsTool
from contenttype import EEARelationsContentType
from relation import EEAPossibleRelation

registerType(EEARelationsTool, PROJECTNAME)
registerType(EEARelationsContentType, PROJECTNAME)
registerType(EEAPossibleRelation, PROJECTNAME)

def initialize(context):
    """ Zope 2
    """
    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME),
                                                      PROJECTNAME)

    cmfutils.ToolInit( PROJECTNAME+' Tools',
                tools = [EEARelationsTool],
                icon='content/tool.gif'
                ).initialize( context )

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)