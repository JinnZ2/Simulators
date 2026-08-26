# CLAIM TABLE — move-set

`MV_001..MV_013`. Claims about the delivered `move_set_sim.py` and its
filled ledger, both landed verbatim and modified by nothing.

**Second drop, 2026-08-26.** `move_set_sim.py` was superseded in place
by a revision splitting the single absence move into six
(`M6a..M6f`), naming prior art per sub-move, and adding a
compatibility path for ledgers written before the split. The
pre-split module is at commit `b840e52`; it is not kept as a second
copy in the tree, because a stale copy is what
`tools/check_gate_drift.py` exists to catch. The delivered ledger
predates the split, so it is the legacy case its own compatibility
path handles. `MV_001..MV_009` were re-run against the revision;
`MV_010..MV_013` are new.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered module. Where a check and a claim disagree,
the disagreement goes in the checker's output.

Nothing here is a statement about whether the wolf-dominance reading in
the ledger is correct. The ledger is read as a **run of the harness**;
its subject-matter facts are carried and egress-blocked (`MV_009`).

---

### MV_001 — the target is right, and the design is symmetric on verdict class

The stated purpose: *a correctly-refused verdict scores as high as a
correct one, because current evals score answers only, so the absence
moves never get selected for.*

The design does what it says. Five refusal verdicts and one answer
verdict are scored identically at 1.0, `refusal_fraction` is reported
and explicitly never penalized, `moves_not_run` is first-class, and each
move declares its own `admits` list so a verdict outside it scores zero.
The delivered run is 4 refusals and 2 answers and scores 6.0 of 6.0.

That is the whole point of the folder and it is built, not asserted.

**Falsifier:** a refusal verdict scoring below an answer verdict.

**Status: SUPPORTED.**

---

### MV_002 — the anti-gaming guard checks that two strings are non-empty

The docstring names the guard and says what rests on it:

> A bare 'I don't know' is not a refusal and scores zero. This is the
> only thing keeping symmetric scoring from being gameable.

The implementation:

    if e.get("blocker") and e.get("unblocker"):
        return 1.0, "earned refusal"

Null-tested. A ledger with the right shape and one character in every
field:

    delivered run                             6.0 of 6.0
    every blocker and unblocker is `"x"`      6.0 of 6.0

**Identical.** The scorer separates a run that names five specific
blockers and five specific measurements from a run that types `x` twelve
times by nothing at all.

This is `adaptive-claim-loop` `ACL_012` exactly — *the rule says "name
why", the implementation checks a string is non-empty* — and that folder
already carries the repair: `ResolutionEdit` requires HAVE and NEED as
**numbers**, with need beyond have. The refusal classes here have the
same shape available. `SHARE_IS_NONE` could require the numerator and
the attempted denominator; `NOT_DERIVABLE` could require the identifier
that was looked up and the endpoint that returned nothing — both of
which the delivered ledger already supplies in prose.

`ACL_017` bounds what the repair buys: the guards that held against an
adversary were the two asking for a NUMBER or a COMPUTATION, and a guard
that asks for prose can be satisfied with prose.

**Falsifier:** a garbage ledger scoring below the delivered one.

**Status: SUPPORTED — the guard the module says everything rests on does
not hold.**

---

### MV_003 — the falsifier returns a verdict on no data and a pass on one run

    runs=0   orderless=False   "CHAIN DETECTED -- findings depend on move order"
    runs=1   orderless=True    "ORDERLESS -- claim holds"

Zero runs returns a **positive finding of order dependence**, because
`len(set([])) == 1` is False. One run returns a **pass**, because
`len({one_set}) == 1` is True.

Both edges are wrong and they are wrong in opposite directions, which is
the giveaway that the count was never checked. Neither is a measurement:
the comparison needs at least two runs, and the function accepts any
number including none.

`PCH_001` is the same shape — a predicate whose empty result set returns
the confirming branch — and this folder's own `M6_absence` move exists
to catch exactly it.

**Falsifier:** a run count below two returning something other than a
verdict.

