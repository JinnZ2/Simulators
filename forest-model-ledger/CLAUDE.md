# CLAUDE.md -- forest-model-ledger

Read the METHOD BRIEF below before `WORK_ORDER.md`, and before touching the
ledger, the model or a run. It is delivered text: verbatim, edited only on its
authors' own correction, with the superseded line kept under the block.
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
- The litter-guild + fire model (work-order run 5) looked plausible and leaked
  ~24 N units. Runs 1–4: N audit VOID. Flat equilibrium = the leak damping
  dynamics. Smooth ≠ correct.   [CORRECTED 2026-11-10, see below the block]
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

## Additions to the brief (by its authors; verbatim)

```text
ADD TO METHOD BRIEF — gate rule (Kavik, 2026-11-10)
If a toolbox trigger fires and the needed tool does not exist:
- mark the run INCOMPLETE (not resolved)
- log the missing tool as a placeholder in ledger/toolkit/
- add it to ledger/NEEDS_TOOL.md (tool, trigger that needed it, run, date)
- put "TOOL NEEDED: <name>" as the FIRST line of the report to Kavik
Never explain a trigger away without the tool.
```

Enforced by `tools/check_ledger.py`: every run carries a status; an INCOMPLETE
run must appear in `ledger/NEEDS_TOOL.md`; every tool named there must have an
entry in `ledger/toolkit/`. The first-line rule is for whoever writes the report.

```text
STANDING RULE (chat side, 2026-11-10 — housekeeping decisions, item 3)
wherever a conflict arises, branch instead of
overwrite — keep both versions, document the difference, decision stays with Kavik.
```

Not enforced by any checker. It applies to merge conflicts and to any two
versions of one thing: no side is picked, both stay inspectable, the
difference is written down per item.

## Status map (read before acting on any run or card)

`ledger/STATUS_MAP.md` says, for every run status and every card status, what
you may do from there by goal (trust it / explore / report now), what is
forbidden, and what moves it to another status. Two axes, never merged:

```text
RUN status   = did the loop finish?        COMPLETE | INCOMPLETE | REPORTED
CARD status  = how far to trust the read?  OPEN | PROVISIONAL | RESOLVED | CURIOSITY
```

The checker fails on any run or card whose status has no entry there.

## Corrections to the brief (by its authors; superseded text kept)

```text
2026-11-10  LESSONS ALREADY PAID FOR, first line. Corrected by the chat-side author
            ("my error"): the delivered line overclaimed.
  was:  - Runs 1–5 looked plausible and leaked ~24 N units. Flat equilibrium = the leak
          damping dynamics. Smooth ≠ correct.
  now:  the measured leak is the litter-guild + fire model only (work-order run 5).
        Runs 1-4: N audit VOID. The ledger already recorded it this way.
        The corrected wording inside the block is this session's rendering of that
        correction, not delivered text.
```

## Where the folder stands against the brief (2026-11-10, after run_10; revise as it moves)

```text
brief says                              folder has
--------------------------------------  ------------------------------------------------
ledger/toolkit/, 7 tools                budget_closure, coincidence_card, assumption_nudge.
                                        Of the brief's seven, ONE is built (budget closure);
                                        the other six are placeholders in ledger/toolkit/
anchor = frozen, TAGGED snapshot        ledger/anchors/ANCHOR_run9.yaml, status candidate;
                                        tag forest-model-ledger-anchor-candidate-run9 SET AT MERGE
                                        (every tag route from the session refused); commit
                                        55c651b is the pin;
                                        three code files pinned by sha256, checked every run
anchor test: 4 conditions               seeds PASS (wired, run_10); budgets PARTIAL (sigma void);
                                        nudges PARTIAL (run_11: 13 of 25 assumptions, 33 of 64
                                        nudges moved nothing, card OPEN); independent PARTIAL
RETURN closes C, N, P, water, energy    N and water close; C, P, energy print VOID
RETURN diffs against the anchor         no diff tool
BRANCH changes ONE component            no branch has been run from run_9 yet
"run the FULL toolbox" on a trigger     run_10 and run_11 ran what exists; six of seven do not.
                                        Both runs are INCOMPLETE under the gate rule;
                                        see ledger/NEEDS_TOOL.md
known error, left in place              N residual -5.0e-11 = deposition counter roundoff;
                                        branch BR_RUN_9B_COMPENSATED_COUNTER (placeholder)
run_9 is a CANDIDATE anchor, not an anchor
```

Do not edit `model/base.py`, `ledger/toolkit/budget_closure.py` or `runs/run_9.py`:
the candidate anchor pins them by hash and `tools/check_ledger.py` fails on drift.
A change to any of them is a new anchor candidate, not an edit.

## Commands

```sh
python3 tests/test_l0.py                  # L0 tests; prints its count
python3 tools/check_ledger.py --tests     # schema + cross-refs + admitting tests
python3 tools/check_ledger.py --selftest  # planted defects; each must fire
python3 runs/run_9.py                     # reproduces samples/run_9.sample.txt
python3 runs/run_10.py                    # reproduces samples/run_10.sample.txt (about a minute)
python3 runs/run_11.py                    # assumption nudges; several minutes; rewrites samples/run_11.json
python3 ledger/toolkit/coincidence_card.py  # reads every card
```

## Hard constraints

```text
void, never dropped     every schema field always present
gate rule               trigger + missing tool = run INCOMPLETE, tool placeholder, ledger/NEEDS_TOOL.md,
                        and "TOOL NEEDED: <name>" as the first line of the report
rejected entries stay   nothing deleted to make the ledger cleaner
admitted needs a test   named in ledger/tests.yaml, passing when run
reported != recomputed  runs 1-8 are carried; only runs with code in the tree are DERIVED here
delivered text          WORK_ORDER.md is never edited; the brief only on its authors' correction, logged
python 3, numpy         scipy allowed by the order, absent in the cloud build environment
```
