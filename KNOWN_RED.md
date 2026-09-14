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
