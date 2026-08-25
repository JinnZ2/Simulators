# CLAIM TABLE — sheet-structure-scan

Claims from building the two scans. `SOURCE_DROP.md` is untouched.

**REFUTATION PROTOCOL.** The parameters are frozen estimates and the
constraints are the claim. A check that fails updates the claim, not the
default — except where a default was chosen for a stated reason and the
reason is what failed, in which case both move and the old one stays
recorded (`SSS_002` is that case).

---

### SSS_001 — the one-reader budget is unspent, and the reason is not frugality

`.xlsx` is a zip of XML. Formulas live in `xl/worksheets/sheetN.xml` as
`<f>` elements, so `zipfile` and `xml.etree` reach everything both scans
need, and the declared slot stays open.

The load-bearing half: **both scans are about the formula layer.**
Precedent depth and constant-versus-derived are properties of formulas,
and the common reader's value-only mode drops them. Reading the XML
directly means the layer under test cannot be discarded by the reader
that was supposed to deliver it. `sheetmodel.read()` raises on any other
extension with that sentence rather than widening itself.

**Falsifier:** a formula construct the stdlib path cannot resolve that
the reader can — the budget is then spent for a reason, not for
convenience. Named ranges are already the candidate: they record
`PRECEDENTS_UNRESOLVED` here.

**Status: SUPPORTED for .xlsx. UNVERIFIED for .xls, .ods, Sheets.**

---

### SSS_002 — the neighborhood shape was refuted by the fixture, and the radius was not the problem

The first build used a square block of radius 2. On this folder's own
demo it reports `variance_sibling` **absent** for `Inputs!B2`, a cell in
a well-formed six-column table whose `sd` column sits three columns away.

Radius 6 reaches it. It also reaches the record above and below, so the
repair trades a false absence for a false presence — and §2 of `SPEC.md`
argues false presence is the costlier direction, because it removes a row
from a report whose subject is what is missing.

The shape is the repair: the whole of the flagged cell's row (one
record), its column within ±radius rows, and the label-row cell above
every column the row touched. A design decision overturned by a fixture,
with the fixture checked in and the first version recorded rather than
deleted.

**Falsifier:** a workbook where the cross reports a companion absent that
a reader finds inside the block.

**Status: SUPPORTED on the fixture. The shape has not met a real sheet.**

---

### SSS_003 — the flag set decides the report more than the scan does

Measured, not asserted, and pinned in the selftest.

| flag source | rows | carry an absence | label cells | strays outside a table | values in a table |
|---|---|---|---|---|---|
| five-cell list | 5 | 4 | 0 | 1 | 3 |
| `--all` | 38 | 23 | 13 | 2 | 8 |

Under `--all`, **15 of 23 absence rows are not values in a table**, and
the largest class is label cells: a header reading `unit price (USD)` is
not itself under a header and its own text is excluded from its own
neighborhood, so it reports `unit` absent.

**This is the argument for CHOICE 1.** Scan two begins *"for every
flagged cell"*, scan one is not in the delivery, and a tool that supplied
its own flagging rule would be putting a framing in the operator's mouth
and then ranking it — which is the one thing the no-labelling constraint
exists to prevent. So the flag set is an input and running without one is
refused; `--all` prints its own provenance into the report header.

**Falsifier:** a real workbook where `--all` and a curated flag list
produce the same composition — the refusal then buys nothing.

**Status: SUPPORTED on the fixture.**

---

### SSS_004 — every terminal ranks 0, and terminals are the cells people quote

`rank = deps × ddepth`. A terminal has no dependents, so the product is
zero whatever its own precedent depth. On the demo, `Summary!B2` sits at
the end of a four-deep chain and ties for last with an unused stray
constant.

This is the delivered formula behaving as specified — *"the sites that
propagate furthest sort to the top"* — and a terminal propagates nowhere.
But near the bottom of a sheet **propagation and consequence run
opposite**, and the reported figure is usually a terminal.

Not repaired. `pdepth` is a column, so the tie is breakable by the
operator, and changing the sort would make the ranking a claim about
importance, which is exactly what the tool is barred from making.

**Falsifier:** a workbook where the top of the rank column is not where a
reader would start.

**Status: SUPPORTED. Stated, not fixed.**

---

### SSS_005 — the row axis collides once per record, not once per table

`widget` and `gadget` are the same collision listed twice, at equal rank,
because every row of the demo table has the same construction pattern. A
five-hundred-row table produces five hundred identical group rows.

