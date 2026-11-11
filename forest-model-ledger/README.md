# forest-model-ledger

A provenance-tracked ledger of forest model components. It holds equations,
what each assumes, what should be seen if an assumption fails, and which test
admitted it. It does not hold answers.

Read `CLAUDE.md` first: it carries the METHOD BRIEF, which governs before the work order.
Work order: `WORK_ORDER.md` (verbatim, co-authored, Kavik + Claude, 2026-11-10).
Claims: `CLAIM_TABLE.md`, `FML_001..024`; constants in `LOG.md`. CC0. *(non-stdlib: numpy)*

```text
ledger/components/*.yaml        one equation each: layer L0..L5, assumes, if_assumption_fails,
   |                            provenance, admitted_by, status
   |  grouped by
   v
ledger/branches/*.yaml          one per equation family; links; convergence_anchors
   |  share
   v
ledger/assumption_blocks/*.yaml one assumption, every component using it (checked both ways)

ledger/toolkit/*.yaml + *.py    tools: what each diagnoses, what it cannot see; cards/ = one per coincidence
ledger/anchors/*.yaml           anchor records: four tests, code pinned by sha256
ledger/tests.yaml               test ids an admission may cite
ledger/regime_map.yaml          families x regimes; every cell void
ledger/data_sources.yaml        listed, not retrieved
ledger/SCHEMA.yaml              the field list and the three rules

model/base.py                   N + water pool model; derivative built only from a flux table
model/l0_audit.py               re-export; the audit lives in ledger/toolkit/budget_closure.py
runs/run_N.md (+ .py)           seed, params, results, flags
tests/test_l0.py                the L0 tests
tools/check_ledger.py           schema, cross-references, admission <=> passing test
```

## Rules

```text
void, never dropped      every field always present; unfilled = void
rejected entries stay    2 rejected components are in the tree
admission needs a test   status admitted <=> admitted_by names a test that passes when run
reported != recomputed   runs 1-5 are logged as reported (code not in this tree); runs 6-8 are the original chat-side code, filed 2026-11-11
a void budget is VOID    never CLOSED, never 0; listed beside every overall verdict
```

## State

```text
components   3 admitted / 15 candidate / 4 placeholder / 2 rejected
branches     5 candidate / 10 placeholder
L0 budgets   N CLOSED, water CLOSED  |  C, P, energy VOID
boundary     deposition, leaching, fire volatilisation live  |  fixation, dust, groundwater, animal transport void
OBSERVED     0 field observations. Everything is model output or a proposed form.
             runs 6-8 carry provenance OBSERVED in the sense: original code and log, as executed chat-side.
toolkit      3 tools built, 6 placeholders (1 of the brief's 7 built)  |  cards: 1 PROVISIONAL, 2 OPEN
runs         5 REPORTED, 3 COMPLETE, 3 INCOMPLETE (tools missing: ledger/NEEDS_TOOL.md)
statuses     what each run / card status allows: ledger/STATUS_MAP.md
anchor       run_9 CANDIDATE: seeds PASS; budgets, nudges, independent budgets PARTIAL
```

Counts come from `python3 tools/check_ledger.py`; if this block and that
output disagree, the output is right.

## Commands

```sh
python3 tests/test_l0.py                  # L0 tests; prints its count
python3 tools/check_ledger.py --tests     # schema + cross-refs + admitting tests
python3 tools/check_ledger.py --selftest  # planted defects; each must fire
python3 runs/run_9.py                     # reproduces runs/run_9.md
python3 runs/run_10.py                    # the too-smooth trigger; reproduces samples/run_10.sample.txt
```

Python 3, numpy (`requirements.txt`). scipy installed on a later attempt in the build
environment; the base stays on its own RK4 because the candidate anchor pins that code. Pinned outputs in `samples/`. The work order allows scipy; nothing uses it yet. YAML is read
by `tools/miniyaml.py` (a strict subset, stdlib); PyYAML, when present, is used
only to cross-check that reader.
