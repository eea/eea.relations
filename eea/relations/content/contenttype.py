""" EEA Relations Content Type
"""
from zope import event
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from eea.facetednavigation.widgets.field import StringField
from eea.relations.events import ObjectInitializedEvent
from Products.TALESField import TALESString

from interfaces import IContentType

EditSchema = ATFolder.schema.copy() + atapi.Schema((
    StringField('ct_type',
        schemata="default",
        vocabulary_factory='eea.relations.voc.PortalTypesVocabulary',
        validators=('eea.relations.contenttype',),
        widget=atapi.SelectionWidget(
            label='Portal type',
            label_msgid='widget_portal_type_title',
            description='Select portal type',
            description_msgid='widget_portal_type_description',
            i18n_domain="eea.relations"
        )
    ),
    StringField('ct_interface',
        schemata="default",
        vocabulary_factory='eea.relations.voc.ObjectProvides',
        validators=('eea.relations.contenttype',),
        widget=atapi.SelectionWidget(
            label='Interface',
            label_msgid='widget_interface_title',
            description='Select interface',
            description_msgid='widget_interface_description',
            i18n_domain="eea.relations"
        )
    ),
    TALESString('ct_default_location',
        schemata="default",
        default="python:object.aq_parent.absolute_url()",
        widget=atapi.StringWidget(
            label='Default location expression',
            label_msgid='widget_portal_type_title',
            description='Enter a TALES expression that resolves the default location for this content type',
            description_msgid='widget_ct_default_location',
            i18n_domain="eea.relations"
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

    def processForm(self, *args, **kwargs):
        """ Raise event on creation
        """
        is_new_object = self.checkCreationFlag()
        super(EEARelationsContentType, self).processForm(*args, **kwargs)
        if is_new_object:
            event.notify(ObjectInitializedEvent(self))
