# gap-markers

A register of **locations**, not findings. Marked gaps in hazard
assessment, infrastructure evaluation, and disaster response
capability — places where a quantity is not measured, a question is
not asked, or an interface is owned by nobody.

`GAP_MARKERS.md` is **delivered verbatim** and modified by nothing
here. Its schema is *parsed* by `markers.py` — field names, `STATE`
values, `KIND` values and the INDEX all come out of the file — so an
edit there and not here turns the selftest red.

    python3 gap-markers/markers.py             # the report
    python3 gap-markers/markers.py --cross     # the KIND x STATE table
    python3 gap-markers/markers.py --selftest  # 66 checks

**The five `gaps/*.md` files the INDEX names did not arrive**, and
nothing here reconstructs them. They are data; inventing an entry puts
a gap in the author's mouth. `load_gaps()` raises rather than
returning an empty list, because a well-formed report with zero rows
over a corpus that is not here is a denominator of zero rendered as
though it had one.

## What the schema does well

**The READING RULE is the strongest thing in the drop.** Sort every
partition before treating it as a constraint: does it encode failure
knowledge — a method found not to transfer, a correlation that breaks
off its calibration range — or does it encode who pays, who is liable,
who holds jurisdiction? Keep the first. Do not inherit the second.

Then: *"Both look identical from outside. The content differs."*

That last line is why nothing here automates it. A keyword sort over
`liable` / `jurisdiction` / `budget` would be a word list deciding a
question the author has already said cannot be decided from the
surface. What is built is a **record** — `sort_record()` takes a
declared branch with a reason, refuses a branch outside the two,
refuses one with no reason, and returns `UNSORTED` rather than
guessing, with `UNSORTED` explicitly not meaning *sorted and found to
be neither*.

**`KIND` is a real addition to `uninstrumented`.** Those eight
mechanisms describe *how* an exclusion operates and none separates
*the physics is not known* from *the institutions divided the budget*.
`BUDGET_BOUNDARY` is the nearest and is narrower — a specific
mechanism, where `boundary-artifact` is a property of the whole gap
that cuts across them. A `STORAGE` exclusion can be either kind.

## What the checks found

**`GM_001` — the distribution is forced, not observed.** The file
states *"Most entries here are boundary-artifact."* That is derivable
from the state definitions with no corpus at all: four of five assert
that the knowledge is present —

    unasked    "data exists, collected for another purpose"
    unowned    "every party competent"
    assembly   "all components present in separate literatures"
    undated    "record exists but currency unknown"

— and a state whose definition says the data exists cannot be a state
where the knowledge is absent. So `KIND` carries information on
exactly one state, `uncounted`, whose definition makes no existence
claim. A schema economy, not a fault: `KIND` stays load-bearing for
the READING RULE, which operates on boundaries rather than entries.
The reading changes from *most of what I found was institutional* to
*four of my five categories can only be institutional*.

The forcing is read from the delivered definitions, not a hand-made
list — swap in a definition with no existence claim and the checker
frees the `KIND` again.

**`GM_005` — the map to `investigation-sim` runs both ways, and it
found a false negative over there.**

    uncounted  -> (no bin)          the DENOMINATOR IS_001 calls uncounted
    unasked    -> (no bin)          see below
    unowned    -> GAP_UNINSTRUMENTED
    assembly   -> (no bin)          a property of a FIELD, not a record
    undated    -> CALCULATED_UNCLOCKED

    bins with no state here:
      KNOWN_ROUTED_AWAY, CONCEIVED_NOT_BUILT, NOT_FORESEEN

`undated` and `CALCULATED_UNCLOCKED` are the same object under two
vocabularies. But **`unasked` names something `investigation-sim`
cannot express**: the instrument exists and reported, and nobody posed
the question. Not `KNOWN_ROUTED_AWAY` — no report was made, so nothing
was routed. Not `GAP_UNINSTRUMENTED` — the instrument is not blind.
Coded honestly, all four of that module's signals read `ABSENT` and
the case lands on **`NOT_FORESEEN`**, *genuinely novel*, while the
data sat in a file the whole time. A specific false negative, found by
this drop — **and repaired the same day**: that module added a fifth
signal and a sixth bin, `HELD_BUT_UNASKED`, and narrowed its `IS_002`,
which had made the *reachability* of the negative load-bearing while
never asserting its *correctness*. A negative returned wrongly tells
the operator to stop looking.

The gap was found by neither module's own checks. It came from mapping
two vocabularies, built for different purposes, against each other — a
single vocabulary cannot enumerate what it has no word for.

The bin vocabulary is **imported**, so a rename over there turns this
red, and a mapping naming a bin that module does not have is refused.

**`GM_006` — the fourth standing caution is `generation-capacity`'s
mechanism 10, arrived at independently.** *"Over enough cycles the
pattern is not suppressed — it is not generated. There is no
residue"* against *"nothing is suppressed at decision time because
nothing is there to suppress."* And the **no residue** clause is what
makes it mechanism 10 rather than mechanism 6: an asymmetric guard
leaves a record of what it rejected; this leaves none.

**`GM_002` — no negative state.** All five values are gaps, so the
register can only ever record gaps and a null test over it has no arm
returning nothing. The delivered framing answers part of it — *"a
marked gap is not a finding, it is a location"* — and what remains is
that the register cannot report **coverage**: there is no denominator
of places looked at, which is the standing caution's own first item
applied to the register itself.

**`GM_003` — `ENTRY_POINT` has no third state.** *"Where one exists"*
means an absent entry point reads either as *searched, no query
available* or *nobody named one*. It is the field that makes a gap
actionable, so a reader picking the cheapest gap to attack reads *no
entry point* as *hard* when it may only mean *unfinished*.

**`GM_008` — my own parse returned six of seven fields and passed
every check.** `WHAT_IS_MISSING` is fifteen characters into a
sixteen-wide column, so it has one space where the regex wanted two.
The field that went missing is the one naming *the specific absence* —
the register's own subject. A non-emptiness check passes on a partial
parse, which is worse than one returning nothing, so the count is now
asserted and so is the one-space column.

## Files

| | |
|---|---|
| `GAP_MARKERS.md` | delivered verbatim |
| `markers.py` | parses the schema, the `KIND × STATE` cross, the reading-rule record, the `investigation-sim` map |
| `selftest_markers.py` | 66 checks |
| `CLAIM_TABLE.md` | `GM_001..GM_010` with a REFUTATION_PROTOCOL |
| `samples/` | pinned output |

`gaps/` is deliberately absent.

Stdlib only, parses under Python 3.9, phone-buildable, CC0.

Siblings: `investigation-sim/` (five bins, mapped both directions),
`uninstrumented/` (the eight-mechanism register `KIND` adds to),
`generation-capacity/` (mechanism 10, and R4's uncounted non-event),
`claim-record/` (what `undated` routes to through `investigation-sim`),
`null-harness/` (the `CONSTANT_FIRES` shape `GM_002` names).
