""" EEA Relation
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation.widgets.field import StringField

from interfaces import IRelation

class TitleWidget(atapi.StringWidget):
    """ Auto generate title
    """
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """ Process form
        """
        ct_from = form.get('from', '')
        ct_to = form.get('to', '')
        if not (ct_from and ct_to):
            return '', {}

        rtool = getToolByName(instance, 'portal_relations')
        brains = rtool.getFolderContents(contentFilter={
            'portal_type': 'EEARelationsContentType',
            'getId': ct_from
        })
        for brain in brains:
            ct_from = brain.Title
            break

        brains = rtool.getFolderContents(contentFilter={
            'portal_type': 'EEARelationsContentType',
            'getId': ct_to
        })
        for brain in brains:
            ct_to = brain.Title
            break

        value = '%s -> %s' % (ct_from, ct_to)
        return value, {}

EditSchema = ATFolder.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        required=0,
        searchable=1,
        accessor='Title',
        widget=TitleWidget(
            label_msgid='label_title',
            modes=(),
            i18n_domain='plone',
        ),
    ),
    StringField('from',
        schemata="default",
        vocabulary_factory='eea.relations.voc.ContentTypes',
        required=True,
        widget=atapi.SelectionWidget(
            format='select',
            label='From',
            label_msgid='widget_from_title',
            description='Select content-type',
            description_msgid='widget_from_description',
            i18n_domain="eea.relations"
        )
    ),
    StringField('to',
        schemata="default",
        vocabulary_factory='eea.relations.voc.ContentTypes',
        required=True,
        widget=atapi.SelectionWidget(
            format='select',
            label='To',
            label_msgid='widget_to_title',
            description='Select content-type',
            description_msgid='widget_to_description',
            i18n_domain="eea.relations"
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
