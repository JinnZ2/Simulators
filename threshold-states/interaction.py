# SPDX-License-Identifier: CC0-1.0
"""interaction.py -- the two-reference interaction test, with its precedence.

Section 8 of threshold-states-in-animal-escape.md (repo root). A joint
(multimodal) response is read against two references: S, the additive
expectation from the separate (unimodal) responses, and M, the largest
single facilitating one. tol is declared as {value, mode}.

Built to operator spec decisions Q1-Q4 (2026-10-07, PROPOSED) and the OPEN
resolution of the same day. The outside cases v2 that test this build were
committed alone, before this build, at 95abc5d (outside_cases_v2.json).

REFERENCES (Q1: cue sign governs)

    S+  = sum of the cues >= 0     (facilitating; a cue of 0 is facilitating)
    M   = max of the cues >= 0     (None when no cue is >= 0)
    N   = sum of the cues < 0      (suppressive; recorded as its own term)
    S   = S+ + N                   (full additive expectation)
    I   = joint - S                (measurand of the RESONANT enum in
                                    JinnZ2/Polyhedral-Intelligence
                                    ontology/relation_classes.json @ 7387230)
    tol = {"value": v, "mode": "absolute" | "relative_to_M"}
          absolute       tol_abs = v
          relative_to_M  tol_abs = v * M      (computed after order 5)

PRECEDENCE (Q2): first match wins. classify() RETURNS every verdict; it
raises only on an internal contradiction (rows not disjoint after 0b).

    order  verdict               condition
    1      MALFORMED_INPUT       see EDGE INPUTS
    2      INSUFFICIENT_CUES     fewer than 2 cues
    3      UNRATED               no tol, or tol with no value
    4      MODE_UNDECLARED       tol value present, mode absent (bare number)
    5      NO_FACILITATING_CUE   no cue >= 0, so M is undefined
    6      BELOW_RESOLUTION      0a  S+ - M <= 2*tol_abs
    7      SUPPRESSION_OVERLAP   0b  S  - M <= 2*tol_abs   (reports I; no class)
    8      rows 1-5, reached only when S - M > 2*tol_abs:
           1  |joint - M| <= tol_abs             REDUNDANT
           2  |joint - S| <= tol_abs             ADDITIVE
           3  joint > S + tol_abs                RESONANT
           4  M + tol_abs < joint < S - tol_abs  ENHANCED_SUBADDITIVE
           5  joint < M - tol_abs                ANTAGONISTIC  (OPEN class)

Once 0a and 0b have not fired the bands are disjoint and exhaustive:

    (-inf, M-tol)  [M-tol, M+tol]  (M+tol, S-tol)  [S-tol, S+tol]  (S+tol, inf)
      ANTAG.         REDUNDANT       ENH_SUBADD      ADDITIVE        RESONANT

Each verdict carries a distinct next action (NEXT_ACTION, returned as
next_action).

EDGE INPUTS (Q3, Q4, OPEN resolution)

    numeric data fields (cues, joint): a non-number -- str, bool, None, NaN,
        +inf, -inf -- is MALFORMED_INPUT. bool is refused although Python
        treats it as an int.
    cues not a list or tuple                      MALFORMED_INPUT
    tol None (or not passed)                      UNRATED
    tol dict with value None or no value key      UNRATED
    tol a bare number                             MODE_UNDECLARED
    tol dict, value present, mode None or absent  MODE_UNDECLARED
    tol value < 0, or a non-number other than     MALFORMED_INPUT
        None (str, bool, NaN, +inf, -inf)
    tol value = 0                                 allowed (exact comparison)
    extra keys in a tol dict                      MALFORMED_INPUT
    mode present and not one of the two names     MALFORMED_INPUT
    tol neither None, a number nor a dict         MALFORMED_INPUT
    negative cues                                 allowed (they are N)

    Absence of a declaration is not malformation; a declaration that is
    present and wrong is.

CHOICES (made here, not in the operator's text)
    [CHOICE 5]  A tol dict with no "value" key reads as value None (UNRATED).
                The operator's text says "tol with no value"; a missing key
                and a null value are taken as the same absence.
    [CHOICE 6]  A tol that is a string or a bool (not a dict, not a number)
                is MALFORMED_INPUT: a value is present and is not a number.
                Order 4 is reserved for a NUMBER given without a mode.
    [CHOICE 7]  When malformation is found in two places, the reason names
                the first in the order cues, joint, tol. The verdict does not
                depend on it.
    Retired: CHOICE 1 (pointwise overlap / BandsOverlap) is superseded by
    0b; CHOICE 3 (NO_FACILITATING_CUE before the tol check) is superseded by
    Q2 order 3-5; CHOICE 4 is the OPEN resolution, now the operator's.
    CHOICE 2 (flag NO_FACILITATING_CUE rather than classify on N) stands.

WHAT IT DOES NOT DO
    It does not choose tol. It does not define the ANTAGONISTIC class: it
    gives that open class a measurable boundary (joint < M - tol). The
    definition stays with the enum's author. Boundaries are compared in the
    caller's number type; pass Fraction or Decimal where exact boundaries
    matter, since a float M + tol can round across a band edge.

Stdlib only. Library module: refuses --selftest (exit 2); the checks are in
test_interaction.py beside it.
"""
from __future__ import annotations

