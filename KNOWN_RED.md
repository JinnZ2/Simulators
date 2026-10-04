# KNOWN_RED.md — the expected-failure baseline

License: CC0.
Baseline established: 2026-09-14, from an external execution pass.
Runner: independent third party (Kimi), 84 executed self-tests plus `self-scan/census.py`.

**Check your failure set against this file before writing anything up.**

```
failure listed here       -> CONFIRMATION. The drift is recorded. Not news.
failure NOT listed here   -> NEW. This is the interesting result. Report it.
listed failure now green  -> ALSO NEW. Something was repaired or something moved.
                             Say which, and say who.
```

Without this file every runner rediscovers the same five drifts and reports them as
findings, which makes repeat runs incomparable and wastes the one thing a second runner
is for.

---

## 1. PINNED RED — by design, never repair

These are calibration anchors in `tools/known_answer.py`. They are documented historical
metric bugs, kept red so the gate proves it can detect a bug at all.

```
ID                  DEFECT                        STATUS
null-harness        verdict-string collision      PINNED. Do not fix.
nonidentity-census  marginal-majority bug         PINNED. Do not fix.
```

Expected gate output: 24/24 registered metrics complete, 84 case verdicts PASS, 2 FAIL.
That is the gate HOLDING. A run reporting 86 PASS / 0 FAIL means the anchors were
removed, and the gate can no longer demonstrate sensitivity.

---

## 2. OPEN DRIFTS — real, recorded, awaiting repair

Four of five share one shape: the test layer references artifacts the folder no longer
contains. This is documentary drift, not computational error.

```
D-1  bridge-impoundment/selftest_bi.py
     FAIL: "the register, Gap 2, and the loop marker are absent."
     SHAPE: test outlived its artifacts
     REPAIR IS AMBIGUOUS: either the artifacts were removed and should be restored,
     or the test's expectation is stale. Determine which before editing either side.

D-2  mining-increment/selftest_mi.py
     FAIL: "the register, both scope modules, and Gaps 1 and 2 are absent."
     SHAPE: same as D-1. Same ambiguity.

D-3  evaluation-frame/selftest_frame.py
     FAIL: masking check — tokens fire unmasked that the design requires masked.
     SHAPE: DIFFERENT. This is a logic assertion failing inside one instrument, not a
     missing file. The only one of the five that is about behaviour rather than
     bookkeeping. Highest diagnostic value.

D-4  columbia-chain-cascade/selftest_kill.py
     FileNotFoundError: expects UNDERGRADUATE_RESEARCH_GAPS.md
     folder carries UNDERGRADUATE_RESEARCH_GAPS_V2.md
     SHAPE: the test is out of sync with the folder's own supersession.
     UNAMBIGUOUS: this is the TEST's defect. The artifact superseded correctly and the
     test was not updated. Smallest repair in the set.
     CLASSIFICATION DISAGREEMENT: this sweep counted it a crash; census filed it
     NONZERO_EXIT_NO_VERDICT. The census label is arguably the more honest one, since a
     crashed test delivered no verdict. Recorded, not resolved.

D-5  zero-sum-curriculum-null/selftest_nc.py
     32/33 checks pass. FAIL: "the three named artifacts have no independent hit in
     the tree."
     SHAPE: same family as D-1/D-2.

D-6  self-scan/resolve.py                    SOME_FAILED
D-7  notes/check_datasets.py                 SELFTEST FAIL, 2 checks failed
     Found by census only; the entry-point sweep missed both. On the census's
     authority, bringing the honest total to seven named drifts.
```

---

## 3. CONTRACT VIOLATIONS — not failures, but the harness cannot tell

Three tools report zero failed checks in their output while exiting nonzero.

```
failure-mode-register
internal-reference-boundary
tools/sourced.py
```

An exit-code/verdict mismatch is precisely the failure mode `null-harness` is pinned red
for: the verdict string and the exit status disagree, so a runner reading one gets a
different answer than a runner reading the other. See `EXIT_CONTRACT.md`.

These are the highest-leverage repairs in this file, because each one silently corrupts
every future automated sweep.

---

## 4. HYGIENE — non-failing

```
columbia-chain-cascade/selftest_ccc_v2.py:261    SyntaxWarning, invalid escape sequence
```

---

## 5. AGGREGATE STATE AT BASELINE

