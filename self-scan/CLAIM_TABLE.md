# CLAIM TABLE — self-scan

Claims about the scan and what it found. `SS_001..SS_012`.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim; it does not retune the scanner. Where a check and a claim
disagree, the disagreement is recorded and the claim is amended in
place with the date, per the arrangement `uninstrumented/` uses for its
cases and `AUDIT_NOTES.md`.

Nothing in this table is a statement about whether a folder's work is
good. `DIVERGED` means a sentence and an artifact differ; it makes no
ruling on which is wrong. That naming came from WO6's amendment to
scan 4 and is used here unchanged.

---

### SS_001 — the target's own stated size is stale in the order that names it

WO10 states the target as 4636 lines, 314 KB. Measured: **6744 lines,
469173 chars**. The order is not wrong; the file grew between writing
and running, which is the quantity under test arriving before the
instrument does.

**Falsifier:** a checkout at the order's own date measuring 4636 lines.

**Status: SUPPORTED.**

---

### SS_002 — six of nine divergences did not match when written, not drifted

S5 asked for a divergence date. Dates alone cannot separate *right when
written and overtaken* from *already differing when written and also overtaken*, so
the check is re-run in a throwaway worktree at the commit that
introduced each number. Result: **6 BORN_DIVERGED, 2 DRIFT, 1
DRIFT_POSSIBLE**, and four of the six carry an interval of +0.00 days —
artifact and paragraph committed together.

**Falsifier:** a replay at the introducing commit returning the stated
number for any claim marked BORN_DIVERGED.

**Status: SUPPORTED, 6 of 9.**

---

### SS_003 — UNRECOVERABLE does not appear, and the first version made it appear anyway

S5 said this is the first run where UNRECOVERABLE should not appear. In
the final run it does not. In an earlier one it appeared **once**, for
`model-provenance`'s "29 selftest\nchecks" — the claim text is wrapped
across a line in markdown, and the first version normalised the newline
out before handing the string to `git log -S`, which then matched
nothing.

An instrument defect reported as an absence in the data. Repaired by
passing the matched text as it appears, newline included.

**Falsifier:** a claim whose introducing commit is genuinely
unrecoverable — a value present in the initial commit of `CLAUDE.md`,
which `-S` cannot date to before the file existed.

**Status: SUPPORTED, and the near miss is the point.**

---

### SS_004 — the imported stance test reads section length, measured at 7x

Applied to this document the WO6 marker test returns NEITHER on 73 of 96
sections, and the sections it does classify are the long ones: median
length 26 / 65 / 142 for NEITHER / PROSPECTIVE / RETROSPECTIVE. A section
in the shortest third gets a non-NEITHER verdict **6%** of the time; one
in the longest third, **44%**.

Mechanism: the test counts markers of two kinds and compares the counts,
so a longer section carries more of both and is likelier to break the
tie. This is a statement about transfer, not a defect — the test was
built for a provenance cell in a workbook and returns NEITHER rather
than guessing.

**Falsifier:** a length-stratified sample in which the share is flat.

**Status: SUPPORTED.**

---

### SS_005 — WO10 S1's own rule is resolvability, not stance

S1 says "RETROSPECTIVE by WO6 rule — operands resolve inside this file
tree". Those are two criteria: the WO6 rule reads markers in a sentence,
and *operands resolve inside the tree* is resolvability, which is what
S3 measures. `sheet-structure-scan` SSS_051 recorded that conflating
them makes two criteria compute one quantity.

Both readings are reported and neither is picked. No claim was removed
from a denominator on stance grounds.

**Falsifier:** a section where the two readings disagree and the
disagreement changes a bin. None occurred, because no extracted claim
falls in a roadmap passage.

**Status: SUPPORTED, and untested at the point where it would matter.**

---

### SS_006 — MAINTAINED is 1 of 42, and it is the only number a test asserts

`tests/test_gate_drift.py` asserts that `GUARDS.md` regenerates
byte-identically from `guards.json`. That is the single claim in
`CLAUDE.md` with a test behind it. Every other number is one a human
typed, checked once, and left.

**Falsifier:** any other extracted claim resolving MAINTAINED.

**Status: SUPPORTED, 1 of 42.**

---

### SS_007 — five IDENTITY claims are not re-checkable from this repository, ever

