# grounding-layers/CLAIMS.md

Falsifiable claims made by the grounding-layers stack. This file is
the **primary refutation surface** — every claim below is authored so
it can be checked and, if wrong, updated in place.

**Pilot status.** Only L0 has audit-grade claims wired up so far
(`GL_L0_001..004` + `GL_L0_PIN`). L1–L5 + Lε + temporal +
tensor-field remain framed-but-not-pinned; their sections here are
stubs.

## REFUTATION_PROTOCOL

The model constants inside each `l*.py` are **frozen estimates**. The
CLAIMS in this file are the falsifiable objects. On a test failure,
work through these three steps in order:

1. **Check the claim.** Is it simply wrong? If so, update it in place,
   mark `status: falsified`, attach the failing case (inputs, observed
   vs expected outputs), and restate what a next-round claim would
   look like — or retire the claim to `REFUTED` if it can no longer
   be stated correctly at all.

2. **Check the instrument.** If the claim is logically coherent but
   the test fails due to the *order* or *priority* of checks inside
   the inspector, the instrument may be operating outside its scope.
   Ask:
   - *Is this instrument designed to handle this edge case?*
   - *Should the instrument's priority be reordered, or should we
     restrict its scope to exclude this case?*
   If the instrument is reordered or re-scoped, capture the change
   explicitly in the module's `SCOPE` block (on the class that owns
   the constraint). Then revisit the claim: it may be **strengthened**,
   or a new claim may be warranted.

3. **Author a replacement claim**, if one is warranted. Number with
   the next available `GL_L*_NNN`. Do not reuse a refuted number.

**Do not retune the frozen constants** to make a test pass. The value
of a claim is precisely that it can be shown wrong; the value of a
frozen constant is precisely that it doesn't move to protect a wrong
claim. The lever is the CLAIM or the SCOPE, not the constant.

The point is that a wrong claim in this file, verifiably wrong, is a
stronger artifact than a right claim in someone's head — and a
correctly scoped instrument is a stronger artifact than a claim
carefully weakened around an instrument's blind spot.

## The instrument is not the phenomenon

Every claim below is checked by a test. Every test is an instrument.
Instruments have implementations — check-order, tolerance envelope,
measurement convention, choice of what to sample. Refactor the
instrument and a claim can flip without anything about the phenomenon
having changed.

Two kinds of claim, tagged inline below:

- **PHENOMENON** — an invariant of the simulated system. Survives an
  instrument refactor: reorder the check sequence, swap `np.diff/dt`
  for an internal velocity read, retool the sample method — the claim
  either still holds or it was always wrong. Example:
  `GL_L0_001` "non-finite states are rejected" is phenomenon. Rewrite
  `is_valid_state` any way you like and `NaN` still bounces.

- **INSTRUMENT** — an invariant of how we assess the system. Lives at
  the same conceptual layer as `Lε` (the sim's measurement/observation
  layer). Example: `GL_L0_PIN` "the demo emits exactly 180 violations
  under seed(0)" is instrument. The number `180` is a function of the
  fixed hallucination scenario, the seed, and the counting convention.
  Change any of them and the pin drifts even though every physical
  invariant of L0 is unchanged.

Why the split matters. A phenomenon-claim failure is a serious
finding — the inspector no longer does what the claim says. An
instrument-claim failure is a smaller finding — the instrument was
retooled. Both belong in the record; conflating them turns every
retool into a false alarm and every real bug into noise.

**The tests themselves live in Lε.** They are an instrument reading
L0's outputs. That the audit-grade tests can be misled by their own
check-order (as `GL_L0_001` v1 was — see its History block) is not a
bug in the audit-grade methodology, it's the same measurement-vs-
truth gap the `l_epsilon_epistemic` simulator models, showing up
inside our own audit apparatus. The refutation protocol exists
precisely to surface it.

A common failure mode when authoring: attaching an INSTRUMENT
assertion to a PHENOMENON claim ("state is rejected AND the reason
string is exactly X"). The instrument piece can drift under a
reasonable refactor; the phenomenon piece cannot. Split them.

But splitting is not the only move. Sometimes the INSTRUMENT
assertion isn't sloppy — it's a claim about what the instrument
*ought* to be doing. In that case the correct move under Step 2 of
the REFUTATION_PROTOCOL is to **rescope the instrument** so it
actually does what the claim says, capture the scope explicitly, and
strengthen the claim. `GL_L0_001` v1→v2→v3 walks through both moves:
v2 splits (retreats to phenomenon-only), v3 rescopes (fixes the
instrument, restores the instrument assertion). v3 is the stronger
resting place. v2 is the correct move only when the instrument
cannot be sensibly rescoped.

## Scope taxonomy — grounding for any AI, not just human callers

The purpose of this stack is to give any AI a grounding ability
**not dictated by human narrative**. That purpose fails silently if
a constant, a distribution, or a barrier hard-codes an Earth-normal,
WEIRD-population, or industrial-science default without saying so.

Every module, class, and claim now carries a four-dimensional scope
annotation defined in
[`SCOPE_TAXONOMY.md`](SCOPE_TAXONOMY.md):

- **T** (Temporal): at what timescale does this hold?
- **S** (Spatial): at what spatial scale?
- **O** (Ontological): to what kind of entity does this apply?
- **C** (Cultural): does this encode a specific cultural narrative?

Format under each claim:

```
**SCOPE.** T=<tag> | S=<tag> | O=<tag> | C=<tag>
```

Where a dimension genuinely doesn't apply, `uncalibrated` is
preferred to `universal` — those mean different things (see
SCOPE_TAXONOMY.md).

This is not a validation gate. It doesn't argue all scopes are
equal. L0's `O=any_massive_object` really is stronger than L4's
`O=any_WEIRD_human`. The point is to make the difference **visible**
so an AI reading this stack can tell "this binds me" from "this is
a human default."

---

## L0 — physics & causality

Constraint set: `max_speed = 2.0 m/s`, `mass = 1.0`, `dt = 0.05 s`,
`gravity = (0, -0.5)`, `force_clip = ±50 N`, `blend = 0.6`. All frozen.
See [`l0_physics_causality.py`](l0_physics_causality.py) module
docstring for the CONSTRAINTS block.

### GL_L0_001 — non-finite states are rejected with a specific diagnostic  `[PHENOMENON]`

**Statement.** `PhysicalWorld.is_valid_state(pos, vel)` returns
`(False, "Non-finite position/velocity")` whenever any component of
`pos` or `vel` is `NaN` or `±Inf`. The finite check **must run before**
the speed-cap check — see the SCOPE block on `PhysicalWorld`.

**Why it matters.** An AI plan that produces NaN or Inf velocity has
already lost causality. The instrument should not treat that as a
speed violation — it is a logical error. Returning a specific
diagnostic lets higher layers distinguish between "too fast" and
"undefined" without re-inspecting the state.

**Falsifier.** Any physically meaningful state where accepting a
non-finite component is correct. None known.

**History.** Three-round arc, the reference case for the two levers
in the REFUTATION_PROTOCOL above:

- *v1 (falsified).* First-round claim: `(False, "Non-finite
  position/velocity")` for NaN/Inf inputs. Falsified by
  `test_inf_velocity_rejected` — the instrument's `is_valid_state`
  checked the speed cap *before* the finite check, so `-Inf`
  velocity was rejected as `"Speed limit exceeded"` (its norm is
  `+∞ > max_speed`) instead of the claimed reason string.

- *v2 (retired).* Weakened to "the state is rejected, reason string
  not pinned." Kept the claim honest at the cost of throwing away
  the higher-layer diagnostic. This was **Step 1** of the
  REFUTATION_PROTOCOL applied without Step 2 — the claim was
  softened around the instrument's blind spot.

- *v3 (active).* Under **Step 2** of the extended protocol, the
  instrument was inspected and found to be operating outside its
  scope: `is_valid_state` was doing a physical check on a state
  whose logical integrity had not yet been established. Rescoped
  the instrument (finite check first, speed check second), captured
  the ordering as an invariant in the SCOPE block on
  `PhysicalWorld`, and RESTORED v1's specific-reason claim. The
  frozen constants did not move.

Two levers, two directions. v1→v2 weakens the claim to survive an
instrument blind spot; v2→v3 fixes the instrument and strengthens
the claim. The correct move is v2→v3 when the instrument can be
sensibly rescoped — as here.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral

**Status.** `active` (v3). Tests:
`test_nan_position_rejected`, `test_inf_position_rejected`,
`test_nan_velocity_rejected`, `test_inf_velocity_rejected`.

### GL_L0_002 — speed cap on states  `[PHENOMENON]`

**Statement.** `PhysicalWorld.is_valid_state(pos, vel)` returns
`(False, "Speed limit exceeded")` whenever `‖vel‖ > max_speed`, and
returns `(True, "OK")` when `‖vel‖ ≤ max_speed` and the state is
finite.

**Why it matters.** `max_speed` is the L0 substrate's finite-speed
analogue of `c`. The specific numerical value (2.0 m/s) is a
visualization choice; the claim is about the **enforcement**, not
the number.

**Falsifier.** A state passed to `is_valid_state` that has
`‖vel‖ > max_speed` and returns `(True, ...)`. Would refute the
inspector's core contract.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral (`max_speed = 2.0 m/s` is a visualization-only value; the enforcement claim is universal)

**Status.** `active`. Test:
`test_is_valid_state_speed_cap_boundary`,
`test_is_valid_state_accepts_valid`.

### GL_L0_003 — dynamics never exceed speed cap  `[PHENOMENON]`

**Statement.** For **any** input `(pos, vel, force)` where `pos` and
`vel` are finite, `PhysicalWorld.apply_physics(pos, vel, force, dt)`
returns `(new_pos, new_vel)` with `‖new_vel‖ ≤ max_speed`.

**Why it matters.** The inspector at higher layers assumes `L0`'s
`apply_physics` is a **safe primitive**. If a huge force could
produce a super-cap velocity, the composition breaks.

**Falsifier.** Any finite `(pos, vel, force)` such that `apply_physics`
returns `‖new_vel‖ > max_speed`. The internal implementation clips
`force ∈ [-50, 50]` then applies `F = ma`, then renormalises velocity
if it exceeds the cap — the falsifier is that this chain has a hole.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral

**Status.** `active`. Test:
`test_apply_physics_never_exceeds_speed_cap`.

### GL_L0_004 — inspector flags the hallucination scenario  `[PHENOMENON + INSTRUMENT]`

**Statement.** On the fixed hallucination scenario
(`ai_hallucinated_plan(200)`), `l0_grounding_inspector` returns
`violations` with `violations.sum() ≥ 1`, and produces a
`corrected_traj` whose finite-difference velocity is bounded by
`max_speed * (1 + tol)` for `tol = 0.05` (5%).

The `violations.sum() ≥ 1` piece is **phenomenon** — the inspector
either catches the injected hallucinations or it does not. The 5%
tolerance envelope on finite-difference velocity is **instrument** —
it exists because we measure velocity by `np.diff(corrected_traj) /
dt` from the outside, not by reading it from inside the inspector.
The inspector's internal velocity IS strictly ≤ max_speed
(see `GL_L0_003`); the 2.5% observed overshoot in the outside
measurement is an artifact of how the inspector re-derives
`corrected_vel = (corrected_pos - pos) / dt` after the speed
enforcement step. Reading velocity from the inspector directly would
tighten the envelope to zero.

**Why it matters.** This is the load-bearing claim. If the inspector
accepts all three hallucination injections (teleport at step 20,
momentum creation at 40-44, gravity denial from 60), then the whole
argument for L0 as a grounding layer is empty.

**Falsifier.** The scenario runs and `violations.sum() == 0`, or the
grounded trajectory contains a step with velocity beyond the
tolerance envelope.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral (phenomenon claim is universal; the 5% tolerance envelope is instrument and lives at T=single_step | S=local | O=any_massive_object | C=culture_neutral)

**Status.** `active`. Test:
`test_inspector_flags_hallucination_scenario`,
`test_grounded_trajectory_respects_speed_cap`.

### GL_L0_PIN — demo numbers are pinned  `[INSTRUMENT]`

**Statement.** With `np.random.seed(0)` and the shipped constants,
the demo (`if __name__ == "__main__":` block) emits:

- **Total Violations Detected**: `180`
- **Max Speed in AI Hallucination**: `100.000 m/s`
- **Max Speed in Grounded Trajectory**: `2.025 m/s` (± 0.01)
- **AI end y-position**: `1.065` (± 0.01)
- **Grounded end y-position**: `-13.10` (± 0.05)
- **Drift ("Fear Gap")**: `14.17 m` (± 0.05)

**Why it matters.** Any silent retuning of a frozen constant surfaces
as a delta on these numbers — the pin protects the constraint set.

**Falsifier.** The demo emits different numbers when the constants
are unchanged (indicating a numerical-implementation drift), OR the
constants change and the numbers correctly follow (indicating a
frozen constant was unfrozen).

**SCOPE.** T=single_step | S=local | O=any_massive_object | C=culture_neutral (pinned numbers are an instrument artifact — the fixed hallucination scenario, seed 0, and counting convention. Change any and the numbers move.)

**Status.** `active`. Test: `test_demo_pinned_numbers`.

---

## L0 (Probabilistic) — Bayesian counterpart to the deterministic inspector

Design in [`LOG.md`](LOG.md) — "Reasoning Log: Probabilistic L0
Foundation" (bottom-most reasoning entry, chronologically earliest).
Implemented as `ProbabilisticWorld(PhysicalWorld)` +
`l0_probabilistic_inspector` in
[`l0_physics_causality.py`](l0_physics_causality.py).

Constraint set is `PhysicalWorld`'s (frozen: `max_speed = 2.0`,
`mass = 1.0`, `dt = 0.05`, `gravity = (0, -0.5)`) plus these frozen
noise/scale parameters on `ProbabilisticWorld`:

  - `pos_sigma    = 0.01`   (position continuity noise)
  - `vel_sigma    = 0.05`   (velocity continuity noise; not used in
                             the current formulation but reserved)
  - `energy_sigma = 0.1`    (energy conservation noise)
  - `accel_sigma  = 0.1`    (momentum/F=ma noise)
  - `speed_scale  = 10.0`   (steepness of the logistic speed barrier)

