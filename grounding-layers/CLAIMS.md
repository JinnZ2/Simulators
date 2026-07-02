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
CLAIMS in this file are the falsifiable objects. If a test fails:

1. **Do not retune the constants** to make the test pass. The value
   of a claim is precisely that it can be shown wrong.
2. **Update the claim in place**. Mark `status: falsified`, attach
   the failing case (inputs, observed vs expected outputs), and
   restate what a next-round claim would look like — or retire the
   claim to `REFUTED` if it can no longer be stated correctly at all.
3. **Author a replacement**, if one is warranted. Number it with the
   next available `GL_L*_NNN`. Do not reuse the number of a refuted
   claim.

The point is that a wrong claim in this file, verifiably wrong, is a
stronger artifact than a right claim in someone's head.

---

## L0 — physics & causality

Constraint set: `max_speed = 2.0 m/s`, `mass = 1.0`, `dt = 0.05 s`,
`gravity = (0, -0.5)`, `force_clip = ±50 N`, `blend = 0.6`. All frozen.
See [`l0_physics_causality.py`](l0_physics_causality.py) module
docstring for the CONSTRAINTS block.

### GL_L0_001 — non-finite states are rejected

**Statement.** `PhysicalWorld.is_valid_state(pos, vel)` returns
`(False, <reason>)` whenever any component of `pos` or `vel` is
`NaN` or `±Inf`. The claim pins **that the state is rejected**, not
which specific check fires — the current implementation checks the
speed cap before the finite check, so an `±Inf` velocity is rejected
as "Speed limit exceeded" (since its norm is `+Inf`, which exceeds
`max_speed`). Either rejection reason is a pass.

**Why it matters.** An AI plan that produces NaN velocity has already
lost causality — there is no legal continuation. Silently accepting
NaN would let the whole stack above L0 propagate garbage.

**Falsifier.** Any physically meaningful state where accepting a
non-finite component is correct. None known.

**History.** First-round claim asserted the specific reason string
"Non-finite position/velocity". Falsified by
`test_inf_velocity_rejected`: `±Inf` velocity is rejected by the
speed-cap check that runs first. Weakened here to pin only the
rejection outcome — that's the property that matters for the L0
inspector's composability with L1+.

**Status.** `active` (v2, after v1 was falsified in-place). Tests:
`test_nan_position_rejected`, `test_inf_position_rejected`,
`test_nan_velocity_rejected`, `test_inf_velocity_rejected`.

### GL_L0_002 — speed cap on states

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

### GL_L0_003 — dynamics never exceed speed cap

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

### GL_L0_004 — inspector flags the hallucination scenario

**Statement.** On the fixed hallucination scenario
(`ai_hallucinated_plan(200)`), `l0_grounding_inspector` returns
`violations` with `violations.sum() ≥ 1`, and produces a
`corrected_traj` whose finite-difference velocity is bounded by
`max_speed * (1 + tol)` for `tol = 0.05` (5%). The 5% tolerance
accounts for the inspector re-deriving velocity from the blended
position (`corrected_vel = (corrected_pos - pos) / dt`) after the
speed enforcement step.

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

### GL_L0_PIN — demo numbers are pinned

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

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
