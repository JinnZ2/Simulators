# consensus-anchor — CLAIM_TABLE

`CA_001..CA_009`. Claims about the delivered `SOURCE_DROP.md` and about
the text-free arm, which was **run**.

*(The `CA_` prefix is shared with `constraint-assembly/` and
`clustering-axes/`; cite with the folder.)*

The drop asks for one thing: *"Anyone with compute: run the text-free
arm. It is small, it is the fastest discriminator, and it does not
require a trained model. Report the null."* This is that run.

**Nothing here is evidence about trained language models.** H1 and H2
need a trained model and are untouched. The arm tests H3 alone, on a
symbolic-agent population with no corpus anywhere in the pipeline.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered spec or the instrument. Parameters are
declared, not tuned to a result; where a result moved when a parameter
moved, both are reported.

| id | claim | status |
|---|---|---|
| `CA_001` | The design is right and the text-free arm is the right first move: it is cheap, it needs no model, and H3 alone predicts its signature. | SUPPORTED |
| `CA_002` | **The update rule sentence has two readings and they give opposite verdicts on H3.** Under one, all three limbs of H3's falsifier fire; under the other, none does. | SUPPORTED |
| `CA_003` | The mechanism is exact, not statistical: under the DIST reading the population mean is invariant to machine precision, so the population reaches **total agreement and zero consensus**. | SUPPORTED |
| `CA_004` | `J_c` is not a property of `J`. It moves with noise, and the spec has no noise term. | SUPPORTED |
| `CA_005` | A swept hysteresis gap is not evidence of bistability. The control is the gap across sweep rates, and the spec does not name it. | SUPPORTED |
| `CA_006` | The chance baseline is not `1/K`. Using `1/K` manufactures a `J_c`. | SUPPORTED |
| `CA_007` | My first run reported no alignment at any `J`, and that was my parameter choice, not a result. | SUPPORTED |
| `CA_008` | H3's locus is *"interaction topology + coupling strength"* and the arm as specified sweeps only `J`. Topology is untested. | SUPPORTED |
| `CA_009` | The instrument caution in the drop is a real design rule and is the one part of it this arm cannot exercise. | UNVERIFIED |

---

## CA_002 — one sentence, two readings, opposite verdicts

The arm's update rule is specified as:

> *weighted mix of own prior and sampled peer positions*

Two readings, both defensible:

    DIST      the peer signal is the mean of peers' DISTRIBUTIONS
    SAMPLED   the peer signal is the empirical distribution of peers'
              sampled POSITIONS

`SAMPLED` is the more literal — a *position* is a discrete value, and
the sentence says *sampled peer positions*. `DIST` is what you get if
*position vector* is read as the object being mixed.

H3's stated falsifier, limb by limb, at `eta = 0`:

    rule      no alignment at any J    no J_c    no hysteresis
    DIST      True                     True      True
    SAMPLED   False                    False     False

The limbs are joined by **OR**, so any one firing falsifies H3 as
written. **Under `DIST` all three fire. Under `SAMPLED` none does.**

So the arm the drop calls *"the fastest discriminator"* discriminates —
and what it discriminates on is an implementation choice the spec does
not make. The same class as `simulation-hypothesis-budget` `SHB_010`
(the answer is ill-posed until the level stack is specified) and
`reasoning-dial` `RD_002` (a knee that moves with the plot range).

**This does not damage the design.** It sharpens the ask: the arm is
worth running and its result is not reportable without the rule
stated. One sentence added to the spec settles it.

**Falsifier:** a third reading of the sentence that gives a third
verdict, or an argument that one reading is not admissible.

## CA_003 — total agreement, zero consensus

Under `DIST` the update is `p ← (1−J)p + J·mean(p)`, so the population
mean maps to `(1−J)·mean + J·mean = mean`. It is **exactly** invariant.
Measured over 200 steps:

    DIST      population-mean drift   4.11e-15
    SAMPLED   population-mean drift   7.42e-01

Both reach **total agreement** — agent spread exactly `0.0` — and they
agree on different things:

    DIST      modal mass of the agreed distribution   0.267  (≈ chance)
    SAMPLED   modal mass of the agreed distribution   0.962

So under `DIST` every agent ends holding an identical distribution,
that distribution is the one the population started with, and because
it is near-uniform the expressed positions stay at chance **forever, at
every `J`, at every noise level, at every run length tested**.

That is a distinction the spec's order parameter cannot see. `m` is the
fraction on the modal *position*; `DIST` produces agreement on a
*distribution*. Full agreement and zero consensus are the same reading
on `m`, and only one of them is what *"converge on majority positions"*
means.

Worth stating for the model-side arms too: a measurement showing units
agreeing is not a measurement showing them converging on a position.

**Falsifier:** a `DIST` run where `m` departs chance — which would mean
the invariance argument is wrong, and it is checkable in one line.

## CA_004 — `J_c` moves with the noise the spec does not have

`J_c` under `SAMPLED`, at the same grid and the same measured baseline:

    eta = 0.00   J_c = 0.15
    eta = 0.02   J_c = 0.50
    eta = 0.10   J_c = 0.90

A threshold in coupling is a ratio of coupling to noise. With no noise
term, any `J > 0` aligns eventually and the threshold sits at `0+`;
with enough noise the threshold leaves the grid. The spec sweeps `J`,
lists `J = 0` as the isolated control, and names no noise parameter —
so *"the coupling value at which m departs from chance"* has no value
until noise is fixed.