All five `SUBJECT_NOT_IN_TREE` verdicts compare a **delivered upload**
against a repo copy: MF_019's stale gate copies, PB_011's three copies
of one file, UNI_068's re-delivery check, SSS_053's two identical
candidate workbooks, and `instrument-epistemology`'s pre-repair output.
Each comparison was made at the time against bytes that were never
committed.

Not a mechanism candidate: nothing prevented the measurement, it was
taken. What is missing is the record of one side, which is closer to
`claim-record`'s field 7 than to an exclusion. `notes/check_uploads.py`
is the repair pattern — record a hash so a re-obtained copy is
checkable — and it did not exist when any of the five was written.

**Falsifier:** a hash recorded beside any of the five, making a
re-obtained copy checkable.

**Status: SUPPORTED, 5 of 5 unresolvable IDENTITY claims.**

---

### SS_008 — "430+ tests green" carries two statements and they came apart

`grounding-layers` is stated as "430+ audit-grade tests green". Measured:
**516 passed, 9 failed**. The lower bound on the count is met; the word
*green* is not. Both are printed and the bin follows the word, with the
alternative reading in the output so it can be argued with.

The mirror case is `fourd-municipal-engine-v2`: "40 pass, 2 skip" is now
37 pass, 2 skip **and 3 failed**, so a count comparison alone would have
reported a suite that shrank rather than one that broke.

**Falsifier:** the nine `grounding-layers` failures turning out to be
environment-specific, which would make the phrase true in its own
context and this reading a property of the container.

**Status: SUPPORTED, and the falsifier is live — the suite needs
numpy, scipy, matplotlib and psutil, all installed for this run.**

---

### SS_009 — running the scan modified the repository it was measuring

The first version ran checks in place. Resolving a COUNT claim means
**executing code**, and this repository's suites write: two provenance
ledgers, a `gate_T.denied.json`, a `pch_log.jsonl`, and one file
literally named `--selftest`.

That is the structural difference between scan 4 on a workbook and scan
4 on a repository, and no fixture could have shown it. Repaired: every
check runs in a throwaway `git worktree` at HEAD, asserted by a selftest
check comparing `git status --porcelain` before and after a scan. The
cost is stated — what is measured is HEAD, so an uncommitted change is
invisible to this scan.

**Falsifier:** a check that dirties the tree despite the worktree.

**Status: REPAIRED, pinned.**

---

### SS_010 — the replay refuses a comparison that is not like-for-like

`sheet-structure-scan`'s replay at the introducing commit returned 209
across **8** modules where the live check reads 237 across **9**.
Comparing 209 to the stated 247 would be a ratio across unlike objects
with a verdict attached, so the state stays `DRIFT_POSSIBLE` and the
note names the module counts.

This is the one claim of the nine whose kind is undecided, and it is
undecided because the guard fired rather than because the evidence is
thin.

**Falsifier:** identifying which module was silent at that revision and
re-running like-for-like.

**Status: SUPPORTED — a guard that fires on a real case.**

---

### SS_011 — every prediction held, and one of them was worth making

P1 through P5 all HELD. P3 and P5 were close to structural knowledge, P2
is nearly free on a file this size, and P4's margin was large against a
line drawn at a different document class.

**P1 is the one that could have failed**: DIVERGED rate 0.182 in the
`selftest N/N` family against 0.364 in the pytest-suite family, a factor
of two in the predicted direction. Mechanism: a `selftest N/N` sentence
and the module printing N are written in one commit with the module as
the authority; a suite count is written once and the suite grows past
it.

**Falsifier:** the two family rates converging on a second document.

**Status: SUPPORTED, with the discount stated.**

---

### SS_012 — the scan corrects nothing, on purpose, and that is a debt

Nine numbers in this table's target do not match their artifacts and this
run leaves them as they are. Correcting them in the same commit would destroy the
sample's reproducibility: `samples/scan.sample.txt` names commits, and
the S5 replay resolves against a history the correction would extend.

The correction is a separate commit after this one. Until it lands, the
nine rows in `RESULTS.md` are the record of what did not match, and since when —
which is the only form in which that record can exist, since fixing a
number removes the evidence that it ever differed.

**Falsifier:** the correction landing and the scan then returning a
lower rate, which would confirm the numbers were the cause rather than
the scan.

**Status: OPEN — the correction is not made.**

