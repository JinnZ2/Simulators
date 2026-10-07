# SPDX-License-Identifier: CC0-1.0
"""interaction.py -- the two-reference interaction test, with its precedence.

Section 8 of threshold-states-in-animal-escape.md (repo root). A joint
(multimodal) response is read against two references: S, the sum of the
separate (unimodal) responses, and M, the largest single one. tol is a
declared tolerance in the response's own units.

PRECEDENCE (operator, 2026-10-07; resolves THIN T-7)

    0.  S - M <= 2*tol             BELOW_RESOLUTION
    1.  |joint - M| <= tol         REDUNDANT
    2.  |joint - S| <= tol         ADDITIVE              (I ~ 0, independent)
    3.  joint > S + tol            RESONANT
    4.  M + tol < joint < S - tol  ENHANCED_SUBADDITIVE
    5.  joint < M - tol            ANTAGONISTIC          (OPEN class)

    I = joint - S, the measurand of the RESONANT enum in
    JinnZ2/Polyhedral-Intelligence ontology/relation_classes.json @ 7387230.

Why step 0 exists. When S - M <= 2*tol the bands [M-tol, M+tol] and
[S-tol, S+tol] touch or overlap, so REDUNDANT and ADDITIVE cannot be told
apart: the weaker cues sum to less than the instrument resolves. Given
S - M > 2*tol, rows 1-5 are disjoint and exhaustive over the real line:

    (-inf, M-tol)  [M-tol, M+tol]  (M+tol, S-tol)  [S-tol, S+tol]  (S+tol, inf)
      ANTAG.         REDUNDANT       ENH_SUBADD      ADDITIVE        RESONANT

classify() does not trust that argument. It evaluates all five predicates
and raises if anything other than exactly one holds.

Correction recorded: joint = S is ADDITIVE, not ENHANCED_SUBADDITIVE. The
earlier table read "M < joint <= S" and put the sum itself in the
subadditive row.

STATES THAT ARE NOT RELATIONS
    UNRATED            tol undeclared (None). Not a zero tolerance.
    BELOW_RESOLUTION   step 0. A reading, not a relation between the cues.

WHAT IT DOES NOT DO
    It does not choose tol. It does not define the ANTAGONISTIC class: it
    gives that open class a measurable boundary (joint < M - tol). The
    definition stays with the enum's author. Boundaries are compared in the
    caller's number type. Pass Fraction or Decimal where exact boundaries
    matter, since a float M + tol can round across a band edge.

Stdlib only. Library module: refuses --selftest (exit 2); the checks are in
test_interaction.py beside it.
"""
from __future__ import annotations

import decimal
import math
import numbers
import sys

UNRATED = "UNRATED"
BELOW_RESOLUTION = "BELOW_RESOLUTION"
REDUNDANT = "REDUNDANT"
ADDITIVE = "ADDITIVE"
RESONANT = "RESONANT"
ENHANCED_SUBADDITIVE = "ENHANCED_SUBADDITIVE"
ANTAGONISTIC = "ANTAGONISTIC"

RELATIONS = (REDUNDANT, ADDITIVE, RESONANT, ENHANCED_SUBADDITIVE, ANTAGONISTIC)
OPEN_CLASSES = (ANTAGONISTIC,)


class InteractionError(ValueError):
    pass


def _finite(x, what):
    # A number, not something float() can parse: "1" is refused, not read.
    ok = (isinstance(x, (numbers.Real, decimal.Decimal))
          and not isinstance(x, bool))
    if ok:
        try:
            ok = math.isfinite(float(x))
        except (TypeError, ValueError, OverflowError):
            ok = False
    if not ok:
        raise InteractionError("%s must be a finite number, got %r" % (what, x))


def references(separate):
    """(S, M) from the separate responses. Two or more cues are required."""
    separate = list(separate)
    if len(separate) < 2:
        raise InteractionError("an interaction needs two or more separate "
                               "responses, got %d" % len(separate))
    for i, x in enumerate(separate):
        _finite(x, "separate[%d]" % i)
    return sum(separate), max(separate)


def classify(joint, separate, tol):
    """Return a dict: relation, step, S, M, I, tol.

    relation is one of RELATIONS, or UNRATED / BELOW_RESOLUTION.
    """
    S, M = references(separate)
    _finite(joint, "joint")
    out = {"S": S, "M": M, "I": joint - S, "tol": tol}
    if tol is None:
        out.update(relation=UNRATED, step=None)
        return out
    _finite(tol, "tol")
    if tol < 0:
        raise InteractionError("tol must be >= 0, got %r" % (tol,))
    if S - M <= 2 * tol:
        out.update(relation=BELOW_RESOLUTION, step=0)
        return out
    rows = [
        (1, REDUNDANT, abs(joint - M) <= tol),
        (2, ADDITIVE, abs(joint - S) <= tol),
        (3, RESONANT, joint > S + tol),
        (4, ENHANCED_SUBADDITIVE, M + tol < joint < S - tol),
        (5, ANTAGONISTIC, joint < M - tol),
    ]
    hit = [(n, rel) for n, rel, cond in rows if cond]
    if len(hit) != 1:
        raise InteractionError("rows 1-5 must be disjoint and exhaustive "
                               "given step 0; %d held: %r" % (len(hit), hit))
    out.update(relation=hit[0][1], step=hit[0][0])
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("interaction.py is a library; run: "
                         "python3 threshold-states/test_interaction.py\n")
        sys.exit(2)
    sys.stderr.write(__doc__)
    sys.exit(0)
