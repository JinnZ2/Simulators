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

---

### SSS_031 — the aggregate hid a distinction a dependent count cannot make: structural versus live

`coupling.py cells` perturbs one constant and walks the whole workbook
under both states. On the Iraq grid factor, under
`Your organisation!C6=Iraq, Electricity, heat, cooling!E7=1000`:

| | |
|---|---|
| cells that moved | **26** |
| structural dependents (graph edges) | **33** |
| of those, did **not** move | **31** |
| moved without being a direct dependent | **24** |

**Both halves are the finding.** 31 of 33 graph edges are dead under
this case, because `Electricity, heat, cooling!A84:B332` is a `VLOOKUP`
range: every cell in it is a structural dependent of every consumer, and
only the row the key selects is a live one. And 24 cells moved that have
no edge from the perturbed cell at all — they sit further down the
chain.

So the dependent-count fallback and the coupling measurement are not
approximations of each other. A count of 33 on a lookup range is a count
of the range's height.

The propagation is correct modelling, not a leak: everything routes
through `Your organisation!D6`, the lookup that resolves the selected
country to its grid factor, and the electric-vehicle and
electric-commuting rows multiply their activity by it — `Owned
vehicles!D33` is `IF('Your organisation'!$C$6<>"",G33*'Your
organisation'!$D$6,0)`. Charging an electric vehicle from a national
grid is what that edge means.

Every moved cell has elasticity **exactly 1.0** except the grand total
at **0.881538**, which is the share result again: a pure product chain
passes a relative change through unchanged, and only the sum dilutes it.

**Falsifier:** a case where the structural and live sets coincide,
making the distinction free.

**Status: SUPPORTED.**

---

### SSS_032 — the Palestine value is a hardcoded constant, so the stated derivation is not live

Asked directly whether any Palestine cell moved under the Iraq
perturbation. **None did, and none can.**

`Electricity, heat, cooling!B296` is a `CONSTANT_NUMBER`. Row 296 holds
exactly two cells — `A296` the country name and `B296` the number — and
neither is a formula. Checked exhaustively: no moved cell is on row 296,
and no cell anywhere in the workbook whose text mentions Palestine
appears in the moved set. The only two such cells are `A296` and the
prose note at `Info and sources!E10`.

**The consequence is about the workbook, not about the scan.** The note
at `Info and sources!E10` states that the Palestine factor is the
average of Iraq, Jordan, Lebanon, the Syrian Arab Republic and Turkey,
and the cell reproduces that mean to 1.1e-16 — but as a **value**, not
as a formula. The relationship is a record of how the number was once
produced. It is not maintained: if any of the five is revised upstream,
this cell does not follow, and nothing in the workbook would show that
it had stopped being the mean.

**Falsifier:** a formula anywhere that recomputes B296 from the five.

**Status: SUPPORTED. Reported as structure; what it means for the
workbook is the operator's reading.**

---

## Claims from scan 4 — stated-relationship maintenance

Work order 4, delivered verbatim in `WORK_ORDER_4.md`. Independent of
scans 1-3: those read structure, this one reads what the workbook says
about its own numbers and checks whether the file still does it. The
occasion is `SSS_032`.

---

### SSS_033 — on the first real workbook the bins are 0 / 2 / 21 / 11

| bin | count |
|---|---|
| MAINTAINED | **0** |
| HOLDS_UNMAINTAINED | **2** |
| BROKEN | **21** |
| NOT_TESTABLE | 11 |

135 prose cells read across 8 sheets located by keyword; 134 classified
`NOT_ARITHMETIC` and counted rather than tested.

**Not one stated arithmetic relationship in this workbook is maintained
by a formula.** Every relationship the prose states about a number is
stated about a constant. The two that still hold, hold by coincidence of
history rather than by construction — which is `SSS_032` generalised
from one case to the whole file.

No aggregate score and no ranking, per S5. The four bins are the
finding.

**Falsifier:** a formula target anywhere in this workbook's stated
relationships.

**Status: SUPPORTED, n=1 workbook.**

---

### SSS_034 — twenty-one targets do not satisfy the relationship stated for them, and twenty of them carry the same wrong number

