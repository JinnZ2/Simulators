#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
grade.py -- RUS-0.2 as published, its calibration sweep, and RUS-0.3.

RUS-0.2 is implemented from the text of
bundle/source/current/regulatory_uncertainty_standard_v02.md sections 5-8,
so that Annex A (annex_a_regrading_v2.csv) can be recomputed and every row
where the Annex and its own standard disagree is a row, not an impression.

    U       coded uncertainty low/moderate/high -> U1/U2/U3
            M1  evidence class none_required          -> U4
            M2  evidence classes all in {animal, in_vitro, eco}... see
                M2_CLASSES; human question            -> at least U3
    C       P + I + D, each 1-3: 3-4 C1, 5 C2, 6-7 C3, 8-9 C4   (section 6)
    G       C_permit score - C_restrict score                    (section 3)
    column  G <= -1 | G = 0 | G = 1-2 | G >= 3                   (section 8)
    floor   MATRIX[U][column]; R1 -> D5; R5 -> one column permissive
    actual  go_ahead D1, warn D2, hold D4, decline D5 (Annex A mapping)
    status  R2: below floor -> NON-CONFORM: below floor; above by 1 ->
            CONFORM (exceeds floor); above by >= 2 with C_restrict >
            C_permit -> NON-CONFORM: over-restrictive with denial harm;
            R3: compelled by statute or court and actual != floor ->
            STATUTE/JUDICIAL-EXCEPTION (undeclared); R5 -> CONFORM (R5
            emergency) when actual >= the R5 floor.

The published sweep (calibration_sweep_v3.csv) names seven variants M0-M6
by their gap thresholds and U3 rows. The thresholds are stated in the CSV
labels; the U3 rows for M4 and M6 are not stated anywhere in the bundle.
SWEEP below carries the labels as published and the U3 rows this module
reconstructed by search (tools/stats.py --sweep shows the search and
whether a reconstruction reproduces the published counts).

