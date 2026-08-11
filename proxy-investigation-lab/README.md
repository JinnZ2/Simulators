# proxy-investigation-lab

Experimental workbench for taking any candidate proxy — from the MSIAF
catalog, a GDPRF knowledge graph, or nowhere at all — and grounding
out as much of it as can possibly be grounded: causal chain,
instrument properties, validity threats, empirically measured
fidelity.

> A proxy is not a fact about the world. It is an *instrument* with a
> claimed target. This lab exists to test that claim as hard as we can.

`PACKAGE_README.md` is the upstream introduction. This file covers
repo positioning and the headline results.

## Headline result 1 — the catalog graded

`experiments/catalog_batch/run.py` grades every proxy in the MSIAF
catalog. From `outputs/catalog-coverage-report.md`, top and bottom:

| Rank | Proxy | Chain fidelity | Grounded | Weakest link | Verdict |
|---|---|---|---|---|---|
| 1 | river-water-level | 0.931 | 1.00 | level→clearance | well grounded |
| 2 | river-draft-limits | 0.874 | 1.00 | depth→limit | well grounded |
| 3 | freight-corridor-volume | 0.810 | 1.00 | volume→axle spectrum | well grounded |
| … | … | … | … | … | … |
| 14 | wh-temp-turnover | 0.297 | 0.50 | hazard→quit intent | partially grounded |
| 15 | behavior-venue-congestion | 0.385 | 0.25 | purpose→timing | mostly assumed |
| 16 | drone-corridor-density | 0.480 | 0.25 | density→conflict | mostly assumed |

Chain fidelity is **multiplicative** — one assumed 0.55 link caps the
whole proxy no matter how good the sensor is. The report ends with a
priority queue: the bottom-of-table proxies are exactly the ones
*used* in MSIAF reasoning while resting on assumed links.

## Headline result 2 — Goodhart is measured, not asserted

`experiments/goodhart_redteam/run.py` simulates 3000 agents over 12
periods who adapt the *observable* once the proxy becomes a decision
target. From `outputs/goodhart-redteam.experiment.json`:

```
baseline_correlation : 0.904
gamed_correlation    : 0.713
fidelity_collapse    : 0.191
```

Plus a **detection surface**: gaming flattens the observed-vs-latent
slope at the top of the distribution (0.633 top-vs-bottom) and
inflates top-decile variance. That is an actionable audit
instruction — audit the top decile first — rather than a warning that
Goodhart exists.

## The seven-phase protocol

1. **Decomposition** — what exactly is the target? What is actually
   observed? What is the claimed mapping?
2. **Grounding chain** — physical/causal links; weak links,
   alternative causes, feedback loops
3. **Instrument characterization** — precision, noise floor,
   systematic bias, and the *provenance* of each
   (measured / estimated / assumed)
4. **Validity threats** — construct redefinition, Goodhart pressure,
   confounders, selection effects, cascade-depth decay
5. **Synthetic ground-truth experiments** — build a world where truth
   is *known*, check the lab recovers the instrument's properties
6. **Calibration** — isotonic / Platt against held-out outcomes,
   report ECE before and after
7. **Coverage tracking** — which dimensions are grounded vs. still
   assumed; the coverage report is part of the deliverable

## What runs

```bash
python3 experiments/burnout_latency/run.py   # Slack latency as burnout proxy
python3 experiments/port_dwell_time/run.py   # drayage dwell as congestion proxy
python3 experiments/wim_pavement/run.py      # WIM axle sensor (G1-grade)
python3 experiments/goodhart_redteam/run.py  # gaming simulation
python3 experiments/catalog_batch/run.py     # grade the whole MSIAF catalog
python3 -m pytest tests/ -q                  # 13 tests
```

Verified on landing: **13/13 green, all 5 experiments run clean.**

## Design stance

- **Known-truth first.** Before trusting a proxy in the wild, test it
  in a synthetic world where the target is known. *If the pipeline
  can't recover a known instrument, it has no business grading an
  unknown one.*
- **Grounding is graded, not binary.** Every aspect ends up
  `measured`, `estimated`, or `assumed` — and the coverage report
  says which.
- **Goodhart is a first-class threat.** Once a proxy is used for
  decisions it stops measuring and starts being gamed. The protocol
  *requires* a Goodhart assessment for any decision-use proxy.

## Repo positioning

Stdlib-only. No `CLAIMS.md`, but the catalog coverage report is a
16-row ranked claim table with a stated grading rule
(measured = 1.0, estimated = 0.5, assumed = 0.0, multiplied along the
chain) — reproducible and falsifiable by re-running with different
link gradings.

## Cross-repo resonances

- **`null-harness/`** — the closest sibling in the repo. That folder
  refuses to trust a *gate* until it beats a known-null and a
  known-signal; this folder refuses to trust a *proxy* until it
  survives a synthetic world where the target is known. Same
  "known-truth first" invariant, one level up the stack. The
  `archetype_library.py` hard gate (`ArchetypeGateNotRun`) and this
  lab's mandatory Phase 5 are the same enforcement move.
- **`rigidification-sensor/`** — measures reversibility rather than
  harm, because harm is the thing everyone already argues about. The
  Goodhart red-team's detection surface is that same instinct: don't
  measure whether gaming is bad, measure *where it shows up*.
- **`open-instrumentation-project/`** — every sensor ships with an
  explicit falsification condition. Same posture, different domain.
- **`equivalence-field/`** — pushes comparison down to INTENSIVE
  variables where extensive totals hide asymmetries. Chain fidelity
  being multiplicative is the same refusal to let a good aggregate
  hide a bad link.

## The family

```
msiaf-framework/            supplies the proxy catalog this lab grades
gdprf-framework/            consumes the calibrated proxies this lab produces
msiaf-gdprf-bridge/         wires the two together on a worked case
instrument-epistemology/    same method, applied to scientific instruments
proxy-investigation-lab/    ← you are here: the experimental arm
```

## Provenance

Source drop: **OKComputer_Create_Another_Repo** (`a21bf9b3-...zip`).
Files byte-identical to the drop apart from the upstream `README.md`
→ `PACKAGE_README.md` rename.

CC0.
