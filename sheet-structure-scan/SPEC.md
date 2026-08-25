# SPEC — sheet structure scan

Two scans over a spreadsheet, ranked by how far a site propagates.
Written to the delivery in `SOURCE_DROP.md`, dated 2026-08-25. CC0.

---

## 0. THE TWO CONSTRAINTS, STATED IN THE SPEC AS ASKED

**C1 — stdlib plus one spreadsheet reader.**

The budget is one reader beyond the standard library. **It is unspent.**
`.xlsx` is a zip of XML and formulas sit in `xl/worksheets/sheetN.xml` as
`<f>` elements, so `zipfile` and `xml.etree` reach everything both scans
need. The slot stays open for a format the standard library cannot open,
and `sheetmodel.read()` raises with that sentence rather than widening
itself.

Frugality is the smaller half of the reason. The larger half: **both
scans are about the formula layer.** Precedent depth and
constant-versus-derived are properties of formulas, and the common
reader's value-only mode drops them. Reading the XML directly means the
layer under test cannot be silently discarded by the reader that was
supposed to deliver it.

**C2 — the tool never labels a site.**

There is no verdict column, no threshold, no ordering by consequence,
and no vocabulary of grading. Every column is a count, a set, or a string
lifted off the sheet.

This is enforced rather than asked for. `no_severity.py` screens 78 words
across two classes — severity (*error, critical, invalid, risk, flaw*)
and interpretation (*should, must, indicates, likely, fix, better*) — and
runs over the emitted table on every invocation. The selftest fails if a
screened word reaches the output, and the screen itself is null-tested in
both directions: known-null text passes, planted violations of each class
are caught, and `terror` / `mustard` / `bustle` are checked against
substring bleed.

The screen's limit is stated at the top of that file rather than at the
bottom: **a keyword screen is stepped around by any paraphrase.** What it
catches is the fluent failure — reaching for the ordinary vocabulary of
grading without noticing — which is the one that happens.

**Scope.** The constraint is on what the tool says about a *site on a
sheet*. It is not on what this spec says about the tool: a design
document that could not call its own neighborhood shape wrong would not
be able to record the fixture that refuted it. The screen runs over the
emitted table and over nothing else, and that boundary is the reason it
can be strict.

---

## 1. WHAT IS READ

A workbook becomes cells and one directed graph.

| per cell | |
|---|---|
| `kind` | `CONSTANT_NUMBER`, `CONSTANT_TEXT`, `CONSTANT_DATE`, `DERIVED` |
| `precedents` | cells the formula references, ranges expanded |
| `notes` | `PRECEDENTS_UNRESOLVED`, `PRECEDENTS_TRUNCATED`, `EXTERNAL` |

| per cell, from the graph | |
|---|---|
| `pdepth` | longest path back to a cell with no precedents; a constant is 0 |
| `deps` | direct dependents |
| `ddepth` | longest path forward; a terminal is 0 |
| `rank` | `deps × ddepth` |

**Not read, stated here rather than discovered later:** named ranges and
structured table references (a formula using one records
`PRECEDENTS_UNRESOLVED` for that term — an unread precedent and a cell
with no precedents must not land in the same bucket), external workbook
links, array formulas beyond their anchor, and merged regions beyond the
anchor cell.

---

## 2. SCAN TWO — COMPANION ABSENCE

> for every flagged cell, check the surrounding neighborhood for a unit
> string, a date, a sample size, or any variance-like sibling. Report
> what's missing rather than what's present.

Four companion kinds, each with three states:

| state | means |
|---|---|
| `ABSENT` | searched the neighborhood, no match |
| `PRESENT` | matched — renders as `-`, since the report's subject is absence |
| `NOT_SEARCHED` | no pattern registered for that kind |

`NOT_SEARCHED` is not decoration. Without it, a kind whose pattern list is
empty reads `ABSENT` on every cell in the workbook, and the report is
about the pattern file rather than about the sheet.

A separate `unsearched` column carries what the *search* could not cover:
`N`/`S` when the row band ran off the sheet, `no-col-label` when the cell
sits outside any label block, `no-row-label` when the sheet has no label
column. **An absence measured without a header is a different reading
from an absence measured with one, and the two must not print alike.**

Cells with nothing absent stay in the table. Dropping them would make the
denominator invisible, and a report of absences with no denominator
cannot be told from a report of a short flag list.

### The pattern lists are tuned toward reporting absence

Deliberately, and the asymmetry is the reason. A pattern that is too
loose produces a false `PRESENT`, which **removes a row from a report
whose whole subject is what is missing**. A pattern that is too tight
produces a false `ABSENT`, which adds a row the operator dismisses in a
second. So bare single-letter unit abbreviations (`m`, `s`, `t`, `c`,
`f`, `k`) are absent from the list: they would match ordinary prose and
silence real gaps.

A word list cannot read sense. `range` is a variance term in one column
and a spatial extent in another and nothing here tells them apart. Swap
`patterns.json` rather than widening the code.

