# sheet-structure-scan

Two scans over a spreadsheet, ranked by how far a site propagates.
The tool reports structure. It does not label a site, and the reading
stays with the operator.

Delivery in [`SOURCE_DROP.md`](SOURCE_DROP.md), verbatim.
Spec in [`SPEC.md`](SPEC.md). Findings from building it in
[`CLAIM_TABLE.md`](CLAIM_TABLE.md) and [`RESULTS.md`](RESULTS.md).

```
python3 scans.py two   book.xlsx --flags FLAGS.txt [--radius N]
python3 scans.py two   book.xlsx --all             [--radius N]
python3 scans.py three book.xlsx
python3 scans.py --selftest
```

## Files

| file | |
|---|---|
| `sheetmodel.py` | reader and precedent graph. `--selftest` |
| `scans.py` | scan two, scan three, ranking, table. `--selftest` |
| `no_severity.py` | the output constraint, enforced. `--selftest` |
| `coupling.py` | sensitivity by perturbation, and the ranking. `--selftest` |
| `scan4.py` | stated-relationship maintenance, and the cross-file emission. `--selftest` |
| `xlsreader.py` | legacy .xls (BIFF8), stdlib. `--selftest` |
| `docreader.py` | legacy .doc container triage and capability declaration. `--selftest` |
| `selection.py` | the WO7 eligibility screen and reject log. `--selftest` |
| `frozen_wo6.json` | the parameter values S2 freezes, written before screening |
| `PREDICTIONS_WO6.md` | H1's predictions, committed before the run |
| `WORK_ORDER_4.md` | scan 4 as delivered, verbatim |
| `patterns.json` | companion patterns for scan two. Swap this, not the code |
| `fixture.py` | the demo workbook, written as a readable table |
| `targets/TARGETS.md` | five workbooks, predictions registered before the data |
| `targets/epa_check.py` | those predictions, runnable. `--selftest` |
| `samples/` | one pinned run of each |
| `samples/runs/` | the real workbook runs, as produced |

## The two constraints

**One spreadsheet reader beyond stdlib, and it is unspent.** `.xlsx` is a
zip of XML and formulas sit in `xl/worksheets/sheetN.xml`, so `zipfile`
and `xml.etree` reach everything both scans need. The slot stays open for
a format the standard library cannot open. The larger reason is not
frugality: **both scans are about the formula layer**, and the common
reader's value-only mode drops it — reading the XML directly means the
layer under test cannot be discarded by the reader that was supposed to
deliver it.

**The tool never labels a site.** No verdict column, no threshold, no
ordering by consequence. `no_severity.py` screens 78 words across
severity and interpretation, runs over every emitted table, and is
null-tested in both directions. Its limit is stated at the top of that
file, not the bottom: a keyword screen is stepped around by paraphrase.

## Scan one is not in the delivery

Scan two begins *"for every flagged cell"* and nothing upstream was
specified, so **the flag set is an input and running without one is
refused.** `--all` exists and prints its own provenance into the report
header.

That is not fastidiousness, and the fixture measures the difference. Run
`--all` on the three-sheet demo: 38 rows, **23 carry an absence, and 15
of those 23 are label cells or strays outside any table** — a header
whose own text carries the unit is not under a header, so it reports the
unit absent. A five-cell flag list produces four absence rows, all of
them values inside a table. **The flag set decides the report more than
the scan does**, which is exactly why inventing one here would be putting
a framing in the operator's mouth and then ranking it.

## What the fixture refuted

A square neighborhood of radius 2 fails on this folder's own demo: the
`sd` column of a six-column table sits three columns from the flagged
cell, so a correctly built table reports its own variance sibling absent.
Widening the radius is the wrong repair — it reaches into the adjacent
record. The shape is a cross instead: the whole row, the column within
±radius, and the label-row cell above every column the row touched.

Written down because it was a design decision that a fixture overturned,
and the fixture is checked in.

## Coupling: the ranking, from what moves rather than from what is wired

`rank = deps x ddepth` measures wiring. `coupling.py` replaces the first
factor with a **dimensionless elasticity** measured by perturbing the
constant and reading the output cells, falling back to the count where a
formula is not evaluable and naming the mode per row.

The evaluator is checked against **Excel's own cached values** — every
derived cell carries the number Excel last computed — and reproduces
**631 of 631 on the UNFCCC workbook, with zero disagreements.** That is
a known-answer run on a file nobody here wrote.

Three things it took to get there, each recorded:

