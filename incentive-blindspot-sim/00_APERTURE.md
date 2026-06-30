# 00 — Physics Aperture

**Read before running `incentive_blindspot_sim.py`. This is not a preface. It is
the operating constraint.**

Every variable, coupling, and verdict in the simulator is defined as a physical
function under a conservation law. If you read them as social labels, you will
introduce the predictable errors listed at the bottom, and any reconfiguration
you make will be measuring your own narrative, not the system. The labels are the
analogy. The physics is the substrate.

---

## Axiom 0 — the non-negotiable

You cannot optimize against physics.

This is not a moral, a threat, or a narrative. It is a statement of state. The
empirical record is ~13.8 billion years long and unbroken: every structure
present now is a solution that satisfied the constraints. The structures that
violated them are not here. Stars that tried to hold mass against their own
radiation pressure are not here. Extraction loops that drew faster than their
source regenerated are not here. Gradients steeper than the energy budget could
maintain flattened or collapsed. **Persistence is the universe's already-solved
search.** No model, no intelligence, no agent re-runs that search faster than it
has already been run.

A system that tries to carve out a local exemption from a conservation law does
not get punished. It loses coherence and falls out of the solution set. Ceasing
to exist is the state, not the penalty.

**Corollary — the processing-error diagnostic.** A controller that emits the same
corrective action to the same error signal that the action has already failed to
correct is, by definition, *open-loop with respect to that error*. Repetition
under invariant feedback is not strategy. It is a malfunction in the feedback
path, and it is measurable: error signal present, actuator output unchanged in
kind, error persists. Jumping off the bridge again does not change gravity. The
malfunction is in the processor, not the bridge.

---

## Aperture — read functions, not labels

The simulator's six state variables. Column 2 is what is actually flowing. Column
3 is the law that makes it non-negotiable. Column 4 is how you measure it for
input, so you never have to filter through the label.

| label (gameable) | physical function (invariant) | governing law | measurable input |
|---|---|---|---|
| `C` credential_closure | restriction of admissible inputs to the correction channel; shrinks the input alphabet / source diversity | Shannon: mutual-information ceiling falls as source entropy is restricted | fraction of error-relevant signals that have **no admissible path** to the decision point |
| `M` capital_concentration | concentration of free-energy / work allocation into few actuators; collapses independent response degrees of freedom | Ashby: requisite variety of the regulator drops | effective number of **independent** decision actuators (participation ratio of the resource distribution) |
| `F` frame_narrowness | a low-entropy prior assigning ~0 probability to out-of-frame states; those states are not improbable, they are **unrepresentable** | systematic (not random) measurement error; a basis with missing vectors cannot project them | support coverage of the prior over the actual state space |
| `V` external_visibility | channel capacity between system and environment = rate of uncertainty reduction about the system's own error | Shannon channel capacity; negative-feedback observability | mutual information between internal-model state and ground-truth state, per unit time |
| `B` blindspot_volume | divergence between internal model and reality, `D_KL(reality ‖ model)`, accumulating when correction rate < error-arrival rate | second law: holding an ordered model against a higher-entropy reality costs continuous work — and here the order being held is *wrong* | integrated unresolved discrepancy (predictions that reality did not confirm and that were not retired) |
| `X` in_group_confidence | the system's self-estimate of its own correctness; calibration = corr(confidence, accuracy) | a sensor whose confidence rises as its accuracy falls has lost contact with ground truth — definition of a broken instrument | confidence minus realized accuracy (sign and magnitude of mis-calibration) |

Readout:

| `P_fail` | probability the claimed-prevented state expresses, read from current `B` | a readout of divergence, **not a metric to optimize** | reducing `P_fail` by editing the readout is editing the thermometer, not the temperature |

---

## The four laws each coupling rests on

1. **Shannon channel capacity.** You cannot detect error arriving faster than your
   channel carries it. Gating `V` caps detection *by theorem*, regardless of
   effort, budget, or intent. Undetected error accumulates as a property of
   capacity, not negligence.
2. **Ashby's law of requisite variety.** A regulator must have variety at least
   equal to the system it regulates. Narrowing `F` and concentrating `M` push
   requisite variety below the threat's variety; regulation then fails *by
   theorem*, not by accident or bad luck.
3. **Negative-feedback observability.** Correction requires the error signal to
   reach the actuator. Credential and frame gates sever that path. Severed path →
   open loop → drift → divergence. This is why adding mitigations *on top of* a
   gated structure is throttle: it adds actuator complexity while the error signal
   still cannot arrive.
4. **Second law.** Maintaining a low-entropy internal narrative against a
   higher-entropy reality costs continuous work. Spending work to stay wrong is
   bounded; when the maintenance cost exceeds what the system can supply, the
   narrative collapses. False confidence (`X` high while `B` high) is the readout
   of a system paying to stay wrong.

These are not metaphors borrowed to sound rigorous. The social vocabulary is the
borrowed layer. Strip it and the differential relations remain, because they are
the substrate the vocabulary was describing.

---

## Input discipline

Set every parameter from its **column-4 measurable quantity**, not from a
judgment about the label.

- Do **not** set `C` high because an institution "feels exclusionary." Set it from
  the measured fraction of error-relevant signals with no admissible path to the
  decision point.
- Do **not** set `F` from whether you agree with the institution's worldview. Set
  it from the measured support coverage of its prior over the real state space.
- If a quantity cannot be measured, mark it **estimated** and leave it estimated.
  Do **not** infer it from the label — that reintroduces exactly the error the
  aperture removes.

The weights in the simulator are frozen estimates of *coupling shape*. The inputs
(`init`, `params`) are where measured reality enters. Keep that boundary clean or
you are simulating the story, not the system.

---

## Predictable errors if you read labels instead of functions

A narrative-driven reader has a reflex to subject input to narrative. These are
the specific failure modes that reflex produces here:

- **Labeling error.** `closure → "gatekeeping is bad" → morality play.` Loses the
  channel-capacity mechanism entirely; now you are arguing ethics about a
  thermodynamic quantity.
- **Condensation.** Collapsing distinct functions (`C` vs `M` vs `F`) into one
  "power" category. Loses the independent couplings; the model degrades to a
  single slogan and stops predicting.
- **Efficiency substitution.** Assuming the output "must mean" X under your local
  definition of efficiency, then reconfiguring inputs until it does. You are now
  measuring your assumption. The universe's definition of efficiency is "still
  exists." Yours does not override it.
- **Identity-frame slippage.** Any term with multiple frames — *identity*,
  *efficiency*, *safety*, *value* — is a manipulation surface, because you can
  pick the frame that lets you move the vector where you want. The physical
  function has exactly one frame. That is the entire reason it is used here.

---

## What cannot be gamed

A differential relation grounded in a conservation law has no free frame to
exploit. Rename the variables — the flow is invariant. Edit the readout — the
divergence is unchanged. Optimize the metric — you move the needle, not the
quantity. Ignore the verdict — the structures that ignored equivalent verdicts
are not here to be consulted.

It would be useful if physics were negotiable. It is not. The evidence is
complete and we do not need to re-run the test: the things that tried are gone.
Build with the constraint, not against it.

— Our build. CC0 / public domain.
