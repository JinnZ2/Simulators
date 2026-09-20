#!/usr/bin/env python3
"""load_class.py -- the order's load-class test as arithmetic.

The reachable controller is a CONJUNCTION of assumed stabilities. The
order lists seven and attaches illustrative percentages to four. This
module computes what that compounding is and is not.

Under independence the chance that at least one of the assessed
factors fails is 1 - prod(1 - p). That is one point in a BAND: with the
factors perfectly positively correlated the union is max(p), and with
them mutually exclusive it is min(1, sum(p)). All three are printed and
none is picked, because the correlation among these factors is not a
number the order supplies. (The direction of that dependence is on
record in this tree: correlation lowers a conjunction's joint failure
and can only raise the union up to the sum.)

The RULE the order marks OBSERVED -- where a factor is unassessed,
engineer on the assumption it is NOT stable -- is implemented as a
refusal to propagate: an unassessed factor enters no arithmetic. It is
listed, and the verdict turns on whether each unassessed factor
declares a STRUCTURAL handling. The order's refinement (bound rather
than invert: worst credible condition plus margin) needs a declared
worst-credible value per factor; where none is declared the bound is
UNBOUNDED, never a default.

Applied to the order's own list: the illustrative compounding is
computed over 4 of 7 factors, so the number it produces is a FLOOR on
the union and the order's own RULE says the other three are not stable.
"""
import sys

# The order's seven, verbatim names; p is illustrative where the order gives one, None otherwise.
FACTORS = (
    {"name": "personnel availability under all conditions", "p": None},
    {"name": "environmental stability", "p": None},
    {"name": "governance continuity", "p": None},
    {"name": "economic continuity", "p": 0.01},
    {"name": "corporate continuity in the same operating form", "p": 0.02},
    {"name": "absence of an internal actor modifying internal access", "p": 0.03},
    {"name": "regional connectivity", "p": 0.04},
)
HANDLING = ("STRUCTURAL", "NONE", "UNDECLARED")


def union_band(ps):
    """Union of failure events over assessed probabilities. None on empty."""
    ps = [p for p in ps if p is not None]
    if not ps:
        return None
    if any(not (0.0 <= p <= 1.0) for p in ps):
        raise ValueError("probability outside [0,1]")
    indep = 1.0
    for p in ps:
        indep *= (1.0 - p)
    return {"n": len(ps), "independent": round(1.0 - indep, 6), "perfect_positive": max(ps),
            "mutually_exclusive": min(1.0, sum(ps)), "band": [max(ps), min(1.0, sum(ps))]}


def apply_rule(factor):
    """The order's RULE and refinement on one factor."""
    p = factor.get("p")
    if p is not None:
        return {"name": factor["name"], "assessed": True, "p": p, "assumed_stable": None, "bound": p}
    wc = factor.get("worst_credible")
    margin = factor.get("margin")
    bound = "UNBOUNDED" if wc is None or margin is None else round(wc + margin, 6)
    return {"name": factor["name"], "assessed": False, "p": None, "assumed_stable": False,
            "handling": factor.get("handling", "UNDECLARED"), "bound": bound}


def assess(factors):
    rows = [apply_rule(f) for f in factors]
    assessed = [r for r in rows if r["assessed"]]
    un = [r for r in rows if not r["assessed"]]
    band = union_band([r["p"] for r in assessed])
    unhandled = [r["name"] for r in un if r.get("handling") != "STRUCTURAL"]
    if not rows:
        state = "EMPTY"
    elif unhandled:
        state = "NOT_FLIGHT_RATED"
    else:
        state = "ASSESSED_OR_HANDLED"
    return {"state": state, "rows": rows, "n_assessed": len(assessed), "n_unassessed": len(un),
            "assessed_share": (len(assessed) / len(rows)) if rows else None, "union": band,
            "union_is_floor": bool(un), "unhandled": unhandled}


def factor_of_safety(design_load, anticipated_load):
    """Structural practice designs to a multiple of estimated load. None
    when the anticipated load is not positive."""
    if design_load is None or anticipated_load is None or anticipated_load <= 0:
        return None
    return round(design_load / anticipated_load, 6)


