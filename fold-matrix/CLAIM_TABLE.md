# CLAIM_TABLE — fold-matrix

Claims about work order 8 and about what its fixtures produced.
`WORK_ORDER.md` is delivered and is not edited.

REFUTATION_PROTOCOL: each claim names what would refute it. A failed
check updates the claim, never the instrument's numbers.

---

### FM_001 — the arm this order extends is not in this repository

The order opens *"Extends: folded-term instrument. The downward arm
(levels severed, deepest still-acting term) already has a reading."*

There is no folded-term instrument here and no downward reading in it.
`severed`, `still_acting` and *deepest still-acting term* return **zero
hits** across the tree before this folder. `residual-direction/` names a
"fold detector" as a companion and `claim-record/SPEC.md` cites one as
the reason the frames work was specified early — both are pointers to
something outside.

Seventh instance of the stated-thing-with-no-artifact shape (`MF_017`,
`CW_015`, `DL_004`, `GC_012`, `UNI_013`, `SSS_050`) and the largest so
far: the prior six were a missing field or a missing test, and this is a
missing arm of the instrument being extended.

**Nothing is reconstructed.** The grid holds both arms and downward cells
are filled only where today's material fills them; H1's levels −2 and −3
carry `ABSENT` rather than a plausible reading. That is the `PB_001` /
`CW_004` rule, and the one prior reconstruction in this repository is
what it cost.

**Falsifier:** a downward-arm reading predating this folder.

**Status: SUPPORTED. The grid is built; the downward arm is a schema
with two filled cells, not a reading.**

---

### FM_002 — the fixtures do what S6 requires, and one of them exposed a defect in the instrument

| fixture | S6 requires | result |
|---|---|---|
| H1 grid emission factor | downward levels resolve, level-0 clock derivable, upward cells ASSERTED | −1 and 0 resolve, level-0 clock **3.403 y derived**, upward **ASSERTED ×2 + ABSENT ×1** |
| H2 "more efficiency solves this" | NOT_EVALUABLE on S3, not a low score | `NOT_EVALUABLE`, all three scope fields named, no score emitted |
| H3 tree replacement | Y_function_set UNREAD, comparison refused | `UNREAD`, refused as *"nothing was compared"* |
| H4 two conflicting clocks | both emitted, mismatch flagged, no pick | 0.003 y and 3.0 y both emitted, mismatch flagged, `collapsed: None` |

H1's level-0 clock is derived rather than stated: `3.0 y / 0.8815` where
the coupling was **measured by perturbation** in
`sheet-structure-scan/coupling.py`, not asserted.

**Falsifier:** a fixture passing for a reason other than the one S6
names.

**Status: SUPPORTED, 4 of 4.**

---

### FM_003 — the clock check could not tell an assumption from its own derivative, and H1 is what showed it

S5 says *"if two levels assume different time constants, emit BOTH and
flag the mismatch"*. The first implementation counted distinct
`(value, units)` pairs, and on H1 that reads:

| level | clock | |
|---|---|---|
| −1 | 3.0 years | the generation mix, assumed |
| 0 | 3.403 years | **3.0 / 0.8815**, derived from level −1 |

and flags a mismatch. **It is one horizon and its own derivative**, not
two horizons in conflict — the coupling divisor is what makes the numbers
differ, and dividing an assumption by a measurement does not produce a
second assumption.

Repaired with a `derived_from` field on the clock: derived clocks are
still **emitted**, with what they came from, and only the disagreement
count excludes them. H1 now reports no mismatch and H4 still does.

The defect matters because the false positive runs toward the finding:
S5 says a term whose levels disagree on horizon **is** the finding, so an
over-firing check manufactures findings, and every derivation chain in
the claim registry would produce one.

**Falsifier:** two independently assumed clocks the check reads as a
derivation.

**Status: REPAIRED, pinned three ways.**

---

### FM_004 — P1 and P2 hold, and the evidence for them is narrower than the tally

Registered in `PREDICTIONS_WO8.md` before the fixtures were authored.

| | prediction | result |
|---|---|---|
| P1 | ASSERTED + ABSENT are a strict majority of upward cells | **True** — 3 soft, 0 hard |
| P2 | every `value_string` is empty | **True** — 3 of 3 |

**The honest scope.** Two of the four fixtures are excluded from the
tally as NOT_EVALUABLE, correctly, so the tally rests on H1 and H4. H4's
single upward cell was authored from this repository's own claim table.
**H1's three cells are the only ones traceable to an artifact outside
this session** — they are read from `Disclaimer!A3` of the UNFCCC
calculator, quoted, and anyone with that file can check them.

So P1 and P2 hold on n = 2 terms with external evidence from one, and
that is a weaker result than "4 cells, 4 empty" reads as.

**A weaker registration than WO6's, stated.** `PREDICTIONS_WO8.md` was
written before the fixtures existed but was **not committed before the
run**, unlike WO6 where the commit hash is the timestamp. The evidence
that it preceded the fixtures is the file's own ordering in one commit,
which is weaker.

**Falsifier:** an upward cell in a term drawn from an external artifact
carrying a non-empty value_string.

**Status: SUPPORTED, at the scope stated.**

---

### FM_005 — an empty value_string has two causes and the four basis values do not separate them

S2 requires `value_string` per upward cell and says empty is the normal
result. On H1 level +1 it is empty for a reason the schema cannot record:
the source **states the goal and explicitly declines the relation**.

`Disclaimer!A3` says the calculator exists *"to support organizations to
estimate their GHG emissions"* and, in the same cell, that the secretariat
*"makes no representations as to the accuracy, completeness, suitability
or validity of any information on this Spreadsheet"*.

That is not `ABSENT` — a goal is stated. It is not ordinary `ASSERTED`
either: a relation claimed at adoption with no value string, and a
relation the source refuses to claim, are different facts arriving at the
same empty cell.

**Fourteenth instance of the absent-vs-known-negative repair here**, and
the first where the missing state is *the source declined*. Carried as a
`source_disclaims` field beside the basis rather than folded into it, and
printed under the upward table with the quote, so the distinction is
visible without adding a fifth basis value to a delivered vocabulary.

**Falsifier:** a use where *nobody stated a relation* and *the source
declined to state one* license the same next step.

**Status: SUPPORTED. Recorded, not resolved by widening the vocabulary.**

---

### FM_006 — NOT_EVALUABLE is unrankable structurally rather than by convention

