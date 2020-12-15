# MIT LICENSE (2018)
# Shaun Harker and Bree Cummins

import copy, json
import networkx as nx

########################
# Directed Graph Class #
########################


class Graph:

    def __init__(self):
        """ Initialize an empty graph object """
        self.vertices_ = set()
        self.adjacency_lists_ = {}
        self.vertex_labels_ = {}
        self.edge_labels_ = {}

    def add_vertex(self, v, label=''):
        """ Add the vertex v to the graph and associate a label if one is given """
        if v in self.vertices_: return
        self.vertices_.add(v)
        self.adjacency_lists_[v] = set()
        self.vertex_labels_[v] = label
        self.edge_labels_[v] = {}

    def add_edge(self, u, v, label=''):
        """ Add the edge u -> v to the graph and associate a label if one is given """
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency_lists_[u].add(v)
        self.edge_labels_[u][v] = label

    def remove_edge(self, u, v):
        """ Remove the edge u -> v from the graph """
        self.adjacency_lists_[u].discard(v)
        self.edge_labels_[u].pop(v, None)

    def remove_vertex(self, u):
        """ Remove the node u and all edges from the graph """
        self.vertices_.discard(u)
        self.adjacency_lists_.pop(u, None)
        self.vertex_labels_.pop(u, None)
        self.edge_labels_.pop(u, None)
        for v in self.vertices():
            self.adjacency_lists_[v].discard(u)

    def vertex_label(self, v):
        """ Return the label on the vertex v """
        return self.vertex_labels_[v]

    def get_vertex_from_label(self, label):
        """ Return the vertex v with label 'label'. Error if non-unique. """
        vertices = [v for v in self.vertices_ if self.vertex_label(v) == label]
        N = len(vertices)
        if N == 1:
            return vertices[0]
        elif N == 0:
            return None
        elif N > 1:
            raise ValueError("Non-unique vertex labels.")

    def edge_label(self, u, v):
        """ Return the label on the edge u -> v """
        return self.edge_labels_[u][v]

    def vertices(self):
        """ Return the set of vertices in the graph """
        return self.vertices_

    def size(self):
        """ Return the number of vertices in the graph """
        return len(self.vertices_)

    def edges(self):
        """ Return a complete list of directed edges (u,v) in the graph """
        return [(u, v) for u in self.vertices() for v in self.adjacencies(u)]

    def adjacencies(self, v):
        """ Return the set of adjacencies (outedges) of v, i.e. { u : v -> u } """
        return self.adjacency_lists_[v]

    def inedges(self,v):
        """ Return the inedges of v, i.e. { u : u -> v } """
        return [u for u in self.vertices_ if v in self.adjacency_lists_[u]]

    def clone(self):
        """ Return a copy of this graph """
        return copy.deepcopy(self)

    def graphviz(self):
        """ Return a graphviz string describing the graph and its labels """
        gv = 'digraph {\n'
        indices = {v: str(k) for k, v in enumerate(self.vertices())}
        for v in self.vertices():
            gv += indices[v] + '[label="' + self.vertex_label(v) + '"];\n'
        for (u, v) in self.edges():
            gv += indices[u] + ' -> ' + indices[v] + ' [label="' + self.edge_label(u,v) + '"];\n'
        return gv + '}\n'

    def transpose(self):
        """ Return a new graph with edge direction reversed. """
        G = Graph()
        for v in self.vertices(): G.add_vertex(v, self.vertex_label(v))
        for (u, v) in self.edges(): G.add_edge(v, u, self.edge_label(u, v))
        return G


##################################################
# Translation to and from network specifications
##################################################


