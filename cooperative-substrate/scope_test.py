#!/usr/bin/env python3
"""The evidence pack's E8 scope test, read from the pack itself: four
conditions a competition-dominant observation is said to require
jointly, and five rows scored on them. Parsed from EVIDENCE_PACK.md so
an edit there and not here turns the selftest red. Cells are
three-valued (y / n / UNRECORDED). Computes what the table can and
cannot separate, and reads the stress axis of E0.1 against the design
axis of C1-C4 on the rows where the pack states both.

    python3 scope_test.py
Refuses --selftest (checks live in selftest_evidence.py).
"""

import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, "EVIDENCE_PACK.md")

COND = re.compile(r"^\s+(C\d)\s+(.+?)\s{2,}(.+?)\s*$")
ROW = re.compile(r"^(\S.*?)\s{2,}((?:C\d\s+[yn]\s+)+)->\s*(.+?)\s*$")

# Declared readings of the pack's arrow text, so the separation checks
# have two classes to separate. A reading, stated here, not computed.
REPORTED_CLASS = {
    "E. coli evolvability": "competition_reported",
    "multiagent turf harness": "competition_reported",
    "Austronesian games": "competition_reported",
    "optimal foraging (field)": "not_reported",
    "lichen altitudinal grad.": "not_reported",
}

# The stress axis of E0.1 per row, as the pack states it (quoted span)
# or UNRECORDED where the pack states no environmental stress.
STRESS_AXIS = {
    "E. coli evolvability": ("harsh", "adaptation scored as growth under stepwise antibiotic"),
    "multiagent turf harness": ("UNRECORDED", None),
    "Austronesian games": ("UNRECORDED", None),
    "optimal foraging (field)": ("UNRECORDED", None),
    "lichen altitudinal grad.": ("gradient", "along independent altitudinal gradients"),
}


def parse(text=None):
    text = text if text is not None else open(PACK, encoding="utf-8").read()
    tail = text.split("test for actual competition scope by:")[1]
    conds, rows = {}, []
    for line in tail.splitlines():
        m = COND.match(line)
        if m and not ROW.match(line):
            conds[m.group(1)] = (m.group(2), m.group(3))
            continue
        m = ROW.match(line)
        if m:
            cells = dict(re.findall(r"(C\d)\s+([yn])", m.group(2)))
            rows.append({"name": m.group(1).strip(), "cells": cells, "reported": m.group(3)})
    return conds, rows


def cell(row, c):
    return row["cells"].get(c, "UNRECORDED")


def conjunction(row, conds):
    vals = [cell(row, c) for c in conds]
    if any(v == "n" for v in vals):
        return "NOT_COMPETITION_DOMINANT_OBSERVATION"
    if all(v == "y" for v in vals):
        return "COMPETITION_DOMINANT_OBSERVATION"
    return "UNDETERMINED"


def separation(conds, rows):
    """Which conditions, alone and in subsets, separate the two declared
    classes; how many distinct condition vectors the rows carry."""
    vectors = {tuple(cell(r, c) for c in conds) for r in rows}
    classes = {r["name"]: REPORTED_CLASS.get(r["name"], "UNRECORDED") for r in rows}

    def separates(subset):
        seen = {}
        for r in rows:
            key = tuple(cell(r, c) for c in subset)
            cls = classes[r["name"]]
            if key in seen and seen[key] != cls:
                return False
            seen[key] = cls
        return True

    alone = {c: separates((c,)) for c in conds}
    minimal = []
    for k in range(1, len(conds) + 1):
        for sub in itertools.combinations(conds, k):
            if separates(sub) and not any(set(m) <= set(sub) for m in minimal):
                minimal.append(sub)
    necessary = [c for c in conds if not separates(tuple(x for x in conds if x != c))]
    return {"distinct_vectors": len(vectors), "rows": len(rows), "separates_alone": alone,
            "minimal_separating_subsets": minimal, "necessary": necessary,
            "conditions_vary_independently": len(vectors) > 2}


def axes(rows, conds):
    """Stress axis (E0.1: harsh -> facilitation, benign -> competition)
    against the design axis (C1-C4) on rows where both are recorded."""
    out = []
    for r in rows:
        stress, span = STRESS_AXIS.get(r["name"], ("UNRECORDED", None))
        design = conjunction(r, conds)
        e01 = {"harsh": "facilitation", "benign": "competition"}.get(stress, "UNRECORDED")
        reported = REPORTED_CLASS.get(r["name"], "UNRECORDED")
        both = stress in ("harsh", "benign") and design != "UNDETERMINED"
        agree = None
        if both:
            agree = (e01 == "competition") == (reported == "competition_reported")
        out.append({"row": r["name"], "stress": stress, "stress_span": span, "e01_predicts": e01,
                    "design": design, "reported": reported, "both_axes_recorded": both,
                    "e01_matches_reported": agree})
    return out


def benign_reading():
    """What the pack's last line asks for, stated as a test and not run."""
    return {
        "as_used": "E0.1 gives 'benign' no axis of its own: it is the end of the stress gradient where "
                   "competition is observed, which reads the outcome back as the condition",
        "test": "removal test: a condition is benign for a coupling when removing the partner leaves "
                "the focal yield unchanged; harsh when yield falls. Yield measured, partner removed, "
                "selection history held (E4) and a partner pool present (E5) -- the E6 design.",
        "status": "NOT_RUN",
    }


def render():
    conds, rows = parse()
    L = ["scope test (E8), parsed from EVIDENCE_PACK.md"]
    for c, (short, long_) in conds.items():
        L.append("  %s %-14s %s" % (c, short, long_))
    for r in rows:
        L.append("  %-26s %s  -> %s  [%s]" % (r["name"], " ".join("%s %s" % (c, cell(r, c)) for c in conds),
                                              r["reported"], conjunction(r, conds)))
    s = separation(conds, rows)
    L.append("distinct condition vectors: %d over %d rows; conditions vary independently: %s" % (
        s["distinct_vectors"], s["rows"], s["conditions_vary_independently"]))
    L.append("separates alone: %s; minimal separating subsets: %s; necessary: %s" % (
        s["separates_alone"], [",".join(m) for m in s["minimal_separating_subsets"]], s["necessary"]))
    L.append("stress axis (E0.1) against design axis (C1-C4):")
    for a in axes(rows, conds):
        L.append("  %-26s stress %-10s e01 %-12s design %-36s reported %-21s both %s match %s" % (
            a["row"], a["stress"], a["e01_predicts"], a["design"], a["reported"], a["both_axes_recorded"], a["e01_matches_reported"]))
    b = benign_reading()
    L.append("'benign': as used -- %s" % b["as_used"])
    L.append("'benign': test -- %s  [%s]" % (b["test"], b["status"]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("scope_test has no selftest; run selftest_evidence.py", file=sys.stderr)
        sys.exit(2)
    print(render())