```
tools/known_answer.py        24/24 complete; 84 PASS + 2 FAIL (pinned)   GATE HOLDS
unittest discover tests      105 tests, OK, ~84s
selftest sweep (84 files)    79 pass / 5 genuine failures
gate-check self              2 HELD_RETRIEVABLE / 2 NOT_HELD
                             (no failure-covering tests, no demo file)
gate-check full tree         2,342 files, all four checks HELD_RETRIEVABLE
self-scan/census.py          5 SOME_FAILED / 5 SOME_FAILED_UNCOUNTED /
                             110 NONZERO_EXIT_NO_VERDICT / 8 OK
falsifier-audit/selftest_fa  28 checks, 0 failed
```

The 110 `NONZERO_EXIT_NO_VERDICT` rows are the largest uncharacterised block in the
tree. They are not failures. They are instruments that did not report, and nobody has
walked them to find out why. That is the biggest single open measurement here.

---

## 6. STILL UNMEASURED

```
CLAIM_TABLE falsifiers have never been executed AS STATED. Running a self-test checks
that a folder is internally consistent. Executing a falsifier checks whether the claim
is WRONG. These are different measurements and only the first has been done.

falsifier-audit/selftest_fa.py passing (28 checks, 0 failed) indicates the extraction
layer is ready for it.

SUBSTANTIVE CORRECTNESS is untouched. A flood model that passes its self-test may still
be a poor flood model. Runnability and self-consistency were measured; correctness about
the world was not, and is not claimed anywhere in this repository.
```

---

## 7. HOW TO UPDATE THIS FILE

Append, do not overwrite. A drift that was repaired keeps its entry with the repair
dated and the repairing change named, because a row that disappears cannot be
distinguished from a row nobody re-ran.

---

## 8. SECOND PASS — 2026-09-14, in-repo runner

Appended per §7. Nothing above this line was edited, including §3, which does
not reproduce: the row stays so that the non-reproduction is a second reading
of it rather than its disappearance.

Runner: an in-repo session on branch `claude/agents-md-guidelines-n9drqg`, at
the commit that landed AGENTS.md, KNOWN_RED.md and EXIT_CONTRACT.md. Method:
direct execution, exit codes read from the shell. Every number below is
recomputable by anyone with the clone.

INTEREST DECLARED. This pass is by a model, grading a baseline produced by a
different model, and it reports that the other runner's self-described
highest-leverage finding does not reproduce. That is a claim in this runner's
favour. It rests on exit codes and `failed:` lines across 24 invocations, so it
does not turn on this runner's judgement, and a third party with the clone
settles it in a minute.

### 8.1 CONFIRMED

```
tools/known_answer.py     24/24 metrics COMPLETE, 84 PASS, 2 FAIL, exit 0.
                          Both FAIL rows are marked FAIL (pinned) and are
                          exactly the two §1 anchors. The gate holds.
unittest discover tests   Ran 105 tests, OK. Exact, not approximate.
D-4                       Confirmed structurally without running it: the
                          folder carries only UNDERGRADUATE_RESEARCH_GAPS_V2.md
                          while selftest_kill.py names the bare filename at
                          four sites (lines 200, 306, 317, 340).
```

### 8.2 §3 DOES NOT REPRODUCE

§3 names three tools that "report zero failed checks in their output while
exiting nonzero" and calls them the highest-leverage repairs in this file.
Swept all 12 entry points across the three targets, bare and `--selftest`:

```
24 invocations, 0 mismatches.

  tools/sourced.py                 bare 0      --selftest 0   (41 checks, 0 failed)
  failure-mode-register            test_register.py    0      (209 checks, 0 failed)
                                   test_register_v2.py 0      (142 checks, 0 failed)
  internal-reference-boundary      test_boundary.py    0      (198 checks, 0 failed)

  6 nonzero rows, all exit 2, all emitting a redirect naming the real entry
  point. AGENTS.md §4 and EXIT_CONTRACT §1 both class exit 2 as NOT a failure.
```

So §3 is the redirect state misfiled, and the two documents landing beside it
already carry the correction. The row is left standing under §7, because a
reader comparing a later sweep against a deleted row cannot tell a repair from
a row nobody re-ran — which is the failure §7 exists to prevent, and which this
row would have caused: nothing was repaired, so a third runner finding those
three green would wrongly credit somebody.

### 8.3 NEW — one real contract violation, of exactly the class §3 claimed

