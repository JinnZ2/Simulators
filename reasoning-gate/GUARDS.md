# GUARDS

Generated from `guards.json`. Do not hand-edit.

License: CC0-1.0

Default is deny. A sim that does not declare gets no
output; an untagged quantity is not recorded; a ratio
across unlike objects is void; a claim without named
support does not enter the conclusion.

Origin: derived from a paired sim-stack audit: one sound sim (with controls and a stated prediction) run alongside two deliberately un-gated sims, so the divergence was observable

## Layers

```
generator   property of the code that produced the data (parameters, sampling rule, seed)
physical    property of the modelled system, defensible outside this script
instrument  property of the measuring apparatus (grid spacing, window, fit range, estimator)
```

No promotion between layers without an explicit,
justified step.

## PRE - before the sim executes

### G-RES - instrument resolution declared before run

```
rule    for every measurement, state the instrument scale and the
        feature scale it must resolve; instrument scale must be finer by
        the stated margin
denies  resolution not declared or instrument coarser than feature:
        output is not admissible
because an apparatus that cannot resolve the feature still emits numbers
        with plausible magnitudes
```

- k-grid spacing dk vs finite-sample peak width 2*pi/L
- finite-size level spacing vs the splitting being swept
- box-count smallest box vs mean nearest-neighbour distance

### G-CTRL - controls sized by fragility, not by expected surprise

Also fires at: post

```
rule    declare named controls with predicted values before running; a
        measurement expected to confirm requires controls first, not
        last
denies  no controls declared: a confirming result cannot be
        distinguished from an artifact
because control budget tends to track anticipated doubt rather than
        measurement fragility, so the most fragile step gets the least
        scaffolding
```

- feed a periodic lattice through the same S(k) code
- feed a 1D line through the same dimension estimator

### G-PRE - expected output written before execution

```
rule    state in advance what the output should look like if the setup
        is working
denies  no expected output recorded: divergence will not be visible
because an artifact is invisible against nothing and obvious against a
        written prediction
```

- expect a dense point spectrum with many sharp peaks across the k-plane
- expect S(k) tail to approach 1

### G-FIT - statistic addresses the stated question

```
rule    restate the question and name why the chosen statistic can
        discriminate it; a statistic blind to the property by
        construction must be flagged
denies  no discrimination argument: statistic may be blind to the
        property under test
because the tested version drifts from the live version without a
        re-derivation step
```

- box-counting dimension is blind to quasiperiodic order by construction: uniform coverage returns the embedding dimension regardless of arrangement

## MID - while quantities are emitted

### G-LAYER - every quantity tagged with its origin layer

```
rule    each recorded number declares layer and the object it is a
        property of; no promotion between layers without an explicit
        step
denies  untagged quantity: cannot be recorded
because generator-level and physical-level statements merge silently
        once they share a table
```

- a branching-walk dimension is a generator property, not a property of the material being modelled

## POST - at report assembly

### G-CTRL - controls sized by fragility, not by expected surprise

Also fires at: pre

```
rule    declare named controls with predicted values before running; a
        measurement expected to confirm requires controls first, not
        last
denies  no controls declared: a confirming result cannot be
        distinguished from an artifact
because control budget tends to track anticipated doubt rather than
        measurement fragility, so the most fragile step gets the least
        scaffolding
```

- feed a periodic lattice through the same S(k) code
- feed a 1D line through the same dimension estimator

### G-DIM - ratios name both operands' objects

```
rule    a ratio is admissible only if numerator and denominator are
        properties of the same object; otherwise it is void and carries
        no interpretation
denies  ratio operands are properties of different objects: void, no
        interpretation permitted
because a labelled dimensionless number of plausible magnitude is
        accepted as physical
```

- eigenvalue splitting over hopping integral, divided by an energy fraction in a branching rule, is void

### G-SUP - every claim names the statistic supporting it

```
rule    each claim lists recorded quantity names; a claim with no
        support is logged as unsupported and does not enter the
        conclusion
denies  claim has no named support
because demotion of a result to exploratory does not survive into a
        summary unless enforced
```

### G-IND - independence asserted, not assumed

```
rule    before calling results convergent, state what is shared between
        them: same data, same generator, same predicted outcome
denies  convergence asserted across measurements with shared inputs
because measurements on the same data whose outcome was predictable in
        advance are restatement, not corroboration
```

## Reading the log

```
gate_<SIM>.json
  declaration               what was promised before the run
  expected / observed       the divergence, logged either way
  generator_level_quantities  numbers that are properties of
                            the code, not of any system
  voided_ratios             computed, then refused
  claims[].status           supported | unsupported | qualified
  findings                  guards that fired in non-strict mode
```
