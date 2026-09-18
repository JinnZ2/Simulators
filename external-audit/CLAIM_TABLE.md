# CLAIM_TABLE.md -- external-audit

Claims `EA_001..EA_0nn` are properties of the two delivered documents and
of this repository's tree, recomputed here. Both delivered documents are
verbatim and are modified by nothing in this folder.

Every count below is reproduced by
`python3 external-audit/recount.py`; every execution result by
`python3 external-audit/run_instruments.py`. Neither number is stored in
prose anywhere in this folder, because a stored count is the object
`self-scan/` measures.

The report's family assignments, audience-fit scores and roadmap
priorities are declared as judgement in its own sections 1 and 15 and are
adjudicated nowhere here.

---

## EA_001 -- two of the folders the report counts do not exist

STATUS: SUPPORTED.

The family tables name **166** folders. `frame-token-audit` and
`gap-register` are not in the tree, and `git grep` finds neither string
anywhere at the surveyed revision -- so they are invented rather than
renamed. Real content folders: **164**.

FALSIFIER: either name resolving to a path, or occurring in any tracked
file outside this folder.

## EA_002 -- the surveyed revision is established, not stated

STATUS: SUPPORTED.

The report states a survey DATE and no commit. `baseline()` establishes
the revision instead: exactly one family (F3) moves between `6633778^`
and `6633778`, and the move is +8 files -- the exact size of the
`failure-mode-register` v3 landing in that commit. Seven families are
exact at the parent and six at the child, so the parent is the fit.

FALSIFIER: a second family moving between the two, which would leave the
date underdetermined by the counts.

## EA_003 -- seven of nine families reproduce exactly, and the two that
## do not are exactly the two carrying a folder that does not exist

STATUS: SUPPORTED. The headline.

At `6633778^`: F3 483, F4 214, F5 280, F6 11, F7 141, F8 175, F9 119 all
exact, and F5's 130 Python files and F6's zero are exact too. F1 is short
by 14 and F2 by 7. **The shortfall is 21, and family-sum 2652 + 21 =
2673, the report's own stated total, to the digit.**

So the report's arithmetic is internally consistent and externally wrong
by exactly the phantom folders. That is a stronger result than a
discrepancy: it locates the whole error.

FALSIFIER: any family reproducing inexactly while carrying no phantom, or
any family carrying a phantom and reproducing exactly.

## EA_004 -- the one directory the survey never names carries the
## refutation of two of its claims

STATUS: SUPPORTED. Section 12.2's "no test-running CI" is REFUTED.

`.github` is the only top-level directory the report's tables never name.
It holds `workflows/test.yml`, which runs `python -m unittest discover`
across **7** suites on push and pull request, and `workflows/study-watch.yml`,
which gates a scheduled job behind a `--selftest`.

Roadmap item 3 survives NARROWED rather than falling: CI exists and
covers 7 unittest suites; it runs neither the per-module `--selftest`
surface nor `tools/known_answer.py`.

FALSIFIER: the workflow files absent, or `test.yml` running no test.

## EA_005 -- "no installable package" is narrowed, not refuted

STATUS: NARROWED.

Three folders ship a package definition -- `crossdomain-eval`,
`fourd-municipal-engine`, `fourd-municipal-engine-v2` -- and the report's
own section 4.1 names the first one's CLI. The claim holds in the form
the roadmap actually needs it: there is no repo-wide installable core.

## EA_006 -- "no machine-readable claim index" holds, and is sharper than
## the report states

STATUS: SUPPORTED, and sharpened.

`tools/validate_claim_table.py` exists to validate a `CLAIM_TABLE.json`.
**Zero such files are in the tree**, against many `CLAIM_TABLE.md`. A
validator with no inputs is `CONSTANT_SILENT` at repository scale: it has
never been able to refuse anything. Roadmap item 1 is therefore not a new
build but the missing producer for a consumer already written.

This is also the one recommendation `RESPONSE_TO_REVIEW.md` section 5
accepts without objection, from the other direction.

## EA_007 -- the markdown-coverage enumeration is right and the count is
## two short

STATUS: PARTLY REFUTED.

The four named exceptions -- `exploration-engine`,
`exploration-playground`, `vector-field-explorer`, `voice-attractor-probe`
-- are all real. Two more folders carry no Markdown: `tools/` and
`tests/`, which are the two the report separately calls infrastructure.
On its own denominator the figure is **160 of 166**, not 162.

Enumeration and count are checked apart here for exactly this reason: a
document can list correctly and total wrong.

## EA_008 -- twenty-one individual numeric claims reproduce exactly

STATUS: SUPPORTED.

