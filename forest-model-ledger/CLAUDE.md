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

## Where the folder stands against the brief (2026-11-11, after run_21; revise as it moves)

```text
brief says                              folder has
--------------------------------------  ------------------------------------------------
ledger/toolkit/, 7 tools                2026-11-11 staged build: all seven built and gated (tests/test_toolkit.py:
                                        known answers + null harness FP 0 / TP 1, harness seeds 0-4).
                                        Held-out gate (tests/test_heldout.py; thresholds frozen by hash first,
                                        HELDOUT_FREEZE.md): 4 PASS; multi_seed_ensemble, ablation,
                                        assumption_block_trace FAIL and are trust PROVISIONAL, not retuned.
                                        equation_family_swap is an ADAPTER (frozen file) bound to the engine
                                        (relational-playground, PR #257) by rp_engine.py: run_21 ran it on the
                                        engine's own fire grid; no ledger component has a second family there.
                                        assumption_block_trace is a placeholder until real data.
                                        Also: coincidence_card, assumption_nudge, attribution_directionality
anchor = frozen, TAGGED snapshot        ledger/anchors/ANCHOR_run9.yaml, status candidate;
                                        archive branch archive/anchor-run9 at 55c651b (no tag; 2026-11-11)
                                        (every tag route from the session refused); commit
                                        55c651b is the pin;
                                        three code files pinned by sha256, checked every run
anchor test: 4 conditions               seeds PASS (wired, run_10); budgets PARTIAL (sigma void);
                                        nudges PARTIAL (run_11: 13 of 25 assumptions, 33 of 64
                                        nudges moved nothing, card OPEN; run_15 split the 33:
                                        18 hidden in noise, 9 absorbed, 2 seed-specific, 2 inert,
                                        2 unresolved at delta 0.5 sd; run_20: HIDDEN 23..15 and
                                        ABSORBED 4..12 over 0.40-0.60 sd); independent PARTIAL
RETURN closes C, N, P, water, energy    N and water close; C, P, energy print VOID
RETURN diffs against the anchor         no diff tool
BRANCH changes ONE component            no branch has been run from run_9 yet
"run the FULL toolbox" on a trigger     run_14..18 re-ran the triggers with the built tools; rows cleared
                                        into NEEDS_TOOL.md's Cleared table. run_10..15 stay INCOMPLETE:
                                        equation_family_swap (engine found, no ledger component under a
                                        second family) and assumption_block_trace (no real data) are still
                                        owed, and CC_004/CC_005 rows are unrun. CC_001 back to PROVISIONAL:
                                        it rests on run_14, where two now-PROVISIONAL tools ran
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
python3 runs/run_12.py                    # attribution_directionality on second-hand seeds; reproduces samples/run_12.sample.txt
python3 runs/run_13.py                    # same tool on first-hand records vs sha-pinned texts; diff against run_12
python3 tests/test_toolkit.py             # the seven tool gates; one line per tool and per null leg
python3 runs/run_14.py                    # CC_001 recheck: multi_seed_ensemble + ablation (about a minute)
python3 runs/run_15.py                    # the 33 non-moving nudges classified (about four minutes, 4 workers)
python3 runs/run_16.py                    # support_match on first-hand cases a-d, before / after
python3 runs/run_17.py                    # parameter_recovery, six parameters
python3 runs/run_18.py                    # residual_regression on N misclosure, 36 configurations
python3 tests/test_heldout.py             # held-out gate; refuses if a frozen tool file changed
python3 runs/run_19.py                    # support_match on a blind coder's records and labels
python3 runs/run_20.py                    # run_15's near-threshold classes over delta 0.40-0.60 sd (about 30 s)
RELATIONAL_PLAYGROUND_PATH=<checkout>/relational-playground python3 runs/run_21.py   # swap on the engine (about 6 min)
python3 runs/run_22.py                    # support_match on case e (first-hand, not author-written); reproduces samples/run_22.sample.txt
python3 tools/check_ledger.py --owed-mode original|owed|proposed   # original is the default; Kavik picks
```

## Hard constraints

```text
void, never dropped     every schema field always present
gate rule               trigger + missing tool = run INCOMPLETE, tool placeholder, ledger/NEEDS_TOOL.md,
                        and "TOOL NEEDED: <name>" as the first line of the report
rejected entries stay   nothing deleted to make the ledger cleaner
admitted needs a test   named in ledger/tests.yaml, passing when run
reported != recomputed  runs 1-5 are carried; only runs with code in the tree are DERIVED here (6-8 since 2026-11-11)
delivered text          WORK_ORDER.md is never edited; the brief only on its authors' correction, logged
python 3, numpy         scipy allowed by the order, absent in the cloud build environment
```
