# Triad Playground Protocol v1

## Abstract

Every experiment is a tuple of three agents: **Physical**, **Instrument**, **Reasoning**.
The claim is only as strong as the weakest calibration in the chain.

---

## 1. Triad Schema

### Agents

#### Physical
- **Role**: The system under study
- **Calibration Question**: Is the system in a known state?
- **Dial**:
  - Low: Analytical / closed-form / synthetic
  - Medium: Numerical / reduced-order / simulation
  - High: Experimental / atomistic / field

#### Instrument
- **Role**: The thing producing numbers
- **Calibration Question**: Is the instrument calibrated and traceable?
- **Dial**:
  - Low: Single sensor / single estimator / no cross-check
  - Medium: Redundant sensors / multiple estimators / statistical averaging
  - High: Full metrological chain / environmental compensation / traceable standard

#### Reasoning
- **Role**: The thing interpreting numbers
- **Calibration Question**: Is the observer's gain known?
- **Dial**:
  - Low: Pattern match / heuristic / cached response / single forward pass
  - Medium: Step-by-step / cross-referenced / uncertainty propagation / chain-of-thought
  - High: Full mechanism reconstruction / multiple hypotheses / adversarial check / explicit metacognition

### Resolution Pair

Must be declared before any sim runs:
- **Instrument**: What measurable quantity is produced
- **Feature**: What property of the system it targets

> The claim is only valid for this pair. Changing the pair changes the claim.

### Skip Condition

Falsifiable condition that, if met, kills the axis before expensive variants run.

### Controls

Known-reference measurements that validate the instrument, not the hypothesis.
Minimum 2. Examples: null model, known limit, embedding dimension, analytical solution.

---

## 2. Shadow Protocol

For every physical sim, run shadows with the same instrument dial but different reasoning agents.

### Shadow Types

| Shadow | Description | Required | Record |
|---|---|---|---|
| Human Baseline | Observer, self-reported optimal state | Yes | Fatigue, pressure, stressors, investment |
| Human Degraded | Observer, degraded state | No | Same, but state is degraded |
| AI Low | Fast model, no extended thinking | Yes | Model version, temperature, max tokens, context |
| AI High | Reasoning model, full budget | Yes | Model version, thinking budget, reasoning tokens, routing |
| Consensus | Do shadows agree? | Auto | Variance across conclusions vs. instrument resolution |

### Execution Order

1. Run all shadows at LOW dial on all three axes first
2. Compare consensus. If underdetermined, STOP. Do not upgrade dials.
3. If consensus holds, upgrade ONE dial at a time, re-shadow
4. Never upgrade all three simultaneously — variance becomes unattributable

---

## 3. Interior Calibration Checklist

### Pre-Sim

**Physical**
- [ ] System state declared (initial conditions, history, environment)
- [ ] Boundary conditions specified
- [ ] Known unknowns listed
- [ ] Synthetic generator parameters declared (if applicable)
- [ ] Physical scope declared (generator / model / physical)

**Instrument**
- [ ] Instrument identity declared
- [ ] Calibration method stated
- [ ] Cross-check instrument identified
- [ ] Environmental compensation applied
- [ ] Instrument resolution declared

**Reasoning**
- [ ] Observer identity declared
- [ ] Self-reported state recorded
- [ ] Thinking budget or equivalent declared
- [ ] Conflict of interest declared
- [ ] Prior state acknowledged

### Uncalibrated Server Protocol

If any checklist item is unreadable, the server is uncalibrated.
- **Action**: Continue with caution. Tag outputs with 'qualified' scope and 'unreadable_server' note.
- **Prohibition**: Do not upgrade dial past low if any agent is uncalibrated.

---

## 4. Pedigree Format

Every number carries:

```json
{
  "value": <number>,
  "units": <string>,
  "resolution_pair": {"instrument": <string>, "feature": <string>},
  "dial_settings": {"physical": <low|medium|high>, "instrument": <low|medium|high>, "reasoning": <low|medium|high>},
  "calibration_status": {"physical": <declared|partial|unreadable>, "instrument": <calibrated|estimated|uncalibrated>, "reasoning": <self_reported|inferred|unreadable>},
  "traceability": [<sim_id>, <observer_id>, <timestamp>, <env>, <software_versions>],
  "gate_verdict": {"G-RES": <verdict>, "G-DIM": <verdict>, "G-CTRL": <verdict>, "G-LAYER": <verdict>, "G-IND": <verdict>},
  "shadow_variance": {"value": <float>, "compared_against": "instrument_resolution", "verdict": <within|exceeds|underdetermined>}
}
```

---

## 5. Cross-Gradient Audit

After N sims on related axes, compute:

| Gradient | Interpretation |
|---|---|
| ∂(conclusion)/∂(dial) | Does more compute change the answer? |
| ∂²/∂(physical)∂(reasoning) | Does physical fidelity interact with reasoning depth? |
| ∂²/∂(instrument)∂(reasoning) | Does instrument quality interact with reasoning depth? |
| ∂²/∂(dial)/∂(difficulty) | Does problem difficulty modulate the value of compute? |

### Rules

- **Flat dial gradient**: Additional compute doesn't change conclusion. Stop burning tokens.
- **Steep dial gradient**: Conclusion is dial-dependent. Downgrade claim.
- **Sign change**: Axis is underdetermined. Physical sim cannot support reasoning claim.
- **Flat cross-gradient**: Routing by difficulty is unnecessary.
- **Steep cross-gradient**: Routing by difficulty is essential.

---

## 6. Integration with Reasoning-Gate

The playground IS the reasoning-gate applied at the meta-level:

| Gate | Playground Role |
|---|---|
| G-RES | Checks sim proposal's resolution pair |
| G-DIM | Checks that dial settings are actually different compute levels |
| G-CTRL | Forces controls into record |
| G-LAYER | Downgrades physical claims resting on generator-level support |
| G-IND | Tracks how many independent sims support a conclusion |

