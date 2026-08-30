# observable-indicator-rules — CLAIM_TABLE

`OIR_001..OIR_009`. Claims about the delivered `SOURCE_DROP.md` and the
pipeline built from it.

**This drop is built to run here.** The spec says the post-processing is
*"stdlib, phone-buildable"* and the router (2D unsteady solve) is *"the
only non-phone term."* So the router output is an **input**: `pipeline.py`
consumes a time-resolved depth field and never runs a solver. The fields
in `ensembles.py` are **synthetic**, authored so ground truth is known;
**nothing in this folder is a claim about any real community, drainage,
road, or household.**

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `OIR_001` | The pipeline is buildable here with the router output as an input, and the spec's falsifiable condition fires both ways: flipping → empty, stable → rules. | SUPPORTED |
| `OIR_002` | **The finding: step 3 is a MISS filter and is blind to false alarms.** A trigger with a perfectly stable order but a high false-alarm rate passes, and the spec's card carries no line for it. | SUPPORTED |
| `OIR_003` | The stability criterion is over-strict — a tie drops a weak-but-valid ordering — which loses rules rather than inventing them, the safe direction for a life-safety card. | SUPPORTED |
| `OIR_004` | The ordinal bet holds: the pipeline extracts a stable order where the magnitude varies 5×, and reports it as a band planned against the short end. | SUPPORTED |
| `OIR_005` | The card is anchored to the household and the route is coupled: when the route closes first, the trigger is upstream of the door. | SUPPORTED |
| `OIR_006` | A run in which neither landmark wets carries no ordering information and is excluded, a boundary the spec leaves open. | SUPPORTED |
| `OIR_007` | The two error rates are asymmetric in the pipeline: step 3 forces the miss rate to ~0 and leaves the false-alarm rate unconstrained. | SUPPORTED |
| `OIR_008` | This is the household-facing product for the same flood family as `columbia-chain-cascade` and `reservoir-chain-coupling`: the coupled solve is done once upstream, the household holds a result not a computation. | SUPPORTED |
| `OIR_009` | Whether any real community has a derivable card, and at what false-alarm rate, is UNVERIFIED — that needs the router run on real terrain, the non-phone term. | UNVERIFIED |

---

## OIR_001 — buildable here, and the falsifiable condition fires

The spec draws the line itself: the router is the only non-phone term,
the post-processing is stdlib. So `pipeline.py` takes the router's
time-resolved depth field as an input and derives the rules; the fields
are synthetic (`ensembles.py`), authored so the answer is known.

The spec's falsifiable condition — *"if step 3 finds no stable
orderings ... this method returns nothing rather than a false rule.
Empty output is a valid, honest result"* — is checked both ways:

    flipping ensemble (every pair reverses)  -> empty output: True
    stable ensemble  (order fixed)           -> rules: 3

A pipeline that always emitted a rule would be `CONSTANT_FIRES`. This
one returns nothing when every pair flips and rules when they hold, so
the empty result is a measurement rather than a failure to run.

**Falsifier:** a flipping ensemble that yields a rule, or a stable one
that yields none. The selftest asserts neither happens.

## OIR_002 — step 3 is a miss filter, blind to false alarms

The load-bearing check (step 3) keeps a pair only if the wetting order
is invariant across the ensemble. Consider a trigger→hazard pair and the
two ways the rule can fail:

    MISS         hazard wets, trigger dry   -- fatal, no warning
    FALSE ALARM  trigger wets, hazard dry   -- cry-wolf, erodes trust

A miss makes the trigger's `t_wet` INF while the hazard's is finite, so
`sign(t_trigger − t_hazard)` is +1 — the opposite of a true positive's
−1. **Step 3 drops the pair on any miss.** Good: it is strict about the
fatal error.

A false alarm makes the hazard's `t_wet` INF while the trigger's is
finite, so `sign(t_trigger − t_hazard)` is −1 — **the same sign as a
true positive.** Step 3 does not drop it. So a trigger that wets in many
runs where the hazard never arrives passes the load-bearing check, and
the spec's card carries a clean lead band with no line for it.

Measured on the `false_alarm_heavy` ensemble:

    trigger kept by step 3:  True
    miss rate:               0.0   (step 3 forces this)
    false-alarm rate:        0.5   (step 3 does not constrain this)
    4 true positives, 4 false alarms

For a rule people *act* on — evacuate every time it fires — the
false-alarm rate is what decides whether they obey it the tenth time.
The pipeline computes the timing (ordering + short-end band) and neither
error rate. `reliability()` adds both, and the card built here carries a
`REL` line the spec's card template does not (the strings *"false
alarm"* and *"miss rate"* appear nowhere in the delivered card).

This is `null-harness`'s FP/TP on a flood card, and the same shape as
`household-scope-audit` and `evaluation-frame`: the denominator excludes
the failure the instrument is silent about. The method's ordering
insight is sound; the card needs two numbers the pipeline does not
produce.

