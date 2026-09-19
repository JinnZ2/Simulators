# CLAIM_TABLE -- criterion-externality

Claims are about the INSTRUMENT and about the delivered order. The fault
model is CONSTRUCTED; the target paper's body is not read; no audit
regime is graded. `CEX_*` ids are permanent. A refuted claim is updated;
the checks are not retuned to preserve it.

---

| id | claim | status |
|---|---|---|
| CEX_001 | the order's separating test holds as arithmetic: axes 1-3 at the top rung and axis 4 at C0 aggregate to 1.00 over three and 0.00 over four | SUPPORTED, arithmetic |
| CEX_002 | under weakest-link aggregation an added axis never raises the aggregate and lowers it on a non-empty set of cells (all 256 grade cells); the order's "it lowers the reported number" needs no model | SUPPORTED, arithmetic |
| CEX_003 | R4 on the constructed form: the beta-factor common cause is a shared draw between parties and carries no term for what the criterion covers, so an excluded class is surfaced at 0.0 at every beta and every party count -- INDEPENDENT on this model; whether the paper's own model has such a term is decided by reading it | DERIVED on the construction; paper NOT READ |
| CEX_004 | the Monte Carlo converges on the closed form q(beta p + (1-beta)(1-(1-p)^n)) within 0.01; the closed form is registered in tools/known_answer.py | SUPPORTED, instrument |
| CEX_005 | the C-grades order AUTHORSHIP and are not monotone in surfaced rate: C2 covers more than C1 and, applied at discretion below a computed crossover (0.959 here, against a stipulated 0.7), surfaces fewer faults than C1 | FINDING on the order's grading |
| CEX_006 | R1 is NOT_RUN: arxiv.org refuses CONNECT (403, 2026-09-19T01:51Z, github.com the control), so the order's own void condition -- the axis present under another name -- cannot be evaluated here and the absence claim stays at abstract level | NOT_RUN, recorded |
| CEX_007 | R3 returns NOT_EVALUABLE: the five regimes are carried UNCODED, a grade with no basis is refused, and both branches of the prediction are reachable on constructed codings | SUPPORTED, machinery; no regime coded |
| CEX_008 | two of the three arrivals resolve in this tree by path and marker and the third (the audit-protocol work order's C4) is not in this tree; all three are one operator's work, so "not built together" is what is established and "independent" is not | FINDING, cross-links |
| CEX_009 | the order's R2 question "whether any fault class moves out of the never-surfaced half" has one answer under a coverage gate before any draw: none; a gate moves classes in only | FINDING, arithmetic |
| CEX_010 | nothing here is evidence about the paper's 5.9%, about any audit regime, or about whether the axis is absent from the paper; every figure in the order is carried and egress-blocked | UNVERIFIED |

---

## CEX_003 -- what R4 does and does not establish

The order calls R4 the cheapest decisive test and says to run it first.
What can run here is the test's FORM: build the beta-factor common cause
as it is usually stated (with probability beta the parties share one
draw), put the criterion in front of every party as a coverage gate, and
ask whether any setting of beta or party count surfaces a class the gate
excludes. None does, and that is a property of the form, since the gate
sits before the draw. The decisive part -- whether the paper's own model
has a coverage term under another name -- is R1, and R1 is NOT_RUN.

## CEX_005 -- the grading and the quantity

C0..C3 grades who authored the ruler. R2 reports surfaced-fault rate. On
this model C2 (third party, discretionary) surfaces fewer faults than C1
(the auditor's own criterion) whenever the discretion probability falls
below `grade_mean(C1) / grade_mean(C2 at q=1)`, computed at 0.959. The
stipulated 0.7 puts C2 below C1. So a regime moving from C1 to C2 raises
its axis-4 rung and can lower the quantity the rung is meant to track. A
grading that is an ordinal on one quantity and is read against another is
`measurand-fork`'s VOID RATIO inside a scale.

## CEX_008 -- convergence and authorship

The order's evidence for the axis is three routes converging. Two are
locatable here: the physics baseline in `PREAMBLE.md` and condition B of
the audit-isolation design in `frame-instruments/`. The third names a
work order not in this tree. All three are written by the same operator
in the same programme; `triad-playground` `TP_003` is the reason that
matters -- shadows reading one declaration share the declaration's
error. Convergence is recorded; independence is not claimed.
