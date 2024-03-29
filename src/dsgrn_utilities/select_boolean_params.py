import itertools
import dsgrn_utilities.parameter_building as buildparam
import dsgrn_utilities.network2logicfile as netlogic
from math import factorial
from functools import reduce


def get_possible_hex_numbers(num_inedges,num_outedges,len_hex_str):
    '''
    Build hex representations for all Boolean functions, monotone and non-monotone, for a node given the node topology.
    This builds on Shaun's tally string representation of DSGRN logic parameters. Each hex code for this node is the
    transformation of a binary number into a hex number. The binary number is constructed by a string of 0's and 1's
    that is made up of binary "output words", where the word length is the number of outedges of the node. The total
    number of words is 2^n, where n is the number of inedges, and each of the source nodes can either be 0 or 1.

    An output word of all zeros indicates that the associated input value is below all output thresholds. The output
    words with all 1's indicate that the input value is above all thresholds. All possible permutations of these words
    correspond to the set of all Boolean functions for this node.

    Ordinarily, the words would be stacked according to a specific order given by DSGRN. However in this case, since
    we build all possible permutations, the order doesn't matter.

    :param num_inedges: integer, number of inedges
    :param num_outedges: integer, number of outedges
    :param len_hex_str: integer, the length of the hex codes in the associated DSGRN logic .dat file. The module
    network2logicfile has functions that can find and read the appropriate logic file for a node.
    :return: List of DSGRN formatted hex numbers
    '''
    num_words = 2**num_inedges
    below_thresholds = "0"*num_outedges
    above_thresholds = "1"*num_outedges
    tally_lists = itertools.product([below_thresholds,above_thresholds],repeat=num_words)
    tally_strings = ["".join(t) for t in tally_lists]
    hex_numbers = [hex(int(t,2)) for t in tally_strings]
    boolean_hex =[]
    for h in hex_numbers:
        boolean_hex.append(buildparam.format_hex(h, len_hex_str))
    return boolean_hex


def subset_boolean_parameters_single_order(network):
    '''
    Alternative name for subset_boolean_parameters.
    :param network: DSGRN.Network object
    :return: List of DSGRN.Parameter objects
    '''
    return subset_boolean_parameters(network)


def subset_boolean_parameters(network):
    '''
    Given a network, get all the DSGRN parameters that are monotone Boolean functions for a single threshold order.
    Do not use this function when searching for all neighbors to Boolean functions, instead use
    subset_boolean_parameters_all_orders().
    :param network: DSGRN.Network object
    :return: List of DSGRN.Parameter objects
    '''
    # pull out information about individual nodes from the network
    num_inedges, num_outedges, groups, essential = netlogic.get_info_from_network(network)
    list_of_hexcodes = []
    list_of_orders = []
    len_hex_strs = []
    # For each node in the network, get the MBFs
    for ie,oe,g,e in zip(num_inedges,num_outedges,groups,essential):
        # handle hack for no out-edges (fake output threshold)
        if oe == 0:
            oe = 1
        # read the appropriate logic .dat file and find out the length of the hex codes in the file for DSGRN formatting
        hexcodes_in_file = netlogic.get_logic_file(ie,oe,g,e)
        len_hex_strs.append(len(hexcodes_in_file[0]))
        # construct all possible Boolean functions
        boolean_functions = get_possible_hex_numbers(ie,oe,len_hex_strs[-1])
        # find all monotone Boolean functions by intersecting all Boolean functions with DSGRN logic parameters
        list_of_hexcodes.append(sorted(set(hexcodes_in_file).intersection(boolean_functions)))
        # specify only a single threshold order. Since all thresholds are bunched together in the same location in
        # the DSGRN parameter inequalities, a single order captures all dynamics.
        list_of_orders.append(list(range(oe)))
    boolean_params = []
    for hex_codes in itertools.product(*list_of_hexcodes):
        param = buildparam.construct_parameter(network,hex_codes,list_of_orders)
        boolean_params.append(param)
    return boolean_params


