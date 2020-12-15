import DSGRN
from dsgrn_utilities.network2logicfile import build_logic_file_name, get_info_from_network


def test():
    network_spec = """
    x : (x)(y)(~z) : E
    y : (x)(~z) : E
    z : (y) : E"""
    network = DSGRN.Network(network_spec)
    num_inedges, num_outedges, groups, essential = get_info_from_network(network)
    logic_files = ["3_2_1_1_1_E.dat","2_2_1_1_E.dat","1_2_1_E.dat"]
    for ni,no,mm,e,lf in zip(num_inedges,num_outedges,groups,essential,logic_files):
        l = build_logic_file_name(ni,no,mm,e)
        assert(l == lf)
    network_spec = """
    x : (x + y)(~z) : E
    y : (x)(~z)
    z : (y + z) : E"""
    network = DSGRN.Network(network_spec)
    num_inedges, num_outedges, groups, essential = get_info_from_network(network)
    logic_files = ["3_2_1_2_E.dat","2_2_1_1.dat","2_3_2_E.dat"]
    for ni,no,mm,e,lf in zip(num_inedges,num_outedges,groups,essential,logic_files):
        l = build_logic_file_name(ni,no,mm,e)
        assert(l == lf)