- **Coupling is a property of the workbook AND a case.** The first run
  returned 0 of 789 in coupling mode, because the workbook is an
  unfilled template: `F6 = D6*E6` with `E6` empty moves nothing under
  any perturbation. `--input Sheet!A1=VALUE` supplies the case and every
  report prints it.
- **The evaluator was not re-entrant.** Parser state lived on the
  instance, so a nested formula resumed the outer one inside itself. It
  cost every rollup in the workbook, and no depth-1 fixture could show
  it.
- **Coverage of a perturbation is a terminal property.** At one point
  627 of 631 formulas evaluated and 0 of 789 constants got a coupling
  number: nearly every constant terminates at one grand total, and two
  `SUMIF` cells in it gated the whole workbook.

**Per-cell, not aggregate.** `coupling.py cells` walks the whole
workbook under both states and lists what moved. On the Iraq grid factor
it separates two things a dependent count cannot: **26 cells moved, 33
structural dependents, 31 of which did not move** — a `VLOOKUP` range
makes every cell in it a graph edge and only the selected row a live one
— and **24 cells moved that are not direct dependents at all.**

Every moved cell has elasticity exactly 1.0 except the grand total at
0.881538: a product chain passes a relative change through unchanged,
and only the sum dilutes it.

And the result the substitution is for. Under a stated case, **3
constants have non-zero coupling and 781 have exactly zero — and every
one of those 781 ranks non-zero under dependent count, up to 380.**

## Scan 4: does a formula still maintain what the prose says

`WORK_ORDER_4.md` is the delivery. A workbook states relationships in
prose -- *this territory takes the average of those thirty-three* -- and
scan 4 asks whether anything in the file still enforces it. Four bins,
and the four bins are the finding: no aggregate score, no ranking, and
**BROKEN is not called an error.** A workbook may have every reason to
hold a number the note beside it no longer describes; the scan does not
know what that reason is, and the reading stays with the operator.

| bin | means |
|---|---|
| `MAINTAINED` | the target is a formula computing the stated relationship |
| `HOLDS_UNMAINTAINED` | the target is a constant that satisfies it anyway |
| `BROKEN` | the target is a constant that does not |
| `NOT_TESTABLE` | the relationship is stated but no operand set resolves |

**On the UNFCCC calculator: 0 / 2 / 21 / 11.** 135 prose cells read
across eight keyword-located sheets, 124 not arithmetic and counted
rather than tested. **Not one stated arithmetic relationship in this
workbook is maintained by a formula** -- every one is stated about a
constant, and the two that hold, hold by history rather than by
construction.

The headline is `SSS_034`. `Info and sources!E10` states that
twenty-two named territories each take the average of thirty-three named
places. **Twenty of them hold `0.52194015744421518`, which is
`Electricity, heat, cooling!B329`, Western Sahara, to all seventeen
digits** -- the target of a *different* stated relationship in the same
cell of prose, the average of five North and West African countries, and
that one holds. One (Macao) holds a third number. **Zero hold the stated
mean.** Verified by hand on `B114` and `B329` independently of the scan.

`when it diverged` returns **UNRECOVERABLE** and says so in those terms:
`.xlsx` carries no per-cell revision history, so the file cannot date
the divergence and the tool does not estimate one. A version series of
the same workbook would bracket it.

Operand count separates the bins here -- both five-operand
relationships hold, the one thirty-three-operand relationship does not,
across every target it states. `BROKEN / (BROKEN + HOLDS) = 0.913`, and
the rate emission prints `n = 1` and refuses a curve: **a point is not a
rate.**

Three resolution problems the real prose forced are fixed by stated
rules rather than by guesses (`SSS_036`), and an operator naming no
operands now lands in `NOT_TESTABLE` rather than falling out of the
count entirely (`SSS_037`).

And scan 4 **shipped without the constraint its own order states**
(`SSS_039`): `scans.py` screens every emitted table through
`no_severity` and scan 4 did not import it. Screening afterwards
returned 24 hits, and their shape is the finding -- 22 are the `BROKEN`
bin name, which the work order delivered and which is on the screened
list. The exemption is **declared and measured**, not taken: one arm
masks the delivered token, a second asserts it is the only thing that
fires without the mask, and a third plants a grading word and requires
it caught through the exemption. The other two hits were reworded
rather than exempted.

## Work order 6: a second workbook, and the legacy reader

