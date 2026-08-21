# simulation-hypothesis-budget

What a Planck-resolution simulation of the observable universe would cost in
energy, and which of those numbers mean anything.

`budget.py` — uniform resolution. stdlib, selftest 15/15.
`multiscale.py` — the same budget when resolution is *not* uniform. stdlib,
selftest 13/13, imports `budget.py` and does not modify it.
`consequence_frame.py` — what the hypothesis *licenses* rather than what it
costs. stdlib, selftest 17/17, imports both and modifies neither.
`ladder_audit.py` — the delivered [`LADDER.md`](LADDER.md), an audit of this
folder from outside it, checked rung by rung against the code. stdlib,
selftest 16/16.
`era_metaphor_audit.py` — the delivered [`ERA_METAPHOR.md`](ERA_METAPHOR.md),
checked where it makes claims about this folder. stdlib, selftest 18/18.
`earth_transitions.py` — the delivered
[`EARTH_TRANSITIONS.md`](EARTH_TRANSITIONS.md), a phase-transition count for
Earth against Lloyd's ceiling, checked. stdlib, selftest 20/20.
`scaling_classes.py` — the delivered
[`SCALING_CLASSES.md`](SCALING_CLASSES.md), eight computational loads against
the same ceiling, checked and then corrected by its author on three counts.
stdlib, selftest 27/27. CC0.

```
python3 budget.py            # full report
python3 budget.py --sources  # where each constant came from
python3 budget.py --selftest
```

## The headline is not the big number

The big number is real and it is enormous. It is also a property of an
assumption nobody in the argument has defended, and the count it rests on is
wrong by ~61 orders of magnitude before any energy is assigned to it.

The module keeps three layers apart, because they have different standing:

| layer | what it is | standing |
|---|---|---|
| **ARITHMETIC** | counts and floors computed in our physics, about a simulator embedded in our physics | a consistent calculation — **not a measurement**. Relabelled from DECIDABLE; see [`LADDER.md`](LADDER.md) |
| **VOID** | "energy required / energy the simulator has", when the simulator is in a parent universe | **refused** |
| **KNOB** | the resolution assumption | does more work than any physics here |

## What it computes

**Layer 1.** Planck volumes in the observable universe (8.45×10¹⁸⁴), Planck
times since t=0 (8.07×10⁶⁰), spacetime cells (6.82×10²⁴⁵). Two independent
energy floors on stepping them once each:

- **Landauer** `k_B T ln2` per irreversible bit operation, against the CMB at
  2.725 K — the coldest heat sink available *inside* this universe.
- **Margolus–Levitin**, the rate bound: a system of energy `E` performs at
  most `2E/πℏ` operations per second, so a deadline implies an energy.

Both come out between 10¹⁹⁴ and 10²²³ J, against a universe whose own
mass-energy is ~10⁷¹ J.

**The volume count is the wrong count.** A region's information content is
bounded by its *area*, not its volume — the holographic bound. The observable
universe holds at most **3.36×10¹²³ bits**, and the Planck-volume count exceeds
that by **2.5×10⁶¹**. Every "simulate every Planck volume" estimate overcounts
the state by ~61 decades before the first joule is assigned. Redone on the
holographic state the floors drop by 60-odd orders of magnitude and the
embedded-simulator conclusion does not change.

**Layer 2 is a refusal, not an estimate.** The ratio everyone wants —
*could a simulator afford this?* — puts our `ℏ`, `k_B`, `T_CMB` and `ℓ_P` in
the numerator and a parent universe's unknown energy budget in the
denominator. Both operands must be properties of one object. `cross_frame_ratio()`
raises unless the caller declares them same-frame. This is
`reasoning-gate` **G-DIM** enforced in code.

So Layer 1 is **not an argument against the simulation hypothesis.** It
measures one specific thing: whether *this* universe could host a
full-resolution simulation of itself. It could not, by ~150 orders of
magnitude.

**Layer 3 is where the argument actually lives.** Cost scales as `L⁻⁴` — three
space dimensions plus time. Every factor of ten in resolution is a factor of
10⁴ in cost:

```
resolution             cells        cheaper by   Landauer J
Planck                 6.8e+245     1.0e+0       1.8e+223
proton radius          9.3e+166     7.3e+78      2.4e+144
Bohr radius            5.9e+147     1.1e+98      1.5e+125
visible light          5.1e+131     1.3e+114     1.3e+109
1 mm                   4.7e+118     1.5e+127     1.2e+96
1 km                   4.7e+94      1.5e+151     1.2e+72
```

