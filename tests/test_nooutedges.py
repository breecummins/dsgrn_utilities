import DSGRN
import ast


def check_Morsegraphs(spec):
    net = DSGRN.Network(spec)
    pg = DSGRN.ParameterGraph(net)
    test = {}
    for pi in range(pg.size()):
        param = pg.parameter(pi)
        dg = DSGRN.DomainGraph(param)
        md = DSGRN.MorseDecomposition(dg.digraph())
        mg = DSGRN.MorseGraph(md, dg)
        test[pi] = ast.literal_eval(mg.annotation(0).stringify())[0]
    return test


def test_network1():
    spec = "A :\nB : A"
    ground_truth = {0 : "FP { 0, 0 }", 1 : "FP { 1, 0 }", 2 : "FP { 0, 0 }", 3 : "FP { 1, 1 }", 4 : "FP { 0, 1 }", 5 : "FP { 1, 1 }"}
    test = check_Morsegraphs(spec)
    assert(test == ground_truth)


def test_network2():
    spec = "A :\nC :\nB : A+C"
    ground_truth = {0 : "FP { 0, 0, 0 }", 4 : "FP { 0, 0, 0 }", 8 : "FP { 0, 0, 0 }", 12 : "FP { 0, 0, 0 }", 16: "FP { 0, 0, 0 }",
                    1 : "FP { 1, 0, 0 }", 5 : "FP { 1, 0, 0 }", 13 : "FP { 1, 0, 0 }",
                    2 : "FP { 0, 1, 0 }", 6 : "FP { 0, 1, 0 }", 10 : "FP { 0, 1, 0 }",
                    3 : "FP { 1, 1, 0 }",
                    7 : "FP { 1, 1, 1 }", 11 : "FP { 1, 1, 1 }", 15 : "FP { 1, 1, 1 }", 19 : "FP { 1, 1, 1 }", 23 : "FP { 1, 1, 1 }",
                    9 : "FP { 1, 0, 1 }", 17 : "FP { 1, 0, 1 }", 21 : "FP { 1, 0, 1 }",
                    14 : "FP { 0, 1, 1 }", 18 : "FP { 0, 1, 1 }", 22 : "FP { 0, 1, 1 }",
                    20 : "FP { 0, 0, 1 }"
                    }
    test = check_Morsegraphs(spec)
    assert(test == ground_truth)


if __name__ == "__main__":
    test_network1()