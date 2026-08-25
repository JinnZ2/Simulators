# WORK ORDER 4 — SCAN 4, STATED-RELATIONSHIP MAINTENANCE

Delivered 2026-08-25. Verbatim. Nothing in this file is edited.

---

```
WORK ORDER 4 — SCAN 4, STATED-RELATIONSHIP MAINTENANCE
Extends: fold detector. New scan, independent of scans 1-3.

S1. TARGET
  Any sheet carrying provenance/method prose (Info and
  sources, Notes, Methodology, References, Assumptions).
  Locate by header keyword, not by fixed sheet name.

S2. EXTRACT
  Parse prose for ARITHMETIC relationships only:
    mean/average of, sum of, product of, quartile of,
    median of, weighted by, scaled by, ratio of, times.
  Record: the operator, the named operands as written,
  the target the prose is attached to.
  Non-arithmetic provenance (source citations, dates,
  "estimated from") -> NOT_ARITHMETIC, counted, not tested.

S3. RESOLVE
  Map named operands to cells/ranges. Ambiguity is not
  guessed: two candidate resolutions -> NOT_TESTABLE with
  both candidates listed.

S4. TEST
  Recompute the stated operation from resolved operands,
  compare to target value. Tolerance stated in output,
  not hardcoded.
    target is a formula        -> MAINTAINED
    constant, relation holds   -> HOLDS_UNMAINTAINED
    constant, relation fails   -> BROKEN
    operands unresolvable      -> NOT_TESTABLE
  BROKEN: report the delta and, if the file carries revision
  history, when it diverged. Unrecoverable -> say so.

S5. OUTPUT
  Per-relationship rows plus bin counts. The four bins are
  the finding; no aggregate score, no ranking.
  BROKEN is not labelled an error.

S6. RATE — the reason this scan exists
  Emit per-workbook: bin counts, file age or version date,
  operand count per relationship, distinguishing
  same-sheet operands from cross-sheet.
  These accumulate across workbooks into a decay curve.
  Ratio to watch: BROKEN / (BROKEN + HOLDS_UNMAINTAINED).
  Do not report a curve from n=1. State n on every emission.

S7. FIXTURES
  G1  formula target, relation true -> MAINTAINED
  G2  UNF Info and sources!E10, Palestine mean of five
      -> HOLDS_UNMAINTAINED. A MAINTAINED verdict is a FAIL.
  G3  constant, one operand edited after the fact
      -> BROKEN, delta reported
  G4  prose naming an operand absent from the workbook
      -> NOT_TESTABLE, no guess
  G5  UNF hotel upper-quartile row -> the source
      distribution is external, so NOT_TESTABLE. A BROKEN
      or HOLDS verdict here is a FAIL: an untestable
      relationship must not score.

S8. CONSTRAINTS
  stdlib plus the spreadsheet reader. No labelling.
  Reports structure; reading stays with the operator.
  Selftest: G5 must not produce a testable verdict.
```