Nineteen root spine documents; no Python at the root; `tools/` 10 and
`tests/` 9; GAP_INDEX 255 entries across 24 folders; `guards.json` 8
guards; `placement.py --selftest` 24/24; `fragility-cascade` 173 files
and 85 Python; `energy` 66; `play-sims` 30/19; `relational` 38;
`gdprf-framework` 33; `msiaf-framework` 14 Markdown; `earth_economics`
21; `emergence-stability-simulator` 28/12; `machine-record-format` 10
Python; the two municipal engines 27+53 = 80.

`fragility-cascade` is stated twice in the report -- 173 files in one
section and "the 85-file audit" in another -- and both are right: one is
the file count and the other the Python count, in a sentence about
Python files. Recorded because the first reading was that it was a
contradiction, and it is not.

## EA_009 -- the report is now inside the tree it counts

STATUS: SUPPORTED. Third instance at repository scale.

Landing the report moves the top-level count and adds files, so a
working-tree recount measures the report's own arrival. `recount.py`
therefore pins every count to a revision and the selftest asserts the
report is NOT present at the revision it is counted against.
`UNI_010` / `ANC_001` / `QA_007` on the largest available substrate.

## EA_010 -- the report's section 0 is the house discipline arrived at
## independently

STATUS: SUPPORTED, and recorded as convergence rather than derivation.

Section 0 is a source-verification record placed BEFORE the body, with
two claims WITHDRAWN and their prior support named, and a
`NOT_VERIFIABLE_HERE` block recording the same arXiv CONNECT 403 with
`github.com` as the same reachability control that
`failure-mode-register/WORK_ORDER_V4.md` section 0-1 carries. Two parties,
same week, same refusal to discharge an unverified prior-art gate.

## EA_011 -- the response accepts an arithmetic that does not hold

STATUS: SUPPORTED. The disagreement runs toward the repository, so it is
stated rather than left.

`RESPONSE_TO_REVIEW.md` section 1 accepts the survey's arithmetic as
"internally consistent" and lists the sums as established. It is
internally consistent, and `EA_001`/`EA_003` show 21 files attributed to
two folders that do not exist. The response's own rule -- the
disagreement is stated rather than resolved in the repository's favour --
applies here in the direction it did not anticipate: the review
undercounted nothing, it counted two things that are not there, and the
response ratified the total.

## EA_012 -- O-1 answered: the instruments run

STATUS: SUPPORTED for the executions; the falsifier half of O-1 stays
OPEN.

`tools/known_answer.py`: **24 metrics registered, 24 expected, COMPLETE,
0 cases disagreeing**. `gate-check`: all four checks
`HELD_RETRIEVABLE`, 2331 files scanned. `self-scan/resolve.py`: all five
registered predictions HELD, one live divergence. The full `--selftest`
sweep is in `samples/` and its counts are printed by
`run_instruments.py`, never stored here.

O-1's second half -- checking claims against their own falsifiers --
is NOT done and is not a runner's job: it needs a reader per claim.

## EA_013 -- one live divergence, found by the repository's own scanner

STATUS: SUPPORTED.

`self-scan` reports `instrument-bias-sims/ 197 selftest checks green`
against an observed **220**, `BORN_DIVERGED` at +0.00 days -- the
artifact and the paragraph counting it committed together and not
agreeing even then. This is the state `self-scan` `SS_026` describes and
it is live at the surveyed revision.

## EA_014 -- UNVERIFIED: no external citation was checked

STATUS: UNVERIFIED, and it covers the folder.

The egress gate refuses every publisher host; the report's own section
0.3 records the same for its arXiv identifiers. Nothing in
`EA_001..EA_013` rests on an external source -- every one is a property
of this tree, recomputable by anyone with the clone.

## EA_015 -- five selftest output conventions, two refusal exit codes,
## and a reader written for one of them under-reports

STATUS: SUPPORTED, and found by running this folder's own instrument
against the tree rather than by reading either document.

The first sweep read **132 modules as NO_CHECKS that do print a check
count**, because its parser knew one convention. The tree uses five:

```
N/N checks passed
selftest: N checks, M failed
<name> selftest: N checks OK
checks: N   failed: M
SELFTEST PASS (M checks failed)
```

and refuses `--selftest` with exit **2** in one folder and exit **1** in
another. So neither the exit code nor a single format is the
discriminator. `run_instruments.py` now parses all five and recognises a
refusal structurally -- no checks reported AND the output names a
different `.py` file to run -- which is a property of what a refusal
does rather than a word list over "library" / "parser" / "run:", the
`T1-1` failure this repository names.

