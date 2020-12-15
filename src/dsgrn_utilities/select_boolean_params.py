import itertools
import dsgrn_utilities.parameter_building as buildparam
import dsgrn_utilities.network2logicfile as netlogic


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


def subset_boolean_parameters(network,path2DSGRN):
    '''
    Given a network, get all the DSGRN parameters that are Boolean functions. Peter proved that the set of all
    monotone Boolean functions is a subset of DSGRN parameters, so we recover all MBFs. Since all DSGRN parameters are
    monotone, any Boolean function that is not monotone is also not a DSGRN parameter. Therefore, the output list
    contains the DSGRN.Parameter objects associated to every possible MBF for the network.
    :param network: DSGRN.Network object
    :param path2DSGRN: string, the top-level directory for the DSGRN git repo. Example: "~/DSGRN", if the repo is in
    your home directory.
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
        hexcodes_in_file = netlogic.get_logic_file(ie,oe,g,e,path2DSGRN)
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

