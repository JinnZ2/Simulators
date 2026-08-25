# RESULTS — first run

Dated 2026-08-25. Workbook: `fixture.py`'s three-sheet demo, generated at
run time. No real workbook has been scanned; every number below is a
property of the tool on a fixture built to carry one of each case.

Pinned output in `samples/`.

---

## Scan two, five flagged cells

```
rank  site        kind             pdepth  deps  ddepth  nbrs  absent                                  unsearched
3     Inputs!B2   CONSTANT_NUMBER  0       1     3       12    -                                       N
2     Model!C2    DERIVED          2       2     1       8     unit,date,sample_size,variance_sibling  N,S
0     Summary!B2  DERIVED          3       0     0       4     unit,date,sample_size,variance_sibling  N,S
0     Model!D2    DERIVED          3       0     0       8     unit,date,sample_size,variance_sibling  N,S
0     Inputs!B9   CONSTANT_NUMBER  0       0     0       0     unit,date,sample_size,variance_sibling  no-col-label
```

Four of five carry an absence. `Inputs!B2` carries none — it has a unit
in its header, a date, an `n` and an `sd` across its row — and it is in
the table on purpose: **a scan that reports everything absent everywhere
passes a one-armed test.**

`Inputs!B9` reports `no-col-label`: it sits eight rows below the table
with blank rows between, so it is not under the header that would have
supplied its unit. That is the distinction between an absence measured
with a header and one measured without.

## Scan three, three collisions listed of four groups

```
rank  label   axis    as written  label at    governs        depths   construction
9     widget  row     widget      Inputs!A2   Inputs!B2:F2   {0}      5c
                      widget      Model!A2    Model!B2:D2    {1,2,3}  3d
                      widget      Summary!A2  Summary!B2     {3}      1d
9     gadget  row     ...
4     total   column  total       Inputs!F1   Inputs!F2:F3   {0}      2c
                      total       Model!C1    Model!C2:C3    {2}      2d
                      total       Summary!B1  Summary!B2:B3  {3}      2d
```

`item` appears on all three sheets governing text constants at depth 0
and is **not** listed. It is counted in the footer instead. A scan that
lists it is listing repetition rather than collision, and the footer is
what keeps the denominator visible.

---

## Four results worth stating

**1. The neighborhood shape was refuted by the fixture, and the radius
was not the problem.** A square block of radius 2 reports the `sd` column
of a six-column table absent, because it sits three columns away. Radius
6 reaches it and also reaches the record above and below. The repair is
the shape — a cross over the record, the column band, and the label row —
not the size. Recorded because a design decision was overturned by a
fixture that is checked in.

**2. The flag set decides the report more than the scan does, measured.**

| flag source | rows | carry an absence | of those, label cells | strays outside a table | values in a table |
|---|---|---|---|---|---|
| five-cell list | 5 | 4 | 0 | 1 | 3 |
| `--all` | 38 | 23 | 13 | 2 | 8 |

Under `--all`, **15 of 23 absence rows are not values in a table.** The
largest single class is label cells: a header reading `unit price (USD)`
is not itself under a header, and its own text is excluded from its own
neighborhood, so it reports `unit` absent. That is why `is-label` is a
marker in the `unsearched` column rather than a suppression — deciding
that a header is not a site is the operator's reading, and the tool says
which rows are headers instead of removing them.

The composition is pinned in the selftest, so it cannot drift out from
under the argument.

**3. Every terminal ranks 0, and terminals are the cells people quote.**
`Summary!B2` sits at the end of a four-deep chain and ranks last, tied
with an unused stray constant. `deps × ddepth` measures propagation, and
propagation is what the delivery asked for — but near the bottom of a
sheet, propagation and consequence run opposite. `pdepth` is a column, so
the information is in the table; it is not in the sort. Not a defect,
and not a fix to be applied quietly.

**4. The row axis collides once per record, not once per table.**
`widget` and `gadget` are the same collision reported twice, because
every row of a three-row table has the same construction pattern. A
five-hundred-row table would produce five hundred identical group rows.
The cheap mitigation — collapse row-axis groups whose occurrence
signature is identical — changes the delivered grouping rule, so it is
named here and not built.

---

## The targets

Five real workbooks across three publishers are named and **none has
been read.** The denial is an **allowlist**, not a per-host block:
`www.epa.gov`, `unfccc.int`, `theclimateregistry.org` and `example.com`
all return 403 at CONNECT while `github.com` reaches the origin, with
DNS resolving for all of them. So substituting a publisher does not help
from inside this session, and there is no third host worth trying.
Reported rather than routed around; a mirror on an allowed host was not
sought, because that is circumventing the denial rather than complying
with it.

What was done instead is in `targets/TARGETS.md`: the Emission Factors
Hub arrived with the standard *if the scan does not light that up, the
scan is broken*, and that standard had no value attached. Sixteen
predictions are now registered — six for the Hub, and P1–P3 for each of
three live-calculator arms (EPA Local Tool, UNFCCC calculator, Climate
Registry tool) plus P4 for the one whose modules were named in advance —
with the argument that **the pair is the test**, since a Hub run alone
cannot separate *the scan works and the Hub is flat* from *the scan
reports everything flat*. The selftest requires **each** arm to
discriminate: a second one that does not adds a name and no evidence.

