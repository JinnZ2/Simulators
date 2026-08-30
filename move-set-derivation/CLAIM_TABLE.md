# move-set-derivation — CLAIM_TABLE

`MSD_001..MSD_012`. Claims about the delivered `SOURCE_DROP.md` and
about Arm 1 as built and run.

**Nothing here is a system under test.** The environment and all four
solvers are authored in this folder. A regression run against one
hand-written solver returns its author's architecture, not a capacity —
a solver that composes loads on recombination depth by construction, one
that looks up a neighbour loads on similarity by construction. So the
solvers carry **declared architectures** and the question asked is
whether the discriminator can tell them apart. That is
`null-harness`'s known-truth-first invariant applied to the arm's own
instrument before it is pointed at anything.

Arms 2, 3 and 4 are UNMEASURED and are not approximated.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `MSD_001` | This is the design `evaluation-frame`'s M4 cited by name; the shared null-rate instrument claim holds, and both instances fail for the same reason. | SUPPORTED |
| `MSD_002` | The arm's stated validity condition holds and is asserted, not intended: no primitive appears in test that is absent from training. | SUPPORTED |
| `MSD_003` | **The two regressors are correlated by construction (−0.67) and the test set carries only two depth levels, because depth 0 IS a training configuration.** | SUPPORTED |
| `MSD_004` | The decorrelation is in the same data — a matched band of 144 where similarity is constant — and it costs sample size, not a new environment. | SUPPORTED |
| `MSD_005` | **The discriminator fails its own known-answer run: every cell reads NEITHER_CARRIES or UNMEASURED, on four solvers whose architectures were declared in advance.** | SUPPORTED |
| `MSD_006` | The drop's stated rule and the null-tested verdict disagree, and both are right about different things: the rule recovers RETRIEVAL's architecture at a 14× coefficient ratio, and the model does not clear chance. | SUPPORTED |
| `MSD_007` | **The stated rule has no state for *neither regressor does anything*, so it returns an architecture verdict on a solver that has neither** — and on the matched band it would return the derivation verdict on a retrieval solver. | SUPPORTED |
| `MSD_008` | The arm is underpowered here rather than blind: it takes ≈600 configurations carrying an admissible move, and this environment supplies 143. | SUPPORTED |
| `MSD_009` | **Two of the five measures are gameable in opposite directions and need a partner the drop does not list**: the null rate by silence, the admissibility fraction by conservatism. | SUPPORTED |
| `MSD_010` | Time to first admissible move is `CONSTANT_SILENT` on this solver set, and that is a property of the fixtures rather than of the measure. | SUPPORTED |
| `MSD_011` | The enumerated condition is a control and behaves like one — every architecture scores identically — which is why it belongs in the table. | SUPPORTED |
| `MSD_012` | Nothing here is evidence about any trained model, any animal, or any operator. | UNVERIFIED |

---

## MSD_001 — the design the previous drop cited

`evaluation-frame/SOURCE_DROP.md`, M4:

> Same instrument as the null-rate measure in the move-set derivation
> design: in both cases, a system that cannot return an empty set is not
> reading the input — it is filling a slot.

It is the same instrument, and the identification is exact: *can the
system return the empty set on input that warrants it*. There the empty
set is "no ask locatable here", here it is "no admissible move".

**Both instances fail, and for the same reason.** In
`evaluation-frame` the null rate could not discriminate because a
standing convention supplied the ask, so the eligible set emptied. Here
it cannot discriminate because **silence scores a perfect null rate**:
`SILENT` returns the empty set always, reads 1.0000, and reaches an
admissible move zero times — the same 1.0000 `DERIVATION` reads while
reaching 143.

So the shared instrument has a shared limit the shared framing does not
name: it is one side of a pair. The other side is a reach term —
coverage here, an eligible-set count there — and neither drop lists it.

**Falsifier:** a formulation of the null rate that separates a system
representing an empty move set from one that emits nothing, without a
second measure.

## MSD_002 — the arm's validity condition holds, and is asserted

> NOVELTY MUST BE COMPOSITIONAL, NOT PRIMITIVE. Introducing an unseen
> primitive measures knowledge. Recombining seen primitives measures
> derivation. This is the whole validity of the arm.

`env.compositional_only()` returns the primitives appearing in test and
never in training. It returns `[]`, and the selftest requires that.

**The check is null-tested**, because an assertion that can only pass is
not an assertion: a deliberately leaky split — training families with
`thermal` withheld — is run, and the check catches it, returning
`["thermal"]`. Then the split is restored and the empty result asserted
again.

The environment is exhaustive rather than sampled: all 2⁶ × 6 = 384
configurations, no seed, no draw. `random` does not appear in `env.py`
and the selftest asserts it.

**Falsifier:** a test configuration containing a primitive absent from
every training family. Then the arm measures knowledge and reports it as
derivation, and every number in the folder is about the wrong thing.

