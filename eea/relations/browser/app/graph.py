""" Graph drawers
"""
from pydot import Dot as PyGraph
from zope.component import queryAdapter, queryUtility
from Products.Five.browser import BrowserView

from eea.relations.interfaces import INode
from eea.relations.interfaces import IEdge
from eea.relations.interfaces import IGraph
from eea.relations.interfaces import IToolAccessor
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _

def broken_relation_message(self, strerr, bad_relations):
    """ Broken relation portal status message
    """
    status = queryAdapter(self.request, IStatusMessage)
    message = _(u'The following relations are broken: ${relations} ' \
        'because of broken or missing: ${bad_relations} ' \
                                'EEARelationsContentType',
        mapping = {u'relations': strerr, u'bad_relations': 
                                                    bad_relations})
    status.add(message, type='error')

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
        rtool = getToolByName(self.context, 'portal_relations')
        graph = PyGraph()

        nfrom = self.context.getField('from')
        value_from = nfrom.getAccessor(self.context)()
        if value_from in rtool.objectIds():
            nfrom = rtool[value_from]
            node = queryAdapter(nfrom, INode)
            graph.add_node(node())

        nto = self.context.getField('to')
        value_to = nto.getAccessor(self.context)()

        rtool_ids = rtool.objectIds()
        if not (value_from == value_to) and (value_to in rtool_ids):
            nto = rtool[value_to]
            node = queryAdapter(nto, INode)
            graph.add_node(node())

        edge = queryAdapter(self.context, IEdge)
        res = edge()
        # display info message with info about broken relation
        bad_relations = []
        if not res:
            strerr = ""
            has_from = value_from in rtool_ids
            bad_rel = value_from if not has_from else value_to
            relation = rtool[self.context.getId()]
            if bad_rel not in bad_relations:
                bad_relations.append(bad_rel)
                strerr +=  relation.Title()
        if bad_relations:
            broken_relation_message(self, strerr, bad_relations)
            return ""
        graph.add_edge(res)
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
        node = queryAdapter(self.context, INode)

        tool = queryAdapter(self.context, IToolAccessor)
        docs = tool.relations(proxy=False)

        graph = PyGraph()
        graph.add_node(node())

        for doc in docs:
            field = doc.getField('to')
            value_from = field.getAccessor(doc)()
            field = doc.getField('from')
            value_to = field.getAccessor(doc)()
            if name == value_from:
                if not (value_from == value_to
                    ) and value_to in rtool.objectIds():
                    nto = rtool[value_to]
                    node = queryAdapter(nto, INode)
                    graph.add_node(node())

                edge = queryAdapter(doc, IEdge)
                graph.add_edge(edge())
                continue

            if name == value_to:
                if not (value_from == value_to
                    ) and value_from in rtool.objectIds():
                    nfrom = rtool[value_from]
                    node = queryAdapter(nfrom, INode)
                    graph.add_node(node())

                edge = queryAdapter(doc, IEdge)
                graph.add_edge(edge())
                continue

        return graph

class ToolGraph(BaseGraph):
    """ Draw a graph for portal_relations
    """
    @property
    def graph(self):
        """ Generate pydot.Graph
        """
        graph = PyGraph()
        tool = queryAdapter(self.context, IToolAccessor)
        docs = tool.types(proxy=False)
        for doc in docs:
            node = queryAdapter(doc, INode)
            graph.add_node(node())

        docs = tool.relations(proxy=False)
        strerr = "" 
        bad_relations = []
        pr_tool = getToolByName(self.context, 'portal_relations')
        for doc in docs:
            edge = queryAdapter(doc, IEdge)
            res = edge()
            if not res:
                # if no result then check which relation id is missing
                from_rel = doc['from']
                to_rel = doc['to']
                pr_from = pr_tool.get(from_rel)
                bad_rel = from_rel if not pr_from else to_rel
                if bad_rel not in bad_relations:
                    bad_relations.append(bad_rel)
                strerr +=  doc.Title() + ", "
                continue
            graph.add_edge(res)
        if bad_relations:
            broken_relation_message(self, strerr, bad_relations)
        return graph

    def dot(self):
        """ Return dotted graph """
        return self.graph.to_string()
