""" demonstrates the use of ATReferenceBrowserWidget """

from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from Products.OrderableReferenceField._field import OrderableReferenceField
from eea.widget.referencebrowser.widget.referencewidget import (
    EEAReferenceBrowserWidget,
)

SCHEMA = ATFolder.schema.copy() + atapi.Schema((
    OrderableReferenceField('relatedItems',
        schemata='default',
        relationship = 'relatesTo',
        multiValued = True,
        isMetadata = True,
        widget=EEAReferenceBrowserWidget(
            label='Related items',
            description='Relations.'
        )
    ),
))

class EEARefBrowserDemo(ATFolder):
    """ Demo from EEAReferenceBrowserWidget
    """
    archetypes_name = meta_type = portal_type = 'EEARefBrowserDemo'
    _at_rename_after_creation = True
    schema = SCHEMA
