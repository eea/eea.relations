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
from Products.CMFPlone import PloneMessageFactory as _
from zope.annotation import IAnnotations


class BaseGraph(BrowserView):
    """ Abstract layer
    """
    def __init__(self, context, request):
        """ BaseGraph Init
        """
        super(BaseGraph, self).__init__(context, request)
        self.anno = IAnnotations(self.context)
        self.pt_relations = getToolByName(self.context, 'portal_relations')

    @property
    def graph(self):
        """ Generate pydot.Graph
        """
        res = self.anno.get('relations_graph')
        if not res:
            self.markBrokenRelations()
            res = self.anno.get('relations_graph')
        return res

    def image(self):
        """ Returns a PNG image
        """
        image = queryUtility(IGraph, name=u'png')
        raw = image(self.graph)

        self.request.response.setHeader('Content-Type', 'image/png')
        return raw

    def brokenRelationMessage(self, strerr, bad_relations):
        """ Broken relation portal status message
        """
        message = _(u'The following relations are broken: ${relations} ' \
            'because of broken or missing: ${bad_relations} ' \
                                    'EEARelationsContentType',
            mapping = {u'relations': strerr, u'bad_relations': 
                                                        bad_relations})
        return message

    def markBrokenRelations(self):
        """ Base method which assignes a pydot.Graph for the graph method
        """
        self.anno['relations_graph'] = PyGraph()

class RelationGraph(BaseGraph):
    """ Draw a graph for Relation
    """

    def markBrokenRelations(self):
        """ Construct graph and return message with info about broken 
        relations for RelationGraph if any errors are found
        """ 
        bad_relations = []
        strerr = ""
        bad_rel = ""

        graph = PyGraph()
        value_from = self.context.getField('from').getAccessor(self.context)()
        nfrom = self.pt_relations.get(value_from)
        if nfrom:
            node = queryAdapter(nfrom, INode)
            graph.add_node(node())

        value_to = self.context.getField('to').getAccessor(self.context)()
        nto = self.pt_relations.get(value_to)
        if not (value_from == value_to) and nto:
            node = queryAdapter(nto, INode)
            graph.add_node(node())

        edge = queryAdapter(self.context, IEdge)
        res = edge()
        if res:
            graph.add_edge(res)
            self.anno['relations_graph'] = graph
            return ""

        if not nfrom:
            bad_rel = value_from
        if not nto:
            bad_rel = value_to
        relation = self.pt_relations[self.context.getId()]
        if bad_rel and bad_rel not in bad_relations:
            bad_relations.append(bad_rel)
            strerr +=  relation.Title()
            self.anno['relations_graph'] = graph
            return self.brokenRelationMessage(strerr, bad_relations)
        return ""

class ContentTypeGraph(BaseGraph):
    """ Draw a graph for ContentType
    """
    def __init__(self, context, request):
        """ ContentTypeGraph init
        """
        super(ContentTypeGraph, self).__init__(context, request)
        self.tool = queryAdapter(self.context, IToolAccessor)
        self.relations = self.tool.relations(proxy=False)

    def markBrokenRelations(self):
        """ Construct graph and return message with info about broken 
        relations for ContentTypeGraph if any errors are found
        """
        bad_relations = []
        strerr = "" 
        name = self.context.getId()
        node = queryAdapter(self.context, INode)
        graph = PyGraph()
        graph.add_node(node())
        for doc in self.relations:
            field = doc.getField('to')
            value_from = field.getAccessor(doc)()
            field = doc.getField('from')
            value_to = field.getAccessor(doc)()
            if name == value_from:
                nto = self.pt_relations.get(value_to)
                if not (value_from == value_to
                    ) and nto:
                    node = queryAdapter(nto, INode)
                    graph.add_node(node())
                edge = queryAdapter(doc, IEdge)
                res = edge()
                if res:
                    graph.add_edge(res)
                else:
                    if value_to not in bad_relations:
                        bad_relations.append(value_to)
                        strerr +=  doc.Title() + ", "

            if name == value_to:
                nfrom = self.pt_relations.get(value_from)
                if not (value_from == value_to
                    ) and nfrom:
                    node = queryAdapter(nfrom, INode)
                    graph.add_node(node())
                edge = queryAdapter(doc, IEdge)
                res = edge()
                if res:
                    graph.add_edge(res)
                else:
                    if value_from not in bad_relations:
                        bad_relations.append(value_from)
                        strerr +=  doc.Title() + ", "

        self.anno['relations_graph'] = graph
        if bad_relations:
            return self.brokenRelationMessage(strerr, bad_relations)
        return ""

class ToolGraph(BaseGraph):
    """ Draw a graph for portal_relations
    """
    def __init__(self, context, request):
        """ ToolGraph init
        """
        super(ToolGraph, self).__init__(context, request)
        self.tool = queryAdapter(self.context, IToolAccessor)
        self.relations = self.tool.relations(proxy=False)

    def markBrokenRelations(self):
        """ Construct graph and return message with info about broken 
        relations for ToolGraph if any errors are found
        """
        bad_relations = []
        strerr = "" 
        bad_rel = ""

        graph = PyGraph()
        types = self.tool.types(proxy=False)
        for doc in types:
            node = queryAdapter(doc, INode)
            graph.add_node(node())

        for doc in self.relations:
            edge = queryAdapter(doc, IEdge)
            res = edge()
            if not res:
                # if no result then check which relation id is missing
                from_rel = doc['from']
                to_rel = doc['to']
                pr_from = self.pt_relations.get(from_rel)
                pr_to = self.pt_relations.get(to_rel)
                if not pr_from:
                    bad_rel = from_rel
                if not pr_to:
                    bad_rel = to_rel
                if bad_rel and bad_rel not in bad_relations:
                    bad_relations.append(bad_rel)
                    strerr +=  doc.Title() + ", "
                continue
            graph.add_edge(res)

        self.anno['relations_graph'] = graph
        if bad_relations:
            return self.brokenRelationMessage(strerr, bad_relations)
        return ""

    def dot(self):
        """ Return dotted graph 
        """
        return self.graph.to_string()
