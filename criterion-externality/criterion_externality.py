#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
criterion_externality -- WO-6, the fourth independence axis, built to the
order and run on a CONSTRUCTED model.

The order's target paper (arXiv:2609.18272) was read by its author at
abstract level only, and from here the host refuses CONNECT (probe
recorded in R1 below), so the paper's own Monte Carlo is NOT re-run. What
runs is a model with the SHAPE the order describes -- weakest-link
aggregation over axes, a beta-factor common cause between parties -- and
one term the order proposes adding: whether the criterion the audit is
run against COVERS a fault class at all. Every number the model returns
is a property of that construction and is marked so. The arithmetic that
survives the construction is stated as arithmetic (CEX_002, CEX_004).

Axes 1-3 (the paper's, carried): PRINCIPAL / SUBSTRATE / EVIDENCE.
Axis 4 (the order's, PROPOSED): CRITERION, graded C0..C3.

Python 3.9, ASCII only, stdlib only. Refuses --selftest; the checks live
in test_criterion.py.
"""

from __future__ import annotations

import random
import sys

AXES3 = ("PRINCIPAL", "SUBSTRATE", "EVIDENCE")
AXIS4 = "CRITERION"
GRADES4 = ("C0", "C1", "C2", "C3")          # the order's grading, PROPOSED
STATUS = ("OBSERVED", "DERIVED", "PROPOSED", "CONSTRUCTED", "CARRIED")

# [CHOICE 1] axes 1-3 are graded on the same four-rung ordinal as axis 4
# (0..3). The paper's own grading of its three axes was not read; a
# grade here is a declared rung, never derived from the paper.
RUNGS = (0, 1, 2, 3)

CHOICES = {
    1: "axes 1-3 graded on a four-rung ordinal 0..3 matching C0..C3; the "
       "paper's own grading is not read",
    2: "weakest-link aggregation is min over axes, normalised to [0,1] by "
       "the top rung; an empty axis set returns None",
    3: "criterion coverage per grade is a declared set of fault classes "
       "(C0 the audited party's subset, C1 the auditor's, C2 a third "
       "party's applied with a discretion probability, C3 all); none is "
       "a fact about any audit regime",
    4: "C2's discretion probability is 0.7, stipulated; the crossover at "
       "which C2 overtakes C1 is computed and printed beside it",
    5: "the Monte Carlo uses 20000 draws per cell, seed 20260918",
    6: "the five regimes the order names for R3 are carried UNCODED; a "
       "grade on a real regime is a reading and none is supplied here",
}


class Refused(ValueError):
    """Raised at intake. A refused record never reaches a readout."""


def absent(v):
    return v is None or v == "" or v == "UNDECLARED"


# --------------------------------------------------------------- aggregation

def weakest_link(grades):
    """min(grades) / top rung. None on an empty set; a grade outside the
    rungs is refused, not clipped."""
    if not grades:
        return None
    for g in grades:
        if g not in RUNGS:
            raise Refused("weakest_link: grade %r is not a rung" % (g,))
    return min(grades) / float(max(RUNGS))


def three_vs_four(g1, g2, g3, c4):
    """The order's separating test: a system at maximum on axes 1-3 and C0
    on axis 4 aggregates to 1.0 over three and 0.0 over four."""
    if c4 not in GRADES4:
        raise Refused("three_vs_four: %r is not a C-grade" % (c4,))
    g4 = GRADES4.index(c4)
    return {"over_three": weakest_link([g1, g2, g3]),
            "over_four": weakest_link([g1, g2, g3, g4]),
            "axis4": c4}


# ------------------------------------------------------------ the fault model

# Eight CONSTRUCTED fault classes. p_det: per-party detection probability
# given the class is in the criterion. Names are shapes, not any audit.
FAULT_CLASSES = [
    {"id": "F1", "p_det": 0.30},
    {"id": "F2", "p_det": 0.10},
    {"id": "F3", "p_det": 0.05},
    {"id": "F4", "p_det": 0.40},
    {"id": "F5", "p_det": 0.02},
    {"id": "F6", "p_det": 0.15},
    {"id": "F7", "p_det": 0.08},
    {"id": "F8", "p_det": 0.25},
]

# [CHOICE 3] coverage by criterion grade
COVERAGE = {
    "C0": {"F1", "F4", "F6", "F8"},                  # authored by the audited
    "C1": {"F1", "F2", "F4", "F6", "F7", "F8"},      # authored by the auditor
    "C2": {"F1", "F2", "F3", "F4", "F6", "F7", "F8"},  # third party, discretionary
    "C3": {f["id"] for f in FAULT_CLASSES},          # re-runnable procedure
}
DISCRETION = {"C0": 1.0, "C1": 1.0, "C2": 0.7, "C3": 1.0}   # [CHOICE 4]

N_DRAWS = 20000                                              # [CHOICE 5]
SEED = 20260918


def surfaced_rate(fault, n_parties, beta, grade, draws=N_DRAWS, seed=SEED):
    """Share of draws in which at least one party surfaces the fault.

    Beta-factor common cause as usually stated: with probability beta the
    parties share one draw (all detect or none); otherwise each draws
    independently. The criterion enters as a gate in front of every
    party: a class outside the criterion is surfaced by nobody, at any
    beta, with any number of parties. That gate is the order's axis 4 and
    is NOT in the beta-factor form; it is the term being added.
    """
    if grade not in GRADES4:
        raise Refused("surfaced_rate: %r is not a C-grade" % (grade,))
    if n_parties < 1 or not (0.0 <= beta <= 1.0):
        raise Refused("surfaced_rate: n_parties >= 1 and 0 <= beta <= 1")
    rng = random.Random(seed)
    covered = fault["id"] in COVERAGE[grade]
    p, q = fault["p_det"], DISCRETION[grade]
    hits = 0
    for _ in range(draws):
        if not covered:
            continue                                  # the gate
        if rng.random() >= q:
            continue                                  # discretion not applied
        if rng.random() < beta:
            if rng.random() < p:
                hits += 1
        else:
            if any(rng.random() < p for _ in range(n_parties)):
                hits += 1
    return hits / float(draws)


def expected_rate(p, n_parties, beta, q):
    """The beta-factor form in closed form, one class, criterion applied
    with probability q:  q * (beta * p + (1 - beta) * (1 - (1-p)^n)).
    The Monte Carlo above converges to this; the closed form is what is
    registered in tools/known_answer.py. None on an out-of-range input."""
    if n_parties < 1 or not (0.0 <= beta <= 1.0) or not (0.0 <= q <= 1.0):
        return None
    if not (0.0 <= p <= 1.0):
        return None
    return q * (beta * p + (1.0 - beta) * (1.0 - (1.0 - p) ** n_parties))


def grade_mean(grade, n_parties=2, beta=0.3, q=None):
    """Expected mean surfaced rate over the eight classes at a grade."""
    q = DISCRETION[grade] if q is None else q
    tot = 0.0
    for f in FAULT_CLASSES:
        if f["id"] in COVERAGE[grade]:
            tot += expected_rate(f["p_det"], n_parties, beta, q)
    return tot / len(FAULT_CLASSES)


def discretion_crossover(n_parties=2, beta=0.3):
    """The C-grades order AUTHORSHIP, not surfaced rate. C2 covers more
    classes than C1 and applies them at discretion q; below q* it surfaces
    fewer faults than C1 does. q* = mean(C1) / mean(C2 at q=1)."""
    c1 = grade_mean("C1", n_parties, beta)
    c2_full = grade_mean("C2", n_parties, beta, q=1.0)
    if c2_full == 0.0:
        return None
    return c1 / c2_full


def r2_rerun(n_parties=2, beta=0.3, draws=N_DRAWS):
    """R2 on the constructed model: surfaced rate under three axes (the
    ruler not modelled, coverage implicitly total) against four axes at
    each C-grade. Delta per grade and the never-surfaced classes."""
    base = {f["id"]: surfaced_rate(f, n_parties, beta, "C3", draws)
            for f in FAULT_CLASSES}
    out = {"three_axes": base,
           "mean_three": sum(base.values()) / len(base), "by_grade": {}}
    for g in GRADES4:
        rates = {f["id"]: surfaced_rate(f, n_parties, beta, g, draws)
                 for f in FAULT_CLASSES}
        never = sorted(k for k, v in rates.items() if v == 0.0)
        mean = sum(rates.values()) / len(rates)
        out["by_grade"][g] = {"rates": rates, "mean": mean,
                              "delta": mean - out["mean_three"],
                              "never_surfaced": never,
                              "never_surfaced_share": len(never) / len(rates)}
    return out


def r4_beta_test(n_parties=2, draws=4000):
    """R4: does the common-cause model detect a party-held criterion?

    For every fault class, two sensitivities:
      beta_sens       surfaced(beta=0) - surfaced(beta=1) at C3
      criterion_sens  surfaced(C3) - surfaced(C0) at beta=0.3
    Axis 4 collapses into axes 1-3 iff every class the criterion excludes
    can be surfaced by SOME setting of beta or party count. It is
    independent iff an excluded class is surfaced at 0.0 at every beta
    and every party count tried.
    """
    rows = []
    for f in FAULT_CLASSES:
        b0 = surfaced_rate(f, n_parties, 0.0, "C3", draws)
        b1 = surfaced_rate(f, n_parties, 1.0, "C3", draws)
        c3 = surfaced_rate(f, n_parties, 0.3, "C3", draws)
        c0 = surfaced_rate(f, n_parties, 0.3, "C0", draws)
        excluded_c0 = f["id"] not in COVERAGE["C0"]
        sweep = [surfaced_rate(f, n, b, "C0", 1000)
                 for n in (1, 2, 4, 8) for b in (0.0, 0.5, 1.0)]
        rows.append({"id": f["id"], "beta_sens": b0 - b1,
                     "criterion_sens": c3 - c0, "excluded_at_C0": excluded_c0,
                     "max_over_sweep_at_C0": max(sweep)})
    excluded = [r for r in rows if r["excluded_at_C0"]]
    reachable = [r["id"] for r in excluded if r["max_over_sweep_at_C0"] > 0.0]
    verdict = ("COLLAPSES_INTO_1_3" if excluded and not [
        r for r in excluded if r["max_over_sweep_at_C0"] == 0.0]
        else "INDEPENDENT_ON_THIS_MODEL")
    return {"rows": rows, "n_excluded_at_C0": len(excluded),
            "reachable_by_beta_or_parties": reachable, "verdict": verdict,
            "scope": "a property of the constructed model; the paper's own "
                     "model is not read"}


# -------------------------------------------------------------- R3 regimes

REGIMES = [   # carried from the order; [CHOICE 6] no grade supplied
    {"name": "financial audit", "axis4": "UNCODED", "basis": None},
    {"name": "clinical trial endpoints", "axis4": "UNCODED", "basis": None},
    {"name": "AI evals", "axis4": "UNCODED", "basis": None},
    {"name": "internal safety review", "axis4": "UNCODED", "basis": None},
    {"name": "professional certification", "axis4": "UNCODED", "basis": None},
]


def code_regime(name, axis4, basis, axes3=None):
    """A grade on a real regime is a reading; it enters only with a basis."""
    if axis4 not in GRADES4:
        raise Refused("code_regime: %r is not a C-grade" % (axis4,))
    if absent(basis):
        raise Refused("code_regime: a grade with no basis is a preference")
    return {"name": name, "axis4": axis4, "basis": basis,
            "axes3": axes3 if axes3 is not None else "UNCODED"}


def r3_prediction(regimes):
    """The order's PROPOSED prediction: most regimes score C0/C1. Returns
    the share, or NOT_EVALUABLE when no regime carries a grade."""
    coded = [r for r in regimes if r["axis4"] in GRADES4]
    if not coded:
        return {"n_coded": 0, "share_c0_c1": None,
                "verdict": "NOT_EVALUABLE (no regime coded)"}
    low = [r for r in coded if r["axis4"] in ("C0", "C1")]
    share = len(low) / len(coded)
    return {"n_coded": len(coded), "share_c0_c1": share,
            "verdict": "prediction holds" if share > 0.5
            else "prediction does not hold, which is the finding"}


# ------------------------------------------------------------- R1 and links

R1 = {"host": "arxiv.org", "probe": "CONNECT tunnel failed, response 403",
      "when": "2026-09-19T01:51Z", "control": "github.com connects",
      "status": "NOT_RUN", "absence_claim": "VERIFIED_AGAINST_ABSTRACT_ONLY"}

ARRIVALS = [
    {"n": 1, "name": "physics as trust floor", "path": "PREAMBLE.md",
     "marker": "the conservation laws do not permit"},
    {"n": 2, "name": "the adjudication finding (condition B)",
     "path": "frame-instruments/workorders/B1-B3_frame_instruments.md",
     "marker": "no statement present"},
    {"n": 3, "name": "C4 in the audit-protocol work order",
     "path": None, "marker": "external to the protocol"},
]


def resolve_arrivals(root):
    import os
    out = []
    for a in ARRIVALS:
        if a["path"] is None:
            out.append(dict(a, state="NOT_IN_TREE"))
            continue
        p = os.path.join(root, a["path"])
        if not os.path.exists(p):
            out.append(dict(a, state="PATH_ABSENT"))
            continue
        text = open(p, encoding="utf-8").read()
        out.append(dict(a, state="RESOLVED" if a["marker"] in text
                        else "MARKER_ABSENT"))
    return out


# ------------------------------------------------------------------ render

def refuse_selftest(name):
    sys.stderr.write("%s carries no selftest; run python3 test_criterion.py\n"
                     % name)
    return 2


def render(root=None):
    import os
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = ["WO-6  CRITERION EXTERNALITY   (model CONSTRUCTED, PROPOSED)",
           "-" * 72,
           "R1  %s: %s at %s; %s -> %s; absence claim %s"
           % (R1["host"], R1["probe"], R1["when"], R1["control"],
              R1["status"], R1["absence_claim"]), ""]
    t = three_vs_four(3, 3, 3, "C0")
    out.append("separating test  axes 1-3 at top rung, axis 4 at C0: "
               "over three %.2f, over four %.2f   [CHOICE 1,2]"
               % (t["over_three"], t["over_four"]))
    out.append("")
    r2 = r2_rerun()
    out.append("R2  surfaced-fault rate, 2 parties, beta 0.3   [CHOICE 3-5]")
    out.append("    three axes (ruler unmodelled)  mean %.4f" % r2["mean_three"])
    for g in GRADES4:
        b = r2["by_grade"][g]
        out.append("    four axes at %s  mean %.4f  delta %+.4f  "
                   "never-surfaced %d of 8 (%s)"
                   % (g, b["mean"], b["delta"], len(b["never_surfaced"]),
                      ",".join(b["never_surfaced"]) or "-"))
    qs = discretion_crossover()
    out.append("    C-grades order authorship, not surfaced rate: C2 falls "
               "below C1 whenever discretion q < %.3f (q is %.1f here)"
               % (qs, DISCRETION["C2"]))
    out.append("")
    r4 = r4_beta_test()
    out.append("R4  beta-factor test  excluded at C0: %d  reachable by any "
               "beta or party count: %s  -> %s"
               % (r4["n_excluded_at_C0"],
                  ",".join(r4["reachable_by_beta_or_parties"]) or "none",
                  r4["verdict"]))
    for r in r4["rows"]:
        out.append("    %s  beta_sens %+.3f  criterion_sens %+.3f  %s"
                   % (r["id"], r["beta_sens"], r["criterion_sens"],
                      "excluded at C0" if r["excluded_at_C0"] else "covered"))
    out.append("    scope: %s" % r4["scope"])
    out.append("")
    p = r3_prediction(REGIMES)
    out.append("R3  regimes carried %d, coded %d -> %s   [CHOICE 6]"
               % (len(REGIMES), p["n_coded"], p["verdict"]))
    out.append("")
    for a in resolve_arrivals(root):
        out.append("arrival %d  %-40s %s" % (a["n"], a["name"], a["state"]))
    out.append("")
    out.append("no claim that adding the axis raises assurance; every delta "
               "above is <= 0")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("criterion_externality.py")
    if "--choices" in argv:
        for k in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (k, CHOICES[k]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