---

### SS_013 — the compute-budget hypothesis is refuted for these claims, and its second half holds in a stronger form

Relayed from another instance: the unbacked numbers here are unbacked
because *"the claim and the check live on different machines"* — the sim
ran on hardware that could run it, the number was written down on a
device that cannot re-run it, so the maintenance operation needs a
resource the author does not have. Proposed consequence: a distinct
`NOT_TESTABLE`-by-compute-budget bin, and the rate split by it.

Measurable rather than arguable, and the measurement is the import
graph. `census.py` walks the tree, and:

    76 of 76 modules exposing --selftest import nothing outside
    the standard library.  74 of the 76 run green here.

    32 of 44 bindable CLAUDE.md claims need nothing but the
    standard library.  5 need only pytest.  4 need more.

**The first half does not describe these claims.** Every module carrying
its own checks is stdlib-only by construction, and this scan ran 41 of
42 claims on one container in one pass. What stands between those
numbers and a check is not a machine; it is that nothing runs the check.

**The second half holds, and more strongly than stated.** The relayed
message says the stdlib-only convention *is* the boundary of what can be
checked locally. Measured, it is better than that: inside the boundary
essentially everything checks — 74 of 76 green — so the constraint is
not merely where checking stops, it is where checking is free.

Where compute does bite is the pytest arm, not the selftest arm:
**4 of 20 test directories** need numpy / scipy / matplotlib / psutil /
jsonschema, and those are the ones a phone cannot run.

**Falsifier:** a module carrying `--selftest` that imports a
third-party package, or a `CLAUDE.md` claim whose only possible check
needs hardware absent here.

**Status: first half REFUTED on measurement, second half SUPPORTED and
sharpened.**

---

### SS_014 — the rate has an environment, and NOT_TESTABLE is not one state

`SS_013`'s useful residue. A claim whose check needs numpy is
`NOT_TESTABLE` on a machine without numpy and resolvable on one with it,
so a rate quoted with no environment is a number with an unstated
denominator — which is the shape this folder exists to find.

The report now prints both. `NOT_TESTABLE` splits by cause:

    SUBJECT_NOT_IN_TREE              5
    SUPERSEDED_IN_THE_SAME_SECTION   3
    QUOTED_NOT_ASSERTED              1
    MISSING_DEPENDENCY               0   (in this environment)

`MISSING_DEPENDENCY` is empty **here** and was 6 before the run
installed pytest, numpy, scipy, matplotlib, jsonschema and psutil. That
is the bin the relayed message asked for; it exists, it is reachable,
and on this machine nothing is in it. The environment block above the
rate says which machine that was.

**Falsifier:** a run on a stdlib-only machine returning the same rate,
which would mean the environment does not move it.

**Status: SUPPORTED — the bin is built, and it is empty here for a
reason the report states.**

---

### SS_015 — the paragraph describing the scan carried a stale count of the scan

The `self-scan/` entry added to `CLAUDE.md` in the commit before this
one stated "69 selftest checks across two modules". Adding `census.py`
made it three modules and a different number, so the sentence describing
the divergence measurement became a divergence, immediately, in the same
document.

Not repaired by writing a bigger number, which would go stale on the
next module. The count is removed and replaced by the command that
produces it: *selftest counts are printed by each module and totalled by
`census.py`*. The only number that cannot go stale is one that is not
written down.

That is `claim-record`'s field-5 rule — derive at read time, never store
— arriving in prose, and it is the structural answer the relayed message
was reaching for: inside the stdlib boundary, write the command rather
than the number.

**Falsifier:** a stored count in this folder's own documentation that
survives a year of edits.

**Status: SUPPORTED, and repaired in the direction the finding points.**

---

### SS_016 — the extractor cannot tell a quoted claim from an asserted one

The new `self-scan/` paragraph quotes `430+ audit-grade tests green`
while discussing `grounding-layers`' claim about it. The extractor
matches pattern, not attribution, and recorded it as a claim **about
`self-scan/`**.

Use-mention: `UNI_009`'s substring bleed and `DF_010`'s use-mention
problem arriving in this scanner, in the one document most likely to
quote claims — an index whose subject is other folders' claims.

