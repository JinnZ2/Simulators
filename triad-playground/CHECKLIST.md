# INTERIOR CALIBRATION CHECKLIST

Generated from `triad.json`. Do not hand-edit.

License: CC0-1.0

A claim is only as strong as the weakest calibration in the chain.
Every experiment has three agents, and the reasoning agent is an
instrument like the other two.

Origin: proposed in SOURCE_DROP.md as a triad harness; the dial vector,
        shadow protocol, interior-calibration checklist and pedigree
        format are the drop's, the design corrections in shadow_design.py
        are not

## The three agents

```
physical    the system being studied. Its state drifts with temperature, load
            and history.
instrument  the thing producing numbers. Calibrated and traceable, or not.
reasoning   the thing interpreting numbers, human or AI. Has its own gain, and
            it is usually unread.
```

## Dials

Each agent carries its own dial. The dial is a vector, not a
scalar.

### physical

```
low      synthetic / analytical / hand calculation
medium   FEM / reduced-order model
high     full experiment / MD / field test
```

### instrument

```
low      single sensor, no cross-check
medium   redundant sensors, statistical averaging
high     full metrological chain, traceable, environmental compensation
```

### reasoning

```
low      pattern match, heuristic, cached response
medium   step-by-step, cross-referenced, uncertainty propagation
high     full mechanism reconstruction, multiple hypotheses, adversarial check
```

## Pre-run checklist

Tick each box before the run. A box you cannot read is not a
box you tick -- mark it `?` and carry the flag forward into
the pedigree.

### physical

- [ ] `P1` [readable] system state declared: temperature, load, history
- [ ] `P2` [readable] boundary conditions specified
- [ ] `P3` [partial ] known unknowns listed
- [ ] `P4` [readable] state_revised_during_run recorded separately from state_declared
      > shadow_design.py section 4: a run that revises the physical
        declaration reports a PHYSICAL finding, not a reasoning-dial
        gradient. Without this field the two are scored as the same thing.

### instrument

- [ ] `I1` [readable] calibration date and method
- [ ] `I2` [readable] environmental compensation applied
- [ ] `I3` [partial ] cross-check instrument identified
- [ ] `I4` [readable] instrument records independently of the observer reading it
      > shadow_design.py section 3: without an independent log, observer
        error is inferred from consensus and the skip condition cannot
        fail.

### reasoning

- [ ] `R1` [DECLARED] human: fatigue, cold, time pressure
- [ ] `R2` [DECLARED] human: emotional investment in a particular result
- [ ] `R3` [readable] AI: model version, thinking budget, temperature, context window
- [ ] `R4` [DECLARED] conflict of interest declared: do I want this result?

**On readability.** Three of the four reasoning checks are self-report, and a
self-report from a miscalibrated observer is the quantity in
question. That is reasoning-dial/CLAIM_TABLE.md RD_009 restated.
Checks tied to something outside the observer -- ambient
temperature, hours since sleep, a timestamp, a model version
string -- are readable; the rest are declarations, and the
pedigree marks which is which.

## Shadow protocol

```
purpose   measure how much of a conclusion is a property of the observer
          rather than of the system
design    2^3 factorial over the three dials at low/high
sealing   each shadow commits its reading before any other shadow's is
          revealed
null      the disagreement between two runs of the SAME observer at the SAME
          dial, measured before any cross-observer spread is interpreted
blind to  consensus is blind to error the shadows share. Shadows reading one
          declaration through one prompt share most of their error.
```

> NOT one-factor-at-a-time. shadow_design.py section 1: OFAT cannot
  estimate an interaction at any number of runs, and the
  cross-gradient the playground exists to measure IS an interaction.
  Eight runs recover every main effect and every interaction
  exactly.

> shadow_design.py section 2: unsealed shadows anchor on each other
  and their agreement measures nothing. ../divergence-playground/
  implements the seal, the three spread axes, and the null ensemble.

### Panel independence

```
rule    require a minimum N_eff over the shadow panel, not a minimum
        shadow COUNT
N_eff   participation ratio of the shadow correlation spectrum, (sum L)^2
        / sum L^2
```

> **why** — shadow_panel.py: a panel of four shadows can carry N_eff = 1.2.
  Counting shadows measures effort; the participation ratio measures
  how much of it was independent. ../model-ecology/phylogeny.py
  already computes this statistic for a family of estimators.

> **v1 gap** — v1 requires human_baseline + ai_low + ai_high. On one model,
  ai_low and ai_high share a family bias and are close to one shadow
  at two dial settings -- so the human is the only decorrelated
  element, and dropping it takes N_eff from 1.61 to 1.14 and the
  false-pass rate from 38% to 84%.

> **without a human** — supported, but the substitution is THREE MODEL FAMILIES, not three
  budgets on one model. Four families with no human reach N_eff 2.18
  and false-pass 12.4%, stronger than v1's required panel with one.
  Adding a human on top of that changes N_eff by -0.02.

> **what a human still uniquely supplies** — embodied context. Cold-stiffened proprioception is not a failure
  mode any model has, which argues for a human shadow on physical
  measurements specifically -- a different argument from the
  decorrelation one.

### Consensus denominator

```
v1 says   'Variance must be compared against instrument resolution, not
          against zero.'
verdict   an improvement over comparing to zero, and still the wrong
          denominator
use       the same-observer repeat variance -- the spread of one observer
          measuring twice at one dial
```

> instrument resolution bounds what the INSTRUMENT can say. Shadow
  spread is bounded by what an OBSERVER can repeat. If observer
  repeat variance exceeds instrument resolution, every panel reads
  'exceeds_resolution' and the verdict is about the observer's
  repeatability, not about underdetermination.

## Skip conditions

```
rule   a skip condition must be able to fail
test   state the outcome that would prevent the skip, and check the
       instrument can resolve it
```

> shadow_design.py section 3: 'all four observers agree within
  instrument resolution' fires whatever the truth is, because
  observers reading one dial agree to within a division by
  construction. That is null-harness's CONSTANT_SILENT.

## Pedigree

Every number carries the chain that produced it.

```
required  value, units, physical_dial, instrument_dial, reasoning_dial,
          calibration_status, traceability, gate_verdict
layer     generator | physical | instrument | reasoning
```

> extends the three layers in ../reasoning-gate/guards.json with a
  fourth. A quantity whose value depends on who read it is
  reasoning-level, and a physical-scope claim resting on one is
  qualified, not supported -- the same rule gate.py already applies
  to generator-level support.

## Gate mapping

> v1 section 6 assigns G-DIM the job of 'checks that dial settings
  are actually different compute levels'. G-DIM in
  ../reasoning-gate/guards.json voids ratios across unlike objects
  and does not do this. The job named is real and unassigned:
  nothing verifies that ai_low and ai_high actually produced
  different reasoning effort, and a model that ignores its budget
  parameter would collapse two declared shadows into one silently.
