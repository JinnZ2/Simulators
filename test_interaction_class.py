"""
test_interaction_class.py -- checks run against the canonical module
threshold-states/interaction.py, reached through the root shim
interaction_class.py. CC0.

One case per row, the boundary cases at M +/- tol and S +/- tol, the
step-0 edge at S - M = 2*tol exactly, and a sweep showing bands 1-5 are
disjoint and exhaustive once step 0 has not fired.

All values are exact (Fraction), so a boundary case tests the boundary
and not float rounding. Stdlib only.

    python3 test_interaction_class.py
"""

import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import interaction_class as ic  # noqa: E402

CHECKS = []


def check(name, cond):
    CHECKS.append((name, bool(cond)))


def label(joint, separate, tol):
    return ic.classify(joint, separate, tol)["relation"]


# Reference case: separate = [2, 3] -> S = 5, M = 3; tol = 1/2.
# S - M = 2 > 2*tol = 1, so step 0 does not fire.
SEP = [F(2), F(3)]
S, M = F(5), F(3)
TOL = F(1, 2)
EPS = F(1, 1000)

# --- one case per row -------------------------------------------------
check("row 0  BELOW_RESOLUTION: separate [3, 0.25], tol 1/2",
      label(F(3), [F(3), F(1, 4)], TOL) == ic.BELOW_RESOLUTION)
check("row 1  REDUNDANT: joint = M",
      label(M, SEP, TOL) == ic.REDUNDANT)
check("row 2  ADDITIVE: joint = S",
      label(S, SEP, TOL) == ic.ADDITIVE)
check("row 3  RESONANT: joint = 7 > S + tol",
      label(F(7), SEP, TOL) == ic.RESONANT)
check("row 4  ENHANCED_SUBADDITIVE: joint = 4",
      label(F(4), SEP, TOL) == ic.ENHANCED_SUBADDITIVE)
check("row 5  ANTAGONISTIC: joint = 1 < M - tol",
      label(F(1), SEP, TOL) == ic.ANTAGONISTIC)

# --- the correction: joint = S is ADDITIVE, not ENHANCED_SUBADDITIVE ----
check("correction: joint = S is not ENHANCED_SUBADDITIVE",
      label(S, SEP, TOL) != ic.ENHANCED_SUBADDITIVE)

# --- boundaries at M +/- tol -------------------------------------------
check("M - tol exactly -> REDUNDANT (closed band)",
      label(M - TOL, SEP, TOL) == ic.REDUNDANT)
check("M - tol - eps -> ANTAGONISTIC",
      label(M - TOL - EPS, SEP, TOL) == ic.ANTAGONISTIC)
check("M + tol exactly -> REDUNDANT (closed band)",
      label(M + TOL, SEP, TOL) == ic.REDUNDANT)
check("M + tol + eps -> ENHANCED_SUBADDITIVE",
      label(M + TOL + EPS, SEP, TOL) == ic.ENHANCED_SUBADDITIVE)

# --- boundaries at S +/- tol -------------------------------------------
check("S - tol exactly -> ADDITIVE (closed band)",
      label(S - TOL, SEP, TOL) == ic.ADDITIVE)
check("S - tol - eps -> ENHANCED_SUBADDITIVE",
      label(S - TOL - EPS, SEP, TOL) == ic.ENHANCED_SUBADDITIVE)
check("S + tol exactly -> ADDITIVE (closed band)",
      label(S + TOL, SEP, TOL) == ic.ADDITIVE)
check("S + tol + eps -> RESONANT",
      label(S + TOL + EPS, SEP, TOL) == ic.RESONANT)

# --- step 0 edge: S - M = 2*tol exactly --------------------------------
# separate [3, 1] -> S = 4, M = 3, S - M = 1 = 2*tol.
EDGE = [F(3), F(1)]
for j in (F(0), F(3), F(4), F(10)):
    check("S - M = 2*tol exactly -> BELOW_RESOLUTION (joint %s)" % j,
          label(j, EDGE, TOL) == ic.BELOW_RESOLUTION)
check("S - M = 2*tol + eps -> resolves (joint = M -> REDUNDANT)",
      label(F(3), [F(3), F(1) + EPS], TOL) == ic.REDUNDANT)

