# FABLE WORK ORDER 3
# provision typing audit + three evidence pulls
# effective-date: forward-only. no prior DBK id re-rated.

────────────────────────────────────────────────────────
STANDING CONSTRAINT (carried from WO1/WO2, DBK_014)
────────────────────────────────────────────────────────
Fable is same-builder with the ordering instance. no return from
this work order is P3-verified. all returns are SAME-NODE
computations. nothing may be labeled "verified" or "P3-passed."
findings dated, claims appended, no prior id re-rated.
REFUSED-BY-§3 is a valid return for any task that cannot be made
self-verifying without an author decision — do not substitute a
preference to complete it.

────────────────────────────────────────────────────────
GOVERNING FRAME FOR THIS ORDER  (the typing rule)
────────────────────────────────────────────────────────
a provision stated as a CHOICE has no falsifier and cannot be part
of a design basis. a human construct is not exempt from the
scientific method. every allowable value in every engineering code
is back-derived from a failure. a design height is not adopted; it
is a load with a wave behind it.

  SCHEMA framing            PHYSICS framing
    "which reading"           "what does it do under load"
    resolved by authority     resolved by failure
    no falsifier              falsifier = the collapse

TWO CLASSES a provision can be:
  DERIVED      names the failure case it is back-derived from.
  PROVISIONAL  names the derivation PATH and is marked pending
               until that path returns data.
a provision that is NEITHER is an assumption wearing a number.

────────────────────────────────────────────────────────
TASK 1 — PROVISION TYPING AUDIT  (the document-level finding)
────────────────────────────────────────────────────────
run across EVERY provision in both delivered artifacts:
  ai_infrastructure_design_basis.md  (P1–P8)
  design_basis_R2_outline.md         (P0.1–P0.5, AX1–AX4, §5–§7)

for each provision emit a row:

  provision_id | class | failure_case_or_path | verdict

  class ∈ {DERIVED, PROVISIONAL, ASSUMPTION}
  DERIVED       → failure_case names a specific incident already
                  cited in the doc or its sibling seed table
  PROVISIONAL   → failure_case_or_path names the study/read that
                  would derive it, AND the doc marks it pending
  ASSUMPTION    → neither present  → THIS IS A KILL, publish it

scoring is TEXTUAL and checkable: a provision is DERIVED only if
the incident id/name is findable in the delivered files or the
seed table. do not credit an incident that lives only in this
work order (the DBK_027 phantom-colophon error — do not repeat it).

deliverable 1:
  - the full provision × class table
  - count of ASSUMPTION-class provisions (the audit's headline)
  - for each ASSUMPTION, the one-line statement it should carry
    instead ("PROVISIONAL, pending <path>") — spec text only,
    not an edit to the files

────────────────────────────────────────────────────────
TASK 2 — B FORK RESOLUTION  (cheap read, governing load case)
────────────────────────────────────────────────────────
from DBK_027: seed letter B predates the B1/B2 split. two branches
were reported and not resolved. this task RESOLVES by reading, not
choosing.

read:
  a) the sibling seed table's B row — what incident does it cite?
  b) R1 §1 and the design basis body — does B2 (the governing load
     for the AI application) appear anywhere as a SEEDED case
     (incident behind it), or ONLY as DERIVED reasoning from the
     737 MAX / MCAS / AOA-disagree logic?

emit the finding:
  branch 1 CONFIRMED  → B1 and B2 both inherit East Palestine;
                        report the SECOND shared node in provenance
                        (East Palestine spanning two info loads),
                        and run the harness dissent_alarm on it the
                        way DBK_027 ran it on E∩F.
  branch 2 CONFIRMED  → B2 rests on NO seed incident. it is a
                        DERIVED provision (from MCAS logic), not a
                        SEEDED one. that is not a defect IF the doc
                        states it — a derived provision is legal.
                        the KILL is only if the provenance section
                        currently IMPLIES a source B2 does not have.
                        check the provenance/custody text and report
                        whether it over-claims a source for B2.

this is a read. the incident either is in the text or it is not.
no author decision. if the text is genuinely ambiguous between
branches, return REFUSED-BY-§3 and quote the ambiguous lines.

deliverable 2:
  - which branch, with the quoted seed-table B row and the R1 §1
    lines that settle it
  - if branch 1: the dissent_alarm result on East Palestine∩(B1,B2)
  - if branch 2: verbatim whether the provenance section claims a
    source for B2, and the exact text if so

────────────────────────────────────────────────────────
TASK 3 — T4 RE-TYPED AS SURVIVAL, NOT TEXT  (DBK_029 follow-on)
────────────────────────────────────────────────────────
DBK_029 framed accounting-selection as "which text governs." re-type
it as physics: retention N_eff is a SURVIVAL COUNT under a loss
event, not a reading of a sentence.

for each of the five consistent accountings + the inexpressible row:
  state the LOSS EVENT that would adjudicate it —
    "provider-only retention, N_eff drops to 2" is a HYPOTHESIS.
    the test is: provider deletes / fails / reprices → is the
    record recoverable from a disjoint hold? count survivors.

do NOT run loss data (none is attached and inventing it repeats
DBK_027). instead:
  - convert each accounting to a falsifiable statement of the form
    "under loss event L, N_eff surviving copies = k"
  - identify which accountings are DISTINGUISHABLE by an observable
    loss event and which collapse to the same observable (if two
    accountings predict identical survivor counts under every loss
    event, they are the same physical claim in two texts — report
    that)
  - the inexpressible row: state explicitly that it is an
    OUT-OF-RANGE sensor reading (DBK_011 reporting its own
    envelope), not a missing value. an out-of-range reading is
    data about the instrument.

deliverable 3:
  - each accounting as a loss-adjudicable statement
  - the distinguishability partition (which accountings any real
    loss event could tell apart)
  - the inexpressible row typed as envelope-report, with the
    loss event under which the inherited metric goes out of range

────────────────────────────────────────────────────────
NOT ASKED (out of scope, flagged not resolved)
────────────────────────────────────────────────────────
- T1 pin t: NOT in this order. t is a LOAD derived from the
  exposure sample (effective_redundancy_test), not a value to
  select. it stays PROVISIONAL until that study returns. do not
  pin it here.
- different-builder verifier: standing DBK_014 gap, uncloseable
  by Fable. do not attempt.
- edits to committed files: none. spec text and findings only.
- the ordering probe (hands repo): NOT Fable's — same-builder
  shares the prior being measured. do not touch.

────────────────────────────────────────────────────────
RETURN FORMAT
────────────────────────────────────────────────────────
same as WO2: all checks green or reported, findings dated, claims
appended DBK_030.. with no prior id re-rated, REFUSED-BY-§3 where
an author decision is required. same-node throughout; nothing
labeled verified.