```
anchor-position/normalize.py
    sys.exit("normalize.py is a library; run: python3 score.py --selftest")
    measured: exit 1, message on stderr, no VERDICT line

A redirect. sys.exit(<str>) prints to stderr and exits 1, which EXIT_CONTRACT §1
reads as "checks ran; at least one FAILED -- a RESULT". 101 sibling redirects
declare 2. One file, and it is the only one.
```

PINNED in `tests/test_run_manifest.py`. Repairing it turns that test red on
purpose: the repair has to arrive with an update to this file.

### 8.4 NEW — the §5 block of 110 has a candidate account

`tools/run_manifest.py` landed this pass (AGENTS.md §1 named it and it did not
exist). It classifies every tracked `.py` from the AST, running none of them:

```
REDIRECT        102      SELFTEST     82      TEST_FILE   146
CLI             390      LIBRARY     240      UNPARSEABLE   1
UNCLASSIFIED      0      <- a visible zero, never a bucket of last resort
```

Validated against execution in both directions: all 102 predicted redirects were
run, 101 exit 2, and the single deviation is §8.3, which the classifier had
already flagged. A 15-file sample of SELFTEST contains no hidden redirect.

`self-scan/census.py` sweeps modules whose source contains `--selftest` and
files a nonzero exit with no VERDICT line as NONZERO_EXIT_NO_VERDICT. That
population is REDIRECT + SELFTEST = 184, of which 102 are redirect stubs that
exit 2 and print no VERDICT line. So the largest uncharacterised block in the
tree is mostly, and possibly almost entirely, the redirect class — which the
contract says is not a failure and which AGENTS.md §4 was written to stop a
sweep from counting as one.

### 8.5 UNPARSEABLE is a state, and one file is in it

```
relational/cartesian_vs_relational_demo.py
    SyntaxError under python 3.11: invalid decimal literal
    PEP 701 nested same-quote f-strings; needs 3.12+. Already recorded in
    CLAUDE.md. It is neither a pass nor a failure, and a sweep that files it
    as either is wrong in a way the third state makes visible.
```

### 8.6 MOVED BY THIS CHANGE — said here because §7 asks who moved it

```
unittest discover tests   105 -> 121 tests, OK.
                          +16 from tests/test_run_manifest.py, added this pass.
```

§5's baseline figure of 105 is therefore stale by this runner's own doing rather
than by drift, and is left standing as the baseline it is. AGENTS.md §1 reads
"~105 tests" and now understates by 16. Not corrected here: the record lands
first and the correction is a separate change, because correcting a number in
the same commit that reports it removes the evidence that it ever differed. The
house repair for a stored count is to delete the count and name the command that
produces it.

### 8.7 STILL UNMEASURED — unchanged

§6 stands in full. CLAIM_TABLE falsifiers have still never been executed as
stated, and substantive correctness is still untouched. Nothing in this pass
bears on either.

The EXIT_CONTRACT §5 check is also still unbuilt. `run_manifest.py` is its
static half only: it reads the exit code a redirect DECLARES, never the one it
emits, and the two can disagree. Closing it means running each entry point and
comparing its VERDICT line against its exit status, which is the measurement
the manifest exists to make cheap and does not itself perform.

### 8.8 A GAP IN THE CONTRACT ITSELF

EXIT_CONTRACT §1 has four states and none of them describes the tree's own
calibration gate. `tools/known_answer.py` prints 2 FAIL rows and exits 0, by
design, because those rows are the anchors that prove it can detect a bug at
all. Exit 0 reads "all passed" and is false of it; exit 1 reads "at least one
FAILED" and would make the gate red forever. The state is "checks ran, failures
present and expected," and the table has no row for it.

---

## 9. SECOND PASS, CONTINUED — census run, and a correction to §8

Appended per §7. §8 is left standing, including the part of it that is wrong.

### 9.1 CORRECTION to §8.2

§8.2 concluded that §3 does not reproduce and offered an account: "the redirect
state misfiled." The conclusion stands and is independently established by the
24 direct invocations. **The account was wrong**, and `self-scan/census.py`
names the real mechanism. Superseded, not deleted, so the correction is legible
as a correction.

### 9.2 THE MECHANISM — a defect in census.py, not in the three tools

`census.py` line 189 screens output it could not parse:

