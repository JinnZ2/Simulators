#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
grade.py -- RUS-0.1 and RUS-0.2 grading, as functions.

RUS-0.1 is implemented from the text of
source/kimmy_v1/regulatory_uncertainty_standard_draft.md sections 5-8, so
that Annex A can be recomputed and every place the Annex disagrees with its
own standard becomes a row, not an impression.

    U   coded uncertainty low/moderate/high -> U1/U2/U3
        M1  evidence class none_required        -> U4
        M2  evidence classes all in {animal, in_vitro} and the material
            question is human health            -> at least U3
    C   P + I + D, each 1-3: 3-4 C1, 5 C2, 6-7 C3, 8-9 C4
    floor  matrix[U][C]; R1 -> D5; R5 -> C one class lower
    actual go_ahead D1, warn D2, hold D4, decline D5 (Annex A's own mapping;
           D3 is unused because no conditional-with-sunset exists)
    status R2: actual >= floor conforming (exact / exceeds), below
           non-conforming; R3: compelled by statute or court and actual !=
           floor -> STATUTE-EXCEPTION (undeclared); R5: CONFORM (R5) only
           if actual >= the R5 floor.

RUS-0.2 (this registry's PROPOSED revision, schema/../RUS-0.2.md) adds the
consequence of a wrongful RESTRICTION:

    C_restrict  Pr + Ir + Dr, each 1-3, same banding
                Pr  population that loses the benefit (<1e5 / 1e5-1e7 /
                    >1e7 or an essential service)
                Ir  harm from wrongful restriction (alternatives exist /
                    partial / none: progressive or fatal disease, or loss of
                    an essential service)
                Dr  reversibility of the restriction (product can return /
                    sponsor or supply exits / near-irreversible)
    floor F     as RUS-0.1, from U x C_permit
    ceiling K   variant-dependent (below)
    R1a         U1-U2 evidence of absence of benefit, or of harm with no
                benefit claimed by any party: F = K = D5
    R1b         U1-U2 evidence of benefit with the harm question resolved
                absent: F = D1
    status      F <= K: below F -> BELOW_FLOOR, above K -> ABOVE_CEILING,
                else WITHIN_BAND.  F > K (conflict): below K -> BELOW_FLOOR,
                above F -> ABOVE_CEILING, between -> CONFLICT_UNDECLARED
                (no record in the sample declares a tradeoff).  A
                non-conformity in the direction a statute or court compelled
                is reported as EXCEPTION_UNDECLARED_<DIRECTION>.

Variants (all computed, one normative):
    V0  RUS-0.1: floor only, ceiling D5             (one-sided instrument)
    V1  floor from the difference C_eff = C_permit - max(0, C_restrict -
        C_permit), ceiling D5                       (two-sided, floor only)
    V2  NORMATIVE: ceiling K = 6 - matrix[U][C_restrict] (mirror)
    V3  ceiling K = 6 - index(C_restrict), U-independent

[CHOICE G1] V2 is normative because it applies the same safety-factor
matrix to both errors; V1 is the REVIEW R4 fix read literally (floor set
from the difference) and is kept to show that any floor-only instrument
cannot produce a restrictive non-conformity. V3 tests whether the result
depends on letting U lower the ceiling.

Library; checks run in tools/validate.py --selftest. Stdlib only.
"""

import sys

MATRIX = {  # RUS-0.1 section 8, rows U1..U4, columns C1..C4
    "U1": ["D1", "D1", "D2", "D2"],
    "U2": ["D1", "D2", "D3", "D3"],
    "U3": ["D2", "D3", "D4", "D4"],
    "U4": ["D3", "D4", "D4", "D5"],
}
ACTUAL_OF = {"go_ahead": "D1", "warn": "D2", "hold": "D4", "decline": "D5"}
U_OF = {"low": "U1", "moderate": "U2", "high": "U3"}
M2_CLASSES = {"animal", "in_vitro"}
VARIANTS = ("V0", "V1", "V2", "V3")
NORMATIVE = "V2"
PERMISSIVE_NC = ("BELOW_FLOOR", "EXCEPTION_UNDECLARED_PERMISSIVE")
RESTRICTIVE_NC = ("ABOVE_CEILING", "EXCEPTION_UNDECLARED_RESTRICTIVE")


def d_index(d):
    return int(d[1])


def d_of(i):
    return "D%d" % max(1, min(5, i))


def c_index(c):
    return int(c[1])


def band(score):
    """RUS-0.1 section 6 banding of a 3-9 axis sum."""
    if not 3 <= score <= 9:
        raise ValueError("axis sum %r outside 3-9" % score)
    if score <= 4:
        return "C1"
    if score == 5:
        return "C2"
    if score <= 7:
        return "C3"
    return "C4"


def u_grade(uncertainty, evidence_classes, human_question=True):
    """RUS-0.1 section 5 with modifiers M1 and M2. Returns (U, rule)."""
    classes = set(evidence_classes)
    if "none_required" in classes:
        return "U4", "M1 none_required"
    u = U_OF[uncertainty]
    if human_question and classes and classes <= M2_CLASSES and u in ("U1", "U2"):
        return "U3", "M2 animal-only, extrapolation unresolved"
    return u, "coded uncertainty %s" % uncertainty


def floor01(U, C, r1=False, r5=False):
    """RUS-0.1 required direction. Returns (floor, rule)."""
    if r1:
        return "D5", "R1"
    if r5:
        c = "C%d" % max(1, c_index(C) - 1)
        return MATRIX[U][c_index(c) - 1], "R5 (C one lower)"
    return MATRIX[U][c_index(C) - 1], "matrix"


def status01(floor, actual, forced=False, r5=False):
    """RUS-0.1 status, by the standard's own rules (R2, R3, R5)."""
    a, f = d_index(actual), d_index(floor)
    if forced and a != f:
        return "STATUTE-EXCEPTION (undeclared)"
    if r5:
        return "CONFORM (R5 emergency)" if a >= f else \
            "NON-CONFORM: below safety factor"
    if a == f:
        return "CONFORM (exact)"
    if a > f:
        return "CONFORM (exceeds safety factor)"
    return "NON-CONFORM: below safety factor"


def ceiling(variant, U, C_restrict):
    if variant in ("V0", "V1"):
        return "D5"
    if variant == "V2":
        return d_of(6 - d_index(MATRIX[U][c_index(C_restrict) - 1]))
    if variant == "V3":
        return d_of(6 - c_index(C_restrict))
    raise ValueError("unknown variant %r" % variant)


def floor02(variant, U, C_permit, C_restrict, r5=False):
    cp = c_index(C_permit)
    if r5:
        cp = max(1, cp - 1)
    if variant == "V1":
        cp = max(1, cp - max(0, c_index(C_restrict) - c_index(C_permit)))
    return MATRIX[U][cp - 1]


def status02(F, K, actual, forced_dir=None, tradeoff_declared=False):
    """Band status. forced_dir is 'restrictive', 'permissive' or None."""
    f, k, a = d_index(F), d_index(K), d_index(actual)
    if f <= k:
        if a < f:
            s = "BELOW_FLOOR"
        elif a > k:
            s = "ABOVE_CEILING"
        else:
            s = "WITHIN_BAND"
    else:
        if a < k:
            s = "BELOW_FLOOR"
        elif a > f:
            s = "ABOVE_CEILING"
        else:
            s = "WITHIN_BAND" if tradeoff_declared else "CONFLICT_UNDECLARED"
    if s == "BELOW_FLOOR" and forced_dir == "permissive":
        return "EXCEPTION_UNDECLARED_PERMISSIVE"
    if s == "ABOVE_CEILING" and forced_dir == "restrictive":
        return "EXCEPTION_UNDECLARED_RESTRICTIVE"
    return s


def grade02(U, C_permit, C_restrict, actual, r1="none", r5=False,
            forced_dir=None, variant=NORMATIVE):
    """One case under one variant. Returns dict(floor, ceiling, status)."""
    if r1 == "R1a":
        F, K = "D5", "D5"
    else:
        F = floor02(variant, U, C_permit, C_restrict, r5)
        K = ceiling(variant, U, C_restrict)
        if r1 == "R1b":
            F = "D1"
    if variant == "V0":
        # RUS-0.1's one-sided instrument: same floor as V2, no ceiling.
        K = "D5"
    return {"floor": F, "ceiling": K,
            "status": status02(F, K, actual, forced_dir)}


def direction_counts(statuses):
    """Permissive vs restrictive non-conformity, with and without exceptions."""
    out = {"permissive": 0, "restrictive": 0, "permissive_ex": 0,
           "restrictive_ex": 0, "conflict": 0, "within": 0}
    for s in statuses:
        if s == "BELOW_FLOOR":
            out["permissive"] += 1
        elif s == "EXCEPTION_UNDECLARED_PERMISSIVE":
            out["permissive_ex"] += 1
        elif s == "ABOVE_CEILING":
            out["restrictive"] += 1
        elif s == "EXCEPTION_UNDECLARED_RESTRICTIVE":
            out["restrictive_ex"] += 1
        elif s == "CONFLICT_UNDECLARED":
            out["conflict"] += 1
        elif s == "WITHIN_BAND":
            out["within"] += 1
    return out


def one_directional(counts):
    """The Annex A finding, read three ways. Returns a dict of booleans."""
    return {
        "strict": counts["restrictive"] == 0 and counts["restrictive_ex"] == 0,
        "excluding_exceptions": counts["restrictive"] == 0,
        "skew_permissive": (counts["permissive"] + counts["permissive_ex"])
        > (counts["restrictive"] + counts["restrictive_ex"]),
    }


def main():
    sys.stderr.write("grade.py is a library; checks run in "
                     "tools/validate.py --selftest\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
