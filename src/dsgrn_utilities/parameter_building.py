import DSGRN


def name2index(network,node_name):
    '''
    Gets the index of a network node name.
    :param network: DSGRN.Network object
    :param node_name: the string identifier for a node in the network
    :return: An integer that is the index of the node name (i.e. the line number in the network specification that
    starts with the node name).
    '''
    return network.index(node_name)


def index2name(network,node_index):
    '''
    Gets the node name of a network node index.
    :param network: DSGRN.Network object
    :param node_index: the integer that is the index of the node name (i.e. the line number in the network specification
    that starts with the node name).
    :return: The string identifier for a node in the network.
    '''
    return network.name(node_index)


def specify_order_eq(param,node_index,permutation):
    '''
    Checks if the threshold permutation has a specific order for the given DSGRN parameter index and
    network node name.
    :param param: DSGRN.Parameter object
    :param node_index: The index of a node in a DSGRN network (i.e. the line number in the network specification
    that starts with the node name). If needed, the function name2index() transforms a node name into its index.
    :param permutation: List that is a permutation of consecutive integers, i.e. [0,1,3,2] for 4 outedges.
    Each integer is the order index of a threshold. The indices in the order parameter are NOT the node indices in
    the DSGRN network. The order integers are consecutive. We have that p < q are two order indices if and only if
    the node index of the network node p is less than the node index of q.
    :return: True or False -- the order parameter is correct or not.
    '''
    return param.order()[node_index].permutation() == permutation


def specify_order_list(param,node_index,list_of_permutations):
    '''
    Checks if the threshold permutation is in a list of specific orders for the given DSGRN parameter index and
    network node name.
    :param param: DSGRN.Parameter object
    :param node_index: The index of a node in a DSGRN network (i.e. the line number in the network specification
    that starts with the node name). If needed, the function name2index() transforms a node name into its index.
    :param list_of_permutations: List of lists that are permutations of consecutive integers, i.e. [[0,1,3,2],[1,0,3,2]]
    for 4 outedges.
    Each integer is the order index of a threshold. The indices in the order parameter are NOT the node indices in
    the DSGRN network. The order integers are consecutive. We have that p < q are two order indices if and only if
    the node index of the network node p is less than the node index of q.
    :return: True or False -- the order parameter is in the list or not.
    '''
    return param.order()[node_index].permutation() in list_of_permutations


def specify_hex_eq(param,node_index,hexcode):
    '''
    Checks if the hex code for a parameter and network node is a specific value.
    :param param: DSGRN.Parameter object
    :param node_index: The index of a node in a DSGRN network (i.e. the line number in the network specification
    that starts with the node name). If needed, the function name2index() transforms a node name into its index.
    :param hexcode: A DSGRN string-formatted hex code (see format_hex()) identical to the format in the logic .dat files
    in DSGRN/src/DSGRN/Resources/logic. An example of a hexcode for a 2-in, 3-out node would be "FF8". If needed,
    there is a function format_hex() in this module that transforms a python hex code into a DSGRN formatted hex code.
    :return: True or False -- the logic parameter is correct or not
    '''
    return param.logic()[node_index].hex() == hexcode


def specify_hex_list(param,node_index,list_of_hexcodes):
    '''
    Checks if the hex code for a parameter and network node is in a list of specific values.
    :param param: DSGRN.Parameter object
    :param node_index: The index of a node in a DSGRN network (i.e. the line number in the network specification
    that starts with the node name). If needed, the function name2index() transforms a node name into its index.
    :param list_of_hexcodes: A list of DSGRN string-formatted hex codes (see format_hex()) identical to the format in
    the logic .dat files in DSGRN/src/DSGRN/Resources/logic. An example of a list of hexcode for a 2-in, 3-out node
    would be ["600", "EC0", "FF8"]. If needed, there is a function format_hex() in this
    module that transforms a python hex code into a DSGRN formatted hex code.
    :return: True or False -- the logic parameter is in the list or not
    '''
    return param.logic()[node_index].hex() in list_of_hexcodes


def format_hex(hex_code,len_str):
    '''
    Format a python hex number into DSGRN hex code.
    :param hex_code: A python hex number
    :param len_str: The length of the hex strings in the logic .dat file in DSGRN/src/DSGRN/Resources/logic for the
    specific node under consideration.
    :return: A DSGRN string formatted hex code. Example: "0xfc0" will be converted to "FC0" for a 2-in, 3-out node.
    '''
    hex_str = str(hex(int(hex_code,16)))[2:].upper()
    if len(hex_str) < len_str:
        # adjust to make hex parameters the right length
        # this is particularly important for 0
        hex_str = "0"*(len_str-len(hex_str)) + hex_str
    return hex_str


def logic_parameter(num_in,num_out,hex_code):
    '''
    Given the number of inedges, number of outedges, and logic hex code, construct a DSGRN.LogicParameter.
    :param num_in: integer, number of inedges
    :param num_out: integer, number of outedges
    :param hex_code: string, DSGRN formatted hexcode such as "FF8". If needed, there is a function format_hex() in this
    module that formats a python hex code as a DSGRN formatted hex code.
    :return: DSGRN.LogicParameter object
    '''
    return DSGRN.LogicParameter(num_in,num_out,hex_code)


def order_parameter(outedge_order):
    '''
    Given the order of outedges, create a DSGRN.OrderParameter.
    :param outedge_order: List that is a permutation of consecutive integers, i.e. [0,1,3,2] for 4 outedges.
    Each integer is the order index of a threshold. The indices in the order parameter are NOT the node indices in
    the DSGRN network. The order integers are consecutive. We have that p < q are two order indices if and only if
    the node index of the network node p is less than the node index of q.
    :return: DSGRN.OrderParameter object
    '''
    return DSGRN.OrderParameter(outedge_order)


def construct_parameter(network,hex_codes,orders):
    '''
    Construct the DSGRN.Parameter object associated to a specified network and collections of hex codes and orders for
    each node.
    :param network: DSGRN.Network object
    :param hex_codes: List of strings that are DSGRN formatted hex codes, one for each node. Example: ["0","FC00","C0"]
    for the network specification "A : A + B\nB : (B)(~A)(~C)\nC : A + C". Notice that the hex codes must be given in
    the same order as the nodes in the network specification. If needed, there is a function format_hex() in this
    module that formats a python hex code as a DSGRN formatted hex code.
    :param orders: List of lists of permutations of order indices, one for each node. Example: for the same network
    specification as above, the orders could be [[0,1,2],[1,0],[1,0]]. Notice that the permutations must be given in
    the same order as the nodes in the network specification.
    :return: DSGRN.Parameter object
    '''
    logic_params = []
    order_params = []
    for i in range(network.size()):
        num_indeges = len(network.inputs(i))
        num_outedges = len(network.outputs(i))
        # hack for handling no out-edges
        if num_outedges == 0:
            num_outedges = 1
        logic_params.append(logic_parameter(num_indeges,num_outedges,hex_codes[i]))
        order_params.append(order_parameter(orders[i]))
    return DSGRN.Parameter(logic_params,order_params,network)