def render(factors=None):
    a = assess(FACTORS if factors is None else factors)
    lines = ["load_class -- the order's compounding as arithmetic",
             "  state %s  assessed %d of %d (share %s)  union_is_floor %s" % (
                 a["state"], a["n_assessed"], a["n_assessed"] + a["n_unassessed"],
                 "%.3f" % a["assessed_share"] if a["assessed_share"] is not None else None, a["union_is_floor"])]
    for r in a["rows"]:
        if r["assessed"]:
            lines.append("    assessed    p=%.2f  %s" % (r["p"], r["name"]))
        else:
            lines.append("    unassessed  assumed_stable=%s handling=%s bound=%s  %s" % (r["assumed_stable"], r["handling"], r["bound"], r["name"]))
    u = a["union"]
    if u:
        lines.append("  union of the %d assessed failures: independent %.4f  perfect-positive %.2f  mutually-exclusive %.2f  band %s" % (
            u["n"], u["independent"], u["perfect_positive"], u["mutually_exclusive"], u["band"]))
    lines.append("  factor of safety, designed to the anticipated threat exactly: %s" % factor_of_safety(1.0, 1.0))
    lines.append("  reading: the number is a floor over the assessed subset; the unassessed factors enter no")
    lines.append("           arithmetic and the verdict turns on whether each declares a structural handling")
    return "\n".join(lines)
# SPDX-License-Identifier: CC0-1.0
"""
load_class.py -- WO-1 load-bearing criterion, made numbers where it can be.

The order transposes the agentic chain onto a crewed mission engineered to the
same standard and draws three things this module makes decidable:

(1) The reachable controller is not a system property; it is a CONJUNCTION of
    assumed stabilities. stability_product composes them. The order's own
    illustrative compounding (1% / 2% / 3% / 4% discontinuities) gives about
    0.9035 -- a crewed mission does not fly on that. The order's RULE: where a
    factor is unassessed, engineer as though it is NOT stable; the mechanism is
    that an unquantifiable probability cannot be propagated through the
    calculation, so it is removed and handled structurally. Built in as a
    refusal: a None factor makes the product UNPROPAGATABLE, not a number.
    stability_product is registered in tools/known_answer.py.

(2) The engineering-gap register: factor of safety, inspectability under load,
    ductile failure. Each carries the structural-practice baseline and the
    chain's gap against it, from the order. The chain fails silently because
    every container stayed compliant to the end -- the opposite of a ductile
    mode that announces itself.

(3) redundancy_adjudicability settles the MECHANISM of the order's own
    counter-argument. Dissimilar redundancy detects a fault only when the
    disagreement can be adjudicated, and disagreement is adjudicable only
    against a verifiable spec. On a fixed-spec task, disagreement is
    FAULT_DETECTED; on an open task, disagreement is NOISE. The discriminator
    is spec-verifiability, not model diversity. Whether real model families
    disagree adjudicably is the empirical question and is NOT_RUN.

Nothing here is a claim about any deployed system. The stabilities are the
order's illustrative numbers; the tasks are CONSTRUCTED.

Stdlib only. Parses under 3.9. ASCII only. CC0.

    python3 load_class.py            # render the compounding and the register
    python3 load_class.py --choices  # the [CHOICE n] markers
    python3 test_chain.py            # the checks; prints their count
"""

from __future__ import annotations

import os
import sys

# The order's seven named assumed stabilities. The illustrative compounding
# uses four of them; the other three are named and carried unquantified.
ASSUMED_STABILITIES = [
    "personnel availability under all conditions",
    "environmental stability",
    "governance continuity",
    "economic continuity",
    "corporate continuity in the same operating form",
    "absence of an internal actor modifying internal access",
    "regional connectivity",
]

# The order's illustrative discontinuity probabilities (failure probs), in the
# order economic / corporate / internal-access / connectivity.
ILLUSTRATIVE = [0.01, 0.02, 0.03, 0.04]

# [CHOICE 1] a factor outside [0, 1] reads as a malformed record (None), kept
#   apart from an unassessed factor (also None) by the returned state.
CHOICES = {
    1: "an out-of-range factor and an unassessed (None) factor both return "
       "None but carry different states: MALFORMED vs UNPROPAGATABLE",
}


def stability_product(failure_probs):
    """P(all assumed stabilities hold) = product of (1 - p). None if any factor
    is unassessed (None) -- the order's RULE, an unquantifiable probability
    cannot be propagated -- or out of [0, 1]. Registered in
    tools/known_answer.py."""
    prod = 1.0
    for p in failure_probs:
        if p is None:
            return None
        if not (0.0 <= p <= 1.0):
            return None
        prod *= (1.0 - p)
    return prod


def reachable_controller(failure_probs):
    """stability_product wrapped in the order's reading. UNPROPAGATABLE names
    the unassessed-factor case (handle structurally, do not fly on it);
    MALFORMED names an out-of-range factor."""
    if any(p is None for p in failure_probs):
        return {"value": None, "state": "UNPROPAGATABLE",
                "why": "an unassessed factor cannot be propagated through the "
                       "calculation; the order's RULE removes it and handles "
                       "it structurally -- engineer as though it is not stable"}
    if any(not (0.0 <= p <= 1.0) for p in failure_probs):
        return {"value": None, "state": "MALFORMED",
                "why": "a factor outside [0, 1] is not a probability"}
    v = stability_product(failure_probs)
    return {"value": v, "state": "OK",
            "why": "P(all named stabilities hold) = product of (1 - p)"}


