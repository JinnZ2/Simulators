# SAL-WO3 pre-registration (written and committed before any scan is run)

## The series

- **Source:** this repository's own git history, which is a real record
  anyone with the clone can regenerate. It is not a constructed fixture.
- **Pin:** all commits reachable from `5e75eb63a8da29c6bf3fc1a2db8d6eddaf8bc102`,
  the HEAD before this work order started. The clone was unshallowed first;
  the root commit is `d90f021`.
- **Case:** one calendar day, from the first commit day to the last,
  inclusive.
- **Output:** the number of commits whose committer date (`%cs`) falls on
  that day. A day with no commit is a measured 0, because the history is
  complete.
- **Factor A:** day index (0, 1, 2, …), in date order.
- **Factor B (coupling scan only):** ISO weekday (1–7) of the same day.
- **Inside the measurement:** the series includes commits made by sessions
  like this one. It records the repository's activity, not anyone's
  productivity, and no reading of it is made here.

## Procedures (the delivered lab 0.3, unmodified)

1. `scan_transitions`, absolute threshold 10.
2. `threshold_sweep`, thresholds in this order: 5, 10, 20, 40.
3. `order_permutation_probe`, 25 permutations, seed 3, threshold 10.
4. `coupling_scan`, factor A = day index, factor B = weekday, threshold 10.
5. Null expectation (SAL-WO1) beside the scan, under a declared generator:
   independent normal days with the series' own mean and sd. This
   generator is a stated choice; real days are neither independent nor
   normal.

## Predictions

- **P1 (from reading the code, SAL_012):** the coupling scan's coincidence
  record will hold zero factor-A-only and zero factor-B-only pairs. No
  factor value is missing, and both scans use the same order and outputs.
- **P2:** the observed region count at threshold 10 will differ from the
  null expectation, because real commit days cluster. Direction not
  predicted.
- **P3:** the permutation probe will flag pairs that never occur in the
  given order, as the report saw on its synthetic demo.

No verdict follows from any of these. The records are appended with
`interpretation: unassigned`, as the lab requires.

## Amendment 1 (committed before any scan ran)

The pin's full hash above is wrong: it was typed, not copied. The
7-character prefix `5e75eb6` is right. The real commit is
`5e75eb6e74a74046049af9bc01fc94d42f0bcd9b`. Nothing else changes, and the
original line is left as written so the error stays on the record. The run
script resolves the pin by `git rev-parse 5e75eb6` and checks it against
this full hash.
