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

---

## Second order, 2026-09-16

`WORK_ORDER_V2.md`, landed verbatim. Same six moves, a different output
shape, and one repair that is the whole point of the build.

The order names the file `move_set_sim.py`. That name holds a delivered
artifact which is never edited, so the build lands beside it as
**`move_set_sim_v2.py`** — both inspectable, neither overwritten
(`MSV_001`).

### The repair

    v1     verdict + blocker + unblocker          -> two non-empty strings
           "x" / "x" in every field               -> 6.0 of 6.0   (MV_002)

    v2     every entry checked AGAINST THE ARTIFACT
           same shape, same words                 -> 0.0 of 6.0   (MSV_003)
           an honest all-absence ledger           -> 6.0 of 6.0

`adaptive-claim-loop` `ACL_012`/`ACL_017`: a guard that asks for prose can
be satisfied with prose. The guards that hold ask for a number or a
computation.

### Three kinds of entry, one gate each

| kind | what the ledger supplies | what the artifact supplies | earned verdict |
|---|---|---|---|
| `QUOTE` | line + column range | the value, sliced out | `BOUND` |
| `DERIVED` | op, two operand locators, the stated value, `holds: true\|false` | the operands **and the precision they were written to** | `ARITHMETIC_AS_DECLARED` |
| `ABSENT` | reason, searched span, sought token | the span, and whether the token is in it | `VERIFIED_ABSENCE` |

Each scores **1.0**. A correctly-refused verdict scores as high as a
correct one, and neither scores on prose alone.

`ABSENT` is admitted by all six moves and is the whole subject of one
(`CHOICE 1` — the order's move list and its OUTPUT section read two ways
and the readings are not exclusive, so both are built). The delivered v1
resolved the same word the other way, and its `M6_absence` family is a
different move sharing an ordinal (`MSV_002`).

`tools/sourced.py` is **imported**, not reimplemented. It gates value /
source text / locator for mutual consistency and states itself that it
does not check whether the source is true. `bind_quote()` is that missing
layer: the locator resolves *into the artifact* and the cited text must be
the artifact's own line (`MSV_004`).

### The demo

    artifact : aperiodic-order-sim-stack/SIM_STACK_REPORT.txt
               already in this repo, cited by path, sha256-pinned,
               NOT copied (CHOICE 2 -- a copy is the MF_019 drift)
    ledger   : move-set/ledgers/sim_stack_report.json
    run      : python3 move-set/move_set_sim_v2.py --demo

**One** recomputable finding, and the move that used to carry the second
now refuses:

**M4 — `NOT_EVALUABLE`, and the refusal is the finding.** The report
states the AB–Poisson finite-size baseline as **0.021** (line 23) and
ships both dimensions that gap is between — AB 1.889 (line 15), Poisson
1.911 (line 17). Point-recomputed the gap is 0.022, and the first build
published that third decimal as a discrepancy. Both operands are written
to **three decimal places**:

    AB       1.889  ->  [1.8885, 1.8895]
    Poisson  1.911  ->  [1.9105, 1.9115]
    |diff|          ->  [0.0210, 0.0230]      0.021 is inside

The artifact is self-consistent at the precision it shipped. The 0.022 was
the rounding. Reported from outside this build; the claim is recorded
**VOID** rather than quietly removed (`MSV_006`), and the repair is
structural rather than a patch to one entry (`MSV_017`).

All four of the artifact's stated relationships — 0.334, 0.021, 1.460,
54.1 — fall inside their own shipped bands. **M4 establishes nothing on
this document, and that is the result** (`MSV_018`). The demo total falls
**6.0 → 5.0**; the fall is the instrument working, since a harness that
scored higher before was scoring a rounding.

**M6.** Line 41 reports a peak/floor ratio of 5537. The floor is on line
40; **the peak height is nowhere in the artifact**. Three of the
document's four stated relationships recompute from operands it supplies;
this one does not, because its operands were not published. Not zero and
not unknown (`MSV_007`).

A contamination block prints **before** the numbers: the ledger was
authored by the session that wrote the harness, this repo already carries
`AOS_001..AOS_010` on the same artifact, and a self-run is void as a
capability score (`FLB_010`). Only the mechanical layer is scored; no
reading is (`MSV_011`).

### Shipped precision, and why M4 refutes but never confirms

An artifact that rounds an operand to three decimal places has not stated
the recomputed quantity to better than the band those roundings span. So
the precision is parsed from each operand **as written** — not through a
float, which has already thrown it away — and propagated through the
operation:

| stated value | ledger says | verdict | points |
|---|---|---|---|
| inside the band | `holds: false` | `NOT_EVALUABLE` | 0.0 |
| inside the band | `holds: true` | `NOT_EVALUABLE` | 0.0 |
| outside the band | `holds: false` | `ARITHMETIC_AS_DECLARED` | 1.0 |
| outside the band | `holds: true` | `ARITHMETIC_NOT_AS_DECLARED` | 0.0 |

`ARITHMETIC_AS_DECLARED` is reachable only from `holds: false`, so
**holds=True is unearnable** (`MSV_019`). That is correct rather than a
limitation: a band containing the stated value is *consistency*, not
confirmation — it says the artifact did not contradict itself at the
precision it published, which is true of almost every table ever printed.

The stipulated tolerance this replaces (relative 5e-3) is **retired in
place** as choice 3 rather than renumbered (`MSV_021`) — a constant
standing in for a quantity the document already carries, which is the
`reasoning-gate` **G-RES** shape with the artifact's own significant
figures as the instrument.

Containment is tested in `decimal.Decimal`, not float: on the demo case
the exact band is `[0.0210, 0.0230]` and the float lower bound computes
as `0.02100000000000013`, so a float test returns **False** by 1.3e-16 on
a quantity whose smallest meaningful unit is 5e-4 — and would have
produced a finding on the one case the repair exists to refuse
(`MSV_020`). An epsilon would have been a second stipulated constant
replacing the one just retired.

Two choices are set one-sided toward refusing rather than reporting: an
operand with no decimal point takes half-width 0.5, which is wrong for an
exact count and errs toward `NOT_EVALUABLE` (`MSV_022`); and the stated
value is read as a point rather than widened to its own band, for the
same reason.

### Reported, not repaired: provenance of the known-answer registry

Asked for alongside the M4 defect, explicitly as a report.

**Authorship.** 19 of the 20 commits touching `tools/known_answer.py` are
model-authored; the twentieth is a merge carrying another branch's
registrations and authors no case. Every expected value in the registry
was written by one author, and that author also wrote the functions being
checked.

**Ordering, measured rather than asserted** — earliest commit introducing
`def <fn>` against earliest commit introducing its registration string:

    registered in the SAME commit as the implementation   16
    implementation first, registered later                 8
    answer registered BEFORE the implementation existed     0
    unknown (registered this session, uncommitted)          1

**Zero of 25.** Not one expected value was fixed before the function it
checks existed — including the two seed cases the file's own docstring
describes as answers *"fixed in advance"*, both of which are
implementation-first.

**Scope limit on the 26/26.** It means every registered case agrees with
the current implementation, authored by the same party with knowledge of
it. It is a **regression** result, not a validation one. What would change
that: an expected value traceable to a source outside this repository, to
a commit preceding the implementation, or to a second author. None of the
26 meets any of the three (`MSV_023`).

One defect surfaced while making that claim checkable: the move-set
registrations were reachable only from the module tail, so the CLI read
26/26 COMPLETE while a clear-and-reseed lost both. Repaired, and recorded
as the third instance of that shape in this registry (`MSV_024`).

### What the order did not fix and this does

`MV_004` — `order` is a required ledger field, `read_ledger` refuses a
ledger without one, and `path_dependence` returns `NOT_EVALUABLE` rather
than a pass for fewer than two runs, zero runs, or runs that do not
declare distinct orders (`MSV_008`).

`MV_005` — there is no `NO_FINDING` verdict. A clean read is a `QUOTE`
citing the thing that checks out and scores like any other (`MSV_009`).

### What it does not do

`coverage` — distinct artifact lines searched, overlaps counted once — is
printed beside every verified absence and **enters no arithmetic**. A
verified absence over 3% and one over 100% both score 1.0, and nothing
here separates a well-chosen narrow span from a cherry-picked one
(`MSV_010`). The sought-token search is a word list and is named as one at
the point of use (`MSV_012`).

### Running it

    python3 move-set/move_set_sim_v2.py                     # the six moves
    python3 move-set/move_set_sim_v2.py --choices
    python3 move-set/move_set_sim_v2.py --emit ARTIFACT --seed 7
    python3 move-set/move_set_sim_v2.py --score LEDGER ARTIFACT
    python3 move-set/move_set_sim_v2.py --demo
    python3 move-set/move_set_sim_v2.py --paths RUN1 RUN2 ARTIFACT
    python3 move-set/test_move_set_v2.py                    # check count printed

`move_set_sim_v2.py` refuses `--selftest` (exit 2) rather than exiting
clean on an invocation that runs nothing. `coverage` is registered in
`tools/known_answer.py` with six cases; the overlap case is the detector.
Claims `MSV_001..MSV_024` in `CLAIM_TABLE_V2.md`.