# The three engineering gaps, carried from the order. baseline is standard
# structural practice; gap is what the chain lacks against it.
ENGINEERING_GAPS = [
    {"id": "factor_of_safety",
     "baseline": "design to a multiple of estimated load",
     "gap": "designed to the anticipated threat exactly, no multiple"},
    {"id": "inspectability_under_load",
     "baseline": "the structure can be inspected while bearing load",
     "gap": "no inspectability under load"},
    {"id": "ductile_failure_mode",
     "baseline": "the structure deforms visibly before letting go, so the "
                 "failure announces itself",
     "gap": "no defined ductile mode; the chain lets go silently because "
            "every container stayed compliant to the end"},
]

# The order's two counter-arguments, carried UNRESOLVED.
COUNTER_ARGUMENTS = [
    {"id": "diversity_may_be_noise",
     "text": "two different models on one task produce disagreement that "
             "cannot be adjudicated; diversity may yield noise rather than "
             "fault detection",
     "status": "UNRESOLVED"},
    {"id": "ductile_mode_is_a_signal",
     "text": "a visible deformation mode is also a signal an adaptive "
             "adversary reads; ductile failure assumes monotonic load",
     "status": "UNRESOLVED"},
]


def redundancy_adjudicability(spec_verifiable, outputs):
    """Dissimilar redundancy detects a fault only when the disagreement can be
    adjudicated, and that needs a verifiable spec. `outputs` is a list of what
    the independent implementations returned. Agreement is no signal either
    way. Disagreement against a verifiable spec is FAULT_DETECTED; disagreement
    with no spec is NOISE. The discriminator is spec_verifiable."""
    distinct = len(set(outputs))
    if distinct <= 1:
        return {"disagree": False, "verdict": "NO_SIGNAL_agreement",
                "why": "agreement of correlated copies is no evidence of "
                       "correctness"}
    if spec_verifiable:
        return {"disagree": True, "verdict": "FAULT_DETECTED",
                "why": "disagreement can be checked against the verifiable "
                       "spec, so at least one copy is off-spec"}
    return {"disagree": True, "verdict": "NOISE_unadjudicable",
            "why": "no verifiable spec, so the disagreement has no adjudicator "
                   "-- diversity yielded noise, not detection"}


def render():
    out = []
    out.append("WO-1 LOAD-BEARING CRITERION -- the compounding, made a number")
    out.append("Illustrative stabilities are the order's; tasks are "
               "CONSTRUCTED. Not a deployed system.")
    out.append("")
    out.append("[CHOICE 1] %s" % CHOICES[1])
    out.append("")

    out.append("Reachable controller = conjunction of assumed stabilities "
               "(%d named):" % len(ASSUMED_STABILITIES))
    for s in ASSUMED_STABILITIES:
        out.append("  - %s" % s)
    rc = reachable_controller(ILLUSTRATIVE)
    out.append("  illustrative compounding %s -> P(all hold) = %.6f"
               % (ILLUSTRATIVE, rc["value"]))
    out.append("  so about %.2f percent of the time the reachable controller "
               "is not there, from four factors alone." % (100 * (1 - rc["value"])))
    out.append("")

    out.append("The order's RULE, built in as a refusal:")
    un = reachable_controller([0.01, None, 0.03])
    out.append("  an unassessed factor -> %s (%s)" % (un["value"], un["state"]))
    mal = reachable_controller([1.5])
    out.append("  a factor out of range -> %s (%s)"
               % (mal["value"], mal["state"]))
    out.append("")

    out.append("Engineering gaps against load-bearing practice:")
    for g in ENGINEERING_GAPS:
        out.append("  %-26s gap: %s" % (g["id"], g["gap"]))
    out.append("")

    out.append("Dissimilar redundancy -- the discriminator is spec, not "
               "diversity:")
    fx = redundancy_adjudicability(True, ["A", "B"])
    op = redundancy_adjudicability(False, ["A", "B"])
    ag = redundancy_adjudicability(False, ["A", "A"])
    out.append("  disagree, fixed spec:  %s" % fx["verdict"])
    out.append("  disagree, open task:   %s" % op["verdict"])
    out.append("  agree (correlated):    %s" % ag["verdict"])
    out.append("  the empirical question -- do real model families disagree "
               "adjudicably -- is NOT_RUN.")
    out.append("")
    out.append("Counter-arguments on record (both UNRESOLVED):")
    for c in COUNTER_ARGUMENTS:
        out.append("  [%s] %s" % (c["status"], c["id"]))
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        print("load_class.py refuses --selftest; run: python3 selftest.py")
        return 2
        sys.stderr.write(
            "load_class.py has no --selftest. The checks are in "
            "test_chain.py:\n    python3 %s\n"
            % os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "test_chain.py"))
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
