# run_15 -- run_11's trigger re-run with multi_seed_ensemble and ablation (card CC_003)

```text
status     : INCOMPLETE -- gate rule: residual_regression, equation_family_swap, parameter_recovery, assumption_block_trace still owed to run_11's trigger; see ledger/NEEDS_TOOL.md
code       : runs/run_15.py
seed       : 0..19, paired (each nudge on the same seeds as the anchor)
params     : the 33 ALL_INSIDE nudges of run_11, read from samples/run_11.json ; ablation arms grass removed (G0=0, uG=0), fire removed (seeds 0..9)
results    : of the 33: HIDDEN_IN_NOISE 18, ABSORBED 9, SEED_SPECIFIC 2, INERT 2, UNRESOLVED 2
flags      : 6 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_15.py (680 simulations, about four minutes on 4 workers) ; pinned in samples/run_15.sample.txt
feeds      : CC_003_nudges_that_move_nothing ; multi_seed_ensemble ; ablation ; ledger/NEEDS_TOOL.md (two rows cleared)
l0_closure : not re-read per nudge here; run_11 closed N and water on all 64 nudges (63 of 64 overall, the planted leak excepted)
```

## Classes (work order 2026-11-11: inert | absorbed | hidden in noise | seed-specific)

```text
class            n   definition (first that applies)                               nudges
HIDDEN_IN_NOISE  18  an output resolved on common seeds AND material (> 0.5 sd)    kT x2, kG x2, Wh x2, uG x1.1, KG x0.9, b x2, Kf x2,
                                                                                    W_dry x1.1, kill_T x1.1, et x2, drain x2
ABSORBED         9   resolved somewhere (own flux row or an output), nothing        uG x0.9, KG x1.1, aG x2, aT x2, kill_G x0.9,
                     material                                                       kill_T x0.9, season x1.1
SEED_SPECIFIC    2   no material move; mixed signs beyond 2 sd on some seeds        season x0.9, drought_sd x1.1
INERT            2   every output and own path EXACT_ZERO or EQUIVALENT             p_ign x1.1, kill_G x1.1
UNRESOLVED       2   none of the above at 20 seeds                                  p_ign x0.9, drought_sd x0.9
```

Every decomposition and every water nudge (kT, kG, Wh, et, drain) moves outputs by
0.6 to 2.1 sd: run_11's three unpaired seeds could not see them. The grass-side
nudges (uG, KG, aG, aT, kill_G) are resolved and mostly immaterial on the late
outputs, and the ablation agrees: removing grass entirely leaves every late
output EQUIVALENT or UNRESOLVED and moves only fire_out and grass_gone_yr. p_ign
is the one fire term that stays inside noise while W_dry, fuel_th, burn and vol move.

## Flags

```text
1  First draft of this run read MOVED as "moved". On common seeds a deterministic shift far
   below any noise band resolves at a huge z: aG x1.1 moves fire_out by -0.001 (0.0006 sd),
   z -55. The draft classed 27 of 33 HIDDEN_IN_NOISE. multi_seed_ensemble now reports
   `material` (|mean| > delta) beside the verdict, ablation's MATTERS needs it, both gates
   re-run (13 of 13, 8 of 8), run_14 re-run with readings unchanged. The draft output is
   not kept; this note is the record of it.
2  The HIDDEN / ABSORBED line is the 0.5 sd materiality [CHOICE]. Three mirror pairs straddle
   it: uG (0.52 / 0.50 sd), KG (0.46 / 0.52), kill_T (0.58 / 0.48). Their class is the choice's.
3  ABSORBED here means the change arrived and was taken up below material size. It does not
   say WHAT absorbs it; for the grass terms the ablation points at the grass being gone by
   year 19 (CC_003 low_dim_projection), for aG at tree uptake being N-limited.
4  p_ign inside noise while the other fire terms move is what the threshold-reset reading
   predicts (CC_003 local_normal_form). It is not that slot's evidence: the slot's exit
   names equation_family_swap, which is not built.
5  Own-path rows were found mechanically (rates at x1.0 vs x1.1 at sampled states).
   drought_sd and drought act through the per-year precipitation factor and are DECLARED
   onto the precipitation row; the mechanical test cannot see them.
6  INCOMPLETE stays: four tools are still owed to run_11's trigger.
```
