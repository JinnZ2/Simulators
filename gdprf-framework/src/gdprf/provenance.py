"""Provenance layer — lineage for every evidence ingestion and belief update.

Every gradient update must be auditable: what evidence entered, from which
instrument, under which calibration state, processed by which engine version,
and what the belief was before and after. Records follow a W3C PROV-inspired
Entity / Activity / Agent model and are hash-chained so the ledger is
tamper-evident.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProvenanceRecord:
    """One immutable entry in the provenance ledger.

    entity:   what was produced/consumed (claim_id, proxy_id, edge_id)
    activity: what happened (evidence_ingestion, calibration, gradient_update,
              gate_decision, decision_point)
    agent:    what performed it (engine version, calibration method, human id)
    """
    record_id: str
    entity: str
    activity: str
    agent: str
    inputs: dict = field(default_factory=dict)    # state before / evidence in
    outputs: dict = field(default_factory=dict)   # state after / result
    timestamp: str = field(default_factory=_now)
    content_hash: str = ""
    previous_hash: str = ""

    def seal(self, previous_hash: str = "") -> "ProvenanceRecord":
        self.previous_hash = previous_hash
        payload = json.dumps(
            {k: v for k, v in asdict(self).items() if k not in ("content_hash",)},
            sort_keys=True, default=str)
        self.content_hash = hashlib.sha256(payload.encode()).hexdigest()
        return self


class ProvenanceLedger:
    """Append-only, hash-chained ledger. Verify with .verify_chain()."""

    def __init__(self):
        self.records: list[ProvenanceRecord] = []

    def append(self, record: ProvenanceRecord) -> ProvenanceRecord:
        prev = self.records[-1].content_hash if self.records else "GENESIS"
        record.seal(prev)
        self.records.append(record)
        return record

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for r in self.records:
            if r.previous_hash != prev:
                return False
            payload = json.dumps(
                {k: v for k, v in asdict(r).items() if k not in ("content_hash",)},
                sort_keys=True, default=str)
            if hashlib.sha256(payload.encode()).hexdigest() != r.content_hash:
                return False
            prev = r.content_hash
        return True

    def lineage(self, entity: str) -> list[ProvenanceRecord]:
        """All records touching one entity, in order — the audit trail."""
        return [r for r in self.records if r.entity == entity]

    def to_json(self) -> str:
        return json.dumps([asdict(r) for r in self.records], indent=2, default=str)