def subset_boolean_parameters_all_orders(network):
    '''
    Given a network, get all the DSGRN parameters that are Boolean functions for all threshold orders.
    This is the function to use when assessing neighbors for Boolean functions.
    (See get_Boolean_parameter_neighbors_for_MBFs() in get_parameter_neighbors.py.)
    
    Peter proved that the set of all strict monotone Boolean functions is a subset of DSGRN parameters, so we recover all MBFs, when considering a nonessential network.
    Since all DSGRN parameters are monotone, any Boolean function that is not monotone is also not a DSGRN parameter.
    Therefore, the output list contains the DSGRN.Parameter objects associated to every possible strict MBF for the network.
    
    :param network: DSGRN.Network object
    :return: List of DSGRN.Parameter objects
    '''
    # pull out information about individual nodes from the network
    num_inedges, num_outedges, groups, essential = netlogic.get_info_from_network(network)
    list_of_hexcodes = []
    list_of_orders = []
    len_hex_strs = []
    # For each node in the network, get the MBFs
    for ie,oe,g,e in zip(num_inedges,num_outedges,groups,essential):
        # handle hack for no out-edges (fake output threshold)
        if oe == 0:
            oe = 1
        # read the appropriate logic .dat file and find out the length of the hex codes in the file for DSGRN formatting
        hexcodes_in_file = netlogic.get_logic_file(ie,oe,g,e)
        len_hex_strs.append(len(hexcodes_in_file[0]))
        # construct all possible Boolean functions
        boolean_functions = get_possible_hex_numbers(ie,oe,len_hex_strs[-1])
        # find all monotone Boolean functions by intersecting all Boolean functions with DSGRN logic parameters
        list_of_hexcodes.append(sorted(set(hexcodes_in_file).intersection(boolean_functions)))
        # specify only a single threshold order. Since all thresholds are bunched together in the same location in
        # the DSGRN parameter inequalities, a single order captures all dynamics.
        list_of_orders.append(list(itertools.permutations(range(oe))))
    boolean_params = []
    for hex_codes in itertools.product(*list_of_hexcodes):
        for orders in itertools.product(*list_of_orders):
            param = buildparam.construct_parameter(network,hex_codes,orders)
            boolean_params.append(param)
    return boolean_params


def count_boolean_parameters(network):
    '''
    Given a network, count all the DSGRN parameters that are strict monotone Boolean functions.

    Peter proved that the set of all strict monotone Boolean functions is a subset of DSGRN parameters, so we recover all MBFs, when considering a nonessential network.
    Since all DSGRN parameters are monotone, any Boolean function that is not monotone is also not a DSGRN parameter.
    Therefore, the output list contains the DSGRN.Parameter objects associated to every possible strict MBF for the network.

    :param network: DSGRN.Network object
    :return: Two integers, the count for a single order and the count for all orders.
    '''
    # pull out information about individual nodes from the network
    num_inedges, num_outedges, groups, essential = netlogic.get_info_from_network(network)
    num_hexcodes = []
    num_orders = []
    # For each node in the network, get the number of hexcodes and the number of orders
    for ie,oe,g,e in zip(num_inedges,num_outedges,groups,essential):
        # handle hack for no out-edges (fake output threshold)
        if oe == 0:
            oe = 1
        # read the appropriate logic .dat file and find out the length of the hex codes in the file for DSGRN formatting
        hexcodes_in_file = netlogic.get_logic_file(ie,oe,g,e,netlogic.get_path_to_logic_files())
        len_hex_str = len(hexcodes_in_file[0])
        # construct all possible Boolean functions
        boolean_functions = get_possible_hex_numbers(ie,oe,len_hex_str)
        # find all monotone Boolean functions by intersecting all Boolean functions with DSGRN logic parameters
        num_hexcodes.append(len(set(hexcodes_in_file).intersection(boolean_functions)))
        # the number of orders is the factorial of the number of outedges
        num_orders.append(factorial(oe))
    single_order_count = reduce((lambda x, y: x * y), num_hexcodes)
    all_orders_count = single_order_count * reduce((lambda x, y: x * y), num_orders)
    return single_order_count, all_orders_count

