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
every render. The render opens with the position line the order's first
paragraph asks for: this file is a row, not an exception.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `readout_count.py` | the instrument, one stdlib file |
| `selftest_rc.py` | known answers first, both directions of every guard; writes the samples |
| `CLAIM_TABLE.md` | `RC_001..RC_009` |
| `samples/` | constructed rows and the pinned renders |

The instrument refuses `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. No author section. Stdlib only,
parses under 3.9, runs on a phone, CC0.
