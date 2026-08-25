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

---

# Amendment — the compute-budget hypothesis, measured

A relayed reading of the first run: the forty-one unbacked numbers are
not an absence of maintenance but a structural feature of the document
class — the sim ran on hardware that could run it, the number was
written down on a device that cannot, so the claim and the check live on
different machines and the maintenance operation needs a resource the
author does not have. Proposed: a distinct `NOT_TESTABLE`-by-compute-
budget bin, and the rate split by it.

It is a better-shaped hypothesis than the one it replaces, and it is
measurable. The measurement is the import graph, and `census.py` takes
it.

## What the census found

    MODULES EXPOSING --selftest: 76
      stdlib          76

      GREEN                   52
      GREEN_UNCOUNTED         22
      RAN_NO_VERDICT           1
      EXCLUDED_SELF_REFERENCE  1

      checks counted: 1225, over the 52 modules that print a count.
      22 more pass without printing one, so 1225 is a FLOOR.

    TEST DIRECTORIES: 20
      total: 1198 passed, 15 failed, 3 skipped

**76 of 76.** Every module in this repository that carries its own
checks imports nothing outside the standard library. Not most — all of
them. And 74 of the 76 run green on this container.

**32 of 44 bindable `CLAUDE.md` claims need nothing but the standard
library.** Five need only pytest. Four need anything more.

## So the first half of the claim does not describe these numbers

This scan resolved 41 of 42 claims, on one container, in one pass of
about twenty minutes. Compute budget was not what stood between any of
them and a check. What stands between them is that **nothing runs the
check** — there is no runner, not no machine.

The distinction matters because the two have different repairs. "The
author cannot run it" is repaired by someone else running it. "Nobody
runs it" is repaired by a line in a test file, and this repository
already has the mechanism: `tests/test_gate_drift.py` is the one place
where a `CLAUDE.md` number has a test behind it, and it is one line of
work per number, not a machine.

## The second half holds, and is stronger than stated

The relayed message says the stdlib-only, phone-buildable constraint is
"the boundary of what can be checked locally". Measured, it is better
than that. Inside the boundary essentially everything checks — 74 of 76
green — so the constraint is not merely where checking stops. It is
where checking is **free**.

Where compute does bite is the pytest arm and not the selftest arm: 4 of
20 test directories need numpy / scipy / matplotlib / psutil /
jsonschema, and those are the ones a phone cannot run. That is the real
population the hypothesis describes, and it is a different population
from the one it was pointed at.

## What was adopted anyway

The proposed bin is built, because the argument for it is right even
though its instance was not:

    NOT_TESTABLE, by cause
      SUBJECT_NOT_IN_TREE              5
      SUPERSEDED_IN_THE_SAME_SECTION   3
      QUOTED_NOT_ASSERTED              1
      MISSING_DEPENDENCY               0   (in this environment)

`MISSING_DEPENDENCY` is empty **here** and held 6 before this run
installed pytest, numpy, scipy, matplotlib, jsonschema and psutil. So
the rate is a property of the document **and the machine**, and the
report now prints the environment above it — a rate quoted without one
is a number with an unstated denominator, which is this folder's own
subject.

## Two things the amendment cost

**The paragraph describing the scan carried a stale count of the scan.**
The `self-scan/` entry written in the previous commit said "69 selftest
checks across two modules"; `census.py` made that three modules and a
different number within the hour. Repaired by removing the count and
naming the command that produces it, rather than by writing a bigger
number that goes stale on the next module. `claim-record`'s derive-at-
read-time rule, arriving in prose.

**The census could not census its own run.** `census.py` advertises
`--selftest`, discovers itself, and the first version ran itself, which
runs itself. It hung. `UNI_010` in a third form — a runner running
itself rather than a scanner reading its own output. It stays in the
inventory and is not executed, with the state saying so.

## Not green, and what it is

Two modules and four suites:

    instrument-bias-sims/_shared.py     RAN_NO_VERDICT
    self-scan/census.py                 EXCLUDED_SELF_REFERENCE

    crossdomain-eval/tests              NO_SUMMARY (5 collection errors)
    fourd-municipal-engine/tests        19 passed, 3 failed
    fourd-municipal-engine-v2/tests     37 passed, 3 failed, 2 skipped
    grounding-layers/tests              516 passed, 9 failed

