# WORK-ORDER ASSESSMENT

Candidates that fall out of the two reports and this audit. These are
proposals for the operator to accept, change or drop. None is started.

| id | work order | buildable here? | why | first deliverable |
|---|---|---|---|---|
| SAL-WO1 (DONE) | **Analytic null beside every scan.** For a declared generator, compute the expected flag count in closed form, e.g. (n−1)·P(\|ΔU\|>θ), and print it next to any real scan, so a real count is read against an expectation rather than against a demo. | yes | SAL_004: the shipped null is a constant of the generator. A closed form makes it a known answer instead of a figure. | `null_expectation()` registered in `tools/known_answer.py`, with uniform and normal cases |
| SAL-WO2 | **`confound_record` type** (the report's own top recommendation). One record per alternative explanation: test applied, result, status, version stamp. Same no-verdict schema. | yes | Thread B's ten-confound list is still prose. The record makes "which explanations were tested" countable. | schema, validator and tests, kept apart from the coupling scan as the report asks |
| SAL-WO3 | **First real-data scan.** Run all four 0.3 procedures unchanged on one documented real series, append the records, and read them against WO1's expectation. | yes, if a series is chosen | SAL_010: nothing has touched real data. The series must be one whose bytes are in the tree: `notes/datasets/` indexes the UCI `mechanical-analysis` set, but its bytes are not checked in. | one appended stream plus a short reading note |
| SAL-WO4 | **ETH live-claim registry.** The report's three-record tracking protocol (UNKNOWN status, appended events, nothing edited in place), started now with today's anchors. | yes (records only); updates need egress | The claim is one day old. The time each claim spends in each state is the measurement, and it can only be recorded going forward. | `claims/eth.jsonl` with the first `audit_event` per claim, Anthropic item marked NOT_LOCATED |
| SAL-WO5 | **Fold the lab into the repo's tools rather than run it beside them.** The transition engine overlaps `null-harness` (null runs), `claim-record` (append-only, no-verdict) and `criteria-drift` (versioned rulers). | assessment only | Two record schemas with one rule invite drift. | a mapping table, then a decision for the operator: keep separate, adapt, or merge |

Suggested order: WO1 (small, fixes the shipped null), then WO2, then WO3.
WO4 is time-sensitive if the operator wants the ETH case tracked from day one.

## Status

- **SAL-WO1 done.** `null_expectation.py` gives the closed-form expected
  flag count. Uniform: (n−1)(1−θ/w)². Normal: (n−1)·erfc(θ/2σ).
  - A relative threshold returns NOT_DERIVED and a single case returns
    NO_DENOMINATOR; neither is ever read as 0.
  - Checked against the lab's own unmodified `null_baseline_scan` at 4,000
    replications (closed form, then recorded mean):

    | noise and threshold | closed form | recorded |
    |---|---|---|
    | uniform, θ = 10 | 8.910 | 8.852 |
    | uniform, θ = 60 | 1.760 | 1.748 |
    | normal, θ = 7 | 3.544 | 3.528 |

  - Registered in `tools/known_answer.py` as
    `scope-audit-lab/null_expectation.py::from_generator`.
  - Spread across replications is not derived: adjacent pairs share a case.