`Info and sources!E10` states that twenty-two named territories each
take the average of thirty-three named places. The scan resolves all
thirty-three operands and every target, and reports:

| what the target holds | targets |
|---|---|
| **0.52194015744421518** | **20** |
| 0.23879807608323081 | 1 |
| the stated mean, 0.46020578160626169 | **0** |

**0.52194015744421518 is `Electricity, heat, cooling!B329`, Western
Sahara** — to all seventeen digits. Western Sahara is the target of a
*different* stated relationship in the same cell of prose, the average
of five North and West African countries, and that one holds.

So twenty territories carry a number computed for somewhere else.
Verified by hand on `B114` (Bouvet Island) and `B329` independently of
the scan. Relative delta 0.118 on the twenty; 0.481 on Macao.

**This is reported as structure and is not called an error.** A
workbook may have every reason to hold a number the note beside it no
longer describes, and this scan does not know what that reason is. What
it can say is that the file states one thing and holds another, and that
nothing in the file would have surfaced it.

`when it diverged` is **UNRECOVERABLE** and says so: `.xlsx` carries no
per-cell revision history, so the file cannot date the divergence. A
version series of the same workbook would bracket it.

**Falsifier:** a reading of `E10` under which those twenty-two
territories are not assigned that average.

**Status: SUPPORTED.**

---

### SSS_035 — operand count separates the bins here, which is the S6 signal at n=1

| bin | operand counts |
|---|---|
| HOLDS_UNMAINTAINED | **5, 5** |
| BROKEN | **33** (21 targets, one relationship) |
| NOT_TESTABLE | 0 (no operands named) |

Both five-operand relationships hold. The thirty-three-operand one does
not, across every target it states. `BROKEN / (BROKEN + HOLDS) = 0.913`.

That is exactly the quantity S6 says to accumulate, and **one workbook
is one point.** The rate emission prints `n = 1` and refuses a curve in
those words: *a point is not a rate*. The within-workbook pattern —
more operands, more drift — is one observation and is stated as one.

`cross-sheet` is 0 here: every operand of every tested relationship
resolves on the same sheet as its target.

**Falsifier:** a second workbook where the relationship with more
operands is the one that holds.

**Status: SPECIFIED, n=1. No curve reported.**

---

### SSS_036 — three resolution problems the real prose forced, each fixed by a stated rule rather than a guess

**Punctuation cannot split the operand list.** `Bonaire, Sint Eustatius
and Saba` is one country containing a comma and an "and"; so are `Heard
Island and McDonald Islands`, `Wallis and Futuna Islands` and
`China, Macao Special Administrative Region`. Splitting on commas and
"and" produced **38 operands where the prose names 33**, inventing five.
The split is now **resolved, not guessed**: at each position take the
longest label the workbook itself carries, and emit unmatched text as a
fragment that goes on to fail resolution. The workbook supplies the
vocabulary.

**Country names are ambiguous between two tables.** `Jordan`, `Turkey`
and `Fiji` each resolve to a grid factor on one sheet and a hotel factor
on another — genuinely two candidates with different values, so S3 makes
them NOT_TESTABLE and the Palestine relationship failed to test at all.
Repaired with a **declared scope**: when the target resolves on one
sheet, operands are sought on that sheet first. That is not a
tie-break — the rule is stated, applied to every operand alike, printed
with the verdict, and **the ambiguity guard survives inside the scope**:
two candidates on the target's own sheet are still AMBIGUOUS.

**The prose and the sheet use different names.** The note says
`Palestine`; the row says `State of Palestine`. Exact matching alone
made G2 NOT_TESTABLE, which the fixture calls a fail. Repaired with a
**unique whole-word containment** match, recorded in the row as
containment rather than exact, and AMBIGUOUS when more than one label
contains the name.

All three were found by running the scan on a real file. None is
visible on a fixture written by the same hand as the scan.

**Falsifier:** a case where one of the three rules picks a resolution a
reader would not.

**Status: SUPPORTED.**

---

### SSS_037 — an operator with no operands must land in a bin, or an untestable relationship leaves the count

