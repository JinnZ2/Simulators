"""Scope-transition experiment engine (v0.2). Standard library only.

Behavior (as specified; nothing more):
  1. Take cases in the order given. The engine never sorts by factor value.
  2. Compare adjacent cases in that order and calculate output changes.
  3. Record changes that exceed a declared threshold as CANDIDATE transition
     regions.
  4. Preserve missing inputs: a missing factor or output is recorded with a
     reason, never silently dropped, interpolated, or replaced.
  5. Report candidate regions without declaring their causes or significance.

Interpretation boundary: an exceedance is a recorded observation, not a
verdict. The engine does not decide that a scope boundary exists, that a
model failed, or that a transition is real. Those remain questions for
follow-up experiments recorded separately.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable
import math

THRESHOLD_KINDS = ("absolute", "relative")
DELTA_STATUSES = ("computed", "not_computed")
DIRECTIONS = ("increase", "decrease", "unchanged", "unknown")


@dataclass(frozen=True)
class Case:
    """One observed case in a factor-variation series."""
    case_id: str
    factor_value: float | None
    output_value: float | None
    factor_label: str = "factor"
    output_label: str = "output"
    notes: tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.case_id, str) or not self.case_id.strip():
            raise ValueError("case_id must be a non-empty string.")
        for name, value in (("factor_value", self.factor_value),
                            ("output_value", self.output_value)):
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a number or None.")


@dataclass(frozen=True)
class AdjacentDelta:
    """Comparison of two adjacent cases in the given order."""
    left_index: int
    right_index: int
    left_case_id: str
    right_case_id: str
    factor_left: float | None
    factor_right: float | None
    output_left: float | None
    output_right: float | None
    delta: float | None
    absolute_delta: float | None
    relative_delta: float | None
    delta_status: str
    notes: tuple[str, ...] = ()


def _finite(value: float | None) -> bool:
    return value is not None and math.isfinite(float(value))


def _direction(delta: float | None) -> str:
    if delta is None:
        return "unknown"
    if delta > 0:
        return "increase"
    if delta < 0:
        return "decrease"
    return "unchanged"


def adjacent_deltas(cases: Iterable[Case],
                    zero_tolerance: float = 0.0) -> list[AdjacentDelta]:
    """Compare each adjacent pair in the given order; record, never drop.

    Relative change is measured against the left (earlier-in-order) output.
    It is undefined when that output is within zero_tolerance of zero; the
    absolute delta is still computed and the reason is recorded.
    """
    ordered = list(cases)
    if not math.isfinite(float(zero_tolerance)) or zero_tolerance < 0:
        raise ValueError("zero_tolerance must be finite and non-negative.")
    deltas: list[AdjacentDelta] = []
    for left_index in range(len(ordered) - 1):
        left = ordered[left_index]
        right = ordered[left_index + 1]
        notes: list[str] = []
        reasons = []
        if not _finite(left.factor_value):
            reasons.append("left factor missing or non-finite")
        if not _finite(right.factor_value):
            reasons.append("right factor missing or non-finite")
        if not _finite(left.output_value):
            reasons.append("left output missing or non-finite")
        if not _finite(right.output_value):
            reasons.append("right output missing or non-finite")

        delta = absolute = relative = None
        if not reasons:
            delta = float(right.output_value) - float(left.output_value)
            absolute = abs(delta)
            if abs(float(left.output_value)) > zero_tolerance:
                relative = absolute / abs(float(left.output_value))
            else:
                notes.append(
                    "Relative change undefined: left output is within zero "
                    "tolerance; absolute delta retained."
                )
            status = "computed"
        else:
            notes.append("Delta not computed: " + "; ".join(reasons) + ".")
            status = "not_computed"

        deltas.append(AdjacentDelta(
            left_index=left_index, right_index=left_index + 1,
            left_case_id=left.case_id, right_case_id=right.case_id,
            factor_left=left.factor_value, factor_right=right.factor_value,
            output_left=left.output_value, output_right=right.output_value,
            delta=delta, absolute_delta=absolute, relative_delta=relative,
            delta_status=status, notes=tuple(notes),
        ))
    return deltas


def scan_transitions(cases: Iterable[Case], *, threshold: float,
                     threshold_kind: str = "absolute",
                     zero_tolerance: float = 0.0,
                     scan_label: str | None = None) -> dict[str, Any]:
    """Record candidate transition regions where adjacent change exceeds
    threshold. Exceedance test is strictly greater-than: a change exactly
    equal to the threshold is recorded but NOT flagged as a candidate.
    """
    if not math.isfinite(float(threshold)) or threshold < 0:
        raise ValueError("threshold must be finite and non-negative.")
    if threshold_kind not in THRESHOLD_KINDS:
        raise ValueError(f"threshold_kind must be one of {THRESHOLD_KINDS}.")

    ordered = list(cases)
    deltas = adjacent_deltas(ordered, zero_tolerance=zero_tolerance)

    candidates: list[dict[str, Any]] = []
    unresolved: list[str] = []
    for d in deltas:
        unresolved.extend(d.notes)
        if d.delta_status != "computed":
            continue
        metric = d.absolute_delta if threshold_kind == "absolute" else d.relative_delta
        if metric is None:
            unresolved.append(
                f"{threshold_kind} metric undefined between {d.left_case_id} "
                f"and {d.right_case_id}; exceedance not evaluated."
            )
            continue
        if metric > threshold:
            candidates.append({
                "between": [d.left_case_id, d.right_case_id],
                "order_indices": [d.left_index, d.right_index],
                "factor_interval": [d.factor_left, d.factor_right],
                "output_change": d.delta,
                "direction": _direction(d.delta),
                "metric_kind": threshold_kind,
                "metric_value": metric,
                "threshold": float(threshold),
                "classification": "candidate transition region; cause and "
                                  "significance unassigned",
            })

    factor_label = ordered[0].factor_label if ordered else "factor"
    output_label = ordered[0].output_label if ordered else "output"
    return {
        "scan_label": scan_label,
        "factor_label": factor_label,
        "output_label": output_label,
        "case_count": len(ordered),
        "cases": [{
            "order_index": i, "case_id": c.case_id,
            "factor_value": c.factor_value, "output_value": c.output_value,
            "notes": list(c.notes),
        } for i, c in enumerate(ordered)],
        "deltas_computed": sum(1 for d in deltas if d.delta_status == "computed"),
        "deltas_not_computed": sum(1 for d in deltas if d.delta_status == "not_computed"),
        "candidate_regions": candidates,
        "unresolved": unresolved,
        "config": {
            "threshold": float(threshold),
            "threshold_kind": threshold_kind,
            "zero_tolerance": float(zero_tolerance),
            "exceedance_rule": "strictly greater than threshold",
            "ordering_rule": "input order preserved; never sorted",
        },
        "interpretation": "unassigned",
        "limitations": [
            "Candidate regions are recorded observations, not detected boundaries.",
            "No cause, significance level, or model verdict is assigned.",
            "Adjacent-pair comparison cannot distinguish a transition from "
            "noise, measurement error, or an unrecorded confound.",
        ],
    }