The repository's own `self-scan/census.py` shows the same symptom under
its own vocabulary: `RAN_NO_VERDICT` and `SOME_FAILED_UNCOUNTED` are
where a module's wording fell outside its reader.

FALSIFIER: a sixth convention in the tree. It would land in `NO_CHECKS`
rather than being absorbed, which is asserted.

## EA_016 -- the live self-test failures are content findings, not
## broken tests -- with one exception

STATUS: SUPPORTED. This is the answer the response's section 2 asked
for, in the form it asked for it.

Four of five are an instrument reporting on the corpus:

```
bridge-impoundment/selftest_bi.py        44 of 45
    "the register, Gap 2, and the loop marker are absent"

mining-increment/selftest_mi.py          55 of 56
    "the register, both scope modules, and Gaps 1 and 2 are absent"

zero-sum-curriculum-null/selftest_nc.py
    "the three named artifacts have no independent hit in the tree"
    -- ZSN_005 / ZSN_008 firing live

notes/check_datasets.py                  2 checks
    "G-SPAN resolves outside sim-span/ ... the term has an antecedent
     independent of the note and finding 3 must be restated"
```

The fourth is the sharpest in the sweep: an instrument telling its
operator that a finding recorded earlier has gone stale, and naming the
file that broke it.

The fifth is a broken run and is `EA_018`.

Two more rows are properties of the sweep and not of the tree, and are
kept in their own states rather than counted as failures:
`tests/test_sourced.py` and `tests/test_study_watch.py` are unittest
files whose parser rejects the flag (`FLAG_NOT_ACCEPTED`), and
`ch4-four-box/tn_inversion.py` and `units_test.py` carry their checks on
plain invocation (`RUNS_BARE`, established by re-running them bare, not
by reading their wording).

## EA_017 -- O-1 is half answered, and the half that is not is not a
## runner's job

STATUS: PARTLY SUPPORTED, half OPEN.

`tools/known_answer.py` (24 metrics, 24 expected, COMPLETE, 0 cases
disagreeing), `gate-check` (four checks, all `HELD_RETRIEVABLE`, 2331
files scanned), `self-scan/resolve.py` (all five registered predictions
HELD) and the full `--selftest` surface have been run at a pinned
revision. That is O-1's first clause.

The second clause -- "no claim in any CLAIM_TABLE was checked against
its own falsifier" -- is NOT done here. It needs a reader per claim
across 98 claim tables, and a runner cannot do it. It stays open, and
`EA_006` names the artifact that would make it tractable: the claim
export is a validated format with no producer.

## EA_018 -- a delivered input four modules read is not in the tree, and
## one published regeneration claim cannot be checked because of it

STATUS: SUPPORTED. Found by the sweep, confirmed by hand, and it is a
repository defect rather than an artifact of the sweep.

`columbia-chain-cascade/UNDERGRADUATE_RESEARCH_GAPS.md` -- the v1 gap
file -- is referenced by `assemble_gaps_v2.py`, `gap_completeness.py`,
`kill_audit.py` and `selftest_kill.py`, and only
`UNDERGRADUATE_RESEARCH_GAPS_V2.md` is in the tree.

Two consequences:

```
selftest_kill.py    dies on FileNotFoundError before its first check
assemble_gaps_v2    cannot run at all: its whole job is to build v2 from
                    v1 verbatim
```

So the published claim that v2 is v1 plus two cards plus the addenda,
and that *stripping the fences returns v1 byte-for-byte*, **is not
checkable from this tree** -- the input side of the identity is absent.
That is the `SS_026` shape: a stated relationship whose operand is not
there, and it was invisible until something ran.

FALSIFIER: the v1 file landing, after which `assemble_gaps_v2.py --check`
either reproduces v2 or does not, and either outcome is a result.

---

## The second pass (`DEEP_RESEARCH_2026_09_14_V2.md`)

The review landed twice. The second rendering replaces section 0 with an
execution record answering the response's request, and so becomes a
second independent sweep of this tree to set beside `run_instruments.py`
and beside the repository's own `self-scan/census.py`. Claims
`EA_019..EA_027` are about the pair, computed by `crosscheck.py`.

### EA_019 -- the second pass is a revision, and it REPLACES its own verification record

STATUS: SUPPORTED.

