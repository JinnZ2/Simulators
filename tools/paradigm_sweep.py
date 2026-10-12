#!/usr/bin/env python3
"""paradigm_sweep.py - contrast-then-obliques sweep. CC0. stdlib only.

Move: paradigm (input) -> contrast/inverse (input, sets axis) -> obliques off
the axis -> each bearing is a literature query -> mark status -> classify.
Tool processes; it does not judge. Judgment fields are user input/output.

Usage:
  paradigm_sweep.py new --paradigm contain --inverse "utilize what it does" \
      --domain "fusion plasma" --home "plasma physics,fusion engineering" -o sweep.json
  paradigm_sweep.py add sweep.json --family custom --question "..."
  paradigm_sweep.py set sweep.json B03 --status EMPTY --opens yes \
      --study "ref|field|note"
  paradigm_sweep.py queries sweep.json
  paradigm_sweep.py report sweep.json
  paradigm_sweep.py selftest
"""
import argparse, json, sys
from dataclasses import dataclass, field, asdict

STATUS = ("UNCHECKED", "EMPTY", "PARTIAL", "DENSE")

FAMILIES = {
    "contrast": ["{inverse} instead of {paradigm}"],
    "relation": [
        "power-over: {paradigm} {domain} fully",
        "power-under: let {domain} set the terms; build around what it does",
        "power-with: co-regulate with {domain}",
        "partial power-over: {paradigm} only some degrees of freedom of {domain}",
        "no power relation: what does {domain} do left alone",
    ],
    "scale": [
        "many small {domain} instead of one large",
        "{domain} at a much larger or much smaller scale",
    ],
    "time": [
        "do not hold {domain} steady; cycle or pulse it and harvest each relaxation",
        "what is usable from {domain} before '{paradigm}' becomes necessary",
    ],
    "multiplicity": ["swarm: many interacting {domain} at once; the interaction is the object"],
    "signal": ["treat whatever defeats '{paradigm}' as the readout, not the enemy"],
    "borrowed": ["let another system do the work of '{paradigm}' (external field, medium, constraint)"],
    "incentive": [
        "who is rewarded for '{paradigm}'; what does the unrewarded angle look like",
        "what would get funded if '{inverse}' were the default",
    ],
}

@dataclass
class Bearing:
    id: str
    family: str
    question: str
    query: str = ""
    opens_new_space: object = None      # user judgment: "yes" / "no" / None
    status: str = "UNCHECKED"
    studies: list = field(default_factory=list)   # [{"ref","field","note"}]
    notes: str = ""

@dataclass
class Sweep:
    paradigm: str
    inverse: str
    domain: str
    home_fields: list
    bearings: list = field(default_factory=list)

def _next_id(sw):
    return f"B{len(sw.bearings) + 1:02d}"

def new_sweep(paradigm, inverse, domain, home_fields, families=None):
    sw = Sweep(paradigm, inverse, domain, list(home_fields))
    ctx = dict(paradigm=paradigm, inverse=inverse, domain=domain)
    for fam, temps in FAMILIES.items():
        if families and fam not in families:
            continue
        for t in temps:
            q = t.format(**ctx)
            sw.bearings.append(Bearing(_next_id(sw), fam, q, f"{domain} :: {q}"))
    return sw

def add_bearing(sw, family, question):
    b = Bearing(_next_id(sw), family, question, f"{sw.domain} :: {question}")
    sw.bearings.append(b)
    return b

def classify(b, home):
    if b.status == "UNCHECKED":
        return "UNCHECKED"
    if b.status == "EMPTY":
        return "LOCATED_GAP"
    if any(s.get("field") and s["field"] not in home for s in b.studies):
        return "UNJOINED_INTERSECTION"
    if b.status == "PARTIAL":
        return "EDGE"
    return "MAPPED"

def save(sw, path):
    with open(path, "w") as f:
        json.dump(asdict(sw), f, indent=2)

def load(path):
    with open(path) as f:
        d = json.load(f)
    d["bearings"] = [Bearing(**b) for b in d.get("bearings", [])]
    return Sweep(**d)

