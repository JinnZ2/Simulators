# SPDX-License-Identifier: CC0-1.0
"""
The pairing separation -- the one operation the whole gap turns on.

The marker's load-bearing sentence is "measuring pairings instead of averaging
over them." An outcome for a specific operator on a specific unit decomposes
into three orthogonal parts:

    outcome(op_i, unit_j) = mu + a_i + b_j + r_ij
                             |     |     |     |
                             |     |     |     the PAIRING residual (coupling)
                             |     |     the unit's average effect
                             |     the operator's average effect
                             the grand mean

`a_i` and `b_j` are the two MAIN effects -- how good this operator is on
average, how good this unit is on average. `r_ij` is the INTERACTION: how
much better (or worse) THIS operator does on THIS unit than either average
predicts. A model that fits only the main effects -- the ordinary way
operator and machine are accounted for -- reports `r_ij` as noise and cannot
see the coupling at all.

This is the same decomposition run under three vocabularies with no
cross-citation (all carried from the marker, none a result here):
  - plant breeding: general combining ability (GCA = a_i, b_j) vs specific
    combining ability (SCA = r_ij), separated by diallel analysis;
  - primate field archaeology: preference for individual units (a_i, b_j) vs
    preference for pairings (r_ij), separated statistically;
  - two-way ANOVA: main effects vs the interaction term.

The separation is built and tested here on CONSTRUCTED data. Nothing here is
a result about any operator, machine, plant, or microbe: no fleet, plant,
incident, or symbiosis data is read (none is available -- egress-blocked),
and every literature claim in MARKER.md is carried, not verified.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from collections import namedtuple
from typing import Dict, List, Optional, Tuple

# One observation: an operator label, a unit label, an outcome value.
Obs = namedtuple("Obs", "operator unit value")

NOT_ESTIMABLE = "NOT_ESTIMABLE"
UNDEFINED = "UNDEFINED"

Decomp = namedtuple(
    "Decomp",
    "operators units mu a b r ss_op ss_unit ss_pair ss_total status detail")


def cell_means(obs: List[Obs]) -> Dict[Tuple[str, str], float]:
    """Mean outcome per (operator, unit) pairing."""
    acc: Dict[Tuple[str, str], List[float]] = {}
    for o in obs:
        acc.setdefault((o.operator, o.unit), []).append(o.value)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def _labels(obs: List[Obs]):
    ops, units = [], []
    for o in obs:
        if o.operator not in ops:
            ops.append(o.operator)
        if o.unit not in units:
            units.append(o.unit)
    return sorted(ops), sorted(units)


def decompose(obs: List[Obs]) -> Decomp:
    """Split the outcomes into grand mean + operator main effect + unit main
    effect + pairing residual, and return the orthogonal sums of squares.

    Requires a COMPLETE design -- every (operator, unit) pairing observed --
    because the interaction cannot be estimated for a pairing that was never
    run. An incomplete design returns status NOT_ESTIMABLE naming the missing
    pairings, which is itself the gap: the pairing effect is invisible
    exactly where the pairing was never measured.
    """
    if not obs:
        return Decomp((), (), None, {}, {}, {}, 0.0, 0.0, 0.0, 0.0,
                      NOT_ESTIMABLE, "no observations")
    ops, units = _labels(obs)
    cm = cell_means(obs)
    missing = [(i, j) for i in ops for j in units if (i, j) not in cm]
    if missing:
        return Decomp(tuple(ops), tuple(units), None, {}, {}, {}, 0.0, 0.0,
                      0.0, 0.0, NOT_ESTIMABLE,
                      "missing pairings: %s" % missing)
    I, J = len(ops), len(units)
    cells = {(i, j): cm[(i, j)] for i in ops for j in units}
    mu = sum(cells.values()) / (I * J)
    row_mean = {i: sum(cells[(i, j)] for j in units) / J for i in ops}
    col_mean = {j: sum(cells[(i, j)] for i in ops) / I for j in units}
    a = {i: row_mean[i] - mu for i in ops}
    b = {j: col_mean[j] - mu for j in units}
    r = {(i, j): cells[(i, j)] - mu - a[i] - b[j] for i in ops for j in units}
    ss_op = J * sum(a[i] ** 2 for i in ops)
    ss_unit = I * sum(b[j] ** 2 for j in units)
    ss_pair = sum(r[(i, j)] ** 2 for i in ops for j in units)
    ss_total = ss_op + ss_unit + ss_pair
    return Decomp(tuple(ops), tuple(units), mu, a, b, r,
                  ss_op, ss_unit, ss_pair, ss_total, "OK", None)


def interaction_fraction(obs: List[Obs]):
    """SS_pair / SS_total -- the share of structured variation that lives in
    the pairings rather than in either main effect. Returns None when the
    design is not estimable or when there is no structured variation at all
    (SS_total == 0) -- never 0.0 for 'undefined', which would read as 'no
    coupling' where the truth is 'nothing varies'."""
    d = decompose(obs)
    if d.status != "OK":
        return None
    if d.ss_total == 0.0:
        return None
    return d.ss_pair / d.ss_total


def best_pairing(obs: List[Obs]) -> Optional[Tuple[Tuple[str, str], float]]:
    """The pairing with the largest positive residual -- the coupled pair
    that outperforms what either partner's average predicts. This is the
    pair a main-effects model cannot surface: both partners can be exactly
    average on their own (a_i = b_j = 0) and the pairing still wins."""
    d = decompose(obs)
    if d.status != "OK":
        return None
    (i, j), val = max(d.r.items(), key=lambda kv: kv[1])
    return (i, j), val


def main_effects_prediction(d: Decomp, operator: str, unit: str) -> float:
    """What a model that AVERAGES over pairings predicts: mu + a_i + b_j. It
    is blind to r_ij by construction -- the difference between this and the
    observed cell mean IS the coupling the averaging discards."""
    return d.mu + d.a[operator] + d.b[unit]


def averaged_over_pairings_misses(obs: List[Obs]) -> Dict[str, object]:
    """The demonstration the marker asks for: how much the pairing structure
    a main-effects model throws away, and the specific pair it cannot see.
    Returns the discarded fraction and the best pair with the error a
    main-effects model makes on it."""
    d = decompose(obs)
    if d.status != "OK":
        return {"status": d.status, "detail": d.detail}
    frac = None if d.ss_total == 0 else d.ss_pair / d.ss_total
    bp = best_pairing(obs)
    detail = None
    if bp is not None:
        (i, j), resid = bp
        pred = main_effects_prediction(d, i, j)
        observed = pred + resid
        detail = {"pair": (i, j), "residual": resid,
                  "main_effects_predicts": pred, "observed": observed,
                  "operator_main_effect": d.a[i], "unit_main_effect": d.b[j]}
    return {"status": "OK", "discarded_pairing_fraction": frac,
            "best_pair": detail}


if __name__ == "__main__":
    import sys
    sys.stderr.write("coupling_separation.py is a library; its checks live "
                     "in operator-machine-coupling/selftest_omc.py.\n")
    sys.exit(2)
