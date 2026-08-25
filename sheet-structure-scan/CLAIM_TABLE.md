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

Five workbooks are named as targets across three publishers. **None has
been read.** Details and the pre-registration in
[`targets/TARGETS.md`](targets/TARGETS.md).

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

---

### SSS_015 — the egress denial is an allowlist, so substituting a publisher does not help

Four target hosts, three publishers, all 403 at CONNECT:

| host | result |
|---|---|
| `www.epa.gov` | 403 to CONNECT, 15:14:12Z |
| `unfccc.int` | 403 to CONNECT, 15:40:03Z |
| `www.theclimateregistry.org` | 403 to CONNECT, 15:40:03Z |
| `example.com` | 403 to CONNECT, 15:40:15Z |
| `github.com` | **400 from the origin** |
| `raw.githubusercontent.com` | **301 from the origin** |

DNS resolves for all six. **`github.com` returning a real HTTP status
while `example.com` does not is what separates an allowlist from a
denylist aimed at a publisher.** The inference that a different host
would not be covered by an `epa.gov` denial is reasonable, was testable,
was tested, and does not hold here: `unfccc.int` and
`theclimateregistry.org` were denied for the same reason as the first
host, not for a reason about them.

What this rules out is a strategy, not just two files: no public
workbook publisher is reachable from this session, so there is no third
host worth trying. Fetching the same bytes from a mirror on an allowed
host is available and was **not** done — that is circumventing the
denial rather than complying with it, and it is the operator's call.

**Falsifier:** any non-allowlisted host returning a status from the
origin.

**Status: SUPPORTED. Four attempts, no retries, no alternate route.**

---

### SSS_016 — three arms are registered for the discriminator, and each is required to discriminate

`local`, `unfccc` and `tcr` all serve the live-calculator arm. They are
registered separately rather than merged, because **the predictions that
follow from "a live calculator" are not the predictions that follow from
a described module structure.**

`P1`–`P3` — derived share, rank-zero share, max precedent depth — are
registered for all three, since each follows from the one structural
fact stated about each workbook.

`P4`, the cross-module collision, is registered **only for `local`**,
where the community and government-operations modules were named in
advance. For `unfccc` and `tcr` it is explicitly not registered and the
report prints why: a collision prediction read off a workbook's own
sheet list *after* opening it is a post-hoc threshold wearing a
prediction's clothes.

The selftest asserts per arm that the chain shape holds every one of its
predictions and the flat shape fails its first two. Asserted per arm and
not once, because **registering a second discriminator that does not
discriminate adds a name and no evidence** — which is the failure mode
`SSS_013` exists to prevent, one level up.

`tcr` carries one open item: its file format was not stated, so the
legacy `.xls` contingency in `SSS_001` may still be spent there. The
`.xlsx` on the UNFCCC target does close it for that one.

**Falsifier:** a real live calculator returning `rank_zero_share > 0.95`
— which would either refute "live calculator implies formula chains" or
implicate the scan, and the other two arms are what tell those apart.

**Status: SPECIFIED. No arm has been run.**

---

## Claims from the first real workbooks

Two files arrived on 2026-08-25: the UNFCCC GHG emissions calculator
ver 01.1 (`.xlsx`, uploaded twice — byte-identical, md5
`57d3ffd7…`) and The Climate Registry LGO Standard Inventory Report
(`.xls`, OLE2/BIFF8). **`SSS_010` is closed: the tool has met a real
workbook.**

---

### SSS_017 — the reader read 696 of 825 formula cells as constants

The UNFCCC workbook holds **825 formula cells**: 105 plain, 720 shared.
A shared formula stores its text **once**, on the group master, tagged
with an index; every follower carries only the index and inherits the
same formula with its relative references translated by its own offset.

The reader took `<f>` with an empty body as no formula. It counted
**129** derived cells — exactly the 105 plain plus the 24 masters that
carry text — and read the other **696 as constants.**

Consequences were not confined to one column. Those 696 cells had no
precedents recorded, so `pdepth`, `deps`, `ddepth` and `rank` were wrong
for every cell downstream of any of them, and scan three's
constants-versus-derived was reading a property of the file format.

`shift_formula(text, drow, dcol)` translates a master's relative
references, leaving `$`-pinned halves alone, with string literals masked
at preserved length so the edit spans still line up. Eleven hand-set
cases are pinned, including `#REF!` on an off-sheet shift and a literal
that must not move.

**This defect was invisible on the fixture**, because `fixture.py` writes
only plain formulas. `SSS_010` said passing is weaker evidence than
failing; this is what that was about.