# --- tol = 0 -----------------------------------------------------------
check("tol 0, joint = M -> REDUNDANT",
      label(M, SEP, F(0)) == ic.REDUNDANT)
check("tol 0, joint = S -> ADDITIVE",
      label(S, SEP, F(0)) == ic.ADDITIVE)

# --- absence and malformed input ---------------------------------------
check("tol undeclared -> UNRATED, never a default",
      label(S, SEP, None) == ic.UNRATED)
check("UNRATED is not a relation", ic.UNRATED not in ic.RELATIONS)
check("BELOW_RESOLUTION is not a relation",
      ic.BELOW_RESOLUTION not in ic.RELATIONS)
# Canonical refusals (consolidation changed the first three; see shim).
for bad_name, args in (("joint absent", (None, SEP, TOL)),
                       ("single response", (F(3), [F(3)], F(0))),
                       ("negative tol", (S, SEP, F(-1))),
                       ("empty separate", (S, [], TOL))):
    try:
        ic.classify(*args)
        check("%s raises InteractionError" % bad_name, False)
    except ic.InteractionError:
        check("%s raises InteractionError" % bad_name, True)
try:
    ic.classify(S, None, TOL)
    check("separate None refused", False)
except TypeError:
    check("separate None refused (TypeError, list(None))", True)

# --- step reported -----------------------------------------------------
check("detail names step 2 for ADDITIVE",
      ic.classify(S, SEP, TOL)["step"] == 2)

# --- disjoint and exhaustive, by sweep ---------------------------------
# For several (separate, tol) with step 0 not firing, every joint on a
# fine exact grid must satisfy exactly one of bands 1-5.
configs = [
    ([F(2), F(3)], F(1, 2)),
    ([F(1), F(1), F(1)], F(1, 4)),
    ([F(5), F(1, 2), F(2)], F(1, 3)),
    ([F(3), F(1) + EPS], F(1, 2)),
    ([F(2), F(3)], F(0)),
]
bad = 0
points = 0
for sep, tol in configs:
    s, m = sum(sep), max(sep)
    assert s - m > 2 * tol
    lo, hi = m - tol - 2, s + tol + 2
    steps = 800
    grid = [lo + (hi - lo) * F(k, steps) for k in range(steps + 1)]
    # include every boundary exactly, and eps either side of it
    for b in (m - tol, m + tol, s - tol, s + tol):
        grid += [b - EPS, b, b + EPS]
    for j in grid:
        points += 1
        hits = sum(1 for _, _, h in ic.rows(j, s, m, tol) if h)
        if hits != 1:
            bad += 1
check("bands 1-5 disjoint and exhaustive over %d points" % points, bad == 0)

# The sweep can fail: on a config where step 0 SHOULD fire (S - M < 2*tol)
# bands 1 and 2 overlap, and the same count finds a point with two hits.
s0, m0, t0 = F(4), F(3), F(1)
overlap = any(sum(1 for _, _, h in ic.rows(j, s0, m0, t0) if h) > 1
              for j in (m0, s0, (m0 + s0) / 2))
check("sweep detects overlap when step 0 is bypassed", overlap)

# --- one module: the shim re-exports canonical objects -----------------
import interaction as canon  # noqa: E402  (path set by the shim)
check("shim classify is the canonical object", ic.classify is canon.classify)
check("shim rows is the canonical object", ic.rows is canon.rows)
check("shim InteractionError is canonical",
      ic.InteractionError is canon.InteractionError)
check("canonical path recorded",
      ic.CANONICAL_PATH == "threshold-states/interaction.py"
      and os.path.isfile(os.path.join(os.path.dirname(
          os.path.abspath(__file__)), ic.CANONICAL_PATH)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "interaction_class.py")).read()
check("shim defines no comparison logic",
      "<=" not in src.split("def main")[0] and "abs(" not in src)

# --- library refuses --selftest ----------------------------------------
check("interaction_class.py refuses --selftest (exit 2)",
      ic.main(["--selftest"]) == 2)


def main():
    failed = [n for n, ok in CHECKS if not ok]
    for n, ok in CHECKS:
        print(("PASS " if ok else "FAIL ") + n)
    print("%d/%d" % (len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
