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

---

# OUTCOME, added after the run

Registered predictions are above this line and were committed at
`9af360c`, before `scan4.py run` was pointed at the file.

| | outcome |
|---|---|
| **P4** at least one testable relationship | **REFUTED.** 189 prose cells, 188 not arithmetic, **0 testable** |
| **P1** operand count separates the bins | **UNREACHABLE** — no bins to separate |
| **P2** a fill-value collision appears | **UNREACHABLE** — no relationship, no targets |
| **P3** MAINTAINED is empty | **UNREACHABLE** — vacuously 0, and 0 of 0 is not the claim |

P4 existed to make exactly this distinction, and it earned its place:
without it, "MAINTAINED = 0" would have been reported as P3 holding, on
a file where every bin is 0.

**S4's stated fallback is *no collision found → H1 unsupported here*, and
that is not the right report.** H1 is a hypothesis about workbooks that
state two relationships. This workbook states none, so it is outside the
population rather than a negative instance — recorded as `SSS_043`, with
the reason: its provenance prose is *instructions to a filer*, not
*claims about values the file ships*.

**S5 did not fire.** Four of five sheets are located by
`provenance_sheets()` and there are 333 text cells over 25 characters, so
there is provenance prose; it just does not state arithmetic. The stop
condition is for a workbook with no provenance sheet, and this is a
workbook with provenance sheets and no relationships — a state S5 does
not have a branch for, and the one this run landed in.

**No tuning was done** (S2). `PROVENANCE_WORDS` still lacks `meth`, so
`4. Calc. Meth. Disclosure` is located by its row-1 label rather than by
its sheet name; adding `meth` would have been tuning to this file and was
not done.
