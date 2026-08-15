# figures — the eight shipped PNGs

Checked in exactly as delivered in `sim_stack_results.zip`. Not
regenerated, not cropped, not recolored. The generator code was not
shipped, so these figures are the only primary evidence for the drop's
numbers.

Each entry below names what the panel shows and which claim in
[`../CLAIM_TABLE.md`](../CLAIM_TABLE.md) it bears on.

## SIM-B — fractal dimension (the decisive sim)

### `sim_b_point_sets.png`
The five point sets, one panel each. Read the panel titles — they carry
the sample sizes, and the sample sizes are the problem: Ammann-Beenker
12,000, Cascade **1,024**, Poisson 12,000, Lattice 12,100, Line 12,000.
The bounding boxes also differ (AB spans ±2, Cascade roughly x ∈ [−8, 18]
and y ∈ [−26, 5], the rest ±20), so the Cascade is both sparser and
differently shaped than everything it is compared against.

→ `AOS_003`, `AOS_004`

### `sim_b_boxcount.png`
`log N(s)` vs `log(1/s)`, one panel per set, single global fit. Gives
AB 1.769, Cascade 1.529, Poisson 1.852, Lattice 1.869, Line 0.979 —
none of which are the numbers in the report.

The saturation ceilings are visible here and are the clearest single
piece of evidence for `AOS_003`: the Cascade curve flattens at
`log N = 3.0` (= 1024 points), every other curve flattens at
`log N = 4.08` (= 12,000). The sparse set has a visibly shorter scaling
window.

→ `AOS_003`

### `sim_b_boxcount_local.png`
Local slope `d log N / d log(1/s)` per set, with the chosen fit window
shaded green. **This is the source of the report's headline table** —
AB 1.889, Cascade 1.555, Poisson 1.911, Lattice 1.964, Line 1.000.

Worth reading against `sim_b_boxcount.png`: the same data under a
different fit rule moves AB by 0.120 and the AB−Cascade gap from 0.240
to 0.334. The fit window is a free parameter with an effect comparable
to the effect being measured.

→ `AOS_003`, `AOS_004`

### `sim_b_sandbox.png`
**The figure that is not in the report.** Sandbox / mass-radius
estimator, `log M(r)` vs `log r`, global fit: AB 1.961, Cascade
**2.208**, Poisson 1.972, Lattice 1.995, Line **1.913**.

Two things at once. The Cascade now reads *above* Ammann-Beenker,
reversing the sign of the drop's headline quantity. And the Line — true
dimension exactly 1.000 — reads 1.913, so the estimator is broken.

→ `AOS_001`, `AOS_002`

### `sim_b_sandbox_local.png`
Sandbox with plateau fit windows: AB 1.946, Cascade 1.969, Poisson
1.930, Lattice 1.913, Line 1.844. The AB−Cascade separation collapses
to 0.023 — inside the report's own 0.021 finite-size baseline.

The Line panel is the diagnostic one: its local slope oscillates around
1.8–2.0 across the *entire* radius range, never approaching 1.0. The
sandbox failure is systematic, not a bad window choice.

→ `AOS_001`, `AOS_002`

### `sim_b_summary.png`
Bar chart of the reported box-counting dimensions, plus a zoomed panel
excluding the Line. This is the figure the report's verdict is built on,
and it shows only the estimator that separates. The sandbox numbers
appear in no summary figure.

→ `AOS_001`, `AOS_004`

## SIM-A — structure factor (exploratory)

### `sim_a_structure_factor.png`
Six panels. Top row: `S(k)` maps for AB and Cascade, and radial profiles
on a log scale. Bottom row: radial profile on a linear scale, peak
sparsity, diffuse floor.

The two `S(k)` maps are the ones to look at. AB shows a single bright
spot at the origin on an otherwise black field; Cascade shows nothing.
The eight-fold Bragg star that would signal Ammann-Beenker order is not
visible, because the linear color scale is dominated by the
forward-scattering peak at `S(0) ≈ 11,500`.

The top-right radial profile carries the part of the SIM-A reading that
does hold: AB oscillates with real structure out to |k| ≈ 20 while
Cascade is flat at ≈ 1, the signature of an uncorrelated set.

→ `AOS_006`, `AOS_007`

## SIM-C — threshold sweep (exploratory)

### `sim_c_threshold_sweep.png`
Left: mean band-edge splitting vs aperiodicity fraction `f`, with a ±1σ
band and the detected knee at f = 0.65. Right: |curvature| of that
curve, same knee marked.

The curvature panel has comparable peaks at f ≈ 0.45, 0.55, 0.65, 0.70,
0.80 and 0.90; the winner leads by no more than the scatter between its
neighbours. On the left panel the knee lands on a local *minimum* of the
splitting curve, and the σ band spans most of the rise.

→ `AOS_005`
