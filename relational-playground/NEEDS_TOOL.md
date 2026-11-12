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
ablation                 playground/analysis/ablation.py               unexpected deviation: run 8's spot-0.2 reading does not hold over seeds forest_fire_regime PART 3        2026-11-11
residual_regression      playground/analysis/residual_regression.py    unexpected deviation: run 8's spot-0.2 reading does not hold over seeds forest_fire_regime PART 3        2026-11-11
parameter_recovery       playground/analysis/parameter_recovery.py     unexpected deviation: run 8's spot-0.2 reading does not hold over seeds forest_fire_regime PART 3        2026-11-11
assumption_block_trace   playground/analysis/assumption_block_trace.py unexpected deviation: run 8's spot-0.2 reading does not hold over seeds forest_fire_regime PART 3        2026-11-11
```

What the toolbox did run on PART 2: budget closure (every run CLOSED), a
40-seed ensemble with variance per level, and one equation-family swap (grid
against mean-field ODE). The branching family exists and was not run on it.

Run status under the gate rule:

```text
forest_fire_regime PART 1   COMPLETE     no trigger fired: the port met every target fixed in PREREG.md
forest_fire_regime PART 2   INCOMPLETE   two logged features did not appear and 21 coincidence cards are OPEN;
                                         four toolbox tools do not exist
forest_fire_regime PART 3   INCOMPLETE   the ports met 8 of 8 targets (PREREG_ORIGINALS.md); then the 20-seed spread of the
                                         original design put the spot-0.2 gap outside 0.05 on 17 of 20 seeds at drought 0.5.
                                         That is a deviation from run 8's own reading; the same four tools do not exist
```

What the toolbox did run on PART 3: budget closure on run 6 (CLOSED; the old model
LEAK), a 20-seed loop written by hand, and one equation-family swap (the Poisson
branching family's die-out beside the count of replicates that burned under 5%).
Two coincidence cards are OPEN with evidence entered and no slot set.