import decimal
import math
import numbers
import sys

MALFORMED_INPUT = "MALFORMED_INPUT"
INSUFFICIENT_CUES = "INSUFFICIENT_CUES"
UNRATED = "UNRATED"
MODE_UNDECLARED = "MODE_UNDECLARED"
NO_FACILITATING_CUE = "NO_FACILITATING_CUE"
BELOW_RESOLUTION = "BELOW_RESOLUTION"
SUPPRESSION_OVERLAP = "SUPPRESSION_OVERLAP"
REDUNDANT = "REDUNDANT"
ADDITIVE = "ADDITIVE"
RESONANT = "RESONANT"
ENHANCED_SUBADDITIVE = "ENHANCED_SUBADDITIVE"
ANTAGONISTIC = "ANTAGONISTIC"

RELATIONS = (REDUNDANT, ADDITIVE, RESONANT, ENHANCED_SUBADDITIVE, ANTAGONISTIC)
OPEN_CLASSES = (ANTAGONISTIC,)
# Orders 1-7, in precedence order.
STATES = (MALFORMED_INPUT, INSUFFICIENT_CUES, UNRATED, MODE_UNDECLARED,
          NO_FACILITATING_CUE, BELOW_RESOLUTION, SUPPRESSION_OVERLAP)
VERDICTS = STATES + RELATIONS

NEXT_ACTION = {
    MALFORMED_INPUT: "fix the input",
    INSUFFICIENT_CUES: "add cues",
    UNRATED: "declare tol",
    MODE_UNDECLARED: "declare the tol mode",
    NO_FACILITATING_CUE: "separate suppression study",
    BELOW_RESOLUTION: "tighten tol / more samples",
    SUPPRESSION_OVERLAP: "model suppression explicitly",
    REDUNDANT: "read as redundant (joint ~ M)",
    ADDITIVE: "read as additive (I ~ 0, independent)",
    RESONANT: "read as resonant (I > tol)",
    ENHANCED_SUBADDITIVE: "read as enhanced, subadditive",
    ANTAGONISTIC: "refer the boundary to the enum's author (open class)",
}

TOL_MODES = ("absolute", "relative_to_M")


class InteractionError(ValueError):
    """Internal contradiction only. Input problems are returned as verdicts."""


def absolute(value):
    return {"value": value, "mode": "absolute"}


def relative_to_M(value):
    return {"value": value, "mode": "relative_to_M"}


def _is_number(x):
    # A finite number, not something float() can parse: "1" is not a number.
    if isinstance(x, bool) or not isinstance(x, (numbers.Real, decimal.Decimal)):
        return False
    try:
        return math.isfinite(float(x))
    except (TypeError, ValueError, OverflowError):
        return False


def _tol_reading(tol):
    """(kind, value, mode, reason) for a tol declaration.

    kind is MALFORMED_INPUT, UNRATED, MODE_UNDECLARED or "OK".
    """
    if tol is None:
        return UNRATED, None, None, "no tol declared"
    if isinstance(tol, dict):
        extra = sorted(set(tol) - {"value", "mode"})
        if extra:
            return MALFORMED_INPUT, None, None, "tol carries unknown keys %r" % extra
        value, mode = tol.get("value"), tol.get("mode")
        if mode is not None and mode not in TOL_MODES:
            return MALFORMED_INPUT, value, mode, ("tol mode must be one of %r, "
                                                  "got %r" % (TOL_MODES, mode))
        if value is not None and not _is_number(value):
            return MALFORMED_INPUT, value, mode, ("tol value must be a finite "
                                                  "number, got %r" % (value,))
        if value is not None and value < 0:
            return MALFORMED_INPUT, value, mode, "tol value must be >= 0, got %r" % (value,)
        if value is None:
            return UNRATED, None, mode, "tol has no value (undeclared)"
        if mode is None:
            return MODE_UNDECLARED, value, None, "tol value given with no mode"
        return "OK", value, mode, None
    if _is_number(tol):
        if tol < 0:
            return MALFORMED_INPUT, tol, None, "tol value must be >= 0, got %r" % (tol,)
        return MODE_UNDECLARED, tol, None, "tol given as a bare number (no mode)"
    return MALFORMED_INPUT, tol, None, ("tol must be None, a number or "
                                        "{value, mode}, got %r" % (tol,))


