import DSGRN,os,itertools
import dsgrn_utilities.get_parameter_neighbors as pn
import dsgrn_utilities.select_boolean_params as selectbool
import dsgrn_utilities.parameter_building as build


def test1(path2DSGRN=os.path.expanduser("../../DSGRN")):
    print(
        "This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    network_spec = """
    A : (~B) : E
    B : (~A)(~C) : E
    C : (A) : E"""
    network = DSGRN.Network(network_spec)
    #single order
    boolean_params = selectbool.subset_boolean_parameters_single_order(network, path2DSGRN)
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
    assert(set(neighbors) == ans2)

    #all orders
    boolean_params = selectbool.subset_boolean_parameters_all_orders(network, path2DSGRN)
    param_graph = DSGRN.ParameterGraph(network)
    MBF_indices = set([param_graph.index(param) for param in boolean_params])
    assert(MBF_indices == ans2)
    neighbors = pn.get_parameter_neighbors_from_list(param_graph,MBF_indices)
    # no extra neighbors possible in essential graph
    assert(MBF_indices == set(neighbors))


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
    ans = [param_graph.index(param) for param in a + b]
    answers = set(param_indices).union(ans)
    assert(answers == neighbors)


def test2a(path2DSGRN=os.path.expanduser("../../DSGRN")):
    print(
        "This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    network_spec = "A : (~B)\nB : (~A)(~C)\nC : (A)"
    network = DSGRN.Network(network_spec)
    param_graph = DSGRN.ParameterGraph(network)
    MBFs, all_neighbors = pn.get_Boolean_parameter_neighbors(network,path2DSGRN)
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