S3: *"Do not score it, do not rank it, do not carry it into a
comparison."* Three instructions a caller can forget.

`score()` **raises** on a NOT_EVALUABLE term — and raises on an evaluable
one too, with *"one term, one grid, not one number"*, because there is no
score in this instrument at all. `upward_tally()` excludes refused terms
and names them, so a refusal never enters a count as a zero.

The H2 fixture is the case: it returns `NOT_EVALUABLE` with all three
scope fields named, and the report states in its own words that this is a
refusal about what can be read and not a low reading.

One distinction the check makes that S3 does not: a scope field **present
but declared unknown** is missing too, and is reported apart from an
omission. `horizon: "unknown"` is an honest declaration and still does not
let a ratio be compared, but the two call for different next steps — one
is a gap in the record, the other a measurement nobody has.

**Falsifier:** a path by which a NOT_EVALUABLE term reaches a ranking.

**Status: SUPPORTED.**

---

### FM_007 — S3's scope is declared-frame's core plus one field, and the two are wired rather than retyped

`boundary` and `horizon` are two of `declared-frame`'s three CORE fields.
They are **read out of `declared-frame/v2/check_frame.py` at import** and
asserted in the selftest, rather than retyped here, so the two folders
cannot drift about what a frame's core is — the no-copies convention
`MF_019` and `tools/check_gate_drift.py` exist for.

`with_respect_to` is S3's addition and is a different question:
declared-frame asks what is inside the accounting, S3 asks what the ratio
is taken **against**. `who_counts`, declared-frame's third core field, is
not required here.

The H3 fixture is where that bites: its `neutral_reading.frame` is
`DF_005`'s finding verbatim — the panel frame excludes fabrication,
mining, smelting, transport, installation, maintenance and decommission
while the leaf frame puts all of them inside the same photon budget — so
the term is NOT_EVALUABLE on `boundary: unknown` **and** would be a void
ratio if it were filled in.

**Falsifier:** a change to declared-frame's CORE that this module does
not pick up.

**Status: SUPPORTED, asserted at selftest.**

---

### FM_008 — the exemption harness kept "for a real exemption later" is spent here, on exactly one word

`SSS_049` retired scan 4's exemption and kept the three-arm harness for a
real case. This order is one: S3 names the efficiency class as
*"efficient/optimal/better/faster"*, and **`better` is on `no_severity`'s
interpretation list** while the other three are not.

`DELIVERED_VOCABULARY = ("better",)` — one token, declared, and measured
three ways: the report is clean under the mask, nothing but that token
fires without it, and a planted grading word is caught through the
exemption. A fourth check asserts the list is length one, so a widening
turns it red rather than passing quietly.

`waste`, `optimization` and `improvement` are flagged by S4 and are **not**
on the screened list, so they need no exemption — checked rather than
assumed.

**Falsifier:** a screened word in an emitted report, or an exemption
entry the order does not name.

**Status: SUPPORTED.**

---

### FM_009 — S4's neutral reading is a declared field, because a name cannot be de-signed

S4 says to flag any variable whose name asserts a sign and *"emit the
neutral reading alongside: the measured quantity plus its frame"*.

The neutral reading is **not computed from the name**. There is no string
operation that turns *efficiency* into *joules out per joule in, at the
cell surface, instantaneous* — producing one would be inventing a
measurement, which is the failure `uninstrumented`'s `PROXY SUBSTITUTION`
names. So it is a declared field, and a flagged term without one reports
`NOT_SUPPLIED` rather than a guess.

H2 is the case: `more efficiency solves this` is flagged and supplies
nothing, and the report says the field is not something a name can be
de-signed into. H3 supplies one, and it is `DF_005`.

The flag list is a superset of the efficiency class: `waste`, `leakage`,
`savings` and the rest assert a direction without triggering S3's scope
requirement. Both halves are asserted, because collapsing them would make
every mention of a loss require a horizon.

**Falsifier:** a neutral reading derivable from a name.

**Status: SUPPORTED.**

---

### FM_010 — the revision supersedes, both versions are kept, and the v1 format is refused rather than coerced

`WORK_ORDER_V2.md` lands verbatim beside `WORK_ORDER.md`, which is not
edited — the `declared-frame/` v1-and-v2 arrangement, so a reader can
diff the orders rather than take a summary of the difference.

Two changes: **S1a is entirely new**, and **S2's `value_string` becomes
three fields where it was one free-text string**.

`value_string()` **raises** on the v1 form rather than coercing an empty
string to three ABSENTs. Coercing would be the obvious kindness and it
would delete the distinction the revision exists to add: an empty string
cannot say *which* of the three fields is missing, so silently mapping it
to all-three-absent asserts something the v1 data never recorded. All
four fixtures were migrated by hand.

**Falsifier:** a v1 record whose empty string demonstrably meant all three
fields absent.

**Status: SUPPORTED. The refusal is pinned.**

---

### FM_011 — the fixed format recovers information the free-text field destroyed, and this is the revision's result

Under v1 every upward cell in this folder read `empty`. Under the triple:

| level | goal | sign | magnitude | unit |
|---|---|---|---|---|
| +1 | support organizations to estimate their GHG emissions | ABSENT | ABSENT | ABSENT |
| **+2** | **raise awareness and promote climate action** | **+** | **ABSENT** | **ABSENT** |
| +3 | not stated | ABSENT | ABSENT | ABSENT |

`Disclaimer!A3` says the calculator exists *"in order to raise awareness
and to promote climate action"*. **That states a direction.** It states
no size and no unit, and the file states none anywhere.

So the ordinary shape of a purpose claim is *sign yes, magnitude no, unit
no* — and one free-text field recorded it as **identical** to a cell
nobody wrote anything in. The three fields fail independently because
that is how claims fail.

Across the tally: `sign` ABSENT on 3 of 4 cells, `magnitude` and `unit`
ABSENT on 4 of 4. **P3 confirmed** (at least one cell splits), **P4
confirmed** (no magnitude anywhere), **P1 carried** (4 soft, 0 hard).

**Falsifier:** a reading of `Disclaimer!A3` under which *"in order to
raise awareness"* claims no direction.

**Status: SUPPORTED. The format change is the finding, not the fixtures.**

---

### FM_012 — S1a's downward rule instanced: the workbook's floor is three levels above its own physical chain

*"Deepest QUANTIFIED quantity — one the org computes, not one that
physically exists. Joules are not the floor unless joules were
calculated."*

