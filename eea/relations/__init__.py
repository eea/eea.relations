""" EEA Relations
"""
try:
    import zope.annotation
except ImportError:
    #BBB Plone 2.5
    import plone25

import validators
import field
import widget

def initialize(context):
    """ Zope 2 """
    import content
    content.initialize(context)
