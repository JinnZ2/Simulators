# upgrade-queue

A **parked queue** of proposed changes to the falsifier / claim-record
format, delivered verbatim in `UPGRADE_QUEUE.md`. **It is a queue, not a
spec.** Every entry's status is NOT ADOPTED; nothing is adopted by being
written here, and moving an entry to ADOPTED requires its adopt-test to have
run or an explicit recorded decision (the queue's own rules).

Thirteen entries in three tiers by provenance: **FORCED** (an observed
failure in hand, U-01..U-04), **CANDIDATE** (from a registrar, untested
here, U-05..U-09), **SPECULATIVE** (from neither, parked deliberately,
U-10..U-13). Plus a NOT-ON-THIS-LIST section recording what was considered
and left off, with reasons.

## What this folder adds

`queue_check.py` checks only what is verifiable **without adopting
anything**:

1. **structure** — the queue parses into the tiers it declares with the
   entry counts it states (13; FORCED=4 / CANDIDATE=5 / SPECULATIVE=4), and
   every entry carries the global NOT-ADOPTED status.
2. **adopt-rule classification** — per the queue's own rule, an entry that
   only ADDS a field needs no branch entry; one that CHANGES a rule does.
   Only `U-09` (the queue's own *most likely a format rewrite*) is CHANGES;
   the rest ADD a field or are UNKNOWN (Tier 3, placement stated Unknown).
   Each `kind` is a declared reading of the entry's `form` line.
3. **cross-reference resolution** — each entry's referenced artifacts are
   resolved to IN-REPO (path checked on disk) or EXTERNAL, which is what
   says whether an adopt-test could run here. Most Tier-1 adopt-tests are
   **BLOCKED_EXTERNAL** (their corpora are the Kimi / Perplexity / DeepSeek
   runs this repo does not hold), `U-07` is **BLOCKED_UNLANDED** (the FSRI
   report has not landed — egress), `U-04` needs **none** (the nesting
   result is in-repo and is the demonstration), and `U-05` is the only one
   **RUNNABLE_HERE**. Nothing is fabricated; external corpora are marked
   EXTERNAL and in-repo references are verified against the filesystem.

## Run

```
python3 upgrade-queue/queue_check.py     # the structural + cross-ref readout
python3 upgrade-queue/selftest_uq.py     # the checks
```

Stdlib only, parses under Python 3.9, phone-runnable. `queue_check.py`
refuses `--selftest` with rc 2; `selftest_uq.py` prints `selftest: N checks,
M failed`.

| file | what |
|---|---|
| `UPGRADE_QUEUE.md` | delivered verbatim; the parked queue (U-01..U-13) |
| `queue_check.py` | structure + adopt-rule classification + cross-reference resolution |
| `selftest_uq.py` | the checks (18) |
| `CLAIM_TABLE.md` | `UQ_001..UQ_006` |

## The queue is the format learning from its own drops

Several entries turn a finding already recorded in this repository into a
proposed format change: `U-01` (the uncertainty on `ADDENDUM_02`'s required
cut), `U-03` (the ENG-3 sign inversion, `RESULT_repair_adjacency.md` §5),
`U-04` (the nesting cut-height, `DS_014`), `U-07` (the FSRI hold marker),
`U-10` (cooperative-substrate's P5), `U-11` (merge-path's §4 reverse-gap
discipline), `U-12` (railcar's ENVELOPE), `U-13` (K4's N, `DS_013`/`DS_015`).
Each is UNVERIFIED where it rests on an external corpus, and **none is
adopted**. The NOT-ON-THIS-LIST exclusions (no confidence score, no rank, no
verdict field on a branch entry) are the disciplines the repo already holds
(`domain-ledger` `DL_001`, `uninstrumented` SCALAR_DEMAND, the standing
decision against a branch verdict field), now stated as format non-goals.
CC0.
