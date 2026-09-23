# CLAIM TABLE -- automation-gap

Ids are permanent. `AGA_` = automation-gap. Status is SUPPORTED / REFUTED /
UNVERIFIED. Every SUPPORTED claim is a property of the five delivered
documents and is recomputable by anyone with the folder:
`python3 audit.py`. The delivered falsifiers are the documents' own
(`AUT-F1..F8`) and carry their own prefix; nothing here renumbers them.

**Scope, before anything else.** Every figure in the drop is CARRIED --
sourced to reporting this environment cannot reach, the egress gate refusing
every publisher host. Nothing below is evidence about mining haulage,
humanoid robots, container terminals, agriculture, or any vendor. What is
checked is whether the documents agree with themselves and with each other.

---

**AGA_001 -- the distribution table reconciles with the matrix exactly.
SUPPORTED.** All six columns, recomputed from the 16 matrix rows, match the
printed distribution cell for cell, and every column totals 16. Checked by
row order rather than by label, because the distribution's row labels are
prose and the matrix's are column keys. *Falsifier:* any column whose
recomputed PASS/PARTIAL/FAIL/ABSENT counts differ from the printed table.

**AGA_002 -- exactly one record passes all six checks, and it is the one F1
names. SUPPORTED.** Komatsu FrontRunner AHS. The next-highest is the
ag-harvest review at 4 of 6. *Falsifier:* a second all-PASS row.

**AGA_003 -- F1's second sentence is REFUTED by the matrix it sits under.**
F1 states *"Every humanoid record fails at least three."* Counting any
non-PASS cell as a failure -- the reading most favourable to the claim,
since PARTIAL and ABSENT both count against -- two records fail exactly two:

    Figure 02 @ BMW, 11 months     teleop PASS  metrics PASS  envelope PASS
                                   sustained PASS; variation + independent ABSENT
    Digit @ GXO Spanx              identical shape

The first sentence of F1 stands (AGA_002); the second does not. The repair
is a number, not a rewrite: *at least two*, or *at least three except the two
metric-carrying deployments*. **Which rows count as humanoid is a declared
list in `audit.py`, not a delivered field** -- no document carries a form
factor -- so a reader who excludes Digit still has Figure 02 left.
*Falsifier:* a delivered form-factor field that excludes both rows.

**AGA_004 -- F2's two counts hold; one of its sentences over-reads them.
SUPPORTED with a narrowing.** For the four metric-carrying deployment-class
records, independent-evaluation PASS is 0 of 4 and variation PASS is 0 of 4,
both as printed. But the corpus declares its own record discipline in as many
words -- *"ABSENT means the record does not carry the information... an
audience cannot verify what was never disclosed"* -- and F2 then reads
`variation: 0 of 4` as *"every deployment is one task type."* Zero records
showing variation is not the same finding as every deployment being
single-task. **F3 makes the stronger claim correctly**, by naming the actual
tasks (tote transfer, sheet-metal insertion) rather than inferring from
absence. *Falsifier:* a delivered field distinguishing *varied and failed*
from *not reported*.

**AGA_005 -- the Komatsu ledger is internally consistent at the precision it
prints. SUPPORTED, 6 of 6 derived cells.** Hours gain, throughput factor,
both human-hours-per-unit figures, the 81% drop and the tire consumption
factor all recompute from the cells they derive from. The tolerance is the
**shipped precision of each figure as written**, not a constant: `+12%` is a
whole percent and reports 12 +/- 0.5, so a recomputation of 11.77 agrees;
stated to two places it would not, and the suite asserts that. `_halfwidth`
is **imported** from `move-set/move_set_sim_v2.py`, where it is already
registered in `tools/known_answer.py`. *Falsifier:* any derived cell missing
its own inputs' interval.

**AGA_006 -- the tire figure is the top of its own cited range. SUPPORTED.**
The ledger states +40% tire life (factor 0.71) and cites *"replacement at
6,000-7,000 h vs 5,000 h."* That range is +20% to +40%; its midpoint is +30%,
which gives a factor of **0.77, not 0.71**. The ledger takes the favourable
end of a range it supplies. This is separate from, and smaller than, the
drop's own U3 finding that the tire gain is confounded by the surface upgrade
AHS triggered -- U3 questions the attribution, this questions the point
estimate inside it. *Falsifier:* a source fixing replacement at 7,000 h.

**AGA_007 -- the field ledger's denominator is its own. SUPPORTED.**
*"parked-strike discovery is now 2 of 6 entries"*: six headed entry records
(003 + 004 filed as one incident), matching the stated denominator.
*Falsifier:* a seventh headed record without the fraction moving.

**AGA_008 -- all five documents self-date one day ahead. SUPPORTED, recorded
not adjudicated.** Every document dates itself 2026-09-24; the session
landing them runs 2026-09-23. Same class as the forward-dated item in
`deep-research-correction` C-1, and equally not a finding about the content.
Timezone is the ordinary explanation and is not established here.
*Falsifier:* a timezone declaration in the drop.

**AGA_009 -- four named objects are referenced and not delivered.
SUPPORTED.** `WP1`, `WP2`, the *trades-shortage ledger* and the *claim
ledger* are each cited as though filed and appear in no delivered document.
WP1 and WP2 are load-bearing in `FIELD_LEDGER_001` -- entries 001 and 005
read their value against them. The six Simulators folders the drop names
(`effective-redundancy-audit`, `declared-frame`, `closure-cost`,
`instrument-bias-sims`, `labor-instrument`, `readout-count`) all resolve.
*Falsifier:* the four arriving.

**AGA_010 -- two defects in this audit, found by running it, both
under-reporting the drop. SUPPORTED.** A separator quantifier `.{1,3}` was
greedy and ate a digit group out of `6,000-7,000`, parsing the upper bound as
`000` and returning a tire range of `[20.0, -100.0]`; and a stipulated
tolerance of 0.006 flagged the `+12%` row as a disagreement when the document
had printed a whole percent. Both ran toward reporting the drop as less
consistent than it is. Each is pinned by a regression check. *Falsifier:*
neither reproduces on the recorded revision.

**AGA_011 -- UNVERIFIED, and it covers the folder.** No figure in any of the
five documents was checked against a source. The corpus audit's own sampling
declaration already says the corpus is curated and event-sampled, so its
rates are properties of those 16 records; this audit adds only that the
arithmetic over those records is right. Whether the records describe the
world is untouched in both directions.

**AGA_012 -- the field layer's own return loop is the part with no
instrument here. UNVERIFIED.** `FIELD_LAYER_ZERO_BURDEN_SPEC` states a
design rule (*the worker never fills out a form*) and a payment order (*the
system pays the worker first*). `FIELD_LEDGER_001` shows the loop running
once, including a discrepancy held UNRESOLVED and then settled by a pixel
check, and a mechanism correction that superseded the organizer's reading.
Whether the loop survives absent a motivated operator is the claim, and one
ledger is n=1. *Falsifier:* a second operator's ledger, or this one going
quiet.
