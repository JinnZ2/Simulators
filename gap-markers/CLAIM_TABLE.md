# gap-markers — CLAIM_TABLE

`GM_001..GM_010`. Claims about the delivered `GAP_MARKERS.md`, which is
landed verbatim and modified by nothing here.

The five `gaps/*.md` files its INDEX names **did not arrive**. Nothing
here reconstructs them — they are data, and inventing an entry puts a
gap in the author's mouth (`PB_001` / `CW_004`). Every claim below is a
property of the **schema**, which is what did arrive.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered file. Where a check and a claim disagree,
the disagreement goes in the checker's output.

| id | claim | status |
|---|---|---|
| `GM_001` | *"Most entries here are boundary-artifact"* is not an observation about a corpus. It is forced by the state vocabulary and derivable before any entry is written. | SUPPORTED |
| `GM_002` | The register has no negative state, so it can only ever record gaps and cannot report coverage. | SUPPORTED |
| `GM_003` | `ENTRY_POINT` is conditional and has no third state, on the field that makes a gap actionable. | SUPPORTED |
| `GM_004` | The READING RULE is the strongest thing in the drop and is deliberately not automated, on its own say-so. | SUPPORTED |
| `GM_005` | The map to `investigation-sim` is not onto in either direction, and `unasked` named a state that module could not express. | SUPPORTED — **and the finding landed the same day**: that module added a sixth bin and a fifth signal (its `IS_014`) |
| `GM_006` | The fourth standing caution states `generation-capacity`'s mechanism 10, arrived at independently, and the *no residue* clause is what makes it that rather than mechanism 6. | SUPPORTED |
| `GM_007` | The KIND distinction is the thing `uninstrumented`'s eight-mechanism register does not have. | SUPPORTED |
| `GM_008` | My first parse returned six of seven fields and every non-emptiness check passed on it. | SUPPORTED |
| `GM_009` | Five named index files, none present. | SUPPORTED |
| `GM_010` | No gap entry has been read, and the load-bearing empirical question — whether the states are codable against a real gap — is untouched. | UNVERIFIED |

---

## GM_001 — the distribution is forced, not observed

The delivered file states *"Most entries here are boundary-artifact."*
That reads as a fact about the corpus. It is derivable from the state
definitions with no corpus at all.

Four of the five definitions assert that the knowledge is present:

    unasked    "data exists, collected for another purpose"
    unowned    "every party competent"
    assembly   "all components present in separate literatures"
    undated    "record exists but currency unknown"

A state whose own definition says the data, the record, or the
competence exists cannot also be a state where the physics or the
measurement is genuinely not known. So `KIND` is determined on those
four and carries information on exactly one — `uncounted`, whose
definition makes no existence claim and where a deep-void census could
be genuinely unknown *or* simply unfunded.

**This is a schema economy, not a fault.** `KIND` stays load-bearing
for the READING RULE, which operates on *boundaries* rather than on
entries, and the READING RULE is where the distinction does its work.
What changes is how the sentence should be read: not *most of what I
found was institutional*, but *four of my five categories can only be
institutional*.

The forcing is **read from the delivered definitions**, not from a
hand-made list: replace a definition with one making no existence
claim and the checker frees the KIND again, which is asserted.

**Falsifier:** an entry in `unasked`, `unowned`, `assembly` or
`undated` correctly marked `knowledge` — which would mean the state
definition and the entry disagree about whether the data exists.

## GM_002 — no negative state

All five `STATE` values are gaps. There is no value meaning *looked,
and nothing is missing here*.

So the register can only ever record gaps, and a null test over it has
no arm that returns nothing — the `null-harness` `CONSTANT_FIRES`
shape at the schema level. `uninstrumented` `UNI_004` found the same
thing about its own confidence field, and `UNI_006` is still its
standing counterweight.

The delivered framing answers part of it, and the answer is good: *"A
marked gap is not a finding. It is a location."* A register of
locations does not need a negative the way a classifier does.

What it cannot then do is **report coverage**. There is no denominator
of places looked at, so the register can say *here are twenty gaps*
and can never say *of the places examined, twenty had gaps*. That
matters for the same reason `IS_001` matters one folder over: a count
with no denominator is not a rate, and the standing caution's own
first item — *an uncounted population is unbounded in both directions*
— applies to the register itself.

**Falsifier:** a sixth state, or a separate record of places examined.

## GM_003 — `ENTRY_POINT` has no third state

The field reads *"cheapest available first query, where one exists."*

