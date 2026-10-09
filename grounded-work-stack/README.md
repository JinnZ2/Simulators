# grounded-work-stack

An outside deep-research report (Kimi, delivered as
`OKComputer_Unit-Conservation_Gates__Latency_Tools.zip`) on a four-element
framework:

1. unit-and-conservation gates;
2. pre-signal readers;
3. latency-in-the-joins;
4. an anchored channel for worker corrections.

The report and its four figures are landed verbatim:

- `REPORT.md`
- `figs/`

The test file pins their sha256. `check.py` recomputes what is recomputable
from the report's own text (`GWS_001..012`). It edits nothing.

## What the checker finds

**Holds (4).**
- The Mars Climate Orbiter conversion factor.
- The Asana shares.
- The 70% alert cut.
- The I-PASS counts.

**Four tensions or conditions inside the report.**
- **GWS_004.** "Nine workweeks" of 1.8 h/day needs a 200-day year that the
  report never states.
- **GWS_005.** The text's "90–96%" override range excludes a 53% bar in its
  own fig3. The same figure draws a 49–96% range as one 90% bar.
- **GWS_006.** The same override rate is read as "physicians usually right"
  in §5.3 and as a lost signal in §9.
- **GWS_008.** "Four working examples": the count matches the §5 table, but
  the four names in the sentence do not. Two of those names are, by the
  table, not working for corrections.

**Reading (GWS_007).** The conclusion reads one trial's 30% reduction as the
place where "a third of the harm lives". That is a lower bound, not a
location.

**In-tree cross-map (GWS_011).** Each element already has an instrument
here:
- G-DIM in `reasoning-gate/`;
- `tools/presignal_ledger.py`;
- `reporting-chain-loss/`;
- `return-path/`.

Two of these are partial. G-DIM checks units, not conservation.
`reporting-chain-loss/` prices information lost per hop, not time.

## Limits

- **Citations are carried, not read.** The report has 79 URLs over 64
  hosts; egress here is an allowlist.
- **Fig3 values are a hand transcription.** They are declared in
  `FIG3_BARS`.
- **One `no_severity` exemption:** "alert/alerts", the report's own subject.
  It is measured in three arms in `test_check.py`.

## Running

`check.py` refuses `--selftest`.

    python3 check.py
    python3 test_check.py

Stdlib only, parses under 3.9, CC0.
