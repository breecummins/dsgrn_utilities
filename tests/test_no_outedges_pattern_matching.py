import DSGRN

def initialize(ind):
    # ind = parameter index where match should occur
    spec = "x : ~y : E\ny : x : E\nz : x : E"
    network = DSGRN.Network(spec)
    pg = DSGRN.ParameterGraph(network)
    dgs = [DSGRN.DomainGraph(pg.parameter(p)) for p in range(pg.size())]
    sgs = [DSGRN.SearchGraph(dg) for dg in dgs]
    return network, sgs[ind]

def check_poset(network, searchgraph, events,event_ordering):
    patterngraph = DSGRN.PatternGraph(DSGRN.PosetOfExtrema(network,events,event_ordering))
    matchinggraph = DSGRN.MatchingGraph(searchgraph, patterngraph)
    return DSGRN.PathMatch(matchinggraph)

def test_minimal():
    network, sg = initialize(0)
    events, event_ordering = ([("x", "min"), ("y", "min"), ("z", "min")], set([(0, 1), (1, 2)]))
    match = check_poset(network, sg, events, event_ordering)
    print(match)
    assert(match)

def test0():
    yes_posets = [
        ([("x", "min"), ("y", "min"), ("z", "min")], set([(0, 1), (1, 2)])),
        ([("y", "min"), ("z", "min"), ("x", "max"), ("z", "max"), ("y", "max"),
          ("x", "min"), ("y", "min"), ("x", "max"), ("y", "max")],
         set([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)])),
        ([("y", "min"), ("x", "max"), ("z", "min"), ("y", "max"), ("z", "max"),
          ("x", "min"), ("y", "min")],
         set([(0, 1), (0, 2), (1, 3), (1, 4), (2, 1), (3, 5), (4, 3), (5, 6)]))
    ]
    network, sg = initialize(0)
    for events,event_ordering in yes_posets:
        match = check_poset(network,sg,events,event_ordering)
        print(match)
        assert(match)
        print("\n")

def test1():
    no_posets = [
        ([("y, min"), ("x, max"), ("z, max"), ("y, max"), ("x, min"), ("y, min")],
         set([(0, 1), (0, 2), (1, 3), (1, 4), (2, 1), (3, 5), (4, 3)])),
        ([("x", "min"), ("y", "max"), ("x", "max"), ("y", "min"), ("z", "max")],
         set([(0, 1), (1, 2), (2, 3), (3, 4)])),
        ([("x", "min"), ("y", "min"), ("z", "max")], set([(0, 1), (1, 2)])),
        ([("y", "min"), ("x", "max"), ("z", "min"), ("y", "max"), ("x", "min"), ("z", "max")],
         set([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])),
        ([("y", "min"), ("x", "min"), ("z", "max"), ("z", "min")], set([(0, 1), (0, 2), (1, 3), (2, 3)])),
        ([("y", "min"), ("x", "max"), ("z", "min"), ("y", "max"), ("z", "max"),
          ("x", "min"), ("y", "min")],
         set([(0, 1), (0, 4), (1, 2), (1, 3), (2, 3), (3, 5), (4, 1), (5, 6)])),
        ([("y", "min"), ("x", "max"), ("z", "min"), ("y", "max"), ("z", "max"),
          ("x", "min"), ("y", "min")],
         set([(0, 4), (0, 5), (1, 6), (2, 3), (3, 1), (4, 5), (5,3), (5, 2)])),
        ([("y", "max"), ("x", "max"), ("z", "min"), ("y", "min"), ("z", "max"),
          ("x", "min"), ("y", "max")],
         set([(0, 1), (0, 2), (1, 3), (1, 4), (2, 1), (3, 5), (4, 3), (5, 6)]))
    ]
    network, sg = initialize(0)
    for events, event_ordering in no_posets:
        match = check_poset(network,sg,events,event_ordering)
        print(match)
        assert(not match)

if __name__ == "__main__":
    print("should match")
    test0()
    print("\nshould not match")
    test1()
    print("\ntest minimal")
    test_minimal()