`Info and sources!E19` reads *"Hotel Carbon Footprint Per Occupied Room
| All hotels upper quartile emission factor value"*. The operator is
stated; there is no `of` clause and no operand is named, because the
distribution is a published index that is nowhere in the file.

The first build extracted nothing from it and counted it
`NOT_ARITHMETIC`. That satisfies S8's letter — it produced no testable
verdict — and fails G5, which requires `NOT_TESTABLE`. The difference
matters: `NOT_ARITHMETIC` removes the relationship from the four bins
entirely, so a workbook full of untestable stated relationships would
report a clean, small denominator.

Now an operator with no operand clause is a relationship with an **empty
operand list**, which is a fact about the prose, and it bins
`NOT_TESTABLE`. Four of the eleven `NOT_TESTABLE` rows are of this shape.

**Falsifier:** a stated relationship this treatment scores that a reader
would judge testable.

**Status: REPAIRED. G5 produces no testable verdict and no expected
value, asserted in the selftest.**

---

### SSS_038 — the divergence date is unrecoverable from the file, and the tool says that rather than estimating

S4 asks for *when it diverged*, if the file carries revision history.
`.xlsx` carries none per cell unless tracked changes are on, and this
file has none.

Every BROKEN row therefore reports `UNRECOVERABLE`, with the reason and
with what would answer it: a version series of the same workbook would
bracket the change. An estimate here would be worse than the gap — the
question is *when a note and a number stopped agreeing*, and nothing in
a single file records it.

**Falsifier:** a workbook of this format that does carry per-cell
history the tool ignores.

**Status: SUPPORTED.**

---

### SSS_039 — scan 4 shipped without the constraint its own order states, and the constraint fires on the vocabulary the order delivered

`scan4.py` was written, selftested and its runs pinned before anything
screened its output. `scans.py` runs `no_severity` over every emitted
table; scan 4 did not import it at all. The order's S8 says *no
labelling*, and the module enforcing that in this folder was not
connected to the module the order governs.

Screening the pinned runs afterwards returned 24 hits on the main
report, and the shape of them is the finding:

| what fired | where | reading |
|---|---|---|
| `broken` | the `BROKEN` bin name, x22 | **delivered vocabulary** |
| `error` | *"BROKEN is not an error"* | use-mention in the disclaimer |
| `needs` | *"a decay curve needs a series"* | ordinary prose |

**The bin name is in the delivered work order and `broken` is on the
screened list.** Loosening the screen would settle it and is how a screen
becomes decorative, so the exemption is **declared and measured**:
`screened()` masks the delivered token, and `exemption_is_only_the_bin()`
asserts the token is the *only* thing that fires without the mask — two
arms, because masking `BROKEN` also hides any sentence containing it. A
third check plants `this cell is wrong` and requires it caught through
the exemption.

The other two were **reworded rather than exempted** — the same call
`residual-direction` `RDD_008` made when its screen fired on its own
disclaimer. A fourth, `severity` inside a selftest check name, was
renamed for the same reason.

The measurement holds on the real workbook, not only on the fixture: all
three UNFCCC runs are clean under the mask and fire on nothing but the
bin.

**What this does not buy** is anything the screen could not already do.
A paraphrase steps around it, stated at the top of `no_severity.py` and
on record as `UNI_009` / `DF_010` / `ACL_017`. What it buys is that the
fluent failure — reaching for the ordinary vocabulary of grading without
noticing — is caught, and it caught three instances here on first
contact.

**Falsifier:** a grading word emitted by scan 4 that passes both arms.

**Status: REPAIRED, and recorded rather than quietly fixed — a module
landing without the constraint its order states is evidence about how
the constraint travels, not a typo.**

---

### SSS_040 — the legacy constraint is a property of the reader, not of the format, and the one-reader budget stays unspent

WO6 S1 states it as *"legacy readers may not expose formulas, only
cached values"*. True of the reader this repository tested — `SSS_023`
found `xlrd` 2.0.2 hands back cached values with no formula text — and
**false of the file.**

