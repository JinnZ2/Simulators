# Work order -- forest model ledger

Delivered 2026-11-10. Verbatim below; not edited. Findings go in
`CLAIM_TABLE.md` and the ledger, never here.

```text
WORK ORDER — Forest model ledger (co-authored, Kavik + Claude, 2026-11-10)
Goal: build a provenance-tracked model ledger, not answers. Python, stdlib + numpy/scipy only.

STRUCTURE
ledger/components/*.yaml  one file per component:
  id, layer (L0 physics | L1 chemistry | L2 organisms | L3 interactions | L4 disturbance | L5 observation),
  equation, assumes [A1..An], if_assumption_fails {A_i: expected signature},
  scope, provenance (OBSERVED|DERIVED|PROPOSED + source), admitted_by (test id | void),
  test_results [], open_issues [], depends_on [], status (candidate|admitted|rejected|placeholder)
ledger/branches/*.yaml    one per equation family; links to other branches; convergence_anchors []
ledger/assumption_blocks/*.yaml  shared assumptions linked to every study/equation using them
runs/run_N.py + runs/run_N.md  code, seed, params, results, flags
Rule: unfilled fields stay void, never dropped. Rejected entries stay.

L0 AUDIT (highest bar, revisable)
- close N, C, P, water, energy budgets each run; report misclosure
- boundary audit line: deposition, fixation, dust, groundwater, animal transport
- leak-vs-noise rule against measurement error
- multi-budget closure guards against compensating errors
- C:N:P stoichiometry = ranges (softest L0 part)

RUNS TO LOG
1 coupled tree/fungus ODE, fertility sweep: 36 pos/10 neutral/9 neg; sign flip partly circular (written in)
2 120 synthetic studies + method artifacts: bio-only R2 0.15, bio+method 0.66, true bio 0.79; fine mesh inflated ~2x
3 trees+grasses+4 fungi: pairwise-additive prediction impossible (negative) → higher-order effects dominate
4 sweep: whole > parts only at low competition + strong fungal benefit; runaway = no ceiling
5 litter guilds + fire: no fires (threshold miscalibrated)
6 mass-conserving rebuild: old model leaked ~24 N units; conserved misclosure ~1e-9; fire cycle emerged (47 fires); OPEN: grasses extinct
7 percolation vs mean-field ODE, drought sweep: ODE overpredicts mid-drought up to ~60x; grid threshold ~0.6–0.7 with variance spike
8 ember spotting: spot 0.2 converges grid onto ODE at drought ≥0.5 → CONVERGENCE ANCHOR; 5% spotting drops threshold to ~0.5

PLACEHOLDER BRANCHES (status: placeholder)
- stochastic extinction / branching process (revealed run 8)
- Ising (masting synchrony), spin glass (fungus-fungus matrix, alt. stable states),
  MaxEnt (Harte METE), random matrix stability (May), renormalization (scale)
- microbe-explicit decomposition (MIMICS/CORPSE) vs Michaelis-Menten
- animals/insects/birds/earthworms (worms non-native in glaciated N. America; sign is regional)
- regime map: families x regimes (wet|drought|post-fire|dense|mixed), cells = fit, L0 closure, ablation

DATA (later)
Jiang et al. global plant-soil feedback dataset: zenodo.org/records/10403125 (Dryad doi:10.5061/dryad.n2z34tn35)
Karst 2023 CMN review: doi:10.1038/s41559-023-01986-1 (26 field studies)

FIRST TASKS
1 scaffold ledger dirs + schema
2 rebuild run 6 conserved model as base; verify misclosure
3 log runs 1–8 as entries; mark placeholders
```
