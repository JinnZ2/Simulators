# WORK-ORDER ASSESSMENT

Candidates that fall out of the two reports and this audit. These are
proposals for the operator to accept, change or drop. None is started.

| id | work order | buildable here? | why | first deliverable |
|---|---|---|---|---|
| SAL-WO1 (DONE) | **Analytic null beside every scan.** For a declared generator, compute the expected flag count in closed form, e.g. (n−1)·P(\|ΔU\|>θ), and print it next to any real scan, so a real count is read against an expectation rather than against a demo. | yes | SAL_004: the shipped null is a constant of the generator. A closed form makes it a known answer instead of a figure. | `null_expectation()` registered in `tools/known_answer.py`, with uniform and normal cases |
| SAL-WO2 (DONE) | **`confound_record` type** (the report's own top recommendation). One record per alternative explanation: test applied, result, status, version stamp. Same no-verdict schema. | yes | Thread B's ten-confound list is still prose. The record makes "which explanations were tested" countable. | schema, validator and tests, kept apart from the coupling scan as the report asks |
| SAL-WO3 (DONE) | **First real-data scan.** Run all four 0.3 procedures unchanged on one documented real series, append the records, and read them against WO1's expectation. | yes, if a series is chosen | SAL_010: nothing has touched real data. The series must be one whose bytes are in the tree: `notes/datasets/` indexes the UCI `mechanical-analysis` set, but its bytes are not checked in. | one appended stream plus a short reading note |
| SAL-WO4 (DONE) | **ETH live-claim registry.** The report's three-record tracking protocol (UNKNOWN status, appended events, nothing edited in place), started now with today's anchors. | yes (records only); updates need egress | The claim is one day old. The time each claim spends in each state is the measurement, and it can only be recorded going forward. | `claims/eth.jsonl` with the first `audit_event` per claim, Anthropic item marked NOT_LOCATED |
| SAL-WO5 (DONE, decision open) | **Fold the lab into the repo's tools rather than run it beside them.** The transition engine overlaps `null-harness` (null runs), `claim-record` (append-only, no-verdict) and `criteria-drift` (versioned rulers). | assessment only | Two record schemas with one rule invite drift. | a mapping table, then a decision for the operator: keep separate, adapt, or merge |

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
- **SAL-WO2 done.** `confound_record.py` gives four states (UNTESTED,
  RAN_NO_SIGNAL, RAN_SIGNAL, NOT_TESTABLE), each with required fields.
  - A version stamp is required on every tested record (confound 7). A
    missing model id is WITHHELD or NO_BUILD_STRING, with a reason.
  - It is append-only: a status change is a new record that supersedes the
    old one, with chain checks over the stream.
  - Thread B's ten confounds are seeded as UNTESTED.
  - Two encodings, since the delivered lab's type list is closed (SAL_011):
    a native `confound_record` type, and an `audit_event` encoding that the
    unedited lab accepts.
- **SAL-WO3 done.** The scan was pre-registered before running; the pin's
  full hash was mistyped and corrected in a committed amendment before the
  run.
  - Series: this repo's daily commit counts (158 days, unshallowed history).
  - All four lab procedures were run unmodified, and the records validate.
  - All three predictions held. P2 was weak as written, which is recorded.
  - Two findings: the coupling scan cannot separate factors (SAL_012), and
    the real order sits below every shuffled-order null (SAL_013). See
    `real_scan/RESULTS.md`.
- **SAL-WO4 done.** `claims/claim_tracker.py` and `claims/claims.jsonl`
  hold four claims seeded at search depth on 2026-10-27:
  - OpenAI ETH disproof: UNDER_OUTSIDE_REVIEW.
  - Local smoothing / Kakeya: CLAIMED_UNREFEREED.
  - QCD / Yang–Mills existence: UNDER_OUTSIDE_REVIEW.
  - Anthropic-attributed #3-SAT preprint: NOT_LOCATED, not adjudicated.

  The stream is append-only, validated on every append, and keeps two
  clocks apart: the date the source reports and the date the registry
  recorded it. Updates need egress.
- **SAL-WO5 done, decision open.** `FOLD_ASSESSMENT.md` maps every lab
  piece onto its nearest repo tool, sets out three options, and recommends
  the adapter route.
  - Evidence: `fold_probe.py` runs the repo's `null-harness` on the lab
    engine, unmodified. It grades CONSTANT_FIRES in the demo's regime
    (FP 1.000, TP 1.000) and OK in a quiet one (FP 0.000, TP 1.000).
  - Keeping the families separate, adapting, or merging is the operator's
    decision.