**Falsifier:** a formula construct whose follower text this does not
reproduce — array formulas beyond their anchor are the open candidate,
and a follower with no resolvable master now records
`SHARED_MASTER_MISSING` and stays `DERIVED` rather than becoming a
constant.

**Status: REPAIRED. 825 of 825 resolved, 0 `SHARED_MASTER_MISSING`.**

---

### SSS_018 — the diagnostic that found `SSS_017` was itself wrong, in the same direction

The regex used to count `<f>` elements in the raw XML was
`<f([^>]*)>(.*?)</f>|<f([^>]*)/>`. `[^>]*` matches the `/` of a
self-closing tag, so `<f … />` was consumed by the first branch and its
`(.*?)</f>` ran on to the **next** real closing tag, merging the pair.
It reported **476** where a parse reports **825**.

Both errors undercounted, so the diagnosis — *followers are being
dropped* — survived. That is luck, not method: had the diagnostic erred
the other way it would have masked the defect it was written to find.

The lesson is the folder's own: `sheetmodel.py` reads this format with a
parser for exactly this reason, and the throwaway check reached for a
regex.

**Falsifier:** a count from a third route disagreeing with 825.

**Status: RECORDED. The diagnostic was replaced by a parse; the finding
it produced stands.**

---

### SSS_019 — a refuted prediction on real data was the reader, not the workbook

Registered before the file existed: `UNF-P1`, `derived_share > 0.20`.

| run | derived | `derived_share` | `UNF-P1` |
|---|---|---|---|
| as delivered | 129 | 0.037 | **NOT_HELD** |
| after `SSS_017` | 825 | **0.226** | HELD |

`UNF-P2` and `UNF-P3` held in both runs — `rank_zero_share` 0.634 then
0.461, `max_pdepth` 5 — which is what said the scan was finding *some*
propagation and made a reader defect the live hypothesis rather than a
claim about the workbook.

**This is the pre-registration doing the job it was built for.** Without
a threshold fixed in advance, `derived_share = 0.037` on a workbook
described as a live calculator is a number with no one to argue with it,
and the most available reading — *this calculator is mostly reference
tables* — is both plausible and wrong.

`P1` now holds by a **small margin**: 0.226 against 0.20. Reported as
such rather than as a clean pass.

**Falsifier:** a formula construct still unread, which would raise 0.226
further and leave the direction unchanged.

**Status: HELD after repair, 3 of 3.**

---

### SSS_020 — the substantive finding: one sheet computes its emission factors where eight hardcode them

Scan three lists **4 groups of 33** with two or more occurrences: 2 on
the column axis, 2 on the row axis.

`factors`, 11 sheets, rank 975:

| sheet | depths | construction |
|---|---|---|
| Fuels, Refrigerants, WTT-fuels, T&D, Material use, Business travel, Food, Water | `{0}` | pure constants |
| **Home Office** | `{1}` | **31d — pure derived** |
| Employees commuting | `{0,2}` | 40c+8d |
| Electricity, heat, cooling | `{0,1,2}` | 3c+2d |

`kg CO2e`, the output column, 11 sheets, rank 740: nine sheets pure
derived at depth `{1}`; **Home Office at `{2}`**, one level deeper
because its factors are computed rather than looked up; Employees
commuting at `{1,3}`.

Same column name, genuinely different construction, and the depth column
carries the consequence downstream. This is the case scan three was
built for, on a real workbook, and it is not noise — see `SSS_021` for
the two occurrences per group that **are** artifacts, checked and
separated rather than assumed clean.

**Falsifier:** the Home Office factors column turning out to be a lookup
after all, which a reader of that sheet can settle in a minute.

**Status: SUPPORTED. What it means for the workbook is the operator's
reading; the tool reports that the constructions differ.**

---

### SSS_021 — two of the differing occurrences per group are stacked-table artifacts, with a named cause

`Electricity, heat, cooling` and `Water` differ from the rest of their
groups because they carry **more than one table stacked in a column**.
Their governed ranges contain the label text again — `F10` and `F15` on
one, `E12` on the other — and `CHOICE 4` assumes **one label row per
sheet**, so `governed()` runs straight through the second header and
counts it as a constant in the data.

Measured rather than assumed: for each occurrence, the count of cells in
its governed range whose text normalizes to the group's own label. Two
sheets return 2 and 1; the other nine return 0. So **2 of 4 differing
occurrences per group are artifacts and 2 are real**, and `SSS_020`
rests on the two that are.

A real workbook exposed this and the fixture could not, for the same
reason as `SSS_017`.

**Falsifier:** a stacked sheet whose repeated header the label model
already handles.

