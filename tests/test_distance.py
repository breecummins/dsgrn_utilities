from dsgrn_utilities.network_distance import symmetric_difference_graph_distance


def test1():
    netspec1 = "A : (F) : E\nB : (C) : E\nC : (A + E)(~D) : E\nD : (~A)(~E) : E\nE : (F)(~B) : E\nF : (~B) : E"
    netspec2 = "A : (F) : E\nB : (C) : E\nC : (A)(~D) : E\nD : (~A)(~E) : E\nE : (E + F)(~B) : E\nF : (~B) : E"
    assert(symmetric_difference_graph_distance(netspec1,netspec2) == 2)


def test2():
    netspec1 = "A : (F) : E\nB : (C) : E\nC : (A + E)(~D) : E\nD : (~A)(~E) : E\nE : (F)(~B) : E\nF : (~B) : E"
    netspec2 = "A : (F) : E\nB : (C) : E\nC : (A)\nE : (E + F)(~B) : E\nF : (~B)"
    assert(symmetric_difference_graph_distance(netspec1,netspec2) == 6)
