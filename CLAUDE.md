# Simulators

Repository for different simulations and supporting tooling.

## Meta-spine (read first)

The methodology spine sits in four root-level files. Every simulator
in the repo rests on it. Read in order:

- `PREAMBLE.md` — physics baseline as a direct declarative statement.
  "Thermodynamics doesn't negotiate."
- `PROTOCOL.md` — the same baseline as a formal protocol for any
  intelligence reading the repo. Names the Model/Reality Dissonance
  failure mode and the Ground State acknowledgement test.
- `BNRAM_STRICT.md` — finalized repository addendum
  (Bias-Neutralization & Reality-Audit Module v2.0). Operating mandate,
  Physical Audit Protocol, Diagnostic of Deflection, five-section
  BNRAM (Entropy-Constraint Engine, Universal Physical Constant
  Cross-Check, Literal Baseline Lexicon, Shadow-Variable Handling,
  Dissonance-Forced Reset), operational rules, archive requirements.
- `PVL.md` — Phenomenological Validation Layer. Inverse audit
  (physical-state query before literature search), cross-temporal
  correlation (persistence over documentation volume), opaque-source
  flagging. Integrates with BNRAM Shadow-Variable Handling.

Simulator-specific aperture documents live inside their folders
(e.g. `incentive-blindspot-sim/00_APERTURE.md` pins the six
state variables to physical functions and the conservation laws
underneath).

## Layout

- `token-minimizer/` — Token compression tool design notes and a working
  `compress.py` implementation (Python stdlib only). Built around the
  "energy_english" compressed query format, local geometry references, and
  output-side delta compression.
- `emergence-stability-simulator/` — Notes and specification for a Monte
  Carlo test of stable vs. parasitic agent dynamics in multi-model
  emergence. Hypotheses, parameters, metrics, outputs, and a target repo
  structure live here.
- `research-stability-audit/` — Falsifiable-claim framework for testing
  research stability and AI model degradation. Six preset claims with
  measurement methods, thresholds, and cross-references to the
  emergence simulator's agent-level claims (same physics, different
  scale).
- `continuity-audit/` — Field-level audit. Models incentive structure
  as a field acting on a Hill-number diversity field, propagates a
  replicator trajectory, reports a continuity verdict (`SUPPORTS_`,
  `DEGRADES_`, `INDETERMINATE`) plus the falsifier that would flip
  it. Anti-freeze: the verdict is always published alongside the
  full trajectory and an explicit "do not store" note. Stdlib only.
  `continuity_audit.py` is the field-level audit; the companion
  `interface_layer.py` produces the dynamic κ that the audit
  consumes — a translator that widens an agent's reachable-substrate
  band literally is κ dropping. Classification spine: `ENABLING`
  widens the band, `COERCIVE` narrows it.
- `substrate-emergence/` — Reads a material substrate as a profile of
  verb-first axes (`conducts`, `switches`, `dissipates`,
  `holds_heat`, `costs_extract`, `abounds`, `bears_load`, `couples`)
  and reports the architecture the ground wants. A deficit on one
  axis routes to a capability on another — `weak conduction → wide
  parallel paths`, `heat that will not leave → stored state`.
  Returns a relationship-trajectory, never a stored verdict. Two
  modules speaking a shared profile-dict contract:
  `substrate_emergence.py` (read the profile) and
  `site_substrate_map.py` (build a profile from a mix of real-site
  materials plus environment modifiers — wetness, thermal swing,
  energy flux). The two scripts share no imports; paste the profile
  across.
- `neural-augmentation-audit/` — Cost-accounting scaffold (CC0
  document, not code). Names seven constraint axes (metabolic,
  cortical territory, plasticity window, cross-modal reuse,
  attention/WM, inhibition, sleep/autonomic) and a cross-reference
  table mapping each proposed augmentation to what it borrows and
  the predicted deficit, with `[E]`/`[I]`/`[S]` confidence marks per
  cell. Methodology spine: "demote on contact with evidence; never
  modify the table to protect a prior."
- `incentive-blindspot-sim/` — Coupled difference-equation model of
  how an institution's incentive structure (credential closure +
  capital concentration + frame narrowness) gates external
  visibility multiplicatively, lets blind spots accumulate, and
  drives the system toward the failure mode it claims to prevent.
  Six coupled state variables, three scenarios
  (`credentialed_closed`, `distributed_open`,
  `closed_with_transparency`), four falsifiable claims
  (`CLAIM_BS_001..004`) under an explicit `REFUTATION_PROTOCOL`:
  weights are frozen estimates, the coupling topology is the claim,
  and a failed check updates the claim — not the weights.
- `antifungal-mechanism-sim/` — Three-module progression for
  exploring antifungal drug combinations, each opening an axis the
  previous one collapses.
  1. `antifungal_mechanism_sim.py` — interactive CLI over seven
     interaction categories (cell wall / ergosterol / membrane /
     protein / nucleic acid / stress response / quorum-biofilm)
     scored additively (Σ eff − Σ tox − Σ res), with genetic-style
     `crossover(a, b)` returning a random subset of `a ∪ b`.
  2. `antifungal_coupling_core.py` — same seven codes, coupling
     topology: signed pairwise `J[i, j]` (synergy/antagonism) plus
     resistance ∏ over orthogonal axes with same-axis min-not-product.
     Rank-flip claim: the additive scorer and the coupling scorer
     disagree on the SIGN of the best combination; the coupling
     answer (three orthogonal axes → p_res ≈ 0.08 on
     echinocandin+5FC+Hsp90) matches clinical practice.
  3. `temporal_dosing_resistance.py` — adds the time axis (populations
     + genotypes as a kicked relaxor under a dosing schedule) and
     surfaces sequence-dependent kill: `J[i → j] ≠ J[j → i]`, the
     interaction matrix is non-commutative. Empirical: simultaneous
     suppresses ~140× harder than sequential-mono; polyene→azole
     kills ~60% more than azole→polyene.
