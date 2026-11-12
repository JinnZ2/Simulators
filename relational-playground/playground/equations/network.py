"""Family C. dx_i/dt = sum_j A_ij g(x_j) - sum_j A_ji g(x_i): transfer along directed edges.

The adjacency comes from the relational matrix (class "matter transfer" unless
parameters["edge_class"] says otherwise). A reverse edge exists only if written.
"""
import math
from .base import ModelOutput, from_transfers, register


def network(state, env, rel, ctl, p):
    if rel is None:
        raise ValueError("network model needs a relational matrix")
    adj = rel.adjacency(p["edge_class"])
    g = (lambda v: v) if p["g"] == "identity" else (lambda v: math.tanh(v))
    names = [k for k in state if not k.startswith("_")]
    tr = []
    for src in sorted(adj):
        for dst, w in sorted(adj[src].items()):
            if src in state and dst in state:
                tr.append(("%s_to_%s" % (src, dst), src, dst, w * g(state[src])))
            elif src in state:
                tr.append(("%s_to_outside_%s" % (src, dst), src, None, w * g(state[src])))
            elif dst in state:
                tr.append(("outside_%s_to_%s" % (src, dst), None, dst, w * p["outside_level"][src]))
    return ModelOutput(from_transfers(tr, names), transfers=tr,
                       relationship_changes="edges fixed during the run",
                       uncertainty="edge strengths are inputs; topology is not inferred")


register("network", "network", "0.1", network, "rate", requires=("edge_class", "g", "outside_level"),
         limitations=("fixed topology", "transfer depends on the source node only"))