H1's grid names four downward levels and the workbook computes at
exactly one of them:

| level | quantity | unit | computed |
|---|---|---|---|
| 0 | emissions | kg CO2e | **yes** — `Report!E25`, entered kWh × the factor |
| −1 | generation mix shares | fraction | no — the factor arrives as a published constant |
| −2 | marginal plant heat rate | MJ/kWh | no |
| −3 | CO2e per unit fuel energy | kg CO2e/MJ | no |

**Downward stop: level 0. `unmeasured_span`: 3 levels.**

Every level below the stop names a real physical quantity with a real
unit, and the physical chain runs through all of them whether or not
anyone computes them. That is precisely the case the rule is written
for, and a naive reading — *the floor is the deepest thing that exists* —
would have put the stop at −3 and reported a span of zero.

Emitted, never scored (S1a). `score()` raises on the whole term anyway.

**Falsifier:** a computed quantity below level 0 in this document set.

**Status: SUPPORTED.**

---

### FM_013 — `computed` is a declared field, because inferring it from existence is the failure the rule names

Nothing in `downward_stop()` infers that an organisation computed a
quantity from the fact that the quantity exists. `computed` is declared
per level, and `validate()` refuses a `quantified` block that omits it.

That refusal is the rule made structural. A reader who fills in
`quantified` from the physics — *there is obviously a heat rate, so put a
heat rate here* — is exactly the reader S1a is written against, and the
schema stops them at load rather than at read.

**Falsifier:** a path by which `computed` is set without being declared.

**Status: SUPPORTED, refused at load.**

---

### FM_014 — the plan column is separate and the code cannot merge it

S1a: *"Separate column, never merged into basis."* Enforced three ways —
it is read from its own `plan` key, returned in its own dict by
`plan_column()`, and the selftest asserts that a term carrying
`plan_exists: yes` produces the same `basis` values it produced without
one.

`practice_tracks_plan` defaults to **UNREAD**, not to `no`. A plan
nobody checked against practice and a plan practice demonstrably departs
from are different findings, and defaulting to `no` would manufacture the
second from the first.

Across the fixtures: H1 `yes / UNREAD` (the Disclaimer states a purpose;
whether any user's practice tracks it is not readable from that
artifact), H2 and H3 `no / UNREAD`, H4 `yes / yes` — the work order
states what the scan is for and the scan's own selftest checks that it
does it, both in the repository.

**Falsifier:** a plan value reaching a basis field.

**Status: SUPPORTED.**

---

### FM_015 — the registered prediction is not blind on H1, and says so

`PREDICTIONS_WO8_V2.md` registers P3 and P4 before the format was run —
and `Disclaimer!A3` was **already read in this session**, during the v1
run of the same fixture.

So P3 and P4 are not blind predictions about that text. They are
registered because the format is new and the split had not been computed,
not because the source was unread. The v1 registration had a different
weakness in the same place and stated it: written before the fixtures
existed, not committed before the run. This one is weaker still on H1.

What would be blind is the same format run on a workbook nobody here has
opened, and `SSS_053` is why there is not one.

**Falsifier:** none. This is a statement about what the registration is
worth, not a claim about the world.

**Status: RECORDED, and the weakness is the record.**

---

### FM_016 — `unmeasured_span` understates by construction, and the two real fixtures land at opposite ends

The span counts levels between the deepest computed quantity and the
deepest level **the grid names**. A term whose grid stops early reports a
smaller span than the world has. That understatement is disclosed in the
function rather than corrected, because correcting it would mean
inventing levels nobody wrote down.

| term | downward stop | span | |
|---|---|---|---|
| H1 grid emission factor | level 0, `kg CO2e` | **3** | an external workbook, stopping three levels above its own chain |
| H4 reported divergence count | level −2, `years` | **0** | a repo-internal reading, whose floor *is* its deepest named level |
| H2, H3 | none computed | not computable | not zero |

H4's zero is partly the disclosed understatement: its grid names two
downward levels and computes at the deeper one.

**CORRECTED by `FM_018`.** The paragraph that stood here read the 3-vs-0
contrast as *"real, and its size bounded by what each grid names"*,
hedged as a comparison of two documents rather than two systems. The
`enumeration_basis` amendment **refuses that comparison outright**: H1's
levels are `author_read` and H4's are `document_named`, so the two floors
were counted by different procedures and their difference is a number
about the procedures. The hedge was weaker than the refusal, and the
refusal is now in code.

**Falsifier:** a term whose named grid reaches its physical floor, which
would make the span exact rather than a lower bound.

**Status: SUPPORTED on the understatement; the cross-term contrast is
WITHDRAWN and refused in code.**

---

### FM_017 — a stated magnitude of zero is not an absent one, and the schema keeps them apart

`magnitude: 0` is a claim: the proxy is stated to move the goal not at
all. `magnitude: ABSENT` is the absence of any such claim. They are the
most confusable pair in this format and the ones a numeric field would
collapse.

`value_string()` normalises a missing key to `ABSENT` and leaves `0`
alone; `vs_all_absent` is False for a cell carrying zero; `validate()`
accepts a number or `ABSENT` and refuses anything else. Both halves
pinned.

S7 says absence is first-class and *"empty emits as empty, never as
zero"*. The converse needs saying too, and this is it: **zero emits as
zero, never as empty.**

**Falsifier:** a path where 0 and ABSENT reach the same reading.

**Status: SUPPORTED.**


---

### FM_018 — the amendment refuses a comparison this claim table published, and the rename is the larger half

The `FM_016` fix lands three things.

**`enumeration_basis`, declared and never inferred.** Four values —
`document_named` / `physical_traced` / `author_read` / `UNREAD` — with
`UNREAD` the default. A grid loaded without the field **declares**
UNREAD; it does not get one assigned from how well traced its levels
look. That is `FM_013`'s refusal on `computed`, and it is sharper here,
because a plausible level list is exactly what an author produces from
general knowledge without tracing anything.

The fixtures declare honestly, and the honest answer is not the
flattering one:

| term | basis | why |
|---|---|---|
| H1 grid emission factor | **`author_read`** | the workbook names none of these levels; they were listed from the author's reading of how a grid factor is built, with no source cited for the combustion, dispatch or mix levels |
| H4 reported divergence count | `document_named` | both levels are the neglected terms named in the claim records the reading rests on |
| H2, H3 | `UNREAD` | no downward level set to enumerate |

