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
| `patterns.json` | companion patterns for scan two. Swap this, not the code |
| `fixture.py` | the demo workbook, written as a readable table |
| `samples/` | one pinned run of each |

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

## Ten choices

The delivery left ten parameters open. Each is marked `[CHOICE n]` at its
definition, has a default, and is printed into the report header when it
is in force — an absence measured at radius 2 and one measured at radius
6 are different readings. `SPEC.md` §5 is the table.

66 selftest checks across three modules: `sheetmodel` 25, `no_severity`
11, `scans` 30.

CC0. Stdlib only. Parses under Python 3.9.
