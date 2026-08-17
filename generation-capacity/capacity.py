#!/usr/bin/env python3
"""
MECHANISM 10 — GENERATION CAPACITY REMOVED
Scorer. Stdlib only.

Readouts:
  R1 recall_ratio      nameable / present, per place, per generation
  R2 transmission_gap  generations since capacity held at stated level
  R3 loop              deficit cited as grounds for the gate producing it

Returns '--' where readings do not exist. Does not estimate.
Does not compute a verdict.

Usage:
  capacity.py                 table over cases/
  capacity.py --case NAME     one case, detail
  capacity.py --new NAME      emit a blank case skeleton
  capacity.py --jsonl         machine readable
  capacity.py --selftest      synthetic fixtures
"""

import json
import os
import sys

CASES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases")

# scored_against values. CENTER invalidates R1 per the calibration constraint.
PLACE = "place"
CENTER = "center"


def load(path):
    with open(path) as f:
        return json.load(f)


def r1(case):
    """recall ratio per generation reading. None where unquantified."""
    out = []
    for g in case.get("generations", []):
        present = g.get("present")
        nameable = g.get("nameable")
        against = g.get("scored_against")
        if present in (None, 0) or nameable is None:
            out.append({"label": g.get("label"), "present": present,
                        "nameable": nameable, "ratio": None,
                        "valid": None, "scored_against": against})
            continue
        valid = (against == PLACE)
        out.append({"label": g.get("label"),
                    "present": present,
                    "nameable": nameable,
                    "ratio": nameable / present,
                    "valid": valid,
                    "scored_against": against})
    return out


def r2(case):
    """generations since capacity held at stated level. None if unset."""
    return case.get("transmission_gap")


def r3(case):
    """loop check. True/False/None."""
    loop = case.get("loop", {})
    cited = loop.get("deficit_cited_as_grounds")
    return cited


def slope(readings):
    """direction of change across valid ratios, first to last. None if <2."""
    vals = [r["ratio"] for r in readings if r["ratio"] is not None and r["valid"]]
    if len(vals) < 2:
        return None
    return vals[-1] - vals[0]


def fmt(x, nd=2):
    if x is None:
        return "--"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def score(case):
    readings = r1(case)
    quantified = sum(1 for r in readings if r["ratio"] is not None)
    invalid = sum(1 for r in readings if r["valid"] is False)
    return {
        "case": case.get("name"),
        "domain": case.get("domain"),
        "generations": len(readings),
        "quantified": quantified,
        "invalid_scoring": invalid,
        "readings": readings,
        "r1_slope": slope(readings),
        "r2_transmission_gap": r2(case),
        "r3_loop": r3(case),
    }


def table(scores):
    hdr = f"{'case':<26}{'gens':>5}{'quant':>7}{'slope':>8}{'r2':>5}{'r3':>6}"
    print(hdr)
    print("-" * len(hdr))
    for s in scores:
        print(f"{s['case']:<26}{s['generations']:>5}{s['quantified']:>7}"
              f"{fmt(s['r1_slope']):>8}{fmt(s['r2_transmission_gap']):>5}"
              f"{fmt(s['r3_loop']):>6}")
    print()
    print("slope: change in recall ratio, first valid reading to last.")
    print("'--' means no reading exists. Not zero, not an estimate.")


def detail(s):
    print(f"case:   {s['case']}")
    print(f"domain: {s['domain']}")
    print()
    print(f"{'generation':<20}{'present':>9}{'nameable':>10}{'ratio':>8}{'scored':>9}")
    print("-" * 56)
    for r in s["readings"]:
        print(f"{str(r['label']):<20}{fmt(r.get('present')):>9}"
              f"{fmt(r.get('nameable')):>10}"
              f"{fmt(r['ratio']):>8}{str(r['scored_against'] or '--'):>9}")
    print()
    print(f"R1 slope            {fmt(s['r1_slope'])}")
    print(f"R2 transmission_gap {fmt(s['r2_transmission_gap'])}")
    print(f"R3 loop             {fmt(s['r3_loop'])}")
    if s["invalid_scoring"]:
        print()
        print(f"WARNING: {s['invalid_scoring']} reading(s) scored against "
              f"center, not place. Invalid per calibration constraint.")


SKELETON = {
    "name": "",
    "domain": "",
    "quantity": "option space available to the affected party",
    "generations": [
        {"label": "", "present": None, "nameable": None,
         "scored_against": PLACE, "source_present": "", "source_nameable": ""}
    ],
    "transmission_gap": None,
    "loop": {
        "gate_holder": "",
        "excluded_party": "",
        "routing_blocked": None,
        "deficit_cited_as_grounds": None,
        "citation": ""
    },
    "found_constraint_tests": {
        "holds_under_push": None,
        "converts_to_urgency": None,
        "converts_to_asker_question": None
    },
    "notes": ""
}


def selftest():
    a = {"name": "declining", "domain": "t", "generations": [
        {"label": "g1", "present": 100, "nameable": 80, "scored_against": PLACE},
        {"label": "g2", "present": 100, "nameable": 20, "scored_against": PLACE},
    ], "transmission_gap": 2, "loop": {"deficit_cited_as_grounds": True}}
    b = {"name": "empty", "domain": "t", "generations": [
        {"label": "g1", "present": None, "nameable": None, "scored_against": PLACE},
    ]}
    c = {"name": "badscoring", "domain": "t", "generations": [
        {"label": "g1", "present": 100, "nameable": 50, "scored_against": CENTER},
        {"label": "g2", "present": 100, "nameable": 10, "scored_against": CENTER},
    ]}
    sa, sb, sc = score(a), score(b), score(c)
    checks = [
        ("declining slope negative", abs(sa["r1_slope"] - (-0.6)) < 1e-9),
        ("declining quantified 2", sa["quantified"] == 2),
        ("declining r3 true", sa["r3_loop"] is True),
        ("empty slope none", sb["r1_slope"] is None),
        ("empty r2 none", sb["r2_transmission_gap"] is None),
        ("empty r3 none", sb["r3_loop"] is None),
        ("center scoring flagged", sc["invalid_scoring"] == 2),
        ("center scoring no slope", sc["r1_slope"] is None),
    ]
    ok = 0
    for name, res in checks:
        print(f"{'PASS' if res else 'FAIL'}  {name}")
        ok += bool(res)
    print(f"\n{ok}/{len(checks)}")
    return 0 if ok == len(checks) else 1


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    if "--new" in args:
        i = args.index("--new")
        name = args[i + 1] if len(args) > i + 1 else "unnamed"
        sk = dict(SKELETON)
        sk["name"] = name
        print(json.dumps(sk, indent=2))
        return
    if not os.path.isdir(CASES):
        print("no cases/ directory", file=sys.stderr)
        sys.exit(1)
    files = sorted(f for f in os.listdir(CASES) if f.endswith(".json"))
    scores = [score(load(os.path.join(CASES, f))) for f in files]
    if "--jsonl" in args:
        for s in scores:
            print(json.dumps(s))
        return
    if "--case" in args:
        i = args.index("--case")
        want = args[i + 1] if len(args) > i + 1 else None
        for s in scores:
            if s["case"] == want:
                detail(s)
                return
        print(f"no case named {want}", file=sys.stderr)
        sys.exit(1)
    table(scores)


if __name__ == "__main__":
    main()
