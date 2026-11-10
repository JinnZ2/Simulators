# CLAUDE.md -- meander-ledger

The method is not restated here. Read the METHOD BRIEF in
`../forest-model-ledger/CLAUDE.md` before `WORK_ORDER.md`, and before touching the
ledger, the model or a run. At the time this folder was built that file had
sha256 `aceca6217c4b553fbcee582901ba5078aad59e8a7eb56125459340bd00df0e16`.
If the hash differs, the brief has moved; re-read it, and check the gap table
below against it.

This folder uses the forest ledger's SCHEMA and its checker unchanged:

```sh
LEDGER_ROOT=$PWD/meander-ledger python3 forest-model-ledger/tools/check_ledger.py --tests
python3 meander-ledger/tests/test_meander.py      # one line per test; exit 1 on any FAIL
```

## Where this folder does not yet do what the brief says

```text
brief step / rule                 state here
1 ANCHOR (closed, tagged base)    NOT DONE. No ledger/anchors/ entry. run_1's base closes
                                  sediment, but water and energy close by IDENTITY and
                                  momentum is VOID, so no base meets "L0 budgets close".
4 RETURN (re-close L0)            sediment re-closed every run; water/energy identity;
                                  momentum void (Q-05, Q-19).
ANCHOR TEST                       0 of 4 run. Seeds: 3 (lam/W 7.96..8.80). Assumption
                                  nudges: ablations in run_1, not a test record.
                                  Independent budgets: only one budget can fail.
TOOLBOX                           budget closure and coincidence card used (forest tools,
                                  read by import in a subprocess). Residual regression,
                                  equation-family swap, parameter recovery on synthetic
                                  data, assumption-block trace: not run. Parameter
                                  recovery is the cheapest next tool (Q-09).
7 CONNECT                         no convergence_anchors between any two branches.
toy convergence                   NOT grid-converged: ds 0.25 gives lam/W 2.62 (run_2).
```

## Packaging note

Both folders ship packages named `tools/` and `model/`. In one process they
collide, so `tests/test_l0.py` (the shim the forest checker imports) runs
`tests/test_meander.py` in a subprocess, and T_CARDS_READ / T_VERDICT_AGREES_FOREST
reach the forest code in subprocesses too. Do not import across the two folders
in one process.

## Conventions

stdlib only, parses under Python 3.9, CC0, ASCII in authored text. The work order
is verbatim in `WORK_ORDER.md`. Every number in a run file is recomputed by the
script its `code:` line names. The third-party dataset is fetched by
`tools/fetch_data.py` into `data/raw/` (git-ignored), pinned by commit and sha256.

## A defect in the shared checker (recorded, not repaired here)

`forest-model-ledger/tools/check_ledger.py` reads ledger files from `LEDGER_ROOT`
but resolves toolkit `code:` paths and anchor `code` paths against its own folder
(`HERE`), not `ROOT`. This folder has no toolkit .yaml and no anchors, so the
defect does not fire on it today. The first tool or anchor registered here would
be checked against the forest tree. The repair belongs in the forest folder.