A `.xls` is a compound-file container holding a BIFF record stream, and
`struct` reaches it. This target carries **336 `FORMULA` and 23
`SHRFMLA`** records and all 336 decode.

`xlsreader.py` is therefore stdlib, and the one spreadsheet reader
beyond stdlib is unspent for a **second** file format. `SSS_001`'s
argument was that both scans are about the formula layer a value-only
reader drops; the legacy file is the case that argument was made for.

Capabilities are declared per item rather than claimed in prose —
`cell_values`, `cell_kind`, `precedents` yes; **`formula_text` no** —
and callers mark scans NOT_RUN from the declaration.

**Falsifier:** a `.xls` whose formulas this reader cannot reach.

**Status: SUPPORTED.**

---

### SSS_041 — two decoding defects the real file produced, neither visible in a fixture

**(1) Shared-formula masters are written after the first formula that
uses them.** A `FORMULA` carrying `ptgExp` points at a `SHRFMLA` that
has not been read yet, so resolving in stream order returns nothing.
The first version did exactly that and gave **23 cells an empty
precedent list**, which reads as *no precedents* rather than as *not
resolved*. Deferred to a second pass; a key that still does not resolve
now says `SHARED_MASTER_NOT_FOUND`.

**(2) Relative areas were walked past rather than decoded.** `ptgAreaN`
(0x2D) was skipped for its 8 bytes, which left **145 formulas with no
precedents and no note** — the graph silently missing a third of its
edges. Relative refs also store the column delta as a **signed byte**,
not as the 14 bits an absolute ref uses: reading it wide puts a −1
offset in column 16384.

| | before | after |
|---|---|---|
| DERIVED cells with ≥1 precedent | 188 of 336 | **336 of 336** |
| precedent edges | 714 | **1056** |
| cells flagged partial | 23 | 0 |

Both are pinned by selftest checks written from the real token arrays.
Neither was reachable from a constructed fixture, because the fixture
writer emits what the reader expects.

**Falsifier:** a formula in this file whose precedent list the reader
gets wrong.

**Status: REPAIRED, pinned.**

---

### SSS_042 — P4 is refuted: the legacy workbook states no testable relationship, and the zero is the workbook

Registered before the run in `PREDICTIONS_WO6.md`. P4 was *at least one
prose cell yields a testable relationship*, written so that P1–P3 would
be **unreachable rather than refuted** if it failed. It failed.

| | |
|---|---|
| provenance sheets located | 4 of 5 |
| prose cells read | 189 |
| classified NOT_ARITHMETIC | 188 |
| testable relationships | **0** |
| bins | 0 / 0 / 0 / 1 |

**The zero is a property of the workbook, not of the extractor**, and
that is measured rather than argued. Occurrences across all 189 prose
cells: `average` 0, `mean` 0, `sum of` 0, `total of` 0, `multiplied` 0,
`divided` 0, `product of` 0, `equals` 0, `calculated as` 0, `=` 0.

So P1, P2 and P3 are **unreachable on this file**. Per S4, H1 is
therefore not supported here — and the sharper statement is that it is
**not addressable** here, which is a different thing from unsupported
and is `SSS_043`.

**Falsifier:** a stated arithmetic relationship in this workbook's prose
that the extractor missed.

**Status: P4 REFUTED. P1–P3 UNREACHABLE.**

---

### SSS_043 — the two workbooks' provenance prose is a different KIND, and that is the cross-file finding

This is what the second file bought, and it is not what H1 asked about.

| | UNFCCC calculator | LGO inventory report |
|---|---|---|
| prose states | *"Bonaire … : Average of American Samoa, Antigua and Barbuda, …"* | *"Description of computational method:"* |
| about | values the workbook **ships** | values a filer **will supply** |
| tense | retrospective — how this number was produced | prospective — what you are to write here |
| testable relationships | 23 | **0** |

Both files are unfilled templates (`SSS_026`; the legacy file has **zero
constant numbers** in 1580 cells). The difference is not fill state. It
is that one workbook **carries reference data with provenance notes**
and the other **collects data with instructions**, and only the first
kind can state a relationship about its own values.

