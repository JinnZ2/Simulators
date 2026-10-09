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

What is mechanical and what is not:
  * The dependency MAP is declared by whoever knows the ground. The tool
    does not invent prerequisites; a claim with no declared map returns
    UNDECLARED, never "fully accounted for".
  * Degree is computed: hops from the thing along the declared
    prerequisite edges (breadth-first; cycles are fine).
  * Whether the claim NAMES each prerequisite is a word-boundary search
    over its name and declared aliases. That is a word list, and its limit
    is stated plainly: a paraphrase steps around it, and naming a
    prerequisite is not the same as accounting for it. A hit means
    "mentioned", nothing more.

Input (JSON):
  {"claim": "...", "thing": "data center",
   "deps": {"data center": ["electricity", "cooling water", "land"],
            "electricity": ["coal", "natural gas"],
            "cooling water": ["river"]},
   "aliases": {"electricity": ["power", "grid"]},
   "kind": {"electricity": "energy", "cooling water": "matter"}}

Output per prerequisite: degree, kind, MENTIONED / UNSTATED. Per degree:
named/total, or None when no prerequisite sits at that degree (absent is not
zero). Verdict:
  UNDECLARED        no map supplied
  FIRST_DEGREE_UNSTATED  at least one first-degree prerequisite unnamed --
                    the claim writes a coupled thing as standing alone
  FIRST_DEGREE_NAMED     every first-degree prerequisite is named
Deeper degrees are reported, never folded into the verdict.

Usage:
  python3 dependency_check.py CASE.json
  python3 dependency_check.py --demo
  python3 dependency_check.py --selftest
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


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


def check(case):
    claim = case.get("claim", "")
    thing = case.get("thing")
    deps = case.get("deps") or {}
    if not thing or not deps.get(thing):
        return {"verdict": "UNDECLARED", "thing": thing,
                "why": "no prerequisite map declared for the thing; "
                       "an unmapped claim is not read as fully accounted"}
    aliases = case.get("aliases") or {}
    kinds = case.get("kind") or {}
    deg = degrees(thing, deps)
    rows = []
    for name, k in sorted(deg.items(), key=lambda x: (x[1], x[0])):
        hit = mentioned(claim, name, tuple(aliases.get(name, ())))
        rows.append({"name": name, "degree": k,
                     "kind": kinds.get(name, "UNDECLARED"),
                     "state": "MENTIONED" if hit else "UNSTATED",
                     "via": hit})
    declared = set(deps) | {d for v in deps.values() for d in v}
    unreachable = sorted(declared - set(deg) - {thing})
    by_degree = {}
    for k in range(1, max(deg.values()) + 1):
        at = [r for r in rows if r["degree"] == k]
        by_degree[k] = ((sum(r["state"] == "MENTIONED" for r in at), len(at))
                        if at else None)
    first = [r for r in rows if r["degree"] == 1]
    unstated1 = [r["name"] for r in first if r["state"] == "UNSTATED"]
    return {"verdict": "FIRST_DEGREE_UNSTATED" if unstated1
            else "FIRST_DEGREE_NAMED",
            "thing": thing, "rows": rows, "by_degree": by_degree,
            "first_degree_unstated": unstated1, "unreachable": unreachable}


def render(case, res):
    out = ["claim : %s" % case.get("claim", ""),
           "thing : %s" % res["thing"],
           "verdict: %s" % res["verdict"]]
    if res["verdict"] == "UNDECLARED":
        out.append("  %s" % res["why"])
        return "\n".join(out)
    out.append("")
    out.append("  %-6s %-22s %-10s %s" % ("degree", "prerequisite", "kind",
                                         "in the claim"))
    for r in res["rows"]:
        out.append("  %-6d %-22s %-10s %s%s" % (
            r["degree"], r["name"], r["kind"], r["state"],
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


DEMO = [
    {"label": "CONSTRUCTED -- written to show the leak",
     "claim": "Our new data center is clean digital infrastructure that "
              "runs in the cloud.",
     "thing": "data center",
     "deps": {"data center": ["electricity", "cooling water", "land",
                              "copper"],
              "electricity": ["natural gas", "coal"],
              "cooling water": ["river"],
              "copper": ["mine"]},
     "aliases": {"electricity": ["power", "grid"],
                 "cooling water": ["water"]},
     "kind": {"electricity": "energy", "cooling water": "matter",
              "land": "matter", "copper": "matter",
              "natural gas": "energy", "coal": "energy",
              "river": "matter", "mine": "matter"}},
    {"label": "CONSTRUCTED -- same thing, coupling written in",
     "claim": "The data center draws grid power from gas and coal plants, "
              "takes cooling water from the river, sits on 40 acres of "
              "land, and is wired with copper from an open-pit mine.",
     "thing": "data center",
     "deps": {"data center": ["electricity", "cooling water", "land",
                              "copper"],
              "electricity": ["natural gas", "coal"],
              "cooling water": ["river"],
              "copper": ["mine"]},
     "aliases": {"electricity": ["power", "grid"],
                 "cooling water": ["water"], "natural gas": ["gas"]},
     "kind": {}},
    {"label": "CONSTRUCTED -- no map supplied",
     "claim": "The truck is just a machine.", "thing": "truck", "deps": {}},
]


def selftest():
    fails, n = [], [0]

    def ok(c, label):
        n[0] += 1
        if not c:
            fails.append(label)

    deps = {"t": ["a", "b"], "a": ["c"], "c": ["t", "a"], "b": []}
    d = degrees("t", deps)
    ok(d == {"a": 1, "b": 1, "c": 2}, "degrees by hops, cycle back to thing")
    ok(mentioned("Uses water daily", "water") == "water", "match")
    ok(mentioned("waterproof seals", "water") is None, "word boundary")
    ok(mentioned("grid power", "electricity", ("grid",)) == "grid", "alias")
    ok(check({"claim": "x", "thing": "t", "deps": {}})["verdict"]
       == "UNDECLARED", "empty map is UNDECLARED")
    ok(check({"claim": "x", "thing": None, "deps": deps})["verdict"]
       == "UNDECLARED", "no thing is UNDECLARED")
    r = check({"claim": "it needs a and b", "thing": "t", "deps": deps})
    ok(r["verdict"] == "FIRST_DEGREE_NAMED", "first degree named")
    ok(r["by_degree"][2] == (0, 1), "second degree reported, not in verdict")
    r = check({"claim": "it needs a", "thing": "t", "deps": deps})
    ok(r["first_degree_unstated"] == ["b"], "unstated first degree named")
    r = check({"claim": "", "thing": "t",
               "deps": {"t": ["a"], "x": ["y"]}})
    ok(r["unreachable"] == ["x", "y"], "unreachable declared nodes listed")
    gap = check({"claim": "", "thing": "t",
                 "deps": {"t": ["a"], "a": ["c"], "c": ["e"]}})
    ok(gap["by_degree"] == {1: (0, 1), 2: (0, 1), 3: (0, 1)},
       "every degree reported")
    v = [check(c)["verdict"] for c in DEMO]
    ok(v == ["FIRST_DEGREE_UNSTATED", "FIRST_DEGREE_NAMED", "UNDECLARED"],
       "demo reaches all three verdicts")
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