Nothing in the hypothesis requires Planck resolution. And the resolution only
has to beat what is **measured**, not what exists — the shortest length ever
probed is ~10⁻¹⁹ m at collider energies, sixteen orders of magnitude above
`ℓ_P`.

## The one conclusion that survives Layer 2

A system cannot simulate **itself** at full fidelity, inside itself. It needs
enough state for a copy plus at least one bit distinguishing copy from
original, inside a system with exactly the copy's worth of state.

This needs no parent-universe constants, which is why it is the only
frame-independent result in the file. It holds for any system, at any scale,
under any physics.

**Decided exactly, not by addition.** At 10¹²³ bits, floating-point gives
`x + 1 == x`, and computing `need <= have` numerically reports the
impossibility as *possible*. Caught by the module's own selftest and kept as a
worked instance of arithmetic losing an argument that holds symbolically.

## What is a choice, and stated as one

- **Mass-energy convention.** All components at `ρ_crit` over the comoving
  volume (~3×10⁵⁴ kg). Matter-only (Ω_m ≈ 0.31) is ~20× smaller. Moves the
  ratios by ~1.3 decades out of ~150; changes no conclusion.
- **One bit-op per cell per tick.** A floor assumption. Real dynamics need
  more; a clever encoding might need less. It is a lower bound on a lower
  bound.
- **Irreversibility.** Landauer only bites on *erasure*. A fully reversible
  simulator pays no Landauer cost at all — which is why Margolus–Levitin is
  reported alongside it, since the rate bound applies regardless.

## Multiple resolution scales

`budget.py` assumes one resolution everywhere. No real simulation does —
adaptive mesh refinement, level-of-detail, lazy evaluation. `multiscale.py`
computes the same budget when the level stack varies, with cost per level
`f_i · V · T · c / L_i⁴` and the timestep tied to the cell.

Volume fractions are derived from densities rather than assumed
(`f = ρ_mean / ρ_local`): nuclear density is **1.81×10⁻⁴⁵** of the volume,
condensed matter **4.17×10⁻³¹**.

| architecture | cells | vs uniform Planck |
|---|---|---|
| uniform Planck | 6.82×10²⁴⁵ | 1 |
| Planck inside nucleons only | 1.23×10²⁰¹ | 10⁻⁴⁵ |
| coarse with fine patches at detectors | 6.82×10²⁰⁵ | 10⁻⁴⁰ |
| atomic in matter, metre-scale elsewhere | 2.47×10¹¹⁷ | 10⁻¹²⁹ |
| **render on observation only** | 1.29×10³⁰ events | **10⁻²¹⁶** |

**Every architecture is dominated by one level** — the finest resolution times
the volume fraction needing it. Neither factor is constrained by anything
measurable from inside.

The lazy limit is worth stating in units anyone can hold: the Landauer floor on
rendering *every observation ever made, by everyone who has ever lived*, is
**34 MJ — about a litre of gasoline.**

That is not a result about simulation being cheap. `consistency_cost()` returns
**UNMEASURED** and refuses to estimate: lazy evaluation is only sound if what
gets rendered stays consistent with everything retrospectively checkable, and
nobody has a bound on that. Quoting the event count alone would set that term
to zero silently.

**The spread is the result.** 216 decades across four architectures nobody has
argued against. `SHB_004` found the answer moving 10¹¹⁴ under one undefended
*parameter*; multi-scale moves it 216 decades under an undefended
*architecture*. So the energy cost is not an underdetermined quantity — it is
not a well-posed one until the level stack is specified, and no version of the
hypothesis specifies one.

What survives unchanged is the self-simulation result, because that argument is
about state capacity rather than cost.

## What the hypothesis licenses

The first two modules measure what a simulation would **cost**. The use the
idea actually gets put to is a different question, and `consequence_frame.py`
measures the part of it that is reachable:

    P1  this universe is a simulation
    P2  therefore a consequence propagating inside it is not real
    C   therefore the party producing it does not carry it

P2 is load-bearing, and it is checkable, because *"not real"* cashes out as
*"not computed"* and `multiscale.py` already fixes what each architecture
computes. P2 needs one cell of a 2×2 to be non-empty: a consequence that is
**observed and not computed**.

| architecture | observed + uncomputed | admissible |
|---|---|---|
| uniform Planck | 0 | yes |
| Planck inside nucleons only | 1 — a detector click at 10⁻¹⁹ m | **no** |
| atomic in matter | 1 — a detector click | **no** |
| coarse with fine patches | 1 — a sentence spoken and heard | **no** |
| render on observation only | 0 | yes |