**H1 is a hypothesis about workbooks that state relationships.** This
workbook states none, so it is not a negative instance — it is outside
the population. Reporting it as *H1 unsupported* would count a workbook
that cannot address the question as evidence against it.

The generalisation, and it is a prediction for a third file: **a
data-shipping workbook states relationships about its own cells; a
data-collecting workbook states instructions.** Scan 4 has something to
measure only in the first kind.

**Falsifier:** a data-collecting template whose provenance prose states
arithmetic about its own cells, or a data-shipping workbook whose prose
states only instructions.

**Status: SUPPORTED at n=2, and it is n=2.**

---

### SSS_044 — the share has an empty denominator and no direction is stated

S3 asks for `DIVERGED/(D+H)` per workbook and a direction across them.

| workbook | MAINT | HOLDS | DIVERGED | NOT_TEST | share |
|---|---|---|---|---|---|
| unfccc.xlsx | 0 | 2 | 21 | 11 | 0.913 |
| lgo.xls | 0 | 0 | 0 | 1 | **empty denominator** |

`diverged_share()` returns `None`, not `0.0`. Zero would put a workbook
with nothing to measure at the good end of a scale it is not on — the
`PCH_001` shape, and the thirteenth instance of this repair here.

`direction()` therefore returns **`NO_DIRECTION`**, with the reason:
*a direction takes two defined points and 1 of 2 workbooks has an empty
denominator.* n = 2 is printed on the emission, and no curve is emitted
at any n reached here.

**Falsifier:** a second data-shipping workbook, which would give the
first two comparable points this order has not had.

**Status: SUPPORTED.**

---

### SSS_045 — "file date" is two dates, eight years apart, and both are printed

S3 asks for a file date. Both container formats record two, and on the
legacy target they are not close:

| workbook | created | modified |
|---|---|---|
| unfccc.xlsx | 2020-11-24 | 2021-05-25 |
| lgo.xls | **2008-06-04** | **2016-05-02** |

An eight-year gap between creation and last save, on a form whose
filename states the later date. Picking one and labelling it *the file
date* would be a choice presented as a reading, so the column is headed
`created / modified` and carries both.

Only the two date properties of the `SummaryInformation` set are read.
The same property set carries author and company strings; those name a
private individual, are no part of any measurement here, and nothing
reads them.

**Falsifier:** a use of the date column where the two dates license the
same next step.

**Status: SUPPORTED.**

---

### SSS_046 — coupling was silently substituting the forbidden value-only fallback until this order

`coupling.py` ranks by measured elasticity **where computable and by
dependent count where not**, which is right on a workbook whose
formulas are readable. On a reader with no formula text it is exactly
the substitution S1 forbids: every constant falls through to the COUNT
mode and the report prints a ranking under a coupling heading.

Run on the legacy file before the fix, it printed
`evaluator reproduces 0 of 0 cached values; 336 not computable` and then
a COUNT table, with nothing saying the coupling arm had not run.

