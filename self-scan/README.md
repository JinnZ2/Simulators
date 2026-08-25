# self-scan

Scan 4 pointed at this repository's own `CLAUDE.md`.

`sheet-structure-scan` asks whether a workbook's prose still describes
its own cells. This asks the same question of a document whose operands
are files rather than cells: **does a sentence in `CLAUDE.md` still
describe the artifact it names, and does anything assert that it does?**

Delivered order verbatim in `WORK_ORDER_10.md`. Predictions in
`PREDICTIONS_WO10.md`, registered and committed before `resolve.py`
existed. Findings in `RESULTS.md`, claims in `CLAIM_TABLE.md`, pinned
output in `samples/scan.sample.txt`.

## The result

    MAINTAINED           1        rate  9 / 42 = 0.214
    HOLDS_UNMAINTAINED  32
    DIVERGED             9        BORN_DIVERGED   6
    NOT_TESTABLE         8        DRIFT           2
    UNBOUND              0        DRIFT_POSSIBLE  1

**Six of nine divergences did not match when the number was written**,
rather than being overtaken later. Four of those six carry an interval of
zero days: the count and the code it counts were committed together, and
they did not agree even then.

**One number in this file has a test behind it** — `GUARDS.md`
regenerating byte-identically, asserted by `tests/test_gate_drift.py`.
The other forty-one are numbers a human typed once.

## Layout

| file | what |
|---|---|
| `WORK_ORDER_10.md` | delivered order, verbatim |
| `PREDICTIONS_WO10.md` | five predictions, committed before the resolver existed |
| `extract.py` | S1 + S2: sections, stance, claim extraction |
| `bindings.py` | S3: which artifact each claim is about. Declared, never inferred |
| `resolve.py` | S3-S6: run the checks, bin, date the divergences, print the rate |
| `RESULTS.md` | what the run found |
| `CLAIM_TABLE.md` | `SS_001..SS_012` with a REFUTATION_PROTOCOL |
| `samples/scan.sample.txt` | pinned output of `resolve.py --replay` |

## Three decisions worth knowing before reading the numbers

**Extraction is programmatic; binding is declared.** Every claim is
found by pattern over the file — a hand-listed set on this target would
be selected by the party that wrote it. But which artifact a claim is
*about* is written down in `bindings.py`, never guessed: mapping "247
selftest checks green across nine modules" to nine paths is a judgement,
and a scanner that guessed would be reporting its own guess. An unbound
claim reports `UNBOUND`, which is a state and not a pass.

**Every check runs in a throwaway worktree.** The first version ran in
place and modified the repository it was measuring — the suites wrote
two provenance ledgers, a denial record, a JSONL log, and one file
literally named `--selftest`. Resolving a COUNT claim means executing
code, which is the structural difference between scan 4 on a workbook
and scan 4 on a repository. The cost: what is measured is HEAD, so an
uncommitted change is invisible here.

**The scan corrects nothing.** Nine numbers do not match and stay that way in
this commit, because `samples/scan.sample.txt` names commits and the S5
replay resolves against a history a correction would extend. The
correction is a separate, later commit; fixing a number destroys the
evidence that it ever differed, so the record has to land first.

## S5, the part no workbook could answer

Scan 4 returns `UNRECOVERABLE` for every divergence date on a workbook
(SSS_038), because `.xlsx` carries no per-cell history. Git does. For
each divergence this emits the commit that introduced the number, the
last commit touching the artifact, the last commit touching the
paragraph, and the interval.

Where the dates leave the case undecided, the check is **re-run against
the tree as it stood at the introducing commit**, in a worktree. That is
what turns `DRIFT_POSSIBLE` into `DRIFT` or `BORN_DIVERGED` — a
measurement rather than an inference. One case stays undecided, and it
stays undecided because a guard fired: the replay reached eight modules
where the live check reads nine, and comparing them would be a ratio
across unlike objects with a verdict attached.

## Running it

    python3 self-scan/extract.py --selftest      # 25 checks
    python3 self-scan/resolve.py --selftest      # 43 checks
    python3 self-scan/extract.py --sections      # S1 table
    python3 self-scan/resolve.py --replay        # the full run

The scanner is stdlib. Running a folder's own suite needs that folder's
dependencies, declared per binding: `pytest`, `numpy`, `scipy`,
`matplotlib`, `jsonschema`, `psutil` were installed for the pinned run,
and a missing one returns `NOT_TESTABLE` with the name in the reason
rather than a divergence.

CC0. Parses under Python 3.9.
