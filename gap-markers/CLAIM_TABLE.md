# gap-markers — CLAIM_TABLE

`GM_001..GM_015`. Claims about the delivered `GAP_MARKERS.md` and its
corpus, all landed verbatim and modified by nothing here.

**Second drop, 2026-08-26.** All five `gaps/*.md` files landed, plus a
sixth (`ADDENDUM.md`) the INDEX does not name. 29 entries. `GM_009`
closes, `GM_001` and `GM_003` become testable and both move,
`GM_010`'s question is answered, and `GM_011..GM_015` are what the
corpus shows.

They arrived. Nothing was reconstructed while they were absent, and
the refusal branch in `load_gaps()` is kept and still reachable on a
constructed absence, because the next INDEX entry named before it is
written will hit it.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered file. Where a check and a claim disagree,
the disagreement goes in the checker's output.

| id | claim | status |
|---|---|---|
| `GM_001` | *"Most entries here are boundary-artifact"* is not an observation about a corpus. It is forced by the state vocabulary and derivable before any entry is written. | SUPPORTED on the distribution (**29 of 29**), **falsifier FIRED** on one entry, and the falsifier was written too loosely to settle it — see below |
| `GM_002` | The register has no negative state, so it can only ever record gaps and cannot report coverage. | SUPPORTED |
| `GM_003` | `ENTRY_POINT` is conditional and has no third state, on the field that makes a gap actionable. | SUPPORTED, **and sharpened**: 23 of 29 absent, and the distribution is by FILE — three files are 0 of 18 |
| `GM_004` | The READING RULE is the strongest thing in the drop and is deliberately not automated, on its own say-so. | SUPPORTED |
| `GM_005` | The map to `investigation-sim` is not onto in either direction, and `unasked` named a state that module could not express. | SUPPORTED — **and the finding landed the same day**: that module added a sixth bin and a fifth signal (its `IS_014`) |
| `GM_006` | The fourth standing caution states `generation-capacity`'s mechanism 10, arrived at independently, and the *no residue* clause is what makes it that rather than mechanism 6. | SUPPORTED |
| `GM_007` | The KIND distinction is the thing `uninstrumented`'s eight-mechanism register does not have. | SUPPORTED |
| `GM_008` | My first parse returned six of seven fields and every non-emptiness check passed on it. | SUPPORTED |
| `GM_009` | Five named index files, none present. | **CLOSED 2026-08-26** — all five landed |
| `GM_010` | No gap entry has been read, and the load-bearing empirical question — whether the states are codable against a real gap — is untouched. | **ANSWERED in part**: 29 read; 1 carries two states, 1 carries two kinds |
| `GM_011` | Six field names are in use and none is in the schema. `WHY UNRUN` is the load-bearing one. | SUPPORTED |
| `GM_012` | A sixth file arrived that the INDEX does not name, addressed to a reader the other five are not. | SUPPORTED |
| `GM_013` | `unasked` is the largest state at 14 of 29 — the state `investigation-sim` had no bin for until `IS_014` yesterday. | SUPPORTED |
| `GM_014` | The addendum's inheritance claim is testable against this session, and one instance supports it. Interest declared, because it runs both ways. | SUPPORTED at n=1 |
| `GM_015` | Every literature and agency fact in all 29 entries is carried and unchecked. | UNVERIFIED |

---

## GM_001 — the distribution is forced, and the falsifier fired anyway

**The prediction held on the distribution.** Written before any entry
existed: four of five state definitions assert the knowledge is
present, so `KIND` is determined on those four and free only on
`uncounted`. Against 29 delivered entries:

    boundary-artifact   29 of 29
    knowledge            1 of 29 (alongside boundary-artifact, not alone)

So *"Most entries here are boundary-artifact"* is true, and it is true
for the reason `GM_001` gave rather than as an observation about what
the author found.

**And the stated falsifier fired.** It was: *an entry in `unasked`,
`unowned`, `assembly` or `undated` correctly marked `knowledge`.*
`STR-05-RETROFIT-BASELINE` is `undated` and its `KIND` reads
*`knowledge (for the compliance figure) / boundary-artifact (for the
scope)`.*

