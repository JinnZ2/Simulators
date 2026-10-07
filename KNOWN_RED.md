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


## 17. FIFTH PASS — 2026-10-06, the sense_as_match.py redirect (branch claude/sense-as-match)

Renumbered 2026-10-07. This section and the next were §12 and §13 on this
branch. `main` already holds a §12 (cherry-picked from PR #105), §15 and §16,
and reserves §13/§14 for `claude/potential-part-b-k7Qm`. Merging this branch
as numbered would put two different §12s and two §13s in one file. 17 and 18
are free on every branch. Content is unchanged except where §18 says so.

`sense_as_match.py` (root) refuses `--selftest` and says "run test_sense.py";
no `test_sense.py` sat beside it. A root `test_sense.py` now does. It runs the
module's own `run_checks()` and exits with its code. Nothing in
`sense_as_match.py` is edited.

```
test_run_manifest.TestRedirectContract.test_no_redirect_names_a_target_that_is_missing
     before: ['instrument-index/coverage.py', 'sense_as_match.py']
     after:  ['instrument-index/coverage.py']
test_run_manifest.TestRedirectContract.test_the_one_known_violation_is_pinned
     before: anchor-position/normalize.py, instrument-index/coverage.py, sense_as_match.py
     after:  anchor-position/normalize.py, instrument-index/coverage.py
```

Both tests stay red, on `instrument-index/coverage.py`, which this pass does not
touch. The 8 failing ids are unchanged: 133 run, 8 FAIL, before and after.

What the repair is NOT: the redirect is now TRUE, and the target is SELF-GRADED.
The checks were written by the same hand as the module, so the run is a regression
result, not validation (the MSV_023 status). It runs 16 of 18 and exits 1:

```
FAIL positive control fires on a term not at the match site
FAIL score returns UNRATED on a failed gate
```

One cause. `gate()` checks only that the TERM appears whole-word in the source text.
The control's text contains the term and not the basis, so `gate()` returns
`(True, "OK")` where the control expects `NOT_AT_MATCH_SITE`. Either the control is
mis-specified or the gate is missing a basis clause. That is the author's call, and
it is left open. The module's own first comment reads "A gate that never fires is
not a gate", and on its own positive control this one does not fire.

## 18. SIXTH PASS — 2026-10-07, gate() gains the basis clause (branch claude/sense-as-match)

The author's call on §17 is in: the positive control is correct, and `gate()` is missing a basis check. The work was done in order.

1. **Case written first.** Before `gate()` was touched, one case was added to the root `test_sense.py`, outside the module's `run_checks()`:
   - the term is present;
   - the basis is present;
   - the basis sits in a different paragraph;
   - the expected result is `NOT_AT_MATCH_SITE`.
2. **Unpatched run recorded.** The case was then run against the unpatched gate.
3. **Gate patched.** `gate()` then gained [CHOICE 6]: the basis must occur, whole-word, inside at least one match site. A match site is the blank-line-delimited paragraph that holds a whole-word occurrence of the term.

| control | before | after |
|---|---|---|
| positive control fires on a term not at the match site | FAIL | PASS |
| score returns UNRATED on a failed gate | FAIL | PASS |
| other 16 module checks (incl. "a located record passes", declared corpus_default) | PASS | PASS |
| [added] fixture: term present in text | PASS | PASS |
| [added] fixture: basis present in text | PASS | PASS |
| [added] basis present but not at match site -> NOT_AT_MATCH_SITE | FAIL | PASS |
| totals | 16/18 + 2/3, exit 1 | 18/18 + 3/3, exit 0 |

**The patch does not refuse everything.** The two passing cases still pass. These are the located record and the declared corpus_default. A term used in two paragraphs passes when either paragraph holds the basis. This was spot-checked here and is now pinned (§18.1).

**Stated cost of [CHOICE 6].** A paragraph is a layout unit, not a semantic one. A sense stated across a paragraph break therefore reads `NOT_AT_MATCH_SITE`.

**Root suite unchanged:** 133 run, 8 FAIL. The failing ids are identical to §17's.

**The self-graded flag stays.** The added case is by the same hand as the gate it tests. A pass here is a regression result, not validation (the MSV_023 status). The flag lifts when a case authored outside this module passes against `gate()` as it stands.

### 18.1 Pinned since — the hand-checked cases, and the limit

Three cases were hand-checked only and are now pinned in `test_sense.py`:

| case | gate() | pinned as |
|---|---|---|
| term in two paragraphs, basis in the second | `(True, "OK")` | correct |
| term in two paragraphs, basis in the first | `(True, "OK")` | correct |
| basis present, term absent | `(False, "NOT_AT_MATCH_SITE")` | correct |

**LIMIT, pinned as current behaviour: a false NOT_AT_MATCH_SITE.** A sense stated across a paragraph break reads `NOT_AT_MATCH_SITE`, and the reading is correct. The pinned text:

    His disrespect was not ethical.

    It was taking for granted, and thereby missing information.

This is the cost of [CHOICE 6]. A paragraph is a layout unit, and the author's sense is not bounded by layout.

The text has the same shape as the §18 added case: term in paragraph 1, basis in paragraph 2. In one, the basis is the author's statement of the sense; in the other, it is an unrelated sentence. `gate()` reads layout and not intent, so it cannot separate them. Any repair has to do one of three things:

- read something other than paragraph boundaries; or
- admit both cases; or
- refuse both cases, as it does now.

**A repair turns this pin red.** This section must then be corrected, not the pin quietly flipped.

### 18.2 Outside cases — the only flag-lifter

`test_sense.py` loads `sense_outside_cases.json` when that file sits beside it. The cases are authored outside this module (the chat side), and this branch authors none.

**Admissible file** [CHOICE T1], [CHOICE T2]:

- a declared `author`;
- a declared `provenance`;
- `authored_outside_module: true`;
- 3 to 5 cases, each with:
  - a record;
  - a text;
  - an expected `(ok, reason)`;
  - a `why`;
- at least one expected refusal (`ok: false`);
- at least one expected pass.

The expected-pass requirement is added here. It is not in the request. A set of refusals alone passes a gate that refuses everything, which is the constant-output failure `tools/known_answer.py` refuses for the same reason.

**What is not verified.** The author fields are declared. Nothing here can check who wrote a case.

**States:**

| state | when |
|---|---|
| `SELF-GRADED` | no file |
| `NOT_ADMISSIBLE` | the file fails a rule above |
| `OUTSIDE_DISAGREES` | the file is admissible, and some case disagrees with `gate()` |
| `OUTSIDE_AGREES` | the file is admissible, and every case agrees |

- **Only `OUTSIDE_AGREES` lifts the self-graded flag.** A disagreement exits nonzero. It is reported as a finding, and the case is never edited to match.
- **The file's sha256 is printed with the result.** Editing a case after the run therefore shows in the next run's output.
- **All four states are reachable.** Six intake checks show this on constructed files in a temp dir. Those files lift nothing.
- **A real file moves the exit code.** A planted file carrying the §18.1 limit case with `expect OK` read `OUTSIDE_DISAGREES` and exited 1. It was removed, not committed.

**State as committed:**

- 18/18 module checks;
- 13/13 added checks (7 cases, 6 intake);
- 0 outside cases;
- `STATE: SELF-GRADED`;
- exit 0.
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

## 13. SIXTH PASS — 2026-09-30, merge-scar repairs and the compile gate

Order: compile gate first, then repairs one commit per module, then the merge
instrument, then list the loader/argument mismatches. Branch
`claude/potential-part-b-k7Qm`.

### 13.1 The gate, and its first run

`tests/test_compile_gate.py` — `compile()` over every `.py` in the tree
(`ast.parse` does not enforce the `from __future__` placement rule, `compile()`
does), every failure by path, line and message, one declared exemption
(`relational/cartesian_vs_relational_demo.py`, PEP 701, compiled on 3.12+ and
SKIPPED with its reason otherwise). Committed alone at `928b4e4`, before any
repair, so the red run is on the record:

```
compiled 1129 files, 8 red, 1 skipped
RED  assessor-coupling/conditions.py:504            unexpected indent
RED  assessor-coupling/precedent.py:486             unexpected indent
RED  chain-position/load_class.py:156               from __future__ after a stacked docstring
RED  chain-position/trust_provenance.py:236         from __future__ after a stacked docstring
RED  cooperative-substrate-proof/p2_substrate.py:479 unexpected indent
RED  cooperative-substrate-proof/scope.py:182       '[' was never closed
RED  crediting-rate/crediting_rate_v2.py:625        '{' was never closed
RED  stability-trigger-envelope/descent_record.py:766 unterminated triple-quoted string
```

Eight, not the three §12 recorded. §12 was right that the registry caught
those three "by accident of reach"; it reached three of eight.

### 13.2 What the eight are — a correction to §12

Every one of the eight first fails to compile in a MERGE commit whose two
parents both compile, and every one is a file two independent builds of one
folder ADDED under the same name. The merge kept both builds' distinct files
side by side (`test_assessor.py` beside `selftest.py`, `p1_records.py` beside
`p1_dependency_records.py`, and so on) and, for the files whose names collided,
interleaved the two whole files into one: every distinct line of both parents
present, nothing dropped, and nothing that parses. There is no "merged region"
to restore; the unit is the file, and the pick is between two builds.

```
b57c625  (209af6d d23741d)  assessor-coupling/conditions.py, precedent.py
                            instrument-index/build_index.py        (compiles; see 13.4)
1a9c09b  (0e77d9a d1d3c80)  chain-position/load_class.py, trust_provenance.py
e167a67  (e4f5418 4b1f21e)  crediting-rate/crediting_rate_v2.py
                            cooperative-substrate-proof/scope.py, p2_substrate.py,
                            p3_comprehension.py (compiles), run_all.py (compiles)
803ffd5  (038a30f 0c6f40e)  stability-trigger-envelope/descent_record.py
```

§12 read `chain-position/load_class.py` as "broken on the second parent of
b57c625 and carried through". True at b57c625; the break was introduced one
merge earlier, at 1a9c09b, where both parents compile. §12's reading of
`instrument-index/build_index.py::claim_only_fraction` as an argument-shape
mismatch was also wrong: the file is a splice with five functions defined
twice, the later definition winning, and the KeyError was the other build's
`parse_header` receiving this build's rows.

`803ffd5` is the one CONFLICT rather than both-added: one base (bc2b315),
two divergent edits, the merge kept `038a30f`'s rewrite whole and pasted a
54-line fragment of main's `fixtures()` tail (the X6 fixture, STE_011) without
the function head — the unterminated string.

### 13.3 The repairs, one commit per module, the pick stated in each

Each of the eleven commits (`ff36bb0` .. `240425a`) restores the file to ONE
parent's bytes (a diff against that parent for the path is empty), records the
other parent's blob id so it can be checked out in one command, states the
pick and the reason, and records that the other build's suite was red before
(the module did not compile) and is red after (`AttributeError` on the other
build's names). The rule applied uniformly, stated before any file was
touched: **the build whose functions `tools/known_answer.py` registers**
(the operator's own PART B item 13 ordered those registrations reached), and
where no registry name exists (`descent_record.py`), the build the tree's
own records point at (`samples/descent_record.sample.txt` byte-identical to
main's, STE_011's X6 only in main's module, the root `CLAUDE.md` count
"49/49" main's suite). Picks: assessor-coupling ^1 (6ee102a build),
crediting-rate ^1 (ad56177), cooperative-substrate-proof ^1 (f5339f9),
instrument-index ^1 (209af6d), chain-position ^2 (781fb5d, main),
stability-trigger-envelope ^2 (main). The scratch-worktree runs behind the
rule, both directions:

```
pick A (as committed)                      pick B (the other build)
assessor    test_assessor.py 98/0          selftest.py       72 checks 1 FAIL (its own)
crediting   crediting_rate_v2 --selftest 55/0   test_crediting_v2.py 124/0
coop        test_proof.py 194/0            selftest.py       FAIL (its own)
chain       test_chain.py 54/0             selftest.py       96/0
instr-index tests/test_build_index.py 125/0   (^2 has no suite)
ste         test_descent_record.py 49/0     test_envelope.py  217/0
```

Symmetric: each pick makes its own build's suite green and leaves the other
build's suite red, exactly as the folders were red before, only now for a
reason a traceback names. **Resolving each folder to one build — deleting
or renaming the losing build's files — is the RIN_024 decision and is not
taken here.** What this pass changes is that one build per folder now runs.

The cost recorded per folder: `stability-trigger-envelope/test_envelope.py`
(217 checks on the rewrite) is red under the pick, as `test_descent_record.py`
was red under the rewrite before the merge; `chain-position/selftest.py`
(CHP_ claims), `assessor-coupling/selftest.py`, `cooperative-substrate-proof/
selftest.py`, `crediting-rate/test_crediting_v2.py` are the losing builds'
suites and stay red. Nine spliced non-`.py` files are NOT repaired:
`CLAIM_TABLE.md` and `README.md` in all four folders, `chain-position/
WORK_ORDER.md` (the same delivered order twice, 166+166 -> 167 lines),
`crediting-rate/PREDICTION_V2.md`, `cooperative-substrate-proof/LICENSE`,
`instrument-index/INDEX-SPEC.md`, `cooperative-substrate-proof/samples/
run_all.sample.txt` (the one real loss row). The root `CLAUDE.md` carries two
entries for each of these folders, one per build, and is not edited.

### 13.4 The merge instrument (order item 3)

Run as delivered on `b57c625` and `e167a67`, `tools/merge_silent_loss.py`
reports 0 and 1 files with loss (the sample file). Lines lost: none. The
instrument's test is loss, and these merges lost nothing — they kept
everything twice. So the cases are not filed against a reading that cannot
hold them; the instrument gets the reading: `BOTH_KEPT` (file absent at base,
present in both parents, merge equals neither, every distinct line of both
parents in the merge), lost 0, counted apart from loss rows, with a fixture
and selftest check (12 checks). Over the tree it reads 20 files across the
three both-added merges, 11 of them `.py` — the eleventh,
`instrument-index/build_index.py`, compiled and was invisible to the gate;
this reading is what found it. Run appended to
`route-independence/samples/merge_loss.sample.txt`. The clone here is
shallow (41 merges reachable, 4 refused), so it is not a rerun of the sample's
full-history audit.

### 13.5 Order item 4 — the loader/argument mismatches, list only

Three were named. One dissolved (13.2: `build_index.py` was a splice, now
PASS). Two remain, both the registry loader's, not the modules':

```
cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes   NOT_RUN  ModuleNotFoundError: scope
cooperative-substrate-proof/p5_lag.py::lag_ratio                  NOT_RUN  ModuleNotFoundError: scope
```

Both `import scope`, a sibling; `tools/known_answer.py` loads a metric's
module by file path with the folder not on `sys.path`. Not repaired here.

### 13.6 State after this pass

`python3 -m unittest discover tests`: 136 run, 4 FAIL — the same four
`test_run_manifest` rows as §12, untouched. `tests/test_compile_gate.py`:
compiled 1129, 0 red, 1 skipped. `tools/known_answer.py`: registered 50 /
expected 50 COMPLETE, 48 exercised, the two `import scope` rows above the
only never-exercised ones, 0 disagreeing.

## 14. SEVENTH PASS — 2026-09-30, build separation and gate extensions

Order: archive the losing builds (RIN_024 decided: archive, don't delete),
hold the archived suites at a declared state, extend the compile gate with a
duplicate-definition check and the interpreter version, list the spliced
docs and the loader mismatches. Branch `claude/potential-part-b-k7Qm`, PR #105
(subscribed; CI and review comments on it are the only things authorized
there).

### 14.1 What did not hold

- **"each of the 11 folders"** — the eleven restored modules live in **six**
  folders. Six archives, six commits.
- **"EXPECTED_RED"** — three of five archived suites run **GREEN** from their
  archive (cooperative-substrate-proof `selftest.py` 82/0, chain-position
  `selftest.py` 96/0, stability-trigger-envelope `test_envelope.py` 217/0),
  because the losing build moved whole and its suite needs nothing the live
  folder kept. Two are RED for a reason the test names (assessor-coupling
  reads `WORK_ORDER.md` from its own directory, which stayed live;
  crediting-rate imports the shared `crediting_rate.py`, which stayed live);
  instrument-index's losing build shipped no suite. The test declares the
  observed state per suite and fails on a change in either direction; it does
  not declare RED where the tree runs GREEN.
- **The duplicate-definition check is RED on the tree it landed in**: five
  modules besides `build_index.py` trip it (14.4). Recorded; nothing repaired.

### 14.2 The archive (order item 1)

`archive/<folder>/` holds the build the restore commits did not pick, whole:
files that were only ever that build's moved with `git mv`, files both builds
had under one name written from the losing parent's blob byte-for-byte, files
identical in both parents left in place. No file content edited. Each carries
`PROVENANCE.md` (merge sha, both parents, blob per file, the pick rule, the
losing suite's last state). The live folder keeps one build; the spliced
`.md`/LICENSE files stay in it unedited (14.5).

```
247f4cc archive/assessor-coupling            b57c625^2   mv 7   wr 4   shared 1
a2882ca archive/crediting-rate               e167a67^2   mv 32  wr 6   shared 15
9243bcd archive/cooperative-substrate-proof  e167a67^2   mv 7   wr 8   shared 0
4684e40 archive/instrument-index             b57c625^2   mv 4   wr 2   shared 0
c656081 archive/chain-position               1a9c09b^1   mv 8   wr 5   shared 0
a7bef9b archive/stability-trigger-envelope   803ffd5^1   mv 6   wr 5   shared 2
```

Live suites after the move, unchanged: test_assessor 98/0, crediting_rate_v2
--selftest 55/0, test_proof 194/0, test_chain 54/0, test_descent_record 49/0,
instrument-index tests 125/0.

### 14.3 Archived suites, held by `tests/test_archive_expected_red.py`

```
archive/assessor-coupling/selftest.py               RED    FileNotFoundError: WORK_ORDER.md
archive/crediting-rate/test_crediting_v2.py         RED    No module named 'crediting_rate'
archive/cooperative-substrate-proof/selftest.py     GREEN  checks: 82   failed: 0
archive/instrument-index/                           NO_SUITE
archive/chain-position/selftest.py                  GREEN  checks: 96   failed: 0
archive/stability-trigger-envelope/test_envelope.py GREEN  217 checks, 0 failed
```

The eleven modules those builds carry: `conditions.py`, `precedent.py`
(assessor-coupling); `crediting_rate_v2.py`; `scope.py`, `p2_substrate.py`,
`p3_comprehension.py`, `run_all.py` (cooperative-substrate-proof);
`build_index.py`; `load_class.py`, `trust_provenance.py` (chain-position);
`descent_record.py` — each present in its archive at the losing parent's
blob, each present live at the winner's. A folder under `archive/` missing
from the test's table, or lacking `PROVENANCE.md`, also fails it.

### 14.4 Gate extensions (order items 3, 4)

`tests/test_compile_gate.py` now also fails on a top-level `def`/`class`
name bound twice in one module (direct module-body children only; a
try/except redefinition is not read), listed by path, name and lines, with a
planted-duplicate fixture and a clean control; the interpreter version prints
on every run and the PEP 701 skip names it. First run, python 3.11.15:
**compiled 1140, 0 red, 1 skipped, 8 duplicate names in 5 modules** — five
modules besides `build_index.py` trip it:

```
earth_economics/asteroid_mining_audit.py             main 157/476, run_asteroid_fermi 124/437
grounding-layers/cultural_lens.py                    CulturalLens 14/149
grounding-layers/run_grounding_pipeline.py           run_pipeline 57/261
play-sims/atmospheric-heating/meteor_heating_bins.py density 30/281
tools/known_answer.py                                _rcl_composed_bias 911/1813,
                                                     _cpd_stability_product 925/1827,
                                                     _drc_count_relation 939/1796
```

The four delivered-drop hits all enter at merge `04d16d0` (PR #71), bodies
differing — the same class of merge artifact as §13, four merges earlier,
in files that parse. The three in `tools/known_answer.py` are dead earlier
copies of helpers redefined by the registry restorations of 2026-09-23/27
(`d0325d7`, `881c636`); code identical ignoring docstrings, and the later
copy is the one `seed()` reaches, so no registered value moves. **Not
repaired in this pass** (the order asked whether anything else trips it, not
for the trips to be closed); `test_no_module_binds_a_toplevel_name_twice`
stays RED until they are.

### 14.5 The spliced docs (order item 5) — list only, no edits

Every one differs between its two sides; the live copy is the splice.

```
file                                                winner side (build)        loser side (build)         live splice
assessor-coupling/CLAIM_TABLE.md                    b57c625^1 6ee102a 137 ln   b57c625^2 0e77d9a 29 ln    164 ln
assessor-coupling/README.md                         b57c625^1 6ee102a 105      b57c625^2 0e77d9a 159      262
instrument-index/INDEX-SPEC.md                      b57c625^1 209af6d 253      b57c625^2 1d71e9f 166      419
crediting-rate/CLAIM_TABLE.md                       e167a67^1 311              e167a67^2 289              507
crediting-rate/PREDICTION_V2.md                     e167a67^1 ad56177 38       e167a67^2 f168f79 26       64
crediting-rate/README.md                            e167a67^1 236              e167a67^2 179              342
cooperative-substrate-proof/CLAIM_TABLE.md          e167a67^1 f5339f9 366      e167a67^2 8264356 26       392
cooperative-substrate-proof/LICENSE                 e167a67^1 f5339f9 9        e167a67^2 8264356 121      130
cooperative-substrate-proof/README.md               e167a67^1 f5339f9 130      e167a67^2 8264356 142      270
cooperative-substrate-proof/samples/run_all.sample.txt  e167a67^1 f5339f9 20   e167a67^2 8264356 89       104 (the one loss row)
chain-position/CLAIM_TABLE.md                       1a9c09b^2 781fb5d 40       1a9c09b^1 84935a2 28       68
chain-position/README.md                            1a9c09b^2 781fb5d 83       1a9c09b^1 84935a2 179      260
chain-position/WORK_ORDER.md                        1a9c09b^2 781fb5d 166      1a9c09b^1 84935a2 166      167 (same order delivered twice)
stability-trigger-envelope/CLAIM_TABLE.md           803ffd5^2 bc2b315 172      803ffd5^1 bc2b315 60       111
stability-trigger-envelope/README.md                803ffd5^2 bc2b315 352      803ffd5^1 bc2b315 204      216
```

Fifteen, not nine: §13.3 counted the nine in the four §13 folders and missed
instrument-index's `INDEX-SPEC.md` and the crediting-rate/chain-position
docs it listed by name only. The loser side's version of each is now in
`archive/<folder>/` byte-for-byte; the live splice is the separate decision.

### 14.6 Loader mismatches (order item 6) — unchanged

```
cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes   NOT_RUN  ModuleNotFoundError: scope
cooperative-substrate-proof/p5_lag.py::lag_ratio                  NOT_RUN  ModuleNotFoundError: scope
```

### 14.7 State after this pass

`tests/test_compile_gate.py`: compiled 1140 / 0 red / 1 skipped / 8
duplicate names (RED on that check). `tests/test_archive_expected_red.py`:
2 RED as declared, 3 GREEN as declared, 1 NO_SUITE, passing.
`python3 -m unittest discover tests`: 139 run, 5 FAIL — the four
`test_run_manifest` rows of §12 plus the duplicate-name check.
`tools/known_answer.py`: 50/50 COMPLETE, 0 disagreeing.

### 14.8 Correction to 14.4 and to commit 7f5ac2a's message, same pass

Both say the three duplicate helpers in `tools/known_answer.py` are "code
identical ignoring docstrings". They are not — diffed with the docstrings
stripped, after the sentence was already pushed:

```
_rcl_composed_bias      dead@911  loads under module name "_rcl";      live@1813 "_rcl_hop"
_cpd_stability_product  dead@925  loads under "_cpd";                  live@1827 "_cpd_load"
_drc_count_relation     dead@939  no sys.path insert;                  live@1796 inserts
                        measurand-partition/ on sys.path around the load, in try/finally
```

The third difference is load-bearing: `deep-research-correction/check.py`
imports `common` from `measurand-partition/`, so the dead copy would raise
ModuleNotFoundError where the live copy runs. The conclusion in 14.4 stands
for the wrong reason: no registered value moves because the LIVE copy is
the later one and the correct one, not because the copies are the same.
The dead copies are still not removed here. The wrong sentence was a check
written as a claim — the identity was asserted from a diff that showed only
docstring lines because the diff was truncated to six lines — and the
test that caught it was re-running the comparison on the whole body.
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

## 16. 2026-10-05 — the known-answer gate fails on skipped cases; parked items

### 16.1 The change

`tools/known_answer.py` exits nonzero when any case is NOT_RUN. Its summary
ends in a block that cannot be missed:

    SKIPPED (NOT_RUN): 33 cases in 6 metrics   -- GATE RED: a skipped case is not a passing case

[PINNED 2026-10-07] "33 cases in 6 metrics" is the figure @85ce0d9, the commit
that wrote this section. It is 28 cases in 5 metrics @5af0d47 and unchanged
@9262516. Merge 5af0d47 (parents c95a1e5, 85ce0d9) brought in c95a1e5's
crediting split, and crediting_rate_v2.py::position (5 cases) began to run.
The prose here is left as written. Current figures live in the PIN block of
section 19, which tools/known_red_check.py reads.

Each metric is listed with its skip count and the first error.

Old check: exit 0 unless a case disagreed with the registry, a metric was
missing, a registration was unreachable, or a registration sat outside seed().
NOT_RUN counted toward none of these.

New check: all of the above, plus any NOT_RUN case. This tightens the gate and
weakens nothing. Section 15.4 said the gate's green carried 6 never-exercised
metrics. That green is gone.

    tools/known_answer.py   skipped(), exit_code(), the SKIPPED block
    tests/test_known_answer_gate.py
        test_a_skipped_case_turns_the_gate_red             planted raising callable -> listed, exit 1
        test_the_skipped_count_is_printed_in_the_summary   the line is present; nonzero exit whenever the count > 0

Consequence: `ToolRuns::test_tool_exits_clean` is RED again. It is red for the
33 skipped cases below and for nothing else (@85ce0d9; 28 @5af0d47 and
@9262516). Suite (tests/, 136 tests):

    3 failed, 133 passed   @85ce0d9, @5af0d47, @9262516 (same three each time)
      test_known_answer_gate::ToolRuns::test_tool_exits_clean   (16.2: the 33 skips @85ce0d9; 28 @9262516)
      test_run_manifest::TestRedirectContract x2                (16.2: the two redirects)

### 16.2 OPEN — awaiting Kavik (parked; nothing below was changed)

    1  sense_as_match.py -> test_sense.py
       The redirect names a file that has never been committed. Deliver
       test_sense.py, or say what the redirect should name. The redirect
       tests stay RED. Not pinned as a known violation.

    2  instrument-index/coverage.py -> test_index.py
       The fate of the file: losing build of merge b57c625, landed 1d71e9f.
       The pointer names a file that has never been committed.
       Archiving the file (4684e40 on claude/potential-part-b-k7Qm) keeps
       the pointer and does not close this. The redirect tests stay RED.

    3  chain-position/load_class.py and crediting-rate/crediting_rate_v2.py
       Neither compiles; each is a merge splice of two builds. No winning
       build picked.
         load_class.py          SyntaxError: from __future__ imports must
                                occur at the beginning of the file
                                -> stability_product, 5 cases skipped
         crediting_rate_v2.py   SyntaxError: '{' was never closed (line 625)
                                -> position, 5 cases skipped
       [PINNED 2026-10-07] Stale for crediting_rate_v2.py: true @85ce0d9,
       false @5af0d47. The live crediting-rate/crediting_rate_v2.py compiles
       and its --selftest reads 55 checks, 0 failed @9262516. The spliced
       build is archived at crediting-rate/archive/f168f79/. load_class.py
       still does not compile @9262516.

### 16.3 OPEN, not in the parked three, and with the same shape

The remaining four skipped metrics also go through files that section 13 (on
claude/potential-part-b-k7Qm) lists as spliced builds. Repairing any of them is
a build pick, so they are parked with the three above rather than fixed under
"safe parts only".

    assessor-coupling/conditions.py::pool_fraction         IndentationError line 504   6 skipped
    cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes
                                                           ModuleNotFoundError 'scope' 5 skipped
    cooperative-substrate-proof/p5_lag.py::lag_ratio       ModuleNotFoundError 'scope' 6 skipped
    instrument-index/build_index.py::claim_only_fraction   KeyError: 'path'            6 skipped

The gate stays RED until all six skipped metrics run. [PINNED 2026-10-07]
Five @5af0d47 and @9262516: pool_fraction 6, stability_product 5,
gain_from_sizes 5, lag_ratio 6, claim_only_fraction 6 = 28. The "remaining
four" above total 23 @85ce0d9, and 23 + 5 (stability_product) + 5 (position)
= 33.

## 19. 2026-10-07 — baseline by id + cause @ commit; figures pinned and checked

### 19.1 Why

Section 16 said "33 cases in 6 metrics". That was true @85ce0d9 and false
from 5af0d47 on (28 in 5; section 16 now carries the pins inline). Nothing
noticed, because a prose figure is read by nobody. From here on the current
figures sit in the PIN block below and `tools/known_red_check.py` reruns the
instruments they came from. Any mismatch in either direction exits 1, and
`tests/test_known_red_pins.py` puts that check in the suite.

The baseline is adopted as a set of ids, each with a cause and a commit.
A bare count is not adopted: "3 failing" would stay green while one red
test was swapped for a different one.

### 19.2 Baseline @9262516 (136 tests, 3 failed, 133 passed)

    id                                            cause @ commit                                   intended
    test_tool_exits_clean                         85ce0d9: known_answer exits nonzero on NOT_RUN   YES
                                                  (28 cases, 5 metrics @9262516)
    test_no_redirect_names_a_target_that_is_missing
                                                  3 redirects name missing targets (below)         NO
    test_the_one_known_violation_is_pinned        4 violations where 1 is pinned (below)           NO

test_tool_exits_clean is INTENDED red. A clean exit with unrun cases would be
a false pass. It clears when the 28 NOT_RUN cases run. It does not clear by
loosening the gate, and any change that turns it green without the skip count
reaching 0 is a regression of 85ce0d9.

The two redirect tests are red for three files, not one:

    crediting-rate/archive/f168f79/crediting_rate_v2.py -> crediting-rate/test_crediting_v2.py
        The target exists only at commit f168f79.
    instrument-index/coverage.py -> test_index.py
        Section 16.2 item 2. Parked, awaiting Kavik. Never committed.
    sense_as_match.py -> test_sense.py
        Section 16.2 item 1. Clears when claude/sense-as-match merges; that
        branch adds root test_sense.py.

Merging sense-as-match leaves both tests red (2 missing, 3 violations, where
anchor-position/normalize.py is the 1 pinned). It also makes the rm.* pins
below MISMATCH. That is intended: the merge must re-pin them.

### 19.3 The crediting redirect is in the archive, not the live module

    crediting-rate/crediting_rate_v2.py      SELFTEST, 55 checks, 0 failed @9262516
    crediting-rate/archive/f168f79/...       REDIRECT to crediting-rate/test_crediting_v2.py
                                             (resolved from ROOT; present only @f168f79)

The live module is not a redirect. A test that runs its 55 checks is real
coverage of live code, and root `test_crediting_rate_v2.py` does exactly
that. It does NOT clear the violation, because the violation is the
archived copy's. The wrapper is deliberately not named
crediting-rate/test_crediting_v2.py: that would resolve the archived
redirect to a live test, and an archived contract would read as satisfied
by a file it never named.

Two ways to close the archived redirect. Both change the redirect contract,
so neither is taken here:

    (a) run_manifest resolves a redirect under archive/<sha>/ against that
        commit (git cat-file -e <sha>:<target>). The target is checked to
        exist where the archive says it does. It fails on a shallow clone,
        which is reported, not passed.
    (b) Files under */archive/<sha>/ are excluded from the redirect
        contract. ARCHIVED.md already says "run at its own commit".

### 19.4 PIN block

<!-- known-red-pins: begin -->
PIN ka.skipped.cases - 11 @59a5e5d
PIN ka.skipped.metrics - 2 @59a5e5d
PIN ka.skipped.metric cooperative-substrate-proof/p3_comprehension.py::gain_from_sizes 5 @59a5e5d
PIN ka.skipped.metric cooperative-substrate-proof/p5_lag.py::lag_ratio 6 @59a5e5d
PIN rm.redirect_missing archive/instrument-index/build_index.py - @59a5e5d
PIN rm.redirect_missing archive/instrument-index/coverage.py - @59a5e5d
PIN rm.redirect_missing crediting-rate/archive/f168f79/crediting_rate_v2.py - @9262516
PIN rm.redirect_missing instrument-index/coverage.py - @9262516
PIN rm.redirect_missing sense_as_match.py - @9262516
PIN rm.violation anchor-position/normalize.py - @9262516
PIN rm.violation archive/instrument-index/build_index.py - @59a5e5d
PIN rm.violation archive/instrument-index/coverage.py - @59a5e5d
PIN rm.violation crediting-rate/archive/f168f79/crediting_rate_v2.py - @9262516
PIN rm.violation instrument-index/coverage.py - @9262516
PIN rm.violation sense_as_match.py - @9262516
PIN suite.failing test_tool_exits_clean INTENDED @9262516
PIN suite.failing test_no_redirect_names_a_target_that_is_missing UNINTENDED @9262516
PIN suite.failing test_the_one_known_violation_is_pinned UNINTENDED @9262516
PIN suite.failing test_no_module_binds_a_toplevel_name_twice UNINTENDED @59a5e5d
PIN rm.archived_target_missing archive/instrument-index/build_index.py - @d19c52c
PIN rm.archived_target_missing archive/instrument-index/coverage.py - @d19c52c
PIN rm.archived_target_missing crediting-rate/archive/f168f79/crediting_rate_v2.py - @d19c52c
PIN cg.duplicate earth_economics/asteroid_mining_audit.py::main - @59a5e5d
PIN cg.duplicate earth_economics/asteroid_mining_audit.py::run_asteroid_fermi - @59a5e5d
PIN cg.duplicate grounding-layers/cultural_lens.py::CulturalLens - @59a5e5d
PIN cg.duplicate grounding-layers/run_grounding_pipeline.py::run_pipeline - @59a5e5d
PIN cg.duplicate play-sims/atmospheric-heating/meteor_heating_bins.py::density - @59a5e5d
PIN cg.duplicate tools/known_answer.py::_cpd_stability_product - @59a5e5d
PIN cg.duplicate tools/known_answer.py::_drc_count_relation - @59a5e5d
PIN cg.duplicate tools/known_answer.py::_rcl_composed_bias - @59a5e5d
<!-- known-red-pins: end -->

To re-pin: change the figure and its commit together, in the same commit
as the change that moved it, and record the move as a new section here.

### 19.5 Re-pin @59a5e5d — PR #105 merged

The pins above were written @9262516. PR #105 (claude/potential-part-b-k7Qm,
merge d675fc7) then landed on main, now @59a5e5d. Merging main into this
branch made the checker exit 1 on 13 pins. That was the check working:
the tree moved. Each pin now carries the commit where its figure was last
verified. A pin whose figure did not move keeps @9262516.

    figure                           @9262516    @59a5e5d   moved by
    known-answer skipped cases       28          11         #105 builds pool_fraction, stability_product,
    known-answer skipped metrics     5           2            claim_only_fraction (spliced builds separated)
    redirects naming a missing file  3           6          #105 archives three spliced builds to
    contract violations              4           7            archive/<folder>/; each archived copy keeps
                                                            its redirect
    suite                            136 / 3 red 145 / 4 red (main alone; 148 / 4 with this branch)

Still skipped: gain_from_sizes 5 and lag_ratio 6, both ModuleNotFoundError
'scope' (cooperative-substrate-proof). test_tool_exits_clean stays INTENDED
red until those 11 run.

The fourth failure, test_no_module_binds_a_toplevel_name_twice, is section
14.4's: eight duplicate top-level names. Five are in delivered drops, from
merge 04d16d0 (PR #71). Three are dead earlier helper copies in
tools/known_answer.py. Section 14 recorded it "Not repaired in this pass"
and it reached main with #105. It is UNINTENDED, known and parked, not by
design.

The three new redirects. Same shape as 19.3; none is the live code's:

    archive/crediting-rate/crediting_rate_v2.py  -> crediting-rate/test_crediting_v2.py
    archive/instrument-index/build_index.py      -> test_index.py
    archive/instrument-index/coverage.py         -> test_index.py

For the archive/crediting-rate/ copy, the target file does exist beside it:
archive/crediting-rate/test_crediting_v2.py. The redirect names its
pre-archive path, which run_manifest resolves from ROOT because it holds a
"/". Moving the folder broke the pointer, not the file. That adds a third
option to 19.3's two. Not taken:

    (c) for a file under archive/<folder>/, resolve a ROOT-relative target
        "<folder>/<rest>" as archive/<folder>/<rest>. The redirect is then
        checked against the copy that was archived with it.

Under (c), one of the three new violations would resolve. Under (b), all
four archived redirects would leave the contract. Either way, the two live
redirects (instrument-index/coverage.py, sense_as_match.py) remain.

### 19.6 Archived redirects: rule (c) adopted, (b) rejected (d19c52c)

Operator decision, 2026-10-07:

    (c) ADOPTED. A file under archive/<folder>/ that names a ROOT-relative
        target "<folder>/<rest>" resolves it as archive/<folder>/<rest>. The
        copy archived with the file is checked, never the live file at the
        old path (selftest: a live copy at the old path does NOT satisfy it).
    (b) REJECTED. A blanket exclusion of archive/ is an undeclared cut.
        Archives must still resolve; that is custody.

Effect @d19c52c:

    archive/crediting-rate/crediting_rate_v2.py   cleared: archive/crediting-rate/test_crediting_v2.py exists
    missing redirect targets                      6 -> 5
    contract violations                           7 -> 6

The three archived redirects whose targets are genuinely absent stay
violations. Each is tagged target_state ARCHIVED_TARGET_MISSING and pinned
by id (rm.archived_target_missing):

    archive/instrument-index/build_index.py               -> archive/instrument-index/test_index.py
    archive/instrument-index/coverage.py                  -> archive/instrument-index/test_index.py
        test_index.py was never committed (16.2 item 2)
    crediting-rate/archive/f168f79/crediting_rate_v2.py   -> crediting-rate/test_crediting_v2.py
        <folder>/archive/<sha>/ layout; rule (c) covers top-level archive/
        only. The target exists only at commit f168f79.

The live files stay red, as stated: instrument-index/coverage.py ->
test_index.py and sense_as_match.py -> test_sense.py (target_state
MISSING). test_no_redirect_names_a_target_that_is_missing and
test_the_one_known_violation_is_pinned stay UNINTENDED red for 5 missing
targets and 5 unpinned violations.

### 19.7 Duplicate top-level names (14.4): parked, pinned by name

test_no_module_binds_a_toplevel_name_twice stays UNINTENDED red. Each
duplicate is pinned as cg.duplicate <path>::<name>, read from the compile
gate's own sweep(). That is 8 pins, not 5: the 3 dead helper copies in
tools/known_answer.py are still there.

    delivered drops (merge 04d16d0, PR #71) -- the 5 that remain parked
      earth_economics/asteroid_mining_audit.py              main                 157, 476
      earth_economics/asteroid_mining_audit.py              run_asteroid_fermi   124, 437
      grounding-layers/cultural_lens.py                     CulturalLens          14, 149
      grounding-layers/run_grounding_pipeline.py            run_pipeline          57, 261
      play-sims/atmospheric-heating/meteor_heating_bins.py  density               30, 281
    tools/known_answer.py -- dead earlier copies; the later copy is the one seed() reaches
      _cpd_stability_product, _drc_count_relation, _rcl_composed_bias

SUGGESTED, the author's call, not done: remove the three dead helper copies
in tools/known_answer.py. 14.4 says no registered value moves, since seed()
reaches the later copy. Doing so turns their three cg.duplicate pins
MISMATCH, and the re-pin leaves exactly the 5 delivered-drop names.

