# Proxy Investigation Lab

An experimental workbench for **exploring and investigating any proxy** — taking a
candidate proxy from a catalog (MSIAF proxy catalog, GDPRF knowledge graph, or a
brand-new candidate), running it through the scientific method, and grounding out
as much as can possibly be grounded: its causal chain, its instrument properties,
its validity threats, and its empirically measured fidelity.

> A proxy is not a fact about the world. It is an *instrument* with a claimed
> target. This lab exists to test that claim as hard as we can.

## What an Investigation Covers (the "as much ground as possible" checklist)

1. **Decomposition** — what exactly is the target variable? What is actually being
   observed? What is the claimed mapping?
2. **Grounding chain** — the physical/causal links from observable to target;
   where are the weak links, alternative causes, and feedback loops?
3. **Instrument characterization** — precision, noise floor, systematic bias,
   and the *provenance* of each (measured / estimated / assumed)
4. **Validity threats** — construct redefinition (Seltzer 2021), Goodhart
   pressure, confounders, selection effects, cascade-depth decay
5. **Synthetic ground-truth experiments** — generate a world where the truth is
   *known*, then check whether the lab recovers the instrument's properties and
   whether calibration actually fixes overconfidence
6. **Calibration** — fit isotonic / Platt scaling against held-out verified
   outcomes; report ECE before and after
7. **Coverage tracking** — which dimensions of the proxy are grounded vs. still
   assumed; the coverage report is part of the deliverable

## Repo Layout

```
docs/
  investigation-protocol.md    ← the 7-phase scientific protocol for any proxy
  grounding-taxonomy.md        ← types of grounding and evidence strength
schemas/
  investigation.schema.json    ← a full proxy investigation record
  experiment.schema.json       ← a single experiment record
src/proxy_lab/
  decompose.py                 ← claim/target decomposition structures
  grounding.py                 ← causal-chain model, weak-link analysis
  instruments.py               ← instrument model (precision/noise/bias/provenance)
  synthetic.py                 ← synthetic ground-truth world generator
  calibration.py               ← isotonic + Platt calibration, ECE
  coverage.py                  ← grounding coverage report
experiments/
  burnout_latency/             ← worked: Slack latency as burnout proxy
  port_dwell_time/             ← worked: drayage dwell time as congestion proxy
  wim_pavement/                ← worked: WIM axle sensor as pavement-fatigue proxy (G1-grade)
  goodhart_redteam/            ← gaming simulation: proxy fidelity collapse under decision use
  catalog_batch/               ← batch grades the whole MSIAF proxy catalog
outputs/                       ← investigation reports from runs
tests/
```

## Quickstart

```bash
python3 experiments/burnout_latency/run.py
python3 experiments/port_dwell_time/run.py
python3 experiments/wim_pavement/run.py
python3 experiments/goodhart_redteam/run.py
python3 experiments/catalog_batch/run.py     # comparative grounding report for all catalog proxies
python3 -m pytest tests/ -q
```

## Design Stance

- **Known-truth first.** Before trusting a proxy in the wild, test it in a
  synthetic world where the target variable is *known*. If the pipeline can't
  recover a known instrument, it has no business grading an unknown one.
- **Grounding is graded, not binary.** Every aspect of the proxy ends up
  `measured`, `estimated`, or `assumed` — and the coverage report says which.
- **Goodhart is a first-class threat.** Once a proxy is used for decisions, it
  stops measuring and starts being gamed. The protocol requires a Goodhart
  assessment for every proxy intended for decision use.

## Lineage

Built as the experimental arm of the GDPRF (`gdprf-framework`) and the
MSIAF×GDPRF bridge (`msiaf-gdprf-bridge`): the lab *produces* the calibrated,
provenanced proxy objects those systems *consume*.
