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

**Status.** `active`. Tests: full class
`TestL2ProbabilisticInspectorDemoPin`.

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
