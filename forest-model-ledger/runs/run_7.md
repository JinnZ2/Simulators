# run_7 -- percolation grid vs mean-field ODE, drought sweep

```text
status     : COMPLETE
code       : runs/run_7.py
seed       : 3
params     : in the code: L 120, 12 reps, density 0.8, p = 0.2 + 0.75 * drought, one ignition at centre, BFS spread, drought 0.0 .. 1.0 step 0.1
results    : ODE / grid ratio by drought (table below) ; grid rise between drought 0.6 and 0.8 ; grid sd peaks 0.322 at drought 0.7
flags      : 4 (below)
provenance : OBSERVED -- original code, chat-side sandbox 2026-11-10, filed verbatim 2026-11-11 (sha256 eba95252b17a4653...). Rerun in this tree 2026-11-11 on numpy 2.5.3 / scipy 1.18.1: printed output matches the logged output line for line.
feeds      : L4_FIRE_MEANFIELD_ODE ; L4_FIRE_PERCOLATION_GRID ; BR_FIRE_PERCOLATION ; BR_FIRE_MEANFIELD
l0_closure : void
```

## Output (this tree, 2026-11-11)

```text
drought   p    R0   ODE_frac  GRID_frac  grid_sd   ODE / GRID (from the 3-decimal columns)
  0.0  0.20  0.64    0.000     0.000    0.000     both 0
  0.1  0.28  0.88    0.000     0.000    0.000     both 0
  0.2  0.35  1.12    0.206     0.000    0.000     grid prints 0.000
  0.3  0.43  1.36    0.478     0.001    0.001     478
  0.4  0.50  1.60    0.642     0.002    0.002     321
  0.5  0.57  1.84    0.747     0.012    0.014     62
  0.6  0.65  2.08    0.817     0.164    0.123     5.0
  0.7  0.73  2.32    0.866     0.719    0.322     1.2
  0.8  0.80  2.56    0.900     0.954    0.005     0.94
  0.9  0.88  2.80    0.925     0.983    0.003     0.94
  1.0  0.95  3.04    0.943     0.994    0.001     0.95
```

Flags

```text
- CORRECTION 2026-11-11 (chat side, recorded, not reinterpreted): the earlier "up to ~60x" is the ratio at
  drought 0.5 only. At 0.4 it is 321, at 0.3 it is 478. The ratio is stated by drought, not as one number.
- ratios at grid means of 0.001-0.002 come from burns of a few cells with 12 reps; they are noise-dominated
- one seed, one grid size: finite-size effects on the threshold are unassessed
- grid carries no N budget: L0 closure void for this run
- status COMPLETE is PROPOSED by the filing session: code in tree, output reproduced, no toolbox trigger on record
```

History: REPORTED with code / seed / params void until 2026-11-11, when the original code arrived from the chat side.
