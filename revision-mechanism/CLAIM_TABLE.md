# revision-mechanism — CLAIM_TABLE

`RM_001..RM_009`. Claims about the delivered `SOURCE_DROP.md`.

**The study is not run here and is not simulated.** It requires
fieldwork and collective consent, and its own ethics section says
publishing a group's revision procedure without consent can damage the
mechanism being studied. No synthetic site stands in for a real one
anywhere in this folder, and nothing here is a statement about any
community, tradition, region, or body of knowledge.

What is computed is the design's own arithmetic — which of its
comparisons the asked-for sample size can carry — and that needs no
field data at all.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `RM_001` | The inversion is right and is the strongest thing in the drop: a stable environment does not discriminate, so sampling only stable systems guarantees the mechanism stays invisible. | SUPPORTED |
| `RM_002` | **One site pair carries three of the four comparisons and cannot carry the second at any per-site precision.** The second is the one whose prediction is a threshold. | SUPPORTED |
| `RM_003` | Comparison 2 becomes decidable at roughly 4–6 sites with ~100 components coded per site, 8–12 at ~30, and not at 20 sites with ~10. | SUPPORTED |
| `RM_004` | `STATUS` has no state for *checked, still matches*, so an unassessed component and a confirmed-still-fitting one land in the same value — and the headline rate is biased low by exactly the unassessed share. | SUPPORTED |
| `RM_005` | The held-obsolete rate is called *"the single most comparable number across sites"* and its comparability rests entirely on the coding scheme that is absent. | SUPPORTED |
| `RM_006` | Comparison 4 compares a revision in a written record against a revision in a living system, and the drop's own reasoning is why they may not be one object. | SUPPORTED |
| `RM_007` | `CHANGE AS FRAME` is the two-columns discipline designed in, and it makes a mismatch a finding rather than noise. | SUPPORTED |
| `RM_008` | M1–M8 is named, absent, and not reconstructed. Six of the design's measures key off it. | **CLOSED 2026-08-26** — the companion study landed; the scheme is imported, never reconstructed |
| `RM_009` | Nothing here is evidence about any transmission system. The ethics constraint is a constraint on this audit, not only on the fieldwork. | UNVERIFIED |

---

## RM_001 — the inversion, and why it is the strongest part

> *stable environment → good and bad transmission both survive. No
> discrimination. Nothing is being tested.*

That is `null-harness`'s invariant stated about a field method rather
than a gate: **a test both a working and a broken instance passes is
not a test.** A study sampling stable systems is measuring under a
condition where the variable of interest has no consequence, so it
returns a null that is a property of the sampling frame.

And the reframing that follows — *change is the selection pressure; it
is the only condition under which the adaptive mechanism is visible at
all* — is the same move `investigation-sim` `IS_001` had to make in
the other direction. There the trap was a corpus selected on the
outcome; here it is a corpus selected on the *absence* of the outcome.
Both are the sampling frame deciding the result.

The distinction between **content** and **revision mechanism** is the
part that makes the design a design rather than a survey: *"A tradition
with no revision mechanism and one with a strong mechanism look
identical until conditions change."*

**Falsifier:** a stable-environment site where the revision machinery
is nevertheless legible — which would mean change is not required to
make it visible, only helpful.

## RM_002 — one pair carries three of four

    #   comparison                                kind          at a pair
    1   high-change vs low-change, same domain    CATEGORICAL   yes
    2   fast-change vs slow-change                SHAPE         NO
    3   component form, M3 vs M7                  WITHIN_SITE   yes
    4   written vs living, same domain/region     CROSS_MEDIUM  yes

Comparison 1 is a presence/absence contrast on two sites, which is
exactly what a pair is. Comparison 3's denominator is **components,
not sites**, so one site with enough components carries it. Comparison
4 needs one of each medium.

Comparison 2 predicts *"a discontinuity, not a slope"*, which is a
claim about **shape**, and shape is the one thing two points cannot
carry.

