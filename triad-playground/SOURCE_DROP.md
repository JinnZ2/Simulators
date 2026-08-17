# SOURCE_DROP

The delivered proposal, verbatim. Analysis is in [`README.md`](README.md) and
[`CLAIM_TABLE.md`](CLAIM_TABLE.md); the runnable check on the shadow pattern
is [`shadow_design.py`](shadow_design.py).

---

Then the playground isn't a physics sandbox or an AI benchmark. It's a
**triad harness**: every experiment involves three agents — the physical
system, the measurement instrument, and the reasoning agent (human or AI).
The claim is only as strong as the weakest calibration in the chain.

## The Triad Playground Protocol

### The Three Agents

Every sim in the playground is a tuple:

```
(Physical System, Measurement Instrument, Reasoning Agent)
```

| Agent | Role | Calibration Question |
| --- | --- | --- |
| Physical | The thing being studied | Is the system in a known state? |
| Instrument | The thing producing numbers | Is the instrument calibrated and traceable? |
| Reasoning | The thing interpreting numbers | Is the observer's gain known? |

The "interior calibration" framework applies to all three. The AI is an
instrument. The human is an instrument. The physical system has its own state
that drifts with temperature, load, history.

### The Dial is a Vector

Not a scalar. Every sim has three independent dials:

```json
{
  "physical_dial": {
    "low": "synthetic / analytical / hand calc",
    "medium": "FEM / reduced-order model",
    "high": "full experiment / LAMMPS / field test"
  },
  "instrument_dial": {
    "low": "single sensor, no cross-check",
    "medium": "redundant sensors, statistical averaging",
    "high": "full metrological chain, NIST-traceable, environmental compensation"
  },
  "reasoning_dial": {
    "low": "pattern match, heuristic, cached response",
    "medium": "step-by-step, cross-referenced, uncertainty propagation",
    "high": "full mechanism reconstruction, multiple hypotheses, adversarial check"
  }
}
```

### The Cross-Gradient is the Point

The playground's purpose is to measure how errors in one agent propagate
through the others.

Example: run the same aluminum smelting sim (physical dial = medium, FEM)
with three reasoning settings:

| Run | Reasoning Dial | Result | Interpretation |
| --- | --- | --- | --- |
| 1 | Low (heuristic) | "Crack at 200 cycles" | Pattern-matched from previous casting |
| 2 | Medium (step-by-step) | "Crack at 1,800 cycles ± 400" | Propagated uncertainty from grain size distribution |
| 3 | High (mechanism) | "No crack predicted; heuristic was wrong because this is wrought, not cast" | Reconstructed the microstructure difference |

The cross-gradient here is `∂(conclusion)/∂(reasoning_dial)` at fixed
`physical_dial`. If the conclusion changes sign when you turn the reasoning
dial, the physical sim is underdetermined — the reasoning agent is doing more
work than the physical model supports. That's a G-LAYER violation: the
reasoning claim is at a higher layer than the physical evidence can carry.

### The Shadow Sim Pattern

For every physical sim, run a shadow with the same instrument dial but
different reasoning agents:

1. **Human shadow**: You run the numbers yourself, no AI. Record your
   confidence, fatigue level, time pressure.
2. **AI-low shadow**: Fast model, no extended thinking.
3. **AI-high shadow**: Reasoning model, full budget.
4. **Consensus shadow**: Do the three agree? If not, the axis is
   underdetermined.

This is `explore.py` at the triad level: it widens the reasoning declaration
and ranks nothing. It tells you whether the conclusion is robust to the
observer, or whether it's an artifact of one observer's gain.

### The Metrological Pedigree

Every number in the playground carries a full pedigree:

