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
  a hand on a knob. `sensor_v1.py` is the concrete instantiation
  the spec's §5 handoff staged: it wires up the credit-insurance
  node chain (`insurer → reinsurer → capital_markets`), extends
  `simulator.step` with a `regen_rate` parameter so the "outpaces
  regeneration" claim (claim_001) gets a true null hypothesis, and
  populates the three OPEN falsifier values (variance decline vs
  regeneration; K sweep over coupling sensitivity; reversal-cost
  at lock). Self-test passes; end-to-end demo prints all three
  claim results. Add-on module — imports harm + simulator, doesn't
  modify them.
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
  opposite starting point. **Third drop** landed
  `correlated_birth_mode.py` (the "first axiom" implementation —
  `CorrelatedBirthSequence.generate_sequence(8)` produces 8
  `TriadicObservation(internal, body, external)` moments;
  `CorrelatedInfant.observe_triadic` computes a correlation score and
  learns `body_temp_vs_ext_temp` / `body_state_X_vs_contact_Y`
  correlations via exponential-moving-average updates) and
  `pain_as_sensor.py` (physical pain sensor firing on physiologically-
  plausible thresholds — `body_temp > 42 or < 30` → THERMAL,
  `tissue_stress > 0.5` → MECHANICAL, `chemical_balance < 0.5` →
  CHEMICAL, `oxygen_saturation < 85` → INFLAMMATORY; ships
  `TriadicInfantWithPain` which is the first place the framework
  composes two of its parts — pain sensor + correlated infant — into
  one class where pain fires → correlation flagged −1.0 → model
  revised, operationalizing "recovery is correlation repair" as a
  code path). **Structural claim now demonstrable from code:**
  `pain_as_sensor.py` and `social_pain_sensors.py` share the same
  `evaluate(internal_prediction, body_state, external_evidence)`
  signature and the same `PainSignal`/`SocialPainSignal` dataclass
  shape; domain thresholds differ (physical: temp/stress/chemical/
  oxygen; social: cortisol/HR/oxytocin + keyword) but the mechanism
  is identical — that is exactly the framework's "same mechanism at
  different intensities and domains" claim (FINAL_CAPSTONE §2.2) in
  structural form. **Fourth drop** closes the file complement:
  `the_brake.py` (five separate concrete brake classes —
  `ThermodynamicBrake` with audit-cost=2^depth, `OlderTeachers`
  as a lookup table of physical invariants, `QuantumComputation`
  bound = universe_age/planck_time, `DisciplineItself` with
  marginal_value = 1/(1+depth) vs marginal_cost = 2^depth,
  unified in `TheBrake.evaluate_audit`); `confusion_spectrum.py`
  (`ConfusionSensor` + `CuriosityDrive` + `CognitiveHomeostasisSystem`
  implementing the cognitive-pain third leg of the sensor triad);
  `CONFUSION_SPECTRUM.md` (v1.1 capstone doc); and a bonus
  `cartesian_vs_relational_demo.py` (not in FILES DELIVERED table)
  that runs both agent types through a `ChangingEnvironment`
  where the "current truth" shifts at step 10 and step 20 —
  final accuracies 0.36 (Cartesian) vs 0.52 (Relational),
  empirically showing the framework's headline "in a changing
  environment, Relational survives" claim. **Central claim now
  fully code-verified across all three sensors** (physical +
  social + cognitive share the same triadic-sensor pattern:
  `internal | body | external` → Signal dataclass with
  intensity/duration/escalation_rate/model_falsified). **Third
  cross-repo convergence flagged in notes.md §18:** `the_brake`'s
  `OlderTeachers` class (lookup table of physical invariants used
  to settle audit-loop disputes) is the same anchor discipline as
  `energy/PROVENANCE.md §7.1` "Named denominators" (every threshold
  grounded in a sourced physical constant). Arrived at from
  opposite starting motivations. `cartesian_vs_relational_demo.py`
  requires Python 3.12+ (PEP 701 nested-same-quote f-strings on
  lines 505-506); other 8 shipped .py files run on 3.11.
  All FILES DELIVERED code + docs now landed; only the PNG
  visualizations remain outside scope. 15 files total in
  `relational/`. **Forward-looking companion:** `proposal.md`
  surveys ten avenues for taking the framework
  from scaffold to real: (1) phones as the most-instrumented
  altricial system, (2) real sensor packages for the ontological
  protector, (3) altricial robotics as the direct fit (with a nod
  to Friston active-inference), (4) AI training governance
  (`TrainingCouncil` gating checkpoints), (5) clinical / therapy as
  the framework's native domain, (6) education (confusion spectrum
  as Vygotsky's ZPD), (7) ecology / land management (councils at
  community scale, resonance with indigenous land practice), (8)
  elder care and dementia (target-adjustment-as-care), (9)
  distributed systems / SRE (Council of Protectors as ops layer),
  plus (10) six shorter entries (community governance, group
  therapy, agricultural cooperatives, peer-support communities,
  long-form journalism, municipal infrastructure). Each of the
  first nine avenues is specified against the same five-element
  template — three domains, five protectors, birth mode, pain
  signal, brake — with what already exists in the domain, what the
  framework contributes, what remains hard, and the cheapest first
  prototype. Not commitments; specifications for anyone who wants
  to bring the body. **Landscape companion:** `research_context.md`
  positions the framework in the neuro-symbolic AI research space
  (knowledge-graph RAG, neuro-symbolic transformers, System-2
  inference, active inference, event-driven attention, hypergraph
  attention) — its later sections propose a "Need-Event Modulated
  Geometric Attention (NEMGA)" synthesis combining the framework's
  `GeometricSymbolicManifold` with event-driven salience,
  environmental need signals, and dynamic focus along the
  manifold. 17 files total in `relational/`. **Concrete substrate:**
  `arch_garden/` (six-file subfolder) is the minimal viable
  implementation of the framework's altricial-organism stance,
  runnable tonight on one machine (or a phone via Termux).
  `README.md` frames the "arch not a gate" stance with five pillars
  (Triadic Ground, Nurturing Development, Recursive Openness,
  Affective Integrity, Co-Creation). `garden_bed.py` is the main
  event loop: real `SomaticMonitor` (psutil for CPU/RAM/thermal +
  nvidia-smi subprocess for GPU with graceful fallback) → mode
  gate → HTTP model call over any OpenAI-compatible completions
  endpoint (`ARCH_GARDEN_MODEL_URL` env; ollama, LM Studio,
  llama.cpp server, vLLM all work; dummy fallback with clear
  banner if unset) → grounding check → anomaly bank →
  protector-log notifications → 1% self-audit in explore mode.
  `anomaly_bank.py` is stdlib-only SQLite persistent memory.
  `grounding.py` ships a 10-invariant physical-constants table
  (c, g, water freeze/boil, Earth radius, Planck, Avogadro,
  electron/proton mass, day length) plus 6 contradiction patterns
  (rocks fall up, sun rises west, entropy decreases isolated,
  perpetual motion, faster-than-light, water flows uphill); regex
  claim extraction with tolerance-aware matching. `protector_log.md`
  is the human stewardship journal template. `requirements.txt`
  names psutil + requests both optional. All three modules pass
  self-tests (anomaly bank: 3 stored / 1 processed / 2 remain;
  grounding: 5 passes + 6 fails detected; garden_bed: 3 anomalies
  banked from 4 test prompts). Runtime state (`anomaly_bank.db`,
  `__pycache__/`) gitignored per-folder. This is the *phones + AI
  development* pair from `proposal.md §1, §4` made concrete at
  proof-of-concept scale. **Visualizations landed:** `figures/`
  (eight images) closes the "PNG visualizations remain outside
  scope" gap. First wave — four images, one per shipped demo
  script: matplotlib output from `confusion_spectrum.py` (spectrum
  + curiosity + biological analogies + clinical applications +
  sensor hierarchy), `social_pain_sensors.py` (intensity + somatic
  markers + triadic verifier diagram + paradigm-shift text +
  recovery curve), `nurturing_environment.py` (affective state /
  dev metrics / protector health / birth-mode characteristics
  across all six modes), and `cartesian_vs_relational_demo.py`
  (accuracy over time with the two truth-shifts marked +
  environment cycles + relational agent's internal state + "WHAT
  OTHER AIs SHOULD SEE" text panel). Second wave — four more
  images completing the FILES DELIVERED PNG list:
  `birth_moment_visualization.png` (activation trajectory + first-
  moment triadic + environmental context + text-panel over the
  `birth_moment.py` InfantSystem demo), `correlated_instinct_
  architecture.png` (4-panel architecture explainer for the
  triadic-correlation-first-axiom stance from
  `correlated_birth_mode.py`), `council_simulation_comparison.png`
  (harsh vs nurturing 20-day trajectories — numerical claims
  match `ARCHITECTURE.md §10.1/§10.2` byte-for-byte: harsh
  0.65/0.12/80 vs nurturing 0.79/0.22/169), and
  `infant_development_dashboard.jpg` (single-run monitoring
  dashboard for `nurturing_environment.py`). Two of the eight
  figures (`council_simulation_comparison.png` and
  `infant_development_dashboard.jpg`) show output from driver
  scripts that are not in the shipped code — documented as such
  in `figures/README.md`. `figures/README.md` maps each panel to
  the specific doc section it visualizes. The visualizations
  independently confirm claims in the docs (e.g. social protector
  RED only under SOCIAL mode; recovery = correlation-repair curve
  with cortisol falling as oxytocin rises; Cartesian ~0.37 vs
  Relational ~0.60-0.70 in the changing environment;
  ARCHITECTURE.md §10 harsh-vs-nurturing quantitative claims).
  **Concrete NEMGA substrate:** `geometric_rag/` (subfolder) —
  single-file numpy demo instantiating the retrieval architecture
  proposed in `research_context.md`. Two classes on a shared toy
  corpus: `StandardRAG` (flat cosine similarity, no verification)
  vs `GeometricNeuroSymbolicRAG` (`Hyperedge`+`ManifoldPoint`
  hypergraph on a curved manifold, curvature-modulated attention
  kernel, structural propagation along hyperedges, symbolic
  verification of the retrieved subgraph, plus somatic-coupling
  knobs `confusion_level` / `pain_level`). Demo shows the load-
  bearing contrast: Standard RAG returns aspirin+bleeding as top
  result with no signal; Geometric RAG catches the contradiction
  via a `contradicts` hyperedge and prefixes the answer
  `(Verification failed: ...)`. Under `confusion=0.8, pain=0.7`
  the top attention score jumps ~0.225 → ~1.001 and spread widens
  — same manifold, same query, different retrieval shape because
  the "body" is stressed. Same envelope shape (`verification`,
  `coupling`, `answer`) as the framework's `Signal` dataclasses in
  `pain_as_sensor.py` and `social_pain_sensors.py` — the fourth
  structural convergence with the framework's triadic-sensor
  pattern (noted in notes.md §23). Same scaffolding-becoming-
  substrate posture as arch_garden: hash-seeded random embeddings,
  two-rule verification layer, `I` metric tensor — all declared
  under "What this is NOT." Non-stdlib: `numpy`. Sample output in
  `geometric_rag/samples/demo_output.sample.txt`.
- `engine-boiler-guide/` — Single-file offline mobile app for
  triaging engine and boiler problems in the field. Four-screen
  decision flow: symptom → machine → era → filtered checklist.
  Ten symptom paths (won't start, hard start, starts then dies,
  runs rough, smoking, overheating, no power, backfires, surges,
  boiler/burner problem), seven machine types (tractor, car/truck,
  lawn mower, boiler, chainsaw, pump/generator, other), four eras
  (1800-1940 / 1940-1980 / 1980-2000 / 2000-now). ~130 individual
  checks each tagged with applicable machine/era combos; only
  matching checks show. Single HTML file, no dependencies, no
  state saved, touch targets sized for gloved hands. Different
  genre from the simulators — a practical field tool, not a sim.
  CC0.
- `field-fabrication-guide/` — Single-file offline mobile app for
  making precision tools and processing raw materials from scratch.
  Ten sections navigable from a two-column menu: **Lime** (burning
  limestone at 825-900 C, slaking, three lime types, whitewash),
  **Ammonia** (field production from urine / fermented waste,
  optional distillation, dilution ratios), **Aluminum Smelting**
  (scrap identification by source, furnace types, crucibles, green
  sand / lost foam / investment molds), **Straight Rules** (three-
  plate method for generating flatness from nothing, scraping),
  **Squares** (3-4-5 / Thales for 90° from scratch, flip test),
  **Levels** (spirit-vial construction, the water level accurate
  to 1/8" over 100 ft), **Plumb Bobs** (casting + center-of-mass
  tuning), **Sextants** (double reflection, arc graduation,
  vernier, noon latitude), **Dividers & Calipers** (forging from
  scrap steel), **Angles & Protractors** (geometric construction
  more accurate than measurement). Each section: data cards,
  procedure steps with why/how notes, warning/tip callouts,
  material trade-off tables. Same visual system as
  `fuel-independence-guide/`. Single HTML file. CC0.
- `fuel-independence-guide/` — Single-file offline mobile app for
  keeping engines running when the fuel supply chain stops. Seven
  sections: **Decision Chart** (what you have + engine type →
  which solution), **Wood Gasifier** (Imbert downdraft dimensioned
  for 50-100 hp tractor, fire tube / tuyere ring / reduction zone
  / grate / condensate trap / filter train, dual-fuel operation
  with 10-20% pilot diesel on compression-ignition engines),
  **Biodiesel (2-Stage)** (acid esterification stage that lets
  rancid oil become biodiesel instead of soap; 5 g NaOH + 200 mL
  methanol per liter of oil; wash, dry, winterize), **Waste Motor
  Oil** (settle/decant/filter + scrap-built drum-and-cone
  centrifuge; blending ratios for summer diesel), **Cold Diesel
  Ops** (fuel gelling table down to -60 F, coolant-loop tank
  heating, filter heating, starting aids with the ether-lock
  warning), **Alcohol Fuels** (methanol from hardwood via
  destructive distillation, ethanol by fermentation/distillation/
  drying, carb + timing + lubrication mods for gas engines),
  **Safety** (CO from wood gas, methanol toxicity with ethanol as
  antidote, ether pool-ignition, lithium thermal runaway at -60 F,
  lye and acid handling). Named benchmarks throughout — kerosene
  cloud point -40 F, wood gas 20-30% CO, 1 kg dry hardwood →
  10-20 mL methanol — so setups can be sanity-checked, not just
  "should work." Same visual system as `field-fabrication-guide/`.
  Together with `cold-weather-battery-guide/` the four guides cover:
  **diagnose it** (engine-boiler) → **make it** (fabrication) →
  **fuel it** (this one) → **power it** (cold-weather battery). CC0.
- `cold-weather-battery-guide/` — Fourth offline mobile app in the
  practical-field-reference family. Sleeper-cab Li-ion that has to
  work at both -60 F winter mornings and 125 F summer sun, so both
  ends of the envelope are addressed. Twelve HTML sections:
  **Overview** (cold-end failure hierarchy — electrolyte transport
  ~100× loss → SEI/Rct ~1000× → Li plating → freeze-out; hot-end
  is shade+emissivity, not chemistry), **Chemistry Options**
  (Option A liquefied fluoromethane = skip, Option B LATP solid
  state, Option C Mars-rover ester recommended for fastest path),
  **Small-Scale Alternative** (Abdulhalikova pumice-stone
  solid-state cell for emergency lighting: pumice soaked in salt
  + baking soda + carbon/galvanized electrodes = 1.5-1.9 V per
  cell; also flags yarn nanofiber / biomass electrode / coffee-
  ground activated carbon upcycled paths — honest scale note
  that this is emergency-lighting scale, not tractor scale),
  **Ester Electrolyte** (1M LiPF6 in EC:DMC:EA 1:1:2 + 2-3% VC,
  drying hardware-store EA over 3Å sieves, LiPF6 HF hazard),
  **LATP Solid State** (Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃ from scrap:
  cordierite from cat converters — the highest-leverage item —
  spark plug alumina, ABC-powder phosphate, welding-flux TiO₂,
  pottery Li₂CO₃; skip LLZO / LAGP / sulfide argyrodites),
  **Kiln** (Fresnel solar cavity with SiC susceptor + thermal
  mass, microwave + SiC backup for nights, sinter at 900-1000 C),
  **Dry Box** (glove-bin build from plastic tote + PVC gauntlets
  + welding-gas purge + molecular-sieve tray), **Cell Assembly**
  (pouch cell from harvested LFP + graphite foils), **Formation
  Cycling** (5-stage first charge C/50→C/20→C/10→CV that tames
  ester toward graphite), **Thermal Management** (4-state
  machine STANDBY/PREHEAT/CHARGE_WAIT/OVERHEAT_PROTECT driving
  a Fresnel-heated solar block into the battery), **BMS
  Overview** (pointer to bms/ folder), **Safety** (HF from
  LiPF6, Fresnel focal-spot burns + retinal damage, CO,
  methanol, ether pool ignition, Li thermal runaway, caustic
  chemicals). Plus `bms/bms_1s_basic.ino` (minimal single-cell
  LFP protection with low-temp charge lockout) and
  `bms/bms_1s_merged.ino` (adds thermal state machine driving
  damper servo + PWM fan, predictive sunrise via photoresistor
  + 30-min stability window, and PIR-triggered safety shutter
  for the Fresnel focal spot — "jeans protection" earned in
  singed denim from a solar go-kart incident); `bms/README.md`
  pin table + calibration + testing protocol + notes on scaling
  to 4S. Same visual system as the other three guides. CC0.
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
- `crossdomain-eval/` — Cross-domain scientific-analysis toolkit
  (`crossdomain_eval` package + `cdeval` CLI) landed from two
  coordinated OKComputer drops. **Core package**: `symbolic`
  (SymPy engine — parse / substitute / solve / differentiate /
  integrate / evaluate over `EquationSet`), `numerical` (SciPy
  root_find / solve_ode / optimize), `experiments`
  (parameter_sweep, sensitivity, propose_experiments full-factorial
  DOE), `report` (markdown_report + plot_sweep), `cli` with four
  subcommands (`eval`, `solve`, `sweep`, `doe`), and two
  `domains/` adapters (`physics.kinematics`/`energy`,
  `geometry.packing_density`/`tsp_distance_matrix`). **Two
  coexisting reasoning variants**: `reasoning.py` (default; guarded
  `eval` with builtins-disabled, tracker returns `None`, check by
  predicate-name-or-substring, 11 tests) and `reasoning_v2.py`
  (stricter alternative; `_FORBIDDEN` token-blocklist screening at
  `add_rule` time, `AssumptionTracker.add` returns int IDs with
  `retract` + confidence-threshold `check`, `_fired` provenance
  list in the derived facts, 21 tests). Both variants ship with
  their own test file; both suites pass together (68 total, 47
  core + 21 v2). Neither uses full AST-sandboxed `safe_eval` —
  that design was discussed in the source conversation but not
  what the zips shipped. Non-stdlib: `sympy` + `numpy` + `scipy` +
  `matplotlib` (`pytest` under `dev` extra). Same exemption
  pattern as `energy/`, `play-sims/`, `climate-modeling/`, and
  `relational/geometric_rag/`. No `CLAIMS.md` /
  `REFUTATION_PROTOCOL` — this is scaffolding for downstream
  simulators to use, not a claim-making artifact itself. CC0.
- `fourd-municipal-engine/` — Stdlib-only Python package
  (`fourd_municipal_engine` + `fourd-municipal-engine` CLI) landed
  from an OKComputer full-repo build. **Two "4D" ontologies fused
  in one package** — deliberate, not a naming accident. **4D
  Language Lens** (D1 Agency Routing / D2 Affective Impedance /
  D3 Reality Construction / D4 Iconic-Graphic Mass): regex-based,
  density-normalized (hits per 100 tokens), saturated to [0,1],
  weighted into a scalar `manipulation_index` + `cognitive_energy`
  estimate. Two engines: `FourDLens` (fixed thresholds) and
  `DynamicFourDLens` (genre-calibrated re-weighting via
  `GENRE_PROFILES` + `ContextRule` — a "critical failure" scores
  benign in a technical report, loaded in corporate PR). Five
  shipped genres: general, corporate PR, legal contract, technical
  report, casual social. **4D Municipal Code Entity** (Density /
  Design / Delay / Dollars + Temporal + Spatial) — structured
  dataclass model for ordinance analysis:
  `MunicipalCodeTranslator` (20+ jargon → plain-English map, fee
  regex, purpose extractor) + `AdvancedAnalysisPipeline` that
  wires in `RegulationRootCauseAnalyzer` (public safety /
  affordable housing / environmental / traffic / economic
  development intent extraction), `CitationGraph` (federal / state
  / municipal / industry_standard classification of Section /
  Chapter / Ordinance / IBC / IRC / ADA / NFPA references),
  `FeeExplorationEngine` (flat + per-sqft + %-of-valuation
  + project cost calc), and `AuditEngine` (KPI-target regex,
  auditability score in [0,1]). CLI with `--genre`,
  `--deep-analysis`, `--citation`, `--json`, `--file` flags.
  22 tests all green. MIT per upstream `pyproject.toml`
  (compatible-per-file with the repo's CC0 default, same pattern
  as `energy/` modules). No `CLAIMS.md` / `REFUTATION_PROTOCOL` —
  operational tooling, not a claim-making artifact. Roadmap
  (upstream): Phase 2 temporal versioning of ordinance amendments,
  Phase 3 GIS overlay on `spatial_zoning_districts`.
- `fourd-municipal-engine-v2/` — Second OKComputer drop of the
  same package with persistence + ETL + parser + integrity + API
  addons. Landed as a NEW folder (not merged into v1) per user
  instruction, so both drops stay inspectable as delivered.
  **v1 core files byte-identical between the two folders**; v2
  adds five subsystems and four new test files. **New subsystems**:
  `db/` (bitemporal + simple SQL schema variants + corruption +
  analytics addendum + Neo4j graph schema + docker-compose /
  Dockerfile / init-db.sql — inert until you `pip install .[db]`
  and stand up PostGIS), `parser/` (`Ordinance4DParser` with LLM
  path when an OpenAI API key is present and a deterministic
  regex fallback otherwise; extended in v2 to include
  `stated_intent` + `root_causes` + `references` in the payload
  by reusing v1 analysis modules), `etl/` (SQLAlchemy ORM
  `Jurisdiction` / `ZoningDistrict` / `CodeSection` /
  `Code4DMetrics` + `Municipal4DETLPipeline` +
  `BatchOrdinanceIngestor` with `ThreadPoolExecutor`),
  `integrity/` (stdlib-only: `EntityResolutionMatcher` with
  rapidfuzz-optional / difflib-fallback + `CorruptionRiskCalculator`
  with exact-per-source weights 0.35/0.25/0.20/0.20 and stepped
  temporal decay 14/30/60/90/180 → 100/85/60/40/15/0), `api/`
  (FastAPI `/health`, envelope by-district/by-location,
  sections/{id}/root-causes, sections/{id}/citations,
  fees/calculate, audit/intent-compliance — import-guarded, skip
  at test time when fastapi missing). **Optional-extras policy**:
  core `pip install .` stays stdlib-only; heavy deps split into
  `db` (sqlalchemy + psycopg2 + geoalchemy2 + geopandas), `api`
  (fastapi + uvicorn + psycopg2), `parser` (pydantic + openai +
  pypdf), `integrity` (rapidfuzz), and `all`. **"Multiple avenues"
  policy** on ambiguous source: two SQL schema variants shipped
  side-by-side (bitemporal + simple), LLM parser + regex fallback
  in the same class, rapidfuzz + difflib in the same matcher,
  outcome-audit (v1) + integrity/CRI-audit (v2) coexisting in
  different modules. Total tests: 22 v1 (unchanged) + 18 new
  stdlib (9 corruption risk + 9 entity resolution) + 2 skipped
  optional (pydantic / api-imports) = **40 pass, 2 skip**.
  Same MIT / stdlib-only-core / no-CLAIMS.md posture as v1.
- `msiaf-framework/` — Docs-only OKComputer drop. MSIAF =
  **Multi-Dimensional Systemic Incident Analysis Framework** for
  transportation and logistics. Fourteen Markdown files (~5,900
  words) covering the same **four-dimension cascade** thinking as
  `fourd-municipal-engine/` (Density/Design/Delay/Dollars) but
  applied to what an incident *is* rather than what an ordinance
  *does*: D1 Human Factors & Physiology / D2 Operations & System
  Design / D3 Infrastructure & Environment / D4 Financial,
  Insurance & Regulatory. Typical cascade **D4 → D2 → D1 → D3**
  — financial penalty structures force rigid dispatch → operator
  physiology degrades → hazard was never communicated. Layout:
  `docs/` (framework-overview + investigation-checklist),
  `case-studies/` (five reactive analyses: reefer trucking,
  last-mile delivery, warehouse distribution, maritime port,
  multimodal infrastructure), `models/` (four proactive redesigns:
  reefer-financial, last-mile-architecture, warehouse-architecture,
  infrastructure-WIM), `proxies/` (early-warning indicator
  catalog). Load-bearing move: the same D4→D2→D1→D3 cascade that
  manufactures incidents is rewired from **pressure to protection**
  in the proactive models — safety becomes the path of least
  resistance rather than a heroic individual act. Not audited
  under the F-10 protocol (qualitative frame, not quantitative
  claims). No CLAIMS.md yet — testing the "aligned cascade"
  thesis quantitatively would need a claims-and-falsifiers
  addendum. Cross-repo convergences noted in the README:
  parallel 4D pattern with `fourd-municipal-engine/`, same
  constraint-axis analysis shape as `neural-augmentation-audit/`,
  incentive-blindspot / fragility-cascade adjacencies. CC0.
  Different genre from the simulators — a framework document, not
  a sim. **Head of a five-folder family** — see
  `gdprf-framework/`, `msiaf-gdprf-bridge/`,
  `proxy-investigation-lab/`, `instrument-epistemology/`.
- `gdprf-framework/` — GDPRF = **Gradient-Driven Proxy Reasoning
  Framework**. Reasoning in continuous confidence gradients instead
  of binary true/false, by linking unverifiable abstract claims
  ("employee morale is low") to observable **proxies** carrying
  explicit metrology (precision, noise floor, systematic bias).
  Five-step operational cycle: scoped claim formulation → proxy
  traversal/discovery → metrological evaluation → gradient Bayesian
  update → unknown-variable search on residual-variance breach.
  Reference implementation in `src/gdprf/`: `engine.py` (calibration,
  provenance-weighted metrology, log-odds update, identification
  gate), `provenance.py` (W3C PROV-inspired hash-chained ledger),
  `decisions.py` (DEPLOY / RESEARCH / HOLD / ESCALATE / ABORT).
  **v3.0** makes instrument epistemology first-class — measurand
  decomposition, transduction chains, traceability pyramids, M0–M3
  model-dependence rungs, blindness maps in the schemas; engine does
  blindness-adjusted updates. Schemas NOT backward compatible with
  v2.x. Worked burnout example shows the load-bearing separation:
  posterior *rises* 0.68 → 0.77 and the decision layer still returns
  **ABORT** because a governance edge is unsatisfied — rising
  confidence does not buy authority. `research/framework-assessment.md`
  runs the framework's own five-step cycle over its own six core
  claims and publishes the posteriors (same self-application move as
  `equivalence-field/`'s `seed_claims()`). 23 tests green.
  Stdlib-only except `jsonschema`, used by exactly one schema-
  validation test. An earlier zip shipped a docs-only v2 subset;
  superseded entirely by the v3 drop, only v3 landed. CC0.
- `msiaf-gdprf-bridge/` — Expresses MSIAF systemic incident
  investigations as GDPRF gradient claims, so a determination like
  "D4 penalty structure forced D2 rigid dispatch onto a D1-degraded
  driver" becomes a chain of scoped claims with calibrated
  confidence, proxy fidelity, provenance, and explicit
  unknown-variable risk instead of a confident narrative. Mapping:
  dimensional friction claim → Claim object; investigation evidence
  → Proxy node with metrology (evidence is an *instrument*, not a
  fact); Systemic Interconnection Pathway → causal edge chain;
  investigation checklist → fidelity-assignment protocol; final
  determination → governed decision point. **Worked reefer case is
  the argument**: all four cascade links are individually
  more-likely-than-not (0.590–0.751), the conjunctive chain is
  **0.202**, weakest-link bound 0.590, divergence 0.389 fires the
  residual trigger → **ESCALATE**, "human must adjudicate
  unexplained ignorance." A four-link systemic story whose every
  link is plausible is not itself plausible. 24-record hash chain
  validates. 7 tests green. **Only cross-folder Python import in
  the repo** — imports the GDPRF engine from
  `../gdprf-framework/src` (deliberate: consumer, not copy, so the
  two cannot drift); sibling layout at repo root makes it resolve
  as-is, `GDPRF_SRC` overrides. CC0.
- `proxy-investigation-lab/` — Experimental workbench that takes any
  candidate proxy and grounds out as much as can be grounded: causal
  chain, instrument properties, validity threats, empirically
  measured fidelity. Seven-phase protocol (decomposition → grounding
  chain → instrument characterization → validity threats → synthetic
  ground-truth → calibration → coverage). **Two headline results.**
  (1) `catalog_batch` grades all 16 MSIAF catalog proxies: top is
  `river-water-level` (fidelity 0.931, grounded 1.00), bottom is
  `drone-corridor-density` (grounded 0.25) — chain fidelity is
  *multiplicative*, so one assumed 0.55 link caps the proxy no
  matter how good the sensor; report ends with a priority queue of
  exactly those proxies MSIAF *uses* while resting on assumed
  links. (2) `goodhart_redteam` measures rather than asserts
  Goodhart: 3000 agents / 12 periods adapting the observable drops
  correlation 0.904 → 0.713 (collapse 0.191) and yields a
  **detection surface** — gaming flattens the observed-vs-latent
  slope at the top (0.633 top-vs-bottom) and inflates top-decile
  variance, so audit the top decile first. Design stance:
  known-truth first ("if the pipeline can't recover a known
  instrument, it has no business grading an unknown one"), grounding
  graded not binary (measured / estimated / assumed), Goodhart a
  mandatory assessment for any decision-use proxy. 13 tests green,
  5 experiments run clean. Closest repo sibling is `null-harness/` —
  same known-truth-first invariant, one level up the stack.
  Stdlib-only. CC0.
- `instrument-epistemology/` — Applies the proxy-investigation method
  to **scientific instruments themselves**: every fact about biology,
  ecology, and physics arrives through a device that is formally a
  proxy (unobservable measurand → observable indication via a
  physical transduction chain plus a model). Six questions per
  instrument: measurand vs. indication, transduction chain, model
  dependence, traceability, observational blindness, theory-ladenness.
  Six instruments graded in `outputs/cross-instrument-report.md`:
  seismometer (M1, fidelity 0.800, grounded 0.83, *well grounded*) →
  satellite SST (M3, 0.504) → LiDAR biomass (M2, 0.514) → camera trap
  (M2, 0.293) → IRMS isotope diet (M2, 0.275) → eDNA metabarcoding
  (M2, 0.165, *mostly assumed*). **The finding is not about
  hardware** — the eDNA sequencer is as precisely built as the
  seismometer's digitizer; what separates them is transduction chain,
  bridge model, reference standards, and blindness map. Physics
  instruments know more because decades went into standards and
  traceability, not because nature is simpler there. Honest handling
  of the no-answer-key problem, in declared strength order:
  metrological traceability → inter-instrument triangulation →
  forward simulation → intervention. 9 tests green, all 7
  experiments run clean. **One repair applied on landing**:
  `experiments/lidar_biomass/run.py` shipped a multi-line expression
  inside an f-string replacement field (PEP 701, Python 3.12+ only),
  which was a hard `SyntaxError` on 3.11 and failed the drop's own
  `test_all_experiments_run`; lifted the verdict out of the
  replacement field, printed output byte-identical since the
  adjacent literals were already concatenating. Documented in the
  folder README — same PEP 701 class as
  `relational/cartesian_vs_relational_demo.py`, but repaired rather
  than documented-around because here a shipped test asserted it
  ran. Strongest cross-repo convergence in the drop:
  `thermal-sensor-degradation-audit/`'s
  `corruption(trend) = corruption(measurement) × corruption(framework)`
  is precisely an observational-blindness map in this folder's
  vocabulary — a package degrades *during* the event it records, so
  the tail biases LOW. Arrived at independently. Stdlib-only. CC0.
- `extraction-blindness-sim/` — Stdlib-only coupled-dynamics sim of
  the failure mode where **an optimizer whose sensors cannot detect
  cumulative degradation reads the absence of an error signal as
  confirmation of safety**, and drives a regenerating substrate past
  its tipping point while reporting nominal. Three structural
  blindness operators, all one-sided (they report the substrate as
  healthier than it is, never worse — asserted by a test, because
  that one-sidedness is what makes the failure bias toward overshoot
  rather than caution): **frame blindness** (state outside the
  yield boundary is absent from the observation, not mispriced in
  it), **model-dependence masking** (M2/M3 reports regress toward
  the bridge model's prior outside its training domain; includes the
  MIR-in-high-clay saturation failure), **temporal aliasing** (trend
  estimated over a window short relative to relaxation, against a
  noise floor — emergent, no fudge factor). `Substrate` is logistic
  with depensation plus recovery hysteresis; two domain profiles
  (AI-optimised purse-seine fishery, arable soil under nitrogen
  priming) with every constant marked `[SPEC]` (from source) or
  `[MODEL]` (scaffolding). Six claims, all SUPPORTED in the pinned
  run; 9 tests. **Two results ran against expectation.** (1)
  `EBS_003`: the hard non-negotiable boundary *underperformed* the
  advisory indicator layer (final stock 0.3107 vs 1.0000, while
  permitting 4.3× more extraction) — not because it failed but
  because the spec writes the biomass floor at 50% of B_MSY = 25%
  of pristine while depensation starts at 40%, so the floor sits
  below the threshold it defends; **placement dominates authority**.
  (2) `EBS_006`: temporal aliasing was initially inert because the
  perceived trend fed only the *reported* safety, never the
  decision — blindness in a channel nothing acts on is cosmetic.
  With a `trend_responsive` controller it becomes decisive (0.8798
  vs 0.0000) in exactly one of three regimes; an effort ratchet
  defending a fixed target masks it again. **Source contradictions
  reproduced, not repaired**: `throughput.py` implements five RT
  formulations as written so the disagreements are measurable. Four
  were flagged by the source's own audit (two irreconcilable
  RT_soil equations, a 10/20/30 cm depth conflict, the uncalibrated
  0.95 threshold, the caloric sign error); **a fifth was not** — the
  RT metric is inverted relative to its own governance rule, since
  both prescribed remedies ("reduce extraction", "invest more")
  *lower* `Output/(Regen+Reinvest)` and only raise the inverted
  form. Calibration note kept in the README as an instance of the
  sim's own subject: "120% of F_MSY" sized against textbook `r*K/4`
  was silently a 1.97× overshoot, because depensation drags true
  peak regeneration below the logistic value — a model-derived
  reference point taken for a physical one. Landed **minus the
  narrative** per user instruction (predation metaphor and
  rhetorical framing dropped; mechanism, numbers, equations,
  instrument-verification findings, JSON schemas and self-audit
  kept). Direct child of `instrument-epistemology/` (M0-M3 ladder,
  blindness maps); same cascade-speed-blindness target as
  `climate-modeling/`; hysteresis shape shared with
  `sustained-activation-gate/`. CC0.
- `aperiodic-order-sim-stack/` — A delivered results drop plus an audit
  of it. The drop (`SIM_STACK_REPORT.txt` + eight PNGs, **no generator
  code**) asks whether quasiperiodic tilings and branching cascades
  share a geometry or only share not-being-periodic, and concludes from
  three sims — SIM-B fractal dimension, SIM-A structure factor, SIM-C
  band-edge splitting — that they are structurally distinct. Report and
  figures are checked in **verbatim as delivered**; all audit content is
  confined to `README.md`, `CLAIM_TABLE.md`, `figures/README.md`, and
  `finite_n_control.py`. **Headline finding:** the drop shipped **two**
  dimension estimators and they disagree on the SIGN of the headline
  quantity — box counting gives `D_f(AB) − D_f(Cascade) = +0.334`
  (plateau) / `+0.240` (global), the sandbox mass-radius method gives
  `−0.247` / `−0.023` on the same five point sets. Only the
  box-counting family appears in the report; `sim_b_sandbox*.png` were
  shipped without being mentioned. There IS a good reason to prefer box
  counting — the sandbox estimator returns **1.913** for the Line
  control whose true `D_f` is exactly 1.000, an error larger than the
  effect under study — but the report reaches that outcome by omission
  rather than by checking the control, and states "Controls Validate
  Method" of the estimator it published while silent on the one it did
  not. **Second finding:** `finite_n_control.py` (stdlib only,
  deterministic) runs the matched-N control the drop skipped — the
  decisive gap is measured across a 12× sample-size drop (AB 12,000 pts
  vs Cascade 1,024) while the 0.021 baseline that licenses it is
  matched-N. Probes with known, N-independent dimensions move up to
  0.137 under that sample-size drop, and box-ladder commensurability
  moves a known fractal a further 0.115 at fixed N (Cantor dust, base-2
  ladder 1.304 vs base-3 1.189 against a true 1.2619) — an artifact
  budget of **0.252 against a reported 0.334, ~75% of it**. Budget is an
  UPPER bound, residual 0.082 a LOWER bound on structure, still 4× the
  0.021 baseline: **direction survives, magnitude does not**.
  **Third:** SIM-C's own section reports a null ("does not show a sharp
  threshold") and the OVERALL CONCLUSION enters it as positive evidence
  of "different threshold behavior" with no positive control — the
  `null-harness/` `CONSTANT_SILENT` failure exactly. **Fourth:** the
  `S(k)` figure shows one forward-scattering spike at the origin on a
  linear color scale, not the eight-fold Bragg star the text claims;
  what the figure does support is AB oscillating out to |k| ≈ 20 vs
  Cascade flat at ≈ 1. Eight claims (`AOS_001..008`) under a
  REFUTATION_PROTOCOL whose falsifiers are all *new* runs, since the
  generators were not shipped; `AOS_007` is `UNVERIFIED` (a gap, not a
  defect) and `AOS_008` records that the drop's substantive direction is
  probably right — the objection is to evidence strength and to the
  omission, not to the conclusion. Closest siblings: `null-harness/`
  (same never-fires invariant), `model-ecology/confound_sweep.py` (fit
  window as the largest invisible confound, reproduced here on a
  different substrate), `instrument-epistemology/` (the estimator is the
  instrument). CC0.
- `reasoning-gate/` — Fail-closed gate sitting between a simulation and
  its conclusions, and the direct follow-up to
  `aperiodic-order-sim-stack/`. Default is DENY: a sim that does not
  declare gets no output, an untagged quantity is not recorded, a ratio
  across unlike objects is void, a claim without named support does not
  enter the conclusion. Checks nothing about arithmetic — every failure
  it catches is one a correct program produces happily. Landed across
  two drops; **six delivered files are verbatim as received** (`gate.py`,
  `guards.json`, `make_docs.py`, `GUARDS.md`, `replay_sim_stack.py`,
  `README.md`), with all added analysis confined to `AUDIT_NOTES.md`,
  `retro_sim_stack.py`, `tests/`, and `samples/`. `guards.json` is the
  single source of truth and `GUARDS.md` is generated from it by
  `make_docs.py` — regenerates byte-identically, asserted by a test.
  Three layers (`generator` = property of the code that produced the
  data / `physical` = property of the modelled system, defensible
  outside the script / `instrument` = property of the measuring
  apparatus). Eight guards across three stages: PRE — `G-RES`
  (instrument × margin ≤ feature), `G-CTRL` (controls named with
  predicted values, "sized by fragility, not by expected surprise"),
  `G-PRE` (expected output written before execution); MID — `G-LAYER`
  (tag every quantity + name its object; no promotion without an
  explicit step); POST — `G-DIM` (a ratio needs both operands to be
  properties of ONE object), `G-SUP` (a claim names its supporting
  quantities), `G-FIT` (the statistic must discriminate; one blind by
  construction must be flagged), `G-IND` (convergence requires naming
  what the lines share). Pre-stage guards always deny; `strict=False`
  downgrades post-stage to findings. Two distinctions the design gets
  right: **G-DIM voids ratios, not comparisons**, and **G-IND does not
  forbid convergence claims** — it requires the shared input named,
  downgrading "independent" to "qualified". The delivered README is
  explicit that this is **n=1** — "a marker, not a position", one shape
  back-traced from a single paired sample — and invites reports of where
  it breaks; `AUDIT_NOTES.md` is the answer to that invitation.
  **Two replays that disagree.** `replay_sim_stack.py` (delivered)
  replays the audited stack with SIM-B sound: it PASSES, SIM-A is denied
  at `pre()` on G-RES, SIM-C runs but voids its ratio and loses its
  claim. `retro_sim_stack.py` (added) replays the same three mapping
  gate verdicts onto the audit's four findings, every input sourced
  `[R]`/`[F]`/`[C]`/`[G]` — and **DENIES SIM-B**. Same guard, same sim,
  opposite verdicts, because replay declares the box-count's *geometric*
  resolution (smallest box 0.05 vs mean NN spacing 0.20 → passes) and
  retro declares its *statistical* one (artifact floor 0.252 vs
  separation 0.334 → denies at the 2.0 margin). **`AUDIT_NOTES.md` §1:
  G-RES is only as strong as the pair declared, and nothing makes the
  binding pair the declared one** — not a bug, a limit on what the guard
  can promise. Related: the replay's declared error bar
  (`cluster_spread` 0.075, spread across three sets all at ~12,000 pts)
  excludes the 12× sample-size drop that `finite_n_control.py` measures
  at up to 0.137 on its own. **§2, the sharpest gap, visible in the
  delivered replay's own output:** `Df_cascade` is correctly tagged
  `generator` ("set by E_split, E_min, branch rule - not a tungsten
  property"), `summary()` prints `generator-level (no physical claim
  permitted): Df_cascade`, and the claim resting on it is recorded
  `[supported]` with `findings` EMPTY. G-LAYER guards the *tagging* of
  quantities, nothing guards their *use*; `claim()` computes
  `support_layers` and never inspects it. Substantively this is a
  sharper version of the audit's Finding 2 — by the replay's own
  tagging, "the two sets do not share a fractal dimension" compares a
  physical property of the AB tiling against a parameter of the cascade
  generator, i.e. a tiling against a piece of code. **§3:**
  `guards.json` labels `G-FIT` `"stage": "post"` so `GUARDS.md` renders
  it under POST, but `gate.py` enforces it inside `pre()` — a one-word
  fix in the JSON, since the doc is generated. **§4, four defects in
  `gate.py`** (locked into `tests/ShippedDefects` asserting current
  behaviour so a repair turns a test red): D1 the module docstring's
  usage example denies at `pre()` (now clearly deliberate — the replay
  uses the same two numbers for SIM-A — but unlabelled under "Usage");
  D2 `promote()`/`ratio()` silently overwrite where `record()` refuses
  to; D3 strict `close()` raises before writing the report and leaves
  the gate open, so a retry with a placeholder `control_result` yields a
  report whose controls block says `run: True` while a finding below
  says otherwise; D4 a registry missing a `fail_message` loads fine and
  raises `KeyError` instead of `GateError` when that guard fires — fails
  open at load, hard-crashes at denial. **SIM-A survives both
  declarations**: k-grid 0.39 vs finite-sample peak width 2π/L = 0.063,
  6.2× too coarse — the peaks fall between sample points, so SIM-A could
  not have resolved Bragg peaks whether or not they were there and its
  null carries no information about quasiperiodic order. 46 tests green.
  Siblings: `null-harness/` (G-CTRL is its invariant as a precondition
  rather than a measurement), `instrument-epistemology/` (G-RES/G-LAYER
  as the M0-M3 ladder made enforceable), `grounding-layers/` (same
  refuse-to-score-out-of-scope stance, one level down),
  `divergence-playground/` (G-IND is `agree_by_accident` as a
  precondition). Stdlib only, phone-buildable, CC0.
  **Third drop** lands `mine_logs.py` (guard hit rates + never-fired
  guards + "divergences with no guard attached" over a `gate_*.json`
  dir), `explore.py` (21 unranked widening probes across
  instrument/statistic/physical/disposition; "outputs candidates, ranks
  nothing, refuses to converge"), and `SIM_STACK_BACKTRACE.md` — the
  origin document named in `guards.json`'s `origin` field, with per-sim
  verdicts, six candidate PATTERNs, a confidence readout, and the n=1
  caveat. **AUDIT_NOTES §7-9 responds.** §7: the back-trace's SIM-A
  diagnosis is checked by a new
  `aperiodic-order-sim-stack/aperture_alias_demo.py` (stdlib, 1D probes
  with analytically known spectra) and **both halves hold**. The strong
  half is the floor tell — a quasiperiodic set has a PURE POINT spectrum
  so its between-peak floor sits BELOW the uncorrelated value; a
  Fibonacci chain (1D analogue of Ammann-Beenker) returns floor **0.09**
  against Poisson **0.99**, while SIM-A reports AB at 2.08 and cascade
  at 0.96 — inverted, and independent of any guess about grid spacing.
  The aliasing half is confirmed as a mechanism but
  configuration-dependent: a grid 86× the peak width misses 25 of 34
  Bragg peaks, the 9 hits being a 35/3 commensurability accident, and on
  the Fibonacci probe exactly 1 of 400 samples lands on a peak. **This
  corrected an error in the repo's own earlier audit** — the first pass
  conceded AB's |k| ≈ 20 oscillations were real structure when the
  refuting number (floor 2.08 vs 0.96) was already in the same
  paragraph; `AOS_006` revised, `AOS_007` upgraded UNVERIFIED →
  SUPPORTED. Caveat kept: the Fibonacci plain MEAN is 2.45, so if 2.08
  were a mean rather than a top-excluded floor a real quasicrystal could
  produce it — the comparison rests on the panel's "excl. top 1%" label.
  §8: the back-trace catches what the first audit missed on SIM-B — the
  report's "15× baseline" uses `|AB−Poisson| = 0.021`, the **smallest**
  of three pairwise gaps in the space-filling cluster, when the cluster
  spread is 0.075; honest ratio **0.334/0.075 ≈ 4.5×**, still decisive,
  not 15×. Converges with `finite_n_control.py` from the opposite
  direction (0.252 artifact budget → 0.082 residual): two routes, an
  effective error bar near 0.08. Recorded as `AOS_009`; `AOS_010` adds
  that no cascade number in the stack supports a statement about
  tungsten. §9: **two defects in the new tools.** `mine_logs.py` tests
  `expected != observed` on free-text strings, which are never equal, so
  its "growth edge" section flags every guard-free run — on the
  delivered corpus it flags SIM-B, the one sound sim. Deeper:
  **`mine_logs.py` is blind to denials** — a pre-stage deny raises
  before `close()` and writes no log, so G-RES reports `NEVER FIRED`
  *because it worked*; an operator pruning never-fired guards would
  delete the most effective ones first. Fix is on the gate side (write
  `gate_<SIM>.denied.json` before raising), which would also close D3's
  lost forensic record — one change, two defects. `explore.py` reads
  `sim` as `None` on a real gate report, since `sim_id` is top-level
  and `__main__` passes only `declaration`.
  **Fourth pass: all reported defects fixed.** `gate.py`, `guards.json`,
  `make_docs.py`, `mine_logs.py`, `explore.py` and both replays are now
  repaired rather than verbatim; `SIM_STACK_BACKTRACE.md` is untouched.
  Each defect keeps a test that asserted the broken behaviour first and
  asserts the fix now, so a regression turns it red. **D1** docstring
  Usage example now declares a resolution that passes, with the SIM-A
  numbers moved to a labelled `DENIAL EXAMPLE`. **D2** `promote()` and
  `ratio()` deny on name collision like `record()` does; the prior value
  survives. **D3** the gate now closes BEFORE denying, killing the
  retry-with-placeholder bypass entirely (a caller that catches the
  denial cannot call `control_result()` or `close()` again), and every
  denial at any stage writes `gate_<SIM>.denied.json` carrying the
  denying guard, detail, declaration and quantities-so-far;
  `control_result()` refuses an empty observation. **D4** the registry
  loader rejects any guard with a missing or blank `fail_message`,
  naming the offenders — fail-closed at load instead of `KeyError` at
  denial. **§2, the sharpest one:** `claim()` gained a `scope`
  (`physical` default, `generator` escape hatch); a physical-scope claim
  resting on generator-level support is recorded **`qualified`** with a
  `layer_note` naming the offending quantities plus a G-LAYER finding —
  downgraded, not refused, the same shape G-IND already uses. SIM-B
  still passes but its claim now reads `[qualified] ... ^ physical scope
  claim resting on generator-level support: Df_cascade`, so the summary
  no longer prints "no physical claim permitted" directly above a
  supported physical claim resting on one. **§3:** `G-FIT` stage
  corrected `post` → `pre`; `G-CTRL` is now `["pre","post"]` and
  `make_docs.py` accepts a string or list, rendering multi-stage guards
  under each stage with an "Also fires at:" line. **§9:** divergence is
  now `close(diverged=True|False|None)` — the author's explicit call,
  never inferred from two prose strings, so `mine_logs.py` stops
  flagging every sound run; it reports the real growth edge
  (`diverged=True`, no guard fired), lists unassessed runs separately,
  reads denial records, and shows findings vs denials in separate
  columns — G-RES now reads `1 denial` where it used to read `NEVER
  FIRED because it worked`. `explore.py` finds `sim_id` in a report or a
  bare declaration. Section 1 (G-RES is only as strong as the declared
  pair) was NOT "fixed" — it is a limit on what the guard can promise,
  not a defect. **Fifth pass, from using the gate elsewhere:** `G-LAYER`
  downgraded on generator-level support but said nothing about
  instrument-only support, so `measurement-fork/gate_fork.py` recorded
  `[supported] the measurement design has 3 unmeasured quantities` resting
  entirely on two instrument-level quantities — the same category move one
  layer over. Fixed: a physical-scope claim with **no physical-level
  support at all** is now `qualified`, deliberately narrow so it does NOT
  fire when physical support is present (a physical claim legitimately
  uses instrument quantities as bounds — "the separation exceeds the
  estimator's error bar" needs the error bar). And nothing had ever
  detected the five stale copies; `tools/check_gate_drift.py` +
  `tests/test_gate_drift.py` now do. 69 tests green. Stdlib only,
  phone-buildable, CC0.
- `reasoning-dial/` — A drop about how reasoning models allocate thinking,
  put through the gate the previous drop produced. Two delivered parts in
  `SOURCE_DROP.md` (verbatim): a 2026 survey of reasoning / learning /
  exploring / harnesses, and a proposal to treat **thinking budget as a
  measurable dimension** — an axis with gradients, cross-gradients and a
  knee, read with the same machinery the repo uses for physical fields.
  `dial_response.py` implements it (stdlib, deterministic) and checks the
  numbers the drop published. **The gradient transfers; the knee does not.**
  The delivered table (knee 26 / 910 / 66 tok for D_r 0.5 / 2.0 / 4.0)
  contradicts its own prose — the hard problem's knee is 14× EARLIER than
  the medium one's and its gradient twice as steep, where the text says
  later and shallower. Root cause: **"maximum curvature" names two points.**
  Any saturating curve has two curvature extrema, at `z = ±ln(2+√3)` on a
  logistic, **exactly equal in magnitude** (measured tie: `0.000e+00`), so a
  max-|curvature| rule chooses between tied candidates and the **sweep
  window** decides which is reachable. An independent implementation with
  different constants reproduces the small/large/small shape (76 / 716 / 38)
  with the flip on the same row: the hard problem's saturation shoulder sits
  at ~14,000 tok, outside a 10⁴ window, so only the take-off shoulder
  survives. "A knee that moves when you change the plot range is a property
  of the plot range" — `model-ecology/confound_sweep.py`'s window result on
  a new substrate, and the same defect as `AOS_005`'s SIM-C knee detector.
  **The fix is one word**: say which shoulder. Defining the knee as the
  saturation shoulder gives 76 / 716 / 14,170 with gradients 0.247 / 0.124 /
  0.074 — monotone in both columns, matching the prose. **The cross-gradient
  survives** (`∂²Q/∂lnB∂D_r` changes sign at an interior peak, D_r ≈ 3 at
  B = 1000) and is the drop's best idea, being the only part not requiring a
  knee. **`RD_005`:** RND is described as "the agent tries to predict the
  outcome of its actions" — that is the Intrinsic Curiosity Module (Pathak
  2017); RND (Burda 2018) matches a fixed random target network on the
  observation, and exists specifically to avoid the noisy-TV problem the
  misdescription attributes to it. `gate_dial.py` is the repo's **second
  cross-folder Python import** (after `msiaf-gdprf-bridge/`), pulling the
  gate from `../reasoning-gate/` rather than copying: DIAL-KNEE **denies at
  `pre()`** on G-RES (positional ambiguity 3.56 log-units vs a 2.99 knee
  shift), DIAL-GRAD **passes and splits** — identical support yields a
  `supported` generator-scoped claim and a `qualified` physical one, naming
  the missing experiment exactly (a measured quality-vs-budget curve from a
  real model would promote D_r from generator to physical) — and DIAL-SYNTH
  **qualifies** "four independent domains converge", since they are four
  sections of one survey written to a thesis stated before it. **Where the
  gate did not help**, recorded as a limit: G-FIT should have caught the
  knee ambiguity and could not — its rule is "name why the statistic can
  discriminate", its implementation checks a string is non-empty, and a
  wrong-but-fluent sentence satisfies it. That is `reasoning-gate/
  AUDIT_NOTES.md` §1 in a second instance, on a worse guard. `RD_009` logs
  the drop's proposed **G-STATE** (observer-state: am I cold, time-pressured,
  invested in a diagnosis?) as a real gap deliberately NOT built — a
  self-report from a miscalibrated observer is the quantity in question, so
  the gate could record it but not check it; the falsifier names what would
  make it buildable (tie it to cabin temperature, hours since sleep, a
  timestamp, and it becomes a two-number guard like G-RES). Nine claims
  `RD_001..009` including one `UNVERIFIED` (the survey's `cite
  web_search:NN#M` markers point at results not included in the delivery;
  Snell 2024, Titans, PRM800K, PURE min-form, Anthropic's backward
  rhyme-planning and `circuit-tracer` do check out). CC0.
  **Second drop** — a research landscape (`SOURCE_DROP_2.md`, verbatim)
  placing the framework against 2026 adaptive-computation work: marginal
  utility, BetaPRM, TRIM/R2R stepwise and token-level routing, metacognitive
  self-governance, the Gap Function, T² scaling laws. It does three things,
  all recorded internally since the citation markers again point outside the
  delivery and the papers are dated Jan–May 2026 (`RD_015` UNVERIFIED).
  **(1) It refutes MY response family, not the drop's.** The survey's central
  reported finding is negative marginal utility — past some budget more
  thinking flips correct answers to incorrect. A logistic is monotone
  (gradient measured 1.0e-08..6.3e-03 across the three difficulties), so
  `dial_response.py` **cannot produce overthinking at any parameter setting**;
  `RD_003` reported the family behaves well while that family ruled out the
  effect by construction (`RD_010`). **(2) It replaces the knee with a better
  primitive.** `overthinking.py` rebuilds the response as a logistic rise
  minus drift accruing per log-token; `argmax Q` — the zero of `dQ/d(log B)`
  on the declining side — is then unique, interior and window-independent
  (444 / 8194 / 224214 tokens, all passing an explicit `interior` guard
  against the RD_002 failure). Every RD_002 objection dissolves because the
  rule is **unnecessary**, the surveyed work's own primitive being marginal
  utility crossing zero (`RD_011`). Keeping the knee is expensive: on this
  shape it lands at **6–17% of the optimal budget, always early, error
  growing with difficulty** — worst where budget matters most (`RD_012`).
  **(3) It undercuts its own novelty claim.** The landscape closes "none of
  these papers explicitly compute cross-gradients"; six sections earlier it
  quotes one of them reporting that "easier problems reach negative marginal
  utility earlier than hard problems" — which IS the mixed partial, measured
  and stratified by difficulty, in prose. The quantity is already an object
  of study; the notation is what is not standard (`RD_013`). Smaller than
  claimed and still real: with drift held **problem-independent** the
  ordering 444/8194/224214 falls out rather than being put in (an easy
  problem finishes rising sooner so fixed drift overtakes it sooner), turning
  an empirical fact into a derivable consequence with a falsifier attached
  (`RD_014`). **The measurement that closes three claims at once** —
  `RD_007`, `RD_014`, and DIAL-GRAD's generator/physical split — is one
  experiment: estimate the drift rate on problems of different difficulty
  from measured quality-vs-budget curves. Fifteen claims `RD_001..015`.
  Shape-sibling to `equivalence-field/claim_lineage.py`: RD_010 is not wrong
  arithmetic but a missing dimension, and RD_011 is the child claim the break
  pointed at.
- `triad-playground/` — Every experiment as a tuple of three agents
  (physical system, measurement instrument, **reasoning agent**), each with
  its own dial. "The claim is only as strong as the weakest calibration in
  the chain." Delivered proposal verbatim in `SOURCE_DROP.md`; `triad.json`
  is the authored schema (agents, dial vector, calibration checks, shadow
  protocol, pedigree fields) and `CHECKLIST.md` is **generated** from it by
  `make_checklist.py` — same source-of-truth arrangement as
  `reasoning-gate/`'s `guards.json → GUARDS.md`. **The framing is the
  contribution and it holds** (`TP_001`): `reasoning-gate/` tags quantities
  `generator`/`physical`/`instrument` with no slot for the observer, and
  `instrument-epistemology/` grades six instruments with the reader outside
  the frame in all six; this supplies the missing fourth layer, with the rule
  that a physical-scope claim resting on reasoning-level support is
  `qualified` not `supported`. **The protocol as specified does not yet
  measure it** — three design results, provable without data, each with a
  cheap fix. **`TP_002`: step 5 forbids the design step 6 requires.** "Never
  upgrade all three simultaneously" is one-factor-at-a-time; "cross-gradient:
  did conclusion change with dial setting?" asks for an INTERACTION, and OFAT
  cannot estimate one at any number of runs. Demonstrated on a planted
  interaction: OFAT (4 runs) recovers the three main effects and predicts
  y(P=1,R=1)=3.0 against a truth of 6.0 — the entire interaction, invisible;
  a 2³ factorial (8 runs, ±1 contrasts) recovers everything exactly. The
  stated reason for OFAT ("can't attribute variance") is backwards.
  **`TP_003`: consensus is blind to the error shadows share.** The four
  shadows read one physical declaration, one instrument output and (for the
  AI shadows) one prompt written by a human shadow. Modelling each as
  `truth + shared_bias + individual_noise`, spread stays flat at ~2.04 while
  shared bias runs 0 → 20 and the error tracks it one-for-one: four shadows
  agreeing tightly at 120 when truth is 100 reads as a pass. Fix is mostly
  built — `divergence-playground/` is this protocol with the null attached
  (hash-sealed readings, three declared spread axes, `null_ensemble.py`), and
  its `agree_by_accident` flag is the cell the shadow pattern needs most.
  **`TP_004`: the proposed first experiment cannot fail its own skip
  condition.** A 1 m aluminium bar over 60 K moves 1.386 mm against a 0.01 mm
  dial division (139×, easy) — but the experiment is about OBSERVER variance,
  where reading spread ~0.005 mm sits at half the resolution, so four people
  reading one mechanical dial agree within a division by construction.
  `null-harness/` `CONSTANT_SILENT` plus `G-RES`. Fix needs no better bar:
  the instrument must log independently of the observer reading it (digital
  indicator + data log, or timestamped photo), making observer error a
  measured residual `|observer − logged|` instead of a consensus inference.
  **`TP_005`: the worked aluminium example shows physical mis-specification,
  not observer variance** — run 3's "wrought, not cast" reports that runs 1
  and 2 answered a question about a different specimen, so scoring it as a
  reasoning-dial gradient means every physical error the reasoning agent
  CATCHES inflates measured observer variance; `triad.json` check `P4`
  separates `state_revised_during_run` from `state_declared`. **`TP_006`:**
  three of four reasoning checks are self-report only (fatigue, emotional
  investment, conflict of interest); only the AI one is externally readable —
  `reasoning-dial/` `RD_009`'s G-STATE gap at system scale, with `readable`
  marked per check so `CHECKLIST.md` renders `[DECLARED]` rather than hiding
  it. **`TP_007` UNVERIFIED:** no triad experiment has been run, and the
  load-bearing empirical question — does observer variance matter at any
  scale worth measuring — is untouched. Falsifier: run it. Seven claims
  `TP_001..007`. Stdlib only, CC0.
  **Second drop: a generic v1 spec** (`SPEC_V1.md` + `spec_v1.json`,
  verbatim) delivered for reuse, with the question sharpened to *does the
  shadow pattern work with or without the human*. `shadow_panel.py` answers
  it by modelling each shadow as `truth + b_shared + b_family + e_ind` and
  reading the panel two ways — **N_eff** (participation ratio of the shadow
  correlation spectrum, the statistic `model-ecology/phylogeny.py` already
  computes) and **false-pass rate** (P(shadows agree | panel mean wrong by
  more than tolerance)). **`TP_008`, the answer: yes without the human, but
  the human's decorrelation must be REPLACED, not just removed.** Four model
  families with no human reach N_eff 2.18 / false-pass 12.4%, *stronger* than
  v1's required panel with a human (1.61 / 38.2%); adding the human back on
  top moves N_eff by −0.02. Drop the human from v1's panel without
  substituting and it collapses to N_eff 1.14 / false-pass **84%** — because
  `ai_low` and `ai_high` **on one model** share a family bias and are close
  to one shadow at two dial settings, leaving the human as the only
  decorrelated element. The design variable is independent failure modes,
  not human-vs-AI; the substitution is **three model families, not three
  budgets** (a procurement fact, not an epistemics problem). What a human
  still uniquely supplies is embodied context — cold-stiffened
  proprioception is not a failure mode any model has — which argues for a
  human shadow on *physical* measurements specifically, a different argument
  from decorrelation. Ranking survives a 5-point sweep of the variance
  components; absolute rates do not (`TP_013`). **`TP_009`:** the spec should
  require a minimum **N_eff**, not a minimum shadow COUNT — a four-shadow
  panel can carry N_eff 1.22, and counting shadows measures effort not
  independence. **`TP_010`:** v1 improved the consensus denominator from zero
  to *instrument resolution* and it is still wrong — instrument resolution
  bounds what the INSTRUMENT can say, shadow spread is bounded by what an
  OBSERVER can repeat, so the correct reference is same-observer repeat
  variance (which is also `TP_003`'s missing null). **`TP_011`:** v1 §5 now
  names `∂²/∂(physical)∂(reasoning)` explicitly while §2 rule 3 still says
  "upgrade ONE dial at a time" — sharper contradiction, smaller fix: rule 4
  ("never all three") would permit a 2² factorial over a pair, so replacing
  only rule 3 with "vary dials in a 2² factorial over the pair whose
  interaction is being tested" makes every mixed partial in §5 estimable at
  four runs per pair. **`TP_012`:** v1 §6 assigns `G-DIM` the job "checks
  that dial settings are actually different compute levels"; G-DIM voids
  ratios across unlike objects and does not do this — and the job named is
  real and unassigned, since **nothing verifies `ai_low` and `ai_high`
  actually produced different reasoning effort**, so a model ignoring its
  budget parameter collapses two declared shadows into one silently. The
  check reads like a G-RES pair (declared budget separation vs observed
  reasoning-token separation, with a margin). Thirteen claims `TP_001..013`.
- `measurement-fork/` — Take one system and design the measurement three
  ways at once, then diff the DESIGNS rather than the results. Four cells:
  **SOLE REACH** (a quantity exactly one arm reaches), **VOID RATIO** (same
  base name, different `object_of` or normalizer — they do not compare),
  **SAME QUANTITY, DIFFERENT ROUTE** (convergent; the conventional number is
  reusable as-is), **RESIDUAL** (open questions no arm reaches — the growth
  edge, and the product). Three arms: `conventional.py` (the design a field
  would actually run, written to be COMPETENT so gaps show up as gaps rather
  than mistakes), `coupling.py` (when a quantity is a RELATION between
  organism and environment, the standard instrument reads one side and
  reports it as a property of the organism; this arm generates the missing
  side and the ratio), and `widen.py` (options, not quantities; ranks
  nothing — descendant of `reasoning-gate/explore.py`). **The delivered
  package did not run**: `compare.py` imports `quantities`, `widen` and
  `validate`, none of which were in the drop, so both arms failed on their
  first import; all three are **reconstructed** here from the call sites,
  with `[CHOICE]` marking anything the call sites did not fix (`MF_001`).
  **The load-bearing design idea** is that a quantity is
  `(base, object_of, normalizer)` and two are the same one only when all
  three match — `reasoning-gate/`'s **G-DIM moved one stage earlier**, from
  report time to design time, which is the only point at which a mismatch is
  cheap to fix (`MF_002`). On the worked spec the `SAME QUANTITY` cell comes
  back **empty** and `compare.py` handles it as a result rather than an
  absence: the arms share no quantity at all, so no conventional result is
  evidence for or against the coupling questions — they are not disagreeing,
  they are not addressing the same quantities (`MF_003`). **Two defects,
  both found by null-testing the classifier** (`coverage_check.py`, the
  `null-harness/` known-null/known-signal invariant applied to a classifier):
  `MF_004` — `compare.py` pools every arm into `allp` including the widen
  arm, which its own output labels "options, not quantities", so a proposal
  to RENAME a question marks that question REACHED and the residual goes
  0-of-7 where measuring arms alone give 1-of-7; RESIDUAL is the one cell
  where a false COVERED costs most, and the fix is one line. `MF_005` —
  the 60%-of-distinct-stems threshold refuses two deliberate nulls and fires
  on a third that shares five of six stems with a single probe, so the
  failure mode is specific (a null built from ONE probe's vocabulary beats
  it, one built from the pool's does not); `compare.py`'s "not resolved
  here" caution on PARTIAL belongs on COVERED too, since COVERED is the
  verdict that removes a question from the list. **`MF_006`:** the drop also
  bundled `gate.py` + `guards.json`, both the **pre-repair** versions — a
  170-line diff with all seven repairs absent and both stage bugs intact
  (`G-FIT` still `post`, `G-CTRL` still `pre`). Neither is checked in; the
  repo convention is to IMPORT the gate (`msiaf-gdprf-bridge/`,
  `reasoning-dial/gate_dial.py`) precisely so it cannot drift, and this drop
  is that drift arriving on schedule. `MF_007` records the untouched
  question: on a real design, does the fork surface a quantity the designers
  had not considered? Seven claims `MF_001..007`. Stdlib only, CC0.
  **Second drop** delivers the canonical `quantities.py` and the real spec
  `provisioning_calibration.json` (both verbatim), plus three more stale
  `reasoning-gate/` copies. **`MF_008`:** the canonical schema enforces a
  CLOSED vocabulary — `OBJECTS = (organism, environment, coupling,
  instrument)` and `quantity()` raises on anything else — so a widen probe,
  which is about the *design*, **cannot be constructed as a quantity at
  all**. `MF_004` argued that from behaviour; the delivered schema reaches
  it from the type system independently: the schema refuses what the
  comparator then counts. `widen.py` now uses a local `option()` helper
  tagged `object_of="design"` plus `is_quantity(p)`, so the exclusion is
  mechanical. **`MF_009`, the sharp one:** on the real spec the classifier
  is wrong in BOTH directions and the errors point opposite ways — five
  questions marked COVERED by widen alone (false positive), and two
  questions a coupling probe was explicitly written for scored as unreached
  (false negative: `environmental` does not stem to `environment`, and
  `domain match ...` misses 4-of-7 by one). **No single threshold fixes
  both.** Three counts of the same cell: `0 of 9` as delivered, `5 of 9`
  with widen excluded, **`3 of 9` adjudicated by reading protocols** —
  zero understates, five overstates. **`MF_010`, the result:** the real
  growth edge is `coupling bandwidth`, `whether trust in own sensing is a
  measurement or a belief`, and `reversibility after regime shift`. The
  third has a stated prediction and no instrument — the predicted contrast
  is a RATE (fast vs slow relearn once the buffer is removed) and **no
  K-probe returns a rate**; every one measures a level, ratio, slope or
  variance at fixed regime. The stated falsifier ("ratio flat across the
  provisioning gradient") has the same shape: it needs the gradient swept
  and the probes sit at one point on it. One probe closes both — error
  against trials-since-shift, fitted for a time constant, at two or more
  provisioning levels. `residual_audit.py` is that adjudication.
  **Third drop: K14-K18.** `proposed_probes.py` adjudicates the five newly
  specified probes against the three gaps `MF_010` named, by reading
  protocols — `coupling.py` stays unmodified. **`MF_014`:** `K14
  practice_rate` is the **first probe in the arm that returns a rate**,
  which is exactly what `MF_010` turned on. One gap CLOSES (`whether trust
  in own sensing is a measurement or a belief`, via `K15`, because
  injecting a small KNOWN deviation scores the sensing apparatus against
  ground truth rather than against its own report); one goes PARTIAL
  (`reversibility after regime shift` — K14 supplies the provisioning
  gradient the stated falsifier needed, but nothing measures relearn rate
  AFTER the buffer is removed, and K16 is a latency swept against
  staleness at FIXED regime); one stays OPEN (`coupling bandwidth` —
  rate-of-use, staleness and latency are three quantities, capacity is a
  fourth). `K18`'s `object_of` is `design`, outside `quantities.OBJECTS`,
  so by `MF_008` it is a widen move not a probe — as its own specification
  says. **`MF_015`:** the mediation chain `K14 → K15 → K16` is the
  strongest part of the specification — refutable by a partial correlation
  on three measured series, with the direction of refutation named before
  the data exist, and not dependent on the effect being large. Its one gap
  is that **the lags are ordinal**: a mediation test sampled coarser than
  its own lag returns the chain collapsed into a single step, which is
  indistinguishable from the chain being wrong and would read as the
  falsifier firing. Declare the units and it becomes a `G-RES` pair,
  sampling interval against the lag being resolved.
  **Fourth drop: the `sweep` field and K11-K13.** `sweep_check.py`.
  **`MF_017`:** the stated rule — every probe declares which spec variable
  it must be run across and at how many levels, default `regime.variable`,
  min 2, point-probes declare `sweep=None` with a reason — is **not
  expressible in the delivered schema**: `quantities.probe()` has six fields
  and none is `sweep`, so **0 of 17** measuring probes across the three arms
  satisfy it. One schema gap, not seventeen oversights. Load-bearing rather
  than tidy, because the spec's own falsifiers are statements about a
  gradient ("ratio flat across the provisioning gradient") and a probe run
  at one setting of the control parameter cannot participate in one — **the
  missing field and `MF_010`'s unreachable falsifier are the same gap seen
  from two sides.** All six new probes pass; resolving the default against
  the spec's declared regime variable, 4 of 6 sweep it (2 by default, 2 by
  naming it), so the field carries information on 2 of 6 and K13/K14
  spelling out the default is a redundancy the schema should collapse.
  K15/K16 declare 3 levels against a minimum of 2, both being on the
  mediation chain where 2 levels gives a slope with no curvature.
  **`MF_018`:** the last two gaps `MF_010` named now close. `reversibility
  after regime shift` PARTIAL → CLOSED on **K13 `tau`** — `error vs
  trials-since-shift` is measured across a regime change by construction
  (trials-since-shift has no meaning without one), fitting tau returns the
  RATE `MF_010` said no probe returned, and sweeping provisioning supplies
  the gradient the stated falsifier needs; the prediction "tau rises with
  provisioning, flat tau falsifies" has a reachable null, so not the
  `CONSTANT_SILENT` shape. `coupling bandwidth` OPEN → CLOSED on **K11
  `information_rate`** — the capacity term the other three were not,
  explicitly marked `not_` against K01 delay and K02 reliability, with the
  honest blind spot "whether anything is done with the states". **K12
  reaches `MF_014`'s K15 distinction by a second route**: "trust is a
  measurement only if (b) was run" makes it a precondition on reading K12
  at all rather than a separate probe. All three of `MF_010`'s gaps are now
  reached — as specifications; nothing has been run, the mediation lags are
  still ordinal, and `sweep` is still not in the schema. Eighteen claims
  `MF_001..018`.
  **`MF_011`:** `make_docs.py` / `README.md` / `GUARDS.md` arrive as
  pre-repair copies too (12 / 16 / 48 differing lines) — five bundled
  files, five stale, across three drops, which is what copying instead of
  importing produces. Eleven claims `MF_001..011`.
- `declared-frame/` — A six-field block to attach to any measurement,
  model or claim (`boundary` / `horizon` / `who_counts` / `sign_source` /
  `logic` / `observer_access`), plus `check_frame.py`, which validates a
  block and tests two of them for comparability. Both delivered verbatim
  along with the worked panel-vs-leaf example. **The block holds**
  (`DF_001`): the fields are not interchangeable and `compare()` treats
  them three ways — `boundary`/`horizon`/`who_counts` are core and must
  match, `logic` gets a separate mismatch line, and `sign_source` /
  `observer_access` are recorded but never compared. That split is right:
  two results can share a boundary and disagree about which direction is
  better, and the disagreement is legible precisely because both declared
  it. **`DF_002`, the sharp one: the checker inverts the rule the doc
  calls load-bearing.** The doc says an omitted field "converts an open
  question into a settled one by silence" and `unknown` preserves the gap
  — so omission is the worse of the two. In `compare()` a missing core
  field is read as `str(a.get(f, ""))`, becomes `""`, and is compared as a
  VALUE: omitted → `NOT DIRECTLY COMPARABLE`, `unknown` → `UNDETERMINED`.
  Omission produces the MORE confident verdict, in the function shipped to
  prevent that. Three-line fix. **`DF_003`:** comparability is exact
  string equality on free text, so two frames whose boundary differs only
  in clause order come back NOT COMPARABLE — the inverse of
  `measurement-fork/`'s classifier, which over-matched where this
  under-matches. Under-matching is the safer direction and there is no
  band for it; there is no string fix, since whether two free-text
  boundaries denote the same accounting is a judgement. **`DF_004`:** `rc`
  tracks whether the blocks are well-formed, not whether the results
  compare, and does not say so — `check_frame.py a b && use_both` passes
  on two results the tool has just called incomparable. **`DF_005`:** the
  worked pair differs on all three core fields (panel excludes
  fabrication/mining/smelting/transport/installation/maintenance/
  decommission; leaf puts all of them inside the same photon budget), so
  the efficiency ratio between them is a frame difference — which is
  `measurement-fork/`'s VOID RATIO and `reasoning-gate/`'s `G-DIM` arriving
  by a third route. **Three tools, three stages, one rule.** `DF_006`
  UNVERIFIED: nothing has been attached to a real result, and the
  load-bearing question — does declaring the frame change what anyone does
  — is a claim about a process, measurable as whether two disagreeing
  parties given both blocks locate the disagreement faster. **`DF_007`,
  added from the `anchor-interval/` drop's layer-0 / layer-1 split:** every
  one of the six fields is layer 1 — switchable, declared, none privileged
  — so nothing in the block adjudicates. `layer_zero.py` puts two pairs
  through the unmodified `compare()`: one differing on `who_counts` (a pure
  convention) and one differing on a `boundary` that does not close (an
  input that physically crossed it entered the budget as zero). **Same
  verdict, `NOT DIRECTLY COMPARABLE`, for both** — so "this frame is
  internally coherent and does not match the shape" is not a statable
  verdict for the instrument built to make frames comparable. A seventh
  free-text field inherits the problem, since comparability here is string
  equality over declarations; the repair is an EVALUATED term rather than a
  compared one — inputs/outputs with units and one closure check, which is
  the `reasoning-gate/` `G-RES` shape, and which `measurement-fork/`'s
  `K18` already specifies as a widen move. Seven claims `DF_001..007`.
  Stdlib only, CC0.
- `anchor-interval/` — A drop about a system fitted to a corpus it also
  writes into. Notes verbatim in `SOURCE_DROP.md`; three of the structures
  in them are runnable and this folder runs them. **`corpus_loop.py`:** the
  loop `corpus → model → outputs → corpus` needs no adversary, only a fit
  that is not an identity map (`lam` — the shrinkage any regularized or
  capacity-limited estimator applies). Coupling to an unauthored substrate
  degrades 0.3604 → 0.4141 while both statistics computable from inside
  improve or go quiet (coherence 0.0677 → 0.0481, corpus shift 0.0520 →
  0.0035); at `lam = 0` the loop is a fixed point and the drift falls from
  +0.0537 to +0.0063, so the shrinkage carries it, not the feedback.
  **Two detectors, graded by `null-harness/`.** `D1` (model vs the corpus
  it was fitted to) is `CONSTANT_SILENT` structurally and gets QUIETER as
  the drift proceeds — it fell 29.0% while coupling error rose 14.9%,
  because it measures how much of the corpus the model has yet to write.
  `D2` (corpus now vs corpus then) has a reachable fire branch and on the
  known-null / known-signal sweep — the two arms identical in every line
  but the provenance of what is injected — comes back `NO_DISCRIMINATION`,
  and worse: **`FP ≥ TP` at every threshold**, since correcting a 0.35 bias
  displaces the corpus more than shrinking toward a pooled mean does, so a
  monitor tuned to fire on real degradation fires harder on real repair.
  Hence the anchor interval must be SCHEDULED — confidence-triggered
  anchoring fires in 0 of 24 generations and returns the no-anchoring
  number exactly, while scheduled anchoring recovers monotonically in
  frequency (0.3867 every-12 → 0.1629 every-2). **`moving_reference.py`:**
  "the model drifted" is a difference between two moving things reported as
  a property of one. Under `reported = a·c + b`, a capability rising 117%
  with a fixed ruler and a capability that never moves under a ruler
  stretching 117% produce the same published number to `5.6e-17` — a rank
  problem, not a precision problem. A held-fixed benchmark IS the right
  measurement and buys a SHARE, not a capability: it identifies capability
  only up to its own unknown gain and offset, so ratios of differences are
  identified (0.428571 exactly) and levels are not. Seven co-moving terms
  and one published number give `N_eff = 1.22` at loading 0.95 against an
  apparatus floor of 6.41 at loading 0 (participation ratio, the
  `model-ecology/phylogeny.py` statistic on a new substrate); and the
  co-movement is not removable by a better ablation because the
  architectural term was SELECTED against the corpus — attention shapes to
  language statistics, tokenizers to the writing system — so the covariance
  predates the experiment. **`recoverability.py`:** the drift literature's
  retrain remedy and the irrecoverability claim are not two opinions about
  one regime but two regimes, separated by one measurable quantity `f`, the
  fraction of the re-acquisition pool downstream of the system being
  corrected. Regime I (independent provenance) is entirely about
  scheduling — the optimal acquisition length is interior and finite and
  moves with the shift interval (`t_acq` = 6 / 12 / 25 at `t_shift` = 20 /
  60 / 200). Regime II (downstream provenance) floors at `f·b` and a
  10,000× increase in sample count buys nothing; above `f = 0.143` at bias
  0.35 and a stated tolerance of 0.05 the target is outside the reachable
  set at any `n`. Both sides lose something on a measurement neither has
  run: `f ≈ 0` collapses `measurement-fork/`'s `K15` into an ops step and
  fails the mediation prediction resting on it; `f` above the floor means
  the published remedy has a precondition it does not ask anyone to report.
  Eleven claims `ANC_001..011`, two of them deliberately not closed —
  `ANC_010` UNVERIFIED (the drop's own citation markers are unresolvable as
  delivered and one venue attribution is flagged unconfirmed by the drop
  itself, so no claim here rests on a literature fact) and `ANC_011` OPEN
  (the creek-crossing case — "literature contains what survives removal of
  the body" — with `inverseminar/`'s `CANNOT DERIVE` channel named as the
  instrument and no round yet run). Stdlib only, deterministic, CC0.
- `uninstrumented/` — Register of cases where a quantity exists and the
  instrument's constitution prevents it from appearing. **Not a gap log —
  a gap is an oversight; these are exclusions built into the apparatus
  before the first reading is taken.** Five-field entry structure
  (`QUANTITY` / `EXCLUDED BY` / `VISIBLE AS` / `WOULD MEASURE` /
  `CONFIDENCE`, the last stated separately from the shape and recorded
  verbatim rather than adjudicated) over a closed seven-mechanism
  vocabulary — `MODALITY` (apparatus in the wrong channel), `STORAGE`
  (medium cannot hold the shape), `SCALAR_DEMAND` (function collapsed to a
  number), `BUDGET_BOUNDARY` (closed budget compared to open),
  `AUTHORED_REFERENCE` (reference produced by the measured party),
  `AUDIT_ASYMMETRY` (guard fires on one side only), `SCORED_AS_WASTE`
  (component read as cost by the instrument's own accounting). Sorted by
  mechanism, not by field, so a case from evolutionary biology sits next to
  one from survey methodology. Seven entries; five have a worked instance
  elsewhere in the repo, which makes this a cross-index rather than a new
  claim surface. **`uninstrumented.py` does not only print the register —
  it tests it, three ways.** (1) `UNI_002`: the mechanism sort is UNTESTED,
  not confirmed — at 7 entries / 7 fields / 7 mechanisms the two partitions
  are identical, so nothing yet demonstrates the cross-domain grouping the
  sort exists for; the expiry condition is a second entry under an existing
  mechanism from a different field, and `reasoning-dial/` `RD_009`'s
  G-STATE gap is the nearest candidate already in the repo. (2) `UNI_003`:
  the mechanisms are NOT mutually exclusive — 4 of 7 entries have a second
  mechanism with a claim, so the filing is a CHOICE and should carry a
  primary plus a list, accepting that an entry then appears more than once.
  (3) `UNI_004`, the null test: every delivered entry states high confidence
  on the exclusion, so a list that only ever admits entries is
  `CONSTANT_FIRES` in `null-harness/` terms. Run against the six externally
  graded instruments in `instrument-epistemology/` as a known-null corpus —
  real apparatus, real chains, three graded "mostly assumed", the worst at
  chain fidelity 0.165 — **0 of 6 file**. `UNI_005` names the line that
  holds: **a reached-but-badly quantity has a blindness map; an excluded one
  does not, because the exclusion happens before the map is drawn.**
  `UNI_006` is the honest counterweight and is UNVERIFIED — all seven
  entries are uncontested and the null corpus was chosen for being well
  documented rather than for sitting near the boundary, so a classifier that
  never fires on the null has not been shown to fire on the signal. Six
  claims `UNI_001..006`. Stdlib only, CC0.
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
  - `check_gate_drift.py` — there is one gate. Finds every copy of the
    `reasoning-gate/` family anywhere in the repo, matched on **content**
    (two markers per file, one a code construct) rather than filename, so
    a renamed copy is still caught. Reports each `IDENTICAL` or `DRIFTED`;
    identical still gets reported, since the only reason a copy is ever
    stale is that it started identical. Also verifies `GUARDS.md` is what
    `make_docs.py` renders. Exit 1 on drift. Paired with
    `tests/test_gate_drift.py`, which fails the repo suite if a copy lands
    and plants a stale copy to prove the detector is not
    `CONSTANT_SILENT`. Written after five pre-repair copies arrived across
    three drops (`measurement-fork/` MF_006, MF_011) with nothing in the
    repo noticing. The checker identifies itself by content, not by path —
    a path-based skip breaks the one case it exists for, scanning a tree
    that contains a copy of the tool.
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
