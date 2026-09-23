# CLAIM TABLE -- automation-gap

Ids are permanent. `AGA_` = automation-gap. Status is SUPPORTED / REFUTED /
UNVERIFIED. Every SUPPORTED claim is a property of the delivered material
and is recomputable by anyone with the folder: `python3 audit.py` for the
six documents (`AGA_001..019`), `python3 register_audit.py` for the
evidence register (`AGA_020..050`). The delivered falsifiers are the
documents' own (`AUT-F1..F8`, `RD-F1..F3`) and carry their own prefixes;
nothing here renumbers them.

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

---

## The evidence register

`driver_hours_evidence_register.py` landed one drop after the seed: a
register of what is known, self-reported and unmeasured about long driving
days, fatigue and driver tenure, across eleven sources and eight questions.
It is a Python object, so `register_audit.py` **imports** it rather than
parsing it -- the objects under test are the register's own -- and no
figure it states appears as a numeric literal in the audit (asserted).
Every source in it is CARRIED: located by a search pass this environment
cannot repeat, and several are marked UNREAD by the register itself.
Nothing below reads a primary source or rules on one.

**AGA_020 -- the register declares one status scale and runs it at four
sites through three mechanisms. SUPPORTED, amended by the revision.** The
docstring declares six rungs *"one scale for every source"* --
`OBSERVED / SECONDARY / DERIVED / PROPOSED / UNMEASURED / UNREAD`. The
sources use three in a `status` field; the question map uses five in a
tuple slot, of which **`PARTIAL`, `SUPPORTED` and `UNRESOLVED` are
declared nowhere** and between them carry five of the ten question
verdicts. Two further revisions added three more sites, all **inline
`[TAG]` markers inside free-text prose** -- a `holds` entry, a
`TERM_NOTES` field, and (in the addenda) an addendum question's status,
a control-loop failure mode, the transfer note and a function docstring:
**five sites, three mechanisms.** A `status` field is a slot a reader can enumerate; a
bracket in a sentence is not, and the declared scale gives no indication
the second kind exists. **`DERIVED` and `PROPOSED` close on one reading
and not on the one the claim registered:** both are exercised, and only
as inline tags, reaching **no status slot anywhere**. The falsifier asked
for a SOURCE carrying `DERIVED`; what arrived was a new kind of entry
carrying it. **The substantive half then closed too** -- see `AGA_043`:
`TRANSFER_NOTE` combines two sources into a third statement and is
tagged. What is left of this claim is the vocabulary: one declared scale,
five sites, three mechanisms, three question tokens declared nowhere.
*Falsifier:* a second declared scale for questions, or a source carrying
`DERIVED`.

**AGA_021 -- S1 and S3 are not two sources. SUPPORTED.** S3's author list
(Braver, Preusser, Ulmer) is a strict **subset** of S1's (Braver, Preusser,
Preusser, Baum, Beilock, Ulmer); the two carry identical sampling-frame
flags (`ON_ROAD`, `ADMISSION`), are eight years apart, and their headline
figures agree (*~3/4* and *73%*) -- which is what one group's instrument
produces and is not two confirmations. QA names four sources; through
`effective-redundancy-audit`'s own `n_eff`, **imported and not
reimplemented**, it is **3**. The collapse is a DECLARED boolean, so a
reader who holds two papers by one group to be two independent readings
gets `n_eff == n_nominal` and the check says which. The register's reading
rules have no rule for a shared node. The overlap is computed from citation
strings, which is a name-token match and not a name index -- stated at the
function, and the only positive it returns is a subset relation over three
tokens, which survives both of that method's failure modes.
*Falsifier:* a fourth reading rule, or QA gaining a source from another
group.

**AGA_022 -- the frame rule says every source carries one and one carries
none. SUPPORTED.** The docstring heads the flag list *"(every source
carries one)"*; **S6 carries an empty list**, and there is no `UNKNOWN`
member, so an empty list reads as *no sampling-frame concern* and as
*frame not established* identically. S6 is the source whose `n`, `years`
and `where` are all `"?"` -- the absence is honest and unrepresentable,
which is the absent-vs-known-negative repair missing on the field the
register's entire bias argument runs through. *Falsifier:* a sixth declared
flag for an unestablished frame.