```
dirty = re.search(r"SELFTEST\s+FAIL\b", out) or \
        re.search(r"\b[1-9]\d*\s+failed\b", out)
clean = re.search(r"SELFTEST\s+PASS\b", out) or \
        re.search(r"\b0\s+failed\b", out)
```

Against the tree's prevailing verdict line the number it reads is the CHECK
count, not the failure count:

```
  checks: 41   failed: 0                 dirty=True   clean=False
  checks: 0    failed: 0                 dirty=False  clean=True
  VERDICT: PASS   checks=35 failed=0     dirty=True   clean=False
```

A module with 41 passing checks is dirty; a module with zero checks is clean.
The screen is monotone in the wrong quantity: the more checks a module runs, the
dirtier it reads.

`resolve.parse_count` reaches this branch only when it cannot extract a count,
and its patterns want `N checks, M failed` with a comma. The colon form
`checks: N   failed: M` misses, so it falls through to the screen, where it is
guaranteed to be filed dirty: clean cannot match that form and dirty always can.

The branch carries a comment saying it exists so that "reporting those as
RAN_NO_COUNT beside a module that errored would put a green module and a broken
one in one bin, which is the mistake this whole folder is about." The regex
performs exactly that: it puts `tools/sourced.py` (41 checks, 0 failed, exit 0)
in the same bin as `notes/check_datasets.py` (2 checks genuinely failed, D-7).

One folder demonstrates it without leaving the folder:

```
failure-mode-register/test_register.py     "209 checks, 0 failed"    -> parsed, GREEN
failure-mode-register/test_register_v2.py  "checks: 142   failed: 0" -> unparsed, DIRTY
```

Same folder, same green state, two formats, two census verdicts.

NOT REPAIRED HERE, per AGENTS.md §2: recorded now, fixed in a separate change,
so the failure and the repair are both in the record.

### 9.3 §3 IS NOW FULLY EXPLAINED — 3 of 3

Census files these as SOME_FAILED_UNCOUNTED:

```
failure-mode-register/test_register_v2.py    <- §3 row 1   (142 checks, 0 failed)
internal-reference-boundary/test_boundary.py <- §3 row 2   (198 checks, 0 failed)
tools/sourced.py                             <- §3 row 3   ( 41 checks, 0 failed)
notes/check_datasets.py                         D-7, a genuine failure
tools/run_manifest.py                           added this pass; see §9.5
```

All three of §3's rows are census false positives from §9.2. §3 is a census
state transcribed into a baseline as a claim about exit codes. Every one of the
three exits 0 and prints 0 failed.

### 9.4 THE §5 BLOCK OF 110 IS SETTLED — §8.4 superseded with the number

Census reproduces the baseline closely on an in-repo run:

```
                          §5 baseline    this pass
NONZERO_EXIT_NO_VERDICT       110           110      exact
SOME_FAILED                     5             5      exact
OK                              8             8      exact
SOME_FAILED_UNCOUNTED           5             6      +1, and the +1 is ours (§9.5)
RAN_NO_VERDICT              not recorded     18
```

Joining the 109 parsable NONZERO rows against the manifest:

```
  REDIRECT      102      not failures. Each names its real entry point.
  CLI             6
  TEST_FILE       1
```

So the largest uncharacterised block in the tree is 102 redirect stubs plus
**seven** genuinely uncharacterised rows. §6's "biggest single open measurement"
shrinks from 110 to 7, and none of the 102 needed running to be characterised.

### 9.5 THE R-2 REPAIR IS BLOCKED BY §9.2

EXIT_CONTRACT §4 R-2 says to add the VERDICT line to every entry point lacking
one, and calls it mechanical and second in leverage. Executed today it would
mis-file every entry point it touches:

```
  VERDICT: PASS   checks=33 failed=0   -> parse_count None -> dirty -> SOME_FAILED_UNCOUNTED
  VERDICT: FAIL   checks=33 failed=1   -> parse_count None -> dirty -> SOME_FAILED_UNCOUNTED
```

PASS and FAIL become indistinguishable under the tree's own whole-tree runner.
`tools/run_manifest.py` is the first instance and it arrived this pass: it emits
the contract's prescribed line, is green at 35 checks 0 failed, and census files
it SOME_FAILED_UNCOUNTED. The instrument that conforms to the contract is the
one the runner mis-reads.