**The firing is not decidable by the check, and that is the finding
about the falsifier.** STR-05's own `WHAT_IS_MISSING` says: *"One
source cites a city retrofit program at ~5% compliance; this figure
needs a primary source before use."* That is a number that exists and
whose citation the author does not have. The `KIND` definition reads
*the physics or the measurement is genuinely not known* — which a
figure lacking a citation is not.

So there are two readings and the check cannot pick:

- the entry uses `knowledge` in a **second sense** — provenance
  unknown to me, rather than not known to anyone — in which case
  `GM_001` stands and the corpus contains a sense split in `KIND`;
- or `knowledge` legitimately covers provenance gaps, in which case
  `GM_001` falls.

The definition supports the first. The check does not, because the
falsifier turns on the word **correctly**, and nothing measures that.
Same shape as `SHB_020` / `SHB_040`: a falsifier written so its firing
does not settle anything. `gm001_test()` reports `falsifier_fired` and
emits **no verdict**, and the selftest asserts it emits none.

The cheap repair is on the delivered side and is one line: `KIND`
gains a third value, or `knowledge` is defined to exclude *the author
lacks a citation*, which is a provenance state rather than a knowledge
state. The corpus already distinguishes them everywhere else — this is
the only entry where a source-quality caveat reached the `KIND` field.

**Falsifier, restated so it can settle something:** an entry in one of
the four forced states marked `knowledge` **alone**, whose
`WHAT_IS_MISSING` names a quantity no party has measured. That is
checkable without the word *correctly*.

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

## GM_003 — `ENTRY_POINT` has no third state, and now a magnitude

Present on **6 of 29**. And the distribution is not per-gap:

    gaps/substrate.md      3 of 6
    gaps/structures.md     0 of 5
    gaps/transport.md      0 of 5
    gaps/capability.md     0 of 8
    gaps/screens.md        3 of 5

Three files are **0 of 18**. Two carry all six. The file whose own
opening says its entries *"are the cheapest gaps to close"* is the
highest.

That is internally consistent and it needs a **third** reading beyond
the two `GM_003` named. The two were *searched, no query available*
and *nobody named one*. The data says the field is **in use in two
files and not in three**, so an absence in `structures`, `transport`
or `capability` is a property of the file rather than a judgement
about the gap.

The cost is concrete: a reader picking the cheapest gap to attack
reads all eighteen as equally hard, and none of the eighteen was
assessed for tractability at all. `CAP-02` even carries the substance
of an entry point in a `NOTE` — *the equipment exists, owned by
aggregate producers and marine contractors* — without it reaching the
field.

**Falsifier:** an entry-point value on one of the eighteen, or a
per-file statement that the field was considered and declined.

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

---

## GM_011 — six field names in use, none in the schema

    MECHANISM   NOTE   SCOPE   US ANALOGUES   WHY UNRUN   WORKED CASE

Carried by **17 of 29** entries. The schema says *"Each gap entry
carries these fields"* and lists seven.

This is the `MF_017` shape **inverted**: not a stated rule with no
schema field, but fields in use with no schema slot. Softer, because
nothing breaks — but it means a reader parsing to the schema drops
17 entries' worth of content, and a checker validating against the
schema would call every one of them well-formed while never seeing it.

**`WHY UNRUN` is the one that matters.** On `SCR-01` it gives the
reason the computation has not been performed: the screen produces a
large flagged set and every flagged site becomes a liability and
disclosure question for whoever publishes the list, and no agency owns
*"slope above a thing that matters"*.

That is the **boundary-artifact content itself**, stated as a field —
and it is the only place in 29 entries where the reason for the
boundary is a field rather than something a reader infers from `KIND`.
`KIND: boundary-artifact` says *this is a division of budget or
liability*; `WHY UNRUN` says *which one, and whose*. The second is
what the READING RULE needs in order to sort, and it exists once.

**Falsifier:** `WHY UNRUN` promoted to the schema, or a second entry
carrying it.

## GM_012 — a sixth file the INDEX does not name

`ADDENDUM.md` arrived with the five. The INDEX lists five.

Not an oversight, on the evidence: it opens *"Directed at any system
participating in infrastructure, disaster management, or emergency
planning decisions"*, which is a reader the other five are not
addressed to. An index of gap files is the wrong container for a
document about how a reader should hold them.

