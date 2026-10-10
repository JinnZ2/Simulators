"""dependency_check.py -- the animacy pass as a dependency check.

CC0. stdlib only. Parses under Python 3.9.

The operator's quick form of the animacy pass: for the thing a claim names,
what matter or energy is a prerequisite for it? Animacy here is degree of
coupling, not alive/dead. A first-degree prerequisite is something the thing
cannot exist or run without. A second-degree one is a prerequisite of that,
and so on along the chain.

The leak this catches: a claim that writes a thing as if it stood alone --
at museum-glass distance -- while it is coupled at first degree to matter
and energy the claim never names.

WHERE THE MAP COMES FROM. The prerequisites are set by physics: what has to
be present for the thing's mass and energy balance to close. "What
combination of events has to happen for that equation to take place" is the
dependency map. So the default is to DERIVE the map:

  * TEMPLATES is a seed set of balance templates. Each entry states the
    balance it comes from and the prerequisites that balance requires. It is
    NOT exhaustive, and where a prerequisite has more than one physical
    route (electricity from heat, from falling water, from light), the
    template names the route-independent requirement (a primary energy
    source) rather than picking one route.
  * derive_map(thing) walks the templates recursively: the thing's
    prerequisites, then theirs, as far as templates reach. A prerequisite
    with no template of its own is a leaf -- still a real prerequisite,
    just not expanded further here.
  * A caller-supplied map AUGMENTS the derived one (union of edges). It is
    the fallback for things whose balance cannot be closed from standard
    inputs: site-conditioned material, a worked process off the corpus.
    `"replace_derived": true` uses the supplied map alone.
  * Every prerequisite carries its map provenance: DERIVED (reached only by
    template edges), DECLARED (only by supplied edges), or BOTH.
  * A thing with neither a template nor a supplied map returns UNDECLARED,
    never "fully accounted for".
  * READ BACKWARDS the same map is the externality test. Templates also
    list what each process "produces" (outputs that must go somewhere).
    closure(thing, booked) checks every required node -- inputs and
    outputs -- against what a claim booked; whatever is required and not
    booked is the externality, already tagged matter or energy.

What is mechanical and what is not:
  * Degree is computed: hops from the thing along the map, breadth-first.
  * Whether the claim NAMES each prerequisite is a word-boundary search
    over its name and aliases. That is a word list, and its limit is stated
    plainly: a paraphrase steps around it, and naming a prerequisite is not
    the same as accounting for it. A hit means "mentioned", nothing more.
  * Matching the claim's thing to a template is by the thing's name or an
    alias; an unlisted synonym falls through to UNDECLARED, not to a guess.

Input (JSON):
  {"claim": "...", "thing": "data center",
   "deps": {"cooling": ["river"]},          # optional, augments the derived
   "aliases": {"electricity": ["power"]},   # optional, added to templates
   "kind": {"river": "matter"}}             # optional

Output per prerequisite: degree, kind, source (DERIVED/DECLARED/BOTH),
MENTIONED/UNSTATED. Per degree: named/total, or None when no prerequisite
sits at that degree (absent is not zero). Verdict:
  UNDECLARED             no template and no supplied map
  FIRST_DEGREE_UNSTATED  at least one first-degree prerequisite unnamed
  FIRST_DEGREE_NAMED     every first-degree prerequisite is named
Deeper degrees are reported, never folded into the verdict.

Usage:
  python3 dependency_check.py CASE.json
  python3 dependency_check.py --demo
  python3 dependency_check.py --templates
  python3 dependency_check.py --selftest
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- templates
# SEED SET, not exhaustive. Each: the balance it comes from, then
# (prerequisite, kind) pairs that balance requires. Aliases are the words a
# claim might use for the thing or a prerequisite.

TEMPLATES = {
    "combustion": {
        "balance": "fuel + O2 -> CO2 + H2O + heat; the reaction needs an "
                   "activation energy to start",
        "requires": [("fuel", "matter"), ("oxidizer", "matter"),
                     ("ignition energy", "energy")],
        "aliases": ["burning", "fire"],
        "produces": [("carbon dioxide", "matter"), ("water vapor", "matter"),
                     ("heat", "energy")],
    },
    "electricity": {
        "balance": "first law: electrical energy delivered = energy "
                   "converted from a primary source minus losses; current "
                   "needs a conducting path",
        "requires": [("primary energy source", "energy"),
                     ("conductor", "matter")],
        "aliases": ["power", "grid", "electric"],
    },
    "thermal power": {
        "balance": "Q_in = W_e + Q_reject; a heat engine needs a heat "
                   "source and a cold sink (second law)",
        "requires": [("combustion", "energy"), ("cold sink", "matter"),
                     ("conductor", "matter")],
        "aliases": ["power plant", "coal plant", "gas plant"],
        "produces": [("rejected heat", "energy")],
    },
    "data center": {
        "balance": "P_electric in = Q_heat out (compute dissipates its "
                   "input as heat); hardware has mass and footprint",
        "requires": [("electricity", "energy"), ("cooling", "matter"),
                     ("land", "matter"), ("conductor", "matter")],
        "aliases": ["datacenter", "server farm", "the cloud"],
        "produces": [("waste heat", "energy"), ("e-waste", "matter")],
    },
    "cooling": {
        "balance": "heat removed = mass flow x heat capacity x temperature "
                   "rise of a sink medium; moving it takes work",
        "requires": [("cold sink", "matter"), ("electricity", "energy")],
        "aliases": ["cooling water", "chiller"],
    },
    "conductor": {
        "balance": "a current path needs a conductive metal; refining it "
                   "from ore is an energy input (e.g. Cu2S + O2 -> 2Cu + SO2)",
        "requires": [("ore", "matter"), ("smelting energy", "energy")],
        "aliases": ["copper", "wire", "wiring", "aluminum"],
        "produces": [("sulfur dioxide", "matter"), ("tailings", "matter")],
    },
    "cold sink": {
        "balance": "a sink absorbs rejected heat; water or air at a lower "
                   "temperature",
        "requires": [("water", "matter")],
        "aliases": ["river", "lake", "cooling tower"],
    },
}


def _template_for(name):
    """Template key for name or an alias; None if no template matches."""
    n = name.lower().strip()
    if n in TEMPLATES:
        return n
    for key, t in TEMPLATES.items():
        if n in (a.lower() for a in t.get("aliases", [])):
            return key
    return None


def derive_map(thing):
    """{node: [prereqs]} derived from templates, recursively; {} if none."""
    out = {}
    start = _template_for(thing) if thing else None
    if start is None:
        return out
    stack = [(thing, start)]
    seen = set()
    while stack:
        node, key = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        reqs = [r for r, _ in TEMPLATES[key]["requires"]]
        out[node] = reqs
        for r in reqs:
            k = _template_for(r)
            if k is not None and r not in seen:
                stack.append((r, k))
    return out


def derived_kinds(dmap):
    kinds = {}
    for node in dmap:
        key = _template_for(node)
        if key:
            for r, k in TEMPLATES[key]["requires"]:
                kinds.setdefault(r, k)
    return kinds


def derived_aliases(names):
    al = {}
    for n in names:
        key = _template_for(n)
        if key:
            al[n] = [key] + list(TEMPLATES[key].get("aliases", []))
    return al


def required_nodes(thing):
    """Every node the thing's balance requires, from the derived map:
    [(name, kind, role, degree)]. Inputs are the derived prerequisites at
    their hop degree. Outputs are what each reached template "produces" --
    mass and energy that leave and must go somewhere -- at the degree of
    the node producing them (the thing itself is degree 0). None if no
    template matches."""
    dmap = derive_map(thing) if thing else {}
    if not dmap:
        return None
    kinds = derived_kinds(dmap)
    deg = degrees(thing, dmap)
    out = [(n, kinds.get(n, "UNDECLARED"), "input", d)
           for n, d in sorted(deg.items(), key=lambda x: (x[1], x[0]))]
    seen = {n for n, _, _, _ in out}
    producers = [(thing, 0)] + sorted(deg.items(), key=lambda x: (x[1], x[0]))
    for node, d in producers:
        key = _template_for(node)
        for name, kind in (TEMPLATES[key].get("produces", []) if key else []):
            if name not in seen:
                seen.add(name)
                out.append((name, kind, "output", d))
    return out


def accounted_for(name, booked):
    """True if the booked list names this node or one of its aliases."""
    names = {b.lower().strip() for b in booked}
    if name.lower() in names:
        return True
    return any(a.lower() in names
               for a in derived_aliases([name]).get(name, []))


def closure(thing, booked):
    """The dependency chain read BACKWARDS. Forward: what the thing's
    balance requires. Backward: has the claim booked every required node?
    Whatever is required and not booked is the externality -- conservation
    says it did not vanish, it left the frame. Each node keeps the
    matter/energy kind the map already carries, so externalities come out
    tagged. None if there is no derived map (cannot be checked; never read
    as closing)."""
    req = required_nodes(thing)
    if req is None:
        return None
    booked = list(booked or [])
    unacc = [r for r in req if not accounted_for(r[0], booked)]
    return {"required": req, "unaccounted": unacc, "closes": not unacc}


# ---------------------------------------------------------------- the pass

def degrees(thing, deps):
    """{prerequisite: degree} by breadth-first hops from thing."""
    seen = {thing: 0}
    frontier = [thing]
    while frontier:
        nxt = []
        for node in frontier:
            for d in deps.get(node, []):
                if d not in seen:
                    seen[d] = seen[node] + 1
                    nxt.append(d)
        frontier = nxt
    seen.pop(thing)
    return seen


def mentioned(claim, name, aliases=()):
    text = claim.lower()
    for term in (name,) + tuple(aliases):
        pat = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
        if re.search(pat, text):
            return term
    return None


def merge_maps(derived, declared):
    """Union of edges; returns (map, {(parent, child): source})."""
    merged, src = {}, {}
    for which, m in (("DERIVED", derived), ("DECLARED", declared)):
        for node, kids in m.items():
            lst = merged.setdefault(node, [])
            for k in kids:
                if k not in lst:
                    lst.append(k)
                prev = src.get((node, k))
                src[(node, k)] = which if prev in (None, which) else "BOTH"
    return merged, src


def node_sources(merged, edge_src):
    out = {}
    for (parent, child), s in edge_src.items():
        prev = out.get(child)
        out[child] = s if prev in (None, s) else "BOTH"
    return out


def check(case):
    claim = case.get("claim", "")
    thing = case.get("thing")
    declared = case.get("deps") or {}
    derived = {} if case.get("replace_derived") else derive_map(thing or "")
    if derived and thing not in derived:
        derived = {}
    if not thing or not (derived.get(thing) or declared.get(thing)):
        return {"verdict": "UNDECLARED", "thing": thing,
                "why": "no balance template and no supplied map for the "
                       "thing; an unmapped claim is not read as fully "
                       "accounted"}
    deps, edge_src = merge_maps(derived, declared)
    sources = node_sources(deps, edge_src)
    deg = degrees(thing, deps)
    kinds = derived_kinds(derived)
    kinds.update(case.get("kind") or {})
    aliases = derived_aliases(deg)
    for k, v in (case.get("aliases") or {}).items():
        aliases[k] = list(aliases.get(k, [])) + list(v)
    rows = []
    for name, k in sorted(deg.items(), key=lambda x: (x[1], x[0])):
        hit = mentioned(claim, name, tuple(aliases.get(name, ())))
        rows.append({"name": name, "degree": k,
                     "kind": kinds.get(name, "UNDECLARED"),
                     "source": sources.get(name, "DECLARED"),
                     "state": "MENTIONED" if hit else "UNSTATED",
                     "via": hit})
    names = set(deps) | {d for v in deps.values() for d in v}
    unreachable = sorted(names - set(deg) - {thing})
    by_degree = {}
    for k in range(1, max(deg.values()) + 1):
        at = [r for r in rows if r["degree"] == k]
        by_degree[k] = ((sum(r["state"] == "MENTIONED" for r in at), len(at))
                        if at else None)
    unstated1 = [r["name"] for r in rows
                 if r["degree"] == 1 and r["state"] == "UNSTATED"]
    tkey = _template_for(thing) if derived else None
    return {"verdict": "FIRST_DEGREE_UNSTATED" if unstated1
            else "FIRST_DEGREE_NAMED",
            "thing": thing, "template": tkey,
            "balance": TEMPLATES[tkey]["balance"] if tkey else None,
            "rows": rows, "by_degree": by_degree,
            "first_degree_unstated": unstated1, "unreachable": unreachable}


def render(case, res):
    out = ["claim : %s" % case.get("claim", ""),
           "thing : %s" % res["thing"],
           "verdict: %s" % res["verdict"]]
    if res["verdict"] == "UNDECLARED":
        out.append("  %s" % res["why"])
        return "\n".join(out)
    if res["template"]:
        out.append("derived from template '%s': %s"
                   % (res["template"], res["balance"]))
    out.append("")
    out.append("  %-6s %-22s %-10s %-9s %s" % (
        "degree", "prerequisite", "kind", "map", "in the claim"))
    for r in res["rows"]:
        out.append("  %-6d %-22s %-10s %-9s %s%s" % (
            r["degree"], r["name"], r["kind"], r["source"], r["state"],
            (" (as '%s')" % r["via"]) if r["via"] and r["via"] != r["name"]
            else ""))
    out.append("")
    for k, v in res["by_degree"].items():
        out.append("  degree %d: %s" % (k, "none declared" if v is None
                                         else "%d of %d named" % v))
    if res["unreachable"]:
        out.append("  declared but not reachable from the thing: %s"
                   % ", ".join(res["unreachable"]))
    out.append("  (a mention is a word match: it does not show the "
               "coupling is accounted for, and a paraphrase evades it)")
    return "\n".join(out)


def render_templates():
    out = ["balance templates -- SEED SET, not exhaustive", ""]
    for key, t in TEMPLATES.items():
        out.append("%s  (aliases: %s)" % (key, ", ".join(t["aliases"])))
        out.append("  balance : %s" % t["balance"])
        out.append("  requires: %s" % ", ".join(
            "%s [%s]" % (r, k) for r, k in t["requires"]))
    return "\n".join(out)


DEMO = [
    {"label": "CONSTRUCTED -- derived from physics, no map supplied",
     "claim": "Our new data center is clean digital infrastructure.",
     "thing": "data center"},
    {"label": "CONSTRUCTED -- same thing, coupling written in, no map",
     "claim": "The data center draws grid electricity, rejects its heat "
              "through cooling water from the river, sits on 40 acres of "
              "land, and is wired with copper smelted from ore.",
     "thing": "data center"},
    {"label": "CONSTRUCTED -- derived, augmented by a site-specific map",
     "claim": "The data center runs on hydro power and cools with lake water.",
     "thing": "data center",
     "deps": {"primary energy source": ["dam"], "dam": ["river flow"]},
     "aliases": {"primary energy source": ["hydro"]},
     "kind": {"dam": "matter", "river flow": "energy"}},
    {"label": "CONSTRUCTED -- no template, no map",
     "claim": "The truck is just a machine.", "thing": "truck"},
]


def selftest():
    fails, n = [], [0]

    def ok(c, label):
        n[0] += 1
        if not c:
            fails.append(label)

    for key, t in TEMPLATES.items():
        ok(t.get("balance") and t.get("requires"),
           "template %s states a balance and requirements" % key)

    deps = {"t": ["a", "b"], "a": ["c"], "c": ["t", "a"], "b": []}
    ok(degrees("t", deps) == {"a": 1, "b": 1, "c": 2},
       "degrees by hops, cycle back to thing")
    ok(mentioned("Uses water daily", "water") == "water", "match")
    ok(mentioned("waterproof seals", "water") is None, "word boundary")
    ok(mentioned("grid power", "electricity", ("grid",)) == "grid", "alias")

    # derived purely from a template
    r = check({"claim": "x", "thing": "data center"})
    ok(r["verdict"] == "FIRST_DEGREE_UNSTATED", "derived thing is checked")
    firsts = {x["name"] for x in r["rows"] if x["degree"] == 1}
    ok(firsts == {"electricity", "cooling", "land", "conductor"},
       "first degree from the data center balance")
    ok(all(x["source"] == "DERIVED" for x in r["rows"]),
       "pure template: every prerequisite DERIVED")
    ok(r["template"] == "data center" and r["balance"], "template named")
    ok(_template_for("server farm") == "data center", "thing alias")
    ok(check({"claim": "", "thing": "the cloud"})["verdict"]
       == "FIRST_DEGREE_UNSTATED", "alias thing derives")

    # augmented by a supplied map
    r = check({"claim": "", "thing": "data center",
               "deps": {"data center": ["land", "permit"],
                        "cooling": ["aquifer"]}})
    src = {x["name"]: x["source"] for x in r["rows"]}
    ok(src.get("permit") == "DECLARED", "supplied-only node DECLARED")
    ok(src.get("land") == "BOTH", "node on both maps is BOTH")
    ok(src.get("aquifer") == "DECLARED", "supplied edge under derived node")
    ok(src.get("electricity") == "DERIVED", "template-only node DERIVED")

    # replace_derived uses the supplied map alone
    r = check({"claim": "", "thing": "data center", "replace_derived": True,
               "deps": {"data center": ["permit"]}})
    ok([x["name"] for x in r["rows"]] == ["permit"], "replace_derived")

    # still UNDECLARED
    ok(check({"claim": "x", "thing": "truck"})["verdict"] == "UNDECLARED",
       "no template, no map: UNDECLARED")
    ok(check({"claim": "x", "thing": None})["verdict"] == "UNDECLARED",
       "no thing: UNDECLARED")
    ok(check({"claim": "x", "thing": "truck", "replace_derived": True,
              "deps": {}})["verdict"] == "UNDECLARED", "empty map UNDECLARED")

    # declared-only path still works as before
    r = check({"claim": "it needs a and b", "thing": "t", "deps": deps})
    ok(r["verdict"] == "FIRST_DEGREE_NAMED", "declared map, first named")
    ok(r["by_degree"][2] == (0, 1), "second degree reported, not in verdict")
    r = check({"claim": "", "thing": "t", "deps": {"t": ["a"], "x": ["y"]}})
    ok(r["unreachable"] == ["x", "y"], "unreachable declared nodes listed")

    # closure: the chain read backwards
    req = required_nodes("data center")
    ok(req is not None and ("waste heat", "energy", "output", 0) in req,
       "thing's own outputs required at degree 0")
    ok(("tailings", "matter", "output", 1) in req,
       "a prerequisite's outputs required at its degree")
    c = closure("data center", ["electricity", "land"])
    ok(not c["closes"] and ("cooling", "matter", "input", 1)
       in c["unaccounted"], "narrow booking does not close; kind carried")
    ok(closure("data center", [r[0] for r in req])["closes"],
       "booking every required node closes")
    ok(closure("data center", ["copper"])["unaccounted"][0][0] != "conductor"
       and not any(u[0] == "conductor" for u in
                   closure("data center", ["copper"])["unaccounted"]),
       "an alias books the node")
    ok(closure("truck", ["x"]) is None, "no map: None, never closes")

    v = [check(c)["verdict"] for c in DEMO]
    ok(v == ["FIRST_DEGREE_UNSTATED", "FIRST_DEGREE_NAMED",
             "FIRST_DEGREE_UNSTATED", "UNDECLARED"], "demo verdicts")
    print("checks: %d   failed: %d" % (n[0], len(fails)))
    for f in fails:
        print("  FAIL", f)
    return 0 if not fails else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--selftest":
        return selftest()
    if argv[0] == "--templates":
        print(render_templates())
        return 0
    if argv[0] == "--demo":
        for c in DEMO:
            print("== %s" % c["label"])
            print(render(c, check(c)))
            print()
        return 0
    with open(argv[0], encoding="utf-8") as f:
        case = json.load(f)
    print(render(case, check(case)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