Now the reader's declaration stops it: **`COUPLING IS NOT_RUN ON THIS
WORKBOOK`**, with what the reader does supply, and the count ranking is
**not** emitted as a stand-in — on this repository's own evidence the
two disagree, 781 constants at exactly zero coupling all ranking
non-zero by count up to 380 (`SSS_030`). Pinned in both directions: a
capable reader is not stopped.

**Falsifier:** a path by which a count ranking reaches a coupling report.

**Status: REPAIRED, pinned.**

---

### SSS_047 — scan three's finding on the legacy file: same label, different construction, in a template's repeated blocks

Scans 1–4 ran unchanged (S2). Scan three found the collision it exists
for, on a real legacy file:

`total location-based scope 2 emissions` labels **ten** row blocks. Some
govern `1c+4d` — five cells, the first a constant — and some govern
`4d`, four cells, all derived. Same label, different construction, in a
form where the ten blocks are meant to be parallel sectors.

17 label groups with two or more occurrences; **9 listed, 8 agreeing on
both construction and depth**, so the listing is selective rather than
firing on repetition.

**Falsifier:** a reading of those blocks under which the fifth cell's
absence is intended.

**Status: SUPPORTED. It is a structure report; what it means is the
operator's.**

---

### SSS_048 — the one NOT_TESTABLE row is a sense collision, and the operand requirement caught it

The legacy file's single non-`NOT_ARITHMETIC` prose cell is
`5. Sector Definitions!B5`, matched on the operator `times`. The text is
*"…often times the outdoor lighting at a given building…"* — an
adverbial, not multiplication.

`UNI_009` / `T1-1`'s shape inside scan 4's own operator vocabulary. It
cost nothing because the second requirement held: no operands are
named, so the row binned `NOT_TESTABLE` rather than producing a
verdict. Recorded rather than repaired, because the guard that caught it
is the one `SSS_037` added, and a word-boundary fix would not address the
class — *times* as multiplication and *times* as an adverb are the same
token.

**Falsifier:** a sense collision that reaches a testable verdict.

**Status: SUPPORTED. Caught by the second condition, not the first.**

---

### SSS_049 — with the exemption retired, one file still fires, and it is the screen's own selftest

The WO4 amendment renamed the bin `BROKEN` → `DIVERGED` and retired the
delivered-order exemption entirely: `DELIVERED_VOCABULARY = ()`, no
token masked, no file exempted. Across every pinned sample in this
folder, scan output and prediction registers included, **one file
fires** — `samples/selftest.sample.txt`, which is `no_severity`'s own
selftest transcript and necessarily contains the words it screens in
order to test them.

That is a statement about the screen's SCOPE, which is emitted reports.
A transcript asserting that `terror` is not `error` is not one.

Four other files fired on first screening and were **reworded, not
exempted** — a check name containing *wrong*, two prediction lines
containing *should*, and two containing *needs*. Fourth consecutive
application of that rule (`RDD_008`, `SSS_039`).

**Falsifier:** a screened word in an emitted report.

**Status: SUPPORTED.**

---

### SSS_050 — S1's second criterion named a test that did not exist, and building it is most of this order

WO7 S1(b) is *"provenance prose classified RETROSPECTIVE under the
amended WO4 test"*. There was no such test. `SSS_043` drew the
retrospective/prospective distinction **in prose**, from two workbooks,
and nothing implemented it — `RETROSPECTIVE` and `PROSPECTIVE` appear
**zero times** in this folder before `selection.py`.

Sixth instance of the `MF_017` / `CW_015` / `DL_004` / `GC_012` /
`UNI_013` shape: a stated rule with no field or function behind it. The
cheapest point to catch it is when the next order tries to use it, which
is what happened.

Built in `selection.py`, calibrated against the two sentences that
motivated `SSS_043` — assigned by hand before this code existed, so they
are known answers rather than fitted ones.

**Falsifier:** an implementation of the WO4 test predating this file.

**Status: SUPPORTED, and REPAIRED.**

---

### SSS_051 — (b) and (c) would be one gate wearing two names, and the classifier is built to keep them apart

The easy implementation of (b) is *does any prose cell yield a
resolvable relationship*, which is (c). Two criteria computing one
quantity is `category-weld`'s mechanism inside the screen: the reject
log would look like two independent gates and be one.

So (b) reads **stance** — who the sentence addresses and in what tense —
and (c) reads **resolvability**, and `independence()` reports whether
they have ever been observed disagreeing.

| (b) passes | (c) passes | candidates |
|---|---|---|
| False | False | 1 |
| True | True | 2 |

**Off-diagonal: 0 of 3.** Under the rule these results use they have not
been observed disagreeing, so on this population the screen cannot say
which criterion is doing the work. Two cases would separate them, and
one is `SSS_052`.

The separating case that is not in hand: a retrospective note whose
operands sit **outside** the file — *"factors taken from the 2019 IEA
world energy balances"* — which is retro and unresolvable. That shape is
common in published workbooks and no candidate here is one.

**Falsifier:** a candidate scoring on the off-diagonal.

**Status: SUPPORTED. The screen is two criteria and has been observed as
one.**

---

### SSS_052 — the stance threshold moves the verdict on the only file that has ever produced a testable relationship

`min_retro = 1` — *any* retrospective sentence makes a workbook
retrospective — is a `[CHOICE]`, and it is load-bearing:

| workbook | RETRO | PROSP | NEITHER | any rule | majority rule |
|---|---|---|---|---|---|
| UNFCCC | 4 | **9** | 122 | RETROSPECTIVE | **PROSPECTIVE** |
| LGO | 0 | 32 | 157 | PROSPECTIVE | PROSPECTIVE |

**The UNFCCC calculator has more than twice as many prospective prose
cells as retrospective ones**, and it is the file carrying all 23
testable relationships this repository has found. A majority rule
rejects it at (b) — the only workbook (c) accepts.

So the threshold is **calibrated by a case rather than stipulated**, and
the case is printed. It also settles `SSS_051` one way: under a majority
rule UNFCCC is (b) PROSPECTIVE and (c) resolvable, which **is** the
off-diagonal cell. Whether the two criteria are independent is a
property of the threshold, not of the criteria.

Both branches are asserted in the selftest on constructed counts, so the
readout is not trusted from the two real files alone.

**Falsifier:** a workbook where the two rules agree and the eligibility
verdict still turns on the threshold.

**Status: SUPPORTED.**

---

### SSS_053 — the reject log, and the population finding S1 anticipated

S1 says the reject log is a finding in its own right. It is, and the
finding is not the one the order expected.

| candidate | a | b | c | d | e |
|---|---|---|---|---|---|
| UNFCCC calculator | pass | pass | pass | **fail** | **fail** |
| UNFCCC calculator (byte-identical duplicate) | pass | pass | pass | **fail** | **fail** |
| LGO inventory report | **fail** | **fail** | **fail** | **fail** | **fail** |

The screen records **every** criterion rather than stopping at the first
failure, because a file failing only (e) is a different candidate from
one failing (a), (b) and (c), and a first-failure log cannot tell them
apart. It separates cleanly here: (a)–(c) are content criteria and
(d)–(e) are novelty criteria, and the prior file passes all three of the
first and neither of the second.

**No third candidate is reachable from this session.** Probe, run
2026-08-25T18:36:44Z: `www.epa.gov`, `unfccc.int`,
`theclimateregistry.org`, `www.eia.gov`, `data.gov` and
`www.ipcc-nggip.iges.or.jp` all return a refused CONNECT; only the
GitHub hosts respond, and trawling third-party repositories on a
reachable host is outside this session's scope. The two prior files are
what is in hand, and one of the three uploaded files is a byte-identical
duplicate of another (`md5 57d3ffd7…`), so the distinct population is
**two**.

S1's own hypothesis — *if most published workbooks fail (b) or (c), the
testable population is small* — is therefore **untested**, and the
reason is not that most workbooks fail: it is that none could be
screened. That distinction is the whole of `SSS_043` applied to this
order's own method.

**Falsifier:** a session that can reach published workbooks, which would
turn this from a reachability report into the population measurement S1
asked for.

**Status: SUPPORTED as a reachability report. S1's population question
is NOT ADDRESSABLE here.**

---

### SSS_054 — all four predictions return NOT ADDRESSABLE, which S3 made a legal verdict one order after it was needed

P1–P4 are registered in `PREDICTIONS_WO7.md` with parameters frozen
beforehand in `frozen_wo6.json`, and all four return **NOT ADDRESSABLE**
for want of an eligible candidate.

S3's clause — *"Each may return NOT ADDRESSABLE. That is a legal verdict
and is not counted as support or refutation"* — is the repair `SSS_043`
argued for, arriving in the order that follows it. Without it, WO6's
zero would have had to be reported as P1 holding and P2–P4 refuted, on
a workbook that cannot state a relationship at all.

**Falsifier:** a use where NOT ADDRESSABLE and a refutation license the
same next step.

**Status: SUPPORTED. Four NOT ADDRESSABLE verdicts, none counted.**

---

### SSS_055 — S4's OUT_OF_SCOPE is built, and the first implementation dropped the row it exists to keep

S4: *"LGO stays in the table as OUT_OF_SCOPE with its zero, never in a
denominator."* Two requirements, and they pull opposite ways in code.

The first implementation skipped out-of-scope workbooks with a
`continue` in the accumulation loop, which removed them from the
**denominator** and from the **table** — the opposite of what S4 asks.
Caught by running it, not by reading it. Both halves are now asserted
separately in the selftest.

A second defect the fixture caught: `scope_of()` first read scope off
the share's denominator, `DIVERGED + HOLDS`, which calls a workbook
whose relationship **is** enforced by a formula out of scope. MAINTAINED
counts; the `G1` fixture, whose single relationship is MAINTAINED, is
what turned it red.

The stance test itself is **imported** from `selection.py` rather than
reimplemented, so the screen that admits a candidate and the emission
that scores it cannot disagree about what RETROSPECTIVE means — the
no-copies convention that `MF_019` and `tools/check_gate_drift.py`
exist for.

**Falsifier:** an out-of-scope workbook absent from a table, or present
in a denominator.

**Status: REPAIRED, both halves pinned.**

---

### SSS_056 — naming the module `select` collided with the standard library, silently and intermittently

`select.py` was the obvious name. `select` is a stdlib module, so
`import select` resolves to the standard library from anywhere whose
`sys.path` does not put this directory first.

It **worked when run as a script** — the script's directory leads
`sys.path` — and failed the first time it was imported from a one-liner
in the same folder. A collision that is invisible in the way the author
runs the file and live in the way anyone else imports it.

Renamed `selection.py`. Recorded rather than quietly fixed because the
failure mode is a property of how it was tested, not of the code: every
check that passed, passed under the one invocation that hides it.

**Falsifier:** an import path under which the two names are equivalent.

**Status: REPAIRED.**

---

### SSS_057 — the SBA run is NOT_RUN on the files and the reader question is answered anyway

`sba.gov` and `www.sba.gov` both return a refused CONNECT, probed
2026-08-25T20:22:15Z — the same allowlist that refused six publisher
hosts at `SSS_053`. No file was uploaded at run time, so **the three
documents were not read by anything**.

What the order asks for regardless is the reader decision, and it has
three states rather than two: outside the budget → declare a capability
item; unreadable → NOT_RUN; and no substitution either way.
`docreader.py` answers it.

| | |
|---|---|
| `container_detect` | **built** |
| `stream_enumerate` | **built** — reused from `xlsreader`, not copied |
| `text` | **NOT BUILT** |
| `paragraph_structure`, `form_fields`, `tables` | NOT BUILT |

Each absence names what it stops. `text` stops **every upward cell** (a
stated goal is text), **every quantified downward stop** (a dollar figure
is text) and the WO7 screen's criteria (b) and (c) — so with text absent
the WO8 grid has nothing to fill and the run is NOT_RUN on all three
files, not partially run.

**The extension is a claim, not a fact**, and `sniff()` is the first
thing that runs: a `.doc` from a government site may be OLE binary Word,
a renamed OOXML zip, or RTF, and the three take three different readers.
The check that matters is tested on a real file — `/tmp/lgo.xls` is OLE
and **must not** read as a Word document, since a reader stopping at the
container signature would accept it. It reads `False` with the reason
naming the missing `WordDocument` stream.

**No text-heuristic substitute is offered, and the refusal is
structural.** `read_doc()` raises rather than returning a degraded read,
and a selftest check reads the module's own source to assert no
`strings`-style path exists in it. The order names the substitution and
so does the module, so it can be refused by name rather than by
intention — the `SSS_046` arrangement, where a dependent-count ranking
was refused as a stand-in for an uncomputable coupling.

**Why the parser is not written ahead of the files:** `SSS_017` and
`SSS_041` are both defects a real file exposed that no fixture could,
because a fixture writer emits what the reader expects. A `.doc` parser
validated against its own synthetic input would be tested by the one
thing that cannot fail it.

**Falsifier:** a session that can reach sba.gov, or the three files
uploaded, either of which turns this from a reader declaration into the
run the order asked for.

**Status: NOT_RUN on the files. The capability declaration is
SUPPORTED.**
