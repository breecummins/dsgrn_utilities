import DSGRN
from min_interval_posets import curve, posets


def PathMatchDomainGraph(domaingraph,patterngraph):
    searchgraph = DSGRN.SearchGraph(domaingraph)
    matchinggraph = DSGRN.MatchingGraph(searchgraph, patterngraph)
    if DSGRN.PathMatch(matchinggraph):
        return True
    else:
        return False


def PathMatchStableFullCycle(domaingraph,patterngraph):
    morsegraph = DSGRN.MorseGraph(domaingraph)
    for i in range(0, morsegraph.poset().size()):
        if morsegraph.annotation(i)[0] == "FC" and len(morsegraph.poset().children(i)) == 0:
            searchgraph = DSGRN.SearchGraph(domaingraph,i)
            matchinggraph = DSGRN.MatchingGraph(searchgraph,patterngraph)
            if DSGRN.PathMatch(matchinggraph):
                return True
    return False


def PathMatchStablePartialCycle(domaingraph,patterngraph):
    morsegraph = DSGRN.MorseGraph(domaingraph)
    for i in range(0, morsegraph.poset().size()):
        if morsegraph.annotation(i)[0] == "PC" and len(morsegraph.poset().children(i)) == 0:
            searchgraph = DSGRN.SearchGraph(domaingraph,i)
            matchinggraph = DSGRN.MatchingGraph(searchgraph,patterngraph)
            if DSGRN.PathMatch(matchinggraph):
                return True
    return False

def check_both(paramind, paramgraph, patterngraph):
    domaingraph = DSGRN.DomainGraph(paramgraph.parameter(paramind))
    dgmatch = PathMatchDomainGraph(domaingraph,patterngraph)
    fcmatch = PathMatchStableFullCycle(domaingraph,patterngraph)
    return dgmatch, fcmatch


def transform_ts(samp_time, samp_traces, names):
    temp_curves = [{t : None for t in samp_time} for _ in range(len(samp_traces[0]))]
    for t, ts in zip(samp_time, samp_traces):
        for k,s in enumerate(ts):
            temp_curves[k][t] = s
    curves = dict(zip(names, [curve.Curve(tc) for tc in temp_curves]))
    return curves


def makeposets(curves,epsilons):
    return posets.eps_posets(curves,epsilons)


def make_patterngraphs(poes,network):
    patterngraphs = dict()
    for (eps, (events, event_ordering)) in poes:
        poe = DSGRN.PosetOfExtrema(network,events,event_ordering)
        patterngraphs[eps] = DSGRN.PatternGraph(poe)
    return patterngraphs


def get_names(network):
    return [network.name(i) for i in range(network.size())]


def main(paramind, paramgraph, network, samp_time, samp_traces, epsilons=[0.0]):
    curves = transform_ts(samp_time,samp_traces,get_names(network))
    poes = makeposets(curves,epsilons)
    patterngraphs = make_patterngraphs(poes,network)
    for eps,patterngraph in patterngraphs.items():
        dg,fc = check_both(paramind,paramgraph,patterngraph)
    return dg, fc, poes


def main_fc_only(paramind, paramgraph, network, samp_time, samp_traces, epsilons=[0.0]):
    curves = transform_ts(samp_time,samp_traces,get_names(network))
    poes = makeposets(curves,epsilons)
    patterngraphs = make_patterngraphs(poes,network)
    for eps,patterngraph in patterngraphs.items():
        #If stable FC is required, then domain match not needed
        domaingraph = DSGRN.DomainGraph(paramgraph.parameter(paramind))
        fc = PathMatchStableFullCycle(domaingraph, patterngraph)
    return fc, poes


def main_pc_only(paramind, paramgraph, network, samp_time, samp_traces, epsilons=[0.0]):
    curves = transform_ts(samp_time,samp_traces,get_names(network))
    poes = makeposets(curves,epsilons)
    patterngraphs = make_patterngraphs(poes,network)
    for eps,patterngraph in patterngraphs.items():
        domaingraph = DSGRN.DomainGraph(paramgraph.parameter(paramind))
        pc = PathMatchStablePartialCycle(domaingraph, patterngraph)
    return pc, poes








