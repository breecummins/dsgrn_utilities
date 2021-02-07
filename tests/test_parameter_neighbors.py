import DSGRN,itertools
import dsgrn_utilities.get_parameter_neighbors as pn
import dsgrn_utilities.select_boolean_params as selectbool
import dsgrn_utilities.parameter_building as build


def test1():
    network_spec = """
    A : (~B) : E
    B : (~A)(~C) : E
    C : (A) : E"""
    network = DSGRN.Network(network_spec)
    #single order
    boolean_params = selectbool.subset_boolean_parameters_single_order(network)
    param_graph = DSGRN.ParameterGraph(network)
    MBF_indices = set([param_graph.index(param) for param in boolean_params])
    logics = list(itertools.product(["C"],["8","E"],["2"]))
    orders1 = [[0,1],[0],[0]]
    orders2 = [[1,0],[0],[0]]
    params1 = [build.construct_parameter(network, h, orders1) for h in logics]
    params2 = [build.construct_parameter(network, h, orders2) for h in logics]
    ans1 = set([param_graph.index(param) for param in params1])
    assert(MBF_indices == ans1)
    ans2 = set([param_graph.index(param) for param in params1 + params2])
    neighbors = pn.get_parameter_neighbors_from_list(param_graph,MBF_indices)
    ans3 = ans2.difference(MBF_indices)
    assert(set(neighbors) == ans3)

    #all orders
    boolean_params = selectbool.subset_boolean_parameters_all_orders(network)
    param_graph = DSGRN.ParameterGraph(network)
    MBF_indices = set([param_graph.index(param) for param in boolean_params])
    assert(MBF_indices == ans2)
    neighbors = pn.get_parameter_neighbors_from_list(param_graph,MBF_indices)
    # no extra neighbors possible in essential graph
    assert(neighbors == set([]))


def test2():
    network_spec = "A : (~B)\nB : (~A)(~C)\nC : (A)"
    network = DSGRN.Network(network_spec)
    param_graph = DSGRN.ParameterGraph(network)
    hc1 = ["0", "8", "0"]
    hc2 = ["F", "8", "0"]
    hc3 = ["C", "8", "0"]
    orders = [[0,1],[0],[0]]
    params = [build.construct_parameter(network,h,orders) for h in [hc1,hc2,hc3]]
    param_indices = [param_graph.index(param) for param in params]
    neighbors = pn.get_parameter_neighbors_from_list(param_graph,param_indices)

    logics1 = list(itertools.product(["4","D"],["8"],["0"]))
    logics2 = list(itertools.product(["0","C","F"],["0","A","C"],["0"]))
    logics3 = list(itertools.product(["0","C","F"],["8"],["2"]))
    a = [build.construct_parameter(network,h,orders) for h in logics1+logics2+logics3]
    b_orders = [[1,0],[0],[0]]
    b = [build.construct_parameter(network,h,b_orders) for h in itertools.product(["0","C","F"],["8"],["0"])]
    ans = set([param_graph.index(param) for param in a + b]).difference(param_indices)
    # answers = set(param_indices).union(ans)
    assert(ans == neighbors)


def test2a():
    network_spec = "A : (~B)\nB : (~A)(~C)\nC : (A)"
    network = DSGRN.Network(network_spec)
    param_graph = DSGRN.ParameterGraph(network)
    MBFs, all_neighbors = pn.get_Boolean_parameter_neighbors(network)
    logics1 = list(itertools.product(["0","C","F"],["0","8","A","C","E","F"],["0","2","3"]))
    orders1 = [[0,1],[0],[0]]
    a = [build.construct_parameter(network,h,orders1) for h in logics1]
    ans = [param_graph.index(param) for param in a]
    assert(set(ans) == set(MBFs))

    logics2 = list(itertools.product(["4","D"],["0","8","A","C","E","F"],["0","2","3"]))
    orders2 = [[1,0],[0],[0]]
    a = [build.construct_parameter(network,h,orders1) for h in logics2]
    b = [build.construct_parameter(network,h,orders2) for h in logics2]
    ans = [param_graph.index(param) for param in a + b]
    all_answers = set(ans)
    assert(all_answers == all_neighbors)


def test3():
    network_spec = "B : (~A)(~C) : E\nA : (~B) : E\nC : (A) : E"
    b,ess_net_spec = pn.make_essential(network_spec)
    assert(not b)
    assert(ess_net_spec == "B : (~A)(~C) : E\nA : (~B) : E\nC : (A) : E")
    network_spec = "B : (~A)(~C)\nA : (~B)\nC : (A)"
    b,ess_net_spec = pn.make_essential(network_spec)
    assert(b)
    assert(ess_net_spec == "B : (~A)(~C) : E\nA : (~B) : E\nC : (A) : E")
    network_spec = "A : (~B)\nB : (~A)(~C)\nC : (A)"
    b,ess_net_spec = pn.make_essential(network_spec)
    assert(b)
    assert(ess_net_spec == "A : (~B) : E\nB : (~A)(~C) : E\nC : (A) : E")

    network_spec = "B : (~A)(~C) : E\nA : (~B) : E\nC : (A) : E"
    ess,noness = pn.make_nonessential(network_spec)
    assert (noness == "B : (~A)(~C)\nA : (~B)\nC : (A)")
    network_spec = "B : (~A)(~C)\nA : (~B)\nC : (A)"
    ess,noness = pn.make_nonessential(network_spec)
    assert (noness == network_spec)
    network_spec = "A : (~B) : E\nB : (~A)(~C)\nC : (A) : E"
    ess,noness = pn.make_nonessential(network_spec)
    assert (noness == "A : (~B)\nB : (~A)(~C)\nC : (A)")