**AGA_023 -- QE's own sentence is 8 of 12 as written and 8 of 9 as meant,
and S6 is what stops it being 9 of 9. SUPPORTED, numbers moved by the
revision.** QE's next-read field
states *"every source here is ON_ROAD cross-section."* Eight of twelve
sources carry `ON_ROAD`; the four that do not are three non-samples (`S9`
VENDOR, `S10` N_OF_1, `Q1` ARCHIVE) and S6. Over samples it is 8 of 9 and
the ninth is S6, whose frame is unstated -- so **`AGA_022`'s missing state
and this unchecked boundary are one gap at two sites**, and supplying S6 a
flag closes both (asserted, in both directions). The sentence is right
about what it means and wrong as written. *Falsifier:* S6 declaring a
frame.

**AGA_024 -- a flag is carried for a consequence and defined as a method,
and the revision added a second instance. SUPPORTED, n=1 -> n=2.** `ON_ROAD` is defined as *"interviewed while working -> excludes
drivers already out"*. S5's `where` is *"carrier records (crash, moving
violation)"* -- **nobody was interviewed**. The revision added **S11**,
`where` = *"carrier records"*, carrying `ON_ROAD` on the same reasoning:
two of the flag's holders now name no method, against five that do (S7's
`where` is `"?"` and is reported as unknown, not as a mismatch). The
author has not seen this audit, so the second instance is independent
recurrence and not a finding disregarded. The survivorship *consequence*
still holds -- a driver who crashes out or quits leaves the roster -- so
the flag is right about the bias and wrong about the mechanism: the
vocabulary conflates a sampling METHOD with a sampling CONSEQUENCE. The
repair is either a member for record-based survivorship or a definition
stated as the consequence. *Falsifier:* S5's `where` naming an interview.

**AGA_025 -- `holds` carries two kinds of entry with no field between them.
SUPPORTED, numbers moved by the revision.** Of 36 entries, **10 are
reading-state notes rather than findings** (*"violator characteristics table exists -- contents UNREAD"*,
*"crash TYPE by tenure: not in relays"*), and **three of eleven sources
contribute no finding at all** -- S7, S8 and Q1 are reading-state top to
bottom. A consumer counting `holds` as evidence gets 36 where 26 are
findings and three sources are worth zero. The revision added four
entries and removed one, and the reading-state count did not move. *Falsifier:* a `reading_state`
field, or a source moving off the all-notes list.

**AGA_026 -- the one containment the register admits, and it holds.
SUPPORTED.** S2 states *47.1% ever fell asleep* and *25.4% in the past
year*; a past-year rate exceeding an ever rate would be impossible, and it
does not (ratio 0.539). The check is shown able to fail on a constructed
reversal, so the pass is a measurement. *Falsifier:* a third rate in S2
that breaks the nesting.

**AGA_027 -- the register gives the Aurora facts a source; `AGA_016` is
not thereby closed. SUPPORTED.** `AGA_016` recorded that
`FIELD_LAYER_SEED_ROADS` cites the observer / roadside-assist / weather
facts to `DEMO_CORPUS_AUDIT`, which carries none of them. S9 cites the same
material to *"Aurora Innovation releases + trade press (Feb-Mar 2026)"* --
an origin rather than a sibling pointer -- and flags it `VENDOR`. Checked
across the folder, **none of the four distinctive terms appears in
`DEMO_CORPUS_AUDIT`**, so `AGA_016` stands as written and what has changed
is that the facts now have a provenance, unread here. *Falsifier:* the
cited sibling gaining the supporting text.

**AGA_028 -- S9's headline cannot be sized from inside the corpus.
SUPPORTED.** *"~1,000 mi Fort Worth-Phoenix in ~15 h, no HOS stop"* derives
**66.7 mph sustained** from the register's own two numbers. The advantage
the phrase names is the difference against a legal driving limit, and
**no driving-hours limit is stated in the register or in any of the six
delivered documents** -- the register states the off-duty figure (S4's
*"< 10 h off"*) and names HOS three times and carries no driving-hours
value. So QH is not merely unmeasured for want of terminal-dwell data: one
of its two terms is absent from the corpus. The delivered corpus and this
audit's own output are scanned apart and both columns print, for the reason
`AGA_030` defect 4 records. *Falsifier:* any delivered document stating a
driving-hours limit.

