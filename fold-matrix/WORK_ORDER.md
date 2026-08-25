# WORK ORDER 8 — FOLD MATRIX, UPWARD ARM

Delivered verbatim. Nothing in this file is edited; the instrument is
`fold_matrix.py`, the registered prediction is `PREDICTIONS_WO8.md`, and
the audit is in `CLAIM_TABLE.md`.

---

WORK ORDER 8 — FOLD MATRIX, UPWARD ARM
Extends: folded-term instrument. The downward arm (levels
severed, deepest still-acting term) already has a reading.
This specs the upward arm and the grid that holds both.

S1. STRUCTURE — one term, one grid, not one number
  Rows = levels, indexed from the term outward:
    negative index = downward toward substrate
    zero          = the term as used
    positive index = upward toward the stated purpose
  Columns, per level:
    severed        what relation was cut at this level
    still_acting   what keeps operating unreported
    clock          time constant ASSUMED at this level
    basis          measured | derived | ASSERTED | ABSENT

S2. UPWARD CELLS — the new arm
  For each positive level, ask what relation to the goal
  was claimed, and how it was established.
    measured  -> a measurement exists, cite it
    derived   -> derived from a measured parent, cite chain
    ASSERTED  -> claimed at adoption, no value string
    ABSENT    -> no goal stated at all
  ASSERTED and ABSENT are the expected majority. Register
  that as a prediction before running.
  Required field per upward cell: value_string —
  sign and magnitude of the claimed relation between proxy
  and goal. Empty is the normal result and is emitted as
  empty, never as zero.

S3. SCOPE FIELD — mandatory on any efficiency-class term
  efficient/optimal/better/faster require:
    with_respect_to, boundary, horizon
  Any missing -> NOT_EVALUABLE for that term. Do not score
  it, do not rank it, do not carry it into a comparison.
  A replacement claim (X more efficient than Y, therefore
  Y redundant) additionally requires:
    Y_function_set  enumerated | PARTIAL | UNREAD
  UNREAD -> the comparison is against an unread baseline.
  Report as NOT_EVALUABLE, not as unsupported.

S4. SIGN HYGIENE
  No term may carry direction in its name. Flag any
  variable whose name asserts a sign (efficiency,
  improvement, optimization, waste). Emit the neutral
  reading alongside: the measured quantity plus its frame.

S5. CLOCK PER LEVEL
  Clocks are collected per row, never collapsed to one
  claim-level clock. If two levels assume different time
  constants, emit BOTH and flag the mismatch. A term whose
  levels disagree on horizon is the finding.

S6. FIXTURES — from today's material
  H1 grid emission factor: downward levels resolve, clock
     at level 0 derivable, upward cells expected ASSERTED
  H2 "more efficiency solves this" as bare claim:
     PASS = NOT_EVALUABLE on S3, not a low score
  H3 tree replacement claim:
     PASS = Y_function_set UNREAD, comparison refused
  H4 a term with two conflicting level clocks:
     PASS = both emitted, mismatch flagged, no pick

S7. CONSTRAINT
  stdlib. No severity language. Reports structure only.
  Absence is first-class throughout: empty value_string,
  UNREAD, ABSENT, NOT_EVALUABLE all emit rather than
  defaulting to a number.
