# scope-audit-lab

Two delivered drops from Kimi (OKComputer, an open-source model), landed
verbatim, plus checks on them.

**Provenance.** The report continues a multi-session, multi-model project:
earlier GPT sessions and the operator's own threads A–D. The operator
states that material like this is a diagnosis and a set of things to note
from work with other AI systems. It is read that way here: notes to check,
not findings.

| uploaded zip | sha256 | landed as |
|---|---|---|
| `OKComputer_Deep_Research_Continuation.zip` | `81c88bec…` | `CONTINUATION_REPORT_V1.md`, `lab_0_2/` |
| `OKComputer_Creative_Scope_Audit_Experiments.zip` | `0ca94c81…` | `CONTINUATION_REPORT_V2.md`, `lab_0_3/` |

The second zip contains the first:

- The same `lab_0_2`, byte-identical.
- The same four report figures, byte-identical.
- The same inner `scope_audit_lab_prototype_0_2.zip`.
- A revised report (V2) and lab 0.3.

Both reports are kept so the revision stays inspectable. The inner zips
duplicate the extracted trees and are not landed. Figures are recorded in
`FIGURES.md` (the repo is text-only).

## What the lab is

```
record types (append-only JSONL, no verdict field ever set)
  model ── experiment ── observation ── audit_event
                │
  transition_scan (0.2): ordered cases -> adjacent deltas -> strictly > threshold
                │        -> candidate region, cause unassigned
                │        missing / non-finite kept, never dropped
  experiments (0.3): null_baseline | threshold_sweep | order_permutation | coupling_scan
```

The design rule is this repo's own: record evidence and provenance, never
issue a verdict the evidence does not force.

## Run

    cd lab_0_3 && python3 -m pytest -q    # 56 passed (lab 0.2: 31)
    python3 check.py                      # audit of the drop
    python3 check.py --selftest           # prints its own check count
    python3 null_expectation.py           # closed-form null beside the shipped null record
    python3 test_null_expectation.py      # checks, incl. against the lab's own generator
    python3 confound_record.py            # SAL-WO2 thread-B confound ledger (test_confound_record.py)
    python3 real_scan/run_scan.py --check # SAL-WO3 first real-data scan reproduces from git
    python3 claims/claim_tracker.py       # SAL-WO4 live claim registry (claims/README.md)
    python3 fold_probe.py                 # SAL-WO5 null-harness grades the lab engine (numpy; FOLD_ASSESSMENT.md)

`check.py` is stdlib only and parses under 3.9. The lab's README asks for
3.10+, but its `X | None` annotations sit behind
`from __future__ import annotations`, so it parses under 3.9; a run on 3.9
is not verified. Sample output: `samples/check.sample.txt`.

## What holds

- Test counts are as stated: 31 (0.2) and 56 (0.3). Both suites pass here.
- The v0.2 demo deltas (27, 61), the threshold-sweep counts (4, 3, 3, 3, 1)
  and the null range (7–11 over 25 replications) all match the report.
- At search depth these anchors check out:
  - the OpenAI ETH announcement of 26 Oct 2026 and its outside reviewers;
  - *Navier–Stokes lost in translation* (arXiv 2610.08144);
  - the Palomar registry (opened 18 Aug 2026);
  - the IEA figures of 17% growth and about 950 TWh by 2030.
- The lab keeps missing, non-finite and zero-valued outputs as three
  distinct states, and its tests pin each one.

## What this audit adds (`CLAIM_TABLE.md`, SAL_001..010)

1. **The ESA row cites the wrong Federal Register document (SAL_001).**
   - The row says "final rule published July 14, 2026".
   - Its link is FR 2025-06746, dated 17 April 2025, which is the
     proposed rule.
   - The final rule is FR 2026-14195, already pinned in
     `habitat-lag-dependency/`.
   - The report says every checkable anchor in its transcript
     "checks out"; its own citation for this one does not.
2. **The null baseline measures the generator (SAL_004).**
   - Uniform noise on [0, 100] against threshold 10 gives an expected
     (n−1)(1−10/100)² = 8.91 flags per 12 cases.
   - The recorded mean is 8.88.
   - The "copious" null count can be computed without running anything:
     it is the width-to-threshold ratio, not a property of the engine.
3. **The demo plants three steps, and the report names two different
   pairs as "planted" (SAL_005).**
   - The series is 5, 6, 4, 31, 30, 8, 9, 60. Its three moves of 20 or
     more are +27, −22 and +51.
   - The sweep paragraph calls the planted steps the ~26 and ~51 moves
     (pairs 2–3 and 6–7).
   - The permutation paragraph's "planted pairs, 9 and 8 of 26 scans"
     are pairs 2–3 and 4–5.
   - The ~51 step appears in 4 of 26 scans.
4. **The demo stream is doubled (SAL_003).** `experiments_demo.jsonl` holds
   the five-record demo twice, identical once ids and timestamps are
   removed. The report describes one five-record stream.
5. **The zero-output demo case is never computed (SAL_006).** The only pair
   whose left output is 0 has a missing right side, so the labelled
   zero-output path is not exercised by the demo. The unit tests do
   exercise it.
6. **A preprint is not located, and this audit has an interest
   (SAL_007).**
   - The "Anthropic/Claude refutation paper" (hexagonmath 2610.00577) was
     not found at search depth.
   - This audit is written by a Claude model, so the claim is recorded as
     NOT_LOCATED and is not adjudicated either way.

Nothing here is a verdict on ETH, on any lab, or on the lab's design.
