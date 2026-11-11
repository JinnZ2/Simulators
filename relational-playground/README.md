# relational-playground

A laboratory for swapping equations, boundaries and controls on one system and
recording where each description holds. Built to `SPEC_GPT.md` (GPT,
2026-11-10, verbatim) plus eight additions from the method brief in
`forest-model-ledger/CLAUDE.md` (`WORK_ORDER.md`, verbatim). Stdlib only. CC0.

Status: instrument built and tested; one experiment run. Nothing here is a
finding about any real forest, organism or AI system. Every parameter is
hand-set and labelled ASSUMED.

## Energy map

```text
SystemDefinition (A) --- several BoundaryMatrix (C) may coexist; none is chosen for you
RelationalMatrix (B) --- directed edges; no reverse edge unless written
ControlMatrix (D) ------ held / varied / perturbed + three observer-regime fields
UncertaintyMatrix (F) -- every number has a status and provenance; unknowns raise
        |
        v
MODEL(state, environment, relationships, controls, parameters)   <- any registered equation
        |
        v
runner.run(config) -- RK4 or step, discrete events, same code for every equation
        |
        +-- L0 gate ............ budgets close or the run is INCOMPLETE
        +-- known-answer gate .. model not through it => UNTRUSTED => INCOMPLETE
        +-- expiry report ...... every UNKNOWN / NOT MEASURED and what would end it
        +-- claims ............. OBSERVED / DERIVED / PROPOSED
        v
record: 12 outputs (spec section 8) + budgets + boundary audit + provenance hashes
        |
        v
analysis: applicability (no score) | transitions | identifiability | failure region | coincidence card
ContinuityMatrix (E) reads trajectories: reorganized is not ceased
```

## Refusals, and where each lives

```text
unknown used as a number          uncertainty.Value.number() raises
parameter missing                 equations/base.Model raises; no default
automatic boundary choice         boundaries.choose() raises
model ranking / score             comparison.rank(), applicability.score() raise
failed sweep point                kept as a MODEL FAILED row
run with a leak or no LIVE budget INCOMPLETE (l0.run_status)
untested equation                 INCOMPLETE (known_answer_gate)
UNKNOWN with no exit stated       refused; VOID is allowed and counted
value status used as a claim tag  claims.claim() raises
cross-system comparison           refused until all observer regimes are declared
two-change branch                 anchor.branch() raises
slot set without evidence         coincidence.set_slot() raises
```

## The eight additions (one commit each)

```text
1 L0 GATE            playground/l0.py                 mass / N / C / water / energy, each LIVE or VOID with a reason
2 ANCHOR LOOP        playground/anchor.py             freeze, verify, one-change branch, RETURN diff, four anchor tests
3 KNOWN-ANSWER GATE  playground/known_answer_gate.py  12 clean + 12 planted draws per model; pass = FP 0 and TP 1
4 EXPIRY             playground/uncertainty.py        expiry_condition; ABSENT_AT_SENSITIVITY(<value>)
5 CLAIM TAGS         playground/reporting/claims.py   separate axis from value statuses
6 OBSERVER REGIMES   playground/controls.py           perturbation / reactivity / strategy
7 EQUATION FAMILIES  equations/percolation.py, branching.py
8 COINCIDENCE CARD   playground/analysis/coincidence.py
```

Reused from the tree, not copied: `divergence-playground/coincidence.py`
(loaded by path), `tools/known_answer.py` (three metrics registered there).
Restated in stdlib, because the original imports numpy or its own loader:
the closure verdict rule of `forest-model-ledger/ledger/toolkit/budget_closure.py`,
the FP/TP classes of `null-harness/null_harness.py`, the reading rule of the
forest ledger's coincidence card.

## First experiment: experiments/model_comparison/forest_fire_regime/

`PREREG.md` was committed before the code that runs it. `RESULTS.txt` is the
output. Runs 6-8 of the forest ledger have no code, seed or parameters in the
tree, so:

```text
PART 1  port of run 9 (the in-tree rebuild of run 6)      9 of 9 targets MET
        fires 80, N misclosure -5.062e-11 (CLOSED), water -3.426e-13 (CLOSED),
        final pools equal to run 9 at 4 decimals, planted leak read as LEAK (-72.64, 59 fires).
        The random draws are numpy's, exported once to fixtures/ and replayed.
        With stdlib's own stream both budgets also close (80 fires).
        Run 6 as logged (47 fires, ~1e-9) is not reproduced: its code is void.

PART 2  rebuild of runs 7-8, one design fixed in advance   2 of 4 logged features appear
        F1 ODE overpredicts up to ~60x .............. DOES NOT APPEAR  (max 14.9x at drought 0.4)
        F2 grid threshold 0.6-0.7, variance spike ... APPEARS          (steepest 0.55-0.60, variance peak 0.60)
        F3 spot 0.2 converges at drought >= 0.5 ..... DOES NOT APPEAR  (inside the 0.05 window from 0.55 up; gap 0.0526 at 0.50)
        F4 5% spotting drops threshold to ~0.5 ...... APPEARS          (steepest 0.50-0.55)
        Under the gate rule PART 2 is INCOMPLETE: see NEEDS_TOOL.md.
        21 coincidence cards opened by grid/ODE agreement, all OPEN.
```

The design of PART 2 is the building session's. A feature that does not appear
says something about this design; the original design is not on record.

## Commands

```sh
cd relational-playground/tests && python3 -m unittest discover -s .      # prints its count; about 25 s
cd relational-playground/experiments/model_comparison/forest_fire_regime
python3 run.py            # both parts, about 2.5 min; rewrites out/ and RESULTS.txt
python3 run.py part1
python3 export_draws.py   # needs numpy; only to re-export the fixture
python3 ../../../../tools/known_answer.py | tail -8                      # repo registry, three playground metrics
```

## Limits

```text
budgets          a run's closure covers LIVE budgets only; C and energy are VOID in every run so far
gate             closed-form cases cover parts of each model, not all of it (forest_n: 4 of 13 fluxes)
observer fields  the meaning given to perturbation / reactivity / strategy is this build's reading (PROPOSED)
C5, C6           named in the work order; the source file holds C1-C4; not invented
spec phases      1-2 built; 3 (boundary variation) has the tools and one test, no experiment;
                 4-6 not run. The four other experiments/ folders are empty.
boundary engine  spec section 6 (interior / interface / exterior measurements, hysteresis runs): hysteresis() exists, nothing else
factorial matrix parameter_sweep covers parameters; boundary / control / environment factors are swapped by hand
```
