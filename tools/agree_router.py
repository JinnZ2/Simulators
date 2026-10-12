#!/usr/bin/env python3
"""agree_router.py - which tools to run first on an agree-set, by bin. CC0. stdlib only.

false_agree.py routes an agree-set by the CAUSE of agreement and returns a bin
per pair. This takes those bins and the tool inventory (tool_inventory.json,
beside this file) and lists the tools to run, in order, per bin.

The standing rule: ALL tools run on ALL bins. The bin sets the ORDER, not the
membership. So every claim-judging tool in the inventory lands in exactly one
of three tiers for each bin, and the tiers together are the whole list:

  PRIMARY   inspects a dimension the bin's own reason turns on. Run first.
  TRIPWIRE  inspects a dimension that would show the bin is MISLABELED. Run
            second, hoping it finds nothing; if it finds something, the
            agree-set goes back to false_agree with the new provenance.
  ALSO      everything else. Run after; a bin's order is a guess about where
            the information is, and the guess can be wrong.

Nothing here scores a tool or a study. Order inside a tier is by how many of
the tier's dimensions the tool inspects, then repo/path; the count is a sort
key and is never printed as a number about the tool.

The inspects tags in the inventory are a model's reading of each module's
docstring, not a computation. A tool tagged wrong lands in the wrong tier;
it never drops out, because ALSO holds everything.

Usage:
  agree_router.py route fa.json [--top N] [--all] [--include-models] [--inventory PATH]
  agree_router.py bin INDEPENDENT_CONVERGENCE [--top N] [--all] [--include-models]
  agree_router.py roles
  agree_router.py selftest
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import false_agree  # noqa: E402  the bin vocabulary and the router of record

INVENTORY = os.path.join(HERE, "tool_inventory.json")

# [CHOICE 1] The role table. Which inspected dimensions set PRIMARY and which
# set TRIPWIRE for each bin. Declared, not derived: it is a reading of what
# each bin's verdict in false_agree.route_pair rests on.
ROLES = {
    "FALSE_AGREE_DEFINITION": {
        "primary": ["TERMS", "SEMANTICS", "FRAME"],
        "tripwire": ["MEASUREMENT", "PROVENANCE"],
        "reason": "lineages recorded distinct; definitions or populations "
                  "differ, so the agreement may be one word over two things",
        "broken": "the two definitions name one measurand after all "
                  "(measurement tools), or the distinct lineage strings "
                  "share an ancestor (provenance tools) - then it was "
                  "SHARED_UPSTREAM",
    },
    "FALSE_AGREE_MEASURE": {
        "primary": ["MEASUREMENT", "PROTOCOL", "CONSERVATION"],
        "tripwire": ["TERMS", "PROVENANCE"],
        "reason": "same definition and population; methods differ, so the "
                  "agreement may be two instruments reading two quantities",
        "broken": "the two methods reach one quantity by different routes "
                  "(then the agreement is real), or a definition difference "
                  "sits upstream of the method (term tools)",
    },
    "SHARED_UPSTREAM": {
        "primary": ["PROVENANCE", "ASSUMPTIONS", "INCENTIVES"],
        "tripwire": ["COUPLING"],
        "reason": "the studies trace to one source; the agreement may be "
                  "one result counted twice",
        "broken": "the shared source does not carry the claim - each study "
                  "derived it independently from shared raw material "
                  "(coupling and independence tools)",
    },
    "INDEPENDENT_CONVERGENCE": {
        "primary": ["CONSERVATION", "COUPLING", "ASSUMPTIONS"],
        "tripwire": ["PROVENANCE", "INCENTIVES", "FRAME"],
        "reason": "distinct lineages, matching definition, population and "
                  "method as far as recorded; the question left is a deep "
                  "shared constraint versus an inherited assumption",
        "broken": "a shared node the lineage field could not draw: a common "
                  "funder, a shared frame, an assumption copied from one "
                  "upstream text",
    },
    "UNDERDETERMINED": {
        "primary": ["PROVENANCE", "GAP"],
        "tripwire": [],
        "reason": "at least one study has no recorded lineage, so the cause "
                  "of agreement cannot be routed",
        "broken": "no tripwire: this bin is a missing input. The move is to "
                  "recover the lineage and route again",
    },
}

# [CHOICE 2] Kinds that enter the tiers by default. DOMAIN_MODEL tools model a
# system rather than judge a claim; --include-models adds them.
DEFAULT_KINDS = ("CLAIM_TOOL",)


class RouterError(Exception):
    pass


def bins_of_record():
    """The bin vocabulary as false_agree itself returns it, read from its
    route_pair source rather than retyped here."""
    import ast
    import inspect
    src = inspect.getsource(false_agree.route_pair)
    found = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
            if node.value.value not in found:
                found.append(node.value.value)
    return found


def load_inventory(path=INVENTORY):
    if not os.path.exists(path):
        raise RouterError("inventory not found: " + path)
    with open(path) as f:
        d = json.load(f)
    if "tools" not in d or "meta" not in d:
        raise RouterError("inventory has no 'tools'/'meta': " + path)
    return d


def plan(bin_name, tools, kinds=DEFAULT_KINDS):
    """Three tiers for one bin. Every tool of the given kinds is in exactly
    one tier; nothing is dropped."""
    if bin_name not in ROLES:
        raise RouterError("unknown bin: %r (known: %s)" % (bin_name, ", ".join(ROLES)))
    role = ROLES[bin_name]
    prim, trip = set(role["primary"]), set(role["tripwire"])
    tiers = {"primary": [], "tripwire": [], "also": []}
    for t in tools:
        if t.get("kind") not in kinds:
            continue
        tags = set(t.get("inspects") or [])
        hit_p = sorted(tags & prim)
        hit_t = sorted(tags & trip)
        if hit_p:
            tiers["primary"].append((len(hit_p), t, hit_p, hit_t))
        elif hit_t:
            tiers["tripwire"].append((len(hit_t), t, hit_t, []))
        else:
            tiers["also"].append((0, t, [], []))
    for k in ("primary", "tripwire"):
        tiers[k].sort(key=lambda x: (-x[0], x[1]["repo"].lower(), x[1]["path"]))
    tiers["also"].sort(key=lambda x: (x[1]["repo"].lower(), x[1]["path"]))
    return {k: [(t, hits, trip) for _, t, hits, trip in v] for k, v in tiers.items()}


def bins_in(agreeset):
    """Pairs per bin for one agree-set, via false_agree.route."""
    out = {}
    for a, b, v in false_agree.route(agreeset):
        out.setdefault(v, []).append((a, b))
    return out


def uncovered_dims(vocab):
    """Inspected dimensions that set no bin's first or second pass. Their
    tools still run, under ALSO."""
    used = set()
    for r in ROLES.values():
        used |= set(r["primary"]) | set(r["tripwire"])
    return [d for d in vocab if d not in used]


def _line(t, hits, trip=()):
    tag = ",".join(hits) if hits else "-"
    if trip:
        tag += " | also tripwire:" + ",".join(trip)
    return "    %s/%s  [%s]  %s" % (t["repo"], t["path"], tag, t["desc"])


def render_bin(bin_name, tools, top, show_all, kinds, pairs=None):
    p = plan(bin_name, tools, kinds)
    r = ROLES[bin_name]
    out = ["", "BIN " + bin_name + ("" if pairs is None else
           "   (%d pair%s: %s)" % (len(pairs), "" if len(pairs) == 1 else "s",
                                   ", ".join("%s~%s" % ab for ab in pairs)))]
    out.append("  why this bin: " + r["reason"])
    out.append("  mislabeled if: " + r["broken"])
    out.append("  tiers: primary %d | tripwire %d | also %d | all run"
               % (len(p["primary"]), len(p["tripwire"]), len(p["also"])))
    for tier, dims in (("primary", r["primary"]), ("tripwire", r["tripwire"])):
        rows = p[tier]
        out.append("  %s on %s:" % (tier.upper(), ",".join(dims) or "(none)"))
        shown = rows if show_all else rows[:top]
        if not rows:
            out.append("    (none)")
        for t, hits, trip in shown:
            out.append(_line(t, hits, trip))
        if len(rows) > len(shown):
            out.append("    ... %d more (--all)" % (len(rows) - len(shown)))
    if show_all:
        out.append("  ALSO:")
        for t, hits, trip in p["also"]:
            out.append(_line(t, hits, trip))
    else:
        out.append("  ALSO: %d more tools run after these (--all lists them)"
                   % len(p["also"]))
    return "\n".join(out)


def render_header(inv, kinds):
    m = inv["meta"]
    n = sum(1 for t in inv["tools"] if t.get("kind") in kinds)
    lines = ["agree_router - tools to run per bin, in order. All tools run on all bins.",
             "inventory: %s, %d tools of kind %s, across %d repos"
             % (m.get("generated", "?"), n, "/".join(kinds), len(m.get("repo_heads", {}))),
             "tags: " + m.get("how_tagged", "?"),
             "not reached: %d repos (absent from the inventory, not zero tools)"
             % len(m.get("not_reached", []))]
    unc = uncovered_dims(m.get("inspects_vocab", []))
    if unc:
        lines.append("dimensions setting no bin's first or second pass "
                     "(their tools run under ALSO): " + ", ".join(unc))
    return "\n".join(lines)


def selftest():
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))
        print("%s  %s" % ("PASS" if cond else "FAIL", name))

    # 1. the role table covers exactly false_agree's bins, read from its source
    rec = bins_of_record()
    ok("roles cover exactly false_agree's bins " + str(sorted(rec)),
       sorted(rec) == sorted(ROLES))
    # 2. primary and tripwire are disjoint per bin, and drawn from the vocab
    inv = load_inventory()
    vocab = set(inv["meta"]["inspects_vocab"])
    for b, r in ROLES.items():
        ok("%s: primary and tripwire disjoint" % b,
           not set(r["primary"]) & set(r["tripwire"]))
        ok("%s: dimensions are in the inventory's vocabulary" % b,
           set(r["primary"]) | set(r["tripwire"]) <= vocab)
    # 3. partition: every tool of the kind lands in exactly one tier, per bin
    tools = inv["tools"]
    n_claim = sum(1 for t in tools if t["kind"] == "CLAIM_TOOL")
    for b in ROLES:
        p = plan(b, tools)
        ids = [(t["repo"], t["path"]) for tier in p.values() for t, _, _ in tier]
        ok("%s: tiers partition all %d claim tools" % (b, n_claim),
           len(ids) == n_claim and len(set(ids)) == n_claim)
    # 4. the inventory carries today's tools where the router expects them
    names = {t["path"] for t in tools if t["repo"] == "Simulators"}
    for f in ("tools/false_agree.py", "tools/provenance_graph.py",
              "tools/paradigm_sweep.py", "tools/conditional_claims.py",
              "tools/presignal_ledger.py", "tools/system_efficiency.py"):
        ok("inventory carries " + f, f in names)
    # 5. provenance_graph is a primary tool for SHARED_UPSTREAM and carries
    #    a tripwire tag on INDEPENDENT_CONVERGENCE: same tool, opposite job.
    #    Its tags straddle that bin's primary (COUPLING) and tripwire
    #    (PROVENANCE), so it sits in PRIMARY there and the tripwire job must
    #    still show - one tier per tool would hide it.
    def where(b, path):
        for tier, rows in plan(b, tools).items():
            for t, hits, trip in rows:
                if t["repo"] == "Simulators" and t["path"] == path:
                    return tier, hits, trip
    ok("provenance_graph: PRIMARY on SHARED_UPSTREAM",
       where("SHARED_UPSTREAM", "tools/provenance_graph.py")[0] == "primary")
    w = where("INDEPENDENT_CONVERGENCE", "tools/provenance_graph.py")
    ok("provenance_graph: tripwire job visible on INDEPENDENT_CONVERGENCE " + str(w[0]),
       "PROVENANCE" in w[2] or w[0] == "tripwire")
    ok("rendered line shows the tripwire tag beside the primary one",
       "also tripwire:PROVENANCE" in _line({"repo": "r", "path": "p", "desc": ""}, w[1], w[2]))
    # 6. an untagged tool is kept, under ALSO, not dropped
    fake = [{"repo": "x", "path": "a.py", "kind": "CLAIM_TOOL", "inspects": [], "desc": ""},
            {"repo": "x", "path": "b.py", "kind": "CLAIM_TOOL", "inspects": ["GAP", "PROVENANCE"], "desc": ""},
            {"repo": "x", "path": "c.py", "kind": "CLAIM_TOOL", "inspects": ["GAP"], "desc": ""},
            {"repo": "x", "path": "d.py", "kind": "DOMAIN_MODEL", "inspects": ["GAP"], "desc": ""}]
    p = plan("UNDERDETERMINED", fake)
    ok("untagged tool lands in ALSO", [t["path"] for t, _, _ in p["also"]] == ["a.py"])
    ok("two-dimension match sorts before one", [t["path"] for t, _, _ in p["primary"]] == ["b.py", "c.py"])
    ok("DOMAIN_MODEL excluded by default, included on request",
       len(plan("UNDERDETERMINED", fake)["primary"]) == 2 and
       len(plan("UNDERDETERMINED", fake, kinds=("CLAIM_TOOL", "DOMAIN_MODEL"))["primary"]) == 3)
    # 7. an unknown bin refuses; a missing inventory refuses
    try:
        plan("NOT_A_BIN", fake)
        ok("unknown bin refuses", False)
    except RouterError:
        ok("unknown bin refuses", True)
    try:
        load_inventory(os.path.join(HERE, "no_such_inventory.json"))
        ok("missing inventory refuses", False)
    except RouterError:
        ok("missing inventory refuses", True)
    # 8. end to end through false_agree: a constructed agree-set
    S = false_agree.Study
    ags = false_agree.AgreeSet("constructed: X rises with Y", [
        S("A", definition="d1", population="p", method="m", lineage="L1"),
        S("B", definition="d1", population="p", method="m", lineage="L2"),
        S("C", definition="d1", population="p", method="m", lineage="L1"),
        S("D", definition="d2", population="p", method="m", lineage="L3"),
        S("E", lineage=""),
        S("F", definition="d1", population="p", method="m2", lineage="L4"),
    ])
    got = bins_in(ags)
    ok("constructed agree-set reaches all five bins " + str(sorted(got)),
       sorted(got) == sorted(ROLES))
    ok("A~C routed SHARED_UPSTREAM", ("A", "C") in got.get("SHARED_UPSTREAM", []))
    text = "\n".join(render_bin(b, tools, 3, False, DEFAULT_KINDS, pr) for b, pr in got.items())
    ok("render names every bin present", all(("BIN " + b) in text for b in got))
    # 9. no number about a tool is printed: tier lines carry tags, not counts
    line = _line({"repo": "r", "path": "p.py", "desc": "d"}, ["GAP", "PROVENANCE"])
    ok("a tool line carries its matched tags, no count", "[GAP,PROVENANCE]" in line)
    # 10. the render screens clean
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE), "sheet-structure-scan"))
        import no_severity
        hits = no_severity.hits(render_header(inv, DEFAULT_KINDS) + "\n" +
                                  "\n".join("  why this bin: %s\n  mislabeled if: %s"
                                            % (r["reason"], r["broken"]) for r in ROLES.values()))
        ok("router's own prose screens clean through no_severity", not hits)
    except ImportError:
        ok("no_severity available", False)

    failed = sum(1 for _, c in checks if not c)
    print("checks: %d   failed: %d" % (len(checks), failed))
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    for name in ("route", "bin"):
        s = sub.add_parser(name)
        s.add_argument("target")
        s.add_argument("--top", type=int, default=10)
        s.add_argument("--all", action="store_true")
        s.add_argument("--include-models", action="store_true")
        s.add_argument("--inventory", default=INVENTORY)
    sub.add_parser("roles")
    sub.add_parser("selftest")
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        return selftest()
    if a.cmd == "roles":
        for b, r in ROLES.items():
            print("%-24s primary=%s tripwire=%s" % (b, ",".join(r["primary"]),
                                                     ",".join(r["tripwire"]) or "-"))
        return 0
    if a.cmd not in ("route", "bin"):
        ap.print_help()
        return 2
    kinds = DEFAULT_KINDS + (("DOMAIN_MODEL",) if a.include_models else ())
    try:
        inv = load_inventory(a.inventory)
        print(render_header(inv, kinds))
        if a.cmd == "bin":
            print(render_bin(a.target, inv["tools"], a.top, a.all, kinds))
        else:
            ags = false_agree.load(a.target)
            print("agree-set: " + ags.claim_under_test)
            for b, pairs in sorted(bins_in(ags).items()):
                print(render_bin(b, inv["tools"], a.top, a.all, kinds, pairs))
    except RouterError as e:
        print("refused: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
