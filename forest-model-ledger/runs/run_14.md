# run_14 -- run_10's trigger re-run with multi_seed_ensemble and ablation (CC_001 recheck)

```text
status     : INCOMPLETE -- gate rule: residual_regression, equation_family_swap, parameter_recovery, assumption_block_trace still owed to run_10's trigger; see ledger/NEEDS_TOOL.md
code       : runs/run_14.py
seed       : 0..9
params     : model/base.py DEFAULTS, unedited ; arms: dep=0, fires off, deposition counter read at its exact value dep*years
results    : the seed-invariant N misclosure is the deposition counter: removing the counter alone moves it +5.008e-11 with every other output EXACT_ZERO and the fire cycle intact (785 fires)
flags      : 5 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_14.py ; pinned in samples/run_14.sample.txt
feeds      : CC_001_n_misclosure_seed_invariance (recheck; PROVISIONAL -> RESOLVED) ; multi_seed_ensemble ; ablation ; ledger/NEEDS_TOOL.md (two rows cleared)
l0_closure : N CLOSED, water CLOSED in every arm (misclosures 1e-11 to 1e-14) ; C / P / energy VOID
```

## Trigger

run_10's: N misclosure -5.0e-11, near-identical across seeds (card CC_001). run_10
answered it with hand-written seed loops and a dep=0 arm; the card went PROVISIONAL
until multi_seed_ensemble and ablation existed. Both are now built and gated
(tests/test_toolkit.py). This run is the recheck.

## Reading

```text
tool                arm                          reading
multi_seed_ensemble base, seeds 0-9              N_mis INVARIANT (cv 0.0044); counter error CONSTANT +5.007905e-11, 1 distinct value
ablation            deposition off (dep=0)       MATTERS, CO_ABLATED [fire]: 0 fires on every seed. The drop removed two things
ablation            fire off                     N_mis UNRESOLVED, mean diff -2.8e-13 (z -1.7); still INVARIANT under the arm
ablation            deposition counter exact     N_mis MOVED +5.008e-11; fires, fire_out, water, T_mean EXACT_ZERO; N_mis VARIES (-5.4e-13..+1.1e-13)
```

The ablation run_10 could not do: remove the counter, keep deposition and fire.
The seed-invariance goes with the counter and with nothing else. What is left
after it (range -5.4e-13 .. +1.1e-13, varying by seed) is the rest of the roundoff,
fire events included: fire off moves the residual by -2.8e-13, not resolved at 10
seeds.

## Flags

```text
1  CO_ABLATED is the tool reproducing run_10's own flag mechanically: the dep=0 arm has
   0 fires on every seed. Its MATTERS reading belongs to {deposition, fire}, not to
   deposition.
2  seed_invariance at REL_TOL 0.05 also reads fires (cv 0.026), fire_out (0.006) and T_mean
   (0.020) INVARIANT. They vary by seed (7, 10, 10 distinct values). Relative spread
   cannot tell "should be noise around zero" from "a mean plus noise": the label is
   reliable here only on N_mis and the counter, whose mean is the residual. Recorded as
   a cannot_see on the tool, not retuned to this run.
3  The first draft of run_14 used hand-set equivalence margins. The water band (1e-12) sat
   below water's own roundoff sd (2.0e-12) and flagged seed_specific on roundoff. Margins
   are now derived from the base sd (0.5 sd, 2 sd) and printed; the draft is kept in the
   module comment.
4  fire off: N_mis UNRESOLVED and seed_specific at band 2 sd. The fire cycle moves the
   residual at the 1e-13 level, two orders under the counter. Not resolved at 10 seeds.
5  INCOMPLETE stays: four tools are still owed to run_10's trigger (and run_14 inherits
   the trigger). The two rows for multi_seed_ensemble and ablation move to the cleared
   table, cleared by this run.
```
