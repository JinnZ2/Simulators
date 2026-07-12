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
- `grounding-layers/` — Seven-layer probabilistic grounding stack
  (L0-L5 + Lε) built around one argument: **any layer above L0 is
  bounded by every layer below it**, extended by SCOPE-annotated
  category-error guards that refuse to score claims outside a
  layer's ontology.

  **Entry point for any AI**: [`entry.py`](grounding-layers/entry.py)
  exposes a single `audit(claim_or_plan, ontological_scope)` call
  that accepts either a natural-language string or a structured plan
  dict and returns the full seven-layer result. See
  [`USAGE.md`](grounding-layers/USAGE.md) for the read-first guide.

  Seven deterministic + seven probabilistic layer inspectors:
  `l0_physics_causality` (+`ProbabilisticWorld`),
  `l1_thermodynamics_entropy` / `l1_thermodynamics`
  (+`ProbabilisticThermodynamicsWorld`),
  `l2_planetary_mass_balance` / `l2_planetary`
  (+`ProbabilisticPlanetaryWorld`),
  `l3_ecological_homeostasis` / `l3_ecology`
  (+`ProbabilisticEcologicalWorld`),
  `l4_biomechanical_sensorimotor` / `l4_human`
  (+`ProbabilisticHumanWorld` with category-error guard for
  non-human ontological scopes),
  `l5_human_construct` / `l5_core` (+`l5_probabilistic_inspector`
  with pluralistic frames + category-error guard),
  `l_epsilon_epistemic` / `l_epsilon_epistemic_v2`
  (+`l_epsilon_probabilistic_inspector` with two-axis
  category-error guard).

  Meta files: [`SCOPE_TAXONOMY.md`](grounding-layers/SCOPE_TAXONOMY.md)
  (four-dimension T | S | O | C vocabulary),
  [`CLAIMS.md`](grounding-layers/CLAIMS.md) (73 falsifiable claims,
  all with SCOPE annotations, REFUTATION_PROTOCOL, category
  taxonomy), [`LOG.md`](grounding-layers/LOG.md) (design record,
  read bottom-up), [`USAGE.md`](grounding-layers/USAGE.md)
  (AI-facing usage guide).

  Three related simulators sit alongside the L-stack:
  `temporal_dysrhythmia` (six timescales from μs to
  millennia, translator-switch coupling), `tensor_field_resilience_v1`
  (F/A/T/M institutional-governance vectors), and
  `tensor_field_resilience_v2` (v1 + G/W/Y anchors, unstable vs
  resilient scenarios). Also `inverse_knowledge_tree.py`: verification
  by demonstrated lineage (peer to the L-stack, not a member of it),
  and `scope_profile.py`: six-factor scope matrix for human-embodied
  claims. Sourced from `JinnZ2/Resilient-AI-Human-Collaboration-` and
  archived at `legacy/Organize3.md`; non-stdlib is `numpy`,
  `matplotlib`, `scipy`. 430+ audit-grade tests green.
- `earth_economics/` — Coupled physics–economics–accountability
  simulator. `earth_economic_sim.py` runs a unified loop
  (EarthSystemsInterface → EconomicModel → ThermodynamicAuditor).
  `asteroid_mining_audit.py` runs a thermodynamic + atomic-balance
  audit on platinum extraction; `fermi_paradox_audit.py` audits
  civilization models. `equations.yaml` catalogues Regenerative
  Index / VFD / SCI / OCDI / RPI. `scenarios/` carries nine
  comparative-economics profiles (Ainu, Sámi, Aboriginal Australia,
  Ubuntu, Potlatch, open-source gift, Arabic trust-based trade,
  USSR 1985, US 2026) plus a `results.md` and a shared
  `system_profile.py` dataclass. No CLAIMS.md or REFUTATION_PROTOCOL
  yet.
- `model-ecology/` — "Which model predicts best?" vs "what is the
  domain of validity of this framework?" — the repo only answers the
  second. Fifteen real rolling estimators across four families
  (spectral / geometric / probabilistic / statistical), each with
  declared assumptions and limitations, none carrying a planted
  family signal. `phylogeny.py` computes `N_phylo` vs `N_empirical`
  (participation ratio of the correlation spectrum) with a
  permutation null on family labels; `disagreement.py` splits
  outliers into consensus / structured / isolated regimes plus a
  prophet / crank / conformist / workhorse census;
  `confound_sweep.py` separates apparatus floor / autocorrelation /
  real structure / window / preprocessing (the window is the
  largest and most invisible confound); `meta_engine.py` runs
  observer + representation invariance sweeps with `manifold`
  registered as one representation among five, no special standing.
  `demo.py` reproduces every CLAIM_TABLE headline (P1 REFUTED,
  N_eff = 2.48, D1 REFUTED, D2 prophets recur, manifold does NOT
  support in 11/12 seeds).
- `fragility-cascade/` — Physics-grounded audit of value substrates
  from a barrel you can hold to a resource-backed token you can
  only be promised. Five running sims: `substrate_spectrum.py`
  (Monetary Durability Index across seven substrates, ~7 orders of
  magnitude ground→cloud), `redemption_entropy.py` (independence
  `(1-p)^L` marketing model vs common-mode correlation physics;
  reproduces ~0.81 compute, ~0.60 AI field numbers),
  `product_multiplicity.py` (oil-like 1/√N CoV collapse vs
  compute-like flat CoV), `attack_tree.py` (fractal attack surface,
  25 leaves, super-linear growth 1→1093 through depth 6), and
  `cascade_redesign_vulnerability.py` (T_crit = W + A; system T_crit
  = 9 months at settlement layer; substrate exposure invariant
  under AI speed, dE/dT = 0 — The Decoupling Result).
  `THE_FRAGILITY_CASCADE.md` carries the canonical prose plus the
  Stewardship Paradox and AI-governor addenda; `CLAIM_TABLE.md`
  pins 8 substrate claims + 4 redesign-cascade claims.