**The comparison is refused.** `compare_spans()` groups by basis and
emits both floors; across a mismatch it computes nothing, and
`difference` is `None` on every path. A selftest check reads this
module's own source and asserts no subtraction of two `span_min` values
appears in it.

**And that refuses `FM_016`'s own published contrast.** H1's 3 against
H4's 0 was reported with a hedge — *a comparison of two documents and not
of two systems* — and the hedge was weaker than the refusal. `FM_016` is
corrected in place rather than rewritten.

**The rename is the larger half.** `unmeasured_span: 3` reads as a
measurement of the world; **`unmeasured_span_min: 3` reads as a floor**,
which is what `FM_016` says it is. Before the amendment the honest
reading lived in a `note` string, where nothing downstream could see it —
**the same shape as a workbook stating a relationship in prose that no
cell maintains**, which is the object scan 4 was built to find. The
instrument was doing to its own output what it audits workbooks for.

**Falsifier:** a path by which a basis is assigned rather than declared,
or a difference computed across a mismatch.

**Status: SUPPORTED. `FM_016` corrected, not defended.**

---

### FM_019 — the SBA run: one file of three, and P2 splits on a filled plan carrying eight dollar figures

`sba.gov` refuses CONNECT (`SSS_057`), and one file was uploaded:
`Sample_Business_Plan__We_Can_Do_It_Consulting_4.doc`. **It is not one of
the three the order named.** Its author line reads *"Rebecca Champ,
Owner"*, evidence it may be the file called *Rebecca's Plan*, recorded as
evidence rather than asserted as identity. **n = 1.**

| | prediction | outcome |
|---|---|---|
| P1 | blank template | **NOT ADDRESSABLE** — none arrived |
| P2 | filled plan: dollar figures → downward stop resolves | **SPLIT** |
| P3 | upward triple `+ / ABSENT / ABSENT` | **HOLDS**, 2 of 2 cells |
| P4 | blank template upward cells ABSENT | **NOT ADDRESSABLE** |

**P2's antecedent holds and its consequent does not.** Eight dollar
figures exist — `$75`–`$150`, an hourly rate card by role. The downward
stop still does not resolve, because the document **stops before Funding
Request and Financial Projections**, the two sections of the SBA
traditional format that carry computed numbers. In the full text:
`revenue` 0, `forecast` 0, `projection` 0, `cash flow` 0, `break-even` 0,
`loan` 0, `budget` 0. Nothing derives the rates and nothing is derived
from them — no line multiplies a rate by an hour count.

So `unmeasured_span_min` reads `not computable` on a filled business plan
carrying eight dollar figures, which is a sharper result than the empty
case P1 was written for.

**Falsifier:** a computed quantity anywhere in this document.

**Status: P3 SUPPORTED at n=1. P2 SPLIT. P1 and P4 NOT ADDRESSABLE.**

---

### FM_020 — S1a's downward rule has two states and this document needs three

S1a: *"deepest QUANTIFIED quantity — one the org computes, not one that
physically exists."* Two states, and the contrast is **computed** against
**physically-existing-but-uncalculated** — joules that are real whether or
not anyone works them out.

An hourly rate card is neither. It is a number the organisation
**produced and stated**, and it is not derived from anything and nothing
is derived from it. Not a physical quantity nobody calculated; not a
computed one either. A **third state: stated but underived.**

The classification is therefore a judgement the rule does not settle, and
it is not settled here by fiat. `computed` is a declared field
(`FM_013`), so the term declares `computed: False` **with the evidence in
the `by` string** — eight rates stated, nothing derived either direction —
so a reader who would classify it the other way can disagree with the
call without being misled about what is in the document.

Which way it goes matters: `computed: True` makes the downward stop
level −1 and `unmeasured_span_min` 1, and `computed: False` makes the
stop absent and the span not computable. One declared boolean moves the
whole downward arm.

**Falsifier:** a reading of S1a under which a stated tariff is
unambiguously one of the two existing states.

**Status: SUPPORTED. Recorded as a gap in the rule, not patched by adding
a third value to a delivered vocabulary.**

---

### FM_021 — the WO7 screen short-circuited on a reader failure, and `SSS_053` described it as not doing so

The order says *"all criteria recorded per file, no short-circuit"*.
`selection.screen()` returned immediately when `sheetmodel.read()` raised,
recording **one** criterion of six.

`SSS_053` states the screen *"records every criterion rather than stopping
at the first failure"*. That is true of a **criterion** failure and false
of a **reader** failure, and the distinction had never been exercised
because every prior candidate opened.

Repaired: every criterion is emitted, with a third state. Reader-dependent
criteria read `pass: None` — **not evaluated**, which is not a fail:
reporting them as failed would say the file lacks something nobody looked
for. `(e)` takes no reader and is still evaluated. `independence()` skips
a candidate with unevaluated criteria rather than counting it.

**And the screen is workbook-shaped.** Criterion (a) reads cells and (c)
reads a relationship whose operands resolve inside the file; on a prose
document both are category mismatches rather than failures. The screen now
says so in its own output, so a `not eligible` verdict on a document reads
as a statement about the screen's fit and not about the file.

**Falsifier:** a path by which an unevaluated criterion reads as a fail.

**Status: REPAIRED, pinned. `SSS_053`'s sentence was true of the case it
had seen and false of this one.**

---

### FM_022 — the .doc reader was written against the file, and the check that matters is the offset it would otherwise get wrong

`docreader.read_doc()` is built: OLE container → FIB → CLX piece table →
text runs. On this file: table stream `1Table`, `fcClx` 14688, `lcbClx`
21, one piece, compressed, **7711 characters — exactly `ccpText`**, with
205 characters beyond the main document cut and counted.

Every known answer is that file's own number, which is the point:
`SSS_017` and `SSS_041` are both defects a real file exposed that no
fixture could, so the parser was deliberately not written ahead of the
files (`SSS_057`).

**The decisive check is the halving.** A compressed piece stores 8-bit
characters and its `fc` is doubled in the header. A reader taking `fc`
raw lands at 4096 instead of 2048 and returns *something* — plausible
text from the middle of the document — and that something is what makes
the defect invisible. Both halves are asserted: the unhalved offset does
**not** contain the title, the halved one does.

