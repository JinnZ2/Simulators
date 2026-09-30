"""test_gate.py — known-answer tests for the gate module.

Run: python3 test_gate.py
"""

from graph import Graph, Channel, Admissibility, project, TOKEN_NODE
from cut import cut_vertices, vertex_connectivity, is_connected
from domains import DOMAINS
from projections import project_all, DEFAULT_THETAS

CHECKS = 0
def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)

# --- graph + channel --------------------------------------------------

def test_channel_validates():
    Channel("A", "B", frozenset({"physical"}))
    for bad_kinds in (frozenset({"cats"}), frozenset({"physical", "frogs"})):
        try:
            Channel("A", "B", bad_kinds)
            check(False, f"should reject kinds={bad_kinds}")
        except ValueError:
            check(True, "rejected unknown kind")
    try:
        Channel("", "B", frozenset({"physical"}))
        check(False, "should reject empty src")
    except ValueError:
        check(True, "rejected empty src")

def test_project_keeps_only_matching():
    g = Graph("t", "S", "T")
    g.add_channel(Channel("S", "T", frozenset({"physical"}), label="phys"))
    g.add_channel(Channel("S", "T", frozenset({"physical", "legal"}),
                          label="phys+legal"))
    g.add_channel(Channel("S", "T", frozenset({"legal", "practical"}),
                          label="legal+prac"))
    theta = Admissibility.of("phys+legal", "physical", "legal")
    p = project(g, theta)
    labels = sorted(sum(g2.edges().values(), set()) for g2 in [p])[0] if False else None
    # simpler: check channel count
    check(len(p.channels) == 1, f"expected 1 channel, got {len(p.channels)}")
    check(p.channels[0].label == "phys+legal", "wrong channel kept")

# --- cut --------------------------------------------------------------

def test_cut_vertex_single():
    # S -> X -> T and S -> Y -> T. Removing X leaves S->Y->T.
    # Removing either alone does not disconnect, so κ=2.
    g = Graph("diamond", "S", "T")
    g.add_channel(Channel("S", "X", frozenset({"physical"})))
    g.add_channel(Channel("X", "T", frozenset({"physical"})))
    g.add_channel(Channel("S", "Y", frozenset({"physical"})))
    g.add_channel(Channel("Y", "T", frozenset({"physical"})))
    kappa, cuts = cut_vertices(g)
    check(kappa == 2, f"expected κ=2, got {kappa}")
    check(cuts == set(), "no single cut vertex in diamond")
    check(vertex_connectivity(g) == 2, "vertex_connectivity disagrees")

def test_cut_vertex_articulation():
    # S -> X -> T only. X is the sole cut vertex.
    g = Graph("chain", "S", "T")
    g.add_channel(Channel("S", "X", frozenset({"physical"})))
    g.add_channel(Channel("X", "T", frozenset({"physical"})))
    kappa, cuts = cut_vertices(g)
    check(kappa == 1, f"expected κ=1, got {kappa}")
    check(cuts == {"X"}, f"expected {{X}}, got {cuts}")

def test_token_is_cut_vertex():
    g = Graph("token-only", "S", "T")
    g.add_channel(Channel("S", "T", frozenset({"physical", "legal"}),
                          requires_token=True, label="via token"))
    kappa, cuts = cut_vertices(g)
    check(kappa == 1, f"expected κ=1, got {kappa}")
    check(TOKEN_NODE in cuts, f"token not in cuts: {cuts}")

def test_token_not_cut_when_bypass_exists():
    g = Graph("bypass", "S", "T")
    g.add_channel(Channel("S", "T", frozenset({"physical", "legal"}),
                          requires_token=True, label="via token"))
    g.add_channel(Channel("S", "T", frozenset({"physical", "legal"}),
                          label="direct"))
    kappa, cuts = cut_vertices(g)
    check(kappa == 2, f"expected κ=2, got {kappa}")
    check(TOKEN_NODE not in cuts, "token should not be cut vertex when bypass exists")

def test_disconnected():
    g = Graph("disc", "S", "T")
    g.add_channel(Channel("S", "X", frozenset({"physical"})))
    check(not is_connected(g), "should be disconnected")
    kappa, cuts = cut_vertices(g)
    check(kappa == 0, f"expected κ=0, got {kappa}")
    check(cuts == set(), "no cut vertices in disconnected graph")

