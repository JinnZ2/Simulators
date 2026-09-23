# CLAIM TABLE -- automation-gap

Ids are permanent. `AGA_` = automation-gap. Status is SUPPORTED / REFUTED /
UNVERIFIED. Every SUPPORTED claim is a property of the six delivered
documents and is recomputable by anyone with the folder:
`python3 audit.py`. The delivered falsifiers are the documents' own
(`AUT-F1..F8`, `RD-F1..F3`) and carry their own prefixes; nothing here
renumbers them.

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

**AGA_008 -- all six documents self-date one day ahead. SUPPORTED, recorded
not adjudicated.** Every document dates itself 2026-09-24; the session
landing them runs 2026-09-23. Same class as the forward-dated item in
`deep-research-correction` C-1, and equally not a finding about the content.
Timezone is the ordinary explanation and is not established here.
*Falsifier:* a timezone declaration in the drop.

**AGA_009 -- four named objects were referenced and not delivered. HALF
CLOSED: two arrived, two did not.** `WP1`, `WP2`, the *trades-shortage
ledger* and the *claim ledger* were each cited as though filed. **WP1 and
WP2 arrived** one drop later as the two sections of
`FIELD_LAYER_SEED_ROADS`, which is what `FIELD_LEDGER_001` entries 001 and
005 read their value against. The two ledgers are **still absent and still
cited** -- *trades-shortage ledger* in the Komatsu scaffold, *claim ledger*
in the zero-burden spec -- so the claim stands on half its subject. The six
Simulators folders the drop names (`effective-redundancy-audit`,
`declared-frame`, `closure-cost`, `instrument-bias-sims`,
`labor-instrument`, `readout-count`) all resolve. **The check distinguishes
FILED from CITED**, because its first version tested for the name and
reported both ledgers delivered on the strength of the sentences that cite
them -- a citation read as a filing, in the check written to separate the
two (`AGA_019`). *Falsifier:* the remaining two arriving.

**AGA_010 -- two defects in this audit, found by running it, both
under-reporting the drop. SUPPORTED.** A separator quantifier `.{1,3}` was
greedy and ate a digit group out of `6,000-7,000`, parsing the upper bound as
`000` and returning a tire range of `[20.0, -100.0]`; and a stipulated
tolerance of 0.006 flagged the `+12%` row as a disagreement when the document
had printed a whole percent. Both ran toward reporting the drop as less
consistent than it is. Each is pinned by a regression check. *Falsifier:*
neither reproduces on the recorded revision.

**AGA_011 -- UNVERIFIED, and it covers the folder.** No figure in any of the
six documents was checked against a source. The corpus audit's own sampling
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

---

**AGA_013 -- the seed's tire-cost ratio recomputes from the cells printed
beside it. SUPPORTED.** `FIELD_LAYER_SEED_ROADS` WP1 states *"concrete
0.29c / asphalt 0.43c / gravel 1.07c -- gravel ~= 2.5-3.7x paved."* Gravel
over asphalt is 2.4884 and gravel over concrete is 3.6897; both agree at the
**shipped precision of the stated bound** (one decimal, so +/- 0.05), which
is the tolerance rule the rest of this folder already runs on. The two
surfaces the cell calls paved are the two the range spans, in that order.
*Falsifier:* a fourth surface in the cell, or the stated range given to two
places.

**AGA_014 -- two rows of one table are 35x apart on a comparison they both
make. SUPPORTED, adjudicating neither.** The maintenance row states gravel
at *"~4x paved"*; the Minnesota row two lines below states *"gravel
$1,887/mi/yr vs paved $13.45/mi/yr"*, a ratio of **140.3x**. The two are
**different quantities** -- frequency against expenditure -- so this is a
tension and not a contradiction, and neither figure is scored here. What
would settle it is the county's own units on the $13.45 cell; a per-mile
annual paved-maintenance figure below fifteen dollars is the part a reader
should check first. The audit function carries no verdict token and a check
asserts it. *Falsifier:* the county record stating its units.

**AGA_015 -- the seed uses a provenance label its own header does not
declare, on the rows the section's argument rests on. SUPPORTED.** Line 3
declares `MEASURED / VENDOR / FORECAST / CONSTRUCTED`. The tables use
`INDUSTRY-STATED` on **7 rows** -- every WP2 requirement row -- and WP2's
framing turns on exactly that distinction: *"these are the autonomy
industry's **own stated requirements**, not skeptics' estimates."* Under the
declared vocabulary the nearest member is `VENDOR`, which is the label the
section is written to avoid. Either the header gains a fifth member or the
rows take an existing one; the audit picks neither. *Falsifier:* a fifth
declared label.

**AGA_016 -- one of the seed's two citations into its siblings resolves and
one does not. SUPPORTED.** *"(from the Komatsu scaffold, V2.1)"* resolves:
the corrugation figure sits inside that document's V2.1 section and the two
figures match. *"MEASURED (from demo-corpus audit)"* on the Aurora
emergency-procedures row does not: the observer, roadside-assist and
weather-pull-over facts are in `AUTOMATION_GAP_AUDIT` section 1, and
`DEMO_CORPUS_AUDIT` carries Aurora as a single matrix row with none of them
(term counts 0 against 4, printed so the call is checkable). The facts are
real and in the folder; the pointer names the wrong sibling. The term list
is stated as one -- a paraphrase steps around it. *Falsifier:* the cited
document carrying the supporting text.

**AGA_017 -- every figure THE COLLISION restates traces to the WP1 row it
restates. SUPPORTED, 3 of 3.** Tire cost `2.5-3.7x` and maintenance
frequency `4x` are identical to their rows; roughness `~1,000 mm/km per
metre` falls inside the row's `+970-1,100`. This is the containment check,
not a new measurement: the argument section introduces no figure its own
tables do not carry. *Falsifier:* a fourth figure in the section with no
row behind it.

**AGA_018 -- the Caltrans survey's two numbers have exactly one integral
reading, and it is the favourable one. SUPPORTED.** The seed states *"18
companies, 90% response"* and *"top ask, 12/18 companies."* If 18 were
surveyed, respondents are 16.2 -- not an integer, so that reading is
impossible; if 18 responded, the population was 20 exactly. The 12/18 share
therefore reads over respondents, which is what the section needs. Recorded
because the phrasing is ambiguous and the arithmetic settles it in the
document's favour. *Falsifier:* the survey stating a population.

**AGA_019 -- three defects in this session's own checks, each found by
running and each running toward the reassuring answer. SUPPORTED.**
(1) `4x maintenance / frequency` **wraps across a line** in the delivered
text; a single-space pattern matched nothing and the containment check
reported two restated figures where the document restates three -- an
under-count of the document's own consistency. (2) The falsifier-id scan
counted every occurrence, so `AUT-F1` -- defined in the gap audit and
**cited** in the corpus audit's cross-links -- reported as a collision; a
citation read as a second definition. (3) `named_and_absent` tested for the
object's name, so both ledgers reported **delivered** on the strength of the
sentences that cite them; a citation read as a filing, in the check whose
whole job is that distinction. Defects 2 and 3 are the same error at two
sites, and both are the shape this folder's siblings record repeatedly: a
mention is not the thing. Each is pinned by the case that exposed it.
*Falsifier:* any of the three failing to reproduce on the recorded revision.
