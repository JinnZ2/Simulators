"""test_domains.py -- checks on the SHIPPED domains.py (P-11, P-12 scope).

The work order's STEP 4 names test_domains_gated.py with three checks:
  - unknown gate tag raises
  - survival final == 0 for any GATES permutation
  - node-name collisions across domains reported (P-11)

The first two are properties of domains_gated.py, which was NOT
delivered with this order (see ../INVENTORY.md, STEP 1). They are not
built here, because building them means reconstructing the module they
test, and a reconstruction is a second author's reading wearing the
first author's filename (category-weld/ CW_004). The third is a
property of domains.py, which is in the tree, and is built.

KEY-HOLDER: the expected values below were written by the same agent
that read the code. They are a REGRESSION pin on the shipped data --
they make a change visible -- not a validation of the data.

Run: python3 test_domains.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph import Graph, Channel, TOKEN_NODE
from domains import DOMAINS
from cut import vertex_connectivity

CHECKS = 0
def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)

TERMINALS = {"NEED", "SATISFIED", TOKEN_NODE}


def node_collisions(domains=DOMAINS):
    """Return {node: sorted(domain names)} for every non-terminal node
    name that appears in two or more domains."""
    seen = {}
    for name, fn in domains.items():
        for node in fn().nodes:
            if node in TERMINALS:
                continue
            seen.setdefault(node, set()).add(name)
    return {n: sorted(d) for n, d in seen.items() if len(d) >= 2}


def union_graph(domains=DOMAINS, namespaced=True):
    """One graph, every domain's channels, NEED -> SATISFIED. With
    namespaced=False node names are merged across domains exactly as a
    naive union would merge them; with namespaced=True each internal
    node is prefixed by its domain."""
    g = Graph("union" + ("[ns]" if namespaced else "[raw]"), "NEED", "SATISFIED")
    for name, fn in domains.items():
        for ch in fn().channels:
            def nm(v):
                if v in TERMINALS or not namespaced:
                    return v
                return "%s:%s" % (name, v)
            g.add_channel(Channel(src=nm(ch.src), dst=nm(ch.dst), kinds=ch.kinds,
                                  requires_token=ch.requires_token, label=ch.label))
    return g


def test_collisions_on_shipped_domains():
    c = node_collisions()
    check(c == {"ROUGH": ["shelter", "sleep"], "SHELTER_SYS": ["shelter", "sleep"]},
          "collision set moved: %r" % c)


def test_collision_detector_fires_on_a_plant():
    def a():
        g = Graph("a", "NEED", "SATISFIED")
        g.add_channel(Channel("NEED", "X", frozenset({"physical"})))
        g.add_channel(Channel("X", "SATISFIED", frozenset({"physical"})))
        return g
    def b():
        g = Graph("b", "NEED", "SATISFIED")
        g.add_channel(Channel("NEED", "X", frozenset({"physical"})))
        g.add_channel(Channel("X", "SATISFIED", frozenset({"physical"})))
        return g
    def c():
        g = Graph("c", "NEED", "SATISFIED")
        g.add_channel(Channel("NEED", "Y", frozenset({"physical"})))
        g.add_channel(Channel("Y", "SATISFIED", frozenset({"physical"})))
        return g
    check(node_collisions({"a": a, "b": b, "c": c}) == {"X": ["a", "b"]}, "plant not caught")
    check(node_collisions({"a": a, "c": c}) == {}, "no collision reads as empty, not as a hit")


def test_union_kappa_depends_on_namespacing():
    """P-11's mechanism on the shipped data: a union over raw node names
    merges shelter's ROUGH with sleep's ROUGH, so a disjoint-path count on
    the union is a property of the naming, not of the domains. Both counts
    are printed; the assertion is only that they differ, which is what
    makes the question 'was the union namespaced' load-bearing."""
    raw = vertex_connectivity(union_graph(namespaced=False))
    ns = vertex_connectivity(union_graph(namespaced=True))
    print("  union kappa: raw names = %d, namespaced = %d" % (raw, ns))
    check(ns > raw, "namespacing did not change the union count (raw=%d ns=%d)" % (raw, ns))


def test_identity_has_exactly_one_token_free_channel_pair():
    """P-12 (domains.py half): identity's only token-free avenue is
    CASH_INFORMAL. Whether cash is itself a token is a schema question
    (bearer vs ledger) the graph does not declare; this pins the
    count so that a declaration, when made, changes a number."""
    g = DOMAINS["identity"]()
    free = sorted({ch.dst for ch in g.channels if ch.src == "NEED" and not ch.requires_token})
    check(free == ["CASH_INFORMAL"], "identity token-free first hops: %r" % free)
    check(all(ch.label.startswith("cash") for ch in g.channels if ch.dst == "CASH_INFORMAL"),
          "the token-free avenue is labelled cash")


def main():
    tests = [
        test_collisions_on_shipped_domains,
        test_collision_detector_fires_on_a_plant,
        test_union_kappa_depends_on_namespacing,
        test_identity_has_exactly_one_token_free_channel_pair,
    ]
    for t in tests:
        t()
    print("checks: %d" % CHECKS)
    print("tests:  %d" % len(tests))
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