Fifteen failures across 1213 tests. None of them is in the stdlib
selftest arm.

---

# Handoff run — four items, three measured and one absent

## 1. Self-enumeration: one defect or two? Two.

`census.py` hung on itself and wrote into the tree it measured, and the
hypothesis was that these are one problem — anything enumerating the
tree it runs in has both by construction.

`enumerators.py` tests it on the population: 50 modules call a
directory-enumeration primitive, 49 ran, both properties measured by
running rather than read from source.

                       writes: yes   writes: no
    enumerates self yes            1           15
    enumerates self no             2           31

    of 16 that enumerate themselves, 1 writes  (6%)
    of 33 that do not,               2 write   (6%)
    difference: +0 points

**Refuted, and refuted on its own examples.** All three modules the
handoff named — `uninstrumented/scan.py`, `reasoning-gate/mine_logs.py`,
`inverseminar/inverseminar.py` — enumerate themselves and **none of them
writes**.

The diagonal share is 65% and is not the test. Three of 49 modules write
at all, so a thin margin makes the diagonal read high for a reason
unrelated to the hypothesis; the within-group rates are printed instead
and the power bound is stated.

**The replacement predictor is execution.** Reading a tree cannot dirty
it; running what is in the tree can, and `census.py`'s writes were its
children's:

                       writes: yes   writes: no
    executes yes                   3           16
    executes no                    0           30

    16% against 0%.  All three writers execute; nothing that does
    not execute writes.

Labelled weaker in the output, because `executes` is read from source
while `writes` is observed.

**One finding about the instrument.** Running each module with
`--selftest` reached *no enumeration at all* for the two named scanners,
because their selftests do not exercise the walk. The real invocations
are declared, found by running them: `scan.py` with no argument prints
usage and exits 0, and `mine_logs.py .` raises `FileNotFoundError`
before its glob because the guards path defaults relative to the cwd.
Without that, the arm that matters would have been measured as zero.

## 2. Stale-number repair: 35 of 42, and all 9 that diverged

    35 of 42 resolved claims have a command that produces the
    stated number.
     7 have a check that is not a count -- byte comparisons, a
       regeneration, a git diff.
     9 of 9 DIVERGED claims are convertible.

**One correction to the framing.** Conversion does not make a claim
`MAINTAINED`. It makes it stop being a claim: there is no stored number
left to diverge from, which is a different state from a number a test
asserts. `MAINTAINED` means something checks it; converted means nothing
needs to. The report says this where it prints the number, because
counting the second as the first would report a removed claim as an
asserted one.

Not applied here, per `SS_012`. The pinned sample names commits and the
S5 replay resolves against a history a correction would extend.
Measuring is this commit; applying is the next.

## 3. Use-mention: the file supplied its own control

The test is structural, not semantic. Markdown puts a quoted claim in a
code span and an asserted one in running prose:

    line  236   430+ audit-grade tests green.       bare, asserted
    line 6665   `430+
      audit-grade tests green`                      in a span, quoted

The same string, both ways, in the same file — a two-directional known
answer the document supplied without being asked.

The flag never excludes. A flagged claim must be declared in
`bindings.py`, and a selftest check asserts every quoted claim has one.
A silent misattribution becomes a required decision.

## 4. WO9 (PlanExe) is not here

Searched `PlanExe`, `plan_exe`, `WORK_ORDER_9`, `WO9`, case-insensitive,
across every text file and the full git history on all branches.
Nothing. The orders present are 4, 6, 7 and 10 plus four unnumbered
ones.

Not reconstructed — an order is a delivered artifact, and inventing one
puts a specification in the author's mouth.

The point survives the absence and is the sharpest thing in the handoff:
**everything this folder has run measures a corpus.** A known answer
declared by a generator's own authors would measure the **instrument**,
which is the `null-harness` known-truth-first invariant, and this folder
has never had one. The order is what is missing, not the argument.
