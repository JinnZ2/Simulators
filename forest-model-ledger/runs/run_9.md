# run_9 -- rebuild of the run-6 conserved model as the ledger base

```text
status     : COMPLETE
code       : runs/run_9.py
seed       : 0 (base cases) ; 0..9 (seed sweep)
params     : model/base.py DEFAULTS, hand-set, no tuning pass ; 300 yr ; RK4 dt 1/52 (1/104 for the dt check)
results    : N misclosure -5.062e-11, water -3.426e-13, overall PASS ; 80 fires ; grasses extinct
flags      : 6 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_9.py
feeds      : L0_N_BUDGET ; L0_WATER_BUDGET ; L0_LEAK_VS_NOISE ; L0_BOUNDARY_AUDIT ; L4_FIRE_FUEL_MOISTURE ; L2_GRASS_GROWTH ; L1_LEACHING
l0_closure : N CLOSED, water CLOSED, C / P / energy VOID
```

## Flow

```text
deposition 300.00 --> [S] --uptake--> [T] --payment--> [F]
                       ^   \--uptake--> [G]             |
                       |                 |  mortality   | turnover
                       +--decomp-- [Lt] [Lg] <----------+
                       |
        leaching 5.61 <+        fire: litter + grass --> volatilised 270.74 (out)
                                                     \-> ash to S
d_pools +23.65 = in 300.00 - out 276.35        misclosure -5.062e-11
```

Fire is the N outlet: 270.74 of 276.35 exported. With fire off the same
deposition leaves by leaching instead (200.86) and the pools hold +99.14.

## Cases (seed 0)

```text
case               N verdict  N misclosure   water misclosure   fires  grass < 1e-6 at yr
base               CLOSED     -5.062e-11     -3.426e-13         80     18.96
no_fire            CLOSED     -5.075e-11     -2.209e-13          0     20.50
planted_leak_0.3   LEAK       -7.264e+01     -2.645e-13         59     19.17
base_dt_half       CLOSED     +7.124e-11     -2.790e-12         79     18.96
```

Fire interval, base: mean 3.59 yr, sd 2.09 yr.
Final pools, base: S 0.3715  T 36.6196  G 0.0000  F 0.9468  Lt 3.6619  Lg 1.0482  W 0.6393.

## Seeds 0..9 (base)

```text
fires          75 .. 81
grass gone     year 18.96 .. 20.52, 10 of 10 seeds
N misclosure   -5.00e-11 .. -5.06e-11, 10 of 10 PASS
```

## Flags

```text
- The ~24 N unit leak of the pre-run-6 model is NOT verified. That code is not in
  this tree. What is verified: the rebuilt model closes, and the audit catches a
  leak when one is planted (-72.64). The planted leak is a test of the
  instrument, not a reconstruction.
- Closure is by construction for every transfer routed through the flux table.
  The audit detects paths outside the table. It does not test whether a flux
  has the right size.
- N misclosure is near-identical across seeds (-5.0e-11): deterministic roundoff
  in the accumulators, dominated by the constant deposition term. It is not
  evidence of anything beyond float64.
- 80 fires here vs 47 reported for run 6: not comparable. Different parameters;
  run 6's length and parameters are not on record.
- Grass extinction reproduces, and also occurs with fire OFF. In this rebuild
  the cause is competitive (soil N drawn down to ~0.4, plus shading), not fire.
  One hand-set parameter point; no sweep. Whether run 6 went extinct for the
  same reason is unknown.
- scipy is absent in the build environment (work order allows it). Integrator is
  a fixed-step RK4 in numpy. Halving dt moves fires 80 -> 79 and final T by 1.8%:
  the trajectory is not dt-converged to better than that; closure is.
```
