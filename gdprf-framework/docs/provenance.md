# Provenance Layer

Every belief change in GDPRF must be auditable. The provenance layer records the
full lineage of evidence and updates: **what** entered, **from which** instrument,
**under which** calibration state, processed by **which** engine version, and what
belief looked like **before and after**.

## Model

Records follow a W3C PROV-inspired triple:

| Field | Role | Examples |
|---|---|---|
| `entity` | What was produced/consumed | claim_id, proxy_id, edge_id |
| `activity` | What happened | `evidence_ingestion`, `calibration`, `cascade_assembly`, `gradient_update`, `gate_decision`, `decision_point` |
| `agent` | What performed it | engine version, calibration method, human reviewer id |

Each record carries `inputs` (state before / evidence in) and `outputs` (state
after / result), a timestamp, and two hashes.

## Tamper-Evident Hash Chain

The ledger is append-only and hash-chained: every record's `content_hash` covers
its full content plus the previous record's hash. Modifying any historical record
breaks `verify_chain()` — the same property that makes audit logs trustworthy in
regulated metrology, applied here to machine belief.

```python
from gdprf.provenance import ProvenanceLedger, ProvenanceRecord
ledger = ProvenanceLedger()
ledger.append(ProvenanceRecord("rec-0001", entity=claim_id,
                               activity="gradient_update", agent="gdprf-engine 2.1.0",
                               inputs={"prior": 0.68}, outputs={"posterior": 0.7696}))
assert ledger.verify_chain()
```

## Audit Retrieval

`ledger.lineage(entity)` returns the complete ordered trail for one claim or
proxy — sufficient to reconstruct *why the system believed what it believed* at
any point, which is what the Human Translation Layer renders for overseers.

See a live ledger: [`../examples/burnout-run-provenance.json`](../examples/burnout-run-provenance.json)