**The legacy constraint is about a reader, not a format.** S1 states that
legacy readers expose only cached values, which is true of `xlrd`
(`SSS_023`) and false of the file: a `.xls` is a compound-file container
holding a BIFF record stream, and `struct` reaches it. The target carries
**336 `FORMULA` and 23 `SHRFMLA`** records and all 336 decode, so
`xlsreader.py` is stdlib and **the one-reader budget stays unspent for a
second file format**. Capabilities are declared per item — `cell_values`,
`cell_kind`, `precedents` yes, **`formula_text` no** — and callers mark
scans NOT_RUN from the declaration rather than from a note.

**Two decoding defects the real file produced.** Shared-formula masters
are written *after* the first formula that uses them, so resolving in
stream order gave 23 cells an empty precedent list that reads as *no
precedents*; and relative areas were walked past rather than decoded,
leaving 145 formulas with no edges and no flag. 188 of 336 → **336 of
336**, 714 edges → 1056. Neither was reachable from a fixture, because
the fixture writer emits what the reader expects.

**The prediction that failed is the one written to fail cleanly.** P4 —
*at least one prose cell yields a testable relationship* — was registered
before the run so that P1–P3 would be **unreachable rather than refuted**
if it went. It went: 189 prose cells, 188 not arithmetic, **zero testable
relationships**. And the zero is the workbook, measured rather than
argued: `average` 0, `mean` 0, `sum of` 0, `multiplied` 0, `divided` 0,
`equals` 0, `=` 0 across all 189.

**What the second file actually bought** is `SSS_043`, and it is not what
H1 asked. The two workbooks' provenance prose is a different *kind*:
UNFCCC says *"Bonaire: Average of American Samoa, Antigua and Barbuda,
…"* — retrospective, about values it ships. LGO says *"Description of
computational method:"* — prospective, about values a filer will supply.
Both are unfilled templates, so fill state is not the difference. One
**ships data with provenance notes**; the other **collects data with
instructions**, and only the first kind can state a relationship about
its own cells. H1 is not refuted here — it is **not addressable** here,
and reporting the file as evidence against H1 would count a workbook that
cannot answer the question as an answer.

**So the share has an empty denominator and no direction is stated.**
`diverged_share()` returns `None`, not `0.0` — zero would put a workbook
with nothing to measure at the good end of a scale it is not on.
`direction()` returns `NO_DIRECTION` and says why. n = 2 is printed, and
no curve is emitted.

**"File date" turned out to be two dates.** Both containers record a
created and a modified time, and on the legacy target they are **eight
years apart** (2008-06-04 / 2016-05-02) on a form whose filename states
the later one. The column is headed `created / modified` and carries
both; picking one would be a choice presented as a reading. Only the two
date properties are read — the same property set names a private
individual, and nothing reads it.

**One thing the order caught that was live.** `coupling.py` ranks by
elasticity where computable and by dependent count where not, which is
right on a readable workbook and is exactly S1's forbidden substitution
on a reader with no formula text. It printed a COUNT table under a
coupling heading with nothing saying the coupling arm had not run. It now
stops: `COUPLING IS NOT_RUN ON THIS WORKBOOK`, with what the reader does
supply, and the count ranking is **not** offered as a stand-in — the two
disagree on this repo's own evidence (`SSS_030`).

