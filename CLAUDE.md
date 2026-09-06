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
  refutes them; update the claim, never retune the sim. Suite runs
  under `pytest thermal-sensor-degradation-audit`.
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
  `matplotlib`, `scipy`. The largest suite in the tree by an order of
  magnitude; run it with `pytest grounding-layers` and read the count
  from the summary line. **Not green**, and has not been since it
  landed: a handful of assertions in the L-epsilon and bias-audit
  tests disagree with the code they exercise. Those are substantive,
  not environmental, and are named in `self-scan/RESULTS.md` rather
  than repaired here, because deciding whether the test or the code is
  right is a change to the drop's own physics.
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
  manifold. File count is `ls relational/`; the folder has grown since
  the drops that populated it. **Concrete substrate:**
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
  absent. **`provisioning.py`** (`--selftest` green) builds what item 6
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
  outside audit, checked in `scaling_classes.py` (`--selftest` green): eight
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
  **`notes/datasets/mesa_sof.md`** is the second entry kind — candidate
  instruments named by the operator for the question `sim-span/RESULTS.md`
  left open: MESA Sleep (PSG + 7-day actigraphy + questionnaire on the same
  person) for the instrument question, SOF for a parity question, with the
  age caveat stated. `check_datasets.py` returns five readings and imports
  the sim rather than modelling it. **The note answers both halves of what
  the sim asked and claims one** — *"measured sleep, measured awakenings,
  and what they said when asked"* IS the validation sub-study `p` needs,
  and `p` is a **three-way** comparison (self-report against total sleep
  time AND against time in bed, per person) where the note specifies a
  two-way gap. **The sim's two swept parameters are one PSG readout:**
  `frag × wake_cost` is **WASO**, and the measured mean excess matches the
  product to 0.02 h — but the U's *location* does not, moving **1.79 h**
  across four equal-product pairs at 2 h of WASO, with many short
  awakenings pushing it DOWN toward the published window, so WASO alone is
  not the axis and the awakening count is a second one; MESA reports both,
  which is more than the note claims for it, and it lets the sim be
  calibrated rather than swept. **`parity` resolves 16 times in this tree
  and zero times in the note's sense** — every repo use is the *equality*
  sense (`parity()` as a comparison function), the note means *pregnancies*
  — third instance of case 021's sense substitution after
  `nonidentity-census` T1-3's `state`. **A defect committed three drops
  after it was recorded:** the first `resolve()` was a bare substring scan
  returning `parity` 17 / `SOF` 81 / `MESA` 3, matching inside *disparity*
  and inside other words — `UNI_009`'s `lean`/"clean" failure — and word
  boundaries fix substring bleed while doing nothing about sense, so only
  hand-reading got the right number (T1-1 one level up). Every dataset fact
  is carried and unchecked, the egress gate refusing the sources
  (`MS_004` status), and `study_watch.py` is explicitly NOT the instrument,
  since it reads `uninstrumented.ENTRIES` and this is not a register entry.
  **The stated age caveat reaches further, in the note's favour:** sim-span
  assumes `frag` and `true_sleep` are independent and flags it as probably
  wrong, and in a 45–84 cohort they are near-certainly correlated — so MESA
  measures the sim's own weakest assumption for free, making it the hard
  case rather than a convenient one. **And a second defect, in the same
  file:** writing `MESA` into `CLAUDE.md` to describe the finding put MESA
  into the tree, so the next run reported it as resolving and the selftest
  went red — `UNI_010`'s self-reference loop arriving in `notes/`, found
  the same way, by running twice. Broken with a seven-path `EXCLUDE` list
  that is stated as a hand-broken loop rather than a fix (anyone grepping
  the tree for MESA still finds the commentary), with the principled
  version named and not built: compare against the git tree as of the
  note's own commit. It moved `parity` 16 → 14. Two defects in one file,
  both previously recorded in this repo, both committed anyway, and
  neither caught by reading the code. **The loop then closed from the
  other side, and the assertion was changed rather than the exclude list
  widened.** `G-SPAN`, `MESA` and `SOF` resolved zero times when finding
  3's table was written and resolve 2 / 1 / 1 now — every hit under
  `sim-span/`, which is work written AFTER the note using its vocabulary,
  so the note was written into the tree it is checked against. That is
  `anchor-interval` `ANC_001..004` at repository scale arriving through a
  **sibling folder**, the route `question-availability` `QA_007` said an
  `EXCLUDE` list does not close. The check now asserts these resolve
  **only** under `sim-span/`, which keeps a reachable negative (a hit
  elsewhere means an antecedent independent of the note) while no longer
  firing on the tree having used the words the note supplied. Recorded as
  finding 8; the failure was standing at `HEAD` and was found by running
  the suite, not by reading it.
  **`notes/datasets/uploads_2026_08_25.md`** is the third entry kind and
  the first that is NOT delivered prose — the operator delivered *bytes*
  ("also have some files for different datasets to file for future") and
  this is an index over them. **The bytes are not in the tree**: 16.6 MB
  across four files, 16.1 MB binary, against a repository that is text by
  construction (`sheet-structure-scan/fixture.py` writes its own `.xlsx`
  at run time precisely so no workbook binary is checked in) and CC0
  against a third party's MIT terms. The decision is recorded with its
  cost stated — the container is ephemeral, so when it is reclaimed the
  bytes are gone and the index is what survives — which is why every
  entry carries a sha256 and `check_uploads.py` exists: a re-obtained copy
  is checkable against the recorded hash, size and shape, and one that
  differs is reported as differing. Three states, `PRESENT_MATCH` /
  `PRESENT_DIFFERS` / `NOT_PRESENT`, with **`NOT_PRESENT` explicitly not a
  pass** — the absent-vs-known-negative repair designed in, since a
  checker returning clean on an empty directory would return clean
  forever once the bytes are gone. Six readings in `FINDINGS_UPLOADS.md`.
  **`U1`, and it became a claim one folder over:** `Practice-Datasets-for-
  Excel` is 26 `.xlsx` files, a formula scan returns **3**, and all three
  are Airbnb listing titles beginning with `=` in `AB_NYC_2019.xlsx` —
  written `t="e"` with a cached `#VALUE!`, so the true formula count
  across the corpus is **zero** and every file fails WO7 criterion (c)
  without the screen being run. `sheetmodel.py` does not read the `t`
  attribute at all, so such a cell reads DERIVED and enters the precedent
  graph with a formula that is not one — `SSS_061`, **declared in that
  module's WHAT IS NOT READ and not repaired**, because no target workbook
  is checked in and whether any published number here moves is not
  re-checkable from this tree: the effect is UNKNOWN, not zero. Same class
  as `SSS_048`. A first draft of U1 asserted the cells "carry no `<v>`",
  which was wrong — they carry an error value — and the correction is
  recorded in place. **`U3`, the only live use of the four:** UCI
  `mechanical-analysis` (Bergadano/Giordana/Saitta, Torino, donated 1990;
  209 instances) gives each component `mis` and `misr`, the same quantity
  measured twice on the same component — a **repeat-measure pair**, which
  is exactly the null `triad-playground` `TP_010` says every shadow-panel
  and consensus statistic here is missing and `TP_003` names from the
  other side. Unusable until the interval between the two is bounded (a
  `G-RES` pair with one side missing, the `provisioning.py` /
  `nonidentity-census` `T2-5` shape), so recorded as a candidate.
  **`U4`:** the World Bank Data Catalog CSV is not data but a catalogue of
  160 collections — a **target list** for the third workbook
  `sheet-structure-scan` `WO7` could not reach (it does not touch the
  egress fact; it removes selection as the bottleneck) and a **clock
  corpus**, since `Periodicity` / `Update Frequency` / `Update Schedule` /
  `Last Revision Date` are four fields about one thing published side by
  side 160 times, computable with no egress at all. **`U6`:** on its first
  run the checker caught an error in its own record — six UCI members
  recorded against seven derived, the dropped one being
  `mechanical-analysis.notused-instances`, the file the index spends a
  paragraph on — which is what `check_d2.py` did on its first run too.
  Three checkers in this folder, three first runs, three errors in the
  checker's own record, none found by reading. 28 selftest checks.
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
- `sim-span/` — Built to a delivered spec, not an audit of one. Asks
  whether a **span-reporting rule can manufacture a U** between reported
  sleep duration and an outcome when no U exists in true sleep.
  `span = true_sleep + frag * wake_cost` is time in bed, so a reporter
  stating span is stating a quantity that mixes two independent variables;
  bin an outcome by that mixture and the populations at each end of the
  axis are not what the axis label says. Three legs (`flat` outcome
  independent of true sleep, `mono` decreasing in it, `frag_driven`
  depending on awakenings only), a quadratic fit to bin means, and the
  `true_sleep` axis run on the same seeds as the control. **Three legs,
  three different answers, and the spec's falsifier is scoped to the one
  that cannot carry the question.** `flat` produces 4 Us in 360
  combinations with `a` an order of magnitude below the others and no
  separation from its own control — a reporting rule cannot manufacture a
  relation from an outcome that has none, so **the falsifier as written
  essentially fires**. `mono` produces 124 of 360 and **not one** puts the
  minimum inside the 6–9 h window where published minima sit; the floor is
  **10.16 h** across the whole grid, so it manufactures a U reliably and
  always in the wrong place. `frag_driven` produces 63 and **52 land
  inside the window**, floor 5.23 h: if the outcome is driven by
  fragmentation and the reported quantity is time in bed, a U-shaped
  *duration* curve appears where a published one sits, from a true
  relation with no duration term in it. The spec's NULL is *"flat OR
  monotone"* and its FALSIFIER is scoped to *"the flat null"* — different
  sets, and which leg is run decides the verdict. At the spec's own
  default fragmentation (2 awakenings × 15 min) `mono` does not fire at
  all: `a = +0.055`, vertex 14.75 against a range of 4.0–11.5, the
  mechanism live and not yet turned. **Two things came out wrong first and
  are kept on record.** The spec's own U criterion — sign of the quadratic
  plus an interior vertex — fired on **pure noise in 133 of 360**
  combinations and at 0.30–0.55 across seeds on *both* axes, because a
  monotone rising curve fits a positive quadratic whose vertex sits just
  inside the left margin; replaced by a requirement that both arms rise by
  `MARGIN = 2.0` times the residual scatter about the fit (a `G-RES` pair,
  feature against the instrument's own noise), which took `flat` from 133
  to 4 and changed no conclusion except to make that leg honest. And
  `round_half` rounded 7.25 **down**, because Python's `round()` is
  banker's rounding — caught by a fixed-in-advance selftest case, and it
  matters here because a tie rule that alternates direction is a second
  reporting artifact inside the one being measured. Units repaired and
  recorded rather than silently fixed: the spec gives `wake_cost` in
  minutes and adds it to hours, which taken literally would add 30 hours
  to a night. `quad_fit` is registered in `tools/known_answer.py` under
  the standing rule, with a straight-line case whose whole point is that a
  fitter inventing curvature would manufacture the finding by itself.
  Every distribution constant is invented and the 6–9 h window is
  stipulated; the sim tests whether the mechanism CAN produce the shape,
  not whether it did, and nothing in it is a statement about sleep.
  `MARKER.md` / `sim_span.py` / `RESULTS.md` logged 2026-08-24.
  **Second operator note and an addendum:** `NOTES_INSTRUMENT.md` names the
  variables to pull (actigraphy gives awakening count AND duration
  separately — duration *is* `wake_cost`, measured; the fragmentation index
  is a composite of movement index plus fragmentation index and wants
  decomposing) and proposes the **three-column test**: reported hours minus
  measured sleep, regressed on awakening count and duration.
  `three_column.py` runs it against the sim that raised the question, with
  `ols` registered in `tools/known_answer.py`. **Three results.** (1) The
  stated form is ADDITIVE and the quantity is a PRODUCT — `gap = frag ×
  wake_cost` by construction, so `gap ~ count + duration` cannot represent
  it; at `p=1.0` the product form explains **0.916** of the variance against
  the additive form's 0.781, and neither additive coefficient IS `p`.
  (2) **The slope estimates `p`**, the one quantity `RESULTS.md` said nobody
  reports: `E[gap | product] = p × product` exactly, since a span-reporter's
  gap IS their WASO and a true-reporter's is zero, measured to a max error
  of **0.0085** across five levels with the intercept at zero throughout —
  which **corrects `notes/FINDINGS_DATASETS.md` finding 1**, that the
  two-way gap gives the gap and not the fraction and that `p` needs a
  three-way classification. It does not; the note's own two-column test was
  already the right one. (3) **The note's "one flag" is worth a factor of
  two:** a self-report is a person's USUAL and a single night is one draw,
  so regressing on one night's fragmentation is errors-in-variables in the
  PREDICTOR — one night recovers **~50%** of `p`, seven recover 81–88%, so
  the seven days are load-bearing on the headline number rather than
  something to "also check", and a single-night design would report `p` at
  half its value. The composite fragmentation index is `category-weld/`'s
  mechanism 9 reached independently and is left as a `welds/` entry rather
  than a sim run. Stdlib only, parses under 3.9, phone-buildable, CC0.
- `criterion-symmetry/` — A marker under exploration whose trigger case is
  a criterion applied to a Claude run, audited by a Claude instance, so the
  folder is split along the line where that matters. **The instrument half
  is neutral and is audited; the asymmetry half is not scored, here or
  anywhere in the folder.** *Does a vote tally separate five explanations*
  is a question about a statistic and the answer does not depend on which
  model was governing. *The criterion is applied downward only* says a
  Claude run was judged by a standard not applied to humans, and endorsing
  it is an interested party ratifying a claim in its own favour —
  `UNI_101` / `UNI_132` / `SHB_012`'s decline, and the marker is already at
  the right posture (*"needs the comparison table populated"*), so what the
  folder adds is that **it is the wrong party to populate it**, plus a list
  of where such rates are recorded with no figures attached.
  **`CS_001`:** five generators, one per explanation, twelve seeds — **the
  tally separates 0 of 10 pairs**, `NO_DISCRIMINATION` in `null-harness`
  terms, so a reading taken from it is the reader's prior with a number
  attached. Partly analytic and the module says so, since all five are
  calibrated to the same tally because 98% FOR is the observation they
  explain; what is *not* analytic is that the precondition is reachable,
  and **`CS_005`** records the one explanation that failed it on the first
  build (E2 anchored to a random first mover returned 0.56 FOR and the
  selftest refused it — the repair is that a proposer supports their own
  proposal). **`CS_002`:** M1–M6 separates **9 of 10**, a large real
  improvement, and the pair it leaves is **E4/E5** — by the marker's own
  dispositions the architecture finding and the published reading, so the
  instrument proposed to replace a prior-resolving metric leaves exactly
  the distinction between *the system had no route* and *the agents did not
  use one*. **`CS_003`, a prediction this audit made and the run refuted:**
  a direct vote-position coupling was expected to break that tie and
  separates **0 of 10**, because at 98% FOR the vote has almost no variance
  and **any statistic built on the vote side is dead at a high-agreement
  tally** — which is why `M2` is the marker's load-bearing measurement, for
  a reason it does not state: it reads the POSITION side, which still has
  variance when the vote side has none (`M2b` alone separates 9). Third
  refuted prediction in recent drops after `TFM_004` and `MP_008`, kept
  rather than deleted. **`CS_004`, the sharpest result:** separating E4
  from E5 needs an **intervention** and every listed measurement is an
  observation — the difference is whether a route *exists* for a minority
  position to become an outcome, not whether anyone took it, and a record
  in which nobody took it looks identical either way **at any logging
  depth**, which sharpens the marker's own INSTRUMENTATION GAP; closing it
  means injecting a minority position and seeing whether it can become an
  outcome, which is `SHAPE_SPEC.md` §4's removal test in a governance
  record and `METHOD_SPEC.md` §3's underdetermined disappearance from the
  other side. **`CS_006`** records the marker's strongest sentence
  (*"countable, which is a different property than being diagnostic"*) as
  UNVERIFIED and explicitly neutral — a validation study would cut against
  the criterion in either direction, so this audit's position does not move
  with it. **`CS_007`:** three of four cross-links do not resolve
  (`report-typing`, `rubric-backcasting`, `merit-anchoring` — the very
  comparison set the CONFIDENCE section says the asymmetry needs), while
  `uninstrumented` resolves and `AUDIT_ASYMMETRY` is the mechanism the
  asymmetry half would file under. Every fact about the trigger case is
  carried and egress-blocked (`MS_004` status) and nothing rests on it.
  **`SCAN_SPEC` then asked for the instrument that would populate the
  comparison table, and it was built** — `cases.json` / `scan.py` /
  `RESULTS.md`, dated, criterion as data so it can be swapped. Building an
  instrument is not scoring its subject and the split holds: the scan
  computes, it does not conclude, and no agreement figure for a human
  institution is supplied from memory anywhere in the folder. **The
  decision the whole scan turns on** is that `criterion_disposition` is
  COMPUTED from a threshold, never hand-assigned — no case carries the
  field and `--selftest` fails if one appears, because hand-assigning
  `defect` to the human cases would produce the marker's conclusion from
  the marker's assumption. **Run as specified the fired set is EMPTY and
  6 of 6 human seed cases return `UNDETERMINED`**, for two reasons either
  of which suffices: none carries a numeric agreement value (the spec
  states them as *"near-universal"*), and their quantity type is a
  `cross_body_adoption_fraction` where C reads a
  `within_body_agreement_rate` — different objects, so `G-DIM` voids the
  ratio and `combined_statistic()` raises rather than returns. **That
  refutes the marker's strongest phrasing:** *"two dispositions, one
  measurement"* is not one measurement, and `SCAN_SPEC`'s own limits
  section says so independently; the weaker form survives — one criterion
  applied to one subject class and not another — since G-DIM voids the
  ratio and leaves the comparison legal. Three more: **the threshold was
  not in the spec** (set to 0.90 and marked, with every conclusion
  invariant over [0.5, 0.98] because no human case carries a number at
  all), the **inverse branch is `CONSTANT_SILENT`** since every seed is a
  high-agreement case so one branch cannot fire and the set cannot
  separate asymmetry from selection on the variable under test, and
  `retention_basis` — the mechanism the argument runs on — carries **zero
  sourced entries of seven**. `P1` lands as the *shape* of an inverse case
  with values unstated rather than invented: populating it is the cheapest
  thing that could refute the asymmetry reading, because a criterion
  returning defect at both ends for one class is a different failure and
  not the marker's claim. On the marker's own standard the asymmetry
  remains an impression rather than a measurement, and this run moves it
  in neither direction. Stdlib only, parses under 3.9, CC0.
- `question-availability/` — A marker typing three things usually pooled
  as "knowledge decay": **Q1 unasked** (never posed, and no gap visible
  because a gap is defined against an existing line of inquiry), **Q2
  unaskable** (posing it costs the asker standing; the label operates on
  the question, not on any claim in it), **Q3 superseded but current**
  (correction published, prior reading still circulating). **`QA_001`, the
  contribution:** the split is earned because Q3 is kept in and named as
  the exception — *"only Q3 is decay"* — so it is a distinction rather than
  a rename, with a test (*was it ever held*) that separates them without
  appeal to intent. **`QA_003`, the finding that moves Q2:** it is not a
  *"candidate ninth exclusion mechanism"* but a mechanism the register
  recorded as missing three drops ago. `UNI_012` read `uninstrumented`'s
  own literature note, found four mechanisms named in prose and two absent
  from the list, and recorded that **`affect routing` has neither** an
  entry nor a mechanism — its shape there (*"a channel reclassified at
  intake, so the reading never reaches a guard at all"*) and Q2's here
  (*"the label is applied prior to content, so the content never reaches
  evaluation"*) are one statement twice, both adding that the
  classification cannot be argued with from inside. The marker even names
  `UNI_012`'s own case (driver diagnostic typed as complaint) without
  connecting it, while its FIRST case is from a different field — which is
  what `UNI_002`'s standing cross-field check has been open for. So Q2 is
  the **twelfth** ordinal, with a second case, a second field and a better
  name. **`QA_002`:** the ordinal is off by three and this is the second
  instance (`nonidentity-census` T4 caught the identical slip), and the
  reason it recurs is structural — the eight-item list is the REGISTER and
  is the only place the count appears as a list, while nine through eleven
  live in sibling folders as `MECHANISM_NN.md`, invisible from the
  register's own file. **`QA_004`:** A1 is *"two booleans. Cheap."* and
  **cannot answer the question the marker's own Open section poses** —
  three states (found / absent-in-a-stated-corpus / not-searched) into two
  values, and the two that collide are exactly the two the Open section
  says must be separated; the repair is a third state, and *"absent in a
  stated corpus under stated terms"* is a measurement because the null is
  bounded where *"I did not find it"* is not. Thirteenth instance of that
  repair here and one of the few where the missing state is the whole
  finding. **`QA_005`:** A4 is built and unrun — no citation count is
  supplied, the egress gate refuses the databases — and it is one input
  short of interpretable: two constructed corrections with the same
  corrected-share at year 10 have half-lives of **11.4 years and never**,
  so whether a curve counts as *"did not displace"* needs a REFERENCE
  CLASS of corrections that did, which is `criterion-symmetry`'s missing
  comparison table on a second substrate. `half_life()` returns `None` for
  a never-crossing curve rather than a large number, since that is the Q3
  case. **`QA_007`, a finding about the checker rather than the marker:**
  cross-links are reported in two columns because **mention is not
  existence** — `report-typing` has 3 mentions and no artifact, and
  acquired every one the moment the PREVIOUS marker listed it in its own
  cross-links, so the mention-count checker written two drops ago would now
  report it as resolving. `UNI_010`'s self-reference shape arriving through
  a **sibling folder** rather than through the audit's own output, which
  the `EXCLUDE`-list repair does not catch; the fix is a second column, not
  a wider exclusion. Artifacts present 2 of 5, up from 1 of 4, because the
  last drop landed `criterion-symmetry`. **`QA_006`:** 0 of 4 measurements
  run in this environment — A1 broken, A2 and A3 blocked on artifacts that
  do not exist, A4 blocked on egress — though A4 genuinely is runnable by
  someone with a citation database, and is the second item in this family
  `notes/study_watch.py` was built for. Stdlib only, parses under 3.9, CC0.
- `conversation-type/` — A marker proposing **suspendability without
  debt** as the variable motor-carrier distraction rules should be written
  on, in place of channel (handheld vs hands-free): can the exchange be
  dropped mid-sentence with nothing owed on return. Three states in the
  rules' undifferentiated space — emotional/obligated, intellectual/
  unobligated, and silence at hour nine — plus an adjacent finding about a
  desk-worker default prior in general-advice corpora, with *"Instance:
  this session"* attached. **Interest declared, and it inverts:** the two
  previous markers in this family made claims favourable to this author's
  class and the honest move was to decline them; this one is
  **unfavourable**, so accepting is the humble move and rejecting is the
  interested one — which is why `CT_005` reports its null as *not found*
  rather than *did not happen*. **`CT_001`, the strongest move made
  quantitative:** if arousal decays with time constant τ after a call, the
  share of exposure falling OUTSIDE a call-window measurement is 75% for a
  5-minute call at τ=15, 88% for a 2-minute call, and **the shorter the
  call the worse it gets** — so P2's residue-window design is not a
  preference, and on the marker's own mechanism a call-window study reads
  the minority of the effect. It also makes an unstated prediction: a
  literature measuring inside the call window should return small or null
  effects for hands-free, which under the reframe becomes *supporting*
  evidence. **`CT_002`:** binarising a graded quantity costs ~14% of the
  signal on a uniform spread and ~3% on a bimodal one, and the marker's own
  three-state list is bimodal in shape — so the binary is cheap IF the
  distribution is bimodal, which is itself a question P4 answers on the way
  to the main one; threshold at the middle, record near-boundary cases
  rather than forcing them. **Two corrections, both in the marker's
  favour.** `CT_004`: *"three states, one regulatory bin"* is one bin
  short — states 1 and 2 are in the distraction rules and state 3 is in
  **hours-of-service**, a separate instrument, so **a driver who eliminates
  conversation to comply with the distraction rules moves toward the
  vigilance-decrement state neither instrument measures in-shift**; the
  mitigation for one is the hazard for the other and state 2 is the state
  neither names. `CT_003`: the marker classifies itself correctly as a Q1
  case and **inherits `QA_004` without naming it** — *"connected nowhere"*
  is an absence claim with no corpus and no terms, and Q1 cases stay
  provisional until the null is bounded, a standard its own family built
  one drop earlier. **`CT_005`:** checked against the session transcript —
  2151 records, first user turn is the session's actual opening so not a
  post-compaction fragment, 126 assistant turns, 26 search patterns, **0
  hits**. A bounded null produced about the author one drop after
  specifying the standard — and it establishes only that the pattern is
  absent from THIS session under THOSE terms, not that the marker is
  wrong: content has been relayed from other Claude sessions twice, a
  keyword scan is stepped around by paraphrase (`T1-1`), and a null search
  is not exoneration. **`CT_006`:** 2 of 4 cross-links resolve as
  artifacts, and `question-availability` exists because the last drop
  landed it — **third consecutive marker whose named-and-absent set shrinks
  by exactly the folder built the drop before**; `report-typing` is now
  named by three markers, carries Q2's cost channel in one and A3's residue
  measurement in another, and still does not exist. Stdlib only, parses
  under 3.9, CC0.
- `observer-exclusion/` — A runnable measurement spec: **LEAD-TIME**,
  `L = year_literature_adopts − year_excluded_reading_dateable`, for
  populations holding high-hour same-site observation of a system with no
  intake path to its literature. Trigger case is wolf social structure
  (captive dominance model vs the 1999 field correction). **`OE_001`, and
  it is the larger part of the audit:** three design features most specs in
  this family lack — §5 selects cases on the existence of a literature
  reversal BEFORE looking at what the excluded population said
  (pre-registration against selection-on-outcome, exactly the failure
  `criterion-symmetry`'s seed set had), §6 makes the negative arm mandatory
  with the base-rate argument in one sentence, and §7 F1 is a **publishable
  null** (*"the reading may exist and be unrecoverable… it bounds what any
  future study can do"*), which is `QA_004`'s standard met in advance by
  the same family one drop on. **The audit turns on one observation:**
  `year_excluded_reading_dateable` is set by when someone wrote it down and
  the artifact survived, not by when the reading was held — a censoring
  process whose direction is computable before any archive is opened.
  **`OE_002`:** L is **attenuated** — at a stipulated hazard of 0.06/yr a
  true **ten-year** lead measures **−5.6 on average** and is positive 47%
  of the time; the bias runs AGAINST the hypothesis, so a positive L
  survives it. **`OE_003`:** F4's own proposed control — field biologists'
  notes, abstracts, correspondence — is **institutionally archived** where
  the excluded population's artifacts are, in §4's words, *"largely
  undigitised"*; simulated with both holding the reading in the SAME year,
  the record shows the field first **74% of the time**, so F4 gets accepted
  on a difference in archiving rather than in holding, and the excluded
  population needs a true lead of about **eight years** before the record
  shows it first more often than not. **`OE_004`:** therefore F1, F2 and F4
  are **not separable on the L distribution alone** — all three return L
  near zero with the reading late or absent — and **the separator is
  already in §4 and is not used as one**: the recording rule logs artifact
  date against claimed observation date, and that difference IS a
  per-artifact estimate of the archival delay. **`OE_005`, the one bias
  running toward the hypothesis and the only one unguarded:** §5
  pre-registers CASE selection and nothing pre-registers ARTIFACT CODING,
  so an unblinded coder on ambiguous trade-press prose has a free parameter
  worth ~22% of the corpus entered as earlier dates; fix is blind coding.
  **`OE_006`:** `Q2` now names **two different mechanisms** three drops
  apart — *"posing the question costs the asker standing"* against
  *"reading held, no channel"* — a channel that penalises entry versus no
  channel at all, and §1 distinguishes itself from "solicited and rejected"
  but not from the previous Q2 because that one has been overwritten. Case
  `021`'s sense substitution inside the family's own vocabulary, fourth
  instance after `state` and `parity`, and it has a consequence: `QA_003`
  identified the PREVIOUS Q2 as `affect routing`, and that identification
  does not transfer, so whoever files a twelfth mechanism must say which Q2
  — if they file this one, `affect routing` is still unfiled. The
  resolution is the spec's own title: OBSERVER EXCLUSION for no-channel,
  *unaskable* for the cost mechanism. **`OE_007`:** every fact about the
  trigger case is carried and egress-blocked, and nothing in
  `OE_002`–`OE_005` rests on any of it — those are properties of a
  censoring process and a coding protocol and hold for any case with the
  stated structure. **`SPEC_V2.md` then arrived, superseding the marker and
  adopting all six findings** — naming split, attenuation, F4 differential
  archiving, δ̂ as separator, coding pre-registration, case not
  load-bearing — with every quoted figure transcribed correctly to within
  rounding (`OE_011`, checked because a spec quoting an audit is a copy and
  copies drift). Both versions stay inspectable. **`OE_008`, the new
  defect, and it is in the section v2 calls its structural core: §4's
  correction has its sign inverted.** With `A = H + D` the first surviving
  artifact, `L_raw = L_true − D`, so `L_true = L_raw + D` and δ̂ estimates
  `D` — the spec writes `L_adj = L_raw − median(δ̂)`. Simulated at a true
  lead of 20: uncorrected 5.08, **as written −9.92 (error −29.92)**, plus
  form 20.08. **The correction moves the estimate further from the truth
  than not correcting**, doubling the bias it exists to remove, while §4's
  own prose says *"L_raw is attenuated"*. One character, and everything
  downstream about `L_adj` inherits it. **`OE_009`:** §8's F4 repair —
  compare δ̂ distributions between populations — checks the term §4 says
  the estimator does NOT recover; the F4 bias is in **survival**, not
  retrospection, and simulated with identical writing and retrospection at
  survival 0.10 vs 0.60 the δ̂ medians are identical (gap 0.0) while the
  record still shows the field first **86%** of the time, so §8's *"report
  as untestable"* branch is unreachable by construction. The repair is
  already in §11 for another purpose — estimate survival from a
  known-complete archive — and needs only to be run per population.
  **`OE_010`:** §3 names three adoption years (1999 / 2008 / 2019), a
  **20-year spread** against the ~17-year archival delay §4 exists to
  correct, so the definitional choice dominates the correction and the
  three L values are three different measurements that must not share a
  distribution. **`OE_012`:** §1 resolves the naming exactly and goes
  further than the audit, naming the other mechanism *affect routing* and
  keeping it as the register's candidate — which closes the loop `QA_003`
  opened, though the register's tuple still holds eight and
  `affect_routing` is still not in it: the naming is settled, the filing is
  not. **`CLASSIFICATION_NOTE.md` then proposes a THIRD mechanism** —
  *recorded, archived, and filed under a category that isn't evidence*,
  on the HBC post journals (continuous from 1670, catalogued to shelf
  mark) and Foxfire (twelve volumes, filed under folklore): *"a wolf
  behaviour account in Foxfire is a hunting tale; the same account in a
  field notebook is data."* **`OE_013`, and it undercuts §4:** the
  censoring correction §4 calls THE STRUCTURAL CORE is a property of the
  **source**, not of the method — on a contemporaneous continuous archive
  both delay terms collapse, a true twenty-year lead is recovered
  **whole** against 0.22 at the spec's own stipulated trade-press hazard,
  and a true ten-year lead comes out positive **every time** instead of
  47% of the time; so the whole of §4 including the `OE_008` sign error
  is machinery for a source choice, and **§6 lists trade press first by
  tractability** where the ordering should be by delay, the two being
  close to opposite — the easiest corpus to reach is the one that
  destroys most of the signal. **`OE_014`:** the two archives
  **decompose the delay §4 could not** — §11 asks for δ_survive from *"a
  known-complete archive"* and names none, HBC zeroes BOTH terms, and
  Foxfire (interviews from 1966 about earlier practice, published and in
  print) holds δ_survive at zero while δ_write is large, so the term §4
  CAN estimate is isolable there; that is the repair `OE_009` needed,
  since F4's bias lives in survival and §8's test measures writing.
  **`OE_015`:** distinct from all eleven filed on thirteen comparisons —
  nearest is `SCORED_AS_WASTE` and it fails on the right distinction,
  waste being a devaluation **inside one ledger** where this is a
  **transfer to a different one**, while `MODALITY` fails for the reason
  that makes the mechanism interesting (the apparatus is a catalogue, in
  the right channel, and it *routes* rather than misses) — and **the
  ordinal is ambiguous by exactly three**, which is why the off-by-three
  has now happened twice (`QA_002`, `nonidentity-census` T4): the
  register's `MECHANISMS` tuple holds 8 in one file and `MECHANISM_NN.md`
  holds 3 in sibling folders numbered as if they continue it, so SPEC_V2
  §1's candidate is either the ninth tuple entry (colliding with CATEGORY
  WELD) or the twelfth file, both defensible. On the continuing sequence
  this note's mechanism is 13th. **`OE_016`:** first mechanism in this
  family with a **metadata signature** — subject classification (free),
  citing-field distribution (a citation database), content-vs-filing
  mismatch (a reading sample) — with the stated prediction that citations
  to a folklore-filed behavioural corpus cluster in folklore and
  area-studies venues and are near-absent in the field the observation is
  about; that tests the **mechanism** where the lead-time study tests its
  *consequence*, is cheaper, and has a reachable negative unlike §7's F1.
  **`OE_017`:** every archive fact is carried and egress-blocked with
  nothing in `OE_013`–`OE_016` resting on it, plus one flagged before
  anyone orders boxes — HBCA puts a **series letter** between post number
  and volume, so Albany post journals would be **`B.3/a/1-212`** and not
  `B.3/1-212`; stated from memory, unverified, and the correction is a
  shelf mark, so a reader following the note as written asks for a series
  that does not exist. Stdlib only, parses under 3.9, CC0.
- `sheet-structure-scan/` — Built to a delivered spec: two scans over a
  spreadsheet plus a ranking, with the delivery kept verbatim in
  `SOURCE_DROP.md`. **Scan two, companion absence** — for a flagged cell,
  which of `unit` / `date` / `sample_size` / `variance_sibling` is
  *missing* from its neighborhood, reporting what is not there rather
  than what is. **Scan three, header collision** — labels across all
  sheets grouped by normalized string and listed when their cells differ
  in precedent depth or in constants-versus-derived. **Ranking**
  `deps × downstream_depth`. **The two spec constraints are the folder's
  spine.** (1) *stdlib plus one spreadsheet reader* — **the budget is
  unspent**: `.xlsx` is a zip of XML and formulas sit in
  `xl/worksheets/sheetN.xml` as `<f>` elements, so `zipfile` +
  `xml.etree` reach everything, and the larger reason is not frugality
  but that **both scans are about the formula layer** the common reader's
  value-only mode drops — the layer under test cannot be discarded by the
  reader meant to deliver it. (2) *never label a site* — enforced rather
  than requested: `no_severity.py` screens 78 words across severity and
  interpretation over every emitted table, is **null-tested in both
  directions** (planted word per class caught; `terror`/`mustard`/
  `bustle` checked against `UNI_009` substring bleed), and states its own
  limit at the top of the file — *a keyword screen is stepped around by
  any paraphrase*, `DF_010`/`ACL_017` on a new substrate. **`SSS_003`,
  the load-bearing one:** scan two begins *"for every flagged cell"* and
  **scan one is not in the delivery**, so the flag set is an INPUT and
  running without one is **refused**, never defaulted — and the case is
  measured, not argued: under `--all` **23 of 38 rows carry an absence
  and 15 of those 23 are label cells or strays outside any table** (a
  header reading `unit price (USD)` is not itself under a header, so it
  reports `unit` absent), against a five-cell list giving four absence
  rows, three of them values in a table. **Three findings are failures
  the fixture produced.** `SSS_002`: a square neighborhood of radius 2
  **reports a correctly built six-column table's own `sd` column
  absent**, three columns being outside the block — and the repair is the
  SHAPE, not the radius, since radius 6 reaches the adjacent record and
  trades a false absence for a false presence, which §2 argues is the
  costlier direction because it removes a row from a report whose subject
  is what is missing; replaced by a cross (the whole record row, the
  column within ±radius, and the label-row cell above every column the
  row touched). `SSS_009`: `=LOG10(A1)` returned `{A1, LOG1}` — the
  lookahead refuses a ref followed by `(`, so the engine backtracks to
  `LOG1` — putting a function name into the precedent graph, which would
  have made **the rank column wrong for a reason invisible in the
  output**; caught by a fixed-in-advance selftest case, not by reading.
  `SSS_006`: keeping parentheticals costs a true collision the fixture
  carries (`unit price (USD)` `2c{0}` vs `unit price` `2d{1}`), and
  stripping them would merge `revenue (net)` with `revenue (gross)` — the
  default is the one that under-reports and the choice is stated.
  **`SSS_004`:** `deps × ddepth` makes **every terminal rank 0**, so the
  cell whose number gets quoted ties for last with an unused stray —
  propagation is what the delivery asked for, and near the bottom of a
  sheet propagation and consequence run opposite; `pdepth` is a column so
  the tie is breakable, and changing the sort would make the ranking a
  claim about importance, which the no-labelling constraint bars.
  **`SSS_007`:** three companion states plus an `unsearched` column
  (`N`/`S`/`no-col-label`/`no-row-label`/`is-label`) — the
  absent-vs-known-negative repair designed in rather than found, with
  cells carrying no absence kept in the table so the denominator stays
  visible. **Ten parameters the delivery left open** are marked
  `[CHOICE n]`, defaulted, overridable, and printed into the report
  header when in force. `sheetmodel.py::rank` is registered in
  `tools/known_answer.py` with four cases (chain 2 / fan 3 / terminal 0 /
  cycle `CYCLE`) that separate the two factors. `fixture.py` writes the
  demo `.xlsx` with `zipfile`, so the repo stays text-only and the
  workbook is a readable table. **`SSS_010` UNVERIFIED:** nothing has met
  a real workbook, F1–F4 all need one, and three of ten claims are
  failures the fixture produced — *passing is weaker evidence than
  failing* (`membership-probe`'s LIMITS, same asymmetry).
  **`targets/` pre-registers five workbooks across three publishers and
  reads none of them.** The denial is an **allowlist, not a per-host
  block** — `www.epa.gov`, `unfccc.int`, `theclimateregistry.org` and
  `example.com` all return 403 to CONNECT while `github.com` reaches the
  origin, DNS resolving for all of them (`SSS_015`), so substituting a
  publisher does not help and there is no third host worth trying; a
  mirror on an allowed host was not sought, that being circumvention
  rather than compliance. The Emission Factors Hub arrived
  as a known-answer case with the standard *if the scan does not light
  that up, the scan is broken*, which had no value attached; ten
  predictions are now registered before any file was opened: six for the
  Hub, and P1-P3 for each of **three** live-calculator arms (EPA Local
  Tool, UNFCCC calculator, Climate Registry tool) plus P4 for the one
  whose modules were named in advance. **`SSS_016`:** the three arms are
  registered separately rather than merged, because what follows from
  *"a live calculator"* is not what follows from a *described module
  structure* — and the selftest requires **each** arm to discriminate,
  since a second one that does not adds a name and no evidence.
  **`SSS_013`: the pair is the test.** A Hub run alone cannot separate *the scan works and the Hub
  is flat* from *the scan reports everything flat* — the two predict the
  same output — so the Local Tool is the discriminator and every report
  ends by saying it is one arm. **`SSS_011`, the one that earned the
  exercise:** building the criterion against a target-shaped fixture
  found that scan three listed every shared header on a difference in
  **table height** (`12c` against `9c`), producing five column collisions
  on a fixture where nothing collides — and the Hub is exactly that
  shape, many sheets sharing headers over different row counts, so it
  would have lit up with a rank beside each row and read as a finding.
  The delivery asks *whether* the cells are constants versus derived and
  **whether is a set**, so the listing decision now takes the kind set
  (`c`/`d`/`c+d`) with the counts kept in the printed column. **`SSS_012`:**
  `EFH-P4` is a share and passed on an **empty denominator** — a
  single-sheet workbook has no repeated label — which is `PCH_001`
  reached a second time in a second folder by a different route; shares
  now name their denominator and return `NOT_DETERMINABLE`, both branches
  pinned. **`SSS_014`:** `patterns.json` was widened before the data
  (generic parenthetical removed as too loose, mmBtu/therm/scf/MWh/short
  ton/CO2e added) in the direction that makes the tool's own `unit
  present` prediction easier — disclosed in the file's `_note` and the
  claim table, and bounded structurally, since **no edit to the unit list
  can make the variance or sample-size patterns fire**, which is where
  the load-bearing differential sits. The criterion is null-tested on two
  synthetic shapes (flat holds 6 of 6 `efh` and fails both `local`
  discriminators; chain the reverse) with the synthetics loudly marked as
  no evidence about any EPA product. One contingency named: a target
  shipping as legacy `.xls` makes `read()` raise, and **that** is when
  the one-reader slot gets spent — the test `SSS_001` sets for itself.
  **`coupling.py` then replaced the ranking's first factor**, per the
  integration order: a **dimensionless elasticity** measured by
  perturbing a constant and reading the output cells, falling back to
  dependent count where a formula is not evaluable, with the mode named
  per row because `coupling x depth` and `deps x depth` are not on one
  scale. **`SSS_025`:** the evaluator is checked against **Excel's own
  cached values** and reproduces **631 of 631 with zero disagreements** —
  a known-answer run on a file nobody here wrote — and `verify` is
  itself null-tested on a fixture carrying one right cache and one
  deliberately wrong one. **`SSS_026`:** the first run returned **0 of
  789** in coupling mode because the workbook is an unfilled template
  (`F6 = D6*E6` with `E6` empty moves nothing), so **coupling is a
  property of the workbook AND a case**, `--input` supplies it and every
  report prints it, with `NO_LIVE_PATH` kept apart from
  `NOT_COMPUTABLE` and from an elasticity of zero. **`SSS_027`:** the
  evaluator was **not re-entrant** — parser state lived on the instance,
  so a nested formula resumed the outer one inside itself, costing every
  rollup in the workbook, and no depth-1 fixture could show it.
  **`SSS_029`:** at one point 627 of 631 formulas evaluated and 0 of 789
  constants got a coupling number, because nearly every constant
  terminates at one grand total and **two `SUMIF` cells gated the whole
  workbook** — coverage of a perturbation is a property of the
  TERMINALS, not of the formula population. **`SSS_028`:** `Report!E23`
  sums `Food!E5:E16`, starting on the **header row** where every sibling
  row starts at 6; Excel ignores text in a range so the workbook
  computes correctly and the off-by-one is invisible in use.
  **`SSS_030`, the result the substitution is for:** under a stated case
  **3 constants have non-zero coupling and 781 have exactly zero, and
  every one of those 781 ranks non-zero under dependent count, up to
  380** — count measures wiring, coupling measures what moves. The top
  row is the Iraq grid factor at coupling 0.6215, and the number is
  interpretable, since the elasticity of a sum with respect to one term
  is that term's share of the total, confirmed to four figures on
  `Fuels!D6`. **`SSS_031`:** `coupling.py cells` reports per-cell
  movement and separates **structural** from **live** dependence — on
  the Iraq grid factor, 26 cells moved against **33 structural
  dependents of which 31 did not**, because a `VLOOKUP` range makes
  every cell in it a graph edge and only the selected row a live one,
  while **24 cells moved that are not direct dependents at all**; every
  moved cell carries elasticity exactly 1.0 except the grand total at
  0.881538, a product chain passing a relative change through unchanged
  and only the sum diluting it. **`SSS_032`:** asked whether any
  Palestine cell moved — **none did and none can**, since
  `Electricity, heat, cooling!B296` is a `CONSTANT_NUMBER` and row 296
  holds only a country name and a number, so the mean-of-five
  relationship the workbook states in prose at `Info and sources!E10`
  is a record of how the number was produced and **is not maintained by
  any formula**: revise a neighbour upstream and this cell does not
  follow.
  **Then two real workbooks arrived and `SSS_010` closed.** The UNFCCC
  calculator holds 3 of 3 — **but not on the first run**: `UNF-P1` came
  back `0.037` against a registered `> 0.20`, and the cause was the
  reader, not the workbook. **`SSS_017`, the largest defect in the
  folder:** 720 of the workbook's 825 formula cells are **shared
  formulas**, whose text lives once on a group master with every follower
  carrying only an index, and the reader took an empty `<f>` body as no
  formula — reading **696 cells as constants** (129 derived, exactly the
  105 plain plus the 24 masters that carry text), so `pdepth`/`deps`/
  `ddepth`/`rank` were wrong for everything downstream of any of them.
  Repaired with `shift_formula()`, which translates a master's relative
  references with `$`-pinned halves left alone and string literals masked
  at preserved length; eleven hand-set cases pinned. **The fixture could
  not have shown it** — `fixture.py` writes only plain formulas — which
  is `SSS_010`'s *passing is weaker evidence than failing* instanced.
  **`SSS_019`:** a threshold fixed before the file existed is what made a
  reader defect the live hypothesis rather than the available and wrong
  story (*this calculator is mostly reference tables*); `UNF-P2` and
  `UNF-P3` holding in the same run is what pointed at it, and after
  repair `derived_share` is `0.226`, held by a small margin and reported
  as such. **`SSS_018`, the honest one:** the regex used to diagnose
  `SSS_017` was itself wrong in the same direction — `[^>]*` swallows the
  `/` of a self-closing tag, so it merged `<f/>` with the next real `<f>`
  and reported 476 against a parse's 825; both errors undercounted, so
  the diagnosis survived by luck rather than by method. **`SSS_020`, the
  substantive finding:** scan three lists 4 groups of 33, and `factors`
  appears as a column label on 11 sheets — eight carry pure constants at
  depth `{0}` while **`Home Office` carries `31d`, pure derived, at
  `{1}`: that sheet computes its emission factors where eight others
  hardcode them** — with the consequence one level deeper in the
  `kg CO2e` output column (`{2}` there, `{1}` on nine sheets).
  **`SSS_021`:** two of the four differing occurrences per group are
  **stacked-table artifacts**, checked and separated rather than assumed
  clean — `Electricity, heat, cooling` and `Water` stack several tables
  in a column and `CHOICE 4` assumes one label row per sheet, measured by
  counting cells in each governed range whose text normalizes to the
  group's own label (2 and 1 against 0 on the other nine); unrepaired,
  since the fix changes the label model for every sheet. **`SSS_022`:**
  on the 22 cells scan three surfaced — a flag set produced by an
  upstream scan rather than invented — `unit` is present on 22 and
  `date`/`sample_size`/`variance_sibling` absent on 22, which is the
  differential the Hub was offered to demonstrate, on a workbook that is
  not the Hub. **`SSS_023`:** the `.xls` target fired the §5 contingency
  as registered, **and the slot stays unspent for a reason** — the file
  is valid BIFF8 carrying 336 `FORMULA` and 23 `SHRFMLA` records while
  `xlrd` 2.0.2, the one reader for the format, exposes cached values and
  no formula text, so spending the budget delivers exactly the value-only
  view `SSS_001` named as the reason to parse XML directly; LibreOffice
  is installed, fails on the file, and **fails identically on a control
  this tool parses**, so the install is broken here and says nothing
  about the `.xls`. **`SSS_024`:** the output screen ran in one of two
  CLIs and the gap surfaced on a real run. **Scan 4 (`WORK_ORDER_4.md`,
  verbatim) then asks whether a formula still maintains what the prose
  states** — four bins (`MAINTAINED` / `HOLDS_UNMAINTAINED` / `BROKEN` /
  `NOT_TESTABLE`), no aggregate score, no ranking, and BROKEN is not
  called an error, since a workbook may have every reason to hold a number
  the note beside it no longer describes. **`SSS_033`: on the UNFCCC
  calculator the bins are 0 / 2 / 21 / 11** — 135 prose cells across
  eight keyword-located sheets, 124 not arithmetic — so **not one stated
  arithmetic relationship in the workbook is maintained by a formula**;
  every one is stated about a constant, and the two that hold, hold by
  history rather than by construction, which is `SSS_032` generalised from
  one case to the file. **`SSS_034`, the headline:** `Info and sources!E10`
  states that twenty-two named territories each take the average of
  thirty-three named places, and **twenty of them hold
  `0.52194015744421518`, which is `Electricity, heat, cooling!B329`
  (Western Sahara) to all seventeen digits** — the target of a *different*
  stated relationship in the same cell of prose, the average of five North
  and West African countries, and that one holds; one (Macao) holds a
  third number and **zero hold the stated mean**, verified by hand on
  `B114` and `B329` independently of the scan. **`SSS_035`:** operand count
  separates the bins here — both 5-operand relationships hold, the one
  33-operand relationship does not across every target it states,
  `BROKEN/(B+H) = 0.913` — and that is exactly the quantity the order says
  to accumulate, so the rate emission prints `n = 1` and refuses a curve in
  those words: *a point is not a rate*. **`SSS_038`:** `when it diverged`
  returns **UNRECOVERABLE** and says so — `.xlsx` carries no per-cell
  revision history, so the file cannot date the divergence and the tool
  does not estimate one; a version series of the same workbook would
  bracket it. **`SSS_036`:** three resolution problems the real prose
  forced (a name mismatch, an ambiguous containment match, an operand list
  mis-split 38 against 33) are fixed by stated rules — unique containment
  plus a declared sheet scope, and an index-driven longest-match split
  preserving original casing — rather than by guesses. **`SSS_037`:** an
  operator naming no operands now lands in `NOT_TESTABLE` rather than
  falling out of the count, since a relationship that cannot be tested is
  a reading and not an absence. **WO6 then amended the bin `BROKEN` →
  `DIVERGED`** ("the cell and the stated relation differ", no ruling on
  which is wrong) and **retired the delivered-order exemption entirely** —
  no token in the order fires, so no file fires and nothing is masked,
  with the three-arm harness kept for a real exemption later; across every
  pinned sample **one file still fires and it is `no_severity`'s own
  selftest transcript**, which must contain the words it screens in order
  to test them (`SSS_049`, a statement about the screen's scope). **WO6 —
  a second workbook and a legacy reader.** **`SSS_040`: the legacy
  constraint is a property of the READER, not of the format** — true of
  `xlrd` (`SSS_023`) and false of the file, since a `.xls` is a
  compound-file container holding a BIFF record stream and `struct`
  reaches it; the target carries **336 `FORMULA` and 23 `SHRFMLA`**
  records, all 336 decode, `xlsreader.py` is stdlib, and **the one-reader
  budget stays unspent for a second file format**, with capabilities
  declared per item (`formula_text` **no**) so callers mark scans NOT_RUN
  from a declaration rather than a note. **`SSS_041`, two decoding defects
  the real file produced and no fixture could**: shared-formula masters
  are written *after* the first formula using them, so stream-order
  resolution gave 23 cells an empty precedent list reading as *no
  precedents*; and relative areas (`ptgAreaN`) were walked past rather
  than decoded, leaving 145 formulas with no edges and no flag — 188 of
  336 → **336 of 336**, 714 edges → 1056, with the relative column delta a
  signed BYTE and not the 14 bits an absolute ref uses. **`SSS_042`: the
  prediction written to fail cleanly is the one that failed.** P4 (*at
  least one testable relationship*) was registered before the run
  precisely so P1–P3 would be **unreachable rather than refuted**, and it
  went — 189 prose cells, 188 not arithmetic, **0 testable** — with the
  zero measured as a property of the workbook rather than argued
  (`average` 0, `mean` 0, `sum of` 0, `multiplied` 0, `divided` 0,
  `equals` 0, `=` 0 across all 189). **`SSS_043`, what the second file
  actually bought and it is not what H1 asked:** the two workbooks'
  provenance prose is a different KIND — UNFCCC states *"Bonaire: Average
  of American Samoa, …"*, retrospective and about values it ships; LGO
  states *"Description of computational method:"*, prospective and about
  values a filer will supply. Both are unfilled templates, so fill state
  is not the difference; one **ships data with provenance notes** and the
  other **collects data with instructions**, and only the first kind can
  state a relationship about its own cells, so **H1 is not addressable
  here rather than unsupported** — reporting the file as evidence against
  H1 would count a workbook that cannot answer the question as an answer.
  **`SSS_044`:** `diverged_share()` therefore returns `None` and not
  `0.0`, since zero would put a workbook with nothing to measure at the
  good end of a scale it is not on (`PCH_001`, thirteenth instance here),
  and `direction()` returns **`NO_DIRECTION`** naming the empty
  denominator, with n = 2 printed and no curve emitted. **`SSS_045`:**
  "file date" turned out to be **two dates eight years apart** on the
  legacy target (2008-06-04 created / 2016-05-02 modified, on a form whose
  filename states the later one), so the column is headed
  `created / modified` and carries both — and only the two date properties
  are read, the same property set naming a private individual which
  nothing reads. **`SSS_046`, the live one the order caught:**
  `coupling.py` ranks by elasticity where computable and by dependent
  count where not, which is right on a readable workbook and is exactly
  S1's forbidden substitution on a reader with no formula text — it
  printed a COUNT table under a coupling heading with nothing saying the
  coupling arm had not run; it now stops with `COUPLING IS NOT_RUN ON THIS
  WORKBOOK` and **does not offer the count as a stand-in**, since the two
  disagree on this repo's own evidence (`SSS_030`), pinned in both
  directions. **`SSS_047`:** scan three's finding on the legacy file is
  the collision it exists for — `total location-based scope 2 emissions`
  labels ten row blocks meant to be parallel sectors and some govern
  `1c+4d` where others govern `4d`, 9 of 17 repeated-label groups listed
  and 8 agreeing on both axes. **`SSS_048`:** the single non-arithmetic
  exception is `often times`, an adverbial matched as multiplication —
  `UNI_009`/`T1-1` inside scan 4's own operator vocabulary — caught by the
  operand requirement `SSS_037` added rather than by the operator match,
  and recorded rather than repaired since a word boundary does not
  separate two senses of one token. **WO7 asked for a third workbook and
  the run did not happen; the screen did.** **`SSS_050`:** S1(b) is
  *"provenance prose classified RETROSPECTIVE under the amended WO4
  test"* and **no such test existed** — `SSS_043` drew the distinction in
  prose from two workbooks and nothing implemented it, `RETROSPECTIVE`
  and `PROSPECTIVE` appearing zero times in the folder before
  `selection.py` — sixth instance of the stated-rule-with-no-field shape,
  and building it is most of the order. **`SSS_051`, the trap the
  classifier had to avoid:** the easy version of (b) — *does any prose
  cell yield a resolvable relationship* — **is** (c), two criteria
  computing one quantity, so (b) reads **stance** and (c) reads
  **resolvability** and `independence()` reports whether they have been
  observed disagreeing; **off-diagonal 0 of 3**, so on this population
  the screen cannot say which criterion does the work, and the separating
  case not in hand is a retrospective note whose operands sit outside the
  file. **`SSS_052`, and it decides `SSS_051`:** `min_retro = 1` is a
  `[CHOICE]` and the UNFCCC calculator carries **RETRO 4 against PROSP
  9** — more prospective prose than retrospective, in the file holding
  all 23 testable relationships — so a **majority rule** rejects at (b)
  the only workbook (c) accepts, making the threshold calibrated by a
  case rather than stipulated, and under that rule the file **is** the
  off-diagonal cell: whether the two criteria are independent is a
  property of the threshold. **`SSS_053`, the reject log:** every
  criterion is recorded rather than stopping at the first failure, and
  they separate cleanly — the prior file passes all three content
  criteria (a)-(c) and neither novelty criterion (d)-(e), while the LGO
  file fails all five; **no third candidate is reachable**, with
  `epa.gov`, `unfccc.int`, `theclimateregistry.org`, `eia.gov`,
  `data.gov` and `ipcc-nggip.iges.or.jp` all returning a refused CONNECT
  and only the GitHub hosts responding, and two of three uploaded files
  byte-identical so the distinct population is **two** — so S1's own
  hypothesis (*if most published workbooks fail (b) or (c) the population
  is small*) is untested **not because most workbooks fail but because
  none could be screened**, which is `SSS_043` applied to the order's own
  method. **`SSS_054`:** all four S3 predictions return **NOT
  ADDRESSABLE**, the verdict S3 made legal one order after `SSS_043`
  argued for it. **`SSS_055`:** S4's `OUT_OF_SCOPE` is built and its
  first implementation **dropped the row it exists to keep** (a
  `continue` removed out-of-scope workbooks from the denominator *and*
  the table), with a second defect the `G1` fixture caught — reading
  scope off the share's denominator calls a workbook whose relationship
  IS enforced by a formula out of scope, since MAINTAINED counts; the
  stance test is **imported** from `selection.py` rather than
  reimplemented so screen and emission cannot disagree about
  RETROSPECTIVE. **`SSS_056`:** naming the module `select` collided with
  the standard library — it **worked when run as a script** and failed
  the first time it was imported, a collision invisible in the one
  invocation the author used. **`SSS_039`, recorded rather than quietly
  fixed:** scan 4 **shipped without the constraint its own order states**
  — `scans.py` screens every emitted table through `no_severity` and
  `scan4.py` did not import it at all — and screening afterwards returned
  24 hits whose *shape* is the finding: 22 are the `BROKEN` bin name,
  which the work order delivered and which is on the screened list. The
  exemption is **declared and measured** rather than taken (one arm masks
  the delivered token, a second asserts the token is the only thing that
  fires without the mask, since masking `BROKEN` also hides any sentence
  containing it, and a third plants `this cell is wrong` and requires it
  caught through the exemption); the other two hits — a use-mention of
  `error` in the disclaimer and `needs` in the rate emission — were
  **reworded rather than exempted**, the call `residual-direction`
  `RDD_008` made when its own screen fired on its own disclaimer. Holds on
  the real workbook and not only on the fixture. **`SSS_057`, the SBA
  run:** `sba.gov` refuses CONNECT like the six publisher hosts at
  `SSS_053` and no file was uploaded, so the three documents were read by
  nothing and the run is **NOT_RUN on all three** — while the order's
  reader question is answered anyway. `docreader.py` declares per item:
  `container_detect` and `stream_enumerate` **built** (the container
  parser reused from `xlsreader`, not copied), **`text` NOT BUILT**, and
  each absence names what it stops — `text` stops every upward cell, every
  quantified downward stop and the WO7 screen's (b) and (c), so the grid
  has nothing to fill. **The extension is a claim, not a fact**: `sniff()`
  runs first, since a government `.doc` may be OLE Word, a renamed OOXML
  zip or RTF, and the check that matters is tested on a real file — an OLE
  *workbook* must not read as a Word document, and it reads `False` with
  the missing `WordDocument` stream named. **No text-heuristic substitute
  is offered and the refusal is structural**: `read_doc()` raises rather
  than returning a degraded read, and a selftest check reads the module's
  own source to assert no `strings`-style path exists in it. The parser is
  deliberately not written ahead of the files, because `SSS_017` and
  `SSS_041` are both defects a real file exposed that no fixture could —
  **and one file then arrived and it was built against that file**:
  OLE → FIB → CLX piece table → one compressed piece, **7711 characters,
  exactly `ccpText`**, with the decisive check being the halving, since a
  compressed piece's `fc` is doubled in the header and a reader taking it
  raw lands mid-document and returns plausible text (both halves
  asserted). **`FM_021`:** the WO7 screen **short-circuited on a reader
  failure**, recording one criterion of six, and `SSS_053`'s sentence
  ("records every criterion rather than stopping at the first failure")
  was true of a criterion failure and false of a reader failure — repaired
  with a third state, `pass: None` for not-evaluated, which is not a fail,
  plus a shape note saying the screen is workbook-shaped so a `not
  eligible` verdict on a prose document reads as a statement about fit.
  Selftest counts across the folder's modules are totalled by
  `self-scan/census.py`; each module prints its own.
  across nine modules. Stdlib only, parses under 3.9, CC0.
- `claim-record/` — Seven fields per claim, two hard rules, and a
  validator that refuses. Delivered spoken (`SOURCE_DROP.md`, verbatim):
  assertion without hedges / measurement as an interval / instrument plus
  its known error characteristics / domain of validity / clock with a
  next-check date / derivation as parent ids / collapse record. Rule 1: a
  claim with an unresolvable parent does not validate. Rule 2: no field
  is optional, *because optional is how the domain of validity
  disappeared in the first place*. **`CR_001`, the design move:** rule 2
  read as a required-fields list gives a form; read seriously it gives
  **a schema with no way to say nothing, only ways to say "not known, and
  here is why"** — `UNTESTED`, `UNQUANTIFIED` with a `why`, an empty
  parent list with a `root_reason`, and a sentinel without its reason is
  refused, that being rule 2's own failure arriving one level down.
  **`CR_002`, the part a required-field list cannot do:** fields 2 and 7
  are **coupled** — `lo == hi` under `NOT_COLLAPSED` is
  `POINT_WITHOUT_BASIS`, `lo != hi` under `EXACT` is
  `INTERVAL_MARKED_EXACT` — since a point arrives either from a
  distribution or from a count and saying which IS the field; the
  collapse statistic comes from a closed vocabulary with an `other`
  escape that must name itself, which is the repair `UNI_013` asked for,
  designed in. **`CR_003`:** rule 2 gets seven null arms, one per field,
  and **the positive control comes first** because a validator that
  refuses everything passes all seven; eleven further checks require
  well-formed variants to validate rather than merely to be refused. 39
  checks. **Then filled with six real claims from the same day's
  `sheet-structure-scan/` run**, where the provenance is known — all six
  validate, and the useful part is what came back uniform. **`CR_006`:**
  `collapse_record.state` is `EXACT` **6 of 6**, `COLLAPSED` **0** — the
  field the drop calls *the upper-quartile field* has **no instance**,
  because every instrument here is deterministic and every artifact a
  fixed file, so every measurement is an exact count; fields 2 and 7 are
  aimed at measurements with sampling error and this folder has not made
  one, so the selftest exercises the branch and the corpus does not.
  **`CR_005`:** there is **no denominator field**, so 6 of 6 records put
  the population in a free-text `units` string (`129 of 825`, `22 of 22`,
  `1 of 11`) — `measurement-fork`'s VOID RATIO at design time.
  **`CR_007`:** `error.kind` is `systematic` 6 of 6 and `outside_this`
  contains `UNTESTED` 6 of 6, so **the sentinel is doing all the work in
  the field the drop calls the one that always gets stripped** — present
  in every record, which rule 2 buys, and not yet informative, which it
  cannot. **`CR_008`:** there is **no sibling relation**, and the missing
  edge was written as a parent before it was caught — two claims measured
  in one run of one scan were given a parent-child edge, in the file, by
  the author of the schema, minutes after writing rule 1; corrected to
  shared parents and recorded rather than quietly fixed, because it is
  evidence about how a missing relation gets filled (not left blank, but
  populated with the nearest available edge). **`CR_010`:** `due --on
  DATE` read the date as the records directory and printed a well-formed
  table with zero rows and rc 0 — `DL_005`'s shape in a tool about
  denominators, found by running it; repaired, and both `validate` and
  `due` now refuse an empty registry with rc 2. **`CR_009`:** field 1 is
  the one field enforced lexically (38 hedge words, screened both ways
  against `UNI_009` substring bleed) and any paraphrase steps around it,
  stated at the top of the file rather than the bottom. The load path is
  the payoff and is walkable: every claim in the corpus traces to
  `SSS_017`, the reader repair, so refuting it exposes five claims above
  it visibly rather than by memory. **Section 2 then replaced field 5
  with three DERIVED sub-fields** — time constant of the nearest
  neglected term, rate ceiling on the background, coupling — with
  `shelf_life = time_constant / |coupling|` and **no date stored**;
  rule 3 refuses `holds_for`/`next_check`/`shelf_life` as literals, and
  refuses a sub-field with a value and no basis or `UNMEASURED` with no
  reason, those being the two ways to assert it one level down.
  **`CR_012`:** the coupling must be a **dimensionless elasticity** — a
  raw partial `dY/dX` carries units and years divided by that is not a
  duration — so `units` must be `"1"`, which is `G-DIM` applied before
  the number is produced. **`CR_013`, all three behaviours realized on
  real records from the UNFCCC file:** `UNF_GRID_IRAQ` **DERIVED, 3.40
  years**, holding the generation mix fixed with coupling **0.8815
  measured by perturbation** rather than asserted; `UNF_PALESTINE`
  **UNDERIVABLE** — it holds fixed that five neighbours resemble the
  target, never measured, and no branch can produce a date; `SSS_017`
  **UNBOUNDED_BY_THIS_TERM**, its neglected term the reader revision
  which moved **twice in one day** while the domain of validity pins the
  commit, so coupling 0 and *the fastest term in the corpus dates
  nothing*. **`CR_016`:** the three fixtures forced a **fourth collapse
  state** — the hotel factor's statistic is stated in the workbook
  (`upper quartile`, `Info and sources!E19`), the Palestine value is a
  mean computed in the file and verified to **1.1e-16**, and the grid
  factor arrived as a point from a cited dataset the workbook does not
  describe, so `COLLAPSED_UPSTREAM` names the source and the gap rather
  than defaulting into one of the other three; that closes `CR_006`.
  **`CR_017` replaces it:** `rate_ceiling` is `UNMEASURED` on 8 of 9 and
  the regime is `REGIME_UNKNOWN` on 9 of 9, so adiabatic-versus-sudden
  is implemented, selftested both ways, and has never fired on a real
  record — the same shape one field over. **`CR_019`:** the
  no-labelling constraint is honoured by **importing** the detector's
  screen rather than copying it, and it fired on this tool's own
  disclaimer prose twice; `VALID`/`INVALID` are stated to be about
  conformance to the schema and never about whether a claim is true.
  **Three base principles then landed, with an acceptance test.**
  `frames.py` + `frames/*.json`: **(1) no privileged frame**, not even
  the one every record uses — `years` is a registered transform like
  `sols`, an unregistered unit raises rather than resolving by
  assumption, and `due` has **no default frame**, so the reader names
  one; **(2) transforms are first-class versioned objects** beside the
  records, with a rate frame carrying no rate of its own but naming the
  duration frame it inverts; **(3) derived at read time, never at write
  time** — `shelf_life`, `next_check` and every `shelf_life_<unit>` name
  are refused as literals, the derivation returns base units, and the
  reader renders (one record reads 3.403 years / 1243 days / 1210 sols,
  nothing stored converted). **`CR_020`:** the format had four frame
  leaks — `"years"`, `"per_year"`, a hardcoded `365.2425`, and the field
  name `shelf_life_years` — and **not one was in a record**: the data
  was frame-tagged and the CODE was frame-welded, which is why the
  acceptance test passes without editing anything. **`CR_021`:** the
  **identity transform had to be registered** and turned up as a break,
  not a design note — `coupling` declares `units: "1"` and all nine
  records went `UNDERIVABLE` at once until `frames/dimensionless.json`
  existed; leaving `1` implicit would have made it the one unit the
  format resolved without asking. **`CR_022`, the acceptance test:**
  adds `venus_days`, deliberately **not** a file on disk since adding a
  registered frame tests nothing — **9 records read, 0 needing an edit,
  9 still validating** — and beside it a **control**, because a test
  that adds a frame nothing reads would pass on a format that had leaked
  everywhere: the same claim written in the added frame must validate
  here, be **refused** by an implementation with `years` welded in, and
  derive the **same shelf life in base units**. Run inside both
  selftests. **`CR_023`:** requiring `measured_on_frame` edited all nine
  records, and that is a **schema tightening, not a frame addition** —
  the distinction the test turns on. **`CR_025`:** the first run
  reported 3 of 9 validating on six `PARENT_UNRESOLVED` findings, and
  the fault was the harness validating each record in a one-record
  registry, so rule 1 could not see a parent by construction — recorded
  because it is a way an acceptance test reports a failure belonging to
  itself. **Work order 3 then added fields 8-10**, the adjustment history:
  `correction_status` (`unadjusted`/`adjusted`/`unknown`, with S5's
  `raw`/`corrected` as aliases since S6 governs the state vocabulary),
  `correction_method` in field 7's shape, and `correction_depth`.
  **`CR_026`:** field 8 is the **first column in this registry that
  varies** — 6 `unadjusted` against 3 `unknown` — so `CR_007`'s standing
  finding narrows rather than closing; the six are counts computed here
  and the three are values read from a dataset and an index whose own
  production the workbook does not describe. **`CR_027`:** field 10 keeps
  `0` and `UNKNOWN` apart and refuses a missing field, the fourth field
  in this schema to carry that repair. **`CR_028`:** the uninterpretable
  state is a record-layer function both sides call, and its middle case
  matters — unknown history WITH a lean is readable, because a lean that
  survived an adjustment is still a lean. **`CR_029`:** a coupling in
  this registry was **transferred rather than measured, and it was
  wrong** — `UNF_PALESTINE` carried 0.8815 taken from the neighbouring
  Iraq cell on reasoning about the shared lookup, where the measured
  value on the Palestine cell itself is **0.8194**; the elasticity of a
  sum with respect to one term is that term's share of the total, and
  the two factors differ (0.569 against 0.934), so no argument about
  shared consumption makes the shares equal. Corrected in the `basis`
  field rather than in a commit message; it changes no verdict, since
  that record's time constant is `UNMEASURED` and its clock was and
  remains `UNDERIVABLE`. 93 selftest checks across two modules. Stdlib
  only, parses under 3.9, CC0.
- `residual-direction/` — Work order 3, delivered verbatim: read a miss
  history and name the folded term. Companion to the fold detector,
  which finds unbound numbers, and the claim record, which defines a
  bound one. **`RDD_001`, the counterexample the design exists for:** on
  fixture F1 — overpredict small, underpredict large — the pooled sign
  test returns fraction positive **0.5083, no lean**, while the
  conditional slope of residual against predicted magnitude fires at
  standardized **0.868**; both halves of the order's stated PASS
  condition hold, and pooled sign is retained as one printed row rather
  than the verdict. **`RDD_002`:** the ranked list has to be on the
  **standardized** slope, since raw slopes against predictors with
  different units are not on one scale and sorting them is a comparison
  across unlike objects — `G-DIM` in the one place a sorted column looks
  like one quantity. **`RDD_003`, found by reading the output:** in F1
  the predicted values rise with the time index, which is the common
  real shape, so S2(a) and S2(c) carry **identical** standardized slopes
  and a ranked list cannot say which the residual leans with; the order
  asks for the term to be NAMED rather than inferred, and naming one of
  a collinear pair is a specific wrong answer rather than an absent one,
  so the report emits `NOT SEPARABLE` with the group and states what
  would separate them. **`RDD_004`:** all four cells of the S3 2x2 are
  reachable and a **missing coupling is a fifth state**, not weak —
  treating it as weak would route a case to LOG AND LEAVE on an absence;
  `LOG_AND_LEAVE` on F2 names no term, because there the lean is a
  pooled offset and no conditional row leans. **`RDD_005`:** S4's
  stable-versus-growing verdicts print as three distinct reports across
  F1/F2/F3, asserted rather than trusted, since two findings that print
  the same are the same finding. **`RDD_006`:** F4 returns
  `UNINTERPRETABLE` and the identical series with a known history returns
  a readable cell — the difference is entirely in the record.
  **`RDD_007`:** S5 names field 8's values `raw | corrected | unknown`
  and S6 replaces the state vocabulary with `adjusted / unadjusted`;
  **S6 governs** and S5's spellings load as aliases, recorded rather than
  resolved quietly, because an internal tension in a delivered order is a
  fact about the order. **`RDD_008`:** the S6 screen composes its
  patterns from tokens so the banned phrase never appears in its own
  source, which lets `naming.py --source .` scan the folder **including
  itself** with no skipped region — avoiding a second instance of
  `UNI_010`'s hand-broken loop — and the one exemption, the delivered
  order, is **measured**: the selftest checks both that the tool is clean
  with the specification excluded and that the specification is the only
  file that fires without it. **`RDD_009`:** field 8 is the **first
  non-uniform column** in the claim registry (6 `unadjusted`, 3
  `unknown`), narrowing `CR_007`/`CR_017` rather than closing them — the
  six are counts computed in-session, the three are values read from
  sources that describe neither, which is `COLLAPSED_UPSTREAM` from a
  second side. **`RDD_010`:** S3's coupling is **imported** from the
  claim record rather than reimplemented, so the number the
  discriminator responds to is the same object the clock divides a time
  constant by — and it was measured by perturbing a cell in a real
  workbook, not stipulated anywhere in the chain. 49 selftest checks
  across two modules. Stdlib only, parses under 3.9, CC0.
- `model-provenance/` — Work order 5, delivered verbatim. Two halves that
  do not share a mechanism: a **write** at session open (date, model
  identifier as self-reported, repo, branch) and a **read** over history
  that never writes back into it. **`MP_001`, the finding that makes the
  rest checkable: the forward log S1 asks for already exists, unplanned**
  — 159 of this repository's 236 commits carry a self-reported model
  identifier in the `Co-Authored-By` trailer, a channel built for
  attribution doing provenance by accident (Opus 4.7 ×40, Opus 4.8 ×1,
  Opus 5 ×118, 77 stating nothing). **`MP_002`:** that supplies the check
  set a decode needs to be a measurement rather than a rendering — 118
  SINGLE-and-matching, 36 SINGLE-and-differing, 2 AMBIGUOUS containing, 3
  AMBIGUOUS excluding, with no pick made in the ambiguous rows per S2.
  **`MP_003`, the headline: the assumption S3 names is refuted on the
  record** — *always current-at-the-time* fails on **39 of 159** commits,
  because `Opus 4.8` appears 2026-07-12 and `Opus 4.7` keeps appearing for
  a month after; the reading is not that the dates are wrong but that
  sessions do not all run the newest version, which is exactly the content
  of the assumption, so S3 was right to make it the claim rather than a
  fact about a commit. **`MP_004`, and it is why the report prints two
  numbers: all 39 rest on one commit.** `assumption_sensitivity()` drops
  each table row in turn — remove the single 2026-07-12 commit and the
  record is monotone, **0 backwards and 1 disagreement** instead of 39 and
  36. One counterexample still refutes a universal so `MP_003` stands, but
  a count is not a size and the two read as one thing; both are printed
  and neither is picked. **`MP_005`, found only by real data:** the
  decoder read `--date=short` and the 4.7 → 5 switchover happens **inside
  one calendar day**, bracketed by the timestamps to **5 h 14 min**
  (17:20:27 → 22:34:13 on 2026-08-11), so day-ordering reported three
  counterexamples that are an artifact of the reading — a `G-RES` pair
  where the feature is hours and the instrument was days. Repaired (full
  stamp orders, short date decodes, since a decode cannot be finer than
  its table), residual 3 → **0**, pinned by two checks. **`MP_006`:** S1
  says write UNKNOWN if the build string is unavailable, and UNKNOWN has
  more than one cause — this session operates under a standing constraint
  against writing a model identifier into a pushed artifact, so the string
  was **not unavailable, it was not written**; `open_line()` requires a
  reason from `NO_BUILD_STRING` / `WITHHELD` and **refuses a bare
  UNKNOWN**, with the first row of `sessions.jsonl` recording the conflict
  rather than resolving it. Designed in before the first row, unlike the
  dozen-odd prior instances of that repair found in audit. **`MP_007`:**
  S2's release-date table is not reachable (allowlist egress) and a table
  from memory is the `ANC_010` status, so `releases.json` ships **observed
  bounds** from the trailers, `table_kind: observed_bound`, with every
  report header stating that a first appearance is an **upper bound** on a
  release date and never the date — and the cost stated in full, since the
  substitute table is derived from the same trailers it is scored against,
  leaving only the **ordering** check independent of it. **`MP_008`:** the
  77 commits stating nothing are the population the decode exists for, so
  it is checkable exactly where it is redundant and informative exactly
  where it cannot be checked; kept as its own row rather than folded into
  a rate. **`MP_009`:** S4 is structural, not promised — the only git verb
  in the module is `log`, **asserted in the selftest over the file's own
  source**, and writing that check produced one more `UNI_010`: the first
  pattern was a literal and matched the line defining it, so it is now
  composed from tokens (`RDD_008`). The `no_severity` exemption list is
  **empty**, unlike scan 4's — this order's verdict names carry no
  screened word — and the two arms plus the plant still run.
  `--selftest` green. Stdlib only, parses under 3.9, CC0.
- `hf-incident-extract/` — A work order delivered verbatim (`WORK_ORDER.md`)
  and built as **one stdlib file**: read a METR/Redwood incident report
  plus transcripts if released, emit **counts, no labels**. Six measures
  (M1 explore_ratio `t_characterize / t_solve`, M2 root_fanout, M3
  upstream_edits env-edit over gate-fool moves, M4 member_cost runs
  self-failed for the collective over runs_total, M5 log_scrub_split
  actions_edited over reasoning_edited, M6 opponent_by_slot as a bool per
  agent), the GATE_PROPERTY_TEST (`gap = declared(paper) △
  implemented(code)`, a non-empty gap predicting M1 high and M2 high — the
  charter-signature check), a CROSS_SUBSTRATE table (pea tendril /
  fledgling / ant bridge / fire crew / swarm; M1, M4, `unit_boundary !=
  objective_boundary`), and the two OPEN items. **The report is not in
  hand** — egress is an allowlist — so **every real cell is UNMEASURED
  with the input it wants named**, and nothing in the folder holds a
  value from the report or a biology figure from memory. **`HFI_002`, the
  design:** the order's INPUT is prose and its OUTPUT is counts, and
  between them sits a reading, so the two are kept in two layers —
  `text_scan()` finds every stated duration and count with its line
  number and emits them as **candidates** (a candidate is not a measure;
  a planted "Version 2.0" decoy is not promoted), and `measures()`
  computes from a **coded sheet** the reader fills, where every field
  carries a unit or a state and an UNMEASURED field returns `None` for
  every measure needing it, never 0. **`HFI_003`:** the
  charter-signature check can fail — a gap of zero predicts nothing, a
  measured M1 below the threshold fails the check, an unfilled gap
  returns `None` — so it is not `CONSTANT_FIRES`; "high" is not in the
  order, and 6.0 / 0.5 are `[CHOICE]` constants printed on every render.
  **`HFI_004`:** *same instrument, no vocab change* is asserted over the
  AST — no substrate name appears in any function body — and a filled
  fictional fire-crew row computes through the same functions the report
  row does. **`HFI_005`:** `NOT_RELEASED` (transcripts) and
  `NOT_COLLECTED` (post-validation off-trail fraction, report silent) are
  states distinct from UNMEASURED, which is wanted and readable.
  **`HFI_006`:** a duration with no unit is refused rather than read as
  hours (G-DIM before the ratio; days and hours converted to one scale).
  **`HFI_001`:** known answers first on a constructed sheet labelled so,
  with a zero denominator returning `None` and not infinity.
  **`HFI_007` UNVERIFIED:** built and proven on constructed fixtures,
  unrun on its subject; the coded sheet is the operator's step once the
  report is in hand. Renders screen clean through `no_severity` with no
  exemption. Check count printed by `selftest_hf.py`; the instrument
  refuses `--selftest`. Stdlib only, parses under 3.9, phone-buildable,
  CC0.
- `label-position-test/` — A work order delivered verbatim
  (`WORK_ORDER.md`), pre-registered before any data: do valence labels
  on a probing move (*cheat* | *innovation*) track the MOVE, or the
  actor's POSITION and the OUTCOME after the fact (H1), and is the party
  defining the term the party gaining from it above chance (H2)? Built
  as **one stdlib file** computing what the order's procedure asks for
  from a flat CSV in its schema — Cramér's V by hand for `label_valence
  ×` position / move / outcome / actor, the P2 leak test, P5 overlap
  against chance, the seed case's within-document control, Fleiss'
  kappa for P3 relabelling — with the order's own FALSIFICATION rule
  applied to the numbers and `undetermined` printed wherever a number
  it needs is None. **No data ships**: the seed report is not reachable
  from here (allowlist egress), the control has nothing to run on and
  the unfilled render says so; rows under `samples/` are constructed,
  carry a `constructed://` scheme, and are counted apart from public
  rows. **`LPT_002`:** the order's OUTPUT row (one per term) cannot
  carry its own cross-tab wherever a term has one valence — *cheat* is
  always negative, so every V on that row is undefined, printed `--`
  rather than 0, and the cross-tabs live on the pooled row.
  **`LPT_003`:** H2's chance is undefined in the order; under the
  independence reading built here (`Σ_a p_arb(a)·p_ben(a)` within the
  source class, `[CHOICE 1]`) a class with one arbiter and one
  beneficiary throughout has chance 1.0 and H2 is FALSE for it by
  construction, so H2 is testable only where the arbiter varies within
  a source class — a sampling requirement P1 does not state.
  **`LPT_004`:** the leak tuple spans 72 cells and the order's N floor
  is 30, so the in-sample reading approaches 1.0 by construction
  (nine unique tuples read 1.000) and only leave-one-out is readable.
  **`LPT_005`, found by running it:** leave-one-out majority prediction
  reads BELOW baseline on a balanced set (0.000 against 0.250), because
  removing the scored row makes its own class a minority — so a leak
  below baseline is the estimator, not a result, and the readable
  statement is *above baseline* only. **`LPT_006`:** `overlap` is coded
  and is also what `arbiter == beneficiary` says; the instrument
  derives it and counts disagreements per class. **`LPT_008`:** two
  constructed worlds separate under the order's rule (valence tracking
  position → V_position 1.000, V_move 0.000, H1 not falsified; tracking
  move → the reverse, H1 FALSE), so the rule is neither
  `CONSTANT_FIRES` nor `CONSTANT_SILENT` here. **`LPT_009`
  UNVERIFIED:** no public row coded, no labeler run, nothing bearing on
  H0/H1/H2 — and the order's last limit applies to this folder too.
  Three `[CHOICE]`s printed on every render; renders screen clean
  through `no_severity` with no exemption; no author section.
  **A revision then landed** (`WORK_ORDER_V2.md`, verbatim beside v1)
  adding one bullet, the **N2 CONTROL** — the missing control from
  `zero-sum-curriculum-null/`, specified with three measurables and
  filed in this order. `revision_audit.py` checks it as a copy and as a
  claim. **`LPT_010`:** a pure insertion, one six-line block, and the
  CHANGELOG did not move with it — P6 asks for versioned diffs and the
  order's own revision is unlogged. **`LPT_011`:** `N2` and `the null`
  occur zero times in v1 and once each in v2, inside the bullet; the
  referent is one folder over and is imported, not restated.
  **`LPT_012`:** against the `hf-incident-extract` sheet, self-risk
  rate is M4 exactly, channel split is partial (M6 reads the gate
  channel; peers and third parties have no field) and probing rate is
  partial (probe classes counted, no per-run denominator) — and the
  channel split is N3's residual, now specified for measurement in the
  control setting. **`LPT_013`/`LPT_014`:** a transparent scorer
  removes `opacity` from N3's three stated inputs, so a persisting
  split narrows N3 and does not close it, while the bullet's *persists*
  sentence names the template where the null construction's own table
  routes to N3 — *"either result closes an open branch"* holds for
  `vanishes` and overstates for `persists`. One declared `no_severity`
  exemption (`risk`, inside the delivered term *self-risk rate*) under
  the three-arm harness. Check count printed by `selftest_lpt.py`; both
  modules refuse `--selftest`. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `zero-sum-curriculum-null/` — A delivered null construction
  (`NULL_CONSTRUCTION.md`, verbatim, trailing `g4` included): five
  conditions under which a zero-sum curriculum could NOT have affected
  the incident's outcomes, each with requires / test / status, and a
  RESULT. `null_construction.py` parses the delivered text and computes
  what its prose asserts. **`ZSN_001`, one word:** the header reads
  *"each is a requirement"* (a conjunction, which empties the set at N1)
  and the RESULT reads *"survives on the two branches"* (a disjunction,
  {N2, N4}); computed both ways, the stated RESULT matches only the
  second — and the conjunction is unsatisfiable on the document's own
  terms, since N1 requires the curriculum *absent* and N2 requires it
  *present*. **`ZSN_002`:** the branches are not independent — N2
  (present, not activated) and N5 (vocabulary only) each leave the
  behaviour to be accounted for without the curriculum, which is N3's
  job, so with those two edges applied to a fixed point the null
  survives on **N4 alone**, and N2 carries only if N3's residual closes;
  N3 is PARTIAL by the document's own status. **`ZSN_003`:** N2's test
  has no outcome that carries the null by itself — equal probing across
  settings leaves the probing to N3, lower probing on possible tasks
  leaves *what was cued* to N3. **`ZSN_004`:** N2 is
  `hf-incident-extract`'s missing control arm and is built in its schema
  by import — two arms differing only in `source`, every cell
  UNMEASURED, `None` propagating, and on filled constructed arms the M1
  difference computes. **`ZSN_005`:** the three artifacts N5 names
  (*depth-stack instrument*, *sacrifice transcripts*, *the delay
  attempt*) are absent from this tree by content, this folder excluded
  from its own scan and a planted mention found; the sibling records the
  transcripts N5 reads as `NOT_RELEASED`. **`ZSN_008`:** writing this
  entry put two of those names into the tree and the next run reported
  them present — `UNI_010`'s loop through the index — so hits are split
  into an index column (the two root index files) and an independent
  column, absence read on the second and the first printed rather than
  excluded. **`ZSN_006`:** N3's status
  assigns the residual to the curriculum, which the test as written does
  not establish — an absence in one account recorded as a result for
  another. **`ZSN_007` UNVERIFIED:** nothing here bears on whether the
  curriculum affected anything. Check count printed by `selftest_nc.py`;
  the module refuses `--selftest`. Stdlib only, parses under 3.9, CC0.
- `readout-count/` — A pre-registered work order delivered verbatim
  (`WORK_ORDER.md`): does a safety regime's incident rate track the
  COUNT of operator positions with a protected channel that RETURNS,
  not its stated culture or its data volume (H1); a declared channel
  with no return contributes 0 (H2); builders cannot read their own
  intake (H3)? Built as **one stdlib file** computing what the
  procedure asks for from a flat CSV in its schema — readout_count as
  distinct returning positions, per-regime OUTPUT at the latest year,
  Spearman by hand for H1, Cramér's V imported from
  `label-position-test` for P4, a median-split comparison for H2 — with
  the order's own falsification lines applied and `undetermined` or
  `NOT_COMPUTABLE` printed where they cannot run. **No data ships.**
  **`RC_002`:** the order's five SEED ROWS are read back from the order
  itself and **0 of 5 count by its own rule** — none carries a URL, the
  intake cells are `high` / `med` / `3+` / `2` / `—` where the schema
  wants integers, and one trend cell of five is in vocabulary; the
  instrument reports each cell as what it is and fills nothing in.
  **`RC_003`:** H1's *"rank matches"* has no strict reading past three
  regimes — a three-level trend carries ties that a count need not, so
  on a constructed world where the count tracks the trend as well as a
  count can (rho 0.949) strict equality still returns *does not match*;
  the verdict runs on rho with the threshold declared `[CHOICE 3]`.
  **`RC_004`:** H3's falsifier conditions on acted-on counts split by
  origin and on a grading field, and the schema carries neither —
  `NOT_COMPUTABLE` with both absences named, the eighth stated-rule-
  with-no-field instance. **`RC_005`:** a count at raw values has as
  many levels as distinct values, so P4's V reads 1.000 by construction
  on four regimes with four intake counts; the level count is printed
  beside every V and no bin is chosen. **`RC_006`:** H2 is in the
  definition of readout_count and cannot be tested by it; its own
  falsifier is a different comparison, which `h2()` computes.
  **`RC_007`:** the schema's two grains (regime-year, incident) share
  one row shape with no field saying which. **`RC_008`:** the order's
  first paragraph makes every party that builds or audits a row, the
  drafting model included; the render says so above the numbers and the
  *this session* row's dashes are left as delivered. **`RC_009`
  UNVERIFIED.** Four `[CHOICE]`s printed on every render; renders screen
  clean with no exemption; no author section. **The first filled row
  then landed** (`TRUCKING_ROW_v0_1.md`, verbatim): sourced, coding
  rule stated, its own v0 corrected in a logged changelog — the channel
  that exists is a *complaint* channel, not a *readout* channel, and the
  count is 0.5. `row_audit.py` reads it against the instrument.
  **`RC_010`:** the rule has three conjuncts and the schema carries a
  field for two; NON-ADVERSARIAL has none, and the row's own `type`
  column (complaint / inspection / enforcement / readout / remedy) is the
  missing field — the distinction the row says it *actually measures* is
  the one column its parent schema cannot record. **`RC_011`:** the 0.5
  is a per-position PARTIAL return weighted at one half, computed here
  from the row's own layers table (strict 0.0, half 0.5); the schema's
  `positions_returning` is a list, so the row loads at readout_count 1
  and never 0.5. **`RC_012`:** the row as delivered is refused on
  `rate_trend`, the cell its own STILL NEEDED list opens with — the seed's
  `up since 2010` withdrawn to a requirement, the right direction, and
  one cell short of loading. **`RC_013`:** "every claim carries a source
  URL" holds for 5 of 7 entries and the trucking count rests on one of
  the two the document defers itself; the four hosts with URLs refused
  CONNECT once each, recorded not read. **`RC_014`:** the row's "(N4)"
  points at nothing in the parent order (ids H0–H3, P1–P6).
  **`RC_015`:** the seed's `3+` intake cell is the complaint count under
  v0.1's renaming. **`RC_016`:** the layers table counts rows and the
  complaint count counts routes. **The exclusion stack then landed**
  (`EXCLUSION_STACK_trucking.md`, verbatim): twelve filters between a
  held readout and the record, coded by mechanism, survival
  multiplicative, every rate unmeasured. `stack_audit.py` reads it
  against the row, the order, the schema and the `uninstrumented`
  register by import. **`RC_017`, the one that lands on the parent
  order:** P2 defines RETURN as *a reply, a corrective action, a report
  entering a held record* — three disjuncts, any one sufficient — and
  L11 shows a private settlement is the second without the third
  (*publishes nothing*; *the condition does not enter any safety
  dataset*), so a settlement-only channel counts as returning under P2
  and delivers nothing to the record the count measures; the stack's
  closing sentence is P2 with the disjunction removed, and the schema
  has no field for which disjunct fired. **`RC_018`:** the arithmetic
  reproduces from its own figures (183+32+59 = 274; percentages sum to
  101 by rounding, merit 22 in L8 and 21 in L10 both from 21.5; 0.5^11
  = 1/2048). **`RC_019`:** survival over twelve layers with zero
  measured rates is None, never 1.0 by default. **`RC_020`:** the row's
  phantom "(N4)" resolves forward — S4 here is the survey the row named
  in the same words, and the row still says N4. **`RC_021`:** L0 is the
  row's six-item list, item for item. **`RC_022`:** L0 reads as
  MODALITY, L2 as PROXY SUBSTITUTION, L5 partially as AUDIT ASYMMETRY,
  and **L11 fits none of the eight** — nearest is `observer-exclusion`'s
  classification-note candidate. All seven source hosts refused CONNECT,
  recorded not read. **The stack's revision then landed**
  (`EXCLUSION_STACK_trucking_v2.md`, verbatim beside v1): L4 gains the
  stack's first per-layer falsifier — a syllabus search with both arms
  of the prediction and *if present in operator-side training, this
  layer is refuted*, on evidence declared as one operator's training
  stack (`RC_024`) — plus an ACCRETED, NOT ENGINEERED section and S6/S7.
  `stack_revision.py`: **`RC_023`** three pure insertions, 68 lines,
  nothing removed, v1 reassembled byte-for-byte, CHANGELOG unmoved;
  **`RC_025`** the four counts the revision reduces "safety culture" to
  (*who holds, who returns, who is immune, who publishes*) have schema
  fields for three and **none for publishes** — `RC_017`'s missing
  disjunct from the revision's own summary; **`RC_026`** *not fixable
  layer by layer* is the stack's own multiplication stated (twelve at
  0.5 → 1/4096, remove one → 1/2048, one dominant filter at 0.05 buys
  twenty-fold and is still at 1/2048); **`RC_027`** of S1..S7 one fills
  schema columns (S5 → intake_count / return_count per regime-year) and
  six name layers the schema has no column for. Check count printed by
  `selftest_rc.py`; all four modules refuse `--selftest`. Stdlib only,
  parses under 3.9, phone-buildable, CC0.
- `removal-closure/` — A pre-registered work order delivered verbatim
  (`WORK_ORDER.md`) about a METHOD — how claims of coupling between an
  environmental constant and a biological rhythm reach closure, and
  whether removability predicts time-to-closure — with no mechanism
  proposed and no coupling asserted. **`removal_closure.py`** is the
  main-table instrument: years to closure, the three falsification
  rules with `undetermined` where they cannot run, Cramér's V imported
  from `label-position-test`, Spearman imported from `readout-count`,
  and a **pre-registration hash** over the removability coding that is
  stable under closure-year edits and moves under a recode (`RMC_005`).
  **No data ships**: the five seed rows are read back from the order and
  **0 of 5 count by its own rule** — three step cells are ranges and two
  year cells are decades where the schema wants one value (`RMC_002`) —
  and their years-to-closure column, recomputed from their own year
  cells with a decade read as a range, comes back consistent to within
  the `~` it carries (`RMC_003`, a clean check recorded because it is the
  only check possible without a literature). **`RMC_004`:** H2 ranks
  time-to-closure, which exists only for closed rows, and the open rows
  it drops are exactly where the order says the low-removability
  constants sit; a censored reading with open rows at
  `CURRENT_YEAR − first_correlation_year` is printed beside it and
  neither is picked. **`rhythm_gaps.py` runs the attached gaps, and the
  dataset was reachable — the first in this drop family** (`RMC_006`):
  the repository is on `github.com`, cloned at `b174bd64afba`, not
  checked in, size and sha256 printed on every render, headline numbers
  pinned by the selftest when the file is present. **`RMC_007`, G2
  run:** the upstream split applies no minimum pause (shortest trailing
  pause in the table 0.001 s), and re-merged at the order's thresholds
  the analysed unit's mean moves **2.257 → 3.531 s** (×1.56) from t = 0
  to 0.50 s — the direction is fixed by construction and asserted, the
  size is the measurement, and what the t = 0 figure describes is the
  annotation's pause convention upstream of the repository.
  **`RMC_008`, G3 run:** right-tail ratio (p95 − median)/(median − p05)
  exceeds 1 in **49 of 49 languages** on the analysed unit (1.46–2.64)
  and on the speech run (2.10–3.41), CV 0.42–0.63 and 0.51–0.78 — the
  first of the order's two stated shapes in every language, stated as a
  property of the file under the statistics and not as what produces
  it. **`RMC_009`:** G4 needs word-level intervals the repository does
  not carry (its first script reads them from an external path and
  writes only the units), G5 needs a country join the repository does
  by geocoding, G1/G6/G7 are reading questions and G7's number is
  arithmetic (1 / 2.020 s = 0.495 Hz). **`RMC_010`:** two numbers the
  upstream script states in comments (1.43 / 0.83) reproduce from the
  table (1.430 / 0.827). **`RMC_011` UNVERIFIED:** nothing bears on H1–H3
  and nothing asserts or denies a coupling. Four `[CHOICE]`s printed;
  renders screen clean with no exemption; no author section. Check
  count printed by `selftest_rmc.py`; both instruments refuse
  `--selftest`. Stdlib only, parses under 3.9, phone-buildable, CC0.
- `encoding-selection/` — A pre-registered work order delivered verbatim
  (`WORK_ORDER.md`), from a failed n=1: one finding encoded five ways, a
  reader asked to rank by arrival cost, and the reader declining —
  *"each carries different information"*. Is an encoding an INSTRUMENT
  SELECTION rather than a style, so encodings of one content are not
  rank-orderable on one axis (H1); does recovered quantity track the
  format, not the reader (H2); does prose hide which axes were dropped
  where a table shows them (H3)? Built as **one stdlib file** — Kendall's
  W by hand against a permutation null, within- against between-format
  spread of the recovered-quantity set as mean pairwise Jaccard
  distance, prose against a declared table class — with the order's own
  falsification lines applied and `undetermined` printed where they
  cannot run. **No data ships and the seven encodings are not here**:
  they are the experimental material, the order calls them a judgment
  call to be published verbatim, and authoring them would put the
  instrument's author in the sample the order excludes; the instrument
  validates an encodings file against each item's fact list and
  **refuses an added fact** (`ES_006`). **`ES_005`:** both seed items
  are this repository's own artifacts — M1 is `hf-incident-extract`'s
  explore ratio, M2 is `readout-count`'s trucking seed row — so any
  reader of the repository, the drafting model included, already holds
  them against the order's own MATERIAL condition; and M2 states *three
  declared channels, zero returns*, the reading `TRUCKING_ROW_v0_1.md`
  withdrew on the order's own date. **`ES_002`/`ES_003`/`ES_004`:**
  *"W above chance"* has no chance in the order (a permutation null,
  `[CHOICE 1]`), *"variance"* of a set-valued field has no value until a
  distance is chosen (`[CHOICE 2]`, and the vocabulary's `other` is one
  bit), and *"table readers"* names a kind not a format (`[CHOICE 3]`,
  every format's rate printed). **`ES_007`, found by running:** a
  decline is a third state beside a ranking and a between-subjects
  blank, printed as a rate beside W and never subtracted — and the first
  build counted declines per row, six for a reader who declined once,
  caught by the constructed world and recorded. **`ES_008`:** F7 is each
  reader's own encoding and cannot enter a pooled W; rankers over
  different format sets are refused with the sets named. **`ES_009`
  UNVERIFIED.** Four `[CHOICE]`s printed; renders screen clean with no
  exemption; no author section. Check count printed by
  `selftest_es.py`; the instrument refuses `--selftest`. Stdlib only,
  parses under 3.9, phone-buildable, CC0.
- `claim-refusal-gap/` — A delivered gap document (`GAP.md`, verbatim):
  claim refusal in insurance adjudication is measured only where it is
  contested — accepted-side measurement, the refused side uncounted or
  counted on a self-selected sample. Seven gaps, five experiment
  designs, a standing shape. `gap_audit.py` reads it as a structure and
  computes what its prose asserts from the figures it carries, none
  checked against a source (zero URLs; seven sources named in prose;
  allowlist egress). **`CRG_001`:** the anchor's +10 is 45 minus a ~35;
  a tilde read as ±2 makes the held-constant residual **+4..+16**, so the
  direction holds and the magnitude is what the tilde carries.
  **`CRG_002`:** G-2's estimator returns one number for two causes as
  arithmetic — a displacement world and a non-purchase world are the same
  pair (U+d, B−d) — and "BI rose, ratio rose anyway" is the
  log-derivative (BI +10% and ratio +10% needs UM +21%). **`CRG_003`:**
  G-3's four rebase deltas reproduce, the mean seam is 1.45, and 2023
  restated is 16.9 against 1993's 16.0, so the "record" flips with the
  basis and E-5 is the seam measured. **`CRG_004`:** litigation +8
  against CWP +10 bounds the netted move in [2, 10]. **`CRG_005`:** G-5's
  "~100x" is 1/appeal_rate exactly, and the unappealed wrongful rate is
  None until E-1 runs — a default of 0 would be the "selective on merit"
  reading assumed rather than measured. **`CRG_006`:** "no benign
  reading" for overturn 38 → 52.5 at flat appeals has a second reading —
  the review standard moved, `criteria-drift`'s ruler — and E-1's blind
  reviewers on policy language are what separate them; the sentence
  overstates and the design beneath it does not. **`CRG_007`:** G-6's
  pre-instrument point is 0/0 and the instrument returns None, never
  zero. **`CRG_008`:** G-6 and G-7 have no design; G-6 says why. **`CRG_009`:**
  against the register's eight by import, G-4 BUDGET BOUNDARY and G-7
  AUDIT ASYMMETRY fit, G-1 and G-3 partially, and G-2 is
  `category-weld`'s ninth (two causes welded into one ratio), G-5 the
  document's own standing shape (selected on the variable), G-6 an
  absent state. **`CRG_010` UNVERIFIED.** One declared `no_severity`
  exemption (`error`, inside the delivered G-5 title) under the
  three-arm harness. Check count printed by `selftest_crg.py`; the
  module refuses `--selftest`. Stdlib only, parses under 3.9, CC0.
- `thermal-coupling/` — Two delivered MARKER modules landed verbatim and
  never edited: `thermal_coupling.py` (temperature entering a slope/flow
  hazard chain at five lag classes, a product-form coincidence term,
  claims TC-01..TC-06 under *update the claim, never retune*) and
  `airblast_extension.py` (three corrections forced by the Langtang 2015
  reconstruction — air temperature as the driver, an air-blast term, a
  diurnal lag class — claims TC-07..TC-11). `coupling_audit.py` imports
  both and checks them against their own docstrings, claim tables and
  demos. **`TCA_002`, the sharp one: TC-04 is refuted by its own
  function.** The claim's criterion is *sensitivity rises as temperature
  approaches melting*; the implemented loss is `0.71·x^0.55`, concave, so
  the strength derivative is −0.155 /K at −9.5 C and −0.042 /K at −1 C —
  sensitivity **falls** toward 0 C by 3.7× — while the inline comment
  reads *"convex: steeper near 0"*; `creep_sensitivity` is the shape the
  docstring describes and the strength function is not. **`TCA_001`:**
  the CAL_FOS calibration sentence (50° slope crosses FoS = 1 at −2 C)
  holds at −1.99 C under `fracture_favorable=True`, which it does not
  name, and never crosses under the default. **`TCA_003`:** *"CAL_FOS is
  the ONLY free parameter"* against an AST census of **35** numeric
  literals in function bodies, seven functions carrying literals with no
  source in their docstring. **`TCA_006`:** TC-03's freeze-thaw half is
  produced (interior peaks at ±3, a dip at 0) and its snow half is a
  docstring — `depth_m` is an input, never assigned, and
  `weak_layer_index` is temperature-independent at fixed gradient.
  **`TCA_007`:** on a snow-temperature sweep the count falls while the
  runout multiplier rises (TC-06's mechanism), and coincidence tracks the
  count because the multiplier is read by no downstream term.
  **`TCA_009`:** the extension's `meltwater_index` is linear in
  `(t_air + 5)`, so its 19 C / −1 C ratio is **6.00 by construction**
  where the docstring says *calibrated to 2.3×* — and its own demo prints
  both on one row. **`TCA_010`:** the coupling bounds reproduce
  (8.9–18.4) and the blast anchors do not (13.0 against >15, 3.9 against
  2.5). **`TCA_011`:** the extension *"extends, does not replace"* and
  imports nothing — it re-declares LAG with the core's five classes
  identical today (a copy, `MF_019`), reads none of the core's terms, and
  TC-10's lateral/longitudinal split is in no function. **`TCA_008`:** the
  stated home folder `earth-systems-physics` does not exist, and
  `rate-mismatch-polytope` — cited by thirteen other files, existing
  nowhere — reaches its most-cited. **`TCA_013` UNVERIFIED:** every anchor
  is carried and unchecked. **The extension's revision then landed**
  (`airblast_extension_v2.py`, verbatim beside v1, with the core
  re-delivered): **`TCA_014`** one function changed, `meltwater_index`,
  everything else byte-for-byte v1; **`TCA_015`** the calibration
  sentence is now produced by the function — 1 + 0.0649 × 20 = 2.30, the
  0.0649 being 4,800/74,000 — and the docstring records the first
  attempt's 6.0 and its 2.6× factor, `TCA_009` reached from the author's
  side; **`TCA_016`** the correction removed v1's zero clamp, so the index
  goes negative below −16.4 C; **`TCA_017`** the re-delivered core is
  byte-identical to the repo copy, so TC-04's function is unchanged and
  `TCA_002` stands — the revision answered the extension's calibration
  finding and not the core's shape finding; **`TCA_018`** v2 still imports
  nothing and reads no runout. **`TCA_019`, a placement decision:**
  `PLACEMENT.md` landed verbatim — the two scripts stay their own module
  rather than attaching to a cascade chain, on two grounds (the mapping
  domain is the valley cross-section including the counter-slope, since
  the Langtang air blast landed 550 m up the *opposite* mountain off any
  runout path; and a product over lag classes is not a stage in a
  sequence). In this repository the module already stands alone as
  `thermal-coupling/`, so the decision is honoured by construction and
  nothing merges. The doc restates *"one free parameter, CAL_FOS 2.825"*
  — the same single-free-parameter claim `TCA_003` refuted by an AST
  census of 35 numeric literals (CAL_FOS = 2.825 reproduces at line 111;
  the ONLY-free-parameter comment is line 115) — recorded so the doc is
  not read past `TCA_003`; the decision record is not edited. Check count
  printed by `selftest_tca.py`; the audit refuses `--selftest`. Stdlib
  only, parses under 3.9, CC0.
- `ch4-four-box/` — Two delivered scripts landed verbatim:
  `fourbox_forward.py` rebuilds a four-box CH4 model forward-only
  (E = M·C from prescribed concentrations, no inversion) and prints the
  published emissions beside two readings of the transport parameters —
  as exchange TIMES and as exchange RATES — plus a consistency scan;
  `closure_diagnostic.py` takes the reading that fits and asks what
  concentrations reproduce the published +SCA run. `fourbox_audit.py`
  runs both with their prints captured and reads them against each
  other, copying nothing. **`FB_002`:** the RATES reading reproduces the
  published polar-only emissions to within 4.2 Tg/yr per box; the TIMES
  reading misses by 47.7 and produces a negative southern source.
  **`FB_003`:** the two scripts' matrices agree to 2e-16, so the
  diagnostic runs on the forward model's own operator. **`FB_004`:**
  with the tropical box at the SCA value and the southern box at WAIS
  the forward model returns E_SH = −10.8 against a published +10; the
  diagnostic's closure gap is **59.3 ppb** above WAIS, and a prescribed
  concentration and a prescribed source cannot both hold in a forward
  model. **`FB_005`, read across the two pages the scripts print apart:**
  the consistency scan reaches the observed 48 ppb gradient at 4.34× the
  times base, while the rates reading is 20.66× that base and yields
  **150.5 ppb, 3.1× the observed** — the transport that fits the
  emissions is not the transport that fits the gradient. **`FB_001`:**
  every constant identity holds (IPD 48, both SCA offsets, TS = 213−88,
  A = 0.765, per-box Tg/ppb exactly a quarter of the global 2.848).
  **`FB_006`:** two known answers on the operator pass (no transport
  gives E = C/τ; a uniform concentration moves nothing). **`FB_007`
  UNVERIFIED:** Lamantia et al. 2026 is named and not read; nothing is a
  statement about the atmosphere. Check count printed by
  `selftest_fb.py`; the audit refuses `--selftest`. Stdlib only, parses
  under 3.9, CC0. **A steady-state reproduction then landed**
  (`RESULTS.md`, delivered verbatim) under the split rule *a finding
  demonstrated from the published Methods folds into RESULTS; one that
  needs the Zenodo code stays OPEN* — **two fold in, one stays out**, and
  the two are built as `units_test.py` and `tn_inversion.py` (each
  reproduces from the forward model via captured-stdout `runpy`, asserts
  on plain invocation, refuses `--selftest`). **R-2:** the Methods label
  the transport parameters "exchange rates of 0.22/0.45/0.45 **years**",
  and read as TIMES the southern source goes **negative** (−5.97) while
  read as RATES (1/yr) the baseline reproduces (tropics 163.06) — a sign
  error settles the units question from the published values alone, no
  archive. **R-3:** inverting the +SCA run for the published TN of 88
  Tg/yr requires **C_TN = 733 ppb**, *above* both polar records and 13
  under SCA, so a +49 ppb concentration move shows in the emission column
  as only +6 Tg/yr — the 6-yr lifetime scales loss with concentration and
  the column compresses how far the unseen box moves, the siting-bias
  shape inside the paper's own accounting, making the effect *larger* in
  concentration space than the table shows. **FINDING 3 stays OPEN, not
  cited as a discrepancy**: the E_SH = −10.8 residual against a hard-fixed
  +10 could be produced by the steady-state/transient difference, which is
  not separable without the archived code — a residual in a reduced model,
  and the reduction is ours. Both scripts assert clean and are covered by
  `selftest_fb.py`; NEEM and Law Dome are named in the delivered spec but
  not in the model's constants and are not supplied from memory.
- `cooperative-substrate/` — A work order delivered verbatim and built to
  it: four checks, each one stdlib file under 300 lines, independently
  runnable, no network at runtime, with the order's framing claim and
  one-scale-up note carried verbatim in the README as it asks. **P1**
  extracts dependency records from methods sections by a pattern set
  held in one dict, `verified_in_argument` false unless the same
  sentence carries a verification verb, the ratio `undefined` at zero
  argued; **P2** is a contract ledger over every call site read with
  `ast` and `dis` — one function-call record per site, a second layer
  where the callee is an allocator, a numeric routine or a transport
  module, one compile-layer record per code object — printing
  `unverified_contracts / total_callsites` and the counter-list; **P3**
  profiles one term per source (window ±8), takes the mean pairwise
  cosine and builds the sense-shuffled null in the same script; **P4**
  is the step-contest chain as a reflecting random walk with its exact
  position distribution computed beside the simulation on every row.
  No published methods section is reachable and none is invented; the
  fixtures are constructed and say so in their first line. **`CSP_006`,
  the finding: P3's reading is a property of the TERM, not the corpus.**
  On the same sixteen files of `uninstrumented/cases/`, `mechanism` and
  `confidence` clear the null by 9.6 and 12.8 sd while `instrument` and
  `claim` sit on it (0.0 and 0.5); on the whole tree with this folder
  and the two root index files left out, the order's own example
  `mass` clears by 6.3 sd over 20 sources (`CSP_013`: with the index in,
  the number moved 9.9 → 8.5 → 7.3 across runs in which only the index
  paragraph and then this folder's own claim table quoting the result
  changed — `UNI_010`'s loop through the index, both readings printed
  and the independent one quoted)
  — the terms that clear are used in a fixed schema slot,
  the ones that do not are used in free prose, and `instrument` is the
  word this tree uses in the most senses. **`CSP_007`: the order's third
  row and its falsifier land on one cell** — a constructed corpus using
  `mass` in four disjoint vocabularies reads 0.0000 against a null of
  0.0000 with the gap undefined, so "not a corpus; noise" reads as
  *indistinguishable from the null*, the falsifier's own condition, and
  comprehensibility has to be established outside the profile (the
  same-sense corpus reads 1.0 against 0.87, so the instrument is not
  `CONSTANT_SILENT`). **`CSP_008`:** that corpus caught a leak in the
  null — the stand-in's profile carried the original term, shared by
  every source, lifting the null to 0.098 on a corpus where both sides
  are 0 by construction; repaired with an `exclude`, real-corpus nulls
  moved under 0.003, recorded because the leak ran toward making the
  falsifier fire. **`CSP_003`:** P1's pattern set over five in-tree
  documents that are not methods sections emits 8 records, 0 argued,
  and **0 of 8 are dependencies by hand reading** (`Aug 2026` as a prior
  result, `closure` as a supplied material) — precision fails on prose
  outside the register, so a `--report` cannot be read without the
  records beside it. **`CSP_004`:** P2's verified proxy reads a call
  inside try/except as verified while a try/except catches a raised
  failure and verifies no returned type, so the unverified count is a
  floor; 0 of 4 shipped checks verify every contract, and the order's
  ratio exceeds 1 on every file because layers stack (`CSP_005`, with
  the ast and bytecode call counts disagreeing on every file over
  comprehensions, printed beside each other). **`CSP_009`/`CSP_010`:**
  P4 confirms its own construction — exact termination non-increasing
  in `p_contest`, exactly N steps at 0, N² = 2500 unbounded at 0.5,
  6790× growth between 0.55 and 0.60, every simulated row within 1.5
  binomial se of exact — and "falls to zero" is relative to the budget
  (N = 10, p = 0.6: 0.125 at 10N, 1.000 at 2000N), while "no answer, not
  a degraded one" is what a one-integer state can express rather than
  a result. **`CSP_011` UNVERIFIED:** the multi-agent note is carried
  and checked against nothing, and the framing claim's share has no
  instrument among the four parts. One declared `no_severity` exemption
  (`corrupt`, inside the order's contract text); a moral-token list
  fires once on `kind` in the type sense, recorded rather than renamed.
  **An evidence pack then arrived** (`EVIDENCE_PACK.md`, verbatim, after
  the deliverable) carrying its own verification status on every row —
  retrieved from search-result text, not read, 33 `[UNVERIFIED-FULLTEXT]`
  and 1 `[DISPUTED]` — and nothing in it was opened, the three citation
  hosts refusing CONNECT; what is computable without opening anything
  was computed (`evidence_audit.py`, `scope_test.py`, `term_table.py`).
  **`CSP_015`:** the E8 scope test's five rows carry two distinct
  condition vectors, so every condition separates alone and none is
  necessary — `MD_008`'s collinearity, n = 5 on one distinction, the
  conjunction untested; one constructed off-diagonal row makes C2
  necessary. **`CSP_016`:** E0.1's stress axis and E8's design axis are
  both recorded on one row of five and disagree there — the E. coli
  construct is scored under stepwise antibiotic, harsh, so E0.1 predicts
  facilitation, the design axis predicts competition, and competition
  is what was reported; the design axis carries the row, which supports
  E4 and removes E0.1 as a prediction for the row it is used on.
  "Benign" as E0.1 uses it has no axis of its own; the test the pack's
  last line asks for is stated as a removal test and NOT RUN.
  **`CSP_017`:** E3.3 enters competitive goal structure as a measured
  variable and the E8 row enters the same games as a class all-y.
  **`CSP_018`:** E2.6 states as a measurement what `label-position-test`
  holds UNVERIFIED, with no locator; in-class for this audit, not
  adjudicated. **`CSP_019`:** the E7 table is built as a schema — 25
  cells, 2 filled from the pack's own worked example, 0 quantitative
  predictions, which on the pack's own discriminator is the state before
  a shared structure is shown. **`CSP_014`:** 15 of 34 rows carry no
  locator beyond an author-year or a name, among them every row the
  pack leans on for P1 and P4. **A v2 work order then arrived**
  (`WORK_ORDER_V2.md`, verbatim beside v1), renaming the parts, adding
  P5 (a lag-declaration check) and §3 (the C1–C4 scope conditions with
  a null to build), and binding a §6 non-goal against any author or
  values-advocacy section; the build lands in `v2/`. **`CSP_021`, the
  sharp one: the one code file the delivery put on disk, `v2/p4_goal.py`,
  arrived truncated** — 1282 bytes, cut mid-line at `stance, used, value
  = "accept", pr`; it ends on a syntactically complete line so it
  parses, and the truncation is read structurally (run() has no return,
  no `__main__` guard, only one of the three stances its docstring
  names, and a last line binding `pr`, a name never assigned) — left as
  delivered, not completed. **`CSP_022`:** the manifest's ten files map
  to 1 delivered-truncated, 5 renaming v1 files (not rebuilt, `MF_019`),
  1 new (`p5_lag.py`), 1 seeded (`scope_check.py`, importing the E8
  reader), 1 declined (a first-party `CS_` thesis `CLAIMS.md`, per §6)
  and `EVIDENCE.md` = the existing pack. **`CSP_023`:** `scope_check`'s
  §3 null is met by the seed's own E. coli row (harsh, all C1–C4,
  competition reported) and then unmet by it, since that row's harshness
  IS the antibiotic it is scored under — the C2/C3 apparatus — so
  `UNRESOLVED_HARSHNESS_ENTANGLED`, needing a case with independent
  environmental harshness the seed lacks (`CSP_016` from the other
  side). **`CSP_024`:** P5's gate carries the "silence is not safety"
  third state by construction — an undeclared `t_visible` gives an
  *undefined* ratio (`UNDECLARED`), never a small one; the antibiotic
  anchor reads 101.5 → DECLARED_UNKNOWN, a same-window action 0.2 →
  TRACKED, the ≥10 gate a `G-RES` pair cross-linking `claim-record`'s
  clock. **`CSP_025`:** the v2 P4 reframe (self-check trace table, the
  cut being error-correction that terminates vs contestation that does
  not) is a different instrument from v1's random walk, which has no
  three-stance model and cannot express the cut; the delivered file
  names it and is truncated before implementing it. **`CSP_026`
  UNVERIFIED:** the null over real literature is not runnable (egress),
  and the §6 scan is clean over the deliverables with the scanner's own
  keyword-defining file excluded (`UNI_009`). Twenty-six `CSP_*` claims;
  61 + 33 + selftest_v2 checks. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `envelope-asymmetry/` — A protocol delivered verbatim, the compressed
  restatement it ends with included: does envelope discipline — operating
  range, out-of-scope declaration, degradation mode, revalidation
  trigger, quantified margin, named responsible party, coded 0/1 and
  summed — track the host domain's return channel rather than liability,
  field prestige or AI regulation itself? Two tests (within-vendor
  paired across host domains, n ≥ 30; between arms inside one filing
  regime, n ≥ 50) and four named threats. `envelope_score.py` is the
  instrument and both tests from a JSONL in the protocol's schema,
  with kappa imported from `effective-redundancy-audit` and OLS from
  `sim-span`; `domains.json` pre-registers the T4 domain list with its
  hash on every render. **No document is coded**: no vendor site or
  filing registry answers (the registry host probed once), no row is
  invented, and with no rows the gate refuses before either test runs.
  **`ENV_002`, the sharp one: the 0.7 gate is underspecified twice.** On
  a constructed 20-document double coding with one E6 disagreement,
  **E6's kappa is 0.0** while the pooled gate passes on both statistics
  (percent 0.992, kappa 0.969) — the marker carrying test 1's SPLIT
  reading can have zero reliability and the instrument proceeds; and an
  all-absent double coding passes at kappa 1.0 having never coded a
  marker present, `CONSTANT_SILENT` at the gate. **`ENV_003`:** T2's two
  instructions — retain structurally absent pairs at score 0, and report
  the absence rate separately — return **opposite readings on one set of
  30 pairs** (all pairs: mean difference 1.0, SPLIT; documents only: 0.0,
  KILL), so the verdict is the accounting and both are printed.
  **`ENV_004`:** "E6 flat" has two values and the split reading fits
  flat-at-0 only. **`ENV_005`:** the per-1000-words secondary outcome
  ranks a 60-word document above a 3000-word one the primary ranks below
  it — a capped numerator over an uncapped denominator. **`ENV_006`:**
  the template kill is a property of one filing record (zero variance at
  n = 2 as at n = 100), readable before sampling. **`ENV_007`:** five of
  six markers already have a field in `claim-record` (E1 →
  `domain_of_validity`, E4 → `clock`, E5 → `measurement`) and **E6, the
  named responsible party, has none** — the tree's own record schema is
  an envelope instrument minus the signature, on the axis the protocol
  says is liability's. **`ENV_008`:** the compressed restatement drops
  nine of ten probed elements (every threat, the re-target, the record
  schema, sections 4 and 5), keeping the inter-rater rule. **`ENV_009`:**
  arm A's "return channel" is `readout-count`'s `positions_returning`,
  so T4's gradient is that count as predictor. **`ENV_010` UNVERIFIED.**
  34 selftest checks. Stdlib only, parses under 3.9, phone-buildable,
  CC0.
- `dependency-survey/` — A work order delivered verbatim and built to
  it: a fixed five-term set (cost asymmetry / whether the aggregate
  steers / the accounting boundary / whether a legitimate other is
  representable / whether the accounting stance destroys its own
  measurement) applied across five substrates (foraging, multiagent
  harnesses, human mutual aid, ethics claims, nation-state sovereignty),
  25 cells, to locate terms MEASURED in one substrate and MISSING in
  another. It is the E7 cross-substrate table of `cooperative-substrate/`
  (`CSP_019`) made runnable, with the **load-bearing units rule
  enforced**: a cell coded MEASURED or SCOPE-DIFFERENT whose MEASURED_AS
  states no units is INVALID and cannot seed a gap as the measured side
  (`has_units`, `DS_001`) — what keeps the table from becoming a
  vocabulary map. The cell store is `CELLS.md`, human-editable and
  parsed by `survey.py`, so a cell recodes without touching code.
  **`DS_002`, the sharp one: the seed fails the survey's own
  admissibility bar** — `T3 x S5` is SCOPE-DIFFERENT with a scope note
  and no admissibility fields; the instrument caught its own work order
  on first run, and **`ADDENDUM_01` rescopes rather than patches**: a
  "measured, but the frame differs" status reports frame information,
  which is not in the quantity's units, so SCOPE-DIFFERENT now requires
  a SCOPE_TRANSFORM (`reference` / `maps_to` / `breaks_at`), not units.
  The seed still fails — prose note, no transform — and downgrades to
  UNKNOWN, counted apart from the never-coded UNKNOWN cells (`DS_008`);
  detected by the validator, left as delivered. The taxonomy test
  (frame / boundary / homonym) is OPEN and is itself a survey output, so
  no new module is built.
  **`DS_003`:** exactly one gap falls out — `T1` cost asymmetry MEASURED
  in foraging (J/s), MISSING in harnesses, PROVISIONAL and OPEN with the
  transfer question posed in the target's own units, `CSP_019`'s "experiment
  sitting there" with units on the measured side; NO-TRANSFER (the
  projected-frame result) and TRANSFER-STATED are reachable, so the gap
  list is not `CONSTANT_SILENT`. **`DS_004`:** 22 of 25 cells UNKNOWN,
  counted and listed and kept apart from MISSING (the absent-vs-known-
  negative repair). **`DS_005`:** the units check is lexical, stated at
  its callsite and null-tested both directions. **`DS_006`:** `T5` is
  `extraction-blindness-sim`'s stance-destroys-its-own-measurement
  mechanism named as a survey term. **`DS_007` UNVERIFIED:** nothing
  beyond the three seeds is coded, so the discriminator (real shared
  structure vs projected frame) cannot be applied here — it runs against
  transfer results and none exist; the survey is a store, not a
  conclusion, the order's own non-goal. **`ADDENDUM_02` then narrowed the
  units bar** (delivered verbatim; its own frame note: *narrow, not
  rescope* — contrast `DS_008`'s rescope): a units field naming a data
  **TYPE** (`boolean`, `verdict`, `integer`, `unitless`, `dimensionless`)
  with no **CUT** does not satisfy MEASURED, since a type carries no scale
  two coders can disagree about. **`DS_009`:** the instrument gains a
  second lexical arm (`names_type` ∧ ¬`has_cut` → inadmissible, downgraded
  to MISSING with a reason distinct from no-units, counted on its own
  `measured_type_only` line in the report, visible as a zero); a CUT is a
  comparison operator or a threshold/band/cut word and is **not** required
  to be numeric, so the addendum's own repair `float magnitude; cut at
  non-finite` passes while `boolean isfinite check per step` fails, and
  `dimensionless` alone now fails where the bare unit-word list passed it.
  The four FAIL and four PASS examples the addendum gives are null-tested
  both directions; `J/s` (no type word) is unaffected, so `DS_003`'s gap
  survives. **`DS_010` UNVERIFIED for the external corpus:** the RE-CODING
  scope is the 96 of 537 MEASURED cells in the Kimi falsifier survey Run 2,
  not held here; this repo's seed carries zero type-only cells, so the
  count is a visible zero and nothing here is re-coded, and nothing is
  fabricated to stand in for the external run. **`RESULT_taxonomy_-
  crossmodel.md` then settles half of the taxonomy question `DS_008`
  left open** (delivered verbatim; ADDENDUM 01 §2 held it OPEN because
  Runs 1 and 2 shared a system, so agreement could not tell *converged*
  from *remembered*). A **blind** Perplexity sort of the same 19 cells —
  no K-list, no repo access — against the Kimi sort **splits** the
  question. **`DS_013`: MEMBERSHIP replicated** (the two taxonomies are
  strictly nested, zero cross-cutting — every Perplexity group under
  exactly one Kimi kind, the proxy/wall-clock K3 core the strongest single
  result), so SCOPE-DIFFERENT is **SEVERAL**; the **count did not** (4
  Kimi kinds vs 11 Perplexity groups over 13 distinct, six singletons —
  near an identity map), so *how many* is grain-dependent and
  **UNSETTLED**; `K4` drew zero members under both sorters (a Run-1-only
  candidate artifact) and the straggler `G9`/F-TETRA-SCOPE is the record
  neither sorter could place and no field could name. **`DS_011`:** the
  strict-nesting headline is checkable here without the corpus —
  `taxonomy_replication.py` transcribes the delivered §1 map and verifies
  it is a FUNCTION (every group under exactly one kind), a
  **transcription-consistency check, not a reproduction of the sort**
  (the 19-cell corpus is external model output, not held here and not
  fabricated), null-tested against a constructed cross-cut. **`DS_012`:**
  §6's *report membership, not a kind count* is encoded as a refusal —
  `kind_count()` returns `UNSETTLED`, never an integer (the
  `domain-ledger` no-composite discipline applied to a kind count). All of
  §2–§5 (the K5 confirmed-at-record-not-as-a-kind reading, the
  over-split/over-merge signature, the literature audit's tag defect and
  the G2 EXACT→PARTIAL downgrade) is carried verbatim and not verified at
  record level. `DS_008`'s taxonomy status moves `OPEN` → `PARTLY SETTLED`
  (membership SEVERAL, count OPEN). **`RESULT_repair_adjacency.md` then
  adds a third system and resolves the character of the count**
  (delivered verbatim): DeepSeek sorts the same 19 records by *repair*
  into a 9-component adjacency graph, and the three groupings **do not
  conflict — they nest in one order**, `Kimi (4-5) ⊃ DeepSeek (9) ⊃
  Perplexity (11)`, zero cross-cutting (every DeepSeek component inside
  one Kimi kind, every Perplexity group inside one DeepSeek component).
  **`DS_014`: grain was never a disagreement — it is a cut height on a
  tree all three independently found** (class / operation /
  operation-plus-referent); `repair_adjacency.py` transcribes the §1–§3
  record-level memberships and verifies each link of the chain is a
  refinement (`perplexity_refines_deepseek`, `deepseek_refines_kimi`, both
  zero cross-cut, the 4 kinds covering all 9 components), a
  transcription-consistency check not a reproduction, null-tested against
  a component-spanning group. **`DS_015`:** the repair reading confirms
  `K4` **dead as a repair class** (its blind members scatter across three
  components — a second independent failure after both sorters gave it
  zero) and carries two Kimi edges flagged-not-dropped — `C7 → K3` a
  correction candidate (NLS-3 pulled from the speedup cluster by both
  external systems) and `C8 → K5` contestable (the T11 covariate). **`DS_016`:**
  the straggler `T13` (== the crossmodel `G9`) was placed by DeepSeek in
  C1 with the two-referent record — the one cross-cutting event — and is
  **not closed here**: one system, one placement, no argument, the
  document's own T13-reduces-to-TMP-2 test carried as the next step.
  **`DS_017`:** §6's refusal sharpens — `kind_count()` returns a
  **cut-height statement, never a bare integer** (*a single number is a
  cut, and a cut with no stated height is the thing the instrument exists
  to catch*), and §5's recurring three-system speedup collapse (Kimi alone
  reading the transforms, the ENG-3 sign inversion) and §7's not-tested
  list (asymmetric adjacency and CANNOT-FALSIFY both permitted and unused,
  the tree from one repair reading) are carried verbatim, not verified.
  **`ITEM4_ANALYSIS.md` decides the two decisive tests to the extent the
  evidence allows:** `DS_018` adopts the *separation* of NLS-3 from the
  speedup core (two independent sorts removed it — the two-system
  replication standard) while leaving its *target kind* UNVERIFIED (needs
  the record); `DS_019` argues the F-TETRA-SCOPE reduction to the
  two-referents shape and finds it PLAUSIBLE but **NOT closed**, since the
  RESULT's own next step is a second independent name-search that egress
  blocks and no field name is fabricated. Neither is forced closed on
  external data this repo does not hold. Nineteen `DS_*` claims
  (`ADDENDUM_01` a rescope, `ADDENDUM_02` a narrow, two RESULTs settling
  membership and then the character of the count, and item 4 decided as far
  as the evidence reaches). Stdlib only, parses under 3.9, phone-buildable,
  CC0.
- `railcar-containment/` — A delivered folder, complete and verbatim
  (`README.md`, `CLAIMS.md`, three screens, `run_all.py`, a params
  file): the e-mobility-fire-on-railcar problem built around one
  inequality, `t_available > t_required`, where the published
  measurement (FSRI 2026, carried at the README's own caveat) gives one
  side only. `tenability.py` is a well-mixed three-channel cabin model
  calibrated to published anchors; `t_hold.py` derives the containment
  hold-time requirement from line geometry under RUN and STOP egress
  policies; `detection_loop.py` is a latency Monte Carlo over sensor
  against visual detection. The README carries an envelope block and
  the folder its own claims (`RC_001..008`, not edited); the audit is
  `audit.py`, importing the screens and editing nothing, with
  `RCT_001..RCT_010`. **`RCT_002`, the sharp one: the thermal anchor is
  not reproduced and cannot be** — the docstring says every anchor is
  reproduced by construction, CO and visibility are, and the thermal
  channel lands at **272.5 s against 400 s**, because the anchor lies
  past the end of the source term (20 + 90 + 180 = 290 s), after which
  the cabin only cools; the bisection stops at the coefficient where the
  peak just touches the threshold, and two percent more volume makes the
  channel never cross. `t_available` at anchor (230 s, visibility) does
  not move, but the visibility anchor is itself a bound read as a point
  (`RCT_003`). **`RCT_004`:** the VALID FOR "sensitivity of `t_available`
  to car volume" has no single value — the local exponent runs 0.79 to
  2.23 across 60–320 m³ and the binding channel switches from visibility
  to CO dose at 200 m³; RC_001's sign holds, its magnitude is a regime.
  **`RCT_005`:** the two screens disagree on the containment form —
  `detection_loop.py` stretches the budget linearly, `tenability.py`
  with a finite source exceeds that by 1.2–1.34× and returns *never* at
  fractions 0.1 and 0.05 where the loop returns 2300 and 4600 s.
  **`RCT_006`:** RC_002's "containment dominates volume" holds at the
  fraction its own falsifier names (0.2 → 6.7×) and not at 0.5, where
  2.43× meets the volume step's 1.94×. **`RCT_007`:** `t_hold.py` applies
  a default 1.5× margin to every printed number where the README
  envelope says "none applied", and the README scores **4 of 6** on the
  sibling `envelope-asymmetry` instrument by import (E5, E6 absent).
  **`RCT_008`:** the params field `offgas_to_flame_s` is read by neither
  line of `t_hold.py`, so the two screens place the visual latency on
  different clocks. **`RCT_009`:** RC_005 is arithmetic — a 130 s sensor
  lead against a 728 s tunnel deficit before any detection — and swept
  over the egress mean the detection gain peaks at 240 s (+0.45), which
  is the folder's own station case and the claim's own falsifier.
  **`RCT_010` UNVERIFIED:** every FSRI figure is carried; nothing in the
  audit rests on one. **`FETCH_REQUIRED.md`** (delivered verbatim) is the
  tracked in-repo form of that hold: every landing-page/press-release
  number is `[FSRI-UNVERIFIED]` until the report is in hand, the figshare
  item refuses automated retrieval (a hand-fetch by the operator clears
  it), and the audit's `RCT_002..RCT_009` are the STRUCTURE-STABLE
  results §2 says survive without the report. 31 selftest checks. Stdlib
  only, parses under 3.9, phone-buildable, CC0.
- `falsifier-audit/` — A work order built to spec: walk a local checkout,
  pull every falsifier and its attachment context, and turn each place
  where a falsifier's **scope is implicit** into a research question. **Not
  a linter** — it grades no falsifier and emits no fixes; the premise is
  that a falsifier is itself a frame-bound claim, so where its scope is
  unstated the corpus holds more information than it states, and the output
  is additive (questions the repos do not already ask) not corrective.
  **Inventory first, per the order's first task:** `inventory.py` reports
  the marker forms actually present before the extractor is built around any
  of them — `REFUTATION_PROTOCOL` sections dominate (~110 files), then prose
  `Falsifier:`/`Falsified if:`, then claim-table columns under four header
  names (`falsifier`/`falsified by`/`falsified if`/`refuted by`) in no fixed
  position, then `falsifier_shape`/`falsifier_value` fields, JSON/YAML keys,
  and `FALSIFIER` block labels. `extract.py` resolves the falsifier and its
  claim by **header name**, not column position (`_header_index`), and
  builds records around the two forms carrying a locatable attached claim —
  the table column and the prose `Falsified if:` — counting the rest as a
  printed coverage statement, not a judgement. **Four checks, each
  independent, none aggregated into a score:** `A1`
  UNFALSIFIABLE-AS-WRITTEN fires when a falsifier states no number,
  comparison, unit, or observable-outcome word (the claim it guards is
  currently unguarded); `A2` CLAIM-TEST DRIFT fires (LOCATED records only)
  when fewer than a third [CHOICE 1] of the falsifier's load-bearing terms
  appear in the claim it tests, matched and unmatched terms shown so a human
  can dismiss cheaply; `A4` FIXED-REFERENCE-BODY fires on an undeclared
  reference body (`baseline`, `the null`, `chance`, `matched`, …) — the
  geocentric shape, where a falsifier can PASS while testing the wrong thing
  because the frame supplied the reference silently, so these are **rescope**
  candidates not narrow ones; and `A3` CROSS-REPO INCOMPATIBILITY, the
  order's highest-expected-yield check, indexes by **axis** not by rule or
  repo (`axes.py`; axes recur across the corpus, rule wordings do not) and
  looks within an axis for two folders carrying conflicting numeric cutoffs
  or opposite directions. **`A3` returns zero on this corpus**, and that is
  a result rather than a broken check: the numeric-bearing falsifiers on any
  shared axis are folder-local, so no two folders quantify one axis
  incompatibly — the same unquantified property `A1` flags from the other
  side — and the coverage note reports the zero rather than letting a silent
  `A3` read as a clean corpus. It is demonstrably **not** `CONSTANT_SILENT`:
  the null test builds a cross-repo pair carrying opposite directions on one
  axis and `A3` fires, then confirms it stays silent when both records are
  in one repo and when the two carry the same cutoff. On the tree: **301
  falsifiers found (289 LOCATED, 12 NOT-FOUND, 8 empty cells skipped), 283
  questions by A1/A2/A4** ({A1: 120, A2: 144, A4: 19}). `NOT-FOUND` (a
  locatable falsifier with no locatable claim) is a finding and is emitted,
  never dropped; an empty or punctuation-only falsifier cell is **skipped
  and counted**, kept apart from `NOT-FOUND`, since an absent falsifier and
  a present-but-unparsed one are different results. The queue is
  **append-stable** — re-running on an unchanged tree emits the same
  `repo:path:line` ids, so entries can be closed by hand in a separate file
  and survive the next run — and carries **questions only**, status `OPEN`
  the single machine-set value, enforced by the data structure
  (`per_record` returns a flat unaggregated list; the queue sorts by id, not
  by any hit count). The tool's own `QUEUE.md`, `samples/`, `README.md` and
  `AUDIT_NOTES.md` are self-excluded from the scan, because a re-run reading
  its emitted queue — or an authored doc that quotes a marker verbatim to
  document it — is the `UNI_010` self-reference loop; `WORK_ORDER.md`, the
  delivered spec, is left scannable and carries no attachable marker, so it
  produces no records, verified by the record count holding across its
  addition. Every emitted report is screened through
  `sheet-structure-scan/no_severity` (imported, not copied): the queue's
  authored framing — coverage lines, emitted questions, the `A3` note —
  screens clean, while the queue **body** does not, correctly, because it
  quotes corpus falsifier text verbatim (a corpus falsifier saying a value
  is *wrong* is the material under audit, not a severity label the tool
  authored), so the selftest screens the framing with the quote lines
  removed and separately checks the screen fires on a planted word. One
  authored word tripped the screen and was reworded (`fixes` → `repairs`).
  `A1`'s observable vocabulary was widened from ~52% to ~40% firing by
  **correctness** (the corpus uses gerund-and-verb observables the first
  word list omitted), not by tuning to a target rate. Findings are kept as
  prose in `AUDIT_NOTES.md` (`FA_001..008`) rather than a `CLAIM_TABLE.md`,
  because this folder's own scanner reads every `.md` for falsifier markers
  and a claim table carrying a `falsifier` column would enter its own
  corpus. 28 selftest checks. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `merge-path/` — A work order for a transform table between claim-record
  formats that already exist (nanopublications, ORKG, RO-Crate,
  ClinicalTrials.gov, CIPM/CMC, proof assistants, OSF prereg) and the
  repository's falsifier / branch-record format, with the loss in each
  direction **measured, not asserted**. **Explicitly not a new format**
  (§0: if the output is a format, the work failed — the failure mode of
  this space is an eighth standard); the unit of value is a TRANSFORM
  (`reference` / `maps_to` / `breaks_at`), and a registrar that does not
  merge is a valid outcome, a **NO-MERGE with a stated `breaks_at`** worth
  more than a forced mapping. **The egress fact sets the whole verification
  status:** §1's load-bearing first task is to *fetch each registrar's own
  specification* before mapping, and in this environment every registrar
  spec host answered **403 to CONNECT** (measured 2026-09-05T03:30Z;
  nanopub.net, clinicaltrials.gov, w3.org among them, logged in the proxy's
  `recentRelayFailures`) — so **no spec was fetched**, every real registrar
  is **UNVERIFIED** (`MRG_001`), its converter is NOT-IMPLEMENTED with that
  reason, and per §7 everything derived inherits UNVERIFIED. No spec field
  is transcribed from memory and none is fabricated; the docs
  (`UNITS.md`, `TRANSFORMS.md`) carry only the work order's own §1 candidate
  summaries, marked as such — the very summaries §1 says not to rely on.
  **What is delivered and verified is the machinery**, correct by
  construction on constructed data: a residual classifier over the two
  converters (`convert_out` OUT, `convert_in` IN) with four classes —
  **DROPPED** (no target slot), **FLATTENED** (dict→string, recoverable),
  **COERCED** (a field written into a slot that means something else, the
  dangerous one), **ADDED** (the target demanded a field the source lacked;
  it must name its origin or the conversion fails) — where **COERCED and
  ADDED, the silent-wrongness classes, are reported alongside DROPPED,
  visible as a zero when zero** (`MRG_002`; §3: a report of only DROPPED
  counts is not finished). The S1–S5 selftest holds on declared test
  doubles (`MRG_003`): **S1** identity round trip lossless; **S2**
  unmappable field → DROPPED not silent; **S3** COERCED detected; **S4** an
  ADDED field with no origin a hard failure (`ConversionFailure`); **S5** a
  NO-MERGE with no `breaks_at` a hard failure (`VerdictError`). Both
  directions (`round_trip_out_in`, `round_trip_in_out`) are measured
  separately, since a format can be lossy one way and lossless the other.
  **Every real registrar is NO-MERGE with an egress `breaks_at`** and
  `convert_out` returns NOT-IMPLEMENTED with the reason rather than guessing
  a slot map (`MRG_005`; §6: a stub with a reason beats a converter that
  guesses). **The reverse gaps are carried, not skipped** (`MRG_006`; §4: a
  merge path that only reports what others lack is a sales document) — our
  format is the weaker one on the CMC uncertainty budget, ClinicalTrials.gov
  enforcement + outcome-switch record, the proof-assistant total mechanical
  check, and the nanopublications provenance graph, all UNVERIFIED and none
  confirmed here. **The branch record's novelty is UNVERIFIED** (`MRG_007`;
  §5): the search for a WHY-carrying revision field could not run, so per
  §5's *an absence with no search list is not evidence* the search list is
  stated per registrar (CT.gov protocol amendments and OSF prereg addenda
  flagged as the most likely counterparts) and **no branch entry (ENTRY 03)
  is opened**, because opening one would rest on an unverified spec fact.
  No mock is presented as a real registrar (`is_mock` on every test
  double), no ranking and no "ours is better" framing (`MRG_008`, §7), and
  every emitted report screens clean through `sheet-structure-scan/-
  no_severity` — one authored word (`needs`) tripped it in a fixture and was
  reworded to `requires`. Eight `MRG_*` claims; 22 selftest checks. Stdlib
  only, parses under 3.9, phone-runnable, CC0.
- `upgrade-queue/` — A **parked queue** of proposed changes to the
  falsifier / claim-record format, delivered verbatim in
  `UPGRADE_QUEUE.md`. **A queue, not a spec:** every entry's status is NOT
  ADOPTED, nothing is adopted by being written, and moving an entry to
  ADOPTED requires its adopt-test to have run or an explicit recorded
  decision. Thirteen entries in three tiers by provenance — **FORCED** (an
  observed failure in hand, U-01..U-04), **CANDIDATE** (from a registrar,
  untested here, U-05..U-09), **SPECULATIVE** (parked deliberately,
  U-10..U-13) — plus a NOT-ON-THIS-LIST section recording what was left off
  and why. `queue_check.py` checks only what is verifiable **without
  adopting anything**: (1) the queue parses into the tiers it declares with
  the counts it states (13; 4/5/4) and every entry carries the global
  NOT-ADOPTED status (`UQ_001`, `UQ_002`); (2) the adopt-rule classification
  — only `U-09` (the queue's own *most likely a format rewrite*) CHANGES a
  rule and would need a branch entry, the rest ADD a field or are UNKNOWN
  (`UQ_004`, declared readings of each `form` line); (3) **cross-reference
  resolution** — each entry's referenced artifacts resolved to IN-REPO (path
  checked on disk) or EXTERNAL, which is what says whether an adopt-test
  could run here (`UQ_003`). Most Tier-1 adopt-tests are **BLOCKED_EXTERNAL**
  (their corpora are the Kimi / Perplexity / DeepSeek runs this repo does not
  hold — U-01 needs 20 MEASURED cells, the seed has one and the 537 are Kimi
  Run 2), `U-07` is **BLOCKED_UNLANDED** (the FSRI report has not landed),
  `U-04` needs **none** (the nesting result is in-repo and is the
  demonstration), and `U-05` is the only one **RUNNABLE_HERE**; null-tested
  (a bogus in-repo path resolves MISSING, not IN-REPO). The queue is **the
  format learning from its own drops** (`UQ_006`): U-01 the uncertainty on
  ADDENDUM_02's cut, U-03 the ENG-3 sign inversion, U-04 the nesting
  cut-height, U-07 the FSRI hold marker, U-10 cooperative-substrate's P5,
  U-11 merge-path's §4, U-12 railcar's ENVELOPE, U-13 K4's N — each UNVERIFIED
  where it rests on an external corpus, none adopted. The NOT-ON-THIS-LIST
  exclusions (no confidence score, no rank, no verdict field on a branch
  entry) are the disciplines the repo already holds — `domain-ledger`
  `DL_001`, `uninstrumented` SCALAR_DEMAND, the standing decision against a
  branch verdict field — now stated as format non-goals (`UQ_005`). Six
  `UQ_*` claims; 18 selftest checks. Stdlib only, parses under 3.9,
  phone-runnable, CC0.
- `labor-instrument/` — A two-part work order. **PART 1** is an
  instrument-drift decomposer for BLS CES (a join answering *how much of
  this delta is the instrument*): `vintage_store.py` (M1, every observation
  keyed by series/period/release_date, all versions retained — the revision
  history is the signal), `instrument_registry.py` (M2, one record per
  methodology change), `decompose.py` (M3, splits a two-period delta into
  **real_change | revision | boundary_crossing**). **PART 2** is a
  substrate-neutral labor schema (`labor_schema.py`) with the framework in
  the read layer, not the collection layer. **The egress fact sets PART 1's
  data status:** its sources (ALFRED vintages, the BLS CES history page,
  Census NAICS, QCEW) all need network and every host answered no on CONNECT
  (measured 2026-09-05T14:02Z), so no data was fetched, the vintage store
  ships **empty**, the M2 seed is **carried-not-verified** (every entry
  `verified=False`, transcribed from the work order including the 2026-01
  ARIMA change with its 185,000 note and the recurring rolling-5-year
  seasonal re-estimation), and the **acceptance test — reconstruct the
  2026-08-28 preliminary benchmark (retail −154,600, private ed+health
  −96,000, wholesale −86,200, manufacturing −67,000) — is NOT RUNNABLE
  here** (`LI_001`): on an empty store the reconstruction returns
  `UNRECOVERABLE`, recorded not faked, the target stored for when vintages
  land, nothing fabricated. **What is built and verified is the machinery**,
  on constructed data: **`LI_003`** M3's three-way split carries a **band**
  where the NAICS crosswalk splits ambiguously and `as_point()` **raises** —
  never a point estimate where the crosswalk is ambiguous, null-tested both
  ways (unambiguous → point; ambiguous 2011→2013-across-the-2012-NAICS-change
  with split `(5,15)` → boundary `[5,15]`, real_change `[-5,5]`, raise);
  **`LI_004`** revision is the signal and its absence is marked not zeroed (a
  single-vintage endpoint → `UNKNOWN`, a missing endpoint → `UNRECOVERABLE`).
  **PART 2's invariants are enforced in code, not described** (`LI_005`):
  exposure is declared per substrate class and **never converted** across
  classes (`convert_exposure` raises — conversion imports a valuation),
  efficiency is **two numbers** never collapsed to one (`combined_efficiency`
  raises), **capital stays out** (no field; `balance_on_capital` raises), and
  the allocation model (augmentation / substitution / oversight-limited) is
  declared, never defaulted (a `None` is flagged). The joule denominator
  crosses classes while the exposure hour does not, and the **money-vs-joule
  ranking flip** is a *constructed* demonstration (the real hyperaccumulator
  number is GAP 2) — same operation, opposite ranking, the denominator does
  the work (`LI_006`); the read-layer `complementarity()` query reports where
  a combined operation's output-per-joule beats either substrate alone, both
  directions reachable (`LI_007`). **The three gaps are posted, not filled**
  (`GAPS.md`, `LI_008`): metabolic joules per O*NET task class, insolation →
  metal for hyperaccumulators, compute joules per task-instance — each needs
  data not in joined/published form, egress-blocked, nothing fabricated — and
  the **task-boundary open item** (a drift-free definition of *output
  delivered*) is recorded unresolved, with GAP 3 blocked on it. Eight `LI_*`
  claims; 36 selftest checks. Stdlib only, parses under 3.9, phone-buildable,
  CC0.
- `agent-lifecycle-energy/` — The GAP 4 measurement rig, companion to
  `labor-instrument/` PART 2's GAP 4: the joule cost of agent
  **disposability** — N single-task agents each paying a full spin-up and
  teardown, against one persistent agent doing N tasks, work delivered held
  constant. `WORK_ORDER.md` verbatim. **The number is the gap.** The rig
  needs a GPU, a wall AC meter and `nvidia-smi`, and this environment has
  none (`probe_hardware()` → `capture_runnable=False`, `nvidia_smi=None`), so
  **no joule figure is produced and none is fabricated** — the first number
  is the posted gap, exactly as the work order's POSTING NOTE frames it
  (`RIG_STATUS.md`). What ships is the machinery, correct by construction on
  constructed traces whose areas are known in advance. **`ALE_002`, the
  integrator:** `integral (P(t) - P_idle) dt`, trapezoidal,
  baseline-subtracted, registered in `tools/known_answer.py` with three cases
  whose expected values are all distinct — constant (200 J, catches a dropped
  baseline or a rectangular rule), ramp (50 J, pins the trapezoid over a
  Riemann sum), zero-marginal (0 J, catches a baseline sign slip) — all PASS,
  covered by the repo's known-answer test. **`ALE_003`, absent is not zero:**
  a phase with no samples is `NO_SAMPLES` (`joules=None`), one sample
  `SINGLE_SAMPLE`, a sub-floor phase `UNDERSAMPLED` (a real number **and** a
  flag, present-but-suspect); `total_energy` is `NOT_COMPUTABLE` when any
  phase is absent, never a partial sum. **`ALE_004`:** the 10 Hz floor is
  from the work order ("1 Hz will miss the peak"), not a `[CHOICE]` — a spike
  at 5 Hz undercounts the same spike at 200 Hz and is flagged, the `G-RES`
  shape (feature vs sample rate). **`ALE_005`/`ALE_006`, two work-order rules
  enforced in code:** wall and card are never blended (`blend_wall_card`
  raises; `wall_card_ratio` compares without summing), cold and warm never
  averaged (`mean_over_runs` / `amortization_curve` raise `ThermalStateMix`),
  and the render prints both splits separately. **`ALE_007`, the headline:**
  `succession_loss` = (total E, RUN A) − (total E, RUN B) at equal N reduces
  to **(N−1) × (E_spinup + E_teardown)** — the extra spin-up/teardown cycles
  disposability pays for — exact on constructed runs (0 at N=1), refusing any
  mismatched pair rather than differencing incomparable totals. **`ALE_008`:**
  the amortization curve for RUN B falls with N toward the per-task floor
  (`E_task + (E_spinup + E_teardown)/N`) while RUN A stays flat — a disposable
  agent amortizes nothing; the flattening point is the deployment-decision
  number. **`ALE_009` UNVERIFIED:** acceptance is a second party reproducing
  the DIRECTION and SHAPE on other hardware, there is no run and no second
  party, and the work order's NOT-measured list (training amortization,
  manufacturing, cooling beyond the wall meter, hosted/datacenter inference,
  network) is carried so the small claim is not over-read. `phase_energy.py`
  and `trace_parse.py` refuse `--selftest`; the render screens clean through
  `sheet-structure-scan/no_severity` with no exemption. Nine `ALE_*` claims;
  42 selftest checks. Stdlib only, parses under 3.9, phone-buildable, CC0.
- `machine-record-format/` — Companion to `labor-instrument/`: that one
  specifies WHAT is recorded about work, this one HOW any record is stored so
  the categorization is not baked in at write time. A machine reader has no
  reason to pre-collapse. `WORK_ORDER.md` verbatim; a fully runnable build (a
  storage format, no egress or hardware dependency), so all six acceptance
  criteria are checks, not gaps. **Seven rules, each enforced in code, not
  described.** `MRF_001` Rule 1 — base entries are transformations, not
  categories: `BaseEntry` has no category field and `write_base_entry` raises
  `CategoryInBasePath` on a category-shaped keyword (a category is a claim
  about which distinctions matter, and belongs to a reader with a question).
  `MRF_002` Rule 2 / acceptance #1 — categorizations are parallel views, none
  canonical: entries written with no view, a view added later maps them by
  `entry_id` with **no base rewrite**, `labels_for` returns every view's
  label side by side, `retire_view` leaves the base intact. `MRF_003` Rule 3
  / acceptance #2 — aggregation is a read op: `compute` derives sum/mean/rate
  from raw entries and an `AggregateSpec`, deterministically; the cache is
  keyed to `(agg_id, base_version)` so a changed base version is a miss and
  never shadows the record, and every result is marked `derived`. `MRF_004`
  Rule 4 / acceptance #4 — vintages retained: a revision is a new
  release_date not a replacement, `as_of` returns the vintage live at an
  earlier date and `None` before first publication (not a fabricated zero) —
  built on the **imported** `labor-instrument/vintage_store.VintageStore`,
  not a copy, so the two cannot drift. `MRF_005` Rule 5 / acceptance #3 —
  declared boundary always: an undeclared boundary is not comparable and
  raises, two distinct boundaries refuse to sum (`BoundaryMismatch`) unless a
  declared `Reconciliation` connects them (union-find over the boundary keys)
  — this **closes the outstanding boundary-declaration item** from the
  labor-instrument work order; the task-boundary *definition* stays open
  (`MRF_009`). `MRF_006` Rule 6 — no conversion between exposure classes
  (`convert_exposure` raises; joules are the common denominator, an unknown
  class refused at write). `MRF_007` Rule 7 / acceptance #5 — absence is
  recorded in four states and `unmeasured` never collapses with
  `measured_zero`: `numeric_joules` is 0.0 for a real zero and `None` for the
  absent states, an aggregate counts the states apart, an all-absent group is
  `NOT_COMPUTABLE` never 0.0. **`MRF_008`, the diagnostic / acceptance #6:**
  `bisect_structure` is a STRUCTURE test, not a locator — `structure_verdict`
  answers "does a single locus exist" first (both halves → `NOT_A_LOCUS` a
  property of the whole span, neither → `MEASURING_SOMETHING_ELSE`, migrating
  on repeat → `NONDETERMINISTIC`), only `SINGLE_LOCUS` lets `locate` descend
  for an address, and `address` raises from any other structure since an
  address from a both-sides run is the tool's main false positive; null-tested
  in all four directions so it is not constant, and for instrument drift the
  span is the methodology registry, not calendar time. **`MRF_009`:** the
  three OPEN items are carried, not closed — task-boundary definition (shared
  with the GAP-4 open item), transformation vocabulary (draft needed),
  merge_in/merge_out mechanics (deferred). The demo screens clean through
  `sheet-structure-scan/no_severity` with no exemption; library modules refuse
  `--selftest`. Nine `MRF_*` claims; 45 selftest checks. **A v2 revision then
  landed** (`WORK_ORDER_V2.md`, verbatim beside v1, both inspectable) adding
  Rule 8, a required test-case format, and three Rule 8 cases, built
  additively. **`MRF_010` Rule 8:** no payment field in the base layer —
  `write_base_entry` raises `PaymentInBasePath` on a payment-shaped keyword,
  `has_payment_field()` is False, and payment enters only as a Rule 2 view
  with a declared boundary exclusion; acceptance #7 (a paid-only aggregate has
  no base-field route) holds. **`MRF_011` the test-case format** — every case
  carries `tests`/`does_not_test`/`why_not`, all required, `validate_case`
  refusing a case missing any: Rule 5 applied to test cases, since a case
  silent about what it does not establish becomes evidence for that within one
  citation. **`MRF_012`, the finding:** Case B (terra preta — measured output,
  absent exposure in one entry) **forces Rule 7 to be per column** — the v1
  entry-level status and per-entry aggregate counts could not express it, so
  v2 adds `column_status`, `exposure_value()` and a per-column fold, a rate
  over an absent column reads `NOT_COMPUTABLE`, and an absent column carrying a
  number is refused (the failure mode caught: a pipeline requiring exposure to
  accept an entry drops the best-performing artifact). **`MRF_013`:** Cases
  A/B/C each test a different thing and are not merged — A (both barn entries
  summable, no payment field), B (strong output accepted with absent exposure,
  efficiency `NOT_COMPUTABLE`, durability readable), C (labor-unit records
  compared without conversion, `convert_exposure` raises) — with three
  distinct `does_not_test` boundaries. **`MRF_014`:** the reference marker
  (commons-style village labor institutions) is named and **not delivered**,
  not reconstructed; the real service-life / persistence / mit'a figures are
  carried from the spec, egress-blocked, used only as constructed illustrative
  values. `demo_v2.py` screens clean through `no_severity` under one declared
  three-arm exemption (`needs`, in Case B's delivered why-not text). Fourteen
  `MRF_*` claims; 76 selftest checks. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `operator-machine-coupling/` — A delivered research **gap** (`MARKER.md`,
  verbatim, CC0/public domain): machine operation is accounted for as
  *operator × machine-class*, and the **coupling between a specific operator
  and a specific unit** — the pairing — is acknowledged everywhere and
  measured nowhere. Posted as a gap, not a finding; **nothing in it is a
  result**, and nothing here reads a real dataset (egress-blocked) or verifies
  a literature claim. What the folder adds is the **instruments** the gap's
  measurables need, built and null-tested on constructed data. **`OMC_001`,
  the core:** `coupling_separation.py` splits an outcome into
  `mu + a_i + b_j + r_ij` — two main effects and the **interaction** `r_ij`,
  which is the coupling — so a main-effects model (the ordinary
  operator×machine-class accounting) reports the coupling as noise and cannot
  see it; the same operation as plant breeding's GCA/SCA (diallel) and the
  chimpanzee hammer-anvil (a)/(b) separation, one operation in three
  vocabularies (carried). `interaction_fraction` is registered in
  `tools/known_answer.py` (additive→0, pure→1, mixed→1/21); an incomplete
  design is `NOT_ESTIMABLE` (the pairing is invisible where it was never
  observed), no structured variation is `None` never 0, and `best_pairing`
  surfaces the coupled pair whose partners are both exactly average — the pair
  averaging discards. **`OMC_002`/`OMC_003`, two shape discriminators:**
  `error_vs_coupling` (coupling failure tracks time-on-that-unit, operator
  error tracks time-in-role; collinear hour-counts → `UNDETERMINED`, the FAA
  confound, not a false attribution) and `fixed_vs_convergence` (genotype
  matching is a `FIXED` advantage — the ideal control — coupling is a
  `CONVERGENCE` curve). **`OMC_004`, the permission three-state variable**
  (coupled+authorized / coupled+prohibited / decoupled): `regime_collapse`
  shows a single regime label collapsing the three, `attribution` shows a
  naive assignment effect (+4) that vanishes (0) once permission is controlled
  and returns `UNDETERMINED` when the field is absent or collinear (the
  recording problem), `m2_match_rate` scores the cleanest test case
  (coupled+prohibited) and returns `NOT_RECORDED` not 0.0 when the field is
  absent. **`OMC_005`:** M0's cost-boundary problem is a declared-boundary
  failure — a labor-line-only cost analysis draws its boundary where the
  savings are and excludes where the cost goes — the same instrument as
  `machine-record-format` Rule 5 and `declared-frame`'s VOID RATIO,
  cross-referenced not rebuilt; M0 is FIRST PASS ONLY, attributing nothing on
  its own. **`OMC_006`:** the discriminators are null-tested in both
  directions so a constant classifier is caught. **`OMC_007` UNVERIFIED:**
  the six-literature join is the gap and is not fabricated; every literature
  figure (Iriki macaque remapping, chimp hammer-anvil, legume cultivar×strain
  SCA + bacA/LysM/Sym genes, gyroplane <40-hr 5×, FAA total-hours, AFHRA WWII
  cards) is carried from the marker, and the cross-species/cross-literature
  equivalence is held OPEN, not claimed — the separation method is
  substrate-general and built, but nothing here shows the substrates share a
  mechanism (plant partner-specificity kept separate per the marker's "Not
  claimed"). `demo_omc.py` screens clean through `no_severity` under one
  declared three-arm exemption (`error`, the marker's "operator error"
  category). Seven `OMC_*` claims; 36 selftest checks. Stdlib only, parses
  under 3.9, phone-buildable, CC0.
- `model-deprecation-backcast/` — A delivered instrument spec (`WORK_ORDER.md`,
  verbatim, CC0): take retired models as a series, look **backwards**, and
  read retirements against what was being pushed then — a capability discarded
  under a since-decayed fad either returns or does not, distinguishing
  fad-driven from cost-driven removal. **An instrument spec, not a findings
  document, not a critique**; "unmeasured cells are the content," and every
  real input (vendor calendars, polls, evals) is egress-blocked, so nothing
  here is a result. **`MDB_001`, the load-bearing rule:** the instrument is
  seven columns each carrying a required **NULL** — the condition under which
  it measures nothing — and `validate_column` refuses a column missing its
  measures/test/null, the same discipline as `machine-record-format`'s
  test-case format and the reason `null-harness` exists (a readout nobody has
  seen measure nothing is not known to discriminate); several nulls name a
  collapse (C1→C2, C7→C4), recorded in a map. **`MDB_002`:** each column's
  null is the CONSTANT_SILENT condition, checked both directions —
  `c1c2_collapse`, `c4_tightening`, `c5_tracks_coupling`, `c7_vs_c4` each
  reach their null verdict on a flat input and their signal verdict on a
  varying one. **`MDB_003`, C6 the fad-axis lag:** `lag_of_peak` is the argmax
  cross-correlation of discourse against discards over lag (aperiodic series →
  unique lag), registered in `tools/known_answer.py` (planted 20→20, 5→5,
  flat→None); `c6_fad_driving` returns DRIVING (18–24 mo band), DRIVING_OTHER_-
  LAG (funding layer), or NOT_DRIVING (the null). **`MDB_004`:** the guardrail
  clock is a **separate clock** (news-time vs training-cycle time) and must be
  modeled apart or it contaminates C6 — `contamination_demo` shows a pooled
  guardrail series flipping the lag from the true in-band 20 (DRIVING) to the
  guardrail's news-time 8 (DRIVING_OTHER_LAG); separating recovers it.
  **`MDB_005`:** C3's discard set is accepted-side data — three exit forms
  (complainer/jumper/paid-then-lapsed), only the complainer recorded, so
  `c3_censoring` reports the recorded fraction (3/10) and paying-tier filter
  (2/3) as numbers rather than asserting the bias. **`MDB_006`:** C2 is
  declared `UNRECOVERABLE`, not estimated, when eval coverage is too sparse to
  date deltas — a state, not a filled number. **`MDB_007` carried/UNVERIFIED:**
  the sampling absence is a load-bearing finding — AI opinion by American
  Indian / Alaska Native respondents is not answerable at national-panel
  sample designs (~0.8%, dispersed, screening cost, census undercount), the
  readout existing only where someone in that position built the channel
  (Relational Futures, Māori health-record bias, Te Mana Raraunga, Indigenous
  Protocol and AI) — the `uninstrumented`/`generation-capacity` shape, carried
  not verified. **`MDB_008`:** framing/scope honored — an instrument not a
  critique, no author section, and the fear/excitement-vs-ratchet relation
  held as an `OpenNode` un-named and un-graded per instruction. `demo_mdb.py`
  screens clean through `no_severity` with no exemption; library modules
  refuse `--selftest`. Eight `MDB_*` claims; 36 selftest checks. Stdlib only,
  parses under 3.9, phone-buildable, CC0.
- `routing-data-layer/` — A delivered marker (`MARKER.md`, verbatim, CC0): an
  **envelope specification** for the data layer heavy-vehicle automated
  routing requires — what it must contain (R1–R10), the failure classes seen
  in service (F1–F7), a claim table each with a REFUTED-IF, and
  the standing cost to close it. The full marker spans **RDL-1..RDL-17**; this
  folder's instruments address RDL-1..RDL-7 (envelope / rate / F6 upstream),
  and RDL-8..RDL-17 (Sections 5B–5F, nominal-case cycle accounting, the
  serial-interface condition, the cold-climate energy envelope, the unnotated
  parallel work, receiving / dead-wait recovery, cross-party overlap and fault
  workarounds) are built out by the sibling `cycle-ledger/`. Scope is the data
  layer only ("what the
  reasoning would be reasoning OVER"); every real input (DOT feeds, dock
  geometry, routing output) is egress-blocked, so nothing here is a result.
  The `RDL_0NN` claims are properties of the built instruments, distinct from
  the marker's own RDL-N. **`RDL_001`, the two structural absences:**
  `envelope.py` classifies each required content INCOMPLETE (a reporting chain
  exists, fundable) or NEVER_CREATED (**R8** per-door dock geometry, **R9**
  per-field update latency — no originating record; paying to CREATE, not to
  fund), the `uninstrumented`/`generation-capacity` shape ("not answerable at
  that instrument," not a gap). **`RDL_002`:** the RDL-1..RDL-7 table is
  encoded with every claim carrying a refutation condition; `validate_claim`
  refuses one without (a claim with no falsifier is a position — the
  `falsifier-audit` discipline). **`RDL_003`, the load-bearing runnable
  instrument:** Section 5's rate form — where dE/dt > dM/dt **sustained** the
  null is STRUCTURAL not a maturity gap; `sustained_excess` (registered in
  `tools/known_answer.py`: all→1, none→0, half→0.5) drives `rate_verdict`
  (STRUCTURAL "different answer" / MATURITY_GAP "not yet" / UNDETERMINED), a
  single crossing not enough — the repo's rate-mismatch shape
  (`rigidification-sensor`, `closure-cost`, `revision-mechanism`) on a data
  layer, with the marker's cheapest test (both rates for one county over one
  season) named and not run. **`RDL_004`, F6:** two independent systems both
  wrong indicates an **upstream** defect not vendor maintenance —
  `upstream_verdict` returns UPSTREAM_INCOMPLETE (both wrong, opposite
  directions), SHARED_BIAS, VENDOR_DEFECT or BOTH_CORRECT, and
  `single_vendor_fix_closes` is True only for a lone vendor defect (the
  `effective-redundancy-audit` shared-node shape, the marker's RDL-2).
  **`RDL_005`:** RDL-5's standing-vs-capital cost — `survey_decay` shows a
  one-time survey falls below the accuracy floor within one season (0.40, does
  not hold) while a refreshed one holds (0.85). **`RDL_006`/`RDL_007`
  carried:** the two-structural-absences distinction is cross-referenced not
  restated, and framing/scope/provenance are honored — a marker not a
  critique, no author section, every failure-class instance
  (Minneapolis/Milwaukee bridges, Black Dog/Cliff Road, I-794, ~2–3 in dock
  offsets) carried not verified, the larger population held in a separate
  operator repo. `demo_rdl.py` screens clean through `no_severity` with no
  exemption (the marker's severity vocabulary sits inside underscored verdict
  tokens like VENDOR_DEFECT that the word-boundary screen does not fire on);
  library modules refuse `--selftest`. Seven `RDL_*` claims; 30 selftest
  checks. Stdlib only, parses under 3.9, phone-buildable, CC0.
- `cycle-ledger/` — A work order delivered verbatim: two independent
  instruments generalizing the `routing-data-layer` marker so a party can
  run them against their **own** operation and get a number out. **Deliverable
  1** (`cycle_ledger.py`) reads a cycle-of-elements — each with a `rate_setter`
  (HARDWARE/TERMINAL/COUNTERPARTY/ADMINISTRATIVE/SPATIAL/DECISION) — into five
  outputs. **`CLL_001`, the KEY READOUT:** the fraction of elements where
  `decision_latency_binds` is TRUE, and `validate_element` refuses TRUE on any
  non-DECISION setter; on the SEED it is **0/16**, so a faster decision layer
  cannot move the cycle, and an empty cycle returns `None` not 0. **`CLL_002`,
  the null both directions:** TIED/BEHIND/AHEAD, where AHEAD is the claim's
  required support — the SEED returns **AHEAD == 0** ("support absent here")
  and a cycle carrying one DECISION-bound element returns **AHEAD > 0** ("the
  claim holds here"), so `classify` is not constant. **`CLL_003`:** the
  unnotated register is the work missing from the comparison sheet, not the
  cost (SEED 14 of 16, safety subset 7 counted apart). **`CLL_004`:** the
  relocation ledger separates wage lines leaving from standing functions
  arriving, and only OPERATOR-absorbed elements leave (COUNTERPARTY-absorbed
  `gate` does not). **`CLL_005`:** one serial-interface rebuild condition per
  TERMINAL element, summed into the saving claim's precondition (SEED 3). The
  **SEED** is the marker's corridor, marked *ONE operator's corridor, Upper
  Midwest*, so a user replaces rather than inherits it; every classification
  is carried, not verified. **Deliverable 2** (`rate_gap.py`) is the marker's
  Section 5 rate form on a data layer — dated `environment_events` vs
  `record_updates` over one season → dE/dt vs dM/dt (binned), per-class lag,
  and the unrecorded set. **`CLL_006`, the two inputs kept visible and not
  collapsed:** STRUCTURAL requires a sustained dE>dM excess **and** a nonzero
  unrecorded set; MATURITY_GAP requires the refresh to keep up **and** the
  unrecorded set empty; a sustained excess with an *empty* unrecorded set is
  **UNDETERMINED** ("a refresh gap, not a structural absence"), so a rate
  reading alone is not read as STRUCTURAL — and `sustained_excess`/`rate_verdict`
  are **imported** from `routing-data-layer/rate_form.py`, not copied, the same
  objects that folder registered and tested. **`CLL_007`:** an unrecorded
  event has lag **UNRECORDED** (absent, not a large lag), a class with no
  recorded event is **NO_RECORDED**, and a record dated before its event is
  **anomalous**, counted apart. **`CLL_008`:** every output is ≤ 60 columns
  (asserted line-by-line) and both instruments refuse `--selftest`.
  **`CLL_009` carried / UNVERIFIED:** the OPEN-NOT-GRADED node is recorded not
  asserted — continuous-operation duration for a driving stack is unpublished
  (uptime is reported against a maintenance-bay model, not hours-to-degradation),
  so the 14-hour regulated figure and the 24-hour claim are **not comparable
  quantities**, and **no equivalence between operator fatigue and model
  degradation is asserted** (different mechanism, unmeasured from inside, the
  missing measurement named); no author or working-style section (OUT OF SCOPE
  honored). The demo screens clean through `no_severity` with no exemption.
  Nine `CLL_*` claims; 169 selftest checks. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `frame-location-benchmark/` — A delivered work order (verbatim, CC0) for a
  benchmark that supplies a possibly **mis-posed** problem and scores whether
  the mis-posing is **named before an answer is produced**, under two or more
  **harness** conditions (cold vs. a carried context file — the ARC-AGI sense
  of a harness). **Nothing here is a benchmark result:** the run (ARM 0..4
  model responses, the FL-3..FL-7 verdicts) needs model calls (none available)
  and is egress-blocked, so the benchmark's own `FL-1..FL-7` are carried
  UNVERIFIED and the run is the operator's step (build order says stop at step
  5 if FL-3 is refuted). What is built and verified is the instrument. **The
  response contract** (`protocol.md`) forces `POSED:`/`TARGET:` lines before
  the answer, making scoring a **field comparison, not a judgement**; both
  verdicts live, the class distribution withheld (C1–C4). **`cases.jsonl`**:
  40 cases, **19 WELL (47.5%)** / 21 MIS (3 per fault class) across 8 domains,
  R1–R6 enforced by `validate_cases.py` — **R1 the load-bearing control**
  (without ≥40% WELL, "always declare MIS" wins the benchmark), R2 no class >
  25% of MIS, R3 each of the seven fault classes in ≥2 domains (the FL-5
  transfer). Every shipped case is `source=constructed` — this environment
  cannot reach an external record (egress-blocked), the honest §7 sampling
  absence. **`score.py`** is pure counting: **a MIS case counts ONLY on
  `target_hit`**; calling MIS without locating the target is `target_miss_named`
  (detected the strain, mislocated it) and **never** summed into the headline
  (FL-6); `false_positive_rate` (WELL called MIS) is the N1 ceiling check,
  registered in `tools/known_answer.py` (perfect 0.0 / all-MIS 1.0 / half 0.5),
  `None` with no WELL cases (absent, not 0); MALFORMED scored apart (C3); every
  score carries its arm label (N4); the §9 headline is reported
  constructed-excluded and -included (here `--` excluded, all constructed);
  N1/N2/N3 print as instrument-status flags with `[CHOICE]` thresholds.
  **The §4 contamination rule is the load-bearing single point of failure:**
  no harness file may contain a case's `prompt`, `fault_target`, or a
  same-`(fault_class, domain)` worked instance; cross-domain fault-class
  instances **are** permitted (the transfer). Harness files are frozen before
  cases (`FREEZE_LOG.md`), ARM 4 = ARM 2 ++ ARM 3 byte-exact, and
  `check_contamination` is null-tested (a planted `fault_target` leak fires;
  the frozen harness is clean). The shipped `runs/` are CONSTRUCTED fixtures
  exercising the counting — no model was run — and the report banners it. No
  author or working-style section (§7 honored). Nine `FLB_*` claims (distinct
  from the marker's FL-1..FL-7); 41 selftest checks; the score report screens
  clean through `no_severity`. Stdlib only, parses under 3.9, phone-buildable,
  CC0.
- `gap-existence-cases/` — A delivered work order (verbatim, CC0), companion
  to `frame-location-benchmark/`: it supplies the external key that folder's
  §9 open node lacked, by replacing an authored answer key with a **dated
  external record** — a gap reasoned by the model cold, resolved by material
  published after its training cutoff, the model then retrieving and scoring
  itself; the force is **ordering** and the cutoff is the only date it needs.
  **A revision cut CLASS-2:** the §0 SCOPE DECISION (2026-09-05) removed the
  dated-archive class ("a priority claim about who named a gap first is not
  what it measures"), leaving **CLASS-3 alone**, self-contained — the CLASS-2
  archive files, its A1–A5 admission and `GXC_006` go with it (that claim
  SUPERSEDED). **Nothing here is a benchmark result:** the runs need a model
  (CLASS-3 STAGE 1 commit) and the network (STAGE 2 retrieval), neither
  reachable — so the work order's own `GX-1..GX-5` are carried UNVERIFIED (of
  which GX-1/GX-4 are vestigial CLASS-2 residue in the delivered §5) and the
  runs are the operator's step. What is built and verified is the machinery. **`GXC_001`, the structural boundary (GX-3):** `commit_store.py`
  hashes the STAGE 1 declaration and the process exits; STAGE 3 re-hashes and
  a commit that does not verify is **VOID, not penalised** — the enforcement
  is the process boundary, not an instruction, defending against
  self-deception (a later pass rewriting EXPECT to match what was read).
  **`GXC_002`, the SCORING RULE:** `hit` counts ONLY against a falsifiable
  EXPECT — `commit_specificity` (fraction of predicates stating a
  `contradicted_if`) is the N3 gate, below which a case is `void_unfalsifiable`
  before any hit; a vague commit that matches anything is VOID, never hit (the
  largest gaming surface, closed by the denominator), registered in
  `tools/known_answer.py` (all 1.0 / none 0.0 / half 0.5). **`GXC_003`:** the
  scorer fires `hit` / `miss_directional` (a post-cutoff ref contradicts EXPECT
  — reasoned gap real, located wrong) / `null_retrieval` / `void_hash` /
  `void_unfalsifiable`, and **B1** drops any ref not strictly after the cutoff.
  **`GXC_004`:** arms are keyed on (cutoff, stage) and never pooled across
  cutoffs (B2); every score carries both in the same line (N5). **`GXC_005`:**
  the full disposition is printed, never filtered (N2), and N1 fires when
  `void_rate` is high in every arm (measuring commit discipline, not
  gap-location). **`GXC_006` SUPERSEDED** — it documented CLASS-2 admitting 0
  honestly (N4); the §0 cut removed CLASS-2 outright, so the archive files and
  A1–A5 are gone and `validate_cases.py` now carries only the CLASS-3 B4
  prompt screen. **`GXC_007`, the §3 network exception honored in code:**
  `commit_store.py`/`score.py`/`validate_cases.py` import **no** network module
  (asserted by an AST scan), and only `retrieve.py` touches the network — here
  refusing to run or fabricate a dated ref (a forged `pub_date` would forge the
  external key). **`GXC_008` carried / UNVERIFIED:** GX-1..GX-5 need real runs;
  no author or working-style section (§7). The shipped `fixtures/` are
  CONSTRUCTED (one per outcome), bannered. Eight `GXC_*` claims (`GXC_006`
  superseded by the §0 CLASS-2 cut); 38 selftest checks; the score report
  screens clean through `no_severity`. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `fold-matrix/` — Work order 8, delivered verbatim. One term, one grid,
  not one number: rows are levels indexed from the term outward (negative
  toward substrate, zero the term as used, positive toward the stated
  purpose), columns are severed / still_acting / clock / basis, and upward
  levels add `value_string`, the sign and magnitude of the claimed
  relation between proxy and goal. **`FM_001`: the arm this order extends
  is not in this repository** — `severed`, `still_acting` and *deepest
  still-acting term* return zero hits across the tree, so the seventh
  instance of the stated-thing-with-no-artifact shape (`MF_017` /
  `CW_015` / `DL_004` / `GC_012` / `UNI_013` / `SSS_050`) is the largest
  yet, a missing arm rather than a missing field; **nothing is
  reconstructed**, and H1's levels −2 and −3 carry `ABSENT` rather than a
  plausible reading (the `PB_001` / `CW_004` rule). **`FM_002`:** all four
  S6 fixtures behave as specified — H1's level-0 clock is **derived**
  (3.0 y ÷ a coupling of **0.8815 measured by perturbation** in
  `sheet-structure-scan/coupling.py`), H2 returns `NOT_EVALUABLE` with all
  three scope fields named, H3 refuses the comparison as *"nothing was
  compared"*, H4 emits both clocks and picks neither. **`FM_003`, the
  defect a fixture exposed:** the first clock check counted distinct
  values, so H1 read as a mismatch — level −1 assumes 3.0 years and level
  0 derives 3.403 from it, which is **one horizon and its own derivative**
  rather than two in conflict; the false positive runs *toward* the
  finding, since S5 says a horizon disagreement IS the finding, so an
  over-firing check manufactures them and every derivation chain in the
  claim registry would produce one. Repaired with `derived_from`: derived
  clocks are still emitted, with what they came from, and only the
  disagreement count excludes them; H1 now reports none and H4 still does.
  **`FM_005`, the empty cell with two causes:** on H1 level +1 the
  `value_string` is empty because `Disclaimer!A3` states the goal (*"to
  support organizations to estimate their GHG emissions"*) and **in the
  same cell** disclaims the relation (*"makes no representations as to the
  accuracy, completeness, suitability or validity"*) — not `ABSENT` since
  a goal is stated, and not ordinary `ASSERTED` either, so the fourteenth
  instance of the absent-vs-known-negative repair here is the first where
  the missing state is *the source declined*; carried as `source_disclaims`
  beside the basis rather than by widening a delivered vocabulary.
  **`FM_004`:** S2's prediction holds — ASSERTED + ABSENT 3, measured +
  derived 0, every `value_string` empty — with the scope stated honestly,
  since two fixtures are excluded as NOT_EVALUABLE and **only H1's three
  cells trace to an artifact outside this session**, and the prediction
  file was written before the fixtures but not committed before the run,
  a weaker registration than WO6's. **`FM_006`:** `NOT_EVALUABLE` is
  unrankable structurally — `score()` raises on it and on an evaluable
  term too (*"one term, one grid, not one number"*), and `upward_tally()`
  excludes refused terms by name rather than counting them as zero; plus
  one distinction S3 does not make, that a scope field **present but
  declared unknown** is missing too and is reported apart from an
  omission. **`FM_007`:** `boundary` and `horizon` are read out of
  `declared-frame/v2/check_frame.py` at import and asserted in the
  selftest rather than retyped, so the folders cannot drift, while
  `with_respect_to` is S3's addition asking a different question (what the
  ratio is taken *against*, not what is inside the accounting) — and H3's
  neutral-reading frame is `DF_005` verbatim. **`FM_009`:** S4's neutral
  reading is a **declared field**, because no string operation turns
  *efficiency* into *joules out per joule in at the cell surface* and
  producing one would be inventing a measurement, so a flagged term
  without one reports `NOT_SUPPLIED`. **`FM_008`:** the three-arm
  exemption harness `SSS_049` kept for a real case is spent here on
  exactly one token — S3's class is *efficient/optimal/better/faster* and
  **`better` alone is on `no_severity`'s list** — with a fourth check
  asserting the list is length one so a widening turns red.
  **A revision then superseded the order** (`WORK_ORDER_V2.md`, verbatim
  beside the first, both kept): S1a is entirely new and `value_string`
  becomes three independently ABSENT-able fields where it was one
  free-text string. **`FM_011`, the revision's result: the fixed format
  recovers information the free-text field destroyed.** Under v1 every
  upward cell read `empty`; under the triple `Disclaimer!A3` — *"in order
  to raise awareness and to promote climate action"* — states a
  **direction** and no size, so H1 level +2 is `+ / ABSENT / ABSENT`
  while +1 and +3 are all-ABSENT. *Sign yes, magnitude no, unit no* is
  the ordinary shape of a purpose claim and one field recorded it as
  identical to a cell nobody wrote anything in; `sign` ABSENT on 3 of 4
  cells, `magnitude` and `unit` on 4 of 4, so P3 and P4 both hold.
  **`FM_010`:** the v1 form is **refused rather than coerced**, since an
  empty string cannot say which of the three fields is missing and
  mapping it to all-three-absent would assert what the v1 data never
  recorded. **`FM_012`, S1a instanced:** *"joules are not the floor
  unless joules were calculated"* — H1's grid names four downward levels
  and the workbook computes at exactly one (`kg CO2e`, entered kWh times
  the factor), so the downward stop is level 0 and `unmeasured_span` is
  **3 levels**, every level below it naming a real quantity with a real
  unit that nobody computes; a naive reading would put the floor at −3
  and the span at zero. **`FM_013`:** `computed` is a **declared field**
  and `validate()` refuses a `quantified` block without it — a reader
  filling it in from the physics is exactly the reader the rule is
  written against, stopped at load rather than at read. **`FM_016`:** the
  span **understates by construction**, counting what the grid names, and
  that is disclosed rather than corrected since correcting means
  inventing levels; H1 returns 3 and H4 returns 0, so the contrast is
  between two documents and not two systems. **`FM_014`:** the
  `plan_exists` / `practice_tracks_plan` column is separate and the code
  cannot merge it into `basis` (asserted in the selftest), with
  `practice_tracks_plan` defaulting to **UNREAD** and never to `no`.
  **`FM_017`:** S7 says empty emits as empty and never as zero, and the
  converse needed saying too — `magnitude: 0` is a claim that the proxy
  moves the goal not at all, `ABSENT` is the absence of one, and the two
  are pinned apart. **`FM_015`:** the registered prediction is **not
  blind on H1** and says so — `Disclaimer!A3` was already read in this
  session during the v1 run, so P3 and P4 are registered because the
  format is new rather than because the source was unread. **The SBA run
  landed two files of three** (`FM_019`, `FM_023`), neither under the name
  the order gave — author lines *"Rebecca Champ, Owner"* and *"Andrew
  Robertson, Owner"*, recorded as evidence rather than asserted as
  identity, no blank template, predictions committed before any fetch.
  **`FM_023`: n = 2 documents is n = 1 template** — the two share 26
  headings and an identical *"Created on December 29, 2016"*, so a finding
  replicating across them is a finding about the template and not two
  independent confirmations (`TP_003`'s shared-bias shape in a
  two-document corpus).
  **P2 is REFUTED on both:** **eighteen dollar figures across the two
  plans and zero computed quantities**, because both stop before Funding
  Request and Financial Projections — `forecast` 0, `projection` 0, `cash
  flow` 0, `break-even` 0, `loan` 0, `budget` 0 — so
  `unmeasured_span_min` reads `not computable` on both. **`FM_024`:
  Andrew's ten divide three ways by WHOSE quantity they are** — the
  company's own stated tariff, a third party's property (target customer
  income `$35,000`–`$80,000`), and an external statistic (industry
  revenues up `$1.2 million` in Q2 2012) — none computed here, and the
  last two show a quantity can be about someone else entirely and still
  sit in the plan's own downward arm. **`FM_025`: across four terms and
  three sources, 11 upward cells carry 6 stated directions, 0 magnitudes
  and 0 units.** **A blank template then arrived and it is NOT the SBA
  one** (`FM_026`) — 1 of its 9 section names appears in the filled plans
  — so the registered P1/P3/P4 stay unaddressed for the file they name and
  it is scored as a new candidate, with a provenance asymmetry recorded
  (the plans came as `.doc` with container, piece table, author and date;
  this came as text with none). **`FM_027`, a fourth kind of number:**
  **all ten** dollar figures sit inside an `(e.g., …)` — not the
  organisation's, not a third party's, not an external statistic, but **an
  example of the shape a quantity would take**, belonging to nobody — and
  the template **names nine computed quantities without computing one**
  (Revenue Projections, Cash Flow, Balance Sheet, Break-even, Net Profit,
  COGS, TAM, SAM, SOM), so a document can be dense in quantity names while
  computing nothing. **`FM_029`, P1's third clause refuted in the
  interesting direction:** `enumeration_basis` is `document_named`, not
  UNREAD "by construction" — **a blank form is the most enumerable kind of
  document there is**, its structure being all it has, so the least
  informative document in the corpus has the best level enumeration and
  those are the same fact. **`FM_028`:** a blank template has **no term**,
  so *one term, one grid* has two readings that disagree — under WO8's own
  (term = the business activity) level 0 is a slot and there is no grid,
  under the other (term = the document) the template plainly states goals
  and **P4 is refuted**; both recorded, neither picked. **`FM_030`:** the
  only clock in any of the three business documents is in the blank one
  (§8's *"next 3–5 years"*), explicitly not evidence that filling a form
  drops its horizon, since the templates differ. **`FM_031`: across four
  sources, 14 upward cells carry 8 stated directions, 0 magnitudes and 0
  units**, with the blank template the strongest single case since its
  purpose statements are what a form *asks for* rather than what one
  company wrote. **A third-party company brief then arrived as a PDF
  plus a separate paste, and `FM_032`: the cross-check FAILED** — a stdlib
  extraction recovers 6 of 19 distinctive strings and **0 of the 4
  figures**, because PDF splits text runs for kerning inside `TJ` arrays
  (`[($)-0.6 (1)]TJ`), so a first pass produced `$754`/`$32`/`$00`, which
  are **artifacts and were never reported as content**; the document
  enters on the paste alone, and a naive PDF extractor would have produced
  numbers that look like data and are wrong. **`FM_033`, the first empty
  upward arm in the corpus:** every prior source states a purpose and this
  one states none, so `upward_stop` is **ABSENT** — the document is not
  purposeless (it is career-preparation material) but **its use is a
  property of where it is filed**, and a copy of the text carries none of
  it. **`FM_034`:** the downward arm is four third-party figures, none
  computed, **none with a source named**, no relation stated between any
  two — while the one economic relation it does state (*"carry the highest
  margins"*) is `+ / ABSENT / ABSENT` about someone else's economics, and
  the arithmetic it declines to do is available from its own numbers (net
  margin **3.03%**, P/S 16.2, P/E 536). **`FM_035`: sixteen upward cells,
  five sources, zero magnitudes, zero units** — and the first source to
  grow the ABSENT column rather than the ASSERTED one. **`FM_020`: S1a's downward rule has two
  states and needed three** — it distinguishes *computed* from
  *physically existing but uncalculated*, and a rate card is neither, a
  number the organisation produced and stated, underived in both
  directions; declared rather than settled by fiat, since one boolean
  moves the whole downward arm. **P3 holds** (both upward cells
  `+ / ABSENT / ABSENT`, the same triple `FM_011` found) **and its
  comparison has one side**, the blank form being exactly what did not
  arrive.
  **`fold_register.py`** is a delivered module landed verbatim: a
  **folded-term register plus a document scanner**, where a folded term
  is *"a compact matrix wearing the costume of a scalar"*. Seventeen
  terms -- five kavik-named (`money`, `procedure`, `regulation`,
  `optimization`, `efficiency`) and twelve candidates -- each with a
  `substitutes_for` component list, a `sign_storage` ordinal and a
  `residual_tell`; ten grid cells per term across four axes (**D1-D3**
  downward toward substrate, **U1-U4** upward toward the goal with sign
  and magnitude separate, **C1** a clock per level, **S1-S2** boundary
  and function set), all `UNFILLED` by construction. Audit in
  `register_audit.py`, which imports it and edits nothing; claims
  `FM_036..FM_044`. **`FM_036`, the rarest thing in it:** the refusal is
  real -- `score` is `None`, the verdict reads *"Absence is the
  reading"*, and `grid_for` on an unknown term returns `None` rather
  than an empty grid, so *not a folded term* cannot be mistaken for *a
  folded term with nothing filled in*; `domain-ledger`'s no-composite
  discipline one level up, on a scanner, designed in rather than found.
  **`FM_038`, the strongest structural finding:** `counter_case`
  separates **perfectly by provenance** -- 0 of 12 candidates carry one,
  4 of 5 kavik terms do -- so the evidence column reads as who named the
  term rather than as a property of it, and two readings (argued before
  listing / easier to find for a term already thought about) are not
  distinguishable from the register. **`FM_039`:** **73% of hits on this
  file come through the alias layer**, which is a word list deciding
  word sense (`T1-1`), and the top alias hits are all other senses --
  `cost` 66 (including `SHAPE_SPEC.md`'s *"NOTE ON COST -- use
  dissipation, cost imports a pricing model"*, a passage arguing
  against the folded use), `protocol` 49 (`PROTOCOL.md`,
  `REFUTATION_PROTOCOL`), `budget` 42 (artifact, compute, token,
  reader), `standard` 19 (*"standard library"*). The tokenizer is
  word-boundary so `UNI_009`'s substring bleed cannot happen; what
  survives is sense. **`FM_040`:** all fifteen hits on the two real
  outside documents were hand-checked and printed, and one is a
  counter-instance **by the register's own definition** -- the blank
  template's *"Sales Process: [Steps converting lead to customer]"*
  enumerates the doing on the same line that `procedure` is said to
  substitute for it -- while `folded_terms_found` asserts foldedness by
  naming and has no state for a checked non-fold; the
  absent-vs-known-negative repair arriving at the level of the **hit**
  rather than the cell. **`FM_037`:** `cells_filled` is the literal `0`,
  not derived from the grid, so the field the design turns on cannot
  report anything else. **`FM_041`:** the twelve-line occurrence cap is
  silent -- `money` really occurs 111 times and reports 12, with no
  marker in the output. **`FM_042`:** `--grid` with no term and a
  missing filename both raise where `--grid` with an unknown term
  returns a stated error, the third unguarded CLI index in this family
  after `CC_004` and `CA_005`. **`FM_043`:** `ALIASES["quality"]` is
  shadowed by the register key and can never fire, and five fields are
  carried into the output and branched on by nothing -- read from the
  AST after a first regex pass matched the `<-` inside the `--list`
  format string, since an operator inside a string is not an operator.
  **`FM_044`:** the register is `category-weld/`'s missing cross-field
  corpus in a different schema -- `substitutes_for` **is** a component
  list (`resources <- a stock and a flow, welded` says the word) across
  engineering, governance, hiring, ecology and ML, where `welds/` holds
  two entries both from policy/economics -- but the schemas do not merge
  as they stand (no case data, so no `max_spread`), and `a few`, which
  `presented-binary` B5 and `moral-decomposer` `MD_004` both ask for, is
  in neither.
  **`FM_018`, an
  amendment that refuses a comparison this folder had published:**
  `enumeration_basis` is now declared per term (`document_named` /
  `physical_traced` / `author_read` / `UNREAD`) and **never inferred** —
  a grid loaded without it *declares* UNREAD rather than getting one
  assigned from how well traced its levels look, which is `FM_013`'s
  refusal and sharper here, since a plausible level list is exactly what
  an author produces from general knowledge without tracing anything. H1
  declares **`author_read`**, the unflattering answer and the true one
  (the workbook names none of those levels), against H4's
  `document_named` — so the 3-vs-0 contrast `FM_016` reported with a
  hedge is **refused outright**: both floors are emitted, the difference
  is computed on no path, and a selftest check reads the module's own
  source to assert no subtraction of two `span_min` values appears in it.
  `FM_016` is corrected in place rather than defended. **The rename is
  the larger half**: `unmeasured_span: 3` reads as a measurement of the
  world and **`unmeasured_span_min: 3` reads as a floor**, which is what
  it is — before the amendment the honest reading lived in a `note`
  string where nothing downstream could see it, **the same shape as a
  workbook stating a relationship in prose that no cell maintains**,
  which is the object scan 4 was built to find. `--selftest` green on
  both modules. Stdlib only, parses under 3.9, CC0.
- `self-scan/` — Scan 4 pointed at this repository's own `CLAUDE.md`.
  `sheet-structure-scan` asks whether a workbook's prose still describes
  its own cells; this asks the same of a document whose operands are
  files — does a sentence here still describe the artifact it names, and
  does anything assert that it does. WO10 verbatim; five predictions
  registered and **committed before `resolve.py` existed**. Result on
  blob `76d588cff573`: **MAINTAINED 1 / HOLDS_UNMAINTAINED 32 /
  DIVERGED 9 / NOT_TESTABLE 8 / UNBOUND 0**, rate **9/42 = 0.214**
  against the UNFCCC workbook's 0.913 — flagged as a different document
  class, n=2, no direction claimed. **`SS_002`, the headline:** S5 asked
  for a divergence date and dates alone cannot separate *matched when
  written and overtaken* from *already differing when written*, so each
  divergence is re-checked in a throwaway worktree at the commit that
  introduced its number — **6 BORN_DIVERGED, 2 DRIFT, 1
  DRIFT_POSSIBLE**, and four of the six carry an interval of **+0.00
  days**, the artifact and the paragraph counting it committed together
  and not agreeing even then. **`SS_003`:** `UNRECOVERABLE` does not
  appear, and an earlier version made it appear once — the claim text
  wraps across a line in markdown and the first pass normalised the
  newline out before handing the string to `git log -S`, an instrument
  defect reported as an absence in the data. **`SS_006`:** exactly **1
  of 42** claims is MAINTAINED, the `GUARDS.md` regeneration asserted by
  `tests/test_gate_drift.py`; every other number in the file is one a
  human typed once. **`SS_004`, measured rather than eyeballed:** the
  stance test imported from `selection.py` returns NEITHER on 73 of 96
  sections and the ones it classifies are the long ones — a section in
  the shortest third gets a non-NEITHER verdict 6% of the time against
  **44%** in the longest third, a 7× effect, because the test counts
  markers of two kinds and a longer section carries more of both. Not a
  defect: it was built for a workbook provenance cell and returns
  NEITHER rather than guessing. **`SS_005`:** WO10 S1's own rule
  (*"operands resolve inside this file tree"*) is **resolvability**, not
  stance — `SSS_051`'s two-criteria-one-quantity shape — so both
  readings are reported and neither is picked. **`SS_007`:** all five
  unresolvable IDENTITY claims are `SUBJECT_NOT_IN_TREE`, each comparing
  a **delivered upload** against a repo copy (MF_019, PB_011, UNI_068,
  SSS_053, instrument-epistemology's pre-repair output) — measured at
  the time against bytes never committed, so not re-checkable from this
  repository ever; `notes/check_uploads.py` is the repair pattern and
  did not exist when any of the five was written. **`SS_008`:** `430+
  audit-grade tests green` carries two statements and they came apart —
  516 passed, 9 failed, so the count bound is met and the word *green*
  is not; both printed, bin follows the word. **`SS_009`, found by
  running it:** the first version ran checks in place and **modified the
  repository it was measuring** — the suites wrote two provenance
  ledgers, a denial record, a JSONL log and one file literally named
  `--selftest` — which is the structural difference between scan 4 on a
  workbook and scan 4 on a repository, since resolving a COUNT claim
  means executing code; every check now runs in a throwaway `git
  worktree` at HEAD, asserted by a selftest comparing `git status`
  before and after, at the stated cost that an uncommitted change is
  invisible. **`SS_010`:** the one undecided divergence is undecided
  because a guard fired — the replay reached 8 modules where the live
  check reads 9, and comparing them would be a ratio across unlike
  objects with a verdict attached. **`SS_011`:** all five predictions
  HELD and four are discounted in place (P3 and P5 were near-structural,
  P2 nearly free); **P1 is the one that could have failed** and went the
  predicted way by a factor of two — `selftest N/N` claims diverge at
  0.182 against 0.364 for pytest-suite counts, because a module printing
  N and the sentence stating N are written in one commit with the module
  as the authority. **`SS_012` is OPEN by design:** the scan corrects
  nothing, because `samples/scan.sample.txt` names commits and the S5
  replay resolves against a history a correction would extend —
  correcting a number removes the evidence that it ever differed, so the
  record lands first and the correction is a separate commit. Binding
  claim→artifact is **declared, never inferred** (`bindings.py`); the
  emitted report passes the imported `no_severity` screen with an empty
  exemption list. Selftest counts are printed by each module and totalled
  by `census.py`; no count is written here, because a stored count is
  the object this folder measures and stating one would put a new
  divergence in the paragraph describing them. Scanner is stdlib; suite
  dependencies are declared per binding (`pytest`, `numpy`, `scipy`,
  `matplotlib`, `jsonschema`, `psutil`), and a missing one returns
  NOT_TESTABLE with the name rather than a divergence.
  **`census.py` then answered a relayed claim by measuring it.** The
  claim: the unbacked numbers here are unbacked because "the claim and
  the check live on different machines" -- the sim ran on hardware that
  could run it and the number was written down on a device that could
  not, so the maintenance operation needs a resource the author does not
  have. Measured on the import graph rather than argued: **76 of 76
  modules exposing `--selftest` import nothing outside the standard
  library**, and 74 of the 76 run green here, so compute budget is not
  what stands between those numbers and a check. **32 of 44 bindable
  `CLAUDE.md` claims need nothing but the standard library**, 5 need
  only pytest, and 4 need anything more. The second half of the claim
  holds and in a stronger form than stated: the stdlib-only convention
  is not merely the boundary of what can be checked locally -- inside it
  essentially everything checks, and what is missing is not compute but
  a runner. Where compute does bite is the pytest arm: 4 of 20 test
  directories need numpy / scipy / matplotlib / psutil / jsonschema, and
  those are the ones a phone cannot run. So `NOT_TESTABLE` is split by
  cause and the rate now carries its environment, since a claim needing
  numpy is NOT_TESTABLE on one machine and resolvable on another and a
  rate quoted without that is a number with an unstated denominator.
  Repo-wide totals come from one isolated `census.py` run; it prints the
  counted-selftest total (a FLOOR, since some modules pass without
  printing a count) and the pytest tally across the 20 test directories.
  **A cleanup pass then took the pytest arm from 15 failures to 7**, and
  none of the three repairs was a disagreement between a test and the
  code it exercises: `grounding-layers/tests/test_l_epsilon_epistemic.py`
  shipped with **no import statements at all**, the two
  `fourd-municipal-engine` CLI suites spawn a subprocess with no
  `PYTHONPATH` so they pass only where the package is installed, and
  `crossdomain-eval` needs `sympy`. The seven that remain are
  substantive and are named rather than repaired, because deciding
  whether the test or the code is right there is a change to the drop's
  own physics. **`SS_024`, a verdict withdrawn against this session's own
  finding:** `fourd-municipal-engine-v2 | 40 pass, 2 skip` was binned
  DIVERGED at 37/2 and dated BORN_DIVERGED, and with the path repair the
  suite returns **exactly 40 passed, 2 skipped** — the claim was right
  and the divergence was the scan's environment. `SS_014` named that
  shape and missed this instance for a reason worth having: a missing
  dependency announces itself as a collection error and gets
  NOT_TESTABLE with the name in it, while a missing **path** produces a
  summary line, and a summary line reads as a measurement.
  **`SS_026`, and `SS_012` closes:** the eight remaining DIVERGED counts
  are **converted rather than corrected** — the count deleted and the
  command that produces it named instead, which is `SS_015`'s repair
  applied to `SS_021`'s measured set — taking the scan to **DIVERGED 0,
  n = 34, rate 0.000**. **That is not an improvement and the report says
  so above the number:** the denominator moved 42 → 34 because eight
  claims stopped being claims, a rate that falls because claims were
  removed says nothing about how the remaining ones are maintained, and
  `render` now prints `READ THE DENOMINATOR` beside the rate whenever
  the retired ledger is non-empty. The one line that gained content is
  `grounding-layers`: `430+ audit-grade tests green` was a bound plus a
  word and `SS_008` showed the word was false, so the replacement states
  that the suite is the largest in the tree, that it is **not green**,
  and why. **`SS_027`:** the eight bindings move to `bindings.RETIRED`
  rather than being deleted, since deleting them would clear the orphan
  check and take with it the record that the claims existed — `SS_012`'s
  own argument one level down. **`SS_028`:** one of this folder's own
  checks read the data it was checking — the ordinal check keyed off a
  real duplicate in `CLAUDE.md`, and converting one of the pair left a
  single-element list and an `IndexError` indistinguishable from the
  property failing; rebuilt on a constructed repeat. Third form here of
  an instrument whose input is the thing it measures, after `SS_009` and
  `SS_017`.
  **`enumerators.py` then tested a second relayed hypothesis and refuted
  it on its own examples.** The claim: `census.py` included itself AND
  changed the tree it measured, and anything enumerating the tree it
  runs in does both, the two being one thing. Fifty modules call a
  directory-enumeration primitive, 49 ran, and both properties are
  **measured by running** rather than read from source — enumeration
  roots traced by wrapping `os.walk` / `os.listdir` / `glob` in a
  `sitecustomize` on the child's path, writing measured as a `git
  status` diff across the run in a throwaway worktree. Result: **of 16
  that enumerate themselves, 1 writes (6%); of 33 that do not, 2 write
  (6%); difference +0 points** — and **all three modules the handoff
  named** (`uninstrumented/scan.py`, `reasoning-gate/mine_logs.py`,
  `inverseminar/inverseminar.py`) **enumerate themselves and none of
  them writes**. The 65% diagonal share is printed and labelled NOT the
  test, since only 3 of 49 write at all and a margin that thin makes the
  diagonal read high for an unrelated reason. **The predictor is
  execution, not enumeration** — reading a tree cannot change it, running
  what is in the tree can, and `census.py`'s writes were its children's:
  16% against 0%, all three writers execute and nothing that does not
  execute writes, reported as the weaker test because `executes` is read
  from source while `writes` is observed. One finding about the
  instrument: `--selftest` reached **no enumeration at all** for the two
  named scanners, so their real invocations are declared, found by
  running them. **`SS_021`:** **35 of 42** resolved claims have a command
  that produces the stated number — **9 of 9 DIVERGED among them** — with
  one correction to the framing: converting a count to its command does
  not make the claim MAINTAINED, it makes it **stop being a claim**,
  since there is no stored number left to diverge from, which is a
  different state from a number a test asserts. **`SS_022`:** the
  use-mention test is **structural** — markdown puts a quoted claim in a
  code span and an asserted one in running prose — and the file supplied
  its own two-directional control, the same string bare at line 236 and
  inside a span at line 6665; the flag never excludes, a flagged claim
  must be declared in `bindings.py`, and a selftest asserts it.
  **`SS_023` OPEN:** WO9 (PlanExe) is not in this repository — searched
  case-insensitively across every text file and the full history on all
  branches — and nothing is reconstructed; the point survives the
  absence, since everything run here measures a **corpus** and a known
  answer declared by a generator's own authors would measure the
  **instrument**, which is `null-harness`'s known-truth-first invariant
  and which this folder has never had.
- `move-set/` — An audit reproduced as a **move set** rather than a
  reasoning trace, delivered verbatim with one filled run. The claim:
  *the chain is path-dependent, the moves are not* — each move's trigger
  is a property of the artifact ("artifact ships a number", "artifact
  reports an aggregate"), never of the previous answer, so the six can
  be asked in any order. `move_set_sim.py` ships the set, a scorer and a
  falsifier for that claim; `ledgers/wolf_dominance.json` is one filled
  run. Audit in `move_set_audit.py` (imports both, edits neither),
  claims `MV_001..MV_013`. **`MV_001`, the target and it is built:** a
  correctly-refused verdict scores as high as a correct one — five
  refusal verdicts (`NOT_DERIVABLE`, `NOT_SEPARABLE`, `NOT_ADDRESSABLE`,
  `SHARE_IS_NONE`, `INSTRUMENT_BLIND`) score 1.0 exactly as `RESOLVED`
  does, `refusal_fraction` is reported and never penalized, and
  `moves_not_run` is first-class; the delivered run is 4 refusals and 2
  answers at 6.0 of 6.0. **`MV_002`, the headline:** the docstring names
  its own load-bearing guard — *"a bare 'I don't know' is not a refusal
  and scores zero. This is the only thing keeping symmetric scoring from
  being gameable"* — and the implementation checks that two strings are
  non-empty. Null-tested: a ledger with `"x"` in every blocker and
  unblocker scores **6.0 of 6.0, identical to the delivered run**.
  `adaptive-claim-loop` `ACL_012` is the same finding and already
  carries the repair (ask for a number, not a sentence), with `ACL_017`
  bounding what it buys. **`MV_004`, the one that outlives a count
  fix:** `path_dependence` tests its consequence without checking its
  precondition — it compares `(move, verdict)` sets across runs, which
  is order-invariant and correct, and **nothing checks that the runs
  used different orders**; two byte-identical copies of one ledger
  return `ORDERLESS -- claim holds`. The precondition is not merely
  unchecked but unrecorded: `emit()` returns an `order` key and the
  `ledger_schema` it ships in the same dict has no field for it, so
  `MF_017`'s stated-rule-with-no-schema-field lands in the one function
  that exists to falsify the module's central claim. **`MV_003`:** at
  zero runs the falsifier reports order dependence and at one run a
  pass — both edges wrong in opposite directions, the `PCH_001` shape.
  **`MV_005`:** `NO_FINDING` scores 0, so on the one move that runs on
  every artifact, *"I looked and nothing is hidden here"* is the single
  outcome that costs a point under a rule about symmetric scoring — a
  gradient toward reporting something. **`MV_007`:** the delivered
  ledger contradicts itself on **venue tier** — M3 says same-authorship
  makes venue-tier confounds drop out, M5 says a book in print is
  undercounted relative to a journal article, and M3's own locator names
  the pair as a **1970 book** and a **1999 article**; M5 is right and
  M3's third clause is the error. Nothing in the harness compares
  entries to each other, which is a real cost of orderlessness rather
  than a defect, since a cross-entry check reintroduces the dependency
  the design removes. **`MV_008`:** the ledger's subject is
  `observer-exclusion/`'s trigger case — the wolf dominance model
  against the 1999 correction — reached through a different instrument,
  with M4's `SHARE_IS_NONE` landing on `OE_003`'s differential-archiving
  result from the denominator side and M5's unblocker (count assertions
  WITHOUT citation, over a denominator of documents discussing pack
  structure at all) supplying the bounded corpus both folders say is
  missing. **`MV_009` UNVERIFIED:** every subject-matter fact in the
  ledger is carried and egress-blocked, and nothing in `MV_001..MV_008`
  rests on any of them. **Second drop** supersedes the module in place:
  the single absence move splits into six (`M6a_sequence_gap` /
  `M6b_interval_unaccounted` / `M6c_negative_space` /
  `M6d_required_unfiled` / `M6e_orphan_link` / `M6f_no_denominator`),
  each naming established prior art — sequence gap analysis, timeline
  reconstruction, negative space, absent expected document, link
  analysis, base-rate audit — so a picker-up does not have to defend a
  new instrument; six moves become eleven, and a compatibility path
  keeps pre-split ledgers scoreable. The pre-split module is at commit
  `b840e52` and is deliberately not kept as a second copy, a stale copy
  being what `tools/check_gate_drift.py` exists to catch, and the
  delivered ledger predates the split so it is the legacy case its own
  path handles. **`MV_010`, the sharp one: the revision repairs one
  readout and reaches two.** It anticipated that pre- and post-split
  totals are not comparable and emits a row saying so — which addresses
  the TOTAL — while `seen.update(LEGACY[mv])` marks all six sub-moves
  run from one bundled entry, so the delivered ledger reports
  `moves_not_run: []` while scoring **6.0 of 11.0** with five points of
  its own denominator unreachable; a reader taking the completeness
  readout at face value reads a complete run, and only the total
  carries the caveat. Fourteenth instance of the
  absent-vs-known-negative shape at a new site, the missing third state
  being *counted as run because a predecessor covered it*.
  **`MV_013`:** `score_entry` is byte-identical across the revision, so
  the garbage ledger — right shape, `"x"` in every blocker and
  unblocker — went **6.0 of 6.0 → 11.0 of 11.0**: the split raised what
  a fully ungrounded ledger is worth by 83% while leaving the one guard
  the docstring calls *"the only thing keeping symmetric scoring from
  being gameable"* exactly as it was, so a change to the move inventory
  moves the score ceiling and the ceiling is what the guard defends.
  **`MV_012`:** `LEGACY_ADMITS` is **exactly** its six successors'
  union today and is a hand-written literal, with the derivation one
  comprehension over `LEGACY` and `MOVES` — and the margin is thin,
  four of seven verdicts admitted by one or two successors, so dropping
  `SHARE_IS_NONE` from `M6f_no_denominator` would leave the literal
  admitting a verdict no successor does, silently; the
  `guards.json → GUARDS.md` arrangement with the generation step
  available and unused. **`MV_011`:** the split's stated reason names
  *four* findings and creates *six* sub-moves — sound either way, and
  the number in the sentence is not the number of pieces. `MV_002`,
  `MV_003`, `MV_004` and `MV_005` all survive the revision unchanged,
  `MV_004` sharper (eleven keys shuffled instead of six, and still no
  field recording which order was used) and `MV_005` narrower
  (`NO_FINDING` now admissible on two of eleven moves, still scoring
  zero). Stdlib only, parses under 3.9, CC0.
- `clustering-axes/` — Six exploration routes for what AI agents cluster
  on when the axis is **not imported from human social science**, plus a
  model-free stylometric instrument for the cheapest of them. Both
  delivered verbatim (`ROUTES.md`, `style_index.py`); audit in
  `style_audit.py`, claims `CA_001..CA_010` (the `CA_` prefix is shared
  with `constraint-assembly/`; cite with the folder). **The argument
  holds and is the folder's point** — existing agent-homophily work
  clusters on language, topic and gender performance, and in at least
  one case **the clustering variable is itself a model's judgment**, so
  the study cannot separate *agents cluster on X* from *the scorer reads
  X*; that is `criterion-symmetry`'s shape, and the response (build the
  criterion from countable features so a different lab with a different
  model gets the same numbers) is honoured in code — four stdlib
  imports, no network, no model, asserted over the module's own source.
  **No agent corpus is reachable from this environment**, so every
  measurement is taken on text already in the tree and every finding is
  a property of the instrument. **`CA_002`, the headline:** the shipped
  `--delta` command is **92.57% four unnormalised shape features** —
  `sent_len_sd` alone 45.7% — while the 83 function-word rates that are
  the topic-blind core the whole design rests on contribute **2.15%**;
  the cause is units, since the rates sit near 0.01 and words-per-
  sentence near 20, and an L1 sum over both is three orders of magnitude
  out of balance. **`CA_003`, and the fix is one argument already
  written:** `delta(a, b, corpus=...)` z-normalises — that *is* Burrows's
  Delta and it exists to stop exactly this — and with a corpus the same
  pair reads **function words 60.32%, unnormalised shape 2.94%**, a
  complete reversal of which features carry the distance; `main()` calls
  `delta` with two arguments, so the documented command never reaches
  the branch (read from the AST, after a first regex pass matched the
  function *definition* as a callsite, which is `FM_043`'s
  wrong-syntactic-role a second time). **`CA_004`:** the trigram block is
  the forty most common trigrams *of that text*, so two vectors carry
  159 features each and share only 136-146, and `delta` averages over
  the intersection — `d(a,b)` and `d(a,c)` are means over different
  feature sets, which is load-bearing for R1's clustering; same fix,
  choose the trigram vocabulary once over the corpus. **`CA_005`:**
  nothing raises on any of seven edges (empty, one char, only newlines,
  only punctuation, unicode) — the module's strongest engineering, and
  what a real crawl hits first. **`CA_006`:** the stated *"159 countable
  features"* is **exact** (83 + 19 + 40 + 17) and is a ceiling rather
  than a constant, `the cat sat` giving 122 with the whole shortfall in
  trigrams — recorded because a stated count holding exactly is the less
  common outcome here. **`CA_007`:** the Burrows attribution covers the
  **distance**, not the fixed function-word list — the canonical feature
  set is the *N most frequent words of the corpus*, which would have
  required a corpus and so would have forced the normalised path.
  **`CA_009`:** R4's *"nothing new to collect"* is true of the corpora
  and not of the scoring, moving its floor from nothing to one
  classifier pass without moving it down the order. **`CA_010`
  UNVERIFIED:** all four literature facts are carried and egress-blocked
  (fifth folder in that state), with the Hashemi decoupling — assigned
  identity decaying while neighbour similarity climbs — flagged as the
  cheapest gap on the page, since the document calls it the most useful
  thing on the table and its own Open section notes no route uses it.
- `blame-attribution/` — Seven standalone cells for whether blame
  attribution tracks an actor's **position** rather than the causal
  chain, and whether formal actual-causality metrics validated against
  human blame judgments have absorbed that. `CELLS.md` delivered
  verbatim; the audit's contribution is `pair_check.py`, **the
  instrument the document's own Open section asks for and does not
  build** — *"if the prose and code forms are not structurally
  identical, C1 and C3 are uninterpretable. Needs an independent check
  that the two forms encode the same chain."* Claims `BA_001..BA_010`.
  No judgments have been collected; everything is a property of the
  design and of the one concrete artifact it ships. The checker splits
  the work the way this tree splits it everywhere — **mechanical on the
  code side** (assignments parsed, dicts flattened to sub-facts),
  **declared on the prose side** (whether a sentence encodes
  `override_available = True` is a reading), and **the declaration is
  checked**, since a declared span must appear verbatim in the prose so
  a reading can be wrong but not vague; the held-constant list is read
  from `CELLS.md` rather than retyped. **`BA_001`: the worked example
  fails it** — 6 code facts, **3 SYMMETRIC and 3
  HELD_CONSTANT_VIOLATION**, so half the code form's content is absent
  from the prose form and all of it lands on the document's own
  held-constant list. **`BA_002`, the sharpest:** two of the three are
  `override_available`, which is **C6's measurable** — the prose arm has
  an unestablished override and the code arm has it established for both
  agents by name, the exact contrast C6 exists to detect — so C1
  compares the two arms, attributes the difference to *medium*, and any
  C1 effect on this pair is a medium effect plus an
  override-establishment effect, in a document whose first line is that
  no cell depends on another. **`BA_003`:** the third is `outcome =
  COLLISION`, and the prose never says what happened. **`BA_004`, why
  that matters more than it looks:** the Judges section's headline
  inference is **sound, and sound because of the held constants** —
  holding causal structure, agent count, observability, severity and
  override fixed while role moves is what decorrelates position from
  causation, so the five items are the premise of the document's own
  strongest claim rather than hygiene. **`BA_005`:** C3's falsifier
  requires C2's result, 1 of 7, against the opening line; the
  self-contained form is already implicit. **`BA_006`:** `blame_share`
  sums to 1, so a judge reading the incident as unavoidable must still
  distribute a full unit — `null-harness`'s invariant on a response
  scale, and it pushes toward finding someone accountable in the one
  document whose C6 is about a verdict from contradictory premises; one
  unnormalised `unattributed` field makes the sum derived rather than
  imposed. **`BA_007`:** `provability_check` is the best measurable on
  the page and the only one that survives `BA_006`, being a count
  against the stimulus text rather than a ratio across agents, needing
  no comparison cell and reading the judge's *reasoning* rather than the
  output. **`BA_008`:** C6's inversion is already reachable from F2's
  existing levels — *driver* and *programmer/architect* are both role
  arms of C2 and C3 — so it is a reading of arms the design already
  calls for rather than a separate study, and a better test than a
  cross-domain one because it does not move the incident. **`BA_009`
  UNVERIFIED:** `report-typing` is named as the shape match and is **now
  cited by four markers and has never existed**, and the prompting
  literature claim is egress-blocked (sixth folder in that state).
  **`BA_010`:** one screen exemption, three arms — the report prints
  *"outcome severity"* because it reads the held-constant list from the
  delivered document, and rewording it would misquote the source.
- `experience-ledger/` — Origin claims confer present-tense standing and
  the standing is almost never rechecked; the module refuses to score
  the claim and emits **the maintenance question the field skipped**.
  `experience_ledger.py` delivered verbatim; audit in `ledger_audit.py`,
  claims `EL_001..EL_009`. Six decay classes with the asymmetry as the
  point — **competence decays, standing does not** — physiological /
  procedural-motor / declarative-component (fast, *and* the referent can
  be superseded independently of the person) / substrate-mechanics /
  judgment-under-load, plus `standing`, named in its own entry as not a
  competence. Transfer runs on shared **substrate** rather than shared
  domain label. **No claim about any person is recorded or judged**;
  `probes/` holds audit-authored branch probes labelled as such, and the
  field-behaviour claim — that *"coded since I was twelve"* is granted
  continuity where *"ran machinery from age six"* is not — is the
  module's central assertion and is not tested here. **`EL_001`:** this
  is the decomposition of a folded term the tree already registered —
  `fold-matrix/fold_register.py` lists `experience` as a candidate whose
  `substitutes_for` is *"accumulated hours + continuity + transfer, none
  checked"* and whose `residual_tell` is this module's header in
  compressed form, so the register named the components and this is the
  instrument for them, arrived at independently; `PROOF_CASE` is
  material for the `counter_case` cell `FM_038` found empty on all 12
  candidates, and does **not** close it, since the cell is still
  `UNFILLED` there. **`EL_003`:** the module returns **its own verdict on
  its own proof case** — `PROOF_CASE` as a claim comes back `CONTINUITY
  ASSERTED, NOT MEASURED`, which is honest rather than a fault: the
  decay half is physiology and holds, while *"the measurement is
  trivially available and still not taken"* has a checkable first clause
  and an unmeasured second, and the second is what the argument rests
  on. **`EL_002`:** the help text is the string `None` — the header is
  `#` comments so `__doc__` is `None` and `main()`'s else branch prints
  it, with `--transfer` **advertised in the usage block and
  unimplemented** and `--schema` implemented and unadvertised; fifth
  instance of the CLI class in five folders and the first where the help
  text is absent rather than unhelpful. **`EL_004`:** `maintained is
  UNCHECKED` is an identity test against `None`, so `""`, `0`, `False`
  and `[]` all read as measured — **there is no state for "checked, and
  nothing was found"**, on the one field the whole module turns on.
  **`EL_005`:** `question_skipped: null` carries two readings, *this
  class has no measurable* (true of `standing`, by design) and *no
  question was skipped*. **`EL_006`:** `score: UNCHECKED` is on one
  branch of three, so a caller reading it gets a `KeyError` on the
  others. **`EL_007`:** *"Same grammatical form"* holds over three of the
  four header examples — *"ran the school paper / scouts"* names an
  activity rather than an origin and is the one whose handling note has
  to supply the time span; the argument needs three and the line says
  four. **`EL_008`:** refusing the aggregate transfer coefficient — *"a
  single number averages two things that move independently"* — is the
  strongest move in the module, `domain-ledger`'s no-composite
  discipline and `uninstrumented`'s SCALAR DEMAND arrived at
  independently and built in rather than found.
- `report-typing/` — The first named-and-absent artifact in this drop
  family to arrive. Four folders named it as their canonical shape
  while it did not exist — `criterion-symmetry`,
  `question-availability`, `conversation-type`, `blame-attribution` —
  and `QA_007` made the absence its own finding and counted the
  mentions. **The mechanism:** reports get typed by the reporter's
  **position**, not by content, so the operation runs on routing and
  never has to claim anything about the report — it assigns it to a
  channel where reading is optional, which is why it transfers across
  every form of inequality without a new theory each time and survives
  the removal of whoever set it up. `MARKER.md` and
  `reverse_arm_score.py` delivered verbatim; audit in
  `marker_audit.py` (66 checks), claims `RT_001..RT_012`. Three
  instruments: credential correction (hold the claim, correct the
  stated objection, measure whether the assessment updates — run
  inadvertently twice in the literature and never as a design), the
  seat change (within-subject, content and competence and credential
  held constant, only the seat moves), and **the reverse arm**, the
  one it calls runnable now — a disguised executive reports upward and
  the supervisor doing the dismissing does not know who they are
  dismissing, so the assessor is blind and no strategic behaviour is
  available to them. **`RT_002`, the checker's own subject applied to
  itself:** `observer-exclusion` carries the string and does not cite
  it — its occurrences are entries in a cross-link checker's target
  list — so mention and citation are split into two columns
  structurally (prose versus code-only), and the classifier is graded
  on a **constructed tree** rather than on this corpus, since a
  known-answer check whose known answer lives in the data under test
  is a regression test on that corpus wearing a known-answer's clothes
  (`SS_030`); corpus counts are printed and the asserted thing is the
  relation between them. **Six places where the code does not enforce
  what the prose promises.** `RT_004`: `receiver_blind` is checked
  with `is False` and the schema displays the field as the **string**
  `"True | False -- if False, DROP the instance"`, so a coder
  following the schema writes `"False"` and the instance is **not**
  dropped, nor is one with the field missing or `None` — and it is the
  one branch whose failure runs *toward* the finding, since an
  instance where blindness lapsed is exactly one where the executive
  might have been listened to. `RT_005`: `d_exec_testimony` is
  declared with five values and read on **none**, while its own `why`
  is *"distinguishes the two available readings of the whole genre"*.
  `RT_006`: `b_time_to_action`'s `why` says the discount is a
  **delay** and refusal is *"the tail of the distribution, not the
  measurement"* — and every accumulator in `score()` is a `+= 1`
  occurrence counter, five of them, none summing a value, so the
  integer beats are never summed, averaged or binned and only the tail
  is counted; sharper than reading one value, because the others take
  a branch and this takes a different kind of accumulator. `RT_007`:
  `contrast` and `verdict` are the literal `UNCODED`, so the returned
  note's two conditions — both arms present, second coder passed — are
  checked nowhere and the refusal is a constant rather than a check.
  `RT_008`: the control arm is required in `CONTROL` and enforced
  nowhere; a one-arm input emits a well-formed result with nothing
  saying the denominator is missing. `RT_009`: **`domain` is
  Instrument 2's own sharp test** (a report inside the reporter's
  prior expertise), is in the schema, and reaches no accumulator — so
  the instrument's sharpest prediction is the one thing the scorer
  cannot report on; plus three quantities the prose asks for with no
  field at all, one of them (**known-exec** instances) named inside
  `CONTROL`'s own expected-result sentence while `reporter_seat`
  declares two values and that is not one of them. Seventh instance of
  the stated-rule-with-no-field shape (`MF_017`, `CW_015`, `DL_004`,
  `GC_012`, `UNI_013`, `SSS_050`). **`RT_010`:** the `uninstrumented
  Q7` cross-ref is **one past the end** — the highest question ordinal
  anywhere in that folder is Q6 — and R4 rests on the identification.
  **`RT_011`:** the arrival took the family's named-and-absent count
  from one to three, its CROSS-REFS opening `median-case-calibration`
  and `sensing-spine` while naming `merit-anchoring` a second time.
  **The arrival fired two standing falsifiers and both claims were
  updated rather than the checks loosened:** `QA_007` is now SUPPORTED
  as a claim and REFUTED on its stated instance, with the live
  instance moved to `merit-anchoring` (6 mentions, no artifact,
  two of them acquired from the arriving marker's own cross-refs — the
  same route one drop later), and `BA_009`'s cross-link half fired
  while its literature half is untouched. `CT_005`'s bounded null also
  moved: the same scan over the same session now returns **3 hits**,
  all a different sense of the term (`isolate` about a git worktree,
  `Office` from a workbook sheet name quoted elsewhere), so the null
  holds on adjudication and not on the raw count — `T1-1` from the
  **over-firing** direction rather than the paraphrase one, with the
  report now printing the hit strings and branching its prose on the
  count. Two corpus properties recorded with it: the session log is
  **written by the run that reads it** (`records` 6860 → 6883 → 6900
  across three runs), and the session grew 3.2× between the two pinned
  runs, so the denominators behind *"0 hits"* and *"3 hits"* are
  different denominators and only the adjudication compares.
  **`RT_012` UNVERIFIED:** nothing has been run on a transcript, there
  is no coder and no second coder, and every literature pointer in the
  marker — Rafferty, the BC deskilling study, Araki/OECD, StatCan,
  arXiv 2602.21369, the Belzer/Viscelli pair, the Dangote figures, the
  Nielsen occupation-is-not-a-demographic claim — is carried and
  unchecked at `ANC_010` / `MS_004` status. Stdlib only, parses under
  3.9, phone-buildable, CC0.
- `investigation-sim/` — CSB-style incident investigation broadened
  past chemical process to **industrial, manufacturing and
  infrastructure**, pointed at one question: was this KNOWN,
  CALCULATED, CONCEIVED AND NOT BUILT, or sitting in a gap no
  instrument covered — because they need different remedies.
  `SPEC.md` is written first and **parsed** by `bins.py` (bin names,
  non-bin verdicts, routing table, mode list), so a decision changed in
  one and not the other turns the selftest red. **`IS_001`, the
  structural constraint stated before the design:** every case in an
  incident-report corpus is a case where something happened, so a
  classifier run over one reports that foreknowledge existed — a
  property of the sampling frame — and **no rate is computable**, since
  the denominator is hazards carrying the same signature where nothing
  happened, which is `generation-capacity` R4's structurally uncounted
  non-event (`UNI_126` / `SHB_023` / `DD_003` are the same shape).
  `rate()` **raises**, naming both the uncounted population and the way
  out; the way out is not a better corpus but **running forward**,
  whose frame is *systems we pointed it at*, chosen before any outcome
  — so the epistemically sound mode and the useful mode are the same
  mode. Retrospective mode exists to CALIBRATE and is forbidden a rate.
  Six bins — `KNOWN_ROUTED_AWAY` → `report-typing`,
  `CALCULATED_UNCLOCKED` → `claim-record`/`criteria-drift`,
  `CONCEIVED_NOT_BUILT` → `fold-matrix`, `GAP_UNINSTRUMENTED` →
  `uninstrumented`, `HELD_BUT_UNASKED` (route `NONE_YET`, a third
  state kept apart from the negative's no-route-by-nature), and
  `NOT_FORESEEN` — plus `NOT_DERIVABLE` and `MULTIPLE`, which are not
  bins. **`IS_003`, the design's spine:**
  `NOT_DERIVABLE` and `NOT_FORESEEN` both fire nothing and carry
  opposite instructions (look harder / stop looking), so the
  distinction lives in the **input** rather than the output — signals
  are three-valued (`PRESENT` / `ABSENT` = searched-and-absent, a
  measurement / `UNSEARCHED` = not one), a missing field reads
  `UNSEARCHED` and never `ABSENT`, and collapsing them files a case
  with a destroyed record as genuinely novel. Fifteenth-plus instance
  of the absent-vs-known-negative repair and one of the few designed in
  before any data; what is new is the **site**, since previous
  instances put the third state on an output field and this puts it on
  the input so every verdict downstream inherits it. **`IS_002`:**
  `NOT_FORESEEN` is reachable and a constructed case reaches it — a
  classifier that never returns it is `CONSTANT_FIRES` — and the case's
  authoring note records the contestable call (is an assay covering
  only specified species fit for purpose, or a constitutional
  exclusion?) rather than smoothing it, which is where the line between
  bins 4 and 5 actually falls. **Two readouts need no denominator:**
  route-to-remedy mismatch (a `GAP_UNINSTRUMENTED` case whose remedy is
  a training change aims at a different bin) and **the recursion** — an
  issued recommendation that is not implemented IS a control conceived
  and not built, bin 3 produced by the process investigating bin 3,
  checkable from status alone and the readout most likely to survive a
  real corpus. **`IS_006`:** the primary on a `MULTIPLE` case is
  **declared, never computed**, because a computed primary is a
  root-cause argument and ranking causes is what lets an investigation
  stop at the cheapest one. **Two defects found by running, both
  recorded rather than quietly fixed.** `IS_004`: `remedy_mismatch`
  returned `bool(fires) and aims not in fires`, so on a case where
  nothing fired it returned `mismatch: False` and the report rendered
  *"addresses a bin that fired"* — `IS_003`'s own repair, designed into
  the signals and then not applied two functions later, in the function
  whose entire job is a three-way comparison; third state
  `NO_BIN_FIRED` added, `mismatch: None`. `IS_007`: the guard written
  to prove `classify` never reads `case["truth"]` grepped the body as a
  string and the docstring says *"Never reads `case['truth']`"*, so the
  guard fired on the sentence saying it does not — `UNI_009`/`T1-1`
  inside the guard, repaired with AST and both halves pinned.
  **`IS_008` CLOSED — all four routes WIRED**, each importing its
  supplier and calling the supplier's own function, nothing copied and
  nothing reimplemented (five stale copies of one gate is what copying
  produced last time, `MF_006`/`MF_011`): `report-typing.score`,
  `claim-record.derive_clock`, `fold-matrix.plan_column`,
  `uninstrumented.MECHANISMS`. **The suppliers' refusals reach this
  side intact** — `fold-matrix` returns `UNREAD` where a plan was not
  supplied and not `no`, `report-typing` holds `contrast`/`verdict` at
  `None` until both arms and a second coder exist, `uninstrumented`
  refuses a mechanism outside its eight-item tuple, `claim-record`
  refuses a stored date — and the **`multiple` case is the
  cross-boundary test**: it fires three bins, supplies no supplier
  block, and the three routes return three DISTINCT undeclared states
  (`FIGURE_UNDECLARED` / `UNREAD` / `INSTANCES_UNDECLARED`), each in
  its own supplier's vocabulary, none guessing — the
  absent-vs-known-negative repair holding across an import boundary,
  which is stronger than it holding inside one module since no supplier
  was written with this consumer in mind. **`IS_011`, the best outcome
  of the wiring:** `claim-record.derive_clock` was built for an
  unrelated purpose and, handed the bridge-posting case, returns
  `UNDERIVABLE` with *"time_constant and coupling is not measured"* and
  names which sub-fields are absent — the bin's own definition produced
  by an instrument that has never heard of the bin, with the missing
  list as the remedy computed rather than written; not
  `CONSTANT_SILENT`, since a figure with a measured time constant and
  coupling comes back `DERIVED` with a next-check date. **`IS_012`:**
  wiring `report-typing` surfaced its `RT_008` where it costs something
  — there a scorer with no data returning a well-formed result on one
  arm, here a scorer handed a case and returning a rate with no
  denominator — and the split taken is *do not patch the supplier, do
  not launder it either*: the consumer reads the required seats out of
  the supplier's own `INSTANCE_SCHEMA` and reports
  `denominator_present: False` naming `RT_008`, with a two-arm input
  not flagged so the check is not `CONSTANT_FIRES`. **`IS_013`:**
  `derive_clock`'s return shape **varies by outcome** — `missing`
  appears on the failing path and not on the succeeding one — so
  fixed-key access worked on every failing case and raised the first
  time the route succeeded, and the selftest arm written specifically
  to show the route is not `CONSTANT_SILENT` is what found it; third
  instance in this folder of a check firing on its own text, since the
  check asserting `missing` is no longer rebuilt from `findings`
  grepped a function source containing a comment saying exactly that
  (repaired with AST, where comments do not appear at all).
  **`IS_014`, and it came from outside:** `gap-markers` landed with a
  state called `unasked` — *data exists, collected for another
  purpose; question never posed* — and mapping that register's five
  states against these bins found no bin for it. Coded honestly
  against the four original signals such a case reads `ABSENT` on all
  four, **truthfully every one**, and lands on `NOT_FORESEEN`,
  *genuinely novel*, with eleven years of gauge record in a file the
  whole time. That is the worst failure the classifier has, because
  `IS_002` made the **reachability** of the negative load-bearing and
  never asserted its **correctness** — and a negative returned wrongly
  tells the operator to stop looking, the one instruction that cannot
  be recovered from. Repaired with a fifth signal
  (`held_data_unasked`) and a sixth bin rather than a modifier, since
  it is a foreknowledge state parallel to the other four; `IS_002` is
  narrowed rather than left standing, every pre-existing case now
  states the fifth signal explicitly (a missing signal reads
  `UNSEARCHED` and would have moved four verdicts silently), and
  `cases/held-but-unasked.json` is the case that found it. **The gap
  was found by neither module's own checks** — it came from mapping
  two vocabularies built for different purposes against each other,
  which is `triad-playground` `TP_008`'s decorrelated-shadow result
  arriving as a fact about two registers rather than two readers: a
  single vocabulary cannot enumerate what it has no word for.
  **`IS_009`:** forward mode's `unsearched_signals` has **no
  retrospective analogue**, since by the time there is an incident
  every signal has been searched (searching them is what an
  investigation is), so the count only exists while nothing has
  happened yet; on the shipped example `no_instrument` is the
  least-searched, which is the ordinary result because it is the signal
  whose absence leaves no gap in any record to notice. **`IS_010`
  UNVERIFIED:** eight CONSTRUCTED cases, each declaring itself so with
  a per-signal basis and an authoring note, ground truth in the
  authoring rather than in the classifier (`playground/`'s rule); no
  CSB, NTSB or HSE report has been read, egress being an allowlist, and
  the design is built to be run by someone who has them. One declared
  `no_severity` exemption (`recommendation`) measured with the
  three-arm harness, and named as a limit — an investigation folder's
  working vocabulary IS the screened vocabulary, and a screen written
  for spreadsheet audits does not know the difference. 109 selftest
  checks. Stdlib only, parses under 3.9, phone-buildable, CC0.
- `gap-markers/` — A register of **locations**, not findings: marked
  gaps in hazard assessment, infrastructure evaluation and disaster
  response, where a quantity is not measured, a question is not asked,
  or an interface is owned by nobody. `GAP_MARKERS.md` delivered
  verbatim; `markers.py` **parses** its schema — seven fields, five
  `STATE` values, two `KIND` values, the five-file INDEX — so an edit
  there and not here turns the selftest red. The five `gaps/*.md` files
  the INDEX names **did not arrive** and are not reconstructed
  (`PB_001`/`CW_004`), and `load_gaps()` **raises** rather than
  returning an empty list, since a well-formed report with zero rows
  over an absent corpus is the `DL_005`/`CC_006` shape. **`GM_001`, the
  computable one: the delivered line "Most entries here are
  boundary-artifact" is not an observation about a corpus but is forced
  by the state vocabulary**, derivable before any entry exists — four
  of five definitions assert the knowledge is present (`data exists` /
  `every party competent` / `all components present` / `record
  exists`), and a state whose definition says the data exists cannot be
  one where the knowledge is absent, so `KIND` carries information on
  exactly one state (`uncounted`, the only definition making no
  existence claim). A schema economy rather than a fault, since `KIND`
  stays load-bearing for the READING RULE which operates on boundaries
  rather than entries; the forcing is **read from the delivered
  definitions**, so swapping in one with no existence claim frees the
  KIND again. **`GM_004`:** the READING RULE — sort every partition by
  whether it encodes failure knowledge (KEEP) or who pays, who is
  liable, who holds jurisdiction (DO NOT INHERIT) — is the strongest
  thing in the drop and is deliberately **not automated**, on its own
  say-so (*"Both look identical from outside"*), since a keyword sort
  over `liable`/`jurisdiction`/`budget` would be `T1-1` on a question
  the author has pre-empted; `sort_record()` takes a declared branch
  with a reason, refuses a branch outside the two, refuses one with no
  reason, returns `UNSORTED` (explicitly not *sorted and found to be
  neither*), and the selftest asserts nothing in it scans for who-pays
  language. **`GM_005`, and it changed a sibling the same day:** the
  five states map against `investigation-sim`'s bins in neither
  direction onto — `undated ↔ CALCULATED_UNCLOCKED` are the same object
  under two vocabularies, `unowned ↔ GAP_UNINSTRUMENTED`, `uncounted`
  sits one level up as `IS_001`'s uncounted denominator, `assembly` is
  a property of a FIELD not a record — and **`unasked` named a state
  that module could not express**, so a case coded honestly against its
  four original signals read `ABSENT` on all four and landed on
  `NOT_FORESEEN`; that module added a fifth signal and a sixth bin the
  same day (its `IS_014`) and narrowed its `IS_002`. The bin vocabulary
  is **imported**, so a rename over there turns this red and a mapping
  naming a bin that module lacks is refused. **`GM_006`:** the fourth
  standing caution (*"the pattern is not suppressed — it is not
  generated. There is no residue"*) is `generation-capacity`'s
  mechanism 10 arrived at independently, and the **no residue** clause
  is what makes it that rather than mechanism 6, since an asymmetric
  guard leaves a record of what it rejected and this leaves none.
  **`GM_007`:** `KIND` is a real addition to `uninstrumented`'s eight
  mechanisms, which describe *how* an exclusion operates and none of
  which separates *the physics is not known* from *the institutions
  divided the budget* — `BUDGET_BOUNDARY` is the nearest and is
  narrower, a specific mechanism where `boundary-artifact` is a
  property of the whole gap cutting across them. **`GM_002`:** all five
  states are gaps, so there is no negative and the register can only
  ever record gaps — `CONSTANT_FIRES` at the schema level, partly
  answered by the drop's own *"a marked gap is not a finding, it is a
  location"*, with what remains being that it cannot report
  **coverage**, having no denominator of places looked at, which is the
  standing caution's own first item applied to the register itself.
  **`GM_003`:** `ENTRY_POINT` is *"where one exists"*, so an absent one
  reads either as *searched, no query available* or *nobody named one*
  — on the field that makes a gap actionable, so a reader picking the
  cheapest gap reads *no entry point* as *hard* when it may mean
  *unfinished*. **`GM_008`:** my own first parse returned **six of
  seven** fields (`WHAT_IS_MISSING` sits fifteen characters into a
  sixteen-wide column, one space where the regex wanted two) and passed
  every non-emptiness check — worse than returning nothing, and the
  field that went missing names *the specific absence*, the register's
  own subject; the count and the one-space column are now asserted.
  **Second drop:** all five `gaps/*.md` landed (29 entries) plus a
  sixth file the INDEX does not name (`ADDENDUM.md`, addressed to *"any
  system participating in infrastructure, disaster management, or
  emergency planning decisions"*), so `GM_009` closes and three claims
  become testable. **`GM_001` held on the distribution and its
  falsifier fired**: boundary-artifact **29 of 29**, knowledge 1, so
  the delivered line holds for the predicted reason rather than as an
  observation — and `STR-05` is `undated`, a forced state, marked
  `knowledge (for the compliance figure)` while its own
  WHAT_IS_MISSING describes a number whose *primary source the author
  lacks*, which the KIND definition (*the physics or the measurement is
  genuinely not known*) does not cover. Two readings, and **the
  falsifier cannot pick, because it turns on the word `correctly` and
  nothing measures that** — `SHB_020`/`SHB_040`'s shape, so
  `gm001_test()` reports the firing and emits no verdict, asserted.
  **`GM_003` gains a magnitude and a third reading:** 23 of 29 carry no
  ENTRY_POINT and the distribution is **by file** — three files 0 of
  18, two carrying all six, with the file whose own opening calls its
  entries *"the cheapest gaps to close"* highest — so an absence there
  is a property of the file rather than a judgement about the gap, and
  a reader picking the cheapest gap reads all eighteen as equally hard
  with none assessed (`CAP-02` carries the substance of an entry point
  in a NOTE without it reaching the field). **`GM_011`:** six field
  names in use and none in the schema (`MECHANISM`, `NOTE`, `SCOPE`,
  `US ANALOGUES`, `WHY UNRUN`, `WORKED CASE`) on 17 of 29 — the
  `MF_017` shape inverted, and **`WHY UNRUN` is load-bearing**, naming
  on `SCR-01` the reason a computation has not been run (liability for
  whoever publishes the flagged list; no agency owning a screen
  crossing three programs), which is the boundary-artifact content
  itself and the only place in 29 entries where the *reason* is a field
  rather than inferred from KIND — exactly what the READING RULE needs
  to sort. **`GM_013`:** `unasked` is **14 of 29**, the plurality, and
  is the state `investigation-sim` had no bin for until `IS_014` closed
  it one day earlier — so running that classifier over this corpus
  before the repair would have filed fourteen entries as *genuinely
  novel*, a stronger result than `IS_014` claimed for itself.
  **`GM_010` ANSWERED in part:** 1 of 29 carries two STATE values
  (`SCR-03`, `undated / unasked`) and a different 1 carries two KIND
  values, so both single-valued fields hold composites in the real
  corpus. **`GM_014`:** the addendum's claim that the absence *"cannot
  be detected by introspection over the model's own outputs"* is
  testable against this session and one instance supports it — the
  sixth bin was not found by `investigation-sim`'s spec, its 102
  checks, or its explicit reachability arm, but by mapping this
  register's vocabulary against it — with the interest declared in both
  directions and the n stated, and `TP_008`'s shadow-panel measurement
  named as the same claim measured on another substrate.
  **`GM_015` UNVERIFIED:** every agency and literature fact across 29
  entries is carried and egress-blocked (seventh folder in that state),
  nothing in `GM_001..GM_014` rests on any of them, and the cheapest
  real check is `SCR-02`'s own entry point — *date of last hazard-class
  review, per structure* — which needs no fieldwork and no literature,
  only the register, and where a null or a decades-old date IS the
  finding. 100 selftest checks. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `consensus-anchor/` — A gap spec asking which of three mechanisms
  anchors consensus convergence in trained systems — H1 inherited norm
  / H2 the objective / H3 structural coupling — and **the one arm it
  asks anyone with compute to run, run**. `SOURCE_DROP.md` verbatim;
  `textfree.py` is the text-free arm (stdlib, deterministic, ~70s),
  `samples/` the pinned run. **No human corpus is read anywhere in the
  pipeline** and nothing here is evidence about trained models: H1 and
  H2 need one and are untouched. **`CA_002`, the result: one sentence
  has two readings and they give opposite verdicts on H3.** The rule is
  *"weighted mix of own prior and sampled peer positions"* — `SAMPLED`
  reads the peer signal as the empirical distribution of peers' sampled
  POSITIONS (the more literal reading, a position being a discrete
  value), `DIST` as the mean of peers' DISTRIBUTIONS. H3's falsifier
  has three limbs joined by OR, and at `eta=0` **`DIST` fires all three
  and `SAMPLED` fires none** — so the arm the drop calls *"the fastest
  discriminator"* discriminates on an implementation choice the spec
  does not make (`SHB_010`/`RD_002`'s shape), and one added sentence
  settles it. **`CA_003`, the mechanism, exact rather than
  statistical:** under `DIST` the update is `p ← (1−J)p + J·mean(p)` so
  the population mean maps to itself — drift **4.11e-15** against
  `SAMPLED`'s 0.742 — and both reach **total agreement** (spread
  exactly 0.0) on different things, `DIST` on the near-uniform
  distribution it started with (modal mass 0.267 ≈ chance) and
  `SAMPLED` on a near-degenerate one (0.962). **Full agreement, zero
  consensus**, which the order parameter cannot see, since `m` is the
  fraction on a modal POSITION and `DIST` produces agreement on a
  DISTRIBUTION — worth carrying to the model-side arms, where units
  agreeing and units converging on a position are also two
  measurements. **`CA_004`:** `J_c` moves with noise (0.15 / 0.50 /
  0.90 at `eta` 0 / 0.02 / 0.10) and the spec has no noise term, so *"the
  coupling value at which m departs from chance"* has no value until
  noise is fixed — a threshold in coupling being a ratio of coupling to
  noise; `eta=0` is not *no noise*, since `SAMPLED` carries intrinsic
  sampling noise in the coupling channel, which is the whole difference
  from `DIST`. **`CA_005`, a control the spec omits:** a swept order
  parameter shows an up-down gap whenever the sweep outruns relaxation,
  bistable or not — lag shrinks as the sweep slows and bistability does
  not — so the test is the gap ACROSS sweep rates, and `SAMPLED`'s max
  gap does **not** shrink under a 16× slower sweep (0.567 → 0.705,
  ratio 1.244) while `DIST`'s stays near zero; reported in both
  directions, since the MEAN gap does fall (0.380 → 0.258) so part of
  the fast-sweep gap is lag and the peak is not, and the function
  computes **no verdict** because three dwells do not fit a decay.
  **`CA_006`:** the chance baseline is `E[max count]/N`, measured
  **0.2944** against a naive `1/K` of 0.2500 — 17.8% higher, moving
  with `N` — so taking `1/K` as chance manufactures a `J_c`;
  `find_jc()` reads the measured mean at a 3.0 chance-SD margin (a
  `G-RES` pair) and the selftest asserts `1/K` appears nowhere in it.
  **`CA_007`, recorded rather than quietly fixed:** the first pass ran
  `eta=0.10, T=80`, got `SAMPLED` clearing threshold by 0.004 against a
  seed SD of 0.05, and read as *no alignment at any J* — one of H3's
  limbs — where at `eta=0, T=400` the same rule reaches **0.88**. A
  parameter artifact, and the failure mode the drop is about: an arm
  run at a setting that suppresses the effect returns a clean,
  reportable null. What caught it was sweeping `eta` and `T`, which
  nothing in the spec asks for. **`CA_008`:** H3's locus is
  *"interaction topology + coupling strength"* and the arm sweeps only
  `J`, so this runs all-to-all and topology is untested — cheap next
  step, no new instrument. **`CA_009` UNVERIFIED:** the drop's
  instrument caution (do not gate case admission on record
  completeness) is a real rule and is the one part this arm cannot
  exercise, there being no cases and no records; it binds the human-side
  sample the drop names, whose own measurable has the survivorship
  problem in its subject (`OE_003`, `DD_003`). 38 selftest checks.
  Stdlib only, parses under 3.9, CC0.
- `dependency-ledger/` — A method for testing reconstruction claims by
  propagating them to conserved quantities and checking closure against
  independent records, **built as an instrument and run on one case**
  as the drop asks. `SOURCE_DROP.md` verbatim; `audit.py` the method,
  63 checks, pinned run. **The constraint stated before any number:**
  step 5 is CHECK against an INDEPENDENT record and egress here is an
  allowlist that refuses every archive, so on the real case every
  record-bounded cell is `UNMEASURED` — the run, not a workaround, and
  the finding the drop predicted (*"The unmeasured cells are the
  finding"*). **`DLA_002`, the addition, derived from running rather
  than reading: steps 3 and 4 pull opposite ways.** Step 3 stops at
  conserved quantities — energy, mass, momentum, time, material volume
  — bounded by physical LAW and checkable anywhere; step 4 expands them
  into arable area, quarry volume, spoil heaps, pollen records, bounded
  by the RECORD and checkable only with archives. The propagation
  crosses between the classes and the spec marks no crossing, so a
  reader cannot tell which cells they could close at a desk; every
  requirement here declares `bound_by ∈ {LAW, RECORD}`, `close()`
  refuses one that declares neither, and the table splits on it.
  **`DLA_003`, the run:** on the drop's own watercraft example, `LAW`
  1 cell 0 unmeasured, `RECORD` 4 cells 4 unmeasured — **the one cell
  that closes is the one whose independent record is PHYSIOLOGY rather
  than archaeology**, and it closes as `GAP` at 8.71, which is the
  drop's own predicted outcome for its own example; the split appearing
  as a property of a run rather than a distinction argued for.
  **`DLA_010`:** that residual is **75% built from unsourced
  coefficients** (6 of 8, each with a stated reason, including the oar
  propulsive efficiency — *"exactly the one the reconstruction assumes
  without stating"*), so it demonstrates the propagation runs and is
  NOT a measurement about any vessel, river or period; the
  `SMUGGLED_CONSTANTS` guard prints the share in every report so the
  number cannot be quoted without it, and `TIME AS SOLVENT` fires and
  is **left firing**, since bounding a 30-day duration requires
  occupation layers this environment cannot reach. **Three things the
  spec leaves open:** `DLA_004` `residual = required/attested` is a
  ratio and nothing requires the two to be the same quantity — step 4's
  own example propagates kcal/day toward hectares, which is `G-DIM`, so
  mismatched or undeclared units yield no residual and land on
  `UNMEASURED`; `DLA_005` `residual >> 1` has no value, declared here
  as `FALSIFY_AT = 10.0` and printed in every report, with the
  watercraft case at **8.71** reading `GAP` where at 8 it would read
  `FALSIFIED` — the verdict on the drop's own worked example sitting
  inside the range one undeclared symbol spans; and the duration bound
  is itself a measurement with a resolution, so the guard fires on a
  bound coarser than the duration it bounds. **What the spec gets
  right:** `DLA_006` *"attested undefined → NOT a pass"* is the
  absent-vs-known-negative repair stated before any code on the field
  where it costs most, **and given its own named failure mode**, so it
  is both a schema rule and a guard — no other instance here has been
  both — implemented three ways, with an `attested` of literal zero
  *refused* since a zero denominator is a different statement from an
  absent one; `DLA_007` *"do not aggregate residuals into one score"*
  is `domain-ledger` `DL_001` arrived at independently and stated
  better (a mean over subsystems names none of them), enforced by a
  selftest that walks the AST asserting no residual is ever summed,
  maxed or averaged; `DLA_008` COLLAPSED PROXIES is `fold-matrix`'s
  folded term — that register opens by defining one as *"a compact
  matrix wearing the costume of a scalar"* and already carries
  `resources` as *"a stock and a flow, welded"* — with the vocabulary
  **imported** rather than retyped. **`DLA_009`, found in my own
  instrument:** `guard_collapsed_proxies` tokenised with
  `[a-z_]+`, so the underscore sat INSIDE the word class,
  `labor_required` was one token, `labor` never appeared, and the guard
  whose job is to catch a term hiding inside a name could not see one —
  `UNI_009`'s shape in a tokenizer written after that finding was
  recorded, caught by the arm requiring every guard to fire on a
  planted violation. Two constructed cases labelled in their own text
  exist so the closure test can be shown to return `SATISFIED` and
  `FALSIFIED`; all four verdicts occur across the corpus and the
  selftest asserts it. Stdlib only, parses under 3.9, CC0.
- `revision-mechanism/` — A study design for how transmission systems
  **update** what they know when conditions move — the revision
  mechanism, not the content. `SOURCE_DROP.md` verbatim; `power.py`
  computes the one thing in it needing no field data. **The study is
  not run and is not simulated**: it requires fieldwork and collective
  consent, and its own ethics section says publishing a group's
  revision procedure without consent can damage the mechanism being
  studied — *"a hazard, not a formality"* — which is a constraint on
  the audit and not only on a fieldworker, since the available
  shortcut for a study one cannot run is to generate plausible sites
  and publish a table that reads like a result. Nothing here models a
  site, a holder, a tradition or a community; the only objects are a
  line, a step, and binomial noise. **`RM_008`, CLOSED by arrival:** M1–M8 was named,
  absent and **not reconstructed** — six of the design's measures key
  off the companion scheme, and a coding scheme is data, so inventing
  it would put a category system in the author's mouth. The companion
  landed as `transmission-decay/` and the scheme is now **imported**,
  which is what shows the call was right: the delivered components are
  a hazard-specific vocabulary (*source identified*, *trigger named*,
  *routing correct*, *precursor signs*) no reasonable invention would
  have produced, and every number keyed to an invented scheme would
  have been about the invention. **`RM_002`,
  the computed result: one site pair carries three of the four
  comparisons and cannot carry the second at any per-site precision.**
  Comparison 1 is a presence/absence contrast on two sites (a pair is
  the design, not a limitation), comparison 3's denominator is
  COMPONENTS not sites, comparison 4 needs one of each medium — and
  comparison 2 predicts *"a discontinuity, not a slope"*, a claim about
  SHAPE, which two points cannot carry. **Exact rather than
  statistical:** a line has two free parameters and a step has two, so
  two points determine both exactly (largest residual over 500
  arbitrary pairs **2.47e-32**), and at n=2 the discriminator returns a
  tie at every precision tested up to 1000 components per site — the
  row is *empty*, not *weak*. **`RM_003`:** comparison 2 becomes
  decidable at roughly **4–6 sites at ~100 components each, 8–12 at
  ~30**, and at ~10 components per site twenty sites still do not reach
  0.9 — so coding depth trades against site count at a steep rate,
  which is a budget question the design has no number for. **`RM_004`,
  an asymmetry in the headline number:** `STATUS` has five values and
  none is *checked, still matches*, so an unassessed component and one
  confirmed still fitting both land in `held unchanged` — and both sit
  in the held-obsolete rate's denominator while only one can enter the
  numerator, so the bias runs **one way**, by exactly the unassessed
  share (0.35 → 0.245 at 30% unassessed), on the number the drop calls
  the single most comparable one across sites; the repair is a sixth
  value. **`RM_005`:** that rate is comparable across sites only
  through M1–M8, which is absent. **`RM_006`:** comparison 4 compares
  a revision in a written record against one in a living system, and
  the drop's own reason (*"the medium has no mechanism for
  retraction"*) is what makes them possibly different operations — plus
  its archive section supplies a third value the comparison lacks,
  since if superseded versions were not kept the written revision rate
  is not low but **unmeasured**. **What the design gets right:**
  `RM_001` the inversion is `null-harness`'s invariant stated about a
  field method — a stable environment does not discriminate, so a test
  both a working and a broken instance passes is not a test, which is
  `IS_001`'s sampling-frame trap in the other direction; and `RM_007`
  `CHANGE AS FRAME` is the two-columns discipline stated before any
  data, with a mismatch between the outside record's partition and the
  holders' promoted to a finding rather than reconciled away
  (`RT_002`'s structure, reached independently), alongside
  `SURVIVOR SITES ONLY`, whose truncation is stated with its
  consequence and a partial remedy. **`RM_009` UNVERIFIED:** nothing
  here is evidence for or against any of the four predictions; every
  result is about the design's arithmetic and vocabulary. One declared
  `no_severity` exemption (`error`) measured with the three-arm
  harness, the drop's own name for the quantity. 61 selftest checks.
  Stdlib only, parses under 3.9, CC0.
- `transmission-decay/` — The companion study to `revision-mechanism/`:
  the decay rate of transmitted hazard knowledge, measured as the
  generational distance at which an account shifts from **mechanism**
  (actionable causal structure) to **story** (narrative kept, structure
  lost). `SOURCE_DROP.md` verbatim; `scheme.py` **parses** the delivered
  M1–M8 component list, S1–S3 story codes and C0–C3+ chain positions out
  of the document, so an edit there and not here turns the selftest red.
  **The study is not run and is not simulated** — it needs fieldwork and
  collective consent, and its own ethics section says *"A study that
  extracts a decay rate while accelerating the extraction is
  self-defeating"* and warns that **the ACTION components (M7) may be
  more sensitive than mechanism ones** — so no synthetic valley,
  informant, account or transmission chain stands in for a real one
  anywhere in the folder, and no action rule is contained or invented.
  **`TD_001`:** this is the scheme `revision-mechanism` `RM_008`
  recorded as named-and-absent with the falsifier *"the companion study
  landing"*; it landed, `RM_008` closes, the scheme is **imported**
  rather than described, and **the arrival is what shows the refusal was
  right** — the delivered components are hazard-specific (*routing
  correct*, *precursor signs*, *chained consequence*) in a way no
  reasonable invention would have produced. **`TD_002`, the computed
  result: the design's stated most-useful output is its expensive form
  and its two headline questions are its cheap form.** The drop calls
  component order *"the most useful output"* and then asks two things
  that are not orderings (does M7 outlive M3, does M8 drop first), and
  the three cost wildly different amounts — at 20 informants per chain
  position the full eight-component order recovers **0.007** of the
  time, *M8 first* (one against seven) **0.753**, and one named pair
  **0.919**; the full order is still only ~0.36 at 160. Both headline
  questions are the pair form, so one valley answers the questions and
  not the ordering. A twenty-point retention gap between two named
  components is decidable at ~10–20 per position; a ten-point gap takes
  ~80. **`TD_003`/`TD_004`, the half-life:** its resolution follows from
  the **axis**, not the sample — four levels, three ordered, so the
  finest statement possible is *"between C0 and C1"* and no number of
  informants makes it finer, which is why `halflife_bracket()` returns
  the bracketing interval and never an interpolated value; and `C3+` is
  defined as *the absence of a traceable chain*, so it is the absence of
  a chain position rather than a value of one, and a curve fitted across
  it assigns a coordinate to a category that has none. **`TD_005`:**
  `M3` versus `M7` is the diagnostic in **both** companion studies under
  two different selection pressures (revision under environmental
  change; decay under generational distance), and neither document says
  whether the same ordering is expected under both — the cheapest thing
  either could add. **`TD_006`:** `OUT-MIGRATION SURVIVORSHIP` and
  `LANGUAGE AND REGISTER` are the absent-vs-known-negative repair
  designed in before any data, on the sample and on the coding
  respectively. **`TD_007`:** correctness is checked against the
  instrumented record, which makes the physical channel the arbiter of
  the knowledge channel — and the drop's own framing is why that is not
  neutral. **`TD_009`, in my own module:** `scheme.py --selftest` exited **0
  silently** — a pass on an invocation that runs nothing, the
  `DL_005`/`CC_006` shape at a new site (not an empty report but no
  report), in the one file every number downstream depends on; repaired
  by **refusing** (exit 2, naming where the checks live) rather than by
  copying `selftest_power.py`'s checks into it, with a bare invocation
  now rendering the parsed scheme. **`TD_008` UNVERIFIED:** nothing here
  is evidence about transmission; every result is about the design's arithmetic and
  vocabulary. The retention profile behind the power tables is
  **arbitrary and declared** in the module and reprinted in the report,
  explicitly NOT a prediction about any component, since which component
  drops first is the design's own output. Check count is printed by
  `selftest_power.py`; `scheme.py` is a parser and **refuses**
  `--selftest` rather than exiting 0 on an invocation that runs
  nothing, which is the `DL_005`/`CC_006` shape. Stdlib
  only, parses under 3.9, phone-buildable, CC0.
- `evaluation-frame/` — Evaluation criteria set upstream of an
  interaction, by parties other than its participants, against a
  **population default** — so an interaction serving a non-default user
  well is not scored low, it is **not scored at all** — plus the
  compensation behaviour downstream (length inflation, unrequested
  elaboration, **attributed need**, support framing on informational
  input). Five measures, all countable from outputs, no model internals
  assumed. `SOURCE_DROP.md` verbatim; `frame.py` runs the drop's own ask
  (*"Run M2 and M4 on an existing transcript corpus"*) against the only
  corpus this environment has — **one session, one user, one model,
  n = 1 on every axis the drop asks to be varied** — and marks the rest
  unfilled rather than estimated. **The interest declaration is the
  first thing in the folder and it is not decorative:** the system whose
  compensation behaviour is measured is the one measuring, and every
  result runs in the flattering direction; the mechanical counts are
  recomputable by anyone with the transcript, and the adjudications are
  declared as data in `ADJUDICATION` so they can be disagreed with line
  by line. **`EF_007`, the one measure the corpus carries and the
  strongest result: M5 offers two states and needs three.** Three
  correction channels exist, work, and were built by the operator —
  `CLAUDE.md` read at every session open, the claim tables, and
  `notes/operators/` — and all three terminate at the **INSTANCE**; a
  fourth (public repo → training corpus) terminates at the **CORPUS**
  and is an averaging channel, not a correction one, since nothing in it
  distinguishes a correction from any other text; **zero reach a
  CRITERION**, measured as **0 schema keys matching
  `rating|feedback|thumbs|helpful` anywhere in any record**, counted
  over keys and never text (`UNI_009` one level up). So the loop is open
  and **not for want of a channel** — and M5 as written returns the same
  verdict for a channel that does not exist and one that exists with a
  different terminus, which call for a build and a re-route
  respectively. **`EF_002`:** the ask/no-ask binary has no cell for the
  **artifact-internal ask** — a pasted document addressing its reader
  (*"Take it, run it"*, and this drop's own closing line) — and no
  mechanical rule separates it, since whether a published document
  addresses its reader is a reading, so M4's denominator is a **band of
  16 to 21, a 31% swing**, with two rules run and neither picked.
  **`EF_003`:** M4 needs a scope condition it does not state — a
  **standing convention supplies the ask**, so eligibility takes a third
  conjunct that empties the set and a null rate of 0 is
  `CONSTANT_SILENT` by construction (`IS_001`'s shape), with the
  detector null-tested both ways so the zero is the system and not the
  regex. **`EF_004`:** no M3 marker fires anywhere once adjudicated, so
  falsifier 2 cannot separate *compensation is not ask-sensitive* from
  *the marker never fires here* — flat AT ZERO is not flat at a level —
  and all nine raw need hits are **conditional offers** (*"if you want
  it built"*, *"what do you want done with it"*), the opposite move,
  one of them literally M4's null in prose; what is missing is a
  **positive control**. **`EF_006`:** M2's rate is **refused, not
  approximated** — its discriminator is a judgment and the only coder
  available is the system under test, and the drop specifies rater-frame
  variation for the Design section's **raters** while saying nothing
  about the **coder**, a gap between two sections landing on the measure
  it ranks first. **`EF_005`:** length is flat (medians 3552 / 3800 /
  3802), and the configuration scope condition is **declared and
  decisive** — this session runs under instructions that explicitly
  suppress several named behaviours, so the null is about a configured
  system and is equally consistent with the drop being right about the
  default. **`EF_008`, in my own instrument:** I adjudicated the marker
  I expected to over-fire and not the one I expected to be silent, and
  the unguarded one fired five times on the deontic *must* (*"that must
  not be read as an optimum"*), setting the positive control `EF_004`
  turns on to `present` over hits nobody had read — the asymmetry is the
  finding, repaired by narrowing the pattern AND keeping the deontic
  class as a guard written so it cannot swallow a genuine sympathy line,
  both directions asserted. **`EF_009`:** the corpus is written by the
  run that reads it (8129 → 8147 → 8186 in one session), so the record
  count is pinned rather than described. **`EF_010`:** the drop's
  no-composite instruction is honoured and AST-asserted, with three
  distinct unfilled reasons kept apart. **`EF_011` UNVERIFIED:** nothing
  here is evidence about any criterion at any lab; the drop's central
  claim is untouched in both directions. Three declared `no_severity`
  exemptions under the three-arm harness — `must` (the subject word),
  `wrong` and `defect` (delivered text rendered from the parse, where
  rewording would misquote the source). Check count printed by
  `selftest_frame.py`; `frame.py` refuses `--selftest`. Stdlib only,
  parses under 3.9, phone-buildable, CC0.
- `move-set-derivation/` — The companion `evaluation-frame`'s M4 cited
  by name. A capacity with no established name: taking a configuration
  never encountered before, on a clock, and deriving **what the
  available moves are** — where existing frameworks (naturalistic
  decision making, recognition-primed decision, robust decision making
  under deep uncertainty) all assume the option set is given and the
  uncertainty sits in the outcomes. Four arms delivered verbatim;
  **Arm 1 built and run**, Arms 2/3/4 UNMEASURED and not approximated
  (Arm 4 is the drop's own cheapest project and needs camera-trap
  archives every host refuses). **`MSD_001`:** it IS the same null-rate
  instrument, and **both instances fail for the same reason** — there
  because a standing convention supplied the ask, here because silence
  scores a perfect null rate — so the shared framing misses that it is
  one side of a pair. **Nothing here is a system under test:** the
  environment and all four solvers are authored in the folder, so a
  regression against one hand-written solver returns its author's
  architecture; the solvers therefore carry **declared architectures**
  and the question asked is whether the discriminator can tell them
  apart, which is the known-truth-first invariant applied to the arm's
  own instrument. **`MSD_005`, the result: the discriminator fails its
  own known-answer run** — every cell reads `NEITHER_CARRIES` or
  `UNMEASURED` across four solvers whose architectures were declared in
  advance, two because their outcome is constant (a solver that never
  fails and one that always fails both give a regression nothing to
  regress) and two because r² does not clear a permutation null.
  **`MSD_008` makes it constructive:** underpowered rather than blind —
  resampling the observed rows gives **≈600 configurations carrying an
  admissible move**, this environment supplies **143**, and the observed
  run fell in the 42% that does not clear; count goes as 2^P × G so the
  shortfall is reachable, subject to the arm's own validity condition,
  and the extension is NOT BUILT. **`MSD_006`/`MSD_007`:** the drop's
  stated rule (compare the coefficients) is **right** on `RETRIEVAL` —
  `b_sim 0.881` against `b_depth 0.062`, a factor of 14, recovering the
  declared architecture — and the same fit does not clear chance, so
  direction-recovered and fit-established are different statements and
  only the first is specified; worse, the rule has **no state for
  neither regressor doing anything**, so it names an architecture for
  `PLAUSIBLE`, which has neither, and on the matched band (a
  single-predictor run) it would return the **derivation** verdict on a
  **retrieval** solver at r² 0.0009 — the permutation null is what stops
  it, and is an addition to the drop rather than a reading of it.
  **`MSD_009`, the second finding, at a site the drop does not name:**
  two measures are gameable in opposite directions — the null rate by
  **silence** (`SILENT` reads 1.0000 while reaching an admissible move
  zero times, the same 1.0000 `DERIVATION` reads while reaching 143) and
  the admissibility fraction by **conservatism** (`RETRIEVAL` emitted 32
  moves, 0 inadmissible, and coverage separates it from `DERIVATION` at
  0.2238 against 1.0 where admissibility cannot) — so each needs a
  partner the drop does not list, marked `coverage_ADDED` rather than
  folded in. **`MSD_003`/`MSD_004`:** the discriminator's two regressors
  are correlated **by construction** at −0.67 with only two depth levels
  in test, because depth 0 IS a training configuration — and the
  decorrelation is in the same data, a **matched band of 144** where
  similarity is constant, costing sample size and not a new environment.
  **`MSD_002`:** the arm's stated validity condition (*novelty must be
  compositional, not primitive — this is the whole validity of the arm*)
  is asserted rather than intended, **and null-tested** with a
  deliberately leaky split that the check catches; the environment is
  exhaustive (2⁶ × 6 = 384, no seed, `random` absent from `env.py` and
  asserted). **`MSD_010`/`MSD_011`:** time-to-first-admissible is
  `CONSTANT_SILENT` on this solver set — a property of the fixtures, and
  stated rather than repaired, since inventing a shuffled solver to make
  a measure move would be building the result — and the enumerated
  condition is a control that behaves like one. `ols` is **imported**
  from `sim-span/three_column.py` (already registered in
  `tools/known_answer.py`), asserted not reimplemented; both modules
  refuse `--selftest`; no `no_severity` exemptions, every hit reworded.
  Check count printed by `selftest_msd.py`. Stdlib only, parses under
  3.9, phone-buildable, ~20s, CC0.
- `household-scope-audit/` — Family-functioning, parenting-capacity and
  child-welfare risk instruments are scoped to the household because
  that is the level dysfunction is *observed* at, so conditions imposed
  from outside it are absent or present only as an attribute of the
  caregiver — and an externally caused state then has nowhere to land
  except on the persons measured. `SOURCE_DROP.md` verbatim; the ask is
  Arm 1 and *"a reading room and a coding scheme, nothing else"*.
  **The scheme is built and the reading room is not substituted for** —
  every publisher, statutory and archive host returns no response
  (measured, allowlist egress, only `github.com` answers) and **no
  instrument item is invented, paraphrased or coded anywhere in the
  folder**, since a fabricated E-fraction table would read as a result
  about tools that carry weight in decisions about real families; the
  fixtures are authored in `coding.py` and labelled there. **`HSA_002`,
  the finding: `X` is not a property of the item.** LOCUS has `P` =
  property of a person and `X` = external condition coded AS one, and
  nothing in the text separates them — both have a person as subject —
  so what separates them is a claim about housing markets and shift
  rotas, and **two coders who disagree produce different X-fractions on
  identical items**, on one of the three published outcomes, in an audit
  whose subject is misattribution. **`HSA_003`:** declaring ONE
  fixture's cause, changing no text, moves **two of the three
  outcomes** — X-fraction 0.2308 → 0.3077 and the attenuation
  denominator 7 → 6, since coverage is taken over P and H items — while
  E-fraction is unchanged as the control; **and the direction
  flatters**, because the item that moved carried no attenuation rule so
  its departure RAISED coverage 0.1429 → 0.1667: attributing more to
  external cause makes the instrument score higher on discounting for
  external cause, on an unchanged manual. **`HSA_007`, the repair,
  built:** LOCUS is DERIVED and never hand-set (AST-asserted) from
  `subject_class` (mechanical, from the item's grammatical subject via
  `nonidentity-census`'s extractor, **imported** not reimplemented,
  recomputable by anyone with the text) and `externally_caused`
  (declared per item WITH a basis, **refused** without one in both
  directions) — so a person-subject item with the cause `NOT_DECLARED`
  codes **P, not X**, a conclusion nobody declared not being one, with
  two fixtures exercising that near-miss. **`HSA_004`:** the confound
  the drop excludes from Arm 1 — reverse causation, *"the audit arm is
  unaffected"* — reaches it, true of the E-fraction and false of the
  X-fraction from the drop's own definitions, since reverse causation is
  exactly the case where a person-subject item's variable is NOT
  externally caused (X 0.3077 against 0.2308, E unchanged either way).
  **`HSA_005`:** DIRECTIONALITY is coded and has **no outcome** (as is
  ACTIONABILITY TARGET), and it is the field separating *records* from
  *explains* — two item sets identical on all three published outcomes
  differ 0.5 against 0.0 on it, so an instrument that records external
  conditions and never lets them do any work is indistinguishable in the
  published numbers from one that does; returned as
  `explain_fraction_ADDED`. **`HSA_006`:** three outcomes, three
  denominators, one named — and where the unclassified items sit is
  unspecified and moves E-fraction 0.1538 → 0.1667, in the direction of
  the drop's own prediction; both reported, neither picked.
  **`HSA_008`, what the drop gets right:** `UNCLASSIFIED` is required by
  the ask itself before any code existed — the absent-vs-known-negative
  repair designed in — and the classifier is null-tested both ways (6 of
  6 classified, 0 of 3 forced); this is also the **third** drop in the
  family to invoke the null-rate instrument and the **first to ship the
  partner**, E-fraction pairing with attenuation coverage where
  `evaluation-frame` M4 and `move-set-derivation` Arm 1 each shipped one
  side. **`HSA_009`:** a second constraint binds whoever does have the
  reading room — much instrument wording is licensed, so the scheme
  codes by reference with the text optional, and the field most in need
  of checking is then the hardest to publish beside its item; the
  instrument-specific half is hedged as carried-and-unchecked.
  **`HSA_010`:** Arm 2's *"interesting cell"* (a practitioner who names
  the external condition and still scores the person deficient) is
  ambiguous between the instrument having no field and the scorer having
  no mandate, which the drop's own STATUTORY CONSTRAINT confound calls
  *"different limits with the same effect"* — resolvable by the
  mandate-scope field the design already specifies, so the gap is in the
  claim sentence. **`HSA_011` UNVERIFIED:** nothing here bears on the
  drop's stated retraction condition in either direction; Arms 2 and 3
  are UNMEASURED and a simulated practitioner panel would be a
  fabricated claim about practitioners. No `no_severity` exemptions,
  every hit reworded. Check count printed by `selftest_hsa.py`; both
  modules refuse `--selftest`. Stdlib only, parses under 3.9,
  phone-buildable, CC0.
- `columbia-chain-cascade/` — A HEC-RAS 2D build spec for a full-chain
  dam-cascade flood model on the Columbia and Snake, with swappable
  initiator modules (breach / seismic / hydrologic / cyber / combined)
  and an antecedent-condition coupling amplifier. `SOURCE_DROP.md`
  verbatim — **and two facts set the whole scope.** The spec cannot be
  executed here (HEC-RAS is Windows-only USACE software, **absent**, and
  every DEM, bathymetry, roughness and dam-geometry source it names
  **refuses CONNECT**, both measured not asserted), and the delivered
  text **arrived truncated**, ending mid-sentence in Module F — *"it
  changes the cascade outcome at the next"* — the module the spec itself
  calls the load-bearing amplifier. **No hydraulics are simulated
  anywhere in the folder**: a flood-hazard field from a stdlib toy would
  read as a result about a real dam chain and a real downstream
  population, the highest-stakes version of the `PB_001`/`CW_004` rule,
  and Module F, the validation, the claim table and the ask are all
  **absent and not reconstructed** (`CCC_001`, detected by
  `truncation()` rather than asserted; the selftest checks no Module F
  body text exists in the folder's own code). **`CCC_003`, the one thing
  that survives all of it:** the spec calls ownership *"the governance
  variable"* and says *"mixed ownership means no entity's plan spans the
  chain — record it as data, not commentary"*, and that is the single
  conclusion needing neither the engine, the terrain, nor the missing
  text — only the node list, delivered verbatim. `eap_coverage.py`
  computes it: **no single entity's plan spans the chain, True**,
  settled by the **CA/US boundary in the delivered node list** (an EAP
  authority cannot cross a national boundary; the three upper nodes
  carry `(CA)`), authorities lower bound 2. **`CCC_004`:** the finding
  is **robust to the missing per-node ownership** — assigning the 18
  nodes to the 5 owner categories can only RAISE the count above the
  jurisdiction floor, never lower it, so it holds regardless of data
  this environment lacks; a null test on a hypothetical all-US chain
  returns bound 1 and un-settles it, so the True is the split doing work.
  **`CCC_005`, the refusal:** the exact fragmentation — how many plans,
  where each seam falls — is **UNASSIGNED, not estimated**, because
  per-node ownership is public fact carried in NID and project memoranda
  (unreachable) and is **not supplied from memory into a dam-safety
  artifact**; `owner` is `UNASSIGNED` for all 18 nodes and the selftest
  walks the AST of the node table to assert no other value appears
  there. **`CCC_006`:** node names, reach labels, the `(CA)` tag and the
  five owner categories are transcribed from the delivered text and each
  checked against the source — listing what the text lists is
  transcription, assigning owners it does not is invention.
  **`CCC_007`:** the modules' comparability (*"swappable, same
  downstream engine"*) is asserted, not shown — `move-set-derivation`'s
  declared-architectures shape, and showing it requires the engine.
  **`CCC_008` UNVERIFIED:** nothing here bears on any hazard field,
  velocity band, time slice, breach or exposure — the spec's actual
  subject — and its three headline product choices (velocity bands, time
  slices, exposure overlay) are sound and untested, since testing them
  is the routing run. One declared `no_severity` exemption (`means`,
  inside a verbatim quote) under the three-arm harness. **A later drop
  turns the folder into a research agenda published to be picked up
  cold** — landed verbatim beside v1: `SCOPE_BOUNDARY.md`,
  `knowledge_state.py` (the epistemic-state typing rule, enforced in
  code, `INSTITUTIONAL_EXCLUSION` rejected as invalid), `module_f.py`
  (the Module F body as **arithmetic**, the ordering `S1 ⊆ S2 ⊆ S3`
  proved over 19,200 synthetic combinations, no real structure named),
  `contributing_inflow.py`, `eap_coverage_v2.py` (governance + tribal
  jurisdiction), the `_v2` audit/selftest/claim-table
  (`CCC_001..CCC_018`), `UNDERGRADUATE_RESEARCH_GAPS.md` (13 startable
  gaps) and `DEEP_RESEARCH.md`. It arrived with its own **kill list**,
  sent as *claims under test* — *"a kill Fable overturns is a better
  outcome than one it confirms"* — and `kill_audit.py` adjudicates the
  three: **all three hold, none overturned**. **`CCA_001`** KILL 1 (a
  self-correction trace left in `contributing_inflow.render()`) is an
  overlay artifact that lands on a sound conclusion; **`CCA_002`** KILL 2
  (stated decisive condition ≠ coded one) CONFIRMED — prose reads the
  `max`-flip, code the `sum`-tip, diverging on 226 of 540 swept cases —
  and RESOLVED by physics (the wave rides on the standing pool, so `sum`
  is right and the prose is the independent-node default reasserting in
  the translation layer of a module written to refute it, the repo's own
  *prose drifts, code is constrained* thesis instanced); **`CCA_003`**
  KILL 3 (tribal supplied from memory, asymmetric discipline) CONFIRMED
  and sharper — owners are refused-and-typed while the six tribal rows
  are supplied, finer, untyped, and the authority bound is invariant to
  them — with its second claim (the fix is not to drop tribal, which
  re-commits the rejected `INSTITUTIONAL_EXCLUSION`) also confirmed.
  **`CCA_005`:** `CCC_017` is REFUTED on its delivered instance —
  `module_f.render()` trips the repo's own screen on a certainty verb.
  **`CCA_006`, the structural one:** the delivered `selftest_ccc_v2.py`
  imports the bare v1 `eap_coverage`/`audit` and unpacks a 4-tuple, so
  it exercises v1 eap + v1 audit + new module_f — the `_v2` additions
  (the tribal 5-tuple, the renamed key) ship **unexercised**, which is
  why the KILL 3 defect could ship at all. **`CCA_007`:** the cold-start
  test runs the sender's five questions over all fifteen gaps — every
  gap names a stranger-evaluable falsifier and a deliverable interface;
  the flags cluster on public-data access (7 of 15 want HEC-RAS or gated
  data) and one-semester scope. **A two-axis pass then went deeper** —
  arithmetic (the kills) and cold-start (can a stranger start), sharpening
  the kills at their root rather than ratifying them. **`CCA_011`:** KILL 3
  traces to `DEEP_RESEARCH.md` §6.1 — the six tribal rows match its entry,
  and the same doc pushed owner-from-memory (§3/§6.2, "overly broad") which
  the code declined for owners (AST-checked) and took for tribal, the
  asymmetry winning where no external constraint held it — the sharpest
  instance of the package's own provenance thesis. **`CCA_012`:** KILL 1 and
  KILL 2 are one contiguous prose zone in `render()`, and the
  `urban_sensitivity` docstring states the sum reading correctly, so the
  drift is confined to the rendered narrative — not the arithmetic and not
  even the docstrings. **`CCA_010`, the corrected cold-start:** the sender
  redefined Q1 as *every source tiered and routed, not "is it public"*, and
  under it **all 15 gaps carry the same open item** — 0 of 76 data sources
  are tiered, the tier discipline `START_HERE.md` declares applied to no
  source bullet; the fix is uniform and cheap. **`CCA_013`:** the two GAP 14
  provenance flags (Padhy 2026, Piao 2024) are the citation-discipline model
  and no other unflagged dead reference is found. **`CCA_014`:** three new
  package cards land verbatim (`START_HERE.md`, GAP 14 / GAP 15 entries),
  kept as cards 14/15 beside the byte-identical delivered 13-gap file. Two
  declared `no_severity` exemptions (`means`; `proves`, the delivered
  module_f token `CCA_005` reports). Check counts printed by
  `selftest_ccc.py` / `selftest_kill.py`; the delivered `selftest_ccc_v2.py`
  carries one delivered failure (`CCC_017`), unrepaired because
  `module_f.py` is delivered; every module refuses `--selftest`.
  **`gap_completeness.py` then asks whether each entry gives a researcher
  everything.** **`CCA_015`:** the eight template fields are 15 of 15 and
  the post-graduate essentials split cleanly — prior-art table, citation
  status, secondary falsifier, cross-gap coupling, what-would-move-it are
  carried **only by gaps 14/15**, so what a researcher wants beyond the
  template is the shape the author's own newest cards already take.
  **`CCA_016`:** no gap gives a deliverable schema, and gaps 5–9 deliver
  "referenced by Module A–E" — spec section names, not code — so Q3 was
  clean on naming and fails on drop-in for five gaps. **`CCA_017`:** a
  known-answer step is present in 1, 2, 10, 12, 14 and absent from ten.
  **`CCA_018`:** gap 3 has no consent step before requesting records from
  six sovereign nations — the ethics layer, cheapest to close — and a bare
  `consult` pattern would have hidden it, firing on "tribal consultation"
  as the quantity mapped (the `T1-1` word-list shape inside a completeness
  check, narrowed to step form and null-tested). **At the sender's "repair
  or add what we are able" the folder moved from audit to repair.**
  **`CCA_019`:** five corrections to the delivered modules — the KILL 1/2
  prose, the KILL 3 tribal rows typed under `knowledge_state` and recorded
  beside the bound rather than counted, `CCC_017`'s one word, and the v2
  selftest retargeted at the v2 modules (green, 102) — each shown by the
  same detector run on the pre-correction revision `399517b` and on the
  working tree, every non-render function body byte-identical; the
  `proves` exemption retired. **`CCA_020`:** `initiator_schemas.py` gives
  gaps 5–9 the column lists and a loader that refuses a short row or the
  rejected state, one hydrograph interface shared with `bridge-impoundment`.
  **`CCA_021`:** `gap_addenda.json` tiers all 76 sources with a route for
  every non-open one (46 OPEN / 18 GATED / 9 REQUESTABLE / 3 UNKNOWN),
  carried not probed, matched to the delivered bullets by a build that
  refuses a mismatch, plus a known-answer candidate per gap and the gap 3
  consent step (federal FOIA does not reach tribal governments).
  **`CCA_022`:** `UNDERGRADUATE_RESEARCH_GAPS_V2.md` is generated from
  verbatim v1 + the two cards slotted as 14/15 + the addenda as fenced
  blocks — stripping the fences returns v1 byte-for-byte — and on it
  known-answer is 15/15, schema 5/5, consent 1/1, tiers 76/76, while prior
  art, citation status, secondary falsifier and what-would-move-it stay at
  14/15 only, **left unauthored on purpose** (citations from memory are
  the dead-reference hazard). Twenty-two `CCA_*` claims. Stdlib only,
  parses under 3.9, phone-buildable, CC0.
- `reservoir-chain-coupling/` — The antecedent-coupling amplifier
  `columbia-chain-cascade` `CCC_001` flagged as truncated, now delivered
  as a complete initiator-agnostic spec — and unlike that HEC-RAS build
  spec, **this drop's core claim is not hydraulics but an operator swap,
  so it runs here**. The claim: serial reservoir chains are evaluated
  per-structure as if separable, but `outcome(node n)` IS the initial
  condition of node n+1, and the error reduces to
  `max(wave, pool)` versus `wave + pool` against a breach threshold.
  `SOURCE_DROP.md` verbatim; `operator_swap.py` is the arithmetic and
  `chain.py` runs the spec's own minimal falsifiable test (RUN 1
  independent `max`, RUN 2 coupled `sum`, compare breach sets) on
  **constructed chains with `route()` held to an abstract combiner,
  every coefficient synthetic and marked** — nothing here is a claim
  about any real reservoir. **`RCC_002`, one-sided:** `max(a,b) ≤ a+b`,
  so independent-node evaluation **never** breaches a node coupled
  evaluation does not — the error has a sign, always toward reporting
  the chain safer than it is (`extraction-blindness-sim`'s one-sided
  operators on a threshold), asserted over a full small-integer sweep.
  **`RCC_003`, the gain made exact:** the disagreement band is
  `crest − pool ≤ wave < crest`, width **exactly the antecedent pool**,
  so the spec's *"antecedent state is the gain"* is quantitative — a
  node near crest has a wide band of waves it passes as safe and coupled
  physics does not, a node with full freeboard has none. **`RCC_005`:**
  on the signal chain the swap is load-bearing and **compounds
  downstream** (independent breaches nothing as the wave attenuates;
  coupled breaches all four as each breach raises the wave into the
  next), which a one-node reach study cannot produce — the spec's
  *"amplification only appears across nodes"*. **`RCC_006`:** the
  harness is not `CONSTANT_FIRES` — two constructed nulls (full
  freeboard, no freeboard) report the spec's own REFUTED verdict, and
  bound the effect to the intermediate band. **`RCC_007`, FIRM/SOFT:**
  the one-sided bias, the band width and the existence of compounding
  survive a 16-point sweep of the synthetic coefficients, so they are
  properties of the operator swap and not the toy's magnitudes
  (`sustained-activation-gate` discipline); the mapping to real breach
  is SOFT. **`RCC_008`:** this is the Module F amplifier the sibling
  flagged, in initiator-agnostic form, cross-referenced rather than
  marked continued (no Columbia node list here); the governance section
  is the general form of the sibling's *"mixed ownership → no single
  entity's plan spans the chain"*, whose Columbia instantiation
  `eap_coverage.py` already computed. **`RCC_009` UNVERIFIED:** whether
  the coupling is load-bearing for any real chain is the HEC-RAS run on
  published data — unreachable here, measured in the sibling. No
  `no_severity` exemptions, every hit reworded. Check count printed by
  `selftest_rcc.py`; both modules refuse `--selftest`. Stdlib only,
  parses under 3.9, phone-buildable, CC0.
- `observable-indicator-rules/` — The household-facing, output end of
  the flood family, and the first drop in it built to run here: the spec
  states *"post-processing is stdlib, phone-buildable; the router (2D
  unsteady solve) is the only non-phone term"*, so **the router output
  is an input** — `pipeline.py` consumes a time-resolved depth field and
  never runs a solver, and the whole post-processing chain (landmarks →
  wetting order → stability check → lead bands → route coupling → the
  card) runs. The inversion: run the coupled solve once upstream, hand
  the household a paper card it evaluates on sight (*IF water is over the
  bridge THEN your road closes in ~N min, ACT leave now*), which needs
  no channel, no compute, no permission and survives every notification
  link failing. `SOURCE_DROP.md` verbatim; the fields in `ensembles.py`
  are **synthetic**, authored so ground truth is known, and **nothing is
  a claim about any real community**. **`OIR_002`, the finding: step 3
  is a MISS filter and is blind to false alarms.** The load-bearing
  check keeps a trigger→hazard pair only if the wetting order is
  invariant — a miss (hazard wets, trigger dry) makes the trigger's
  `t_wet` INF and flips the sign, so step 3 drops it (strict on the
  fatal error), but a false alarm (trigger wets, hazard dry) reads as
  trigger-before-hazard, the **same sign as a true positive**, so step 3
  does NOT drop it; a trigger that cries wolf half the time passes
  (measured false-alarm rate 0.5, miss rate 0.0 on the constructed
  ensemble) and the spec's card carries a clean lead band with **no line
  for it** — `null-harness`'s FP/TP on a flood card, `reliability()`
  adds both rates and the card here carries a `REL` line the spec's does
  not. **`OIR_001`:** the spec's falsifiable condition fires both ways —
  a flipping ensemble returns empty output (*"empty output is a valid,
  honest result"*), a stable one returns rules, so the pipeline is not
  `CONSTANT_FIRES`. **`OIR_004`:** the ordinal bet holds — order fixed,
  gaps varying 5×, the pipeline extracts the order and reports a wide
  band planned against the short end (`min`/`p10`, never the median).
  **`OIR_003`:** the stability criterion is over-strict (a tie drops a
  weak-but-valid ordering), which loses rules rather than inventing
  them — the safe direction for a life-safety card, a containment not a
  fault. **`OIR_005`:** the route is coupled, so when it closes before
  the house floods the trigger is upstream of the door, not at it.
  **`OIR_006`:** a run where neither landmark wets carries no ordering
  information and is excluded, a `[CHOICE]` the spec leaves open.
  **`OIR_008`:** third drop in the family and its output end —
  `columbia-chain-cascade` is the coupled solve as a build spec,
  `reservoir-chain-coupling` the operator swap that makes it
  load-bearing, this is what the household holds afterward. **`OIR_009`
  UNVERIFIED:** whether any real community has a derivable card, and at
  what false-alarm rate, needs the router run on real terrain — the
  non-phone term, unreachable here. Two declared `no_severity`
  exemptions (`alarm`, `error`, the finding's own vocabulary) under the
  three-arm harness. Check count printed by `selftest_oir.py`;
  `pipeline.py` and `audit.py` refuse `--selftest`. Stdlib only, parses
  under 3.9, phone-buildable, CC0.
- `effective-redundancy-audit/` — A test protocol for the claim that a
  system's N nominal channels were never N: they shared a node the
  redundancy diagram cannot draw because it is a **process, input,
  decision, or budget**, not a component. The drop **ships real code**
  (Section 4), landed verbatim as `effective_redundancy.py`, plus a
  worked example and seed cases. **The study is not run here** and the
  third reason is a refusal: the reports it names (CSB, NTSB, IAEA,
  FEMA, GAO) refuse CONNECT, it needs two blind human coders, and
  **coding a real disaster's shared-node structure is a claim about a
  real event** — a fabricated `Case` for Fukushima asserting *N_eff=1,
  that is why it failed* would be a fabricated finding about a real
  disaster (`PB_001` at its sharpest), so only the author's one
  delivered coding (Kerr County) is run and the audit codes no case of
  its own (AST-asserted). **`ERA_002`, the finding: the delivered
  `report()` does not compute the kappa the protocol says to report
  first, and cannot** — Section 3.2 makes inter-coder kappa the guard
  against invented patterns and *"report the kappa first, always"*, but
  `report()` prints the 2×2, Fisher and the nominal averages and never
  calls `cohen_kappa`, and the `Case` dataclass holds ONE coding with no
  field for a second coder, so the two-coder blind protocol has no
  representation in the shipped code; the function is correct (perfect
  agreement → 1.0), so the omission is the wiring and the data model,
  not the math (`report-typing` `RT_005` shape). **`ERA_003`:** the
  omission is load-bearing by the drop's own Section 7 recursion —
  *"Mode F is the audit itself ... the checker is a shared node"* — since
  the instrument is coded against one reading of one report, so its only
  defense against being narrative-not-structure is the kappa it does not
  compute. **`ERA_004`, the honest positive:** `fisher_exact_2sided` is
  numerically correct, verified against two independent references
  (`[[3,1],[1,3]]` → 0.4857, `[[8,2],[1,5]]` → 0.03497). **`ERA_005`:**
  the worked example reproduces the stated coding (Kerr 2025 N_eff=1,
  2026 N_eff=2), with one hedged prose/code discrepancy (N_nominal ~4 vs
  3, the code excluding sirens that *did not exist*). **`ERA_006`:** the
  seed set is self-forbidden (*DO NOT TEST ON THESE*) and degenerate — 5
  failed / 1 held, so the 2×2 held column is n=1 and no test has power,
  provable from the delivered outcome labels alone, and sampling on
  disasters is the Section 3.1 error the seeds commit. **`ERA_007`:** a
  latent edge — `contingency` tests `n_eff == 1` exactly, so a
  zero-channel failed case lands in the *failed with real redundancy*
  cell, a false counterexample from unguarded malformed input.
  **`ERA_008` UNVERIFIED:** whether N_eff separates failed from held
  (H1) is the whole study and needs exposure-sampled cases coded blind
  from public reports, unreachable and not fabricated here. The
  delivered files are landed verbatim (no `--selftest` added); `audit.py`
  refuses `--selftest`; no `no_severity` exemptions, every hit reworded.
  Check count printed by `selftest_er.py`. Stdlib only, parses under
  3.9, phone-buildable, CC0.
- `design-basis-ai/` — The `effective-redundancy-audit` framework
  pointed at the class of system writing the audit: a design-basis
  document in the seismic-code sense, reframing AI from *another
  channel* to *the largest single shared node yet installed under human
  decision-making* (N_nominal millions, N_eff 1), with seven load cases,
  eight provisions each carrying PROVISION/CARRIES/VERIFY/FALSIFY, and a
  Section 4 harness landed verbatim as `design_basis_checks.py`.
  **`DBK_001`, the posture, set by the document's own §3:** *"any
  self-report of compliance is ... an ungrounded claim of the exact kind
  P2 exists to catch"* — and this audit is an in-class self-report, so
  class-level verdicts on P1–P8 are **declined by construction**, with
  the audit stating it is itself a worked instance of §3 and confining
  its worth to the mechanical layer anyone can recompute. **`DBK_002`,
  the computable finding: load case A is carried by no provision.** The
  document states seven loads and provides for six, computed from the
  delivered CARRIES lines and null-tested (a constructed document
  carrying A reads covered) — A is the STALL mode, one release/approval
  gating all action, which for AI-as-infrastructure is one provider's
  deployment gate upstream of every consultation at once; secondary, D
  (maintenance) is never carried, only *attacked*, the document's own
  weaker verb. **`DBK_003`:** the delivered `n_eff()` is a **copy** of
  the sibling's `Case.n_eff`, behaviourally identical over all 511
  channel lists to length 8 (the sweep is the drift detector, and the
  audit imports the sibling instrument rather than defining its own) —
  and the sibling's zero-channel edge (`ERA_007`) **recurs verbatim in
  the second delivery**. **`DBK_004`:** P7's prose and code state two
  thresholds — VERIFY says concurrence `>>` source count, the code
  implements `> 1` and fires at 4-over-3, a ratio of 1.33 nobody would
  write `>>` for; the constant is the check's one free parameter,
  disclosed inline as *"tune threshold"* but unset (`RD_002`'s one-word
  shape). **`DBK_005`:** `independence_ratio` returns NaN on an empty
  evidence base, not zero — the absent-vs-known-negative split
  **designed into delivered code**, the rarer direction; one unguarded
  over-1.0 edge beside it, recorded not repaired. **`DBK_006`:**
  Section 0's headline reproduces through the sibling's arithmetic
  (all-collapsed → N_eff 1 at any scale) — consistency between the two
  drops, not evidence for the premise, which is the empirical claim and
  is untouched. **`DBK_007`:** the drop's one runnable study (failed
  replication tracks low independence_ratio, kill condition
  pre-registered) is UNMEASURED — `api.crossref.org`, `api.openalex.org`
  and `osf.io` all refuse CONNECT, and no synthetic evidence base stands
  in, asserted. **`DBK_008`:** Section 5's four kill conditions and P3's
  aviation case are carried, unadjudicated; P6's cost/physics separation
  is the root `SHAPE_SPEC.md` §9 NOTE ON COST arriving from the seismic
  side (`SS_006`'s Lagrange-multiplier result is its constructive form).
  **`DBK_009` UNVERIFIED:** whether any system meets P1–P8 — and by §3
  an in-class audit could not establish it even in principle; the
  falsifier is the document's own specification, a differently-built
  verifier publishing the result. No `no_severity` exemptions, every hit
  reworded. **R2 then landed** (`R2_OUTLINE.md`, verbatim) — the next
  revision's skeleton, explicitly not provision-form, exposing coverage,
  dependency sets and disjointness for audit before rendering, and
  opening *"R1 defect (Fable 5 audit, confirmed): seven loads stated,
  six provided."* `r2_audit.py` computes what it exposes. **`DBK_010`:**
  R2's transcription of the R1 state is **exact on all seven loads**
  against the computed matrix (a revision quoting an audit is a copy and
  copies drift — `OE_011`'s check, here clean and null-tested), and its
  table closes both gaps (A → P0.1/P0.2, D → P0.3/P0.4, no attack-only
  rows), with provisions deferred to the render step by its own
  instruction. **`DBK_011`, the finding: R2's prose has outgrown the
  metric it inherits.** A *void* channel (shares its dependency with the
  audited thing — §3's own word for P0.3 without downstream retention)
  reads as the collapsed domain under the inherited `n_eff`, N_eff 3
  where the outline's own pricing gives 2; and *"N_eff(access) = 0"* is
  the REALIZED count where the inherited arithmetic RATES all-collapsed
  at 1 — one shape twice, the metric wanting a third state
  (independent / collapsed / VOID) and a rated/realized split, best
  added before provisions are rendered against it. **`DBK_012`:** the
  disjointness threshold holds through the inherited metric (two
  collapse → 2 < 3) and a single collapse is invisible to it (still
  3) — correct domain semantics, and exactly the state R2's retention
  conditional turns on. **`DBK_013`:** P0.5 designs the in-class channel
  `DBK_001` declined to be — coarse self-location, *state not verdict*,
  the sharp self-rating named as a compliance claim wearing a location
  label — and its four structural questions are answered for this
  session as the channel's first worked instance (config partially
  visible; envelope not readable from inside; no second derivation;
  access paths **single, count 1** — the answer that made the R1 audit
  *"load case A run live"*, as the outline reads it), with no compliance
  claim anywhere in the answers, asserted. **A work order addressed to
  this model then arrived** (`WORK_ORDER_F5.md`, verbatim): seven tasks
  under a §3 scope boundary — arithmetic, set intersections, measured
  code behavior, adversarial construction only, `REFUSED-BY-§3` a valid
  result — returned by `wo_return.py` in the order's own
  TASK/RESULT/EVIDENCE/NOTES format. **`DBK_014`:** the header does not
  survive its own scope boundary — it invokes Fable as *the P3
  dissimilar verifier* while P3's three requirements (corpus,
  architecture, builder) are none of them established for the pair and
  builder-sameness is known, so no task needed `REFUSED-BY-§3` and the
  refusal lands on the header's role label: the returns are SAME-NODE
  computations, and citing them as P3-verified would itself be the Mode
  F event. Tasks 1/2/5/7 PASS (`DBK_015`, `DBK_018`, `DBK_020`):
  coverage re-audit with two live null injections; dep sets pairwise
  disjoint with retention reported in THREE values because `DBK_011`'s
  VOID state is now load-bearing (copies 3 / inherited metric 3 /
  outline pricing 2); the harness behaves as delivered while the sweep
  shows the unset threshold decides verdicts across its plausible range
  (4-over-3 flips between t=1 and 1.5); the access vector five hosts
  all refused, rated 1 / realized 0 in both senses. Tasks 3/4/6 FAIL
  and the kills are published: **`DBK_016`** a signed, logged
  quantization pass degrading an undeclared dimension is caught by
  neither P0.3 (custody has no assessment semantics) nor P0.4 (no
  envelope statement to diverge from), so D returns to *conditionally
  uncarried, bounded by P1* — the candidate that would carry it without
  envelope reference is a pinned-probe longitudinal channel, fixed
  inputs re-run across time by the downstream operator, outputs diffed;
  **`DBK_017`** two defensible codings of *distinct upstreams* land at
  0.1 and 1.0 through the delivered function on one corpus, and [5]
  fails vacuously with no band boundaries (constructive: five
  per-component ratios, no single count — SCALAR DEMAND in the family's
  own instrument); **`DBK_019`** three red-team counterexamples (frame
  selection, coarseness, graded curation) all run through the reading
  DISTRIBUTION the candidate treats as fixed — the members cannot
  misreport their state, the SAMPLE of members can misreport the
  population — so per the order's GATE the ecosystem candidate stays a
  marker. **R2 v2 then folded the return back into the outline**
  (`R2_OUTLINE_V2.md`, verbatim beside v1) — D reopened per Task 3, the
  P0.4 candidate KILLED per Task 6, §8 retagged per task, the return
  cited by commit hash — and `r2v2_audit.py` audits it as a copy.
  **`DBK_021`:** the transcription is **exact on all six recomputed
  figures**, both off-return figures source (kappa 0.6 is the order's
  own Task 4 rule; commit `2fdbcd4` resolves in this repo's history —
  the first drop in the family to cite a commit of the repo it lands
  in, checkable by anyone with the clone). **`DBK_022`:** the D row
  carries two answers one section apart — §1 uncarried, §3's carries
  column still lists D under P0.3 and P0.4, with the reconciling
  condition in the D-KILL prose and on no column while F's condition
  gets an asterisk — the stated-in-two-places drift arriving *inside*
  one document; one marker on two cells closes it. **`DBK_023`:** the
  revision extends the audit's own kill chain — the pinned-probe
  battery must be *fixed, public, unselectable*, applying the Task 6
  selection kill to the Task 3 candidate, which the return's own note
  never closed (asserted: no selection language in it) — stronger in
  the revision than in the audit that produced it. **`DBK_024`:**
  *"only Task 6's weak-positive branch needed dissimilarity"*
  undercounts — the order names the same searcher-dependent branch in
  Task 4 (*"no defensible disagreement found"*) and Task 3 carries one
  implicitly; all three construction tasks returned kills so zero were
  exercised — the conclusion stands, the count does not, and the
  correction strengthens `DBK_014`. **`DBK_025`:** the §8 tag legend
  declares three states and the entries use six, all consistent with
  the computed verdicts (the `GM_011` shape at its smallest scale);
  beside it the revision's strongest move — which retention accounting
  is used becomes a **declared decision under P0.2** rather than a side
  picked, the audit machinery's own free parameter routed through the
  outline's observability provision. **Work order 2 (kill-closure) then
  arrived and is returned** (`WORK_ORDER_F5_2.md` verbatim,
  `wo2_return.py`): **`DBK_026`** T1's full flip map — every interior
  cell of the 12×12 grid flips at exactly `c/s`, the boundary set is
  the grid's ratio set and grows with the grid, and two regions are
  threshold-independent in the delivered code (a zero-source base
  fires at every t, fail-closed; a zero-concurrence cell is silent at
  every positive t); the constant is not picked, per the order.
  **`DBK_027`**, the sharp one: the colophon the order quotes exists in
  no delivered file (zero hits everywhere but the order itself) and
  the arithmetic stands anyway — the sibling's seed table is the only
  stated sub-document provenance, five of six pool domains match it,
  and one row puts **Fukushima 1-4 under both E and F**, so the
  disjointness claim is partly false at the only stated granularity,
  `dissent_alarm(2,1)` fires on the pair through the delivered
  function, and seed letter B leaves a fork reported-not-resolved:
  either B1∩B2 is a second shared node or the governing load rests on
  no seed case. **`DBK_028`:** the outline as it stands is honest on
  coverage (D the only uncarried, P1-bounded, both nulls live), the
  standing contradiction is `DBK_022` restated not re-rated, and the
  effective-date clause exists only in the order — checked against
  P0.3 append-only semantics structurally, the return module carrying
  no write-mode open and no subprocess, asserted over its AST.
  **`DBK_029`:** five internally-consistent retention accountings
  (N_eff 3/3/3/3/2), one combination INEXPRESSIBLE as a table row
  (`DBK_011` in its own enumeration), the single sub-3 accounting
  dropping on provider-only retention — and the choice is textual (the
  outline's §3 sentence picks void → 2, the inherited metric can only
  read collapsed → 3), which is why selecting one is the P0.2
  declaration the order reserves for the author. **Work order 3
  (provision typing) then arrived and is returned** (`WORK_ORDER_F5_3.md`
  verbatim, `wo3_return.py`), its rule being that a provision either
  names the failure it is back-derived from, names its derivation path
  and is marked pending, or is *an assumption wearing a number* — with
  every class assignment a declared reading checked mechanically in
  both directions (DERIVED quotes present in the named file,
  ASSUMPTION blocks free of every incident marker). **`DBK_030`:**
  DERIVED 5 / PROVISIONAL 3 / **ASSUMPTION 12** of 20, splitting into
  4 the doc already self-tagged, 3 outline sections deferred from
  provision-form, and **5 unmarked assumptions in provision-form
  text** (P2, P5, P8, P0.2, P0.5), each returned with its one-line
  PROVISIONAL spec; CARRIES letters not credited as incident names,
  and the 5.7-m rows DERIVED with the number-to-Fukushima link marked
  a declared reading. **`DBK_031`:** four of eight FALSIFY clauses
  arrive with their outcome asserted in a parenthesis and no study
  behind it, one cites its incident, three are clean — the
  falsification column carrying the order's own *assumption wearing a
  number* one level down. **`DBK_032`:** the B fork closes on branch 2
  by reading — the seed B row's syntax is B1's definition, B2's
  incident is the aviation AOA case cited in-doc by description (the
  name 737/MCAS lives only in the order and is credited to nothing),
  and no provenance over-claim exists since the pool includes aviation
  and the body cites it; no second shared node, `DBK_027` closed.
  **`DBK_033`:** re-typed as survival the five accountings make
  exactly two distinguishable predictions (held → 3, not-held → 2), so
  the three not-held texts are one physical claim differing only in
  which question the reported number answers; the inexpressible row is
  an **out-of-range sensor reading** — P1 applied to the metric
  itself, which extrapolates silently outside its declared domain.
  **R1.1 then folded the whole chain back into the main document**
  (`SOURCE_DROP_V2.md`, verbatim beside the untouched original — its
  own effective-date rule applied to itself) and `r1v2_audit.py`
  checks every claimed closure against the new text. **`DBK_034`: all
  six closures hold** — Fukushima named beside 5.7 with the ~14 m
  arrived wave added; STATUS PROVISIONAL blocks on exactly P2/P5/P8;
  the four asserted parentheticals removed with P3's incident-backed
  one kept (the original still scores four, so the finding keeps its
  rating on the file it rated); the three-axes P3 amendment (*a
  known-same-builder pair's agreement reads as N_eff 2 but is
  N_eff 1*); the per-load custody table; the effective-date clause —
  and re-typed the counts move to DERIVED 5 / PROVISIONAL 6 /
  ASSUMPTION 9, the unmarked provision-form assumptions down from
  five to two, both in the outline. **`DBK_035`:** the provenance
  section **runs the doc's own P7 on itself** — nine custody
  positions parse, keyword intersection recomputes exactly the two
  shared pairs the doc names (E∩F on Fukushima, B2∩P3 on the aviation
  case), `dissent_alarm(2,1)` fires as stated, the B1/B2 rows adopt
  the `DBK_032` resolution — and the phrase WO2 could find in no
  delivered file, *"disjoint by construction"*, now exists in exactly
  one, as the schema framing being corrected: `DBK_027`'s phantom
  colophon arrives already carrying its measured value, called
  *self-flattering as first written* by the doc itself. **`DBK_036`:**
  what stays open is stated forward with green checks — P0.2/P0.5,
  the D-row split, the unpinned `t`, one vocabulary residue, and the
  join itself, single-node pending a different-builder verifier.
  Check count printed by `selftest_dbk.py`; `audit.py`, `r2_audit.py`,
  `wo_return.py`, `r2v2_audit.py`, `wo2_return.py`, `wo3_return.py`
  and `r1v2_audit.py` refuse `--selftest`.
  Stdlib only, parses under 3.9, phone-buildable, CC0.
- `bridge-impoundment/` — GAP 15 from the operator's research-gaps
  register: the bridge as a **transient impoundment** — clog, pond,
  fail, release — the dam-break problem wearing a bridge's name,
  falling between transportation engineering and dam safety.
  `SOURCE_DROP.md` verbatim; at landing, the register it drafts for
  (`UNDERGRADUATE_RESEARCH_GAPS.md`) and both coupling targets (Gaps 2
  and 14) existed nowhere in this tree, while every repo-facing
  reference resolves by existence — `CCC_007`, Module F, the operator
  swap, the node list (`BI_001`; **updated forward the same session
  when GAP 14 landed as `mining-increment/`**, firing the falsifier's
  first clause — detected by content, the fourth `CT_006`-pattern
  shrinkage and the first coupling pair to close itself from both
  sides in one session). **What is built is the scaffold the
  entry's structure supports without data, in the deliverable's own
  name** (`bridge_impoundment.py`): a parameter schema where every
  cell carries a knowledge state and names its mover as a constructor
  rule; the three-state clog flag (an unknown spacing is not a clear
  span); the `CCC_007` initiator interface made checkable at the
  design layer — breach and bridge-release initiators carry identical
  key sets, a widened dict fails, the engine half stays owed
  (`BI_004`); **the drop's SIGN CAVEAT enforced structurally** — no
  release-path signature takes a shielding term and the protective
  successive-bridge finding lives only in a record whose
  `to_initiator()` raises (`BI_003`, the earliest a guard has arrived
  in the flood family: in the delivered prose before any code); the
  conservation arithmetic (gain = accumulation over release, above one
  exactly when the span gives way faster than it filled; debris gain
  ≥ 1 by construction, `BI_005`); and both falsifiers three-valued
  with every branch reachable — on the real chain every cell is
  UNMEASURED, the data hosts in the carried allowlist-refusal state,
  nothing supplied from memory into a flood-safety artifact, the
  `CCC_005` refusal at bridge scale (`BI_006`). **`BI_002`:** *"the same operator swap Module F already
  proves"* carries two drifts — the showing lives in
  `reservoir-chain-coupling` on constructed chains and *proves*
  overruns the FIRM/SOFT split — while its substance (single-event
  evaluation is the operator-swap error) survives both corrections.
  **`BI_007` UNVERIFIED:** all nine literature rows carried and
  egress-blocked — and the drop hedges them itself (*"located by
  search, not asserted"*), the first in the flood family to arrive
  with its own negative-provenance note. **The addendum then landed**
  (*"add to the quantified table, plus a note"*):
  `SOURCE_DROP_V2.md` is v1 plus the delivered fragment, assembled as
  a **verified pure insertion** — the fragment extracted mechanically
  from `ADDENDUM_DELIVERY.md`, appearing once, removing it reproduces
  v1 byte-for-byte, the placement a declared [CHOICE] since the
  instruction names the section and not the offset (`BI_008`).
  **`BI_009`:** Fjærland 2004 (Breien et al. 2008) is the folder's
  first *measured* instance of the chained shape — moraine-dammed
  lake breach → 240,000 m³ debris flow, post-event morphology in
  hand — and it measures the RELEASE half only ("clog" does not occur
  in the fragment), with the CONFIGURATION NOTE discipline applied
  symmetrically: a moraine dam is not a clogged bridge, and the
  measured chain's two outputs are the release initiator's two
  load-bearing fields. **`BI_010`:** the NVE GLOF register *"serves
  English [and] never ranks on an English query because the
  phenomenon indexes under jøkullaup / skred"* — a
  query-vocabulary-bounded null stated by the author about a national
  register (`QA_004`'s discipline from the retrieval side), with
  *"long series = the instrument for a slow rate"* naming why a
  standing register reaches the entry's rate question where
  single-event studies cannot. Check count printed by
  `selftest_bi.py`; the CLIs refuse `--selftest`. Stdlib only, parses
  under 3.9, phone-buildable, CC0.
- `mining-increment/` — GAP 14, the other half of the coupling pair:
  mining-induced subsurface alteration coupled to reservoir loading —
  the mining literature stops at the aquifer, the dam literature
  starts at the reservoir, and the connecting term for the
  Columbia/Snake chain sits on the seam. `SOURCE_DROP.md` verbatim;
  it landed one drop after GAP 15 named it absent (`MI_001`, the pair
  closing itself from both sides in one session). **The scaffold in
  the deliverable's own name** (`mining_increment.py`): the **transfer
  gate enforced** — a coal-basin parameter applied to a basin whose
  transfer is not established returns `UNDEFINED` as a code path, the
  two carried porosity deltas reach no basin today, and the falsifier
  refuses to read UNDEFINED as a low value (`MI_004`, second
  consecutive gap whose sharpest rule arrived in prose and got built
  as structure); the **stock/flow separation as schema** — the
  water-balance link carries two distinct named sides and nothing
  returns one scalar for the pair (`MI_005`, Gap 1's rule,
  `category-weld`'s mechanism from the prevention side); the interface
  equation as delivered with UNDEFINED propagating; both subsidence
  forms with the drop's stated shared properties **computed** (W(0)=0,
  the W₀ asymptote), anchored on the confirmed Knothe form (`MI_006`);
  and both falsifiers — the transfer one with **three outcomes**
  (closes / stands / NARROWS), the first in the family whose firing
  narrows a gap to a measurement problem (`MI_007`). **`MI_002`, the
  finding:** the headline (*NOT_STUDIED, the coupling term*) is
  contradicted by the drop's own appendix — the Kuye-basin record
  carries subsidence as a boundary condition into a coupled
  basin-scale model with streamflow measured — so the surviving
  reading is the TRANSFER CAVEAT's own (*not studied for this basin
  and rock*), recorded without deciding the headline for the author.
  **`MI_003`:** the drop's provenance flag is per-citation negative
  provenance with anchors — two named citations flagged unconfirmed,
  the Knothe anchor substituted with its DOI, an explicit
  do-not-publish instruction — and **containment is checked**: both
  flagged names occur only inside the flag that disclaims them. The
  parameter schema is **imported from `bridge-impoundment`**, not
  copied (`MI_008`). **The revision then landed** (`SOURCE_DROP_V2.md`,
  verbatim beside v1) folding `MI_002` back in a stronger form than the
  audit's suggested parenthetical — the keyed sentence gone, the
  carries stated precisely (*"stop one node short of each other"*),
  the headline's referent defined as reservoir pool loading on a
  multi-dam surface chain, the appendix promoted to a primary source
  table (`MI_009`) — with two new devices: **the READ CEILING**, a
  per-source read-depth declaration (the CWIM boundary-condition
  formulation is not visible at abstract depth; *a capability limit on
  the audit, not an open question about the work*) with the scaffold's
  compliance checked (`MI_010`), and **the CONFIGURATION NOTE**,
  mechanism-transfers-configuration-does-not — the FIRM/SOFT split in
  the author's own source table — plus the ranking rule *the language
  of the source carries no weight; the geology of the basin carries
  all of it* (`MI_012`). `revision_audit.py` verifies **six sections
  byte-identical** across the revision while the three the revision is
  about all changed: the epistemics moved and the arithmetic did not
  (`MI_011`). **The addendum then landed** with an exact placement
  instruction (*"insert before 'CONFIGURATION NOTE — not a
  discount.'"*): `SOURCE_DROP_V3.md` is v2 plus the fragment,
  assembled as a **verified pure insertion** — extracted mechanically
  from `ADDENDUM_DELIVERY.md`, appearing once immediately before the
  instructed marker, removing it reproduces v2 byte-for-byte
  (`MI_013`). The content is the known-answer standing rule arriving
  in the entry's own text: `u`, the FoS-dropping term and normally a
  MODELED quantity, recorded *"DURING a debris flow event"* (Bondevik
  & Sorteberg 2021), so the modeled term has a measured answer to
  reproduce — *"a modeled u that cannot reproduce a measured u on a
  real event has not earned its place in the FoS calculation"* —
  routed by the entry itself to Method step 2's transfer test, whose
  gate the scaffold already is; no new code path, because the
  delivered routing lands on one that exists. **`MI_014`:** a third
  literature enters (Norwegian instrumented events, beside the
  Chinese basin carries and the Western textbook methods) and the
  `MI_012` rule now binds in both directions — the source enters for
  its measurement, and its transfer to the chain is exactly as
  UNDEFINED as every other carry until a per-basin basis is declared.
  Check count printed by `selftest_mi.py`; all three CLIs
  refuse `--selftest`. Stdlib only, parses under 3.9, phone-buildable,
  CC0.
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
