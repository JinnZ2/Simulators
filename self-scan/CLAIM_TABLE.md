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
