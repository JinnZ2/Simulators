# WO8 S2 — prediction, registered before running

S2: *"ASSERTED and ABSENT are the expected majority. Register that as a
prediction before running."*

**P1 — ASSERTED and ABSENT together are a strict majority of upward
cells** across the fixtures, and `measured` + `derived` together are a
minority.

**P2 — `value_string` is empty on every upward cell.** Stronger than P1
and separable from it: a cell can be ASSERTED and still carry a stated
sign and magnitude, and the prediction is that none does.

## What the fixtures are drawn from, stated so the prediction is readable

The upward cells for H1 and H4 are taken from the UNFCCC calculator's own
`Disclaimer!A3` and `Info and sources`, not composed. Its stated purposes
are quoted in the term files: *"to support organizations to estimate
their GHG emissions"* and *"in order to raise awareness and to promote
climate action"*. Whether those come with a measured relation is a fact
about that text, readable by anyone.

H2 and H3 are scope-class fixtures and are expected to return
NOT_EVALUABLE before any upward cell is reached; per S3 that is a
refusal, not a low score, and their cells are not counted toward P1 or P2.

## Registered ahead of the run

Committed before `fold_matrix.py --run` was executed on any term file.
