#!/usr/bin/env python3
"""false_agree.py - route an agree-set by the CAUSE of agreement. CC0. stdlib only.

Density is not truth. Counting cannot separate independent convergence from one
source echoed downstream. This compares provenance fields across studies that
agree, and routes the agreement. It does not count and does not judge truth.

Per study the user records:
  id, claim, definition, population, method, lineage (source the claim/data traces to)

Usage:
  false_agree.py new "claim under test" -o fa.json
  false_agree.py add fa.json --id S1 --definition "..." --population "..." \
      --method "..." --lineage "Smith2019 dataset"
  false_agree.py route fa.json
  false_agree.py selftest
"""
import argparse, json, sys
from dataclasses import dataclass, field, asdict
from itertools import combinations

@dataclass
class Study:
    id: str
    claim: str = ""
    definition: str = ""
    population: str = ""
    method: str = ""
    lineage: str = ""      # where the claim/data came from; the provenance root

@dataclass
class AgreeSet:
    claim_under_test: str
    studies: list = field(default_factory=list)

def _norm(x):
    return (x or "").strip().lower()

def route_pair(a, b):
    """Route one pair by cause of agreement. Order of checks matters:
    missing provenance first, then shared source, then definition, then method."""
    if not _norm(a.lineage) or not _norm(b.lineage):
        return "UNDERDETERMINED"
    if _norm(a.lineage) == _norm(b.lineage):
        return "SHARED_UPSTREAM"
    if _norm(a.definition) and _norm(b.definition) and _norm(a.definition) != _norm(b.definition):
        return "FALSE_AGREE_DEFINITION"
    if _norm(a.population) and _norm(b.population) and _norm(a.population) != _norm(b.population):
        return "FALSE_AGREE_DEFINITION"
    if _norm(a.method) and _norm(b.method) and _norm(a.method) != _norm(b.method):
        return "FALSE_AGREE_MEASURE"
    # distinct lineage, same definition/population/method as far as recorded:
    return "INDEPENDENT_CONVERGENCE"

def route(ags):
    out = []
    for a, b in combinations(ags.studies, 2):
        out.append((a.id, b.id, route_pair(a, b)))
    return out

def summary(ags):
    pairs = route(ags)
    order = ["SHARED_UPSTREAM", "FALSE_AGREE_DEFINITION", "FALSE_AGREE_MEASURE",
             "UNDERDETERMINED", "INDEPENDENT_CONVERGENCE"]
    buckets = {k: [] for k in order}
    for i, j, r in pairs:
        buckets[r].append(f"{i}~{j}")
    lines = [f"CLAIM: {ags.claim_under_test}   studies={len(ags.studies)} pairs={len(pairs)}"]
    verdict = "INDEPENDENT_CONVERGENCE"
    for k in order:
        if buckets[k]:
            lines.append(f"  [{k}] {', '.join(buckets[k])}")
    # set-level read: any shared-upstream or false-agree downgrades the whole dense bin
    if buckets["SHARED_UPSTREAM"]:
        verdict = "GAP_IN_DISGUISE: agreement traces to one source"
    elif buckets["FALSE_AGREE_DEFINITION"] or buckets["FALSE_AGREE_MEASURE"]:
        verdict = "NOT_THE_SAME_CLAIM: terms/methods differ under the agreement"
    elif buckets["UNDERDETERMINED"]:
        verdict = "UNAUDITED: provenance missing; agreement not yet real"
    lines.append(f"  => {verdict}")
    return "\n".join(lines)

def save(ags, path):
    with open(path, "w") as f:
        json.dump(asdict(ags), f, indent=2)

def load(path):
    with open(path) as f:
        d = json.load(f)
    d["studies"] = [Study(**s) for s in d.get("studies", [])]
    return AgreeSet(**d)

def selftest():
    ags = AgreeSet("effect X raises Y")
    # two echoing one source
    ags.studies += [
        Study("S1", lineage="Smith2019", definition="d1", population="p1", method="m1"),
        Study("S2", lineage="Smith2019", definition="d1", population="p1", method="m1"),
    ]
    assert route_pair(ags.studies[0], ags.studies[1]) == "SHARED_UPSTREAM"
    # independent convergence
    a = Study("S3", lineage="fieldA", definition="d1", population="p1", method="m1")
    b = Study("S4", lineage="fieldB", definition="d1", population="p1", method="m1")
    assert route_pair(a, b) == "INDEPENDENT_CONVERGENCE"
    # same number, different definition
    c = Study("S5", lineage="fieldA", definition="d1", population="p1", method="m1")
    d = Study("S6", lineage="fieldB", definition="d2", population="p1", method="m1")
    assert route_pair(c, d) == "FALSE_AGREE_DEFINITION"
    # same conclusion, incompatible method
    e = Study("S7", lineage="fieldA", definition="d1", population="p1", method="survey")
    f = Study("S8", lineage="fieldB", definition="d1", population="p1", method="imaging")
    assert route_pair(e, f) == "FALSE_AGREE_MEASURE"
    # missing provenance
    g = Study("S9", lineage="", definition="d1")
    assert route_pair(a, g) == "UNDERDETERMINED"
    assert "GAP_IN_DISGUISE" in summary(ags)
    save(ags, "_fa_selftest.json")
    import os
    ags2 = load("_fa_selftest.json")
    os.remove("_fa_selftest.json")
    assert len(ags2.studies) == 2
    print("SELFTEST OK")

def main(argv=None):
    p = argparse.ArgumentParser(description="route an agree-set by cause of agreement")
    sp = p.add_subparsers(dest="cmd", required=True)
    n = sp.add_parser("new"); n.add_argument("claim"); n.add_argument("-o", "--out", default="fa.json")
    a = sp.add_parser("add"); a.add_argument("path")
    a.add_argument("--id", required=True)
    for fld in ("claim", "definition", "population", "method", "lineage"):
        a.add_argument(f"--{fld}", default="")
    for name in ("route", "summary"):
        sp.add_parser(name).add_argument("path")
    sp.add_parser("selftest")
    args = p.parse_args(argv)
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "new":
        save(AgreeSet(args.claim), args.out); print(f"-> {args.out}"); return
    ags = load(args.path)
    if args.cmd == "add":
        ags.studies.append(Study(args.id, args.claim, args.definition,
                                 args.population, args.method, args.lineage))
        save(ags, args.path); print(f"{args.id} added ({len(ags.studies)} studies)")
    elif args.cmd == "route":
        for i, j, r in route(ags):
            print(f"{i}~{j}\t{r}")
    elif args.cmd == "summary":
        print(summary(ags))

if __name__ == "__main__":
    main()
