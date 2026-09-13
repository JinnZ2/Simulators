# WORK ORDER — terrain_prior.py

CC0. Stdlib only. No network. No ML. Phone-buildable.

## What it does

Takes an observed indicator — vegetation type, landform feature, flow
evidence — and returns what must have been true for that indicator to be
there, expressed as a substrate prior with stated confidence and stated
scope.

It does NOT plan routes. It does NOT rate terrain. It produces a PRIOR that a
planner or a probe can then test, and it records what the prior was derived
from so the derivation can be checked when it turns out wrong.

## Why it is a different class of instrument

Existing legged-robot traversability work is REACTIVE and POINT-SAMPLED. It
probes the ground with a force sensor on arrival, or detects slip and
entanglement proprioceptively and recovers. Both know only once the robot is
already there.

Vegetation and landform integrate over YEARS. Water table, drainage, soil
type, disturbance history — the variables that determine bearing and
entanglement — are invisible to a single-timepoint sensor and are written
into what grows and into what the water did. The indicator is not an
obstacle. It is a RECORD OF THE PROCESS THAT PRODUCED THE SITE.

Current pipelines classify vegetation as an obstacle class only, which asks
"what will this impede" and never "what does this indicate."

## Critical: this is not a species lookup table

The instrument stores DERIVATIONS, not correlations. Each entry must carry
the mechanism — what has to be true for this to be here — because the
mechanism is what transfers to a region whose species list is different.

A correlation table trained on one biome fails silently in another. A
derivation fails loudly, because the mechanism can be checked against the
site.

## Two output variables, never collapsed

The measurand is NOT "traversability." Traversability is not a property of
terrain. It is a relation between a specific morphology and a specific
substrate, and rating the ground alone is the defect this instrument exists
to remove.

    BEARING       what the ground will support, expressed as pressure over
                  contact area, NOT as pass/fail
    ENTANGLEMENT  what the vegetation will do to a limb swept through it,
                  as a function of limb geometry

These are independent and can point opposite directions. Bog: low bearing,
low entanglement. Cattail stand: low bearing AND high entanglement. Dense low
brush over hardpan: high bearing, high entanglement.

Collapsing them to one score destroys the only information a planner can act
on.

## Intake

    observation = {
      "obs_id": str,

      "indicator_type": "VEGETATION" | "LANDFORM" | "FLOW_EVIDENCE"
                      | "SUBSTRATE_VISIBLE",
      "indicator": str,            # free text as observed, not normalised

      "context": {                 # all optional, all improve the prior
         "flow_direction_known": bool,
         "position_relative_to_obstruction": "UPSTREAM" | "DOWNSTREAM"
                                           | "LATERAL" | "NONE" | "UNKNOWN",
         "season": str,
         "recent_precipitation": str,
         "slope": float
      },

      "region": str,               # scope field, NOT a lookup key
      "observer_baseline": str     # who holds the prior, over what period
    }

## Morphology profile — supplied separately, per platform

    morphology = {
      "platform_id": str,
      "contact_area": float,          # per foot
      "contact_pressure": float,      # mass distributed over contacts
      "n_contacts": int,
      "swing_profile": str,           # what the limb sweeps through
      "joint_exposure": [str],        # which joints are catchable
      "ankle_to_foot_ratio": float,   # governs how vegetation binds
      "recovery_from_entanglement": "PASSIVE" | "ACTIVE" | "NONE"
    }

The SAME observation returns different ratings for different morphologies. A
high-pressure small-contact foot and a low-pressure broad-contact foot get
opposite bearing results on the same bog. Neither is the terrain's property.

## Derivation entries — the content of the instrument

Each entry has this shape. Mechanism is mandatory.

    {
      "indicator": "cattails",
      "mechanism": "obligate of saturated or standing shallow water; root
                    mat over unconsolidated saturated sediment",
      "implies_bearing": "LOW, and lower than the surface mat suggests",
      "implies_entanglement": "HIGH — dense flexible stems at limb height,
                               bind when displaced",
      "two_layer": True,
      "confidence": "HIGH",
      "scope": "temperate wetland margins",
      "falsified_by": "cattails on a drained or filled site; mat over hardpan"
    }

