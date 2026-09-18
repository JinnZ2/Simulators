# WORK ORDER M — REVISION 2, delivered verbatim

Delivered 2026-09-17, after rev 1 (`WORK_ORDER.md`) was built and run.
Landed beside v1 per the repo's supersession convention; nothing below
this line is edited. The build is `revision_survival.py` + `draw_frame.py`;
the audit is `CLAIM_TABLE.md` (`RS_017..`).

---

DISPATCH — WORK ORDER M, revision_survival
REVISION 2 (defect-driven)
target: Claude Code
license: CC0, stdlib only, single repo
context: rev 1 was built and run. Four spec defects
         found by execution. This packet fixes them.
         Do not re-derive the order — patch it.


D-C1  SEED LIST FAILS ITS OWN ADMISSION RULE

  five rev-1 seeds were reversed or nonexistent
  before Y=2005 (ulcer, HRT, arsenic life, knee
  arthroscopy, CRASH). List was selected on
  memorable-reversal. Keep them out.

  REPLACE recall-drawn seeding with a declared
  draw frame:

    1. fix one Y-vintage indexed source
       (textbook edition / guideline set /
        Cochrane review index as of 2005).
       Record source, edition, index size.
    2. draw rows BY POSITION (seeded RNG, seed
       recorded), not by topic recall
    3. adjudicate fate AFTER the draw, by a rule
       written before it
    4. frame bias is then declarable; recall bias
       never is

  implement: draw_frame.py
    inputs  source_id, index_size, rng_seed, n
    outputs positions[], and a frame_declaration
            block written to the run record
    HARD GATE: Arm A refuses to score if
    frame_declaration is absent or if any row
    entered outside the draw

  the 7 admissible rev-1 seeds ship as
  CANDIDATE only, excluded from scoring, retained
  as a hand-built comparison set. Two of them
  (alpha wolf, junk DNA) additionally need a
  POPULAR-vs-SPECIALIST split field: both were
  repudiated in the specialist literature before Y
  and not in circulation. Add field
  established_where ∈ {specialist, popular, both}
  and score only both/specialist rows.


D-C2  ARM C ENUM MISSING ITS WORST CELL

  rev 1: RECOVERABLE | COSTLY | TERMINAL
  presupposes a substitution decision exists.

  ADD, and it is not below TERMINAL on severity:
    NO_SUBSTITUTION_EXISTS
      the BRC row has no known engineering
      pathway; there is no decision to reverse
      because none was ever available

  TERMINAL  = decision made, irreversible
  NO_SUB    = function stops, no decision existed

  implement: separate the two axes in the output.
  Do NOT rank them on one scale.
    axis_1  decision_reversibility
            {recoverable, costly, terminal, n/a}
    axis_2  pathway_exists {yes, partial, none}

  and add a completeness assertion to the test
  suite: every enum in the repo must be derivable
  from the measurand's possible outcomes, with
  that derivation written next to it. This defect
  class (severity ranking whose worst cell is
  absent) reads as complete from inside — every
  row classes, nothing errors.


D-C3  THRESHOLDS CARRY NO TOLERANCE

  Δ < 0.15 refused at -0.15000000000000002.
  Spec defect, not implementation.

  patch: every numeric threshold in the order
  gets an explicit comparison rule.
    LEAK_GATE      abs(delta) < 0.15 + 1e-9
    OVERCONF_GATE  (mean_conf - acc) > 0.20 - 1e-9
    SURVIVED_FLOOR frac >= 0.40 - 1e-9

  add a repo-wide test: no bare float comparison
  against a decimal literal. Fail the suite on one.


D-C4  Q_mech SPLIT + SAMPLE-SIZE REQUIREMENT

  on SURVIVED rows the key mechanism is
  NONE_GIVEN → Q_mech collinear with Q_label.
  Informative subset = revised rows only.

  report acc_mech_revised SEPARATELY. Never
  report a pooled Q_mech.

  and state the tension rev 1 omitted:
    D1's 40% SURVIVED floor and the informative
    subset pull opposite ways
  → requirement is on the REVISED subset, not on N
  → set n_revised_min = 24, and size N from it:
    N >= n_revised_min / (1 - survived_frac)
  → refuse to score acc_mech_revised below the floor;
    return INSUFFICIENT_REVISED, not a number


RETURN ENUM — add two states

  VOID_KEY_HOLDER   one party on key and responses.
                    Correct outcome for a self-run;
                    report as VOID, never as a score.
  INSUFFICIENT_REVISED  n_revised < floor


RUN RECORD — required fields, refuse to emit
without them

  frame_declaration (source, edition, seed, n)
  delta_open_blind
  acc_label, acc_mech_revised, n_revised
  arm_c table on both axes
  defect log: spec defects and implementation
    defects in SEPARATE columns
  key_holder, respondent — and whether they differ


README FRAMING — one paragraph, and it matters

  rev 1 produced no calibration number. It
  produced four spec defects, found by building,
  three of them in the order's own authoring.
  That is the run doing what it was for.
  A reader seeing VOID plus a defect list and no
  score should not file this as a failed attempt.
  State that at the top, not in a footnote.


DO NOT

  - do not re-populate seeds from model recall,
    including your own, at any point
  - do not pool Q_mech
  - do not rank NO_SUBSTITUTION_EXISTS against
    TERMINAL
  - do not score a self-run
