# OPEN QUESTION E9 -- WALKING criterion is false-alarm-prone at small n

Status: OPEN / EMPIRICAL. Do NOT patch with a guessed threshold.
Logged: divergence_log.ndjson, entry 03efe4e41e61, 2026-07-24
Register: EXPERIMENT_register.md E9

## What happened

divlog.residual() classifies a disagreement history's SHAPE. WALKING (real
drift) fires when the band-gap sequence between the two axes is monotonic.

During the divlog build, a series intended as INTERMITTENT (noisy, no trend)
was classified WALKING. Investigation: the series had gaps -1, 0, +2, which
IS monotonic, so the code was correct per its own rule. The test was mis-built.

But the mis-build exposed a real defect in the SPEC, not the code:

    at n=3, "monotonic" and "trending" are nearly the same thing BY CHANCE.
    a short random walk is monotonic often enough that WALKING will cry drift
    on noise. This is a criterion (bias) problem, not a sensitivity problem
    (modes.py / signal-detection vocabulary): the classifier errs toward false
    alarms.

## Why we are NOT fixing it now

The correct repair is a number -- a minimum run length, or a monotonicity that
must survive some noise band -- and that number is an EMPIRICAL question about
how real inter-module divergence behaves over time. Guessing it here would be
exactly the substitution the calibration-audit repo exists to prevent: an
inferred prior overriding measurement that does not exist yet.

## What Claude Code should do in the repo

    1. Land divlog.py v1 AS IS. It is correct per spec. Do not special-case.
    2. Copy this file into the repo as an open issue / docs entry.
    3. Copy divergence_log.ndjson entry 03efe4e41e61 as the first log record --
       it is the worked example of the log's own purpose.
    4. DONE ALREADY -- divlog.py v1 ships with a pointer comment at residual()'s
       WALKING branch. Do not add a second one.
    5. Leave residual() returning WALKING on monotonic sequences. When E9 is
       resolved, the fix is a NEW divlog entry that `supersedes` 03efe4e41e61,
       plus a versioned change to the rule -- never an untracked edit.

## How E9 gets resolved (the experiment, not the guess)

    SYNTHETIC arm: generate known INTERMITTENT (stationary + noise) and known
    WALKING (monotone trend + noise) series across n = 3..30. Sweep candidate
    rules (min run length; Mann-Kendall-style trend test; require gap change to
    exceed a noise estimate). Report BOTH false-alarm and miss rates at each n.
    A rule with zero false alarms and high misses is not a win -- it is the
    criterion pushed the other way (E9 acceptance requires both curves).

    FIELD arm: only real inter-module divergence histories fix the noise scale.
    Kavik's operational logs over months (register E16) supply it. Until then
    the synthetic arm bounds the rule; the field arm calibrates it.

## Invariant reminder for whoever closes this

    resolution is a new superseding entry + a versioned rule change.
    the log is append-only. the old behavior stays on the record.