ORDER: §9.2 before R-2. Either teach `parse_count` the contract's format, or
make the screen read the number that follows `failed`, and null-test it on both
formats before anything is rolled out.

### 9.6 ENVIRONMENT — census's pytest arm is blind here

```
python3 -m pytest   ->  No module named pytest
```

Every `*/tests` row is NO_SUMMARY for that reason, not because the suites are
broken. §5's "unittest discover tests, 105 tests, OK" came from a direct
unittest run and is unaffected. A sweep on a machine without pytest and one with
it are not comparable on that arm, which is the same requirement §5's own
NOT_TESTABLE split states: a rate quoted without its environment has an unstated
denominator.

### 9.7 A METHOD NOTE ON THIS PASS

The first census run here was piped through `tail -40` and gave totals of 24
NONZERO and 3 SOME_FAILED_UNCOUNTED. Those were the last forty lines, not the
run. Caught before anything rested on them, and recorded because a truncated
sweep reported as a sweep is the same defect class as everything above: a number
whose stated source does not support it.

---

## 10. THIRD PASS — a correction to §9.4, from a defect in the manifest

Appended per §7. §9.4 stands as written; this reads it a second time rather
than replacing it.

§9.4 joined census's 109 parsable `NONZERO_EXIT_NO_VERDICT` rows against
`tools/run_manifest.py` and reported:

```
  REDIRECT      102
  CLI             6
  TEST_FILE       1     -> "seven genuinely uncharacterised rows"
```

**The six CLI rows were redirects the classifier could not see.** Recomputed on
the repaired classifier, against the same census output:

```
  REDIRECT      108
  TEST_FILE       1     -> ONE uncharacterised row
```

### 10.1 The defect

`run_manifest.py` found a module's checks by looking for the literal
`"--selftest"` inside an `if` test. A module that declares the flag through
argparse and tests `args.selftest` carries the literal only in an
`add_argument` call, so the classifier saw no selftest branch and filed the
module as `CLI`.

Found by writing two argparse-style modules in `substrate-alternative/` and
reading their rows, not by reading the classifier. No fixture written by the
same hand that wrote it would have caught this, for the same reason the earlier
two defects in that file needed real input: the author writes one style.

Blast radius across the tree:

```
SELFTEST   85 -> 130     45 modules carrying checks were filed as CLI
REDIRECT  102 -> 108      6 redirects were missed entirely
CLI       392 -> 342
LIBRARY   240 -> 239
```

So the manifest was under-reporting the check surface it exists to enumerate by
45 modules, in the file whose whole argument is that a sweep should know what it
is choosing not to measure.

### 10.2 What moves and what does not

```
§6  "biggest single open measurement"     110 -> 7 (§9.4) -> 1 (here)
§9.4 join                                  superseded by the numbers above
§9.2 census dirty-regex defect             unchanged, still unrepaired
§9.3 §3 fully explained, 3 of 3            unchanged
§9.5 R-2 blocked by §9.2                   unchanged
§1  pinned anchors                         unchanged, 24/24 with 84 PASS 2 FAIL
contract violations                        unchanged at one, normalize.py
```

The one remaining uncharacterised row is a `TEST_FILE`. Nobody has walked it.

### 10.3 Recorded because the direction matters

Every correction in this file so far has made a reported problem smaller: §3
did not reproduce, §9.4 cut 110 to 7, this cuts 7 to 1. That is three
consecutive findings shrinking under measurement, which is worth noticing as a
pattern rather than as three separate reliefs. The instrument was wrong in the
alarming direction each time.

The one that did not shrink is §9.2, which was found rather than inherited and
is still open.

---

## 11. FOURTH PASS — 2026-09-29, baseline taken for PR #101 (potential/)

`python3 -m unittest discover tests` on `main @ 5b727ca`: 133 run, 8 FAIL. Run
again on the PR head with the same command: 133 run, 8 FAIL, the same eight by id.
None of the eight is in §1–§10 above. Every one is on a path PR #101 does not touch.

