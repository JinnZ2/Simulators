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

And the result the substitution is for. Under a stated case, **3
constants have non-zero coupling and 781 have exactly zero — and every
one of those 781 ranks non-zero under dependent count, up to 380.**

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

133 selftest checks across five modules: `sheetmodel` 26,
`no_severity` 11, `scans` 35, `targets/epa_check` 29, `coupling` 32.

CC0. Stdlib only. Parses under Python 3.9.
