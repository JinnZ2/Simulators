## Five-state grading

A status field for any claim, measurement, or requirement.

```
true
false
lapsed
partial
unknown
undifferentiated
```

`lapsed` — was true, conditions have since changed.
`partial` — true within a stated sub-range, not outside it.
`unknown` — no measurement taken.
`undifferentiated` — NO INSTRUMENT DISTINGUISHES THE CANDIDATE READINGS
YET. This is not "the same" and not "false".

### Why it matters

Standard practice collapses `unknown` and `undifferentiated` into
`false`. That is where directional information is discarded. A claim
marked `false` is closed; a claim marked `undifferentiated` names a
missing instrument, which is a place to build.

### Enforcement

Any implementation that accepts this field must reject a dataset using
only `true`/`false` across all rows, with status `void`. A two-state
return means the grading was not run.

### Intake use

Ask BEFORE measuring, not after an anomaly:

1. Is there an instrument that could render this true, false, lapsed,
   partial, unknown, or undifferentiated?
2. If yes, is it the proper instrument for this quantity?
3. If no instrument exists, record `undifferentiated` and name what the
   instrument would have to do.

The error this prevents: assuming that what cannot be measured does not
exist, or exists only in the currently measurable state.

### Related tell

A claim that cannot be falsified from inside its own framework is an
indication of a MISSING INSTRUMENT. Absence of a check where a check
should be is positive evidence, not neutral.
