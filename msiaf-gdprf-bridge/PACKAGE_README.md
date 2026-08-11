# MSIAF × GDPRF Bridge

Expresses **MSIAF systemic incident investigations** as **GDPRF gradient claims** —
so a determination like *"the financial penalty structure (D4) forced a rigid
dispatch schedule (D2) onto a driver in poor physiological state (D1)"* stops being
a confident narrative and becomes a chain of claims, each with calibrated
confidence, proxy fidelity, provenance, and an explicit unknown-variable risk.

## The Philosophical Mapping

| MSIAF | GDPRF | Why they fit |
|---|---|---|
| Dimensional friction claim (D4→D2 etc.) | Claim object, scoped to the incident | Each link in the cascade is assertable, contestable, measurable-in-principle |
| Investigation evidence (ELD logs, dispatch messages, soil compaction tests) | Proxy nodes with metrology | Evidence is an *instrument* with precision, bias, and noise — not a fact |
| Systemic Interconnection Pathway | Causal edge chain in the VKG | Fidelity decays along the cascade — a 4-link chain cannot be as confident as its best link |
| Post-Incident Investigation Checklist | Proxy discovery + calibration protocol | The 4 phases are a structured way to assign fidelity gradients |
| Final determination ("systemic failure, not driver error") | Decision point over aggregated posteriors | DEPLOY / ESCALATE / HOLD — with confident-and-ignorant escalation |
| Investigator's report | Provenance ledger + Human Translation Layer | Hash-chained audit trail: why the system believes what it believes |

## Quickstart

```bash
python3 src/run_reefer_case.py      # full worked investigation
python3 -m pytest tests/ -q         # test suite
```

## Contents

- [`docs/mapping.md`](docs/mapping.md) — the conceptual bridge, in detail
- [`cases/reefer-trucking.case.json`](cases/reefer-trucking.case.json) — the reefer
  run-off-road incident expressed as claims, proxies, and edges
- [`src/bridge.py`](src/bridge.py) — MSIAF→GDPRF translation + systemic aggregation
- [`src/run_reefer_case.py`](src/run_reefer_case.py) — end-to-end investigation run
- [`outputs/`](outputs/) — investigation report + provenance ledger from the run

## Dependencies

Imports the GDPRF reference engine from `../gdprf-framework/src` (v2.1). Run from
a directory layout where both repos are siblings, or set `GDPRF_SRC`.

## The Load-Bearing Insight

MSIAF's power is refusing the single-cause story. GDPRF's power is refusing the
unearned-confidence story. Together: a systemic determination that knows *how sure
it is*, knows *what it doesn't know*, escalates when it's confident AND ignorant,
and leaves a tamper-evident trail from raw evidence to final determination.
