# revision-mechanism

A study design for how transmission systems **update** what they know
when conditions move — the revision mechanism, not the content.

`SOURCE_DROP.md` is delivered verbatim. `power.py` computes the one
thing in it that needs no field data; `selftest_power.py` is 57 checks.

    python3 revision-mechanism/power.py             # the report
    python3 revision-mechanism/power.py --selftest

## What is not here

**The study is not run and is not simulated.** It requires fieldwork
and collective consent, and its own ethics section says publishing a
group's revision procedure without consent can damage the mechanism
being studied — *"a hazard, not a formality."*

That sentence is a constraint on this audit, not only on a
fieldworker. The available shortcut for a study one cannot run is to
simulate it: generate plausible sites, plausible held-obsolete rates,
plausible provenance codings, and publish a table that reads like a
result. Published into a CC0 repository, that is a fabricated claim
about real communities whether or not any is named.

So **nothing here models a site, a holder, a tradition, or a
community.** The only objects in `power.py` are a line, a step, and
binomial noise.

**M1–M8 is named, absent, and not reconstructed.** Six of the design's
measures key off the companion study's coding scheme, which is not in
this repository. A coding scheme is data; inventing it would put a
category system in the author's mouth and every number downstream
would be about the invention.

## What is computed

**One site pair carries three of the four comparisons and cannot carry
the second at any per-site precision.**

    #   comparison                                kind          at a pair
    1   high-change vs low-change, same domain    CATEGORICAL   yes
    2   fast-change vs slow-change                SHAPE         NO
    3   component form, M3 vs M7                  WITHIN_SITE   yes
    4   written vs living, same domain/region     CROSS_MEDIUM  yes

Comparison 1 is a presence/absence contrast on two sites — a pair is
the design, not a limitation. Comparison 3's denominator is
**components, not sites**. Comparison 2 predicts *"a discontinuity,
not a slope"*, which is a claim about **shape**, and shape is what two
points cannot carry.

**That is exact, not statistical.** A line has two free parameters and
a step has two, so two points determine both exactly — largest
residual under either model over 500 arbitrary pairs is **2.47e-32**.
At `n = 2` the discriminator returns a tie at every precision tested
up to 1000 components per site. The row is *empty*, not *weak*.

    n     M=10   M=30   M=100
    2     tie    tie    tie
    3     0.66   0.80   0.93
    4     0.70   0.81   0.94
    6     0.73   0.85   0.98
    8     0.75   0.88   0.98
    12    0.84   0.93   0.99
    20    0.87   0.97   1.00

So comparison 2 needs **4–6 sites at ~100 components each, 8–12 at
~30**, and at ~10 components per site twenty sites still do not reach
0.9. Depth of coding trades against site count at a steep rate, which
is a budget question the design does not currently have a number for.

## An asymmetry in the headline number

`STATUS` has five values and none of them is *checked, still matches*:

    held unchanged
    revised          content changed, function retained
    extended         new content added for new conditions
    dropped          no longer transmitted
    held obsolete    still transmitted, no longer matches conditions

`held obsolete` is *checked and does not match*. So an unassessed
component and one confirmed still fitting both land in `held
unchanged` — and both sit in the held-obsolete rate's denominator
while only one can enter the numerator.

**The bias runs one way, by exactly the unassessed share:**

    unassessed   observed   understated by
    0.00         0.350      0.000  ( 0%)
    0.10         0.315      0.035  (10%)
    0.30         0.245      0.105  (30%)
    0.50         0.175      0.175  (50%)

The transmission system's own error rate is reported *lower* than it
is — in the direction that makes any system look better — on the
number the drop calls the single most comparable one across sites.
What would close it: a sixth value, *held unchanged, match confirmed*,
distinct from *held unchanged, match not assessed*.

## Three more, briefly

**The inversion is the strongest thing in the drop.** *"Stable
environment → good and bad transmission both survive. No
discrimination."* That is `null-harness`'s invariant stated about a
field method: a test both a working and a broken instance passes is
not a test. `investigation-sim` `IS_001` is the same move in the other
direction — there a corpus selected on the outcome, here one selected
on its absence.

**The held-obsolete rate is comparable only through M1–M8.** A rate is
comparable across sites when the denominator is the same kind of thing
at each, and what counts as a component is fixed by the absent scheme.

**Comparison 4 compares two objects that may not be one.** A revision
in a written record and a revision in a living system are both called
revision, and the drop's own reason — *"the medium has no mechanism
for retraction"* — is what makes them possibly different operations.
The drop is explicit that it *"tests the framing claim rather than
assuming it"*, which is the right posture; what it takes is one line
saying what counts as a revision in each medium. And its own archive
section supplies a third value the comparison lacks: if superseded
versions were not kept, the written revision rate is not low, it is
**unmeasured**.

## What the design gets right

`CHANGE AS FRAME` — *"Holders may partition change differently. Record
their partition separately and do not overwrite it. A mismatch between
the two partitions is a finding."* Two columns kept apart with the
disagreement promoted to a result, stated before any data.
`report-typing` `RT_002` reached the same structure independently.

`SURVIVOR SITES ONLY` — the truncation is stated, its consequence is
stated, a partial remedy is named, and the ask repeats it: *"Report
the truncation at the failure end rather than estimating around it."*

## Files

| | |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim |
| `power.py` | the detectability computation, the unassessed-component bias, the comparison classification |
| `selftest_power.py` | 57 checks |
| `CLAIM_TABLE.md` | `RM_001..RM_009` with a REFUTATION_PROTOCOL |
| `samples/` | pinned run |

One declared `no_severity` exemption (`error`), measured with the
three-arm harness — the drop calls the held-obsolete rate *"the
transmission system's own error rate"*, which is the delivered
document's own name for the quantity.

Stdlib only, parses under Python 3.9, deterministic, CC0.

Siblings: `null-harness/` (a test both instances pass is not a test),
`investigation-sim/` (`IS_001`, the sampling frame deciding the
result), `consensus-anchor/` (`CA_004`–`CA_006`, thresholds needing a
declared margin and a measured baseline), `observer-exclusion/`
(`OE_003`, survivorship in a transmission record),
`report-typing/` (`RT_002`, two columns kept apart).