**And this is exact, not statistical.** A line has two free parameters
and a step has two. Two points determine both exactly. Measured over
500 arbitrary pairs, the largest residual under either model is
**2.47e-32** — machine zero. So at `n = 2` the discriminator returns a
tie at every per-site precision tested, including 1000 components per
site: the row is *empty*, not *weak*.

    n     M=10   M=30   M=100
    2     tie    tie    tie

No amount of care in the field changes this. It is the arithmetic of
fitting two two-parameter models to two points.

**Falsifier:** a statistic that separates a step from a slope on two
points without assuming one of them.

## RM_003 — the site count comparison 2 needs

Accuracy at telling a generating step from a generating slope, both
passing through the same endpoints so the endpoints alone cannot
separate them:

    n     M=10   M=30   M=100
    2     tie    tie    tie
    3     0.66   0.80   0.93
    4     0.70   0.81   0.94
    6     0.73   0.85   0.98
    8     0.75   0.88   0.98
    12    0.84   0.93   0.99
    20    0.87   0.97   1.00

So: **4–6 sites at ~100 components each; 8–12 at ~30; and at ~10
components per site, twenty sites still do not reach 0.9.**

That is a concrete number for a design decision, produced with no
fieldwork, and it says the depth of coding per site trades against the
number of sites at a steep rate — which is a budget question the drop
does not currently have an answer for.

Every parameter is declared and none is measured: the low and high
rates, the break point, the range of the rate ratio, and the fitting
rule. The result that does *not* depend on them is the `n = 2` row.

**Falsifier:** a per-site precision or an effect size where the
ordering inverts.

## RM_004 — `STATUS` has no *checked and still matches*

    held unchanged
    revised          content changed, function retained
    extended         new content added for new conditions
    dropped          no longer transmitted
    held obsolete    still transmitted, no longer matches conditions

`held obsolete` is **checked and does not match**. Nothing is
**checked and does match**. So a component nobody assessed and a
component assessed as still fitting both land in `held unchanged`.

Both sit in the held-obsolete rate's denominator — *"still-transmitted
components"* — and only one can enter the numerator. **The bias runs
one way**, and by exactly the unassessed share:

    unassessed   observed   understated by
    0.00         0.350      0.000  ( 0%)
    0.10         0.315      0.035  (10%)
    0.30         0.245      0.105  (30%)
    0.50         0.175      0.175  (50%)

So the transmission system's own error rate is reported *lower* than
it is, in the direction that makes any system look better than it is,
on the number the drop calls the single most comparable one across
sites.

The absent-vs-known-negative repair, on a five-value vocabulary that
already separates four other states carefully. What would close it: a
sixth value — *held unchanged, match confirmed* — distinct from *held
unchanged, match not assessed*. Two states, currently one.

**Falsifier:** a coding protocol requiring every `held unchanged`
component to be assessed, which would make the two states identical in
practice.

## RM_005 — the most comparable number rests on the absent scheme

> *HELD-OBSOLETE RATE — fraction of still-transmitted components that
> no longer match conditions. This is the transmission system's own
> error rate and the single most comparable number across sites.*

A rate is comparable across sites only if the denominator is the same
kind of thing at each. The denominator here is *components*, and what
counts as a component is fixed by M1–M8 — which is in the companion
study and not in this repository.

So the drop's own most-comparable number is comparable **through** the
scheme that is absent, and two sites coded under different component
inventories yield two rates that are not the same quantity. That is
not a defect in the design; it is a dependency the design has and the
delivered text does not flag on this measure specifically.

**Falsifier:** M1–M8 landing, at which point this is checkable rather
than structural.

## RM_006 — comparison 4's two objects

> *written records show LOWER revision rates and HIGHER held-obsolete
> rates, because the medium has no mechanism for retraction.*

A revision in a written record — a new edition, an erratum, a
superseding text — and a revision in a living system — a holder
changing what they teach — are both called *revision*, and the
comparison is a ratio of their rates.

The drop's own stated reason is what makes them possibly not one
object: *"the medium has no mechanism for retraction."* If the medium
lacks the mechanism, then a written "revision" is a different
operation from a living one, and the rate comparison is across unlike
objects — `reasoning-gate`'s `G-DIM`.

