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
