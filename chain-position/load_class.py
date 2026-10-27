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