def split(separate):
    """Cue-sign split: dict S_plus, M, N, S, n_facilitating, n_suppressive.

    M is None when no cue is facilitating. Assumes the cues are finite
    numbers (classify() checks that first); raises InteractionError if not.
    """
    separate = list(separate)
    for i, x in enumerate(separate):
        if not _is_number(x):
            raise InteractionError("separate[%d] is not a finite number: %r" % (i, x))
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


def rows(joint, S, M, tol):
    """The five row predicates, without steps 0a/0b.

    Returns [(row, relation, held)]. classify() applies 0a and 0b first;
    this exists so a check can show what the rows do when they are bypassed.
    """
    return [
        (1, REDUNDANT, abs(joint - M) <= tol),
        (2, ADDITIVE, abs(joint - S) <= tol),
        (3, RESONANT, joint > S + tol),
        (4, ENHANCED_SUBADDITIVE, M + tol < joint < S - tol),
        (5, ANTAGONISTIC, joint < M - tol),
    ]


_EMPTY = ("S_plus", "M", "N", "S", "I", "n_facilitating", "n_suppressive",
          "tol", "tol_value", "tol_mode")


def _verdict(out, relation, order, step=None, reason=None):
    out.update(relation=relation, order=order, step=step, reason=reason,
               next_action=NEXT_ACTION[relation])
    return out


def classify(joint, separate, tol=None):
    """Return a dict: relation, order (1-8), step (0a / 0b / row number or
    None), reason, next_action, S_plus, M, N, S, I, n_facilitating,
    n_suppressive, tol (tol_abs), tol_value, tol_mode.

    relation is one of VERDICTS. Fields not computed at the verdict's order
    are None. Never raises on input; see the module docstring.
    """
    out = dict.fromkeys(_EMPTY)
    # 1. MALFORMED_INPUT
    if not isinstance(separate, (list, tuple)):
        return _verdict(out, MALFORMED_INPUT, 1,
                        reason="cues must be a list, got %r" % (separate,))
    for i, x in enumerate(separate):
        if not _is_number(x):
            return _verdict(out, MALFORMED_INPUT, 1,
                            reason="cue %d is not a finite number: %r" % (i, x))
    if not _is_number(joint):
        return _verdict(out, MALFORMED_INPUT, 1,
                        reason="joint is not a finite number: %r" % (joint,))
    kind, value, mode, why = _tol_reading(tol)
    out.update(tol_value=value, tol_mode=mode)
    if kind == MALFORMED_INPUT:
        return _verdict(out, MALFORMED_INPUT, 1, reason=why)
    # 2. INSUFFICIENT_CUES
    if len(separate) < 2:
        return _verdict(out, INSUFFICIENT_CUES, 2,
                        reason="%d cue(s); an interaction needs 2 or more"
                        % len(separate))
    r = split(separate)
    out.update(r, I=joint - r["S"])
    S, M = r["S"], r["M"]
    # 3, 4
    if kind == UNRATED:
        return _verdict(out, UNRATED, 3, reason=why)
    if kind == MODE_UNDECLARED:
        return _verdict(out, MODE_UNDECLARED, 4, reason=why)
    # 5
    if M is None:
        return _verdict(out, NO_FACILITATING_CUE, 5,
                        reason="no cue >= 0; M is undefined")
    tol_abs = value if mode == "absolute" else value * M
    out["tol"] = tol_abs
    # 6. 0a
    if r["S_plus"] - M <= 2 * tol_abs:
        return _verdict(out, BELOW_RESOLUTION, 6, step="0a",
                        reason="S+ - M = %r <= 2*tol = %r" % (r["S_plus"] - M, 2 * tol_abs))
    # 7. 0b
    if S - M <= 2 * tol_abs:
        return _verdict(out, SUPPRESSION_OVERLAP, 7, step="0b",
                        reason="S - M = %r <= 2*tol = %r; I = %r reported, no class"
                        % (S - M, 2 * tol_abs, out["I"]))
    # 8. rows 1-5
    hit = [(n, rel) for n, rel, cond in rows(joint, S, M, tol_abs) if cond]
    if len(hit) != 1:
        raise InteractionError("rows 1-5 must be disjoint and exhaustive once "
                               "S - M > 2*tol; held %r (S=%r M=%r tol=%r joint=%r)"
                               % (hit, S, M, tol_abs, joint))
    return _verdict(out, hit[0][1], 8, step=hit[0][0])


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("interaction.py is a library; run: "
                         "python3 threshold-states/test_interaction.py\n")
        sys.exit(2)
    sys.stderr.write(__doc__)
    sys.exit(0)