**Status: SUPPORTED, unrepaired.** The repair is a label model that
detects a second header row inside a governed range, which changes
`CHOICE 4` for every sheet, not only these.

---

### SSS_022 — on the 22 cells scan three surfaced, the differential the Hub was supposed to show

Flag set produced by **scan three**, not invented for scan two: the
first cell governed by each occurrence of each listed column collision.
22 cells across 11 sheets.

| companion | present | absent |
|---|---|---|
| `unit` | **22** | 0 |
| `date` | 0 | **22** |
| `sample_size` | 0 | **22** |
| `variance_sibling` | 0 | **22** |

Uniform. **The emission-factor and result columns of this calculator
carry a unit and carry no vintage, no sample size and no uncertainty
within reach of the number** — which is the structural claim the
Emission Factors Hub was offered to demonstrate, holding on a workbook
that is not the Hub.

It is one workbook and the Hub arm is still missing, so this is not the
known-answer test `SSS_013` describes. It is one observation of the
predicted differential.

**Falsifier:** a factor column on any sheet carrying a variance sibling
within the cross neighborhood.

**Status: SUPPORTED, n=1 workbook.**

---

### SSS_023 — the `.xls` contingency fired, and the one available reader would not have helped

`sheetmodel.read()` raised on the LGO Standard Inventory Report exactly
as `TARGETS.md` §5 registered, and the CLI now reports it with rc 3
rather than a traceback.

**The slot stays unspent, and not out of stubbornness.** The workbook is
valid BIFF8, five sheets, and carries **336 `FORMULA` records and 23
`SHRFMLA`**. The one reader available for the format, `xlrd` 2.0.2,
exposes `ctype` and `value` per cell and **no formula text** — it hands
back cached values. Both scans are about the formula layer, so spending
the budget on it delivers precisely the value-only view that `SSS_001`
named as the reason to parse the XML directly. **The constraint's stated
reason turns out to be load-bearing at the exact moment the budget would
be spent.**

The converter route is **untested here, not refuted**: LibreOffice is
installed and fails with *"source file could not be loaded"* — and fails
identically on a control input this tool parses without difficulty, so
the install is broken in this environment and the result says nothing
about the `.xls`. The route that would work is a conversion on a machine
with a working LibreOffice, then the stdlib path on the `.xlsx`; a
converted copy is a different artifact from the delivered one and any
result should say so.

**Falsifier:** a reader for this format that exposes formula text, which
would make the budget worth spending.

**Status: NOT SCANNED. The discriminator arm stands at one of three.**

---

### SSS_024 — the output screen ran in one of two command-line paths

`scans.py main()` screened its table on every invocation. `epa_check.py`
printed its profile unscreened, and the gap surfaced on a real run: the
`unfccc` target's `not_registered` note carried a screened word.

Wired into both, and the selftest now checks **every** target's render
rather than one — the earlier check passed because it happened to use
the target with no such note.

Worth separating from a false alarm: the word was in prose about the
*registration process*, not about a site on a sheet, which is the
use-and-mention boundary `DF_010` names. The reword was cheap and
keeping the screen strict is the point, so the prose moved rather than
the screen.

**Falsifier:** a third output path that prints without screening.

**Status: REPAIRED.**

---

## Claims from the coupling integration

`coupling.py`, built to section 4 of the 2026-08-25 order: replace
dependent count with coupling strength where it is computable from the
workbook, by perturbing the constant and measuring movement in the
output cells.

---

### SSS_025 — the evaluator reproduces 631 of 631 cached values, and that is a known-answer run on real data

Every derived cell in an `.xlsx` carries the value Excel last computed
for it. `coupling.py verify` recomputes each one and compares.

| run | reproduced | disagreed | not computable |
|---|---|---|---|
| arithmetic only | 475 | 0 | 156 |
| + lazy `IF`, comparisons, BLANK | 608 | 0 | 23 |
| + re-entrancy repair (`SSS_027`) | 627 | 0 | 4 |
| + `SUMIF` | 629 | 0 | 2 |
| + Excel's range semantics (`SSS_028`) | **631** | **0** | **0** |
| + `VLOOKUP` exact | 631 | 0 | 0 |

**Zero disagreements at every stage.** This is the discipline
`tools/known_answer.py` states, run against a file nobody here wrote,
and it is stronger evidence than any fixture: the answers were fixed by
Excel before the evaluator existed.

`verify` is itself null-tested in both directions on a fixture carrying
one right cached value and one deliberately wrong one, because a verify
that reported everything as matching would pass a one-armed test.