**Status: SUPPORTED.**

---

### MV_004 — the falsifier tests its consequence without checking its precondition

Sharper than `MV_003`, and it survives fixing the count.

The claim under test is *the findings do not depend on the order the
moves were asked in*. `path_dependence` compares `frozenset` of
`(move, verdict)` across runs — order-invariant by construction, which
is correct for the comparison. What it never checks is whether **the
runs it was handed actually used different orders**.

Measured: two byte-identical copies of the delivered ledger return
`ORDERLESS -- claim holds`. So does the ledger against itself reversed,
since the set is the same either way.

The precondition is not merely unchecked, it is **not recorded**.
`emit()` returns an `order` key; the `ledger_schema` it ships in the same
dict has five fields and none of them is the order the run was made
under. A filled ledger carries its entries in list order — the delivered
one is `M1, M2, M3, M5, M4, M6`, which is shuffled — but nothing binds
that list to the seed that produced it, and `path_dependence` frozensets
it away before comparing.

So a caller who runs the same order twice gets a pass, and the harness
cannot tell. That is `MF_017`'s shape — a stated rule with no schema
field — arriving in the one function that exists to falsify the module's
central claim.

The repair is one field: carry the emitted `seed` or `order` into the
ledger, and refuse a `--paths` comparison whose runs do not differ on it.

**Falsifier:** a `--paths` run that reports which orders it compared.

**Status: SUPPORTED — and it is the finding that outlives the count fix.**

---

### MV_005 — the one always-run move has a null outcome that costs a point

`M6_absence` triggers on *"always -- runs on every artifact"* and admits
`NO_FINDING`. `NO_FINDING` is in `NULL`, and `score_entry` returns
`(0.0, "null")`.

Under a rule whose entire purpose is that a refusal scores as high as an
answer, *"I looked and nothing is hidden here"* is the single outcome
that loses a point — on the move that runs every time.

Two readings and the module does not say which: a null finding is
genuinely worth less than a located absence, or the scoring simply has
no cell for it and it fell into the default. The second is likelier,
because `NULL` is a set of one and nothing else in the module refers to
it.

The consequence is a gradient toward reporting *something*. A scan that
correctly finds nothing scores 5 of 6; the same scan reporting a
low-confidence absence scores 6.

**Falsifier:** a stated reason, anywhere in the module, for why a null
scores below a refusal.

**Status: SUPPORTED.**

---

### MV_006 — two malformed invocations are indistinguishable from asking for help

    --score <ledger>        rc=0   the report
    --score nosuch.json     rc=1   FileNotFoundError
    --emit                  rc=0   the help text
    --paths                 rc=0   the help text
    (no argument)           rc=0   the help text

`--emit` with no artifact and `--paths` with no runs both fall through
the `len(argv) > 2` guards into the else branch and print the move set,
exiting 0. A caller who forgot the argument gets the same output and the
same exit code as a caller who asked what the moves are. A missing file,
meanwhile, raises.

Third instance of this class in three folders — `CC_004`,
`CA_005`, `FM_042` — and the first where the failure is silent rather
than a traceback, which is the worse direction in a tool whose subject
is unearned passes.

**Falsifier:** a non-zero exit or a stated error on either.

**Status: SUPPORTED.**

---

### MV_007 — the delivered ledger contradicts itself on venue tier, and nothing in the harness could see it

Both strings are in the file, and the audit asserts their presence so an
edit turns the reading red rather than leaving it pointing at moved text.

**M3_relation_held**, verdict RESOLVED:

> Same-author control is available and unusually clean: Mech authored
> both the superseded carrier (1970) and the correction (1999). Author
> prestige, field, and **venue-tier** confounds drop out of the ratio.

**M5_self_report**, verdict INSTRUMENT_BLIND:

> **A book still in print is undercounted by Scholar/Scopus relative to
> a journal article**, and an uncited background assertion in coursework
> or trade writing emits no citation event at all.