Handled by declaration rather than by a cleverer pattern:
`QUOTED_NOT_ASSERTED` is a binding reason, so the occurrence is counted,
excluded from every denominator, and says why. A pattern that tried to
detect quotation would be guessing at attribution, which is the thing
`bindings.py` exists to refuse.

**Falsifier:** a quoted claim that a pattern can separate from an
asserted one without reading attribution.

**Status: SUPPORTED — recorded, not pattern-matched away.**

---

### SS_017 — the census could not census its own run

`census.py` advertises `--selftest`, so it discovers itself, and the
first version then **ran** itself — which runs itself. It hung.

`UNI_010`'s self-reference loop in a third form: not a scanner reading
its own output (`uninstrumented/scan.py`) and not a note written into
the tree it is checked against (`notes/` finding 8), but a runner
running itself. Found by it hanging, not by reading it.

The module stays in the inventory and in the tier count, where it is a
real row, and is not executed; the state is `EXCLUDED_SELF_REFERENCE`
rather than the row disappearing.

A second isolation defect surfaced in the same module: `resolve._run`
resolves its cwd through `resolve.base()`, and `census.py` passed the
worktree path while leaving `BASE` unset, so children ran with the
working tree as cwd and one wrote a denial record into it — `SS_009`
recurring one module over, in the module written to record `SS_009`.
Both are pinned by selftest checks.

**Falsifier:** a census that can measure its own run without recursing.

**Status: REPAIRED, both pinned.**

---

### SS_018 — the one screen exemption, declared and measured

WO10 S7 says no severity language. The scan report passes the imported
`no_severity` screen with an empty exemption list. The census report
does not: when a `tests/` directory prints no summary, the detail column
relays **pytest's own last line**, which reads `5 errors in 0.66s`.

That word is the tool's. Rewording it would misquote the tool, so it is
exempted — and exempted the way `sheet-structure-scan` SSS_049 kept the
three-arm harness for: one arm masks the relayed text and asserts the
report is otherwise clean, a second asserts the relay is the **only**
thing that fires without the mask, and a third plants a violation and
requires it caught through the exemption.

Exactly one row in the corpus uses it (`crossdomain-eval/tests`), and it
is a row reporting that a suite did not run.

**Falsifier:** a second thing firing without the mask, which the second
arm turns red.

**Status: SUPPORTED, three arms.**

---

### SS_019 — self-enumeration and tree-writing are independent; the hypothesis is refuted on its own examples

Handoff item 1: `census.py` hung on itself **and** wrote into the tree it
measured, and the hypothesis is that anything enumerating the tree it
runs in has both by construction, because the exclusion and the
isolation are one problem.

`enumerators.py` tests it against the population. Fifty modules call a
directory-enumeration primitive; forty-nine ran. Both properties are
**measured by running**, not read from source: enumeration roots are
traced by wrapping `os.walk` / `os.listdir` / `glob` in a
`sitecustomize` on the child's path, so what is recorded is where the
module really looked, and writing is a `git status` diff across the run
in a throwaway worktree.

                       writes: yes   writes: no
    enumerates self yes            1           15
    enumerates self no             2           31

    of 16 that enumerate themselves, 1 writes  (6%)
    of 33 that do not,               2 write   (6%)
    difference: +0 points

**The three modules the handoff named all enumerate themselves and none
of them writes** — `uninstrumented/scan.py`, `reasoning-gate/mine_logs.py`
and `inverseminar/inverseminar.py` are `yes / no` each. The paired
prediction fails on exactly its own examples.

The diagonal share is 65% and is **not** the test: only 3 of 49 modules
write at all, so with a margin that thin the diagonal is mostly the
`(no, no)` cell and would read high whatever the self column did. The
report prints the within-group rates instead and states the bound.

**A finding about the instrument on the way:** running each module with
`--selftest` reached **no enumeration at all** for the two named
scanners, because their selftests do not exercise the walk. Their real
invocations are declared in `INVOCATIONS`, found by running them —
`scan.py` with no argument prints usage and exits 0 without walking, and
`mine_logs.py .` raises `FileNotFoundError` before its glob because the
guards path defaults relative to the cwd. Measuring the arm that matters
required knowing that.

**Falsifier:** a population with a fuller write margin in which the two
rates separate.

**Status: REFUTED, at low power, with the power bound stated.**

---

### SS_020 — the predictor is execution, not enumeration

