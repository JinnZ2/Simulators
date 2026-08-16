# Baseline recovery: the provenance fork

CC0-1.0. Two positions that look contradictory resolve into one
axis plus one prior question.

## The apparent contradiction

    DRIFT-LITERATURE REMEDY
      detect drift -> retrain on recent data
      presupposes a clean reference obtainable on demand

    IRRECOVERABILITY
      baseline is acquirable only during a stable interval.
      Once deviating, no clean reference exists to acquire.

## Fork 1 -- timing (secondary)

    axis = shift_interval / reference_acquisition_time

      > 1   retraining works. K15 is an ops step.
      < 1   no plateau long enough to sample. Staleness is
            permanent until another stable period.

## Fork 2 -- provenance (primary; decides whether fork 1 is
## even reached)

    reference INDEPENDENT of the system
      -> fork 1 holds. Timing decides.

    reference DOWNSTREAM of the system
      -> timing is irrelevant. Sampling longer returns more
         data from the same source.
      -> recoverable only by re-grounding on a reference the
         system did not generate and cannot edit.

## The loop being detected

    system drifts from substrate
      -> validation shifts to internal consistency
         (cheap, always available, always passes)
      -> outputs enter the corpus
      -> next fit trains on them
      -> coherence RISES while substrate coupling falls
      -> every internal instrument reads improving

## Test

Trace the retraining corpus for system-authored content. If the
fraction rises across retraining cycles, the loop is closed and
every downstream fit statistic is reading itself.

## Remedy, stated structurally

Re-anchor on a reference the system did not produce. Not a
held-out slice of the same corpus -- that drifted with
everything else.

Precondition: the trigger cannot live inside the drifted layer.
A monitor trained on the corpus reports coherence, correctly,
and is wrong. So the anchor interval runs periodically
regardless of whether anything looks wrong.

That is K14. The reference stays fresh because the practice runs
when nothing is at stake, which is the only time it is
acquirable.
