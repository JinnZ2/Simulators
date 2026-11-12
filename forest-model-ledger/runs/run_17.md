# run_17 -- parameter_recovery on the candidate anchor, run_11's trigger (card CC_003)

```text
status     : COMPLETE -- no new trigger fired; the question was answered with a gated tool. run_11's other owed tools stay owed to run_11
code       : runs/run_17.py
seed       : observation 100..104 ; fit 0..4 at every grid value
params     : one parameter at a time at x0.6 .. x1.4 of DEFAULTS, the rest at DEFAULTS
results    : dep, kT, uG RECOVERED ; kill_G, p_ign PARTIAL ; aG NOT_IDENTIFIABLE
flags      : 4 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_17.py ; pinned in samples/run_17.sample.txt
feeds      : parameter_recovery ; CC_003_nudges_that_move_nothing ; ledger/NEEDS_TOOL.md (parameter_recovery / run_11 cleared)
l0_closure : not re-read here
```

## Reading

```text
param   recovery          plausible            run_15 class of its +-10% nudges
dep     RECOVERED         x1.0                 (moved in run_11)
kT      RECOVERED         x1.0                 HIDDEN_IN_NOISE
uG      RECOVERED         x0.8 .. x1.2         HIDDEN x1.1 / ABSORBED x0.9
aG      NOT_IDENTIFIABLE  every grid value     ABSORBED (chi2 7.4 flat to one decimal)
kill_G  PARTIAL           x0.6 .. x1.2         INERT x1.1 / ABSORBED x0.9 ; chi2 110 at x1.4
p_ign   PARTIAL           x1.0 .. x1.4         INERT x1.1 / UNRESOLVED x0.9 ; theta_hat x1.2
```

The ordering agrees with run_15: parameters whose nudges were HIDDEN_IN_NOISE are
recovered, the ABSORBED one is not identifiable from these outputs at all, the
INERT ones are bounded on one side.

## Flags

```text
1  chi2 at x1.0 is 7.4 for every parameter: at x1.0 every run is the DEFAULTS run, so this
   is the observation-vs-fit seed noise (nine outputs), the same number six times. Expected.
2  kill_G: inert at +-10% (run_15) and visible at x1.4 (chi2 110). The response is not
   linear in the nudge; run_11's +-10% was too small to see it.
3  p_ign: theta_hat lands at x1.2, not x1.0; the truth is plausible but the grid is
   not bounded above. Consistent with a threshold-reset fire cycle, not evidence for it
   (CC_003 local_normal_form stays void until equation_family_swap exists).
4  One parameter at a time. Joint identifiability is not read.
```