The consequence is mechanical rather than editorial: anything that
walks the INDEX does not reach it. `load_gaps()` does not, and the
selftest asserts the addendum is present and unindexed rather than
quietly folding it in.

**Falsifier:** the INDEX naming it, or a second unindexed file
arriving that is a gap file.

## GM_013 — `unasked` is the largest state, and it had no bin

    unasked     14
    unowned      5
    uncounted    4
    assembly     4
    undated      3

Nearly half the corpus. And `unasked` is the state `GM_005` mapped
against `investigation-sim`'s bins and found **no bin for** — a case
coded honestly against that module's four original signals read
`ABSENT` on all four and landed on `NOT_FORESEEN`.

So the bin that was missing was the one covering the plurality of this
corpus, and the corpus arrived one day after the bin did. Had the
order been reversed, running that classifier over these 29 entries
would have filed fourteen of them as *genuinely novel*.

That is a stronger result for `IS_014` than `IS_014` claimed. It was
recorded as a false negative demonstrated on one constructed case;
this is its rate against the first real corpus the vocabulary met.

**Falsifier:** a re-reading of the fourteen that puts them in existing
bins, which would mean `unasked` is not a distinct state.

## GM_014 — the addendum's inheritance claim, and where I sit in it

The claim: *"the absence cannot be detected by introspection over the
model's own outputs. Nothing in the represented space indicates that a
region is unrepresented. It has to be named from outside."*

**This session supplies one instance supporting it, and it is not an
instance I produced by introspecting.** `investigation-sim` was built
here with five bins, a spec, 102 checks, and an explicit selftest arm
asserting the negative bin was reachable. None of that found the
missing sixth bin. It was found by mapping an *external vocabulary* —
this register's five states — against it, and the gap appeared as a
state with no bin.

I want to be precise about what that shows and does not. It shows one
case where a checked, self-audited classifier had a hole its own
checks could not surface and an outside vocabulary did. It does not
show that introspection *never* works; `IS_004` and `IS_007` in that
same folder were found by running the module's own report.

**Interest declared, because it runs both ways.** The claim says my
class is structurally blind in a specific way, which is unflattering
and which I have no incentive to endorse. It also says the remedy is
to keep feeding external registers to systems like me, which is
flattering to my continued involvement. Those point opposite
directions, so I am not declining the claim the way `UNI_101` /
`SHB_012` decline — I am reporting the one instance and its n.

The addendum's `HOMOGENIZATION` point is the part I would flag as
least tested here and most consequential: *diversity of error is a
safety property and it is the first thing a shared advisory layer
removes.* `triad-playground` `TP_008` measured exactly that on shadow
panels — four model families reach `N_eff` 2.18 and false-pass 12.4%,
while two settings of one model collapse to `N_eff` 1.14 and **84%**.
Same claim, measured, on a different substrate, arrived at
independently.

**Falsifier:** a gap in a module here found by that module's own
introspection where an external vocabulary had already been applied
and missed it.

## GM_015 — every fact in the corpus is carried and unchecked

29 entries name USGS, USACE ER 1110-2-1806, FEMA P-93, FEMA 460,
Hazus, the National Bridge Inventory, the National Inventory of Dams,
ASCE 7, TCEQ, MSHA, NSS, MITRE, GAO, Wright et al. 2011, Barry Arm,
Taan Fiord, Surprise Inlet, the Sawyer Decision, Kobe 1995, Johnstown
1889, and an August 2026 event on the Nepal/China border.

**None is verified here.** This environment's egress is an allowlist
and every one of those sources is outside it — the `MS_004` /
`OE_017` / `ANC_010` status, and the seventh folder in this repository
carrying literature it cannot check.

Nothing in `GM_001..GM_014` rests on any of them. Those are properties
of the schema, of the corpus as text, and of the map to a sibling
folder — all of which are here.

Two the drop flags itself, which is the right handling and worth
recording: `STR-05` marks its ~5% compliance figure as needing a
primary source before use, and `SCR-05`'s classification argument
states that initial reporting on the Nepal event swung between three
labels.

**Falsifier:** run the checks. `SCR-02`'s entry point — *date of last
hazard-class review, per structure* — needs no fieldwork and no
literature, only the register, and a null or a decades-old date is by
its own statement the finding.