**AGA_029 -- the register self-dates to the session, which bounds
`AGA_008`. SUPPORTED.** `AGA_008` records all six delivered documents
self-dating 2026-09-24, one day ahead of the session landing them. The
register dates itself **2026-09-23**, the session date. `AGA_008` is
therefore a property of the six and not of the drop family; the six still
agree with each other (asserted). *Falsifier:* a seventh document dating
2026-09-24.

**AGA_030 -- four defects in this session's own checks, each found by
checking or by running, none by reading. SUPPORTED.**
(1) `frame_definition_fit` returned a bare boolean, so S7 -- whose `where`
is `"?"` -- printed `fits definition: False` **identically to S5's measured
mismatch**: the absent-vs-known-negative collapse this folder records
repeatedly, committed inside the check, on the field that decides
`AGA_024`. Repaired to three states, with `None` for unknown pinned in both
directions. (2) A first hand-pass located the Aurora facts with a bare
`40%` pattern, which matches the Komatsu ledger's `+40%` tire figure -- a
different quantity -- and would have returned a duplication count that is
not one; the shipped check uses distinctive terms only and says so. (3) `AGA_031` was first
written as *"two of the eight questions rest on it and both are
UNMEASURED"*; three name S10, one of those three is SUPPORTED, and exactly
one rests on it alone -- a claim written from a plausible reading of the
data rather than from the data, in a table about restated figures. Caught
before commit by computing it, and now computed by a check rather than
asserted. (4) Writing `AGA_028` down put
the phrase *driving-hours limit* into `CLAIM_TABLE.md`, a `.md` file in the
folder `hos_sizing` scans -- so the next run read **the audit's own record
of an absence as evidence of a presence** and the suite went red. Repaired
by scanning the delivered corpus and the audit's own output **apart**, with
the delivered list imported from `audit.DOC` rather than retyped and the
audit-side count printed rather than excluded: an exclude list would close
the loop by hiding it, and anyone grepping the folder still finds the
phrase. Defect 2 is the same class as `AGA_019`'s falsifier-id over-count,
a pattern matching a second referent; defect 3 is `AGA_019`'s third, a
sentence standing in for a count; defect 4 is `UNI_010`'s self-reference
loop, arriving here through the claim table rather than through a samples
directory. *Falsifier:* any of the four failing to reproduce on the
recorded revision.

**AGA_031 -- the register places the operator's own record inside its own
sample and takes no exemption. SUPPORTED.** S10 is the requester's
first-hand record and is scored on the same six-rung scale as every
published source, carries a sampling-frame flag like every other source
(`N_OF_1`), and is governed by a stated non-inference: *"N_OF_1 is
OBSERVED, not anecdote: it bounds what is possible, it does not estimate a
rate."* **Five** of the ten questions name S10 after the revision, up
from three, and the one that rests on it ALONE -- QF -- is still
UNMEASURED with the reason in its own status field (*"N=1 only"*); QA is
SUPPORTED and names three other sources beside it. The rule held while the
register's reliance on the record nearly doubled, which is the harder
test. So the non-inference rule is followed rather than declared. This is the discipline the
sibling register records at `UNI_071` -- noticing does not place a source
outside its own population -- arrived at independently and, unlike there,
built into the scale before any entry. *Falsifier:* a question scoring
SUPPORTED on S10 alone.

**AGA_032 -- UNVERIFIED, and it covers the register.** No source in it was
read. The register says so itself for five of the eleven (`UNREAD`), and
the egress gate refuses every publisher host, so the other six are carried
on the strength of a search pass nobody here can repeat. Nothing in
`AGA_020..050` is evidence about driving hours, fatigue, tenure, any
carrier or any vendor; every one is a property of the register's own
declarations. Whether the eight questions have the status the register
assigns them is untouched in both directions.

---

## The revision

The register was revised after `AGA_020..032` were published against it.
A revision is a copy of its predecessor and copies drift, so
`register_audit.revision()` reports what moved rather than assuming it,
resolving the previous version **by content** -- the most recent commit
whose blob differs from what is on disk -- and not by a position in
history, which would compare against the same bytes as soon as an
unrelated commit landed between them. Twelve pinned checks fired on the
revision; every one named a number that moved, which is the suite working
rather than the revision being wrong.

