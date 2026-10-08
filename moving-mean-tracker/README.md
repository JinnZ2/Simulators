# moving-mean-tracker

**STATUS: PROPOSED instrument. No data yet.** The only provider is
synthetic (`provider.FixtureProvider`), and nothing in this folder measures
any population.

**SELF-GRADED.** `test_tracker.py` and the modules it tests share an
author. A green run shows that the code does what that author wrote it to
do. It does not show that the instrument measures what it claims to.

The delivered texts are landed verbatim: `SPEC.md` (the spec) and
`WORK_ORDER.md` (the dispatch).

## What it tracks

A mean anchored to a moving target (GDP, a wealth gap, a skills or literacy
score) moves with the target. Any norm, filter or loss tied to that mean
inherits the drift. This instrument records the drift per segment, with
per-record provenance, on a fixed schedule. It does not interpret it.

```text
provider ──records + provenance──► assign to segments (frozen rules, hashed)
   (dumb: no stats,                     │
    no scoring)          kept ──────────► n · mean · median · p10 · p90 · mean−median
                         dropped ───────► count per segment, each with its rule
                                         │
run entry ──append, sha256-chained──► run log ──series──► G1 G2 G3 G4
```

| gauge | per run, per segment | reads as |
|---|---|---|
| G1 | mean − median | tail pull on the reference |
| G2 | sample share − population share | access-gate loop running |
| G3 | dropped / (dropped + kept) | cleaning acting as a class filter |
| G4 | dollars per physical unit; across runs (dollar mean ratio / physical mean ratio) − 1 | token drift vs real change |

## States, never zeros

| state | when |
|---|---|
| `UNRATED` | G2 for a segment whose axis has no population reference that is named AND dated, or whose reference gives no share for that segment |
| `INSUFFICIENT_SAMPLE` | the segment has fewer than `min_n` kept records. No stats, no G1 or G4; n only |
| `NOT_DECLARED` | G4 for a metric with no declared physical unit |
| `CROSS_VERSION` | a delta across a change in segment definitions or metric declarations. No delta is computed |
| `None` | a share with an empty denominator (no kept, assigned records on the axis) |

## Refusals (`TrackerRefused`, naming what is missing)

- A config without metrics or segments is refused. A run dated before the
  config's `declared` date is refused.
- A segment rule set whose hash changed under the same version label is
  refused, and so is a metric change under the same `config_version`. A new
  version label is accepted, and every delta across it reads
  `CROSS_VERSION`.
- A dropped record with no `drop_rule` is refused. A kept record with no
  value for a declared metric is refused, because excluding it silently
  would be a drop with no rule.
- A record that matches two segments on one axis is refused.
- A period already in the log is refused: runs are appended, never
  overwritten. Appending to a log whose hash chain fails is refused.
- A run for a period other than the next one is accepted and stamped
  `OFF_SCHEDULE`, with the expected period beside it ([CHOICE 6]).

## Files

```text
tracker.py            config, assignment, stats, run log, gauges, render, CLI
provider.py           Provider interface + FixtureProvider (synthetic)
config.example.json   fixture config: axes band (with reference) and region (without)
test_tracker.py       the dispatch's four tests first, then the rules
SPEC.md, WORK_ORDER.md  delivered, verbatim
CLAIM_TABLE.md        MMT_001..MMT_010
samples/              four-run fixture log, its gauges render, the knobs and the v2 config
```

## Run

```text
python3 test_tracker.py
python3 tracker.py --validate config.example.json
python3 tracker.py --run config.example.json --period 2026Q4 --run-at 2026-10-08 --log LOG.jsonl
python3 tracker.py --run config.example.json --period 2027Q1 --run-at 2027-01-08 --log LOG.jsonl \
        --fixture samples/fixtures/tail_high.json
python3 tracker.py --gauges LOG.jsonl
python3 tracker.py --verify LOG.jsonl
python3 tracker.py --choices
```

`samples/run_log.sample.jsonl` was produced by exactly these steps:

1. 2026Q4, baseline.
2. 2027Q1, tail on the high band.
3. 2027Q2, tail plus half the low band dropped as noise.
4. 2027Q4, the same knobs under band-v2. That run is OFF_SCHEDULE, because
   2027Q3 was skipped.

`samples/gauges.sample.txt` is its render.

## Adding a live provider

Subclass `provider.Provider` and implement `pull(period, pull_date)`. It
returns records in the shape documented at the top of `provider.py`.

- The provider returns records and provenance only.
- If the source drops records as noise, return them flagged `dropped` with
  the source's rule. Do not omit them.

Candidate domains named in the spec are distributional accounts, adult
literacy and skills surveys, and training-text snapshots (filtered vs
unfiltered). None is wired. The spec says to confirm each source before
use.

Stdlib only, parses under Python 3.9, CC0.