`SS_019`'s replacement. `census.py` had both defects and enumeration was
not why: **reading a tree cannot dirty it; running what is in the tree
can**, and the writes were its children's.

Same 2x2 against whether the module executes other code or opens a file
for writing:

                       writes: yes   writes: no
    executes yes                   3           16
    executes no                    0           30

    of 19 that execute or write by design, 3 write  (16%)
    of 30 that do not,                     0 write  (0%)
    difference: +16 points

All three writers execute; nothing that does not execute writes.

Reported as **weaker than the first test and labelled so in the output**:
`executes` is read from the source while `writes` is observed, so a
module that opens a file for writing is close to predicting itself. It
is the contrast with the enumeration column that carries the content,
not the number.

**Falsifier:** a module that writes into the tree without executing
anything or opening a file for writing.

**Status: SUPPORTED, with its own weakness declared in the report.**

---

### SS_021 — 35 of 42 claims are convertible to a command, including all 9 that diverged

Handoff item 2: generalise `SS_015`'s repair. A claim whose number has a
generating command can have the number deleted and the command named
instead.

    35 of 42 resolved claims are convertible
     7 have a check that is not a count -- byte comparisons,
       a regeneration, a git diff: nothing to convert
     9 of 9 DIVERGED claims are convertible

**One correction to the handoff's framing.** It says the conversion turns
DIVERGED-able claims into MAINTAINED-by-construction. It does not. It
makes them **stop being claims**: there is no stored number left to
diverge from, which is a different state from a number a test asserts.
`MAINTAINED` means something checks it; a converted claim means nothing
needs to. Counting the second as the first would report a removed claim
as an asserted one, and the report says so where it prints the number.

The conversion is **not applied here**, per `SS_012`: the pinned sample
names commits and the S5 replay resolves against a history a correction
would extend. Measuring it is this commit; applying it is the next one.

**Falsifier:** a convertible claim whose command produces a different
quantity than the sentence states, which would mean the conversion loses
content rather than storing it elsewhere.

**Status: SUPPORTED — measured, not applied.**

---

### SS_022 — the quoted-context test is structural, and the file supplies its own control

Handoff item 3. `CLAUDE.md` is an index whose subject is other folders'
claims, so it quotes them constantly and a pattern cannot tell a quoted
claim from an asserted one. `SS_016` recorded that after it happened.

The test does not guess at attribution. Markdown puts a quoted claim in
a **code span** and an asserted one in running prose, which is a property
of the markup:

    line  236   430+ audit-grade tests green.       bare, asserted
    line 6665   `430+
      audit-grade tests green`                      in a span, quoted

**The same string, both ways, in the same file** — a matched pair the
document supplied without being asked, so the test has a known answer in
both directions rather than only the one that motivated it. `code_spans`
handles fenced blocks first so a backtick inside a fence does not open a
span, and allows a span to wrap a line, which is how the quoted one is
written.

The flag **never excludes**. A flagged claim must be declared in
`bindings.py`, which is where attribution decisions live, and a selftest
check asserts every quoted claim has an explicit binding. That converts
a silent misattribution into a required decision.

**Falsifier:** a quoted claim in running prose with no code span, or an
asserted one inside a span.

**Status: SUPPORTED, with a two-directional known answer.**

---

### SS_023 — WO9 is not in this repository

Handoff item 4 names WO9 (PlanExe) as the open instrument check: a known
answer declared by the generator's authors, and the only queued run that
measures the **grid** rather than a corpus.

Searched: `PlanExe`, `plan_exe`, `WORK_ORDER_9`, `WO9`, case-insensitive,
across every text file and the full git history including all branches.
**Nothing.** The work orders present are `WORK_ORDER_4`, `_6`, `_7`,
`_10` under `sheet-structure-scan/` and `self-scan/`, plus unnumbered
`WORK_ORDER.md` files under `fold-matrix/`, `model-provenance/`,
`nonidentity-census/` and `residual-direction/`.

Nothing is reconstructed. An order is a delivered artifact and inventing
one puts a specification in the author's mouth — the `PB_001` / `CW_004`
rule.

The point the item makes stands independently and is worth recording
even with the order absent: **everything run in this folder measures a
corpus**, and a known answer declared by a generator's own authors would
measure the **instrument**. That is the `null-harness` known-truth-first
invariant, and this folder has never had one.

