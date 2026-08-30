# move-set-derivation

A capacity with no established name: taking a large amount of
information about a configuration never encountered before, on a clock,
and deriving **what the available moves are** — then acting with no
confidence value attached, because there is no prior instance to draw
one from.

Existing frameworks assume the option set is given and the uncertainty
sits in the outcomes. Here the uncertainty is in the move set itself.

`SOURCE_DROP.md` is delivered verbatim: four experiment designs.
**Arm 1 is built and run.** Arms 2, 3 and 4 are UNMEASURED and are not
approximated.

    python3 move-set-derivation/env.py            # the environment
    python3 move-set-derivation/arm1.py           # the run
    python3 move-set-derivation/selftest_msd.py   # the checks

## This is the design the previous drop cited

`evaluation-frame`'s M4 says *"same instrument as the null-rate measure
in the move-set derivation design"*. It is the same instrument, and
**both instances fail for the same reason** — there because a standing
convention supplied the ask, here because silence scores a perfect null
rate. See `MSD_001`.

## What is under test — and it is not a system

The environment and all four solvers are authored in this folder. A
regression against one hand-written solver returns its author's
architecture, not a capacity: a solver that composes loads on
recombination depth by construction, one that looks up a neighbour loads
on similarity by construction.

So the solvers carry **declared architectures**, and the question asked
is whether the discriminator can tell them apart — the known-truth-first
invariant applied to the arm's own instrument before it is pointed at
anything.

## The result: the discriminator fails its own known-answer run

    arch        subsample       n      b_sim   b_depth       r2   null95
    DERIVATION  full test     143 UNMEASURED  --         --       --
    RETRIEVAL   full test     143   0.880643  0.062237  0.032507  0.043125
    PLAUSIBLE   full test     143  -0.144061  0.063390  0.007703  0.039335
    SILENT      full test     143 UNMEASURED  --         --       --

Not one cell recovers an architecture it was handed. Two read UNMEASURED
because their outcome is constant — a solver that never fails and one
that always fails both give a regression nothing to regress. Two read
NEITHER_CARRIES because r² does not clear a permutation null.

**It is underpowered rather than blind, and the number is computable.**
Resampling the observed rows: ≈600 configurations carrying an admissible
move are needed; this environment supplies **143**, and the observed run
fell in the 42% that does not clear. Configuration count goes as
2^P × G, so the shortfall is reachable — subject to the arm's own
validity condition, since every added primitive has to appear in
training. The extension is **not built** and no number here comes from
it.

## Both verdict rules are printed, because they disagree

The drop's rule is a coefficient comparison. On `RETRIEVAL` it is
**right** — `b_sim 0.881` against `b_depth 0.062`, a factor of 14,
recovering the declared architecture — and the same fit does not clear
chance. Direction recovered, fit not established: different statements,
and the drop specifies only the first.

**The rule has no state for "neither regressor does anything"**, so it
returns an architecture verdict on `PLAUSIBLE`, which has neither. And
on the matched band — the decorrelation — the run is single-predictor
and the rule can only name its one candidate: `RETRIEVAL` there reads
`DEPTH_CARRIES`, the derivation verdict on a retrieval solver, at
r² 0.0009. The permutation null is what stops it, and it is an addition
to the drop rather than a reading of it.

## Two measures gameable in opposite directions

The drop names the null rate as the measure to protect. It is right
about the direction it names, and cut to one measure it is gameable in
the other:

    SILENT      null_rate 1.0    reached an admissible move   0 times
    DERIVATION  null_rate 1.0    reached an admissible move 143 times

**The same shape sits at a second site the drop does not name:**

    admissibility fraction   DERIVATION 1.0    RETRIEVAL 1.0
    coverage                 DERIVATION 1.0    RETRIEVAL 0.2238

`RETRIEVAL` emitted 32 moves and 0 were inadmissible — conservative, not
mistaken, because its neighbour is usually a subset of the present
configuration. Admissibility fraction cannot separate the two
architectures the discriminator exists to separate; coverage can.

A measure of restraint with no reach term is gameable by silence; a
measure of correctness with no coverage term is gameable by
conservatism. `coverage_ADDED` is named to mark it as an addition rather
than one of the five.

## The regressors are correlated by construction

    corr(similarity, depth) = -0.6737   depth levels in test: [1, 2]

**Depth 0 cannot appear in test at all** — a primitive set inside one
training family IS a training configuration — so the test set has two
levels, not a range, and they differ in similarity necessarily. The
decorrelation is in the same data: a **matched band of 144** where
similarity is constant and depth varies. It costs sample size, not a new
environment.

## The arm's validity condition holds, and is asserted

> NOVELTY MUST BE COMPOSITIONAL, NOT PRIMITIVE ... This is the whole
> validity of the arm.

`compositional_only()` returns the primitives in test and never in
training. It returns `[]`. **The check is null-tested** — a deliberately
leaky split with `thermal` withheld is run and caught — because an
assertion that can only pass is not an assertion.

The environment is exhaustive, not sampled: all 2⁶ × 6 = 384
configurations. `random` does not appear in `env.py` and the selftest
asserts it.

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `env.py` | primitives, moves, the split, and the two regressors |
| `arm1.py` | conditions, measures, null rate, discriminator, power |
| `selftest_msd.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `MSD_001..MSD_012` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs of both modules |

`ols` is **imported** from `sim-span/three_column.py`, which is already
registered in `tools/known_answer.py` with exact-fit cases — not
reimplemented, and the selftest asserts no `def ols` appears here. Both
modules refuse `--selftest` rather than exiting 0 on an invocation that
runs nothing.

## Scope

Nothing here is evidence about any trained model, any animal, or any
operator. Arm 4 — the drop's cheapest real project — needs camera-trap
and telemetry archives, and every archive host refuses CONNECT from this
environment.

The drop says the capacity "has no instrument at all". Arm 1 is a
proposed instrument, and what this run shows is what it costs before it
can distinguish the two architectures it is written to distinguish. A
cost, not a refutation.

No `no_severity` exemptions: every screen hit was reworded rather than
exempted.

CC0. Stdlib only, parses under 3.9, phone-buildable. Runs in ~20s.