def createEssentialNetworkSpecFromGraph(graph,essential=True):
    '''
    Given a Graph object from this module, create a DSGRN network specification.
    Vertices of the graph are integers with string labels that will function as node names and edges are pairs of
    integers that are labeled by 'a' for activating or 'r' for repressing.

    :param graph: Graph object
    :param essential: True or False, default=True. Specify whether ALL nodes are essential or ALL nodes are nonessential.
    :return: DSGRN network specification
    '''

    # get nodes in order
    vs = { v : graph.vertex_label(v) for v in sorted(list(graph.vertices())) }

    # get inedges
    graph_edges = { name : sorted([(a, graph.edge_label(a, v)) for a in graph.inedges(v)]) for v,name in vs.items() }

    # generate network spec lines
    network_spec_lines = []
    for node,inedges in  graph_edges.items():
        act = " + ".join(sorted([vs[i] for (i, r) in inedges if r == 'a']))
        if act: act = "(" + act + ")"
        rep = "".join(sorted(["(~" + vs[i] + ")" for (i, r) in inedges if r == 'r']))
        if essential:
            end = " : E\n"
        else:
            end = "\n"
        network_spec_lines.append(node + " : " + act + rep + end)

    # alphabetize lines and cut last new line
    network_spec = "".join(sorted(network_spec_lines))[:-1]
    return network_spec


def getGraphFromNetworkSpec(network_spec):
    '''
    Given a DSGRN network specification, create a Graph object from this module.
    The Graph object will have vertices that are the indices of the nodes in the network, node labels that are the names
    of the nodes, edges that are pairs of indices, and edge labels that are 'a' for activating or 'r' for repressing.
    The essentiality of a node is not saved.

    :param network_spec: DSGRN network specification
    :return: Graph object with vertices as node
    '''
    if not network_spec:
        return Graph()
    eqns = filter(bool, network_spec.split("\n"))
    nodelist = []
    innodes = []
    for l in eqns:
        words = l.replace('(', ' ').replace(')', ' ').replace('+', ' ').replace('*', ' ').split()
        if words[-2:] == [':', 'E']:
            words = words[:-2]
        nodelist.append(words[0])
        innodes.append(words[2:])  # get rid of ':' at index 1
    graph = Graph()
    for k, node in enumerate(nodelist):
        graph.add_vertex(k, label=node)
    for outnode, ies in enumerate(innodes):
        for ie in ies:
            if ie[0] == '~':
                ie = ie[1:]
                reg = 'r'
            else:
                reg = 'a'
            innode = nodelist.index(ie)
            graph.add_edge(innode, outnode, label=reg)
    return graph



##################################################
# Translation to and from networkx graphs
##################################################


def netspec2nxgraph(netspec):
    '''
    Get a node and edge labeled networkx DiGraph from a DSGRN network specification.
    The node labels are node names and the edge labels are 'a' for activating or 'r' for repressing.
    :param netspec: DSGRN network specification
    :return: networkx.Digraph object
    '''
    graph = getGraphFromNetworkSpec(netspec)
    return graph2nxgraph(graph)


def nxgraph2netspec(nxgraph):
    '''
    Get an essential DSGRN network specification from networkx.Digraph object.
    The node labels are taken to be node names and the edge labels are 'a' for activating or 'r' for repressing.
    :param nxgraph: networkx.Digraph object
    :return: DSGRN network specification
    '''
    graph = nxgraph2graph(nxgraph)
    return createEssentialNetworkSpecFromGraph(graph)


def graph2nxgraph(graph):
    '''
    Get a node and edge labeled networkx DiGraph from a Graph object.
    :param graph: Graph object with node and edge labels.
    :return: networkx.Digraph object
    '''
    G = nx.DiGraph()
    for v in graph.vertices():
        G.add_node(v,label=graph.vertex_label(v))
    for (u,v) in graph.edges():
        G.add_edge(u,v,label=graph.edge_label(u,v))
    return G


def nxgraph2graph(nxgraph):
    '''
    Get a node and edge labeled Graph object from a networkx.DiGraph object.
    :param graph: networkx.DiGraph object with node and edge labels.
    :return: Graph object
    '''
    G = Graph()
    labels = nx.get_node_attributes(nxgraph, "label")
    for v in nxgraph.nodes:
        G.add_vertex(v,labels[v])
    for u,v in nxgraph.edges:
        G.add_edge(u,v,nxgraph[u][v]["label"])
    return G



