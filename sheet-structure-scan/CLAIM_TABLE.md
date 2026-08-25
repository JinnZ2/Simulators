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
