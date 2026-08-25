# model-provenance

Work order 5, delivered verbatim in `WORK_ORDER.md`. Two halves that do
not share a mechanism: a **write** at session open, and a **read** over
history that never writes back into it.

| file | |
|---|---|
| `WORK_ORDER.md` | the order as delivered |
| `provenance.py` | both halves. `--selftest` |
| `releases.json` | the version table, with what kind of table it is |
| `sessions.jsonl` | the forward log (S1), append-only |
| `CLAIM_TABLE.md` | `MP_001..009` |
| `samples/` | one pinned run of each command |

```
provenance.py open --repo R --branch B (--model M | --reason NO_BUILD_STRING|WITHHELD)
provenance.py log
provenance.py decode [REPO] [--per-commit] [--window N]
provenance.py verify [REPO] [--window N]
```

## What the run found

**The forward log S1 asks for already exists, unplanned.** 159 of this
repository's 236 commits carry a self-reported model identifier in the
`Co-Authored-By` trailer — a channel built for attribution, doing
provenance by accident. That is what gives S2 a check set, and a decode
with no check set renders rather than measures.

**The assumption S3 names is refuted on the record.** *Always
current-at-the-time* fails on 39 of 159 commits: `Opus 4.8` appears on
2026-07-12 and `Opus 4.7` keeps appearing for a month afterwards. The
reading is not that the dates are wrong — it is that sessions do not all
run the newest version, which is exactly the content of the assumption.
S3 was right to make it the claim rather than a fact about a commit.

**And the 39 rest on one commit.** The report drops each table row in
turn and re-scores: remove the single 2026-07-12 commit and the record
is monotone, 0 backwards and 1 disagreement instead of 39 and 36. One
counterexample still refutes a universal, so `MP_003` stands — but a
count is not a size, the two read as one thing, and both are printed.

**The decoder's own resolution was wrong and only real data showed it.**
The 4.7 → 5 switchover happens inside one calendar day, bracketed to
**5 h 14 min** by the timestamps. Ordering by day reported three
counterexamples that are an artifact of the reading. Full timestamps now
carry the ordering, short dates carry the decode, and two selftest checks
pin the difference.

## The two things this folder cannot do

**The table is not release dates.** S2's input is not reachable from here
(allowlist egress), and a table from memory is this repo's `ANC_010`
status. `releases.json` ships observed bounds from the trailers instead,
labelled `observed_bound`, and every report header says a first
appearance is an **upper bound** on a release date and never the date.
The cost is stated in `MP_007`: the substitute table is derived from the
same trailers it is scored against, so `MP_002` is not independent. What
survives is the ordering check, which uses no dates from the table.

**77 commits state nothing**, and they are the population the decode
exists for. The decode is checkable exactly where it is redundant and
informative exactly where it cannot be checked. `verify` keeps that row
separate rather than folding it into a rate.

## S1: self-report, and the refusal is in code

There is no function here that derives a model identifier from
behaviour, output, timing or history. The one that would is
`infer_model()`, and it raises. That is S1's *do not infer* as an absence
rather than as a rule someone is asked to remember.

`UNKNOWN` takes a reason from a closed vocabulary and a bare one is
refused, because **"could not report" and "did not write" are different
facts that produce the same blank**. The first row in `sessions.jsonl` is
the second of those, and `MP_006` says why in full.

## S4

Reports structure. The only git verb in the module is `log`, so "do not
modify commits" is structural rather than promised. Output is screened
through `sheet-structure-scan/no_severity.py` with the two-arm exemption
arrangement, and unlike scan 4 the exemption list is **empty** — this
order's verdict names carry no screened word.

29 selftest checks. Stdlib only, parses under Python 3.9. CC0.
