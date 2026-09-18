# external-audit

Two documents about this repository, delivered from outside it and landed
verbatim, plus the two checkers that recompute what is recomputable in
them.

```
DEEP_RESEARCH_2026_09_14.md   the review: 166 folders surveyed, nine
                              families, applications and roadmap
RESPONSE_TO_REVIEW.md         the reply: what the review established,
                              what it did not measure, and one request

recount.py                    every countable claim, recomputed at a
                              pinned revision
run_instruments.py            the request in the reply's section 2:
                              run the instruments, report the failures
CLAIM_TABLE.md                EA_001..EA_014
```

Neither delivered document is edited here. Disagreements go in the
checker's output and in the claim table, which is the arrangement
`uninstrumented/cases/` and `AUDIT_NOTES.md` already use.

## What the recount found

The review's arithmetic is **internally consistent and externally wrong
by exactly two folders that do not exist**.

```
family tables name        166 folders
absent from the tree      frame-token-audit, gap-register
                          neither string occurs anywhere in the tree,
                          so invented rather than renamed
real content folders      164

seven of nine families reproduce EXACTLY at 6633778^
the two that do not are exactly the two carrying a phantom

  F1   claimed 326   actual 312   -14   phantom gap-register
  F2   claimed 924   actual 917    -7   phantom frame-token-audit

  family sum 2652  +  21 phantom  =  2673, the stated total
```

The closure to the digit is the result. A discrepancy says a count is
wrong; this locates the whole of it.

## The revision is established, not taken

The review states a survey date and no commit. `baseline()` derives the
revision instead: exactly one family moves between `6633778^` and
`6633778`, by exactly the size of the commit between them. Seven
families are exact at the parent, six at the child.

That matters twice over, because **the report is now inside the tree it
counts**. Landing it changes the folder count. Every number here is
pinned by revision, and a selftest check asserts the report is absent
from the revision it is measured against.

## The directory the survey never names

`.github` is the one top-level directory absent from every family table,
and it carries the refutation of two claims that rest on its absence.

```
section 12.2  "no test-running CI"          REFUTED
              .github/workflows/test.yml runs unittest discover across
              7 suites on push and pull request
roadmap #3    "CI that runs every --selftest"  NARROWED, still worth doing
              CI exists; it covers 7 suites, not the --selftest surface,
              and does not run tools/known_answer.py
```

Two further structural claims, checked:

```
"no installable package"        NARROWED. Three folders ship a package
                                definition. No repo-wide core: true.
"no machine-readable claim
 index"                         HOLDS, and sharper than stated.
                                tools/validate_claim_table.py validates
                                CLAIM_TABLE.json and zero exist:
                                a consumer with no producer.
```

## The instruments, run

The reply's section 2 asks for one thing: run them and report the
failures, on the stated ground that a failing self-test here is a
result. `run_instruments.py` does that in a throwaway worktree at a
pinned revision, because running them in place edits the tree being
measured -- `self-scan` `SS_009`.

`REFUSED` is a first-class state and not a failure: a module that exits 2
on `--selftest` is following the house convention, and one that exits 0
on an invocation running nothing would be the defect. `DEP_MISSING` and
`NO_CHECKS` are kept apart from `FAIL` for the same reason. All five
states are shown reachable on constructed modules before the sweep runs.

Counts are printed by the tools, not stored here.

## What the sweep found

```
300 modules expose --selftest at 6633778

  PASS               156     4922 checks executed
  REFUSED            107     names where its checks do live
  NO_CHECKS           28     exits clean, prints no count
  FAIL                 5
  FLAG_NOT_ACCEPTED    2     unittest files; parser rejects the flag
  RUNS_BARE            2     checks run on plain invocation
  TIMEOUT              0
  DEP_MISSING          0
```

Four of the five failures are content findings -- an instrument
reporting on the corpus, which is what the reply said a failing
self-test here is. The sharpest is `notes/check_datasets.py`, which
reports that `G-SPAN` and `MESA` now resolve outside `sim-span/` and
that *finding 3 must be restated*: a check telling its operator which
recorded finding has gone stale, and naming the file that broke it.

The fifth is a broken run, and it is a real defect
(`EA_018`): `columbia-chain-cascade/UNDERGRADUATE_RESEARCH_GAPS.md` is
read by four modules and is not in the tree, so `selftest_kill.py` dies
before its first check and `assemble_gaps_v2.py` cannot run -- which
means the published *strip the fences and v1 returns byte-for-byte*
identity has no input side and is not checkable here.

## The sweep's own reader was wrong twice first