```
test_known_answer_gate.ManifestIsCovered.test_every_manifest_entry_is_registered
     pre-existing, byte-identical across this PR
     five MANIFEST ids never registered: unowned-join/invariant.py::join_coverage,
     assessor-coupling/conditions.py::pool_fraction,
     instrument-index/build_index.py::claim_only_fraction,
     cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes,
     cooperative-substrate-proof/p5_lag.py::lag_ratio
test_known_answer_gate.SeedReachability.test_every_registration_is_reachable_from_seed
     pre-existing, byte-identical across this PR
     five register() sites in _tra_sle_to_sv (thwaites-risk-audit) that seed() does
     not reach — the MSV_024 shape, fifth instance
test_known_answer_gate.TheGateFires.test_the_registry_is_complete
     pre-existing, byte-identical across this PR
     registered 43 / expected 48 before; 45 / 50 after (PR adds two ids to both lists)
test_known_answer_gate.ToolRuns.test_tool_exits_clean
     pre-existing, byte-identical across this PR
     tools/known_answer.py exits 1 on the two rows above; 0 cases disagree either run
test_run_manifest.TestArgparseSelftestForm.test_argparse_declared_selftest_is_not_filed_as_cli
     pre-existing, byte-identical across this PR
test_run_manifest.TestArgparseSelftestForm.test_those_modules_really_carry_checks
     pre-existing, byte-identical across this PR
test_run_manifest.TestRedirectContract.test_no_redirect_names_a_target_that_is_missing
     pre-existing, byte-identical across this PR
test_run_manifest.TestRedirectContract.test_the_one_known_violation_is_pinned
     pre-existing, byte-identical across this PR
     the four test_run_manifest rows are §10's subject, not yet repaired
```

Beside them, not new: `discover -s grounding-layers` returns 215 run, 18 ERROR
(import failures), the state CLAUDE.md records for that folder.

Two failures NEW to the tree in this pass, both INSIDE potential/ and both found by
running after two masking defects were repaired (P-03, P-04); recorded in
`potential/INVENTORY.md` as P-17 and P-18, listed and not repaired because the
order that landed them did not name them:

```
potential/test_perturbation.py            UnboundLocalError: PERTURBATIONS (re-import
                                          inside the function that first reads it)
potential/tools/registry_sourced.py       --selftest asserts verified != unverified on
                                          a fixture that yields 1 and 1
```

## 12. FIFTH PASS — 2026-09-30, PART B item 13: the §11 known-answer half, closed

Bounded to the two §11 rows the order named — the five `register()` sites in
`_tra_sle_to_sv` that `seed()` could not reach, and the five MANIFEST ids never
registered — and they were one defect: the five blocks had been committed
(79800d3, 6ee102a, 209af6d, f5339f9) after the `return` of `_tra_sle_to_sv`,
dead code inside a helper `seed()` never calls, so each id was unreachable AND
absent from the registry at once. Moved unchanged into `_seed_work_order_metrics()`,
called from `seed()`. `seed_reachable()` was written against exactly this shape
(fourth occurrence) and this is the first instance it caught by itself.

`python3 -m unittest discover tests` on `claude/potential-part-b-k7Qm`: 133 run,
4 FAIL (was 8). `python3 tools/known_answer.py` exits 0: registered 50 / expected
50 COMPLETE, 0 call sites unreachable, 0 cases disagreeing. CLOSED, by id:

```
test_known_answer_gate.ManifestIsCovered.test_every_manifest_entry_is_registered
test_known_answer_gate.SeedReachability.test_every_registration_is_reachable_from_seed
test_known_answer_gate.TheGateFires.test_the_registry_is_complete
test_known_answer_gate.ToolRuns.test_tool_exits_clean
```

EXACTLY WHAT IS LEFT of §11, red and untouched, §10's subject:

```
test_run_manifest.TestArgparseSelftestForm.test_argparse_declared_selftest_is_not_filed_as_cli
test_run_manifest.TestArgparseSelftestForm.test_those_modules_really_carry_checks
test_run_manifest.TestRedirectContract.test_no_redirect_names_a_target_that_is_missing
test_run_manifest.TestRedirectContract.test_the_one_known_violation_is_pinned
```

Beside them, not new but newly VISIBLE — reaching the five registrations ran their
cases for the first time, and `metrics exercised: 44 of 50, cases NOT_RUN: 33`.
The gate does not fail on NOT_RUN (a case that raised on the way in is recorded,
not scored), so these are on no red test; they are listed here because a registry
reading COMPLETE with six metrics never exercised is the state `SS_008` names.
Outside item 13's bound; nothing below was touched:

