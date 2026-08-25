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