Recorded because the numbers above are worth nothing without it.

```
first run    132 modules read NO_CHECKS that DO print a count.
             The tree carries FIVE selftest output conventions, and
             refuses the flag with exit 2 in one folder and 1 in
             another, so neither format nor exit code discriminates.
             The repo's own census.py shows the same symptom as
             RAN_NO_VERDICT.

second run   a crashing module read as REFUSED, because the refusal
             rule looks for the output naming another .py file -- and
             a traceback names .py files. columbia-chain-cascade's
             FileNotFoundError vanished from the failure list.
```

Both are fixed, both have a null test, and all seven states are shown
reachable on constructed modules before the sweep is allowed to run.
`RUNS_BARE` and `FLAG_NOT_ACCEPTED` exist so that a property of the
invocation is not filed as a property of the module.

## What is not done

The reply's O-1 has two halves. The executions are done. **No claim has
been checked against its own falsifier**, which is the half that needs a
reader per claim rather than a runner, and it stays open.

No external citation was checked; the egress gate refuses the publisher
hosts, and the review's own section 0.3 records the same for its arXiv
identifiers. Nothing here rests on one.

## Run

```
python3 external-audit/recount.py
python3 external-audit/recount.py --selftest
python3 external-audit/run_instruments.py --rev 6633778
python3 external-audit/run_instruments.py --selftest
python3 external-audit/recount.py --choices
```

---

## The second pass, and three readers of one tree

The review landed a second time (`DEEP_RESEARCH_2026_09_14_V2.md`, landed
verbatim beside the first, both inspectable). It is a revision, not a
rewrite -- 580 of 649 lines equal, nothing deleted wholesale -- and the
change that matters is that it **replaces** its own section 0: v1's
source-verification record becomes v2's execution record, answering the
response document's request to run the instruments. The four SVG assets
both renderings reference are landed under `assets/`, so the images
resolve for the first rendering too, which had referenced them without
carrying them.

The family tables are byte-identical across the two, so `recount.py`
reads both with one parser (`report_text(path)` / `families(path)`,
generalised rather than copied) and every `EA_001..EA_014` finding
carries to the second pass unchanged -- the two phantom folders included.

What is new is that there are now **three independent sweeps of one
tree**: the second pass's, this folder's `run_instruments.py`, and the
repository's own `self-scan/census.py`. `crosscheck.py` compares them.
Nobody coordinated, which is what makes the panel worth having --
`triad-playground` `TP_008`'s decorrelated shadows, arriving for free.

```
python3 external-audit/crosscheck.py            # the comparison
python3 external-audit/crosscheck.py --choices  # the seven choices
python3 external-audit/crosscheck.py --selftest # the checks
```

Five results, in order of how much they cost to find:

- **Two readers, one run, 0 and 2, both right.** The known-answer gate
  prints 84 PASS and 2 FAIL (pinned) per case and a headline reading
  `cases disagreeing with the registry: 0`. One reader took the column,
  the other the headline. The headline counts disagreement with what the
  registry *expects*; a pinned failure that fails agrees with it. One
  name, two denominators (`EA_020`).
- **Different revisions.** `gate-check` scans 2342 files for the second
  pass and 2331 for ours, which pins `6633778`. The eleven-file gap is
  this folder landing, so the revision is the first candidate explanation
  for every divergence (`EA_021`).
- **Four of five failures agree, and each sweep has one the other
  missed** (`EA_022`).
- **`evaluation-frame`'s selftest reads a path outside the repository.**
  It passes here at both revisions and fails for the second pass; neither
  party is wrong, because the verdict is a property of the sandbox. Its
  own `EF_009` already says the corpus is written by the run that reads
  it -- measured from outside by someone who could not have known to look
  (`EA_023`).
- **The reported exit/verdict mismatch is the refusal convention, and the
  real defect was in the census.** Four rows came back
  `SOME_FAILED_UNCOUNTED` on output saying `failed: 0`, because
  `checks: N   failed: M` was unparsed and the fallback heuristic's dirty
  test matched the **check count**: `142   failed`. Repaired in
  `self-scan/resolve.py::parse_count`, where census reads it, with the
  reason pinned in that module's own selftest (`EA_025`).

And one about this folder: `notes/check_datasets.py` now names
`external-audit/` among the files giving its guarded terms an independent
antecedent. The check is not broken -- it caught the audit (`EA_027`).

Two errors of this session's own are recorded rather than smoothed: an
exit code read from a pipeline instead of from the module (`EA_024`), and
a reader that knew three output conventions in a tree that uses five.