**AGA_033 -- a source whose provenance is another source in the register,
and the shared-node check cannot see it. SUPPORTED.** S11 cites *"Lin et
al. (1994) ... as summarised in McCartt et al. 2000"*, and McCartt et al.
2000 is **S2**. `AGA_021`'s check matches name tokens ahead of the year,
so it finds nothing: S11's own author list and S2's are disjoint, and the
relation that makes them one channel is stated in prose after the
parenthesis. A second shared node, of a different kind from S1/S3 --
there two papers by one group, here one source relayed *through* another
source in the same register -- and nothing in the register marks it.
It costs no `n_eff` today only because S11 reaches no question.
*Falsifier:* S11 entering a question alongside S2, or a `relayed_through`
field.

**AGA_034 -- the TERM_DRIFT flag marks two of the four sources the note
itself names. SUPPORTED.** `TERM_NOTES` states the remedy as *"read item
wording (S1, S2, S7, S8)"*; `TERM_DRIFT` is carried by **S1 and S2 only**.
No source is flagged without being named, so the gap is one-directional:
the two the note says to read and did not get the flag are exactly the two
whose status is already `UNREAD` top to bottom, which is where a flag
would do the most work. QI carries a **third set** (`S1, S2, S10`), and
that is not an error -- S10 is the term-drift evidence and S7/S8 are the
unread items, two roles with one list to put them in. *Falsifier:* S7 or
S8 gaining the flag, or the note narrowing to two.

**AGA_035 -- the closing number counts one token of the three the register
uses for an open cell, so adding open questions lowered the reported
fraction. SUPPORTED.** `main()` counts questions whose status begins
`UNMEASURED`: five. The revision added **QI (`PARTIAL`)** and **QJ
(`UNRESOLVED`)**, both open and neither counted, so the headline reads
**5 of 10** where **7 of 10 are not answered** and only three carry
`SUPPORTED`. The addenda then put a further question -- **QK**,
`UNMEASURED` -- in a **separate list** that `main()` does not count and
`question_refs()` does not reach, so **eleven questions exist, the
closing number is taken over ten, and eight are not answered.** The
register's own thesis is that *an UNMEASURED cell is a result*; three
results were added and the number that reports them went down as a
fraction, 5/8 to 5/10. The repair is the same one `AGA_020`
points at -- the question vocabulary is undeclared, so nothing says which
tokens mean open. *Falsifier:* a declared question scale, or the count
reading every non-`SUPPORTED` status.

**AGA_036 -- the revision measured. SUPPORTED.** +64 lines, -5, against
`1bb8471`. All three top-level objects changed (`SOURCES`, `QUESTIONS`,
`RULES`), **none is byte-identical**, one is new (`TERM_NOTES`) and none
was removed. The five removed lines are S2's frame and predictor-block
entry, replaced in place. What the revision did NOT touch is as recorded:
the self-date stays 2026-09-23 (`AGA_029` unmoved), S6 still carries no
frame flag though the flag vocabulary itself gained a member
(`AGA_022` untouched by a revision that edited the list it is about), and
the S1/S3 shared node stands (`AGA_021`) -- though their frames are no
longer identical, correctly, since S3 is about dispatchers and schedules
and carries no fatigue item to drift. *Falsifier:* a later revision with
an object byte-identical to this one and a claim about it moving anyway.

**AGA_037 -- one defect in this session's harness, found by running.
SUPPORTED.** The three-arm exemption masks each source's `where` string
before screening. S11's *"carrier records"* is a **strict prefix** of S5's
*"carrier records (crash, moving violation)"*, so masking in dict order
replaced the short one first and left `(crash, moving violation)` standing
-- the arm reported the token it had been written to mask. Repaired by
masking longest-first. Same class as `AGA_030` defect 2: a pattern
matching a second referent, here inside the harness that measures the
exemption rather than inside a check. The exemption stays **one token
wide** and the width assertion is unchanged; two further hits the revision
produced (`fix`, the register's own field name, in this audit's prose)
were **reworded rather than exempted**, per the house rule. *Falsifier:*
the prefix collision failing to reproduce on the recorded revision.