**Falsifier:** the order arriving.

**Status: OPEN — the artifact is absent, not the argument.**

---

### SS_024 — one DIVERGED verdict was mine, not the document's

`fourd-municipal-engine-v2 | 40 pass, 2 skip` was binned **DIVERGED**,
observed `37/2 (3 failed)`, and S5 dated it **BORN_DIVERGED** — the
artifact and the paragraph committed together and not agreeing even
then.

It agreed. The suite's CLI tests spawn
`python3 -m fourd_municipal_engine.cli` in a subprocess with **no
PYTHONPATH**, so they pass where `pip install -e .` has been run and
fail on a bare checkout. With one line putting the package root on the
child's path the suite returns exactly **40 passed, 2 skipped**.

The claim was right the whole time. The divergence was the scan's
environment.

`crossdomain-eval`'s "68 total" is the same: 68 passed, once `sympy` —
a declared non-stdlib dependency — is present.

**`SS_014` named this shape and did not catch this instance**, and the
reason is worth having: a missing dependency announces itself as a
collection error, and the scan reports `NOT_TESTABLE` with the name.
A missing **path** produces a summary line, and a summary line reads as
a measurement. The environment block reports what is installed; it has
no cell for what is importable *from where a subprocess runs*.

**Falsifier:** a second DIVERGED verdict that dissolves under an
environment change.

**Status: REFUTED — the verdict was withdrawn, not the claim.**

---

### SS_025 — three mechanical repairs, 15 failures to 7

None of the three was a disagreement between a test and the code it
exercises.

1. `grounding-layers/tests/test_l_epsilon_epistemic.py` shipped with
   **no import statements at all** — it uses `EpistemicInstrument` and
   `np` with nothing binding either, so all three tests raised
   `NameError`. An extraction artifact from a context where both were
   already in scope. Two of the three now pass.
2. `fourd-municipal-engine{,-v2}/tests/test_cli.py` — the PYTHONPATH
   above, six tests across two folders.
3. `crossdomain-eval` — `sympy`, five collection errors.

Repo total moved **1198 passed / 15 failed → 1274 passed / 7 failed**.

The seven that remain are substantive: assertions in the L-epsilon and
bias-audit tests that disagree with the code they exercise, plus a
pinned demo output and a thermodynamic check. Deciding whether the test
or the code is right there is a change to the drop's own physics, so
they are named and left. The line is mechanical-versus-substantive, not
easy-versus-hard.

**Falsifier:** one of the seven turning out to be environmental too.

**Status: SUPPORTED, with the remaining seven classified rather than
fixed.**

---

### SS_026 — the eight DIVERGED claims are converted, and the rate is now 0 for a reason that is not an improvement

`SS_012` recorded the debt and said the correction would be a separate
commit. This is it, and the repair is `SS_015`'s rather than a
correction: **the count is deleted and the command that produces it is
named instead.**

    23 tests green                -> run `pytest thermal-sensor-degradation-audit`
    430+ audit-grade tests green  -> read the summary line; and NOT green,
                                     with the seven named
    17 files total                -> `ls relational/`
    selftest 25/25                -> `--selftest` green
    selftest 20/20                -> `--selftest` green
    247 selftest checks green     -> totalled by self-scan/census.py
    29 selftest checks            -> `--selftest` green
    74 selftest checks            -> `--selftest` green on both modules

Result: **DIVERGED 0, n = 34, rate 0.000.**

**That number is not an improvement and the report says so above it.**
The denominator moved 42 → 34 because eight claims stopped being
claims. A rate that falls because claims were removed says nothing
about how the remaining ones are maintained, and a reader who sees
0.000 without the denominator has been handed exactly the shape this
folder exists to find. `render` now prints `READ THE DENOMINATOR`
beside the rate whenever the retired ledger is non-empty, with the blob
where the eight were last measured.

The `grounding-layers` line is the one that gained content rather than
losing it. `430+ tests green` was a bound plus a word, and the word was
false (`SS_008`); the replacement states that the suite is the largest
in the tree, that it is **not green**, and why the remaining failures
are not repaired here.

**Falsifier:** a converted line that a reader cannot act on — a command
that does not produce what the deleted number stated.

**Status: SUPPORTED. `SS_012` closes.**

---

### SS_027 — a converted binding is retired, not deleted

