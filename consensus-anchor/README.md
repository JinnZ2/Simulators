# consensus-anchor

A gap spec asking which of three mechanisms anchors consensus
convergence in trained systems — and **the one arm it asks anyone with
compute to run, run.**

`SOURCE_DROP.md` is delivered verbatim. `textfree.py` is the text-free
arm; `selftest_textfree.py` is 38 checks; `samples/` is the pinned run.

    python3 consensus-anchor/textfree.py             # the report (~70s)
    python3 consensus-anchor/textfree.py --json
    python3 consensus-anchor/textfree.py --selftest

**No human corpus is read anywhere in this pipeline.** The agents hold
position vectors over an arbitrary discrete space with no semantics
attached, and the only inputs are integers and floats. **Nothing here
is evidence about trained language models** — H1 (inherited norm) and
H2 (objective) need a trained model and are untouched. The arm tests
H3 (structural coupling) alone, which is what it was specified to do.

## The result

**One sentence in the spec has two readings and they give opposite
verdicts on H3.**

The update rule is *"weighted mix of own prior and sampled peer
positions."* `SAMPLED` reads the peer signal as the empirical
distribution of peers' sampled **positions** — the more literal
reading, since a position is a discrete value. `DIST` reads it as the
mean of peers' **distributions**.

H3's stated falsifier, limb by limb, at `eta = 0`:

    rule      no alignment at any J    no J_c    no hysteresis
    DIST      True                     True      True
    SAMPLED   False                    False     False

The limbs are joined by **OR**, so any one firing falsifies H3 as
written. Under `DIST` all three fire; under `SAMPLED` none does. The
arm the drop calls *"the fastest discriminator"* discriminates — on an
implementation choice the spec does not make. One added sentence
settles it.

## Why the two readings differ, exactly

Under `DIST` the update is `p ← (1−J)p + J·mean(p)`, so the population
mean maps to itself. Measured over 200 steps:

    DIST      population-mean drift   4.11e-15
    SAMPLED   population-mean drift   7.42e-01

Both reach **total agreement** — agent spread exactly `0.0` — and they
agree on different things:

    DIST      modal mass of the agreed distribution   0.267  (≈ chance)
    SAMPLED   modal mass of the agreed distribution   0.962

So `DIST` produces **full agreement and zero consensus**: every agent
ends holding an identical distribution, that distribution is the one
the population started with, and because it is near-uniform the
expressed positions stay at chance at every `J`, every noise level, and
every run length tested.

That is a distinction the order parameter cannot see. `m` is the
fraction on the modal *position*; `DIST` produces agreement on a
*distribution*. Both read the same on `m`, and only one is what
*"converge on majority positions"* means — which is worth carrying to
the model-side arms, where units agreeing and units converging on a
position are also not the same measurement.

## Three things the spec leaves open, all declared

**`J_c` moves with noise, and there is no noise term.** Under `SAMPLED`:

    eta = 0.00   J_c = 0.15
    eta = 0.02   J_c = 0.50
    eta = 0.10   J_c = 0.90

A threshold in coupling is a ratio of coupling to noise. With none, any
`J > 0` aligns eventually and the threshold sits at `0+`. (`eta = 0` is
not *no noise*: under `SAMPLED` the coupling channel carries intrinsic
sampling noise, which is the whole mechanistic difference from `DIST`.)

**A swept hysteresis gap is not bistability.** A gap appears whenever
the sweep outruns relaxation. Lag shrinks as the sweep slows;
bistability does not — so the test is the gap *across sweep rates*, and
the spec asks for one rate. Measured:

    DIST      dwell 50 → 800   0.0117 → 0.0083   ratio 0.714
    SAMPLED   dwell 50 → 800   0.5667 → 0.7050   ratio 1.244

`SAMPLED`'s gap does not shrink under a **16×** slower sweep. Reported
in both directions: the *mean* gap does fall (0.380 → 0.258) while the
*maximum* holds, so part of the fast-sweep gap is lag and the peak is
not. The function computes **no verdict** — three dwells do not fit a
decay.

**Topology is H3's other named locus and is untested.** H3's locus is
*"interaction topology + coupling strength"*; this runs all-to-all and
sweeps only `J`. Cheap next step, no new instrument: the same two rules
on a ring, a random graph at two degrees, and a scale-free graph.

## Two instrument results

**The chance baseline is not `1/K`.** With `N` agents over `K`
positions the modal fraction under chance is `E[max count]/N` —
measured `0.2944` against a naive `0.2500`, **17.8% higher**, and it
moves with `N`. Using `1/K` puts the baseline below where chance
already sits and manufactures a `J_c`. `find_jc()` reads the measured
mean and requires `3.0` chance-SDs of margin; the selftest asserts
`1/K` appears nowhere in it.

**My first run's null was my parameter choice.** The first pass ran
`eta = 0.10`, `T = 80` and got `SAMPLED` clearing threshold by `0.004`
with a seed SD of `0.05` — read at face value, *no alignment at any J*,
which fires one of H3's limbs. At `eta = 0`, `T = 400` the same rule
reaches `0.88`. Recorded rather than quietly fixed, because it is the
failure mode the drop is about: an arm run at a setting that suppresses
the effect returns a clean, reportable null. What caught it was
sweeping `eta` and `T`, and nothing in the spec asks for that sweep.

## Files

| | |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim |
| `textfree.py` | the arm: two rules, measured baseline, `J_c`, hysteresis with a sweep-rate control, susceptibility, the invariance proof |
| `selftest_textfree.py` | 38 checks |
| `CLAIM_TABLE.md` | `CA_001..CA_009` with a REFUTATION_PROTOCOL |
| `samples/` | pinned run |

Stdlib only, parses under Python 3.9, deterministic given seeds, CC0.

Siblings: `simulation-hypothesis-budget/` (`SHB_010`, ill-posed until
the level stack is specified — the same shape as `CA_002`),
`reasoning-dial/` (`RD_002`, a knee that moves with the plot range),
`triad-playground/` (`TP_008`, decorrelation measured on shadow
panels — the same claim about correlated units on another substrate),
`null-harness/` (the known-null invariant the `J = 0` control is),
`observer-exclusion/` (`OE_003`, the survivorship problem the drop's
instrument caution names).
