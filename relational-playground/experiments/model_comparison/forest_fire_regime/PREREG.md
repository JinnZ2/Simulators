# PREREG -- forest_fire_regime, written before any run

Written 2026-11-11 by the building session and committed before the code that
runs it. Nothing below was tuned against an output: no output existed.

## What can and cannot be ported

```text
run 6   forest-model-ledger/runs/run_6.md   status REPORTED   code void, seed void, params void
run 7   forest-model-ledger/runs/run_7.md   status REPORTED   code void, seed void, params void
run 8   forest-model-ledger/runs/run_8.md   status REPORTED   code void, seed void, params void
run 9   forest-model-ledger/runs/run_9.py   status COMPLETE   code in tree; the rebuild of run 6
```

The work order says "port run 6 + runs 7-8 ... must reproduce the logged
results". Runs 6-8 have no code, seed or parameters in this tree, so they
cannot be ported and cannot be reproduced in the strict sense. What is done
instead, in two parts kept apart:

```text
PART 1  PORT     run 9 (the in-tree rebuild of run 6) -> playground model forest_n.
                 Target: run 9's own logged numbers. This is a port; it can fail.
PART 2  REBUILD  runs 7-8 from their one-paragraph records. The design below is
                 the building session's. It is ONE design, fixed here. If it does
                 not show a logged feature, that is reported; it is not retried
                 with other settings. Another design would be a branch.
```

## PART 1 targets (from runs/run_9.md, logged)

```text
N misclosure      -5.062e-11   verdict CLOSED     target: CLOSED, |misclosure| < 1e-9
water misclosure  -3.426e-13   verdict CLOSED     target: CLOSED
fires             80           (seed 0, 300 yr, RK4 dt 1/52)
final pools       S 0.3715  T 36.6196  G 0.0000  F 0.9468  Lt 3.6619  Lg 1.0482  W 0.6393
planted leak 0.3  N LEAK -7.264e+01, 59 fires
no fire           0 fires, N CLOSED
run 6 as logged   47 fires, misclosure ~1e-9   NOT a target: run 6 and run 9 are different parameter points
```

Random stream. run 9 draws from numpy's generator. The playground is stdlib
only, and stdlib `random` gives a different stream. Two runs, both reported:

```text
REPLAY   the numpy draws for seed 0 (300 yearly precipitation factors, then the
         ignition uniforms in order) exported once to fixtures/ and replayed.
         Target: the run 9 numbers above, pools to 4 decimals, fires exact.
NATIVE   stdlib random.Random(0). Same equations, different weather and ignition
         draws. Target: both budgets CLOSED. Fire count is reported, with no target.
```

## PART 2 design (the rebuild of runs 7-8)

What the records give: "ODE overpredicts mid-drought up to ~60x; grid threshold
~0.6-0.7 with variance spike" (run 7); "spot 0.2 converges grid onto ODE at
drought >= 0.5; 5% spotting drops threshold to ~0.5" (run 8). They do not give
the grid size, the replicate count, the ODE, or what "drought" multiplies.

```text
quantity compared   fraction of the whole grid burned when the fire is out
drought d           probability that a cell is dry enough to carry fire (p_flammable = d)
levels              d = 0.1 0.2 0.3 0.4 0.5 0.55 0.6 0.65 0.7 0.8 0.9
GRID                playground model percolation, L = 64, ignition left_edge,
                    spot in {0, 0.05, 0.2}, seeds 0..39 (40 replicates), up to 8 L steps
ODE                 mean field of the same rules, fractions of the grid:
                      du/dt = -beta u b        u unburned-flammable, b burning
                      db/dt =  beta u b - b    burn-out rate 1 per step
                      beta  = 4 + spot         four neighbours, plus the ember
                      u(0) = d (1 - 1/L), b(0) = d / L     the lit left column
                    integrated to t = 400, RK4 dt 0.01
budget              cells (grid) and grid fraction (ODE), declared as `mass`; N, C, water, energy VOID
agreement window    |grid mean - ODE| <= 0.05 of the grid, fixed here
```

Logged features and the rule each is read by, fixed here:

```text
F1  ODE overpredicts mid-drought up to ~60x
      rule: max over d in 0.3..0.6 of ODE / grid mean (spot 0) lies in 30..120
F2  grid threshold ~0.6-0.7 with a variance spike
      rule: steepest interval of the grid mean (spot 0) lies inside 0.55..0.7
            AND the replicate variance peaks at a level inside 0.55..0.7
F3  spot 0.2 converges grid onto ODE at drought >= 0.5
      rule: inside the agreement window at every level d >= 0.5
            AND outside it at one level or more with d < 0.5
F4  5% spotting drops the threshold to ~0.5
      rule: steepest interval of the grid mean (spot 0.05) has an end at 0.5 or lies inside 0.4..0.55
```

Each feature reads APPEARS, DOES NOT APPEAR, or NOT EVALUABLE. All four are
reported whichever way they read. A feature that does not appear is a finding
about this design, not evidence about runs 7-8, whose design is void.

Cross-family agreement (F3 inside the window) opens a coincidence card with
every slot void. forest-model-ledger's CC_002 holds the same observation, OPEN,
with the open issue that long-range spotting makes every cell see the mean.

## Not done here

No model is ranked. No level is dropped. No parameter above is changed after
the first run; a change is a new branch with its own record.