RUS-0.3 (this registry's PROPOSED revision, RUS-0.3.md) adds, each as a
switch so every combination is computed:
    M7      symmetric tolerance: below the floor by exactly one class is
            conforming by margin (REVIEW_v2 R7, REVIEW_v3 R13)
    S       substitution rule (REVIEW_v2 R9): a C_restrict lowered because
            "alternatives exist" keeps that credit only when the alternative
            is named AND graded with a C_permit grade below the case's own;
            otherwise C_restrict + 1 (capped at 9)
    R6a     self-sealing restriction held past two annual cycles without a
            new justification on record -> R6_SELF_SEALING (an overlay
            status beside the R2 status, never replacing it)
    R6b     a decision loosening a self-sealing restriction: uncertainty
            maintained by that restriction is not credited toward the floor
            (U one class lower, declared per case)
    BASIS   "action" grades every row on the agency's own move, "outcome"
            on legal status at the coding date; the published Annex mixes
            them (NCR-A05)

Library; refuses --selftest (checks run in tools/validate.py --selftest).
Stdlib only.
"""

import sys

MATRIX = {  # RUS-0.2 section 8: rows U1..U4, columns G<=-1, G=0, G=1-2, G>=3
    "U1": ["D1", "D1", "D2", "D2"],
    "U2": ["D1", "D2", "D3", "D3"],
    "U3": ["D2", "D3", "D4", "D4"],
    "U4": ["D3", "D4", "D4", "D5"],
}
ACTUAL_OF = {"go_ahead": "D1", "warn": "D2", "hold": "D4", "decline": "D5"}
U_OF = {"low": "U1", "moderate": "U2", "high": "U3"}
M2_CLASSES = {"animal", "in_vitro", "invitro"}

S_CONFORM_EXACT = "CONFORM (exact)"
S_CONFORM_EXCEEDS = "CONFORM (exceeds floor)"
S_CONFORM_MARGIN = "CONFORM (within symmetric margin)"
S_R5 = "CONFORM (R5 emergency)"
S_STATUTE = "STATUTE/JUDICIAL-EXCEPTION (undeclared)"
S_BELOW = "NON-CONFORM: below floor"
S_OVER = "NON-CONFORM: over-restrictive with denial harm"
STATUSES = (S_CONFORM_EXACT, S_CONFORM_EXCEEDS, S_CONFORM_MARGIN, S_R5,
            S_STATUTE, S_BELOW, S_OVER)
R6_SELF_SEALING = "R6_SELF_SEALING"

# gap -> column index 0..3, by variant label (the CSV labels, verbatim
# where they state thresholds)
COLUMN_RULES = {
    "published": lambda g: 0 if g <= -1 else 1 if g == 0 else 2 if g <= 2 else 3,
    "lenient":   lambda g: 0 if g <= -1 else 1 if g <= 1 else 2 if g <= 3 else 3,
    "strict":    lambda g: 0 if g <= -3 else 1 if g <= -1 else 2 if g <= 1 else 3,
    "uniform":   lambda g: 1,
}


def d_index(d):
    return int(d[1])


def d_of(i):
    return "D%d" % max(1, min(5, i))


def band(score):
    """RUS-0.2 section 6 banding of a 3-9 axis sum -> C1..C4."""
    if not 3 <= score <= 9:
        raise ValueError("axis sum %r outside 3-9" % (score,))
    if score <= 4:
        return "C1"
    if score == 5:
        return "C2"
    if score <= 7:
        return "C3"
    return "C4"


def u_grade(uncertainty, evidence_classes, human_question=True):
    """Section 5 with M1 and M2. Returns (U, rule)."""
    classes = set(evidence_classes)
    if "none_required" in classes:
        return "U4", "M1 none_required"
    u = U_OF[uncertainty]
    if human_question and classes and classes <= M2_CLASSES and u in ("U1", "U2"):
        return "U3", "M2 animal-only, extrapolation unresolved"
    return u, "coded uncertainty %s" % uncertainty


def floor(U, gap, r1=False, r5=False, columns="published", matrix=None):
    """Required direction class. Returns (floor, rule)."""
    m = matrix or MATRIX
    if r1:
        return "D5", "R1"
    col = COLUMN_RULES[columns](gap)
    if r5:
        col = max(0, col - 1)
        return m[U][col], "R5 (one column permissive)"
    return m[U][col], "matrix"


def status(fl, actual, cp, cr, forced=False, r5=False, symmetric=False):
    """R2/R3/R5 status of one decision against its floor."""
    a, f = d_index(actual), d_index(fl)
    if forced and a != f:
        return S_STATUTE
    if r5:
        return S_R5 if a >= f else S_BELOW
    if a == f:
        return S_CONFORM_EXACT
    if a > f:
        if a - f >= 2 and cr > cp:
            return S_OVER
        return S_CONFORM_EXCEEDS
    if symmetric and f - a == 1:
        return S_CONFORM_MARGIN
    return S_BELOW


def substitution_adjust(cr, alt_claimed, alt_named, alt_grade, cp_grade):
    """Rule S. Returns (cr_effective, rule)."""
    if not alt_claimed:
        return cr, "no alternatives credit claimed"
    if alt_named and alt_grade is not None and int(alt_grade[1]) < int(cp_grade[1]):
        return cr, "credit stands: %s graded %s below %s" % (alt_named, alt_grade, cp_grade)
    why = ("alternative not named" if not alt_named else
           "alternative %s not graded" % alt_named if alt_grade is None else
           "alternative %s graded %s, not below %s" % (alt_named, alt_grade, cp_grade))
    return min(9, cr + 1), "credit withdrawn (%s): C_restrict +1" % why


def r6_status(blocking, cycles_held, justification_on_record):
    """R6a overlay. Returns R6_SELF_SEALING, 'R6 not triggered',
    'R6 not applicable' or 'R6 not evaluable'."""
    if not blocking:
        return "R6 not applicable"
    if cycles_held is None:
        return "R6 not evaluable"
    if cycles_held > 2 and not justification_on_record:
        return R6_SELF_SEALING
    return "R6 not triggered"


def grade_case(case, variant):
    """case: dict with U, cp, cr, actual_action, actual_outcome, forced, r1,
    r5, alt_claimed, alt_named, alt_grade, cp_grade, r6b, r6_blocking,
    r6_cycles, r6_justified. variant: dict(columns, u3_row, symmetric,
    substitution, r6, basis, cr_source)."""
    U = case["U"]
    if variant.get("r6") and case.get("r6b"):
        U = "U%d" % max(1, int(U[1]) - 1)
    cr = case["cr"]
    rule_s = None
    if variant.get("substitution"):
        cr, rule_s = substitution_adjust(cr, case.get("alt_claimed"),
                                         case.get("alt_named"),
                                         case.get("alt_grade"),
                                         case["cp_grade"])
    gap = case["cp"] - cr
    m = dict(MATRIX)
    if variant.get("u3_row"):
        m["U3"] = list(variant["u3_row"])
    fl, frule = floor(U, gap, r1=case.get("r1"), r5=case.get("r5"),
                      columns=variant.get("columns", "published"), matrix=m)
    basis = variant.get("basis", "annex")
    if basis == "action":
        actual = case["actual_action"]
    elif basis == "outcome":
        actual = case["actual_outcome"]
    else:
        actual = case["actual_annex"]
    st = status(fl, actual, case["cp"], cr, forced=case.get("forced"),
                r5=case.get("r5"), symmetric=variant.get("symmetric"))
    out = {"U": U, "cr_eff": cr, "gap": gap, "floor": fl, "floor_rule": frule,
           "actual": actual, "deviation": d_index(actual) - d_index(fl),
           "status": st}
    if rule_s:
        out["substitution_rule"] = rule_s
    if variant.get("r6"):
        out["r6"] = r6_status(case.get("r6_blocking"), case.get("r6_cycles"),
                              case.get("r6_justified"))
    return out


def tally(statuses):
    keys = ("below", "conform", "exceeds", "over_restrictive", "statute")
    out = dict.fromkeys(keys, 0)
    for s in statuses:
        if s == S_BELOW:
            out["below"] += 1
        elif s in (S_CONFORM_EXACT, S_R5, S_CONFORM_MARGIN):
            out["conform"] += 1
        elif s == S_CONFORM_EXCEEDS:
            out["exceeds"] += 1
        elif s == S_OVER:
            out["over_restrictive"] += 1
        elif s == S_STATUTE:
            out["statute"] += 1
    return out


def one_directional(t):
    """'Non-conformity is one-directional', read on a tally. Returns one of
    HOLDS (below > 0, over = 0, and an over-restrictive row was possible),
    HOLDS_UNTESTABLE (over = 0 but no row could produce it), FAILS
    (non-conformity in both directions), NO_NONCONFORMITY."""
    if t["below"] == 0 and t["over_restrictive"] == 0:
        return "NO_NONCONFORMITY"
    if t["below"] > 0 and t["over_restrictive"] > 0:
        return "FAILS"
    if t.get("over_possible", 0) == 0:
        return "HOLDS_UNTESTABLE"
    return "HOLDS"


def over_possible(cases):
    """Rows on which R2's over-restrictive branch can fire at all: a
    restrictive actual (D4/D5) with C_restrict > C_permit."""
    return sum(1 for c in cases if c["cr_eff"] > c["cp"]
               and d_index(c["actual"]) >= 4)


def main():
    sys.stderr.write("grade.py is a library; checks run in "
                     "tools/validate.py --selftest\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