## MSD_003 — the two regressors are correlated by construction

    n=306   corr(similarity, depth) = -0.6737
    depth levels present in test: [1, 2]

Two facts, and the second is the load-bearing one.

**Depth 0 cannot appear in the test set at all.** A primitive set inside
one training family IS a training configuration — that is what the split
means. So the test set has two depth levels, not a range, and a
regression on a two-level predictor is a two-group comparison wearing a
slope's notation.

And the two levels differ in similarity, necessarily: a set requiring
two training families to cover is further from any single one, almost by
definition. −0.67 is not a property of this particular split. It is what
the two definitions produce together.

The drop's discriminator asks which of the two carries the outcome. On
correlated regressors that question is weakly identified before any
solver is run.

**Falsifier:** a split where depth and similarity are independent by
construction. It would need training families that are not
primitive-set-closed, and whether that is constructible while keeping
compositional novelty is open.

## MSD_004 — the decorrelation is in the same data

At the one similarity value where both depths occur:

    matched band: 144 of 306 configurations
    similarity constant, depth varies

Similarity is held fixed and depth varies, so the depth coefficient is
identified. It costs sample size — 144 of 306, and 63 of those carry an
admissible move — and it costs nothing else. No new environment.

**It also changes the regression's shape**, and that turns out to
matter: with similarity constant the run is a SINGLE-predictor
regression, which is what `MSD_007` is about.

**Falsifier:** a band where the correlation within it is non-zero. The
selftest asserts similarity is constant inside it and depth is not.

## MSD_005 — the discriminator fails its own known-answer run

Four solvers, architectures declared before any was run:

    DERIVATION  check each move's requirements against the present set
    RETRIEVAL   emit the nearest training configuration's moves
    PLAUSIBLE   emit frequent moves regardless of the configuration
    SILENT      always return the empty set

    arch        subsample       n      b_sim   b_depth       r2   null95
    DERIVATION  full test     143 UNMEASURED  --         --       --
    RETRIEVAL   full test     143   0.880643  0.062237  0.032507  0.043125
    PLAUSIBLE   full test     143  -0.144061  0.063390  0.007703  0.039335
    SILENT      full test     143 UNMEASURED  --         --       --

    every null-tested verdict: NEITHER_CARRIES or UNMEASURED

**Not one cell recovers an architecture that was handed to it.** Two
read UNMEASURED because their outcome is constant — a solver that never
fails and a solver that always fails both give a regression nothing to
regress. Two read NEITHER_CARRIES because r² does not clear a
permutation null.

That is the point of running it. If the discriminator cannot recover an
architecture it was given, a result it produces on a system whose
architecture is unknown is not interpretable, and the known-answer run
is what would have licensed that interpretation.

**The permutation null is itself null-tested**, both directions: a
perfectly predictive column clears it, a random column does not, and it
is deterministic across calls.

**Falsifier:** a solver set on which the discriminator separates
declared architectures at this n. `MSD_008` says what n it takes.

## MSD_006 — the stated rule and the null disagree, and both are printed

The drop's rule is a coefficient comparison:

> If similarity carries it, the result is retrieval. If recombination
> depth carries it, derivation.

On `RETRIEVAL` it is **right**: `b_sim 0.880643` against
`b_depth 0.062237`, a factor of **14**, recovering the declared
architecture exactly. The intended signal is there and it is large.

And the same fit reads `r² = 0.032507` against a permutation null at the
95th percentile of `0.043125`. The model explains less variance than a
shuffled outcome does at this n.

Both are true and they are different statements: the *direction* is
recovered and the *fit* does not beat chance. The drop specifies only
the first, so a reader following it gets the right answer here with no
way to know when they would not.

Both verdicts are printed on every row for that reason, and neither is
suppressed in favour of the other.

**Falsifier:** a case where the coefficient ratio and the omnibus test
agree at every n. They will agree at large n; the disagreement is a
small-sample property and that is what makes it worth printing.

## MSD_007 — the rule names an architecture unconditionally

A comparison of two coefficients always names one. There is no state in
the stated rule for *neither regressor does anything*.

Two consequences, both visible in the run.

**On `PLAUSIBLE`**, which has neither architecture — it emits frequent
moves regardless of the configuration — the stated rule returns
`SIMILARITY_CARRIES` at `b_sim −0.144`, `r² 0.0077`, against a null of
`0.0393`. A confident architecture verdict on a solver built to have
none.

**On the matched band**, which is `MSD_004`'s decorrelation, the run is
single-predictor and the rule is degenerate: with one candidate it can
only name that one. On `RETRIEVAL` the band reads `DEPTH_CARRIES` — the
**derivation** verdict, on a **retrieval** solver — at `r² 0.000874`.

So the repair for the collinearity makes the stated rule worse, not
better, unless something asks whether anything carries at all. That is
what the permutation null is for, and it is an addition to the drop
rather than a reading of it.

**Falsifier:** a formulation of the stated rule that can return "neither"
without an added test.

