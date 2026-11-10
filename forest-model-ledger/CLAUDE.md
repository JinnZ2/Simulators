# CLAUDE.md -- forest-model-ledger

Read the METHOD BRIEF below before `WORK_ORDER.md`, and before touching the
ledger, the model or a run. It is delivered text: verbatim, never edited here.
Where this folder does not yet do what the brief says, the gap is listed
under it, not smoothed over.

## METHOD BRIEF (verbatim, delivered 2026-11-10)

```text
METHOD BRIEF — read before the work order (co-authored, Kavik + Claude, 2026-11-10)

PURPOSE
Build a reasoning method, not results. Outputs are trail markers. Do not optimize
for clean or plausible-looking outcomes. A smooth result is a trigger, not a success.

FRAME: glacier pathfinding
- Anchor = frozen, tagged snapshot (code + params + seed) whose L0 budgets close.
- Rope = provenance chain + version control. Every branch must be able to return
  to its exact anchor state.
- Branches = several routes from one anchor when the ground is unknown.
  Dead ends and reroutes are kept as map data, never deleted.
- New anchor only after testing the ground (rule below).

LOOP (every branch)
1 ANCHOR   start from a closed base; record its scope
2 BRANCH   change ONE component; list its assumptions A1..An and the failure
           signature expected if each one breaks
3 RUN      record seed, params, code
4 RETURN   re-close L0 budgets (C, N, P, water, energy) → report misclosure;
           diff against the anchor. Mandatory. Nothing counts as explored without it.
5 READ     inside noise → branch holds in this scope
           outside noise → match to failure signatures → toolbox
6 LABEL    conditions, sensitivity, surprises, provenance
           (OBSERVED | DERIVED | PROPOSED), status
           (candidate | admitted | rejected | placeholder)
7 CONNECT  independent branches converging = candidate anchor
8 FREEZE   anchors change only when they fail against data (highest bar, still revisable)

ANCHOR TEST (candidate → anchor)
- budgets close to within measurement-noise rule
- holds across multiple seeds
- holds when each assumption is nudged
- independent budgets close together (guards against compensating errors)

TOOLBOX TRIGGERS
- unexpected deviation
- result too smooth / adds up but doesn't sit right
- nudging an assumption moves nothing (something is absorbing the change)
On trigger: run the FULL toolbox, including tools that seem irrelevant.
Choosing only "relevant" tools lets expectation limit discovery.

TOOLBOX (ledger/toolkit/, each tool lists the deviations it diagnoses)
- budget closure / misclosure → leaks, missing fluxes, boundary gaps
- residual regression on method fields → measurement artifacts vs biology
- ablation (drop one variable) → what actually matters
- multi-seed ensembles + variance → stochastic effects, early-warning spikes
- equation-family swap (ODE | percolation | Ising | spin glass | MaxEnt |
  branching process | random-matrix stability) → regime handoffs
- parameter recovery on synthetic data → can the pipeline see what it claims
- assumption-block trace → shared assumption failing across many studies

LESSONS ALREADY PAID FOR
- Runs 1–5 looked plausible and leaked ~24 N units. Flat equilibrium = the leak
  damping dynamics. Smooth ≠ correct.
- Pairwise-additive prediction failed (impossible negative biomass) → system is
  combinatory; never build the whole from pairs alone.
- Mean-field ODE wrong exactly near thresholds; percolation variance spikes there.
- A convergence seen in one toy with chosen coefficients is a CANDIDATE anchor,
  not an anchor.

LABELING RULES
- Unfilled fields stay void, never dropped. More slots > fewer.
- Placeholders for every open branch so nothing is lost.
- No claims beyond scope. "Doesn't generalize" ≠ "no support" ≠ "unmeasured".
- Report flat: found / scope / unresolved. No hedging, no smoothing.

WHEN UNSURE
Ask one question rather than filling the gap from typical practice.
```

## Where the folder stands against the brief (2026-11-10; revise as it moves)

```text
brief says                              folder has
--------------------------------------  ------------------------------------------------
ledger/toolkit/, 7 tools                ABSENT. Only budget closure exists (model/l0_audit.py)
anchor = frozen, TAGGED snapshot        run_9 is committed, not tagged; no anchor record
anchor test: 4 conditions               seeds 0..9 done; assumption nudges NOT run;
                                        independent budgets: 2 live, 3 void
RETURN closes C, N, P, water, energy    N and water close; C, P, energy print VOID
RETURN diffs against the anchor         no diff tool
BRANCH changes ONE component            no branch has been run from run_9 yet
run_9 is therefore a CANDIDATE anchor, not an anchor
```

## Commands

```sh
python3 tests/test_l0.py                  # L0 tests; prints its count
python3 tools/check_ledger.py --tests     # schema + cross-refs + admitting tests
python3 tools/check_ledger.py --selftest  # planted defects; each must fire
python3 runs/run_9.py                     # reproduces samples/run_9.sample.txt
```

## Hard constraints

```text
void, never dropped     every schema field always present
rejected entries stay   nothing deleted to make the ledger cleaner
admitted needs a test   named in ledger/tests.yaml, passing when run
reported != recomputed  runs 1-8 are carried; only runs with code in the tree are DERIVED here
delivered text          WORK_ORDER.md and the brief above are never edited
python 3, numpy         scipy allowed by the order, absent in the cloud build environment
```