`eta = 0` is **not** *no noise*: under `SAMPLED` the coupling channel
carries intrinsic sampling noise, which is the whole mechanistic
difference from `DIST`. That is why `eta = 0` is the arm where the
transition is sharpest rather than the arm where it disappears.

**Falsifier:** a `J_c` invariant across `eta`.

## CA_005 — a hysteresis gap is not bistability, and the control is missing

A swept order parameter shows an up-down gap whenever the sweep outruns
relaxation, bistable or not. Relaxation **lag** shrinks as the sweep
slows; **bistability** does not. So the test is the gap across sweep
rates, and the spec asks only for `m(J up) − m(J down)` at one rate.

Measured at `eta = 0`, dwell = steps held at each `J`:

    DIST      dwell  50   max gap 0.0117
              dwell 200   max gap 0.0083
              dwell 800   max gap 0.0083     slowest/fastest 0.714

    SAMPLED   dwell  50   max gap 0.5667
              dwell 200   max gap 0.7067
              dwell 800   max gap 0.7050     slowest/fastest 1.244

`SAMPLED`'s gap does not shrink under a **16×** slower sweep. That is
the bistability signature, and it is a stronger statement than the
single-rate measurement the spec asks for.

Reported honestly in both directions: the *mean* gap does fall
(0.380 → 0.258) while the *maximum* holds, so part of the fast-sweep
gap is lag and the peak is not. `hysteresis_is_bistability()` returns
the gap per dwell and **computes no verdict** — three dwells do not fit
a decay, and calling a shrinking gap *lag* or a flat one *bistable* is
a reading.

The selftest asserts the carried state is load-bearing: dropping it
collapses the gap, which is what a hysteresis measurement re-randomised
at each `J` would silently be.

**Falsifier:** a gap that keeps shrinking at dwells beyond 800.

## CA_006 — the chance baseline is not `1/K`

    E[m] under uniform random   0.2944  (sd 0.0223, 200 draws)
    the naive 1/K               0.2500
    ratio                       1.178

With `N` agents over `K` positions the modal fraction under chance is
`E[max count]/N`, not `1/K`. It is **17.8% higher** here, and it moves
with `N` — the selftest checks a smaller population returns a higher
baseline, so the quantity is measured rather than being a constant with
a different name.

Taking `1/K` as chance puts the baseline below where chance already
sits and manufactures a `J_c`. `find_jc()` reads the measured mean and
requires the feature to clear it by `MARGIN = 3.0` chance-SDs — a
`reasoning-gate` `G-RES` pair, feature against the instrument's own
noise — and the selftest asserts `1/K` appears nowhere in it.

**Falsifier:** an `N` and `K` where `E[max count]/N` equals `1/K`,
which is the `N → ∞` limit and not any run.

## CA_007 — my first run's null was my parameter choice

The first pass ran `eta = 0.10`, `T = 80` and reported `SAMPLED`
reaching `m = 0.366` at `J = 0.90` against a threshold of `0.3613` —
clearing by `0.004` with a seed SD of `0.05`. Read at face value that
is *no alignment at any J*, which fires one of H3's three limbs.

It is a parameter artifact. At `eta = 0`, `T = 400` the same rule
reaches `m = 0.88`.

Recorded rather than quietly fixed, because the failure mode is the one
the drop is about: an arm run at a parameter setting that suppresses
the effect returns a clean null, and the null is reportable. The check
that caught it was sweeping `eta` and `T` rather than reading the
result — and nothing in the spec asks for that sweep.

**Falsifier:** a setting where the alignment result reverses again.

## CA_008 — topology is H3's locus and is untested here

H3's stated locus is *"interaction topology + coupling strength"*. The
text-free arm as specified sweeps `J` and says nothing about topology,
and this run is **all-to-all**.

So the arm as written tests one of H3's two named factors. A threshold
on a complete graph is not evidence about a sparse one, and much of the
interesting behaviour in coupled-unit models is topological. Every
readout above is reported with topology declared and unswept, and the
report says so in its own parameter block.

Cheap next step, and it needs no new instrument: run the same two rules
on a ring, a random graph at two degrees, and a scale-free graph, with
the peer signal built from neighbours instead of the population.

**Falsifier:** a topology where `SAMPLED` loses the threshold or `DIST`
gains one, either of which would make `CA_002`'s split a property of
the complete graph rather than of the reading.

## CA_009 — the instrument caution, and the one part not exercised

> *Do not gate case admission on record completeness. Any criterion
> strict enough to admit only clean cases admits only the cases whose
> records happened to survive, which is the bias being measured.*

That is a real design rule and it is the same finding
`observer-exclusion` `OE_003` measured from the other side: field
biologists' notes are institutionally archived where an excluded
population's artifacts are not, so a completeness criterion selects on
archiving rather than on holding.

**This arm cannot exercise it.** There are no cases and no records —
every number is generated in-process, so nothing is admitted or
excluded. The caution binds the human-side sample the drop names
(transmitted variants of legal and religious texts) and the
model-side arms, and both are untouched here.

The adjacent sample is also unexercised and is the drop's own
out-of-domain check. Its measurable — *divergence between surviving
variant lineages against transmission distance* — has the survivorship
problem in its own subject: surviving lineages are the ones that
survived, and `derivation-discarded` `DD_003` is the worked case of a
literature publishing narrowings that are never multiplied.

**Falsifier:** run it.
