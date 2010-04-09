""" Graph drawers
"""
from pydot import Dot as PyGraph
from zope.component import queryAdapter, queryUtility
from Products.Five.browser import BrowserView

from eea.widget.referencebrowser.interfaces import INode
from eea.widget.referencebrowser.interfaces import IEdge
from eea.widget.referencebrowser.interfaces import IGraph

from Products.CMFCore.utils import getToolByName

class BaseGraph(BrowserView):
    """ Abstract layer
    """
    @property
    def graph(self):
        """ Returns a pydot.Graph instance
        """
        return PyGraph()

    def image(self):
        """ Returns a PNG image
        """
        image = queryUtility(IGraph, name=u'png')
        raw = image(self.graph)

        self.request.response.setHeader('Content-Type', 'image/png')
        return raw

class RelationGraph(BaseGraph):
    """ Draw a graph for Relation
    """
    @property
    def graph(self):
        """ Generate pydot.Graph
        """
        graph = PyGraph()
        edge = queryAdapter(self.context, IEdge)
        graph.add_edge(edge())
        return graph

class ContentTypeGraph(BaseGraph):
    """ Draw a graph for ContentType
    """
    @property
    def graph(self):
        """ Generate pydot.Graph
        """
        rtool = getToolByName(self.context, 'portal_relations')
        name = self.context.getId()

        brains = rtool.getFolderContents(contentFilter={
            'portal_type': 'EEAPossibleRelation'
        })

        graph = PyGraph()
        for brain in brains:
            doc = brain.getObject()

            field = doc.getField('to')
            value = field.getAccessor(doc)()
            if name == value:
                edge = queryAdapter(doc, IEdge)
                graph.add_edge(edge())
                continue

            field = doc.getField('from')
            value = field.getAccessor(doc)()
            if name == value:
                edge = queryAdapter(doc, IEdge)
                graph.add_edge(edge())
                continue

        if not graph.get_edges():
            node = queryAdapter(self.context, INode)
            graph.add_node(node())
        return graph

class ToolGraph(BaseGraph):
    """ Draw a graph for portal_relations
    """
    @property
    def graph(self):
        """ Generate pydot.Graph
        """
        brains = self.context.getFolderContents(contentFilter={
            'portal_type': 'EEAPossibleRelation'
        })

        graph = PyGraph()
        for brain in brains:
            doc = brain.getObject()
            edge = queryAdapter(doc, IEdge)
            graph.add_edge(edge())

        brains = self.context.getFolderContents(contentFilter={
            'portal_type': 'EEARelationsContentType'
        })

        edges = graph.get_edges()
        nodes = set(edge.get_source() for edge in edges)
        nodes.update(edge.get_destination() for edge in edges)
        for brain in brains:
            name = brain.getId
            if name in nodes:
                continue
            doc = brain.getObject()
            node = queryAdapter(doc, INode)
            graph.add_node(node())

        return graph
