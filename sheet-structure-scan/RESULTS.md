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

## The EPA targets

Three real workbooks were named and **none has been read**: the egress
gateway answers 403 to CONNECT for `www.epa.gov`, logged
2026-08-25T15:14:12Z–15:14:13Z with DNS resolving normally, so it is a
policy denial and not a network fault. Reported rather than routed
around.

What was done instead is in `targets/EPA.md`: the Emission Factors Hub
arrived with the standard *if the scan does not light that up, the scan
is broken*, and that standard had no value attached. Ten predictions are
now registered — six for the Hub, four for the Local Tool — with the
argument that **the pair is the test**, since a Hub run alone cannot
separate *the scan works and the Hub is flat* from *the scan reports
everything flat*.

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

## What has not been run

No real workbook. Falsifiers F1–F4 in `SPEC.md` §6 all need one, and
until then the tool is checked against a fixture written by the same hand
that wrote the scans. That is the same weakness `membership-probe`'s
LIMITS section names about its own selftest, and it is stated here for
the same reason: passing is weaker evidence than failing.