**Falsifier:** a version of step 3 that constrains the false-alarm rate,
or a demonstration that a dry hazard flips the pair's sign. Neither
holds for the criterion as written.

## OIR_003 — the criterion is over-strict, which is the safe direction

Step 3 uses strict sign-invariance (`all_same(order)`). A tie — two
landmarks wetting in the same timestep — is a third sign value (0), so a
pair that is A-before-B in some runs and A-with-B in others is dropped,
even though *"A wets no later than B in every run"* is a usable rule
(*"when A is wet, B is wet or imminent"*).

    strict sign-invariance keeps the tied pair:  False
    the weak order (A never strictly after B):   True

So the criterion drops a weak-but-valid ordering. That loses some usable
rules — but it **drops rules rather than inventing them**, which is the
correct direction to fail for a life-safety card. Recorded as a
containment, not a fault; the repair, if wanted, is to test weak-order
invariance (ties permitted) rather than strict sign-invariance.

**Falsifier:** a case where strict-invariance invents a rule the weak
order would reject. It cannot — strict is a subset of weak.

## OIR_004 — the ordinal bet holds

The spec's premise: *"magnitude moves with the scenario; the SEQUENCE in
which places wet is far more stable."* The `stable` ensemble fixes the
order (bridge → bend → house) while the gaps vary ~5× across runs.

    stable pairs found:        3
    bridge -> house lead band: 2 to 9.2 steps (width 7.2)

The order is invariant while the magnitude is not, so the point estimate
would lie and the band does not. Reporting the band and planning against
the short end (`min`/`p10`, never the median) is the honest product, and
it is what the spec asks for — the built card uses `["min"]` and never
`["p50"]`, asserted.

**Falsifier:** a stable-order ensemble whose lead band collapses to a
point. The varying-gap construction makes it wide.

## OIR_005 — the route is coupled and the trigger is upstream of the door

The driving insight: *"the route out crosses the same drainages. It can
flood before the household does. Then 'leave when water reaches your
door' is fatal."* `rule_for()` finds the earliest route closure across
the ensemble, and selects a trigger that reliably wets before it with
enough lead to complete movement.

    trigger != household:                     True
    trigger wets before the route closes:     True

So when the route closes before the house floods, the card triggers
upstream of the door, not at it — the spec's *"the water at your door
means the road is already gone."*

**Falsifier:** a route-closes-first ensemble where the chosen trigger is
the household itself. The selftest asserts it is not.

## OIR_006 — no-wetting runs carry no order and are excluded

`sign(INF − INF)` is undefined, and a run in which neither landmark wets
carries no ordering information. The spec's `sign`/`all_same` do not say
what to do with it. `_ordering()` **excludes** such runs from a pair's
stability check — counting one as agreement would inflate stability,
counting it as a flip would suppress a real rule.

    neither-wet run excluded from the pair check:  True
    pair stays stable on the informative runs:     True

Marked `[CHOICE]` in the code, because it is a boundary the spec leaves
open and the reading is defensible rather than forced.

**Falsifier:** a reading on which a no-information run should count as
agreement or as a flip. Excluding it is the only one that adds no false
signal in either direction.

## OIR_007 — the error rates are asymmetric by construction

`reliability()` returns both rates, and they are not symmetric in the
pipeline: step 3 forces the miss rate to ~0 for any kept pair (a miss
flips the sign), while the false-alarm rate is whatever the ensemble
makes it (a false alarm does not flip the sign). A null check confirms
the floor: a trigger identical to the hazard has zero of both.

**Falsifier:** a kept pair with a non-zero miss rate. Step 3 forbids it.

## OIR_008 — the household-facing end of the flood family

This is the third drop in the family, and it is the output end. The
sibling `columbia-chain-cascade` is the coupled solve as a build spec;
`reservoir-chain-coupling` is the operator swap that makes the coupling
load-bearing; this is what the household holds afterward.

The spec's inversion — *"the heavy solve is done once, offline,
upstream. The household holds a result, not a computation"* — is the
same governance point the siblings make from the modeling side: the
coupled chain has no single owner, so the product that survives every
notification link failing is one the household evaluates on sight,
needing no channel, no compute, no permission.

**Falsifier:** the three documents disagreeing on what the coupled solve
produces. They do not; this consumes what the other two describe.

## OIR_009 — no real card is derived here

Everything runs on synthetic ensembles. Whether any real community has a
stable trigger, what its false-alarm rate is, and whether a card is
derivable at all are questions about a real depth field — which needs
the router (HEC-RAS) run on real terrain, the non-phone term the spec
names and this environment cannot reach (measured in
`columbia-chain-cascade`).

What is established is about the pipeline's logic: it extracts stable
orderings, returns empty when there are none, plans against the short
end, couples the route — and, as the spec writes it, the card omits the
two error rates a person acting on it is never shown.

**Falsifier:** run the pipeline on a real router ensemble. Then the
cards are real, and their false-alarm rates decide whether the method
delivers a usable product for that community.
