# run_6 -- mass-conserving rebuild

```text
status     : COMPLETE
code       : runs/run_6.py
seed       : 2 (structure: trait, aff, niche) ; 0 (fire draws)
params     : in the code: nP 8, nF 4, dt 0.05 Euler, T 3000 (60000 steps), fire_thr 0.6 (sweep 0.3 / 0.5 / 0.8 / 1.2)
results    : OLD misclosure -0.020 -> -24.177 by end ; CONSERVED max |misclosure| 1.269e-09 ; 47 fires ; late biomass mean 0.359, swing 0.466, tree share 1.0
flags      : 4 (below)
provenance : OBSERVED -- original code, chat-side sandbox 2026-11-10, filed verbatim 2026-11-11 (sha256 b1ccd82ae2eef8ca...). Rerun in this tree 2026-11-11 on numpy 2.5.3: printed output matches the logged output line for line.
feeds      : L0_N_BUDGET ; L4_FIRE_FUEL_MOISTURE ; L2_GRASS_GROWTH ; BR_MASS_BALANCE
l0_closure : N CLOSED by the run's own audit (max |misclosure| 1.269e-09 at 31 checkpoints); not passed through ledger/toolkit/budget_closure.py ; water / C / P / energy not modelled
```

## Output (this tree, 2026-11-11)

```text
OLD misclosure (N units) at checkpoints: [-0.020 -0.911 -4.442 -8.554 -24.177]
CONSERVED misclosure max: 1.2691900863615047e-09
fires 47  biomass late mean 0.359  swing 0.466  tree share 1.0  Ls range 0.13 2.89
thr 0.3  fires 56  B mean 0.354  swing 0.505  Ls max 2.73
thr 0.5  fires 48  B mean 0.362  swing 0.503  Ls max 2.74
thr 0.8  fires 45  B mean 0.361  swing 0.508  Ls max 2.96
thr 1.2  fires 38  B mean 0.367  swing 0.582  Ls max 3.63
```

Flags

```text
- OPEN: grasses extinct (tree share 1.0)
- 47 fires now has a rate: 47 in T = 3000 time units at fire_thr 0.6. The time unit is not named in the code.
- the file header calls old() "run-4 equations"; FML_009 records the ~24 N unit leak as run 5's model
  (authors' correction 2026-11-10). Both statements are kept; neither is reconciled here.
- run_9 is a different parameter point (RK4, 300 yr, model/base.py); the two fire counts are still not comparable
- status COMPLETE is PROPOSED by the filing session: code in tree, output reproduced, no toolbox trigger on record
```

History: REPORTED with code / seed / params void until 2026-11-11, when the original code arrived from the chat side.
