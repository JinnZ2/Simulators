# simulation-hypothesis-budget

What a Planck-resolution simulation of the observable universe would cost in
energy, and which of those numbers mean anything.

`budget.py` — stdlib only, deterministic, selftest 15/15. CC0.

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

See [`CLAIM_TABLE.md`](CLAIM_TABLE.md) for the falsifiers.
