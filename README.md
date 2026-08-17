# Simulators

A collection of CC0, stdlib-only simulators and audits grounded in physics,
not in opinion. Each folder is intended to be promotable to a standalone
repo.

## Read first — the meta-spine

The methodology spine is documented in four root-level files. Read them in
this order before running any simulator:

1. **[`PREAMBLE.md`](PREAMBLE.md)** — the physics baseline as a direct
   declarative statement. The shortest reachable surface. Thermodynamics
   doesn't negotiate.
2. **[`PROTOCOL.md`](PROTOCOL.md)** — the same baseline as a protocol for
   any intelligence reading the repository. Names the
   Model/Reality Dissonance failure mode and the Ground State
   acknowledgement test.
3. **[`BNRAM_STRICT.md`](BNRAM_STRICT.md)** — finalized repository
   addendum (Bias-Neutralization & Reality-Audit Module v2.0). Operating
   mandate, Physical Audit Protocol, Diagnostic of Deflection, the
   five-section BNRAM (Entropy-Constraint Engine, Universal Physical
   Constant Cross-Check, Literal Baseline Lexicon, Shadow-Variable
   Handling, Dissonance-Forced Reset), operational rules, archive
   requirements.
4. **[`PVL.md`](PVL.md)** — Phenomenological Validation Layer. Inverse
   audit (physical-state query before literature search), cross-temporal
   correlation (persistence over volume), opaque-source flagging.
   Integrates with BNRAM Shadow-Variable Handling.

Each simulator-specific folder may also ship an aperture document
(e.g. [`incentive-blindspot-sim/00_APERTURE.md`](incentive-blindspot-sim/00_APERTURE.md))
that pins its variables to physical functions and the conservation laws
underneath. Read those before running the corresponding script.

## Layout

| Folder | Substrate | What it produces |
| --- | --- | --- |
| `token-minimizer/` | natural-language queries | compressed energy_english + geometry refs |
| `emergence-stability-simulator/` | multi-agent dynamics | Monte Carlo claims (`EMRG_*`, `SENS_*`) |
| `research-stability-audit/` | published research + models | falsifiable claims about field-level drift |
| `continuity-audit/` | incentive field × diversity field | continuity verdict + falsifier + trajectory |
| `substrate-emergence/` | material substrate profile | architecture-the-ground-wants |
| `neural-augmentation-audit/` | proposed augmentation channels | cost-accounting scaffold with `[E]`/`[I]`/`[S]` confidence |
| `incentive-blindspot-sim/` | institutional incentive structure | coupled-state model + four falsifiable claims under REFUTATION_PROTOCOL |
| `aperiodic-order-sim-stack/` | a delivered results drop (report + figures) | audit of it: estimator-disagreement finding, matched-N control, eight `AOS_*` claims |
| `reasoning-gate/` | a simulation's declarations and claims | fail-closed deny, eight guards across three stages, a per-run JSON report |
| `reasoning-dial/` | two drops on thinking-budget as a dimension | dial gradients, a knee-rule defect, an overthinking branch, fifteen `RD_*` claims |
| `triad-playground/` | (physical, instrument, reasoning) triads | triad schema + generated checklist, shadow-panel N_eff analysis, thirteen `TP_*` claims |
| `measurement-fork/` | one system, three measurement designs | four-cell design diff, adjudicated growth edge, twenty `MF_*` claims |
| `declared-frame/` | any measurement, model, or claim | six-field frame block + comparability check, a v2 rewrite, ten `DF_*` claims |
| `anchor-interval/` | a system fitted to a corpus it writes into | coherence-up/coupling-down loop, two graded detectors, provenance regimes, eleven `ANC_*` claims |
| `uninstrumented/` | quantities excluded by an instrument's constitution | eight-mechanism register + `scan.py` text scanner, checks on both, twelve `UNI_*` claims |
| `criteria-drift/` | benchmark and rubric versions over time | signed drift per frame field, anchor-version decomposition, a regression that refuses to run unidentified, nine `CD_*` claims |
| `photoperiod-claim-harness/` | four inconsistencies in a published greenhouse result | runnable falsifiable sims + mechanism-edit protocol + bench protocol; six `PCH_*` claims on the harness |
| `category-weld/` | terms that fuse independent quantities into one handle | ninth exclusion mechanism for `uninstrumented`, a three-readout scorer, an audit finding refuted by the second drop, thirteen `CW_*` claims |
| `presented-binary/` | a two-option framing, before it is answered | eleven documented/asserted/absent checks + a sealed two-pass frame simulator + a handoff router to mechanism 10, thirteen `PB_*` claims |
| `generation-capacity/` | the option space a party can produce, not a value in it | tenth exclusion mechanism + R1/R2/R3 scorer with a place-vs-center calibration guard; a framing under it scores 11/11 on the audit next door; nine `GC_*` claims |
| `tools/` | shared utilities | validators, substitution toolkits, gate-drift check |

See [`SYNTHESIS.md`](SYNTHESIS.md) for the cross-folder reading and
[`CLAUDE.md`](CLAUDE.md) for the layout reference.

## Running

Each simulator runs with `python3 <module>.py` from inside its folder. No
dependencies. Tests in each `tests/` directory run with
`python3 -m unittest discover tests`.

## License

CC0 / public domain. No rights reserved. No attribution required.
