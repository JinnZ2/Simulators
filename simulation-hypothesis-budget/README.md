# simulation-hypothesis-budget

What a Planck-resolution simulation of the observable universe would cost in
energy, and which of those numbers mean anything.

`budget.py` — uniform resolution. stdlib, selftest 15/15.
`multiscale.py` — the same budget when resolution is *not* uniform. stdlib,
selftest 13/13, imports `budget.py` and does not modify it.
`consequence_frame.py` — what the hypothesis *licenses* rather than what it
costs. stdlib, selftest 14/14, imports both and modifies neither. CC0.

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
| **DECIDABLE** | counts and floors computed in our physics, about a simulator embedded in our physics | real numbers |
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

Three terms are required before any cost figure has a value — the level stack
(`SHB_010`), the consistency term (`SHB_009`), the frame of the ratio
(`SHB_003`). All three are established here and none is stated in any version
of the hypothesis. **A figure quoted without them is not a disputed number; it
is a quantity with no value yet.**

See [`CLAIM_TABLE.md`](CLAIM_TABLE.md) for the falsifiers.
