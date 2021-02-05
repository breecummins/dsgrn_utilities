import os


def build_logic_file_name(num_in,num_out,group,ess):
    '''
    Build the  logic file name associated to a node in a DSGRN network.
    All inputs are created from the call to get_info_from_network().

    :param num_in: Number of inedges for the node.
    :param num_out: Number of outedges for the node.
    :param group: A list of integers, each representing a sum in the product represented in the DSGRN network specification.
                  For example, if the node given is 'A : (B)(C+D)(~E)' then the corresponding group is [1,2,1].
    :param ess: True or False. Whether or not the node is essential.
    :return: The logic file name in DSGRN/src/DSGRN/Resources/logic.
    '''
    logic_file = "{}_{}".format(num_in,num_out) + "".join(["_{}".format(n) for n in sorted(group)]) + "{}.dat".format("_E"*ess)
    return logic_file


def get_logic_file(num_inedges,num_outedges,group,essential,path2DSGRN):
    '''
    Read the hex codes from a DSGRN logic .dat file.

    :param num_inedges: Number of inedges for the node.
    :param num_outedges: Number of outedges for the node.
    :param group: A list of integers, each representing a sum in the product represented in the DSGRN network specification.
                  For example, if the node given is 'A : (B)(C+D)(~E)' then the corresponding group is [1,2,1].
    :param essential: True or False. Whether or not the node is essential.
    :param path2DSGRN: The user's path to the DSGRN git repository, such as "~/DSGRN".
    :return: The list of hex strings resulting from reading each line in the logic .dat file.
    '''
    logic_file = build_logic_file_name(num_inedges,num_outedges,group,essential)
    hexstrings = [h.strip() for h in open(os.path.join(os.path.abspath(path2DSGRN),"{}".format(logic_file))).readlines()]
    return hexstrings


def get_in_and_out(network):
    '''
    Retrieve the number of inedges and outedges for every node in a DSGRN network.
    :param network: DSGRN.Network object
    :return: Two lists of integers
    '''
    num_inedges = [len(network.inputs(i)) for i in range(network.size())]
    num_outedges = [len(network.outputs(i)) for i in range(network.size())]
    return num_inedges, num_outedges


def get_info_from_network(network):
    '''
    Given a DSGRN network, find the information about each node in the network that is needed to locate the corresponding
    DSGRN logic file.
    :param network: DSGRN.Network object
    :return: Four lists of information, where each element of a list corresponds to a node in the networks.
    '''
    num_inedges, num_outedges = get_in_and_out(network)
    essential = [network.essential(i) for i in range(network.size())]
    # groups are the lengths of the summations multiplied together in the node logic
    # They are required to be sorted in ascending order.
    groups = []
    for i in range(network.size()):
        L = network.logic(i)
        groups.append(sorted([len(l) for l in L]))
    return num_inedges, num_outedges, groups, essential


