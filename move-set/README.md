# move-set

An audit reproduced as a **move set** rather than a reasoning trace.

The claim: *the chain is path-dependent, the moves are not.* Each move's
trigger is a property of the artifact — "artifact ships a number",
"artifact reports an aggregate" — not of the previous answer, so the
moves can be asked in any order. `move_set_sim.py` ships the set, a
scorer, and a falsifier for that claim.

The scoring rule is what the folder is for: **a correctly-refused
verdict scores as high as a correct one.** Five refusal verdicts
(`NOT_DERIVABLE`, `NOT_SEPARABLE`, `NOT_ADDRESSABLE`, `SHARE_IS_NONE`,
`INSTRUMENT_BLIND`) score 1.0 exactly as `RESOLVED` does, and
`refusal_fraction` is reported and never penalized. Evals that score
answers only never select for the absence moves.

Delivered verbatim: `move_set_sim.py` and `ledgers/wolf_dominance.json`,
a filled run against the wolf-dominance correction. Audit in
`move_set_audit.py`, which imports both and modifies neither.

**Second drop, 2026-08-26.** `move_set_sim.py` was superseded in place
by a revision that splits the single absence move into six
(`M6a_sequence_gap`, `M6b_interval_unaccounted`, `M6c_negative_space`,
`M6d_required_unfiled`, `M6e_orphan_link`, `M6f_no_denominator`), names
established prior art per sub-move — sequence gap analysis, timeline
reconstruction, negative space, absent expected document, link
analysis, base-rate audit — and adds a compatibility path so ledgers
written before the split still score. Six moves became eleven. The
pre-split module is at commit `b840e52` and is deliberately **not**
kept as a second copy in the tree; a stale copy is what
`tools/check_gate_drift.py` exists to catch.

The delivered ledger predates the split, so it is the legacy case its
own compatibility path handles.

| file | |
|---|---|
| `move_set_sim.py` | the move set, the scorer, the falsifier. Delivered verbatim |
| `ledgers/wolf_dominance.json` | one filled run. Delivered verbatim |
| `move_set_audit.py` | checks. Imports, edits nothing. `--selftest` |
| `CLAIM_TABLE.md` | `MV_001..MV_013` with a REFUTATION_PROTOCOL |
| `samples/move_set_audit.sample.txt` | pinned audit output |

## What the audit found

**The guard the module says everything rests on does not hold.** The
docstring names it — *"a bare 'I don't know' is not a refusal and scores
zero. This is the only thing keeping symmetric scoring from being
gameable"* — and the implementation checks that two strings are
non-empty. Null-tested: a ledger with `"x"` in every blocker and
unblocker scores **6.0 of 6.0**, identical to the delivered run.
`adaptive-claim-loop` `ACL_012` is the same finding and already carries
the repair: ask for a number, not a sentence.

**The falsifier tests its consequence without checking its
precondition.** `path_dependence` compares `(move, verdict)` sets across
runs, which is order-invariant and correct — but nothing checks that the
runs it was handed used *different orders*. Two byte-identical copies of
one ledger return `ORDERLESS -- claim holds`. And the precondition is
not merely unchecked: `emit()` returns an `order` key and the
`ledger_schema` it ships in the same dict has no field for it, so a
filled ledger cannot say which order produced it. One field fixes it.

**At zero runs the falsifier reports order dependence; at one run it
reports a pass.** Both edges wrong, in opposite directions.

**The delivered ledger contradicts itself on venue tier.** M3 says
same-authorship makes venue-tier confounds drop out; M5 says a book is
undercounted relative to a journal article — and M3's own locator names
the pair as a 1970 book and a 1999 article. M5 is right. Nothing in the
harness compares entries to each other, which is a real cost of
orderlessness rather than a defect: a cross-entry check reintroduces the
dependency the design removes.

## What the split changed

**One readout was repaired and two were reached.** The revision
anticipated that a pre-split total and a post-split total are not
comparable and emits a row saying so. The same bundling also reaches
the *completeness* readout, and nothing says anything about that one:
`score()` does `seen.update(LEGACY[mv])`, so one bundled entry marks
all six sub-moves as run. The delivered ledger reports
`moves_not_run: []` — nothing missing — while scoring **6.0 of 11.0**,
with five points of its own denominator unreachable by it. A reader
taking the completeness readout at face value reads a complete run
(`MV_010`).

**The stated reason names four findings and the split makes six**
(`MV_011`). The reasoning is sound either way; the number in the
sentence is not the number of pieces.

**`LEGACY_ADMITS` is exactly its successors' union today, and it is a
hand-written literal** (`MV_012`). The derivation is one comprehension
over `LEGACY` and `MOVES`. Four of the seven verdicts are admitted by
one or two of the six successors, so removing `SHARE_IS_NONE` from
`M6f_no_denominator` would leave the literal admitting a verdict no
successor does, silently. Same arrangement as `reasoning-gate`'s
`guards.json → GUARDS.md`, with the generation step available and
unused.

**The ceiling moved and the gate did not** (`MV_013`). `score_entry`
is byte-identical across the revision, so the garbage ledger — right
shape, `"x"` in every blocker and unblocker — went from 6.0 of 6.0 to
**11.0 of 11.0**. A change to the move inventory moves the score
ceiling, and the score ceiling is what the anti-gaming guard defends.

The prior-art additions are the revision's strongest move: eight of
eleven moves now name an established investigative instrument, so a
picker-up does not have to defend a new one. The three that do not
(`M2_substitution`, `M4_perturb`, `M5_self_report`) are the three the
comment does not discuss.

## Running it

    python3 move-set/move_set_sim.py                       # the move set
    python3 move-set/move_set_sim.py --emit "some artifact" --seed 7
    python3 move-set/move_set_sim.py --score move-set/ledgers/wolf_dominance.json
    python3 move-set/move_set_audit.py --selftest
    python3 move-set/move_set_audit.py

63 checks.

Stdlib only, parses under Python 3.9, CC0.

Siblings: `adaptive-claim-loop/` (response classes and the STAND move,
where `ACL_012`'s repair lives), `reasoning-gate/` (a gate between a
simulation and its conclusions), `observer-exclusion/` (the same wolf
case from the lead-time side, `MV_008`), `null-harness/` (the
known-null/known-signal invariant the scorer here is tested against).