def test_kappa_three():
    # three internally disjoint paths
    g = Graph("triple", "S", "T")
    for i in range(3):
        g.add_channel(Channel("S", f"A{i}", frozenset({"physical"})))
        g.add_channel(Channel(f"A{i}", "T", frozenset({"physical"})))
    check(vertex_connectivity(g) == 3, "expected κ=3")

# --- domains ----------------------------------------------------------

def test_domains_exist():
    for name in ("water", "food", "shelter", "defecation",
                 "thermal", "sleep", "medical", "identity"):
        check(name in DOMAINS, f"domain {name} missing")
        g = DOMAINS[name]()
        check(g.source == "NEED", f"{name}: source wrong")
        check(g.target == "SATISFIED", f"{name}: target wrong")

def test_projections_have_token_reading():
    """At least one domain has a token-is-cut reading under at least one θ."""
    found = False
    for name, fn in DOMAINS.items():
        projs = project_all(fn())
        if any(p.token_is_cut for p in projs.values()):
            found = True
            break
    check(found, "no domain reported token as cut vertex under any θ")

def test_projections_disagree_or_agree():
    """A domain can be cut under one θ and not another. Both cases occur."""
    differs = False
    same = False
    for name, fn in DOMAINS.items():
        projs = project_all(fn())
        vals = {p.token_is_cut for p in projs.values()}
        if vals == {True} or vals == {False}:
            same = True
        else:
            differs = True
    check(same, "no domain has a uniform token-cut reading across θ")
    check(differs, "no domain has θ-dependent token-cut reading")

def test_no_composite_key():
    """Projection object carries no 'score' or 'verdict' field."""
    p = project_all(DOMAINS["water"]())["all"]
    d = p.to_dict()
    for bad in ("score", "verdict", "rank", "priority"):
        check(bad not in d, f"projection carries {bad!r}")

# --- README pin (P-02) --------------------------------------------------

def test_readme_water_table_matches_render():
    """The water table in README.md is generated from projections.render,
    not typed. P-02: the typed version disagreed with the code in 3 of 5
    rows, and nothing noticed until a second party ran the CLI."""
    from pathlib import Path
    from domains import DOMAINS
    from projections import project_all, render
    readme = (Path(__file__).resolve().parent / "README.md").read_text().split("\n")
    start = readme.index("    domain: water")
    got = []
    i = start
    while i < len(readme) and (readme[i].startswith("    ") or readme[i] == ""):
        if readme[i] == "" and not (i + 1 < len(readme) and readme[i + 1].startswith("    ")):
            break
        got.append(readme[i][4:] if readme[i] else "")
        i += 1
    want = render("water", project_all(DOMAINS["water"]())).split("\n")
    check(got == want, "README water table differs from render():\n  README: %r\n  render: %r" % (got, want))

# --- P-01 regression pin -------------------------------------------------

def test_direct_edge_counts_as_one_path():
    """P-01: with unbounded capacity on a direct S->T edge, max-flow
    returned 10**9 + 1 as kappa. A direct edge is one path."""
    g = Graph("direct-only", "S", "T")
    g.add_channel(Channel("S", "T", frozenset({"physical"}), label="direct"))
    check(vertex_connectivity(g) == 1, "a lone direct edge is exactly one path")
    kappa, cuts = cut_vertices(g)
    check(kappa == 1 and cuts == set(), "direct edge: kappa 1, no cut VERTEX (no internal vertex exists)")
    # two direct channels between the same pair collapse in _adj to one
    # adjacency edge: recorded limit, asserted so a change is visible.
    g2 = Graph("two-direct", "S", "T")
    g2.add_channel(Channel("S", "T", frozenset({"physical"}), label="a"))
    g2.add_channel(Channel("S", "T", frozenset({"physical"}), label="b"))
    check(vertex_connectivity(g2) == 1, "parallel direct channels collapse to one adjacency edge (limit, stated)")

def main():
    tests = [
        test_channel_validates,
        test_project_keeps_only_matching,
        test_cut_vertex_single,
        test_cut_vertex_articulation,
        test_token_is_cut_vertex,
        test_token_not_cut_when_bypass_exists,
        test_disconnected,
        test_kappa_three,
        test_domains_exist,
        test_projections_have_token_reading,
        test_projections_disagree_or_agree,
        test_no_composite_key,
        test_readme_water_table_matches_render,
        test_direct_edge_counts_as_one_path,
    ]
    for t in tests:
        t()
    print(f"checks: {CHECKS}")
    print(f"tests:  {len(tests)}")
    print("PASS")

if __name__ == "__main__":
    main()
