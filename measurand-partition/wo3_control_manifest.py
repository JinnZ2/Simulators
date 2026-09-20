#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
wo3_control_manifest -- CONTROL MANIFEST AND PREDICTION-ACCURACY FLOOR.

A prediction cannot be scored against an outcome whose variance the
predictor does not control. Longitudinal work scores a coach's selection
judgment against outcomes years downstream and assigns the whole
residual to the judgment; between the two sit variables the observer
does not control. Three deliverables, in the order's order:

  WO-3a CONTROL MANIFEST  per program, per variable: HELD / ADVISED_ON /
        NOT_TOUCHED, with UNDECLARED kept apart from NOT_TOUCHED. Each
        variable carries its controllability class from the order.
        ADVISED_ON is not control -- education on intake is an
        intervention on knowledge -- and is never counted as a fraction
        of HELD.
  WO-3b CONTROL GRADIENT  the share of controllable-in-principle
        variables HELD, per program; NOT_COMPUTABLE while any variable is
        UNDECLARED. Prediction accuracy against that gradient is a trend
        readout that needs three programs with both numbers and returns
        NOT_EVALUABLE below that.
  WO-3c ACCURACY FLOOR  the ceiling on achievable accuracy is 1 minus the
        outcome-variance share of the not-controllable-in-principle
        variables. Every share is a DECLARED input; a ceiling with any
        such share undeclared is UNDECLARED, which is the state the
        literature reads its reliability results in (an implicit 100%).
        `read_against_ceiling` re-reads a reported accuracy as a share of
        the achievable one.

Nothing here rates any program, coach or athlete. The seed manifest is
the order's own partial variable list; the statuses on the demo program
are the order's own reading of published academy descriptions
(EDUCATION on nutrition and hydration -> ADVISED_ON) and are CARRIED, not
verified. The 6.3 h sleep figure is carried the same way and enters no
computation.

