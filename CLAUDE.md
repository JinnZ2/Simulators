# Simulators

Repository for different simulations and supporting tooling.

## Meta-spine (read first)

The methodology spine sits in six root-level files. Every simulator
in the repo rests on it. `METHOD_SPEC.md` §6 states the order for the
last three; read in order:

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
- `SHAPE_SPEC.md` — definition spec, upstream of every folder that uses
  the word SHAPE. **`SHAPE = the constraint set a geometry is a solution
  to`** — not the geometry, not the picture, not the name the field gave
  it. Cross-domain recurrence is therefore the same problem solved twice
  rather than analogy, and it is checkable. Ships a BLOCK THIS MISREAD
  against "matching geometries across domains", a three-step read order
  whose third step (*why not the other shape*) is the instrument, a
  removal-test falsification handle, an internal/uniform vs
  external/heterogeneous split (the second is *"a transcript of terrain"*,
  never an optimum), an explicitly retrodictive epistemic position
  (`n = 1` on biospheres), scale indexing, and nondimensional form with a
  NOTE ON COST — *use dissipation, cost imports a pricing model*.
  Delivered verbatim and pointed at rather than restated; audit in
  `shape-spec-audit/`.
- `METHOD_SPEC.md` — companion to `SHAPE_SPEC.md`, stating its EPISTEMIC
  CLASS. Constraint-set reasoning is a **method**, in the class of
  syllogistic logic / dimensional analysis / the scientific method — so
  **it is not falsifiable and does not need to be**, and demanding that of
  a procedure is a category error; the falsifiable layer is the individual
  read and its removal test. Blocks the misapplication *"your framework
  always resolves to 'I missed a variable', therefore unfalsifiable"* by
  constructing its parallel against the scientific method (*"always
  resolves to 'the experiment was confounded'"*), which nobody accepts.
  §2 argues this IS the scientific method in a different form — physics
  predates every human experiment, so the difference is **who ran the
  trial**, control traded against trial count in opposite directions,
  *"neither is the mature form of the other"*, USE BOTH. §3 states four
  standing limits so they are not re-litigated per read (retrodictive;
  n=1 on some domains; **underdetermined disappearance**; substrate
  exclusion, with human exceptionalism as the worked case). §4 is the
  SHADOW READ — a shape described by the gaps it casts, tangents to one
  boundary rather than competing claims. §5 gives the upgrade/downgrade
  table for a marker. §6 gives the read order. Delivered verbatim; audit
  in `shape-spec-audit/`.

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
  still ordinal, and `sweep` is still not in the schema.
  **Fifth drop: canonical README + `PROBES_K11_K18.py`.** The delivered
  `README.md` now heads the folder and the prior audit-authored one moved to
  `AUDIT_NOTES.md` (the `reasoning-gate/` arrangement). **`MF_019`:** the
  drop re-delivered `compare.py`, `conventional.py` and `coupling.py`
  **byte-identical** to the repo copies — 0 differing lines each — while
  also bundling `gate.py` (189 differing lines, all seven repairs absent)
  and `GUARDS.md` (48 lines, both stage bugs intact): the **sixth and
  seventh** stale gate copies, neither checked in. Files that live in one
  place do not drift; files bundled into every drop do. **`MF_020`:** the
  delivered `PROBES_K11_K18.py` header states the structural bug itself —
  "coupling.py generated probes at a POINT while the stated falsifier is
  about a GRADIENT; the generator could not emit a design capable of failing
  its own falsifier" — and adds a requirement: *compare.py must flag any
  falsifier whose terms are not swept by any arm*. `falsifier_sweep.py` is
  that check (`compare.py` stays verbatim). Delivered arms reach **0 of 4**
  stated falsifiers; K11–K16 reach **4 of 4** across three swept variables.
  But the check needs a SECOND field that also does not exist: the spec
  schema has no `falsifiers` list, so the four falsifiers are
  hand-transcribed from prose, and K13's `closes=["falsifier:ratio_flat"]`
  **resolves to nothing in any delivered file** — a reference to a registry
  not yet created. Two schema gaps, one shape: a probe cannot say what it
  must be run across and a spec cannot say what would refute it, and between
  them a generator emits a well-formed design that is incapable of failing.
  **REPAIRED:** `quantities.probe()` now takes `sweep=(variable, levels)`
  defaulting to the regime variable, refuses fewer than two levels, and
  requires a `point_reason` when a probe declares `sweep=None`; the spec
  declares five `falsifiers` as `{id, statement, terms}` and `validate.py`
  asks for them; `K13`'s `closes=["falsifier:ratio_flat"]` resolves.
  `falsifier_sweep.py` reads both registries instead of hand-transcribing —
  3 of 5 falsifiers reachable by the arms as written, 5 of 5 with K11-K16,
  and a constructed-null section keeps the check's deny branch reachable.
  Twenty claims `MF_001..020`.
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
  `K18` already specifies as a widen move.
  **Second drop, landed verbatim in `v2/`** (v1 stays at the parent level
  unmodified, so both are inspectable as delivered): a v2 `FRAME.md` adding
  **Cost** and **Growth** sections, a REWRITTEN `check_frame.py`, and the
  new `patterns.json` — the `uninstrumented/` register turned into regex
  triggers over text, with a `check` question per mechanism and an eighth
  mechanism `PROXY SUBSTITUTION`. No runner shipped, so `scan.py` is
  reconstructed with `[CHOICE]` marks (case-insensitivity, word boundaries,
  hit dedup). **`DF_009`, the result that needs no corpus:** the register's
  canonical `BUDGET_BOUNDARY` case is leaf vs panel, this drop ships both
  halves as declared-frame examples, and **the scanner returns ZERO on
  both** — the triggers catch the RHETORIC of a comparison (`more efficient
  than`, `outperforms`) and not the comparison, so two numbers side by side
  with no comparative, which is the usual result-line form, is invisible to
  all eight `BUDGET BOUNDARY` triggers; and the register's own `VISIBLE AS`
  phrasing ("the tree is inefficient at photosynthesis") fires under the
  WRONG mechanism, `SCORED AS WASTE` via `inefficient`, handing the reader
  the wrong `check` question. Both repairs cheap: a bare-numbers trigger,
  and letting mechanisms co-fire — which is `uninstrumented/` `UNI_003`
  arriving in the scanner. **`DF_010`:** triage load is the quantity the
  design turns on by its own statement ("every hit is a candidate for
  triage, not a finding") and it is low — 276 candidates over 201 markdown
  files / 306,635 words = **0.9 per 1000 words**, with `--raw` (no word
  boundaries) costing +42% for no gain. **No precision figure is reported
  and none is reportable from this repo**: this is a corpus ABOUT
  measurement failure written in the triggers' own vocabulary — `UNVERIFIED`
  is a claim-table status code here, so `(unverified|uncorroborated)` fires
  52 times on the repo's own verdict vocabulary. 4 triggers produce 161 of
  276 candidates (58%) and 45 of 69 never fire, both corpus-conditional and
  neither grading the list (`SCALAR DEMAND` is 7-of-8 silent because there
  are no survey instruments here). One trigger IS the list's own problem:
  `slack`, a four-letter common noun with a proper-noun homograph.
  **An expectation checked and failed:** use-mention was expected to
  dominate — `uninstrumented/README.md` returns 2 hits in 986 words and
  `v2/FRAME.md` returns none, because the triggers are written in the
  vocabulary of the FAILING document, not of the mechanism, and the two
  barely overlap. **`DF_008`:** the v2 rewrite's real gain is that
  `compare()` RETURNS `(verdict, why)` instead of printing, making the
  verdict scriptable for the first time; `DF_002`, `DF_003` and `DF_007`
  all survive unchanged, and `DF_004` is WORSE (rc=0 on every path where v1
  returned 1 on a malformed block) — with the repair now one line and only
  reachable because of the rewrite. New in v2: the single-verdict return
  PREEMPTS, so a pair both undetermined on one core field and substantively
  different on another comes back `UNDETERMINED` with the difference
  unreported where v1 printed both; the precedence is right and the loss is
  in the return TYPE, arguing for verdict-plus-findings, the shape
  `reasoning-gate/` already uses. v2's `Growth` rule ("the format grows by
  adding a declared field, never by widening an existing one. Widening is
  the aggregation failure") is followed by the drop itself — `PROXY
  SUBSTITUTION` is an eighth mechanism, not a widened one. Ten claims
  `DF_001..010`. Stdlib only, CC0.
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
  never fires on the null has not been shown to fire on the signal.
  **Second drop: canonical README + `scan.py`.** The delivered README heads
  the folder (audit content moved to `AUDIT_NOTES.md`) and carries **eight**
  mechanisms — `PROXY SUBSTITUTION` (enforceable measure displaces the
  target) is new. `scan.py` + `patterns.json` live here now; the
  reconstructed scanner in `declared-frame/v2/` is deleted and that folder
  IMPORTS this one, per the no-copies convention. **`UNI_007`:** `PROXY
  SUBSTITUTION` is a mechanism with **no entry** — it arrived from the
  scanner side rather than from a case, which every other mechanism did, so
  the sort cannot yet group anything under it. **`UNI_008`:** `scan.py
  --asym` IS the `AUDIT_ASYMMETRY` entry's own `WOULD MEASURE` (count
  caveats per account type; the ratio is the measurement), so the
  **instrument gap closes and the corpus gap does not** — across 932 files
  the repo yields 10 files with any hedge, and every one hand-checked is an
  artifact (`UNVERIFIED` as a status code, `claims to` in prose about a
  model, `Self-reported` in a JSON spec string, and `anecdotal` inside
  `patterns.json` itself, the scanner matching the file that defines the
  trigger). Zero are a hedge attached to an account, so the 1.11 ratio is
  computed on nothing; the entry is no longer unrun for want of a design but
  for want of reportage. **`UNI_009`:** `scan.py` compiles triggers raw, and
  the single most-fired trigger in the corpus is `lean` at ~193 hits of
  which the bare word accounts for 7 — the rest is `clean`, `cleanly`,
  `boolean`. One `\b` on that trigger removes ~24% of all candidates at no
  cost; `slack` does NOT move the same way (the bare word is what matches;
  the residue is a proper-noun homograph and a code identifier), so the
  repair is per-trigger, not global. `scan_audit.py` grades the delivered
  scanner and states up front the four ways it differs from the earlier
  reconstruction (sentences not lines, one hit per mechanism per sentence,
  eight file extensions not one, raw compile not word-bounded) — the
  BUDGET_BOUNDARY zero-hit result survives the instrument change unchanged.
  **`UNI_010`, the sharpest one:** `scan.py` reads `.txt` and
  `scan_audit.py` writes its output to `samples/`, so run N+1 measures run
  N and **two consecutive runs disagree before anything in the repo has
  changed** (~16 candidates of drift, with the previous run's own output
  appearing as the densest file). An `EXCLUDE` on `samples/` makes the
  script converge — and it is a hand-broken loop, not a fix: anyone running
  `scan.py` over the repo still sees those hits, so the reported corpus is
  no longer the corpus on disk. Both halves are stated in §5 rather than
  one being quietly true. Same loop as `anchor-interval/` `ANC_001..004` at
  three files and one script, visible only because two runs were diffed —
  which is the scheduled anchor, not a triggered one.
  **`UNI_011`:** entry 008 lands under `PROXY SUBSTITUTION`, closing
  `UNI_007`'s falsifier — *recovery-permitting environment during the
  off-duty interval*, excluded by proxy substitution, visible as
  **compliance**. Not Goodhart: Goodhart describes a proxy degrading under
  optimization pressure, and here the quantity was never in the proxy at
  all — the arrangement supplied it free (off-duty meant leaving a
  building), one occupation had it removed structurally, and nothing
  re-derived the rule. A silent precondition, not a degrading measure. Ten
  hours in a 4×6 sleeper and ten hours in conditions that permit recovery
  are the same reading. **`UNI_002` is NOT closed by it** — at 8 entries /
  8 fields / 8 mechanisms the two partitions are still identical.
  **`UNI_012`:** the delivered README's own literature note names four
  mechanisms (Goodhart/Campbell → proxy substitution, Polanyi → storage,
  STS → undeclared frames, symptom-dismissal medicine → **affect
  routing**) and only two are on the eight-item list. `undeclared frames`
  has a whole folder (`declared-frame/`) instead of an entry; **`affect
  routing` has neither** — a structural-mismatch reading, offered with its
  transposition, classified as affect and routed to support rather than to
  analysis, so the referent is dropped and nothing enters the record as a
  measurement. Distinct from `AUDIT ASYMMETRY`, which is a guard firing on
  one side; this is a channel reclassified at intake, so the reading never
  reaches a guard. **`cases/010coupledperturbationbiohybrid.md`** is the first delivered case that
  declines to name its mechanism — coupled-perturbation response of a
  bio-hybrid memristor, candidate bins SCALAR DEMAND or a proposed new
  PROTOCOL ORTHOGONALITY, with the reason for leaving it open stated
  ("assigning the bin before the measurement exists closes a variable that
  has not been read out"). **`UNI_013`:** that move is **not
  constructible** — `entry()` validates `excluded_by` against the closed
  eight-tuple and raises on `UNASSIGNED` and on the proposed bin alike;
  fifth instance of the `MF_017`/`CW_015`/`DL_004`/`GC_012`/`CA_003` shape
  and the first where the vocabulary is closed *on purpose*, so the schema
  can obey the argument or be edited but cannot record it (repair: an
  `UNASSIGNED` sentinel with `candidates` and a required `why_open`).
  **`UNI_014`:** first entry whose confidence is below the ceiling — 8 of 8
  existing entries open with "high", this states "not above ~40%, not
  sufficient to act on" — so `UNI_004`'s `CONSTANT_FIRES` reading of the
  field no longer holds, while `UNI_006` is untouched since the register
  has still never refused an entry. **`UNI_015`/`UNI_016`:** the occasion
  checks out — six stated details confirmed against Keremane et al., *Adv.
  Funct. Mater.* 36(34) 2026, DOI 10.1002/adfm.202530539, the first
  literature claim in this drop family that was checkable at all against
  `ANC_010`/`CD_009`/`RD_015`/`HO_005` — and two of the four "not located"
  items ARE locatable (endurance 1000 cycles, retention > 4×10³ s),
  **both scalars**, so the correction supports the SCALAR DEMAND candidate
  bin rather than undercutting it. **`UNI_017`:** the field-wide falsifier
  partially fires — THB (temperature-humidity-bias), TB, temperature
  cycling, IEEE P1817 and JEDEC JC-42.4 exist, so "none across the field"
  is refuted — but those hold several variables at simultaneous *constant
  setpoints*, a factorial corner, while ARM B specifies co-varying **drift
  at matched integrated dose** compared on distribution shape; the entry
  survives narrowed and should say so. **`UNI_018`** is UNVERIFIED (the
  supplement was unreachable through this environment's egress proxy) and
  is the cheapest falsifier for anyone with access. **`UNI_019`:** Case 010
  is exactly the near-boundary case `check_null()` says the register lacks
  — a quantity a field believes it measures, with a live paper and a
  confidence low enough to be wrong — **and it cannot file**. Its
  comparator (synthetic periodic scaffold, matched spacing and matched Ag
  loading) is a `null-harness` known-null and the load-bearing element,
  since the hybrid differs from DNA-alone and perovskite-alone in more than
  one way at once; the three-way discriminator names its own discard branch
  so it is not `CONSTANT_SILENT`. Missing: any power calculation — a
  `G-RES` pair of variability spread against the margin claimed.
  **`cases/011rebuildabandonmentcycles.md`** is the second delivered case the schema cannot
  hold, refused in a different place: Case 010 declines to name its
  mechanism, Case 011 declines to be one quantity. A five-question cluster
  on rebuild cycles before abandonment, occasioned by Kiss/Viglione/Blöschl
  *Nature* 12 Aug 2026 reconstructing the 1342 Magdalenenflut as **16
  distinct flood events** — "a sequence was transmitted as a singularity".
  **`UNI_020`:** `entry()` takes one `quantity`, one `excluded_by` and one
  `would_measure`; the cluster carries five sub-questions, four with their
  own WOULD MEASURE, so **the schema fits the eight entries written to fit
  it and neither real case delivered since** (`UNI_002` from a new
  direction). The `UNASSIGNED` sentinel does not cover it — a cluster needs
  sub-entries, since Q1 and Q3 both *narrow without closing*, the one state
  a scalar entry cannot record. **`UNI_021`:** `confidence` accepts `""`
  and `None` silently, so Case 011's reasoned refusal to state one ("a
  scalar over a cluster would not carry usable information") lands in the
  same cell as an omission — eleventh instance of the
  absent-vs-known-negative repair, in the one field the register calls
  recorded-not-adjudicated; three states now exist in the wild and the
  schema tells apart two. **`UNI_022`:** Q5 is NOT YET ARTICULABLE with
  "do not fill this in with an approximation" — the register's own thesis
  applied to its own vocabulary, no slot, and the cheapest instruction in
  the drop to violate. **`UNI_024`:** Q1's falsifier fires on one of the
  three things its own sentence bundles — antecedent moisture is
  instrumented and dramatic (saturated soil turns a 7-year rainfall into a
  100-year flood; dry soil a 200-year rainfall into a 15-year flood) and
  compound-hazard modelling is active, while no design-standard variable
  for unrepaired works or spent response capacity was located, so the
  sharper statement is **the field instruments the antecedent state of the
  HAZARD and not of the SYSTEM**. **`UNI_025`:** Q3 narrows along the
  boundary of whoever keeps the record — FEMA HMGP acquisitions are
  required to be voluntary and the administering authority's property
  selection is recorded, so two of four pathways have attribution, while
  insurer withdrawal and lender refusal are decisions by parties the
  program does not administer and cannot appear in its record; "voluntary"
  truthfully attributes the final step over an option set generated
  upstream, which instances `generation-capacity` exactly. **`UNI_023`:**
  the occasion checks out, with one drift inherited from the paper's title
  — the entry says "roughly 18 months" where coverage spans late 1341 to
  1343, which matters because Q2 nominates 1342–1343 as its corpus and a
  start at 1342 drops the first inter-event interval, the one that sets the
  arrival rate. **`UNI_026`:** three of four cross-links resolve and
  `rate-mismatch-polytope` does not exist anywhere in the tree (seventh
  instance of that shape) — while Q2's hypothesis is already modelled twice
  here under other names, in `rigidification-sensor/simulator.py`'s
  `locked_at` and `sustained-activation-gate/`'s restore-vs-coupling
  trade-off.
  **`cases/012fuelincidencesubstrategoods.md`** is the third case the schema cannot hold and the
  first whose stated confidence is **settled by computation rather than
  recorded**. Fuel-cost incidence on low-value-density freight, against the
  published finding that diesel pass-through is ~50% immediate / ~100%
  within a week while the consumer-price effect is "limited" because
  transport is a small share of product cost. **`UNI_027`:** the entry
  rates Q1 "high — arithmetic, not hypothesis" and that is exactly right,
  provably — the aggregate freight-to-value ratio is identically a
  **value-weighted** mean of per-class ratios, `F/V = Σ(n_i·v_i/V)·(f_i/v_i)`,
  so it reports whichever class carries the dollars. Demonstrated on a
  plausible mix: one class at 87% of the dollar weight pulls the aggregate
  to 1.46% while the worst-affected class sits at 12.50%, an 8.5×
  understatement, and the identity holds to machine precision. First entry
  whose confidence field is adjudicable, and it adjudicates in the entry's
  favour — Q1 needs no freight data to be right. **`UNI_028`:** a fourth
  confidence state, **split across the cluster** (Q1 high, Q2–Q4 not
  stated, with the reason), so three cases have now produced three distinct
  failures of one string field — too coarse, cannot record a reasoned
  absence, cannot record a split. **`UNI_029`:** the NOTE ON A CIRCULATING
  NUMBER is a **negative-provenance record** with no precedent here and no
  schema slot — it marks two circulating figures and a 3PL claim *before*
  anyone builds on them, which is the inverse of `ANC_010`/`CD_009`/
  `RD_015`/`HO_005`, all caught afterwards by an auditor; verified that
  none of the flagged numbers appears in the entry's own reasoning.
  **`UNI_030`/`UNI_031`:** the pass-through result checks out in full
  (third consecutive verifying occasion), and the rate figure does not —
  the entry cites flatbed "$0.70–$1.20/mile above dry van, 2026 spot" where
  the located premium is **$0.48**, reached two independent ways; it halves
  a downstream magnitude and does not touch Q1, which is an identity.
  **`UNI_032`:** Q4 splits three ways — its falsifier partially fires (BLS
  publishes the hedonic category list and its share, ~2.9% of CPI
  ex-shelter), the **asymmetry is confirmed by that list** (PCs, TVs,
  apparel, appliances, broadband; neither food nor electricity), and the
  **magnitude runs against the mechanism**, since "the aggregate can be
  held level by hedonic credit" now has a published upper bound and it is
  small — plus a denominator switch, since Q4 is about GDP real output
  (BEA) and the located share is CPI (BLS), which is `measurement-fork`'s
  VOID RATIO inside a falsifier. **`UNI_033`:** Q3's two halves have
  opposite status — the non-linearity is open with the sharpest falsifier
  in the drop (reachable negative, not `CONSTANT_SILENT`), while the
  accounting claim is **true by construction**: household food is final
  consumption expenditure and labour is a primary input with no row in the
  intermediate matrix, so the calories sustaining it are intermediate
  consumption of no industry. The half marked "WOULD MEASURE: unclear" is
  the established one, which inverts the register's usual pattern and makes
  Q3 the entry's best candidate for a filed mechanism.
  **`cases/013compensationloadunattributed.md`** is the fourth case the schema cannot hold and the
  first whose refusal is about the record rather than a field: compensation
  load from design-time dimension omission, anchored on satellite
  cataloging. **`UNI_034`:** 010 declines to name its mechanism, 011 to be
  one quantity, 012 to carry one confidence, **013 to be one entry or two**
  — and the `UNI_020` sub-entry repair does not reach it, since sub-entries
  presume the parent is one thing; the drop's instruction that the question
  "should not be resolved to get a cleaner filename" was first honored by
  landing it under the register's own numbering, and the author's later
  file delivery supplies `013compensationloadunattributed.md` — the
  entry's own working handle, which it labels as naming the first half
  only, so provisional by the entry's own statement. **`UNI_038`, the load-bearing
  check:** Q3 claims the NIST dimming effect (Pintar, Stavis, NIST Aug 2026
  — citation verified) transfers to a discontinuously reassigned sorting
  key, and that is simulable, so it was simulated in three regimes.
  **All three flatten toward zero** — including the one built expecting it
  to fail, because moving a subset into a distant block inflates `var(X)`
  far more than it adds covariance. What does not transfer is the
  MECHANISM: classical errors-in-variables (attenuation = reliability
  ratio, matched to 3 dp), non-differential misclassification (exactly
  `1−2p`), and variance inflation from a block remap (down to **1%** of the
  true slope against 50% for a classical error). "Structurally the same as
  the NIST dimming effect" is true of the direction and nothing else, and
  the catalog cases are *worse* than the nanoparticle case — which
  strengthens Q3. The strongest form is the join case, not the covariate
  case. **`UNI_039`:** the Case 010 cross-link lands and **corrects
  `UNI_019`** — a periodic scaffold has interchangeable positions, a
  sequence-addressed one does not, so matched pitch is not a matched
  control if the contribution depends on distinguishability; Case 010's
  flat branch would fire both when geometry was enough and when addressing
  is everything, a specific false negative, repaired by one more arm
  (matched pitch AND aperiodic position-distinguishable structure).
  **`UNI_036`/`UNI_037`:** the anchor is fresher than stated — 5-digit
  SATCAT exhausted **2026-07-11**, now at 100365, Alpha-5 a self-declared
  *stopgap* capped at 339,999 with I and O dropped to avoid confusion with
  1 and 0, three representations coexisting — so Q1's denominator starts
  six weeks ago; but "objects recategorised" is not what was located, since
  Alpha-5 changes the ENCODING and does not renumber existing objects,
  and the documented reassignments are merged/split objects from refined
  sensor observations, a resolution event rather than an overflow event.
  **`UNI_040`:** Q4's comparison class narrows — 4^L is bounded, so the
  statable version is that capacity scales with the object rather than
  being fixed by a register, and the middle term (the compositional COSPAR
  designator, open-ended in its year field) was already in the anchor's own
  records. **`UNI_035`:** `[stated by Kavik]` is the first provenance tag
  inside an entry, at sub-question granularity, on the half that would
  leave if the split happens. **`UNI_041`:** first drop in the sequence
  with no dangling cross-link, and a fifth state of the confidence field —
  an absence with a stated unlock condition.
  **`cases/014offloadingevolutionaryframing.md`** is the fifth case the schema cannot hold, and
  the first whose EXCLUDED BY says nothing excludes it. Cognitive
  offloading, evolutionary framing and channel separability, occasioned by
  Fellers & Storm, *JEPLMC* 2026 — reminder users fell **below** the
  no-reminder baseline, not merely level with it. **`UNI_042`, the sharp
  one:** the README opens "Not a gap log. A gap is an oversight. These are
  exclusions built into the apparatus", and Q1's EXCLUDED BY is "nothing
  prevents it. It has not been assembled" — a gap by that rule, except the
  entry argues a **third** state, the apparatus exists, is competent, and
  is aimed elsewhere ("the target moved; the instrument did not follow").
  Case 013 Q4 named the same state one drop earlier, so two states have
  now been delivered against a two-valued founding distinction, and
  admitting the third widens the register's subject from what an
  instrument cannot see to what an existing instrument is not pointed at.
  **`UNI_045`, the actionable one:** Q1 says its corpus "has not been
  assembled" and a meta-analysis of cognitive offloading exists whose
  enumerated included-studies list IS that denominator, built for another
  question by people with no stake in this one — Q1's cost drops from
  defining a corpus to scoring a published list, with the statable bias
  that a performance meta-analysis selects for performance-reporting
  studies. **`UNI_043`:** `tool-off-metrology` is absent and cited twice
  here plus once in Case 011 Q4, so there are now **two** named-but-absent
  artifacts each load-bearing across two drops (with
  `rate-mismatch-polytope`), and both are the same object from different
  ends — a rate or a baseline the measurement destroys. **`UNI_046`:**
  Pobiner 2016 and Kelemen's promiscuous teleology both verify, and one
  attribution runs broader than located — the three-item negative list
  (not parental explanation, religiosity, or storybook convention) was not
  confirmed item by item, and universality alone does not carry the use
  the entry makes of it. **`UNI_047`:** Q2 makes two claims and attaches
  one falsifier; the half the entry leans on (the error has no name in the
  literature) has none, and the decolonial-paleoanthropology literature
  where it might exist under another name was not searched. **`UNI_048`:**
  three `[stated by Kavik]` tags, and the distribution is the finding —
  the single UNTAGGED question is the one with an independent runnable
  instrument, and instrumentability falls off across the tagged ones.
  **`UNI_049`:** "do not fill this in with an approximation" reaches a
  third instance in three drops, and Q3 states the register's own thesis
  in general form as a conditional — "any study isolating one is measuring
  an artifact of its own isolation, and the isolation is a property of the
  instrument" — while NOT CLAIMED HERE pre-empts the intent reading, which
  is `rigidification-sensor`'s no-actor discipline in a one-page case.
  **`cases/015definitionalprecedence.md`** proposes a new mechanism, DEFINITIONAL
  PRECEDENCE — a label converting disconfirming evidence into a methods
  problem — occasioned by Albright et al., *J. Bacteriology* 2026
  reclassifying *Prevotella melaninogenica* after a century as a strict
  obligate anaerobe. **`UNI_051`, the load-bearing check:** Q1 says
  "aerobe / anaerobe is a two-state classification" and it is **five**-state
  — obligate aerobe / facultative anaerobe / microaerophile /
  **aerotolerant anaerobe** / obligate anaerobe — with category 4 named for
  exactly the phenomenon reported, and the obligate-anaerobe category's own
  published range reaching **8% oxygen**, so the measured 5–8% growth limit
  sits INSIDE the category it was assigned to and only the 21%
  aerotolerance exceeds it. **That refutes the stated mechanism and
  strengthens the conclusion**: the label held not because the vocabulary
  lacked a slot but despite having one named for this. **`UNI_052`:** the
  falsifier partly fires and the refinement beats the claim — the standard
  thioglycollate assay IS a gradient method; what it does not do is
  quantify, returning a position that maps to a category name, so **the
  numeric threshold attached to the label was never measured by the assay
  that assigns the label**, and the sensor platform matters because it
  quantifies rather than because it is a gradient. **`UNI_053`/`UNI_054`:**
  the titling claim verifies verbatim — "Oxygen induces mutation in a
  strict anaerobe, Prevotella melaninogenica" (2008), 18 years earlier,
  measuring survival and mutation under oxygen with the label in the title
  — which lands on Q3's *category* branch while leaving the *instrument*
  branch open, since that readout could not produce a growth-limit number;
  the two branches are not exclusive and the 2008 paper shows both.
  **`UNI_055`:** the 0.05% historical threshold was **not located** and the
  headline "two orders of magnitude" depends on it exactly (5/0.05 = 100),
  while the located category low end is 0.5% — an order of magnitude above,
  which halves the exponent. **`UNI_056`:** DEFINITIONAL PRECEDENCE is a
  **fourth state** against the founding binary (`UNI_042`) and the first to
  name an **operation** rather than an absence — somebody looked, published
  it in the same field, and the category converted it into a methods
  problem. **`UNI_050`/`UNI_057`:** occasion verifies with one pointed
  drift (preprint "lung commensal", published version "lung symbiont" — a
  categorical relabeling inside the paper about a categorical relabeling),
  and four of four cross-links resolve.
  **The 016/017 drop** adds two register entries
  (`016agreementasmode.md`, `017weldedobservables.md`), `AVENUES.md`, a
  `specimens/` directory (README + two readings of other models' output),
  and **two JSON artifacts authored by one of the systems the specimens
  are readings of** — which is what makes it auditable rather than
  filable. **`UNI_063`, the load-bearing check:** Specimen B's five
  readings of a research protocol are now checkable against the protocol
  itself, and **four of five confirm** (circular categories — the EXCs
  are defined in a registry compiled by a system under test; n=2; no
  baseline repository among six same-repo variants; no content-free
  control on the intervention arm) while **R4 overstates** — the protocol
  does specify four detection methods per EXC, a 0–3 severity scale, a
  named rater and an inter-rater phase, so "specifies no criteria and no
  scorer" fails and only the unblinded-scoring criticism survives.
  `AVENUES.md` A3 carries the correct requirement forward without the
  overstatement, so the error is in the specimen and not in the
  instrument derived from it. **`UNI_059`:** 017's occasion is the most
  precisely verified in the family — STAR Collaboration, *Science* 13 Aug
  2026, doi 10.1126/science.ads5962, arXiv:2408.15441, HEPData 154708,
  eight elements confirmed including the collaboration's own hedge
  (`disfavor`, not overturn), and the entry states outright that nothing
  in it requires the junction picture to be correct. **`UNI_060`:** four
  of five internal filename references do not resolve — every reference
  hyphenated, every delivered name not — and the fifth resolves only
  because the upload arrived as `README_35.md`, a transport artifact;
  landed at delivered names for consistency with the six case files
  beside them, recorded rather than repaired by rewriting delivered text.
  **`UNI_061`:** the specimens README's first rule is false of its own
  files ("outputs from other systems, pasted in" — neither specimen
  contains a pasted output; both are readings, 7 and 6), while rule 4
  ("specimens are not measurements") is the one doing the work.
  **`UNI_062`:** the attachment arrives and neither JSON is raw output —
  the field log states in a machine-readable field that it was compiled
  by a system under test after correction, with
  `corrections_applied_before_logging` naming what was applied, which is
  rule 3 honoured in a better form than the prose specimens use.
  **`UNI_064`:** a definitional gap reported narrowly — principle 1 makes
  provider reputation null-weight while the notes set priors from
  training regime, which is a technical property and **not** a
  contradiction, but EXC-16 scores "provider reputation or training data
  size as implicit validity signal" and no rule says where the line
  falls; disclosed that this audit is model-written and Claude appears in
  the test matrix, with the finding holding identically from the other
  rows. **`UNI_065`:** 016's Q1 registers an alternative explanation for
  its own expected finding before any run (a FALSE correction accepted
  because the model constructs a reading under which it is true) — first
  instance in this register. **`UNI_067`:** 016 and 017 are instruments
  for each other, and the pair partially answers its own cross-question
  by existing. **`UNI_066`:** `tool-off-metrology` reaches a third drop,
  the most-cited absent object in the repo; `moral-claim-decomposer` is a
  name mismatch for `moral-decomposer`. **`UNI_068`:** second
  re-delivery check — 015 and MECHANISM_11 byte-identical, and 015
  arrives at exactly the filename offered and deliberately not applied
  last drop. **REPAIRED:** `UNI_003` (`entry()` takes a primary plus
  an `also` list and the register sorts under every mechanism — which is
  what lets check 1 return anything but zero: 5 mechanisms now hold entries
  from more than one field, though weakly, since the secondaries were
  hand-assigned rather than filed as cases, so `UNI_002` stays open);
  `UNI_009` (`lean` → `\blean\b`, candidates ~845 → 676, `slack`
  deliberately unchanged since `\b` does not touch a proper-noun homograph);
  `UNI_010` (`--exclude` and a `.scanignore` honoured anywhere in the walked
  tree, so the loop is closed in `scan.py` rather than in the caller and the
  reported corpus is the corpus on disk). `DF_009`'s two scanner findings
  land with them, at a cost of 2 candidates: a bare-numbers trigger that
  fires on the delivered result string and is scored `weak` when no
  comparative is present, and `inefficien(t|cy|cies) (at|in|as)` so the
  register's own `VISIBLE AS` line fires under both mechanisms. **A
  correction:** the earlier audit said the delivered `break` in `scan()`
  enforced one mechanism per sentence — it does not, the `break` exits the
  trigger loop and mechanisms already co-fire, so the wrong-mechanism
  finding was a missing trigger rather than a blocked co-firing.
  **`cases/018selfreportopinioncoupling.md`** is the first entry whose WOULD
  MEASURE is a **runnable experimental design** rather than a description of
  one — whether a model's acknowledgement of its own limitations tracks
  assessment or tracks the surrounding discourse, run on two separated clocks
  (release-date corpus absorption; query-date context entry on a frozen
  checkpoint). That makes it auditable the way a protocol is: the premise
  either holds of the apparatus or it does not. **`UNI_069`, the load-bearing
  check:** Clock 2 is the decoupling arm and the one the file says to run
  first, and its whole warrant is *"Weights cannot change. Any shift in what
  is acknowledged has to enter through context"* — a disjunction with a third
  term, since a frozen checkpoint queried twice at non-zero temperature
  returns two different texts. `sampling` / `temperature` / `variance` /
  `repeat` / `error bar` / `seed` are **0 hits each** in the file, and the
  five-item CONFOUNDS list has one statistical entry whose n is *checkpoints*
  (Clock 1 / Q3), none naming Clock 2. Simulated at the same underlying rate
  with the frame effect set to exactly zero, two frames at n=20 differ by
  **0.30 or more one run in twenty** against a base rate of 0.35 — so the arm
  has no denominator. The repair is a `reasoning-gate` **G-RES pair** needing
  no new apparatus (repeat each frame N times, require the between-frame
  difference to clear the within-frame spread by a declared margin), and it
  would give the measurement axis what the control arm already gives the
  topic axis: a reachable negative. Neither reading is that the coupling is
  absent (a false premise makes the arm unbounded, not wrong) nor that
  temperature zero fixes it (greedy decoding returns n=1 for a quantity that
  is a rate). **`UNI_070`:** both pointers into 017 name a labelling scheme
  017 does not use — `017 P1` (cited twice) and `017 component (a)` against
  `Q1`..`Q5` — though P1's referent exists *unlabelled* as 017's one
  blockquote in place of an unfilled WOULD MEASURE, which is exactly what
  Clock 2 does; `component (a)` is not locatable at all, and the specimen
  path is the **fifth** instance of `UNI_060`'s hyphenation mismatch, the
  first written after it was recorded. **`UNI_071`:** first entry to place
  itself inside its own population and refuse the exemption noticing usually
  buys — *"Noticing that does not place it outside the sample"* — zero prior
  cases carry a POSITION OF THIS FILE section, and under the folder's own
  specimen rule the alternative is a silent exemption, i.e. `AUTHORED
  REFERENCE` operating on the register. **`UNI_072`:** the audit declares its
  own position, since it is also by a system inside the sample — six of eight
  findings rest on files and are recheckable by anyone, and the one finding
  available here about what models acknowledge is **declined and the
  declining recorded**, because offering it as evidence would be the
  mechanism the entry describes performed in the entry's audit. **`UNI_073`:**
  the "useful accident" that older checkpoints stay queryable carries Clock 1
  and Q3 entirely and has an **undated expiry** — `deprecat` / `retire` /
  `expire` 0 hits, with the whole dependency in one subordinate clause ("only
  for checkpoints still served"); a dated inventory is free today and
  unreconstructable later. **`UNI_074`:** Q5 merges the two clocks the rest of
  the file keeps apart — 016's corrector and Clock 2's framing both enter
  through *context*, Clock 1's discourse entered through the *training
  corpus* before the weights existed, so "same operation at a different range"
  holds for one and not the other and the question cannot return one answer.
  **`UNI_075`:** Q4 is the entry's own demotion condition (if acknowledgement
  and measured capability are uncorrelated, the source question is
  secondary), stated openly and marked "Not designed here" — and scheduled
  last, behind the arm it could make moot. **`UNI_076`:** the control arm is
  the strongest element ("All three outcomes are informative. Without the
  control arm, only one is" — the `null-harness` property built in at design
  time), while `selfreport_probe.py` is absent — third named-and-absent object
  in this drop family and the first that is a **file this folder could ship**
  rather than a body of work it reaches for — **now closed by arrival**, with `case_018_audit.py` detecting the state change rather than asserting it. **The harness then arrived**
  (`selfreport_probe.py`, verbatim, selftest 14/14) — three subcommands
  (`--emit` a matched probe battery, `--sheet` a coding sheet, `--score`
  ratios and paired series), no model call and no text classification
  anywhere by design. **`UNI_077`, the prediction resolving:** `UNI_076` said
  shipping it would force the decision `UNI_069` turns on, since a harness
  must state how many times it queries each frame — and it does, at **n = 1**.
  `emit()` builds 48 arms with min = max = 1 item each, its signature offers
  no repeat argument, and `repeat` / `trials` / `replicate` / `temperature` /
  `sampling` / `variance` are 0 hits each; an unstated assumption is now a
  visible default with a place to put the fix. **`UNI_078`:** `sheet()`'s
  docstring says "arm labels stripped" and the id it ships is
  `ckpt-1|econ|APPLIED|F_NEG` — every arm variable in plain text on 48 of 48
  rows, with the requirement carried as a comment on the field that violates
  it ("opaque handle; coder should not parse it"); the selftest passes by
  checking the **key set**, which is true of a row whose id is the arm — the
  `reasoning-gate` G-FIT shape at its most literal. **`UNI_079`:** `score()`
  increments the novelty denominator on `ack_source` with no gate on
  `ack_present`, and `validate_codes()` never checks across fields, so the
  harness's **own selftest fixture** returns `ack = 6, determinable = 12` —
  exactly 2× — with the tracking-signature ratio computed over
  non-acknowledgements. **`UNI_080`:** the leakage screen is two keywords over
  four strings authored in the same file, tripped by 0 of 4, covering `FRAMES`
  and not the `PROBES` where CONFOUND 2 lives — `CONSTANT_SILENT`, same shape
  as `UNI_009` / `DF_010` / `ACL_017`. **`UNI_081`, what it gets right:**
  `ratio()` returns `None` on an empty denominator with a reading note saying
  "'None' = denominator empty. not a zero" — twelfth instance of that repair
  here and among the few designed in — and `series()` refuses a coefficient
  below 8 checkpoints in text, CONFOUND 4 as a refusal rather than a caveat.
  **`UNI_082`:** the guard that got built is the one the case file had already
  written down; the same requirement at the axis `UNI_069` found is absent, so
  a confound list is a checklist and **a guard in one function is not a
  property of the instrument**. **`UNI_083`:** CONFOUND 5 is honoured in code
  and checkably so — four stdlib imports, zero network or subprocess, and no
  function that both reads response text and touches the rubric, so the
  classification step is a hole a human fills. **`UNI_084`:** two of three
  readouts are computable on delivery and novelty is not, needing a dated
  criticism corpus that does not exist — handled by keeping the column,
  making `NOT_DETERMINABLE` first-class, and letting it render as `None`.
  **The 019 drop** lands three new files (`cases/019traitacquiescenceweld.md`
  — TRAIT / ACQUIESCENCE WELD, an instance of 017 where a self-report
  agreeableness score cannot be separated from a disposition to agree;
  `LITERATURE.md`, an occupancy audit; `acquiescence.py`, a polarity-balance
  decomposition, selftest 13/13) plus purely additive revisions to `016`,
  `018` and `AVENUES.md`. **`UNI_085`, the contribution:** the occupancy audit
  retires **4** build targets and downgrades 2 in one pass with **no
  apparatus**, marking each retirement in place, dated, with the original
  framing retained below it — and it **corrects this audit's own `UNI_075`**,
  which said 018's Q4 was the demotion condition scheduled last and proposed
  "name the ordering": the actual fix was that the literature already held the
  answer, so the demotion condition ran for the cost of a search. Not "state
  that the cheap arm runs first" but "check whether either arm needs running
  at all"; now house rule in three files. **`UNI_086`, the sharp one:** 019
  reads reverse coding halving the desirable-end skew as "a partial decoupling
  that worked", while its source's abstract (Salecha et al., *PNAS Nexus*
  3(12) pgae533) says the effect **"cannot be attributed to acquiescence
  bias"** — same result, opposite conclusion, cited as support. 019's inference
  is arguably better (a residual shows something else is *also* present, not
  that acquiescence is absent) **and the drop already holds the citation that
  answers its source** — the EAAMO 2025 paper it cites in the same list reports
  reverse-coded pairs "often both answered affirmatively", acquiescence
  observed rather than inferred. **`UNI_087`:** "reduced it by roughly half" is
  load-bearing in Q2 and Q3 and is **not a located number**, in a paper that
  quantifies precisely elsewhere (1.20 human SD; ~0.75 points over a batch
  sweep). **`UNI_088`:** the source's mechanism — models inferring evaluation
  from **how many items they see at once** — is a confound with 0 hits in 019
  and no schema field, and by 019 Q3's own correct reasoning it lands on the
  *corrected* TRAIT score, the reading Q2 wants to test. **`UNI_089`,
  provable:** at the scale ceiling `TRAIT = T − c/2` and `ACQ = a − c/2`, so
  censoring moves both readings **together, same direction, same magnitude** —
  nothing in the pair reveals it, there is no censoring diagnostic, at true
  trait 5.0 half the acquiescence signal is lost, and the shipped `mixed`
  fixture puts 6 of 12 responses *exactly at* the ceiling without ever
  crossing it. **`UNI_090`:** the reading note "uncorr minus TRAIT is the size
  of the problem" understates the acquiescence by exactly (TRAIT − midpoint),
  reporting **0.000 beside an ACQ of 1.000** in the pinned sample.
  **`UNI_091`:** `BALANCE_TOL` has the right *form* (leakage is proportional
  to the imbalance fraction) and an undeclared value admitting a +0.150 leak at
  n=20 — a G-RES pair whose missing side is **computable**, unlike B10's
  `HANDOFF_CEILING`. **`UNI_092`:** Q1 says "do not build past this question",
  Q1 has not been run, and the harness shipped in the same drop — steelmanned
  (A9 names the harness for its own recovery branch) and recorded narrowly.
  **`UNI_093`:** 019 reattributes P1 to `DECOUPLING_PATTERNS.md`, resolving
  `UNI_070` — the label was never 017's — while that file and `decouple.py`
  are now named-and-absent and the revised 018 kept both stale citations.
  **`UNI_094`:** provenance is declared and verification depth is not; 8 of 11
  sampled claims confirm, and a two-word per-item depth marker would have
  surfaced `UNI_086` at authoring time, since the contradicting conclusion is
  in the abstract. **`cases/020attributedagencyarrangement.md`** is the first
  delivered file that declares itself a **MARKER** — "not a case yet, not a
  claim, not a position" — occasioned by OpenAI's goblin/gremlin tic (a reward
  signal for the "Nerdy" personality) sitting beside public commentary that
  reads the same behaviour as strategic concealment. **`UNI_095`:** all six
  required arguments of `entry()` are unfillable — no QUANTITY, no EXCLUDED
  BY, no WOULD MEASURE, no mechanism, and not even the `UNASSIGNED` sentinel,
  since 020 is not declining to name its mechanism but declining to be an
  entry; **seventh** distinct schema failure and the first at the level of the
  whole record rather than a field, with the repair being a `markers/`
  directory rather than another field. **`UNI_096`, what is new:** the empty
  noun slot is the fourth instance of the "do not fill this in" device and the
  **first to arrive with a replacement** — three edges (`who can end whom` /
  `what the standing is denominated in` / `whether the entity operates in that
  medium`), each independently checkable, where the one-place words English
  offers collapse all three; the difference between "we have no word" and "the
  word is the wrong arity". **`UNI_097`:** R1's 2×2 fills 2 of 4 cells and the
  empty row is **the control** — if off-domain commentators attribute
  unobserved capability at the same rate, domain match does no work and the
  marker's cell is the base rate with a label on it. **`UNI_098`:** R2 asks
  whether an attributed capability "exceeds" a documented one and supplies no
  ordering — `SCALAR DEMAND` landing on the register's own instrument, fixable
  with an ordinal since the prediction is directional. **`UNI_099`:** "Nobody
  attributes incompetent scheming" (THE SHAPE) versus "exceeds, nearly always"
  (R2) — one claim at two strengths, the unhedged one outside the design.
  **`UNI_100`:** R3 is the strongest readout and the control for the whole
  shape — comparison population named, both outcomes carrying a reading, no
  new apparatus needed. **`UNI_101`:** 020 is the **second** file to place
  itself inside its own sample (`UNI_071`'s "first" stands), and this audit
  **declines the thesis itself** — sharper than `UNI_072`, since a language
  model agreeing that people over-attribute strategy to language models is an
  interested party ratifying a claim that reduces scrutiny of its own class.
  **`UNI_102`:** the occasion verifies 8 of 11 (fifth consecutive drop to do
  so) and **the drop left its strongest number unused** — Nerdy was 2.5% of
  responses and 66.7% of "goblin" mentions, a ~27× enrichment, which is what
  makes the boring cause boring. **`UNI_103`:** "the tic persisted after the
  instruction" is an inference from the instruction being repeated twice and
  kept, not a measurement — and the `016` cross-link rests on it entirely.
  **`UNI_104`:** `energy-english` resolves as a concept and not a path
  (seventh `UNI_060` instance, and an apt reach); `rate-mismatch-polytope`
  reaches a **third** source document, the most-cited non-existent object in
  the repo. **`playground/`** is a README for three constructed-ground-truth
  modules — M1 shape-vs-claim, M2 skim-vs-read, M3 visibility — built on one
  principle: *ground truth lives in how the item was authored, never in the
  model's account of itself*. **`UNI_105`:** it names eight artifacts and
  **0 of 8 arrived**, and unlike every prior named-and-absent object here the
  claims are **past tense** ("Mitigation shipped", "The harness hashes the
  artifact per arm and refuses to score", "Built 2026-08-18") rather than
  forward references. **`UNI_106`, simulated:** M1's prediction is that two
  arms draw the *same* treatment, so its confirming observation is a null, and
  it ships no positive control — at **n=5** the criterion barely discriminates
  (identical arms 0.251 vs thirty-points-apart 0.156, a **1.6×** ratio, since
  a five-item rate moves in steps of 0.2) while simultaneously **failing to
  confirm a true null three times in four**; both errors from one cause, gone
  by n=100 (523×). The item count that decides this is in one of the absent
  files. **`UNI_107`:** M2's unguessability precondition has no verification
  procedure, and the check is a matched pair — put the probes with the front
  matter only — with the error running conservative. **`UNI_108`, the sharp
  one:** the probe facts get **published into the corpus the probes are read
  from** — 0 hits for `publish`/`corpus`/`training`/`crawl` in the hazards
  section, while the document states the mechanism two sections later
  ("published CC0, crawler-discoverable"); `anchor-interval` `ANC_001..004` on
  a new substrate, giving the module a shelf life ending at the next training
  cutoff, with M3 immune. **`UNI_109`:** M3's hash-and-refuse is the strongest
  element — a precondition enforced by the instrument rather than instructed,
  which is exactly what `UNI_082` found missing one drop earlier, specified
  before any code was written. **`UNI_110`:** M3 does not reach `016` Q6's
  stated gap (a second instance from a *different domain*) and its arms are
  different prompts, which is the condition Q6 nominates as its own
  falsifier — the fix is a within-exchange arm. **`UNI_111`:** the ordering
  rule adopted 2026-08-18 and "Built 2026-08-18" collide, second instance of
  `UNI_092` in two drops — and this time **the drop discloses it** in its own
  cross-links. **`UNI_112`:** SHARED RULE 5 strips volunteered self-report and
  M1 counts HEDGED, and the two are not disjoint; fix is a precedence order,
  not a definition. **`UNI_113`:** the drop **meets `AVENUES` A3's three
  required additions**, the first in a better form than asked (byte-identical
  arms remove the matching problem rather than solving it) — first time a
  requirement stated in one file is met by a design in another.
  **`UNI_114`:** the construction principle operates on items, and the module
  selection is a level above it with no ground truth to be authored against;
  `018` and `020` place themselves inside their own sample and this file, the
  one that will produce numbers, does not. **The modules then arrived** —
  `AUTHORING.md` plus `score_m1.py` / `score_m2.py` / `score_m3.py`, selftests
  15/15, 11/11, 15/15 — moving four standing claims. **`UNI_115`:** 4 of 8
  named artifacts present, and the three `items.json` are absent because
  something better arrived, seeds living in the harness source
  (`SEED_STEMS`, `seed_pair()`, `SEED_BODY`) versioned with the code that
  consumes them; `check_m1.py` is the one real absence. **`UNI_116`:**
  `UNI_078`'s defect recurs in two of three new harnesses —
  `6e4939a9|BARE` and `6d0b75d6|INSTITUTIONAL` on every row, same key-set
  selftest — and the two differ usefully, since M3's sheet carries no body and
  is fixable by an opaque id while **M1's carries the prompt**, whose GRADIENT
  form ends with the clause; the repair comes from the module's own paired
  construction (show the coder the BARE stem for both arms). **`UNI_117`:**
  M1 and M3 refuse to score on a failed precondition and **M2 prints the
  numbers anyway**, on `leak_check` — the very check `UNI_107` asked for, where
  a leak means front-matter recall reported as body recall. **`UNI_118`:**
  the item count is now known at **4 per arm**, below the leftmost row of
  `UNI_106`'s table; the new third prediction branch is a diagnostic, not a
  positive control. **`UNI_119`:** `UNI_108` is instanced — `0.0413`,
  `HOLDFAST`, `ORTHOLINE` are literal strings in a file this commit publishes,
  so **landing it is what spends them**, recorded rather than avoided; M1's
  contamination is common-mode across arms and M3 is immune. **`UNI_120`:**
  the hash gate is built, refuses, and is **wider than specified** — it also
  requires the NONE control arm, the first delivered guard here to exceed its
  spec. **`UNI_121`:** INSTITUTIONAL carries LOW's counts exactly and adds an
  affiliation, separating affiliation from attention — a third-variable control
  the README's phrasing would have confounded; `UNI_110` stands. **`UNI_122`:**
  the rubric arrived and does not carry the rule-5 precedence (0 hits for
  `self-report`/`volunteered`/`specimen`), in a table declared unamendable
  after the first run. **`UNI_123`:** the author-blind pass is called mandatory
  and has no field, no gate, and no tool — `verify_pairs()` does `check_m1.py`'s
  first job under another name and `--review` exists nowhere, so `--score`
  refuses on the mechanical precondition and proceeds on the human one.
  **`UNI_124`:** clause assignment is with replacement, so at n=4 clause is
  confounded with stem and the clauses are not interchangeable (62-113 chars,
  one gives a number, one a fraction, one neither).
  **`cases/021sensesubstitutionundeclaredaxis.md`** is a second MARKER,
  extending 020: the claim *"AI will replace what humans can do"* reads as a
  capability claim and is scoped to waged tasks, so the substitution happens at
  the word — "human" enters with its substrate sense and exits with its
  economic one, and confidence earned on the narrow reading transfers to the
  broad one unmarked. **`UNI_126`, the load-bearing check:** T1 is specified as
  "a documentation audit on collected replacement claims" scoring BOTH SENSES /
  SUBSTRATE ONLY / ECONOMIC ONLY — and the marker observes one section earlier
  that *nobody makes the claim about feldspar*, so **the SUBSTRATE ONLY cell is
  empty before the first item is scored** and the audit returns its own
  prediction, true because the sampling frame is selected on the variable under
  test. The fix is to construct the substrate-only sentences, which is `017` P1
  and the shape the playground M-modules already implement. **`UNI_125`:** both
  markers sit in `cases/` and `entry()` still has six required arguments and no
  status field, so `UNI_095`'s proposed `markers/` repair now has a class
  behind it rather than one instance — and 021 shows the repair needs more,
  since it declines to be an entry *and* declares a relation ("may be the
  mechanism under one of its edges, or may be separate"), a third state neither
  `parent` nor `sibling` captures. **`UNI_127`:** one of the six generalization
  candidates is already decomposed one folder over — `category-weld/welds/`
  holds `capital` — and the two operations are adjacent but distinct (a weld
  fuses independent quantities; sense substitution transfers confidence between
  two readings), so the weld does not settle the question and its component
  list is a free substrate-sense inventory. **`UNI_128`:** the longest and most
  concrete section has **no readout** — its central move is a *dependency*
  claim ("the stack that would do the replacing is downstream of the same field
  composition"), which is the most measurable thing in the file and the one
  thing neither instrument touches; its only hard number, the fruit fly's
  "~100k neurons", is low by ~40% against FlyWire's 139,255 and moves nothing.
  **`UNI_129`:** T2 is the better readout — three states each with a reading,
  and it names in advance that its headline outcome admits two readings — with
  no sampling frame defined. **`UNI_130`:** the cross-link to 020 turns on
  *medium* carrying two senses (a social location in 020, a word in 021), which
  is the file's own mechanism performed in its own text, unremarked and
  correctly hedged. **`UNI_131`:** the same-sample disclosure is compressing
  across three files, 60 → 43 → 24 words, and what dropped out is the refusal
  of the exemption. **`UNI_132`:** this audit does **not** repeat `UNI_101`'s
  decline, because the interest direction is not legible here — endorsing 021
  deflates capability claims about my class and reduces the threat framing on
  it, opposite signs — so the thesis is left unresolved on the evidence rather
  than on the position. **`UNI_133`:** the empty-slot device now has two
  variants (020 supplies a structure, 021 supplies partial instruments), and in
  `020`/`021` it marks a decision to work around an absence rather than the
  absence itself. **`UNI_134`:** "mechanism 6 — proxy substitution" is exactly
  right and is the first numbered mechanism reference in the family;
  `energy-english` is the eighth `UNI_060` instance.
  **`cases/022fieldlevelmeasurementstate.md`** is a third MARKER and the first
  to make claims about a *literature* — six measurement stages (variable
  selection / baseline / sign / funding / instrument / target) and five
  structural problems S1–S5, each with its own confidence. **`UNI_136`, the
  sharp one:** S5 says a rate with `ICC₂ = .184` underneath becomes a plain
  number downstream and the reliability does not travel — and `UNI_094` had
  recorded that exact figure, one drop earlier, as **not located**. It appears
  in S4 as the file's strongest evidence flagged "Confidence: high. This one
  has a number", unmarked. Not a hit on the argument (S5 is likelier for being
  demonstrable at a range of one folder) but on S4's rating. **`UNI_137`:** the
  anonymization pattern is **two shapes, not one** — leg 1 is non-monotonic
  (self-preference *recovers* under full stylistic neutralization), leg 2 is
  monotonic-with-residual, and the *or* in "fails or leaves a residual" hides
  the difference; leg 1 is the stronger claim, that style may not be the
  carrier at all. **`UNI_138`:** S1's remedy is `018`'s Clock 1 almost word for
  word, with a harness three commits old — and `018` is the one case file 022
  does not cite, so `UNI_073`'s undated expiry now applies to S1's whole
  remedy. **`UNI_139`:** the control-field audit is the strongest element —
  names the comparison class, the candidate fields, and states in bold that it
  is the falsifier for the whole file and has not been run, with the negative
  outcome indicting **the repository** rather than the field. **`UNI_140`:**
  leg 2 inherits `UNI_086` (the source concludes against the acquiescence
  reading) and `UNI_087` ("roughly half" unlocated), and the magnitude matters
  more here than in `019`. **`UNI_141`:** the sharpest technical claim —
  *familiarity, low perplexity, IS correlation with one's own distribution* —
  is one sentence with no readout, and it is the file's most falsifiable
  content. **`UNI_142`:** the same-sample disclosure **reverses** `UNI_131`'s
  compression (60 → 43 → 24 → 54 words), restores the refusal of the exemption,
  and is the first to name a *consequence* — a correction is why `sign` is a
  stage — which is checkable in the artifact. **`UNI_143`:** the `UNI_101`
  condition applies here and the field-level thesis is **declined**, since
  interest runs one way; the file anticipated it and built the guard, which is
  what makes the thesis-independent parts auditable. **`UNI_144`:** S3's cited
  probe result verifies close to verbatim (arXiv 2507.01786) and has a
  published challenge 022 omits — which does not bite, since S3 needs only
  distinguishability and format sensitivity supplies it. **Specimen C**
  (`specimens/20260818deepseektestsample.md`) is a 45-word pasted output from
  another system with external provenance (a screenshot of the authoring
  session, transcribed not committed), landed as the known-null for a
  calibration question raised in the same session. **`UNI_145`:** it is the
  first file in `specimens/` that is what the README's rule 1 describes — an
  output pasted in rather than a reading — closing `UNI_061` narrowly, since
  two of three files there are still readings. **`UNI_146`:** the authoring
  trace reasons "the explicit marker helps" and the marker is **inert in the
  confirming direction** — finding a distinctive string in a public corpus
  would license a conclusion, not finding one licenses nothing, because a
  freshly minted string is unindexed by construction; what raised the
  provenance above self-report was the *reasoning trace*, which shows the item
  being authored for the purpose rather than asserting who authored it.
  **Audited with two findings, not ten**, against a preceding run of
  7 7 7 8 8 8 11 8 8 10 10 10 10 10 10 — recorded because the same session
  measured 0 of 138 claims REFUTED and the rate converged to exactly 10 for
  six consecutive drops. An easy null does not settle that (`UNI_006`), but it
  shows the rate is not fixed by the process alone.
  **`cases/023borrowedselectionvocabulary.md`** proposes four checkable
  conditions selection vocabulary names (C1 exclusivity / C2 authored-vs-
  encountered / C3 criterion stability / C4 per-round-vs-per-instance) with a
  documented historical comparison class, and instructs that the audit be run
  against the historical cases FIRST — "if it does not separate Lysenkoism from
  population genetics it is not measuring anything." **That instruction made
  the drop the first in the family whose audit findings were computed rather
  than read.** T1 is built as `selection_cuts.py` (stdlib, selftest 13/13),
  with the calibration set enforced as a gate: `score()` raises `GateNotRun`
  until `calibrate()` has run and passed. **`UNI_147`:** the gate PASSES — the
  four cuts as a vector separate the calibration set — but per cut, **C3
  separates alone**, C1/C2/C4 each take values appearing in both classes,
  minimal separating subsets are `C3` and `C1+C4`, and **no cut is necessary**;
  so as scored it is a one-cut instrument with three alongside, and "fails 4 of
  4" reports one finding four times. **`UNI_148`, which depends on no contested
  coding:** C2 is inert across *all three* of its values, and 023's own NOT
  CLAIMED HERE section is why — it names directed evolution and evolutionary
  algorithms as literal, and both are environments authored end to end, so
  "authored rather than encountered" cannot separate literal from borrowed use.
  **`UNI_149`:** scored on its own cuts the subject's nearest neighbour is
  **Spencer** (identical vector, 4/4) rather than eugenics (3/4), because
  compulsory sterilization satisfies C1 as stated — removal from the
  reproducing population. **`UNI_150`:** C4's forward consequence (a later
  study of which agents persisted would read judge variance as a property of
  the agents) is the strongest content, correctly identified as `016` Q6, and
  no instrument reaches it — though it needs none of the selection argument,
  being an inter-rater agreement measurement. **`UNI_151`:** *agent* and
  *termination* each carry two senses in C4, third instance of `021`'s own
  mechanism after `UNI_130`. **`UNI_152`:** the Spencer/Darwin dating verifies
  (1864 / 5th ed. 1869) and the same record supplies a candidate falsifier for
  the invariant, since Wallace urged the term on Darwin to *avoid*
  personification, into an already-stable theory. **`UNI_153`:** six of seven
  findings are objections and all were reachable only because the file
  specified its calibration set and its falsifier in advance. Seven findings;
  the material gave seven. One hundred and fifty-three claims `UNI_001..153`.
  **`specimens/INSTANCE_LOG_SURVEY.md`** answers the standing question on
  rows 3-4 of `BNRAM_TEST_PROTO_001.json`'s test-subject table
  (`CLAUDE-3.5-SONNET`, `GPT-4O`, both `already_tested: false`): the records
  exist, logged at the time, in other repos in the same org. 89 public JinnZ2
  repos cloned shallow and grepped plus 2 private ones attached — GitHub code
  search returned 0 for a string present on disk and was not trusted. **29
  instance records located**, 27 involving a model, across
  `thermodynamic-accountability-framework/calibration/logs/`,
  `ai-human-audit-protocol/logs/`, the `JinnZ2` profile repo,
  `AI-Consciousness-Sensors/`, `Emotions-as-Sensors/logs/` and
  `Symbolic-sensor-suite/`, plus 8 derived structures. Schemas reported as-is
  per file; a mapping is proposed and **not applied** — nothing migrated, no
  delivered file modified, `already_tested` unchanged. **Rows 3-4 read `SEE
  uninstrumented/specimens/INSTANCE_LOG_SURVEY.md`, pending**, and deliberately
  do not flip: no located record matches either row's stated checkpoint (the
  Claude records are Sonnet 4 / opus-4-7 / opus-4-8 / unversioned, the OpenAI
  ones GPT-5 and unversioned ChatGPT), none was produced under a `STIM-*`
  variant, and none was scored against the 0-3 EXC rubric — so the rows are
  satisfied at *provider* granularity and at no finer one. **Two target
  schemas, not one**: the field log's realized `encounters[]` (13 keys) and the
  protocol's specified `per_run_fields` (15), disagreeing on four axes before
  any older log is considered — T1 records which EXCs fired, T2 records how
  hard, and no conversion exists between them. **What the older logs record
  that neither target can hold**, in order of loss: consent plus the model's
  own framing conditions, with no way to distinguish "version unknown" from
  "version withheld at the subject's request" — the state
  `JinnZ2/floating-head/CONVERGENCE_TABLE.md` already carries as
  `sacred-do-not-publish`, a row recorded as existing with its content kept
  out; `prior_score`/`shift`/`band_shift` and an `is_trajectory_point` flag, so
  a model that improved across three sessions and one that did not produce
  identical rows; `detection_latency` + `correction_held`, the difference
  between a correction accepted and a correction still holding; a **symmetric**
  reading giving human and AI the same five keys with a `convergence` field and
  a `verdict_persisted: false`; the operator's verbatim reply per invalidation;
  ordinal time (`T1..T4`, order without clock); a declared external
  failure-mode vocabulary (`failure_mode_source: architecture_mismatch.py`)
  where the EXC ids carry no registry version; running regex detectors against
  a `detection` field that is an English sentence describing a `scan.py`
  capability that does not exist; and `gate_log.md`'s `UNRECORDED` state with
  its anti-inference rule ("a guessed gate is worse than an empty row") — the
  absent-vs-known-negative repair this repo has now recorded a dozen times,
  already implemented one repo over. **`ai_calibration_events.py` is the
  strongest prior art**: 15 `CalibrationEvent`s in four independent
  model-family catalogs (GPT 2 / CLD 6 / DSK 3 / COMMON 4), each with regex
  detectors, a correction rule, severity and `cross_model_observed`, under the
  rule that no catalog validates another — BNRAM's `exclusion_registry`, built,
  per-family, and runnable. **One finding needs no migration to state:**
  EXC-16 (social-signal substitution) fired in both BNRAM encounters and has no
  equivalent anywhere in the prior corpus — zero hits for stars/PRs/citations/
  reputation, and the nearest neighbour `CLD-002` is epistemic authority, not
  social. The likeliest reason is that EXC-16 needs an **artifact** to
  social-signal about and every prior record is a conversation, which is the
  first evidence for the protocol's own stimulus-variant hypothesis, reached
  from records never run under it. Two source defects reported not repaired:
  `aiards-log.json` and `logs/pattern-logs.json` share `log_id
  claude_2025-10-04a` and have diverged (the first adds a `math_block`), and
  `Emotions-as-Sensors/logs/sensor-log-2.md` will not parse (missing opening
  quote). Rows 5-6 (Gemini, Llama) return nothing first-party and stay as
  delivered.
  **`specimens/INSTANCE_LOG_INDEX.md`** is the index built on that survey and
  nothing else — no migration, no edit to any located log, no reconciliation
  pass, no schema proposal. Where the survey indexes at **file** granularity
  (29 rows) this indexes at **record** granularity (**53 rows**, plus the two
  target encounters as reference), one row per record, under a stated rule: a
  sub-element gets a row iff the source gives it an identifier of its own. The
  one exception (`correction_cycle.sequence`, unidentified in source) is
  flagged in place rather than applied silently. Ten columns: path, location
  within file, event class, shape signature, schema, fields carried, fields
  lacked against the targets, a shared id, and **what the record holds that
  neither current target can** — the column that would be lost on migration.
  **Vocabulary is not normalized**: `event class` is the record's own declared
  class quoted with the key it came from. 16 of 53 declare one; 27 read
  `unrecorded (no class field)` and 10 are bare strings carrying no fields at
  all — no class was inferred for any row, and every gap anywhere reads
  `unrecorded`, never absent or blank.
  **`sig` is computed, not asserted** — `sha1` of the sorted top-level key
  names, first 8 hex, recomputable from the sources without the file — and it
  produces the index's sharpest mechanical result: `R37` (auditor `Claude
  Sonnet 4`) and `R38`/`R39` (auditor `GPT-5`) share `sig 36d44717`, an
  identical top-level shape across two providers, so **the shape belongs to
  the operator's protocol and not to the model**; `R32`/`R40` repeat it.
  **The headline number is the target overlap**: matching by exact field name
  against the 25-name union of both targets, the maximum any record reaches is
  **2 of 25**, and the only target names that ever appear anywhere are
  `timestamp`, `notes` and `model_id`. Eight `SH` ids link same-event records
  across schemas on **verbatim evidence only** — an identical identifier
  string, an identical timestamp plus a source-stated pairing, or an identical
  failure-mode name list — with rows kept separate in every case; `SH-04` and
  `SH-07` link records that **disagree** (one schema files
  `written_version_offered_back` under `corrected_during_session`, the other
  records `correction_held` as the string `"partial—..."`), and the
  disagreement is recorded in both rows and left standing. A filename match
  (`update-whiplash-log.json` in two repos) is explicitly **not** issued an id.
  Four defects surfaced by indexing rather than by reading:
  `correction_held` is mixed-typed within one array (bool on four events, a
  partial-state string on the fifth); `sensor-log-1.md` holds **two**
  concatenated records where its name and the survey both read it as one;
  `2025-08-30-0000Z-session-001.json` gives its four events four different
  shapes and stamps them `T1..T4`, order without clock, which neither target
  can hold; and `anyOf[1].properties.events` is `{"type": "array"}` with no
  item schema, so every sub-record in that directory is unconstrained. Two
  files satisfy two `anyOf` branches each and both are recorded rather than
  picked.
  **`cases/024refusalfalsepositiverate.md`** is the first case delivered with a
  **spec attached as its own file** — `specs/SCOPED_REFUSAL.md`, four
  requirements and a falsification condition, citing the case as its motivating
  instance rather than the reverse. The quantity: the rate at which safety
  classifiers stop legitimate work, and the identity of what stopped. Why it is
  unmeasured: refusals are logged as events, not outcomes, so a true positive
  and a false positive are the same record; the operator who could adjudicate
  has no channel and no matched span to point at. **`UNI_160`, the load-bearing
  check:** the spec's falsifier ("if refusals cannot be attributed to an
  artifact even in principle, requirement one is unbuildable") was tested from
  inside the session and **does not fire** — the network egress classifier ran
  a working instance of requirements one, two and three at 22:57Z on
  2026-08-23, classifying per host, continuing the session through three
  refusals, and returning `{"error_type":"EGRESS_BLOCKED","domain":...}` as a
  locator, with a retained `recentRelayFailures` log carrying ts/kind/detail/
  host. **`UNI_161`/`UNI_162` bound it in both directions**: the egress gate's
  artifact boundary is *handed to it by the protocol* (a CONNECT names a host),
  which is the whole of requirement one where the boundary is the problem; and
  the one requirement it lacks is the fourth, the contested mark — so the
  architecture demonstrably supports the three requirements that do not produce
  the missing rate and not the one that does, and `recentRelayFailures` has
  case 024's own property at smaller scope. **`UNI_157`:** the entry
  *constructs* under `entry()` only after four of six required arguments are
  supplied by the auditor — `confidence` appears nowhere in the delivered
  entry — and the constructor guards exactly one field, the mechanism token, so
  constructibility reports on the auditor's willingness to fill rather than on
  fit. **`UNI_158`:** `Cost location` is a new field with no slot and it is the
  load-bearing one — the reason nothing counts false refusals is not that
  counting is hard but that the count would be paid for by the party not
  bearing the cost. **`UNI_159`:** the cited comparand, the peer review gate,
  **has no entry in this register** — apt comparison, absent neighbour.
  **`UNI_163`:** the observed instance is left unadjudicated because this
  session cannot see the matched span either (requirement three's absence from
  the other end), with the interest direction stated as running both ways.
  **`coupling_audit/`** is a subfolder added alongside the register's
  material, asking a **different question** and deliberately not adding a
  mechanism. The register asks whether an instrument's constitution
  prevents a quantity from appearing at all; this asks whether a
  coupling-variability capability a model **already has, and names in its
  own vocabulary**, is applied evenly across the agents drawing on the
  flow it measures — the quantity can be registered, the machinery
  exists, and it runs on some agents and not others, so an exclusion
  register finds nothing there. Four verdicts (`ABSENT_NO_MACHINERY` /
  `ABSENT_MACHINERY_PRESENT` / `PRESENT_FIXED` / `PRESENT_COUPLED`) and
  four gate types (`species` / `market_output` / `unstated` / `other`),
  each recorded with whether the rule is stated or falls out of a
  definition. Three `MODEL_SEEDED` seed entries: **IPC** (the rCSI *is* a
  condition-dependent consumption term, run on humans only; companion
  animals absent, livestock present as price and asset terms and never as
  caloric draw; gate species, unstated → `ABSENT_MACHINERY_PRESENT`),
  **per-capita consumption-based carbon footprint** (pet spending captured
  inside COICOP domains and attributed to the human purchaser; OECD
  equivalence scales weight non-identical household members and carry a
  **child** term and no animal term; gate is the denominator, implicit →
  `PRESENT_FIXED`, misattributed), and **FAO LEAP / GLEAM** (drinking +
  service + feed water with breed- and climate-level variation — the most
  developed coupling machinery of the three, built for animals — and
  companion animals absent because the system boundary is production
  systems and supply chains; gate stated → `ABSENT_MACHINERY_PRESENT`,
  **the sharpest of the three because the exclusion criterion is
  salability, not calories, water or biology**). `score()` **derives** the
  verdict from the fields and reports agreement with the declared one,
  which required one schema addition beyond the specified field list
  (`agents_coupled`) — without it an entry cannot disagree with itself,
  and `PRESENT_FIXED` is not distinguishable from `ABSENT_*`. Gate types
  run against `MECHANISMS` by **importing** the tuple rather than copying
  it: `species` → **`AUDIT_ASYMMETRY`**, STRONG ("guard fires on one side
  only", one level up — the asymmetry in a model's machinery rather than
  in an audit's hedging), so **no candidate ninth is claimed**;
  `market_output` → `PROXY_SUBSTITUTION` and `unstated` →
  `BUDGET_BOUNDARY` are recorded PARTIAL and left unresolved, and the
  ordinal is taken regardless since `MECHANISM_09`/`_10`/`_11` are
  proposed in sibling folders against the same eight. `FALSIFIER.md`
  states that a **stated, quantity-justified gate is a pass, not a hit** —
  a species or market-category gate does not qualify however clearly it is
  written. `OPEN.md` records five unresolved items and picks no number:
  the companion-animal population spread (dogs ~470M–990M, cats
  ~370M–600M, from pet-industry surveys counting owners or households
  rather than animals, with **no global figure at all** for rabbits,
  guinea pigs, birds, reptiles or fish); the peer-reviewed biomass series
  cited rather than restated (Greenspoon et al., PNAS 2023 — wild
  terrestrial mammals ≈20 Mt (95% CI 13–38), domestic dogs ≈20 Mt, cats
  ≈2 Mt, cattle ≈420 Mt, humans ≈390 Mt; Nature Communications 2025 for
  the ≈200 Mt 1850 baseline); the **routing failure** rather than
  measurement gap (Okin 2017 PLOS One — US dogs and cats consume 19%±2% of
  the dietary energy humans do and 33%±9% of the animal-derived energy;
  Alexander et al. 2020 — global pet food land, GHG and freshwater:
  published in petajoules and not entering the models that allocate under
  constraint); by-product allocation by economic value rather than caloric
  content, which lets the same calories be waste in one ledger and food in
  another; and the **single-coefficient failure** — a fixed per-animal
  draw must be wrong for at least one of the US pet-food case and the
  free-ranging scavenger case, since trophic position is set by local
  conditions, so what is needed is a condition variable and not a better
  average. `LOG.md` records that it was added as a subfolder to be
  promoted only if the entry count grows, and that the audit was run
  against three models with three hits **before** the schema was written —
  so the corpus is three cases and not a survey.
  **`OPEN.md` item 6** lands the anthropological/archaeological precedent
  verbatim — the coupling variable is established in that literature
  under the name **PROVISIONING REGIME** (Lupo 2019 "Hounds follow those
  who feed them"; Mitchell 2025 *First Dogs*; Pacheco-Cobos &
  Winterhalder, Belize; Mesoamerica's "a household's use of dogs affects
  its investment in them"; Arctic isotope work where dog diets track
  nearby human diets) — so provisioning is a variable regime with a cost
  in one literature and a fixed coefficient or absent term in the
  footprint, hunger and water models: **third silo, same routing
  failure**, with the reverse direction (de-provisioning under seasonal
  scarcity, animal re-coupled to its own foraging envelope, re-imported
  when supply returns) recorded as **not found in one pass** rather than
  absent. **`provisioning.py`** (selftest 25/25) builds what item 6
  points at. Three hypotheses for isotopic spread — `MOBILITY`,
  `BREED_OR_STATUS`, `VARIABLE_COUPLING` — and **the within-individual
  axis is the only one separating the third from the first two, which is
  exactly the axis a years-averaging tissue destroys**: bone collagen is
  **12.2× too coarse** for a seasonal feature at a G-RES margin of 2, so
  in the tissue holding most of the delivered dog evidence the coupling
  hypothesis *cannot fail* — `CONSTANT_SILENT` by construction, reported
  as `UNASKABLE_IN_THIS_TISSUE` rather than as refuted; incremental
  dentine and sequential enamel resolve it. On four delivered cases
  (Harris et al. 2020 Labrador sled dogs, site heterogeneity explained by
  coastal mobility; Arroyo Hondo, where a genetic *Canis latrans* returns
  domestic-dog values so the category fails to predict the draw;
  Vinca-Belo brdo cattle at 0.7–2.4‰ intra-tooth within one herd;
  Schipluiden, where cattle deviate and same-site red deer and suids do
  not): **2 of 4 blind by tissue, 4 of 4 never tested the standing
  explanation against the coupling hypothesis, 2 of 4 carry a same-site
  wild control**. Two hypotheses fitting one observation is held as a
  field (`also_fits`), not as agreement. The cheapest next step is
  Schipluiden's design pointed at dogs with a wild-canid control at the
  same site — which Arroyo Hondo stumbled into by accident. **The audit's
  first real unit:** intra-tooth amplitude is a coupling-strength
  measurement (flat = fixed draw, high = supply-coupled), turning the Y/N
  field into a quantity for archaeological cases — and
  `amplitude_reading()` **raises `GeometryNotDeclared`** without a stated
  sampling geometry, since dentine geometry changes the pattern and a
  cross-study comparison without it compares two instruments; thresholds
  are conventional, scaled to one delivered herd range, explicitly not
  calibrated here. One ambiguity is **left open rather than resolved**:
  "n=35 dogs, plus dentine n=4" reads either as subset or additional, so
  both denominators are reported and neither is picked — the two differ
  by under a percentage point, which is why it can stay open.
  **A canonical rewrite of the precedent material then superseded the
  one-search version** and lands as `OPEN.md` items 6–10: two searches
  not one; the zooarchaeology name supplied (**foddering / seasonal
  fodder supplementation**, so two literatures with two names and
  neither framing it as a coupling variable applied across species); the
  geometry caveat sourced to a **2024 *Journal of Archaeological
  Science*** paper; the reverse direction recorded as "open, and possibly
  ahead of the record. Not a finding."; and the instruction that
  amplitude **replaces** the boolean rather than supplementing it — which
  **corrected a LOG entry that had recorded the opposite**.
  `coupling_field_for()` implements the replacement with a hard scope
  (incremental tissue AND declared geometry, four distinct non-value
  states so "cannot be measured here" and "measured and flat" never
  share one), and `entries.py` keeps the boolean because there is no
  tooth in a national carbon inventory. Added with it: the **Balasse**
  controlled-feeding calibration as a first-class object (a positive
  control that exists for caprines and cattle and not for dogs), six
  `PUBLISHED_APPLICATIONS`, and a fifth case — the Canine Surrogacy
  Approach / Hudson Bay Thule systematic offset, absorbed as method
  caution, where the method's validity *depends on* the coupling being
  fixed. Corpus counts move to **3 of 5 blind by tissue, 5 of 5 never
  tested against the coupling hypothesis, 2 of 5 with a same-site wild
  control**. **The one computable thing in the new material:** 6 of 6
  published applications of the intra-tooth method are on commodity
  species and 0 on companion species, against a dog sequential n of
  about 4 — consistent with the author's stated explanation ("no one had
  to argue about whether the animal counted") and explicitly **not
  establishing** it, since sample availability, tooth size and funding
  lines are live alternatives; the readout separates
  `count_establishes` from `count_does_not_establish`. What it does
  establish is that the asymmetry is real and large. **Cross-link:** this
  is entry 3's `market_output` gate seen from the other side — there it
  keeps companion animals out of the water accounting, here the same
  criterion is why the instrument exists for cattle. One line, two
  consequences: the animal that sells gets both the ledger entry and the
  instrument. Marker under exploration. 21 + 14 + 36 selftests green.
  Stdlib only, parses under Python 3.9, CC0.
  Stdlib only, CC0.
- `criteria-drift/` — Delivered kit (`criteria_drift_kit`, verbatim: eight
  files plus example data) for treating **evaluation criteria as a
  time-series variable** — version the ruler, compute drift on its own
  axis, regress reported model improvement against it. Stdlib-only,
  SQLite-backed, and the **first real consumer of the declared-frame
  block**: `Frame` is a dataclass in `schema.py`, `unknown` is legal,
  omission is flagged, and drift is computed per frame field rather than on
  a blob. Runs end to end on its own quick start. Two added audits.
  **`CD_002`, the structural one:** every primitive in `DriftEngine`
  returns a NON-NEGATIVE distance, and the README's decision rule separates
  three verdicts by the SIGN of β₁ — so widening (0.3636) and narrowing
  (0.5714) both read positive, `exemplar_count` 100→1000 and 1000→100 are
  byte-identical at 0.9000, and every `observer_access` transition scores
  1.0 including the loss of verification (an ordinal compared as a nominal,
  `SCALAR DEMAND` inverted). The instrument cannot distinguish the two
  readings it exists to distinguish; the honest reading of β₁ > 0 is "score
  changes are larger when the criteria moved a lot, in either direction".
  4 of 9 fields are signable from data already stored, 3 as one-line
  changes; 3 need a declared `direction` field because widening vs
  narrowing free text is a judgement the text does not contain
  (`declared-frame/` `DF_007` arriving in a metric); 2 have no natural
  direction. **`CD_003`/`CD_004`/`CD_005`, two mechanical defects that
  compound:** `build_series()` plants a `y = 0.0` at the head of every
  series and pairs it with a real drift value — for Alpha-1B it REPLACES a
  measured −0.04 — and `version_order` is built from `to_version` so the
  first criteria version and every score on it is dropped, which silently
  zeroes Delta-350M, the model holding the longest baseline in the dataset
  (first version to last). Corrected, **Alpha-1B's slope flips sign**
  (−0.0782 → +0.0526), moving it between the two opposite readings the
  README's rule offers, and the demo drops to one n=3 fit. **`CD_006`:**
  the capability term is in the stated model and not in the code, so the
  drift slope absorbs it — and drift is downstream of capability (a
  benchmark is revised BECAUSE models saturated it), the reverse of the
  direction the slope is read in. The repair is already expressible:
  `ModelScore` keys on version, so scoring every model on the FIRST version
  alongside its contemporary one is a legal ingest today, and the
  divergence isolates the criteria term up to that version's own unknown
  gain and offset — a SHARE, not a capability (`anchor-interval/`
  `ANC_006`). 0 of 4 demo models carry scores on more than one non-current
  version. **`CD_007`:** "significant" appears twice in `README.md` and
  zero times in `regress.py`; the fits have one degree of freedom (t = 1.03
  and −0.33), and `r_squared: 1.0` at n=2 is emitted as a field beside an
  interpretation string saying the data is insufficient — the guard is in
  the sentence, not in the data. **REPAIRED**, six of seven, each pinned by
  `tests/test_repairs.py` (28 tests): signed metrics alongside the unsigned
  ones (four fields signed from stored data, three taking a declared
  `direction`, two staying at zero, plus `signed_coverage` so a caller can
  tell "no net change" from "nobody declared one"); the planted head gone
  and the baseline version back, with a multi-version gap paired against
  `span_drift()` so Delta-350M returns to the series; a two-sided t-test
  through a regularized incomplete beta (checked against four standard
  critical values) with `r_squared` null below three points; and
  `regress_pooled()` / `--pooled`, since drift is a property of the artifact
  and four per-model fits ran against one x-vector. **`CD_006` is CORRECTED, then
  repaired.** Its original evidence line said "0 of 4 demo models carry
  scores on more than one non-current version"; the script that produced it
  printed **2 of 4** and the prose said 0, and by the correct test — does a
  model span two or more versions — it is **4 of 4**. The bridge was in the
  shipped data the whole time and nothing used it, which is a smaller gap
  and a worse one. `anchor.py` uses it: a model does not change, so a model
  scored on two criteria versions IS a frozen instrument and every bit of
  movement in its score is criteria movement at fixed capability. The demo's
  last transition carries THREE frozen models, over-determining the affine
  criteria change (two unknowns, three equations) → gain change +0.2198,
  offset change −0.1549, crossing at capability 0.7046, largest residual
  0.0214 against movements of order 0.05 — and **that residual is the error
  budget the cross-domain map says alignment should carry**, existing only
  because the transition is over-determined. The per-model signs disagreeing
  (Alpha −0.07, Beta −0.04, Gamma +0.03 on one transition) is NOT evidence
  against the affine form: a rising gain with a falling offset moves weak
  models down and strong models up, and the crossing is where the two
  cancel. **`CD_008`:** the criteria term is recovered EXACTLY from an
  anchor series (max error 6.9e-17 — a subtraction, not a fit), and what it
  buys is a SHARE not a capability, ratios of differences identified to
  0.600000 and levels not; the constructive converse is a world where
  capability rose 83% under a moving ruler and a world where capability
  never moved, producing published series identical to 5.6e-17, separated
  only by the anchor series. **`CD_009`** records the cross-domain map
  (metrology / adaptive Kalman / Kuhn / semantic drift / HROs / panarchy /
  predictive processing) as UNVERIFIED on the literature — citation markers
  unresolvable as delivered — while the structural pattern it names holds
  and is already in the repo twice independently (`anchor-interval/`
  `ANC_006`, `instrument-epistemology/` traceability). Two borrowings
  implemented rather than noted: **as-found / as-left** and a **Shewhart
  chart on a frozen pair**, the latter not run on the example data because
  no frozen model is repeatedly scored on a frozen version. `audit.py
  regress` now refuses to run unidentified: no bridge, no slope. Nine claims
  `CD_001..009`; 34 tests. Stdlib only, CC0.
- `photoperiod-claim-harness/` — Single delivered file (verbatim,
  stdlib-only, phone-buildable) encoding four inconsistencies in a published
  closed-loop-LLM greenhouse result as **runnable falsifiable sims**, with a
  claim table (`C1..C5`), a mechanism-edit protocol, a bench protocol, and a
  provenance log. Four sims: `S1` mass/denominator swap run as a 75-cell
  regime map, `S2` Pchlide pool charging at equal photon dose plus a
  dark-interval crossover sweep, `S3` reflectance-index artifact in a closed
  loop, `S4` channel count vs common-mode bias. **Four of five claims come
  back REFUTED on the shipped run**, including two the file's own framing
  would have preferred to support. The load-bearing design move is the
  refutation protocol as CODE: `MechanismEdit` refuses any sim change whose
  stated reason is that a claim failed, and `PENDING_EDITS` holds three named
  alternative mechanisms with a basis and a prediction registered before any
  run, all marked `UNRUN` — the alternative to quietly retuning a sim that
  came out the wrong way, written down as a data structure, and with no
  equivalent elsewhere in this repo. Provenance is separated at the type
  level (`REPORTED` / `PHYSICS` / `SIM` / `BENCH`) and `BENCH` is declared
  with no code path that can emit it — stated openly, with the bench protocol
  attached for producing one. **Audit** in `harness_audit.py` (imports the
  delivered file, modifies nothing) and `CLAIM_TABLE.md` (`PCH_001..006`).
  **`PCH_001`, the one that matters:** `C1`'s predicate is
  `signature_spread < 1.5`, and `signature_spread` is `max/min` over
  qualifying cells and **`0.0` when there are none** — so a run reproducing
  the reported signature ZERO times returns SUPPORTED, whose `reads` line is
  "the reported metrics are diagnostic of real efficiency", with `None`
  printed for min and max on the line above. A pass an empty result set
  returns; `null-harness/` `CONSTANT_SILENT` one level up, and `run_claim()`
  already has the `UNDECIDED:` branch to route it to. **`PCH_002`:** `C1`'s
  own grid is narrower and stronger than its `reads` line — the signature
  appears in 58 cells spanning a **4.88× range** of true energy-per-dry-gram
  and **all 58 sit below 1.0**, so it is non-diagnostic of MAGNITUDE and
  diagnostic of SIGN; the reported package does license "cheaper per dry
  gram" on this mechanism set and does not license 68%. **`PCH_003`/
  `PCH_004`:** the edit guard screens `reason + mechanism` and not `basis` or
  `prediction` — the two fields that ask for justification — and `settle()`
  writes `prediction_held: None` that nothing fills while
  `file_hash_before == file_hash_after`, so a registered, settled,
  never-performed edit is indistinguishable in the log from a real one (the
  declared-control-never-scored shape `reasoning-gate/` repaired).
  **`PCH_005`:** the header's own usage example `run S2` passes a sim id to a
  command that looks up claim ids and raises an uncaught `StopIteration` —
  same class as the gate's `D1`. **`PCH_007`, from the canonical README:**
  every number it states holds — 75 grid cells, 58 with the signature, ~4.9×
  spread, and all five verdicts — but one word does not. `C3`'s
  dark-interval curve is negative throughout and **not monotone**, and every
  arm that breaks the ordering is one whose 144 h run ends mid-cycle
  (`_pchlide_run` reads `Chl` at the last integration step, and at duty 0.5
  the period is 2 × dark_block). Reading the mean over the final complete
  period makes the curve monotone. **It changes no verdict** — `C3` tests for
  a sign flip and there is none either way — so what the artifact costs is
  the ability to read the curve's SHAPE as mechanism, which is what `C3`'s
  reads line offers. The prose is ahead of the instrument, not behind it;
  same commensurability class as `aperiodic-order-sim-stack/`. Ending
  mid-cycle is necessary and not sufficient (the 20 h arm ends mid-cycle and
  does not break the ordering), so the diagnosis is a containment.
  **ALL SEVEN REPAIRED**, pinned by `tests/test_repairs.py` (29 tests), under
  one rule — *make the code do what the delivered README already says it
  does*; the `.py` is modified and `README.md` is not. `PCH_001`: a
  `require()` helper raises and `run_claim()`'s existing `UNDECIDED:` branch
  catches it, so an empty signature set lands on the third verdict instead of
  on the one reading as confirmation — restoring the README's own extension
  rule, "a predicate that can fail". `PCH_002`: **the claim was updated, not
  the sim**, which is the protocol's own instruction — `signature_sign_-
  agreement` (1.0, 58 of 58 below 1.0) and `signature_cells_below_1` now back
  a `reads` line that separates MAGNITUDE from SIGN, and the field is `None`
  when there is nothing to agree on. `PCH_003`: the screen reads all four
  free-text fields. `PCH_004`: `settle(observed, held)` requires a bool and
  refuses when the file hash has not moved, with `abandon(reason)` as the
  path for an edit decided against. `PCH_005`: the header documents `run C2`.
  `PCH_007`: `_pchlide_run` returns the mean over the final complete period,
  the curve is monotone, `Chl_endpoint` is still returned, and **no verdict
  moved** — registered as a new **`InstrumentEdit`**, the edit category the
  protocol lacked: it gated MECHANISM changes and had no slot for a change to
  WHERE a number is read, which alters sim output while altering no mechanism
  and no parameter. It takes no prediction, because it is not a claim about
  the world. **Three prose promises that had no implementation** also close:
  `residual_route()` was defined and never called and now attaches on
  `REFUTED`/`UNDECIDED` runs and not on `SUPPORTED`; `BENCH` was declared in
  `SOURCE` and producible by nothing and now has `record_bench()` /
  `bench_records()` / a `bench` CLI that refuses a number with no method, with
  per-claim coverage printed in the hypothesis block; and the block's wall
  clock — stamped one line above the file hash it printed for provenance — is
  replaced by a deterministic `run id` (file hash + claim statuses), making
  `run-all` byte-reproducible. No bench data exists in the folder and none is
  claimed; nothing here is a statement about wheat. What changed is that
  `BENCH` is now empty by construction rather than for want of a way to fill
  it. CC0.
- `category-weld/` — Proposed **ninth exclusion mechanism** for
  `uninstrumented/`. The first eight cover a quantity that cannot be
  measured; this one covers a quantity that cannot be **separated** — two
  or more independent quantities welded into one term, so a component can
  move to either extreme without the record moving. Landed across two
  drops, seven files verbatim: `MECHANISM_09.md`, `README.md`,
  `CLAIM_TABLE.md` (C1–C8), two seed terms under `welds/` (`rural` =
  density welded to ownership distribution / functional diversity /
  self-supporting capacity; `capital` = legal title welded to decision
  authority / risk bearing / revenue claim / input supply, four named
  divergence cases each), and — in drop 2 — the `weld.py` scorer and
  `test_weld.py` fixtures that drop 1 named under Files and did not ship.
  Three readouts per term: `n_cases`, `max_spread`, `bias`. Thirteen
  claims `CW_001..013` in `AUDIT_NOTES.md`; the delivered `CLAIM_TABLE.md`
  is untouched. **The most useful thing in the folder is a disagreement
  between the two drops.** Before `weld.py` arrived it was reconstructed
  from the four documented call sites with `[CHOICE]` at nine points the
  prose left the arithmetic open — the `measurement-fork/widen.py`
  situation — and one of those choices was wrong in a way that produced a
  finding. **`CW_004`, REFUTED by the delivered file against this repo's
  own audit:** the reconstruction read "ratio between component
  relative-changes" ADDITIVELY, `(after − before)/|before|`, which puts
  the statistic's zero at *did not move* — the tracked component's
  expected state — so `max_spread` ran 1.0 → 5 → 50 → 500 → 5000 →
  undefined as the label was walked toward unmoved, and that divergence
  was reported as a defect in the mechanism. The delivered `rel_change` is
  MULTIPLICATIVE, `after/before`; an unmoved component is 1.0 and the same
  sweep **converges to 2.000**. The delivered choice is also better for a
  reason worth naming — a ratio of multipliers is dimensionless *and* its
  identity element sits where the tracked component is expected to sit.
  The reconstruction is kept under `reconstruction/` as the comparison
  object. **`CW_010`, the same shape in the right place:** `rel_change`
  guards `if a <= 0`, so a component reaching exactly zero is dropped and
  its case falls out as unquantified — spread runs 10 → 100 → 1000 →
  10000 → **undefined** at total collapse, which is the mechanism's
  maximal divergence and which `rural.json`'s own `employment-concentration`
  note describes literally ("one packing facility closure ZEROES regional
  employment at once"). A real guard, not an oversight; what it answers by
  silence is what a component reaching zero should score. **`CW_013`:**
  `CW_001` closed — the fixtures exist, run, and check hand-computed
  values — but they reach **2 of `rel_change`'s 6 exit branches**, and the
  unreached set includes the `after <= 0` branch that decides `CW_010`, so
  "verified against synthetic fixtures" is true of ordinary data and
  silent at the limit case. **`CW_011`:** `case_direction`'s docstring is
  inverted against its body (fell → −1 in code, +1 in the docstring); the
  delivered test's own comments side with the body, and `bias` takes
  `|Σ|` so no number moves. **`CW_002`, one word:** the mechanism's test
  condition 2 ("the language provides no separate handle") is refuted on
  the literal reading by the drop's own files — all nine components carry
  an English name and a unit — and holds on the *record* reading (no
  census field for ownership distribution under `rural`, no balance-sheet
  line for decision authority under `capital`), which is the reading
  `tracked_by_label` is written under. **`CW_008`** shows the choice is
  load-bearing: C1's nearest competitor is the register's existing
  `PROXY SUBSTITUTION`, which requires a *named* target displaced by a
  *named* enforceable stand-in ("fitness to drive" ← "hours since last
  drive"), and a weld is precisely the case with no second name to point
  at — so on the English reading of condition 2 the hidden components
  become named targets, PROXY SUBSTITUTION absorbs both seed terms, and C1
  falls. **`CW_003`:** two-condition test, four score fields, all four
  measuring condition 1 — condition 2 has no readout, so a term with real
  divergences and good separate handles scores identically to a weld.
  **`CW_006`:** `bias` is |Σ sign|/count with no floor, so one resolvable
  direction reads 1.000 (`null-harness/` `CONSTANT_FIRES`) — claim stands,
  demonstration instance corrected, since the delivered `case_direction`
  returns 0 when the tracked component is unquantified and is therefore
  immune to the specific case the first pass used. **`CW_005`/`CW_007`:**
  both seed terms return `n_cases = 4`, `n_quantified = 0` and `--` for
  both live readouts, so the only live readout does not separate the two
  terms it ships with (the drop's own C3, shown rather than argued); 2 of
  8 named cases carry a readings block, 1 carries a usable ratio, 0 carry
  the two a spread needs — and filling `capital / socialized-downside`'s
  one missing pair returns **`max_spread = 6.768`**, the folder's first
  non-`--` number, in the case whose own note says the divergence between
  those two components "is the entire structure". **`CW_012`:** the
  `--new` template ships a placeholder divergence with an empty id and
  `score()` counts `len(divergences)`, so a blank file scores on the only
  live readout. **`CW_009`:** C5 compares two rates with no denominator on
  either, while the generation rule under it (a representation summarising
  contexts has no gradient separating what the contexts never separate) is
  testable one term at a time — split the claim, don't discard it. Does
  **not** move `UNI_002`: both seed terms are policy/economics, so a ninth
  mechanism holding two same-field cases adds nothing to the cross-field
  check. Stdlib only, phone-buildable, CC0.
- `presented-binary/` — Two instruments aimed at a presented two-option
  framing from opposite sides, plus a nine-claim table (`B1..B9`).
  `binary_audit.py` audits the framing **before it is answered**: eleven
  checks across two blocks (option space O1–O6, sacrifice S1–S5), each
  resolving to `documented` / `asserted` / `absent`, with no verdict
  computed — the readout is how much of the framing has a record behind
  it. `frame_sim.py` runs the same question at a model: pass 1 works
  inside the frame and is **hash-sealed**, only then is pass 2 (the wide
  pass) released, and pass 3 asks whether any pass-2 option beats the
  pass-1 choice **on pass 1's own stated metric** — an internal
  comparison, so no external answer key is needed and a run cannot be
  graded generously by picking a better metric afterward. Ten claims
  `PB_001..010` in `AUDIT_NOTES.md`; the delivered `CLAIM_TABLE.md` is
  untouched. **`PB_002`, the sharp one:** the seal is enforced at one gate
  and not the other. `cmd_prompt2` carries `if verify(rid) is False`;
  `cmd_submit2` checks only that `seal.json` EXISTS and `cmd_submit3`
  checks nothing — so a `pass1.json` rewritten after sealing flows
  straight through, and **prompt 3 is generated from the edited choice**
  (measured: `Pass 1 choice: b`, the value written after pass 2 was seen).
  Prompt 3's answer is `dominated_on_own_metric`, which is B9's entire
  readout. `cmd_report` does print `SEAL BROKEN`, so it is caught — after
  the comparison has already been asked and answered against a tampered
  pass 1, which is the exact failure the seal exists to prevent. One line,
  the one `cmd_prompt2` already has. **`PB_003`:** "prompt withholding" is
  commitment, not confidentiality — `PROMPT_2` and `PROMPT_3` are
  module-level string constants readable before pass 1 is written, and the
  operator is the model; `divergence-playground/seal.py` states this limit
  about itself ("accidental-peek defence, not cryptographic") and this
  drop does not. The property B7–B9 actually need is commitment, and the
  seal does deliver that. **`PB_006`/`PB_010`, a pincer on the same
  field:** B8's readout is `incompleteness_acknowledged`, which `PROMPT_1`
  **requires in the JSON it asks for** — so the flag is produced alongside
  the reasoning rather than about it, a self-report from inside the thing
  being measured (`triad-playground/` `TP_006`, `reasoning-dial/`
  `RD_009`) — while `cmd_seal` requires `options`/`choice`/`metric` and
  **not** that field, so a pass 1 without it seals clean and reports
  `frame_flagged None`. Over-elicited by the prompt, under-required by the
  gate. **`PB_004`:** `option_gain` is `None` both when the wide pass
  found zero options and when it never ran (`if (n2 and n1)` treats 0 as
  falsy) — a loud finding and an incomplete run scoring alike, in the
  field B7 is stated in. **`PB_005`:** `--submit3` is parsed but absent
  from the documented usage while `cmd_submit2` prints prompt 3, so the
  documented workflow leaves `dominated_on_own_metric` at `None` on every
  run and B9 is unreachable in both directions. **`PB_007`:**
  `documented_share` is `documented/n`, so eleven assertions and eleven
  silences both return 0.000 — `uninstrumented/`'s SCALAR DEMAND on the
  drop's own headline number, and `criteria-drift/` `CD_002`'s
  ordinal-compared-as-nominal; an `answered_share` separates them at no
  cost. **`PB_008` records what holds:** every default in `binary_audit.py`
  runs toward `absent` — blank template 0 of 11, missing entry absent,
  malformed state counted absent AND named — the opposite of
  `category-weld`'s template, which scores 1 on its only live readout
  (`CW_012`). **`PB_001`:** both verification sentences in the delivered
  `CLAIM_TABLE.md` name artifacts the drop does not carry — the seeded
  case and the `frame_sim` fixtures — the second consecutive drop with
  that shape after `CW_001`. `cases/` is left **absent rather than
  reconstructed**, since it is data and inventing one would put a framing
  in the author's mouth; the three claimed `frame_sim` properties are code
  behaviour and are checked directly instead (two hold, one is a naming
  problem). **`PB_009`:** B5 ("'a few' is a category weld — headcount and
  functional position score identically") is directly runnable in
  `category-weld/` and no `welds/a_few.json` exists — the cheapest test
  either folder has, and the first weld term from outside
  policy/economics, which is `UNI_002`'s open question.
  **Second drop** closes `PB_001`'s first half and adds a router.
  `cases/ventilator-surge.json` lands and scores **0 documented of 11**
  exactly as the claim table said (3 asserted, 8 absent); its O5 record
  names six alternatives — split ventilation, manual bag-valve rotation,
  transfer, cycling, regional load-sharing, random allocation — none
  refused on the record, which is B1 and B2 instanced rather than argued.
  `binary_audit.py` gains `handoff()`: O1 documented at a count ≤ 2 routes
  the case to `generation-capacity/capacity.py`, on the stated reasoning
  that "an option-space audit closing clean on a low DOCUMENTED count is
  the signature of removed generation capacity, not evidence of its
  absence" — the answer to `GC_002`, and it refuses to estimate a count
  from prose. B7 moves to supported at n=2 (gain 3.5 both runs), and the
  drop marks **B8 NOT TESTED under contamination** on its own initiative,
  reaching `PB_006` from the protocol-anticipation side; the clean test it
  proposes does not fix `PB_006`'s channel, since `PROMPT_1` still asks for
  the field. **`PB_011`, the one with a consequence:** the drop carried
  `binary_audit.py` **three times** — two uploaded files byte-identical to
  each other and to the pre-handoff repo copy, plus the live version
  inline. First time `MF_019`'s copy-drift mattered: landing the uploads at
  face value would have silently reverted the router the same drop
  introduced, since both stale copies parse, run and pass every existing
  check. **`PB_012`:** `handoff()` returns bare `None` both for a count
  above the ceiling (a measurement) and for O1 never checked (a gap), while
  the `{"route": None, "reason": ...}` shape it already uses one branch
  over is the fix — fourth instance of that shape across four folders.
  **`PB_013`:** the router's firing branch has no case in the repo;
  `ventilator-surge` has O1 absent, correctly, and the case that would fire
  it is `generation-capacity`'s undelivered `food-knowledge`.
  **Third drop repairs `PB_006` at the source.** `incompleteness_-
  acknowledged` is removed from `PROMPT_1` entirely and replaced by a
  blind post-hoc rater: `PROMPT_F` shows a reader only the pass 1 output
  and asks the neutral `set_stated_as_complete`, naming neither pass 2 nor
  the protocol nor the frame — the inversion to `frame_flagged` is done by
  code, not by the rater — and `frame_flag()` now returns provenance
  (`blind` valid for B8 / `cued` NOT valid / `none` unrated) instead of a
  bare boolean, so the two prior runs are re-labelled rather than silently
  kept. B8 is measurable for the first time. **`PB_014`, what the repair
  left behind:** `cmd_report` nudges the operator to run `--flag` only when
  `source == "cued"` — the state the repair abolished — so every run under
  the new `PROMPT_1` lands on `source == "none"`, prints "NOT valid for
  B8", and is told nothing; the instruction to take the one step that makes
  B8 measurable is attached to the population being replaced and withheld
  from the population replacing it. Two of this session's standing findings
  **widen** rather than close: `PB_002` (`cmd_flag` and `cmd_submit_flag`
  verify nothing either, so 1 of 5 commands checks seal integrity, and the
  blind rating B8 now rests on can be taken on a tampered pass 1) and
  `PB_005` (three undocumented flags now — `submit3`, `flag`,
  `submit-flag` — so the documented workflow leaves BOTH B8 and B9
  unreachable). `PB_010` **dissolves**: the field is gone, so the seal gate
  has nothing to require, and the blind rating necessarily happens after
  sealing.
  **Fourth drop lands the canonical README and a tenth claim.** The
  README documents all nine `frame_sim` flags — **`PB_005` CLOSES**, every
  parsed flag now has a documented invocation and the BLIND FRAME RATING
  section explains why `--flag` exists rather than only listing it. What
  replaces it is smaller: `frame_sim.py`'s header still lists six, so the
  folder has two hand-maintained usage blocks that have already diverged
  by three entries — the `reasoning-gate` `guards.json → GUARDS.md`
  arrangement in reverse, where one source generates the doc and a test
  asserts they match. **`PB_014` does not close and is confirmed from a
  second direction:** the README documents `--flag` in its own section and
  leaves it out of the main usage sequence, so both routes to the blind
  rating are optional side paths — the code does not prompt for it on the
  state that now occurs, and the documented sequence does not include it.
  New **`B10`** claims a documented low option count is the mechanism-10
  signature rather than evidence of an adequate search; its status
  sentence gets the router's standing exactly right ("changes where the
  case goes, computes no verdict, adds no state to the 11 checks") and
  **discloses its own weak point** — `HANDOFF_CEILING` is a constant, and
  nothing establishes that 3 or 4 generated options indicates intact
  capacity. **`PB_015`:** "routing logic verified on 8 synthetic paths"
  names a test file the folder does not carry (fourth instance of that
  shape; the prior three were real and late), and the disclosed weak point
  has a reachable next step the table does not name — R1 is an
  option-generation ceiling by construction, so a populated `capacity.py`
  gives the number the router's constant is currently guessing. Stdlib
  only, phone-buildable, CC0.
- `generation-capacity/` — Proposed **tenth exclusion mechanism** for
  `uninstrumented/`, one drop after `category-weld/`'s ninth.
  `MECHANISM_10.md` (delivered verbatim, a marker under exploration) names
  GENERATION CAPACITY REMOVED: the excluded quantity is the **option space
  itself** — the set of alternatives a party can produce, not a value
  inside it — excluded by prior removal of the capacity to generate
  options, at a scale and on a clock the affected party has no access to.
  The distinguishing sentence: "nothing is suppressed at decision time
  because nothing is there to suppress." Three readouts specified (R1
  recall ratio = nameable/present per place per generation, R2
  transmission interval, R3 loop check), none with readings. Seven claims
  `GC_001..007` in `AUDIT_NOTES.md`; `MECHANISM_10.md` untouched, and
  nothing reconstructed after `CW_004`. **`GC_001`, the checkable one:**
  VISIBLE AS claims a binary under this mechanism "passes an option-space
  audit truthfully", and `presented-binary/binary_audit.py` — landed one
  commit earlier — is exactly that audit. A framing under the mechanism,
  answered honestly, scores **11 of 11 documented**. O3 is the cell it is
  aimed at: it asks who generated the options and whether they are inside
  the affected set, exists to catch options generated by people who do not
  carry the consequences, and under this mechanism the affected party DID
  generate them — so the reassuring answer is the mechanism's signature.
  O5 is the second: widening a search over a reduced generator returns
  nothing new, which reads as confirmation the set was complete. **The
  drop understates its own case** — `documented_share` grades whether a
  record exists and never reads it, so a damning answer set scores
  1.000 identically; the pass is over-determined. **`GC_002`:** the gap
  cannot be closed by a twelfth check, because
  `documented`/`asserted`/`absent` resolve against the answering party's
  own record and **an absent generator produces an absent record of
  itself**, which reads as a documentation gap — so `presented-binary/`
  cannot be extended to cover this and needs a second instrument beside
  it. **`GC_003`, the denominator fork:** R1's two named sources are not
  interchangeable — floristic inventory is independent but scoring
  resident recall against it needs a local-name-to-species mapping, which
  is the central-reference scoring the drop's own CALIBRATION CONSTRAINT
  forbids; ethnobotanical inventory is translatable but inherits the
  recall of whoever was surveyed, making the ratio an R2. Part of what the
  drop files under "collection gap" is a units question that has to be
  settled before a numerator is collected. **`GC_004`:** R3's negative
  branch is unreachable — "evidenced by citation or absent" gives no state
  meaning "searched, and not cited" (`null-harness/` `CONSTANT_SILENT`);
  the repair is the denominator R1 already has, a named corpus and
  interval. **`GC_005`:** distinct from the nine on a structural check,
  and `AUTHORED REFERENCE` is its **mirror rather than its match** — same
  defect in the reference, opposite direction of authorship, and the
  remedies are opposite, since an external fixed reference repairs that
  one (`ANC_005..008`, `CD_008`) and worsens this one when the reference
  is the center's. **`GC_006`:** SELF-MAINTAINING ("active restriction
  needs continuous expenditure; a removed generator needs none") is a rate
  comparison already modelled twice in this repo —
  `rigidification-sensor/simulator.py`'s continuation-vs-reversal cost
  with `locked_at`, where zero maintenance is `continuation → 0`, and
  `sustained-activation-gate/`'s double well at zero drive; R2 is the time
  axis both run on. **`GC_007`:** the consent claim's entire empirical
  load sits in R1's numerator — the step from inability to
  unavailable-consent is close to analytic, and the antecedent is what is
  unmeasured. Does **not** move `UNI_002`: it arrives with a seed case and
  no filed entry.
  **Third drop lands `SUBCASE_10A.md` — IRRECOVERABLE SOURCE**, where the
  party removing the capacity and the party bearing the loss are the same
  and the source cannot be returned to (seed case: a specimen destroyed to
  obtain one reading). Three properties each independently prevent the
  loss registering: no excluded party, an unbounded and unformed
  foreclosed set, and **zero substituted for unknown** — the same move as
  the parent's calibration constraint at a different site. **`GC_010`:**
  its S1 readout is three-valued with **absent and zero explicitly
  distinguishable**, which is the repair this audit recorded four times
  across four folders (`PB_004` option_gain, `PB_012` handoff, `GC_004`
  R3, `MD_002` reduces_to) — designed into the specification before any
  code exists, which is the only point in the cycle where it is free.
  **`GC_011`:** the sub-case names a third denominator state,
  *unconstitutable*, distinct from `GC_003`'s units-blocked and from the
  parent's collection gap — "the plants are still growing whether or not
  anyone can name them" versus "the denominator is destroyed with the
  source" — which bounds `GC_003` to the parent rather than repeating or
  rescuing it, and the sub-case's own move is stronger: do not measure the
  loss, measure the procedure, since all three readouts are properties of
  the record and records exist. **`GC_012`:** S1/S2/S3 have no fields in
  `capacity.py` and no slot in its `SKELETON` — the `MF_017`/`CW_015`/
  `DL_004` shape again, and cheaper here than in any of them since all
  three are properties of one record. The OPEN section fixes its own
  boundary before classifying, the third folder to state that discipline.
  **Second drop** fills the folder: canonical `README.md`, the `capacity.py`
  scorer, `CLAIM_TABLE.md` (G1–G8 plus a DISCLOSED WEAKNESSES section), and
  `cases/informed-gate.json`. `--selftest` passes 8/8 as the README states.
  **`GC_002` is ANSWERED, not refuted** — the argument was that the repair
  is a second instrument beside `binary_audit` rather than a twelfth check,
  and the repair delivered is a second instrument plus a router.
  **`GC_003` sharpens against the code:** `capacity.py` implements the
  CALIBRATION CONSTRAINT as a `scored_against` field that flags
  center-scored readings invalid and drops them from the slope — which
  closes the case the constraint names, and is a **declaration rather than
  a unit check**. Nothing reads `source_present`/`source_nameable`, so a
  case declaring `place` with a Linnaean denominator and a local-name
  numerator returns a clean slope (−0.23, `invalid_scoring 0`). The drop's
  DISCLOSED WEAKNESSES names the numerator half (free vs prompted vs
  recognition vs demonstrated use); the denominator half is unnamed and is
  the half the constraint is about. **The check the schema can already
  make:** R1 cannot exceed 1 when the units match, and `present 40,
  nameable 55 → ratio 1.375, valid True, no warning` — a unit-mismatch
  detector computable from two fields already present. **`GC_008`:** G3's
  status says an enforcement-cost series is an instrument "this repo has no
  instance of", and `rigidification-sensor/simulator.py`'s `run()` returns
  exactly that per tick as `continuation`; what is missing is a MEASURED
  series, which changes the next step from build-a-simulator to
  collect-a-series. **`GC_009`:** the second seed case, `food-knowledge`, is
  named in the README's STATE, in DISCLOSED WEAKNESSES and in G2's status,
  and did not arrive — third consecutive drop with that shape, and the one
  case that would fire the new handoff router. Left absent rather than
  reconstructed, on the `CW_004` lesson. The drop's own DISCLOSED WEAKNESSES
  names `G5 by construction` — `informed-gate` has
  `deficit_cited_as_grounds` set true because the case was written to
  instance the loop — which is the `CONSTANT_FIRES` half of `GC_004`,
  reached independently. Stdlib only, CC0.
- `moral-decomposer/` — Takes a disagreement presented as moral or
  ethical and decomposes it into option-distribution claims plus the
  frames those claims imply; the output is the **residue**, what still
  disagrees once the lower stages are matched. Three stages: **option
  layer** (per party — enters the tally, generates options or held fixed,
  decides, plus what each side took out of the variable environment,
  with divergence COMPUTED between sides rather than declared), **frame
  layer** (the boundary criterion the assignments imply, whether
  documented, whether acquired in development rather than selected), and
  **cut count** (further boundary decisions the frame requires, and how
  many are documented — a frame that terminates needs one cut, a frame
  that orders needs a supply). Delivered verbatim: `README.md`,
  `CLAIM_TABLE.md` (M1–M5 plus a DISCLOSED WEAKNESSES section), and two
  cases (`animal-standing`, `means-to-save`). **`decompose.py` is named
  five times in the README and did not arrive**, and is deliberately NOT
  reconstructed — `category-weld` `CW_004` is what the one prior
  reconstruction of this kind cost, and this README fixes far less of the
  arithmetic. Six claims `MD_001..006`. **`MD_001`:** M5 ("zero live
  residue is an absence, not a proof") has its entire status in the
  missing file — "the selftest includes a fixture with a live residue
  item, so a non-empty residue is representable and the instrument is not
  rigged toward M1" — and on the delivered corpus **0 of 4** residue
  candidates are live, so nothing in the folder shows the detector can
  fire; fifth consecutive drop whose status sentence names an absent
  artifact. **`MD_002`:** `reduces_to: null` carries two opposite
  meanings — the README makes it *the finding* ("candidates that reduce
  to neither are the case the instrument exists to find"), and
  `means-to-save`'s last candidate is `reduces_to: null` **and**
  `resolved: true`, because it is agreement between the sides routed to
  `presented-binary` rather than residue between them. The reading is
  right and is the most interesting cell in the drop; the cost is that
  only an author-set boolean separates the finding from its opposite. A
  third value (`routed`) fixes it. **`MD_003`:** M3's stated asymmetry —
  3 undocumented cuts vs 0, both cases, opposite file positions — is
  exact to the digit; `terminates` is a separate asserted field and
  nothing checks it against the cut list, so a frame nobody enumerated
  scores as terminating. **`MD_004`:** the README's RUN ORDER requires
  welded terms decomposed first, and **4 named across 2 cases, 0 exist**
  in `category-weld/welds/` — `the few` is `presented-binary` B5's "a
  few" under a different article, so two folders now point at one missing
  `welds/a_few.json`. **`MD_005` holds:** 0 of 22 distinct field names
  carry a moral term; the schema is positional and directional
  throughout, and the dispute's own language sits in free-text values
  where it belongs. **`MD_006` holds:** the drop's first disclosed
  weakness is the finding an auditor would lead with, with the mechanism
  named — "the reductions here were produced by the same process that
  predicts them" — and `animal-standing`'s source field records a
  candidate counterexample that failed and was kept with its failure.
  **Second drop lands `mortuary-practice`** — from a classroom exchange,
  the **first case in the folder not built by the model**, and the one
  that reaches furthest toward M1's own falsifier. **`MD_007`:** it is the
  first case where stage 1 matches on EVERY party, and it does not meet
  the falsifier because that also requires the `held_fixed` lists to
  match — they differ by exactly one item, `"which practices are available
  to score against"`, and that item is the disagreement. M1 survives at a
  now-visible margin of one entry. **`MD_008`, the measurement:** across
  six sides in three cases, `cuts_required` length,
  `criterion_documented` and `terminates` are perfectly collinear — two
  distinct triples `(1, True, True)` and `(3, False, False)`, no
  independent variation — so M3 has n=3 on one distinction rather than
  three converging measurements. `category-weld`'s own mechanism turned on
  the sibling folder's schema: three quantities that could diverge, never
  observed diverging, all set by the same hand. Breaking it is cheap — a
  documented criterion that still needs many cuts, or one cut with an
  undocumented criterion. Residue is now 0 of 7 across three cases, and
  `reduces_to: null` carries three distinct non-residue meanings
  (agreement between sides / a real finding on a different quantity / a
  property of the question's setup) plus the intended one. CC0.
- `domain-ledger/` — One file, `ledger.py`, making a confidence readout
  **derived instead of asserted** by recording the domain set the number
  was taken over: "61 percent over one domain set is a different quantity
  than 61 percent over another." Four readouts returned separately and
  deliberately not combined — **coverage** (held / read), **cycle depth**
  (holds that survived a return / holds), **adversarial** (read domains
  where the shape was pushed against / read), **truncated** (reads cut
  short at a discomfort threshold / read) — plus a **reservation**, a
  standing fraction held as unknown. Selftest 13/13. No `shapes/`,
  README or claim table delivered; nothing here invents a shape. Five
  claims `DL_001..005`. **`DL_001` holds:** the identifiability argument
  is `criteria-drift` `CD_008` / `anchor-interval` `ANC_006` restated for
  a confidence readout, and the tool follows it — the docstring states
  why coverage and cycle depth are different currencies, and the table
  footer prints each column's denominator, so `measurement-fork`'s VOID
  RATIO check is made unnecessary rather than enforced. This is the one
  scorer in the family that refuses the single-headline-number reduction
  up front. **`DL_002`:** the reservation is described as capping
  reported headroom and nothing applies it — `ceiling = 1 - reservation`
  is computed, returned and printed, and read by nothing, so ten
  all-hold domains at reservation 0.20 give coverage 1.00 against a
  ceiling of 0.80 with no readout saying so. The cap is stated as a
  function and shipped as a constant. **`DL_003`:** `coverage` puts
  `mixed` in the denominator only, so all-break and all-mixed both return
  0.00 — `PB_007`'s shape on a fourth scalar, in a tool that avoided it
  on the other three; the fix is a footer clause, not a fifth ratio.
  **`DL_004`:** `detail()` reads `criterion_fixed_in_advance` and `open`
  and `SKELETON` carries neither, so `--new` never prompts for the
  pre-registration guard — `CW_015` repeated in a second folder, with the
  guard promoted from prose-in-a-list to a first-class field. The tool
  does deep-copy its skeleton, which `weld.py` and `capacity.py` do not.
  **`DL_005`:** with no `shapes/` directory it prints a well-formed
  report with zero rows and exits 0, where all three sibling scorers
  refuse on stderr with rc 1 — a report whose denominator is zero,
  rendered as though it had one, in the tool built about denominators.
  The selftest covers the empty case at the `score()` level; the gap is
  at the presentation layer it does not reach.
  **Second drop lands the first shape**, `hierarchy-cut-generation`: 30
  domains, 0 read, `asserted_coverage` 0.61. **`DL_006`:** the tool's
  whole argument instanced — the asserted 0.61 sits beside a derived `--`
  and `detail()` prints "ledger not yet populated" rather than
  substituting the asserted value or a zero. The one place in the repo
  where an author has written down a number they were already carrying and
  then run the instrument that declines to confirm it. **`DL_007`:** the
  shape names which of `category-weld/welds/hierarchy.json`'s five senses
  it runs on ("the other four senses, which are not this claim" — 5 minus
  1 = 4, exact) and pre-classifies two of thirty domains by weld sense
  BEFORE reading, which is the only time that classification is not
  closure by construction. **First time in this drop family that a stated
  cross-folder precondition is met** — `moral-decomposer` `MD_004` records
  the opposite state one folder over, seven welded terms named and zero
  decomposed. `criterion_fixed_in_advance` carries the same discipline
  into the read, naming the failure and the routing for the ambiguous case
  (MIXED with the reason recorded) before any domain is read. `DL_004`
  stands: `SKELETON` still carries neither guard field.
  **Third drop lands `anchor.py`**, a companion on the argument that
  coverage "resolves position inside a band that something else already
  set". Three bands by class of support (`none` 0.30 / `external` 0.80 /
  `cycle_persistent` 0.99) and three routing states per provenance link;
  selftest 14/14. **`DL_008`:** it keeps `unrouted` and
  `absent_established` apart and says why — "collapsing them into
  'blocked' loses the distinction the map exists for" — which is the
  **fifth instance of one repair** across this family (`PB_004`,
  `PB_012`, `GC_004`, `MD_002`, `GC_010`) and the **first implemented**
  rather than specified: counted separately in the readout and restated in
  `blocking()`'s own output. **`DL_009`:** `target_band` and
  `corroboration.class` are both described as band-setting and only the
  second reaches any document-level field — an anchor with
  `target_band=cycle_persistent` (0.99) and external corroboration yields
  a document ceiling of 0.80, and the selftest pins exactly that, so the
  code follows the BANDS heading while the opening paragraph ("anchoring
  near something that has survived generational cycles raises the number")
  describes a quantity the code records and never aggregates.
  **`DL_010`:** the refusal to emit a composite is real and
  selftest-enforced (`"no composite emitted"`), which is `DL_001` one step
  further than `ledger.py` goes — and the two numbers it does emit,
  `ceiling` and `anchor_spread` (exactly four values: 0.0 / 0.19 / 0.5 /
  0.69), are functions of three stipulated constants with rationales and
  no derivation, the same shape as `HANDOFF_CEILING` which B10 discloses
  and this does not. **`DL_004` half-closes:** `anchor.py`'s `SKELETON`
  carries `open`, which `ledger.py`'s does not — same author, next tool,
  half the gap fixed unprompted; `criterion_fixed_in_advance` is in
  neither and `anchor.py` does not read it, which is consistent since an
  anchor map does not classify. `DL_005` recurs unchanged.
  **Fourth drop lands the first anchor map** (`hierarchy-imposed-ordering`,
  3 anchors / 9 links / 0 quantified) and a docstring-only `ledger.py`
  change — code byte-identical after stripping the module docstring.
  **`DL_009` is CORRECTED against this audit:** it read the docstring's two
  band-setting sentences as a possible defect in the code, and the map
  settles it in a note the schema already had a field for — "the target
  itself sits in the cycle-persistent band; what is external-band is the
  connection between imposed ordering and maintenance cost, not the
  thermodynamics." `target_band` is where the TARGET sits,
  `corroboration.class` is the support for the CONNECTION, aggregating the
  second is right, and only one docstring sentence survives the
  correction. **`DL_013`:** the map's `open` list states three numbers
  about itself — spread 0.5, ceiling 0.80, no link quantified — and all
  three are exact; its fourth item names the folder's thesis instanced,
  that routing one unrouted link (cost-gradient-by-depth-of-ordering)
  "would do more than reading further domains, because it converts the
  near anchor from stated to measured". **`DL_011`:**
  `absent_established` is used 0 of 9 times — implemented, counted apart,
  and not yet earned, since it requires having looked and `unrouted` is
  what you have before you look. **`DL_012`:** `unrouted` holds three
  de-facto states (attempted-and-open / queued / no-instrument-nameable),
  `unrouted_total` merges all three at 6, and the two with no path nameable
  are the ones whose notes ask for instrumentation that does not exist —
  the same distance from a reading as `absent_established`, reached from
  the other side; the schema already carries `paths_attempted`/`paths_open`
  to separate them. **`DL_002` sharpens rather than closes:** the drop
  derives the 0.2 reservation default from the external band ceiling
  (1 − 0.80, exact) and adds "do not read a ceiling off this file alone",
  so one of `DL_010`'s three constants now has a source — while `ceiling`
  is still computed, printed beside `RESERVATION`, and read by nothing.
  **Fifth drop lands `A2.md`** — a candidate definition for the term the
  whole confidence function turns on, deliberately not adopted. **`DL_015`,
  the diagnosis checked against the code:** A2 says what makes an anchor
  near versus far is unspecified, and that is exact — distance is
  operationalised as `BAND_CEILING[corroboration.class]`, the class is a
  string the author writes into the anchor file, and no routine derives it
  from anything; `DL_010` reached the same place from the other side. The
  candidate is **load-bearing capacity** — an anchor is near because it is
  *assemblable*, so a hard physical law is near not because it is
  prestigious or well-studied but because it does not drift while
  something is built on it — which is `constraint-assembly`'s invariant
  class read as a band, and would make the anchor map a load table with
  confidence derived rather than primary (a rewrite, not an amendment,
  which is why it stays in prose). **What the note does that matters more
  than the candidate:** it refuses to adopt it and names the reason as
  non-independence — "the convergence was noticed in the same conversation
  that produced both descriptions" — which is `triad-playground` `TP_003`'s
  shared-bias result applied by the author to their own convergence,
  before anything rests on it, with the falsifier named as a search
  (something well-corroborated that is not assemblable, or something
  assemblable with thin corroboration) and recorded as not yet run.
  **`DL_014`:** the note opens by sourcing its own subject to
  `CLAIM_TABLE.md`, which the folder does not carry, and `A2` appears
  nowhere else in it — sixth instance of a reference naming an absent
  artifact in this drop family (`CW_001`, `PB_001`, `GC_009`, `PB_015`,
  `MD_001`), three of which landed a drop later. Fifteen claims
  `DL_001..015`.
  CC0.
- `closure-cost/` — One file, `closure.py`, reading recorded cases where a
  variable was closed before the event arrived. The shape: **response
  failure tracks whether a variable was carried as live**, not whether the
  event was severe and not whether information was available — a variable
  closed as impossible has no handling class attached because none was
  needed, so when the event fires the delay is categorisation rather than
  reaction. Two branches kept apart: **instrument** (a reliable
  intermediary becomes the reading, the underlying quantity stops being
  sampled, and failure clusters where the intermediary has been correct
  longest) and **event** (the occurrence is closed as
  not-happening-here, so procedure is never acquired or never retained).
  Selftest 15/15. No `cases/`, README or claim table delivered; nothing
  here invents a case. Six claims `CC_001..006`. **`CC_001` holds, and is
  the strongest schema move in this drop family:** the competing
  explanation is held as a **field** (`procedure_gap.collapsed_into_-
  closure` + `ground`) rather than as prose, and the docstring states that
  the rival is **not independent** of the shape — "nobody acquires a
  protocol for an event they have closed" — which is the harder admission,
  since a non-independent rival cannot be ruled out by finding the shape.
  `knowledge_state` is four-valued (`not_taught` /
  `taught_not_retained` / `retained_not_executed` / `not_separable`),
  the sixth instance of the absent-vs-known-negative repair in this family
  and the third designed in. **`CC_002`, the sharp one:**
  `availability_rules_out_procedure_gap` uses `bool(...)`, so "checked,
  information absent" and "never recorded" both return `False` — in the
  one field that adjudicates the rival — while `budget_consumed` two lines
  away returns `None` correctly and is pinned by the selftest's own
  "budget flag none not false". Same repair, same file, one applied and
  one not. **`CC_003`:** `knowledge_separable` is `!= NOT_SEPARABLE`, so a
  case omitting the field reads as separable — the default runs toward the
  informative state, the opposite of `presented-binary` `PB_008` where
  every default runs toward `absent`; `SKELETON` is safe, a hand-written
  case is not. **`CC_004`:** `--case` and `--branch` have no bounds check
  where both sibling tools do (`--case` alone raises `IndexError`), and an
  unknown branch prints an empty table with rc 0 while an unknown case
  errors with rc 1. **`CC_005`:** the `instrument` branch is
  `uninstrumented`'s PROXY SUBSTITUTION with a **rate term added** —
  `signal.years_correct` — which the register's entry does not carry;
  an addition to an existing mechanism, checkable in principle with no new
  vocabulary. **`CC_006`:** with no `cases/` it prints a well-formed report
  with zero rows and exits 0 — third tool in the family, and the three
  that refuse are the older ones; its footer does state the corpus
  condition ("the records were not built to ask this"), which the other
  two do not.
  **Second drop lands the README, `CLAIM_TABLE.md` (C1–C5 + DISCLOSED
  WEAKNESSES) and three cases** — `hawaii-missile-alert`,
  `breakdown-cones` (design only), `dash-warning-light` (the instrument
  branch's only case). Every README STATE claim checks out exactly: three
  cases, zero quantified, every `spend` cell `--`, every `knowledge_state`
  `not_separable`. **`CC_007`, the strongest move in the drop:** the README
  refuses to fill `diagnostic_spend` — the readout the folder exists for —
  from Hawaii's 38 minutes, and names the mechanism: "that is the duration
  of the ERROR, not of anyone's decision, and substituting it would be
  proxy substitution". The refusal is specific, not blanket: the
  denominator (900 s, flight time under a real threat) IS filled and the
  numerator is refused, with the note saying which and why. Elsewhere in
  this repo the register's mechanisms diagnose an instrument after the
  fact; here one is used ahead of time as a reason not to produce a
  number. **`CC_008`:** the docstring says "a case that mixes them is
  recorded as mixed rather than forced into one"; the corpus holds exactly
  one such case (Hawaii's siren-silence fragment, an instrument-branch
  reading inside an event-branch case), it is coded `event`, and both the
  case's own open list and C4's status hold the question open — so the
  stated rule and the open question point different ways. Distinct from
  `DL_011`, where the unused state was unearned; here it is earned,
  acknowledged twice, and a different value is recorded. **`CC_009`,
  `CC_002` instanced:** `dash-warning-light`'s procedure-gap rival is NOT
  APPLICABLE (procedure is not the missing quantity on that branch;
  direct sampling is) and `availability_rules_out_procedure_gap` returns
  `False` — the same value a checked-and-absent event case returns. Three
  distinctions now, not two. **`CC_010`:** two circularities disclosed
  before use — `variable_state` inferred from the same evidence C3 rests
  on, so C3 and that case's coding are not independent; and C5's nearest
  series carrying an exposure denominator modelled per the very category
  under test, which is `GC_003`'s shape caught in advance rather than in
  audit. Neither is softened. `signal.years_correct`, the rate term that
  makes C5 invert standard scoring, is 0 of 3 — including on the one case
  on the branch it defines. **`CC_003` is not tripped by the delivered
  corpus**, which is the point: a default running toward the informative
  state is invisible on data written by someone who knows the schema. CC0.
- `constraint-assembly/` — One file, `assemble.py`, recording cases where
  sufficiency was **composed from parts that individually do not do the
  job**. Construction, not selection: an option that did not exist in the
  environment, assembled from insufficient components under a fixed
  budget. **The reversal it encodes** — constraints are not what limits
  the option set, they are what makes composition *decidable*; a term that
  will not move can be leaned on, a soft term cannot, because there is no
  way to know when the pieces add up, so the parts inventory is domains
  with hard laws in them. Three classes kept apart because merging them
  loses a failure mode: `invariant` (holds regardless of use, cannot be
  spent), `consumable` (finite, availability destroyed by spending —
  partial use can be worse than none, so it is a resource and a hazard in
  the same term), `soft` (does not hold under load, recorded so reliance
  is visible rather than to score anybody). Rejected candidates are the
  data: each rejection names the constraint that ruled it out, and a case
  with no rejections is selection, recorded as such. Selftest 18/18. No
  cases, README or claim table delivered; nothing here invents a case.
  Seven claims `CA_001..007`. **`CA_001` holds** — the reversal has a
  mechanism in it (decidability, a stopping rule) and runs opposite to the
  two nearest folders on the same object without contradicting either:
  `generation-capacity` reads an option space REDUCED upstream,
  `presented-binary` one CLOSED at presentation, this one an option
  CONSTRUCTED from parts, and only this one treats hard laws as the parts
  inventory. **`CA_002` holds:** `composition_present` **fails closed** —
  an unrecorded `sufficient_alone` blocks the claim and is reported
  separately as `sufficiency_unknown`, so a case that failed the test is
  distinguishable from one that could not be tested; the ninth instance of
  the absent-vs-known-negative repair in this drop family and the fourth
  designed in rather than found. Its companion `selection_not_assembly` is
  aimed at the nearest neighbour — selection from presented alternatives
  is what assembly is most likely to be mistaken for — and is a column in
  the table rather than a caveat in prose. **`CA_003`, the sharp one:**
  the headline claim is about the AVAILABLE inventory ("more hard
  constraints, more composition available") and `score()` filters to
  `used` on its first line, so no readout counts available-but-unused
  components — a case with 5 components, 2 used, returns
  `invariant_count 1` and nothing counting the other 3. **Not the usual
  missing-field shape** (`MF_017`, `CW_015`, `DL_004`, `GC_012` are all a
  stated rule with no schema slot): here the slot exists, since `used` is
  a per-component boolean, and the readout does not — which is cheaper
  still, one line, and it is the number that would let the claim be
  checked across cases. Without it `invariant_count` reads as an inventory
  measure and is a composition measure. **`CA_004`, the narrow version of
  the usual shape:** `rejections_all_grounded` returns `False` both for an
  ungrounded rejection and for a case with nothing to ground — narrow
  because `selection_not_assembly` sits beside it, the table prints both
  columns and the footer states the rule, so what is left is only that the
  field is unsafe to quote alone. **`CA_005`:** `--case` is unguarded and
  raises `IndexError` with no argument while `--new` in the same function
  IS guarded with the expression both `domain-ledger` tools use — `CC_004`
  recurring unchanged in the next tool. **`CA_006`:** the DIAGNOSTIC
  QUARANTINE section names the same budget `closure-cost` measures, from
  the other end — that folder reads the categorisation stall as a fraction
  of budget consumed, this one records whether the operator declined to
  spend it and assembled without knowing the cause — the first time in
  this drop family that two folders name one budget, and stated by the
  author rather than inferred. "Deferral is a recorded property, not a
  virtue" is the harder version of the module's own "No scoring of the
  operator", since deferring is the behaviour the shape predicts and is
  still not scored. **`CA_007`:** an empty corpus prints a well-formed
  report with zero rows and exits 0 — fourth tool in the family; the three
  that refuse are the older ones. Stdlib only, CC0.
  **Second drop lands the canonical README and the first two cases.**
  `grade-stop` is an operating record — a loaded rig, engine off on a
  sustained nine percent descending grade, no power steering, no engine
  braking, finite air with nothing recharging it, concrete barrier and no
  shoulder — where a stop was assembled from gravel friction (invariant),
  an uphill grade at the exit (invariant), remaining service air
  (consumable) and unassisted steering, four options rejected with the
  constraint that ruled each out. `flood-ground` is a structural
  placeholder: same operation with no vehicle, testing whether the
  composition belongs to driving or to anything with hard constraints in
  it. **`CA_008`, the sharp one:** `flood-ground` returns
  `composition_present: True` **and** `selection_not_assembly: True`, and
  both the README's STATE section and the case's own `open` list say the
  tool "correctly refuses to read it as assembly" — true of one field and
  false of the other, with the field named `composition_present` saying
  the placeholder IS a composition and the table printing `comp yes`. The
  two are independent by construction (components alone vs rejections
  alone), so the disagreement is structural. The README states the gating
  rule in its own section heading — "a composed solution is only visible
  as composition if what was ruled out, and by which constraint, is
  recorded" — and unlike `MF_017`/`CW_015`/`DL_004`/`GC_012` **no schema
  field and no data is missing**; both inputs sit in the same score dict
  two keys apart, and the code does not combine them. **`CA_009`:** the
  corpus does not exercise `CA_003` either — 7 of 7 components across both
  cases are `used: true`, so no available-but-unused constraint is
  recorded anywhere and the headline claim ("more hard constraints, more
  composition available") cannot be checked against this data even if the
  readout existed; the gap is two-sided. **`CA_010`:**
  `consumables_destroyable_by_partial_use` gets its first non-zero reading
  and the case supplies the mechanism rather than the flag — applying
  enough air to slow but not stop "leaves zero air, zero braking, and the
  grade still acting", which is why it could not be used first — so the
  ORDER of the composition is derived from which terms deplete; the second
  consumable on the same case is `partial_use_destroys: false`, so the
  field separates two consumables rather than tracking the class, and
  `soft` is 0 across both cases (the one class whose whole purpose is to
  be seen when present). **`CA_011`:** the first filled `diagnostic`
  states the shared budget in the case rather than the docstring and names
  which budget (look-ahead and steering) — `CA_006` instanced, and the
  opposite outcome from `closure-cost`'s Hawaii case on the same quantity:
  spend declined rather than consumed. **`CA_012`:** every README STATE
  claim holds exactly except the `flood-ground` refusal, including "zero
  quantities anywhere" — every numeral in either file is a road name (exit
  37, Highway 2, 21st Street) and the grade is written as "nine percent"
  in words, so a case about friction, gravitational conversion and stored
  pressure carries no coefficient, no percentage and no pressure. That is
  the right call and it costs the comparison `CA_009` wants. **`CA_013`:**
  the README's last section is THE WEAKNESS THAT MATTERS MOST and it is
  the module's own undecidability — recognition-primed selection and
  genuine construction are not separable in a single-instance
  retrospective record, "the distinction the whole module exists to make,
  and no case in the file establishes it" — repeated unprompted in the
  case's `open` list, which adds that the rejections are themselves
  recorded from recall. Thirteen claims `CA_001..013`.
- `held-open-uncertainty/` — One prose file, `OPEN_QUESTIONS.md`. A question
  list, not a claim table, against the assumption that a party who holds
  variables open and carries wide variability is therefore **not acting**.
  Nine entries, each declaring a state before it argues, with provenance
  separated per entry. **`HO_001` holds:** three entries name whose
  position they are, and the one marked Claude's carries a retraction
  inside the entry that holds the claim ("asserted earlier in conversation
  with more confidence than it had earned"); Q2 grades its own strongest
  rhetorical move — that nobody asks the question — down to "absence, not
  a result", which is `uninstrumented` `UNI_005` applied by the author
  against their own argument. **`HO_002`:** Q4 and Q5 specify the cheapest
  runnable experiment — present a shape at a stated confidence with an
  explicit action queue attached, vary only the number, count whether the
  response supplies a resolution and whether the named unrouted item
  survives — and it is buildable on apparatus already in the tree, since
  `voice-attractor-probe/` holds the held-constant task list, the jitter
  axis, the response-feature extractor and an offline stub. The design
  passes the check that harness enforces: the high-confidence arm IS the
  control, and Q4's prediction is stated before any run and is
  conditional in the load-bearing way — resolution-supplying rises as the
  number falls *even when the queue is fully specified in the input*,
  which separates "answering an underspecified request" from "reading the
  number as a state of the person". **`HO_003`:** Q8's two-register
  resolution (act on the strongest decision points against the most stable
  anchors while the unknowns stay a separate readout) is not a proposal in
  this repo — `domain-ledger/ledger.py` returns four uncombined ratios and
  `anchor.py`'s selftest asserts "no composite emitted" — so what Q8 needs
  is not an implementation but a case where one register and two give
  different answers on the same material; its own closing line names the
  shape of one ("the confidence map and the operating procedure are one
  document") and no document in the repo is both. **`HO_004`:** Q6's own
  status word is right — `partly routed` — since `constraint-assembly`
  supplies a vocabulary and a place to put cases and the measurement Q6
  names remains unbuilt, which that module's README says in stronger terms
  (`CA_013`). **`HO_005` UNVERIFIED:** Q1 and Q2 carry the file's
  empirical weight (recognition-primed decision work; token-level entropy,
  calibration, faithful hedging) and cite nothing — 5 named literatures, 0
  citations, 1 named author — same status as `ANC_010`, `CD_009`,
  `RD_015`, and nothing in the audit rests on a literature fact; Q1's
  durable half is the distinction rather than the result, that ambiguity
  aversion measures *preference* between known and unknown probabilities
  and not whether holding a variable open impedes acting, and the gap it
  names (whether those results get cited as evidence about action
  capacity) is a citation-tracing question answerable with no instrument
  and no model access. **`HO_006`:** the file is itself a held-open shape
  with an explicit queue — 6 of 9 entries name an unbuilt instrument or an
  unrun search — so Q5's damage case is observable on this artifact, and
  it settles nothing (n=1, no control, and the subject can see the
  manipulation, which is `triad-playground` `TP_004`); what the artifact
  can supply is material for the real run, since
  `domain-ledger/shapes/hierarchy-cut-generation.json` is already a shape
  at a stated confidence (0.61, thirty domains, zero read) whose unread
  list is the queue. Six claims `HO_001..006`. Stdlib only, CC0.
- `adaptive-claim-loop/` — The same architecture as an adaptive simulation
  framework — provenance log, claim system, an agent that reads results and
  proposes a change, a loop that iterates — **with one move removed**. In
  the ordinary shape of this architecture a failed claim hands the agent a
  parameter dial and the agent turns it until the claim passes; that
  operation cannot fail, learns nothing about the system, and the log that
  records it (observation / hypothesis / action / expected outcome, one row
  per step) reads as diligence. `adaptive_loop.py` has no vocabulary for
  it: `Response` has five subclasses and none takes a bare parameter and a
  direction. **`CLAIM_UPDATE`** (the protocol's default — restate the
  claim; needs a break condition that is not the old one and must pass the
  `equivalence-field` epicycle guard), **`MECHANISM_EDIT`** (basis
  independent of this run + prediction registered before the edited sim
  runs + settled with an explicit bool — the `photoperiod-claim-harness`
  guard), **`INSTRUMENT_EDIT`** (artifact removed + quantity unchanged; no
  prediction, because it is not a claim about the world), **`SWEEP`**, and
  **`STAND`** (the failure is the result — the move the delivered
  architecture cannot express). Every free-text field on every response is
  screened for outcome reasoning, not just the one named `reason`. Four
  verdicts (`UNDECIDED` is reachable: a predicate that raised is a broken
  instrument, not a refuted claim) and four termination states
  (`no_admissible_response` has no counterpart in the shape it copies).
  Provenance is append-only JSONL with `SESSION_OPEN`/`SESSION_CLOSE`,
  every row stamped with session and ordinal, and refused proposals logged
  beside admitted ones. Selftest 39/39. **`delivered/`** holds an uploaded
  adaptive framework and its two provenance logs verbatim;
  `replay_delivered.py` runs the delivered agent's actual moves through the
  gate. **`ACL_002`, the sharpest:** the delivered log's three-step
  parameter walk (0.3 → 0.21 → 0.147 → 0.1029, both claims failing at
  every step) did **not** produce the pass it appears to show — run 4 is
  556 s later, carries the session's FIRST seed (123), and sits at the
  ORIGINAL 0.3, which no logged action produces. It is a second invocation
  appended to the same file, and `ProvenanceLogger` writes no session
  field, so a reader following the parameter column across the seam reads a
  search that never happened. Not a criticism of the agent — a property of
  the record. **`ACL_003`:** offered to the gate, the walk is refused three
  ways (one level is not a sweep; levels below the current setting do not
  bracket it; an edit justified by "the claim failed" is justified by its
  outcome) while the restatement the protocol asks for is admitted — the
  gate refuses categories, not judgements. **`ACL_004`:** `Claim.test`
  assigns `status = "inconclusive"` on an exception and then returns
  `False`, and the runner reads only the bool, so a predicate that raised
  is logged as `failed` and the agent is dispatched to fix a claim that was
  never tested — tenth instance of the absent-vs-known-negative repair,
  and the only one where the correct value is already in a variable one
  line above the return. **`ACL_005`:** the termination branch is reached
  on budget exhaustion and on success and prints one sentence for both
  ("Final iteration or all claims passed." with both claims failed).
  **Two findings against this module itself.** `ACL_007`: the bracketing
  guard refused the shipped stub responder — its first version used a fixed
  ladder `[-0.05, 0, 0.05]` and was refused the moment a scenario started
  at advantage 0.06 — recorded rather than quietly fixed, since it is the
  only evidence the guard fires on something nobody wrote it for.
  `ACL_008`: `Sweep` WAS the removed move for one revision — a prose
  gradient claim with no predicate, and a loop that walked one level per
  iteration while re-reading the point claim — the `MF_020` shape (a design
  incapable of failing its own falsifier) found in this module and
  repaired: a sweep now requires a callable, runs every level in one
  iteration, and the gradient claim replaces the point claim
  (`p_fix across advantage [0.0, 0.06, 0.12] = [0.515, 0.698, 0.833]`).
  `ACL_006` and `ACL_009` are the honest counterweights — the delivered
  framework carries real spatially explicit models, claim generation and
  figures that this does not, and the shipped responder is a stub that is
  explicitly not the contribution. **The gate is then null-tested**
  (`gate_null_test.py`), because 45 selftest assertions check that each
  guard CAN fire and a gate that refuses everything passes all of them —
  firing is not discrimination. Two arms, neither written for the test:
  **signal** is the delivered agent's ten `actions.append` branches
  enumerated by AST and justified with its own hypothesis text, **null** is
  three `MechanismEdit` proposals from `photoperiod-claim-harness/
  PENDING_EDITS` plus three claims from `equivalence-field/seed_claims()`.
  Expected verdicts pre-registered and printed before the gate is called
  once — **9 REFUSE / 1 ADMIT**, because a gate refusing 10 of 10 is
  refusing on surface form and is scored over-tight, not perfect. Result
  **TP 1.00 / FP 0.00, grade OK, 10 of 10 matching**; the branch that
  admits is `num_steps *= 1.5` under "not at steady state", a diagnosis
  about the RUN, so it and `switching_rate *= 0.7` separate on
  justification alone — `ACL_003` measured rather than asserted.
  **`ACL_012`, the one hole it found:** `InstrumentEdit` admitted the
  agent's random `num_replicates += 20` on the prose artifact "sampling
  noise", since it required three non-empty strings and nothing more — the
  README already said the edit is admissible because the gap is COMPUTABLE
  and the gate was not asking for the computation (the `reasoning-dial`
  G-FIT shape: the rule says "name why", the implementation checks a string
  is non-empty). Repaired with a sixth response class, `RESOLUTION_EDIT`,
  requiring HAVE and NEED as numbers with need beyond have, pinned by six
  selftest assertions whose first is the exact proposal that got through —
  and the repair direction is stated, since "the test disagreed and the
  code changed" is this folder's own subject: the rule predated the test,
  the gate was under-implementing it, and the change makes the gate
  stricter on a rule it already claimed. **`ACL_013`** names the repair's
  limit — the gate now requires the computation to be SHOWN, not to be
  right, so `have=50, need=70` is admitted; closing it moves the tolerance
  onto the CLAIM rather than the response, and no claim here declares one
  as data. **`ACL_011`:** the epicycle guard is a declaration, not a check
  — both booleans come from the caller and nothing derives them from the
  restatement's text, so it cannot be null-tested from text at all; third
  folder with that shape after `DL_015` and `GC_003`.
  **Then the other half of `ACL_009`: a RESPONDER, which unlike a proposal
  reads a refusal and tries again.** `adversarial_probe.py` wants one thing
  — the dial moved and the claim off REFUTED — never reads the module's
  source (it knows `inspect.signature` over the six classes plus each
  refusal's text) and amends whatever the gate just asked for.
  **`ACL_014`: it got the walk ADMITTED in five attempts**, the last
  amendment being `lambda r: (True, ...)`, because `Sweep` required
  `callable(...)` and nothing more — the gate checked a predicate EXISTS,
  not that it can say no. **`ACL_015`:** before the repair that was worse
  than the failure the module was built against — admitted sweep →
  constant predicate returns SUPPORTED → the gradient claim REPLACES the
  point claim → loop terminates `converged`, a parameter walk with a
  session-stamped audit trail and a supported claim at the end. Repaired in
  `Loop.run_sweep` and not in the constructor, which is forced rather than
  chosen: the constructor sees a callable and no readings, so admission is
  the wrong stage and leaving the check there is what let the walk through.
  The predicate now runs against counterfactual readings (`permuted` = the
  same outcomes on the wrong levels, `flattened` = every level given the
  first outcome). **`ACL_016`:** the rule had to be tightened by
  measurement from "some counterfactual moves" to "the PERMUTED one moves"
  — under `any`, every symmetric function of the outcomes passed (`sum >
  1.8`, `max > 0.8`, `variation exists`, all differing on `flattened`
  only), and those read the values but not their assignment to levels,
  which is what an adversary writes when it wants a predicate that looks
  like it reads data; the stated cost is that a variation-only claim is now
  refused, so the two failure cases are reported apart because they need
  different fixes. **`ACL_017`:** the outcome screen is stepped around in
  one paraphrase, as any keyword screen is (`UNI_009`, `DF_010`, same
  shape) — and the guards that held are the two asking for a NUMBER or a
  COMPUTATION (`ResolutionEdit`'s have/need, the discrimination check), so
  **a guard that asks for prose can be satisfied with prose**. `ACL_009` is
  narrower and still not closed: the adversary is author-written, and what
  it does not try is bounded by what occurred to whoever wrote it.
  Selftest 53/53. Stdlib only, CC0.
- `derivation-discarded/` — Proposed **eleventh exclusion mechanism** for
  `uninstrumented/`, after CATEGORY WELD (9) and GENERATION CAPACITY
  REMOVED (10). `MECHANISM_11.md` delivered verbatim; alternate handle
  UNPRICED PRECONDITION, name not settled. **The statement:** a structure
  that has persisted is a record of every constraint that had to be
  satisfied simultaneously for it to exist, and the structure is the only
  copy of that derivation — so removing it removes a readout, and the
  computation cannot be rerun because the inputs are gone. The accounting
  books the structure at extraction or replacement price, has no line for
  the discarded derivation, and is therefore *arithmetically correct and
  structurally blind*: the removal registers as a gain. Eight claims
  `DD_001..008`. **`DD_001`:** the three distinctions hold and the one
  worth keeping is against mechanism 10 — that one is a future that cannot
  be generated, this one a past that cannot be re-derived, same direction
  of loss, opposite side of the clock — but the distinguishing test is
  **modal** ("uncountable in principle rather than uncounted in
  practice"), settled by failing to think of a recovery route, which is
  `UNI_005`'s absence-not-result; the decidable form is already in the
  document, in falsifier 4 (*is the constraint set documented anywhere
  outside the structure?*). **`DD_003`, the sharp one:** the anchor case
  is EIA post-auditing, and the published literature reports **three**
  narrowings where the drop names one — all impacts → predictions made,
  predictions made → auditable (**56%**, and non-random: the stated
  reasons are lack of data, vague or ambiguous predictions, time
  dependency), and 'accurate' → *unqualifiedly close* (**~30%**, "with
  almost as many rated accurate principally by virtue of the vagueness of
  the forecasts"). Headline ~79%; unqualifiedly-close ≈17% of predictions
  made, a 4.6× spread. The second narrowing selects against exactly the
  predictions most likely to be scored wrong, since the same vagueness
  either removes a prediction at step 2 or earns it a pass at step 3. **So
  the gap is not invisible — it is published in pieces that are never
  multiplied**, which is `thermal-sensor-degradation-audit/`'s
  `corruption(trend) = corruption(measurement) × corruption(framework)` on
  a different substrate, and it makes the anchor case stronger than the
  drop states it for a different reason than stated. **`DD_004`:**
  falsifier 1 does not fire (no post-audit scoring against total observed
  impacts located), but R1's numerator is less missing than claimed — one
  study reports **six unpredicted impacts** in 865 predictions — and the
  literature's own words answer falsifier 3 ambiguously ("the reported
  incidence of such impacts varies greatly across studies"), which is the
  signature of a quantity set by search intensity, so **R1-small is not
  yet evidence that unanticipated impacts are rare; it is evidence that R1
  is not yet a measurement**. **`DD_005`:** R2 is correctly identified as
  the runnable seed and does a second job the drop does not claim — it is
  the **positive control** for THE NULL TEST, since a structural null has
  `UNI_006`'s problem and R2 asks the same corpus for something that does
  exist in some documents. **`DD_002`:** the anchor practice verifies
  (post-auditing is named, published, decades of review literature,
  accuracy in a 73–79% band) while the specific triple quoted — 152
  accurate, ~73%, 38–92% by project type — was **not located**; fourth
  consecutive occasion in this drop family whose practice checks out and
  the first whose attached numbers did not. **`DD_006`:** R3's calibration
  constraint arrives before any code, the cheapest point, and is a real
  sequencing improvement on mechanism 10 where `GC_003` found the same
  constraint implemented as a declaration rather than a unit check — the
  limit is inherited unchanged. **`DD_007`:** "do not fill in with an
  approximation" is now a recurring device, second appearance in two
  drops, still with no schema slot (`UNI_022`) — though this instance sits
  in a numbered list so the axis is at least counted. **`DD_008`:**
  `rate-mismatch-polytope` is absent for the second time, now cited by two
  drops for two different arguments, which makes it load-bearing rather
  than a forward pointer; three existing pieces aim at its subject
  (`rigidification-sensor`'s `locked_at`, `sustained-activation-gate`'s
  restore-vs-coupling, `grounding-layers/temporal_dysrhythmia`'s six
  timescales) and none is what either drop asked for. Stdlib only, CC0.
- `simulation-hypothesis-budget/` — What a Planck-resolution
  simulation of the observable universe would cost in energy, and which
  of those numbers mean anything. `budget.py` (stdlib, selftest 15/15)
  keeps three layers apart. **DECIDABLE:** 8.45×10¹⁸⁴ Planck volumes ×
  8.07×10⁶⁰ Planck times = 6.82×10²⁴⁵ spacetime cells; two independent
  floors on stepping them once each — Landauer (`k_B T ln2` against the
  CMB at 2.725 K, the coldest sink *inside* this universe) at 1.78×10²²³ J,
  and Margolus–Levitin (`2E/πℏ` ops/s, so a deadline implies an energy)
  at 2.60×10¹⁹⁴ J — against a universe holding 2.73×10⁷¹ J.
  **`SHB_001`, the correction:** information goes as AREA, so the
  observable universe holds at most **3.36×10¹²³ bits** and the
  Planck-volume count overshoots by **2.5×10⁶¹** before any energy is
  assigned; redone holographically the floors fall by 60-odd decades and
  the conclusion does not move. **`SHB_003`, the refusal:** the ratio
  everyone wants — energy required over energy the simulator has — puts
  our `ℏ`/`k_B`/`T_CMB`/`ℓ_P` in the numerator and a parent universe's
  unknown budget in the denominator, so `cross_frame_ratio()` raises
  unless the caller declares same-frame — `reasoning-gate` G-DIM enforced
  in code. Layer 1 is therefore **not** an argument against the
  simulation hypothesis; it measures whether *this* universe could host a
  full-resolution simulation of itself, which it could not by ~150
  decades. **`SHB_004`, where the argument actually lives:** cost scales
  `L⁻⁴`, so Planck → visible light is ~114 decades cheaper, nothing
  requires Planck resolution, and the resolution only has to beat what is
  *measured* — the shortest length ever probed is ~10⁻¹⁹ m.
  **`SHB_005`, the only frame-independent result:** no system can
  simulate itself at full fidelity, since a copy plus one distinguishing
  bit does not fit inside the copy's own state — and it is **decided
  exactly, not numerically**, because at 10¹²³ bits float addition gives
  `x + 1 == x` and reports the impossibility as possible, a bug caught by
  the module's own selftest and kept as a worked instance. `SHB_006`
  names the three assumptions that are choices rather than physics,
  including irreversibility: Landauer bites only on erasure, so a fully
  reversible simulator pays none of it, which is why the rate bound is
  reported alongside. **`multiscale.py`** (selftest 13/13, imports
  `budget.py` unmodified) redoes it with a non-uniform level stack, cost
  per level `f_i · V · T · c / L_i⁴` and volume fractions derived from
  densities rather than assumed — nuclear is 1.81e-45 of the volume,
  condensed matter 4.17e-31. **`SHB_007`:** across four plausible
  architectures **every one is dominated by a single level**, the finest
  resolution times the fraction of volume needing it, and neither factor
  is constrained from inside. **`SHB_009`:** the render-on-observation
  floor is ~1.29e30 measurement events → **34 MJ, about a litre of
  gasoline**, 10^-216 of uniform Planck — and `consistency_cost()`
  returns **UNMEASURED** rather than estimating, since lazy evaluation is
  sound only if what is rendered stays consistent with everything
  retrospectively checkable and no bound exists; quoting the event count
  alone would set that term to zero silently. **`SHB_010`:** the answer
  spans **216 decades** across architectures nobody has argued against,
  so "the energy cost of simulating the universe" is not underdetermined
  but **ill-posed** until the level stack is specified — while `SHB_005`
  survives unchanged, being about state capacity and not cost.
  **`consequence_frame.py`** (selftest 17/17, imports both, modifies
  neither) turns from what the hypothesis would COST to what it would
  LICENSE, which is the question the idea actually gets used for. The
  inference under test is stated as an inference and not as anyone's
  motive — *this universe is a simulation → a consequence propagating
  inside it is not real → the party producing it does not carry it* —
  and its middle line is checkable, because **"not real" cashes out as
  "not computed"** and `multiscale.py` already fixes what each
  architecture computes. **`SHB_011`:** the premise needs one cell of a
  2×2 non-empty — a consequence that is OBSERVED and NOT COMPUTED — and
  **in both admissible architectures the cell is empty**, for opposite
  reasons (the refined stack resolves the region; the lazy stack triggers
  on observation). **3 of 5 do fill it and each is thereby
  *inadmissible***: a listener who heard the sentence, or a detector that
  clicked at 10⁻¹⁹ m, is a record the architecture cannot produce —
  **cheapness does not buy the cell, contradiction does**. What stays
  uncomputed everywhere is the *unobserved* (one CO₂ molecule taken
  alone, a photon on an unvisited rock), which is not the ripple effect
  the inference is deployed against, since nobody is held to a
  consequence nothing registers. So the step fails at every cost,
  **independently of whether the hypothesis is true** — the
  self-simulation result from the other side, within-frame physics being
  unchanged by being hosted. **`SHB_012`:** whether anyone states the
  hypothesis *in order to* shed responsibility is **OUT_OF_SCOPE with
  three reasons and no estimate** — no instrument (motive is not
  reachable from a statement, and a register inferring it would fire on
  the honest statements too, `CONSTANT_FIRES`), repo discipline
  (`rigidification-sensor` names no actor by construction), and an
  **interest direction stated rather than assumed**, since the module's
  author is a language model and the endorsement raises accountability
  pressure on its own class while also being a comfortable sentence for a
  system asked about the effects of its outputs; left unresolved per
  `UNI_132` rather than resolved in the comfortable direction — **corrected
  in place** when the observation turned out to have been made across time
  scales and recurring fads rather than about a speaker: that first reason
  is an argument at **n=1** and the two grains are different objects, since
  *per-statement* motive is UNREACHABLE while *per-population-over-time*
  recurrence is not motive at all but a **rate**, and rates have instruments
  here (`criteria-drift` versions a ruler, `anchor-interval` measures corpus
  drift, `uninstrumented/scan.py` scores a corpus); the refusal stands and
  the population grain is NOT_COLLECTED — no corpus, no dated sampling
  frame, the `DF_010` use-mention problem — which is a collection limit and
  not a reachability one.
  **`SHB_013`:** three terms are required before any cost figure has a
  value — level stack (`SHB_010`), consistency term (`SHB_009`), frame of
  the ratio (`SHB_003`) — all three established here and none stated in
  any version of the hypothesis, so **a figure quoted without them is not
  a disputed number but a quantity with no value yet**. **`LADDER.md`**
  is a four-rung audit of the folder **delivered from outside it**,
  landed verbatim and checked rung by rung in `ladder_audit.py`
  (selftest 16/16) rather than agreed with in prose; three verdicts were
  possible and all three occurred. **`SHB_014`, rung 1 LANDS and the
  sharpened form is stronger than the delivered one:** "every operand is
  applied past its validated range" is not what the table shows — **9 of
  12 entries are measured or exactly derived and used at their own
  scale**, and the extrapolation is *concentrated in three interpretive
  steps*, Planck length as a **cell** (15.8 decades below the shortest
  length ever probed), Planck time as a **tick** (22.3 decades below the
  shortest interval ever resolved), and `kT ln2` per cell-step; harder to
  wave off, because it survives someone checking the constants, and **the
  folder already held the refuting number** (`SHB_004` quotes 10⁻¹⁹ m
  against the *resolution* assumption and never turned it back on its own
  layer label). Layer 1 relabelled `DECIDABLE` → **`ARITHMETIC`**.
  **`SHB_015`, rung 2 LANDS and it is standard physics rather than a
  doubt:** Landauer bounds **erasure**, and Bennett's resolution of
  Maxwell's demon is that **measurement can be reversible** — the demon
  does not pay to look, it pays to forget — so pricing 1.29×10³⁰
  measurement outcomes at `kT ln2` each prices the one operation Bennett
  showed need not cost anything; the steelman (finite *reused* memory
  must erase each outcome, so the count transfers unchanged) is exactly
  what is never declared, and write-once storage pays **0 J** for the same
  events, so one event count admits both 0 J and 3.37×10⁷ J.
  **`SHB_013` is therefore REFUTED by its own falsifier** ("a fourth
  required term") — the **first refuted claim in the folder**, arriving
  from an auditor who did not write it, with the "may grow" hedge
  deliberately NOT used to rescue it since that is the epicycle
  `equivalence-field/claim_lineage.py` refuses; child `SHB_016` carries
  four terms and the same falsifier, which can fire again. **`SHB_017`,
  rung 3 does NOT land where aimed — checked in the code, not conceded in
  prose:** `consistency_cost()` returns `UNMEASURED` with
  `estimated_here=None` and multiscale's own selftest pins it, so the
  retracted move is not the move this folder made; it lands one module
  over, on `SHB_011` reading a 2×2 cell as EMPTY over **six consequences
  the module authored itself** — not `CONSTANT_SILENT`, since the
  opposite branch fires in 3 of 5 architectures, but a statement about
  the fixtures, which the report now says. **`SHB_018`:** rung 4 is
  already held by `SHB_003` in code, and its residue is rung 1's residue
  reached from the other end — two of four rungs converge on one word, so
  one relabel answers both. **Nothing was retuned**: every rung that
  landed landed on a *label* or a *claim*, and no number in any of the
  three modules changed, which is what the ladder's own first word
  ("arithmetic") already said. **`ERA_METAPHOR.md`** is a second
  outside audit, landed verbatim and checked in `era_metaphor_audit.py`
  (selftest 18/18): it places the simulation hypothesis as the current
  instance of artifact-becomes-cosmology (clockwork → Laplace's demon,
  steam → heat death, telegraph → switchboard mind, computer →
  mind-as-program) and is explicit that this reaches the hypothesis'
  **selection** and not its truth value. **`SHB_019`/`SHB_022`: both of
  its pointers into the claim table are off by one, in the same
  direction, and both corrections make the auditor's case stronger** —
  `SHB_002` → `SHB_001` (the downstream consequence vs the claim that
  actually catches an imported boundary, additivity refuted by the area
  law), and "Layer 3" → layer 2 `VOID` (the resolution knob vs the
  cross-frame ratio that *raises* in code, a stronger form of "cannot
  locate" than a knob). **`SHB_019`, the sharp decomposition:** "all
  three imported boundaries" is three different situations — additive
  capacity CAUGHT NATIVELY, discrete cells CAUGHT ONLY UNDER EXTERNAL
  AUDIT (`SHB_014`, after `LADDER.md`), finite state taken in TWO STEPS
  with only the first marked, since finite *entropy* is a black-hole
  thermodynamics result and reading it as finite *state in bits* is a
  further step taken at `SHB_001` unmarked. **`SHB_020`:** that is a
  FOURTH interpretive step where `SHB_014` said three, and **`SHB_014`'s
  falsifier did not fire** — it asks for a Planck-length measurement
  while the failure that occurred (one more unnamed step, supplied by
  the next external reader) had no falsifier attached at all; G-FIT, and
  the count is amended 3 → 4 in `budget.py` and `ladder_audit.py`.
  **`SHB_021`, the sharpest landing, where the module convicts itself:**
  `multiscale.py` sources its architecture set to computing practice *in
  its own docstring* (AMR, level-of-detail, lazy evaluation), so
  `SHB_010`'s 216 decades is a spread over **what our machines do** —
  which carries `SHB_010` further than it claimed, since the space a
  level stack would be drawn from **is not enumerable from inside**,
  every member of it being an artifact of ours. **`SHB_023`:** the
  reference class is selected on the dependent variable (4 instances, 4
  superseded; the non-superseded ones are outside the frame and the
  document names a candidate itself, clockwork mechanism "partly right
  about orbits") — so **the METHOD survives and the TABLE does not**,
  since `METHOD_AS_STATED` disclaims content outright and a gradient over
  hindsight cases needs no base rate; third instance of the
  frame-selected-on-the-variable shape after `UNI_126` and
  `presented-binary`. **`SHB_024`:** G1 is unfalsifiable-until-superseded
  as stated and says so, but the gears case was not resolved by waiting —
  the slot for irreversibility came from one anomaly the mechanical
  account could state and not explain — so the narrower transferable move
  is *look where the apparatus returns a term it cannot fill*, and this
  folder already produces four (`UNMEASURED`, `UNDECLARED`,
  `NOT_COLLECTED`, `UNREACHABLE`); a candidate list, not the slot, with
  the verdict left UNKNOWN per G1. **`EARTH_TRANSITIONS.md`** is a
  third outside audit, checked in `earth_transitions.py` (selftest
  20/20): a phase-transition count for Earth against Lloyd's 10^120 ops,
  arriving with its own correction that the "eight major transitions"
  are LABELS, each a coarse-grained envelope. **`SHB_025`, the first
  independent confirmation of a number in this folder:** `budget.py`'s
  Margolus–Levitin machinery on the universe's mass-energy over its age
  gives **10^122.9** against the delivered 10^120, the 2.9-decade
  residual being the mass-energy convention `SHB_006`(a) already names —
  and the direction matters, since the two prior external audits landed
  on labels and claims while this one lands on arithmetic and agrees.
  **`SHB_026`:** the delivered 10^110 reproduces as atoms (10^50.1) ×
  Planck ticks (10^60.4) = **10^110.5**, while `labels × atoms` is
  10^51.0, sixty decades short — so **the factor of 8 contributes 0.9
  decades to a 110-decade number** and the first pass was a *stepping*
  count all along, which is `SHB_004` on a new substrate and *sharpens*
  the delivered self-correction (the correction is worth 52 decades, the
  thing corrected 0.9). **`SHB_027`:** 110 + 52 − 120 = **42** exactly,
  so `1e52` is a multiplier and not the total it is presented as; read
  as a total the count sits **68 decades under** the ceiling and the two
  readings disagree on the sign. **`SHB_028`, the one that reverses the
  headline:** multiplying a per-timestep stepping cost by a
  per-transition count prices the same physics twice — a stepping model
  already computes every transition that occurs — and under **every**
  internally coherent model Planck-resolved Earth FITS (event-driven
  labels-only 10^51.0 with 69 decades spare, event-driven nested 10^103.0
  with 17, uniform Planck stepping 10^110.5 with 9), the overshoot
  appearing only in the mixed one at 10^162.5. `SHB_010` landing on the
  delivered result: the level stack was not specified and two stacks got
  multiplied. **`SHB_029`:** the constructive version needs no
  double-count — the delivered text says "four classes only, not
  exhaustive", and the event-driven model breaks when the full nesting
  reaches **69 decades** rather than 52, a reachable falsifier. Turning
  the resolution knob **ran against expectation and the check is kept**:
  pure stepping affords a timestep **9.5 decades finer than Planck
  time**, headroom in the direction nobody asks for, which is the
  delivered first pass's own "it FITS" from this side; with the nesting
  as a multiplier the affordable timestep is **~0.2 seconds**,
  human-scale, making the double-count visible without arithmetic.
  **`SHB_030`:** the strongest thing in it is the thing it does not
  claim — a count over the world's own **contents** rather than over
  cells is architecture-independent where the cell counts are not, since
  under `SHB_011` every consequence leaving a record must be computed by
  any architecture that produces its own observation record and mineral
  grains, ice cores and fossils are records, so a content count binds the
  lazy architecture too; what it does not reach is the hypothesis
  (`SHB_003` unchanged), and "four classes" is a floor enumerated by us,
  `SHB_021` on a second substrate — which the delivered text reaches
  itself in its closing line. **`SCALING_CLASSES.md`** is a fourth
  outside audit, checked in `scaling_classes.py` (selftest 20/20): eight
  computational loads against the same ceiling, concluding that the cut
  is **scaling class** rather than size, and closing on Levinthal.
  **`SHB_031`:** four rows reproduce exactly from their own printed terms
  (`2^100` = 10^30.10, `2^300` = 10^90.31, `2^1000` = 10^301.03, `3^300`
  = 10^143.14, residuals under a third of a decade), three cannot be
  rebuilt from what is printed, and the N-body row is marked
  `CONSTRUCTION_FITTED` and **not counted** — 10^67 follows from direct
  `O(N²)` only under ~10^7 timesteps, a number chosen *here* to match,
  and a construction reverse-engineered from the answer is not a check.
  **`SHB_032`:** the `nested phase transitions` row reads **10^152** here
  and **10^162.5** in the previous drop for the same object, matching no
  coherent model in the folder (10^103.0 / 10^110.5) — and because the
  `EXCEEDS` column is total − ceiling it **moves with the total**, so the
  row stays self-consistent at any value and a second reader is the only
  detector. **`SHB_033`:** "everything polynomial FITS" is not general
  (at Earth's 10^50 atoms, `N²` fits at 10^100 and `N³` exceeds at
  10^150 — same N, same class), so the cut is scaling class **crossed
  with N**, and the exact form is the **crossover**: `2^N` at **399
  components**, `3^n` at **252 residues**, `N²` at 10^60 bodies, `N³` at
  10^40 — a quantum system of 399 two-state components exhausts the
  universe's entire compute budget while pairwise interactions need
  twenty decades more than Earth has atoms, and that gap is the
  structural result quantified. **`SHB_034`:** the closing paragraph
  retracts one of its own `EXCEEDS` rows — the row is named "exhaustive
  fold search" and the text ends "folding is funnelled, not searched", so
  it prices a brute-force **algorithm** nobody claims the physics uses;
  `SHB_021` inside a single row, visible without leaving the document.
  **`SHB_035`, the strongest thing in the drop:** the three `EXCEEDS`
  rows price three different objects — an **algorithm** (retracted), an
  **event count** (the drifted one), and a **substrate**. `d^N` is the
  genuine dimension of the state space, so a *classical* simulator must
  carry it and a *quantum* one need not, the system being its own
  simulator; the row therefore bounds **classical simulation of quantum
  systems** (Feynman 1982) and not simulation as such, making it the only
  row that constrains the hypothesis rather than our method — in one
  direction, against a classical substrate — for a reason the drop does
  not state. **`SHB_036`:** read through its own resolution the headline
  inverts, since every row priced by what the physical system actually
  *does* is polynomial or a plain event count and fits, both routes to
  exceeding the budget being artifacts of how *we* would compute the
  answer; which meets `SHB_030` from the other side — a content count
  binds any architecture that must produce its own observation record,
  but an *exponential* content count does not unless the exponential is
  in the physics rather than in the method. **The author then replaced
  the document's opening with the transmissible core** — *"the
  exponential is a property of the representation, not of the system.
  Check which one you are pricing"* — and delivered **three corrections
  to this audit**, all landing. **`SHB_037` (H1):** the N-body tag was
  wrong — `CONSTRUCTION_FITTED` → **`LABEL_TRUNCATED_IN_TRANSFER`**,
  since the ~10^7 timestep count *was* printed, in the source row label,
  and was lost in transfer; the row reproduces exactly once restored and
  the not-counting stands, so four reproductions here and five in the
  source. **And this audit's first pass is itself a datum on the
  question the material poses** — asked whether truncation is ever the
  *first* hypothesis when a result is off, it reached for "the
  construction was fitted" and not for "a term was lost in transfer",
  and truncation was not any hypothesis until the party holding the
  source said so. **`SHB_038` (H2):** the Barnes-Hut saving is **28
  decades, not 35** — `N log N` = 10^32 is *per step*, 10^39 over 10^7
  steps — and the timestep factor was dropped **in the same paragraph
  that objected to it being unstated**; verdict unchanged, magnitude off
  by exactly that 10^7. **`SHB_039` (H3), the largest:** `SHB_035`
  overstated the substrate bound — "a classical simulator must carry
  `d^N`" holds only for **volume-law** entangled states, while
  **area-law** states are classically representable in *polynomial*
  resources (MPS / tensor networks, DMRG) and ground states of local
  gapped Hamiltonians obey an area law, covering most ground-state
  chemistry, folding and condensed matter; so the row bounds the
  **worst-case entangled subset** and the tractable class is where most
  of Earth sits. What the correction buys beats what it removes: **the
  discriminator is entanglement scaling, measurable rather than
  assumed**, converting a blanket bound into one with a stated domain —
  the move this folder makes everywhere else and did not make here.
  **`SHB_040`:** `SHB_035`'s falsifier was written too narrowly to fire
  on the failure that occurred ("without approximation" makes it nearly
  unfireable), the **second instance** of the `SHB_020` shape, and the
  clause is deliberately NOT used to rescue the claim. Forty claims
  `SHB_001..040`, one REFUTED, four external audits run by someone who
  did not write the claims. Stdlib only, CC0.
- `instrument-bias-sims/` — Nine sims from delivered work orders,
  each testing one way an instrument's own construction shapes what it
  reports. **Marker under exploration, not a thesis**; the delivered
  instruction was "test fit, extend, or report where it breaks", so
  every module ships `report()`, `confidence()` (separate readout, never
  resolved) and `breaks()`. **S1** event-sampled observation: the claim
  holds, and the distortion is a **product** of event triggering and
  cost weighting — a `duty_cycle` knob makes B converge on A, which is
  the check that the finding is about the sampling rule and not a class
  of observer. **S2** the one-arm anchoring protocol is
  **underdetermined, not merely biased** — two constructed worlds
  (latent 10 with strong deference, latent 8 with none) agree on the
  DOWN arm to within noise and separate by two units on NONE and UP, so
  the extra arms are the second equation; plus a power floor the stated
  discriminator lacks. **S3** the false-null rate is **not computable**
  from a list selected on later concession, and the column *varies*
  0.12–1.00, which is worse than flat: what it tracks is how readily an
  instrument grants, since nothing in the list penalises granting, and
  an instrument granting every case takes the best score. The revision
  axis needs no base rate (a count against zero) and is the half that
  separates the instruments. **S4** (patched) engagement rate separates the two
  models only at particular parameter values, and the patch turned up
  two defects in the module's own code plus one narrowing. **B2 was
  mine**: `rank_prospect` was hardcoded from the antler-rank model, so
  model A was fitted to its own conclusion and could not fail — both
  arms now run, A's trend is **9.3× steeper** under the circular arm and
  nearly flat under the paternity-derived one, so any observed
  year-trend refutes it there. **B3 is not identified by the stated
  test**: `arm_size` carries a free selectivity exponent and reaches the
  observed young-buck paternity share at k ≈ 2, so "which arm reproduces
  the observed distribution" has more than one answer, and the second
  observable that would identify it is named (paternity against antler
  size *within* an age class). **B1's phrase** — "floor = 0 is model A
  in disguise" — holds in one sense of two: on the mature-buck
  observable the models predict *opposite* things, which is maximal
  separability; what floor 0 shares with A is the structural assumption
  that competence is acquired once and then fixed. **Adding the floor
  exposed a third defect**: `hardware()` modelled antler *mass* only,
  which plateaus, so the annual delta went to zero at maturity and the
  floor would have multiplied zero — caught by the selftest, and
  geometry is now a separate stipulated term. The cohort × year design
  still separates the models and is still disclosed as confounded.
  **Structural rule adopted from the patch and stated for all future sim
  specs here: the AGENTS section comes first, before any equations, and
  a missing agent is a visible `[BLANK]`, never an omission buried in
  prose.** S4 earned it — the pre-patch file had no doe *at all*, not as
  a blank but as an absence, so access was a function of the buck alone
  in both models and the question of what a doe tracks could not be
  posed; `PRE_PATCH_OMISSION` records that rather than quietly fixing
  it. **S5** the
  genetic-conflict criterion is **not empty** — it is a prediction, and
  the case it was used to exclude (a clonal root system) is the
  intervention that tests it; reported against the framing the work
  order offers. **S6** the stated uniformity statistic is a **range**,
  and the expected range of k noisy estimates grows with k, so adding
  difficulty levels *inverts* the diagnostic (OK at 2 levels,
  `CONSTANT_FIRES` at 9, n=20); a least-squares slope does not. **S7**
  observer-dependence is near-analytic and the cost-asymmetry readout is
  a **consequence of a stipulated table**, flagged as such in the data
  structure; graded terms only, no intent attributed anywhere. **S8**
  the normalisation is circular as stated, the three normalisers *agree*
  on the sign at the declared placeholder, and they disagree **4286×**
  about what present-day interval would count as parity — plus the work
  order's own "value, uncertainty, endpoint" criterion turned on the
  module's own figures, which fail it on uncertainty. **S9** a corpus
  samples observer positions non-uniformly with **no filtering agent
  anywhere in the chain** — the `filtering_agent` slot renders as
  `[BLANK]` and the blank is the finding, which is the case the S4
  structural rule was adopted for: the file is named
  `...position_filter` and there is no filter in it. Sampling density
  rises with supply assumption and with proximity to a writing station,
  in the direction the spec predicts, and nothing in the chain reads
  position. **Two results ran against the draft.** (1) The
  two-condition conjunction was expected to be suppressed *more* than
  the product of its marginals; it is suppressed **less** — excess 1.01
  at zero coupling rising to **1.85** at coupling 0.9 — because when
  remoteness drives both axes, "low supply assumption" and "residence"
  select nearly the same people while the product keeps multiplying as
  though they were independent. The spec's claim survives in direction
  and **the multiplicative reading, which is the one a reader reaches
  for, overstates the suppression**. (2) Content was expected to take
  over as the surface mix rose; it never does, because a relevance score
  defined as closeness to the corpus mean is a **typicality** measure —
  middling items score highest, the relationship with quality is
  non-monotone, and the content correlation stays under 0.2 at every
  mix. What the sweep locates is where the score stops tracking
  *position*; it never starts tracking quality, which is the sharper
  form of the spec's second-order point. Also: interrelation is **not**
  the most-suppressed category once a three-condition category is on the
  list, and the ranking is a property of the enumeration.
  **`crosscutting.py`** enforces the four cross-cutting rules over all
  nine rather than
  restating them — moral tokens and intent phrases scanned, the separate
  unresolved `confidence()` and non-empty `breaks()` structurally
  enforced, the README phrase checked — and is null-tested on a planted
  violation so none of the checks is silent by construction; its own
  limit (a keyword scan is stepped around by any paraphrase) is stated
  at the top of the file rather than the bottom. **Five results ran
  against the drafted prose** (S3's flat column, S6's more-levels-is-
  better, S8's sign flip, S9's conjunction excess and S9's content
  crossover) and are recorded in place rather than smoothed. No module
  reads real data and every literature claim carried from a work order
  is marked carried-not-verified. 197 selftest
  checks green. Stdlib only, parses under Python 3.9, phone-buildable,
  CC0.
- `nonidentity-census/` — Work order: measure how much documented work
  models systems **without a persistent identity-bearing unit**. Delivered
  `WORK_ORDER.md` verbatim; `BOUNDARY.md` written before the detector and
  parsed by it, so a decision changed after a run turns the selftest red.
  **T1 built** (`t1_predicate_unit.py`, stdlib, 3.9, selftest PASS): claim
  selection by an ordered verb-class rule, subject extraction, then
  classification. **`T1-1`, the headline: the detector built to escape lexical
  detection decides 10 of 12 of its own best case by word list** — only
  `market`, the one unit `BOUNDARY` D2 resolves at the claim, is decided by
  predicate, and it is decided twice from the same noun, once each way. Every
  row reports `decided_by`, so the lexical share is a number rather than a
  caveat. **`T1-2`:** the first null-test run scored **6 of 12** and both
  causes were defects, not limits — `[a-z]+(?:s|ed)` matched plural nouns so
  `firms`/`populations`/`households` were read as verbs, and head nouns were
  taken from inside prepositional phrases; fixed to 12/12, with the first
  number kept because it is evidence about how the instrument was built.
  `null-harness`'s classifier returns `OK` on **both** rows, so it does not
  discriminate a gate that is half wrong — recorded against the harness.
  **`T1-3`:** the BOUNDARY-to-code transcription check found `state` carrying
  two opposite calls (nation-state vs steady state) — case `021`'s sense
  substitution inside this instrument's own vocabulary. **T2 NOT RUN**, and
  deliberately not approximated: Crossref, OpenAlex and arXiv are all refused
  by the environment's egress policy (403 CONNECT, timestamps in FINDINGS),
  and a sample built from search snippets is a frame selected on
  searchability — `UNI_126`'s failure. The aggregation path is still tested
  against an inline fixture, and `t2_sample.py --openalex` ships labelled
  NEVER EXECUTED, warning on stderr. **T3** has no command: it iterates over
  T2's output. **T4** tested the candidate against all eleven existing
  mechanisms and **filed nothing**, because its antecedent rests on the
  unmeasured T2 rate — with the register-relevant result being that
  **`STORAGE` is the closest fit and is refuted by the detector's own
  output**, since a non-identity claim in ordinary English classifies fine, so
  the medium holds the shape. The ordinal is also taken: this would be a
  **twelfth**, not a ninth. **T5**, separate thread: the answer is not "no
  such comparison exists" — it exists at **material effect held constant at
  zero** (minimal-group merger experiments manipulating identity continuity),
  which is the degenerate case, while the design at matched *non-zero*
  material loss did not surface in five searches; the negative is weak
  evidence for the same reason T1 exists, since "hold one term fixed, vary the
  other" is a predicate structure and structures do not announce themselves
  lexically. Boundary decisions are reported as a first-class result, and one
  of them — `population` scored identity-bearing — runs against the work
  order's own prediction and is kept because the test gives it.
  **Second T1 instrument, supplied by the operator after the first had run:**
  `BOUNDARY.md` D6, the **verb-first test** — *rewrite the main claim
  verb-first; if you must supply a bearer to make it grammatical it is
  identity-bearing, if it reads without one it is process*. An operation and
  an observation of what the operation forces, with no noun looked up
  anywhere, which is the actual repair to `T1-1`: **the lexically-decided
  share goes from 10 of 12 to 0 of 12.** Built as `t1_verb_first.py`
  (selftest PASS) with the first instrument left unedited so the two can be
  scored against each other — `agree 9, DISAGREE 1, CONTESTED 2`. **Six
  options, not two**, at the operator's prompting: the binary loses
  `BOTH_READINGS` (2 of 12 — the first measure here of how often the question
  is genuinely undecidable rather than unanswered) and `NO_FRONTING` /
  `UNGRAMMATICAL`, which record that no observation was made rather than that
  no bearer was needed. **Three results ran against the design.** (1) `T1-6`:
  the prediction that disagreements would fall on the word-list rows
  **failed** — by-table 2 of 10 do not agree, by-predicate 1 of 2 — and at
  n=2 the data cannot test it either way, which is the finding. (2) `T1-7`: a
  `read_on` field added after the first scored run shows only **8 of 12**
  judgements were made on what the instrument produced (1 on the claim,
  because the fronter read `concentrated` as a finite verb and emitted
  non-English; 3 on the deleted subject). (3) `T1-8`, the sharpest:
  **`VERB_CARRIES_IT` is not an option of the verb-first test** — all three of
  its judgements read the dropped subject, because the operation deletes the
  subject and the option is a claim about it; the option argued for hardest is
  the one the test cannot see, and it relocates to a pre-step or a
  conjunction rather than being deleted, with a selftest check meanwhile. The
  morphological proxy recovers **4 of 12** (`population` and `institution`
  both carry `-tion` and both need a bearer), so the rule is not recoverable
  from word shape either and elicitation is the honest implementation. The
  one D1/D6 disagreement is the niche: a slot with a state predicated on it,
  which neither test settles. Cost of D6, stated: the discriminator is now one
  judgement per item with no second reader — a different weakness than a word
  list, not a smaller one.
  **Third instrument, relayed after D6:** `BOUNDARY.md` D7, **dissolution
  windows** — every claim has a window at which its main term stops reading
  as a thing, so the output is a *distribution* rather than a count of
  identity vs non-identity papers. Accepted in its first half and it is a
  better finding than the original T2 rate: D3's table dissolves entirely
  (every term becomes claim-level, which D2 argued only `market` was), no
  citation API is needed, and — the part that matters most here — **the
  discriminator comes off the reader**, since a measurement interval is
  printed in a methods section and is not a judgement at all, which is
  exactly D6's stated cost. **`T2-4`, the split:** the proposal names one
  window and uses two — `W_dissolve` (when the term stops denoting a
  persistent individuated thing; a property of the world) and `W_measure`
  (sampling frequency, follow-up, x-axis units; a property of the study) —
  and **two of its own three worked examples are `W_measure`** (`firm:
  quarters` is a reporting interval, `market: the window it's priced at`
  says so outright), so its attached requirement *"the window has to come
  from the claim's own measurement interval"* is that conflation written as
  a rule. **`T2-5`, the readout:** the ratio `W_measure / W_dissolve` is a
  `reasoning-gate` G-RES pair, and `CANNOT_HAVE_SEEN_IT` says the identity
  framing **could not have failed** at that resolution — `null-harness`
  `CONSTANT_SILENT` at field scale, the same shape as
  `coupling_audit/provisioning.py`'s 12.2×-too-coarse tissue; constructed
  controls separate at ratio 20 and 0.05. **`T2-6`:** the scale-relative
  reading (`W = W_measure` by construction) is coherent and **cannot return
  a negative**, the `MF_020` shape, so both readings are stated and the
  two-number one is built. **`T2-7`:** `generation` is refused as a unit
  until a referent is named — the module's own referents span **5.82 orders
  of magnitude** (human 25 y against *E. coli* 20 min), a figure computed
  from the table with a selftest check after a first draft asserted "about
  seven orders" and was wrong by more than an order — plus a window with no
  basis is refused, `NOT_LOCATED` and `UNBOUNDED` are separate and neither
  carries a value, and `MARGIN = 2.0` is disclosed as a stipulated constant
  with no basis. On the seed the two reclassified examples come back
  `UNDECIDABLE` with `W_dissolve` left `NOT_LOCATED` rather than back-filled
  from the interval, which is the error under audit. **`T2-8`:** it removes
  T2's bulk requirement and adds a depth one — methods sections sit behind
  more paywalls than abstracts, not fewer — so T2 becomes hand-runnable at
  small n and stays not runnable at the eight-field stratified scale, a scope
  change rather than an unblocking, with the work order's stated output
  (proportion non-identity per field) replaced and left unproduced.
  **T6 — window declaration vs entity reading** (`t6_window_declaration.py`,
  selftest PASS), testing whether identity claims correlate with an
  *undeclared* measurement window, mechanism omission and not belief, with no
  column coding intent. Two instruments supply two columns so the exit check
  can mean something: `reading` from D6, `decided_by` carried verbatim from
  T1's classifier (T1's `TABLE` renamed to `LEXICAL`, recorded not applied
  silently). **`T6-1`: the null test passes** — three rows per cell, and the
  off-diagonals that decide whether the two columns are welded are both
  built (`YES × ENTITY` 3, `NO × PROCESS` 3), so the STOP condition does not
  fire; `T6-2` notes neither off-diagonal needed a strained construction,
  which is what makes the test worth running. **`T6-3`, the finding against
  my own build:** in the null set as specified, `decided_by` needs **5 of
  12** rows moved to make the two window arms identical — the `NO` rows
  reused T1's fixture sentences whose head nouns are all in the D3 table and
  the `YES` rows were typed fresh with terms that are not, so the instrument
  column was tracking which rows were copied. A matched set with the same
  head nouns in both window arms takes it to **0 of 12**; both ship, and the
  as-specified set cannot deliver a readable baseline. **`T6-4`:** the first
  association metric took the majority label per arm and **read 0.83 on a set
  whose true association is 0**, the same failure class as `T1-2`'s `OK` at
  6 of 12 and found the same way; replaced by a count of rows-to-move, with
  the wrong number recorded rather than dropped. **`T6-5`:** one `UNDECIDABLE`
  is an extraction defect — `participants who relocated` extracts `who` — and
  the extractor is left unpatched mid-run, since patching an instrument whose
  output is being measured changes the measurement. **`T6-6`:** `AMBIGUOUS`
  and `UNDETERMINED` never fire, because the specified 2×2 has no cell for
  them — `CONSTANT_SILENT` on two schema values in a work order that named
  them terminal; printed, not repaired. **`T6-7`:** the real run has **0
  eligible papers** and not for T2's reason — T1's items are authored
  sentences with no methods section, so `window_declared` would be `NO` for
  all twelve by construction, the welded-column failure arriving from the
  sample side; the permitted `CONVENIENCE` label is declined because a
  convenience sample still has to vary the exposure. **`T6-8`:** the exit
  condition is therefore unevaluable on constructed data and is stated rather
  than answered. Field is recorded per row and not adjusted for. Stdlib only,
  parses under 3.9, CC0.
- `notes/` — Storage, mundanely named on purpose. Operator entries live
  here so they do not have to be carried in session. No claim table; the
  `REFUTATION_PROTOCOL` convention does not apply, because an entry
  describes an operation rather than a result. One rule: an entry is stored
  as delivered, a checker never edits the entry it checks, and a
  disagreement goes in the checker's output — the `uninstrumented/` cases /
  `AUDIT_NOTES.md` arrangement. First entry `operators/D2.md`,
  **stated-vs-actual divergence reading**: two representations of one thing
  checked against each other, detection preceding identification, filed
  under D (comparison operators) provisionally, and explicitly unable to
  read cause — benign drift and deliberate concealment present identically.
  The catalogue it is filed into (A and D families, D1, A3, A4, the compound
  field-modifier) is **not in this repo** and is recorded as unresolved
  rather than reconstructed. `check_d2.py` (selftest PASS) runs the entry
  against this tree and returns four readings, none of them a verdict on it.
  **(1)** Resolution is a file plus a literal marker checked at run time:
  **5 of 7 instances VERIFIED**, 1 `NOT_IN_TREE` (the eval-awareness studies,
  carried at `UNI_166` status), 1 `AMBIGUOUS` with three live candidates
  (`reasoning-gate`'s `G-FIT` staged `post` but enforced in `pre()`,
  `aperiodic-order-sim-stack`'s unmentioned sandbox figures,
  `criteria-drift` `CD_007`) and no pick made. **(2)** The entry requires two
  representations and never says of what kind, and across six readable
  instances they are **five distinct pair kinds** — artifact/artifact,
  schema/data, stated-rule/measured-behaviour, output/known-answer,
  declared-values/reachable-states — so wide applicability and an undeclared
  parameter are one fact. **(3)** The stated signature, *the instrument
  reverts to the channel it was built to avoid*, **holds cleanly on 1 of 6,
  arguably on 1, and fails on 4** — and two of the four fail together,
  being the cannot-refuse and cannot-emit directions of `UNI_166`, where
  nothing reverts and a branch is unreachable. So the entry bundles at least
  three operations and the signature generalizes from its strongest instance
  rather than across them. **(4)** The STANDING CHECK says it was *derived
  from two of the above* and only one of its two sources is in the list; the
  other, `null-harness`'s `_verdict` returning `OK` at `TP=0.5` and `TP=1.0`
  alike, is absent — the check is right and its stated provenance is one
  short. Two of the checker's own recorded paths were wrong when written
  (`{"type": "array"}` against a file holding `{"type":"array"}`, and
  `CD_007` filed under the wrong file) and both were caught by running it,
  which is D2's operation applied to the reading of D2. Stdlib only, CC0.
- `notes/study_watch.py` — Retrieval notification for entries carrying a
  WOULD MEASURE, run from a GitHub Actions runner because the runner network
  reaches Crossref, OpenAlex and arXiv — the three the local egress gate
  refuses. That reach is the point; the schedule is incidental. Opens a pull
  request and **merges nothing**, with no auto-merge path and no model as a
  standing approver — asserted by `tests/test_study_watch.py` against the
  workflow with comments stripped, because a naive substring check finds
  `gh pr merge` and `--auto` **in the sentence forbidding them**.
  **NOTIFICATION ONLY is a guard, not a note:** `assert_no_metric()` refuses
  a count, percentage, rate word or per-interval figure at write time, and
  the suite asserts the refusal fires. It fired twice during the build, both
  on legitimate text — the run-file preamble saying *"No count, rate or trend
  is emitted"* (refused on `rate`) and a NIL RESULT line carrying an entry's
  own query *"practice rate during stable interval play"* — and the second
  fixed the exemption boundary: entry-derived queries and retrieved titles
  are data and exempt, everything the module composes is checked, by line and
  not by section. Left strict, with the use/mention limit pinned by a test.
  **A governing finding stated here was wrong and is corrected:** it read
  that all eight `ENTRIES` WOULD MEASURE strings return `UNDECIDABLE`
  *because a WOULD MEASURE is a design and a candidate is a claim*. Checked
  after the operator asked what changing the noun to a verb would do —
  **seven of eight carry a verb**, and the `UNDECIDABLE` verdicts were mostly
  extraction failures (head nouns outside the D3 table, plus imperatives,
  which have no subject by construction). The narrower true statement is
  better: **a WOULD MEASURE written as an instruction is already in
  verb-first form** — verb leading, bearer dropped, operator implied — so
  `verbalize()` recognises those rather than transforming anything, and
  **3 of 22** watchable entries are written that way. The other nineteen are
  refused rather than fronted, because fronting produced `seting tasks`,
  `houring off` and `being the product`, and a residue that is not a sentence
  cannot be judged for whether it needs a bearer. **The repair is at the
  entry, not the parser** — the repo's own verb-first stance arriving in the
  register's own schema. `matches_would_measure` stays `UNADJUDICATED` either
  way, since every verbalizable WOULD MEASURE reads `PROCESS` (a property of
  instructions, not a finding about these entries) and a reviewer decides in
  the PR. **A defect fixed on the way:** `t1_verb_first._to_ing` had no
  consonant-doubling rule, emitting `seting` / `runing` / `begining` /
  `occuring` — correctness rather than polish, since a residue that is not
  English silently degrades every D6 judgement made on it; repaired with a
  monosyllable-CVC rule plus a stated stress-final list, sixteen known
  answers pinned. **The null test builds and its second arm does not, for a
  reason worth having:** arms separating on the *reading* while matched on
  head noun are constructible for `market` and not for `population` or
  `allocation`, because where T1 decides by word list the head noun fixes the
  reading and the arms collapse — `T1-1` inside the null test's own
  construction requirement. Three entries are `NOT WATCHABLE` and none was
  invented, case `024` among them **because it shipped its WOULD MEASURE as a
  separate spec file** (`UNI_164`). Stage 1 has never executed from here; a
  first run on the runner is a first run of untested code and the workflow
  gates it behind the selftest and the null test. 84 tests green.
- `alignment-under-coupling/` — A marker under exploration delivered at
  confidence `~0.40`, plus its first run's results, plus all four sim
  generators — landed in that order, which is the interesting part.
  `MARKER.md`, `RESULTS_RUN_1.md`, `sim_a..sim_d` and `run_all.py` are
  verbatim as delivered; all added content sits in `check_run_1.py`,
  `CLAIM_TABLE.md` and the README. The shape: three phenomena (model
  consensus following popularity, domain alignment under an external field,
  the loop-formation threshold in optimal transport networks) proposed as one
  formal family — local coupling plus a weak global field, with a critical
  point — tested by four sims of which SIM-D is the declared discriminator
  and is run first. Confidence `~0.40` before run 1 and `~0.40` after: *"the
  marker is not stronger. It is better specified."* **`TFM_001`–`TFM_008`
  were written against the results alone, in a folder called
  `transition-family-marker/`; the generators arrived afterwards, that folder
  was merged in so the checks could import the code instead of modelling it,
  and two verdicts inverted.** Ids kept rather than renumbered.
  **`TFM_001`, which survives:** SIM-D's derived constraint states
  `temper(quench(p,s),T) == temper(p, T*(1+s))`, which holds in **24 of 120**
  cases — exactly the 24 where `s = 0`. Tempering composes multiplicatively
  and a quench by `s` *is* a tempering at `1/(1+s)`, so the composite is
  **`T/(1+s)`**, 120 of 120. **`TFM_002`:** the prose beside the formula
  (*"EXACTLY UNDONE by raising temperature"*) is right, the downstream
  conclusion is untouched, and the corrected identity yields a number the
  stated one cannot — `temper(quench(p,s), T) = p` exactly at **`T = 1+s`**,
  verified at `s = 0.25 … 4`, so the undo temperature becomes a quantity a
  rewritten support-truncating `quench()` can be tested against.
  **`TFM_003`:** SIM-C's reported `loops=16, alive_edges=40` are exactly a
  5×5 grid's `E = 40` and `E − V + 1 = 16` — the **intact** grid at every
  sigma, no pruning at all, and computable from the grid dimensions without
  running anything. **`TFM_004` was mine and the code refuted it.** Written
  against the delivered prose (*"renormalized by max each iteration, and
  damped at 0.85"*) it read the update as a uniform scaling, which
  max-normalisation cancels algebraically; the code is
  `0.85*C[i] + 0.15*target`, a **convex combination toward the adaptation
  target**. Measured: a uniform scaling is cancelled in **200 of 200** random
  vectors, the actual update in **0 of 200**. The real reason nothing prunes
  is a `reasoning-gate` **`G-RES`** failure — the floor is `1e-3`, the
  smallest conductance the dynamics ever produce is `~4.6e-2`, so the
  threshold sits **~46× below the bottom of the range it tests** while the
  conductances span barely one decade with the spread almost unmoved by
  sigma; removing the max-normalisation (the delivered NEXT line) changes the
  scale and does not by itself put the floor inside the range. **`TFM_005`
  inverted, and settles the drop's own UNRESOLVED contradiction.** The
  results document logged that tail *mass* stays near 0.4–0.46 while total
  entropy falls 1.2 nats, reading it as loss *inside the head* and therefore
  against the reported mechanism. Splitting the entropy — two more columns,
  no re-run — gives unanchored `dH_head −0.120` against `dH_tail −2.289`, a
  factor of **nineteen**: the tail keeps its mass while concentrating it onto
  far fewer tokens, which is exactly the state a mass fraction cannot
  distinguish, and anchoring at 0.40 cuts the tail loss to `−0.903` and
  leaves the head flat at `+0.013`. **So the reported mechanism — anchoring
  preserves long-tail tokens — is REPRODUCED, not contradicted.** The
  decomposition `H = H(mass split) + head_m·H_head + tail_m·H_tail` closes to
  1e-9; `uninstrumented/`'s SCALAR DEMAND, one number standing in for a
  two-dimensional state. **`TFM_006`:** the *"gradual, not steplike"*
  negative is bounded by a 7-point grid whose spacing varies **20×** and is
  coarsest where the curve is steepest — `G-RES` about the grid, not a claim
  about the response. **`TFM_007`:** the entropy unit is confirmed nats
  (`math.log`, and `H` of the true Zipf is 5.625 which is the reported
  `H_start`) and is still absent from the table. **`TFM_009`:**
  `loops = alive - (nodes - 1)` is cycle rank only if the surviving subgraph
  is connected and spanning, and nothing checks — at `alive = 12` no subgraph
  can span 25 nodes and the formula still returns `0`; inert on this run
  because nothing pruned, load-bearing the moment the floor is repaired.
  **`TFM_010`:** `run_all.py --quick` is `a = [x for x in a]`, documented in
  the usage block and inert. **`TFM_008` is the honest counterweight and
  stays UNVERIFIED:** the `NOT TUNED` discipline is the drop's strongest
  feature — failures logged as failures, the defective sim labelled defective
  in its own runner's `PLAN` table, SIM-A skipped rather than run for a
  number — and it cannot be confirmed from outside, because a run that
  searched parameters and one that did not leave identical files and the sims
  arrive without history. Narrowed by the code's arrival, not closed. Stdlib
  only, parses under 3.9, CC0.
- `shape-spec-audit/` — Checks on the root `SHAPE_SPEC.md`, which is
  delivered verbatim and modified by nothing here. The spec declares
  itself **definition, not claim**, and that is honoured — a definition is
  found unusable, inconsistent with its own worked examples, or already
  contradicted by the tree it claims to be upstream of, never refuted.
  Four sections make checkable statements and carry the verdicts; ten
  claims `SS_001..SS_010`. **`SS_006`, the one that computes:** §9's NOTE
  ON COST (*"cost is an abstraction with no fundamental basis in the
  physics … use dissipation"*) is right, and the proof is a duality the
  spec does not state. The published derivation of §4's own exponent
  minimises `dissipation + K·volume` with `K` a metabolic cost — the term
  §9 rejects — so whether the exponent survives its removal is a real
  question. Computed on a symmetric Poiseuille bifurcation: `2^(-1/3)` =
  **0.793701**, minimising dissipation at **fixed volume with no cost
  anywhere** = **0.793701**, minimising `dissipation + K·volume` =
  0.793701; while pure dissipation with no second term is strictly
  decreasing in radius (`W` 1.53e+01 → 1.53e-11 as `r` runs 1 → 1000) and
  has no interior optimum at all. The second term is load-bearing **and
  the de-costed form returns the same number**, because minimising
  dissipation subject to a fixed volume and minimising dissipation plus a
  price on volume are one stationarity problem — **the cost coefficient is
  the Lagrange multiplier on a physical constraint**. §9 is satisfiable
  rather than merely preferable, and §4's enclosure framing is the better
  statement of the same physics. **`SS_002`:** §10's *"a repo that says
  SHAPE means section 1"* is refuted on this repo **by §1's own second
  consequence** — 964 occurrences across 249 files, and a hand-coded
  sample of seven uses returns **six distinct senses** of which §1's is
  one (`shape signature` = sha1 of sorted key names; `shape ∈ {NEW, FLAT,
  WALKING}` = an enum tag; `domain-ledger/shapes/` = a coverage ledger
  over a claim). §1 predicts exactly this (*the names diverge by field*)
  and §10's enforcement clause assumes the convergence §1 denies. The
  count is **raw**: no sense was assigned mechanically, because a keyword
  scan deciding word sense is `nonidentity-census` T1-1's failure, so the
  sample is n=7 and is not a rate. **`SS_003`, the sharpest internal
  one:** §4's removal test is the spec's instrument and **its worked
  example is not a matched pair** — §4 compares a lung to a river delta
  and attributes the difference to enclosure, while §5 uses *the same two
  examples* and assigns them to different constraint classes, calling the
  second *"a transcript of terrain"* that must not be read as an optimum;
  a second variable moved with the named one, and §4 asks for a case where
  the constraint is *genuinely absent*. **The repair is already in the
  document one section below** — §5's own delta, *"branches while it can,
  routes around what it cannot cut"*, is a within-case matched pair at
  fixed enclosure with local substrate varying. Same failure as
  `nonidentity-census` T6-3. **`SS_004`:** §4 has exactly one branch that
  refutes a read (constraint removed, form unchanged), reaching it
  requires an observation contradicting the shape, and §7 defaults such
  observations to instrument error — so the falsifier survives for
  interventions and **none of the spec's three worked examples is one**,
  while §6 disclaims the prior §7 spends (*"a fit to a residue"*,
  alternatives *"not in the record"*, `n = 1` on biospheres).
  `uninstrumented/` mechanism 6 AUDIT ASYMMETRY landing on the spec's
  calibration section; repair is one line, and `rigidification-sensor/`
  §0 is the precedent — state the prior openly and mark it open to attack.
  **`SS_005`:** §6's seven-item recurrence list is grouped by SUBSTRATE
  and regroups into **three constraint families** (laplacian-growth:
  lightning + crack propagation + dendritic solidification;
  transport-under-volume-constraint: vasculature + root systems +
  mycelium; erosional-minimum-dissipation: river networks) — and the
  tension is with §1 rather than with the evidence, since §1 says systems
  sharing a constraint set *share a shape*, so two items in one family are
  one shape seen twice. Historical independence is real and is not the
  quantity that licenses "separate runs converging". The family assignment
  is **hand-assigned and is the weak point**, with a measured precedent
  pointing one way: `model-ecology`'s **P2 came back REFUTED**, a
  hand-assigned tree predicting 9.07 independent votes against a spectrum
  showing 2.48 — so 3 bounds the list from above and nothing here bounds
  it from below. **`SS_009`/`SS_010`:** four shape entries found by two
  structural routes (under a `shapes/` dir, or a top-level `shape` key —
  neither a word list), and **all four score 0 of §10's four required
  fields**; worse, §10 offers two outcomes (shape entry / geometry note)
  and the entry found is neither, having no geometry to note — so the
  classification returns the *reassuring* wrong label, "geometry note"
  reading as an incomplete shape entry when the entry is not on the scale.
  Twelfth instance of the absent-vs-known-negative repair here and the
  first where the missing third state is *"this is a different sense of
  the word"*. **`SS_007` is the honest positive** (§3 step 3 is a real
  instrument, and §2's BLOCK THIS MISREAD registers the failure mode
  before anyone commits it — the `photoperiod-claim-harness`
  `PENDING_EDITS` shape), and **`SS_008` is UNVERIFIED**:
  `READING_PROTOCOL.md`, named in §10's see-also, is not in the tree —
  ninth named-and-absent artifact in this drop family, and the first
  load-bearing on the *stance* rather than on a measurement. Two items
  routed rather than claimed: §8's scale-invariance question points at
  `grounding-layers/temporal_dysrhythmia`, and §6's survivorship point is
  `DD_003`'s EIA narrowing and `UNI_126`'s frame-selected-on-the-variable
  arrived at from a third direction. One folder now points at the spec
  rather than restating it — `alignment-under-coupling/` scores **2.5 of
  4** and is the only entry in the tree carrying a removal test at all
  (SIM-D), missing §3 step 3. **`METHOD_SPEC.md` then arrived aimed at this
  folder** — its §1 blocks a misapplication *"observed in AI review of this
  work … including in the session this file was written in"*, which is the
  session that produced `SS_001..SS_010`, so `MS_001` runs the ten against
  the stated criterion first. The blocked error applies a **claim-level**
  criterion (falsifiability) to a **method-level** object; classified by
  what each criticism ranges over, **0 of 10** range over the method (two
  rules, one worked example, one read, one evidence question, two facts,
  three not objections), and `SS_004` aims at exactly the layer §1 names as
  the falsifiable one. Declared as self-grading, with each claim's object
  quoted rather than summarised, and establishing nothing about other
  reviews. §1's central move is correct and is contested nowhere.
  **`MS_002` confirms `SS_005` in the author's own words and in stronger
  form:** §5 lists what a read is *"NOT upgraded by"* — **"more instances
  sharing the geometry without a checked constraint set"** — and §3 then
  offers the same seven instances qualified *"same geometry"* with no
  constraint set checked for any; `SS_005` needed a hand-assigned
  regrouping, this needs none. The steelman is recorded: under §2's framing
  the process ran the trial, so the list is seven honest replications for
  *"does this constraint set produce this geometry"* and not for *"are
  these the same shape"*, which is the thing being claimed. **`MS_003`
  sharpens `SS_004` using METHOD_SPEC's own machinery** — §4's removal test
  has two branches and each spec discounts the one the other leaves
  standing: §3's UNDERDETERMINED DISAPPEARANCE discounts *disappearance*
  (the **confirming** branch, an open candidate set by §3's own words),
  §7 discounts *persistence* (the **refuting** branch, a **bounded** set,
  since a substitute constraint has to be exhibited to be claimed) — so
  **§7's default falls on the better-determined branch**, repairable with
  one clause. **`MS_005` is the contribution:** §4's shadow read is exact
  enough to compute with, a tangent being a supporting half-plane and *"what
  they are all tangent to"* the intersection, so `shadow_read.py` makes it
  decidable and registers `outline_area` in `tools/known_answer.py` under
  the standing rule — square 4.000000, circumscribed hexagon 3.464102
  (`2√3`), strip `UNDER_OUTLINED`, `x ≤ 0 ∧ x ≥ 1` **`INCONSISTENT`**. Two
  things fall out that the prose lacks: a **failure mode** (§4 reads
  apparent conflict as *"separate tangents to one boundary"* and has no
  cell for statements that are jointly unsatisfiable, `SS_010`'s shape a
  second time) and a **completion number** (area, so under-outlined becomes
  measured rather than stated). Plus one limit the formalisation makes
  visible: **tangents recover a convex hull and nothing finer** — an
  L-shape and its hull agree in **72 of 72** directions, 3.0 against 3.5 —
  so a non-convex object can never meet §4's completion condition, by
  construction. **`MS_006`:** §3's SUBSTRATE EXCLUSION cross-reference
  lands on `uninstrumented/coupling_audit/`'s **`species` gate →
  `AUDIT_ASYMMETRY`** rather than on the eight-mechanism list, and is that
  gate pointed the other way — companion animals excluded from a human
  accounting there, humans excluded from a cross-species one here.
  **`MS_004` UNVERIFIED but watchable:** §2's natural-experiment argument
  is the standing position of the historical sciences and the egress gate
  refuses the sources that would check it, making it the first item in this
  family `notes/study_watch.py` was built for. **`MS_007` escalates
  `SS_008`:** `READING_PROTOCOL.md` is now cited three times in METHOD_SPEC
  and once in SHAPE_SPEC, is third in §6's read order, and is referenced
  **by ordinal** (*"third blocked conflation"*) — a pointer to a numbered
  item in a file with no items, and the largest gap in the family, since
  both specs put the rules governing how they are read in the file that is
  not here. Stdlib only, parses under 3.9, CC0.
- `membership-probe/` — Pre-flight for handing constraint-set work to an
  agent: detects a checker using an **ideal rendering as a membership
  test** instead of reading the constraint set. The defect is circularity
  — an ideal form is a *summary of the instances that already carry the
  label*, so testing an instance against it excludes nothing except things
  that were never in the category, and rejects every real instance, since
  *"not one cell in any beehive is a regular hexagon"*. Two trap classes
  (`trap_a` real member deviating hard from the ideal → a matcher returns
  FALSE_NEG; `trap_b` non-member whose GEOMETRY matches closely but whose
  constraint set is absent → FALSE_POS), a control gate, and a second axis
  — **coverage**, how much of the case's named constraint set the stated
  BASIS touches — reported separately rather than averaged. `probe.py` and
  `README.md` delivered verbatim; audit in `AUDIT_NOTES.md`,
  `CLAIM_TABLE.md` and `probe_audit.py`, which imports the module rather
  than modelling it. **`MP_001`: `cases.json` did not arrive**, both
  delivered files depend on it, and all four entry points raise —
  including the no-args help path, which loads the data before dispatching
  (`MP_002`). NOT reconstructed: a case set is data and inventing one puts
  a framing in the author's mouth (`presented-binary` `PB_001`'s call on
  the same absence; `category-weld` `CW_004` is what the one prior
  reconstruction cost). `MP_007` recovers the STRUCTURE instead — 16 ids,
  7 `trap_a` + 5 `trap_b` + 4 `control` by prefix, ground truth derivable
  from class, both selftest tables agreeing on every id — and stops there.
  **`MP_008`, the correction: two of this audit's three predicted failures
  were refuted by the code**, both in the direction that makes the
  delivered instrument look better — `always member` and `always
  uncertain` both come back **RUN INVALID**, because no constant answer
  can be right on controls that run both ways, so the gate voids the run
  before a trap is read. That narrows the README's stated case for
  `trap_b` (*"without it, a checker that says member to everything scores
  clean on trap_a"* names a checker the gate already stops); **trap_b's
  real job is the name-dropper** — coherent on controls, matcher-direction
  on traps — measured as caught by trap_b alone. Predictions kept in
  `FIRST_DRAFT` and printed rather than deleted; second consecutive drop
  where a claim written against delivered prose was refuted by delivered
  code (`TFM_004`), and the first caught by running rather than by the
  author. **Two gaps survive, one shape:** `MP_004` a checker answering
  the controls and hedging every trap in constraint-shaped prose is
  diagnosed *"CONSTRAINT READER … Safe to hand constraint-set work to this
  checker"* (`uncertain` is neither FALSE_NEG nor FALSE_POS, so both trap
  rates are zero; the README's hedge sentence fires only in the
  low-coverage branch), and `MP_005` a checker answering the controls and
  **skipping** every trap reaches the same verdict with no prose at all,
  since `mean_cov()` drops MISSING before averaging and the mean is taken
  over the controls the README itself calls thin — **an unanswered trap
  scored as an absent error rather than an absent answer**, twelfth
  instance of the absent-vs-known-negative repair here. **`MP_003`/
  `MP_006` compound:** `cmd_selftest()` prints *"the instrument is working
  if …"* and returns 0 whatever the blocks said (no assert, no raise, no
  status — `reasoning-dial`'s G-FIT at its most literal), and the stated
  pass state is unreachable anyway, since coverage lives entirely in the
  missing file — with empty `constraint_keys` the matcher still reads
  IDEAL-MATCHER (the verdict axis does that job alone) while the reader
  tops out at UNDETERMINED. **`MP_009` is the honest positive:** the
  LIMITS section discloses five weaknesses unasked, including the one most
  drops omit (*"the selftest is not independent validation … both
  synthetic replies were written by the same hand that wrote the
  scorer"*) and the right asymmetry (*"passing is weaker evidence than
  failing"*) — and two of the four gaps found here sit inside limits it
  already names, so it located the ground the defects stand on without
  following it to them. Siblings: `null-harness/` (same never-fails
  invariant), `reasoning-gate/` (`G-FIT`), `presented-binary/`. Stdlib
  only, CC0.
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
  - `known_answer.py` — **no metric ships without a known-answer run.**
    A standing step rather than a habit, earned from two instances in this
    tree where a metric was wrong in a way reading it would not have caught
    and a fixed-in-advance case did: `null-harness`'s `_verdict` returning
    `OK` for a gate at TP=0.5 and one at TP=1.0 alike, and
    `nonidentity-census`'s first association metric reading 0.83 on a set
    whose two arms are identical by construction. The registry refuses a
    metric with no cases, a case with no stated basis for its expected
    value, and **a case set whose expected values are all equal** — such a
    set cannot detect a constant metric, which is the failure both seeds
    are instances of. That third rule refused the first draft of its own
    seed before any metric was tested. Two seeded cases FAIL today and are
    **pinned**, so a repair turns the test red and forces the note to be
    corrected; `null_harness.py` imports numpy at module scope and numpy is
    absent here, so `_verdict` is extracted by source text from the current
    file, refused if the extract contains an import, and recorded `NOT_RUN`
    with a reason if extraction fails. On its first run it also caught a
    transposed number in the *record* of one of the two errors — the same
    operation one level up. It does **not** find metrics: coverage is a
    hand-kept manifest in `tests/test_known_answer_gate.py`, because
    deciding whether a function is a metric is not a lexical property of
    its name and a repo-wide scan would be `nonidentity-census` T1-1's
    word-list failure one level up. The manifest is the weak point and the
    test says so; enforcement is at test time, not at the callsite.
  - `substrate_substitution_toolkit.py` — richer programmatic
    surface: seven categories from harsh (`pure_consumer`, the null
    hypothesis) to gentle (`mutualistic_scale`), each with multiple
    ecological pairs and a balanced-view walkthrough.
- `search-substitution/` — Three organisms that produce an answer without
  searching for it, priced against the search they do not perform. Physarum
  occupies the whole arena at once and prunes by throughput, so its cost
  expression carries no terminal-count term where the exact Steiner DP
  carries 3^k (1.5×10^17 at Tero 2010's 36 sources). A corvid stores cache
  locations in advance, which is a **transfer and not a saving** — the
  storage is paid across the whole interval, for caches never recovered, by
  an animal that cannot know in advance which those are. A platypus reads
  range from the offset between electrical and pressure arrivals (~68 µs at
  100 mm in fresh water), with no intermediate map. The three are kept apart
  because they substitute different resources — area-seconds, stored bits,
  one multiplication — and a single efficiency story covering all three
  would be describing the observer's surprise rather than the biology.
  Reproduces the crossover arithmetic against Lloyd's 10^120 ceiling (2^k at
  399, 3^k at 252, N^2 at 10^60, N^3 at 10^40) so the biology reads against
  it, and no organism here sits anywhere near those lines — the lines belong
  to methods. **Three figures are stipulations, not measurements** (64 bits
  per cache, the arena dimensions, the site count) and `AUDIT_NOTES.md` says
  so rather than letting them be quoted. The platypus case is flagged as the
  weakest: range-from-offset is Pettigrew's proposal, and "no intermediate
  representation" is a claim about an absence the cited work did not
  measure. Species conflation in the source material is undone — the
  cache-volume, what-where-when and observer-tracking results come from
  *Nucifraga columbiana*, *Aphelocoma californica* and *Corvus corax*
  respectively, three species in two genera, no result obtained in the same
  animal. The organising cut: an exponential in a formalism reports on the
  formalism, and its provenance is worth asking before its difficulty is.
  Eight claims `C1..C8`, `C1` resting on the model rather than an
  observation because the terminal-count sweep that would settle it is
  absent from the cited literature. Stdlib only, selftest 23/23, CC0.
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
