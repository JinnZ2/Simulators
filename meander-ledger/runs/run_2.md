# run_2 -- slot-1 probe on the toy: is lam/W set by width-scaled numerics?

```text
code       : runs/run_2.py
seed       : 0
params     : run_1 base ; neck 2 W and 0.5 W ; ds 0.25 W (dt 0.2) ; aspect 10 for 15000 steps
results    : neck 2 W 7.34 ; neck 0.5 W 7.78 ; ds 0.25 W 2.62 (sinuosity 1.90) ; aspect 10 still straight at 15000 steps (2.65 = noise floor)
flags      : 3 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_2.py (samples/run_2.sample.txt)
feeds      : L3_BEND_GROWTH_KINEMATIC ; L4_CUTOFF ; L5_WAVELENGTH_ESTIMATOR ; MC_002
l0_closure : sediment CLOSED in all 5 cases
```

## Flags

```text
- Not grid-converged: halving ds moves lam/W from 8.69 to 2.62 at similar sinuosity.
  No toy wavelength is admissible.
- The estimator (curvature sign changes) counts jitter-scale wiggles as inflections:
  the same failure the dataset's estimator shows (run_3). Same instrument class, two
  substrates.
- The neck threshold moves lam/W by ~15%; not the controlling term.
```
