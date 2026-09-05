# model-deprecation-backcast

`WORK_ORDER.md` is a delivered instrument spec (verbatim, CC0): take
retired/deprecated models as a series, look **backwards**, and read
retirements against what was being pushed in that period — a capability
discarded under a fad that has since decayed either returns or does not,
which distinguishes fad-driven removal from cost-driven or load-bearing
removal. It is **an instrument specification, not a findings document, not a
critique**: "unmeasured cells are the content."

Every real input — vendor deprecation calendars, opinion polls, third-party
evals — is egress-blocked, so **nothing here is a result**. What the folder
builds is the instrument structure with the **null per column** enforced, and
the columns whose null is a quantitative shape made runnable on constructed
data, each null-tested in both directions.

## The load-bearing rule: a null per column

Each of the seven columns carries what it measures, where the record exists
and where it does not, the proposed test, and **THE NULL** — the condition
under which that column measures nothing. `instrument.py` encodes the seven
columns as structured objects and `validate_column` **refuses a column
missing its null** — the same discipline as `machine-record-format`'s
test-case format, and the reason `null-harness` exists one level up: a
readout nobody has seen measure nothing is not known to discriminate. Several
nulls name a **collapse** (C1→C2 if stated reasons match measured delta;
C7→C4 if per-turn cost is flat in ontological distance), recorded in the
collapse map.

## The runnable nulls (`null_check.py`)

- **C6, the fad-axis lag** — `lag_of_peak` is the argmax over L of the
  cross-correlation of discourse against discards at lag L (aperiodic series,
  so the lag is unique); registered in `tools/known_answer.py`.
  `c6_fad_driving` returns DRIVING (peak in the 18–24 mo band),
  DRIVING_OTHER_LAG (a peak outside it — the funding layer), or NOT_DRIVING
  (no peak — **the null: the fad axis is not driving**).
- **C1/C2 collapse**, **C4 tightening**, **C5 coupling**, **C7→C4 collapse** —
  each a small statistic whose null (no variation) reads nothing and whose
  signal reads something; each verdict reached by a constructed input.
- **C2 unrecoverable** — `c2_recoverable` returns a STATE, not an estimate,
  when eval coverage is too sparse to date deltas to version boundaries
  ("declared so rather than estimated").
- **C3 accepted-side censoring** — `c3_censoring` returns the recorded and
  paying-tier fractions: three exit forms (complainer / jumper /
  paid-then-lapsed), only the complainer leaves a record, so the complaint
  signal is a censored, paying-tier-filtered estimator.

## The guardrail clock (`guardrail_clock.py`)

A separate layer, not a column: safety/guardrail language moves on **news
time** while C1–C7 move on **training-cycle time**. `contamination_demo`
shows that pooling a news-time guardrail series into the discards flips the
C6 lag reading from the true in-band lag (DRIVING) to the guardrail's
news-time lag (DRIVING_OTHER_LAG); separating the clocks recovers it — the
work order's warning, demonstrated.

## Stated up front, not as a caveat

The sampling absence is in the instrument body (`SamplingAbsence`), not a
footnote: AI opinion by American Indian / Alaska Native respondents is **not
answerable** at national-panel sample designs (~0.8% of population, dispersed,
screening cost, census undercount) — the readout exists only where someone in
that position built the channel (Relational Futures, Māori health-record
bias, Te Mana Raraunga, Indigenous Protocol and AI). Carried, egress-blocked,
not verified. This is the `uninstrumented` / `generation-capacity` shape: a
quantity excluded by the instrument's constitution, not a gap.

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | the delivered instrument spec, verbatim |
| `instrument.py` | the seven columns + required null, guardrail clock, sampling absence, open node |
| `null_check.py` | the runnable per-column nulls + `lag_of_peak` + C3 censoring |
| `guardrail_clock.py` | the two-clock contamination demonstration |
| `demo_mdb.py` | a worked pass on constructed data, screened through `no_severity` |
| `selftest_mdb.py` | 36 checks — the columns, the nulls both directions, the lag, the contamination |
| `CLAIM_TABLE.md` | `MDB_001..MDB_008` |
| `samples/mdb_demo.sample.txt` | one constructed report |

## Run

```
python3 model-deprecation-backcast/selftest_mdb.py    # 36 checks
python3 model-deprecation-backcast/demo_mdb.py        # the worked pass
python3 tools/known_answer.py                         # lag_of_peak known-answer
```

Library modules refuse `--selftest` with rc 2. The demo screens clean through
`sheet-structure-scan/no_severity` with no exemption. Stdlib only, parses
under Python 3.9, phone-buildable, CC0.

## Out of scope, and open

No section about the author, no working-style profile, no characterization of
anyone whose case appears as an instance (OUT OF SCOPE, honored). The
fear/excitement-vs-discard-ratchet relation is held as an **open node**,
un-named and un-graded per instruction (`OPEN_NODE`). Nothing here is a
result; if someone runs a column against real data and its null fires, that
is a finding and should be posted.