**Building the criterion found two defects, and one of them would have
fired on the real Hub as a finding.** Two flat sheets sharing their
headers over twelve and nine rows returned constructions `12c` and `9c`,
which differ, so five column collisions were listed on a fixture where
nothing collides — and the Hub is exactly that shape. The delivered spec
asks *whether* the cells are constants versus derived, and whether is a
set; the listing decision now takes the kind set and the counts stay in
the printed column (`SSS_011`). The other: a share passed on an empty
denominator (`SSS_012`).

The synthetic profiles the criterion separates:

| readout | flat two-sheet table | three-sheet chain |
|---|---|---|
| `derived_share` | 0.000 | 0.444 |
| `rank_zero_share` | **1.000** | 0.556 |
| `max_pdepth` | 0 | 4 |
| `unit_present` | 1.000 | 1.000 |
| `variance_present` | 0.000 | 0.000 |
| `listed_col_count` | 0 | 1 |

Those two workbooks were written here. **Nothing in them is evidence
about any EPA product**, and a criterion that separates two shapes
written by one hand has not been shown to separate two written by
another.

## FIRST REAL RUN — 2026-08-25

Two files arrived. `SSS_010` is closed.

**UNFCCC GHG emissions calculator ver 01.1** (`.xlsx`, 19 sheets, 3656
cells) — the pre-registered check, against thresholds pushed two commits
before the file existed:

```
UNF-P1  derived_share    > 0.2      0.226     HELD
UNF-P2  rank_zero_share  < 0.95     0.461     HELD
UNF-P3  max_pdepth       > 2.0      5.000     HELD
```

**It did not hold on the first run.** `UNF-P1` came back `0.037`,
`NOT_HELD`, and the reason was the reader, not the workbook: 720 of the
825 formula cells are **shared formulas**, which store their text once on
a group master and carry only an index on every follower. The reader
took an empty `<f>` body as no formula and read **696 cells as
constants** — 129 derived instead of 825, which is exactly the 105 plain
formulas plus the 24 masters that carry text.

That is what a threshold fixed in advance is for. `derived_share = 0.037`
on a workbook described as a live calculator has an available and wrong
reading — *this is mostly reference tables* — and nothing to argue with
it. What made a reader defect the live hypothesis instead was `UNF-P2`
and `UNF-P3` holding in the same run: the scan was finding propagation,
just not enough of it.

The diagnostic that found the defect **was itself wrong in the same
direction** (`SSS_018`): a regex counting `<f>` elements, whose `[^>]*`
swallowed the `/` of self-closing tags and merged them with the next real
one, reporting 476 against a parse's 825. Both errors undercounted, so
the diagnosis survived by luck.

### What the scans found

**Scan three: 4 groups listed of 33.** The substantive one is `factors`,
appearing as a column label on 11 sheets. Eight carry pure constants at
depth `{0}` — lookup tables. **`Home Office` carries `31d`, pure derived,
at depth `{1}`: that sheet computes its emission factors where eight
others hardcode them.** The consequence shows downstream in the `kg CO2e`
output column, which sits at depth `{1}` on nine sheets and at `{2}` on
Home Office.

Two of the four differing occurrences per group are **artifacts with a
named cause** and were separated rather than assumed clean: `Electricity,
heat, cooling` and `Water` stack more than one table in a column, and
`CHOICE 4` assumes one label row per sheet, so `governed()` runs through
the second header. Measured by counting cells in each governed range
whose text normalizes to the group's own label — two sheets return 2 and
1, the other nine return 0.

**Scan two, on the 22 cells scan three surfaced** (flag set produced by
an upstream scan, not invented for the occasion):

| companion | present | absent |
|---|---|---|
| `unit` | **22** | 0 |
| `date` / `sample_size` / `variance_sibling` | 0 | **22** |

Uniform. The factor and result columns carry a unit and carry no vintage,
no sample size and no uncertainty within reach — which is the differential
the Emission Factors Hub was offered to demonstrate, appearing on a
workbook that is not the Hub.

**The Climate Registry LGO Standard Inventory Report** (`.xls`) — the §5
contingency fired as registered. The slot stays unspent for a reason: the
file is valid BIFF8 carrying 336 `FORMULA` and 23 `SHRFMLA` records, and
`xlrd` 2.0.2, the one reader for the format, exposes cached values and no
formula text. Spending the budget on it delivers exactly the value-only
view `SSS_001` named as the reason to parse XML directly. LibreOffice is
installed, fails on this file, and fails identically on a control this
tool parses — so the install is broken here and that result says nothing
about the `.xls`.

## What has not been run

The Emission Factors Hub — the known-answer arm — and the EPA Local
Tool. One of three discriminator arms has run. Falsifiers F1–F4 in `SPEC.md` §6 all need one, and
until then the tool is checked against a fixture written by the same hand
that wrote the scans. That is the same weakness `membership-probe`'s
LIMITS section names about its own selftest, and it is stated here for
the same reason: passing is weaker evidence than failing.
