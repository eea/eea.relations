""" Demonstrates the use of EEAReferenceBrowserWidget """

from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
try:
    from Products.OrderableReferenceField._field import OrderableReferenceField
except ImportError:
    from Products.Archetypes.atapi import ReferenceField as OrderableReferenceField

from eea.relations.widget.referencewidget import (
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
