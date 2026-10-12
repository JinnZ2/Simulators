#!/usr/bin/env python3
"""provenance_graph.py - prove lineage independence by common-ancestor reachability.
CC0. stdlib only.

Nodes = claims/datasets/assumptions. Edge A->B means "A derives from B".
Ancestors(X) = every node reachable from X following edges (X itself included).
Two studies are INDEPENDENT iff Ancestors(a) and Ancestors(b) are disjoint.
Any shared node is a WITNESS that the agreement is one source echoed.

Decidable, deterministic. Proves a graph property; judges no truth.

Usage:
  provenance_graph.py new -o prov.json
  provenance_graph.py edge prov.json --from S1 --to Smith2019   # S1 derives from Smith2019
  provenance_graph.py edge prov.json --from S2 --to Smith2019
  provenance_graph.py check prov.json S1 S2          # -> SHARED or INDEPENDENT + witness
  provenance_graph.py roots prov.json S1             # list ancestors of S1
  provenance_graph.py selftest
"""
import argparse, json, sys
from dataclasses import dataclass, field, asdict

@dataclass
class Graph:
    edges: dict = field(default_factory=dict)   # node -> list of nodes it derives from

def add_edge(g, src, dst):
    g.edges.setdefault(src, [])
    if dst not in g.edges[src]:
        g.edges[src].append(dst)
    g.edges.setdefault(dst, [])   # ensure dst exists as a node

def ancestors(g, node, _seen=None):
    """node itself plus everything reachable by following 'derives-from' edges.
    Cycle-safe via the seen set."""
    if _seen is None:
        _seen = set()
    if node in _seen:
        return _seen
    _seen.add(node)
    for parent in g.edges.get(node, []):
        ancestors(g, parent, _seen)
    return _seen

def independent(g, a, b):
    """Return (is_independent, sorted_witness_list). Witness = shared ancestors."""
    shared = ancestors(g, a) & ancestors(g, b)
    return (len(shared) == 0, sorted(shared))

def check_set(g, nodes):
    """Pairwise over a set. Any shared ancestor downgrades the whole set."""
    from itertools import combinations
    results = []
    all_independent = True
    for a, b in combinations(nodes, 2):
        ok, witness = independent(g, a, b)
        results.append((a, b, ok, witness))
        if not ok:
            all_independent = False
    return all_independent, results

def save(g, path):
    with open(path, "w") as f:
        json.dump(asdict(g), f, indent=2)

def load(path):
    with open(path) as f:
        d = json.load(f)
    return Graph(edges=d.get("edges", {}))

def selftest():
    g = Graph()
    # S1 and S2 both derive from Smith2019 -> shared
    add_edge(g, "S1", "Smith2019")
    add_edge(g, "S2", "Smith2019")
    ok, wit = independent(g, "S1", "S2")
    assert ok is False and wit == ["Smith2019"], (ok, wit)
    # S3 derives from fieldA only -> independent of S1
    add_edge(g, "S3", "fieldA")
    ok, wit = independent(g, "S1", "S3")
    assert ok is True and wit == [], (ok, wit)
    # deeper chain: S4->B->Smith2019 ; shares Smith2019 with S1 transitively
    add_edge(g, "S4", "B")
    add_edge(g, "B", "Smith2019")
    ok, wit = independent(g, "S1", "S4")
    assert ok is False and "Smith2019" in wit, (ok, wit)
    # cycle safety: X->Y->X must not hang
    add_edge(g, "X", "Y")
    add_edge(g, "Y", "X")
    assert "X" in ancestors(g, "X") and "Y" in ancestors(g, "X")
    # set-level: S1,S2,S3 -> not all independent (S1~S2 shared)
    all_ind, res = check_set(g, ["S1", "S2", "S3"])
    assert all_ind is False
    save(g, "_prov_selftest.json")
    import os
    g2 = load("_prov_selftest.json")
    os.remove("_prov_selftest.json")
    assert independent(g2, "S1", "S2")[0] is False
    print("SELFTEST OK")

def main(argv=None):
    p = argparse.ArgumentParser(description="prove lineage independence by reachability")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("new").add_argument("-o", "--out", default="prov.json")
    e = sp.add_parser("edge"); e.add_argument("path")
    e.add_argument("--from", dest="src", required=True)
    e.add_argument("--to", dest="dst", required=True)
    c = sp.add_parser("check"); c.add_argument("path"); c.add_argument("a"); c.add_argument("b")
    r = sp.add_parser("roots"); r.add_argument("path"); r.add_argument("node")
    cs = sp.add_parser("checkset"); cs.add_argument("path"); cs.add_argument("nodes", nargs="+")
    sp.add_parser("selftest")
    args = p.parse_args(argv)
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "new":
        save(Graph(), args.out); print(f"-> {args.out}"); return
    g = load(args.path)
    if args.cmd == "edge":
        add_edge(g, args.src, args.dst); save(g, args.path)
        print(f"{args.src} -> {args.dst}")
    elif args.cmd == "roots":
        print(" ".join(sorted(ancestors(g, args.node))))
    elif args.cmd == "check":
        ok, wit = independent(g, args.a, args.b)
        if ok:
            print(f"INDEPENDENT: {args.a} and {args.b} share no ancestor")
        else:
            print(f"SHARED: {args.a} and {args.b} both trace to {wit} "
                  f"-> agreement is one source echoed, not convergence")
    elif args.cmd == "checkset":
        all_ind, res = check_set(g, args.nodes)
        for a, b, ok, wit in res:
            print(f"{a}~{b}\t{'INDEPENDENT' if ok else 'SHARED:' + ','.join(wit)}")
        print("=> ALL INDEPENDENT" if all_ind
              else "=> NOT ALL INDEPENDENT: dense bin downgraded")

if __name__ == "__main__":
    main()
