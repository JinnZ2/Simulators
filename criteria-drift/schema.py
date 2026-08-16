"""
schema.py — Core data structures for the Criteria Drift Auditor.

Aligned with the Declared Frame:
  boundary, horizon, who_counts, sign_source, logic, observer_access

Each CriteriaVersion is a snapshot of the ruler at a point in time.
ModelScores are attached to versions, not to models in isolation.
"""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List, Any
import json


@dataclass
class Frame:
    """The six-field declared frame. UNKNOWN is a legal value."""
    boundary: str
    horizon: str
    who_counts: str
    sign_source: str
    logic: str
    observer_access: str

    def validate(self) -> List[str]:
        problems = []
        for field in ["boundary", "horizon", "who_counts",
                      "sign_source", "logic", "observer_access"]:
            val = getattr(self, field, None)
            if val is None:
                problems.append(f"OMITTED   {field} — write 'unknown'")
            elif str(val).strip() == "":
                problems.append(f"EMPTY     {field}")
        return problems

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> "Frame":
        return cls(
            boundary=d.get("boundary", "unknown"),
            horizon=d.get("horizon", "unknown"),
            who_counts=d.get("who_counts", "unknown"),
            sign_source=d.get("sign_source", "unknown"),
            logic=d.get("logic", "unknown"),
            observer_access=d.get("observer_access", "unknown"),
        )


@dataclass
class CriteriaVersion:
    """One version of a benchmark/evaluation criteria."""
    artifact_name: str          # e.g. "MMLU", "HumanEval"
    version_id: str             # e.g. "v1.0", "v2.0-pro"
    timestamp: str              # ISO-8601
    frame: Frame
    # Optional structured rubric for deeper drift measurement
    rubric_dimensions: Optional[List[str]] = None
    rubric_weights: Optional[Dict[str, float]] = None
    exemplar_count: Optional[int] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["frame"] = self.frame.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CriteriaVersion":
        return cls(
            artifact_name=d["artifact_name"],
            version_id=d["version_id"],
            timestamp=d["timestamp"],
            frame=Frame.from_dict(d["frame"]),
            rubric_dimensions=d.get("rubric_dimensions"),
            rubric_weights=d.get("rubric_weights"),
            exemplar_count=d.get("exemplar_count"),
            notes=d.get("notes", ""),
        )


@dataclass
class ModelScore:
    """A model's reported score on a specific criteria version."""
    model_name: str
    criteria_artifact: str
    criteria_version: str
    score: float                # 0.0–1.0 or raw
    score_type: str             # "accuracy", "pass@1", "win_rate", etc.
    timestamp: str              # when reported
    source_url: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelScore":
        return cls(**d)
