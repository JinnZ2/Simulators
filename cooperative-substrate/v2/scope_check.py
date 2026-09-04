#!/usr/bin/env python3
"""scope_check.py -- the C1-C4 coding pass, SEEDED and extended, not
rewritten. The seed is `../scope_test.py`, which reads the four
conditions and five rows from EVIDENCE_PACK.md; this imports that parse
and its declared class and stress maps rather than restating them, adds
the harsh axis as a first-class field, and builds the NULL the v2 order
§3 asks for:

    find a harsh-environment study with C1-C4 ALL PRESENT.
      if competition still dominates there -> scope conditions are not
        sufficient; stress is doing independent work
      if no such study exists -> that absence is itself the finding

`extend(cases)` accepts new coded cases; the seed is not edited.
Refuses --selftest (checks live in selftest_v2.py).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import scope_test as SEED  # noqa: E402

CONDS = ("C1", "C2", "C3", "C4")

# Harshness of each seeded row, and whether it is INDEPENDENT of the
# scoring apparatus. A reading, stated here, not computed -- the same
# form as SEED.STRESS_AXIS. The E. coli row's harshness is the antibiotic
# it is scored under, so it is not separable from C2 (externally imposed
# win condition) and C3 (single scalar): harshness == apparatus.
HARSH_INDEPENDENT = {
    "E. coli evolvability": (False, "harsh = growth under stepwise antibiotic, which IS the C2/C3 scoring apparatus"),
    "multiagent turf harness": ("UNRECORDED", None),
    "Austronesian games": ("UNRECORDED", None),
    "optimal foraging (field)": ("UNRECORDED", None),
    "lichen altitudinal grad.": ("UNRECORDED", "stress is a gradient, not scored as harsh; SEED marks it 'gradient'"),
}


def seed_cases():
    """The five rows from the seed, each a coded case with a harsh axis."""
    conds, rows = SEED.parse()
    cases = []
    for r in rows:
        stress, _ = SEED.STRESS_AXIS.get(r["name"], ("UNRECORDED", None))
        cases.append({"name": r["name"], "cells": dict(r["cells"]),
                      "reported": SEED.REPORTED_CLASS.get(r["name"], "UNRECORDED"),
                      "harsh": stress == "harsh",
                      "harsh_independent": HARSH_INDEPENDENT.get(r["name"], ("UNRECORDED", None))})
    return conds, cases


def classify(case, conds=CONDS):
    return SEED.conjunction({"cells": case["cells"]}, conds)


def all_present(case, conds=CONDS):
    return all(case["cells"].get(c) == "y" for c in conds)


def null_search(cases, conds=CONDS):
    """The order's §3 null. Antecedent: harsh AND all C1-C4 present AND
    competition reported. If met, the reading turns on whether the
    harshness is INDEPENDENT of the apparatus: if it is, scope conditions
    are not sufficient and stress does independent work; if it is not,
    the case cannot resolve the null and one with independent harshness
    is needed -- which the seed lacks."""
    antecedent = [c for c in cases if c["harsh"] and all_present(c, conds) and c["reported"] == "competition_reported"]
    if not antecedent:
        return {"antecedent_met_by": [], "verdict": "ABSENCE_IS_THE_FINDING",
                "reason": "no harsh + all-C1-C4 + competition-reported case in the set"}
    resolving = [c for c in antecedent if c["harsh_independent"][0] is True]
    entangled = [c for c in antecedent if c["harsh_independent"][0] is False]
    if resolving:
        return {"antecedent_met_by": [c["name"] for c in antecedent], "verdict": "SCOPE_NOT_SUFFICIENT",
                "reason": "a case has harsh, all C1-C4, competition reported, and harshness independent of the apparatus: stress does independent work",
                "resolving": [c["name"] for c in resolving]}
    return {"antecedent_met_by": [c["name"] for c in antecedent], "verdict": "UNRESOLVED_HARSHNESS_ENTANGLED",
            "reason": "the antecedent is met, but the only harsh case's harshness IS the C2/C3 apparatus, so it cannot separate stress from scoping; a case with independent environmental harshness is needed and the seed lacks one",
            "entangled": [(c["name"], c["harsh_independent"][1]) for c in entangled]}


def extend(cases, new):
    """Append coded cases. Each needs name, cells (C1-C4 in y/n), reported
    and harsh; the seed is not modified. Refuses a malformed case."""
    out = list(cases)
    for c in new:
        for k in ("name", "cells", "reported", "harsh"):
            if k not in c:
                raise ValueError("case missing %r" % k)
        if any(c["cells"].get(x) not in ("y", "n") for x in CONDS):
            raise ValueError("case %r: every C1-C4 cell must be y or n" % c["name"])
        c.setdefault("harsh_independent", ("UNRECORDED", None))
        out.append(c)
    return out


def render():
    conds, cases = seed_cases()
    L = ["scope_check (C1-C4), seeded from ../scope_test.py, extended not rewritten"]
    for c in cases:
        L.append("  %-26s %s harsh %-6s independent %-6s -> %-36s [%s]" % (
            c["name"], " ".join("%s %s" % (x, c["cells"].get(x, "?")) for x in conds),
            c["harsh"], str(c["harsh_independent"][0]), c["reported"], classify(c)))
    ns = null_search(cases)
    L.append("null search (§3): antecedent met by %s -> %s" % (ns["antecedent_met_by"], ns["verdict"]))
    L.append("  %s" % ns["reason"])
    if ns.get("entangled"):
        for name, why in ns["entangled"]:
            L.append("  entangled: %s -- %s" % (name, why))
    L.append("SGH pressure: the seed's one harsh case has harshness == apparatus, so 'benign' is not shown to be the operative variable here")
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("scope_check has no selftest; run selftest_v2.py", file=sys.stderr)
        sys.exit(2)
    print(render())
