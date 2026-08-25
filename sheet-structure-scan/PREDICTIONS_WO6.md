# WO6 S4 — H1, registered before the run

Written and committed before `scan4.py run` was pointed at the legacy
file. `git log` for this file is the timestamp; a prediction added after
a result is not a prediction.

## H1, from `SSS_034` at n=1

> Where a provenance note states two relationships, the lower-operand-
> count one survives and its value propagates into the higher one's
> targets.

On the UNFCCC calculator: one 5-operand relationship holds, one
33-operand relationship diverges across all 21 of its targets, and 20 of
those 21 carry the 5-operand relationship's own target value to
seventeen digits.

## What was already known before the run

Stated so the predictions are readable against what they could have used.
All of this comes from the reader, not from scan 4:

- 5 sheets, 1580 cells, 336 DERIVED, 1244 CONSTANT_TEXT, **0 constant
  numbers** — the same unfilled-template shape as `SSS_026`.
- 4 sheets are located by `provenance_sheets()`, so `S5`'s stop
  condition does not fire and the run proceeds.
- 333 text cells longer than 25 characters, i.e. a real prose population.

Nothing above says which prose cells state an arithmetic relationship,
how many operands any of them names, or what any target holds.

## Predictions

**P1 — operand count separates the bins.** Relationships with fewer
operands land in `MAINTAINED` or `HOLDS_UNMAINTAINED`; relationships with
more land in `DIVERGED`. Registered as: **the mean operand count of the
DIVERGED bin exceeds that of the HOLDS + MAINTAINED bins.**

**P2 — a fill-value collision appears.** At least one DIVERGED target
holds a value that is the target of a *different* stated relationship in
the same workbook, to full float precision. This is the specific
mechanism `SSS_034` found and is the half of H1 that is not just
"bigger relationships break more".

**P3 — `MAINTAINED` is empty.** No stated relationship is enforced by a
formula. The UNFCCC file returned 0, and the reason there was structural
(every relationship is stated about a constant), not particular to it.

**P4 — the bins are not all empty.** At least one prose cell yields a
testable relationship. If scan 4 returns nothing testable at all, P1–P3
are unreachable rather than refuted, and that is the result.

## What refutes H1 here

Per S4: **no collision found means H1 is unsupported on this file, and
that is stated plainly.** P1 holding without P2 is the weaker reading —
larger relationships diverging more often is a size effect and needs no
propagation mechanism.

n will be 2. Two points give a direction, not a rate, and a direction
only if the sign is the same.