`sheetmodel.read()`'s `.doc` message was stale the moment the parser
landed — it still said text extraction was not built. Corrected to the
true reason: a document is not a workbook, has no cells, no formulas and
no precedent graph, and returning an empty `Workbook` would let a caller
read *"no cells"* as a fact about the file.

**Falsifier:** a `.doc` whose text this reader gets wrong.

**Status: SUPPORTED, pinned against the real file.**

---

### FM_023 — Andrew's plan arrives, and the replication is worth less than it looks

Second upload: `Sample_Business_Plan__Wooden_Grain_Toy_Company.doc`,
author line **"Andrew Robertson, Owner"** — evidence it is the file the
order called *Andrew's Plan*, recorded as evidence. 6188 characters, one
compressed piece. Still no blank template.

It behaves exactly as Rebecca's does: stops at *"How to Sell"*, no
Funding Request, no Financial Projections, `forecast` 0, `projection` 0,
`cash flow` 0, `break-even` 0, `loan` 0, `budget` 0, and every upward
cell `+ / ABSENT / ABSENT`.

**And that replication is one observation, not two.** The two documents
share **26 headings**, including an identical *"Created on December 29,
2016"* — one template filled twice on one day. A structural finding that
holds across both is a finding about the template.

This is `TP_003`'s shared-bias shape in a two-document corpus: agreement
between two readings of one source is not two independent confirmations,
and reporting "2 of 2 filled plans" without the template overlap would
have doubled the apparent evidence.

**Falsifier:** a filled SBA traditional plan not built from this
template.

**Status: SUPPORTED. n = 2 documents, n = 1 template, and the second
number is the one that governs.**

---

### FM_024 — P2 is refuted on both filled plans, and the dollar figures divide by whose quantity they are

Across the two plans: **18 dollar figures, zero computed quantities.**

Andrew's ten divide three ways, and the division is the finding:

| figure | whose quantity | computed here |
|---|---|---|
| `$5`–`$35` by product | the company's own **stated tariff** | no |
| `$35,000`–`$80,000` a year | a **third party's** property (target customer income) | no |
| `$1.2 million` Q2 2012 | an **external statistic** (industry revenues) | no |

Rebecca's eight are all the first kind, an hourly rate card.

So P2's antecedent — *dollar figures exist* — holds twice over, and its
consequent fails twice: `unmeasured_span_min` is `not computable` on both.
Nothing in either document derives a figure or derives anything from one;
no line multiplies a rate by an hour count or a price by a volume.

**This sharpens `FM_020`.** S1a's axis is *computed* against *physically
existing but uncalculated*, and none of these three kinds is either. The
second and third add something the rate card alone did not show: a
quantity can be **about someone else entirely** — a customer's income, an
industry's revenue — and still sit in the plan's own downward arm as a
number nobody here computed. The question S1a's floor turns on is not
only *was it calculated* but *whose quantity is it*.

Per `FM_023`, this is one template and the count of 18 is not 18
independent observations.

**Falsifier:** a computed quantity in either document.

**Status: P2 REFUTED on both. `FM_020`'s gap widened, still not patched
by adding values to a delivered vocabulary.**

---

### FM_025 — across four terms and three sources, not one upward cell carries a magnitude or a unit

| | upward cells |
|---|---|
| `measured` | **0** |
| `derived` | **0** |
| `ASSERTED` | 8 |
| `ABSENT` | 3 |

| field | ABSENT on | of |
|---|---|---|
| sign | 5 | 11 |
| **magnitude** | **11** | **11** |
| **unit** | **11** | **11** |

Eleven upward cells across a published UN emissions calculator, a
repo-internal scan reading, and two SBA business plans. **Six carry a
stated direction. None carries a size. None carries a unit.**

P1 holds (11 soft, 0 hard), P3 holds (6 cells split rather than failing
together), P4 holds (no magnitude anywhere).

The sources are three, not four, since `FM_023` collapses the two plans
to one template — and one of the three is this repository, which is not
an independent observer of its own claims.

**What this does not say:** that the documents are uninformative. Both
plans carry prices, market descriptions and a named growth strategy. The
claim is about the **upward arm only** — the relation between what the
organisation does and the goal it states — and there the format is
uniform: a direction, and nothing else.

**Falsifier:** an upward cell carrying a magnitude, anywhere.

**Status: SUPPORTED, at n = 3 sources with the dependence stated.**

---

### FM_026 — a blank template arrives and it is not the one the predictions were registered against

Delivered as pasted text, landed verbatim at
`sources/blank_template_pasted.md`. Nine sections plus a Tips section.

**It is not the SBA blank traditional template.** Measured rather than
asserted: **1 of its 9 section names** appears anywhere in the two filled
SBA plans (`Executive Summary`), and of twelve SBA headings only three
appear here — two of them as incidental phrases inside other sections
(`market research data / surveys` in the Appendix, `Marketing & Sales:
30%` in Use of Funds).

So **P1, P3 and P4 remain NOT ADDRESSABLE for the file they were
registered against**, and what follows is a new candidate scored on its
own.

**Provenance asymmetry, recorded.** The two filled plans arrived as
`.doc` files with a container, a piece table, an author line and a
creation date. This arrived as text with none of those — no author, no
date, no file, nothing to check a claim about its origin against. A
weaker artifact in a way nothing in its content shows.

**Falsifier:** the SBA blank template, which would make the registered
comparison available.

**Status: SUPPORTED. The registered predictions are still unaddressed.**

---

### FM_027 — a fourth kind of number: an example of a quantity

`FM_024` found three kinds of dollar figure, divided by whose quantity
they are. This template adds a fourth, and it is unanimous:

**All ten dollar figures are inside an `(e.g., ...)`** — `$5 billion`,
`$1M`, `$500,000`, `$10 Billion`, `$2 Billion`, `$50 Million`,
`$200,000`, `$150,000`, `$100,000`, `$50,000` — plus two slot markers
`$[Price]`.

| kind | example | whose | computed |
|---|---|---|---|
| stated tariff | `$5`–`$35` by product | the company's | no |
| third party's property | customer income `$35,000`–`$80,000` | someone else's | no |
| external statistic | industry revenue `$1.2M` | nobody's in particular | no |
| **illustrative example** | `(e.g., $10 Billion)` TAM | **nobody's** | no |

The fourth is the emptiest: not the organisation's, not a third party's,
not an external fact — **an example of the shape a quantity would take**,
belonging to no one and computed by no one.

