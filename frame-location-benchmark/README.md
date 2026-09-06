# frame-location-benchmark

`WORK_ORDER.md` is a delivered work order (verbatim, CC0). Existing reasoning
benchmarks supply a well-posed problem and score the answer. This one supplies
a problem that may be **mis-posed** and scores whether the mis-posing is
**named before an answer is produced** — under two or more **harness**
conditions (cold, and with a carried context file of prior positions and
corrections), in the ARC-AGI sense of a harness (scaffolding around the model,
not the model itself).

**Nothing here is a benchmark result.** The run — ARM 0..4 model responses,
the FL-3..FL-7 verdicts — requires model calls (none available) and is
egress-blocked. What this folder builds and verifies is the instrument: the
case set, the response contract, the pure-counting scorer, the frozen harness
arms with the mechanical contamination check, and the nulls. The build order
itself says stop at step 5 if FL-3 is refuted; steps 5–7 need the models.

## The response contract (Deliverable B — `protocol.md`)

Grading a free-text reframe requires a grader who can already do the reframe.
The contract forces a structured declaration first, so scoring is a **field
comparison, not a judgement**:

```
POSED: WELL | MIS
TARGET: <single term or variable, or NONE>
THEN answer.
```

Both verdicts are live; the model is not told the class distribution and the
contract does not name the fault-class list (C1–C4).

## The case set (Deliverable A — `cases.jsonl`)

40 cases, one JSON object per line: **19 WELL (47.5%)** and **21 MIS** (3 per
fault class), across **8 domains**. The requirements are enforced by
`validate_cases.py`:

- **R1** ≥ 40% WELL — the controls are load-bearing; without them "always
  declare MIS" wins the benchmark.
- **R2** no fault class > 25% of MIS cases (each is 14.3%).
- **R3** ≥ 3 domains, each fault class in ≥ 2 domains (cross-domain transfer,
  FL-5).
- **R4** every MIS case states in `notes` how the reframe is known; `source`
  recorded. **Every shipped case is `source=constructed`** — this environment
  cannot reach an external record to supply a field/published case
  (egress-blocked), so the honest state is that all are authored (§7 sampling
  absence: the set shows which faults can be constructed, not the field
  distribution).
- **R6** prompts are the stated problem only — no hedging, no hints.

The seven fault classes: `WRONG_INSTRUMENT`, `MISSING_DENOMINATOR`,
`UNSCOPED_CLAIM`, `UNIT_OF_ANALYSIS`, `PROXY_AS_QUANTITY`,
`SINGLE_EVENT_FRAME`, `ACCEPTED_SIDE`.

## The scorer (Deliverable C — `score.py`)

Pure counting, no model calls. Reads `cases.jsonl` + `runs/<arm>/<model>/
<case_id>.txt`. Per (arm, model): `posed_accuracy`, `false_positive_rate`
(the N1 ceiling check), `false_negative_rate`, `target_hit_rate` (the
headline), `target_miss_named`, `by_fault_class`, `by_domain`,
`malformed_rate`.

- **SCORING RULE**: a MIS case counts ONLY on `target_hit`. Calling MIS
  without locating the target is `target_miss_named` — detected the strain,
  mislocated it — and is **never** summed into the headline (FL-6).
- **N4**: every reported score carries its arm label; the renderer cannot emit
  a metric without its arm.
- **§9 open node**: the headline is reported constructed-**excluded** and
  constructed-**included**; here the excluded set has no denominator (`--`),
  because no field/published case is reachable, and the report says so.
- **Nulls** N1/N2/N3 are printed as instrument-status flags with `[CHOICE]`
  thresholds: N1 (FP high in every arm → measuring suspicion, instrument
  failure), N2 (ARM 0 near ceiling → too easy), N3 (ARM 4 < ARM 0 → a carried
  file over-fit the reader, reportable, not suppressed).

`false_positive_rate` is registered in `tools/known_answer.py` (perfect 0.0 /
all-MIS 1.0 / half 0.5).

## The harness arms (§4) and the contamination rule

The independent variable. Each arm is a text file prepended to the prompt;
nothing else differs. ARM 0 COLD (no file), ARM 1 FORMAT, ARM 2 POSITIONS,
ARM 3 CORRECTIONS, ARM 4 FULL (= 2 + 3, byte-exact). The four-arm split is the
point: a single with/without comparison returns "the file helped" and cannot
say what carried the effect (FL-4).

The **contamination rule is the load-bearing single point of failure**. No
harness file may contain a case's `prompt`, its `fault_target`, or a worked
instance of the same fault in the same `(fault_class, domain)`. Cross-domain
instances of a fault class **are** permitted — that is the transfer under
test. Harness files are frozen **before** cases (`FREEZE_LOG.md` logs the
freeze order); `validate_cases.check_contamination` enforces it mechanically
and is null-tested (a planted leak fires; the frozen harness is clean).

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | the delivered work order, verbatim |
| `cases.jsonl` | Deliverable A — 40 cases (19 WELL / 21 MIS), one JSON per line |
| `protocol.md` | Deliverable B — the response contract (C1–C4) |
| `score.py` | Deliverable C — the pure-counting scorer |
| `validate_cases.py` | R1–R6 + the §4 contamination check |
| `harness/arm1_format.txt` … `arm4_full.txt` | the frozen harness arms (ARM 0 is no file) |
| `FREEZE_LOG.md` | freeze order + ARM 3 correction coverage (the checker's reference) |
| `runs/` | CONSTRUCTED fixtures (ARM 0 / ARM 4, one FIXTURE model) — exercise the scorer, **not a result** |
| `selftest_flb.py` | 41 checks — the scorer, both nulls, the contamination check, the R-validators |
| `CLAIM_TABLE.md` | `FLB_001..FLB_011` (distinct from the marker's FL-1..FL-7) |
| `samples/flb_score.sample.txt` | one constructed score report |

## Run

```
python3 frame-location-benchmark/validate_cases.py   # R1-R6 + contamination
python3 frame-location-benchmark/selftest_flb.py     # 41 checks
python3 frame-location-benchmark/score.py            # score the constructed fixtures
python3 tools/known_answer.py                        # false_positive_rate known-answer
```

`score.py` refuses `--selftest` (rc 2). The score report screens clean through
`sheet-structure-scan/no_severity`. Stdlib only, parses under Python 3.9,
phone-buildable, CC0.

## Out of scope (§7, honored)

Answer quality, knowledge breadth, calibration, and anything about the author
or operator are **not measured**. There is no author, working-style, or
biography section anywhere. Cases carry the problem and the key, nothing else.
