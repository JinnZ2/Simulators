# run_11 -- assumption_nudge on the candidate anchor (anchor test 3)

```text
status     : INCOMPLETE -- gate rule: tools missing, see ledger/NEEDS_TOOL.md
code       : runs/run_11.py
seed       : 0, 1, 2 per nudge ; 0..9 for the noise band
params     : model/base.py DEFAULTS, unedited ; one override per nudge ; x1.1 and x0.9 per hand-set parameter, x10 for two structural nudges, leak 0.3
results    : 64 nudges on 13 of 25 assumptions ; budgets closed under 63 ; 33 moved nothing detectable ; no runaway with the ceiling lifted
flags      : 8 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_11.py ; pinned in samples/run_11.sample.txt and samples/run_11.json
feeds      : ANCHOR_run9 (test 3) ; CC_003_nudges_that_move_nothing ; L3_LIGHT_CEILING ; L0_WATER_BUDGET ; L2_GRASS_GROWTH ; assumption_nudge
l0_closure : N and water CLOSED under 63 of 64 nudges ; N LEAK under the planted off-table path ; C / P / energy VOID
```

## Loop

```text
ANCHOR   run_9, three code files pinned by sha256
BRANCH   one parameter override per nudge; the assumption it belongs to is named
RUN      3 seeds per nudge
RETURN   anchor re-run after every nudge: bit-identical 64 of 64; budgets re-closed
READ     output mean against the anchor's, noise = 2 x sd over anchor seeds 0-9   [CHOICE]
```

## Where the change went

```text
what was nudged                       what moved                               reading
------------------------------------  ---------------------------------------  ---------------------------
deposition +-10%                      fire export +-27 (16 sd), fires +-8      N in sets N out
leak 0.3 (off-table path)             N LEAK -72.6; water still closed         the written signature for A1
ceiling lifted x10                    soil N -0.43 (17 sd), leaching -3.59;    NO runaway. Trees are bounded
                                      tree N 38.99 against 38.87               by N supply, not the ceiling
fungal benefit near-linear (Kf x10)   tree N +7.5, fungal N -1.07 (26 sd)      largest structural response
fuel_th, burn, vol +-10%              fire count 3.1-4.2 sd                    the fire cycle's own terms
uT, K, KT, leach, mT, mF, c, mG       one or two outputs, 2.0-8.1 sd           local, as expected
P0, W_dry x0.9, drought +0.1          water, leaching, fires                   --
33 other nudges                       nothing outside noise                    TRIGGER, card CC_003
```

## Flags

```text
- INCOMPLETE under the gate rule (2026-11-10): the trigger below needs ablation,
  multi_seed_ensemble, equation_family_swap and parameter_recovery; none exists.
- TRIGGER: 33 of 64 nudges leave every output inside noise. Card CC_003 is OPEN:
  three causes supported and not separated from each other (N throughput fixed by
  the budget; grass-side parameters unreachable after extinction; low power at
  3 seeds), one slot not looked at (fire cycle as a threshold reset).
- The failure signature written for the light ceiling (runaway, from run 4) did
  not appear. Run 4 has no N audit. In a model that conserves N the budget does
  the bounding. The ledger entry keeps its text and records the contradiction.
- 12 of 25 assumptions cannot be nudged without new pools, cohorts or space.
  Each is listed with its reason. Anchor test 3 is PARTIAL on that ground alone.
- Six water parameters belong to no listed assumption. Nudged anyway.
- P0 x0.9 and drought +0.1 are the same run: one parameter under two names.
- No 10 percent nudge keeps grasses. Extinction year stays in 17.5-21.4.
- The first pass of this run read pools at year 300, one phase of the fire cycle:
  soil N had a noise band of 417 percent. Pools are now read as means over years
  100-300. 35 nudges were ALL_INSIDE on the first pass, 33 on this one; tree
  turnover (mT) moved from inside to outside.
```
