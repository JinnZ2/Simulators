<!-- SPDX-License-Identifier: CC0-1.0 -->
# FWO-14 -- Reference-instability series (DESIGN ONLY; nothing run)

Status: DESIGN_WRITTEN. No row below is sourced, no series is read, no G(t)
snapshot is computed. Every candidate row is CANDIDATE_UNSOURCED, recalled in
session with no document reached (the egress allowlist refuses every
central-bank, statistical-agency and treasury host; the probe record is in
`SOURCES.md`). The order says SOURCE per row; a row without one is listed so
that the shape of the enumeration is visible and is marked so that it cannot
be quoted as a fact.

Her framing (OBSERVED, carried): a structural reference that changes shape
periodically is not a reference. It is like concrete that changes shape
mid-span.

## 1. The row type

```
redefinition {
  date            ISO date, or a year with the precision stated
  what_changed    one of: anchor | convertibility | regime | operating_target | index_method | accounting_boundary
  decided_by      an institution, never a person
  series_crossing which long-run series denominated in the unit run through the change
  adjusted        per series: ADJUSTED_FOR (how) | NOT_ADJUSTED | UNKNOWN
  source          required; CANDIDATE_UNSOURCED until a document is read
}
```

`what_changed` carries six classes because the order names three (anchor,
convertibility, governing regime) and the metrology comparison it asks for
adds three the physical case has: the operating target (what the standard
is realised against), the method of the index that measures in the unit,
and the boundary of what the unit's own accounts count. A change in any of
the six is a change of standard for a series denominated in the unit.

## 2. Candidate rows (CANDIDATE_UNSOURCED, in date order as recalled)

| date | what_changed | decided_by | series crossing | adjusted? |
|---|---|---|---|---|
| 1971-08 | convertibility (dollar-gold window closed) | US executive | every dollar series | UNKNOWN |
| 1971-12 | anchor (par value reset under a multilateral agreement) | treasuries, multilateral | exchange-rate series | UNKNOWN |
| 1973 | regime (float; the par-value system ends in practice) | treasuries, central banks | exchange-rate and reserve series | UNKNOWN |
| 1976-1978 | regime (float legalised in the international monetary articles) | IMF membership | as above | UNKNOWN |
| 1979-1982 | operating_target (reserve targeting adopted, then abandoned) | US central bank | rate and money-stock series | UNKNOWN |
| 1993 | operating_target (money-stock targets formally set aside) | US central bank | money-stock series | UNKNOWN |
| 1999 | index_method (geometric-mean formula in the consumer price index) | US statistical agency | every real-dollar series deflated by it | UNKNOWN |
| 2002 | index_method (chained consumer price index introduced) | US statistical agency | as above | UNKNOWN |
| 2008 | operating_target (interest on reserves; balance-sheet operations) | US central bank | rate series | UNKNOWN |
| 2012 | regime (explicit numeric inflation target) | US central bank | rate and price series | UNKNOWN |
| 2013 | accounting_boundary (research and development capitalised in the national accounts) | US statistical agency | output and productivity series | UNKNOWN |
| 2020 | regime (average-inflation targeting) | US central bank | price series | UNKNOWN |

Twelve candidates, none sourced, none dated finer than the recall allows.
Rows the recall is least sure of are the 1976-1978 and 1979-1982 pairs,
which may each be two rows. Nothing is added to make the table look
complete; a complete enumeration is the run, and the run is not done.

## 3. The design question, as a measurement

For a long-run series S denominated in the unit (a wage series, a price
series, a debt series, an output series), the two quantities are:

```
crossings(S)  = number of redefinition rows whose date lies inside S's span
                AND whose series_crossing names S's class
adjusted(S)   = the vector of `adjusted` values for those rows, never summed
```

The comparison the order asks for is with physical metrology. When the
metre or the kilogram was redefined, every series in the unit carries a
documented correction with a stated uncertainty across the change, and the
old realisation stays traceable to the new one. The design test is whether
any economic series carries, at each of its crossings, (a) a documented
correction, (b) a stated uncertainty of that correction, (c) traceability of
the pre-change values to the post-change standard. A series carrying all
three at a crossing reads ADJUSTED_FOR; one carrying none reads
NOT_ADJUSTED; one whose documentation cannot be reached reads UNKNOWN. The
expectation is not registered, because no series can be read here; the
`labor-statistic-instrument-drift` comparison the order names is the same
instrument-change problem applied to the unit itself, and that folder is
not in this tree.

## 4. G(t): the dependency topology at seven dates

Nodes and edges are FWO-5's: a node is a dependency category, an edge is a
route carrying FWO-8's `edge_class` and `coupling_side`. A snapshot G(t) is
the three FWO-5 cases (or their period-appropriate equivalents) re-coded as
of t in {1971, 1980, 1990, 2000, 2010, 2020, 2026}.

Per snapshot, the readouts kept apart:

```
independence band      FWO-5's [lo, hi] over routed dependencies
DIRECT count           FWO-8 tally
RECURSIVE count        FWO-8 tally
selection-layer rows   FWO-8 layer_rows(G, "selection")
survival-layer rows    FWO-8 layer_rows(G, "survival")
conversion points      FWO-5 ordering, plus FWO-13's tax_step
```

The direction is not assumed. Three readings are each possible and each has
a falsifier stated before any snapshot exists:

- coupling INCREASED: the independence band's low end falls monotonically
  across the seven dates; refuted by any two consecutive snapshots where it
  rises.
- coupling DECREASED: the low end rises; refuted symmetrically.
- coupling CHANGED FORM: the band is flat within one dependency of itself
  while the edge-class tally moves (e.g. ACCESS falling and RECURSIVE or
  TEMPORAL rising); refuted if the tally is flat too.

A snapshot needs the period's own routes coded from a period document with
SOURCE; a snapshot coded from memory would be seven copies of one session's
reading with dates attached, which is the key-holder failure the packet
names, so no snapshot is coded here.

## 5. What would move this from DESIGN to BUILT

1. one reachable document per candidate row (a treasury release, a central
   bank statement, a statistical-agency methodology note), read, with the
   row's `source` filled and its date confirmed or corrected;
2. one long-run series with its methodology history, read, so `adjusted` can
   take a value other than UNKNOWN at each crossing;
3. one period document per G(t) date for one of the three cases.

None of the three is reachable from this session.
