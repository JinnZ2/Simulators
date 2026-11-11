# NEEDS_TOOL -- tools a fired trigger needed and did not find

Gate rule (forest-model-ledger/CLAUDE.md): trigger + missing tool => the run is
INCOMPLETE, the tool gets a placeholder, a row goes here, and the report opens
with "TOOL NEEDED: <name>".

```text
tool                     placeholder                                   trigger that needed it                                   run                              date
ablation                 playground/analysis/ablation.py               unexpected deviation (F1, F3) + cross-family agreement   forest_fire_regime PART 2        2026-11-11
residual_regression      playground/analysis/residual_regression.py    unexpected deviation (F1, F3) + cross-family agreement   forest_fire_regime PART 2        2026-11-11
parameter_recovery       playground/analysis/parameter_recovery.py     unexpected deviation (F1, F3) + cross-family agreement   forest_fire_regime PART 2        2026-11-11
assumption_block_trace   playground/analysis/assumption_block_trace.py unexpected deviation (F1, F3) + cross-family agreement   forest_fire_regime PART 2        2026-11-11
```

What the toolbox did run on PART 2: budget closure (every run CLOSED), a
40-seed ensemble with variance per level, and one equation-family swap (grid
against mean-field ODE). The branching family exists and was not run on it.

Run status under the gate rule:

```text
forest_fire_regime PART 1   COMPLETE     no trigger fired: the port met every target fixed in PREREG.md
forest_fire_regime PART 2   INCOMPLETE   two logged features did not appear and 21 coincidence cards are OPEN;
                                         four toolbox tools do not exist
```
