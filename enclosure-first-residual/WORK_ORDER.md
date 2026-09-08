# WORK ORDER K — enclosure_first_residual.py

Delivered 2026-09-06. Verbatim. Nothing in this file is edited.

---

```
=====================================================
WORK ORDER K — enclosure_first_residual.py
target: Fable / Claude Code
repo:   method-layer? NO → sims repo
        (it models a system; consumes F and G)
deps:   method-layer (F branch_set,
        G envelope/return enum)
        stdlib only, phone-buildable, CC0
=====================================================

PURPOSE
  Invert the intake order for behavior
  attribution. Enter enclosure terms
  FIRST, measure residual, and only
  then treat the residual as a trait
  candidate. Trait is not excluded —
  it is demoted from assumption to
  survivor of a control.

=====================================================
UNIT
=====================================================
  person-window = (person_id, t0, t1)
  NOT person.
  Rationale: the discriminator needs
  the same person under two option
  sets. Person-level units cannot
  see enclosure change and silently
  collapse K into a trait study.

  REQUIRE: >=2 windows per person for
  the within-person arm. Single-window
  persons go to the between arm only
  and are flagged.

=====================================================
ENCLOSURE TERMS (independent)
=====================================================
  option_set_size    int
      exits enumerable from CURRENT
      state
  exit_cost[]        float per exit
      as fraction of resources
      AVAILABLE, not of total
  reachability[]     0/1 per exit
      reachable WITHOUT first exiting
      something else
  reversibility      0/1 per exit
      (from G — can prior state be
      restored)

  derived:
    effective_exits =
      count(reachability==1
            AND exit_cost <= 1.0)

  NOTE: effective_exits is the term
  that carries the hypothesis.
  option_set_size alone is the
  nominal count and will overstate.

=====================================================
BEHAVIOR TERMS (dependent)
=====================================================
  borrowed GRADED forms from the
  animal literature — do not use the
  human label set (rigidity,
  resistance to change, closed-
  minded). Those are closed nodes.

  latency_to_approach_novel   float
  test_phase_present          0/1
  perseveration_rate          float
  arousal_clearance_time      float

  each requires an operationalization
  string in the schema. A term with
  no operationalization = BLOCKED,
  not estimated.

=====================================================
PIPELINE
=====================================================
  1. NULL FIRST (blocking gate)
     shuffle enclosure terms WITHIN
     population, refit, record
     residual distribution.
     Print null residual mean + CI
     BEFORE any real fit.
     If observed residual is inside
     the null band → return
     UNKNOWN_measurable. Do not
     report a trait.

  2. between arm
     behavior ~ enclosure_terms
     across person-windows
     → residual_between

  3. within arm  (the discriminator)
     restrict to persons with
     >=2 windows AND
     |Δeffective_exits| >= threshold
     Δbehavior ~ Δenclosure
     → residual_within

  4. compare
     residual_within << residual_between
        → enclosure account
     residual_within ≈ residual_between
        → trait candidate SURVIVES
          control, report with CI
     residual_within > residual_between
        → confound, likely selection
          into windows; report and
          stop

=====================================================
RETURN TYPE  (from G — enum, peer classes)
=====================================================
  ENCLOSURE_DOMINANT(fraction, CI)
  TRAIT_RESIDUAL(fraction, CI)
  UNKNOWN_measurable(reason)
  BLOCKED(no_within_person_windows)
  BLOCKED(unoperationalized_term)
  OUT_OF_ENVELOPE

  A trait result is a RESULT. So is
  no result. Do not privilege the
  scored return.

=====================================================
ENVELOPE (declared, from G)
=====================================================
  valid when:
    enclosure change is EXOGENOUS to
    the person (policy change, cliff,
    lease end, restoration)
  out of envelope when:
    the person chose the enclosure
    change → reverse causation
    unresolvable, return
    OUT_OF_ENVELOPE

=====================================================
FIRST RUN — cheapest
=====================================================
  natural experiment, published panel
  data, zero collection:
    benefit cliff crossing
    licence suspension / restoration
    lease end / forced move
    plant closure
  criterion: option set jumped in a
  known direction on a known date,
  exogenously.

=====================================================
BRANCH SET (emit to F)
=====================================================
  origin_pattern:
    "behavior attributed to individual
     trait"
  branches:
    enclosure_constraint
    trait_plain
    selection_into_enclosure
    measurement_artifact_of_label_set
  discriminator: within-person
    Δenclosure
  cost: low (published panels)
  status: open
  predicts_elsewhere: animal
    captive-vs-released (different
    domain, same discriminator)
```
