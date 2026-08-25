# Predictions, WO10 — registered before any suite was run

Committed before `resolve.py` existed. `extract.py` had been run, so the
claim population (50) and the section stances were known; **no claim had
been resolved against the tree**, and none of the five below is about a
quantity `extract.py` reports.

**Not blind, and more so than S7 says.** S7 records that this file has
been read. Stronger: parts of it were written by this session, and the
`sheet-structure-scan` / `claim-record` / `fold-matrix` / `notes` lines
were written within the last few days of repository time. Predictions
about those folders are worth less than predictions about the older ones,
and P1 is stated so that the split can be checked.

**Environment, declared before it can be blamed:** `pytest` was not
present and was installed (9.1.1) before this file was written, because
without it every pytest-suite COUNT would be NOT_TESTABLE and the run
would measure the container. Whether the numpy/scipy folders get their
dependencies is decided per item during the run and recorded per item.

---

**P1 — the two COUNT families separate, and `selftest N/N` holds more
often than a pytest-suite count.** A `selftest N/N` sentence and the
module that prints N are written in the same commit and the module is the
authority; a suite count is written once and the suite grows afterwards
without anyone revisiting the sentence. Predicted: the DIVERGED rate
among `selftest_ratio` + `selftest_checks` claims is **lower** than among
`tests_green` + `pass_skip` claims.

**P2 — at least one COUNT claim is DIVERGED.** A file this size with
numbers this specific, maintained by hand, over months.

**P3 — IDENTITY claims are mostly not DIVERGED.** They name a specific
artifact pair and a byte comparison; the pairs are stable. Predicted:
DIVERGED on **fewer than a third** of the resolvable IDENTITY claims.

**P4 — the rate is below 0.5**, and therefore well below the UNFCCC
workbook's 0.913. Different document class, so this is a second point and
not a direction.

**P5 — MAINTAINED is near zero, with one predicted exception.**
Almost nothing in `tests/` asserts a number that appears in `CLAUDE.md`.
The exception is the `GUARDS.md` regeneration claim, which
`tests/test_gate_drift.py` does assert. Predicted: MAINTAINED count is
**1 or 2**.

---

**Legal verdicts, per WO7's precedent:** NOT ADDRESSABLE is available to
any of these. P1 in particular is not addressable if either family comes
back entirely NOT_TESTABLE, and that outcome is recorded rather than
counted as support.