580 of 649 lines are equal, ratio 0.9070, **0 lines deleted wholesale**
-- a revision, not a rewrite. The change is concentrated in the front
matter and in section 0, which does not grow: v1's `## 0.
Source-verification record` is **replaced** by v2's `## 0. Re-audit
addendum`, and with it v1's two tables -- the WITHDRAWN claims table and
the arXiv `NOT_VERIFIABLE_HERE` table -- survive only as prose bullets in
v2 section 0.3. Both renderings are landed side by side rather than one
overwriting the other, which is this repository's own supersession
convention applied to a document delivered from outside it.

**The family tables are byte-identical across the two renderings**
(9 families parsed from each, equal), so `recount.py` reads both with one
parser and every `EA_001..EA_014` arithmetic finding carries to the
second pass without recomputation -- including the two phantom folders
and the 2652 + 21 = 2673 reconciliation. `recount.report_text` and
`recount.families` were generalised to take a document rather than being
copied, the `MF_019` discipline and the move `entries_v2`/`entries_v3`
already made for the four work orders.

FALSIFIER: a third rendering whose family tables differ from these.

### EA_020 -- two outside readers of one known-answer run reported 0 and 2, and both were right

STATUS: SUPPORTED, and it is the cleanest VOID RATIO instance in the
tree.

`tools/known_answer.py` prints **84 PASS and 2 FAIL (pinned)** per case,
and then a headline reading `cases disagreeing with the registry: 0`.
The second pass read the per-case verdicts and reported `84 PASS + 2 FAIL
(pinned)`. `run_instruments.py` read the headline and reported 0. Neither
reader was careless: the headline counts disagreement with what the
registry **expects**, and a pinned failure that fails agrees with its
expectation, while the per-case column counts raw verdicts. One name over
two denominators, on a summary line -- `measurement-fork`'s VOID RATIO,
demonstrated rather than argued, because two parties who never spoke
produced the two numbers.

The gate exits 0 and is correct to: a pinned failure is expected. What is
missing is that the headline does not say which quantity it is.

FALSIFIER: a third reader of the same run reporting a number that is
neither 0 nor 2.

### EA_021 -- the two sweeps ran at different revisions, and the gap is this audit folder

STATUS: SUPPORTED.

`gate-check` reports `files_scanned` and both sweeps quote it: the second
pass **2342**, `run_instruments.py` **2331**. The second pass states a
survey date and no commit; ours pins `6633778` by its own `[CHOICE 11]`.
2342 is what the tree scans at `f02edb3`, and the eleven-file difference
is `external-audit/` landing. So the first candidate explanation for any
divergence between the sweeps is the revision, not the runner -- and the
measurement moved because the measuring was committed, which is
`UNI_010` / `ANC_001` / `QA_007` at repository scale, reached through the
instrument rather than through the index.

`crosscheck.py` therefore takes every file count at a **commit**, never
the working tree (`[CHOICE 6]`), since this audit is still being written
into the tree it measures.

FALSIFIER: the two counts agreeing at one revision.

### EA_022 -- four of five failures agree; each sweep carries one the other missed

STATUS: SUPPORTED.

| module | second pass | ours |
|---|---|---|
| `bridge-impoundment/selftest_bi.py` | FAIL | FAIL |
| `mining-increment/selftest_mi.py` | FAIL | FAIL |
| `columbia-chain-cascade/selftest_kill.py` | FAIL | FAIL |
| `zero-sum-curriculum-null/selftest_nc.py` | FAIL | FAIL |
| `evaluation-frame/selftest_frame.py` | FAIL | -- |
| `notes/check_datasets.py` | -- | FAIL |

The `selftest_kill.py` row is `EA_018` reached independently from
outside: the folder carries only `UNDERGRADUATE_RESEARCH_GAPS_V2.md`
while four modules read the v1 name, so the published *strip the fences
and v1 returns byte-for-byte* identity has no input side in this tree.

FALSIFIER: a re-run at one revision in one sandbox in which the two sets
are equal.

### EA_023 -- `evaluation-frame`'s selftest reads a path outside the repository

STATUS: SUPPORTED, and it is the sharpest result of the cross-check.

`evaluation-frame/frame.py` sets `CORPUS_DIR =
"/root/.claude/projects/-home-user-Simulators"` and says in its own
comment that *the transcript is not a checked-in artifact*. The selftest
returns 73 checks, 0 failed here, at `6633778` and at `f02edb3` alike;
the second pass reports it failing a masking check. **Neither party is
wrong.** The verdict is a property of the sandbox, not of the tree, so
`crosscheck.py` reports it `ENVIRONMENT_DEPENDENT` and scores it against
neither sweep (`[CHOICE 5]`).

`EF_009` already records that this corpus is written by the run that
reads it. This is that finding measured from outside, by a party who
could not have known to look for it -- the decorrelated-shadow result
`triad-playground` `TP_008` says a consensus statistic is worthless
without, arriving for free because nobody coordinated.

FALSIFIER: the module returning the same verdict in a sandbox with no
transcript at that path.

### EA_024 -- `notes/check_datasets.py` is not an exit/verdict mismatch, and a first pass here said it was

STATUS: SUPPORTED, and the error was mine.

The module prints `SELFTEST FAIL (2 checks failed)` and exits **1**. A
first reading in this session recorded exit 0 -- because the exit code
was taken from a pipeline (`... | tail -3; echo $?`) rather than from the
module. That is the same class of defect this folder exists to find,
committed inside it, and it is recorded rather than quietly corrected.

FALSIFIER: none needed; the exit code is one command away.

### EA_025 -- the reported exit/verdict mismatch is the refusal convention, and the defect is in the census

STATUS: SUPPORTED, and this is the finding that pays for the cross-check.

The second pass's section 0.1 reports that the repository's own census
surfaces *three tools that report zero failed checks in their output
while exiting nonzero -- an exit-code/verdict mismatch*, and names
`failure-mode-register`, `internal-reference-boundary` and
`tools/sourced.py`. Run here, those three are green and exit 0 at their
runners; what exits nonzero in those folders is the **module**, which
refuses `--selftest` with exit 2, prints no failed-check count, and names
the runner that holds the checks -- the house convention.

Running the census directly shows something sharper. Four rows come back
`SOME_FAILED_UNCOUNTED` **on output that says `failed: 0`**:

```
failure-mode-register/test_register_v2.py   SOME_FAILED_UNCOUNTED  checks: 142   failed: 0
failure-mode-register/test_register_v3.py   SOME_FAILED_UNCOUNTED  checks: 132   failed: 0
internal-reference-boundary/test_boundary.py SOME_FAILED_UNCOUNTED checks: 198   failed: 0
tools/sourced.py                            SOME_FAILED_UNCOUNTED  checks: 41    failed: 0
```

`checks: N   failed: M` is a fourth output convention that
`self-scan/resolve.py::parse_count` did not parse, so it fell through to
the heuristic, whose dirty test is `\b[1-9]\d*\s+failed\b` -- and that
matches **the check count**, `142   failed`, not the failure count. The
clean test `\b0\s+failed\b` does not fire, the zero sitting after the
word, so the misread was unambiguous rather than a tie. Four green
modules were filed as failing by their own passing output.

So the second pass detected a real anomaly and attributed it to the three
tools; the anomaly is in the instrument that reported it, and the three
tools are exactly the folders whose runners use that convention.

REPAIRED in `parse_count` rather than in the census, since census calls
it and `resolve.py` reads it too, with four checks pinned in
`resolve.py --selftest` including the two that state why the shape has to
be parsed rather than classified. The census before and after, whole
tree, nothing else changed:

```
                        before   after
