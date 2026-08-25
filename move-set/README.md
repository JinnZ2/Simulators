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

| file | |
|---|---|
| `move_set_sim.py` | the move set, the scorer, the falsifier. Delivered verbatim |
| `ledgers/wolf_dominance.json` | one filled run. Delivered verbatim |
| `move_set_audit.py` | checks. Imports, edits nothing. `--selftest` |
| `CLAIM_TABLE.md` | `MV_001..MV_009` with a REFUTATION_PROTOCOL |
| `samples/audit.sample.txt` | pinned audit output |

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

## Running it

    python3 move-set/move_set_sim.py                       # the move set
    python3 move-set/move_set_sim.py --emit "some artifact" --seed 7
    python3 move-set/move_set_sim.py --score move-set/ledgers/wolf_dominance.json
    python3 move-set/move_set_audit.py --selftest
    python3 move-set/move_set_audit.py

Stdlib only, parses under Python 3.9, CC0.

Siblings: `adaptive-claim-loop/` (response classes and the STAND move,
where `ACL_012`'s repair lives), `reasoning-gate/` (a gate between a
simulation and its conclusions), `observer-exclusion/` (the same wolf
case from the lead-time side, `MV_008`), `null-harness/` (the
known-null/known-signal invariant the scorer here is tested against).
