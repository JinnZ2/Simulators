# NEEDS_TOOL

Gate rule (METHOD BRIEF addition, 2026-11-10): a trigger fired, the tool did not
exist, the run is INCOMPLETE. One row per (tool, trigger, run). A row leaves this
file only when the tool is built AND has been run on that trigger.

`needed for` separates a tool the trigger specifically calls for from one owed
only because the brief says to run the full toolbox.

| tool | trigger that needed it | run | date | needed for |
|---|---|---|---|---|
| ablation | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | specific: separate the three supported causes from each other |
| multi_seed_ensemble | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | specific: 10 nudges sit at 1.2-1.9 sd on 3 seeds; power, and variance near the fire threshold |
| equation_family_swap | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | specific: the unlooked-at slot, fire cycle as a threshold reset |
| parameter_recovery | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | specific: parameters that move no output cannot be recovered from outputs; which ones is this tool's question |
| residual_regression | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | full toolbox |
| assumption_block_trace | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | full toolbox |
| ablation | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| multi_seed_ensemble | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| equation_family_swap | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| parameter_recovery | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| residual_regression | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| assumption_block_trace | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| multi_seed_ensemble | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | specific: run_10 used hand-written seed loops in place of the tool |
| ablation | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | specific: run_10 dropped deposition and fire by hand; the dep=0 arm removed both at once |
| residual_regression | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | full toolbox |
| equation_family_swap | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | full toolbox |
| parameter_recovery | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | full toolbox |
| assumption_block_trace | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | full toolbox |

run_10 and run_11 predate the rule. Marking them INCOMPLETE is the rule applied
backwards by the session that ran them, not an instruction from the rule's author.
| ablation | same shape across three families, first hand (card CC_005) | run_13 | 2026-11-11 | full toolbox |
| multi_seed_ensemble | same shape across three families, first hand (card CC_005) | run_13 | 2026-11-11 | full toolbox |
| equation_family_swap | same shape across three families, first hand (card CC_005) | run_13 | 2026-11-11 | full toolbox |
| parameter_recovery | same shape across three families, first hand (card CC_005) | run_13 | 2026-11-11 | full toolbox |
| residual_regression | same shape across three families, first hand (card CC_005) | run_13 | 2026-11-11 | full toolbox |
| assumption_block_trace | same shape across three families, first hand (card CC_005) | run_13 | 2026-11-11 | full toolbox |
| support_match | detector reads support stated, not support matching; silent on cases a and b first hand (card CC_005) | run_13 | 2026-11-11 | specific: case a states its evidence and the evidence does not support the attribution |
