# WO10 run — scan 4 on this repository's own CLAUDE.md

Run 2026-08-25 against `CLAUDE.md` blob `76d588cff573`, repo HEAD
`2e880af`. Pinned output in `samples/scan.sample.txt`, which prints both
anchors in its header. Command: `python3 self-scan/resolve.py --replay`.

The anchor is not decoration. This scan's own subject is a sentence that
outlived the artifact it describes, and `CLAUDE.md` is edited by the same
commit that lands this folder -- so a sample without a version is a claim
about a file that no longer exists. Line numbers below refer to that
blob.

    target      6744 lines, 469173 chars, 96 sections
    claims      50 extracted by pattern, 50 bound

    MAINTAINED           1
    HOLDS_UNMAINTAINED  32
    DIVERGED             9
    NOT_TESTABLE         8
    UNBOUND              0

    rate  DIVERGED / (DIVERGED + HOLDS + MAINTAINED) = 9 / 42 = 0.214

**The work order's own header is the first divergence.** WO10 states the
target as *4636 lines, 314 KB*; it is **6744 lines, 469 KB**. Not an
error in the order — the file grew between the order being written and
being run, which is the subject.

## The headline: most of these never matched

S5 asked for a divergence date and said UNRECOVERABLE should not appear.
It does not appear. What appeared instead is a distinction the dates
alone could not settle, so the check was re-run against the tree as it
stood at the commit that introduced each number:

| kind | n | meaning |
|---|---|---|
| BORN_DIVERGED | 6 | the check did not return the stated number at the introducing commit |
| DRIFT | 2 | it matched when written and was overtaken |
| DRIFT_POSSIBLE | 1 | the replay was not like-for-like; undecided |

Six of nine divergences are not drift. They did not match at the moment
they were written, and the evidence is that the artifact has not been
committed since — or, where it has, that re-running the check in a
worktree at the introducing commit returns something other than the
stated number.

Four of the six have an interval of **+0.00 days**: the artifact and the
paragraph stating its count were committed **in the same commit**. A
count written in the same commit as the code it counts, and not matching
it.

## The nine

| section | claim | stated | observed | kind |
|---|---|---|---|---|
| thermal-sensor-degradation-audit | 23 tests green | 23 | 33 | BORN_DIVERGED |
| grounding-layers | 430+ audit-grade tests green | 430+ | 516 passed, 9 failed | DIVERGED (see below) |
| relational | 17 files total | 17 | 22 | BORN_DIVERGED (18 at introduction) |
| fourd-municipal-engine-v2 | 40 pass, 2 skip | 40/2 | 37/2, 3 failed | BORN_DIVERGED |
| uninstrumented | selftest 25/25 | 25 | 36 | DRIFT |
| simulation-hypothesis-budget | selftest 20/20 | 20 | 27 | DRIFT |
| sheet-structure-scan | 247 selftest checks green | 247 | 237 | DRIFT_POSSIBLE |
| model-provenance | 29 selftest checks | 29 | 28 | BORN_DIVERGED |
| fold-matrix | 74 selftest checks | 74 | 73 | BORN_DIVERGED |

`grounding-layers` is the one claim carrying **two statements in one
phrase**: a lower bound on a count and the word *green*. The bound is met
(516 >= 430) and the suite is not green (9 failing). Both are printed;
the bin follows the word, and the alternative reading is stated in the
output so it can be argued with rather than assumed away.

`fourd-municipal-engine-v2` is the same shape read from the other side:
"40 pass, 2 skip" is now 37 pass, 2 skip **and 3 failed**, and a count
comparison alone would have reported a suite that shrank rather than one
that broke.

## S1 — the stance test does not transfer, and the reason is measurable

WO10 S1 says to confirm RETROSPECTIVE programmatically rather than
assume it. Confirming it **failed**, informatively.

    NEITHER       73    median section length  26 lines
    PROSPECTIVE   14    median section length  65 lines
    RETROSPECTIVE  9    median section length 142 lines

    a section in the shortest third gets a verdict other than
    NEITHER  6% of the time; one in the longest third, 44%.

The imported test counts markers of two kinds and compares the counts.
A longer section carries more of both, so it is likelier to break the
tie — a **7x** effect between the shortest and longest thirds. Applied
to documentation prose the test is substantially reading length.

That is not a defect in the test, which was built for a provenance cell
in a workbook and returns NEITHER rather than guessing. It is a
statement about transfer, and it has a consequence for the order: WO10's
own stated rule is *"operands resolve inside this file tree"*, which is
**resolvability**, not stance. `sheet-structure-scan` SSS_051 recorded
that those are two criteria computing one quantity when conflated. Here
they are kept apart: the marker reading is reported, and resolvability
is what S3 measures. Neither is picked.

Two sections carry the roadmap markers S1 names by example (`relational/`
and `fourd-municipal-engine/`, on `proposal.md` and a Phase-2/3 roadmap).
Nothing was removed from a denominator on that basis, because none of
the 50 extracted claims falls in a roadmap passage — the claims are
counts and byte comparisons, and a roadmap states neither.

