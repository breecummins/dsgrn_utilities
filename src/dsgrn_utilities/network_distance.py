import dsgrn_utilities.graphtranslation as gt


def transform_edges_from_index_to_label(graph):
    '''
    Edges in the graph object in graphtranslation are tuples of node indices.
    This function replaces the node index by the node name in the network.
    :param graph: A graphtranslation.Graph() object
    :return: Edges that are written in the form (source node name, target node name, regulation 'a' or 'r').
    '''
    edges = graph.edges()
    labeledges = set()
    for u,v in edges:
        labeledges.add((graph.vertex_label(u),graph.vertex_label(v),graph.edge_label(u,v)))
    return labeledges


def symmetric_difference_graph_distance(netspec1,netspec2):
    '''
    Find the symmetric difference graph distance measure for two DSGRN network specifications.
    This distance assumes that node names are unique identifiers for nodes. In other words, two nodes
    are counted as having a distance of zero if and only if they have the same node name.
    This function does NOT consider isomorphisms to be distance zero unless the node names are the same.
    Note that if a node is missing, then the distance counts the missing node  AND all the inedges and outedges.

    :param netspec1: DSGRN network specification
    :param netspec2: DSGRN network specification
    :return: The sum of the difference between the node sets and edge sets for the two networks (the symmetric difference).
    '''
    g1 = gt.getGraphFromNetworkSpec(netspec1)
    g2 = gt.getGraphFromNetworkSpec(netspec2)
    nodes1 = set([g1.vertex_label(v) for v in g1.vertices()])
    nodes2 = set([g2.vertex_label(v) for v in g2.vertices()])
    node_diff = nodes1.symmetric_difference(nodes2)
    edges1 = transform_edges_from_index_to_label(g1)
    edges2 = transform_edges_from_index_to_label(g2)
    edge_diff = edges1.symmetric_difference(edges2)
    return len(node_diff) + len(edge_diff)