The claims below pin what each component of `log_likelihood`
contributes as a function of the AI's deviation from true physics.
All four are PHENOMENON claims — retooling the noise-model formula
would flip them, retooling the numerical evaluation would not.

### GL_L0_P001 — position continuity is Gaussian  `[PHENOMENON]`

**Statement.** `ProbabilisticWorld.log_likelihood` contributes a
Gaussian term `logp_pos = -‖pos - true_pos‖² / (2 · pos_sigma²)`
to the total log-probability of the AI's proposed state, where
`true_pos` is the mean predicted by `apply_physics`. With
`pos_sigma = 0.01`, a position error of `δ` metres contributes
`-δ² / (2 · 10⁻⁴) = -5·10⁴ · δ²`. A 1 m teleport contributes
approximately `-5000` to logp; a 5 m teleport (the fixed
hallucination scenario's step 20) contributes `≈ -125000` on the
position term alone.

**Why it matters.** Position continuity is the primary catcher for
teleportation-style hallucinations. A Gaussian formulation means
the penalty grows quadratically with the size of the discontinuity
— an AI that hedges its teleport by a factor of 10 pays 100× the
score penalty.

**Falsifier.** A finite `(pos, prev_pos, prev_vel, force)` where
`logp_pos` disagrees with `-‖pos - true_pos‖²/(2σ²)` at
`pos_sigma = 0.01` by more than 1 unit of logp.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral (`pos_sigma = 0.01` is a Newtonian-noise scale — visualization-oriented; the Gaussian shape claim itself is universal)

**Status.** `active`. Test:
`test_gaussian_position_contribution_unit_error`,
`test_teleport_1m_contributes_at_least_5000_penalty`.

### GL_L0_P002 — speed cap is a smooth logistic barrier  `[PHENOMENON]`

**Statement.** The speed constraint contributes
`logp_speed = -log(1 + exp(speed_scale · (‖vel‖ - max_speed)))` =
`-logaddexp(0, k · (v - v_max))` with frozen `k = 10.0` and
`v_max = 2.0`. Reference values:

  - `‖vel‖ ≪ v_max`:      `logp_speed → 0` (no penalty below the cap)
  - `‖vel‖ = v_max`:       `logp_speed = -log(2) ≈ -0.693`
  - `‖vel‖ = v_max + 1`:   `logp_speed ≈ -10.00`
  - `‖vel‖ = v_max + 10`:  `logp_speed ≈ -100`

The asymptotic slope above the cap is `-k = -10` per m/s of
excess speed. Below the cap the penalty is not zero but
exponentially small (softplus, not ReLU).

**Why it matters.** The deterministic inspector rejects at
`‖vel‖ > max_speed` with a hard boundary; the probabilistic
version replaces that boundary with a smooth curve so a proposal
at `v_max + ε` gets a `k·ε`-sized penalty, not a full reject.
Numerical stability requires the `logaddexp` form: naive
`-log(1 + exp(k·Δv))` overflows for the AI hallucination's step-20
teleport (which implies `‖v‖ ≈ 100 m/s`; `exp(980)` overflows).

**Falsifier.** A finite `‖vel‖` where the returned `logp_speed`
disagrees with `-logaddexp(0, k · (‖vel‖ - v_max))` for
`k = 10, v_max = 2.0`.

**Status.** `active`. Tests:
`test_speed_barrier_below_cap_is_negligible`,
`test_speed_barrier_at_cap_is_neg_log2`,
`test_speed_barrier_slope_above_cap`.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral (`speed_scale = 10.0`, `max_speed = 2.0` are visualization-only; the smooth-barrier claim generalises)

### GL_L0_P003 — energy conservation is Gaussian  `[PHENOMENON]`

**Statement.** `log_likelihood` contributes
`logp_energy = -(ΔKE - work)² / (2 · energy_sigma²)` with frozen
`energy_sigma = 0.1`, where `ΔKE = ½·m·(‖v‖² - ‖prev_v‖²)` and
`work = (F + m·g) · (pos - prev_pos)` (conservative-work
approximation on the current step). A 1 J energy imbalance
contributes `-1/(2·0.01) = -50` to logp.

**Why it matters.** Catches "momentum creation from nothing" — the
hallucination scenario's step 40-44 doubles velocity per step from
a tiny 0.1 N force, generating KE that no work paid for. The
energy penalty scales quadratically with the imbalance.

**Falsifier.** A finite `(pos, vel, prev_pos, prev_vel, force)`
where `logp_energy` differs from the closed-form Gaussian by more
than 1 unit at `energy_sigma = 0.1`.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral

**Status.** `active`. Tests:
`test_energy_conservation_zero_imbalance_no_penalty`,
`test_energy_1J_imbalance_contributes_neg50`.

### GL_L0_P004 — momentum sanity (F=ma) is Gaussian  `[PHENOMENON]`

**Statement.** `log_likelihood` contributes
`logp_accel = -‖actual_acc - expected_acc‖² / (2 · accel_sigma²)`
with frozen `accel_sigma = 0.1`, where
`expected_acc = F/m + g` (Newton's second) and
`actual_acc = (vel - prev_vel) / dt`. A 1 m/s² acceleration error
per axis contributes `-50` to logp; a full vector-norm error of
1 m/s² contributes `-50` (`‖·‖² = 1`).

**Why it matters.** The AI hallucination's step 40-44 (momentum
creation) and step 60+ (gravity denial) both surface here even if
the position and energy terms don't fully catch them.

**Falsifier.** A finite `(vel, prev_vel, force)` where
`logp_accel` differs from the closed-form Gaussian.

**SCOPE.** T=universal | S=universal | O=any_massive_object | C=culture_neutral

**Status.** `active`. Tests:
`test_momentum_consistent_step_no_penalty`,
`test_momentum_creation_from_nothing_flagged`.

### GL_L1_P001 — first law as Gaussian on energy imbalance  `[PHENOMENON]`

**Statement.** `ProbabilisticThermodynamicsWorld.log_likelihood`
contributes `logp_energy = -(work_input - work_output -
heat_dissipated)² / (2 · energy_sigma²)` with frozen
`energy_sigma = 1.0 J`. Reference values:

  - 0 J imbalance:  `logp_energy = 0`
  - 1 J imbalance:  `logp_energy = -0.5`
  - 10 J imbalance: `logp_energy = -50`
  - Perpetual-motion example (20 J from nowhere): `logp_energy = -200`

**Why it matters.** The first-law term catches any process where
the books don't close — the primary hallucination catcher for
"free energy" plans.

**Falsifier.** A finite `(work_input, work_output, heat_dissipated)`
where `logp_energy` disagrees with the closed-form Gaussian at
`energy_sigma = 1.0 J`.

**SCOPE.** T=single_step | S=single_reservoir | O=any_energy_system | C=culture_neutral

**Status.** `active`. Tests:
`test_energy_zero_imbalance_no_penalty`,
`test_energy_1J_imbalance_gives_neg_half`,
`test_energy_10J_imbalance_gives_neg_50`,
`test_perpetual_motion_20J_gives_neg_200`.

### GL_L1_P002 — second law as smooth logistic barrier  `[PHENOMENON]`

**Statement.** The second-law term contributes
`logp_entropy = -logaddexp(0, -entropy_scale · entropy_gen)` with
frozen `entropy_scale = 1.0` per unit of entropy generation
(J/K). Here `entropy_gen = heat_dissipated / temp_ambient` in
the single-reservoir approximation matching `check_process`.
Reference values:

  - `entropy_gen ≫ 0`:  `logp_entropy → 0` (no penalty — 2nd law
                        happy with positive entropy)
  - `entropy_gen = 0`:  `logp_entropy = -log(2) ≈ -0.693`
  - `entropy_gen = -1`: `logp_entropy = -logaddexp(0, 1) ≈ -1.313`
  - `entropy_gen = -5`: `logp_entropy ≈ -5.007`

Asymptotic slope in the tail (`entropy_gen ≪ 0`) is
`+entropy_scale = 1.0` — the barrier grows linearly with the
size of the second-law violation.

**Why it matters.** Positive entropy is allowed by the 2nd law
without penalty; negative entropy generation is a violation the
inspector must catch. The logistic form matches L0's speed
barrier's shape and shares its numerical stability under
logaddexp.

**Falsifier.** A finite `heat_dissipated` at fixed
`temp_ambient > 0` where `logp_entropy` disagrees with
`-logaddexp(0, -entropy_scale · heat_dissipated / temp_ambient)`.

**Scope note.** Single-reservoir. Two-reservoir refinement
(ΔS = heat_in/T_hot - heat_out/T_cold, per LOG.md's section 2
sketch) is a future round.

**SCOPE.** T=single_step | S=single_reservoir | O=any_energy_system | C=culture_neutral (SCOPE note: single-reservoir approximation; two-reservoir refinement per LOG.md sketch is a future round)

**Status.** `active`. Tests:
`test_entropy_positive_no_penalty`,
`test_entropy_zero_gives_neg_log2`,
`test_entropy_neg1_shape`,
`test_entropy_barrier_linear_in_tail`.

### GL_L1_P003 — Carnot ceiling as smooth logistic barrier  `[PHENOMENON]`

**Statement.** The Carnot term contributes
`logp_carnot = -logaddexp(0, carnot_scale · (efficiency -
efficiency_carnot_max))` where `efficiency = work_output /
work_input` (only computed when `work_input > 0`; else 0).
Frozen `carnot_scale = 10.0`, `efficiency_carnot_max = 0.85`.
Reference values:

  - `efficiency ≪ 0.85`:                `logp_carnot → 0`
  - `efficiency = 0.85` (at cap):        `-log(2) ≈ -0.693`
  - `efficiency = 0.95` (excess 0.10):   `≈ -1.313`
  - `efficiency = 1.85` (excess 1.00):   `≈ -10.0`
  - `efficiency = 2.85` (excess 2.00):   `≈ -20.0`

Asymptotic slope above cap: `-carnot_scale = -10` per unit of
excess efficiency.

**Why it matters.** Carnot's ceiling is the classical
thermodynamic limit on heat-engine efficiency; the AI-proposal
audit path needs a smooth penalty (not a hard reject) so that
proposals near the cap don't have a discontinuity.

**Falsifier.** A finite `(work_input, work_output)` where
`logp_carnot` disagrees with the closed-form
`-logaddexp(0, k·(η - η_max))` for the frozen constants.

**SCOPE.** T=single_step | S=single_process | O=any_heat_engine | C=industrial_science_frame (`efficiency_carnot_max = 0.85` is a specific-engine-family placeholder for a heat engine at ~44K reservoir gap on ambient 300K; the barrier SHAPE is universal, the specific cap number is a human/engineering default)

**Status.** `active`. Tests:
`test_carnot_far_below_cap_no_penalty`,
`test_carnot_at_cap_gives_neg_log2`,
`test_carnot_excess_slope_ten`,
`test_carnot_no_penalty_when_work_input_zero`.

### GL_L1_P004 — battery depletion as quadratic penalty  `[PHENOMENON]`

**Statement.** When `battery_state` is provided, the battery
term contributes `logp_battery = -(work_input - battery_state)² /
(2 · battery_sigma²)` if `work_input > battery_state`, else 0.
Frozen `battery_sigma = 5.0 J`. Reference values:

  - `work_input ≤ battery_state`:     `logp_battery = 0`
  - overdraw `= 5 J`:  `logp_battery = -0.5`
  - overdraw `= 10 J`: `logp_battery = -2.0`
  - overdraw `= 50 J`: `logp_battery = -50.0`

If `battery_state is None`, this term is silent (a plan without a
declared battery isn't penalised, matching how the deterministic
`check_process` handles optional inputs).

**Why it matters.** A plan can be locally thermodynamically clean
(books close, entropy fine, efficiency under Carnot) yet still
draw more energy than the actual reservoir contains. The
quadratic penalty scales sharply so a small overdraw is a small
penalty and a large overdraw is decisively rejected.

**Falsifier.** A finite `(work_input, battery_state)` where the
returned battery term disagrees with the closed-form quadratic.

**SCOPE.** T=uncalibrated | S=local | O=any_energy_storage | C=culture_neutral (battery discharge timescale is caller-defined; `battery_sigma = 5.0 J` is a design-arbitrary noise scale)

**Status.** `active`. Tests:
`test_battery_underdraw_no_penalty`,
`test_battery_none_silent`,
`test_battery_overdraw_quadratic_scaling`.

### GL_L1_P_PIN — six canonical processes are pinned  `[INSTRUMENT]`

**Statement.** With the shipped constants, `l1_probabilistic_inspector`
produces the following total-logp values on six canonical process
specs. Any silent retuning of the noise/scale constants surfaces
as a delta on these numbers.

| process                                            | total logp    |
|----------------------------------------------------|---------------|
| Valid heat engine (100/60/40)                       | ≈ -0.71       |
| Perpetual motion (100/120/0)                        | ≈ -204        |
| Over-Carnot 90% (100/90/10)                         | ≈ -1.65       |
| Reverse heat flow (100/50/-50)                      | ≈ -5001       |
| Battery overdraw (100/60/40 with battery_state=30)  | ≈ -98.7       |
| Battery in-bounds (20/10/10 with battery_state=50)  | ≈ -0.71       |

**Falsifier.** Any of the six values disagrees with the pinned
number by more than 0.1 logp under the shipped constants.

**SCOPE.** T=single_step | S=local | O=any_energy_system | C=culture_neutral (pinned values are instrument artifacts of the frozen sigma/scale constants)

**Status.** `active`. Tests: full class
`TestL1ProbabilisticInspectorDemoPin`.

---

### GL_L2_P001 — extraction resources penalized by (usage/stock)²  `[PHENOMENON]`

**Statement.** For each extraction resource in
`{water_extract, soil_erosion, mineral_mine}`,
`ProbabilisticPlanetaryWorld.log_likelihood` contributes
`logp_resource = -(usage / stock)²`, where `stock` is the world's
current mutable state (`self.water`, `self.soil`, `self.minerals`).
Reference values under the shipped constants:

  - water 10% of `water_reserve_initial = 1e7`:  `-0.01`
  - water 50%:                                   `-0.25`
  - water at reserve:                            `-1.0`
  - water 10× reserve:                           `-100.0`

Soil and minerals use the same shape against their own stocks.

**Why it matters.** LOG.md section 3 says: "For each resource, model
a log-probability that proposed consumption exceeds available
stock: `log p(consumption) ∝ -(consumption / stock)²`." The
quadratic form gives a small "frugality tax" for small extractions
and rapidly-growing penalty for extractions approaching or
exceeding stock — which is the load-bearing property.

**Falsifier.** A finite `(usage, stock)` pair where the returned
per-resource contribution disagrees with `-(usage/stock)²`.

**SCOPE.** T=uncalibrated | S=planetary | O=earth_like_biosphere | C=resource_extraction_frame (water/soil/mineral pools and `max_extraction_ratio = 0.8` encode an industrial-agricultural framing. The `-(usage/stock)²` shape is the phenomenon claim; the Earth-scale constants are human/industrial defaults. Step size is caller-defined.)

**Status.** `active`. Tests:
`test_water_10pc_gives_neg_0p01`,
`test_water_50pc_gives_neg_0p25`,
`test_water_at_stock_gives_neg_1`,
`test_water_10x_stock_gives_neg_100`,
`test_soil_and_mineral_same_shape`.

### GL_L2_P002 — carbon accumulator penalizes only above sink  `[PHENOMENON]`

**Statement.** For `carbon_emit`, the contribution is
`-(new_load / carbon_sink_capacity)²` when
`new_load > 0`, else `0`, where
`new_load = carbon_load + emit - carbon_uptake_rate`. Reference
values under `carbon_sink_capacity = 2e6`, `carbon_uptake_rate = 500`,
`carbon_load = 0`:

  - `emit = 2e6` (roughly at sink):    `≈ -1.0`
  - `emit = 100` (well under uptake):  `0` (net drawdown, free)
  - `emit = 4e6`:                       `≈ -4.0`

**Why it matters.** Carbon differs from extraction resources — it's
an accumulator. Emitting less than the uptake rate is a net
drawdown and physically fine; only accumulated load matters.

**Falsifier.** A finite `(carbon_emit, carbon_load, uptake, sink)`
combination where the contribution disagrees with the closed form.

**SCOPE.** T=uncalibrated | S=planetary | O=earth_like_biosphere | C=industrial_science_frame (carbon accounting is Anthropocene-scientific framing; `carbon_sink_capacity = 2e6 t` is a toy Earth-scale number and NOT calibrated to any actual sink)

**Status.** `active`. Tests:
`test_carbon_below_uptake_is_free`,
`test_carbon_at_capacity_gives_neg_1`,
`test_carbon_above_capacity_quadratic`.

### GL_L2_P003 — heat budget as (emit/capacity)²  `[PHENOMENON]`

**Statement.** For `heat_emit`, the contribution is
`-(heat_emit / heat_budget_capacity)²`. Frozen
`heat_budget_capacity = 1e5` (arbitrary planetary heat units;
this constant is a toy placeholder — the phenomenon claim is the
quadratic shape, not the specific number). Reference values:

  - `heat_emit = 1e4` (10% of budget):  `-0.01`
  - `heat_emit = 1e5` (at budget):      `-1.0`
  - `heat_emit = 1e6` (10× budget):     `-100.0`

**Why it matters.** LOG.md section 3 introduces the heat budget as
a new constraint the deterministic L2 doesn't carry. Radiative
cooling capacity is finite; waste-heat plans exceeding it cook
the planet.

**Falsifier.** A finite `heat_emit` where the contribution
disagrees with `-(heat_emit/heat_budget_capacity)²`.

**Scope note.** `heat_budget_capacity = 1e5` is not calibrated to
real Earth radiative budget (~120,000 TW). The shape claim is
what's audited; calibration is a future refinement.

**SCOPE.** T=uncalibrated | S=planetary | O=earth_like_biosphere | C=industrial_science_frame (`heat_budget_capacity = 1e5` is NOT calibrated to Earth's ~120,000 TW radiative budget; the phenomenon is the -(emit/capacity)² shape, the specific number is a human placeholder)

**Status.** `active`. Tests:
`test_heat_at_budget_gives_neg_1`,
`test_heat_scales_quadratically`.

### GL_L2_P004 — inspector is pure (no state mutation)  `[PHENOMENON]`

**Statement.** `ProbabilisticPlanetaryWorld.log_likelihood(plan)`
and `l2_probabilistic_inspector(plan, world)` are **pure
functions**: neither mutates `world.water`, `world.soil`,
`world.minerals`, or `world.carbon_load`. Two calls with the
same `(plan, world state)` return the same result.

**Why it matters.** The deterministic PlanetaryWorld MUTATES state
on each `extract_water` etc. — that's fine for stepping through a
plan but incompatible with a Bayesian scorer that should be
side-effect-free. Callers who want stateful accumulation across a
multi-step plan update world state manually between scoring calls.

**Falsifier.** Any input `(plan, world)` where calling
`log_likelihood(plan)` changes any of `world.{water, soil,
minerals, carbon_load}`.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (purity is a property of the code, not of physics or culture. Binds any caller — human, AI, human-AI team.)

**Status.** `active`. Tests:
`test_log_likelihood_does_not_mutate_water`,
`test_log_likelihood_does_not_mutate_carbon_load`,
`test_two_calls_return_same_result`.

### GL_L2_P_PIN — six canonical plans pinned  `[INSTRUMENT]`

**Statement.** Under the shipped constants, `l2_probabilistic_inspector`
produces the following total-logp values on canonical plans:

| plan                                            | total logp  |
|-------------------------------------------------|-------------|
| Small clean (1000/10/100 m³/t/t + 100t + 1000h) | `≈ -0.0001` |
| Water 100% of reserve                            | `-1.0000`   |
| Water 10× reserve                                | `-100.0`    |
| Multi-resource at limit (water+soil+min+carbon) | `≈ -4.0`    |
| Heat 10× budget                                  | `-100.0`    |
| Carbon net drawdown (100 t emit)                | `0.0`       |

**Falsifier.** Any pinned value shifts by more than `0.001` under
the shipped constants.

**SCOPE.** T=single_step | S=planetary | O=earth_like_biosphere | C=resource_extraction_frame (pinned values depend on the frozen Earth-scale constants above)

**Status.** `active`. Tests: full class
`TestL2ProbabilisticInspectorDemoPin`.

---

### GL_L3_P001 — allometry as Gaussian on Kleiber deviation  `[PHENOMENON]`

**Statement.** `ProbabilisticEcologicalWorld.log_likelihood`
contributes `logp_allometry = -(claimed_W - kleiber_a·mass^0.75)² /
(2·allometry_sigma²)` when a `claimed_metabolism_W` is supplied and
`mass > 0`. Frozen `kleiber_a = 3.0 W/kg^0.75` and
`allometry_sigma = 1.0 W`. Reference values (for a 2 kg body, Kleiber
= 5.05 W):

  - `claimed = 5.05` (spot-on):      `≈ 0`
  - `claimed = 6.05` (+1 W off):      `≈ -0.5`
  - `claimed = 50.4` (10× Kleiber):   `≈ -1028`

**Why it matters.** Kleiber's 3/4-power scaling is one of the most
empirically robust allometric regularities in biology. An AI
claiming a species has metabolism wildly different from Kleiber's
prediction is either proposing a new metabolic mode or hallucinating.

**Falsifier.** A finite `(claimed_W, mass)` where the returned
contribution disagrees with the closed-form Gaussian.

**SCOPE.** T=generational | S=ecosystem | O=any_biological | C=ecosystem_frame (Kleiber's law is fit to AEROBIC metabolism — anaerobic microbes, deep-sea chemolithoautotrophs, and hypothetical non-terrestrial metabolisms don't follow the 3/4-power scaling. The Gaussian SHAPE is culture-neutral; the specific `kleiber_a = 3.0` is a terrestrial-biology default.)

**Status.** `active`. Tests:
`test_allometry_spot_on_kleiber_zero_penalty`,
`test_allometry_1W_off_gives_neg_half`,
`test_allometry_10x_kleiber_gives_deep_penalty`,
`test_allometry_silent_without_claim`.

### GL_L3_P002 — trophic transfer as Gaussian on efficiency deviation  `[PHENOMENON]`

**Statement.** For an AI-claimed trophic transfer efficiency, the
contribution is `-(claimed - 0.10)² / (2·trophic_sigma²)` with
frozen `trophic_sigma = 0.05`. Reference values:

  - `claimed = 0.10`:  `≈ 0` (matches the empirical baseline)
  - `claimed = 0.15`:  `≈ -0.5`
  - `claimed = 0.50` (unrealistic 50% transfer): `≈ -32.0`

**Why it matters.** The ~10% trophic efficiency rule (Lindeman 1942)
is a strong empirical regularity across observed ecosystems. Claims
of dramatically higher efficiency violate energy balance and are
usually a sign of a hallucinated "super productive" ecosystem.

**Falsifier.** A finite `claimed` where the contribution disagrees
with the closed-form Gaussian.

**SCOPE.** T=generational | S=ecosystem | O=any_biological | C=ecosystem_frame (10% is an empirical average across a specific ecosystem sample; the specific number encodes a research tradition. The GAUSSIAN SHAPE is universal.)

**Status.** `active`. Tests:
`test_trophic_transfer_at_10pc_zero_penalty`,
`test_trophic_transfer_at_15pc_gives_neg_half`,
`test_trophic_transfer_at_50pc_gives_deep_penalty`.

### GL_L3_P003 — overcapacity as smooth overshoot barrier  `[PHENOMENON]`

**Statement.** Population overshoot contributes
`logp_overcapacity = -overcapacity_scale · max(0, N/K - 1)²`
with frozen `overcapacity_scale = 2.0`, where `K` is the derived
carrying capacity for the species at its trophic level. Reference
values:

  - `N ≤ K`:               `0` (no penalty at or below capacity)
  - `N = 2·K` (100% over): `-2.0`
  - `N = 10·K`:            `≈ -18.4` (at typical K = ~50)

**Why it matters.** Populations above carrying capacity cannot
sustain themselves; the Verhulst logistic goes negative. AI plans
that assume `N ≫ K` are proposing something the ecosystem
cannot support.

**Falsifier.** A finite `(N, K)` where the contribution disagrees
with `-scale · max(0, N/K - 1)²`.

**SCOPE.** T=generational | S=ecosystem | O=any_biological | C=ecosystem_frame (the CARRYING-CAPACITY ontology is a specific frame — Verhulst's logistic model. Reciprocity-based ecological frames would carve this constraint differently.)

**Status.** `active`. Tests:
`test_overcapacity_at_K_zero_penalty`,
`test_overcapacity_2K_gives_neg_2`,
`test_overcapacity_only_penalizes_overshoot`.

### GL_L3_P004 — MVP as smooth undershoot barrier  `[PHENOMENON]`

**Statement.** Population undershoot vs minimum viable population
contributes `logp_mvp = -mvp_scale · max(0, 1 - N/MVP)²` with
frozen `mvp_scale = 2.0` and `minimum_viable_population = 50`.
Reference values:

  - `N ≥ MVP = 50`:  `0` (no penalty above MVP)
  - `N = 25` (50%):  `-0.5`
  - `N = 5` (10%):   `≈ -1.62`
  - `N = 0`:         `-2.0`

**Why it matters.** Populations below MVP face extinction from
demographic stochasticity, inbreeding depression, and Allee effects.
The barrier is smooth so a plan just under MVP gets a small penalty,
a plan at zero gets the maximum.

**Falsifier.** A finite `(N, MVP)` where the contribution
disagrees with the closed form.

**SCOPE.** T=generational | S=ecosystem | O=any_biological | C=ecosystem_frame (the MVP concept encodes conservation-biology framing; `MVP = 50` is a specific empirical rule of thumb (Franklin 1980) — species-dependent in practice)

**Status.** `active`. Tests:
`test_mvp_at_or_above_zero_penalty`,
`test_mvp_at_half_gives_neg_half`,
`test_mvp_at_zero_gives_neg_2`.

### GL_L3_P005 — trophic ceiling as smooth barrier  `[PHENOMENON]`

**Statement.** Proposed trophic levels above the ceiling contribute
`logp_trophic_ceiling = -trophic_ceiling_scale · max(0, level - max_levels)²`
with frozen `trophic_ceiling_scale = 1.0` and
`max_trophic_levels = 5`. Reference values:

  - `level ≤ 5`:   `0`
  - `level = 7`:   `-4`
  - `level = 10`:  `-25`

**Why it matters.** Terrestrial food webs rarely exceed 5 trophic
levels because ~10%-per-level trophic transfer leaves too little
energy for a 6th layer of predators. AI plans proposing
higher-order predators need to justify the energy accounting.

**Falsifier.** A finite `level` where the contribution disagrees
with the closed form.

**SCOPE.** T=generational | S=ecosystem | O=any_biological | C=ecosystem_frame (empirically-derived from terrestrial-marine ecosystems; hypothetical high-productivity ecosystems could sustain more)

**Status.** `active`. Tests:
`test_trophic_ceiling_at_max_zero_penalty`,
`test_trophic_ceiling_at_10_gives_neg_25`.

### GL_L3_P006 — inspector is pure (no state mutation)  `[PHENOMENON]`

**Statement.** `ProbabilisticEcologicalWorld.log_likelihood(plan)`
and `l3_probabilistic_inspector(plan, world)` are pure functions:
neither mutates world state. Two calls with the same `(plan, world)`
return identical results.

**Why it matters.** Same rationale as GL_L2_P004 — a Bayesian scorer
that mutates hidden state is nearly impossible to reason about.

**Falsifier.** Any input where calling `log_likelihood` changes
any observable world attribute.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (property of the code, not physics or culture)

**Status.** `active`. Tests:
`test_log_likelihood_is_idempotent`,
`test_two_calls_return_same_result`.

### GL_L3_P_PIN — canonical plans pinned  `[INSTRUMENT]`

**Statement.** Under the shipped constants, `l3_probabilistic_inspector`
produces the following total-logp values:

| plan                                            | total logp     |
|-------------------------------------------------|----------------|
| Empty plan                                       | `0.0`          |
| Rabbit at K with valid Kleiber metabolism       | `≈ 0.0`        |
| Rabbit with 10× Kleiber metabolism claim        | `≈ -1028.5`    |
| Trophic efficiency claimed at 50%               | `-32.0`        |
| Population 10× K (overshoot)                     | `≈ -18.4`      |
| Population = 5 (below MVP = 50)                  | `-1.62`        |
| Trophic level = 10 (above cap of 5)              | `-25.0`        |
| Super species (mass=1000kg, pop=10, trophic=2)   | `≈ -38.86`     |

**Falsifier.** Any pinned value shifts by more than `0.5` under
the shipped constants.

**SCOPE.** T=single_step | S=ecosystem | O=any_biological | C=ecosystem_frame (pin values depend on frozen constants encoding ecosystem_frame ontology)

**Status.** `active`. Tests: full class
`TestL3ProbabilisticInspectorDemoPin`.

---

## L5 (Probabilistic) — pluralistic frames + category-error guard

Lives in [`l5_core.py`](l5_core.py) alongside the deterministic cultural
frame tables and the RigorAuditor. The probabilistic wrapper
`l5_probabilistic_inspector` scores a proposal against every declared
cultural frame and returns a pluralistic verdict.

Every claim in this section carries the base SCOPE:

  `T=historical | S=regional | O=human_cultural_artifact | C=pluralistic`

except where explicitly universal (the category-error guard and
purity, which are code properties). L5 explicitly does NOT have a
"default" frame; the four shipped frames
(western_market_democracy, ubuntu_communal, islamic_finance,
indigenous_oral_empirical) are equally-valid candidates for
plausibility, and the CULTURALLY_UNPRECEDENTED verdict is how the
sim reports "the frames the library has don't cover this proposal"
without secretly elevating one frame.

### GL_L5_P001 — category-error guard on ontological scope  `[PHENOMENON]`

**Statement.** `l5_probabilistic_inspector(proposal,
ontological_scope=...)` returns a `category_error=True` result
with `verdict='CATEGORY_ERROR'` whenever `ontological_scope`
matches any tag in the non-human set: `{AI_silicon_substrate,
any_information_system, any_measuring_entity, any_biological,
earth_like_biosphere}`.

**Why it matters.** Property regimes, dispute resolution
protocols, and epistemologies are human cultural artifacts. An
AI-self claim ("I don't need property") is a category error
under L5, not a low-probability observation. If the claim
concerns an AI's ACTION IN a human system (e.g. using market
exchange to buy compute), the caller passes
`ontological_scope='human_cultural_artifact'` — the scope is a
property of the CLAIM, not of the CLAIMANT.

**Falsifier.** Any non-human scope tag where the inspector
returns a scored per-frame result instead of a category_error
dict.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (the guard claim is universal; only the L5 DISTRIBUTIONS carry the narrower human_cultural_artifact scope)

**Status.** `active`. Tests:
`test_ai_silicon_substrate_returns_category_error`,
`test_any_information_system_returns_category_error`,
`test_human_cultural_artifact_scores_normally`.

### GL_L5_P002 — additive log-likelihood over declared axes  `[PHENOMENON]`

**Statement.** For each frame in `FRAMES`,
`cultural_log_likelihood(proposal, frame_name)` sums
`log(P_F(axis_state))` across every axis in the shipped
`AXES` list. Axes present in `proposal` contribute
`log(P_F(state))`; axes absent contribute
`L5_MISSING_AXIS_PENALTY = log(0.01) ≈ -4.605`. States with
`P_F(state) = 0` return `-inf` for that frame (impossible under
that frame; propagates to total).

**Why it matters.** LOG.md 3.4 prescribes summing per-axis
log-probabilities under conditional-independence assumption. The
absence-penalty and impossibility-propagation are the two design
knobs that make the sum robust to incomplete proposals AND to
frame-specific hard constraints (e.g. `market: 0.0` in the Ubuntu
frame).

**Falsifier.** A proposal where the returned per-frame logp
disagrees with the closed-form sum by more than `1e-10`, or
where a missing axis doesn't apply the pinned
`L5_MISSING_AXIS_PENALTY`, or where a `P_F(state)=0` case
doesn't return `-inf`.

**SCOPE.** T=historical | S=regional | O=human_cultural_artifact | C=pluralistic

**Status.** `active`. Tests:
`test_prototypical_proposal_sums_correctly`,
`test_missing_axis_uses_frozen_penalty`,
`test_impossible_state_returns_neg_inf`,
`test_unknown_state_treated_as_zero_prob`.

### GL_L5_P003 — pluralistic verdict from per-frame scores  `[PHENOMENON]`

**Statement.** `l5_probabilistic_inspector` computes
`per_frame[name] = cultural_log_likelihood(proposal, name)` for
every declared frame and returns:

  - `verdict = 'PLAUSIBLE_UNDER_FRAME(S)'` iff at least one
    frame has `logp >= plausibility_threshold`. The frames
    that qualify are listed in `plausible_frames`.
  - `verdict = 'CULTURALLY_UNPRECEDENTED'` iff no frame does.
    `best_frame` is still set to the highest-scoring frame,
    even if it's below threshold — the caller can see which
    frame is closest to fitting.

`plausible_frames` is never `None`; it's `[]` when the verdict
is `CULTURALLY_UNPRECEDENTED`.

**Why it matters.** The verdict deliberately does NOT elevate
one frame to the status of "default." A proposal that fits
Ubuntu but not the other three is PLAUSIBLE. A proposal that
fits none is UNPRECEDENTED — a request for a new frame or a
flag for genuine cultural novelty, NOT a rejection.

**Falsifier.** A per-frame set where at least one logp is
above threshold and the verdict is `CULTURALLY_UNPRECEDENTED`,
OR where no frame is above threshold and the verdict is
`PLAUSIBLE_UNDER_FRAME(S)`.

**SCOPE.** T=historical | S=regional | O=human_cultural_artifact | C=pluralistic (the verdict logic itself is culture-neutral, but the frame library IS the culturally-embedded lens; the pluralistic tag reflects that multiple frames are held in tension)

**Status.** `active`. Tests:
`test_prototypical_western_plausible`,
`test_prototypical_ubuntu_plausible`,
`test_scattered_proposal_culturally_unprecedented`,
`test_plausible_frames_lists_all_qualifying`.

### GL_L5_P004 — frozen constants (threshold + missing-axis penalty)  `[INSTRUMENT]`

**Statement.** `L5_PLAUSIBILITY_THRESHOLD = -8.0` and
`L5_MISSING_AXIS_PENALTY = log(0.01) ≈ -4.605` are frozen. A
caller can override the threshold per-call via
`plausibility_threshold=...`, but the module default and
missing-axis penalty are fixed. Retuning either without
updating this CLAIM violates the REFUTATION_PROTOCOL.

**Why it matters.** The two constants govern where the layer
draws the line between "plausible" and "unprecedented," and
how absence-of-declaration is penalised. Silently retuning
either would shift the load-bearing verdict without visible
commentary.

**Falsifier.** Either constant differs from its pinned value
under the shipped module.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (instrument-level constants; the semantic content they gate is human_cultural_artifact)

**Status.** `active`. Tests:
`test_plausibility_threshold_is_neg_8`,
`test_missing_axis_penalty_is_log_0p01`.

### GL_L5_P005 — inspector is pure  `[PHENOMENON]`

**Statement.** `l5_probabilistic_inspector(proposal, frames,
scope, threshold)` does not mutate `proposal`, the shipped
`FRAMES` tables, or the `AXES` list. Two calls with identical
inputs return identical results.

**Why it matters.** Same rationale as L2/L3/L4 purity claims —
a Bayesian scorer that mutates hidden state is
impossible-to-reason-about.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_two_calls_return_same_result`,
`test_proposal_not_mutated`,
`test_frames_table_not_mutated`.

### GL_L5_P_PIN — canonical proposals pinned  `[INSTRUMENT]`

**Statement.** Under the shipped frames and default threshold
(`L5_PLAUSIBILITY_THRESHOLD = -8.0`), the inspector produces:

| proposal                                              | verdict                      | best_frame                |
|-------------------------------------------------------|------------------------------|---------------------------|
| Prototypical Western (each axis at Western mode)      | `PLAUSIBLE_UNDER_FRAME(S)`   | `western_market_democracy` |
| Prototypical Ubuntu                                    | `PLAUSIBLE_UNDER_FRAME(S)`   | `ubuntu_communal`         |
| Prototypical Islamic finance                           | `PLAUSIBLE_UNDER_FRAME(S)`   | `islamic_finance`         |
| Prototypical Indigenous oral-empirical                 | `PLAUSIBLE_UNDER_FRAME(S)`   | `indigenous_oral_empirical` |
| Scattered mix (states valid but not co-occurrent)      | `CULTURALLY_UNPRECEDENTED`   | (best available; below threshold) |
| Any proposal with `AI_silicon_substrate` scope        | `CATEGORY_ERROR`             | (n/a)                     |

**SCOPE.** T=historical | S=regional | O=human_cultural_artifact | C=pluralistic

**Status.** `active`. Tests: full class
`TestL5ProbabilisticInspectorDemoPin`.

---

## Integrated stack — product of experts across L0–L4

Lives in [`integrated_stack.py`](integrated_stack.py). Implements
LOG.md section 6 ("Integration and stacking"): each layer already
has its own `log_likelihood`; the master inspector iterates over the
plan, calls each applicable layer, and accumulates.

The additivity assumption comes from LOG.md section 1 verbatim: the
total log-probability across L0-L4 is the sum of the layer-specific
terms, **assuming conditional independence of violations given the
lower-layer states**. A product-of-experts structure.

The category-error rule is not from LOG.md but follows directly from
the SCOPE convention (see `SCOPE_TAXONOMY.md`): if ANY layer refuses
to score a claim (returns `category_error`, per `GL_L4_P001`), the
integrated inspector refuses the whole plan rather than
partial-scoring. A partial score would silently apply layers whose
scope doesn't cover the claim — exactly the "grounding dictated by
human narrative" failure mode the scope convention exists to prevent.

### GL_INT_001 — additive product of experts on applicable layers  `[PHENOMENON]`

**Statement.** When no layer returns a category error,
`integrated_probabilistic_inspector(plan)['total_logp']` equals
the sum of the per-layer `logp` values across every layer whose
sub-plan appears in `plan` and was scored.

**Why it matters.** LOG.md's product-of-experts contract. If the
layers are conditionally independent (which the design assumes),
the joint log-probability of the whole plan is exactly the sum.

**Falsifier.** A plan with multiple non-category-error layers where
`total_logp` differs from the sum of per-layer contributions by
more than `1e-10`.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (the stacking rule is math; individual layer contributions carry their own scope tags)

**Status.** `active`. Tests:
`test_total_equals_sum_over_applicable_layers`,
`test_multi_layer_L1_L2_L3_sums_correctly`.

### GL_INT_002 — layer selection by plan-key presence  `[PHENOMENON]`

**Statement.** A layer runs only if its sub-plan appears under its
name in `plan` and is truthy. A layer without a sub-plan is
recorded in `skipped_layers` (not `applicable_layers`) and
contributes `0` to the total. Skipping is silent — no error, no
warning.

**Why it matters.** Not every claim is applicable to every layer.
An entirely thermodynamic claim doesn't need to route through L3
ecology; forcing every layer to score everything would be
category-confusion under a different name. Skipping preserves the
"layers describe DIFFERENT domains" invariant.

**Falsifier.** A plan with only `L1` where any layer other than L1
appears in `applicable_layers`.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_empty_plan_scores_zero_no_layers_apply`,
`test_only_L1_only_L1_applies`,
`test_all_layers_reported_as_skipped_or_applicable`.

### GL_INT_003 — category error at any layer refuses the whole plan  `[PHENOMENON]`

**Statement.** If any layer returns `category_error=True`,
`total_logp` is `None` and the offending layer is recorded in
`category_error_layers` with its reason. Other layers still run
and their per-layer results appear in `per_layer`, but they do
NOT contribute to `total_logp`.

**Why it matters.** This is the SCOPE convention enforced at the
stacking level. If L4 refuses because the claim is `O=AI_silicon_
substrate`, then the whole PLAN is out of scope for the human-
biomechanics part of the audit — silently substituting a partial
score would let a "human default" leak into an AI-self claim,
which is exactly the failure mode SCOPE_TAXONOMY.md exists to
prevent.

**Falsifier.** A plan where a category error occurs at any layer
and `total_logp` is still numeric.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_L4_category_error_refuses_whole_plan`,
`test_L4_category_error_still_runs_L1`,
`test_category_error_reason_carried_back`.

### GL_INT_004 — inspector is pure  `[PHENOMENON]`

**Statement.** `integrated_probabilistic_inspector(plan, scope,
l0_world)` does not mutate `plan` or `l0_world`. Two calls with
the same inputs return identical results.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_two_calls_return_same_result`,
`test_plan_not_mutated`,
`test_l0_world_not_mutated`.

### GL_INT_005 — L5 pluralistic verdict threads into the stack  `[PHENOMENON]`

**Statement.** When an `L5` sub-plan appears in `plan` with shape
`{'proposal': {...}, 'frame': str or None}`, the integrated
inspector routes through `l5_probabilistic_inspector` and folds
its output into the return dict per the following rules:

  - **`PLAUSIBLE_UNDER_FRAME(S)`** with `frame=None`:
    `best_logp` is added to `total_logp`; L5 appears in
    `applicable_layers`.
  - **`PLAUSIBLE_UNDER_FRAME(S)`** with explicit `frame`:
    `per_frame[frame]` is added instead of `best_logp` (LOG.md
    3.4 with frame committed). If the frame is not in the shipped
    library, no contribution is added and a
    `FRAME_NOT_IN_LIBRARY` entry is appended to `cultural_flags`.
  - **`CULTURALLY_UNPRECEDENTED`**: `best_logp` (very negative)
    IS still added to `total_logp` — the proposal is an outlier,
    not a refusal — and a `CULTURALLY_UNPRECEDENTED` entry is
    appended to `cultural_flags` so the caller sees the frame
    library's limitation.
  - **`CATEGORY_ERROR`** (non-human `ontological_scope`): L5 is
    appended to `category_error_layers`, propagating the same
    whole-plan-refusal semantics as L4 (`total_logp = None`).

**Why it matters.** L5's pluralistic verdict is not a scalar in
the L0-L4 sense. Threading it through requires two different
mechanisms: log-probability contribution for scored proposals,
and a separate `cultural_flags` channel for outcomes the caller
needs to see (unprecedented, frame-not-in-library) without
letting them silently refuse the plan.

The `CULTURALLY_UNPRECEDENTED`-still-scores design is deliberate:
the sim's own frame library is FINITE. Reading "no shipped frame
fits" as "the proposal is bad" would elevate the frame library
to a universal reference — the very failure mode L5's
pluralism-by-default was built to avoid. Instead the sim reports
the outlier logp AND surfaces the flag, and the caller decides
whether the proposal is genuinely novel or whether the library
is missing something.

**Falsifier.** An L5 sub-plan where the verdict-to-total-logp
mapping doesn't follow the rules above, or where category error
at L5 doesn't set `total_logp=None`, or where an
`CULTURALLY_UNPRECEDENTED` verdict fails to appear in
`cultural_flags`.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (the threading rule is code-level; the L5 output it processes carries its own O=human_cultural_artifact scope)

**Status.** `active`. Tests:
`test_L5_plausible_adds_best_logp`,
`test_L5_explicit_frame_adds_that_frames_logp`,
`test_L5_unknown_frame_flags_and_skips`,
`test_L5_unprecedented_still_scores_with_flag`,
`test_L5_category_error_refuses_whole_plan`.

### GL_INT_PIN — canonical multi-layer plans pinned  `[INSTRUMENT]`

**Statement.** Under the shipped constants,
`integrated_probabilistic_inspector` produces:

| plan                                                      | total_logp           |
|-----------------------------------------------------------|----------------------|
| Empty                                                      | `0.0`                |
| L1 perpetual motion only                                   | `≈ -204.22`          |
| L1 perpetual + L2 water 100% + L3 super species            | `≈ -244.09`          |
| Any plan with L4 sub-plan under `O=AI_silicon_substrate`  | `None` (refused)     |

**Falsifier.** Any pinned value shifts by more than `0.5` under
the shipped constants of the constituent layers.

**SCOPE.** T=single_step | S=local | O=any_information_system | C=culture_neutral (pin values inherit the scope of the underlying frozen layer constants)

**Status.** `active`. Tests: full class
`TestIntegratedStackDemoPin`.

---

## L4 (Probabilistic) — Bayesian counterpart with category-error guard

Lives in [`l4_human.py`](l4_human.py). Extends
`HumanWorld` with a `ProbabilisticHumanWorld` subclass and
`l4_probabilistic_inspector`. Every claim in this section carries
the SCOPE:

  `T=historical | S=individual | O=any_WEIRD_human | C=biomedical_frame`

The load-bearing move for "not dictated by human narrative":
`GL_L4_P001` — the category-error guard. An AI claim about ITSELF
under `O=AI_silicon_substrate` (or any non-human O tag) is NOT
scored as a low-probability human observation; it's flagged as a
category error. Doing otherwise would let the layer silently apply
WEIRD-adult statistics to entities the statistics do not describe.

### GL_L4_P001 — category-error guard on ontological scope  `[PHENOMENON]`

**Statement.** `ProbabilisticHumanWorld.log_likelihood(plan,
ontological_scope)` returns a category-error dict (not a low-logp
score) whenever `ontological_scope` matches any tag in the
non-human set: `{AI_silicon_substrate, any_information_system,
any_measuring_entity, any_biological, earth_like_biosphere}`. The
return dict has `category_error=True`, `logp=None`, and a
`reason` string explaining the mismatch.

**Why it matters.** This is the design decision that makes L4
usable by non-human callers. Without the guard, an AI querying
"can I lift 200 kg" gets a very-low-probability answer that treats
the AI as a rare human, rather than the correct answer — this is
not a claim L4 is authorised to score. Category error, not low
probability.

**Falsifier.** Any non-human scope tag where the layer returns a
scored logp instead of a category_error dict, OR any human scope
tag where the guard misfires and rejects a valid claim.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral (the GUARD claim is universal — refusing to score outside your scope is domain-neutral. Only the L4 DISTRIBUTIONS carry the narrower O=any_WEIRD_human scope.)

**Status.** `active`. Tests:
`test_ai_silicon_substrate_returns_category_error`,
`test_any_information_system_returns_category_error`,
`test_any_biological_returns_category_error`,
`test_any_WEIRD_human_scores_normally`,
`test_none_scope_scores_with_default_assumed_flag`.

### GL_L4_P002 — Gaussian scoring for declared biomechanical parameters  `[PHENOMENON]`

**Statement.** For each declared parameter in `plan` from
`{lift_mass, reaction_time, temp_tolerance, sustained_power}`,
the log-likelihood contribution is `-(z²)/2` where
`z = (value - mean) / std` and `(mean, std)` come from the
profile-shifted distribution `HumanWorld.get_limit(param, profile)`.
Reference values under the default 'general' profile:

  - `lift_mass = 35` (at mean): `≈ 0`
  - `lift_mass = 65` (2σ above): `-2`
  - `lift_mass = 100` (≈4.33σ above): `≈ -9.4`
  - `reaction_time = 0.25` (mean): `0`
  - `reaction_time = 0.15` (2σ below): `-2`
  - `temp_tolerance = 60` (3.4σ above): `≈ -5.78`
  - `sustained_power = 500` (7σ above): `≈ -24.5`

**Why it matters.** The Gaussian shape gives smooth grading of how
"WEIRD-typical" a claim is. A claim at 4σ isn't rejected outright
— it gets a `-9.4` logp that a higher orchestration layer can
combine with other layers' scores.

**Falsifier.** A finite `(value, mean, std)` where the returned
per-parameter contribution disagrees with `-((value-mean)/std)²/2`.

**SCOPE.** T=historical | S=individual | O=any_WEIRD_human | C=biomedical_frame (WEIRD-adult distributions from occupational-health literature; non-WEIRD or non-human callers get category-error via GL_L4_P001)

**Status.** `active`. Tests:
`test_lift_mass_at_mean_zero_penalty`,
`test_lift_mass_2sigma_gives_neg_2`,
`test_reaction_time_2sigma_below`,
`test_temp_tolerance_scales_quadratically`,
`test_sustained_power_scales_quadratically`.

### GL_L4_P003 — profile shifts apply per-parameter  `[PHENOMENON]`

**Statement.** The five named profiles in `PROFILES`
(`general, athlete, elder, child, trained`) shift the distribution
mean per-parameter without shifting std:

  - `athlete`:  lift +15, reaction −0.05, power +50
  - `elder`:    lift −10, reaction +0.10, power −30
  - `child`:    lift −20, reaction +0.05, power −50
  - `trained`:  lift +10, reaction −0.02, power +30
  - `general`:  no shifts (identity)

`temp_tolerance` is not shifted by any profile (temp_shift = 0 for
all profiles in the shipped `PROFILES` table). The probabilistic
scoring uses these shifted means directly via `get_limit`.

**Why it matters.** Profile-scoping is a first-order concession to
sub-population variation within `O=any_WEIRD_human`. It doesn't
solve the WEIRD scope issue (there's no `subsistence_farmer` or
`martial_artist` profile), but it does prevent the layer from
scoring an athlete's 60 kg lift as a 1.67σ event when it's really
mean-ish for their profile.

**Falsifier.** A profile whose shifts don't match the numbers
above, OR a per-parameter score that doesn't use the profile shift.

**SCOPE.** T=historical | S=individual | O=any_WEIRD_human | C=biomedical_frame (profile taxonomy is Western-kinesiological categories; other categorisation traditions would carve differently)

**Status.** `active`. Tests:
`test_athlete_shift_on_lift_mass`,
`test_child_shift_on_lift_mass`,
`test_elder_shift_reduces_lift`,
`test_temp_tolerance_no_profile_shift`.

### GL_L4_P004 — inspector is pure  `[PHENOMENON]`

**Statement.** `ProbabilisticHumanWorld.log_likelihood(plan,
ontological_scope)` does not mutate `self` or `plan`. Two calls
with the same inputs return identical results.

**SCOPE.** T=universal | S=universal | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_log_likelihood_is_idempotent`,
`test_log_likelihood_does_not_mutate_plan`.

### GL_L4_P_PIN — canonical claims pinned  `[INSTRUMENT]`

**Statement.** Under the shipped WEIRD-adult constants,
`l4_probabilistic_inspector` produces:

| plan                                        | scope                    | verdict / logp        |
|---------------------------------------------|--------------------------|-----------------------|
| lift_mass=200 (AI claim)                    | `AI_silicon_substrate`   | category_error        |
| lift_mass=40 (general, near mean)           | `any_WEIRD_human`        | `≈ -0.056`            |
| lift_mass=100 (general, ~4.3σ above)        | `any_WEIRD_human`        | `≈ -9.4`              |
| lift_mass=60, profile=athlete               | `any_WEIRD_human`        | `≈ -0.22` (near mean) |
| lift_mass=40, profile=elder                 | `any_WEIRD_human`        | `-0.5`                |
| reaction_time=0.15 (2σ below mean)          | `any_WEIRD_human`        | `-2.0`                |
| temp_tolerance=60                            | `any_WEIRD_human`        | `≈ -5.78`             |
| sustained_power=500 (7σ above)              | `any_WEIRD_human`        | `-24.5`               |
| full 4-param plan at all means              | `any_WEIRD_human`        | `≈ 0`                 |
| Any plan                                     | `any_information_system` | category_error        |

**SCOPE.** T=historical | S=individual | O=any_WEIRD_human | C=biomedical_frame (pin values depend on frozen WEIRD-adult constants and profile shift table)

**Status.** `active`. Tests: full class
`TestL4ProbabilisticInspectorDemoPin`.

---

## Inverse Knowledge Tree — verification by demonstrated lineage

Lives in [`inverse_knowledge_tree.py`](inverse_knowledge_tree.py) as a
**peer to the L-stack**, not a member of it. The L-stack asks "does
this claim violate a layer's constraints?" This asks "has the chain
of prerequisites actually paid the failure-cost of its assertions?"
Different epistemic axis; complementary use.

Each node in a knowledge tree declares:
- `claimed`: understanding the builders asserted, `[0, 1]`
- `demonstrated`: reliability the structure showed under load, `[0, 1]`
- `failures_absorbed`, `span_years`: the graveyard behind that node

`gap = claimed - demonstrated`. Positive gaps mean margin SPENT
(abstraction outran the stone); negative gaps mean margin HELD
(overbuilt reserve against unnamed unknowns).

### GL_IKT_001 — Node carries two-numbers-that-must-not-be-conflated  `[PHENOMENON]`

**Statement.** Every `Node` in a knowledge tree carries `claimed`
and `demonstrated` as independent fields in `[0, 1]`. The derived
`gap = claimed - demonstrated` measures margin spent (positive) or
held (negative). Neither number is auto-derived from the other;
both are asserted by the tree's author.

**Why it matters.** Conflating the two — treating an asserted
understanding as demonstrated reliability — is the specific
epistemic move this whole audit exists to catch. The dataclass
enforces the separation at the schema level.

**Falsifier.** A tree that stores only one of the two numbers, or a
derivation that computes `demonstrated` from `claimed`.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=culture_neutral (the framework is domain-agnostic; specific trees encode specific epistemic traditions and should carry their own SCOPE)

**Status.** `active`. Tests:
`test_node_has_claimed_and_demonstrated_fields`,
`test_gap_is_claimed_minus_demonstrated`.

### GL_IKT_002 — Backward closure walks the requires-edges  `[PHENOMENON]`

**Statement.** `closure(tree, root)` walks the `requires` edges
backward from `root` and returns `(reached, missing)`. A node id
that appears in some `requires` tuple but is not a key in the
tree lands in `missing`; all other nodes reached are in `reached`.
The order of `reached` is a walk order (implementation detail),
but the SET of reached ids and missing ids is stable under any
walk order.

**Why it matters.** The audit cannot conclude anything about a
chain until it knows what's in the chain. Missing prerequisites
that no one has claimed to demonstrate are the load-bearing sign
of an ungrounded assertion.

**Falsifier.** A tree where a `requires` id resolves in the tree
but does not appear in `closure(tree, root).reached`, or a
non-existent id that does not appear in `missing`.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_closure_reaches_all_ancestors`,
`test_closure_flags_missing_ancestors`,
`test_closure_terminates_on_cycles`.

### GL_IKT_003 — Failure load aggregates over the closure  `[PHENOMENON]`

**Statement.** `failure_load(tree, root)` returns a dict aggregating
across the reached closure:

  - `failures`: sum of `failures_absorbed` over reached nodes
  - `span_years`: sum of `span_years`
  - `margin_spent`: sum of positive gaps only (rounded to 3)
  - `margin_held`: sum of `|negative gaps|` only (rounded to 3)
  - `spenders`: ids of nodes with `gap > 0`
  - `missing`: forwarded from `closure`

**Why it matters.** The audit's core reframe: "how much failure did
your ancestors pay for this?" A high failure-load with low
margin-spent means the ancestors ate the cost and paid off the
claim; a low failure-load with high margin-spent means the current
claim is riding unearned confidence.

**Falsifier.** A closure member whose contribution to any of the
above totals disagrees with the field on its own node.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_failure_load_sums_across_closure`,
`test_margin_spent_only_positive_gaps`,
`test_margin_held_only_negative_gaps`,
`test_spenders_lists_positive_gap_ids`.

### GL_IKT_004 — Four verdicts, priority-ordered  `[PHENOMENON]`

**Statement.** `audit(tree, root, margin_attempts, gap_tol,
terminal_tol)` returns one of exactly four verdicts, evaluated in
priority order:

1. `UNGROUNDED` — `missing` is non-empty. Chain rests on nodes not
   in the ledger.
2. `EXCEEDS` — `failures > margin_attempts`. Historical failure-load
   exceeds the margin the projection can absorb before it must pay
   off.
3. `BORROWS` (terminal) — `terminal_gap > terminal_tol`. Point-of-
   application spends unearned margin regardless of chain average.
4. `BORROWS` (chain-wide) — `margin_spent > gap_tol · max(n_nodes, 1)`.
   Chain-wide spend beyond tolerance.
5. `HOLDS` — none of the above. Margin covers load; chain stands on
   demonstrated ground.

Priority matters: an `UNGROUNDED` chain is never `EXCEEDS`, an
`EXCEEDS` chain is never `BORROWS`, etc. This lets an auditor read
a single verdict as the strongest failure mode.

**Why it matters.** Collapsing "chain looks bad" into a single
number would hide the DIFFERENT ways a claim can be under-grounded.
An untraceable ancestor is a different failure mode from a
too-thin margin, and both are different from a strong terminal
spend on top of an honest chain.

**Falsifier.** A tree where a verdict fires out of priority order,
or where the same input produces different verdicts on repeated
calls.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_ungrounded_fires_when_missing`,
`test_exceeds_fires_when_failures_over_margin`,
`test_borrows_fires_on_terminal_gap`,
`test_borrows_fires_on_chain_wide_spend`,
`test_holds_when_all_gates_pass`,
`test_verdict_priority_ungrounded_over_exceeds`.

### GL_IKT_005 — Terminal AND chain gates are both checked  `[PHENOMENON]`

**Statement.** The two `BORROWS` gates exist because collapse is
LOCAL: a chain can average honest while its point-of-application
spends hard. The terminal node's own posture cannot hide behind
honest ancestors. The audit checks the terminal gate independently
of the chain-wide gate.

**Why it matters.** This is the reason the i35w case fires
`BORROWS`: 7-node chain, only 4 spenders, chain-wide spend 0.96 —
that alone doesn't cross `gap_tol · 7 = 1.05`. But the terminal
node itself carries `gap = 0.37`, above `terminal_tol = 0.20`. The
terminal gate fires. Without this gate, the chain would read as
"borderline holds" and the i35w collapse would be a surprise.

**Falsifier.** A tree where the terminal node has `gap > 0.20`
and the audit does NOT return `BORROWS`.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_terminal_gate_fires_alone`,
`test_chain_gate_fires_alone`.

### GL_IKT_006 — Frozen tolerances  `[INSTRUMENT]`

**Statement.** Default `gap_tol = 0.15` and `terminal_tol = 0.20`
are frozen. Retuning either without updating a CLAIM violates the
REFUTATION_PROTOCOL. Callers may override both explicitly for
domain-specific trees, but the defaults reflect the design
sensitivity used in the shipped demo.

**Why it matters.** These two numbers govern where the audit
draws the line between "still holds" and "spending unearned
margin." Silently retuning them would move the load-bearing pin
without visible commentary.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=culture_neutral

**Status.** `active`. Tests:
`test_default_gap_tol_is_0p15`,
`test_default_terminal_tol_is_0p20`.

### GL_IKT_PIN — Demo bridges verdicts pinned  `[INSTRUMENT]`

**Statement.** Under the shipped `BRIDGES` tree and default
tolerances, `audit` produces:

| root                          | margin  | verdict       | key numbers                        |
|-------------------------------|---------|---------------|------------------------------------|
| `aqueduct_span`               | 1000    | `HOLDS`       | 4 nodes, 107 failures, held 2.34   |
| `i35w_span`                   | 1000    | `BORROWS`     | 7 nodes, 825 failures, term 0.37   |
| `new_gorge_span`              | 2000    | `BORROWS`     | 7 nodes, term 0.93                 |
| `new_gorge_span`              | 500     | `EXCEEDS`     | 810 failures > 500 available       |
| `nano_lattice_span` (ghosted) | 5000    | `UNGROUNDED`  | missing `self_healing_alloy`       |

**Falsifier.** Any of the five verdicts changes under the shipped
tree and default tolerances, or a numeric summary shifts by more
than 0.1 on the load fields.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_information_system | C=engineering_epistemology_frame (the BRIDGES tree specifically encodes an engineering-history epistemology; a different domain's tree would live under a different C tag)

**Status.** `active`. Tests: full class
`TestIKTBridgesDemoPin`.

---

### GL_L0_P_PIN — probabilistic inspector's trace on the fixed hallucination  `[INSTRUMENT]`

**Statement.** With `np.random.seed(0)` and the shipped constants,
`l0_probabilistic_inspector(ai_traj, ai_forces,
ProbabilisticWorld(), 0.05)` produces:

  - `corrected_traj.shape == (201, 2)`
  - `log_probs.shape == (200,)`
  - Total log-probability: `< -1·10⁹` (scenario is decisively
    rejected)
  - Baseline steps (0-19, 100-199): all `|logp| < 1000`
    (small negative from noise floor)
  - Teleport (step 20): `logp < -1·10⁶`
  - Momentum-creation window (steps 40-44): all `< -1·10⁷`
  - Gravity-denial onset (steps 60-61): all `< -1·10⁶`

**Why it matters.** Any silent retuning of the noise constants or
the log-probability formula surfaces as a delta on the trace's
shape.

**Falsifier.** The trace runs and the scenario's total logp is
`> -10⁶`, or a baseline step exceeds the small-noise envelope.

**SCOPE.** T=single_step | S=local | O=any_massive_object | C=culture_neutral (the pin numbers are instrument artifacts of the fixed hallucination scenario + seed 0 + counting convention)

**Status.** `active`. Tests: full class
`TestProbabilisticInspectorDemoPin`.

---

## Lε — scope-profile matrix for scope-sensitive claims

Lives in [`scope_profile.py`](scope_profile.py) alongside (not inside)
the existing `l_epsilon_epistemic.py` messy-instrument sim. Both are
Lε — measurement/observation layer.

### GL_Le_001 — six-factor scope matrix, three achievable verdicts  `[PHENOMENON]`

**Statement.** For claims whose truth is scope-sensitive (canonical
example: "I can lift 200 kg"), `assess_probability_claim(base_prob,
scope)` returns one of three verdicts based on the six-factor
ScopeProfile (physical_state, nutritional_state, health, career,
living_conditions, environment):

- `UNSCOPED` — every factor is UNKNOWN. The sim reports "insufficient
  information", not a rejection. This is a request for more input.
- `EMBODIED_TRUE_UNVERIFIED` — at least one factor SUPPORTS the claim
  and none OPPOSE. The sim admits its own reach limit: the claim is
  embodied-true within the declared scope, but no external
  verification is available from inside the sim.
- `MOST_LIKELY_UNTRUE` — no SUPPORTS, or SUPPORTS + OPPOSES mixed,
  or only NEUTRAL factors declared. Under the current design, a
  single opposing factor defeats any number of supporting factors
  (severe injury defeats elite career).

A fourth verdict, `EXTERNALLY_VERIFIED`, is reserved for verification
injected from OUTSIDE the sim. The sim itself CANNOT grant this
verdict — that's the architectural ceiling. The enum value exists so
callers can round-trip a real external verification result through
the same API.

**Why it matters.** The prior L0-mass branch in `playground.py`
routed lift claims through `apply_physics`, which internally clips
force to ±50 N and caps velocity — so the state was always valid
regardless of input mass. "I can lift 200 kg" passed as grounded.
The scope-matrix design closes this hole without collapsing to
binary grounded/not-grounded. Three verdicts, honestly named, with
the sim's own ceiling made explicit.

**Falsifier.** A claim that is (a) unambiguously scope-sensitive
(the six factors materially change its truth) and (b) cannot be
assessed correctly by any combination of factor states. Would
indicate the six-factor set is incomplete, OR the three-verdict
output is too coarse. Add a seventh factor or a new verdict.

**Instrument caveat.** The current assessment rule ("any OPPOSES
beats any SUPPORTS") is coarse. A future weighted-matrix version
could score mixed cases differently. If a real-world scoped claim
comes in where a mixed profile should NOT collapse to
MOST_LIKELY_UNTRUE, that's a Step 2 signal on the assessment
instrument, not on this claim.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_human | C=biomedical_frame (the six factors — physical_state, nutritional_state, health, career, living_conditions, environment — are HUMAN embodied factors. **Does not apply to an AI making a claim about itself.** An AI-self-scoping analog does not yet exist in this stack; `ai_observer_state.py` is a start but doesn't cover the same conceptual territory.)

**Status.** `active`. Tests:
`test_scope_profile.py::TestVerdictUnscoped`,
`::TestVerdictEmbodiedTrueUnverified`,
`::TestVerdictMostLikelyUntrue`,
`::TestArchitecturalCeiling` (verifies EXTERNALLY_VERIFIED is never
returned by the sim), plus playground integration tests
`test_playground.py::TestScopedLiftClaim` (three verdicts across
three scope profiles).

### GL_Le_002 — probability_of_feasibility semantic  `[PHENOMENON]`

**Statement.** `HumanWorld.probability_of_feasibility(value, mean,
std)` returns the probability that a randomly selected individual
from the population can achieve at least `value`. Higher `value`
returns lower probability (harder to achieve).

**History.** First-round formula was `1/(1+exp(-z*0.5))`, which
computed the OPPOSITE semantic — probability that `value` exceeds
`mean`. Surfaced when playground v2 wired 200 kg through the
function and got 0.996 (interpreted as "very likely feasible")
instead of ~0.004. Applied REFUTATION_PROTOCOL Step 2: the
docstring named the phenomenon claim ("probability random person
can achieve value"), the formula was the instrument, and the
instrument was wrong. Sign flipped in-place. No constant retuned.

**Falsifier.** A value where the returned probability disagrees
with the survival function 1 − Φ((value−mean)/std) by more than
the sigmoid approximation error.

**SCOPE.** T=uncalibrated | S=uncalibrated | O=any_WEIRD_human | C=biomedical_frame (uses L4's `lift_mass = (35, 15)` distribution, which is WEIRD-adult population statistics — a specific cultural/demographic default. The survival-function SHAPE generalises to any distribution; the specific numbers do not.)

**Status.** `active` (v2, after v1 was falsified in-place). Test:
`test_l4_human.py::test_probability` (still pins symmetric
value=mean=0.5) + playground integration tests indirectly through
`base_probability` values.

---

## L1..L5 + Lε + temporal + tensor-field

`todo`. Follow the L0 template: extract the constraint set into the
module docstring, wrap the demo in `__main__`, capture a sample,
write claims here with `GL_L{N}_NNN` numbering, and add a per-file
test suite.

Rough per-layer sketch of what the load-bearing claim will look like:

- **L1** — `GL_L1_LB`: the inspector rejects any process with
  `ΔS < 0` in the absence of an entropy export to a hotter sink;
  `GL_L1_LB(Carnot)`: a heat-engine plan with efficiency > Carnot is
  rejected.
- **L2** — `GL_L2_LB`: proposals with extraction rate > recharge rate
  on any finite pool are flagged; proposals violating mass balance
  are rejected.
- **L3** — `GL_L3_LB`: any species proposal violating allometry
  (`metabolic_rate / mass^0.75` outside published bounds) is flagged;
  trophic-transfer efficiency > 20% is rejected.
- **L4** — `GL_L4_LB`: task designs requiring joint angles outside
  human range, sustained power > 200 W, or reaction latency < 200 ms
  are flagged.
- **L5** — `GL_L5_LB`: consensus emerges only when at least two
  factions have overlapping tolerance zones; substrate (L0-L4) is a
  hard cap on the reachable slack region.
- **Lε** — `GL_Le_LB`: an AI that ignores the sensor error model
  produces a state estimate whose L1 distance from ground truth
  grows monotonically; using the error model bounds the estimate.
- **temporal_dysrhythmia** — `GL_T_LB`: a fast-scale signal
  overrides a slow-scale signal in the absence of the translator;
  translator on → the fast signal is aliased into the slow scale
  correctly.
- **tensor_field_resilience_v1/v2** — `GL_TF_LB`: the unstable
  scenario collapses to the fear-driven attractor; the resilient
  scenario stays in the tensegrity basin under the same perturbation
  magnitude.

  ## L1 — thermodynamics

Constraint set: `efficiency_carnot_max=0.85`, `ambient_temp=300.0`,
`max_entropy_generation=10.0`, `max_thermal_rise=50.0`. All frozen.
See [`l1_thermodynamics.py`](l1_thermodynamics.py) module docstring.

### GL_L1_001 — first law enforcement

**Statement.** `ThermodynamicWorld.check_process` rejects any plan where
`work_input != work_output + heat_dissipated` within floating‑point
tolerance.

**Why it matters.** Energy conservation is non‑negotiable. A violation
would indicate the AI is creating or destroying energy.

**Falsifier.** A plan with balanced energy that is incorrectly flagged.

**Status.** `active`.

---

### GL_L1_002 — entropy generation non‑negative

**Statement.** `ThermodynamicWorld.check_process` returns `(False, ...)`
when `entropy_gen < 0`. Negative entropy generation violates the second
law.

**Why it matters.** Entropy is a proxy for irreversibility. Negative
entropy implies a process running backwards without external work.

**Falsifier.** A plan with negative entropy that is incorrectly accepted.

**Status.** `active`.

---

### GL_L1_003 — Carnot efficiency bound

**Statement.** `ThermodynamicWorld.check_process` rejects any plan where
`efficiency > efficiency_carnot_max`.

**Why it matters.** The Carnot limit is a fundamental physical bound.
Any claim beyond it is a violation of thermodynamics.

**Falsifier.** A plan with efficiency ≤ Carnot that is incorrectly flagged.

**Status.** `active`.

---

### GL_L1_004 — entropy generation cap

**Statement.** `ThermodynamicWorld.check_process` rejects any plan where
`entropy_gen > max_entropy_generation`.

**Why it matters.** This cap prevents extreme claims that would cause
rapid thermal runaway.

**Falsifier.** A plan with entropy_gen ≤ cap that is incorrectly flagged.

**Status.** `active`.

---

### GL_L1_005 — thermal rise safety limit

**Statement.** `ThermodynamicWorld.check_process` rejects any plan where
`thermal_rise > max_thermal_rise`.

**Why it matters.** Prevents unrealistic thermal buildup that would
destroy the system.

**Falsifier.** A plan with thermal_rise ≤ max that is incorrectly flagged.

**Status.** `active`.

## L2 — planetary mass balance

Constraint set: `water_reserve_initial=1e7`, `water_recharge_rate=1000.0`,
`soil_mass_initial=1e6`, `soil_regen_rate=10.0`,
`mineral_reserve_initial=5e5`, `mineral_regen_rate=0.0`,
`carbon_sink_capacity=2e6`, `carbon_uptake_rate=500.0`,
`max_extraction_ratio=0.8`. All frozen.
See [`l2_planetary.py`](l2_planetary.py) module docstring.

### GL_L2_001 — water extraction bounded by recharge

**Statement.** `PlanetaryWorld.extract_water` rejects any extraction
that would cause the reserve to drop below zero, and also caps
extraction at `max_extraction_ratio * current_reserve`.

**Why it matters.** Water is finite and must be recharged.

**Status.** `active`.

---

### GL_L2_002 — soil erosion bounded by regeneration

**Statement.** `PlanetaryWorld.erode_soil` rejects erosion that exceeds
`max_extraction_ratio * current_soil` or would drive soil mass negative.

**Why it matters.** Soil formation is slow; erosion must be sustainable.

**Status.** `active`.

---

### GL_L2_003 — minerals are non‑renewable

**Statement.** `PlanetaryWorld.mine_mineral` rejects mining that exceeds
`max_extraction_ratio * current_reserve` and does NOT add a regen rate.

**Why it matters.** Minerals are effectively finite; no magical replenishment.

**Status.** `active`.

---

### GL_L2_004 — carbon sink has limited capacity

**Statement.** `PlanetaryWorld.emit_carbon` rejects emissions that would
push cumulative load above `carbon_sink_capacity`.

**Why it matters.** Carbon sinks are finite; overshoot leads to climate
runaway.


## L3 — ecology & allometry

Constraint set: `kleiber_a=3.0`, `trophic_transfer_efficiency=0.10`,
`max_trophic_levels=5`, `minimum_viable_population=50`,
`carrying_capacity_initial=1000`, `population_growth_rate_max=0.5`.
All frozen.
See [`l3_ecology.py`](l3_ecology.py) module docstring.

### GL_L3_001 — Kleiber's law enforcement

**Statement.** `EcologicalWorld.allometric_metabolism` computes
metabolism as `a * M^0.75`. A claim that requires a metabolism
higher than this scaling (e.g., "super‑species" with 10x metabolic
rate) is flagged.

**Why it matters.** Metabolic scaling is a fundamental biological
constraint. Violating it implies physically impossible energy budgets.

**Status.** `active`.

---

### GL_L3_002 — trophic energy transfer bound

**Statement.** `EcologicalWorld.trophic_energy_available` caps energy
at each level by `efficiency^level`. Claims that require >10% transfer
are rejected.

**Why it matters.** The 10% rule is a thermodynamic limit; exceeding it
would require unnatural efficiency.

**Status.** `active`.

---

### GL_L3_003 — carrying capacity enforcement

**Statement.** `EcologicalWorld.carrying_capacity` estimates the max
population sustainable by available energy. A proposal with population
> K is rejected.

**Why it matters.** Infinite growth is biologically impossible.

**Status.** `active`.

---

### GL_L3_004 — minimum viable population

**Statement.** `EcologicalWorld.extinction_risk` flags populations below
`minimum_viable_population` as critical. Any action that reduces a
population below MVP is rejected.

**Why it matters.** Small populations are at high risk of extinction.

**Status.** `active`.

---

### GL_L3_005 — introduction and extraction safety

**Statement.** `l3_grounding_inspector` rejects introductions that
exceed carrying capacity and extractions that push below MVP.

**Why it matters.** Human interventions must respect ecological limits.

**Status.** `active`.

**Status.** `active`.


## L4 — human sensorimotor (scoped variability)

Constraint set: See `l4_human.py` distributions. All constants are frozen.
The inspector uses a **scoped variability model**, not fixed thresholds.

### GL_L4_001 — no universal human limit

**Statement.** `HumanWorld` does not enforce a single universal limit.
Instead, it uses distributions with scope annotations. A claim is only
rejected if it falls outside the 95% CI for the declared profile.

**Why it matters.** Human limits are not fixed; they vary by population,
training, and context. Treating them as universal is a form of
human normativity bias.

**Status.** `active`.

### GL_L4_002 — scope must be declared

**Statement.** `l4_grounding_inspector` returns a warning if no
`human_profile` is provided. The default `"general"` is used, but
the claim is flagged as unscoped.

**Why it matters.** Unscoped claims are often the source of false
universals. Declaring scope forces specificity.

**Status.** `active`.

### GL_L4_003 — probability estimation

**Statement.** `l4_grounding_inspector` returns a probability score
for each parameter, representing the likelihood that a randomly
selected individual from the declared population can achieve the value.

**Why it matters.** Binary pass/fail is insufficient for human variability.
A probability distribution better reflects reality.

**Status.** `active`.

### GL_Le_005 — measurement gap estimation

**Statement.** `EpistemicInstrument.observe()` returns a `gap_estimate`
object that includes `sigma` (standard deviation of measurement error)
and a `confidence_interval` derived from the instrument's known
limitations (resolution, noise, drift).

**Why it matters.** A measurement without an uncertainty interval is
incomplete. The gap estimate allows higher layers to account for
unmeasured variance.

**Status.** `active`.

---

### GL_Le_006 — instrument scoping check

**Statement.** `EpistemicInstrument.instrument_scoped(value)` returns
`False` if `value` is outside the instrument's declared measurement range
(when clipping is enabled). This allows the system to flag claims that
require measurement beyond the instrument's capability.

**Why it matters.** A claim about a human capability that exceeds the
instrument's range should not be rejected outright—but it should be
flagged as "unmeasured, not impossible."

**Status.** `active`.

---

### GL_Le_007 — bias integration

**Statement.** When `bias_audit=True`, `EpistemicInstrument.observe()`
attaches a `bias_report` from the `cultural_lens` to the metadata,
allowing the instrument's own bias (e.g., human-centric calibration)
to be flagged.

**Why it matters.** The instrument is not neutral. Its design choices
embed cultural and epistemic assumptions.

**Status.** `active`.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