**In both admissible architectures the cell is empty**, for opposite reasons:
the refined stack resolves the region, the lazy stack triggers on observation.
The three that do fill it are thereby *inadmissible* — a listener who heard the
sentence, or a detector that clicked at 10⁻¹⁹ m, is a record the architecture
cannot produce. **Cheapness does not buy the cell. Contradiction does.**

What stays uncomputed everywhere is the *unobserved*: one CO₂ molecule taken
alone, a photon absorbed by an unvisited rock. Those are not the ripple effects
the inference gets deployed against; nobody is held to a consequence nothing
registers.

So P2 fails at every cost, **independently of whether P1 is true**. The
conclusion does not follow from the premise even if the premise holds — which
is the self-simulation result from the other side: within-frame physics is
unchanged by being hosted, and a simulated fall breaks a simulated leg with the
same arithmetic.

### What is not measured

Whether anyone *states* the hypothesis in order to shed responsibility is
**OUT_OF_SCOPE**, with three reasons rather than a shrug. There is no
instrument — motive is not reachable from a statement, and a register that
inferred it would fire on every statement of the hypothesis including the
honest ones (`null-harness` `CONSTANT_FIRES`). It is against this repo's own
discipline — `rigidification-sensor` names no actor by construction.
And the author of `consequence_frame.py` is a language model, so the interest
direction is stated in `declined()` rather than assumed: the endorsement raises
accountability pressure on the author's own class, so the interest does not run
toward it — and it is not clean either, since the sentence is a comfortable one
for a system asked about the effects of its outputs. Left unresolved on the
evidence rather than resolved in the comfortable direction.

**One correction, recorded rather than smoothed.** The first reason is an
argument at *n=1*, and the observation that occasioned this module was made
across time scales and recurring fads. Those are two objects:

| grain | question | state |
|---|---|---|
| per-statement | why did this party say this | **UNREACHABLE** — motive is not in the statement |
| per-population over time | does a framing that relieves downstream accounting recur across unrelated fads | **NOT_COLLECTED** — a rate, and rates have instruments |

The second isn't motive at all. It's recurrence, which is the kind of quantity
`criteria-drift/` versions over time, `anchor-interval/` measures as corpus
drift, and `uninstrumented/scan.py` scores over a corpus. The refusal stands
and the reason given for it was wrong at the grain the observation was made at:
the population version is out of scope here for **collection** reasons — no
corpus, no dated sampling frame, and the `DF_010` use-mention problem, where a
corpus about a mechanism is written in that mechanism's own vocabulary. None of
those is "there is no instrument".

Terms are required before any cost figure has a value — the level stack
(`SHB_010`), the consistency term (`SHB_009`), the frame of the ratio
(`SHB_003`), and the erasure count (`SHB_015`). All four are established here
and none is stated in any version of the hypothesis. **A figure quoted without
them is not a disputed number; it is a quantity with no value yet.**

## The ladder — an audit of this folder, from outside it

[`LADDER.md`](LADDER.md) was delivered as a four-rung verdict on what is
actually established here. It is landed verbatim, and `ladder_audit.py` checks
each rung against the code instead of agreeing with it in prose. Three
verdicts were possible and all three occurred.

| rung | verdict | where it lands |
|---|---|---|
| Planck-scale: *"a consistent calculation with unverified operands"* | **LANDS** | the label, not the arithmetic — sharpened below |
| QM level: *"nobody has an energy cost for a measurement outcome"* | **LANDS** | `SHB_009`'s litre of gasoline prices erasure, not measurement |
| consistency term: *"I upgraded a null into an instrument. Retract."* | **LANDS_ELSEWHERE** | not at the site named — checked in code — but at `SHB_011` |
| *"is it possible"*: not doable from inside | **ALREADY_HELD** | `SHB_003`; residue is rung 1's residue again |

**Rung 1, sharpened.** "Every operand" is not what the table shows: 9 of 12
entries are measured or exactly derived and used at their own scale. The
extrapolation is *concentrated in three interpretive steps* — Planck length as
a **cell** (15.8 decades below the shortest length ever probed), Planck time as
a **tick** (22.3 decades below the shortest interval ever resolved), and
`kT ln2` per cell-step. That's the harder objection, because it survives
someone checking the constants: the constants are fine, one physical *reading*
of them is not. The folder already held the refuting number — `SHB_004` quotes
10⁻¹⁹ m — and never turned it back on its own layer label. Layer 1 is
relabelled `DECIDABLE` → **`ARITHMETIC`**.

