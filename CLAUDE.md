# Simulators

Repository for different simulations and supporting tooling.

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
  otherwise.
- Notes files (`NOTES.md`) preserve design thinking as written so the
  reasoning is traceable; implementation files keep to what the notes
  specify.
- Each simulator subfolder is intended to be promotable to its own repo
  later (e.g. `emergence-stability-simulator` is sketched as a standalone
  CC0 repo in its notes).
