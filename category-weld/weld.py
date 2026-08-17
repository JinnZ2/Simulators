#!/usr/bin/env python3
# CC0. stdlib only. python3 weld.py [--term T] [--jsonl] [--new TERM]
#
# Reads welds/*.json, emits three readouts per term:
#   n_cases     how many divergence cases are named
#   max_spread  largest ratio between component relative-changes in one case
#   bias        how consistently divergence runs the same direction (0..1)
#
# Cases without paired before/after readings still count toward n_cases
# and are reported separately as n_unquantified. They do not contribute
# to max_spread or bias. An unquantified case is a gap marker, not a
# smaller case.

import argparse
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WELDDIR = os.path.join(HERE, "welds")


def load_welds(path=WELDDIR):
    out = []
    for f in sorted(glob.glob(os.path.join(path, "*.json"))):
        with open(f, "r", encoding="utf-8") as fh:
            w = json.load(fh)
        w["_file"] = os.path.basename(f)
        out.append(w)
    return out


def rel_change(reading):
    """after/before as a ratio. None if unusable."""
    if not reading:
        return None
    b = reading.get("before")
    a = reading.get("after")
    if b is None or a is None:
        return None
    try:
        b = float(b)
        a = float(a)
    except (TypeError, ValueError):
        return None
    if b == 0:
        return None
    if a <= 0 or b < 0:
        return None
    return a / b


def case_spread(case, components):
    """Max ratio between any two component relative-changes in this case.

    Returns (spread, ratios) or (None, {}) if fewer than two components
    have usable paired readings.
    """
    ratios = {}
    for cid in components:
        r = rel_change(case.get("readings", {}).get(cid))
        if r is not None:
            ratios[cid] = r
    if len(ratios) < 2:
        return None, ratios
    vals = list(ratios.values())
    spread = max(vals) / min(vals)
    return spread, ratios


def case_direction(case, tracked, ratios):
    """+1 if the untracked component fell relative to the tracked one,
    -1 if it rose relative, 0 if not resolvable.

    'tracked' is the component the term is read off in practice. The
    direction says which side of the weld is being hidden.
    """
    if tracked not in ratios:
        return 0
    others = {k: v for k, v in ratios.items() if k != tracked}
    if not others:
        return 0
    # widest-diverging other component sets the direction for the case
    far = max(others.items(), key=lambda kv: abs(math.log(kv[1] / ratios[tracked])))
    d = math.log(far[1] / ratios[tracked])
    if d == 0:
        return 0
    return -1 if d < 0 else 1


def score(weld):
    comps = [c["id"] for c in weld.get("components", [])]
    tracked = weld.get("tracked_by_label")
    cases = weld.get("divergences", [])

    spreads = []
    dirs = []
    for c in cases:
        s, ratios = case_spread(c, comps)
        if s is None:
            continue
        spreads.append(s)
        d = case_direction(c, tracked, ratios)
        if d != 0:
            dirs.append(d)

    n_cases = len(cases)
    n_quant = len(spreads)
    max_spread = max(spreads) if spreads else None
    bias = abs(sum(dirs)) / len(dirs) if dirs else None

    return {
        "term": weld.get("term"),
        "domain": weld.get("domain"),
        "n_components": len(comps),
        "n_cases": n_cases,
        "n_quantified": n_quant,
        "n_unquantified": n_cases - n_quant,
        "max_spread": max_spread,
        "bias": bias,
    }


def fmt(v, nd=2):
    if v is None:
        return "--"
    if isinstance(v, float):
        return ("%." + str(nd) + "f") % v
    return str(v)


def table(rows):
    hdr = ["term", "comp", "cases", "quant", "spread", "bias"]
    print("  ".join(h.ljust(w) for h, w in zip(hdr, [18, 4, 5, 5, 7, 5])))
    print("-" * 50)
    for r in rows:
        line = [
            str(r["term"])[:18].ljust(18),
            str(r["n_components"]).ljust(4),
            str(r["n_cases"]).ljust(5),
            str(r["n_quantified"]).ljust(5),
            fmt(r["max_spread"]).ljust(7),
            fmt(r["bias"]).ljust(5),
        ]
        print("  ".join(line))
    print()
    print("spread/bias read only from cases with paired before+after")
    print("readings. '--' means no case is quantified yet.")


def detail(weld):
    s = score(weld)
    print("TERM      %s" % s["term"])
    print("DOMAIN    %s" % s["domain"])
    print("TRACKED   %s" % weld.get("tracked_by_label"))
    print()
    print("COMPONENTS")
    for c in weld.get("components", []):
        print("  %-14s %s [%s]" % (c["id"], c.get("name", ""), c.get("unit", "")))
    print()
    print("DIVERGENCE CASES")
    comps = [c["id"] for c in weld.get("components", [])]
    for c in weld.get("divergences", []):
        sp, ratios = case_spread(c, comps)
        mark = fmt(sp) + "x" if sp else "unquantified"
        print("  [%s] %s" % (mark, c.get("id", "")))
        for line in wrap(c.get("note", ""), 66):
            print("      " + line)
        for cid, r in ratios.items():
            print("        %-14s x%.3f" % (cid, r))
    print()
    print("READOUTS  cases=%s quantified=%s spread=%s bias=%s" % (
        s["n_cases"], s["n_quantified"], fmt(s["max_spread"]), fmt(s["bias"])))


def wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


TEMPLATE = {
    "term": "",
    "domain": "",
    "tracked_by_label": "",
    "components": [
        {"id": "", "name": "", "unit": ""},
        {"id": "", "name": "", "unit": ""}
    ],
    "divergences": [
        {
            "id": "",
            "note": "",
            "readings": {
                "": {"before": None, "after": None, "source": ""}
            }
        }
    ]
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--term", help="detail view for one term")
    p.add_argument("--jsonl", action="store_true", help="one score per line")
    p.add_argument("--new", metavar="TERM", help="emit a blank weld file")
    a = p.parse_args()

    if a.new:
        t = dict(TEMPLATE)
        t["term"] = a.new
        print(json.dumps(t, indent=2))
        return

    welds = load_welds()
    if not welds:
        print("no weld files in %s" % WELDDIR, file=sys.stderr)
        return 1

    if a.term:
        for w in welds:
            if w.get("term") == a.term:
                detail(w)
                return
        print("no such term: %s" % a.term, file=sys.stderr)
        return 1

    rows = [score(w) for w in welds]
    if a.jsonl:
        for r in rows:
            print(json.dumps(r))
    else:
        table(rows)


if __name__ == "__main__":
    sys.exit(main() or 0)
