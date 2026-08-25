# WORK ORDER 6 — SECOND WORKBOOK, LEGACY READER

Delivered verbatim, together with the amendment to work order 4 that
arrived with it. Nothing in this file is edited; the audit is in
`CLAIM_TABLE.md` (`SSS_040..049`) and the results in `README.md`.

---

AMEND WO4 S4/S5: rename bin BROKEN -> DIVERGED
  "the cell and the stated relation differ" — no ruling on
  which is wrong, no damage asserted.
  Retire the delivered-order exemption entirely; if the
  order no longer names a screened token, no file fires.
  Keep the three-arm harness — it's the right structure for
  a real exemption later. Just don't spend it on this.
  Reword the two use-mention hits: already done, correct.

WORK ORDER 6 — SECOND WORKBOOK, LEGACY READER

S1. READER
  Add legacy .xls support. Target:
  2016-05-02-LGO-Standard-Inventory-Report.xls
  Constraint: legacy readers may not expose formulas, only
  cached values. If formulas are unavailable, say so and
  mark every scan that depends on them NOT_RUN. Do not
  substitute value-only heuristics and report them as
  scan output.

S2. RUN
  Scans 1-4 unchanged. No tuning to this file.

S3. CROSS-FILE, the reason this runs
  Emit, per workbook, side by side:
    bin counts, DIVERGED/(D+H), file date,
    operand count per relationship, and the bin each
    operand count landed in.
  n = 2. Print n. Still refuse a curve; two points give a
  direction, not a rate. Say direction only if the sign
  is the same.

S4. HYPOTHESIS UNDER TEST — H1
  From SSS_034, n=1: where a provenance note states two
  relationships, the lower-operand-count one survives and
  its value propagates into the higher one's targets.
  Test: does operand count separate the bins in this file
  too, and does any fill-value collision appear.
  No collision found -> H1 unsupported here, stated plainly.
  Prediction registered BEFORE the run, as before.

S5. CONSTRAINT
  If this workbook has no provenance prose sheet, that is
  the finding. Report it and stop; do not go looking for
  a substitute source of relationships.
