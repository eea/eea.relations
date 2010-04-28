""" Demonstrates the use of EEAReferenceBrowserWidget """

from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
try:
    from Products.OrderableReferenceField._field import OrderableReferenceField, OrderableReferenceWidget
except ImportError:
    from Products.Archetypes.atapi import ReferenceField as OrderableReferenceField

from eea.relations.widget.referencewidget import (
    EEAReferenceBrowserWidget,
)
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

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
    #OrderableReferenceField(
    #'relatedItems',
    #relationship = 'relatesTo',
    #multiValued = True,
    #isMetadata = True,
    #languageIndependent = False,
    #index = 'KeywordIndex',
    #widget = ReferenceBrowserWidget(
        #allow_search = True,
        #allow_browse = True,
        #allow_sorting = True,
        #show_indexes = False,
        #force_close_on_insert = True,
        #label = "Related Item(s)",
        #label_msgid = "label_related_items",
        #description = "",
        #description_msgid = "help_related_items",
        #i18n_domain = "plone",
        #visible = {'edit' : 'visible', 'view' : 'invisible' }
        #)
    #)
))

class EEARefBrowserDemo(ATFolder):
    """ Demo from EEAReferenceBrowserWidget
    """
    archetypes_name = meta_type = portal_type = 'EEARefBrowserDemo'
    _at_rename_after_creation = True
    schema = SCHEMA
