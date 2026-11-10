"""Core data structures and audit operations. Standard library only."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Iterable
import json
import math
import uuid

SCHEMA_VERSION = "0.1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class Record:
    schema_version: str
    record_type: str
    record_id: str
    created_utc: str
    payload: dict[str, Any]

    @classmethod
    def create(cls, record_type: str, payload: dict[str, Any],
               record_id: str | None = None) -> "Record":
        return cls(SCHEMA_VERSION, record_type, record_id or new_id(record_type),
                   utc_now(), payload)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class NumericComparison:
    prediction: float
    observation: float
    residual: float
    absolute_residual: float
    relative_residual: float | None
    combined_uncertainty: float | None
    normalized_residual: float | None
    comparison_status: str
    notes: tuple[str, ...] = ()


def compare_numeric(prediction: float, observation: float,
                    prediction_uncertainty: float | None = None,
                    observation_uncertainty: float | None = None,
                    zero_tolerance: float = 0.0) -> NumericComparison:
    """Calculate comparison fields; do not infer a cause or pass/fail verdict."""
    if not all(math.isfinite(float(v)) for v in (prediction, observation, zero_tolerance)):
        raise ValueError("Prediction, observation, and zero_tolerance must be finite.")
    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be non-negative.")
    for name, value in (("prediction_uncertainty", prediction_uncertainty),
                        ("observation_uncertainty", observation_uncertainty)):
        if value is not None and (not math.isfinite(float(value)) or value < 0):
            raise ValueError(f"{name} must be finite and non-negative.")

    residual = float(observation) - float(prediction)
    absolute = abs(residual)
    relative = absolute / abs(float(observation)) if abs(float(observation)) > zero_tolerance else None
    combined = normalized = None
    notes = []
    if prediction_uncertainty is not None and observation_uncertainty is not None:
        combined = math.hypot(float(prediction_uncertainty), float(observation_uncertainty))
        if combined > 0:
            normalized = residual / combined
        else:
            notes.append("Normalized residual undefined because combined uncertainty is zero.")
    else:
        notes.append("Combined uncertainty not calculated: both uncertainty inputs are required.")
    if relative is None:
        notes.append("Relative residual undefined because observation is within zero tolerance.")

    return NumericComparison(float(prediction), float(observation), residual, absolute,
                             relative, combined, normalized,
                             "computed; interpretation unresolved", tuple(notes))


def make_model(*, name: str, version: str, purpose: str, target_quantity: str,
               scope_included: Iterable[str], scope_excluded: Iterable[str] = (),
               assumptions: Iterable[str] = (), dependencies: Iterable[dict[str, Any]] = (),
               units: dict[str, str] | None = None, unknowns: Iterable[str] = (),
               representation: dict[str, Any] | None = None,
               provenance: dict[str, Any] | None = None) -> Record:
    required = {"name": name, "version": version, "purpose": purpose,
                "target_quantity": target_quantity}
    for field, value in required.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string.")
    payload = {
        **required,
        "scope": {"included": list(scope_included), "excluded": list(scope_excluded)},
        "assumptions": list(assumptions),
        "dependencies": list(dependencies),
        "units": units or {},
        "unknowns": list(unknowns),
        "representation": representation or {},
        "provenance": provenance or {"status": "not supplied"},
    }
    return Record.create("model", payload)


def make_experiment(*, model_record_id: str, question: str, conditions: dict[str, Any],
                    changed_factors: Iterable[str], control_description: str,
                    planned_comparisons: Iterable[str] = (),
                    expected_observations: str | None = None,
                    status: str = "planned") -> Record:
    if not model_record_id.strip() or not question.strip():
        raise ValueError("model_record_id and question must be non-empty.")
    if status not in {"planned", "run", "aborted", "incomplete"}:
        raise ValueError("status must be planned, run, aborted, or incomplete.")
    return Record.create("experiment", {
        "model_record_id": model_record_id, "question": question, "conditions": conditions,
        "changed_factors": list(changed_factors), "control_description": control_description,
        "planned_comparisons": list(planned_comparisons),
        "expected_observations": expected_observations, "status": status,
    })


def make_observation(*, experiment_record_id: str, model_record_id: str, quantity: str,
                     predicted_value: float | None, observed_value: float | None,
                     unit: str | None, prediction_uncertainty: float | None = None,
                     observation_uncertainty: float | None = None, method: str = "unspecified",
                     conditions: dict[str, Any] | None = None,
                     source_kind: str = "unspecified", notes: Iterable[str] = ()) -> Record:
    payload = {
        "experiment_record_id": experiment_record_id, "model_record_id": model_record_id,
        "quantity": quantity, "predicted_value": predicted_value, "observed_value": observed_value,
        "unit": unit, "prediction_uncertainty": prediction_uncertainty,
        "observation_uncertainty": observation_uncertainty, "method": method,
        "conditions": conditions or {}, "source_kind": source_kind, "notes": list(notes),
        "interpretation": "unassigned", "candidate_explanations": [],
    }
    if predicted_value is not None and observed_value is not None:
        payload["comparison"] = asdict(compare_numeric(
            predicted_value, observed_value, prediction_uncertainty, observation_uncertainty))
    else:
        payload["comparison"] = {"comparison_status": "not computed",
                                 "reason": "prediction or observation missing"}
    return Record.create("observation", payload)


def make_audit_event(*, subject_record_ids: Iterable[str], event_kind: str,
                     description: str, evidence: Iterable[str] = (),
                     unresolved_questions: Iterable[str] = (),
                     proposed_next_tests: Iterable[str] = ()) -> Record:
    if not event_kind.strip() or not description.strip():
        raise ValueError("event_kind and description must be non-empty.")
    return Record.create("audit_event", {
        "subject_record_ids": list(subject_record_ids), "event_kind": event_kind,
        "description": description, "evidence": list(evidence),
        "unresolved_questions": list(unresolved_questions),
        "proposed_next_tests": list(proposed_next_tests), "verdict": None,
    })


def validate_record(data: dict[str, Any]) -> list[str]:
    errors = []
    for key in ("schema_version", "record_type", "record_id", "created_utc", "payload"):
        if key not in data:
            errors.append(f"missing top-level field: {key}")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"unsupported schema_version: {data.get('schema_version')!r}")
    if data.get("record_type") not in {"model", "experiment", "observation", "audit_event"}:
        errors.append(f"unknown record_type: {data.get('record_type')!r}")
    if not isinstance(data.get("payload"), dict):
        errors.append("payload must be an object")
    return errors


def write_jsonl(path: str, records: Iterable[Record]) -> int:
    """Append JSONL records; never overwrite an existing event stream."""
    count = 0
    with open(path, "a", encoding="utf-8") as stream:
        for record in records:
            stream.write(record.to_json() + "\n")
            count += 1
    return count


def read_jsonl(path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records, errors = [], []
    with open(path, "r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append({"line": line_number, "error": f"invalid JSON: {exc.msg}"})
                continue
            structural = validate_record(data)
            if structural:
                errors.append({"line": line_number, "error": structural})
            else:
                records.append(data)
    return records, errors
