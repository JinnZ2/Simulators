# WO8 (revised) S2 — prediction, registered before running the new format

S2 still says *"ASSERTED and ABSENT predicted majority — register before
running"*, and the `value_string` format has changed from one free-text
field to three independently ABSENT-able ones. So the basis prediction
carries over and the value_string prediction has to be restated.

**P1 (carried) — ASSERTED + ABSENT are a strict majority of upward
cells.** Held under v1 at 3 soft / 0 hard.

**P3 — the three value_string fields do not fail together.** Under the
v1 free-text format every upward cell read `empty`, and the prediction is
that the fixed format splits at least one of them: at least one cell
carries a stated `sign` with `magnitude` and `unit` both ABSENT.

**P4 — no upward cell carries a magnitude.** Stronger and separable: a
stated direction is cheap and a stated size is not.

## What is NOT blind here, stated plainly

`Disclaimer!A3` of the UNFCCC calculator was **already read in this
session**, during the v1 run of the same fixture. P3 and P4 are therefore
**not blind predictions about that text** — I have seen it. They are
registered because the format is new and the split has not been computed,
not because the source is unread.

The v1 registration (`PREDICTIONS_WO8.md`) had the same weakness in a
different place and said so: written before the fixtures existed, not
committed before the run. This one is weaker still on H1 and is recorded
as such rather than presented as a fresh test.

What would be blind: the same format run on a workbook nobody here has
opened.

## S1a, registered as an expectation rather than a prediction

S1a is new and has no fixture history, so nothing about it is registered
as a prediction. What is expected, stated so it can be checked against
what happens: the downward stop will sit **above** the deepest level in
the grid on H1, because the physical chain continues past what the
workbook computes — which is exactly the case the *"joules are not the
floor unless joules were calculated"* rule is written for.