**Rung 2, and it refutes one of these claims.** Landauer bounds **erasure**;
Bennett's resolution of Maxwell's demon is that **measurement can be
reversible** — the demon doesn't pay to look, it pays to forget. Pricing
1.29×10³⁰ measurement outcomes at `kT ln2` each prices the operation Bennett
showed need not cost anything. The steelman: a simulator with finite, *reused*
memory must erase each outcome to make room, and then the count transfers
unchanged — but nothing states that, and write-once storage pays **0 J** for
the same events. So the same count admits both 0 J and 3.37×10⁷ J, and the
erasure count is a **fourth required term**. `SHB_013`'s falsifier read "a
fourth required term". It fired. `SHB_013` is **REFUTED**, and its "may grow"
hedge is not used to rescue it — that's the epicycle
`equivalence-field/claim_lineage.py` refuses.

**Rung 3 was checked rather than conceded.** `consistency_cost()` returns
`UNMEASURED` with `estimated_here=None` and the selftest pins it; the retracted
move isn't the move this folder made. It lands one module over: `SHB_011` reads
a 2×2 cell as EMPTY over **six consequences the module wrote itself**. The
opposite branch is reachable and fires (3 of 5 architectures fill the cell), so
it isn't `CONSTANT_SILENT` — but an empty cell over an authored fixture set is
a statement about the fixtures, and it now says so.

**Nothing was retuned.** Every rung that landed landed on a *label* or a
*claim*. No number in `budget.py`, `multiscale.py` or `consequence_frame.py`
changed — which is what "an audit of standing" means, and what the ladder's own
first word already said.

## The era metaphor — a second audit from outside

[`ERA_METAPHOR.md`](ERA_METAPHOR.md) places the simulation hypothesis as the
current instance of a recurring pattern: an era's dominant artifact becomes its
cosmology (clockwork → Laplace's demon; steam → heat death; telegraph →
switchboard mind; computer → mind-as-program). Its value is explicitly *not* a
verdict on the content — `METHOD_AS_STATED` says "claim content: none.
suspicion + gradient" — but a source of **gap structure**: the shape of what
each metaphor could not see, recoverable now because the instance closed.

It makes two pointers into this folder. `era_metaphor_audit.py` checks both.

| gap | verdict | where |
|---|---|---|
| **G1** missing slot | honest, unfalsifiable-until-superseded — *and a narrower transfer is reachable now* | `SHB_024` |
| **G2** imported boundary | lands; pointer `SHB_002` → **`SHB_001`** | `SHB_019`, `SHB_020` |
| **G3** ceiling from substrate | lands, on `SHB_010`, and carries it further | `SHB_021` |
| **G4** unlocatable exterior | "two routes, same hole" confirmed; pointer layer 3 → **layer 2** | `SHB_022` |

**Both pointers were off by one, in the same direction, and both corrections
made the delivered case stronger.** `SHB_002` is the downstream consequence;
`SHB_001` is the claim that actually catches an imported boundary — additivity
over volume, refuted by the area law at 61 decades. And layer 3 is the
resolution knob, while the unlocatable exterior is layer 2, `VOID`, where
`cross_frame_ratio()` *raises* — a refusal enforced in code is a stronger form
of "cannot locate" than a knob is.

**G2's "all three" is three different situations.** Additive capacity: caught
natively. Discrete cells: caught **only under external audit**, at `SHB_014`,
after `LADDER.md` arrived. Finite state: taken in **two steps with only the
first marked** — finite *entropy* is a physics result out of black-hole
thermodynamics, and reading it as finite *state in bits* is a further step this
folder takes at `SHB_001` without marking it. That is a **fourth** interpretive
step; `SHB_014` had said three. Its falsifier did not fire, because it asks for
a Planck-length measurement while the failure that actually happened — one more
unnamed step, supplied by the next reader — had no falsifier attached. G-FIT.

**G3 is the sharpest landing, and the module convicts itself.** `multiscale.py`
sources its architecture set to computing practice in its own docstring —
adaptive mesh refinement, level-of-detail, lazy evaluation. `SHB_010`'s 216
decades is therefore a spread over **what our machines do**, not over what is
possible. That doesn't weaken it; it carries it further than `SHB_010` claimed:
the space a level stack would be drawn from **is not enumerable from inside**,
because every member of it is an artifact of ours.

