""" EEA Relations
"""
try:
    import zope.annotation
    zope.annotation #pyflakes
except ImportError:
    #BBB Plone 2.5
    import plone25
    plone25 #pyflakes

import validators
import field
import widget
field, validators, widget # pyflakes

def initialize(context):
    """ Zope 2 """
    import content
    content.initialize(context)
