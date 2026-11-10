# forest-model-ledger

A provenance-tracked ledger of forest model components. It holds equations,
what each assumes, what should be seen if an assumption fails, and which test
admitted it. It does not hold answers.

Work order: `WORK_ORDER.md` (verbatim, co-authored, Kavik + Claude, 2026-11-10).
Claims: `CLAIM_TABLE.md`, `FML_001..012`. CC0. *(non-stdlib: numpy)*

```text
ledger/components/*.yaml        one equation each: layer L0..L5, assumes, if_assumption_fails,
   |                            provenance, admitted_by, status
   |  grouped by
   v
ledger/branches/*.yaml          one per equation family; links; convergence_anchors
   |  share
   v
ledger/assumption_blocks/*.yaml one assumption, every component using it (checked both ways)

ledger/tests.yaml               test ids an admission may cite
ledger/regime_map.yaml          families x regimes; every cell void
ledger/data_sources.yaml        listed, not retrieved
ledger/SCHEMA.yaml              the field list and the three rules

model/base.py                   N + water pool model; derivative built only from a flux table
model/l0_audit.py               budget closure, boundary audit line, leak-vs-noise verdict
runs/run_N.md (+ .py)           seed, params, results, flags
tests/test_l0.py                the L0 tests
tools/check_ledger.py           schema, cross-references, admission <=> passing test
```

## Rules

```text
void, never dropped      every field always present; unfilled = void
rejected entries stay    2 rejected components are in the tree
admission needs a test   status admitted <=> admitted_by names a test that passes when run
reported != recomputed   runs 1-8 are logged as reported (code not in this tree); only run_9 runs here
a void budget is VOID    never CLOSED, never 0; listed beside every overall verdict
```

## State

```text
components   3 admitted / 15 candidate / 4 placeholder / 2 rejected
branches     5 candidate / 9 placeholder
L0 budgets   N CLOSED, water CLOSED  |  C, P, energy VOID
boundary     deposition, leaching, fire volatilisation live  |  fixation, dust, groundwater, animal transport void
OBSERVED     0 entries. Everything is model output or a proposed form.
```

Counts come from `python3 tools/check_ledger.py`; if this block and that
output disagree, the output is right.

## Commands

```sh
python3 tests/test_l0.py                  # L0 tests; prints its count
python3 tools/check_ledger.py --tests     # schema + cross-refs + admitting tests
python3 tools/check_ledger.py --selftest  # planted defects; each must fire
python3 runs/run_9.py                     # reproduces runs/run_9.md
```

Python 3, numpy (`requirements.txt`). Pinned outputs in `samples/`. The work order allows scipy; nothing uses it yet. YAML is read
by `tools/miniyaml.py` (a strict subset, stdlib); PyYAML, when present, is used
only to cross-check that reader.
