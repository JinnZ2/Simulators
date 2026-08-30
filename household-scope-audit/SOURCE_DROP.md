# Gap: family-functioning instruments have no field for conditions outside the household

Study design. Arm 1 requires no new data collection — it audits existing
published instruments. Arm 2 validates against data that already exists.

CC0. No rights reserved.

## The gap

Dysfunction is diagnosed at the level it is OBSERVED. For families, that is
the household. Every widely used instrument is scoped to that unit:

    family functioning scales
    parenting-capacity assessments
    clinical intake and family-systems formulations
    child-welfare risk and safety instruments

Conditions imposed from OUTSIDE the household — employment structure, shift
scheduling, housing instability, benefit cliffs, medical debt, transport
access, incarceration exposure, utility shutoff policy — are, in most of these
instruments, either absent, or present only as an attribute OF the caregiver.

Where the variable is absent, an externally caused state has nowhere to land
except on the persons measured. This is a representational limit, not a
scoring error, and it produces misattribution BY CONSTRUCTION rather than by
oversight.

    ask what the instrument cannot represent

Same instrument logic as a null-rate measure: a system with no slot for
absence emits a positive reading regardless of input.

## Arm 1 — instrument audit (no new data)

Corpus: published family-functioning, parenting-capacity, and child-welfare
risk instruments, plus their scoring manuals. Include instruments in active
statutory use, not only research scales.

For each ITEM in each instrument, code:

    LOCUS
      P   property of a person (trait, skill, attitude, capacity)
      H   property of household interaction
      E   property of conditions outside the household
      X   external condition coded AS a personal property
          (e.g. "fails to provide stable housing" — a housing-market
           variable recorded as a caregiver attribute)

    DIRECTIONALITY
      does any item permit an external cause to EXPLAIN a household
      observation, or only to co-occur with it

    ACTIONABILITY TARGET
      what does a poor score direct intervention at
        person / household / external condition

    ATTENUATION
      does the manual instruct the scorer to discount an item when a
      stated external condition accounts for it — and is that
      instruction mandatory or discretionary

    PRIMARY OUTCOME
      E-fraction   = E items / total items
      X-fraction   = X items / total items
      attenuation coverage = fraction of P and H items with a mandatory
                             external-cause attenuation rule

    PREDICTION  E-fraction near zero across instruments
                X-fraction substantially above zero
                attenuation rules discretionary where they exist at all

If E-fraction is materially non-zero and attenuation is mandatory, the gap is
not real and the claim should be retracted.

## Arm 2 — misattribution under matched conditions

Tests whether the representational limit produces misattribution in scoring,
using vignettes rather than new fieldwork.

    DESIGN   2 x 2, between-scorer
             household observation: identical in all conditions
             stated external condition: absent / present and severe
             instrument used: one high-E-fraction, one near-zero

    SCORERS  practitioners who use the instrument, and a lay comparison
             group. Same vignettes.

    MEASURES
      score difference by external-condition presence, per instrument
      free-text attribution coding: personal / household / external
      recommended action target
      whether the scorer volunteers the external condition unprompted

    PREDICTION  near-zero-E instrument: score does not move when the
                external condition is stated, and free-text attribution
                stays on the person
                high-E instrument: score moves, attribution shifts

The interesting cell is a practitioner who NAMES the external condition in
free text and still scores the person as deficient. That dissociation shows
the constraint is in the instrument, not in practitioner judgment — which is
the whole claim.

## Arm 3, optional — administrative validation

Where already-collected records permit:

    link case-level assessment scores to external conditions measurable
    independently of the assessment (documented shift schedule, eviction
    filing, benefit termination date, utility shutoff, distance to
    services)

    MEASURE  fraction of variance in assessment score attributable to
             independently measured external conditions

    PREDICTION  substantial. Every unit of that variance is currently
                recorded as a property of the family.

## Confounds

    PRACTITIONER COMPENSATION
      experienced practitioners often correct for external conditions
      informally, off the instrument. That improves outcomes and HIDES
      the gap. Measure it directly (free-text vs score divergence)
      rather than treating it as noise — it is evidence the instrument
      is being worked around.

    STATUTORY CONSTRAINT
      some scorers cannot act on external conditions even when they see
      them, because the mandate is scoped to the household. Record
      mandate scope separately from instrument scope; they are different
      limits with the same effect.

    SELECTION INTO ASSESSMENT
      families reach assessment through referral pathways already
      correlated with external conditions. Do not read prevalence off
      an assessed sample.

    REVERSE CAUSATION
      household dysfunction can produce external conditions (job loss,
      housing loss). The audit arm is unaffected — it measures
      representational capacity, not causal share. Arm 3 is affected and
      needs temporal ordering.

    CONSTRUCT DRIFT
      "functioning" is defined differently across instruments. Report
      per-instrument, never pooled.

## What this is not

Not a claim that household-level variables are unimportant, or that no family
has internally generated dysfunction.

Not a claim of intent. Incentive direction and cost asymmetry are sufficient:
instruments are cheaper to build on what the assessor can observe in a
household visit, and interventions are cheaper to fund at the household than
at the structural level. No author required and none posited.

The claim is only that an instrument with no field for a variable will assign
that variable's effects to whatever fields it does have.

## Ask

Run Arm 1. It needs a reading room and a coding scheme, nothing else. Publish
the E-fraction, X-fraction, and attenuation coverage per instrument, with the
items you could not classify marked unclassified rather than forced.
