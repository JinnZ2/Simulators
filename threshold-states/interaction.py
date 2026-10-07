# SPDX-License-Identifier: CC0-1.0
"""interaction.py -- the two-reference interaction test, with its precedence.

Section 8 of threshold-states-in-animal-escape.md (repo root). A joint
(multimodal) response is read against two references: S, the additive
expectation from the separate (unimodal) responses, and M, the largest
single facilitating one. tol is a declared tolerance in the response's own
units.

PRECEDENCE (operator, 2026-10-07; resolves THIN T-7)
CUE SIGN (operator, 2026-10-07, after outside case OC-2)

    facilitating cues (>= 0): S+ = their sum, M = their max
    suppressive cues  (< 0):  N  = their sum, recorded as its own term
    additive expectation:     S  = S+ + N; rows 1-5 read joint against S
    no facilitating cue:      M undefined -> NO_FACILITATING_CUE  [CHOICE 2]

    0.  S+ - M <= 2*tol            BELOW_RESOLUTION
    1.  |joint - M| <= tol         REDUNDANT
    2.  |joint - S| <= tol         ADDITIVE              (I ~ 0, independent)
    3.  joint > S + tol            RESONANT
    4.  M + tol < joint < S - tol  ENHANCED_SUBADDITIVE
    5.  joint < M - tol            ANTAGONISTIC          (OPEN class)

    I = joint - S, the measurand of the RESONANT enum in
    JinnZ2/Polyhedral-Intelligence ontology/relation_classes.json @ 7387230.

Why step 0 exists. When S - M <= 2*tol the bands [M-tol, M+tol] and
[S-tol, S+tol] touch or overlap, so REDUNDANT and ADDITIVE cannot be told
apart. With no suppressive cue S = S+, step 0 is exactly that test, and
given it rows 1-5 are disjoint and exhaustive over the real line:

    (-inf, M-tol)  [M-tol, M+tol]  (M+tol, S-tol)  [S-tol, S+tol]  (S+tol, inf)
      ANTAG.         REDUNDANT       ENH_SUBADD      ADDITIVE        RESONANT

With a suppressive cue (N < 0) step 0 tests S+ - M, as specified, and S - M
can still be <= 2*tol. Then the M band and the S band touch, overlap, or
swap order (S < M), and some joints satisfy two rows. The rows stay
exhaustive. Where exactly one row holds, that row is returned. Where more
than one holds, classify() raises BandsOverlap naming the rows: an
ambiguous reading is refused, not resolved by order.  [CHOICE 1]

classify() evaluates all five rows every time and does not rely on the
band argument.

Consequence, computed and pinned in test_interaction.py: the split changes
a reading only where S - M <= 2*tol < S+ - M (plus NO_FACILITATING_CUE).
There the pre-split rule (S = sum of all cues, step 0 on S - M) read
BELOW_RESOLUTION; the split gives the one row that holds, or BandsOverlap.
Everywhere else the two rules agree. The split adds N as a recorded term;
it does not by itself give every suppressive case a reading. With one
facilitating cue S+ - M = 0, so step 0 fires at any tol >= 0 whatever N is
(outside case OC-2 still reads BELOW_RESOLUTION).

Correction recorded: joint = S is ADDITIVE, not ENHANCED_SUBADDITIVE. The
earlier table read "M < joint <= S" and put the sum itself in the
subadditive row.

STATES THAT ARE NOT RELATIONS
    NO_FACILITATING_CUE  every cue < 0, so M is undefined. Checked before
                         tol, since it is a property of the cues.  [CHOICE 3]
    UNRATED              tol undeclared (None). Not a zero tolerance.
    BELOW_RESOLUTION     step 0. A reading, not a relation between the cues.

CHOICES (made here, not in the operator's text)
    [CHOICE 1]  Overlap after step 0: pointwise. A unique row is returned;
                two or more rows raise BandsOverlap. The alternative,
                refusing the whole case once S - M <= 2*tol, was not taken.
    [CHOICE 2]  No facilitating cue: the operator offered "classify on N
                alone, or flag NO_FACILITATING_CUE". No rows were given for
                N alone, so the flag is taken.
    [CHOICE 3]  NO_FACILITATING_CUE is returned before the tol check, so
                such a case reads NO_FACILITATING_CUE even with tol None.
    A cue of exactly 0 is facilitating (>= 0), per the operator's text.

WHAT IT DOES NOT DO
    It does not choose tol. It does not define the ANTAGONISTIC class: it
    gives that open class a measurable boundary (joint < M - tol). The
    definition stays with the enum's author. Suppression (N < 0) borders
    that class; the split above is arithmetic only and does not define
    antagonism. Boundaries are compared in the caller's number type. Pass
    Fraction or Decimal where exact boundaries matter, since a float
    M + tol can round across a band edge.

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

NO_FACILITATING_CUE = "NO_FACILITATING_CUE"

RELATIONS = (REDUNDANT, ADDITIVE, RESONANT, ENHANCED_SUBADDITIVE, ANTAGONISTIC)
OPEN_CLASSES = (ANTAGONISTIC,)


class InteractionError(ValueError):
    pass


class BandsOverlap(InteractionError):
    """Two or more of rows 1-5 hold. Only reachable with N < 0 (see the
    module docstring); carries the rows that held and the references."""

    def __init__(self, rows, refs):
        self.rows = rows
        self.refs = refs
        ValueError.__init__(self, "bands overlap after step 0 (S - M = %r, "
                            "2*tol = %r); rows held: %r"
                            % (refs["S"] - refs["M"], 2 * refs["tol"], rows))


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


def split(separate):
    """Cue-sign split: dict S_plus, M, N, S, n_facilitating, n_suppressive.

    M is None when no cue is facilitating. Two or more cues are required.
    """
    separate = list(separate)
    if len(separate) < 2:
        raise InteractionError("an interaction needs two or more separate "
                               "responses, got %d" % len(separate))
    for i, x in enumerate(separate):
        _finite(x, "separate[%d]" % i)
    fac = [x for x in separate if x >= 0]
    sup = [x for x in separate if x < 0]
    S_plus = sum(fac)
    N = sum(sup)
    return {"S_plus": S_plus, "M": max(fac) if fac else None, "N": N,
            "S": S_plus + N, "n_facilitating": len(fac),
            "n_suppressive": len(sup)}


def references(separate):
    """(S, M): S = S+ + N, M = max facilitating cue (None if there is none)."""
    r = split(separate)
    return r["S"], r["M"]


def classify(joint, separate, tol):
    """Return a dict: relation, step, S, M, I, tol, S_plus, N,
    n_facilitating, n_suppressive.

    relation is one of RELATIONS, or NO_FACILITATING_CUE / UNRATED /
    BELOW_RESOLUTION. Raises BandsOverlap where two rows hold.
    """
    r = split(separate)
    _finite(joint, "joint")
    S, M = r["S"], r["M"]
    out = dict(r, I=joint - S, tol=tol)
    if M is None:
        out.update(relation=NO_FACILITATING_CUE, step=None)
        return out
    if tol is None:
        out.update(relation=UNRATED, step=None)
        return out
    _finite(tol, "tol")
    if tol < 0:
        raise InteractionError("tol must be >= 0, got %r" % (tol,))
    if r["S_plus"] - M <= 2 * tol:
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
    if len(hit) > 1:
        raise BandsOverlap(hit, out)
    if not hit:
        raise InteractionError("rows 1-5 must be exhaustive; none held "
                               "(S=%r M=%r tol=%r joint=%r)" % (S, M, tol, joint))
    out.update(relation=hit[0][1], step=hit[0][0])
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("interaction.py is a library; run: "
                         "python3 threshold-states/test_interaction.py\n")
        sys.exit(2)
    sys.stderr.write(__doc__)
    sys.exit(0)
