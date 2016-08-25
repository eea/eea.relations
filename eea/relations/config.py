""" Config
"""
from eea.relations import graph
from zope.i18nmessageid import MessageFactory
try:
    from plone.app.async import interfaces
    IAsyncService = interfaces.IAsyncService
except (ImportError, AttributeError):
    ASYNC = False
else:
    ASYNC = True

EEAMessageFactory = MessageFactory('eea')
GRAPHVIZ_PATHS = graph.GRAPHVIZ_PATHS
PROJECTNAME = 'eea.relations'
ADD_CONTENT_PERMISSION = "Add portal content"
