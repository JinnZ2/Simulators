# SAL-WO3 results: the first real-data scan

Run as pre-registered (`PREREGISTRATION.md`, commits `b2d19c6` and the
amendment `95619cb`, both before the run). Reproduce with
`python3 run_scan.py --check`, which rebuilds from git and compares to the
committed `stream.jsonl` and `series.json`.

## The series

The repository's own history at pin `5e75eb6`: 158 calendar days, 1,424
commits, 61 zero days (measured, since the clone was unshallowed). Mean
9.0 commits/day, sd 15.1, max 89.

## What the delivered lab recorded (unmodified)

| procedure | result |
|---|---|
| scan, threshold 10 | 42 candidate regions over 157 adjacent pairs |
| sweep 5 / 10 / 20 / 40 | 69 / 42 / 21 / 9 |
| permutation probe, 25 shuffles | 1,316 distinct pairs; 1,274 never adjacent in the real order |
| coupling, day index vs weekday | 42 coincident, 0 A-only, 0 B-only |
| null, independent normal days at the series' mean and sd | 100.55 expected |

All four records pass the lab's own `validate_record`.

## Against the predictions

- **P1 HELD.** The coupling scan returned 0 single-factor pairs. This was
  predicted from the code, not from the data: `coupling_scan` runs both
  factors in the same row order over the same outputs, so it can only
  separate them where a factor value is missing (SAL_012).
- **P2 HELD, and the prediction was weak.** Observed 42 against an expected
  100.55. P2 named no tolerance and no direction, so it could only have
  failed on an exact tie. This is recorded against the pre-registration,
  not excused.
- **P3 HELD.** 1,274 pairs appear only under shuffling.

## Not pre-registered (added after the run, labelled as such)

The normal null fits the series badly: the data are zero-heavy counts,
and the generator admits negative days. The permutation probe already
contains a better null, the same 158 days with their order destroyed:

```
shuffled order (25):  mean 59.2, range 53..65
real order:           42  (below all 25)
normal null:          100.6
```

Of the 58.6 gap to the normal null, the order-only part is −17.2: busy
days come in runs, so day-to-day jumps above 10 are rarer than the same
days in shuffled order would give. The rest is the generator's misfit.

## What this does and does not show

It shows the lab runs end to end on a real series and that its records
validate. It shows SAL-WO1's caution in practice: a declared generator can
be far from the data, and the null worth reading is the one that keeps the
data's own values.

It says nothing about anyone's productivity, about any session, or about
whether the repository is healthy. Interpretation stays unassigned.