**This does not sink the comparison.** The drop is explicit that it
*"tests the framing claim rather than assuming it"*, which is the
right posture and rarer than it should be. What it takes is one added
line saying what counts as a revision in each medium, so the ratio has
an object.

The 'Why this beats the archive' section half-supplies it: *"revision
usually is not [measurable in archives], because superseded versions
were not kept."* If superseded versions were not kept, the written
revision rate is not low — it is **unmeasured**, which is a third
value the comparison does not currently have.

**Falsifier:** a written corpus where superseded versions were kept,
making the written revision rate measurable rather than absent.

## RM_007 — `CHANGE AS FRAME` is the two-columns discipline

> *"high change" is defined from an outside physical record. Holders
> may partition change differently. Record their partition separately
> and do not overwrite it. A mismatch between the two partitions is a
> finding.*

Two columns kept apart, with the disagreement between them promoted to
a result rather than reconciled away. `report-typing` `RT_002` reached
the same structure for mention-versus-citation; `divergence-playground`
built a whole folder on spread between readers being the object rather
than the noise.

Here it is stated in a confounds list, before any data, with the
mismatch named as a finding in advance. That is the strongest single
sentence in the confounds section, and it is what stops the outside
physical record from silently becoming the ground truth for a variable
the study is about.

`SURVIVOR SITES ONLY` is the same quality: the truncation is stated,
its consequence is stated (*"it bounds every conclusion about failure
rates"*), and a partial remedy is named rather than the problem being
estimated around. The ask repeats it — *"Report the truncation at the
failure end rather than estimating around it."*

**Falsifier:** none. This is a design property and it is present.

## RM_008 — M1–M8 is named, absent, and not reconstructed

Six of the design's measures key off it:

    STATUS (per component)
    REVISION PROVENANCE (per component)
    LATENCY (per component)
    HELD-OBSOLETE RATE (denominator is components)
    ROBUSTNESS FORM (per component)
    comparison 3 (M3 vs M7 by name)

**Not reconstructed.** A coding scheme is data, and inventing M1–M8
would put a category system in the author's mouth — every number
downstream would then be about the invention. The `PB_001` / `CW_004`
rule, and it binds harder here because the categories would shape what
a field coder saw.

The selftest asserts no M1–M8 *definition* appears in this folder and
that no coding-scheme file was created. That check's first version
grepped `M1 `..`M8 ` and fired on my own *references* to comparison 3
— a reference is not a definition, and use-mention got the check
before it got the corpus.

**Falsifier:** the companion study landing.

**FIRED, 2026-08-26.** It landed as `transmission-decay/`. The scheme
is now **imported** from `transmission-decay.scheme.COMPONENTS` rather
than described as absent — eight components, comparison 3's `M3` and
`M7` both resolve, and the import means the two folders cannot drift.

Recorded rather than quietly updated because the claim's whole content
was that a coding scheme is data and inventing it would put a category
system in the author's mouth. Not reconstructing it was the right call
and the arrival is what shows it: the delivered `M1..M8` are a
hazard-specific vocabulary — *source identified*, *trigger named*,
*routing correct*, *precursor signs* — that no reasonable invention
would have produced, and every number keyed to an invented scheme would
have been about the invention.

## RM_009 — the ethics constraint binds this audit

> *Publishing a group's revision procedure without consent can damage
> the mechanism being studied. That is a hazard, not a formality.*

That sentence is a constraint on **me**, not only on a fieldworker.
The available shortcut for a study I cannot run is to simulate it —
generate plausible sites, plausible held-obsolete rates, plausible
provenance codings — and publish a table that reads like a result.
Anything published that way into a CC0 repository is a fabricated
claim about real communities, whether or not any is named.

So nothing here models a site, a holder, a tradition, or a community.
The only objects in `power.py` are a line, a step, and binomial noise,
and the selftest asserts the report states this and names the consent
reason.

What that leaves unverified is everything the study is about. The
inversion, the four predictions, the latency measure, the provenance
coding, the held-obsolete rate itself — none is tested here, and no
result in `RM_001..RM_008` is evidence for or against any of them.
They are statements about a design's arithmetic and vocabulary.

**Falsifier:** run it, with consent, at a site count `RM_003` says
carries the comparison you want.