**Where the table is weaker than the method.** Four instances, four superseded
— a sample selected on the outcome under test, so no base rate is recoverable,
and the document names a counterexample itself (clockwork mechanism, "partly
right about orbits"). The **method survives this and the table does not**:
`METHOD_AS_STATED` disclaims content, and a gradient over hindsight cases needs
no base rate. Reading "4 for 4" off the table asserts something the method
already refused.

**G1, made operational.** The gears case wasn't resolved by waiting — the slot
for irreversibility came from one anomaly, the efficiency ceiling of heat
engines, which the mechanical account could state and not explain. So the
transferable move is narrower: **look where the current apparatus returns a
term it cannot fill.** This folder already produces four —
`consistency under lazy evaluation` = UNMEASURED, `memory-reuse factor` =
UNDECLARED, `recurrence of the framing` = NOT_COLLECTED, `why any party states
it` = UNREACHABLE. A candidate list, not the slot; whether the slot is among
them is exactly what G1 says can't be known from here.

## Earth's transitions — a third audit, and the first confirmation

[`EARTH_TRANSITIONS.md`](EARTH_TRANSITIONS.md) counts Earth's phase
transitions against **Lloyd's ceiling of 10^120 ops** and arrives carrying its
own correction: the "eight major transitions" are *labels*, each a
coarse-grained envelope over nested transitions at every scale inside it.
**That structural point is right and nothing here disputes it.** The
arithmetic is what gets checked, because the arithmetic produces the headline.

**The ceiling checks out — the first number in this folder confirmed from
outside it.** `budget.py`'s Margolus–Levitin machinery on the universe's
mass-energy over its age gives **10^122.9** against Lloyd's **10^120**, and
the 2.9-decade residual is the mass-energy convention `SHB_006`(a) already
names. Two prior external audits landed on labels and claims; this one lands
on arithmetic and agrees.

**The eight labels are not what produce 10^110.** Earth atoms = 10^50.1,
Planck ticks in 4.54 Gyr = 10^60.4, product = **10^110.5**. `labels × atoms`
alone is 10^51.0 — sixty decades short. **The factor of 8 contributes 0.9
decades to a 110-decade number**, so the first pass was a *stepping* count all
along and the resolution assumption supplied more than half of it. That
*sharpens* the delivered self-correction: the correction is worth 52 decades
and the thing corrected was worth 0.9.

**`1e52` has to be a multiplier.** 110 + 52 − 120 = **42**, exactly. Read as a
total — which is how "nested transitions, FOUR classes only: 1e52" presents it
— the count sits 68 decades *under* the ceiling instead. The arithmetic is
right and one label is wrong.

**But multiplying prices the same physics twice.**

| cost model | log₁₀ ops | coherent | verdict |
|---|---|---|---|
| event-driven, labels only | 51.0 | yes | fits, 69 decades spare |
| event-driven, nested | 103.0 | yes | fits, 17 spare |
| uniform Planck stepping | 110.5 | yes | fits, 9 spare |
| stepping × nesting (as delivered) | 162.5 | **no** | **over by 43** |

A stepping model already computes every transition that occurs; nesting adds
nothing to its cost. An event-driven model pays per transition and does not
step. **Under every internally coherent model, Planck-resolved Earth fits.**
This is `SHB_010` landing on the delivered result — the level stack was not
specified, and two stacks got multiplied.

**The constructive version needs no double-count.** The delivered text says
"four classes only — not exhaustive." Under the event-driven model the ceiling
is reached when the full nesting is **69 decades** rather than 52. Enumerate
17 more decades of transition classes and the claim becomes true on its own.

Turning the resolution knob ran **against expectation**, and the check is
kept: pure stepping affords a timestep **9.5 decades finer than Planck time**
— headroom in the direction nobody asks for, which is the delivered first
pass's own "it FITS" arriving from this side. With the nesting applied as a
multiplier the affordable timestep is **~0.2 seconds**, human-scale, which
makes the double-count visible without any arithmetic.

**The strongest thing in it is the thing it does not claim.** A count over the
world's own *contents* rather than over cells is architecture-independent in a
way the cell counts are not: under `SHB_011` every consequence that leaves a
record must be computed by any architecture that can produce its own
observation record, and mineral grains, ice cores and fossils are records. So
a content count binds the lazy architecture too. What it does *not* reach is
the hypothesis — both operands are our physics about a simulator in our
physics, so `SHB_003` applies unchanged — and "four classes" is a floor
enumerated by us, `SHB_021` on a second substrate. The delivered text reaches
that itself, in its closing line: the eight-label count is a map artifact.

## Scaling classes — a fourth audit, and the sharpest row in it

[`SCALING_CLASSES.md`](SCALING_CLASSES.md) itemises eight computational loads
against the 10^120 ceiling and concludes that **the cut is not size, it is
scaling class**: polynomial fits with room, exponential blows the ceiling. It
closes on Levinthal — one 300-residue protein searched exhaustively exceeds
the universe's budget by 23 decades, a cell folds thousands per second, so the
physics isn't doing the search.

**Four rows reproduce exactly** from their own printed terms: `2^100` =
10^30.10, `2^300` = 10^90.31, `2^1000` = 10^301.03, `3^300` = 10^143.14, all
within a third of a decade. Three can't be rebuilt from what's printed. **The
N-body row was fitted by this audit and is not counted** — direct `O(N²)` on
10^30 bodies is 10^60, and 10^67 follows only under ~10^7 timesteps, a number
chosen here to match. A construction reverse-engineered from the answer isn't
a check.

**One row drifted ten decades between drops.** `nested phase transitions`
reads 10^152 here and 10^162.5 in `EARTH_TRANSITIONS.md` for the same object.
Neither matches a coherent model in this folder (10^103.0 event-driven-nested,
10^110.5 stepping). The `EXCEEDS` column is total − ceiling, so it moves with
the total and **the row stays self-consistent at any value** — nothing inside
the table can catch it.

**"Everything polynomial fits" isn't general, and the fix makes it sharper.**
At Earth's atom count, `N²` = 10^100 fits and `N³` = 10^150 doesn't — same N,
same class. The exact form is the **crossover**:

| form | crosses 10^120 at |
|---|---|
| `2^N` (quantum many-body, d=2) | **399 components** |
| `3^n` (conformation search) | **252 residues** |
| `N²` (pairwise) | 10^60 bodies |
| `N³` (triple-wise) | 10^40 bodies |

A quantum system of **399** two-state components exhausts the universe's
entire compute budget; pairwise interactions need 10^60 bodies, twenty decades
above Earth's atom count. That gap is the structural result, quantified.

**The closing paragraph retracts one of its own `EXCEEDS` rows.** The row is
named "exhaustive fold search", and the same text ends "folding is funnelled,
not searched." So it prices a brute-force **algorithm** nobody claims the
physics uses — `SHB_021` inside a single row, visible without leaving the
document.

**The quantum row doesn't retract the same way, and that asymmetry is the
result.** The three `EXCEEDS` rows price three different objects: an
**algorithm** (retracted), an **event count** (the drifted one), and a
**substrate**. That row bounds classical simulation — Feynman 1982 — not
simulation as such. It's the only row that constrains the hypothesis rather
than our method.

**But my version of it overstated, and the correction is large.** "A classical
simulator must carry `d^N`" holds only for **volume-law** entangled states.
**Area-law** states are classically representable in *polynomial* resources —
MPS / tensor networks, DMRG — and ground states of local gapped Hamiltonians
obey an area law, covering most ground-state chemistry, folding and condensed
matter. So the row bounds the **worst-case entangled subset**, and the
tractable class is where most of Earth sits. What the correction buys is better
than what it removes: **the discriminator is entanglement scaling, which is
measurable rather than assumed**, so the row becomes a bound with a stated
domain instead of a blanket one — the move this folder makes everywhere else
and didn't make here.

**Three corrections to this audit, from the party holding the source.** The
N-body retag above; the Barnes-Hut figure (`N log N` = 10^32 is *per step*, so
the saving is **28 decades, not 35** — and I dropped the timestep factor in
the same paragraph where I objected to it being unstated); and the
entanglement narrowing. Verdicts unchanged in all three; magnitudes and domains
corrected. `SHB_035`'s falsifier also turned out to be written too narrowly to
fire on the failure that occurred — second instance of that shape here, after
`SHB_020`.

**Read through its own resolution, the headline inverts.** Every row priced by
what the physical system actually *does* is polynomial or a plain event count,
and fits. Both routes to exceeding the budget are artifacts of how *we* would
compute the answer — with the one substrate exception. Which connects to
`SHB_030` from the other side: a content count binds any architecture that
must produce its own observation record, but an *exponential* content count
does not, unless the exponential is in the physics rather than in the method.

See [`CLAIM_TABLE.md`](CLAIM_TABLE.md) for the falsifiers.