def report(sw):
    order = ["LOCATED_GAP", "UNJOINED_INTERSECTION", "EDGE", "MAPPED", "UNCHECKED"]
    groups = {k: [] for k in order}
    for b in sw.bearings:
        groups[classify(b, sw.home_fields)].append(b)
    lines = [f"PARADIGM: {sw.paradigm}  |  CONTRAST: {sw.inverse}  |  DOMAIN: {sw.domain}"]
    for k in order:
        if not groups[k]:
            continue
        lines.append(f"\n[{k}] ({len(groups[k])})")
        for b in groups[k]:
            o = "" if b.opens_new_space is None else f" opens={b.opens_new_space}"
            flds = sorted({s.get('field', '?') for s in b.studies})
            fs = f" fields={flds}" if flds else ""
            lines.append(f"  {b.id} [{b.family}] {b.question}{o}{fs}")
    return "\n".join(lines)

def _parse_study(s):
    parts = (s.split("|") + ["", "", ""])[:3]
    return {"ref": parts[0].strip(), "field": parts[1].strip(), "note": parts[2].strip()}

def selftest():
    sw = new_sweep("contain", "utilize what it does", "fusion plasma",
                   ["plasma physics", "fusion engineering"])
    assert sw.bearings[0].family == "contrast"
    assert any(b.family == "multiplicity" for b in sw.bearings)
    b_gap, b_join, b_edge, b_map = sw.bearings[1:5]
    b_gap.status = "EMPTY"
    b_join.status = "DENSE"
    b_join.studies.append({"ref": "x", "field": "slime mold ecology", "note": ""})
    b_edge.status = "PARTIAL"
    b_edge.studies.append({"ref": "y", "field": "plasma physics", "note": ""})
    b_map.status = "DENSE"
    b_map.studies.append({"ref": "z", "field": "fusion engineering", "note": ""})
    h = sw.home_fields
    assert classify(b_gap, h) == "LOCATED_GAP"
    assert classify(b_join, h) == "UNJOINED_INTERSECTION"
    assert classify(b_edge, h) == "EDGE"
    assert classify(b_map, h) == "MAPPED"
    add_bearing(sw, "custom", "plasma swarm coupled to an external field")
    save(sw, "_selftest_sweep.json")
    sw2 = load("_selftest_sweep.json")
    assert len(sw2.bearings) == len(sw.bearings)
    assert classify(sw2.bearings[2], h) == "UNJOINED_INTERSECTION"
    import os
    os.remove("_selftest_sweep.json")
    assert "LOCATED_GAP" in report(sw)
    print("SELFTEST OK")

def main(argv=None):
    p = argparse.ArgumentParser(description="contrast-then-obliques sweep")
    sp = p.add_subparsers(dest="cmd", required=True)

    n = sp.add_parser("new")
    n.add_argument("--paradigm", required=True)
    n.add_argument("--inverse", required=True)
    n.add_argument("--domain", required=True)
    n.add_argument("--home", default="")
    n.add_argument("--families", default="")
    n.add_argument("-o", "--out", default="sweep.json")

    a = sp.add_parser("add")
    a.add_argument("path")
    a.add_argument("--family", default="custom")
    a.add_argument("--question", required=True)

    s = sp.add_parser("set")
    s.add_argument("path")
    s.add_argument("id")
    s.add_argument("--status", choices=STATUS)
    s.add_argument("--opens")
    s.add_argument("--study", action="append", default=[])
    s.add_argument("--notes")

    for name in ("queries", "report"):
        sp.add_parser(name).add_argument("path")
    sp.add_parser("selftest")

    args = p.parse_args(argv)
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "new":
        home = [x.strip() for x in args.home.split(",") if x.strip()]
        fams = [x.strip() for x in args.families.split(",") if x.strip()] or None
        sw = new_sweep(args.paradigm, args.inverse, args.domain, home, fams)
        save(sw, args.out)
        print(f"{len(sw.bearings)} bearings -> {args.out}")
        return
    sw = load(args.path)
    if args.cmd == "add":
        b = add_bearing(sw, args.family, args.question)
        save(sw, args.path)
        print(b.id)
    elif args.cmd == "set":
        b = next((x for x in sw.bearings if x.id == args.id), None)
        if b is None:
            sys.exit(f"no bearing {args.id}")
        if args.status:
            b.status = args.status
        if args.opens is not None:
            b.opens_new_space = args.opens
        b.studies += [_parse_study(x) for x in args.study]
        if args.notes:
            b.notes = args.notes
        save(sw, args.path)
        print(f"{b.id} -> {classify(b, sw.home_fields)}")
    elif args.cmd == "queries":
        for b in sw.bearings:
            print(f"{b.id}\t{b.query}")
    elif args.cmd == "report":
        print(report(sw))

if __name__ == "__main__":
    main()
