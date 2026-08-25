# WORK ORDER 8 — FOLD MATRIX, UPWARD ARM (revised)

Delivered verbatim. Supersedes `WORK_ORDER.md`, which is kept unedited
so both versions stay inspectable — the `declared-frame/` v1-and-v2
arrangement.

**What changed, for a reader diffing the two:**

- **S1a is entirely new.** Stop rules from the document set rather than
  absolutes, `artifact_id` on the upward stop, a downward stop at the
  deepest *quantified* quantity rather than the deepest physical one,
  `unmeasured_span` emitted and not scored, and a `plan_exists` /
  `practice_tracks_plan` column that must never merge into `basis`.
- **S2's `value_string` becomes a fixed format**: three fields —
  `sign`, `magnitude`, `unit` — each independently ABSENT-able, in place
  of one free-text string.

The audit of the revision is in `CLAIM_TABLE.md` (`FM_010..`).

---

WORK ORDER 8 — FOLD MATRIX, UPWARD ARM
Extends the folded-term instrument. Downward arm has a
reading; this specs the upward arm and the grid holding both.

S1. STRUCTURE — one term, one grid, not one number
  Rows = levels indexed from the term outward:
    negative = downward toward substrate
    zero     = term as used
    positive = upward toward stated purpose
  Columns per level:
    severed | still_acting | clock | basis
    basis in {measured, derived, ASSERTED, ABSENT}

S1a. STOP RULES — from the document set, not absolutes
  Upward: highest level with a stated artifact (business
    plan, charter, stated principle). Record artifact_id.
    No artifact -> stop, basis ABSENT.
  Downward: deepest QUANTIFIED quantity — one the org
    computes, not one that physically exists. Joules are
    not the floor unless joules were calculated. Record
    quantity and unit.
  Emit unmeasured_span: their downward stop vs where the
    physical chain continues. Emitted, not scored.
  Separate column, never merged into basis:
    plan_exists | practice_tracks_plan (yes|no|UNREAD)

S2. UPWARD CELLS
  Per positive level, what relation to the goal was claimed
  and how established. ASSERTED and ABSENT predicted
  majority — register before running.
  Mandatory value_string, fixed format, three fields each
  independently ABSENT-able:
    sign      + | - | ABSENT
    magnitude number | ABSENT
    unit      unit of the claimed proxy->goal relation
              | ABSENT
  Empty emits as empty, never as zero.

S3. SCOPE — mandatory on efficiency-class terms
  efficient/optimal/better/faster require with_respect_to,
  boundary, horizon. Any missing -> NOT_EVALUABLE: not
  scored, not ranked, not carried into comparison.
  Replacement claims also require Y_function_set
  (enumerated | PARTIAL | UNREAD). UNREAD -> comparison
  refused, reported as NOT_EVALUABLE not unsupported.

S4. SIGN HYGIENE
  Flag any variable whose name asserts direction
  (efficiency, improvement, waste). Emit neutral reading:
  measured quantity plus frame.

S5. CLOCKS PER LEVEL
  Collected per row, never collapsed. Two levels with
  different time constants -> emit both, flag mismatch,
  no pick. Disagreeing horizons are the finding.

S6. FIXTURES
  H1 grid emission factor — downward resolves, level-0
     clock derivable, upward expected ASSERTED
  H2 "more efficiency solves this" bare
     PASS = NOT_EVALUABLE on S3, not a low score
  H3 tree replacement claim
     PASS = Y_function_set UNREAD, comparison refused
  H4 conflicting level clocks
     PASS = both emitted, flagged, no pick

S7. CONSTRAINT
  stdlib. No severity language. Structure only. Absence
  first-class: empty value_string, UNREAD, ABSENT,
  NOT_EVALUABLE all emit rather than defaulting to a number.