---

## 3. SCAN THREE — HEADER COLLISION

> collect column and row labels across all sheets, group by normalized
> string, and flag any label whose cells differ in precedent depth or in
> whether they're constants versus derived. Same name, different
> construction.

Labels are grouped on `(normalized string, axis)`. A group with two or
more occurrences is listed when its occurrences differ in **depth set**
or in **construction**. Groups that agree are counted in the footer, not
dropped — again the denominator.

Construction is reported as a composition (`2c`, `3d`, `4c+1d`), not a
majority label. **A majority vote reports a column of nine constants and
one formula identically to a column of ten constants, and that one
formula is the whole of what "same name, different construction" is
about.**

---

## 4. RANKING

> dependent count times downstream depth, so the sites that propagate
> furthest sort to the top.

`rank = deps × ddepth`, per cell. For a label group, the sum over the
cells it governs.

**Two properties of that formula, stated because they are visible in
every run and are not defects:**

1. **Every terminal ranks 0.** A terminal propagates nowhere, which is
   what the formula measures. It is also, usually, the cell whose number
   somebody quotes. So the ranking orders by propagation and not by
   consequence, and near the bottom of a sheet the two run opposite.
   `pdepth` is a column, so the information is in the table; it is not in
   the sort.
2. **A cell in a cycle has no finite forward path** and ranks `CYCLE`,
   which sorts apart from every number rather than to the top or the
   bottom.

---

## 5. THE TEN PARAMETERS THE DELIVERY LEFT OPEN

Each is marked `[CHOICE n]` at its definition, has a default, and can be
overridden. The report header prints the ones in force for that run,
because an absence measured over a radius of 2 and one measured over a
radius of 6 are different readings.

| n | parameter | default | where |
|---|---|---|---|
| 1 | flag source | **none — refused** | `scans.py` docstring |
| 2 | neighborhood radius | 2 | `DEFAULT_RADIUS` |
| 3 | neighborhood shape | cross, not block | `neighborhood()` |
| 4 | label row / column | first majority-text row, then column | `label_row`, `label_col` |
| 5 | normalization | case, whitespace, edge punctuation; parentheticals kept | `normalize()` |
| 6 | construction | composition, not majority | `_construction()` |
| 7 | dependent count | direct, not transitive | `Workbook.rank` |
| 8 | range expansion cap | 4096 cells | `RANGE_CELL_CAP` |
| 9 | group rank | sum over governed cells | `_group_rank()` |
| 10 | cycle | named state, not a number | `precedent_depth` |

### 1 — the flag source, which is the one that matters

**Scan two begins "for every flagged cell" and scan one is not in the
delivery.** So the flag set is an input: a plain list of `Sheet!A1`
addresses. Running scan two without one is **refused**, not defaulted.

`--all` exists, is explicit, and prints its own provenance into the
report header (`--all: every non-empty cell, no upstream scan`).

Inventing a flagging rule here would put a framing in the operator's
mouth and then rank it — which is the one thing C2 exists to prevent.

### 3 — the neighborhood shape, which the fixture refuted

A square block of radius 2 **fails on this folder's own fixture**: the
`sd` column of a six-column table sits three columns from the flagged
cell, so a correctly built table reports its own variance sibling absent.
Widening the radius is the wrong repair — it reaches into the adjacent
record instead.

The shape is therefore a cross: the whole of the flagged cell's **row**
(one record), its **column** within ±radius rows (the neighbouring
records), and the **label-row cell above every column the row touched**,
because a unit, an `n` and an `sd` are named in the header and carried as
bare numbers underneath.

A sheet holding two tables side by side over-reaches on the row axis.
Stated, not hidden.

### 5 — normalization, and what the choice costs

Parentheticals are **kept**. `unit price (USD)` and `unit price` stay
distinct, because deciding that a unit annotation does not change what a
label names is a judgement about the sheet.

The cost is real and the fixture carries it: those two labels *are* the
same quantity at two constructions (constants on one sheet, derived on
another) and the scan does not list them. Stripping parentheticals would
list it — and would also merge `revenue (net)` with `revenue (gross)`.
The choice is the operator's; the default is the one that under-reports.

---

## 6. FALSIFIERS

| # | what would refute the design |
|---|---|
| F1 | a workbook where the cross neighborhood reports a companion absent that a human reading the same sheet finds within the block — the shape is wrong, not the radius |
| F2 | a `PRESENT` produced by a pattern matching a word in its other sense, hiding a real gap — the asymmetry argument in §2 fails |
| F3 | a listed collision whose occurrences a reader judges to be the same construction — depth set and composition do not capture construction |
| F4 | a workbook where the top of the rank column is not where the reader would start — the ranking measures something other than reach |
| F5 | a screened word reaching the emitted table, or a graded reading reaching it in words the screen does not hold |

F1–F4 need a real workbook, and none has been run against one. That is
the state, not a limitation to be argued around.