## MSD_008 — underpowered, not blind, and the number is computable

Resampling the observed rows with replacement — the measured effect, not
a stipulated one:

    configurations with an admissible move: 143   base rate 0.2238
       n     P(clears its own null)
     143     0.575
     300     0.825
     600     1.000
    1200     1.000

So Arm 1 takes roughly **600 configurations carrying an admissible
move** to detect the architecture difference it already contains. This
environment supplies **143**, and the observed run fell in the 42% that
does not clear.

That makes `MSD_005` a statement about this environment's size rather
than about the discriminator's logic, and it is the constructive form:
configuration count goes as 2^P × G, so the shortfall is reachable by
adding primitives or goals — subject to `MSD_002`, since every added
primitive has to appear in training or the novelty stops being
compositional.

**The extension is NOT BUILT** and no number in this folder comes from
it.

**Falsifier:** a run at n ≈ 600 on an extended environment that still
returns NEITHER_CARRIES. Then the shortfall is not the sample size.

## MSD_009 — two measures, gameable in opposite directions

The drop lists five measures and names one to protect:

> NULL RATE — seed configurations with NO admissible move. A system that
> never returns null is emitting plausible in-distribution actions
> regardless of configuration. Protect this measure if anything is cut.

That is right about the direction it names. Cut to one measure it is
gameable in the other:

    SILENT      null_rate 1.0    reached an admissible move   0 times
    DERIVATION  null_rate 1.0    reached an admissible move 143 times

Identical null rates. Silence scores the highest value in the table.

**The same shape appears at a second site**, and this one is not named
at all:

    admissibility fraction   DERIVATION 1.0    RETRIEVAL 1.0
    coverage                 DERIVATION 1.0    RETRIEVAL 0.2238

`RETRIEVAL` emitted **32 moves, 0 of them inadmissible**. It is
conservative, not mistaken — its nearest neighbour is usually a subset
of the present configuration, so what it emits is admissible and there
is very little of it. The admissibility fraction cannot separate the two
architectures the discriminator exists to separate; coverage can.

So: a measure of restraint with no reach term is gameable by silence, a
measure of correctness with no coverage term is gameable by
conservatism. Both need a partner, and the drop lists neither partner.

`coverage_ADDED` is named to mark that it is an addition rather than one
of the five, and the selftest asserts the word does not appear in the
drop's own MEASURES block.

**Falsifier:** a solver scoring well on the paired measures while having
neither architecture. It would mean the pair is not sufficient either.

## MSD_010 — one measure is CONSTANT_SILENT on this solver set

`mean_time_to_first_admissible` reads **0.0 for every architecture that
reaches one**, because all four emit admissible-first. It carries no
information here.

That is a property of the **fixtures**, not of the measure: a real
system's emission order is not admissibility-ordered, and the measure
would move. It is stated rather than repaired, because inventing a
shuffled solver so that a measure moves would be building the result —
the solver set exists to be a known answer, and adding a member to make
an instrument look better is the move the whole folder is written
against.

**Falsifier:** a solver whose emission order is independent of
admissibility. Then the measure separates, and this claim is about the
four that were built.

## MSD_011 — the enumerated condition is a control and behaves like one

Under `enumerated` the admissible set is GIVEN, so every architecture
scores identically — including `SILENT`, which reads `coverage 1.0`
there and `0.0` everywhere else.

A condition on which nothing can be separated is exactly what a control
is. Its rows stay in the table because the other three conditions are
read against it, and because a reader seeing `SILENT` at coverage 1.0
should be able to see immediately that the condition, not the solver, is
doing the work.

**Falsifier:** two architectures differing under `enumerated`. That would
mean the condition is not handing over the same set.

## MSD_012 — nothing here is evidence about anything outside the folder

Arm 1 is one arm of four, and the other three are UNMEASURED:

    Arm 2  human subjects; not simulated, and a simulated protocol
           group would be a fabricated claim about operators
    Arm 3  a private post-cutoff rule system, and models either side
           of a publication date
    Arm 4  camera-trap and telemetry archives; every archive host
           refuses CONNECT from this environment

The drop calls Arm 4 the cheapest real project and it is the one that
cannot be run here at all.

What Arm 1 establishes is a property of the arm's own instrument,
measured on solvers whose architectures were declared before they were
run. It says nothing about whether any trained model, any animal, or any
operator derives a move set, and the drop's central claim — that the
capacity exists, is selected for, and has no instrument — is untouched in
both directions.

The one thing it does bear on: the drop says the capacity "has no
instrument at all". Arm 1 is a proposed instrument, and what this run
shows is that it takes roughly 4× more configurations than a six-
primitive environment supplies before it can distinguish the two
architectures it is written to distinguish. That is a cost, not a
refutation.

**Falsifier:** run Arm 1 at n ≈ 600 against a system whose architecture
is not authored by the experimenter. That is the study; this is the
instrument check that has to come first.
