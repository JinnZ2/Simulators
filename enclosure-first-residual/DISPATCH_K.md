# DISPATCH K -- enclosure_first_residual (re-issue)

Received 2026-09-23. Verbatim. Nothing in this file is edited. The original
order it re-issues is `WORK_ORDER.md` (delivered 2026-09-06); both are kept
so the deltas are inspectable. The check-first report and the deltas are in
`CLAIM_TABLE.md` (`EFR_010..EFR_012`).

---

```
═══════════════════════════════════════════
DISPATCH K — enclosure_first_residual
TARGET: Claude Code
REPO: JinnZ2/Simulators, folder enclosure-first-residual/
stdlib only, CC0, phone-buildable
BUILD ON CONSTRUCTED DATA. Real run NOT_RUN.
═══════════════════════════════════════════

CHECK FIRST (report before building)
  method-layer: does F (branch_set) exist? path.
  method-layer: does G (envelope / return enum) exist?
    absent → define the return enum locally in this
    folder, mark G_ABSENT in README. Do not build G.

UNIT
  person-window = (person_id, t0, t1), NOT person.
  within arm REQUIRES >=2 windows per person.
  single-window persons → between arm only, flagged.
  no repeated windows in dataset → BLOCKED, never fall
  back to between-only (it would become the study it
  replaces).

ENCLOSURE TERMS (independent)
  option_set_size   int    exits enumerable from CURRENT state
  exit_cost[]       float  fraction of resources AVAILABLE, not total
  reachability[]    0/1    reachable without first exiting another
  reversibility[]   0/1    prior state restorable
  effective_exits = count(reachability==1 AND exit_cost<=1.0)
  option_set_size is nominal and overstates; effective_exits
  carries the hypothesis.

BEHAVIOR TERMS (dependent) — graded, animal-literature forms
  latency_to_approach_novel   float
  test_phase_present          0/1
  perseveration_rate          float
  arousal_clearance_time      float
  each REQUIRES an operationalization string in schema.
  missing string → BLOCKED(unoperationalized_term), not estimated.
  DO NOT use human labels (rigidity, resistance to change,
  closed-minded) — closed nodes.

PIPELINE
  1 NULL FIRST, blocking: shuffle enclosure terms within
    population, refit, print null residual mean + CI BEFORE
    any real fit. observed inside band → UNKNOWN_measurable.
  2 between arm: behavior ~ enclosure → residual_between
  3 within arm: persons >=2 windows AND |Δeffective_exits| >=
    threshold (threshold in data file, provenance chained):
    Δbehavior ~ Δenclosure → residual_within
  4 compare:
    within << between  → ENCLOSURE_DOMINANT
    within ≈ between   → TRAIT_RESIDUAL survives control, with CI
    within > between   → selection into windows; report, stop

ENVELOPE
  valid: enclosure change EXOGENOUS (policy change, benefit
    cliff, lease end, licence suspension/restoration, plant
    closure)
  person chose the change → OUT_OF_ENVELOPE

RETURN (peer classes, none privileged)
  ENCLOSURE_DOMINANT(fraction, CI)
  TRAIT_RESIDUAL(fraction, CI)
  UNKNOWN_measurable(reason)
  BLOCKED(no_within_person_windows)
  BLOCKED(unoperationalized_term)
  OUT_OF_ENVELOPE

CONSTRUCTED FIXTURES (all four required, planted faults must fire)
  F1 enclosure-driven world    → ENCLOSURE_DOMINANT
  F2 trait-driven world        → TRAIT_RESIDUAL
  F3 selection-into-windows    → within > between, stop
  F4 no operationalization     → BLOCKED

REAL-RUN SPEC (write into README, do not run)
  target: published panel with exogenous option-set jump on a
  known date AND >=2 windows/person AND >=1 graded behavior term.
  EXPECTED: most panels carry enclosure but not behavior →
  BLOCKED(unoperationalized_term). Record which panels checked.
  panel survey is UNRUN — list it as the open item.

BRANCH SET (emit to F if present)
  origin: "behavior attributed to individual trait"
  branches: enclosure_constraint / trait_plain /
    selection_into_enclosure / measurement_artifact_of_label_set
  discriminator: within-person Δenclosure
  predicts_elsewhere: animal captive-vs-released

DELIVERY
  claim table, permanent IDs, falsifier per claim
  contamination declared before numbers (fixtures are
  implementation-authored → REGRESSION, not validation)
  refusal states typed, not errors
═══════════════════════════════════════════
```
