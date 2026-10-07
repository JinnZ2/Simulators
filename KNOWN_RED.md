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

