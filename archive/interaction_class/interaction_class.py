"""
interaction_class.py -- classify a joint response against its separate
responses, by the precedence ordered 2026-10-07. CC0.

Companion to threshold-states-in-animal-escape.md, section 8.

    S   = sum of the separate responses
    M   = largest single separate response
    tol = declared; from sampling variance where available

    step 0   S - M <= 2*tol              BELOW_RESOLUTION
    step 1   |joint - M| <= tol          REDUNDANT
    step 2   |joint - S| <= tol          ADDITIVE        (I ~ 0)
    step 3   joint > S + tol             RESONANT
    step 4   M + tol < joint < S - tol   ENHANCED_SUBADDITIVE
    step 5   joint < M - tol             ANTAGONISTIC    (OPEN class)

Once step 0 has not fired, M + tol < S - tol, so bands 1-5 partition the
real line: disjoint and exhaustive. test_interaction_class.py checks both
properties by sweep, on exact rationals.

Not decided here:
- ANTAGONISTIC is a band. The class definition is OPEN, pending the
  author of Polyhedral-Intelligence ontology/relation_classes.json.
- Which reference (S or M) a published study used. A study reporting
  against M only cannot separate ENHANCED_SUBADDITIVE from RESONANT.

Absence is not a value:
- tol undeclared  -> UNRATED (never a default tol)
- joint absent    -> UNRATED
- negative tol, or no separate responses -> ValueError (malformed input)

Exact boundaries are exact only for exact input (int, Fraction). Float
input inherits float rounding at the boundaries.

Stdlib only. Library module: refuses --selftest (exit 2).
"""

import sys

UNRATED = "UNRATED"
BELOW_RESOLUTION = "BELOW_RESOLUTION"
REDUNDANT = "REDUNDANT"
ADDITIVE = "ADDITIVE"
RESONANT = "RESONANT"
ENHANCED_SUBADDITIVE = "ENHANCED_SUBADDITIVE"
ANTAGONISTIC = "ANTAGONISTIC"

LABELS = (BELOW_RESOLUTION, REDUNDANT, ADDITIVE, RESONANT,
          ENHANCED_SUBADDITIVE, ANTAGONISTIC)


def bands(joint, S, M, tol):
    """Predicates for steps 1-5, in order. Used by classify() and by the
    disjointness sweep in the tests."""
    return (
        (REDUNDANT, abs(joint - M) <= tol),
        (ADDITIVE, abs(joint - S) <= tol),
        (RESONANT, joint > S + tol),
        (ENHANCED_SUBADDITIVE, M + tol < joint < S - tol),
        (ANTAGONISTIC, joint < M - tol),
    )


def classify(joint, separate, tol):
    """Return (label, detail). detail carries S, M and the step that fired,
    or the reason for UNRATED."""
    if separate is None or len(separate) == 0:
        raise ValueError("no separate responses: S and M are undefined")
    if tol is not None and tol < 0:
        raise ValueError("tol is negative: %r" % (tol,))
    S = sum(separate)
    M = max(separate)
    if tol is None:
        return (UNRATED, {"reason": "tol undeclared", "S": S, "M": M})
    if joint is None:
        return (UNRATED, {"reason": "joint absent", "S": S, "M": M})
    if S - M <= 2 * tol:
        reason = "S - M <= 2*tol"
        if len(separate) < 2:
            reason += " (fewer than two separate responses)"
        return (BELOW_RESOLUTION, {"step": 0, "reason": reason,
                                   "S": S, "M": M})
    for step, (label, hit) in enumerate(bands(joint, S, M, tol), start=1):
        if hit:
            return (label, {"step": step, "S": S, "M": M})
    raise AssertionError("unreachable: bands 1-5 are exhaustive once "
                         "step 0 has not fired")


def main(argv):
    if "--selftest" in argv:
        print("this is a library module; run test_interaction_class.py",
              file=sys.stderr)
        return 2
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