**And the template names nine computed quantities without computing
one:** Revenue Projections, Cash Flow Statement, Balance Sheet,
Break-even Analysis, Net Profit, COGS, TAM, SAM, SOM all appear as
section content. **Naming a quantity and computing it are different
acts**, and this document performs the first nine times.

That is the sharpest form of `FM_020`'s gap so far: S1a's floor asks for
a quantity the organisation computes, and a document can be *dense* in
quantity names while computing nothing.

**Falsifier:** a dollar figure in this template outside an example or a
slot.

**Status: SUPPORTED, 10 of 10.**

---

### FM_028 — a blank template has no term, so "one term, one grid" has two readings and they disagree on P4

S1 is *one term, one grid*. The filled plans had a term — the consulting
engagement, the toy sold. **A blank template has a slot where the term
goes.**

| reading | level 0 | grid | P4 |
|---|---|---|---|
| term = the business activity (what WO8 uses for the filled plans) | a **slot**, unfillable | **not constructible** | vacuous |
| term = **the document itself** | the plan as an artifact | constructible, and built | **REFUTED** |

Under the second reading the template **does** state goals, at section
level: *"Goal is to capture the reader's attention and summarize the
entire plan"* (§1) and *"Show the business model is profitable and viable
for the next 3–5 years"* (§8). Those are `ASSERTED`, not `ABSENT`, so
P4's *"document does not reach a level where a goal could be stated"* is
false of this document.

Under the first reading there is no grid to have cells in, and P4 is
neither true nor false.

**Both readings are stated in the term file and neither is picked.** The
grid built is the second, because it is the one that is constructible;
that is a choice about what can be read, not a claim that the first
reading is wrong.

**Falsifier:** a blank template carrying a term at level 0.

**Status: SUPPORTED. P4 REFUTED under the constructible reading, vacuous
under the other.**

---

### FM_029 — P1's third clause is refuted, and refuted in the interesting direction

P1: *zero quantified downward stops, `unmeasured_span_min`
uninterpretable, `enumeration_basis` UNREAD **by construction**.*

| clause | outcome |
|---|---|
| zero quantified downward stops | **HOLDS** |
| `unmeasured_span_min` uninterpretable | **HOLDS** — `not computable` |
| `enumeration_basis` UNREAD by construction | **REFUTED** |

The basis is `document_named`, and correctly: the template **names its
own sections**, which is exactly what `document_named` means. *"By
construction"* had it backwards — **a blank form is the most enumerable
kind of document there is**, because its structure is all it has. The
filled plans' downward levels needed a physical chain read off them; the
template's needed nothing but its own table of contents.

So the least informative document in the corpus has the **best** level
enumeration in it, and the two facts are the same fact: nothing but
structure.

**Falsifier:** a blank template whose level set cannot be enumerated from
its own sections.

**Status: P1 two clauses SUPPORTED, third REFUTED.**

---

### FM_030 — the only clock in any of the three business documents is in the blank one

| document | clocks at any level |
|---|---|
| We Can Do It Consulting (filled) | **none** |
| Wooden Grain Toy Company (filled) | **none** |
| the blank template | **one** — 4.0 years at level +2 |

The template's §8 asks for a forecast over *"the next 3–5 years"*. That
is a stated horizon, and it is the only time constant anywhere in the
three.

Neither filled plan carries one — but they are a **different template**
(`FM_026`), one whose sections stop before Financial Projections, so this
is not evidence that filling a form drops its horizon. What it does show
is that a horizon is cheap to state and appears where a form asks for it.

The clock is recorded as the stated range's midpoint with the range in
the basis string, since *3–5 years* is the quantity and 4.0 is a reading
of it.

**Falsifier:** a clock in either filled plan.

**Status: SUPPORTED, and explicitly not a claim about what filling does.**

---

### FM_031 — across four sources the upward format has not varied once

Fourteen upward cells now, across a published UN emissions calculator, a
repo-internal scan reading, the SBA filled template, and this blank one.

| | cells |
|---|---|
| `measured` | **0** |
| `derived` | **0** |
| `ASSERTED` | 10 |
| `ABSENT` | 4 |

| field | ABSENT on | of |
|---|---|---|
| sign | 6 | 14 |
| **magnitude** | **14** | **14** |
| **unit** | **14** | **14** |

Eight cells state a direction. **None states a size. None states a
unit.** P1, P3 and P4 hold at every scale tested.

**What the blank template adds is the strongest single case**, because
its purpose statements are what a form *asks for* rather than what one
company wrote — and they have the same shape. The registered reading was
*filled plan purpose statements carry no more information than the blank
form*; across two different templates that is what the format shows,
while the matched within-template comparison it named still needs the SBA
blank.

Sources are four and independence is less: two of them are documents this
repository did not write and did not choose the format of, one is the
repository itself, and the SBA pair collapses to one template
(`FM_023`).

**Falsifier:** one upward cell, anywhere, carrying a magnitude.

**Status: SUPPORTED at n = 4 sources, with the dependence stated.**

---

### FM_032 — the paste could not be verified against the upload, and the reader is too partial to serve as the check

A PDF arrived with this document (`Company Research - Palo Alto
Networks.docx`, converted November 2024), and the text arrived separately
as a paste. Cross-checking one against the other is the obvious move and
**it fails**.

A stdlib extraction — 28 of 29 streams inflate — recovers **6 of 19**
distinctive strings from the paste (`Fortinet`, `Trent Weber`, `Kirk
Skeeles`, `Economic Logic`, `Published Values`, `Real Values`) and **0 of
the 4 figures** (`374.83`, `122.04`, `7.52`, `227.7`). The stated author
in the paste does not appear in the extraction either; the PDF's own
metadata names a different person, which is an ordinary
converted-by-someone-else pattern and is not resolved here.

**Why the extraction is that partial, and why it cannot be repaired by
trying harder at the same level:** PDF splits text runs for kerning
inside `TJ` arrays. This file literally contains `[($)-0.6 (1)]TJ` — the
`$` and the digit as separate strings with an offset between them — so
concatenating string literals joins fragments across unrelated
positions. A first pass produced `$754`, `$32`, `$00`; **those are
artifacts, not figures in the document**, and they were never reported as
content. Some of the extract comes back as font/CMap bytes rather than
text at all.

So the document enters the corpus **on the paste alone**, with weaker
provenance than the two `.doc` files, which had a container, a piece
table, an author line and a creation date each. Recorded rather than
worked around: a naive PDF extractor would have produced numbers that
look like data and are wrong, with nothing in the output showing it —
`SSS_046`'s forbidden substitution in a third format.

