# CLAIM TABLE -- terrain-prior

Claims are `TPR_*`.  `TP_` is taken by `triad-playground/`.

These are claims about the instrument and about the work order it was built
to.  None of them is a claim about terrain, about any site, or about what any
platform would do on any ground.  `TPR_012` is why.

Every claim below is checked by `python3 test_terrain.py` unless it says
otherwise.

---

## TPR_001 -- the order states the validation target's bearing at two rungs

Validation case A: *"MUST return LOW bearing"*.  The order's own derivation
text for the same site: *"Bearing is absent."*

On an ordinal ladder those are different rungs, and the difference is not
cosmetic: `VERY_LOW` supports no platform, `LOW` supports a low-pressure one.
`boulder_rung_divergence()` computes where they part -- **one platform of two,
the broad-contact low-pressure one, where VERY_LOW gives EXCEEDS and LOW gives
WITHIN.**

`[CHOICE 10]` enters the entry at `VERY_LOW`, from the derivation text, because
the derivation text is the derivation and the validation case is a statement
about direction.  The disagreement is computed rather than resolved quietly,
and the test asserts the direction both readings agree on (below `MODERATE`)
separately from the rung this build picked.

STATUS: SUPPORTED, computed.

---

## TPR_002 -- the stated validation target returns a prior with no falsifier

The order: *"`falsified_by` is returned with every prior.  A prior that cannot
say what would disprove it is not engineering grade."*

`falsifier_coverage()` over the order's own seed set: **1 stated of 6.**  The
one is the cattail entry, which is the only entry the order writes out in
full.  The boulder -- *"the validation target for the whole instrument"* --
states none, and none is invented here.

So by the order's own sentence, the prior the instrument is validated on is
not engineering grade.  That is a gap in the derivation set, not in the code:
the code returns the field, empty, and counts it.

STATUS: SUPPORTED, counted.

---

## TPR_003 -- the axis the order protects is the axis its seed set does not fill

The order is emphatic that bearing and entanglement must never be collapsed.
`class_coverage()` over the seed set:

* entanglement unstated on **4 of 6** entries
* entanglement `LOW` reached by **no** entry
* entanglement `MODERATE` reached by exactly one entry -- the mechanism-less
  one, which by `P5` can never produce a prior at all

The second output variable exists in one entry of the order's five.  Nothing
is imputed; the counts are the finding.

STATUS: SUPPORTED, counted.

---

## TPR_004 -- P3 is specified on bearing only, and case C splits on both axes

`P3_MORPH_SPLIT`: *"bearing result differs in DIRECTION across two supplied
morphology profiles"*.

On validation case C the entanglement verdicts also differ in direction --
`BINDS` on the high-susceptibility platform, `CLEARS` on the low one -- and
**nothing fires**.  `entanglement_split_has_no_check()` reports it.

Not repaired.  Adding a sixth check would be adding a check the order does not
have, and the order's five are the object under test.

STATUS: SUPPORTED, computed.

---

## TPR_005 -- the validation target's prior is context-conditioned and the entry schema has no field for it

A boulder's upstream side is scoured and its downstream side is fines.  The
prior is different on the two sides of one indicator.  The order's entry
schema has one `implies_bearing` field.

`[CHOICE 4]` adds `context_branches`, each with a `when` dict of context keys
that must all match.  **An entry with branches and no matching branch returns
NO prior**, with reason `NO_CONTEXT_BRANCH`, rather than falling back to an
unconditioned reading -- a fallback would return the scoured-side answer for
the deposition side, which is precisely the error the case exists to catch.

STATUS: SUPPORTED.

---

## TPR_006 -- none of the order's eight morphology fields reaches a check

The order specifies `contact_area`, `contact_pressure`, `n_contacts`,
`swing_profile`, `joint_exposure`, `ankle_to_foot_ratio` and
`recovery_from_entanglement`, plus `platform_id`.
`morphology_fields_reaching_a_check()` returns **0 of 8**.

Every verdict in this module rests on two fields this build ADDED under
`[CHOICE 2]`: `pressure_class` and `entanglement_susceptibility`.  They are
declared, never derived, because the order supplies no threshold that turns
any of its numbers into a class, and an invented kPa threshold would put a
number nobody measured inside a bearing verdict.

Stated precisely: **the morphology profile as the order specifies it cannot
produce a verdict without one further declaration, and the declaration is
doing all the work.**  That is a statement about this build, not about whether
the order's fields matter.  An AST check asserts no function derives anything
from any of the seven numeric or descriptive fields.

STATUS: SUPPORTED, computed and asserted.

---

