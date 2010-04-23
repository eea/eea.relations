""" Graph utilities
"""
import os
from tempfile import mktemp
from zope.interface import implements
from interfaces import IGraph
from eea.relations.config import GRAPHVIZ_PATHS

class Graph(object):
    """ Generates a PNG graph
    """
    implements(IGraph)

    def __init__(self, format):
        self.format = format

    def __call__(self, graph):
        """ Draw pydot.Graph
        """
        if GRAPHVIZ_PATHS:
            graph.progs = GRAPHVIZ_PATHS

        writter = getattr(graph, 'write_' + self.format, None)
        if not writter:
            return None

        path = mktemp('.%s'  % self.format)
        prog = GRAPHVIZ_PATHS
        img = writter(path=path)

        img = open(path, 'rb')
        raw = img.read()

        img.close()
        os.remove(path)

        return raw

PNG = Graph('png')
