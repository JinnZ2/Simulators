# readout-count

A pre-registered work order, delivered verbatim in `WORK_ORDER.md`:
does a safety regime's incident rate track the count of operator
positions with a protected channel that RETURNS, rather than its stated
culture or its data volume? One stdlib file computes what the order's
procedure asks for from a flat CSV in its schema and applies the
order's own falsification lines to the numbers.

**No data ships.** The five seed rows in the order carry no URL and
their count cells are grades, bounds and dashes; the instrument reads
them back from the order and reports each against what a row carries
before it counts, filling nothing in.

    python3 readout-count/readout_count.py                   # unfilled, with the seed readiness table
    python3 readout-count/readout_count.py --csv ROWS.csv    # the numbers
    python3 readout-count/selftest_rc.py                     # the checks

| step | function | reads |
|---|---|---|
| P2 | `derive` | readout_count = distinct positions_returning; declared_count; return_rate (None on empty) |
| OUTPUT | `per_regime` | latest year per regime, external_detection_rate over its rows |
| H1 | `h1` | Spearman rho by hand across ≥ 4 regimes; strict rank equality printed, not used |
| P4 | `cross_tabs` | Cramér's V (imported from `label-position-test`) with the level count beside it |
| H2 | `h2` | declared-high / return-low arm against high-return arm, median splits |
| H3 | `h3` | NOT_COMPUTABLE from the schema, both missing columns named |
| seed | `seed_rows`, `seed_readiness` | the order's own table, cell by cell |

Four choices the order leaves open are marked `[CHOICE]` and printed on
every render.

**The trucking row.** `TRUCKING_ROW_v0_1.md` corrects the parent's own
seed row: the channel that exists is a complaint channel, not a readout
channel, and the count is 0.5 on one partial-return equipment channel.
`row_audit.py` shows the row's coding rule has one conjunct the schema
cannot record (the row's own `type` column is the missing field), that
the 0.5 is a per-position partial return the schema's list cannot hold
(the row loads at 1, never 0.5), that the row is refused on the one
cell its own STILL NEEDED list opens with, that five of seven source
entries carry a URL and the count rests on a deferred one, and that the
row's "(N4)" points at nothing in the parent order. The render opens with the position line the order's first
paragraph asks for: this file is a row, not an exception.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `readout_count.py` | the instrument, one stdlib file |
| `selftest_rc.py` | known answers first, both directions of every guard; writes the samples |
| `TRUCKING_ROW_v0_1.md` | the first filled row, delivered verbatim: sourced, coding rule stated, count 0.5 |
| `row_audit.py` | the row against the instrument: rule vs schema, what the 0.5 is, the load attempt, sources, the (N4) pointer, the seed cells |
| `CLAIM_TABLE.md` | `RC_001..RC_016` |
| `samples/` | constructed rows and the pinned renders |

The instrument refuses `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. No author section. Stdlib only,
parses under 3.9, runs on a phone, CC0.