So an entry with no `ENTRY_POINT` carries two readings: **searched,
and no query is available** (a measurement about the gap's
tractability), or **nobody named one** (a measurement about the
entry's completeness). They are the two states this repository has now
separated a dozen times, and `ENTRY_POINT` is the field that makes a
gap actionable — so it is the one where the collapse costs most. A
reader picking the cheapest gap to attack reads *no entry point* as
*hard*, and it may only mean *unfinished*.

Cheap: a sentinel — `NONE_LOCATED` with a reason, distinct from an
omitted field.

**Falsifier:** a third value, or a per-entry statement of which
absence it is.

## GM_004 — the reading rule, and why it is not automated

    1. Does the boundary encode failure knowledge — a method that was
       found not to transfer, a correlation that breaks off its
       calibration range, a sampling assumption that does not hold?
       KEEP IT.
    2. Does the boundary encode who pays, who is liable, or who holds
       jurisdiction? DO NOT INHERIT IT.

    Both look identical from outside. The content differs.

This is the strongest thing in the drop. It is an operational
instruction, it names both branches with examples, and its last two
sentences state its own difficulty rather than hiding it.

That last part is why nothing here automates it. A keyword sort over
`liable` / `jurisdiction` / `budget` would be a word list deciding a
question the author says cannot be decided from the surface —
`nonidentity-census` `T1-1` exactly, and the author has pre-empted it.

What is built is a **record**: `sort_record()` takes a declared branch
with a reason, refuses a branch outside the two, refuses a branch with
no reason, and returns `UNSORTED` rather than guessing — with
`UNSORTED` explicitly not meaning *sorted and found to be neither*.
The selftest asserts nothing in the function scans for who-pays
language.

Third folder in this family with that shape after `DL_015`, `GC_003`
and `ACL_011`: a declaration, not a check, and correctly so.

**Falsifier:** a boundary whose branch is decidable from its surface
text, which would mean the rule's last two sentences overstate.

## GM_005 — the map to `investigation-sim`, both directions

    uncounted  -> (no bin)
    unasked    -> (no bin)
    unowned    -> GAP_UNINSTRUMENTED
    assembly   -> (no bin)
    undated    -> CALCULATED_UNCLOCKED

    bins with no state here:
      KNOWN_ROUTED_AWAY, CONCEIVED_NOT_BUILT, NOT_FORESEEN

Two of five map. The bin vocabulary is **imported** from
`investigation-sim.bins.BINS`, so a rename over there turns this red
rather than silently mismatching, and a mapping naming a bin that
module does not have is refused.

`undated` and `CALCULATED_UNCLOCKED` are the same object — *record
exists but currency unknown, a date field answers it* against *the
figure survived and the conditions under which it held did not*. Two
authors, two vocabularies, one state.

**The sharpest unmapped member is `unasked`.** The instrument exists
and reported, and nobody posed the question. That is neither
`KNOWN_ROUTED_AWAY` — no report was made, so nothing was routed
anywhere — nor `GAP_UNINSTRUMENTED`, where the instrument is blind by
its own constitution. `investigation-sim` has no bin for it and its
four signals cannot code it: `prior_report` is `ABSENT` truthfully,
`no_instrument` is `ABSENT` truthfully, and the case lands on
`NOT_FORESEEN` — *genuinely novel* — when the data was sitting in a
file the whole time.

**That was a specific false negative in the module one folder over,
and this drop found it.** It has been repaired: `investigation-sim`
added a fifth signal, `held_data_unasked`, and a sixth bin,
`HELD_BUT_UNASKED` — a bin rather than a modifier, because it is a
foreknowledge state parallel to the other four. Its
`cases/held-but-unasked.json` is the case that found it, and its
authoring note records that the four original signals all read
`ABSENT` truthfully. `IS_002` over there was narrowed rather than left
standing: it made the *reachability* of `NOT_FORESEEN` load-bearing
and never asserted its *correctness*, and a negative returned wrongly
tells the operator to stop looking.

The bin vocabulary here is imported, so this row now maps and the
selftest asserts both that it maps and that the row still records it
had no bin when the finding was made.

**What it says about the method**: the gap was not found by any check
inside either module. It was found by mapping two vocabularies built
for different purposes against each other — `triad-playground`
`TP_008`'s decorrelated-shadow result arriving as a fact about two
registers rather than two readers. A single vocabulary cannot
enumerate what it has no word for.

Running the other way, this register has no state for `NOT_FORESEEN`,
which follows from `GM_002`.

`uncounted` maps to nothing because it sits one level up: it is the
**denominator** `IS_001` says is uncounted, not a bin among the bins.

**Falsifier:** a coding of a real gap that fits a bin this map says it
does not, or `investigation-sim` gaining the fifth signal.

## GM_006 — the fourth caution is mechanism 10, arrived at independently

> A correct output that contradicts an incentive is indistinguishable
> from an error to whoever checks it against the accepted result. The
> correction pressure runs one direction. Over enough cycles the
> pattern is not suppressed — it is not generated. There is no residue.

`generation-capacity/MECHANISM_10.md` names GENERATION CAPACITY
REMOVED, whose distinguishing sentence is *"nothing is suppressed at
decision time because nothing is there to suppress."*

Same statement. And the **no residue** clause is precisely what makes
it mechanism 10 rather than mechanism 6 (`AUDIT_ASYMMETRY`, a guard
firing on one side): an asymmetric guard leaves a record of what it
rejected, and this leaves none, because the pattern stops being
produced. `GC_006` reads the same shape as a rate comparison —
suppression needs continuous expenditure, a removed generator needs
none.

The drop reaches it from correction pressure on outputs; mechanism 10
reaches it from option spaces. Neither cites the other.

**Falsifier:** a residue — a record of outputs that contradicted an
incentive and were corrected, in a system old enough for the pattern
to have stopped being generated.

## GM_007 — KIND is what the register does not have

`uninstrumented`'s eight mechanisms — `MODALITY`, `STORAGE`,
`SCALAR_DEMAND`, `BUDGET_BOUNDARY`, `AUTHORED_REFERENCE`,
`PROXY_SUBSTITUTION`, `AUDIT_ASYMMETRY`, `SCORED_AS_WASTE` — describe
*how* an exclusion operates. None of them separates *the physics is
not known* from *the institutions divided the budget*.

`BUDGET_BOUNDARY` is the nearest and is narrower: it is a closed
accounting compared to an open one, a specific mechanism, where
`boundary-artifact` is a **property of the whole gap** that cuts
across mechanisms. A `STORAGE` exclusion can be either kind — a medium
that genuinely cannot hold the shape, or a schema someone chose.

So `KIND` is orthogonal to the eight and is a real addition. What
`GM_001` shows is that it is orthogonal to the mechanisms and *not*
to this drop's own five states.

**Falsifier:** a mechanism in the register that already carries the
distinction.

## GM_008 — my parse returned six of seven and passed

`fields()` required two spaces after the field name.
`WHAT_IS_MISSING` is fifteen characters into a sixteen-wide column, so
it has one, and the parse returned **six**.

A check asserting the parse is non-empty passes on that. A check
asserting five states and two kinds passes on that. The field that
went missing is the one naming *the specific absence* — the register's
own subject.

Repaired, and the arms that would have caught it are now the parse
arms: the count is asserted, every parsed name is asserted to appear
in the delivered file, and the one-space column is asserted to parse.

Same class as `bins.py`'s own rule that a parse returning nothing must
not pass — and worse, because a partial parse returns *something*.

**Falsifier:** a field in the delivered file that the parse does not
return.

## GM_009 — five named, none present

    gaps/substrate.md    NO    ground, fill, water, deposition, voids
    gaps/structures.md   NO    dams, bridges, dual-function, underground
    gaps/transport.md    NO    rail, barge, air, road, staging
    gaps/capability.md   NO    fabrication, response cadre, matching
    gaps/screens.md      NO    computable screens not run; date fields

`load_gaps()` **raises** rather than returning an empty list, and the
exception names the files and says they are not reconstructed. A
well-formed report with zero rows over a corpus that is not here is
the `DL_005` / `CC_006` shape — a denominator of zero, rendered as
though it had one.

No `gaps/` directory was created, and the selftest asserts that too.

`gaps/screens.md` is the one to want first: *computable screens not
run; date fields not queried* is by its own description the cheapest
set, and `undated` is the state with a live route to
`claim-record.derive_clock` through `investigation-sim`.

**Falsifier:** the files landing.

## GM_010 — nothing has been coded

No gap entry exists here. Every readout is a property of the schema,
and the load-bearing empirical questions are untouched:

- Are the five states codable against a real gap, or does a real gap
  carry two of them?
- Is `KIND` decidable in the field, given that `GM_001` says four of
  five states decide it in advance?
- Does the READING RULE separate anything when a real boundary is put
  to it?

The third is the one to run first and it needs no corpus of gaps at
all — only a handful of real boundaries and two readers, which is the
`triad-playground` shadow-panel design with the null attached.

**Falsifier:** run it.