The cheap mitigation — collapse row-axis groups whose occurrence
signature (spans, depths, constructions) is identical — changes the
delivered grouping rule, so it is named and not built.

**Falsifier:** a real workbook whose row-axis collisions differ per
record, which would make the collapse lossy.

**Status: SUPPORTED.**

---

### SSS_006 — the normalization choice loses a true collision, and the fixture carries the case

Parentheticals are kept, so `unit price (USD)` on `Inputs` and
`unit price` on `Model` are two groups of one and neither is listed —
although they are the same quantity at two constructions (`2c` at depth
`{0}` against `2d` at depth `{1}`), which is precisely what scan three is
for.

Stripping parentheticals lists it, and also merges `revenue (net)` with
`revenue (gross)`. Deciding that a unit annotation does not change what a
label names is a judgement about the sheet, so the default is the one
that under-reports and the choice is the operator's.

**Falsifier:** a corpus where parenthetical annotations are
overwhelmingly units rather than qualifiers, which would make the other
default the better one.

**Status: SUPPORTED, and the cost is on the record rather than in the
footnotes.**

---

### SSS_007 — three states per companion, and a fourth column for what the search could not cover

`ABSENT` / `PRESENT` / `NOT_SEARCHED`, plus an `unsearched` column
carrying `N`, `S`, `no-col-label`, `no-row-label`, `is-label`.

`NOT_SEARCHED` fires when the pattern file registers nothing for a kind.
Without it, an empty pattern list reads `ABSENT` on every cell and the
report is about the pattern file rather than the sheet. `no-col-label`
separates an absence measured with a header from one measured without.

This is the absent-versus-known-negative repair, which this repository
has now recorded more than a dozen times and implemented at construction
only a handful — where it is free. Cells with nothing absent stay in the
table for the same reason: dropping them makes the denominator invisible,
and a report of absences with no denominator cannot be told from a report
of a short flag list.

**Falsifier:** a state the three values conflate that an operator needs
apart.

**Status: SUPPORTED.**

---

### SSS_008 — the no-labelling constraint is enforced and null-tested, and its limit is one paraphrase

`no_severity.py` screens 78 words across severity (*error, critical,
invalid, risk, flaw*) and interpretation (*should, must, indicates,
likely, fix, better*), runs over every emitted table, and returns a
non-zero exit if one appears. Null-tested in both directions: known-null
text passes, a planted word of each class is caught, and `terror`,
`mustard` and `bustle` are checked against substring bleed — the failure
recorded here under `UNI_009`.

**A keyword screen is stepped around by any paraphrase.** *"This cell is
wrong"* is caught; *"this cell will not survive contact with the audit"*
is not. Stated at the top of that file rather than the bottom, alongside
`DF_010` and `ACL_017` which are the same limit on other substrates. What
the screen buys is the fluent failure — reaching for the ordinary
vocabulary of grading without noticing — which is the one that happens.

Scope: the constraint is on what the tool says about a site on a sheet,
not on what the spec says about the tool. A design document that could
not call its own neighborhood shape wrong could not have recorded
`SSS_002`.

**Falsifier:** a graded reading reaching an emitted table in words the
screen does not hold.

**Status: SUPPORTED for the vocabulary. The paraphrase channel is open by
construction.**

---

### SSS_009 — a defect in the reference parser that reading would not have caught

`=LOG10(A1)` returned `{A1, LOG1}`. The pattern refuses a reference
followed by `(`, so `LOG10` fails the lookahead — and the engine then
backtracks to `LOG1`, which is followed by `0` and passes. A function
name entered the precedent graph as a cell.

Caught by a fixed-in-advance selftest case, not by reading the regex.
Repaired with a second lookahead forbidding a following identifier
character, and the case is kept.

It matters beyond tidiness: a phantom precedent inflates `pdepth` on
every cell downstream of the formula and adds a dependent to a cell that
does not exist, so **the rank column would have been wrong for a reason
invisible in the output.**

**Falsifier:** another function-name shape that survives both lookaheads.

**Status: REPAIRED, case pinned.**

---

### SSS_010 — nothing here has met a real workbook

Every number in `RESULTS.md` is a property of the tool on a fixture
written by the same hand that wrote the scans. Falsifiers F1–F4 in
`SPEC.md` §6 all require a real sheet.

The nearest sibling is `membership-probe`, whose LIMITS section names the
same weakness about its own selftest and states the right asymmetry:
**passing is weaker evidence than failing.** Three of the claims above
(`SSS_002`, `SSS_003`, `SSS_009`) are failures the fixture produced, so
the fixture has done the thing a fixture can do. It has not done the
other thing.