**AGA_038 -- what the revision gets right, and it is the strongest content
in the folder. SUPPORTED.** Two things. **(1)** The term-drift note
records a **citation-chain conversion** as an observation rather than an
inference: the S2 abstract says *"at the wheel of a truck"*, later
citations restate it as *"while driving"*, and both wordings are carried
with their sources so a reader can see the conversion happen. That is the
`term-drift-citation` folder's subject -- does a citation still attach to
what it cites -- arriving from a different direction and on a case where
the two readings have **opposite signs for risk**: a rest act and a hazard
event counted as one. **(2)** QJ states a contradiction between two
sources the register already holds -- S2 has experience predicting MORE
*"fell asleep at the wheel"*, S5 has crash risk FALLING with experience --
lists three rival explanations (exposure, age, term drift), says which
predicts the contradiction fully and which only partly, and **picks
none**. The register's own term-drift hypothesis is the one that predicts
it fully, and it is not thereby selected. *Falsifier:* a later revision
resolving QJ without the item wording being read.

**The UNVERIFIED claim covers the revision too** (`AGA_032`): no source in it was read, S11 is
relayed rather than located, and the secondary review the S2 holds cite is
carried at the same status as everything else.

---

## The addenda

Two further additions, landed the same day: a continued-work block (QK, the
clock-vs-state control loops, a behaviour-anchored record schema, W1-W9) and
a **proposed gate map** G0-G4 with the first runnable arithmetic in the
register. The addenda are **pure additions** -- `SOURCES`, `QUESTIONS`,
`RULES` and `TERM_NOTES` are byte-identical across them, asserted. Every
input to the arithmetic is declared `PLACEHOLDER` by the register itself,
and nothing below is a statement about any route, season, carrier or
vehicle.

**AGA_039 -- the two blocks the G0 gate runs on carry provenance by
different means, and only one survives import. SUPPORTED.**
`EVENT_CLASSES` -- the RATE, the gate's denominator -- carries a source
string as a fourth tuple element on all six rows. `REST_BLOCK` -- the
WINDOW, the gate's numerator -- carries it in **comments**, which are not
in the object at all: a consumer importing the register gets four bare
numbers. The comments themselves hold three classes with nothing marking
them apart (`handoff_lead_min` PLACEHOLDER; `nap_min` and `inertia_min`
literature-but-NOT-VERIFIED; **`cycle_min` neither**), so the block whose
values decide whether the gate passes is the one a reader cannot grade.
*Falsifier:* a source field on `REST_BLOCK`.

**AGA_040 -- the G0 block recomputes, and note 3 holds. SUPPORTED.**
Human-required interrupt rate **0.330/h**, mean gap **181.8 min**, and
the four window rows reproduce (60 min -> 0.719, 75 -> 0.662, 110 ->
0.546, 125 -> 0.503). The binding row is `cycle_min` at high inertia,
**P 0.503** -- a coin flip. Note 3 says *"the binding term is
`p_machine_fails`, not raw event rate"* and that is exactly right:
`heavy_traffic_merge` has the **highest raw rate** (0.50/h) and
contributes 0.05, while `work_zone` at 0.30/h contributes **0.09** and is
the top interrupter. Removing it -- the lever the note names -- takes the
rate to 0.24 and the binding row to **0.607**. *Falsifier:* a rate table
where the top raw rate and the top contributor are the same row.

