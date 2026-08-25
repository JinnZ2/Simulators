# CLAIM_TABLE — model-provenance

Claims about work order 5 and about what it found when run on this
repository. `WORK_ORDER.md` is delivered and is not edited.

REFUTATION_PROTOCOL: each claim names what would refute it. A failed
check updates the claim, never the instrument's numbers.

---

### MP_001 — the forward log S1 asks for already exists, unplanned, in the Co-Authored-By trailer

S1 specifies a write that nobody has been doing. But **159 of this
repository's 236 commits already carry a self-reported model identifier**,
in the `Co-Authored-By` trailer that the commit template appends:

| stated | commits | first | last |
|---|---|---|---|
| Claude Opus 4.7 (1M context) | 40 | 2026-07-08 | 2026-08-11 |
| Claude Opus 4.8 | 1 | 2026-07-12 | 2026-07-12 |
| Claude Opus 5 | 118 | 2026-08-11 | 2026-08-25 |
| no version stated | 77 | | |

The trailer is a self-report: the string was written by the session that
made the commit, and no other party supplied it. So S1's channel exists
at 67% coverage and was built for attribution rather than for provenance.

That is the whole reason S2 is checkable here — see `MP_002`.

**Falsifier:** a trailer written by anything other than the session it
names.

**Status: SUPPORTED, measured.**

---

### MP_002 — S2 has a check set, and it is what turns a decode into a measurement

A date-to-version decode with nothing to score against renders rather
than measures: every commit gets a candidate and no candidate can be
wrong. The trailers (`MP_001`) supply the missing arm.

Scored on this repository, table as shipped, window 1 day:

| outcome | commits |
|---|---|
| decode SINGLE, matches trailer | 118 |
| decode SINGLE, differs from trailer | 36 |
| decode AMBIGUOUS, contains trailer | 2 |
| decode AMBIGUOUS, excludes trailer | 3 |
| no version stated | 77 |

The ambiguous rows are reported apart from the single ones and **no pick
is made in them**, per S2.

**Falsifier:** a repository where the decode agrees with every trailer,
which would make the check set uninformative rather than confirming.

**Status: SUPPORTED.**

---

### MP_003 — the assumption S3 names is refuted on this repository's record

S3 says the derivation is *always current-at-the-time*, and says to
record it as the derivation rather than as a fact. Scored:

| quantity | value |
|---|---|
| commits stating a table version | 159 |
| stating an earlier version after a later one had appeared | **39** |
| assumption holds | **False** |

Every counterexample is the same shape: `Claude Opus 4.8` appears on
2026-07-12, and `Claude Opus 4.7` continues to appear on 39 commits
across the following month, through 2026-08-11.

**The reading is not that the dates are wrong.** It is that sessions do
not all run the newest available version, which is precisely the content
of the assumption. S3 was right to make it the claim.

**Falsifier:** a reading of the 4.8 commit under which it is not a
session on 4.8 — a hand-edited trailer, a cherry-pick, a rebase carrying
an older trailer forward.

**Status: SUPPORTED.**

---

### MP_004 — the refutation rests on one commit, and the report says so rather than reporting 39

39 counterexamples is a number that reads as overwhelming. It is not.
`assumption_sensitivity()` drops each table row in turn and re-scores:

| table row | rests on | backwards without it | attributable |
|---|---|---|---|
| Claude Opus 4.7 (1M context) | 40 commits | 0 | 39 |
| **Claude Opus 4.8** | **1 commit** | **0** | **39** |
| Claude Opus 5 | 118 commits | 39 | 0 |

**All 39 counterexamples, and all 36 decode disagreements, are
attributable to a single commit.** Remove `b3fffc64` (2026-07-12,
`Add thermal sensor degradation audit simulator`) and the record is
monotone: 0 backwards, 1 disagreement.

The claim in `MP_003` is unchanged — one counterexample refutes a
universal — but the *count* is not evidence of the size of the effect,
and the two are easy to read as one thing. Both readings are printed and
neither is picked.

**Falsifier:** a second version row resting on more than one commit that
produces counterexamples of its own.

**Status: SUPPORTED. n=1 on the mechanism.**

---

### MP_005 — the decoder's own resolution was wrong, and only the real data showed it

`git_log()` first read `--date=short`. On this repository the 4.7 → 5
switchover happens **inside one calendar day**:

```
2026-08-11 17:20:27 +0000  Claude Opus 4.7 (1M context)   <- last
2026-08-11 22:34:13 +0000  Claude Opus 5                  <- first
```

**Bracketed to 5 h 14 min.** Ordering by day therefore reported three
counterexamples on 2026-08-11 that are an artifact of the reading: at
timestamp resolution the record is in order. A `reasoning-gate` G-RES
pair — the feature is hours, the instrument was days.

