# run_8 -- ember spotting

```text
status     : INCOMPLETE
code       : runs/run_8.py
seed       : 4
params     : in the code: L 100, 10 reps, density 0.8, p = 0.2 + 0.75 * drought, spot 0 / 0.05 / 0.2 / 1.0, drought 0.2 / 0.4 / 0.5 / 0.6 / 0.7
results    : spot 0.2 vs ODE at drought 0.5 / 0.6 / 0.7: 0.73 vs 0.75, 0.84 vs 0.82, 0.90 vs 0.87 -> CA_1 stays CANDIDATE ; spot 0.05 at drought 0.5: 0.38, sd 0.31
flags      : 5 (below)
provenance : OBSERVED -- original code, chat-side sandbox 2026-11-10, filed verbatim 2026-11-11 (sha256 bf65e9b7b024b0d9...). Rerun in this tree 2026-11-11 on numpy 2.5.3 / scipy 1.18.1: printed output matches the logged output line for line.
feeds      : L4_EMBER_SPOTTING ; CA_1 ; BR_FIRE_PERCOLATION ; BR_FIRE_MEANFIELD
l0_closure : void
```

## Output (this tree, 2026-11-11)

```text
drought  ODE   | spot=0   0.05   0.2   1.0  (mean / sd)
 0.2   0.21  | 0.00/0.00  0.00/0.00  0.00/0.00  0.05/0.09
 0.4   0.64  | 0.00/0.01  0.02/0.06  0.33/0.27  0.45/0.30
 0.5   0.75  | 0.01/0.01  0.38/0.31  0.73/0.01  0.60/0.30
 0.6   0.82  | 0.20/0.15  0.81/0.01  0.84/0.01  0.74/0.25
 0.7   0.87  | 0.76/0.26  0.82/0.27  0.90/0.00  0.78/0.26
```

Flags

```text
- CORRECTION 2026-11-11 (chat side, recorded, not reinterpreted): the convergence at spot 0.2, drought >= 0.5
  was read by eye, with no pre-declared tolerance, on 10 reps and one seed. CA_1 is a CANDIDATE only.
- at spot 1.0 the grid sits below the ODE (0.60 / 0.74 / 0.78 vs 0.75 / 0.82 / 0.87) with sd 0.25-0.30
- revealed a missing family: stochastic extinction / branching process (BR_BRANCHING_PROCESS, placeholder)
- grid carries no N budget: L0 closure void for this run
- status INCOMPLETE is PROPOSED by the filing session: the coincidence trigger on card CC_002 can now be
  worked, and the tools it calls for are placeholders (ledger/NEEDS_TOOL.md)
```

History: REPORTED with code / seed / params void until 2026-11-11, when the original code arrived from the chat side.
