# SIM-SPAN

STATUS: marker under exploration. Built to a delivered spec, run once,
logged 2026-08-24. Confidence in the mechanism: it can produce the shape.
Confidence that it did produce any published shape: none, and not asked.

CC0. stdlib only. No deps.

---

## QUESTION

    Can a span-reporting rule manufacture a U between reported sleep
    duration and an outcome, when no U exists in true sleep?

## MECHANISM UNDER TEST

    span = true_sleep + frag * wake_cost      (time in bed)
    reported = span, rounded to the half hour

A reporter who states time in bed is stating a quantity that mixes two
independent variables. Bin an outcome by that mixture and the populations
at each end of the axis are not what the axis label says they are.

## NULL, AS SPECIFIED

    True sleep has a flat OR monotone relation to the outcome. If a U
    appears on the reported axis, the reporting rule produced it.

## LEGS

    flat          outcome independent of true_sleep
    mono          outcome decreases with true_sleep
    frag_driven   outcome depends on frag only

## MEASUREMENT

Bin by reported, mean outcome per bin, fit a quadratic. Report the sign
of the quadratic term and the LOCATION of the minimum. Same on true_sleep
as the control axis. A U on reported with no U on true is the positive
result.

The vertex location is reported because a U at the wrong place on the
axis does not explain a U at the right place, and the spec's measurement
section asks for the location without routing the falsifier through it.

## SWEEP

    p             fraction of agents reporting span rather than true sleep
    mean frag     awakenings per night
    mean wake_cost  minutes awake per awakening

## FALSIFIER, AS SPECIFIED

    If no combination produces a U on the reported axis under the flat
    null, the reporting artifact cannot explain the published U on its
    own, and the finding survives this objection.

## OPEN

    - the spec's NULL is "flat or monotone"; its FALSIFIER is scoped to
      flat alone. Those are different sets and the legs disagree, so
      which one is run decides the answer. See RESULTS.md.
    - independence of frag and true_sleep is assumed and is probably
      false of real sleepers.
    - the rounding rule is invented, and its tie behaviour was not
      specified.
    - the outcome model is not a biological ageing clock.
    - this tests whether the mechanism CAN produce the shape. Not
      whether it did.
