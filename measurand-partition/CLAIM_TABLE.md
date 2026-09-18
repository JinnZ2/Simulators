# CLAIM_TABLE -- measurand-partition

Claims are about the INSTRUMENTS and about the delivered orders. Every
record the modules carry is CONSTRUCTED and marked PROPOSED, the
delivery's own tag; nothing here is a claim about any person, program,
structure or piece of wood, and no literature figure the orders carry has
been checked against a source.

`MPS_*` ids are permanent. A refuted claim is updated; the checks are not
retuned to preserve it.

---

| id | claim | status |
|---|---|---|
| MPS_001 | the common structure is one record shape and all four delivered populations read UNPARTITIONED under it; an unenumerated unmeasured set reads NOT_EVALUABLE, never PARTITIONED | SUPPORTED, schema |
| MPS_002 | WO-1's STEP 3 is a gate, not a subtraction: the order supplies no axis-to-performance model and none is invented, so a residual's size is never computed here | DECIDED, limit |
| MPS_003 | the two-setting arm runs without a model; one moved label establishes a floor; single-setting individuals are UNBOUNDED and an unrun arm is NOT_RUN, never floor 0 | SUPPORTED, constructed |
| MPS_004 | WO-2's measurement fault reproduces: band-low, band-high and flat return one point read at the standard level and the sweep separates them | SUPPORTED, constructed |
| MPS_005 | a curve's absences are three states -- NOT_REGISTERED, NOT_ESTIMABLE, CEILING_NOT_REACHED -- and a level nobody swept is NOT_SWEPT, not interpolated | SUPPORTED |
| MPS_006 | ADVISED_ON is not control: the academy as described grades 0.40 with two advised variables counted apart; an UNDECLARED variable makes the gradient NOT_COMPUTABLE | SUPPORTED, statuses carried |
| MPS_007 | WO-3b and WO-3c cannot return a number from what the literature publishes: no program carries a measured accuracy, and the ceiling is UNDECLARED until the not-controllable variance shares are | FINDING on the design |
| MPS_008 | WO-4a's ~40% holds (41.4%) and its mechanism sentence does not: I = b h^3/12 is cubic in depth times linear in width; depth alone gives 33% | FINDING, arithmetic |
| MPS_009 | the order's arithmetic names stiffness and its test measures strength; on the 4x4 the ratios are 0.586 and 0.670 | FINDING, arithmetic |
| MPS_010 | the square 4x4 understates the general substitution: a 2x4 keeps 0.502 of a full section's stiffness | DERIVED |
| MPS_011 | WO-4b's critical split is enforced: pooled() refuses, REMOVED censors, UNKNOWN maintenance is counted apart, an unmatched stratum enters no comparison | SUPPORTED, machinery |
| MPS_012 | a maintenance-conditional durability claim reads against the maintained arm only, from a declared boolean and never from wording | DECIDED |
| MPS_013 | under PODIUM three constructed athletes are failures; under LEARNED the same three are AHEAD on four of five capacities and TIE on the released-for one -- the category is manufactured by the measurand | SUPPORTED as instrument; the prediction stays PROPOSED |
| MPS_014 | LEARNED is NOT_COMPUTABLE without untrained age peers, the group no program recruits; manufactured is then None, not 0 | SUPPORTED |
| MPS_015 | an imported frame must declare its measurand apart from its fields; PODIUM is never a default | SUPPORTED |
| MPS_016 | four of five orders rest a step on an absence and only WO-4b states its corpus; the other nulls carry no corpus and no terms | FINDING, QA_004 |
| MPS_017 | nothing here is evidence about any child, athlete, coach, structure or piece of wood; every literature figure is carried and egress-blocked | UNVERIFIED |

---

## MPS_001 -- the common structure as a record

