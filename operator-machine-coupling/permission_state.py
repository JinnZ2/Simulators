# SPDX-License-Identifier: CC0-1.0
"""
The permission variable -- the third condition, institutional and usually
unrecorded.

    COUPLED_AUTHORIZED   operator reads unit, acts on the reading
    COUPLED_PROHIBITED   operator reads unit, files a report, waits;
                         the signal dies in the queue
    DECOUPLED            no reading to act on

The marker's two load-bearing points, both built here on CONSTRUCTED data:

  - Any study that treats maintenance regime as ONE variable collapses these
    three. `regime_collapse` shows a single regime label mapping many-to-one
    onto the three states, so the middle case disappears into an average.
  - Without the permission field, assignment structure alone carries
    permission, hiring selection, and coupling capacity as unseparated
    confounds. `attribution` shows a naive assignment effect that is actually
    the permission state, and returns UNDETERMINED when the field is absent
    and permission is collinear with assignment -- the recording problem the
    marker names. Recording the three-state variable costs one field and
    makes the effect attributable.

COUPLED_PROHIBITED is the cleanest test case (M2): the operator's diagnosis
exists as a record and can be scored against what the repair eventually
found. `m2_match_rate` computes that, gated to the middle state, and returns
NOT_RECORDED (never 0.0) when the permission field is absent.

Nothing here is a result about any real maintenance operation.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from collections import namedtuple
from typing import Dict, List, Optional

COUPLED_AUTHORIZED = "coupled_authorized"
COUPLED_PROHIBITED = "coupled_prohibited"
DECOUPLED = "decoupled"
STATES = (COUPLED_AUTHORIZED, COUPLED_PROHIBITED, DECOUPLED)

NOT_RECORDED = "NOT_RECORDED"          # the field was never written down
UNDETERMINED = "UNDETERMINED"

# A maintenance record. `permission` may be None -- the marker's recording
# problem: the state is almost never in any system.
Rec = namedtuple("Rec", "assignment permission outcome "
                        "operator_dx repair_found")


def validate_state(s: str) -> None:
    if s not in STATES:
        raise ValueError("permission state must be one of %r; got %r"
                         % (STATES, s))


def regime_collapse(records: List[Rec]) -> Dict[str, object]:
    """A single 'maintenance regime' label is many-to-one onto the three
    permission states. Returns, per assignment label, which permission states
    it actually contains -- if more than one, the label collapses them."""
    out: Dict[str, set] = {}
    for r in records:
        if r.permission is not None:
            out.setdefault(r.assignment, set()).add(r.permission)
    return {k: sorted(v) for k, v in out.items()}


def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def attribution(records: List[Rec]) -> Dict[str, object]:
    """Naive assignment effect vs the effect once permission is controlled.

    naive: mean(outcome | dedicated) - mean(outcome | pooled).
    controlled: the same difference computed WITHIN each permission stratum
                and averaged -- if permission drives the outcome, this shrinks
                toward zero and the naive effect was the confound.

    Returns UNDETERMINED for the controlled effect when the permission field
    is absent, or when permission is collinear with assignment (each
    assignment has only one permission state), because then the two cannot be
    separated -- the recording problem, quantified.
    """
    ded = [r.outcome for r in records if r.assignment == "dedicated"]
    pool = [r.outcome for r in records if r.assignment == "pooled"]
    naive = None
    if ded and pool:
        naive = _mean(ded) - _mean(pool)
    have_perm = [r for r in records if r.permission is not None]
    if len(have_perm) < len(records) or not have_perm:
        return {"naive_assignment_effect": naive,
                "controlled_assignment_effect": UNDETERMINED,
                "reason": "permission field absent on some/all records "
                          "(NOT_RECORDED); assignment carries it as a confound"}
    # collinearity: does each assignment carry more than one permission state?
    by_assign = regime_collapse(records)
    if all(len(v) <= 1 for v in by_assign.values()):
        return {"naive_assignment_effect": naive,
                "controlled_assignment_effect": UNDETERMINED,
                "reason": "permission is collinear with assignment (each "
                          "assignment has one permission state); not separable "
                          "even with the field"}
    diffs = []
    for st in STATES:
        d = [r.outcome for r in records
             if r.assignment == "dedicated" and r.permission == st]
        p = [r.outcome for r in records
             if r.assignment == "pooled" and r.permission == st]
        if d and p:
            diffs.append(_mean(d) - _mean(p))
    controlled = _mean(diffs) if diffs else UNDETERMINED
    return {"naive_assignment_effect": naive,
            "controlled_assignment_effect": controlled,
            "reason": None}


def m2_match_rate(records: List[Rec]) -> object:
    """M2, the cleanest test case: among COUPLED_PROHIBITED records (operator
    diagnosed, was not authorized to act), the fraction where the operator's
    diagnosis matched what the repair eventually found. Returns NOT_RECORDED
    (not 0.0) when no record carries the permission field, so an absent field
    never reads as a zero match rate."""
    if not any(r.permission is not None for r in records):
        return NOT_RECORDED
    prohibited = [r for r in records if r.permission == COUPLED_PROHIBITED
                  and r.operator_dx is not None and r.repair_found is not None]
    if not prohibited:
        return None            # no scorable middle-case records (not 0.0)
    matches = sum(1 for r in prohibited if r.operator_dx == r.repair_found)
    return matches / len(prohibited)


if __name__ == "__main__":
    import sys
    sys.stderr.write("permission_state.py is a library; its checks live in "
                     "operator-machine-coupling/selftest_omc.py.\n")
    sys.exit(2)