Python 3.9, ASCII only, stdlib only. Refuses --selftest.
"""

from __future__ import annotations

import sys

from common import Refused, absent, refuse_selftest

CONTROLLABLE = "CONTROLLABLE_IN_PRINCIPLE"
NOT_CONTROLLABLE = "NOT_CONTROLLABLE_IN_PRINCIPLE"
CLASSES = (CONTROLLABLE, NOT_CONTROLLABLE)
STATUSES = ("HELD", "ADVISED_ON", "NOT_TOUCHED", "UNDECLARED")
MIN_PROGRAMS = 3   # [CHOICE 2]
CHOICES = {
    1: "the gradient counts HELD over controllable variables only; "
       "ADVISED_ON is reported beside it and never as a fraction of HELD",
    2: "the accuracy-vs-gradient trend requires %d programs carrying both a "
       "gradient and a measured accuracy; below that NOT_EVALUABLE"
       % MIN_PROGRAMS,
    3: "variance shares are declared inputs summing to at most 1; the "
       "ceiling is 1 - sum(shares of not-controllable variables), "
       "UNDECLARED if any such share is",
}

# the order's partial list, carried
VARIABLES = {
    "nutrition": CONTROLLABLE,
    "hydration": CONTROLLABLE,
    "sleep opportunity": CONTROLLABLE,
    "training load": CONTROLLABLE,
    "coaching contact": CONTROLLABLE,
    "endocrine developmental timing": NOT_CONTROLLABLE,
    "experienced social environment": NOT_CONTROLLABLE,
}


def read_program(rec):
    """Fields: id, statuses {variable: status}, accuracy (measured
    prediction accuracy in [0,1] or None), status tag."""
    for k in ("id", "statuses", "accuracy", "status"):
        if k not in rec:
            raise Refused("program %s: missing %s" % (rec.get("id"), k))
    if rec["status"] not in ("OBSERVED", "DERIVED", "PROPOSED"):
        raise Refused("program %s: status %r" % (rec["id"], rec["status"]))
    st = dict(rec["statuses"])
    for v in VARIABLES:
        if v not in st:
            st[v] = "UNDECLARED"      # absent is UNDECLARED, never NOT_TOUCHED
        if st[v] not in STATUSES:
            raise Refused("program %s: status %r on %s" % (rec["id"], st[v], v))
    for v in st:
        if v not in VARIABLES:
            raise Refused("program %s: %s is not a manifest variable"
                          % (rec["id"], v))
    a = rec["accuracy"]
    if a is not None and (isinstance(a, bool) or not isinstance(a, (int, float))
                          or not 0 <= a <= 1):
        raise Refused("program %s: accuracy must be in [0,1] or None" % rec["id"])
    out = dict(rec)
    out["statuses"] = st
    return out


def manifest(program):
    """WO-3a. One row per variable."""
    return [{"variable": v, "class": VARIABLES[v], "status": program["statuses"][v]}
            for v in VARIABLES]


def control_gradient(program):
    """WO-3b, the grade. [CHOICE 1]."""
    rows = manifest(program)
    ctrl = [r for r in rows if r["class"] == CONTROLLABLE]
    undeclared = [r["variable"] for r in rows if r["status"] == "UNDECLARED"]
    held = [r["variable"] for r in ctrl if r["status"] == "HELD"]
    advised = [r["variable"] for r in ctrl if r["status"] == "ADVISED_ON"]
    not_touched = [r["variable"] for r in ctrl if r["status"] == "NOT_TOUCHED"]
    if undeclared:
        return {"id": program["id"], "state": "NOT_COMPUTABLE",
                "gradient": None, "undeclared": undeclared,
                "held": held, "advised_on": advised, "not_touched": not_touched}
    return {"id": program["id"], "state": "COMPUTED",
            "gradient": len(held) / float(len(ctrl)), "undeclared": [],
            "held": held, "advised_on": advised, "not_touched": not_touched}


def accuracy_vs_gradient(programs):
    """WO-3b, the test. Sign of the trend of measured accuracy against the
    gradient over programs carrying both; NOT_EVALUABLE below MIN_PROGRAMS.
    A sign, not a coefficient: nothing here is a fit."""
    pts = []
    for p in programs:
        g = control_gradient(p)
        if g["gradient"] is not None and p["accuracy"] is not None:
            pts.append((g["gradient"], p["accuracy"]))
    if len(pts) < MIN_PROGRAMS:
        return {"state": "NOT_EVALUABLE", "n": len(pts), "trend": None,
                "reads": "fewer than %d programs carry both a gradient and "
                         "a measured accuracy; 'the eye is unreliable' stays "
                         "UNPARTITIONED" % MIN_PROGRAMS}
    if len(set(g for g, _ in pts)) < 2:
        return {"state": "NOT_EVALUABLE", "n": len(pts), "trend": None,
                "reads": "every program sits at one gradient; no trend"}
    mg = sum(g for g, _ in pts) / len(pts)
    ma = sum(a for _, a in pts) / len(pts)
    cov = sum((g - mg) * (a - ma) for g, a in pts)
    trend = "RISES" if cov > 0 else ("FALLS" if cov < 0 else "FLAT")
    return {"state": "EVALUATED", "n": len(pts), "trend": trend,
            "reads": "accuracy %s with control; a rise partitions some of "
                     "the residual off the judgment, a flat trend leaves it "
                     "there" % trend.lower()}


def accuracy_floor(shares):
    """WO-3c. shares: {variable: share of outcome variance or None}.
    Ceiling = 1 - sum of the not-controllable shares; UNDECLARED when any
    of those is None. [CHOICE 3]."""
    for v in shares:
        if v not in VARIABLES:
            raise Refused("share on %s, not a manifest variable" % v)
    nc = [v for v, c in VARIABLES.items() if c == NOT_CONTROLLABLE]
    missing = [v for v in nc if shares.get(v) is None]
    if missing:
        return {"state": "UNDECLARED", "ceiling": None, "missing": missing,
                "reads": "no ceiling can be stated; a reliability figure "
                         "read here is read against an implicit 100%"}
    tot = sum(s for s in shares.values() if s is not None)
    if tot > 1.0 + 1e-9 or any(s < 0 for s in shares.values() if s is not None):
        raise Refused("variance shares must be non-negative and sum to <= 1")
    ceiling = 1.0 - sum(shares[v] for v in nc)
    return {"state": "STATED", "ceiling": ceiling, "missing": [],
            "reads": "achievable accuracy is capped at %.2f by variables no "
                     "observer controls" % ceiling}


def read_against_ceiling(reported, floor):
    """A reported accuracy as a share of the achievable one. None when the
    ceiling is UNDECLARED or zero."""
    c = floor["ceiling"]
    if reported is None or c is None or c <= 1e-9:
        return None
    return reported / c


# --- constructed demo, PROPOSED ---------------------------------------------

DEMO_PROGRAMS = [
    read_program({"id": "academy-as-described",
                  "statuses": {"nutrition": "ADVISED_ON", "hydration": "ADVISED_ON",
                               "sleep opportunity": "NOT_TOUCHED",
                               "training load": "HELD", "coaching contact": "HELD",
                               "endocrine developmental timing": "NOT_TOUCHED",
                               "experienced social environment": "NOT_TOUCHED"},
                  "accuracy": None, "status": "PROPOSED"}),
    read_program({"id": "day-program", "statuses": {"training load": "HELD"},
                  "accuracy": None, "status": "PROPOSED"}),
]

DEMO_SHARES_UNDECLARED = {"endocrine developmental timing": None,
                          "experienced social environment": None}
DEMO_SHARES_STATED = {"endocrine developmental timing": 0.25,
                      "experienced social environment": 0.15,
                      "training load": 0.10}


def render(programs=None):
    ps = DEMO_PROGRAMS if programs is None else programs
    out = ["WO-3  CONTROL MANIFEST   (programs CONSTRUCTED, PROPOSED; the "
           "academy statuses are the order's reading, CARRIED)", "-" * 72]
    for p in ps:
        out.append("  program %s" % p["id"])
        for r in manifest(p):
            out.append("    %-32s %-30s %s" % (r["variable"], r["class"], r["status"]))
        g = control_gradient(p)
        out.append("    gradient %s   held %d   advised_on %d   not_touched %d"
                   "   undeclared %s  [CHOICE 1]"
                   % (g["state"] if g["gradient"] is None else "%.2f" % g["gradient"],
                      len(g["held"]), len(g["advised_on"]), len(g["not_touched"]),
                      ",".join(g["undeclared"]) or "-"))
    t = accuracy_vs_gradient(ps)
    out.append("  WO-3b accuracy vs gradient: %s (n %d)  [CHOICE 2]" % (t["state"], t["n"]))
    out.append("    " + t["reads"])
    fu = accuracy_floor(DEMO_SHARES_UNDECLARED)
    fs = accuracy_floor(DEMO_SHARES_STATED)
    out.append("  WO-3c accuracy floor, shares undeclared: %s  missing %s"
               % (fu["state"], ",".join(fu["missing"])))
    out.append("  WO-3c accuracy floor, shares CONSTRUCTED: %s  ceiling %.2f   "
               "a reported 0.60 reads %.2f of achievable  [CHOICE 3]"
               % (fs["state"], fs["ceiling"], read_against_ceiling(0.60, fs)))
    out.append("  the 6.3 h against 8-10 h sleep figure is carried from the "
               "order and enters no computation")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("wo3_control_manifest.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