**Falsifier:** a workbook where the evaluator reproduces fewer than it
claims, or disagrees.

**Status: SUPPORTED, n=1 workbook.**

---

### SSS_026 — coupling is a property of the workbook AND a case, not of the workbook alone

The first run returned **0 of 789 constants in the coupling mode.** The
cause was not a missing function: the workbook is an unfilled template,
every activity cell is empty, `F6 = D6*E6` evaluates to zero on both
sides of any perturbation, and **nothing moves because nothing flows.**

So `elasticity()` takes `inputs` — the case the coupling is measured
under — and the case is printed into every report. Without one the
header says so: *"none given — an unfilled template moves nothing."*

A distinct state came with it. `NO_LIVE_PATH` (terminals evaluate, base
is zero) is not `NOT_COMPUTABLE` (no terminal could be evaluated), and
neither is an elasticity of zero, which would read as *measured, and it
does not matter*.

**Falsifier:** a workbook whose coupling is stable across every case,
which would make the case parameter decoration.

**Status: SUPPORTED.**

---

### SSS_027 — the evaluator was not re-entrant, and only a nested formula could show it

Parser state lived on the instance. Evaluating a referenced cell
re-enters `_eval` and overwrites `_s`, `_i` and `_sheet`, so the outer
formula resumed parsing inside the inner one.

It cost `SUM(E3:E24)` over derived cells — **every rollup in the
workbook** — and the fixture could not show it, because every formula in
the fixture was one level deep. Repaired by saving and restoring parser
state across nesting, with a fixture that sums three derived cells and
then continues the outer expression.

Same lesson as `SSS_017`: a fixture written by the author of the code
exercises the depths the author thought of.

**Falsifier:** a nesting shape the save does not cover.

**Status: REPAIRED, pinned.**

---

### SSS_028 — the workbook's grand total sums from a header row, and the evaluator had to match Excel to see it

`Report!E23` is `SUM(Food!E5:E16)`. **Every sibling row starts at row 6**
— `'WTT- fuels'!F6:F30`, `'Material use'!E6:E43`, `'Home Office'!J6:J36`
— and this one starts at 5, which is the column header cell containing
the text `kg CO2e`.

Excel ignores text inside a range aggregate, so the workbook computes
correctly and the off-by-one is invisible in use. The evaluator raised
on it, which is how it was found; matching Excel's rule was the repair,
and the observation is the finding.

**Falsifier:** another sheet whose report row also starts at the header,
making it a convention rather than an outlier.

**Status: SUPPORTED. Reported as structure; what it means for the
workbook is the operator's reading.**

---

### SSS_029 — coverage of a perturbation is a property of the terminals, not of the formula population

At one point the evaluator reproduced **627 of 631** formulas and **0 of
789** constants reached a coupling number.

The reason is structural: almost every constant in the workbook
terminates at one cell, `Report!E25`, the grand total. That cell summed
two `SUMIF` rows, and **two unsupported cells gated the coupling mode
for the entire workbook.**

So formula coverage and coupling coverage are different quantities and
the first does not imply the second. A tool reporting only the first
would have looked 99.4% complete while measuring nothing.

**Falsifier:** a workbook with many independent terminals, where partial
formula coverage buys proportional coupling coverage.

**Status: SUPPORTED.**

---

### SSS_030 — replacing dependent count with coupling changes the answer, not the presentation

Under the stated case `Fuels!E6=1000, Your organisation!C6=Iraq,
Electricity, heat, cooling!E7=1000`:

| | constants |
|---|---|
| ranked | 789 |
| coupling mode | 784 |
| **coupling > 0** | **3** |
| coupling exactly 0 | 781 |
| count-mode fallback | 5 |

**Every one of the 781 zero-coupling constants ranks non-zero under
dependent count, from 3 up to 380.** Dependent count measures *wiring*;
coupling measures *what moves given a case*. On a workbook where most
lines have no activity data, those are opposite answers.

The top row is the Iraq grid factor at coupling 0.6215 and rank 3.107 —
and the number is interpretable: the elasticity of a sum with respect to
one of its terms is that term's **share of the total**, which the
`Fuels!D6` case confirms to four figures (0.44327 / 0.56877 = 0.7794
against a measured 0.7793).

**The two modes are not on one scale** and the report says so, sorting
within mode rather than merging them — a column mixing `coupling × depth`
with `deps × depth` is a ratio across unlike objects.

**Falsifier:** a fully populated case where the two orderings agree,
which would make the substitution cosmetic.

**Status: SUPPORTED under the stated case. Coupling is case-dependent by
construction and the case is printed with every run.**