```
assessor-coupling/conditions.py::pool_fraction
     IndentationError, conditions.py line 504 — an unclosed `sys.stderr.write(`
     spliced between two copies of main()'s tail. Compiles in BOTH parents of
     merge b57c625 and not in the merge: a decision taken inside the merge
     commit, tools/merge_silent_loss.py's subject.
crediting-rate/crediting_rate_v2.py::position
     SyntaxError, `{` never closed at line 625. Compiles in BOTH parents of merge
     e167a67 and not in the merge — same shape as the row above.
chain-position/load_class.py::stability_product
     SyntaxError, `from __future__` after a third stacked module docstring
     (line 156). Broken on the second parent of b57c625 (1a9c09b side) and
     carried through the merge, not introduced by it.
cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes
cooperative-substrate-proof/p5_lag.py::lag_ratio
     ModuleNotFoundError: `scope` — both modules `import scope`, a sibling, and
     the registry loads them by file path with the folder not on sys.path.
     A property of the helper's loader, not of the modules.
instrument-index/build_index.py::claim_only_fraction
     KeyError 'path' / KeyError 3 — the registry's cases hand the function a list
     of shape strings and the function reads row dicts; helper and callee
     disagree on the argument shape.
```

The three syntax rows are the load-bearing ones: three modules on `main` do not
compile, two of them since a merge commit that neither side asked for, and no
suite in `tests/` or in CI reads them, so the registry running them is the only
instrument that noticed. Each is a separate repair on its own folder and none is
authorized by PART B; recorded so the next `--selftest` sweep does not read
`COMPLETE` as `ran`.

## 15. TICKET — 2026-10-04, the eight main-branch failures

Numbered 15 because sections 13 and 14 exist on the unmerged branch
`claude/potential-part-b-k7Qm`, and reusing them would collide when it merges.
This branch is `claude/fix-known-answer-run-manifest`, cut from `c03efc4`.

### 15.1 Break commits (T1)

Every first-parent commit from `1a6a129` to `c03efc4` was checked out and the
8 node ids were run (108 commits; a linear scan, not a bisect, because a test
can break, be repaired and break again). The break below is the commit after
the last PASS, from which every later commit is FAIL.

    test                                                         break    first-parent commit
    TestRedirectContract::test_no_redirect_names_a_target_...    026d2fd  PR #89 (instrument-index)
    TestRedirectContract::test_the_one_known_violation_...       026d2fd  PR #89
    TestArgparseSelftestForm::test_argparse_declared_...         2fa8648  PR #83, red on arrival
    TestArgparseSelftestForm::test_those_modules_really_...      2fa8648  PR #83, red on arrival
    ToolRuns::test_tool_exits_clean                              2fa8648  PR #83
    TheGateFires::test_the_registry_is_complete                  2fa8648  PR #83
    ManifestIsCovered::test_every_manifest_entry_is_registered   d1d3c80  PR #85
    SeedReachability::test_every_registration_is_reachable_...   3bfb65f  PR #95

The known-answer tests have been red continuously since 2fa8648, but the cause
has changed over that time:

    2fa8648   ledger/py_ledger/engine.py::quantize and ::recompute expected
              and not registered
    d1d3c80   seed() raises NameError on _drc_count_relation
    3bfb65f   onward: register() calls stranded after the `return` of
              _tra_sle_to_sv (KNOWN_RED section 11)

The cause at c03efc4 is the third one.

### 15.2 Classification (T2)

    GATE_BROKEN    the four known-answer tests. tools/known_answer.py is the
                   gate. Five register() calls sat in dead code, so five
                   metrics were expected and never registered, and the gate
                   reported it correctly.
    FIXTURE_DRIFT  the two argparse tests. They pin substrate-alternative/
                   pilot_loop.py and frame_audit.py as written by fa9a00e.
                   Merge dbf4cb0 resolved both paths to the 948033a build,
                   which refuses --selftest. The classifier is correct.
    FIXTURE_DRIFT  the two redirect tests. Their fixture is the live tree, and
                   the tree gained two redirects naming files that have never
                   been committed:
                       instrument-index/coverage.py -> test_index.py
                         (landed 1d71e9f, the losing build of merge b57c625)
                       sense_as_match.py -> test_sense.py
                         (delivered e884901)
                   The gate fired correctly on real defects. None of the four
                   offered classes says that directly; FIXTURE_DRIFT is the
                   nearest.

No failure is ENV and none is TEST_WRONG.

### 15.3 What this branch changes (T4)

    3f177fd   cherry-pick -x of 1803391 from claude/potential-part-b-k7Qm,
              unchanged. It moves the five register() calls into
              _seed_work_order_metrics(), which seed() calls. The check is
              unchanged. The four known-answer tests close.
    (repin)   tests/test_run_manifest.py TestArgparseSelftestForm.
              OLD instances: pilot_loop.py, frame_audit.py.
              NEW instances: search-substitution/search_substitution.py,
              qrng-pair-search/qrng_pair_search.py.
              The check is unchanged (an argparse-declared, attribute-tested
              --selftest classifies SELFTEST, on real files that carry the
              form). One assertion is added: a pin must not also carry the
              `"--selftest" in` literal, because such a pin would pass under
              the old classifier and would not discriminate.
              Verified by hand: a00aa9e^:tools/run_manifest.py files both new
              pins CLI, and the current one files both SELFTEST. The old
              pilot_loop pin reads REDIRECT under both classifiers, so it no
              longer discriminated either.
    NOT CHANGED  the two redirect tests stay red. Repairing them requires
              authoring a missing test file or editing a delivered file.
              Pinning the two paths as known violations would weaken an
              assertion whose own message says "if it is a new violation,
              that is the finding". These are findings, left to the owner:
                - sense_as_match.py: deliver test_sense.py, or say what the
                  redirect should name
                - instrument-index/coverage.py: RIN_024's archive decision
                  (4684e40, unmerged) moves the file but keeps the pointer,
                  so it does not close this either

### 15.4 What green does not mean after this branch

After the cherry-pick the known-answer gate exits 0 with 50 of 50 registered
and 0 unreachable. Six metrics are registered and never exercised: 33 cases
come back NOT_RUN, and the gate does not fail on NOT_RUN.

    assessor-coupling/conditions.py::pool_fraction
    chain-position/load_class.py::stability_product       load_class.py does not compile
    cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes
    cooperative-substrate-proof/p5_lag.py::lag_ratio
    crediting-rate/crediting_rate_v2.py::position         crediting_rate_v2.py does not compile
    instrument-index/build_index.py::claim_only_fraction

These are the merge splices that section 12 lists, and that section 13 on
claude/potential-part-b-k7Qm restores file by file. They are not ported here.
Each restore picks which build wins, and that decision is outside this ticket.

### 15.5 Builds merged while a gate was red (T3), flag only, no re-score

KEY_HOLDER_UNGUARDED (known-answer gate, red since 2fa8648). 23 metrics were
added to EXPECTED_METRICS while the gate was red, at the first-parent commit
shown. Any new defect in them was masked by the existing red.

    PR #83 2fa8648   ledger/py_ledger/engine.py::quantize, ::recompute
    PR #85 d1d3c80   additivity-inheritance::interaction_ss,
                     credential-channel::routing_cost,
                     criterion-externality::expected_rate,
                     deep-research-correction::count_relation,
                     reporting-chain-loss::composed_bias,
                     chain-position::stability_product *,
                     measurand-partition::stiffness_ratio
    PR #88 7705cef   terminal-crossing::expected_crossings
    PR #91 429f773   unowned-join::join_coverage,
                     assessor-coupling::pool_fraction *,
                     instrument-index::claim_only_fraction *
    PR #95 3bfb65f   automation-gap::p_uninterrupted,
                     thwaites-risk-audit::sle_to_sv
    PR #94 724937f   crediting-rate::position *,
                     cooperative-substrate-proof::gain_from_sizes *, ::lag_ratio *
    PR #96 0c6f40e   route-independence::independence_ratio, ::lag_years,
                     ::net_positions
    PR #101 6470987  potential::vertex_connectivity, ::unprovenanced_attested

    * = cases still NOT_RUN after this branch (15.4)

KEY_HOLDER_UNGUARDED (run_manifest redirect contract, red since 026d2fd).
30 REDIRECT records were added at or after 026d2fd:

    route-independence 20, cooperative-substrate-proof 3,
    instrument-index 2, unowned-join 2, thwaites-risk-audit 1,
    undeclared-cuts 1, (root) 1

All of them resolve today except the two in 15.2.

### 15.6 Suite (tests/, pytest)

    c03efc4 (main)    8 failed, 125 passed   (133 tests)
    this branch       2 failed, 132 passed   (134 tests: one added in the
                                              repin; the 2 are the redirect
                                              tests, 15.3)
