# encoding-selection

A pre-registered work order, delivered verbatim in `WORK_ORDER.md`: is
an encoding an instrument selection rather than a style, so that
encodings of one content are not rank-orderable on a single arrival-cost
axis? One stdlib file computes what the order's procedure asks for from
a flat CSV in its schema — Kendall's W by hand with a permutation null,
within- against between-format spread of the recovered-quantity set,
prose against the table class on dropped-axes naming — and applies the
order's own falsification lines.

**No data ships, and the seven encodings are not here.** They are the
experimental material and the order says they are a judgment call to be
published verbatim; the instrument validates an encodings file against
each item's fact list and refuses an added fact. The origin reader is
excluded by the order's own last limit.

    python3 encoding-selection/encoding_selection.py                          # unfilled
    python3 encoding-selection/encoding_selection.py --csv ROWS.csv --encodings ENC.json
    python3 encoding-selection/selftest_es.py

| step | function | reads |
|---|---|---|
| OUTPUT | `per_format` | n, recovered-quantity frequencies, dropped-axes rate, rank declines |
| H1 | `h1` / `kendall_w` / `w_null` | W over rankers on a common format set; declines counted apart |
| H2 | `h2` | mean pairwise Jaccard distance within and between formats, and across one reader's formats |
| H3 | `h3` | prose against the declared table class, every format printed |
| material | `check_encodings` | seven formats per item; carried / dropped over the fact list; added facts refused |

Four choices the order leaves open are `[CHOICE]`s printed on every
render. Both seed items are this repository's own artifacts, and M2
states the reading the trucking row withdrew on the order's own date
(`ES_005`).

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `encoding_selection.py` | the instrument, one stdlib file |
| `selftest_es.py` | known answers first, both directions; writes the samples |
| `CLAIM_TABLE.md` | `ES_001..ES_009` |
| `samples/` | constructed rows and encodings, the pinned renders |

The instrument refuses `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. No author section. Stdlib only,
parses under 3.9, runs on a phone, CC0.