The eight bindings would have become orphans and the orphan check would
have gone red. Deleting them would have cleared it, and taken with it
the record that the claims ever existed — which is `SS_012`'s own
argument, one level down: correcting a number removes the evidence it
differed, and that applies to the binding too.

They move to `bindings.RETIRED`, which nothing reads. Three selftest
checks hold the line: retired and live are disjoint, no retired key
still names a live claim, and the ledger is non-empty.

**Falsifier:** a retired binding reappearing in `BINDINGS`.

**Status: SUPPORTED.**

---

### SS_028 — one of my own checks read the data it was checking

`resolve.selftest` asserted that a repeated `(section, pattern, value)`
triple gets distinct ordinals, and it keyed off a **real duplicate in
`CLAUDE.md`** — `simulation-hypothesis-budget`'s two `selftest 20/20`
occurrences. Converting one of them left the list with a single element
and the check raised `IndexError`.

The check was correct about the code and wrong about how to ask. A
known-answer check that reads the corpus under test breaks when the
corpus changes, and the failure is indistinguishable from the property
failing. Rebuilt on a constructed repeat, with a second check that
ordinals do not collide across different triples.

Same family as `notes/` finding 8 and `UNI_010`: an instrument whose
input is the thing it measures. Third form in this folder after
`SS_009` (a scan that modified its tree) and `SS_017` (a census that
ran itself).

**Falsifier:** a check here that still depends on a specific string in
`CLAUDE.md`.

**Status: REPAIRED.**

---

### SS_029 — the quoted-claim count grows with every audit paragraph, and the check that reports it raised instead

`SS_016` found one quoted claim. There are now **three**, all in the
`self-scan/` paragraph: `40 pass, 2 skip` quoted by `SS_024` while
withdrawing a verdict against it, `430+ audit-grade tests green` quoted
twice, once by `SS_008` and once by `SS_026` reporting what replaced it.

That is structural, not accidental. **A folder whose subject is other
folders' claims quotes them**, and every audit paragraph written here
adds more. The structural test (`SS_022`) catches all three from the
markdown, and each is declared in `bindings.py` rather than
pattern-matched away — so the count going up is the flag working, not
drift.

**The check written to report this state raised on it.** It indexed
`bindings.BINDINGS[c["key"]]` directly, so a newly quoted claim with no
binding yet gave a `KeyError` inside the selftest instead of a failed
check. A raise is not a failing check; it is a dead selftest, and the
whole suite stops there. Changed to `.get`, plus a check that the
quoted set has more than one member so the branch cannot go silent.

Second instance in this pass of one of my own checks breaking on the
data it reads, after `SS_028`. Both were found by running, neither by
reading.

**Falsifier:** a quoted claim outside the `self-scan/` paragraph, which
would make the pattern about the file rather than about audit prose.

**Status: SUPPORTED, and the check is repaired.**

---

### SS_030 — the conversion destroyed the control the quoted-context test rested on

`SS_022`'s strongest feature was that the file **supplied its own
two-directional known answer**: `430+ audit-grade tests green` appeared
bare at line 236 and inside a code span at 6665, so the structural test
had a positive and a negative case in the corpus itself, and neither was
constructed.

`SS_026` converted the bare one. Every remaining occurrence is a
quotation, and `extract.py`'s check — *"the file carries the same claim
quoted and bare"* — went red. `census.py` went red behind it, because it
runs `extract.py --selftest` as its sibling-module probe.

**A repair in one place took out a test in another**, and the test it
took out was the one holding the finding that motivated the repair's
own scanner.

Rebuilt as a constructed pair, so it cannot be destroyed by an edit to
the corpus, with the real file checked only for what stays true of it:
every remaining `430` occurrence is quoted. The constructed control is
weaker as evidence — `MP_008`'s shape, checkable where it is redundant —
and it is the version that survives the document changing under it.

Third instance in one pass of a check keyed to a specific string in the
corpus under test, after `SS_028` and `SS_029`. All three were found by
running.

**The general form, and it is worth stating once:** a known-answer
check whose known answer lives in the data under test is not a
known-answer check. It is a regression test on the corpus wearing one's
clothes.

**Falsifier:** a check in this folder that still reads `CLAUDE.md` for
its expected value.

**Status: REPAIRED, and the class named.**