Seed entries, each with its mechanism stated:

- PINE STAND — litter and duff over root structure; surface soft, substrate
  typically firm. TWO-LAYER: a sensor reading the top layer gets the bearing
  exactly backwards. This is the case that breaks naive probing.
- CYPRESS — standing or seasonally standing water, buttressed roots,
  irregular contact geometry. A different environment entirely from pine
  despite both being "trees" to a classifier.
- FIRM MATURE HARDWOODS — sustained drainage over the tree's lifetime;
  bearing inferable from the fact the tree is standing.
- CATTAILS / REEDS — as above. Entrapment layer.
- DOWNSTREAM OF A BOULDER IN A DRY STREAMBED — the load-bearing landform
  case. The obstruction sorted the sediment; the deposition zone behind it is
  fines dropped from slowed water, poorly consolidated. The surface reads
  SMOOTHER AND FINER than the scoured side, so every existing sensor rates it
  BETTER. Bearing is absent. Derivable from flow direction plus one
  obstruction, before contact.

The boulder case is the validation target for the whole instrument: a prior
that is correct, derivable from process, opposite to what the sensors say,
and available before arrival.

## Checks

    P1_TWO_LAYER      indicator implies surface and substrate differ; flag
                      that a surface-only reading will invert
    P2_SENSOR_INVERT  indicator implies the standard sensor suite will rate
                      this BETTER than it is (the dangerous class)
    P3_MORPH_SPLIT    bearing result differs in DIRECTION across two supplied
                      morphology profiles; report both, never merge
    P4_OUT_OF_SCOPE   observation region not in entry scope; return the prior
                      with scope mismatch flagged, NOT suppressed
    P5_NO_MECHANISM   entry lacks a mechanism; entry is UNRATED and must not
                      generate a prior

## Return

    {
      "obs_id": str,
      "bearing_prior":      {"value": str, "confidence": str, "mechanism": str},
      "entanglement_prior": {"value": str, "confidence": str, "mechanism": str},
      "flags": [check codes],
      "scope": str,
      "derived_from": str,
      "falsified_by": str
    }

`falsified_by` is returned with every prior. A prior that cannot say what
would disprove it is not engineering grade.

## Validation cases

A — BOULDER, DRY STREAMBED. flow_direction_known True, position DOWNSTREAM.
→ MUST return LOW bearing AND fire P2_SENSOR_INVERT. If it does not flag the
sensor inversion, the instrument has no advantage over the existing suite.

B — PINE STAND. → MUST fire P1_TWO_LAYER and return bearing referencing the
substrate, not the duff.

C — MORPHOLOGY SPLIT. Same bog observation, two profiles: high-pressure small
contact, and low-pressure broad contact.
→ MUST return opposite bearing results and fire P3_MORPH_SPLIT. If it returns
one answer, it has reverted to rating the terrain.

D — FALSIFIER, NO MECHANISM. Entry with indicator and implication but no
mechanism field.
→ MUST fire P5 and return NO prior. If a correlation without a mechanism can
produce a prior, the instrument is a lookup table and will fail silently
outside its source biome.

E — OUT OF SCOPE. Indicator observed outside the entry's stated scope.
→ MUST return the prior WITH P4 flagged, not suppress it. Suppression
destroys the only signal available; an unscoped prior honestly labelled is
usable, a missing one is not.

## Hard constraints

- No entry without a mechanism.
- No single traversability score, ever. Two variables out, always.
- No terrain rating independent of a morphology profile.
- Region is a scope field, never a lookup key — the mechanism transfers, the
  species list does not.
- observer_baseline is carried verbatim. The prior belongs to whoever holds
  it and over what period, and that provenance travels with it.

## Open

- The derivation set has to come from someone with a long direct baseline.
  Same problem as unpriced productivity in a new domain: the people holding
  these priors are the least represented in text, and the priors have never
  been written in a form anything can read.
- Animal route data is the same record in another format. Game trails are the
  answer to the question this instrument asks, already computed over
  whole-population multi-year sampling, encoded as route rather than as data.
  Reading trails as a derivation source is a second intake path, not specced
  here.