- `AMOC/` — REGIME_SHIFT trajectory framework for asking what a
  specific patch of ground does when Atlantic overturning flips.
  Seven modules (`forcing.py`, `baseline.py`, `divergence.py`,
  `sitespec.py`, `response.py`, `trajectory.py`, plus the worked
  `carlton_county.py` slice). Two forcing instruments (`StommelBox`,
  `KramersWell`) sweep a freshwater-loading control parameter and
  surface the spinodal; paleo analogs (Younger Dryas, 8.2ka,
  Heinrich 1) supply patterns; `divergence.py` strips analog terms
  that needed continental ice / meltwater buffer / permafrost cycle
  and discounts recovery because present loading is ocean-sourced
  and not finite. Honest-gap protocol: missing site data stays
  `None`, response bands widen and tag the gap, never silently
  fill with false precision. Four claims (`RGS_001..004`) follow
  the REFUTATION_PROTOCOL pattern.
- `play-sims/` — Exploratory sandbox and the repo's explicit exception
  to stdlib-only. Seventeen visualisation-first simulations across five
  domains: `plasma-waves/` (4 — 1D/2D FDTD, wave→dust heating, 2D PIC),
  `atmospheric-heating/` (6 — meteor ablation → cascade → oblique EM
  → GCM+acoustic dashboard → flare/radio/climate ultimate),
  `sponge-reef/` (3 — basic → light+temp+herbivory → seasons+larvae),
  `exoplanet-forensics/` (3 — multi-framework, data archaeology,
  population synthesis), `photon-upconversion/` (1 — TTA-PUC + solar
  boost). Extracted verbatim from archived source drops under
  `legacy/` (`Organize.md`, `Organize2.md`); each `.py` file's
  docstring names its `legacy/OrganizeN.md` source and the line range
  it came from. Non-stdlib: `numpy`, `matplotlib`, `scipy`, `sklearn`,
  `ipywidgets`, `ipython` (per-folder `requirements.txt`). No claim
  tables, no `REFUTATION_PROTOCOL` — the audit convention does not
  apply here. Read them as sketches.
- `legacy/` — Archived source drops. The repo root reserves one
  filename — `Organize.md` — as the intake slot for a bulk
  collaborative code drop. After extraction into `play-sims/` (or
  wherever), `git mv Organize.md legacy/OrganizeN.md` moves the drop
  to the archive with the next unused round number, keeping the root
  clear for the next drop. See [`legacy/README.md`](legacy/README.md)
  for the full ingestion protocol.
- `tools/` — Shared utilities.
  - `validate_claim_table.py` — lightweight schema validator for
    any `CLAIM_TABLE.json` produced in the repo; accepts both the
    `statement`/`status` and `hypothesis`/`is_falsified` flavours.
  - `substrate_substitution.py` — lightweight CLI that walks a
    CLAIM_TABLE and prints the grass/grasshopper substitution next
    to each claim. Structural enforcement for narrative-instinct
    bias.
  - `substrate_substitution_toolkit.py` — richer programmatic
    surface: seven categories from harsh (`pure_consumer`, the null
    hypothesis) to gentle (`mutualistic_scale`), each with multiple
    ecological pairs and a balanced-view walkthrough.
- `SYNTHESIS.md` — Top-level synthesis describing how the three folders
  fit together, how claims flow between them, and how to read the
  artifacts in order.
- `CASE_STUDY_NARRATIVE_INSTINCT.md` — Empirical record of a multi-
  round correction sequence in which the AI repeatedly inverted the
  framing of scale_builder / narrative claims and the user repeatedly
  caught it. Documents the substitution-test methodology and serves
  as evidence for EMRG_009 (a narrative-only system cannot
  self-correct narrative-instinct from inside its own scope).
- Each simulator subfolder ships a `samples/` directory with one
  small representative output (CLAIM_TABLE, ASCII report, geometry
  file). Samples are checked in so the corpus is browsable on GitHub
  without running anything.

## Working branch

Active development happens on `claude/token-minimizer-emergence-sim-T4pjn`.
All changes for the token minimizer + emergence simulator scaffolding land
on that branch.

## Conventions

- Python files target the standard library only unless a note says
  otherwise. **Exception**: `play-sims/` uses `numpy`/`matplotlib`/
  `scipy`/`ipywidgets` and is exempt from this rule.
- Notes files (`NOTES.md`) preserve design thinking as written so the
  reasoning is traceable; implementation files keep to what the notes
  specify.
- Each simulator subfolder is intended to be promotable to its own repo
  later (e.g. `emergence-stability-simulator` is sketched as a standalone
  CC0 repo in its notes).