GREEN                      146     150
SOME_FAILED_UNCOUNTED        5       1
checks counted            6236    6749
```

Four modules moved from a failure bin into GREEN on unchanged output, and
**513 checks that were already passing started being counted** -- the
repo's own headline check total was 8% low because four suites' results
were unparsed. The one row remaining in `SOME_FAILED_UNCOUNTED` is
`notes/check_datasets.py`, which genuinely fails.

FALSIFIER: a fifth convention landing and reaching the heuristic.

### EA_026 -- three readers, one trap, and only the one that named a state avoided it

STATUS: SUPPORTED.

The trap is a refusal read as a failure. `run_instruments.py` fell into
it first and recorded it as `EA_015`, repairing it with a structural
refusal test and a `REFUSED` bin. `self-scan/census.py` bins it honestly
as `NONZERO_EXIT_NO_VERDICT` -- 109 rows, the largest bin in the tree --
and the second pass read that bin as a defect in the tools it names.
Three independent readers, one trap; the only one that did not fall in is
the one carrying a state for it, which is the absent-vs-known-negative
repair doing exactly what this repository claims for it, on evidence
nobody here produced.

FALSIFIER: a reader with a `REFUSED` bin that still reports a refusal as
a failure.

### EA_027 -- this folder changed another folder's check, and the check said so

STATUS: SUPPORTED.

`notes/check_datasets.py` fails with *G-SPAN resolves outside sim-span/*
and names three files, two of them `external-audit/CLAIM_TABLE.md` and
`external-audit/README.md`. At `6633778` it named only
`notes/memory-export/`. The audit landed, the terms acquired an
antecedent independent of the note the check was written to guard, and
the check reported it and named the files -- it is not broken, it is
working, and what it caught is the audit.

FALSIFIER: the check naming no `external-audit/` file at a revision that
carries this folder.
