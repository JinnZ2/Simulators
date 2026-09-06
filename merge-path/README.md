# merge-path

A transform table between claim-record formats that already exist and this
repository's falsifier / branch-record format, with the loss in each
direction **measured, not asserted**. Built to `WORK_ORDER.md`.

**It is not a new format** (§0). If the output of this work were a format,
the work failed; the failure mode of this problem space is producing an
eighth standard. The unit of value is a TRANSFORM — `reference` (what a
registrar's record is taken against) / `maps_to` (its correspondent in the
falsifier format) / `breaks_at` (where the correspondence fails). **A
registrar that does not merge is a valid outcome; a NO-MERGE with a stated
`breaks_at` is worth more than a forced mapping.**

## The egress fact sets the verification status

The work order's §1 requires **fetching each registrar's own specification**
before mapping. In this environment the egress proxy is an allowlist and
every registrar spec host answered **403 to CONNECT** (probed
2026-09-05T03:30Z; nanopub.net, clinicaltrials.gov, w3.org among them). **No
spec was fetched.** Per §7, every real registrar is therefore **UNVERIFIED**,
its converter is NOT-IMPLEMENTED with that reason, and everything derived
inherits UNVERIFIED. No spec field is transcribed from memory and none is
fabricated; the docs carry only the work order's own §1 candidate summaries,
marked as such — the very summaries §1 says not to rely on.

**So what is delivered is the machinery, verified, plus a scaffold ready to
be filled from a fetched spec.** The residual classifier, the round-trip
test, and the S1–S5 selftest are correct by construction and run on
constructed data; the per-registrar transforms are NO-MERGE-with-`breaks_at`
until someone whose egress reaches the spec hosts fills them in.

## Run

```
python3 merge-path/run_all.py        # round trip over the fixture set
python3 merge-path/report.py         # print MERGE_REPORT.md
python3 merge-path/report.py --write  # (re)write MERGE_REPORT.md
python3 merge-path/selftest.py        # S1-S5 + null tests
```

Stdlib only, parses under Python 3.9, phone-runnable. The library modules
refuse `--selftest` with rc 2; `selftest.py` prints `selftest: N checks, M
failed`.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `UNITS.md` | §1 inventory — one block per registrar, all UNVERIFIED (spec unfetched) |
| `TRANSFORMS.md` | §2 IN/OUT per registrar, each a NO-MERGE with an egress `breaks_at` |
| `REVERSE_GAPS.md` | §4 where our format is weaker — carried UNVERIFIED, not skipped |
| `BRANCH_SEARCH.md` | §5 the branch record's novelty — UNVERIFIED, with the search list stated |
| `registrars.py` | the shared Registrar model + registry (added over §6's list; reason stated) |
| `convert_out.py` | §2 OUT: falsifier record → registrar record |
| `convert_in.py` | §2 IN: registrar record → falsifier record |
| `residual.py` | §3 round trip + residual classification (DROPPED/FLATTENED/COERCED/ADDED) + `verdict` |
| `run_all.py` | §6 runs the round trip over the fixture set |
| `report.py` | §6 emits `MERGE_REPORT.md` |
| `selftest.py` | §6 S1–S5 + null tests |
| `CLAIM_TABLE.md` | `MRG_001..MRG_008` |

## The machinery (verified)

Residual classes (§3), each exercised on a **declared test double** (no mock
is a claim about any real registrar): **DROPPED** (no target slot),
**FLATTENED** (a dict collapsed to a string, human-recoverable), **COERCED**
(a field written into a slot that means something else — the dangerous one),
**ADDED** (the target demanded a field the source lacked; it must name its
origin or the conversion fails). **COERCED and ADDED are reported alongside
DROPPED**, visible as a zero when zero — a report of only DROPPED counts is
not finished. The two directions (`round_trip_out_in`, `round_trip_in_out`)
lose different things and are measured separately; asymmetry is information.

The S1–S5 selftest (`MRG_003`): identity round trip lossless; unmappable →
DROPPED not silent; COERCED detected; ADDED with no origin a hard failure;
NO-MERGE with no `breaks_at` a hard failure.

## Constraints honoured

No new format (`MRG_004`). No ranking of registrars, no "ours is better"
framing (`MRG_008`) — the reverse gaps (`REVERSE_GAPS.md`) record where our
format is the weaker one (uncertainty budget, enforcement, total mechanical
check, provenance graph), carried UNVERIFIED. No author-characterizing
section. Nothing is registered anywhere. Every registrar statement cites its
spec URL as an identifier. CC0.