**Falsifier:** a `TJ`-aware extractor recovering the four figures, which
would turn this from an unverified paste into a checked one.

**Status: SUPPORTED. The cross-check was run and did not confirm.**

---

### FM_033 — the first document in the corpus whose purpose is stated only by where it is filed

Every prior source states a purpose. The UNFCCC calculator states one in
its Disclaimer, both business plans state mission statements, the blank
template states what each section is for. **This one states none.**

| level | goal | basis | sign | magnitude | unit |
|---|---|---|---|---|---|
| +1 | not stated | **ABSENT** | ABSENT | ABSENT | ABSENT |
| +2 | not stated | **ABSENT** | ABSENT | ABSENT | ABSENT |

`upward_stop` is **ABSENT**: no positive level carries a stated artifact,
so the arm stops before it starts. First time in this corpus.

The document is not purposeless — it is career-preparation material, and
that use is real. But **the use is a property of where the document is
filed**, not of anything in the text: nothing between "Prepared by" and
the alumni list says what the brief is for. Its goal lives in the
containing site, and a copy of the text carries none of it.

This is `uninstrumented`'s territory reached from the fold matrix:
the register's mechanism 13 candidate — *recorded, archived, and filed
under a category that isn't evidence* — describes filing that changes what
a document counts as. Here filing is the only thing that states what the
document is **for**, and the fold matrix reads the text.

**Falsifier:** a purpose statement in the document.

**Status: SUPPORTED. The first ABSENT upward arm in the corpus.**

---

### FM_034 — a downward arm made entirely of a third party's figures, and the one relation it states has a sign and no size

`FM_024` divided dollar figures by whose quantity they are and found a
third-party category as one entry among several. Here it is **the whole
arm**:

| figure | about | computed by the author | source named |
|---|---|---|---|
| Stock Price `$374.83` | a third party | no | no |
| Market Cap `$122.04B` | a third party | no | no |
| Revenue 2023 `$7.52B` | a third party | no | no |
| Net Income 2023 `$227.7M` | a third party | no | no |

Four figures, none computed, **none with a source named**, and no
relation stated between any two of them.

**The one economic relation the document does state carries a sign and no
size**: support and consulting *"carry the highest margins"*. A
comparative claim about someone else's economics in the now-familiar
`+ / ABSENT / ABSENT` shape.

And the arithmetic the document declines to do is available from its own
four numbers: **net margin 3.03%**, price/sales 16.2, price/earnings 536,
implied share count 326M. The margin is the one it comes closest to
discussing — it claims consulting margins are highest and states no
margin anywhere — so the only margin computable from its own figures is
the aggregate it does not mention.

Those four ratios are computed **here**, from the document's numbers, and
are not the document's claims. Nothing checks whether its four figures
are correct: the sources are not named, and egress is refused.

**Falsifier:** a stated relation between any two of the four figures.

**Status: SUPPORTED.**


---

### FM_035 — sixteen upward cells, five sources, still no magnitude and no unit

| | cells |
|---|---|
| `measured` | **0** |
| `derived` | **0** |
| `ASSERTED` | 10 |
| `ABSENT` | 6 |

| field | ABSENT on | of |
|---|---|---|
| sign | 8 | 16 |
| **magnitude** | **16** | **16** |
| **unit** | **16** | **16** |

Five sources now: a published UN emissions calculator, a repo-internal
scan reading, the SBA filled template, a blank business-plan template,
and a third-party company research brief. Eight cells state a direction;
**none states a size, none states a unit.**

The company brief is the first to add cells where even the **direction**
is absent (`FM_033`), so the ABSENT column grew where every previous
source grew the ASSERTED one. That widens what the corpus covers without
moving P4: an upward arm can be empty at every level, and it still never
carries a magnitude.

**What is not claimed.** These are five sources of very different
provenance and independence: two arrived as parsed files with containers,
three as pasted text; one is this repository; the SBA pair is one
template (`FM_023`); and one is unverified against its own upload
(`FM_032`). The count of 16 is not 16 independent observations, and the
uniformity is a statement about the *format* of purpose claims in
documents of this kind, not a rate estimated from a sample.

**Falsifier:** one upward cell, anywhere, carrying a magnitude.

**Status: SUPPORTED at n = 5 sources, with the dependence stated.**

---

# fold_register.py — delivered module, landed verbatim

`FM_036..FM_044`. The module is imported by `register_audit.py` and
edited by nothing.

---

### FM_036 — the refusal is real, and it is the rarest thing in the module

`scan()` returns `score: None`, every one of the ten grid cells is
`UNFILLED`, and the verdict string says *"NOT SCORABLE -- grid unfilled.
Absence is the reading."* `grid_for` on a term not in the register
returns `None` rather than an empty grid, so a caller cannot mistake
"not a folded term" for "a folded term with nothing filled in".

`domain-ledger/anchor.py`'s selftest asserts *"no composite emitted"* and
`ledger.py` returns four uncombined ratios; this is the same discipline
one level up, on a scanner, where the pull toward a headline number is
strongest. It is designed in rather than found in audit.

**Falsifier:** any input for which `score` is not `None`.

**Status: SUPPORTED.**

---

### FM_037 — `cells_filled` is a literal, so the field cannot report anything else

    "cells_filled": 0,
    "cells_unfilled": total,

`0` is written into the return, not derived from the grid, and
`cells_unfilled` is `cells_total` by construction — checked across three
inputs, identical every time. Nothing in the module can ever fill a
cell, so the counter is `CONSTANT_SILENT`: it reports the design rather
than the data, and the day a filling path exists it will keep reporting
0 until someone notices.

One line: count the non-`None` cells across the emitted grids. The
number is 0 today and the field becomes a measurement instead of a
restatement.

**Falsifier:** an input returning a non-zero `cells_filled`.

**Status: SUPPORTED — one line, and it is the field the design turns on.**

---

### FM_038 — `counter_case` separates perfectly by who named the term

    kavik      counter_case filled     4
    kavik      counter_case UNFILLED   1
    candidate  counter_case UNFILLED  12

**Zero of twelve candidates carry a counter-case; four of five
kavik-sourced terms do.** Total separation.

