import DSGRN, os, itertools
import dsgrn_utilities.parameter_building as buildparam
import dsgrn_utilities.select_boolean_params as selectbool

def test1(path2DSGRN=os.path.expanduser("../../DSGRN")):
    network_spec = """
    x : (x)(y)(~z) : E
    y : (x)(~z) : E
    z : (y) : E"""
    network = DSGRN.Network(network_spec)
    pg = DSGRN.ParameterGraph(network)
    boolean_params = selectbool.subset_boolean_parameters(network,path2DSGRN)
    print("This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    assert(len(boolean_params) == 18)
    list_of_hexcodes = ["C000","FFFC","FCC0","FFC0","FCF0","FCCC","FC00","F0C0","CCC0"]
    morsegraphs = []
    for param in boolean_params:
        # param = pg.parameter(p)
        assert(buildparam.specify_order_eq(param,0,[0,1]))
        assert(buildparam.specify_hex_list(param,0,list_of_hexcodes))
        assert(buildparam.specify_order_eq(param,1,[0,1]))
        assert(buildparam.specify_hex_list(param,1,["C0","FC"]))
        assert(buildparam.specify_order_eq(param,2,[0,1]))
        assert(buildparam.specify_hex_list(param,2,["C"]))
        morsegraphs.append(DSGRN.MorseGraph(DSGRN.DomainGraph(param)).stringify())
    for p,mg in zip(boolean_params,morsegraphs):
        i = pg.index(p)
        param = pg.parameter(i)
        assert (buildparam.specify_order_eq(param, 0, [0,1]))
        assert (buildparam.specify_hex_list(param, 0, list_of_hexcodes))
        assert (buildparam.specify_order_eq(param, 1, [0,1]))
        assert (buildparam.specify_hex_list(param, 1, ["C0", "FC"]))
        assert (buildparam.specify_order_eq(param, 2, [0,1]))
        assert (buildparam.specify_hex_list(param, 2, ["C"]))
        mg2 = DSGRN.MorseGraph(DSGRN.DomainGraph(param)).stringify()
        assert(mg == mg2)


def test2(path2DSGRN=os.path.expanduser("../../DSGRN")):
    network_spec = """
    A : (C)(~B) : E
    B : (~A)(~C) : E
    C : (A)(~B) : E
    D : (~A)(~B) : E"""
    network = DSGRN.Network(network_spec)
    pg = DSGRN.ParameterGraph(network)
    boolean_params = selectbool.subset_boolean_parameters_single_order(network,path2DSGRN)
    print("This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    assert(len(boolean_params) == 16)
    for param in boolean_params:
        # original parameter description
        logics = [param.logic()[j].stringify() for j in range(network.size())]
        orders = [param.order()[j].stringify() for j in range(network.size())]
        # transformed through index parameter description
        iparam = pg.parameter(pg.index(param))
        ilogics = [iparam.logic()[j].stringify() for j in range(network.size())]
        iorders = [iparam.order()[j].stringify() for j in range(network.size())]
        assert(logics == ilogics)
        assert(orders == iorders)
        assert(param.network().specification() == iparam.network().specification())
        mg = DSGRN.MorseGraph(DSGRN.DomainGraph(param))
        img = DSGRN.MorseGraph(DSGRN.DomainGraph(iparam))
        assert(mg.stringify() == img.stringify())


def test3():
    path2DSGRN = os.path.expanduser("../../DSGRN")
    network_file = "toggle_switch_33node_reduction_4node.txt"
    network = DSGRN.Network(network_file)
    boolean_params = selectbool.subset_boolean_parameters(network,path2DSGRN)
    print("This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    assert(len(boolean_params) == 48000)
    network_file = "toggle_switch_33node_reduction_4node_E.txt"
    network = DSGRN.Network(network_file)
    boolean_params = selectbool.subset_boolean_parameters(network,path2DSGRN)
    assert(len(boolean_params) == 1458)


def test4(path2DSGRN=os.path.expanduser("../../DSGRN")):
    network_spec = """
    A : (~B) : E
    B : (~A)(~C) : E
    C : (A) : E"""
    network = DSGRN.Network(network_spec)
    boolean_params = selectbool.subset_boolean_parameters_all_orders(network, path2DSGRN)
    print(
        "This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    assert(len(boolean_params) == 4)
    logics = set([tuple([param.logic()[j].hex() for j in range(network.size())]) for param in boolean_params])
    logics_predict = set([tuple(l) for l in itertools.product(["C"], ["8", "E"], ["2"])])
    assert(logics==logics_predict)
    orders = set([tuple([param.order()[j].stringify() for j in range(network.size())])  for param in boolean_params])
    orders_predict = set([tuple(o) for o in itertools.product(["[0,1]","[1,0]"],["[0]"],["[0]"])])
    assert(orders == orders_predict)

    network_spec = """
    A : (~B)
    B : (~A)(~C)
    C : (A)"""
    network = DSGRN.Network(network_spec)
    boolean_params = selectbool.subset_boolean_parameters_all_orders(network, path2DSGRN)
    print(
        "This test assumes that dsgrn_utilities has the same path as DSGRN.\nWill fail with FileNotFound error if not.")
    logics = set([tuple([param.logic()[j].hex() for j in range(network.size())]) for param in boolean_params])
    print(logics)
    assert(len(boolean_params) == 108)
    logics_predict = set([tuple(l) for l in itertools.product(["0","C","F"], ["0","A", "C","8", "E","F"], ["0","2","3"])])
    assert(logics==logics_predict)
    orders = set([tuple([param.order()[j].stringify() for j in range(network.size())])  for param in boolean_params])
    orders_predict = set([tuple(o) for o in itertools.product(["[0,1]","[1,0]"],["[0]"],["[0]"])])
    assert(orders == orders_predict)