def test4():
    network_spec = "A : (~B)\nB : (~A)(~C)\nC : (A)"
    network = DSGRN.Network(network_spec)
    param_graph = DSGRN.ParameterGraph(network)
    essential_indices, essential_neighbors = pn.get_essential_parameter_neighbors(param_graph)
    orders1 = [[0,1],[0],[0]]
    orders2 = [[1,0],[0],[0]]
    logics = list(itertools.product(["C"],["8","E"],["2"]))
    ans1 = [build.construct_parameter(network,h,orders1) for h in logics]
    ans2 = [build.construct_parameter(network,h,orders2) for h in logics]
    ess_answers = [param_graph.index(param) for param in ans1 + ans2]
    assert(set(ess_answers) == set(essential_indices))
    logics1 = list(itertools.product(["4","D"],["8","E"],["2"]))
    logics2 = list(itertools.product(["C"],["0","A","C","F"],["2"]))
    logics3 = list(itertools.product(["C"],["8","E"],["0","3"]))
    ans1 = [build.construct_parameter(network,h,orders1) for h in logics1+logics2+logics3]
    ans2 = [build.construct_parameter(network,h,orders2) for h in logics1+logics2+logics3]
    ess_answers = [param_graph.index(param) for param in ans1 + ans2]
    assert(set(ess_answers) == set(essential_neighbors))


def test5():
    network_spec = "A : (~B)\nB : (~A)(~C)\nC : (A) : E"
    network = DSGRN.Network(network_spec)
    param_graph = DSGRN.ParameterGraph(network)
    essential, noness_net_spec = pn.make_nonessential(network_spec)
    assert(noness_net_spec == "A : (~B)\nB : (~A)(~C)\nC : (A)")
    noness_network = DSGRN.Network(noness_net_spec)
    noness_param_graph = DSGRN.ParameterGraph(noness_network)
    orders1 = [[0,1],[0],[0]]
    orders2 = [[1,0],[0],[0]]
    logics_all_hexcodes = list(itertools.product(["0","4","5","C","D","F"],["0","8","A","C","E","F"],["2"]))
    logics1 = list(itertools.product(["0"],["0"],["2"]))
    ans1 = [build.construct_parameter(network, h, orders1) for h in logics1]
    ans2 = [build.construct_parameter(network, h, orders2) for h in logics1]
    paramlist = [param_graph.index(param) for param in ans1 + ans2]
    new_paramlist, neighbors = pn.get_parameter_neighbors_from_list_in_nonessential_pg(param_graph, paramlist)
    assert(set(new_paramlist) == set([noness_param_graph.index(param) for param in ans1 + ans2]))
    logics2 = list(itertools.product(["0"],["0"],["0","3"]))
    logics3 = list(itertools.product(["4"],["0"],["2"]))
    logics4 = list(itertools.product(["0"],["8"],["2"]))
    ans1 = [build.construct_parameter(noness_network,h,orders1) for h in logics3+logics2+logics4]
    ans2 = [build.construct_parameter(noness_network,h,orders2) for h in logics3+logics2+logics4]
    neighbor_check = [noness_param_graph.index(param) for param in ans1 + ans2]
    assert(set(neighbors) == set(neighbor_check))


def test6():
    network_spec = "i1 : i1 : E\ni2 : i2 : E\no : (~x3)(~x4) : E\nx1 : i1 : E\nx2 : i2 : E\nx3 : ~x1 : E\nx4 : (~x2)(~x3) : E"
    network = DSGRN.Network(network_spec)
    param_graph = DSGRN.ParameterGraph(network)
    essential, noness_net_spec = pn.make_nonessential(network_spec)
    noness_network = DSGRN.Network(noness_net_spec)
    noness_param_graph = DSGRN.ParameterGraph(noness_network)
    orders1 = [[0,1],[0,1],[0],[0],[0],[0,1],[0]]
    orders2 = [[0,1],[0,1],[0],[0],[0],[1,0],[0]]
    essential_logic = ["C","C","8","2","2","C","8"]
    neighbor_logic =  ["C","C","8","2","2","4","8"]
    neighbor_orders11 = [[0,1],[1,0],[0],[0],[0],[0,1],[0]]
    neighbor_orders12 = [[1,0],[0,1],[0],[0],[0],[0,1],[0]]
    neighbor_orders21 = [[0,1],[1,0],[0],[0],[0],[1,0],[0]]
    neighbor_orders22 = [[1,0],[0,1],[0],[0],[0],[1,0],[0]]
    ess_params = [build.construct_parameter(network,essential_logic,o) for o in [orders1,orders2]]
    ess_pinds = [param_graph.index(p) for p in ess_params]
    noness_pinds = [noness_param_graph.index(p) for p in ess_params]
    neighbor_params = [build.construct_parameter(noness_network,neighbor_logic,o) for o in [orders1,orders2]]
    neighbor_params += [build.construct_parameter(noness_network,essential_logic,o) for o in [neighbor_orders11,neighbor_orders12,neighbor_orders21,neighbor_orders22]]
    neighbor_pinds = [noness_param_graph.index(p) for p in neighbor_params]
    found_inds, found_neighbors = pn.get_parameter_neighbors_from_list_in_nonessential_pg(param_graph,ess_pinds)
    assert(set(noness_pinds) == set(found_inds))
    assert(set(neighbor_pinds).issubset(found_neighbors))



if __name__ == "__main__":
    test6()