`common.attribution(observed, setting, unmeasured, assigned_to)` returns
UNPARTITIONED when unmeasured variables exist and the residual went to
the observed thing, PARTITIONED when the list is empty, ASSIGNED_ELSEWHERE
when it went somewhere else, and NOT_EVALUABLE when the list is `None` --
nobody enumerated it, which is not the same as nobody left anything out.
The four delivered populations are entered with the orders' own partial
lists and all four read UNPARTITIONED. A schema, not a finding: whether
an assignment is right is not a property of the record.

## MPS_002 -- STEP 3 is a gate

The order's STEP 3 says "report the RESIDUAL after A1-A4 are entered".
Entering four axes and reporting what is left presupposes a model of what
each axis contributes to a performance score, and the order has none. So
`residual()` returns RESIDUAL_CANDIDATE carrying the raw score only when
every axis is MEASURED with a named instrument ([CHOICE 1]) and the
interaction is entered, and NOT_SEPARABLE naming the missing axes
otherwise. It never subtracts, asserted over the source. The design
separates; the size of what it separates is the operator's model.

**Falsified if** a residual value ever differs from the entered score.

## MPS_003 -- the two-setting floor

Grouped by individual, those labelled at two or more settings are the
denominator; those whose label differs are the numerator; the share is a
floor on displacement. On the constructed set: p-01 moved
(deficit/typical), p-02 did not, floor 0.50, FLOOR_ESTABLISHED. Three
individuals at one setting are UNBOUNDED and out of the denominator
([CHOICE 2]); two individuals at one setting each is NOT_RUN with floor
`None`; two at two settings with no movement is NO_CASE_FOUND at floor 0,
stated as not established above it.

## MPS_004 -- the measurement fault, reproduced

Three constructed curves over levels 0..10 at register threshold 0.5
([CHOICE 1]): band 1-4, band 6-9, flat 0.1. At the standard level 5 all
three return 0.10. Under the sweep: BAND_LOCATED with the point
ABOVE_CEILING, BAND_LOCATED with the point BELOW_FLOOR, NOT_REGISTERED.
Shutdown-at-ceiling and no-response-below-floor return the same score and
both are indistinguishable from a flat curve -- the order's sentence, as
a number.

## MPS_005 -- three absences

NOT_ESTIMABLE (fewer than three levels, [CHOICE 2]), NOT_REGISTERED (no
level reaches the threshold), CEILING_NOT_REACHED (registering at the top
of the sweep, [CHOICE 3]) are distinct returns, all reached. `single_point`
on a level not swept returns NOT_SWEPT; nothing interpolates.

## MPS_006 -- ADVISED_ON is not HELD

The order's own note: published academy descriptions show EDUCATION on
nutrition and hydration, an intervention on knowledge, not control of
intake. The demo program enters those two as ADVISED_ON and grades 0.40 =
2 HELD of 5 controllable, with the advised count printed beside and never
inside the fraction ([CHOICE 1]). A record with a variable absent reads
UNDECLARED and the gradient is NOT_COMPUTABLE naming it; NOT_TOUCHED is a
declaration, not a default. The statuses are the order's reading of
marketing copy, CARRIED.

## MPS_007 -- 3b and 3c have no inputs yet

`accuracy_vs_gradient` requires three programs carrying both a gradient
and a measured accuracy ([CHOICE 2]) and no such program exists, so it
returns NOT_EVALUABLE and "the eye is unreliable" stays UNPARTITIONED --
the order's own word. `accuracy_floor` requires a declared outcome-variance
share for each not-controllable variable ([CHOICE 3]) and returns
UNDECLARED without them, which is the state the literature is in: a
reliability figure read with no stated ceiling is read against 100%. On
constructed shares (0.25 + 0.15 not controllable) the ceiling is 0.60 and
a reported 0.60 reads as 1.00 of achievable. Both trends (RISES, FALLS)
and the one-gradient NOT_EVALUABLE are reached on constructed programs.

## MPS_008 -- the fourth power is two factors

