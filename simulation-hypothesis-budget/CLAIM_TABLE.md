# CLAIM_TABLE — simulation-hypothesis-budget

Six claims, `SHB_001..006`. Every number reproduces from
[`budget.py`](budget.py); the sample is pinned at
[`samples/budget.sample.txt`](samples/budget.sample.txt).

## REFUTATION_PROTOCOL

The constants are frozen and sourced (`--sources`). The claims are about what
follows from them. A failed check updates the claim, never the constants — and
where a claim rests on a stated *choice* rather than on physics, the choice is
named in the claim so it can be varied.

| id | claim | falsifier | status |
|---|---|---|---|
| `SHB_001` | **The Planck-volume count is the wrong count, by ~61 decades.** Information in a region is bounded by area, not volume: the observable universe holds at most **3.36×10¹²³ bits** against **8.45×10¹⁸⁴** Planck volumes, a ratio of **2.5×10⁶¹**. Every "simulate every Planck volume" estimate overcounts the state before assigning any energy. | a derivation of the holographic bound that scales with volume, or a demonstration that the simulated state must exceed the physical state | SUPPORTED |
| `SHB_002` | **Two independent floors agree that this universe cannot host a full-resolution simulation of itself.** Landauer (`k_B T ln2` at 2.725 K) gives 1.78×10²²³ J; Margolus–Levitin (rate bound over 13.787 Gyr) gives 2.60×10¹⁹⁴ J; the universe's mass-energy is 2.73×10⁷¹ J. On the *holographic* state the floors fall to 7.07×10¹⁶¹ and 1.03×10¹³³ J and still exceed it by 10⁶¹–10⁹⁰. The correction changes the exponent, not the conclusion. | a physical bound below both, or an encoding whose state is smaller than the holographic bound | SUPPORTED |
| `SHB_003` | **The ratio "energy required / energy the simulator has" is VOID across frames, and the module refuses to compute it.** The numerator uses our `ℏ`, `k_B`, `T_CMB`, `ℓ_P`; a parent universe need share none of them, and whether it has a Landauer limit at all is unconstrained from inside here. `cross_frame_ratio()` raises unless the caller declares same-frame — `reasoning-gate` G-DIM in code. **So Layer 1 is not an argument against the simulation hypothesis**; it is a measurement of self-hosting. | a measurement, from inside, of any parent-universe constant | SUPPORTED |
| `SHB_004` | **The resolution assumption does more work than any physics in the argument.** Cost scales as `L⁻⁴`. Planck → proton radius is ~19 decades of length and ~79 of cost; Planck → visible light is ~114 decades of cost. Nothing in the hypothesis requires Planck resolution, and the resolution only has to beat what is **measured** — the shortest length ever probed is ~10⁻¹⁹ m, sixteen decades above `ℓ_P`. An argument whose conclusion moves by 10¹¹⁴ under an undefended parameter is a statement about that parameter. | an argument that a simulation must resolve below what its inhabitants can measure | SUPPORTED |
| `SHB_005` | **Full-fidelity self-simulation is impossible for any system, and it is the only frame-independent result here.** A system needs state for a copy plus ≥1 bit distinguishing copy from original, inside a system holding exactly the copy's state. No parent constants required. **Decided exactly, not numerically**: at 10¹²³ bits float addition gives `x + 1 == x`, which reports the impossibility as *possible* — caught by this module's own selftest and kept as a worked instance of arithmetic losing an argument that holds symbolically. | a coding scheme in which a system's full state plus a distinguishing marker fits inside that state | SUPPORTED (holds) |
| `SHB_006` | **Three assumptions are choices, not physics, and are named.** (a) mass-energy at `ρ_crit` over the comoving volume rather than matter-only — ~1.3 decades out of ~150, no conclusion moves; (b) one bit-op per cell per tick — a lower bound on a lower bound; (c) **irreversibility** — Landauer bites only on erasure, so a fully reversible simulator pays none of it, which is why Margolus–Levitin is reported alongside, the rate bound applying regardless. | any of the three turning out to be forced rather than chosen | SUPPORTED (holds) |
