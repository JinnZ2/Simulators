# run_18 -- residual_regression on run_10's trigger (card CC_001; run_14 inherits it)

```text
status     : COMPLETE -- no new trigger fired; answered with a gated tool. run_10 / run_14 keep their other owed rows
code       : runs/run_18.py
seed       : 0, 1
params     : dt {1/52, 1/64, 1/104} x dep {0.8, 1.0, 1.2} x years {150, 300}; everything else DEFAULTS
results    : with the counter's model-free roundoff declared as a method field: METHOD_ARTIFACT, R2 1.000, biology adds 0.000. Generic method fields alone: UNEXPLAINED
flags      : 3 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_18.py ; pinned in samples/run_18.sample.txt
feeds      : residual_regression ; CC_001 (no slot change; RESOLVED by run_14) ; ledger/NEEDS_TOOL.md (two rows cleared)
l0_closure : N misclosure is the residual under study; range -1.27e-10 .. +8.16e-11 over 36 runs
```

## Flags

```text
1  Fit 1 (dt, steps vs dep, fires, T_mean): UNEXPLAINED. Biology dB 0.27 at p 0.026, under the
   0.01 line. A looser alpha would have called this N residual biology: the counter's
   roundoff scales with dep. The regression is as good as the method field it is given.
2  Fit 2 / fit 3: the model-free counter error explains the residual at R2 1.000; biology adds 0.
   This is run_10 section 6 recomputed as a regression across 36 configurations.
3  Found by this run and repaired before recording: unscaled lstsq dropped the 1e-11 column
   beside the 1e4 step count, and fit 2 printed fit 1's numbers. Columns are standardised;
   a known-answer case now covers mixed scales; gate re-run 7 of 7.
```
