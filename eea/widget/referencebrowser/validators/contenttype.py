from zope.interface import implements
from Products.validation.config import validation
from Products.validation.interfaces import ivalidator

class ContentType(object):
    """ Validator EEARelationsContentType
    """
    __implements__ = (ivalidator,)

    def __init__( self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, instance, *args, **kwargs):
        """ Validate
        """
        field = kwargs.get('field', None)
        if not field:
            return 1

        name = field.getName()
        if name not in ('ct_type', 'ct_interface'):
            return 1


        if name == 'ct_type':
            other = 'ct_interface'
        else:
            other = 'ct_type'

        request = kwargs.get('REQUEST', None)
        if not request:
            return 1

        form = request.form
        other_value = form.get(other, '')

        if not (value or other_value):
            return ("You have to provide even Portal type or Interface or both "
                    "in order to define a valid Content-Type")
        return 1

validation.register(ContentType('eea-refbrowser-contenttype'))
