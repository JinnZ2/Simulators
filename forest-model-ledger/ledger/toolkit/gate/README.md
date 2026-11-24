# ledger/toolkit/gate: gate runs for the finder and the sorter

CC0. Work order TK-G1, 2026-11-23, co-authored (Kavik + Claude).

Status: gate run; threshold rules declared (DECLARED.json) for the gated
design only. Nothing here is validated.

## What is here

    gate_missing_column_finder.py   gate for missing_column_finder
    gate_denominator_sorter.py      gate for denominator_sorter

Both scripts use the standard library only, a fixed seed (20261123,
printed in every run) and synthetic rows only. No real row is read.
Neither prints PASS or FAIL: the order sets no threshold, and the owner
sets them after reading the tables.

    python3 ledger/toolkit/gate/gate_missing_column_finder.py   # about 50 s
    python3 ledger/toolkit/gate/gate_denominator_sorter.py      # about 3 min

Pinned output: `samples/gate_missing_column_finder.sample.txt`,
`samples/gate_denominator_sorter.sample.txt`.

## What each gate reads [DERIVED]

Finder. The gate calls `missing_column_finder_stdlib.analyse()`, the
standard-library port, not the numpy original. The port was compared with
the original on `holdout/anchor_studies.csv`
(`samples/missing_column_finder_stdlib_compare.sample.txt`). The gate's
"recovered share" is the finder's within-study share for a planted
grouping that is not among the recorded columns.

Sorter. The gate imports `denominator_sorter` itself. `sort_studies()`
groups studies by seven recorded columns and never reads rr, so a gap
between two measurands is split only when a recorded field differs. The
gate runs both forms (RECORDED, UNRECORDED) and reports the tool's
field-drop outcome test beside the split.

## Threshold rules and the null FLAG rate (2026-11-24)

`DECLARED.json` was committed before the null FLAG-rate run. Finder: flag
when the share is above the maximum of the 200-shuffle null at the gated
design. Sorter: a split is bookkeeping, never a finding; a finding needs
the outcome test to fire. A combined claim needs both.

    python3 ledger/toolkit/gate/null_flag_rate_finder.py   # about 3 min, 4 workers

Pinned output: `samples/null_flag_rate_finder.sample.txt`,
`samples/finder_bias.sample.txt`.

## Power floor (2026-11-24)

Declared in `DECLARED.json` (second amendment) before the sweep. Planted
shares 0.02, 0.03, 0.05, 0.07, 20 replicates each, against the declared
null max 0.0326. Floor: planted s = 0.07 (20 of 20 above).

    python3 ledger/toolkit/gate/power_floor_finder.py   # about 80 s

Pinned output: `samples/power_floor_finder.sample.txt`.

## Not established [DERIVED]

- The declared rules hold for the gated design only.
- One synthetic design per tool. Other study counts, row counts, level
  counts and noise shapes: NOT RECORDED.
- The port leaves out the original's `synthetic()` and `gate()`.

Observer slots: null.

## Provenance

Written in the session that ran work order TK-G1 (2026-11-23). Every
number in the sample files is printed by the scripts; none is typed. The
descriptions above are DERIVED from reading the two tools' code on the
PR #334 head (commit c0a7d77c04eff06a00658a79eec4e8e19febddf5).
