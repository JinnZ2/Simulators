# run_21 -- equation_family_swap against the relational-playground engine (follow-up item 3)

```text
status     : COMPLETE -- the swap ran on the engine's own component; no ledger trigger was answered by it (see flag 4)
code       : runs/run_21.py
seed       : grid replicates 0-39 per point (the engine experiment's seeds)
params     : binding ledger/toolkit/rp_engine.py; adapter equation_family_swap.py frozen, unedited;
             engine JinnZ2/Simulators claude/relational-playground @ 2f33dee (relational-playground/ identical to 73f9873);
             component forest_fire_regime; drought 0.1..0.9 (engine PREREG levels); spot 0.0, 0.05, 0.2; L 64;
             adapter K_HANDOFF 3, MIN_RUN 3; spread [CHOICE] se of the grid mean, also read with per-run sd
results    : reproduces the engine's out/part2.json to 0.0 at every point; every engine run COMPLETE
             (its known-answer gate certified first). Disagreement regimes: see table
flags      : 5 (below)
provenance : DERIVED, run by the engine at the pinned commit through the adapter
feeds      : equation_family_swap
l0_closure : the engine's own: mass budget CLOSED on every run; C, N, water, energy VOID in this model
```

Engine at the pinned commit: brief families ODE -> linear, nonlinear; percolation -> percolation;
branching process -> branching; Ising, spin glass, MaxEnt, random-matrix stability: NOT IN ENGINE.
Only forest_fire_regime runs one component under two of them (percolation grid against mean-field ODE).

## Disagreement regimes (percolation vs ODE)

```text
spot  sd = se of grid mean (40 reps)          sd = per-run sd
0.00  0.1-0.6 and 0.7-0.9; agree only at 0.65  0.2-0.55 (ODE over the grid below threshold); ends at 0.6
0.05  0.1-0.9, every point                    0.2-0.5 and 0.7-0.9
0.20  0.1-0.5 and 0.6-0.9; agree at 0.55       0.2-0.4 and 0.65-0.9
```

## Flags

```text
1  The adapter reproduces the engine exactly (same seeds, same calls): the binding reads what the
   engine computes, no more.
2  Under se the families disagree at almost every point: 40 replicates resolve the ODE's ~3-4 %
   shortfall above threshold as surely as its 10-15x excess below. handoff() has no materiality
   margin; it reads RESOLVED as a regime, the same conflation run_15 found in multi_seed_ensemble.
   The engine's own comparison uses an absolute window (0.05). Not retuned: reported.
3  Under per-run sd the spot 0.0 disagreement regime is 0.2-0.55 and ends at 0.6, where the grid's
   variance peaks (sd_run 0.135). That is the brief's lesson read from the other side: the
   variance spike at threshold is what makes the two families indistinguishable there.
4  This is the ENGINE's fire: a fuel grid, not the ledger's L4_FIRE_MEANFIELD_ODE. The engine
   ports the ledger's model (forest_n, part 1) under one family only (nonlinear), so no ledger
   component has a second family to swap against. The six equation_family_swap rows in
   NEEDS_TOOL.md stay open; CC_003's local_normal_form slot is not filled.
5  FML_046 ("engine absent on every branch") is REFUTED: the branch's commits are authored from
   08:43 UTC and the check was at 14:22. Whether it had been pushed then is not known here.
```