## NOT_TESTABLE, in three kinds

    5  SUBJECT_NOT_IN_TREE
    3  SUPERSEDED_IN_THE_SAME_SECTION

**SUBJECT_NOT_IN_TREE** is the interesting one and it is all five
IDENTITY claims that do not resolve. Each compares a **delivered upload**
against a repo copy — `measurement-fork` MF_019's stale gate copies,
`presented-binary` PB_011's three copies of one file,
`uninstrumented` UNI_068's re-delivery check, `sheet-structure-scan`
SSS_053's two identical candidate workbooks,
`instrument-epistemology`'s pre-repair output. The comparison was made,
at the time, against bytes that were never committed. **It is not
re-checkable from this repository and never will be**, and that is a
property of the claim rather than a gap in the scan.

This is the register's own subject arriving in the register's own index.
It is not a mechanism 9-13 candidate: nothing about the apparatus
prevented the measurement — it was taken. What is missing is the
**record of one side of it**, which is closer to `claim-record`'s field 7
than to an exclusion.

**SUPERSEDED_IN_THE_SAME_SECTION** is three claims where the section
states one number and then states a later one for the same artifact
(`reasoning-gate` 46 then 69, `adaptive-claim-loop` 39 then 53,
`relational` 15 files then 17). These are not stale; they are the
record of an earlier drop, deliberately left. Testing them against the
current tree would report a divergence that the document has already
disclosed one paragraph later, so they are excluded with the reason
named and are not in any denominator.

## S6 — the rate, and the second point

    0.214, n = 42

The UNFCCC calculator returned **0.913** under scan 4 (SSS_035). The two
are **flagged as different document classes** and no direction is
claimed: a workbook states a relationship about its own cells and a
formula either maintains it or does not; this file states a relationship
about files beside it and a **test** either asserts it or does not. n=2,
no curve.

One structural difference is worth naming even at n=2. In the workbook,
`MAINTAINED` was reachable in principle — a formula can enforce a stated
relationship. Here it is reachable and essentially unused: **1 of 42**.
The single MAINTAINED claim is `GUARDS.md regenerates byte-identically`,
which `tests/test_gate_drift.py` asserts. Every other number in this
file is a number a human typed and nothing checks.

## Predictions

All five held, and that is worth discounting rather than celebrating.

    P1  HELD -- selftest family 4/22 = 0.182, suite family 4/11 = 0.364
    P2  HELD -- 9 COUNT claims DIVERGED
    P3  HELD -- 0 of 8 resolvable IDENTITY claims DIVERGED
    P4  HELD -- rate 0.214
    P5  HELD -- MAINTAINED = 1, and it is the GUARDS.md claim

P3 and P5 were close to structural knowledge: I knew which IDENTITY
claims name uploads and I knew `tests/` does not assert counts. P2 is
nearly free on a file this size. **P1 is the only one that could have
gone either way**, and it went the predicted way by a factor of two: a
`selftest N/N` sentence and the module printing N are written together
and the module is the authority, while a suite count is written once and
the suite grows past it.

P4's margin is large (0.214 against a 0.5 line) and the comparison it was
aimed at — the UNFCCC 0.913 — is a different document class, so it
resolves the prediction and settles nothing about documents in general.

## What the scan does not do

**It does not fix anything.** Nine numbers in `CLAUDE.md` do not match their artifacts and
this run does not correct them, because correcting them in the same
commit would destroy the sample's reproducibility: `samples/scan.sample.txt`
names commits, and the S5 replay resolves against a history the
correction would extend. The correction is a separate commit, after this
one, and until it lands the nine rows above are the record of what did not
match, and since when.

**It measures HEAD, not the working tree.** Every check runs in a
throwaway `git worktree`, because the first version ran in place and
**modified the repository it was measuring** — the suites wrote two
provenance ledgers, a denial record, a JSONL log, and one file literally
named `--selftest`. That is the difference between scan 4 on a workbook
and scan 4 on a repository: resolving a COUNT claim means executing
code. An uncommitted change is invisible to this scan, and a selftest
check asserts the working tree is unchanged after a run.

**Dependencies were installed for the run and are declared per item.**
`pytest`, `numpy`, `scipy`, `matplotlib`, `jsonschema`, `psutil`. Without
them every suite claim would be NOT_TESTABLE and the run would be
measuring the container rather than the file. Two of them changed a
verdict: `psutil` and `numpy` took `grounding-layers` from "pytest
produced no summary" to 516 passed / 9 failed.

## One incidental finding, outside the claim table

Installing `pytest` to resolve the suite claims turned the repository's
own `tests/` from green to `84 passed, 1 error`. The error is not in
`tests/`: pytest reaches `tools/substrate_substitution_toolkit.py` and
collects `test_claim_with_substitution`, a toolkit entry point whose
name begins with `test_`, then errors on a `claim` fixture that does not
exist.

Latent since the function was written and invisible while pytest was
absent. Marked `__test__ = False`, a pytest-only attribute that changes
nothing for any caller. Recorded here rather than in the claim table
because it is not a claim about `CLAUDE.md` -- it is what happened when
this scan brought a tool into the container in order to measure
something else.
