""" EEA Relations Content Type
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from eea.widget.referencebrowser.config import PROJECTNAME
from eea.facetednavigation.widgets.field import StringField

from interfaces import IContentType

EditSchema = ATFolder.schema.copy() + atapi.Schema((
    StringField('ct_type',
        schemata="default",
        vocabulary_factory='eea.widget.refbrowser.voc.PortalTypesVocabulary',
        validators=('eea-refbrowser-contenttype',),
        widget=atapi.SelectionWidget(
            label='Portal type',
            label_msgid='widget_portal_type_title',
            description='Select portal type',
            description_msgid='widget_portal_tyoe_description',
            i18n_domain="eea.widget"
        )
    ),
    StringField('ct_interface',
        schemata="default",
        vocabulary_factory='eea.widget.refbrowser.voc.ObjectProvides',
        validators=('eea-refbrowser-contenttype',),
        widget=atapi.SelectionWidget(
            label='Interface',
            label_msgid='widget_interface_title',
            description='Select interface',
            description_msgid='widget_interface_description',
            i18n_domain="eea.widget"
        )
    ),
))

EditSchema['description'].widget.modes = ()

class EEARelationsContentType(ATFolder):
    """ Relation node
    """
    implements(IContentType)
    portal_type = meta_type = 'EEARelationsContentType'
    archetypes_name = 'EEA Relation Content Type'
    _at_rename_after_creation = True
    schema = EditSchema

atapi.registerType(EEARelationsContentType, PROJECTNAME)
