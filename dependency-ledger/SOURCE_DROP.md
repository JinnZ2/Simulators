# Dependency Ledger Audit

A method for testing reconstruction claims by propagating them to conserved
quantities and checking closure against independent records.

CC0. No rights reserved.

## Problem

An artifact exists. Its method of production is not documented. Reconstructions
are proposed and evaluated on whether the method sounds achievable.

That is the wrong test. A method is not a claim about one step; it is a claim
about an entire support system, most of which the proposer never states. The
unstated part is where the reconstruction usually fails, and it fails
quantitatively, so it can be checked without new excavation.

## Core assertion

Energy and mass balance. Every proposed method implies a requirement set that
must be satisfied somewhere in the physical record. If the ledger does not
close, the method is wrong, and the size of the gap bounds how much capability
is unaccounted for.

## Procedure

```
1  STATE the artifact as measured quantities only.
   mass, dimensions, tolerances, material, count, finish.
   No interpretation at this step.

2  STATE the proposed method as a sequence of physical operations.

3  PROPAGATE each operation down to conserved quantities.
   Stop only at: energy, mass, momentum, time, material volume.
   Do not stop at an intermediate abstraction ("labor", "workers",
   "ramps"). Those are collapsed matrices and hide the gap.

4  EXPAND each conserved quantity into its own dependency set.
   energy      -> calories -> agricultural output -> arable area,
                  water, storage, seasonality
   tool wear   -> replacement rate -> raw material -> extraction site,
                  transport, smiths, fuel
   waste       -> spoil volume -> where is it now
   transport   -> vehicle/vessel capacity -> propulsion -> per-unit
                  efficiency at that loading

5  CHECK each terminal requirement against an INDEPENDENT record.
   Independent = not the same evidence that motivated the reconstruction.
   Settlement size, granary capacity, quarry volume, spoil heaps,
   deforestation signal, isotope and pollen records, tool finds.

6  REPORT the residual.
```

## Closure test

```
For each terminal requirement r:
    required(r)  from the propagation
    attested(r)  from the independent record
    residual(r) = required(r) / attested(r)

residual <= 1        requirement satisfied
residual >  1        gap; method under-specifies capability
residual >> 1        method falsified as stated
attested undefined   record gap, NOT a pass — flag, do not treat as zero
```

Do not aggregate residuals into one score. The per-requirement residual is the
whole point: it localises the missing capability to a named subsystem.

## Output format

The product is not a verdict. It is a specification for the missing component.

```
MISSING COMPONENT SPEC
  subsystem:      <named unit the reconstruction silently assumed>
  required perf:  <minimum value that closes the ledger>
  constraints:    <period materials, dimensions, environment>
  reachable?:     <is that value physically attainable with attested
                   materials — open question, separate investigation>
```

This converts "knowledge was lost" into a target someone can search for or
rule out.

## Worked example: watercraft propulsion

```
artifact      heavy cargo attested on the far side of a river system
method        rowed/poled vessels of a known attested type
propagate     tonnage x current velocity x distance -> work required
              -> power per rower at attested crew count
check         is that power attainable by a human at sustained output
              over the required duration
residual      if required power per rower exceeds sustained human output,
              the assumed propulsion efficiency is wrong
spec          oar/hull/loading system delivering >= X efficiency at
              displacement D, from attested materials
```

The loss is not "how did they cross the river." It is a specific unit —
oar geometry, hull form, load distribution — whose performance the
reconstruction assumed without stating.

## Worked example: precision gearing

```
artifact      geared mechanism, measured tooth count, pitch, tolerance
method        hand-cut bronze teeth
propagate     tolerance -> required layout and indexing accuracy
              -> a dividing method -> a tool -> a tool-making tradition
              -> practitioners -> training chain -> other output from
                 that chain
check         does any other attested object show the same tolerance
              class; is the dividing tool attested anywhere
residual      an isolated tolerance class with no attested tool and no
              sibling artifacts is a large residual
spec          indexing/dividing technique achieving tolerance T in
              bronze, plus a transmission chain that left one object
```

An isolated artifact with no siblings is itself the measurement: a whole
practice existed and left one trace.

## Failure modes of this method

Guard these explicitly or the audit closes falsely.

```
TIME AS SOLVENT
  "They had centuries." Unbounded duration absorbs any energy gap.
  Duration must be bounded independently (occupation layers, dated
  construction phases, tool-form seriation) before it may be used
  to close a ledger.

SMUGGLED CONSTANTS
  Modern efficiencies substituted for period ones. Every coefficient
  must be sourced to an attested artifact or an experimental
  replication, and marked when it is neither.

LABOR ELASTICITY
  "More workers." Workforce is not free; it propagates to calories,
  water, housing, waste, and command overhead. If a reconstruction
  scales labor, the audit rescales every dependent requirement.

RECORD GAP AS PASS
  Absent evidence recorded as satisfied. It is neither pass nor fail;
  it is an unmeasured cell and must stay visibly unmeasured.

COLLAPSED PROXIES
  Stopping propagation at "labor", "resources", "organisation".
  Each is a matrix entered as a scalar. Expand or the gap hides inside.
```

## Scope

Not limited to antiquity. The same audit applies to any claim that a
capability is reproducible from a record: industrial process restarts,
decommissioned production lines, discontinued materials, procedures
documented but not exercised. The artifact-with-no-procedure case and the
documented-but-unreproducible case are the same measurement.

## Ask

Apply it to one case and publish the residual table, including the
unmeasured cells. The unmeasured cells are the finding.
