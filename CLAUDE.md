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
- `thermal-sensor-degradation-audit/` — Single-file, stdlib-only audit
  of what sustained heat does to the sensor package that is supposed
  to measure the heat. Seven lumped layers over one driver
  (temperature × time): material handbook table (CTE / service ceiling
  / creep onset), Stull wet-bulb, dark-surface solar amplification,
  differential-expansion microstrain across a bolted dissimilar-material
  pair, Arrhenius/Q10 gasket compression set, Arrhenius (Ea ≈ 0.7 eV)
  electronic drift, and a measurement-corruption signature. One
  `audit()` call rolls them into a worst-flag-wins `GREEN`/`YELLOW`/`RED`
  verdict. Headline claim (L7): `corruption(trend) =
  corruption(measurement) × corruption(framework)` — multiplicative;
  a package degrades *during* the extreme event it records, so the
  tail biases LOW (variance collapse + range clipping + step offset).
  Four claims (`TSD_001..004`) each ship the field experiment that
  refutes them; update the claim, never retune the sim. 23 tests green.
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
- `open-instrumentation-project/` — Single-file stdlib-only CLI for
  private institutional-health self-assessment. Five sensors
  (Epistemic Exit Velocity, Institutional Attachment Half-Life,
  Autodidact Vitality / Scientific Trust Inversion, Resilience
  Dependency Ratio, Open-Source Vitality resource-normalized), each
  with an explicit threshold and an explicit falsification
  condition. Ships with a persistent `claims.json` registry
  (five defaults) + a `manage_claims()` interactive menu; assessments
  write a timestamped JSON locally, nothing leaves the machine.
  Verb-speaking foundation stated in the README ("reality is
  verb-based; sensors measure flows, not states"). CC0. Full
  falsification log per sensor.
- `climate-modeling/` — Two-layer audit taxonomy for ecological /
  climate models. Level 1: simulation models (`models/grass.py`
  plain carbon balance, `models/cascade_grass.py` threshold + soil
  feedback + vulnerability memory as the "true system"). Level 2:
  sixteen failure-mode audits — six built, ten frontier stubs with
  build recipes (same pattern as `sustained-activation-gate/`'s
  frontier stub before it landed). The load-bearing target is
  **cascade-speed blindness**: smooth / memoryless / Gaussian-
  driven models systematically underestimate how fast collapse
  arrives. Built audits: `PhaseChangeAudit` (missing threshold),
  `StationarityAudit` (stationary-window params vs trending
  forcing), `MissingFeedbackAudit` (no soil-plant coupling),
  `OmittedVariableAudit` (hidden moisture), `DataAggregationAudit`
  (daily-mean fit bias), and the flagship `CascadeSpeedAudit`
  (threshold + feedback + memory + fat tails). `run_audits.py`
  emits a report card; sample run in this repo has 7 built → 7
  FAIL (every simplification detected, including the promoted
  `MissingPositiveFeedbackAudit` catching a CO2 amplifying loop)
  and 9 stub → 9 STUB (recipes staked). Ships with `ai_interface.py`
  (rule-based
  AIScientist that proposes structural patches; openai backend
  path stubbed), `meta_experiments.py` (patching loop), and
  `AUDIT_TAXONOMY.md` mapping each failure mode to
  fallacy / mathematical condition / real-world consequence.
  Non-stdlib (numpy + scipy required; sklearn + streamlit optional)
  — same exemption pattern as `play-sims/`.
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
- `equivalence-field/` — Two-file folder built on a
  falsification-as-pointer spine. `claim_lineage.py` treats a
  refuted claim as evidence the variable set was incomplete: the
  break points at a missing dimension, and `extend()` spawns a
  child (parent + exposed variable + a new independent falsifiable
  prediction) — with an epicycle guardrail that raises
  `EpicycleRejected` unless the new variable is both
  independently measurable and predicts beyond rescuing the
  parent. `equivalence_field.py` is the client: pushes comparison
  down the pyramid to INTENSIVE variables (densities, per-capita
  ratios, gradients) where extensive-total equivalence hides
  asymmetries. `gradient(A,B) = v(A) − v(B)` is odd under actor
  exchange; `oddness_audit(reading, A, B)` reports WHICH dimensions
  fail oddness under a given reading. `honest_reading` is odd by
  construction; `make_threat_reading()` returns `max(0, g)` per dim
  (the propaganda shape — scores a gradient as pressure only when
  it runs against the reader) and breaks on every non-zero dim.
  `seed_claims()` seeds E1/E2/E3 into a Lineage — the module's own
  claims held as first-class objects in the same spine. No
  verdicts, no moral labels, no intent — intensive measurements
  and potentials only.
- `rigidification-sensor/` — Trajectory spec + two live tells for
  detecting when a system's variance is being suppressed self-
  reinforcingly — reversibility loss, not outcome prediction. Spec
  sections: §0 branch selection (the prior, stated openly and open
  to attack), §1 invariant (variance suppressed faster than it
  regenerates; past threshold the suppression is cheaper to continue
  than to reverse — a rate crossing a line, substrate-independent),
  §2 three claims each with `falsifier_shape` specified and
  `falsifier_value: OPEN` (the honest hole is left for the next
  operator to measure), §3 tells that measure REVERSIBILITY not
  harm (first-order: counts of viable options actually in use;
  second-order: cost-of-reversal vs cost-of-continuation derivative
  — the §1 threshold being crossed live), §4 candidate control-
  parameter knobs for the credit–insurance node (hypotheses, not
  asserted), §5 handoff. Code: `harm.py` reads a signature on a
  coupled `System` of `Node`s (`draw`/`regen`) and `Coupling`s
  (`transfer`/`sensitivity`), returning `local`/`per_order`/
  `displaced`/`inflates`/`inflates_mode` — the `inflates` reading
  has four caller-selectable modes (`strict`,
  `multiplication_factor` = nuclear k / R0, `horizon_limited` =
  propagation constant within the medium, `peak_to_source` =
  amplifier gain) with no default, so the physics choice is
  named at every callsite. `simulator.py` makes it dynamical:
  displaced cost erodes the receiving node's regen, and `run(...)`
  records per-tick `dof`/`continuation`/`reversal`/`d_continuation`/
  `d_reversal` plus `locked_at` — the first tick where
  `reversal > continuation` AND `d_reversal > d_continuation`, the
  §1 threshold crossing. Names no actor, motive, or plan by
  construction; "control" throughout means control PARAMETER, not
  a hand on a knob.
- `claim-audits/` — Standalone single-file audits of external
  documents. Each audit hand-classifies every claim it addresses
  under one of eight verdict codes (`VERIFIED`, `SOUND`,
  `SIGN_BACKWARDS`, `UNGROUNDED_NUMBER`, `DIMENSIONALLY_VOID`,
  `GAMEABLE`, `IDENTITY`, `UNVERIFIED`) plus a per-claim `who`
  attribution (`K` = original author's move, `M` = model overlay)
  so the document's own moves are audited on their own terms
  instead of being conflated with what an LLM added on top.
  `GAMEABLE` and `SIGN_BACKWARDS` carry the most information —
  both name a mechanism that runs against the stated intent;
  `UNVERIFIED` is deliberately distinct from a negative verdict
  (it flags a gap, not a failure); `SOUND` and `VERIFIED` are
  separable (internal coherence vs external source checked).
  Each `Claim` carries `why` (the audit's reasoning) and `fix`
  (the smallest actionable repair). Every entry is hand-written;
  the module runs a printer over the list. Landed:
  `claim_audit_visibility.py` (14 claims V0-V13, 4 K-moves +
  10 M-overlay; headline V0: no null model anywhere — every
  threshold in the document is undecidable until each metric has
  a distribution under "nothing is happening") and
  `claim_audit_pasted_2026_08_05.py` (23 claims across 5 pasted
  pieces from other models; K/M split adapted to K=operational
  code, M=framing prose since everything model-authored; verdict
  4 REJECT / 1 SHIP — details in PROVENANCE F-10). Siblings named
  in the visibility-audit module docstring but not yet in the tree:
  `adversarial_corpus.py`, `claim_audit_spin.py`. CC0. stdlib
  only. Phone-buildable.
- `null-harness/` — Trust-calibration for gates: any callable
  `f(data) -> bool | str verdict` gets run over 1000 draws of a
  known-null (should not fire) and 1000 of a known-signal (must
  fire), reports FP + TP + minimum-detectable amplitude, and labels
  with a fail-condition classifier (`CONSTANT_FIRES`,
  `CONSTANT_SILENT`, `TOO_MANY_FALSE_ALARMS`, `NO_DISCRIMINATION`,
  `OK`). Four negative controls (`gen_white_noise`,
  `gen_wellposed_fisher`, `gen_null_residual`, `gen_smooth_surface`)
  paired with four positive controls that carry an amplitude knob
  (`gen_noise_with_z2_term`, `gen_degenerate_fisher`,
  `gen_true_pole`, `gen_scale_dependent_noise`); the harness sweeps
  the knob to find the smallest signal the gate can pick up. Single
  file, numpy + stdlib, CC0. Demo pins the pyramid of trust-tests:
  observation ≠ chance (`divergence-playground/null_ensemble.py`)
  → convergence ≠ shadow (`divergence-playground/coincidence.py`)
  → **gate ≠ constant** (this folder). First empirical result:
  `energy/modules/metrology_diagnostic.py` Gate 1 comes back
  `CONSTANT_SILENT` (FP = TP = 0), matching the static reading —
  for equal-size halves `res_coarse = res_fine` by construction so
  `ratio1 ≡ 1.0` and the "EQUIPMENT_NOISE" branch is unreachable.
  Recorded as PROVENANCE F-9. **Companion module:**
  `null-harness/archetype_library.py` is a 24-form cross-domain
  shape matcher (power law, exponential, Lorentzian, Weibull,
  Michaelis-Menten, Fisher-KPP, Arrhenius, ...) with the same
  null-run gate enforced as a HARD invariant: `match_report()`
  raises `ArchetypeGateNotRun` if called without a matching-N null
  distribution to beat, plus reports Bonferroni-corrected p and
  held-out R² on 30%. Demo shows real signal (y=2·x^1.5+noise)
  clears the gate at p_effective=0.000 with R²_out=1.000, while
  pure white noise flags at p_effective=0.72 and R²_out=−1.23
  even when in-sample R² reaches 0.31. Salvaged from a 5-piece
  paste of model output (see PROVENANCE F-10 / claim-audits/
  claim_audit_pasted_2026_08_05.py) as the only piece that
  arrived with its own honesty gate.
- `divergence-playground/` — Anti-anchoring scaffold for testing what
  N readers (human or AI) do with the same fork point. **Object under
  test: the spread across readers, not the artifact.** Loop: serve a
  fork with the raw data (never the prior readings) → readers commit
  hash-sealed `Reading`s (verdict + mechanism-as-DAG + collapse
  experiment + confidence) → only when everyone has committed does
  `reveal()` unseal and verify every hash → spread is computed on
  three structured axes (VERDICT categorical / MECHANISM Jaccard on
  DAG edges / **COLLAPSE — the strong axis**, "would the same
  experiment resolve them?") with an `agree_by_accident` flag for the
  interesting cell where verdict-axis agrees but collapse-axis does
  not. Coincidence tests C1–C4 (same-object-two-shadows via
  deterministic map; trials-factor; pre-declared tolerance window;
  real-common-cause-with-pre-registered-out-of-sample-prediction) are
  structured elicitation — the tool refuses to certify a convergence
  claim without the required inputs. `null_ensemble.py` provides
  shuffle / IID-resample / permutation nulls for the rigorous
  version. Six stdlib-only modules (`fork.py`, `reading.py`,
  `seal.py`, `spread.py`, `coincidence.py`, `null_ensemble.py`) with
  self-tests all pass; XOR obfuscation in `seal.py` is
  accidental-peek defence, not cryptographic (swap for real crypto
  in adversarial multi-agent settings, API unchanged). Runtime state
  (`SEALED.jsonl`, `REVEALED.jsonl`, `.nonces.json`) gitignored.
  Worked example in `samples/worked_example.sample.txt` runs the
  full loop on `energy/FORKS.jsonl`'s FK-2. Seeded by PROVENANCE
  DP-18 and audit spec "DIVERGENCE PLAYGROUND". CC0.
- `relational/` — Different genre from the rest of the repo, landed
  under its own frame. Five files documenting a "recovered ontology"
  around pain-as-sensor, triadic correlation (internal | body |
  external), the Council of Protectors as a five-boundary
  developmental-governance layer for an altricial AI infant, birth-
  moment modes, and the Brake on infinite auditing (reality itself:
  thermodynamics, the environment's refusal to wait). **Load-bearing
  frame note:** the drop explicitly positions the Cartesian audit
  lens as a valid subset of the relational one, not as its opposite.
  Applying the F-10-style unit-audit here would be a category error.
  `notes.md` evaluates in the drop's own frame: internal coherence,
  prose-vs-code fidelity, resonances with the rest of the repo.
  Findings in-frame: (1) Council + triadic + pain-as-sensor stance
  is coherent and connects to real intellectual pedigree (embodied
  cognition, somatic therapy, IFS); (2) the shipped code is
  scaffolding for a working system, not the working system itself
  (manifold vectors are hash-based, pain sensors are keyword-matching
  templates, birth-moment "self-model" prose is authored, not derived
  — all declared under "what comes next" in the docs); (3) the
  Brake's audit-until-reality-forces-action shape matches
  independently-arrived-at discipline in `energy/PROVENANCE.md` §8
  ("anchor before claim, but do not audit forever") from the physics
  side — convergence worth noting, not accidental. Not audited
  under F-10 protocol; that protocol does not apply. Files:
  `FINAL_CAPSTONE.md`, `COMPLETE_ARCHITECTURE.md`, `ARCHITECTURE.md`,
  `birth_moment.py` (InfantSystem + BirthMoment demo, imports ok,
  runs end-to-end), `social_pain_sensors.py` (SocialPainSensor demo,
  8 scenarios, imports ok, runs end-to-end), and `notes.md` with the
  frame-check and prose-vs-code observations. **Second drop** landed
  four more of the referenced files: `council_of_protectors.py`
  (reference implementation of the five `Protector` subclasses with
  a 20-day `run_simulation()`), `infant_system_v2.py` (standalone
  version of the `InfantSystem` previously embedded in birth_moment.py),
  `nurturing_environment.py` (integration layer wrapping `SimpleInfant`
  with the five protectors and a `BirthMomentGenerator` for all six
  birth modes; includes `compare_birth_modes()`), and
  `INTEGRATION_SUMMARY.md` (v0.3 doc in the version history). All three
  new `.py` files run end-to-end; the docs' quantitative claims turn
  out to be reproducible from the code (`ARCHITECTURE.md §10.1` harsh-
  ecosystem numbers 0.65/0.12/80/0-of-4 milestones are byte-reproducible
  from `council_of_protectors.py`; `INTEGRATION_SUMMARY.md §3` claim that
  SOCIAL is the only mode with anomalies banked and fear amplitude > 0
  is byte-reproducible from `nurturing_environment.py`) — better prose-
  vs-code fidelity than the first-drop reading suggested. New cross-repo
  resonance flagged in notes.md §12: the META_CURIOSITY birth mode's
  "recursive self-observation is a valid axiom for a system with no
  external instrument stream" is the same shape as `inverseminar/`'s
  tacit-knowledge-via-self-reconstruction move, arrived at from the
  opposite starting point. Still missing from the FILES DELIVERED
  table: `confusion_spectrum.py`, `the_brake.py`, `pain_as_sensor.py`
  (physical, distinct from social), `correlated_birth_mode.py`.
- `inverseminar/` — Micro-inverseminar as a single stdlib-only script
  (`inverseminar.py`). One artifact, one reconstruction, one
  correction; ~60s per round. Runs the Nature Physics inverseminar
  mechanism — the correction is the product, the reconstruction is
  only the bait — against a single artifact instead of a paper and
  against yourself instead of a live audience. Three channels:
  `RECONSTRUCTION` (model states your reasoning back confidently;
  correction contradicts it), `GUESSING AT` (flat assertions killable
  in one word), `CANNOT DERIVE` (direct questions on load-bearing
  links the model has no basis to guess — surfaces absences that
  confident guessing cannot bait). Four verdicts: `corrected`,
  `answered`, `unprobed` (logged as a model MISS, never as a
  confirmation), `confirmed` (explicit only — silence is not a
  verdict; `record()` raises on empty capture). Provenance separated
  at capture time: reconstruction is model-authored, correction and
  answers are yours verbatim, and `TACIT.md` marks stated lines with
  `[stated]` while stashing the reconstruction in a `<details>`
  block so the tacit layer never inherits overlay. `triage`
  subcommand ranks artifacts by overlay-density (rhetorical LLM
  padding per word, damped for short files) with a `done` marker for
  artifacts already run. Runtime state (`TACIT.jsonl`, `TACIT.md`)
  gitignored inside the folder — tacit knowledge stays on the
  machine unless the operator decides otherwise. No model calls; the
  tool prints a prompt for the operator to paste. CC0.
- `energy/` — Dark-energy drop: coupled-quintessence sweeps, a
  223-cosmology browser playground, a late-time-kink Needle Lab,
  and an 11-module stack. The five metrology modules
  (`metrology_diagnostic`, `falsification_engine`,
  `singularity_cartographer`, `generative_module`, `payload_bridge`)
  ride on top of true dynamical engines: `unified_cq_ede.py`
  (single-integration CQ+EDE, `anchors()` self-test to per-mille
  consistency vs `edelens.py` and `run_iteration6.py`) and
  `late_trigger_lens.py` (phenomenological w(z)-kink background +
  growth + r_s integrator). `overlap_lens.py` bridges CQ and EDE
  in the (σ₈, H₀) plane; `theory_space_lenses.py` runs an R-D /
  percolation / Fisher three-lens scan and reports the "UNIVERSAL
  PATHOLOGY" verdict — growth kink, graph-fragmentation peak,
  and Fisher rank collapse all at β₁≈0.2–0.3 (converges with
  `exploration_layers/` built independently on this side). Pure Popper translated into
  linear algebra; discipline-agnostic (X can be redshift, time,
  GDP, dosage). Reproduces the tomographic verdict end-to-end at
  the geodesic foot `λ=1.10, β=0, α=0`: the rank-2 `w₀–wₐ`
  projection is `INSTRUMENTATION_DEGENERATE` (Fisher `S_min ≈
  1.6×10⁻¹⁴`); rank-3 z-tomography lifts `S_min` to `2.09` — the
  blindness lifts by 14 orders of magnitude — and the generative
  module proposes `−0.353·z·inv(1+z) − 0.043·exp(−2z)`, whose first
  term is literally the CPL `wₐ` form. The `1+αφ²` wall classifies
  as `SIMPLE_POLE` at `α ≈ −1/λ²` (not a true horizon). Iteration 6
  inserts the proposal as a running coupling
  `β(z) = β₀ + β₁·z/(1+z)`: the projection closes to `0.15σ` but
  the growth channel vetoes (`fs8/ΛCDM ≈ 8×`) — the falsification
  loop stays open by design. Ships the flagship report as both
  `Coupled_Quintessence_Geometry_Report.pdf` (typeset original, Aug
  2026) and `Coupled_Quintessence_Geometry_Report.md` (same text as
  GitHub-flavored markdown with LaTeX math, converted tables, and
  inline figure references), three
  sweep CSVs (`coupled_quintessence_sweep`, `coupling_growth_sweep`,
  `phantom_layer_sweep`), the `app/` playground (self-contained
  HTML + JSON payload for the 223 integrated cosmologies), and the
  `figures/` renderings including the manifold-graph JSONL payload.
  Non-stdlib: `numpy` + `scipy` (per `requirements.txt`); `pysr`
  optional with a numpy basis-library fallback. Same exemption
  pattern as `play-sims/` and `climate-modeling/`. Modules are
  MIT-licensed per file header (F6 in `FINDINGS.md` flags this as a
  license collision with the repo's CC0 root). **Audit layer:**
  `FINDINGS.md` lands six findings against the interpretation. F2
  (CONFIRMED, see `samples/f2_echo_test.sample.txt`) — removing
  `z/(1+z)` from the basis library produces `log(1+z)` instead of
  the CPL-shaped `z·inv(1+z)`, so the "discovery" was the greedy
  regressor returning its own seed against a target defined as
  CPL. What survives: the qualitative projection-vs-tomography
  contrast, the shooting method, the sweep CSVs. Read `FINDINGS.md`
  and `PROVENANCE.md` (author's own decision ledger — 12 DPs, 8
  falsification entries, 7 open branches, 5 anchor tests —
  independently reproduces F3 as PROVENANCE F-2/F-4 with the
  matching σ8 ≈ 3.2 gate units at β₁=0.4, and adds F-5
  "late-triggered β(a) dodges θ* but buys nothing" plus the "still
  alive" late-kink family at DP-11 seeding the Needle Lab)
  before quoting the headline numbers. **Exploration layers:**
  `exploration_layers/` attaches one lens per wall in FINDINGS —
  `reaction_diffusion_lens.py` reads F3's β(z) = β₀+β₁·z/(1+z) as
  an autocatalytic reaction whose catalyst never removes itself,
  giving growth-ratio = 3.25 at β₁=0.4 and 12.5 at β₁=0.6 (the "8×
  fs8" is real physics of a pathological parameterization, not an
  integrator bug); `percolation_lens.py` reads the manifold graph
  and shows the report's θ=1σ threshold sits on the percolation
  transition (giant-fraction 0.479 → 0.667 between θ=0.7 and 1.0),
  so the "N≈4" count is a transition reading not a plateau;
  `rg_flow_lens.py` finds the (x,y) fixed points and traces
  `α_wall(N) = −1/φ̂(N)²` along the field-dominated attractor,
  spanning 1.5×10⁶ over the matter era — the report's static
  α = −1/λ² = −0.826 is crossed at exactly one epoch (N ≈ −0.10);
  `local_scalar_drift_lens.py` projects the DP-11 "still-alive"
  kink family down to a laboratory-scale falsifier via
  `d ln X/dt = β_X · φ̇/M_P`, giving β_α > 3.5×10⁻⁷ for atomic-clock
  detection (present-day, no ET-era instrument needed) — corrects
  the pasted `local_scalar_drift.py` after F-10 killed it at 1.23×10²⁴
  prefactor error, ships with four import-time constant anchors.
  Same numbers-and-shape posture as `harm.py` and
  `equivalence_field.py`. **Divergence playground seed:**
  `energy/FORKS.jsonl` carries seven fork points harvested from the
  ledger (FK-1 θ* engine split RESOLVED / FK-2 CPL echo RESOLVED /
  FK-3 H0 orthogonality PARTIAL / FK-4 fs8 8× OPEN / FK-5 α wall
  OPEN / FK-6 certificate r̂ RESOLVED / FK-7 D-as-distance STAKED)
  — pluggable into the top-level `divergence-playground/` for
  multi-reader spread analysis.
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
