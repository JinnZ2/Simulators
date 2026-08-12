# msiaf-gdprf-bridge

Expresses **MSIAF systemic incident investigations** as **GDPRF
gradient claims** — so a determination like *"the financial penalty
structure (D4) forced a rigid dispatch schedule (D2) onto a driver in
poor physiological state (D1)"* stops being a confident narrative and
becomes a chain of claims, each with calibrated confidence, proxy
fidelity, provenance, and explicit unknown-variable risk.

`PACKAGE_README.md` is the upstream introduction. This file covers
repo positioning and the worked result.

## The load-bearing insight

MSIAF's power is refusing the single-cause story. GDPRF's power is
refusing the unearned-confidence story. Together: a systemic
determination that knows *how sure it is*, knows *what it doesn't
know*, escalates when it is **confident AND ignorant**, and leaves a
tamper-evident trail from raw evidence to final determination.

## The worked result

`python3 src/run_reefer_case.py` runs the reefer run-off-road incident
end to end. Output (reproduced in `outputs/`):

```
[L1] D4 -> D2                       posterior=0.744 (cascade f=0.837, gate=not_triggered)
[L2] D2 -> D1                       posterior=0.590 (cascade f=0.348, gate=not_triggered)
[L3] D3 hazard + D2 stale feed      posterior=0.751 (cascade f=0.819, gate=not_triggered)
[L4] D1 micro-delay at the moment   posterior=0.611 (cascade f=0.500, gate=failed)

SYSTEMIC DETERMINATION
  chain (conjunctive) confidence : 0.202
  weakest-link bound             : 0.590
  bound divergence               : 0.389 (RESIDUAL TRIGGER)
  max unknown-variable risk      : 0.500

DECISION POINT: ESCALATE
  residual variance trigger with unpassed identification gate;
  human must adjudicate unexplained ignorance

Provenance ledger: 24 records, chain valid: True
```

Read what that actually says. Every individual link is *more likely
than not* (0.59 to 0.75). The conjunctive chain is **0.202**. A
four-link systemic story where each link is plausible is not itself
plausible — and the 0.389 divergence between the conjunctive product
and the weakest-link bound is what fires the residual trigger.

The system does not conclude "systemic failure." It concludes
**ESCALATE** — confident enough to be worth a human's time, ignorant
enough that no machine should close the file. That is the whole
argument of the bridge in one output.

## The mapping

| MSIAF | GDPRF | Why they fit |
|---|---|---|
| Dimensional friction claim (D4→D2) | Claim object, scoped to the incident | Each cascade link is assertable, contestable, measurable-in-principle |
| Investigation evidence (ELD logs, dispatch messages, soil compaction) | Proxy nodes with metrology | Evidence is an *instrument* with precision and bias — not a fact |
| Systemic Interconnection Pathway | Causal edge chain in the VKG | Fidelity decays along the cascade; a 4-link chain cannot be as confident as its best link |
| Post-Incident Investigation Checklist | Proxy discovery + calibration protocol | The 4 phases are a structured way to assign fidelity gradients |
| Final determination | Decision point over aggregated posteriors | DEPLOY / ESCALATE / HOLD, with confident-and-ignorant escalation |
| Investigator's report | Provenance ledger + Human Translation Layer | Hash-chained trail: why the system believes what it believes |

## What runs

```bash
python3 src/run_reefer_case.py   # full worked investigation
python3 -m pytest tests/ -q      # 7 tests
```

Verified on landing: **7/7 green**, worked case runs clean, hash chain
validates (24 records).

## Dependency note

This folder imports the GDPRF reference engine from
`../gdprf-framework/src`. Both folders are landed as **siblings at the
repo root**, so the relative import resolves as-is — verified after
landing. `GDPRF_SRC` overrides the path if you relocate either one.

This is the only cross-folder Python import in the repo. It is
deliberate: the bridge is not a copy of GDPRF, it is a consumer of it,
and duplicating the engine would let the two drift.

## Layout

| Path | What |
|---|---|
| `docs/mapping.md` | The conceptual bridge, in detail |
| `cases/reefer-trucking.case.json` | The incident as claims, proxies, and edges |
| `src/bridge.py` | MSIAF→GDPRF translation + systemic aggregation |
| `src/run_reefer_case.py` | End-to-end investigation run |
| `outputs/reefer-investigation-report.md` | Human-readable determination |
| `outputs/reefer-provenance-ledger.json` | Hash-chained audit trail (24 records) |

The shipped `outputs/` are checked in as delivered. Re-running
regenerates them with fresh timestamps and a correspondingly
different hash chain — everything else is deterministic.

## Repo positioning

Stdlib-only. No `CLAIMS.md`, but the worked case is claim-shaped: four
labelled links with posteriors, an aggregation rule, and a decision
that follows from stated thresholds. Change a proxy's fidelity in
`cases/reefer-trucking.case.json` and the determination moves.

## Cross-repo resonances

- **`divergence-playground/`** — hash-sealed readings that cannot be
  revised after commitment. Same tamper-evidence discipline; here the
  sealed object is a belief-update ledger rather than a reader's
  verdict.
- **`incentive-blindspot-sim/`** — models how incentive structure
  gates visibility *multiplicatively*. The bridge's conjunctive
  collapse (four ~0.65 links → 0.202) is the same multiplicative
  logic applied to evidential confidence instead of visibility.
- **`grounding-layers/`** — bounded-by-every-layer-below. The
  weakest-link bound (0.590) is exactly that, and the gap between it
  and the conjunctive product is treated as information, not noise.

## The family

```
msiaf-framework/            the D1-D4 incident frame (the source claims)
gdprf-framework/            the gradient reasoning engine (the consumer)
msiaf-gdprf-bridge/         ← you are here: the wiring, plus a worked case
proxy-investigation-lab/    grades the proxies this bridge relies on
instrument-epistemology/    the same method turned on scientific instruments
```

## Provenance

Source drop: **OKComputer_Create_Another_Repo** (`a21bf9b3-...zip`).
Files byte-identical to the drop apart from the upstream `README.md`
→ `PACKAGE_README.md` rename.

CC0.