Scan three's finding on the legacy file: `total location-based scope 2
emissions` labels ten row blocks meant to be parallel sectors, and some
govern `1c+4d` while others govern `4d`. 9 of 17 repeated-label groups
listed, 8 agreeing on both axes.

## Work order 7: the selection screen, and no third workbook

**S1(b) named a test that did not exist.** *"Provenance prose classified
RETROSPECTIVE under the amended WO4 test"* — `SSS_043` drew that
distinction in prose, from two workbooks, and nothing implemented it.
`RETROSPECTIVE` and `PROSPECTIVE` appear zero times in this folder before
`selection.py`. Sixth instance of the stated-rule-with-no-field shape,
and building it is most of this order.

**The trap the classifier has to avoid** is that the easy version of (b)
— *does any prose cell yield a resolvable relationship* — **is** (c).
Two criteria computing one quantity is `category-weld`'s mechanism
inside the screen. So (b) reads **stance** and (c) reads
**resolvability**, and `independence()` reports whether they have ever
been observed disagreeing. **Off-diagonal: 0 of 3.** They have not, so
on this population the screen cannot say which criterion is doing the
work.

**And the threshold decides that.** `min_retro = 1` is a `[CHOICE]`, and
the UNFCCC calculator has RETRO 4 against **PROSP 9** — more than twice
as many prospective cells as retrospective ones, in the file carrying
every testable relationship this repository has found. A **majority
rule** calls it PROSPECTIVE and rejects at (b) the only workbook (c)
accepts. So the threshold is calibrated by a case rather than stipulated,
and under the majority rule that file **is** the off-diagonal cell:
whether (b) and (c) are independent is a property of the threshold.

**The reject log, and it is not the finding S1 expected.**

| candidate | a | b | c | d | e |
|---|---|---|---|---|---|
| UNFCCC calculator | pass | pass | pass | fail | fail |
| UNFCCC (byte-identical duplicate) | pass | pass | pass | fail | fail |
| LGO inventory report | fail | fail | fail | fail | fail |

Every criterion is recorded rather than stopping at the first failure,
and they separate cleanly: (a)–(c) are content criteria, (d)–(e) are
novelty criteria, and the prior file passes all of the first and none of
the second.

**No third candidate is reachable.** `www.epa.gov`, `unfccc.int`,
`theclimateregistry.org`, `www.eia.gov`, `data.gov` and
`www.ipcc-nggip.iges.or.jp` all return a refused CONNECT; only the GitHub
hosts respond, and trawling third-party repositories there is outside
this session's scope. Two of the three uploaded files are byte-identical,
so the distinct population is **two**. S1's own hypothesis — *if most
published workbooks fail (b) or (c), the population is small* — is
therefore untested, and **not because most workbooks fail: because none
could be screened.** That is `SSS_043` applied to this order's own
method.

All four S3 predictions return **NOT ADDRESSABLE**, which S3 makes a
legal verdict — the repair `SSS_043` argued for, arriving in the order
that follows it.

**S4's `OUT_OF_SCOPE` is built**, and its first implementation dropped
the row it exists to keep: a `continue` in the accumulation loop removed
out-of-scope workbooks from the denominator *and* from the table. Both
halves are asserted separately now. A second defect the `G1` fixture
caught: reading scope off the share's denominator calls a workbook whose
relationship **is** enforced by a formula out of scope — MAINTAINED
counts.

## Targets

`targets/TARGETS.md` pre-registers sixteen predictions across five
workbooks, before the data, with the argument that **the pair is the
test**: a flat-table result alone cannot separate *the scan works* from
*the scan reports everything flat*. One known-answer arm (the EPA
Emission Factors Hub, terminal constants by design) and three
live-calculator arms (EPA Local GHG Inventory Tool, UNFCCC calculator,
Climate Registry tool). `--selftest` requires **each** arm to
discriminate, since registering one that does not adds a name and no
evidence.

**First real run, 2026-08-25.** The UNFCCC calculator ran and holds 3 of
3 — but not on the first attempt: `UNF-P1` came back `0.037` against a
registered `> 0.20`, and the cause was the reader. 720 of the workbook's
825 formula cells are **shared formulas**, whose text lives once on a
group master, and the reader was reading the other **696 as constants**
(`SSS_017`). A threshold fixed before the file existed is what made a
reader defect the live hypothesis instead of a plausible, wrong story
about the workbook. After the repair: `0.226`, held by a small margin.

What the scans then found: **one sheet computes its emission factors
where eight hardcode them** (`Home Office`, `31d` at depth `{1}` against
`{0}` constants elsewhere), with the consequence visible one level deeper
in the output column — and two of the four differing occurrences per
group are stacked-table artifacts, checked and separated rather than
assumed clean. On the 22 cells scan three surfaced, `unit` is present on
22 and `date`, `sample_size` and `variance_sibling` are absent on 22.

The `.xls` target fired the registered contingency, and the slot stays
unspent for a reason: the file carries 336 `FORMULA` records and the one
reader for the format hands back cached values with no formula text
(`SSS_023`).

The remaining targets are **not read**. The egress policy here is an **allowlist**,
not a per-host block: `github.com` reaches the origin, `example.com`
does not, and all four target hosts return 403 to CONNECT — timestamps
in that file. Substituting a publisher does not help from inside this
session.

Building the criterion against a target-shaped fixture found two defects
first, one of which would have fired on the real Emission Factors Hub as
a finding (`SSS_011`).

## Ten choices

The delivery left ten parameters open. Each is marked `[CHOICE n]` at its
definition, has a default, and is printed into the report header when it
is in force — an absence measured at radius 2 and one measured at radius
6 are different readings. `SPEC.md` §5 is the table.

247 selftest checks across nine modules: `sheetmodel` 27,
`no_severity` 12, `scans` 36, `targets/epa_check` 30, `coupling` 36,
`scan4` 32, `xlsreader` 24, `selection` 26, `docreader` 24.

CC0. Stdlib only. Parses under Python 3.9.
