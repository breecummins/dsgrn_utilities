import DSGRN
import dsgrn_utilities.parameter_building as build


def test1():
    network_spec = "A : A + B\nB : (B)(~A)(~C)\nC : A + C"
    network = DSGRN.Network(network_spec)
    hex_codes = ["000","0000","00"]
    orders = [[0,1,2],[0,1],[0,1]]
    param = build.construct_parameter(network,hex_codes,orders)
    pg = DSGRN.ParameterGraph(network)
    pi = pg.index(param)
    assert(pi == 0)
    mg1 = DSGRN.MorseGraph(DSGRN.DomainGraph(param)).stringify()
    mg2 = DSGRN.MorseGraph(DSGRN.DomainGraph(pg.parameter(pi))).stringify()
    assert(mg1 == mg2)
    hex_codes = ["000","FC00","C0"]
    orders = [[0,2,1],[0,1],[1,0]]
    param = build.construct_parameter(network,hex_codes,orders)
    pg = DSGRN.ParameterGraph(network)
    pi = pg.index(param)
    assert(pi == 2000000)
    mg1 = DSGRN.MorseGraph(DSGRN.DomainGraph(param)).stringify()
    mg2 = DSGRN.MorseGraph(DSGRN.DomainGraph(pg.parameter(pi))).stringify()
    assert(mg1 == mg2)


def test2():
    network_spec = "A : A + B\nB : (B)(~A)\nC : A"
    network = DSGRN.Network(network_spec)
    hex_codes = ["000","00","0"]
    orders = [[0,1,2],[0,1],[0]] # remember C with zero out-edges has a dummy out-edge
    param = build.construct_parameter(network,hex_codes,orders)
    pg = DSGRN.ParameterGraph(network)
    pi = pg.index(param)
    assert(pi == 0)
    mg1 = DSGRN.MorseGraph(DSGRN.DomainGraph(param)).stringify()
    mg2 = DSGRN.MorseGraph(DSGRN.DomainGraph(pg.parameter(pi))).stringify()
    assert(mg1 == mg2)
    hex_codes = ["FD9","40","0"]
    param = build.construct_parameter(network,hex_codes,orders)
    pg = DSGRN.ParameterGraph(network)
    pi = pg.index(param)
    assert(pi == 94)
    assert(build.specify_hex_eq(param,0,"FD9"))
    assert(not build.specify_hex_list(param,0,["FD8","000"]))
    assert(not build.specify_order_eq(param,1,[1,0]))
    assert(build.specify_order_list(param,0,[[0,1,2],[1,0,2]]))
    mg1 = DSGRN.MorseGraph(DSGRN.DomainGraph(param)).stringify()
    mg2 = DSGRN.MorseGraph(DSGRN.DomainGraph(pg.parameter(pi))).stringify()
    assert(mg1 == mg2)


def test3():
    assert(hex(int("0ff",16)) == hex(int("ff",16)))
    assert("0FF" == build.format_hex(hex(int("ff",16)),3))


def test4():
    network_spec = "A : A + B\nB : (B)(~A)(~C)\nC : A + C"
    network = DSGRN.Network(network_spec)
    assert(build.index2name(network,build.name2index(network,"A")) == "A")
    assert(build.index2name(network,build.name2index(network,"B")) == "B")
    assert(build.index2name(network,build.name2index(network,"C")) == "C")
    network_spec = "A : A + B : E\nB : (B)(~A) : E\nC : A : E"
    network = DSGRN.Network(network_spec)
    assert(build.index2name(network,build.name2index(network,"A")) == "A")
    assert(build.index2name(network,build.name2index(network,"B")) == "B")
    assert(build.index2name(network,build.name2index(network,"C")) == "C")

