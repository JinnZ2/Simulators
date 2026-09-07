# frame-instruments -- audit notes

Audit of the folder after its merge to `main`, run by the same system
that built it (FI_010). Method: probe each instrument on a constructed
input where the right answer is known in advance, and let the number
decide. Reading the code found none of the eight; running it found all
eight. Findings and numbers are in `CLAIM_TABLE.md`; `python3 audit.py`
recomputes them.

## What the eight have in common

Six of eight are one shape: a readout that cannot fail in one
direction on some class of input.

- FI_002 and FI_008 are `CONSTANT_SILENT` in B1's stability readout,
  one by an L-invariant statistic and one by tie-breaking on names.
- FI_007 is a check that passed with nothing to compare.
- FI_003 is a design that balanced the axis it named and left the
  adjacent one confounded.
- FI_004 is a lock enforced against the commit file rather than the
  release record.
- FI_001 is the repository's environment, not the instrument: four
  builds each named a module `report`, and the tests worked only
  because each ran alone.

The two recorded and not repaired (FI_005, FI_006) are properties of
definitions the reference spec owns: what counts as a rejoin, and that the
null is one permuted copy. Both print their numbers so the operator
decides with the magnitude in view.

## Repairs, each pinned

| finding | file | test |
|---|---|---|
| FI_001 | all four `test_bN.py` | `audit.py` runs b1 then b4 in one process |
| FI_002 | `b1/summarise.py`, `b1/nulls.py`, `b1/report.py` | `test_separation_set_stability_moves_with_L_and_ties_are_included` |
| FI_003 | `b2/order.py` | `test_order_latin_square_and_shortfall` (12 distinct successor pairs) |
| FI_004 | `b2/agree.py` | `test_ad_divergence_detected` (later commit refused) |
| FI_007 | `b2/agree.py` | same test (`evaluable` False, `failed` None) |
| FI_008 | `b1/summarise.py` | same B1 test (saturated stratum reports whole) |

`agree.py` now takes `--released` instead of `--commits`; the commit
file is still written by `lock.py commit` and is what `release` checks,
but scoring reads the release record, which is the one that records what
the reader had committed when the key was handed over.

## What the audit did not do

No real trace set, case set or reader was involved. The B3 comparison
(condition-B agreement between arms) has never been run. The
reference spec's RU-1 to RU-5 are untouched. No `no_severity` exemption
was declared; every screened word in the tool's own prose was reworded.
