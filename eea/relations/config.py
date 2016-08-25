""" Config
"""
from eea.relations import graph
from zope.i18nmessageid import MessageFactory

EEAMessageFactory = MessageFactory('eea')
GRAPHVIZ_PATHS = graph.GRAPHVIZ_PATHS
PROJECTNAME = 'eea.relations'
ADD_CONTENT_PERMISSION = "Add portal content"

ASYNC = True
try:
    from plone.app.async import interfaces
    IAsyncService = interfaces.IAsyncService
except ImportError:
    ASYNC = False