## TPR_007 -- validation case C names a bog and the order ships no bog entry

Case C: *"Same bog observation, two profiles."*  There is no bog derivation
entry in the order's seed list.

No bog entry is invented.  Case C is run on the cattail entry -- the order's
own low-bearing high-entanglement case -- and the substitution is recorded in
`cases.py`, in the README, and in a test check asserting no entry in the set
is a bog.

STATUS: SUPPORTED, recorded not repaired.

---

## TPR_008 -- the rule that region is not a lookup key leaves a word list as the vegetation intake

Hard constraint: *"Region is a scope field, never a lookup key -- the
mechanism transfers, the species list does not."*  `resolve_entry` obeys it:
an AST check asserts the function never names `region`, and a behavioural
check re-reads every observation with the region replaced and asserts the
entry does not move.

The cost: what is left to enter a `VEGETATION` derivation by is the
indicator's NAME, matched on words.  A word list is exactly what fails in a
region whose species list differs -- the failure the rule exists to prevent,
arriving one layer down in the intake.

The `LANDFORM` path does not have this problem.  The boulder entry is reached
through context -- flow direction plus one obstruction -- not through a name,
and that is why it is the order's validation target.  **Two intake paths with
different epistemic standing under one stated rule**, and only one of them
transfers the way the rule says it should.

STATUS: SUPPORTED, stated at the callsite and in the module docstring.

---

## TPR_009 -- two-layer does not imply the dangerous direction, and pine proves it

`P1_TWO_LAYER` and `P2_SENSOR_INVERT` are different checks and it would be
easy to collapse them.  The order's own seed set separates them:

* PINE -- soft duff over firm substrate.  Two-layer, and the surface reading
  is WORSE than the ground.  `PESSIMISTIC`.
* CATTAILS -- *"LOW, and lower than the surface mat suggests"*.  Two-layer,
  and the surface reading is BETTER than the ground.  `OPTIMISTIC`.

Only the second is the dangerous class.  `P1` fires on pine and `P2` does not,
asserted in both directions.

STATUS: SUPPORTED.

---

## TPR_010 -- a prior is not a rating, and that is how the morphology constraint is met

Hard constraint: *"No terrain rating independent of a morphology profile."*

A PRIOR is a statement about the ground and the process that made it, and is
returned whether or not a morphology is supplied.  A VERDICT is the rating,
and appears only inside `by_morphology`, only per supplied profile.  With no
morphology the return carries priors and an empty `by_morphology` and no
verdict key exists anywhere in it -- asserted.

Nothing merges the rows.  `P3` fires when they disagree and the rows stay.

STATUS: SUPPORTED.

---

## TPR_011 -- no metric is registered in tools/known_answer.py, and here is why

The standing rule in this tree is that no metric ships without a known-answer
run.  Nothing here is registered, and the reason is stated rather than left as
a silent absence:

* `bearing_verdict` and `entanglement_verdict` return declared vocabulary
  members from a membership test against a declared table.  Their known answer
  is the table, and the table is eleven lines of data in the module.
* `falsifier_coverage` and `class_coverage` are counts over the derivation
  set.  Their known answer is the set, and the test asserts the counts
  directly.
* `read` returns a record.

There is no continuous quantity anywhere in the folder, and nothing is
averaged, summed, ranked or ordered -- asserted by AST.

STATUS: SUPPORTED, with the reason stated.

---

## TPR_012 -- UNVERIFIED: nothing here has been checked against a site

No site has been visited.  No indicator has been observed.  No
`observer_baseline` in this folder belongs to a person -- every one reads
`CONSTRUCTED: no person holds this prior and no period is claimed`.  Every
number on every morphology profile is illustrative.

The order's own Open section says why: *"The derivation set has to come from
someone with a long direct baseline... the priors have never been written in a
form anything can read."*  That is the state this folder is in.  What is built
is the shape the priors would be written into, and the counters that say how
much of the shape is empty.

The order's second Open item -- animal route data and game trails as a second
intake path -- is not specced and is not built.

STATUS: UNVERIFIED, and cannot be otherwise from here.

---

## TPR_013 -- declared vocabulary members no entry populates

Reported rather than filled:

* `confidence` `MEDIUM` -- reached by no entry
* `bearing_class` `NOT_STATED` -- reached by no entry; the branch is exercised
  directly in the test
* the boulder entry states no top-level `bearing_class` at all, because its
  prior is branch-conditioned (`TPR_005`)

A declared member nothing populates is not evidence that the member is
reachable, which is why each is checked by name rather than by a count.

STATUS: SUPPORTED, counted.