- `exploration-playground/` — Single-file three-loop discovery
  engine over a Region/Interface/Environment substrate. No failure
  node; three verdicts (SUPPORTED / CONTRADICTED / UNEXPLAINED).
  Score = interestingness (reproducibility × surprise ×
  verdict_weight × question_richness), with UNEXPLAINED weighted 2.0
  and SUPPORTED 0.3 — the loop hunts for surprises, not
  correctness. Every UNEXPLAINED verdict spawns a next-experiment
  question (bisect the delta, trace the pathway).
- `voice-attractor-probe/` — Companion to `exploration-playground/`
  with the same three-loop skeleton but the substrate is LLM output.
  Two layers: modality pull (does the model drift to voice on
  modality-neutral tasks?) and design attractors (which trade-offs
  recur under prompt jitter that shouldn't matter?). Verdicts:
  STABLE_ATTRACTOR / PERTURBATION_SENSITIVE / UNEXPLAINED. Control
  probes ("loud", "nonverbal", "no network") should move the basin;
  if they don't, the model isn't reading hard constraints. Pluggable
  model adapter — ships with a stub so the pipeline runs offline;
  `landscape_summary()` archives one JSON per model version so
  attractor drift can be diffed across versions. Stacked companion
  modules `introspection_delta.py` (v1: one-shot self-model → Lε →
  static probe queue) and `introspection_delta_v2.py` (five run
  modes, interactive informed loop, Lε_spontaneous / Lε_informed
  fork, drift sensor for regenerated-vs-stored self-models,
  measured-cost thermal brake) turn Anthropic's introspection-
  adapter framing into a purely behavioral measurement — the harness
  distinguishes latent-but-verbalizable BLIND_SPOTs (gap > 0) from
  evidence-resistant CONFABULATIONs (informed Lε stays high) without
  activation access.
- `vector-field-explorer/` — Vector-substrate sim for
  superconductor-style measurement spaces. Channels held as
  vectors (2D magnitude+angle or 3D spherical), not scalars — the
  angle is the load-bearing quantity that scalar-projection
  instruments drop. Three coupling kinds (`mag_to_mag`,
  `mag_to_angle`, `angle_to_angle`) map field / strain / phase /
  anisotropy / gap dynamics. A `RelationalDetector` watches
  channel pairs across a sweep and flags PHASE_LOCK / DECOUPLE /
  SIGN_FLIP, gated by warm-up + prior-motion + magnitude-floor
  guards to keep two idle channels from being mis-labelled locked.
  Demo sweep of field magnitude fires 18 SIGN_FLIP events at
  two coherence-inversion parameter clusters; each event becomes a
  falsifiable CouplingClaim. SOFT coupling constants labeled
  PLACEHOLDER inline; swap for measured superconductor values
  before any real claim.
- `exploration-engine/` — Cross-domain chassis with the cascade-
  regime engine dropped in. Six-step architecture: typed `Domain`s
  (financial / material / social / informational / biological /
  regulatory), gradient-driven `Interface` exchange, bistable
  double-well internal dynamics from `sustained-activation-gate/`,
  a `HypothesisGenerator` that scores response nonlinearity as
  residual-from-line / spread and emits `Claim`s when it exceeds
  0.25, a `FalsificationEngine` that stresses hysteresis claims by
  reversing the drive, and an arbitrage flagger that fires only
  when observed gain clears a conversion-loss null floor. Live demo
  runs the over-legibility argument (regulatory pressure → parallel-
  economy lock) as a falsifiable experiment; sample run in this
  repo has Phase B refuting the framework's own headline claim
  (survival 0.50 and 0.00) — the refutation protocol on its own
  argument.
- `sustained-activation-gate/` — Bistable hysteresis module for the
  cascade-regime family. Tilted quartic double-well with Kramers-
  escape noise; three exploration surfaces plus a frontier stub.
  FIRM (physics) and SOFT (biology interpretation) layers
  deliberately separated: the C1→vlPAG stress-circuit labels are
  held in a swappable `INTERPRETATION` dict tagged "ANALOGY_GRADE"
  (one paper, mouse, small-n); the physics claims stand regardless.
  Header carries explicit reliability tiers — `compare_programs()`
  is Tier 1 (four structural claims earned from dynamics),
  `explore_separability()` is Tier 2 (clean θ ≈ 0.0052 boundary),
  `explore_theta_vs_persistence()` is Tier 3 (instructive negative:
  θ flat because baseline collapses faster than the lock persists),
  and `explore_theta_vs_restore()` (the axis Tier 3 relocated) now
  built and pinned: θ rises 23.9× as restore grows 40× — the
  "spares baseline" claim is possible on either side of the
  restoration-vs-coupling trade-off. The soft biology label is a
  registry of three substrates (C1→vlPAG, AMOC overturning, grid
  load blackout) — swap `SELECTED_INTERPRETATION` and the module
  runs unchanged. Ships with README.md + CLAIM_TABLE.md (11
  refutable claims across five groups).
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
