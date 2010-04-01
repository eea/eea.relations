""" EEA Custom Reference Browser Widget
"""
""" EEA Faceted Inheritance
"""
# Plone 2.5 Backward compatible
try:
    from Products.CMFPlone.CatalogTool import _eioRegistry
    def object_provides(object, portal, **kw):
        return [i.__identifier__ for i in providedBy(object).flattened()]

    if not _eioRegistry.has_key('object_provides'):
        _eioRegistry.register('object_provides', object_provides)
except ImportError, err:
    pass

import validators
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types, listTypes
from config import PROJECTNAME, ADD_CONTENT_PERMISSION

def initialize(context):
    """ Zope 2
    """
    import content

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME),
                                                      PROJECTNAME)

    cmfutils.ToolInit( PROJECTNAME+' Tools',
                tools = [content.tool.EEARelationsTool],
                icon='content/tool.gif'
                ).initialize( context )

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