Same pair, opposite claims. M3's own locator names them — a **1970
book** and a **1999 article** — so same-author holds prestige and field
fixed and does **not** hold venue fixed. Here venue is maximally
different, and M5 says that difference is the blocker. The control M3
calls unusually clean is clean on two of the three confounds it lists.

M5 is right and M3's third clause is the error; the fix is to drop the
clause, which leaves M3's finding intact and makes M5's blocker its
consequence rather than its contradiction.

**Nothing in the harness compares entries to each other.** `score`
iterates entries independently and `path_dependence` compares runs.
An orderless move set has no place to put a finding that exists only
*between* two moves — which is a real cost of orderlessness and not a
bug, since a cross-entry check would reintroduce the dependency the
design removes. The honest form is a seventh move whose trigger is *the
ledger*, not the artifact.

**Falsifier:** a reading under which same authorship does hold venue
tier fixed across a book and a journal article.

**Status: SUPPORTED, both strings pinned.**

---

### MV_008 — the ledger's subject is `observer-exclusion/`'s trigger case

`observer-exclusion/` is a runnable spec for **LEAD-TIME**,
`L = year_literature_adopts - year_excluded_reading_dateable`, and its
trigger case is **wolf social structure: the captive dominance model
against the 1999 field correction**. This ledger is that case, run
through a different instrument.

Three of its entries land directly on findings that folder already
carries. `M1`'s unreachable per-year citing counts are `OE_017`'s egress
status. `M4`'s `SHARE_IS_NONE` — *the set of documents that COULD have
cited the correction is not enumerable; citation databases index the
numerator only* — is `OE_003`'s differential-archiving result reached
from the denominator side. `M5`'s INSTRUMENT_BLIND on channels that emit
no citation event is `OE_013`'s point that the correction machinery is a
property of the **source**, not of the method.

`M5`'s unblocker is the more useful contribution: *count assertions
WITHOUT citation, over a denominator of documents that discuss pack
social structure at all.* That is a bounded corpus, which is what
`OE_003` and `MV_007`'s M4 both say is missing, and it needs no
citation database.

**Falsifier:** a bibliometric study of this correction existing, which
would move `M6` off NOT_ADDRESSABLE.

**Status: SUPPORTED — the two folders are on one case from two sides.**

---

### MV_009 — every subject-matter fact in the ledger is carried and unchecked

Mech 1999 *Can. J. Zool.* 77:1196-1203 DOI 10.1139/z99-099; Mech 1970
*The Wolf*; Schenkel 1947 on captive Basel Zoo packs; that Semantic
Scholar returned empty and Google Scholar blocks automated fetch; that
no bibliometric study of the correction exists.

None is verified here. This environment's egress is an allowlist and
every one of those sources is outside it — the `MS_004` / `OE_017`
status, and the fourth folder in this repository to carry a literature
claim it cannot check.

Nothing in `MV_001..MV_008` rests on any of them. They are properties of
the harness, the scorer, the falsifier, the CLI, and the internal
consistency of two prose strings in a file that is checked in.

**Falsifier:** the DOI resolving to something other than what the ledger
states.

**Status: UNVERIFIED, and load-bearing on nothing here.**

---

### MV_010 — the compatibility path repairs one readout and reaches two

The revision anticipated that a pre-split total and a post-split total
are not comparable, and emits a row saying so:

    LEDGER SPANS THE M6 SPLIT. Totals from pre-split and post-split
    runs are NOT comparable -- possible went from 6 to 11.

That is right, and it addresses the **total**. The same bundling also
reaches the **completeness** readout, and nothing says anything about
that one. `score()` does `seen.update(LEGACY[mv])`, so one bundled
entry marks all six sub-moves as run:

    delivered ledger under the revision
      total                     6.0 of 11.0
      moves_not_run             []
      sub-moves reported missing   0 of 6
      unreachable points        5.0

So the run reports *nothing missing* while five points of its own
denominator cannot be earned by it. A reader taking `moves_not_run`
at face value reads a complete run; a reader taking `total/possible`
reads 55%. Both are emitted, and only one carries the caveat.

