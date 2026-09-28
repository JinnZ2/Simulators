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
