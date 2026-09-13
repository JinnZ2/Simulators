# terrain-prior

An observed indicator -- a plant, a landform, a piece of flow evidence -- is a
record of the process that produced the site.  This reads that record and
returns what must have been true for the indicator to be there, as a PRIOR
with a stated mechanism, a stated confidence, a stated scope and a stated
falsifier.

Built to `WORK_ORDER.md`, landed verbatim.

    python3 terrain_prior.py      # the case set, the choices, the counters
    python3 terrain_prior.py --choices
    python3 test_terrain.py       # the checks; prints its own count

Stdlib only.  No network.  Parses under 3.9.  Phone-buildable.  CC0.

## What it does not do

It does not plan routes and it does not rate terrain.  There is no
traversability number anywhere in the folder and there cannot be one: the two
output variables are reported on two vocabularies that do not compare
(`WITHIN`/`EXCEEDS` against `CLEARS`/`BINDS`), no function reads both tables,
and no arithmetic operator touches either.  All three are asserted.

It is not a species lookup table.  Every entry carries a mechanism, because
the mechanism is what transfers to a region whose species list is different.
An entry without one is UNRATED, fires `P5_NO_MECHANISM`, and produces **no
prior at all** -- not a prior with a flag on it, since a caller reading
`bearing_prior["value"]` would still be acting on a correlation.

## Prior, and rating

The hard constraint *"no terrain rating independent of a morphology profile"*
is met by keeping the two apart:

    PRIOR     a statement about the ground and the process that made it.
              Returned whether or not a morphology is supplied.
    VERDICT   the rating.  Produced only inside by_morphology, only per
              supplied profile, never merged across profiles.

With no morphology supplied the return carries priors and an empty
`by_morphology`, and no verdict key exists in it.

## The case set

    A_boulder        the order's stated validation target.  VERY_LOW bearing,
                     P2_SENSOR_INVERT fires, derived from flow direction plus
                     one obstruction, before contact.
    B_pine           P1_TWO_LAYER; bearing references the substrate, and the
                     duff is named as not being the bearing surface.
    C_split          P3_MORPH_SPLIT; two platforms, opposite bearing results,
                     rows kept.
    D_no_mechanism   P5; no prior on either axis.
    E_out_of_scope   P4; the prior returned, flagged, not suppressed.

Five more observations exist only to show that a branch is reachable:
`F_no_branch` (`NO_CONTEXT_BRANCH`), `G_upstream` (the boulder's other side),
`H_no_entry`, `I_intake` (`INTAKE_INCOMPLETE`), `J_cypress` (no morphology, so
a prior and no verdict), `K_hardwoods`.

## What running it says about the work order

Full detail in `CLAIM_TABLE.md` (`TPR_001..TPR_013`).  The four that matter:

**The order states the validation target's bearing at two different rungs.**
Case A says *"MUST return LOW bearing"*; the order's own derivation text for
the same site says *"Bearing is absent."*  Those disagree for a low-pressure
platform -- `VERY_LOW` supports nothing, `LOW` supports a low-pressure foot --
and `boulder_rung_divergence()` computes which platform the difference
reaches.  `[CHOICE 10]` takes the derivation text; the test asserts the
direction both readings agree on separately from the rung.

**The validation target returns a prior with no falsifier.**  The order:
*"A prior that cannot say what would disprove it is not engineering grade."*
`falsifier_coverage()`: **1 of 6** entries states one, and it is the cattail
entry, the only one the order writes out in full.  None is invented.

**None of the order's eight morphology fields reaches a check.**  Every
verdict rests on two fields this build added under `[CHOICE 2]`, declared and
never derived, because the order supplies no threshold that turns any of its
numbers into a class.  The profile as specified cannot produce a verdict
without one further declaration, and the declaration does all the work.

**The rule that region is not a lookup key leaves a word list as the
vegetation intake.**  `resolve_entry` never names `region` -- asserted by AST
and behaviourally, by re-reading every observation with the region replaced --
and what is left to enter a `VEGETATION` derivation by is the indicator's
name.  A word list is what fails in a region whose species list differs, which
is the failure the rule exists to prevent.  The `LANDFORM` path does not have
it: the boulder entry is reached through context, not through a name, which is
why it is the order's validation target.  Two intake paths, one stated rule,
different standing.

## What is transcribed, what is constructed, what is missing

Transcribed from the order: five derivation entries, every mechanism string in
the order's own words.  A class is marked `ORDER_STATED` only where the order
says it and `DECLARED_READING` where somebody read it into a class -- recorded
per axis under `[CHOICE 9]` so the two never merge.

Constructed and labelled: the two morphology profiles (every number
illustrative), the mechanism-less entry for case D, and every observation.

Missing and not supplied: the order specifies case C on a **bog** and ships no
bog derivation entry.  No bog entry is invented.  Case C runs on cattails and
the substitution is recorded in three places, one of them a test check.

`WORK_ORDER.md` is landed verbatim and carries em dashes.  It is not
transliterated into ASCII; the ASCII rule is a rule about what is built here,
and the test records the delivered document as the exception rather than
editing it into compliance.

## Nothing here is a statement about terrain

`TPR_012`.  No site visited, no indicator observed, no `observer_baseline`
belonging to a person, every morphology number illustrative.  The order says
why in its own Open section: the derivation set has to come from someone with
a long direct baseline, and the priors have never been written in a form
anything can read.  What is built is the shape they would be written into, and
the counters that say how much of the shape is empty.

The order's second Open item -- animal route data and game trails read as a
derivation source -- is not specced there and is not built here.