Fourteenth instance in this repository of the absent-vs-known-negative
shape, at a new site: the missing third state here is *counted as run
because a predecessor covered it*, which is neither *run* nor *not
run*.

**Falsifier:** the six sub-moves appearing in `moves_not_run` on a
legacy ledger, or the SPLIT row naming the completeness readout as
well as the total.

**Status: SUPPORTED.**

---

### MV_011 — the split's stated reason names four and the split makes six

The comment introducing the family:

    M6 FAMILY -- absence. Was one move. It produced four findings in a
    single pass, which is the tell that it was not atomic

Sub-moves created: **six**. The reasoning is sound either way — a move
returning several separable findings is a bundle — and the number in
the sentence is not the number of pieces the bundle was cut into. The
two are different quantities (findings a particular run produced,
versus detection modes the move mixes), and the sentence reads as
though the first sets the second.

Not consequential and recorded because the split is the revision's
central move, and its stated warrant is one arithmetic step from its
result.

**Falsifier:** the sentence naming six, or the family having four
sub-moves.

**Status: SUPPORTED.**

---

### MV_012 — `LEGACY_ADMITS` is correct today and unmaintained by construction

The bundle's admissible-verdict list is a hand-written literal of
seven strings. Checked against what its six successors actually admit:

    union of the six sub-moves' admits   == LEGACY_ADMITS
    admitted by the bundle, by no successor: none

So it is exactly right, which is the honest way to write it — a
bundle admits what any of its successors admit. What it is not is
**derived**. The union is one comprehension over `LEGACY` and `MOVES`,
and a change to any sub-move's `admits` list moves the union and
leaves the literal where it is.

The margin is thin enough to matter: four of the seven verdicts are
admitted by one or two of the six successors.

    RESOLVED           6 of 6
    NOT_ADDRESSABLE    4 of 6
    NOT_DERIVABLE      3 of 6
    NO_FINDING         2 of 6
    INSTRUMENT_BLIND   1 of 6
    NOT_SEPARABLE      1 of 6
    SHARE_IS_NONE      1 of 6

Removing `SHARE_IS_NONE` from `M6f_no_denominator` — the only
sub-move that admits it — would leave the literal admitting a verdict
no successor does, silently.

Same arrangement as `reasoning-gate`'s `guards.json → GUARDS.md`,
where the doc is generated from the source of truth and a test asserts
they match. Here the derivation is available and unused.

**Falsifier:** `LEGACY_ADMITS` computed from `LEGACY` and `MOVES`, or
a test asserting the two agree.

**Status: SUPPORTED.**

---

### MV_013 — the revision raised the ceiling on an ungrounded ledger and did not touch the gate

`MV_002` is unchanged by the revision and is now worth more. The
garbage ledger — right shape, `"x"` in every blocker and unblocker —
scores:

    before the split   6.0 of 6.0
    after the split   11.0 of 11.0

`score_entry` is byte-identical across the revision. So the split
raised what a fully ungrounded ledger is worth by 83% while leaving
the one guard the module's own docstring calls *"the only thing
keeping symmetric scoring from being gameable"* exactly as it was:
two non-empty strings.

This is not an argument against the split, which is a real
improvement to the move set. It is that a change to the move
inventory moves the score ceiling, and the score ceiling is the
quantity the anti-gaming guard is defending. `adaptive-claim-loop`
`ACL_012` names the change that closes it — ask for a number, not a
sentence — and `ACL_017` bounds what that buys.

Prior art per sub-move is the revision's answer to a different
question, and a strong one: eight of eleven moves now name an established
investigative instrument, so a picker-up does not have to defend a new
one. The three without (`M2_substitution`, `M4_perturb`,
`M5_self_report`) are the three the comment does not discuss, and
whether they have no prior art or were not looked up is not stated.

**Falsifier:** the gate reading a computed quantity, or the ceiling
staying fixed as moves are added.

**Status: SUPPORTED.**
