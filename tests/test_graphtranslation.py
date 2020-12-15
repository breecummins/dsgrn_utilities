import dsgrn_utilities.graphtranslation as gt

def test():
    netspec = "A : (A + B) : E\nB : (B)(~A) : E\nC : (A) : E"
    assert(netspec == gt.createEssentialNetworkSpecFromGraph(gt.getGraphFromNetworkSpec(netspec)))
    assert(netspec == gt.nxgraph2netspec(gt.netspec2nxgraph(netspec)))
    netspec = "Z : (~x) : E\nx : (y)(~Z) : E\ny : (y) : E"
    assert(netspec == gt.createEssentialNetworkSpecFromGraph(gt.getGraphFromNetworkSpec(netspec)))
    assert(netspec == gt.nxgraph2netspec(gt.netspec2nxgraph(netspec)))