**AGA_041 -- one caveat is stated in two places under two different
conditions, and the two run in opposite directions. SUPPORTED, shown
exactly and with no simulation.** Both cases are Poisson integrals.
**(A) Bursting alone.** In the limit where a burst of `k` arrives at one
instant, the process of BURSTS is Poisson at `lam/k`, so
`P = exp(-lam*w/60k)`, strictly **greater** than `exp(-lam*w/60)` for
every `k > 1`: on the binding row, 0.503 -> 0.709 (k=2) -> 0.872 (k=5) ->
0.934 (k=10). **Poisson is a FLOOR.** **(B) A rate peaking at the hour
rest is needed.** P over a window started at the peak is `exp(-integral)`,
and the integral exceeds `lam*w` at any positive amplitude: 0.503 ->
0.363 -> 0.261 -> 0.189. **Poisson is a CEILING.** The function's
docstring names **B** (*"when events cluster in the same hours as rest
need"*) and is right. The G0 note **drops the condition**, describes
**A** (*"interrupters bunch in the same hours (weather + traffic +
incidents)"*) and draws **B's** conclusion (*"Poisson overstates usable
windows -- treat as ceiling"*). A qualifier lost between two occurrences
of one phrase, with the reading inverting -- which is this register's own
subject, instanced in its own text. Correcting it makes the register's
case **stronger**, not weaker, and strongest where it binds: the row that
reads as a coin flip is the row bursting helps most. *Falsifier:* a
cluster model where P falls at fixed mean rate without the peak being
aligned to rest need.

**AGA_042 -- `p_uninterrupted` is typed as a probability and its domain is
unguarded. SUPPORTED, reported not repaired.** A negative window returns
**1.391** and a negative rate **1.989**. Both valid-domain edges are exact
1.0 and are real measurements rather than defaults -- a zero rate leaves
every window clear, a zero-length window cannot contain an event -- which
is the half that matters and the half that holds. The file is delivered,
so this is recorded rather than patched. The metric is now registered in
`tools/known_answer.py` with five cases; its note states the one class of
error the case set **cannot** catch, since `lam*minutes` is symmetric and
an argument swap returns the same number. *Falsifier:* a domain guard.

**AGA_043 -- a DERIVED entry now exists, closing `AGA_020`'s substantive
half. SUPPORTED.** `TRANSFER_NOTE` draws on **S5** (the NSTSCE authors'
mentoring recommendation, which that source does state -- checked) and on
**TERM_NOTES** (the rest-act / hazard-event drift) and produces a third
statement neither carries: *mentoring runs on words, and where a term has
drifted, told practice arrives inverted -- record the behaviour, not the
phrase.* It is tagged `[DERIVED]`. The `BEHAVIOUR_RECORD_SCHEMA` beside it
is that conclusion built: six fields anchored on what the vehicle and the
body did, with the two free-text fields (`trigger`, `resumed_after`)
carrying the skill the phrase cannot. *Falsifier:* the note resting on one
source.

**The UNVERIFIED claim covers the addenda too** (`AGA_032`): the aviation
planned-nap lead, the FMCSA split-sleeper rule, the team-driver sleep-
quality lead and every event rate are carried or declared placeholder, and
nothing here was read.

---

## ADDENDUM_3.md

A second DELIVERED document, in notes rather than Python: a G0 sleep-quality
factor, a consequence, a two-literature gap, a probe, scope limits, a flip,
a new status rung, and the X1 record. It is landed verbatim and read as
delivered; the register is read as delivered; where the two disagree that is
reported and **not resolved**, and nothing is transcribed from one into the
other. Every source it names is carried or absent, and nothing below is a
statement about sleep, infancy, any population or any operator.

**AGA_044 -- the note declares a status rung the register's scale does not
carry. SUPPORTED.** `STATUS ADDED / EXPLORATION -- real gap, relevance
UNKNOWN; kept, not load-bearing.` The register's docstring declares six
rungs and `EXPLORATION` is not among them. This is the **sixth site** for
one scale and the first in a different file: two delivered documents share
a vocabulary and only one of them declares it. Consistent with `AGA_020`,
and worse in one respect -- a reader of the register alone cannot discover
the rung exists. *Falsifier:* the register's docstring gaining it.

**AGA_045 -- the note makes G0 a per-OPERATOR gate and the register's G0
is per-route. SUPPORTED.** `motion_sleep_history` is entered `OBSERVED,
N=1` with the consequence stated in one line: *"G0 can PASS for one
operator and FAIL for another on the same route."* The register's G0 entry
and its four notes name **route** and **season** and never **operator**
(checked), and `REST_BLOCK` holds four constants where the note treats one
as a variable. So the gate as built cannot express the note's own result:
G0 is indexed on (route, season) and the note adds a third axis.
*Falsifier:* an operator term in `REST_BLOCK` or in the G0 entry.

**AGA_046 -- 'a blanket rule written to the lowest sleeper forfeits the
capacity of everyone above it', made a number. SUPPORTED.** On the
register's own placeholder rate (0.330/h) and its own four windows, a fleet
rule set to the longest (125 min) leaves:

    nap_min/low      60 min   own 0.7189   under the rule 0.5028   -30.1%
    nap_min/high     75 min   own 0.6620                           -24.0%
    cycle_min/low   110 min   own 0.5461                            -7.9%
    cycle_min/high  125 min   own 0.5028                             0.0%

so the best motion-sleeper gives up **30.1% of their own capacity**. The
structural half is sharper than the arithmetic: the gap
`exp(-lam*w1/60) - exp(-lam*w2/60)` **vanishes at both ends** -- at a low
rate everyone clears, at a high rate nobody does -- and peaks at
`lam = 60*ln(w2/w1)/(w2-w1) = 0.678/h`, so **the cost of a blanket rule is
largest exactly where the rule is deciding anything**, and the register's
placeholder regime sits at **82% of that peak**. No fleet aggregate is
emitted: the mix of operators is unmeasured, and a fleet number would be a
figure with no denominator. *Falsifier:* a window set where the longest is
also the most common.

**AGA_047 -- the note carries its own confound and the covariate that
separates it, in adjacent sections, and the compressed record drops the
one that confounds its own prediction. SUPPORTED.** X1 predicts *early
habituation -> smaller motion effect*. `SCOPE LIMITS` names two limits: the
stimulus differs (lab rocking is not cab vibration) and the **good-sleeper
ceiling** -- *"effects may only show in people with room to improve ->
baseline must be recorded"*. A habituated sleeper is a good motion sleeper,
has less room, and shows a smaller effect: **the ceiling predicts the same
direction as the prediction**, so the probe as written -- *one covariate*,
`early_motion_exposure` -- cannot separate them. The second covariate is
named one section above the probe and is in neither `CHEAPEST INSTRUMENT`
nor X1's `probe` field, and X1's `scope` field carries the stimulus limit
and **not** the ceiling (checked). Third instance in this family of a
qualifier lost in compression, after `AGA_041` and the register's own
`TERM_NOTES` subject. The repair is already written: record baseline.
*Falsifier:* `baseline` appearing in the probe.

**AGA_048 -- X1's two halves are both outside the register, and no frame
flag covers the sampling limit it names. SUPPORTED.** Neither adult rocking
labs nor infant carrying studies is among the register's twelve sources
(checked), so unlike **QJ** -- which held a contradiction between two
sources the register already carried -- X1 is a gap between two literatures
it does not hold. That is honest and is what `EXPLORATION` is for. Beside
it: the note states a sampling limit on half 1 (*"young males, lab,
Swiss"*) and the six declared frame flags have **no member for a narrow
laboratory sample**; `ON_ROAD` is the nearest and describes the opposite
kind of draw. The same shape as `AGA_022`'s missing `UNKNOWN`, one axis
over. *Falsifier:* a seventh flag, or either literature entering as a
source.

**AGA_049 -- the note's one pointer resolves nowhere. SUPPORTED.**
`[[per-operator-fitness-vs-lcd-regulation]]` matches no file anywhere in
the tree. Cited as the shape the consequence shares, so it is load-bearing
for the analogy and not for the arithmetic, which `AGA_046` computes
without it. *Falsifier:* the note arriving.

**AGA_050 -- the flip rests on the operator's own record and is fenced four
ways rather than promoted. SUPPORTED.** The `PROPOSED flip` argues that
carried infancy was the ordinary human pattern and that *"the population a
fleet rule is written for may be the unusual one, and your history closer
to the species baseline"* -- a generalization from the register's `N_OF_1`
source, and the one place in the whole register where the operator's own
record could buy an exemption. It does not: the passage is labelled
**PROPOSED**, given the status **EXPLORATION**, marked **relevance
UNKNOWN**, and declared **not load-bearing**, with X1's `anchor` field
stating its own n. `AGA_031` recorded that the operator's record takes no
exemption; this is the harder case, because here the exemption would be
favourable and is declined in the same breath it is proposed. *Falsifier:*
a later entry resting a question on the flip.

**The UNVERIFIED claim covers this note too** (`AGA_032`): Omlin, the
whole-body vibration field (ISO 2631, unsearched by the note's own
statement), the adult rocking literature, the infant carrying literature
and the cross-cultural claim are all carried or declared unsearched, and
nothing here was read.