Second moment of area `I = b h^3 / 12`. Nominal 4x4 to actual 3.5x3.5:
depth ratio cubed is 0.670, width ratio 0.875, product 0.586, so 41.4%
of stiffness goes -- the order's ~40%. The order attributes the fourth
power to depth; a third of it is width. Shrink depth alone and 33% goes.
Registered in `tools/known_answer.py` with the depth-only case as the one
where the sentence and the number part.

## MPS_009 -- stiffness against strength

The ARITHMETIC line is about bending stiffness (I). The TEST line, "load
capacity measured to failure", is about strength: section modulus
`S = b h^2 / 6` times the modulus of rupture. On the 4x4, S keeps 0.670
and I keeps 0.586. A to-failure test returns the strength number and would
be read against the stiffness claim -- `measurement-fork`'s VOID RATIO in
a one-paragraph order. `quantity_mismatch()` says so. Either quantity is
measurable; the order should name which.

## MPS_010 -- the square case understates

A 2x4 (1.5 x 3.5) keeps `0.75 * (3.5/4)^3 = 0.502` of a full 2x4's
stiffness. The 4x4 the order chose is the case where the two shrinking
dimensions are equal; on the common framing sizes the loss is larger.
Every actual dimension but the 4x4's is carried from memory (the US
softwood standard) and is not verified here.

## MPS_011 -- the split is machinery

`split_curves` computes Kaplan-Meier per (population, maintenance arm)
over matched strata only ([CHOICE 1]); `pooled()` raises naming the two
arms; REMOVED censors at the removal year ([CHOICE 2]); UNKNOWN maintenance
is excluded and listed; a stratum with one population is NOT_MATCHED. On
the constructed records the transmitted maintained arm sits at 1.0 at 150
years (a removal is not a failure) and the transmitted neglected arm at
0.5. No county record was read.

## MPS_012 -- the marketing clause, declared

"150 years or more with proper maintenance" is a claim about
MAINTAINED_IN_USE. `claim_scope(years, conditional_on_maintenance)` takes
the boolean declared and refuses a string, so the wording is never
parsed; an unconditional claim reads against both arms.

## MPS_013 -- the manufactured category

Constructed cohort: two SELECTED, three DESELECTED (released for load
tolerance), three UNTRAINED_PEER. PODIUM: 2 succeed, 3 fail. LEARNED:
deselected AHEAD on balance, spatial awareness, controlled falling,
transferable motor structure; TIE on load tolerance ([CHOICE 1] margin
0.05, group averages [CHOICE 2]). The three failures are AHEAD of untrained
peers on four of five capacities, so the category of three exists under
PODIUM and not under LEARNED. The cohort was built to the order's
PROPOSED prediction, so the demo shows the scorer recovers the shape when
present -- a known-answer run, no evidence.

## MPS_014 -- LEARNED needs the missing group

Without UNTRAINED_PEER records `score_learned` is NOT_COMPUTABLE and
`manufactured` returns count `None`. The order says nobody runs the
comparison; the reason is visible in the schema, since the group it needs
is the one a program has no reason to recruit.

## MPS_015 -- the import line

`import_line(frame_fields, measurand)` refuses an absent or empty
measurand; PODIUM is never supplied by default. The sports frame's four
fields travel; whether the deselection problem travels with them is the
one declared value.

## MPS_016 -- the nulls

WO-1 "not searched"; WO-2 "nothing found links intensity to what the
subject can do"; WO-3 the manifest "does not exist"; WO-5 "not found in
any search". None states a corpus or a term. WO-4b states ten results,
all builders, which is a bounded null in the `question-availability`
`QA_004` sense; the others are the author's and are recorded as such.
Nothing here searches either; the egress gate refuses.

## MPS_017 -- UNVERIFIED

Every constructed record is PROPOSED. Every literature figure is carried:
the London taxi hippocampus, the 2025 questionnaire, ~6.3 h against 8-10 h
sleep, the coach's-eye longitudinal result, barns at 250 years. What is
established is that five designs are properties of the code and are met,
two arithmetic statements in WO-4a come apart from their sentences, and
each order's step that rests on an absence is marked as one.
