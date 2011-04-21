""" EEA Relations
"""
import validators
validators.register()

import field
field.register()

import widget
widget.register()

def initialize(context):
    """ Zope 2 """
    import content
    content.initialize(context)