Repaired: the full timestamp is carried for ORDERING, the short date for
DECODING, because the table is date-granular and a decode cannot be
finer than its table. With the 4.8 row dropped the residual goes from 3
to **0**.

No fixture written before the run would have shown it. The repair is
pinned by two selftest checks — a same-day switchover in order scores 0,
and the same two commits with the clock reversed scores 1 — so a
regression to day-resolution turns them red.

**Falsifier:** a switchover this repository records at a resolution the
timestamp cannot separate — two commits at the same second.

**Status: REPAIRED, pinned.**

---

### MP_006 — UNKNOWN needs a reason, and this session's own row is the case that shows why

S1 says: *if the build string is unavailable, write UNKNOWN — do not
infer from behaviour.* The first half is a state and the second is a
refusal, and the state has more than one cause.

This session operates under a standing instruction against writing a
model identifier into any artifact pushed to a repository. The build
string is not unavailable; it was not written. Those produce the same
blank and are different facts, so `open_line()` requires a reason from a
closed vocabulary — `NO_BUILD_STRING` or `WITHHELD` — and **refuses a
bare UNKNOWN**.

The first row in `sessions.jsonl` is `UNKNOWN / WITHHELD`.

This is the fourteenth-odd instance of the absent-vs-known-negative
repair in this repository (`PB_004`, `GC_004`, `MD_002`, `CC_002`,
`CA_002`, `UNI_021`, `CR_027`, `QA_004`, `SSS_007`, ...) and one of the
few designed in before the first row was written rather than found in
audit.

**The conflict is recorded, not resolved.** The operator can run
`provenance.py open --model "..."` under no such constraint, and every
row states which channel it came through.

**Falsifier:** a use of the log where the two reasons license the same
next action, which would make the distinction decorative.

**Status: SUPPORTED, and the constraint is disclosed rather than worked
around.**

---

### MP_007 — the release-date table S2 requires is not reachable, and observed bounds are a weaker substitute that says so

S2's input is *the release-date table for the model line*. It is not
available here: the egress policy is an allowlist (`SSS_015`), and a
table carried from memory is this repository's `ANC_010` / `CD_009` /
`RD_015` / `HO_005` status — carried, unverified, not load-bearing.

`releases.json` therefore ships **observed bounds** from this repo's own
trailers, with `table_kind: observed_bound`, and the decoder prints the
inheritance in every report header rather than in a footnote:

> a first appearance is an **upper bound** on a release date and is never
> the date — the version existed at least that early, and may have
> existed long before anyone committed under it.

Consequence, and it is not small: **the substitute table is derived from
the same trailers `MP_002` scores it against.** The check set is not
independent of the table. What survives that circularity is the
ORDERING check (`MP_003`), which is a statement about the trailer
sequence alone and does not use the table's dates as truth — and the 36
decode disagreements, which are a statement about where the observed
bounds fall relative to the record that produced them.

Swapping in real release dates needs no code change: set `kind` to
`release_date` and the header changes what it says.

**Falsifier:** publisher release dates for these versions, which would
make the decode independent of the trailers and re-score `MP_002` for
real.

**Status: SUPPORTED. The strongest single improvement available to this
folder is a table from outside it.**

---

### MP_008 — 77 commits state nothing, and they are the population the decode exists for

The 159 commits with trailers are where the decode can be checked. The
**77 without** are where it is actually used — and by construction
nothing in this repository can score them.

That is the honest shape of S2's product: it is informative exactly
where it is unverifiable, and verifiable exactly where it is redundant.
The `verify` report keeps `no version stated` as its own row for that
reason.

**Falsifier:** an independent record of what those 77 sessions ran.

**Status: SUPPORTED. This is a limit, not a defect.**

---

### MP_009 — S4 is enforced, and the vocabulary that would trip it is not this order's

Output is screened through `no_severity` — the same module `scans.py`
and `scan4.py` use — with the two-arm measured-exemption arrangement.

Unlike scan 4 (`SSS_039`), **the exemption list here is empty**:
`DELIVERED_VOCABULARY = ()`. Work order 5's verdict names
(`SINGLE`, `AMBIGUOUS`, `NOT_DECODABLE`) carry no screened word, so the
reports pass with nothing masked. The two arms and the plant still run,
so if a grading word ever enters the check turns red rather than being
silently exempted.

"Do not modify commits" is enforced structurally rather than by screen:
the only git verb in the module is `log` — **asserted in the selftest
over this file's own source**, so a write verb added later turns a check
red rather than being caught by a reader.

Writing that check produced one more instance of a shape this repository
has recorded before: the first version's pattern was a string literal,
and it **matched the line that defined it**, reporting a second "verb".
`UNI_010`'s self-reference, caught inside the check that exists to
report it. The pattern is now composed from tokens, the
`residual-direction` `RDD_008` move.

**Falsifier:** any emitted row that ranks a commit or a version.

**Status: SUPPORTED.**
