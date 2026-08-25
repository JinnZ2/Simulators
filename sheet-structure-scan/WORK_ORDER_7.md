# WORK ORDER 7 — THIRD WORKBOOK, SELECTION AND RUN

Delivered verbatim. Nothing in this file is edited; the screen is
`select.py`, the predictions are `PREDICTIONS_WO7.md`, the reject log is
`samples/runs/wo7_reject_log.sample.txt`, and the audit is in
`CLAIM_TABLE.md` (`SSS_050..`).

---

WORK ORDER 7 — THIRD WORKBOOK, SELECTION AND RUN

S1. SELECTION CRITERION — stated before searching
  Eligible iff ALL hold:
    a. ships values in its own cells (not a blank template)
    b. carries provenance prose classified RETROSPECTIVE
       under the amended WO4 test
    c. contains at least one arithmetic relationship whose
       operands resolve inside the file
    d. file date separated from both prior files
    e. different authoring body than UNFCCC and TCR
  Screen a-c programmatically BEFORE running scans 1-4.
  Ineligible -> report why, discard, next candidate.
  Record every candidate screened and its reject reason.
  The reject log is a finding: if most published workbooks
  fail (b) or (c), the testable population is small and
  that is worth knowing independently of any curve.

S2. NO TUNING
  PROVENANCE_WORDS, patterns, tolerances frozen at their
  WO6 values before the candidate is chosen. Any change
  needed to locate this file's provenance is recorded as a
  post-hoc widening and the run is reported twice — frozen
  and widened — as with patterns.json.

S3. PREDICTIONS — registered before the run
  P1 zero MAINTAINED  (n=1 so far, UNFCCC)
  P2 DIVERGED > HOLDS_UNMAINTAINED
  P3 H1: where one provenance note states two relationships,
     the lower-operand-count one survives and its value
     appears in the higher one's targets
  P4 operand count separates the bins
  Each may return NOT ADDRESSABLE. That is a legal verdict
  and is not counted as support or refutation.

S4. CROSS-FILE
  n = 3. Emit share, bin counts, operand counts, file dates,
  per workbook. Print n.
  Curve permitted only if all three are RETROSPECTIVE and
  all three shares are non-None. Otherwise direction only,
  and only if signs agree. LGO stays in the table as
  OUT_OF_SCOPE with its zero, never in a denominator.

S5. CONSTRAINT
  Capabilities declared per item as in WO6. Reader budget
  unspent unless the format genuinely requires it.
  No severity language. Reports structure only.