```json
{
  "value": 1.555,
  "units": "dimensionless",
  "physical_dial": "cascade_generator_E0=2000",
  "instrument_dial": "box_count_50_scales",
  "reasoning_dial": "human_fatigued_6hr_shift",
  "calibration_status": {
    "physical": "generator_params_declared",
    "instrument": "controls_run_line_lattice_poisson",
    "reasoning": "self_reported_fatigue_7/10"
  },
  "traceability": [
    "sim_b_v3_boxcount_detailed",
    "human_operator_JinnZ2",
    "ambient_temp_-35C",
    "time_2204_local"
  ],
  "gate_verdict": {
    "G-RES": "supported",
    "G-DIM": "supported",
    "G-CTRL": "supported",
    "G-LAYER": "qualified_generator_not_physical",
    "G-IND": "n=1_caution"
  }
}
```

This is what makes it metrology, not just simulation. The number is
inseparable from the chain that produced it.

### The Interior Calibration Checklist (Pre-Sim)

Before any triad sim runs:

**Physical**
- [ ] System state declared (temperature, load, history)
- [ ] Boundary conditions specified
- [ ] Known unknowns listed

**Instrument**
- [ ] Calibration date / method
- [ ] Environmental compensation applied?
- [ ] Cross-check instrument identified

**Reasoning**
- [ ] Human: fatigue, cold, time pressure, emotional investment
- [ ] AI: model version, thinking budget, temperature, context window
- [ ] Conflict of interest declared (do I want this result?)

If any check is unreadable, the server is uncalibrated and the chain knows it.

### The Playground Workflow

```
1. PROPOSE
   └─ Declare triad (physical, instrument, reasoning)
   └─ Declare dials for each
   └─ Declare skip_condition
   └─ G-PRE: Is the resolution pair declared? Deny if not.

2. CALIBRATE
   └─ Run interior calibration checklist
   └─ If any agent uncalibrated, flag and continue with caution

3. SHADOW
   └─ Run at lowest dial on all three axes
   └─ Run human shadow (if human is available)
   └─ Run AI-low and AI-high shadows
   └─ Do shadows agree? If not, axis is underdetermined.

4. GATE
   └─ Feed results through reasoning-gate
   └─ Record verdict per number

5. SKIP OR SCALE
   └─ Skip condition met? → Kill axis, log why.
   └─ Promising? → Upgrade ONE dial at a time, re-shadow.
   └─ Never upgrade all three simultaneously (can't attribute variance).

6. AUDIT
   └─ Cross-gradient: did conclusion change with dial setting?
   └─ If yes, the conclusion is dial-dependent, not system-dependent.
   └─ Downgrade claim accordingly.
```

### First Sim Family: "The Observer Effect in Measurement"

This bridges all three domains.

**Physical**: A simple thermal expansion measurement (aluminum bar, -40°C to
+20°C).

**Instrument**: A dial indicator (mechanical, no electronics to fail in cold).

**Reasoning**: Three observers — you fatigued, you rested, AI-low, AI-high.

**Question**: How much of the "measurement error" is actually observer-state
variance?

**Hypothesis**: At -40°C, the instrument is stiff and the human is
cold-stiffened. Both introduce lag. The AI doesn't know about the
cold-stiffening unless you tell it. The uncalibrated server is the human's
proprioception + the AI's lack of embodied context.

**Skip condition**: If all four observers agree within instrument resolution,
observer variance is negligible. Skip to next axis.

**Dial settings**:
- Physical: analytical (known expansion coefficient) → low
- Instrument: single measurement, no replication → low
- Reasoning: human rested → baseline; then human fatigued; then AI-low; then
  AI-high

This is cheap. It's phone-buildable. It tests the core claim of the interior
calibration framework with a physical artifact you can hold.

### What You'd Need to Build

Not software. Just:

1. The triad schema (JSON spec, like `guards.json`)
2. The shadow protocol (which shadows run, in what order)
3. The interior calibration checklist (markdown, human-fillable)
4. The pedigree format (how every number gets tagged)

The reasoning-gate already handles the epistemics. The playground just applies
it at the system level.