**Falsifier:** run it on a workbook nobody here built.

**Status: UNVERIFIED, and it is the cheapest item in the folder.**

---

## Claims from the EPA targets, before the data

Three workbooks were named as targets. **None has been read**: this
session's egress gateway answers 403 to CONNECT for `www.epa.gov`, logged
2026-08-25T15:14:12Z–15:14:13Z with DNS resolving normally. Details and
the pre-registration in [`targets/EPA.md`](targets/EPA.md).

---

### SSS_011 — scan three listed every shared header on a difference in table height

Two flat sheets carrying the same headers over twelve and nine rows
returned constructions `12c` and `9c`. Those differ, so the group was
listed: **five column collisions on a fixture where nothing collides.**

The Emission Factors Hub is exactly that shape — many sheets sharing
headers over different numbers of rows — so the scan would have lit up on
it, with a rank beside each row, and read as a finding. The workbook that
was handed over as a known-answer case found the defect before it
arrived.

`CHOICE 6` was over-specified against its own source. The delivery asks
whether the cells are constants **versus** derived; *whether* is a set,
not a count. The listing decision now takes the kind set (`c` / `d` /
`c+d`) and the counts stay in the printed column, so nine constants and
one formula still reads differently from ten constants — which was the
argument for composition over a majority vote in the first place.

**Falsifier:** a workbook where two occurrences share a kind set and a
depth set and a reader still judges them differently constructed.

**Status: REPAIRED. Both directions pinned — differing heights list
nothing; a mixed column still separates from a pure one.**

---

### SSS_012 — a share passed on an empty denominator, in the check written to test the Hub

`EFH-P4` is `listed_col_share < 0.10`. On a single-sheet workbook no
label can appear twice, the denominator is zero, and the check was
satisfied by a result set with nothing in it.

This is `PCH_001` reached a second time, in a different folder, by a
different route: a predicate that returns a pass on an absence. It was
found by running the criterion against a shaped fixture, not by reading
it — which is the same way `SSS_009` was found.

Fixed: every share names its denominator field, and an empty denominator
returns `NOT_DETERMINABLE` rather than `HELD`. The synthetic hub fixture
was widened to two sheets so the check is exercised, and the one-sheet
version is kept as the case that pins the refusal.

**Falsifier:** another readout in `PREDICTIONS` whose zero state and
whose empty state are the same value.

**Status: REPAIRED, both branches pinned.**

---

### SSS_013 — the pair is the test, and neither workbook alone is

A Hub run alone cannot separate *the scan works and the Hub is flat* from
*the scan reports everything flat*. The two hypotheses predict the same
output.

The Local GHG Inventory Tool is the discriminator. `--selftest` shows the
criterion can do the separation on synthetic shapes — flat holds 6 of 6
`efh` and fails `LOC-P1`/`LOC-P2`; chain holds 4 of 4 `local` and fails
`EFH-P1`/`EFH-P2` — but a criterion that separates two workbooks written
here has not been shown to separate two written by the EPA.

So `epa_check.py` scores one target at a time and ends every report by
saying it is one arm. The instrument is not called until both are in.

**Falsifier:** both real workbooks returning the same profile. That
result is about the scan, not about either workbook, and it is the
outcome the Hub was offered to produce if the scan is broken.

**Status: SPECIFIED. Neither arm has been run.**

---

### SSS_014 — the unit list was widened before the data, toward a prediction, and the direction is on the record

`patterns.json` was edited on 2026-08-25 before any target was opened:
the loose generic parenthetical rule was **removed** (it fired on
`(see note 3)`, the costly direction) and energy and fuel units were
**added** — `mmBtu`, `therm`, `scf`, `MWh`, `short ton`, `CO2e`, and a
slash-parenthetical rule that catches `(kg CO2/mmBtu)`.

Widening the unit list makes `EFH-P3a` — *unit present* — easier to
satisfy, and `EFH-P3a` is a prediction made here. That is tuning toward
one's own expectation and it is recorded rather than left implicit, in
the pattern file's `_note` and here.

What limits the damage is structural, not good intentions: **no edit to
the unit list can make the variance or sample-size patterns fire.** So
the differential — unit present while variance and sample size are
absent, which is the user's own description of the Hub's design — is not
reachable by editing that file. Ten hand-set cases are pinned in the
selftest, and six of the ten are negatives.

**Falsifier:** a real Hub sheet where the widened list reports `unit`
present on a header carrying no unit.

**Status: SUPPORTED as a disclosure. The tuning is real and bounded.**