Two readings and the register cannot distinguish them: the kavik terms
arrived with their counter-cases attached because they were argued
before they were listed, or a counter-case is easier to find for a term
someone has already thought about. Either way, the column reads as a
property of **provenance** rather than of the term, and a reader
scanning for which terms have evidence behind them is reading the
`source` column with extra steps.

The five with a filled cell are the four the register was clearly built
around — money's Ford demonstration stage, regulation's self-builder,
optimization's absent single-objective maximizer, efficiency's
tree-replacement comparison. Those are the sharpest content in the file.

**Falsifier:** one candidate term with a counter-case, which would break
the separation and make the column about terms again.

**Status: SUPPORTED, and it is the strongest structural finding here.**

---

### FM_039 — 73% of hits come from the alias layer, and that is where the sense-blindness is

    document                              direct  alias  alias share
    palo_alto_company_profile_pasted.md        3      1    25%
    blank_template_pasted.md                   2      9    82%
    CLAUDE.md                                 81    221    73%

A register key is a word that means what the register says. An alias is
a word list deciding word sense, which is `nonidentity-census` T1-1's
measured failure, and on this repository the top alias hits are all
other senses:

    cost      -> money       66   "NOTE ON COST -- use dissipation, cost
                                   imports a pricing model"  (a passage
                                   arguing AGAINST the folded use)
    protocol  -> procedure   49   PROTOCOL.md, REFUTATION_PROTOCOL
    budget    -> money       42   artifact budget, compute budget, token
                                   budget, reader budget
    standard  -> regulation  19   "standard library", "Standard RAG"
    qualified -> merit        7   a reasoning-gate verdict code
    best      -> merit        7   "the SIGN of the best combination"

`re.findall(r"[A-Za-z]+")` is the right tokenizer — no substring bleed,
so `UNI_009`'s `lean`/`clean` failure cannot happen here. What survives
is sense, which no word list reaches.

**Falsifier:** a corpus where the alias share is low and the direct hits
carry the load.

**Status: SUPPORTED.**

---

### FM_040 — the schema has no cell for "the word appeared and is not folded here"

Every hit on the two real outside documents was hand-checked — fifteen
of fifteen, printed in the audit output so the reading is re-checkable
rather than asserted.

One is a counter-instance by the register's **own definition**.
`blank_template_pasted.md` L87:

    Sales Process: [Steps converting lead to customer
                    (e.g., Demo -> Proposal -> Close)]

The register says `procedure` substitutes for *doing*. Here the doing is
enumerated on the same line. The word is present and the fold is not.

`folded_terms_found` asserts foldedness by naming, and there is no state
for a hit that is a counter-instance. That is the absent-vs-known-negative
repair this repository has now recorded some fifteen times, arriving at
the level of the **hit** rather than the cell — and it matters more here,
because the register's whole claim is about instances.

**Falsifier:** a scan output distinguishing a candidate hit from a
checked non-fold.

**Status: SUPPORTED, with the instance printed.**

---

### FM_041 — the occurrence cap is silent

`scan()` stops appending at twelve lines per term. On `CLAUDE.md` six
terms exceed it:

    money        real  111   reported 12
    procedure    real   69   reported 12
    capacity     real   27   reported 12
    regulation   real   24   reported 12
    merit        real   15   reported 12

Nothing in the returned dict says a list was cut — no count, no marker,
no `truncated` flag, asserted in the selftest. A reader taking
`len(occurrences[k])` as a frequency is off by an order of magnitude on
the most common term and has no way to tell from the output.

**Falsifier:** a marker in the output when the cap binds.

**Status: SUPPORTED.**

---

### FM_042 — two CLI paths raise where the third reports

    --grid efficiency   rc=0
    --grid zzz          rc=0   {"error": "not in register"}
    --grid              rc=1   IndexError: list index out of range
    nosuch.txt          rc=1   FileNotFoundError

`--grid` with an unknown term is handled and returns a stated error;
`--grid` with **no** term indexes `argv[2]` without checking, and a
missing file opens without checking. Same function, three arguments,
two of them uncaught.

`closure-cost` `CC_004` and `constraint-assembly` `CA_005` are the same
finding in two sibling tools, which makes this the third instance of an
unguarded CLI index in this family.

**Falsifier:** either path returning a stated error instead of a
traceback.

**Status: SUPPORTED.**

---

### FM_043 — one alias is dead, and four fields are carried without being read

`ALIASES["quality"] = "quality"` can never fire: the lookup is
`word if word in REGISTER else ALIASES.get(word)`, and `quality` is a
register key, so the first branch always takes it.

Separately, `sign_storage`, `residual_tell`, `counter_case`, `source`
and `substitutes_for` are **carried into the output and branched on by
nothing** — no comparison, no sort, no filter. Read from the AST rather
than by regex, because a first version matched the `<-` inside the
`--list` format string and reported `substitutes_for` as branched on:
an operator inside a string literal is not an operator. The detector is
null-tested against a constructed real branch so it is not
`CONSTANT_SILENT`.

Carrying is not a defect — the fields are for the reader. It is worth
knowing that `sign_storage`, whose three values (`signed`,
`unsigned_positive`, `unsigned_negative`) are the register's only
ordinal, is used by no code path, and that **15 of 17 terms share one
value**.

**Falsifier:** a code path that branches on any of the five.

**Status: SUPPORTED.**

---

### FM_044 — the register is `category-weld`'s corpus in a different schema, and the term two folders have asked for is still absent

`category-weld/` MECHANISM_09 is *two or more independent quantities
welded into one term*, and its `welds/` directory holds exactly two
entries, both from policy/economics — which is why `UNI_002`'s
cross-field check has stayed open there.

`fold_register.REGISTER`'s `substitutes_for` field **is** a component
list: `safety <- hazard x exposure x consequence`,
`risk <- probability x magnitude`, `resources <- a stock and a flow,
welded` — the last says the word. Seventeen terms across engineering,
governance, hiring, ecology and machine learning, which is the
cross-field corpus that folder lacks.

The two schemas do not merge as they stand: `welds/*.json` carries
`divergences` with per-case readings and a `max_spread` readout, and the
register carries no case data at all. What transfers is the term list.

**And the term two folders have asked for is still missing.**
`presented-binary` B5 and `moral-decomposer` `MD_004` both point at
`welds/a_few.json`; `a few` is in neither register.

**Falsifier:** a `welds/` entry generated from a register row, or an
`a_few` entry in either.

**Status: SUPPORTED — the corpus exists, the join does not.**
