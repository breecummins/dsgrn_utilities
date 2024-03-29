# MIT license (2020)
# Marcio Gamiero and Bree Cummins

import DSGRN
import dsgrn_utilities.select_boolean_params as sbp
import dsgrn_utilities.network2logicfile as netlogic


def is_essential(dsgrn_parameter):
    network = dsgrn_parameter.network()
    inedges, outedges, gps, ess = netlogic.get_info_from_network(network)
    outedges = [i if i > 0 else 1 for i in outedges]
    if all(ess):
        return True
    for node_ind in range(network.size()):
        hexstrings = netlogic.get_hexstrings(inedges[node_ind],outedges[node_ind],gps[node_ind],True)
        if dsgrn_parameter.logic()[node_ind].hex() not in hexstrings:
            return False
    return True


def make_essential(net_spec):
    nodes = [nodespec for nodespec in net_spec.split("\n") if nodespec]
    newnodes = []
    nonessential = False
    for nodespec in nodes:
        if nodespec.count(":") == 2 and nodespec.endswith("E"):
            newnodes.append(nodespec)
        else:
            nonessential = True
            newnodes.append(nodespec + " : E")
    return nonessential, "\n".join(newnodes)


def make_nonessential(net_spec):
    nodes = [nodespec for nodespec in net_spec.split("\n") if nodespec]
    newnodes = []
    essential = False
    for nodespec in nodes:
        if nodespec.count(":") == 2:
            essential = True
            cind = nodespec.rindex(":")
            newnodes.append(nodespec[:cind].strip())
        else:
            newnodes.append(nodespec.strip())
    return essential, "\n".join(newnodes)


def get_essential_parameter_neighbors(parametergraph):
    '''
    This function returns the list of co-dimension 1 neighboring parameters of the essential parameters in a network.
    :param parametergraph: Parameter graph of a network with at least one NONESSENTIAL node.
    :return: List of essential parameters and list of neighboring parameters.
    '''
    # If all nodes are essential return empty list
    net_spec = parametergraph.network().specification()
    nonessential, ess_net_spec = make_essential(net_spec)
    if not nonessential:
        print("Essential network. Not computing neighbors.")
        return [], []
    # Get list of indices of essential parameters and its neighbors embedded in the parameter graph of the original network
    ess_parametergraph = DSGRN.ParameterGraph(DSGRN.Network(ess_net_spec))
    ess_par_indices = []      # Essential parameter indices
    ess_par_neighbors = set() # Neighbors of essential parameters
    for ess_pindex in range(ess_parametergraph.size()):
        # Get the essential parameter
        ess_par = ess_parametergraph.parameter(ess_pindex)
        # Get its index in the original parameter graph
        full_pindex = parametergraph.index(ess_par)
        # Add the index to the list of essential parameters
        ess_par_indices.append(full_pindex)
        # Get the co-dimension 1 neighbors of this essential parameter
        for p_index in parametergraph.adjacencies(full_pindex,"codim1"):
            ess_par_neighbors.add(p_index)
    # Remove neighbors that are essential parameters
    ess_par_neighbors.difference_update(ess_par_indices)
    # Return list of essential parameters and its neighbors
    return ess_par_indices, list(ess_par_neighbors)


def get_parameter_neighbors_from_list_in_nonessential_pg(parametergraph,paramlist):
    '''
    This function returns the list of co-dimension 1 neighboring parameters IN THE NONESSENTIAL PARAMETER GRAPH
    for each of the parameters in paramlist associated to the supplied parameter graph. If the supplied parameter graph
    is nonessential, then all neighbors will be found.
    :param parametergraph: Parameter graph of a network with at least one ESSENTIAL node.
    :param paramlist: list of parameter indices to find neighbors for in the full nonessential graph
    :return: List of new parameter indices in the nonessential graph for each index in paramlist and
    list of neighboring parameter indices.
    '''
    # If all nodes are essential return empty list
    net_spec = parametergraph.network().specification()
    essential, noness_net_spec = make_nonessential(net_spec)
    noness_parametergraph = DSGRN.ParameterGraph(DSGRN.Network(noness_net_spec))
    parlist_indices = []
    parlist_neighbors = set([])
    for pindex in paramlist:
        # Get the parameter object
        par = parametergraph.parameter(pindex)
        # Get its index in the nonessential parameter graph
        full_pindex = noness_parametergraph.index(par)
        # Add the index to the list of essential parameters
        parlist_indices.append(full_pindex)
        # Get the co-dimension 1 neighbors of this essential parameter
        for p in noness_parametergraph.adjacencies(full_pindex,"codim1"):
            parlist_neighbors.add(p)
    # Remove neighbors that are in the input list
    parlist_neighbors.difference_update(parlist_indices)
    # Return list of essential parameters and its neighbors
    return parlist_indices, list(parlist_neighbors)


def get_parameter_neighbors_from_list(parametergraph,paramlist):
    '''
    This function returns the list of the co-dimension 1 neighboring parameters of the parameters in paramlist
    from the supplied parameter graph.
    :param parametergraph: DSGRN parameter graph of a network.
    :param paramlist: list of DSGRN parameter indices
    :return: List of parameter indices including paramlist along with neighbors
    '''
    friends_and_neighbors = set([q for p in paramlist for q in parametergraph.adjacencies(p,"codim1")])
    friends_and_neighbors.difference_update(paramlist)
    return friends_and_neighbors


def get_Boolean_parameter_neighbors(network):
    '''
    This function returns the list of MBF parameter indices (in one threshold permutation) and a list of the
    co-dimension 1 neighbors of the Boolean parameters, including all order permutations.
    :param network: DSGRN.Network object
    :param path2DSGRN: string, the top-level directory for the DSGRN git repo. Example: "~/DSGRN", if the repo is in
    your home directory.
    :return: List of MBF parameter indices and list of neighbor indices.
    '''
    parametergraph = DSGRN.ParameterGraph(network)
    MBFs = [parametergraph.index(p) for p in sbp.subset_boolean_parameters_single_order(network)]
    MBFs_all_orders = [parametergraph.index(p) for p in sbp.subset_boolean_parameters_all_orders(network)]
    neighbors = get_parameter_neighbors_from_list(parametergraph,MBFs_all_orders)
    return MBFs, neighbors

