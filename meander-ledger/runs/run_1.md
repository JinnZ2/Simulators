# run_1 -- meander toy: base, seeds, depth/friction, ablations, planted leak

```text
code       : runs/run_1.py
seed       : 0 (cases) ; 0..2 (base)
params     : model/meander.py DEFAULTS + E 0.3, steps 6000 ; burn 2000 [CHOICE] ; record every 100
results    : base lam/W 7.96..8.80 over 3 seeds ; sinuosity 2.03..2.45 ; cutoffs 7.5..8.0 per 1000 steps ; sediment CLOSED in 13 of 13 unplanted cases, planted leak LEAK -1.213e+02
flags      : 6 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_1.py (samples/run_1.sample.txt)
feeds      : L0_SEDIMENT_BUDGET ; L0_WATER_BUDGET ; L0_ENERGY_BUDGET ; L0_BOUNDARY_AUDIT ; L2_VEGETATION_BANK ; L3_BEND_GROWTH_KINEMATIC ; L4_CUTOFF ; MC_003 ; MC_004
l0_closure : sediment CLOSED ; water, energy CLOSED by IDENTITY ; momentum VOID
```

## Flags

```text
- Sediment closes by construction (every transfer is a counter). The audit catches a
  hidden removal (planted leak) and says nothing about whether a flux has the right size.
- Water and energy close by identity: both sides are one expression in this model.
  They are reported, flagged IDENTITY, and admit nothing.
- Supply 0.2, supply 2.0 and the planted leak leave the planform byte-identical to
  base s0. The migration rule never reads the sediment store. Toolbox trigger:
  nudging moves nothing (MC_004).
- Depth and friction enter only as alpha = 2 Cf / H: aspect 10 == Cf 0.005 and
  aspect 40 == Cf 0.02 to every printed digit (MC_003).
- alpha 0.2 (aspect 10, Cf 0.005) stays straight for 6000 steps; lam/W there (2.71)
  is the estimator reading noise, not bends.
- Build history kept: the first cutoff rule took the first close pair found and cut
  almost the whole channel (sinuosity 3.9 -> 1.0); repaired to the tightest neck.
  Then bends left through the pinned downstream end and multiplicative noise could
  not seed new ones; an additive jitter (0.002 W/step) was added. Both changes are
  in model/meander.py and are choices, not physics.
```
