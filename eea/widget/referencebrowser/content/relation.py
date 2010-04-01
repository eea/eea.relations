""" EEA Relation
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from eea.widget.referencebrowser.config import PROJECTNAME
from eea.facetednavigation.widgets.field import StringField

from interfaces import IRelation

EditSchema = ATFolder.schema.copy() + atapi.Schema((
    StringField('from',
        schemata="default",
        vocabulary_factory='eea.widget.refbrowser.voc.ContentTypes',
        required=True,
        widget=atapi.SelectionWidget(
            format='select',
            label='From',
            label_msgid='widget_from_title',
            description='Select content-type',
            description_msgid='widget_from_description',
            i18n_domain="eea.widget"
        )
    ),
    StringField('to',
        schemata="default",
        vocabulary_factory='eea.widget.refbrowser.voc.ContentTypes',
        required=True,
        widget=atapi.SelectionWidget(
            format='select',
            label='To',
            label_msgid='widget_to_title',
            description='Select content-type',
            description_msgid='widget_to_description',
            i18n_domain="eea.widget"
        )
    ),
))

EditSchema['description'].widget.modes = ()

class EEAPossibleRelation(ATFolder):
    """ Relation
    """
    implements(IRelation)
    portal_type = meta_type = 'EEAPossibleRelation'
    archetypes_name = 'EEA Possible Relation'
    _at_rename_after_creation = True
    schema = EditSchema

atapi.registerType(EEAPossibleRelation, PROJECTNAME)
