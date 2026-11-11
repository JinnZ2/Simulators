# NEEDS_TOOL

Gate rule (METHOD BRIEF addition, 2026-11-10): a trigger fired, the tool did not
exist, the run is INCOMPLETE. One row per (tool, trigger, run). A row leaves this
file only when the tool is built AND has been run on that trigger.

`needed for` separates a tool the trigger specifically calls for from one owed
only because the brief says to run the full toolbox.

| tool | trigger that needed it | run | date | needed for |
|---|---|---|---|---|
| equation_family_swap | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | specific: the unlooked-at slot, fire cycle as a threshold reset |
| residual_regression | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | full toolbox |
| assumption_block_trace | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | full toolbox |
| ablation | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| multi_seed_ensemble | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| equation_family_swap | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| parameter_recovery | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| residual_regression | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
| assumption_block_trace | same shape across three families (card CC_004) | run_12 | 2026-11-11 | full toolbox |
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
| equation_family_swap | run_10 trigger re-run, N misclosure near-identical across seeds (card CC_001) | run_14 | 2026-11-11 | full toolbox |
| parameter_recovery | run_10 trigger re-run, N misclosure near-identical across seeds (card CC_001) | run_14 | 2026-11-11 | full toolbox |
| assumption_block_trace | run_10 trigger re-run, N misclosure near-identical across seeds (card CC_001) | run_14 | 2026-11-11 | full toolbox |
| residual_regression | run_11 trigger re-run, 33 of 64 nudges move nothing detectable (card CC_003) | run_15 | 2026-11-11 | full toolbox |
| equation_family_swap | run_11 trigger re-run, 33 of 64 nudges move nothing detectable (card CC_003) | run_15 | 2026-11-11 | full toolbox |
| parameter_recovery | run_11 trigger re-run, 33 of 64 nudges move nothing detectable (card CC_003) | run_15 | 2026-11-11 | full toolbox |
| assumption_block_trace | run_11 trigger re-run, 33 of 64 nudges move nothing detectable (card CC_003) | run_15 | 2026-11-11 | full toolbox |

## Cleared

A row moves here only when the tool is built, its gate reads PASS (tests/test_toolkit.py),
and it has been run on that trigger in the run named under "cleared by" (the tool's
used_in lists that run). tools/check_ledger.py enforces all three. Rows are moved, never deleted.

| tool | trigger that needed it | run | date | cleared by | how |
|---|---|---|---|---|---|
| multi_seed_ensemble | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | run_14 | seed_invariance on N_mis and the counter, seeds 0-9; replaces run_10's hand-written loops |
| ablation | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | run_14 | three single drops; dep=0 flagged CO_ABLATED [fire]; counter-only drop carries the residual |
| ablation | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | run_15 | grass removed and fire removed against the anchor; grass removal immaterial on late outputs |
| multi_seed_ensemble | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | run_15 | 20 paired seeds; the 33 split HIDDEN_IN_NOISE 18 / ABSORBED 9 / SEED_SPECIFIC 2 / INERT 2 / UNRESOLVED 2 |
| support_match | detector reads support stated, not support matching; silent on cases a and b first hand (card CC_005) | run_13 | 2026-11-11 | run_16 | cases a-d first hand: detector hits 1 before (c1), 3 after (a, b, c1) |
| parameter_recovery | 33 of 64 nudges move nothing detectable (card CC_003) | run_11 | 2026-11-10 | run_17 | six parameters across run_15 classes: 3 RECOVERED, 2 PARTIAL, aG NOT_IDENTIFIABLE |
| residual_regression | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | run_18 | N misclosure on method vs biology over 36 configurations: METHOD_ARTIFACT once the counter error is declared, UNEXPLAINED without |
| residual_regression | run_10 trigger re-run, N misclosure near-identical across seeds (card CC_001) | run_14 | 2026-11-11 | run_18 | N misclosure on method vs biology over 36 configurations: METHOD_ARTIFACT once the counter error is declared, UNEXPLAINED without |

## Owed expiry

Read only under `tools/check_ledger.py --owed-mode proposed` (2026-11-11; the mode is a
proposal awaiting Kavik). One row per owed (tool, run): when the row is no longer
allowed to stay owed. Declared when the row opens. `date:YYYY-MM-DD`, `run:run_N`
(expires once run_N exists) or `VOID`. A row with no entry here reads VOID and is
counted as no exit. Every row open on 2026-11-11 opened before this rule, so none
carries an expiry; none is back-filled.

| tool | run | expires | declared |
|---|---|---|---|
