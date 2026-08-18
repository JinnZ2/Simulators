# AUDIT_NOTES — domain-ledger

Added, not delivered. [`ledger.py`](ledger.py) is the drop as received and
is not modified.

    python3 ledger.py --selftest
    python3 ledger_audit.py

## What the folder is

Two files. `ledger.py` records how much of a domain space a shape was read
across; `anchor.py` records what the shape grounds to and what band that
support already occupies. The companion's framing: coverage "resolves
position inside a band that something else already set."

`ledger.py` — A ledger that makes a confidence readout **derived instead of
asserted**, by recording the domain set a coverage number was taken over.

Four readouts, deliberately not combined: **coverage** (domains where the
shape held / domains read), **cycle depth** (holds that survived a return
/ holds), **adversarial** (domains where the shape was pushed against /
domains read), **truncated** (reads cut short at a discomfort threshold /
domains read). Plus a **reservation** — a standing fraction held as
unknown.

Selftest 13/13.

`anchor.py` — three bands set by the class of support (`none` 0.30,
`external` 0.80, `cycle_persistent` 0.99) and three routing states per
provenance link (`routed` / `unrouted` / `absent_established`). Emits no
composite confidence figure, by design and by assertion in its own
selftest. 14/14.

## File status

| file | status |
|------|--------|
| `ledger.py` | delivered, verbatim — **drop 4 docstring**; code byte-identical after stripping the module docstring |
| `anchor.py` | delivered drop 3, verbatim — companion; selftest 14/14 |
| `anchors/hierarchy-imposed-ordering.json` | delivered drop 4, verbatim — 3 anchors, 9 links, 0 quantified |
| `A2.md` | delivered drop 5, verbatim — a candidate for the anchor-distance term, explicitly not adopted |
| `shapes/hierarchy-cut-generation.json` | delivered drop 2, verbatim — 30 domains, 0 read, asserted coverage 0.61 |
| `README.md`, `CLAIM_TABLE.md` | not delivered — `A2.md` names the second one |
| `ledger_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Nothing here invents a shape. A shape is data — a claim someone holds and
the domains they read it against — and inventing one would put a position
in the author's mouth.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| DL_001 | The load-bearing idea — a coverage number is not portable without its denominator — is `CD_008`/`ANC_006` restated for a confidence readout, and the tool follows it: four readouts returned separately with their denominators named in the output | a reading on which the four are combinable | SUPPORTED (holds) |
| DL_002 | The reservation is defined as capping reported headroom and nothing applies it: `ceiling` is computed, returned, printed, and read by nothing; coverage may exceed it with no readout saying so | a headroom field, or a flag when coverage exceeds the ceiling | SUPPORTED — drop 4 gives the constant a source (0.2 = 1 − the external band ceiling) and does not apply it |
| DL_003 | `coverage` puts `mixed` in the denominator and not the numerator, so all-break and all-mixed both return 0.00 | a footer clause naming what the denominator includes, or a separate ratio | SUPPORTED |
| DL_004 | `detail()` reads `criterion_fixed_in_advance` and `open`; `SKELETON` carries neither, so `--new` never prompts for the pre-registration guard — `CW_015` repeated in a second folder | either field entering `SKELETON` | SUPPORTED |
| DL_006 | The first shape instances the tool's own argument: an asserted 0.61 sits beside a derived `--`, and `detail()` prints "ledger not yet populated" rather than substituting the asserted value or a zero | the derived column filling in and disagreeing with 0.61 | SUPPORTED (holds) |
| DL_007 | The shape names which of `category-weld/welds/hierarchy.json`'s five senses it runs on, and pre-classifies two domains by sense before reading — the first time in this drop family that a stated cross-folder precondition is met | — | SUPPORTED (holds) |
| DL_008 | `anchor.py` keeps `unrouted` and `absent_established` apart and states that collapsing them "loses the distinction the map exists for" — the fifth instance of this repair in the family and the first implemented, counted separately and restated in the output | the two collapsing anywhere in the readout | SUPPORTED (holds) |
| DL_009 | ~~`target_band` and `corroboration.class` are both described as band-setting; only the second reaches a readout~~ | the first anchor map, which shows they are different quantities and the code aggregates the right one | **CORRECTED** — the code is right; one docstring sentence survives |
| DL_011 | `absent_established` is used 0 times of 9 links on the first real map — implemented, counted separately, and not yet earned by any link | a link assigned the state | SUPPORTED (state of the data, not a defect) |
| DL_012 | `unrouted` holds three de-facto states — attempted-and-open, queued, and no-instrument-nameable — and `unrouted_total` merges all three; the schema already carries `paths_attempted`/`paths_open` to separate them | a readout separating them | SUPPORTED |
| DL_013 | The map's `open` list states three numbers about itself — spread 0.5, ceiling 0.80, no link quantified — and all three are exact | any of the three disagreeing | SUPPORTED (holds) |
| DL_010 | The refusal to emit a composite is real and selftest-enforced; the two numbers it does emit (`ceiling`, `anchor_spread`) are functions of three stipulated constants with rationales and no derivation, and unlike `HANDOFF_CEILING` this is not disclosed | a derivation for 0.30 / 0.80 / 0.99, or a disclosure line | SUPPORTED |
| DL_005 | With no `shapes/` directory the tool prints a well-formed report with zero rows and exits 0, where all three sibling scorers refuse on stderr with rc 1 | the empty state refusing, or saying it is empty | SUPPORTED |
| DL_014 | `A2.md` opens by sourcing its own subject to `CLAIM_TABLE.md`, which the folder does not carry, and `A2` appears nowhere else in it — sixth instance of a reference naming an absent artifact in this drop family, three of which landed a drop later | the claim table arriving | SUPPORTED |
| DL_015 | A2's diagnosis is exact against the code: anchor distance is `BAND_CEILING[corroboration.class]`, the class is a declared string, and nothing derives it — `DL_010` from the other side. And the note refuses to adopt its own candidate on stated non-independence, which is `triad-playground` `TP_003`'s shared-bias result applied by the author to their own convergence | a routine deriving the class from something measured | SUPPORTED (holds) |

## 1 — DL_001, the idea and two choices that follow

> A coverage number is not portable without its denominator. 61 percent
> over one domain set is a different quantity than 61 percent over
> another. This records the set.

`criteria-drift` `CD_008` and `anchor-interval` `ANC_006` for a confidence
readout instead of a benchmark: a number is identified only up to the
reference it was taken against, so publish the reference.

**Four readouts, not combined.** The docstring states why — *"Coverage and
cycle depth are different currencies. A shape can be wide and shallow"* —
and `score()` returns them separately. Every other scorer in this family
reduces to one headline number and takes a finding for it
(`PB_007`, `uninstrumented`'s SCALAR DEMAND). This one refuses the
reduction up front, which is why §3 is a one-clause fix rather than a
design problem.

**Denominators printed with the columns.** The table footer says
`cov: held / read` and `cyc: holds that survived a return / holds`, so the
two are visibly not over the same base — `measurement-fork`'s VOID RATIO
made unnecessary rather than enforced.

## 2 — DL_002, the reservation is a constant without its function

> RESERVATION: ... It **caps what the ledger will report as available
> headroom**, and it is why a shape with high coverage still does not
> coalesce.

    ten domains, all hold, reservation 0.20
      coverage 1.00   ceiling 0.80   coverage > ceiling: True
      fields naming headroom: none

`score()` computes `ceiling = 1 - reservation`, returns it, and `detail()`
prints it beside `RESERVATION`. Nothing reads it.

Not a wrong number — the docstring is explicit that reservation is *not*
subtracted from coverage, and it is not. What is missing is the readout
the same paragraph promises: the cap is stated as a function and shipped
as a constant. One line — `headroom = min(coverage, ceiling)`, or a flag
when coverage exceeds it.

## 3 — DL_003, one scalar over two different failures

    all break   coverage 0.00   breaks 2   mixed 0
    all mixed   coverage 0.00   breaks 0   mixed 2

`coverage` is holds / read, and `mixed` sits in the denominator only. A
break is the shape failing; a mixed read is the shape doing something the
two-value vocabulary cannot hold. Both return 0.00.

The information survives — `break_domains` and `mixed_domains` are
returned separately and printed under their own headings — so the loss is
in the derived scalar alone, the shape `PB_007` records one folder over.

Cheapest fix is not a fifth ratio. The footer reads `cov: held / read` and
does not say mixed is in `read`; one clause would.

## 4 — DL_004, the guard field, again

    SKELETON keys            : asserted_coverage, domains, reservation,
                               shape, source, statement
    read by detail(), absent : criterion_fixed_in_advance, open

`criterion_fixed_in_advance` is `category-weld` `CW_015`'s
pre-registration guard **promoted to a first-class field** — there it was
prose inside a term's `open` list, here it has its own key and its own
heading. Right direction, and the same discipline reached a third time
(`reasoning-gate` `G-PRE`, `photoperiod-claim-harness`'s `MechanismEdit`).

And it repeats `CW_015`'s gap exactly: `--new` emits a skeleton without
it, so the field a new shape most needs prompting for is the one the
template is silent about. Two folders, same drop family, same miss.

One thing this tool gets right that the other two do not:

    category-weld/weld.py              --new deep-copies: False
    generation-capacity/capacity.py    --new deep-copies: False
    domain-ledger/ledger.py            --new deep-copies: True

`dict(TEMPLATE)` is a shallow copy sharing nested lists with the module
global — harmless as called in both, one edit away from mutating the
template. `ledger.py` round-trips through JSON.

## 5 — DL_005, the empty report

No `shapes/` directory is delivered. `load()` returns `[]`, `table([])`
prints headers and the full explanatory footer, `main()` returns `None`:

    rows printed  : 0
    lines printed : 9
    exit code     : 0

    category-weld/weld.py              refuses: True
    presented-binary/binary_audit.py   refuses: True
    generation-capacity/capacity.py    refuses: True

Every sibling refuses on stderr with rc 1. This one prints a well-formed
report with no content and exits clean, and the footer's closing line —
*"Unpushed domains are not neutral. Each is an untested surface"* — prints
over zero domains.

The tool's subject is confidence readouts that do not carry their
denominator. Its empty state is a report whose denominator is zero,
rendered as though it had one.

The selftest does cover the empty case at the `score()` level — *"empty
ledger gives none not zero"*, *"empty mismatch is none"* — and those are
the right two checks. The gap is one level up, at a presentation layer the
selftest does not reach.

## 6 — DL_006, an asserted number with no derived one beside it

    hierarchy-cut-generation   domains 30   read 0
                               asserted 0.61   derived --   mismatch --

The shape's source field states the file's purpose:

> Coverage asserted at 0.61 over a domain set carried in working memory
> rather than written down. This file exists to convert the asserted
> number to a derived one; until the read column is filled the derived
> number is unavailable, and that unavailability is the current state, not
> a failure.

`detail()` prints `derived -- ledger not yet populated` rather than
substituting the asserted value or a zero — the branch `DL_002` and
`DL_005` are about, used correctly.

This is the one place in the repo where an author has written down a
number they were already carrying and then run the instrument that
declines to confirm it. Thirty domains, none read, every ratio `--`, and
the reservation's ceiling with nothing yet to cap.

## 7 — DL_007, the run order met

> Runs on the imposed_ordering sense only — see category-weld
> welds/hierarchy.json for the other four senses, which are not this
> claim.

    category-weld/welds/hierarchy.json components (5):
        nested_containment, organizing_abstraction, imposed_ordering,
        ordering_origin, cut_rate
    minus imposed_ordering = 4; the statement says four: True

    domains pre-classified by weld sense, before being read:
        mathematics / order theory      nested_containment sense lives here
        computer science / type systems organizing_abstraction sense lives here

`moral-decomposer` `MD_004` records the opposite state one folder over — a
stated RUN ORDER requiring welded terms decomposed first, seven named,
zero decomposed. Here the weld exists, the shape names which of its five
senses the claim runs on, and two of thirty domains are pre-classified as
probably belonging to a different sense **before** reading, which is the
only time that classification is not closure by construction.

`criterion_fixed_in_advance` carries the same discipline into the read:

> Reclassifying a case as not-really-hierarchy after seeing which way it
> read is closure by construction and is not permitted; such a case is
> MIXED with the reason recorded.

Names the failure, names the routing for the ambiguous case, fixes both
before any domain is read. `DL_004` stands unchanged — `SKELETON` carries
neither field, so a shape from `--new` starts without them — and the
delivered shape shows what they are for.

## 8 — DL_008, the repair, implemented

`anchor.py`'s PROVENANCE CHAINS section:

> **routed** — a path to the next link exists and is stated
> **unrouted** — no path found yet. Alternate paths not exhausted.
> **absent_established** — investigated and the link genuinely does not
> ground that way. Not a failure — a finding, and its own measurement
> problem needing instrumentation.
>
> Collapsing unrouted and absent_established into "blocked" loses the
> distinction the map exists for.

Fifth instance of one repair across this drop family, and the second built
in rather than found:

    PB_004   frame_sim option_gain        0 options found == never ran
    PB_012   binary_audit handoff()       above ceiling == never checked
    GC_004   MECHANISM_10 R3              not cited == no corpus searched
    MD_002   moral-decomposer reduces_to  irreducible == routed elsewhere
    GC_010   SUBCASE_10A S1               absent vs zero, designed in
    DL_008   anchor.py routing states     unrouted vs absent_established

    one unrouted + one absent_established -> unrouted_total 1, absent_total 1

`GC_010` was the first time the distinction was specified ahead of code.
This is the first time it is **implemented** — counted separately in the
readout, and restated in `blocking()`'s output rather than left to the
reader's memory.

What it is not: a reading. No `anchors/` file exists, so the three states
have never been assigned to a real link.

## 9 — DL_009, one of two band-setting fields is aggregated

The opening paragraph and the BANDS heading name different fields:

> What sets the band is where the shape ANCHORS: what it grounds to, and
> what band **that anchor already occupies**.

> BANDS — set by the **class of support**, not by sampling effort.

The schema carries both, and on an anchor where they differ:

    target_band          cycle_persistent (0.99)
    corroboration class  external (0.80)
    document ceiling     0.80

`target_band` is computed per anchor, printed by `detail()`, and
aggregated by nothing — `ceiling_class`, `ceiling`, `anchor_spread`,
`chains_complete`, `unrouted_total` and `absent_total` all ignore it.
Anchoring to thermodynamics, a cycle-persistent target, gives a document
ceiling of 0.80 because the corroboration is external.

**The selftest pins exactly this**: its `thermo` anchor has
`target_band=cycle_persistent` and the asserted check is `ceiling == 0.80`.
The choice is deliberate and the BANDS heading is the one the code follows.

The residue is the opening paragraph, which says anchor proximity sets the
band and that "anchoring near something that has survived generational
cycles raises the number". On the delivered code it does not — proximity
raises `target_ceiling`, which no readout uses. Which of the two sentences
is right is a design question; what is checkable is that a field the
docstring calls band-setting reaches no readout.

## 10 — DL_010, a real refusal over stipulated constants

> No composite figure is emitted. Weighting near against far anchors is
> not specified, and a number produced by guessing at it would be less
> honest than the anchors themselves.

The selftest asserts it — `("no composite emitted", "confidence" not in s)`
— so the refusal is enforced, not promised. That is `DL_001`'s
refusal-of-reduction one step past where `ledger.py` takes it, and the
strongest instance in the family.

Two numbers are emitted and both are functions of three stipulated
constants:

    BAND_CEILING   {none: 0.30, external: 0.80, cycle_persistent: 0.99}
    anchor_spread  takes exactly four values: 0.0, 0.19, 0.5, 0.69

The three have stated rationales — no external body behind it, one reading
of outside material, held across cycles — and no derivation.
`anchor_spread` is a difference of two of them and inherits that.

Same shape as `presented-binary`'s `HANDOFF_CEILING`, which B10 discloses
in its own weak-point line. Here the equivalent line is not written. The
tool refuses to guess at the weighting *between* bands and stipulates the
bands themselves — a defensible split, not stated as one.

The bands are ordinal by construction (`BAND_ORDER`) and `ceiling_class`
is the ordinal readout. `ceiling` converts the ordinal to a number, which
is the step with nothing behind it — `criteria-drift` `CD_002`'s
ordinal-compared-as-nominal, arriving from the opposite direction.

## 11 — DL_004, half the gap closes in the next tool

    ledger.py SKELETON : asserted_coverage, domains, reservation, shape,
                         source, statement
    anchor.py SKELETON : anchors, asserted_confidence, open, sense, shape,
                         statement

    open                        ledger: False   anchor: True
    criterion_fixed_in_advance  ledger: False   anchor: False

`anchor.py` carries `open` in its skeleton. Same author, next tool, half
the gap closed without being asked. `criterion_fixed_in_advance` is in
neither — and `anchor.py` does not read it at all, which is consistent:
the field belongs to a read that classifies domains, and an anchor map
does not classify.

`DL_004` stands for `ledger.py` unchanged, with the direction of travel
recorded beside it. `DL_005` recurs unchanged too — `anchor.py` with no
`anchors/` directory prints headers and its full footer and exits 0.

## 12 — DL_009, CORRECTED

`DL_009` read the docstring's two band-setting sentences as a possible
defect: `target_band` is computed per anchor and reaches no document-level
readout, while the opening paragraph says anchor proximity sets the band.

The first real anchor map settles it, in a note the schema already had a
field for:

> The target itself sits in the cycle-persistent band. **What is
> external-band is the connection between imposed ordering and maintenance
> cost, not the thermodynamics.**

The two fields are not two descriptions of one thing. `target_band` is
where the *target* sits; `corroboration.class` is the class of support for
the *connection* between the shape and that target. Anchoring to
thermodynamics does not inherit thermodynamics' band.

So aggregating `corroboration.class` and not `target_band` is correct.
**This audit read a tension in the prose as a possible defect in the code;
the code is right.**

What survives is one paragraph — *"anchoring near something that has
survived generational cycles raises the number"* describes something the
code does not do and, on the map's own reading, should not. Proximity to a
cycle-persistent target is context, not corroboration.

## 13 — DL_011, the third state, unassigned

    routed               3
    unrouted             6
    absent_established   0

`DL_008` recorded `absent_established` as the first implementation of a
repair specified five times. On the first real map it is used zero times
of nine links.

Not a defect. The culture anchor's second link writes down exactly what
assigning it would mean:

> If this establishes as ABSENT — the construct genuinely does not ground
> in biology — that is a finding requiring its own instrumentation and
> scientific method, not a failure of the shape.

The state is understood, its consequence is recorded, and no link has been
investigated far enough to earn it. `absent_established` requires having
looked; `unrouted` is what you have before you look, and the map is at the
before-you-look stage throughout.

## 14 — DL_012, three states inside one

    link                                          attempted   open
    expenditure to hold an ordering rises ...             0      3
    a system running a rising cost gradient ...           0      2
    environment-coupled vs imposed ordering               0      1
    cultural and religious orderings ...                  0      3
    that provenance grounds through biology               0      0
    human-centrism and ego in the source material         0      0

Every unrouted link has 0 attempted paths; 2 of 6 have no open path named
either. The docstring's definition — *"no path found yet. Alternate paths
not exhausted"* — covers three situations the data distinguishes and the
readout does not:

    paths attempted, none worked, others open   work has been done
    nothing attempted, open paths named         work is queued
    nothing attempted, no path nameable         no instrument exists

`unrouted_total` counts all three as 6. The two in the third group are the
ones whose notes ask for new instrumentation (*"No instrument
identified"*) — the same distance from a reading as `absent_established`,
reached from the other side.

The schema already carries what separates them, and `blocking()` prints
both fields. The gap is at the readout — the same shape as `DL_003`: the
information survives per item and the derived scalar merges it.

## 15 — DL_013, the map's own numbers

    Anchor spread is 0.5                          0.5   exact
    The ceiling reported is 0.80                  0.80  exact
    No link anywhere in this file is quantified   0     exact

Three self-reported numbers, three exact. The second carries its own
qualification — *"It is a ceiling on the whole sense, not a report that
the shape is near it"* — which is the distinction `DL_010` turns on, made
by the author in the file.

The fourth open item is the folder's thesis instanced:

> The load-bearing unrouted link is cost-gradient-by-depth-of-ordering on
> the thermodynamic anchor. Routing it with a number would do more than
> reading further domains, because it converts the near anchor from stated
> to measured.

`ledger.py`'s new paragraph says coverage *"resolves position inside a
band that anchor distance already set ... Reading further domains moves
the number within a band; it does not promote a shape between bands."* The
map then names which single measurement beats more coverage — and it is a
link in a provenance chain, not a domain in a ledger.

That is the pair doing the job it was built for, on one shape, with no
reading taken in either.

## 16 — DL_002, a source for the constant

Drop 4 changes `ledger.py` by docstring only (code byte-identical after
stripping the module docstring). One addition derives the constant
`DL_010` flagged:

> The 0.2 default here encodes only the external-band ceiling of 0.8. The
> 30 floor ... and the 99 band ... live in anchor.py where the source class
> is recorded. **Do not read a ceiling off this file alone.**

    1 - SKELETON reservation           = 0.80
    anchor.py BAND_CEILING['external'] = 0.80

One of `DL_010`'s three constants now has a stated source; 0.30 and 0.99
remain stipulated.

`DL_002` stands unchanged — `ceiling` is still computed, returned, printed
beside `RESERVATION`, and read by nothing. The disclosure sharpens it: the
file now says *do not read a ceiling off this file alone* and `detail()`
still prints `RESERVATION 0.20 ceiling 0.80` as a line of the report. A
number no readout applies and the docstring warns against reading is the
one line in the output with no consumer.

## Relation to the rest of the repo

- `criteria-drift/`, `anchor-interval/` — §1. Same identifiability
  argument, applied to a self-reported confidence instead of a benchmark
  score.
- `category-weld/` — §4. `criterion_fixed_in_advance` is `CW_015`'s guard
  with a schema slot, and the template gap comes with it.
- `presented-binary/` — §3 is `PB_007`'s shape on a different scalar, in
  a tool that avoided it on three others.
- `presented-binary/` — §10. `HANDOFF_CEILING` and `BAND_CEILING` are the
  same kind of constant; B10 discloses its one, `anchor.py` does not.
- `triad-playground/`, `reasoning-dial/` — `truncated` and `channel`
  record where a reading stopped and how it was taken, which is the
  observer-state axis `TP_006` and `RD_009` both name as unbuilt. Here it
  is a field; nothing yet reads it against an outcome.

---

# Drop 5 — `A2.md`, a candidate held open

A prose note. Records a candidate definition for the term A2 flagged as
unspecified, and does not adopt it. Nothing in `anchor.py` changed.

## 17 — DL_014, the note names a claim table the folder does not carry

    files in domain-ledger/ : A2.md, AUDIT_NOTES.md, anchor.py,
                              ledger.py, ledger_audit.py
    CLAIM_TABLE.md present  : False

> A2 in `CLAIM_TABLE.md` records that confidence tracks distance to an
> anchor already in a high band, and flags that what makes an anchor
> *near* versus *far* is unspecified.

The first sentence sources its own subject to a document that is not in
the folder, and `A2` appears nowhere else in `domain-ledger/`. The note is
readable without it — it restates what A2 flagged before building on it —
so nothing is unrecoverable. What is missing is the row the candidate is a
candidate **for**, and with it the other claims a reader would check this
one against.

Sixth instance of one shape in this drop family:

    CW_001   fixtures named in a status sentence     landed one drop later
    PB_001   seeded case + frame_sim fixtures        one of two landed
    GC_009   cases/food-knowledge.json               named 3x, absent
    PB_015   8 synthetic routing paths               absent
    MD_001   decompose.py selftest fixture           absent
    DL_014   domain-ledger/CLAIM_TABLE.md            absent

Three of the six landed in a later drop. The shape is not a defect in any
one drop — it is what writing the prose before the artifact produces, and
it is only visible from outside because the reference and the tree get
read together.

## 18 — DL_015, the diagnosis is right, and converges with `DL_010`

    BAND_CEILING : {'none': 0.3, 'external': 0.8, 'cycle_persistent': 0.99}
    set by       : corroboration.class, a declared label
    measured by  : nothing in anchor.py

A2 says the term the whole function turns on — what makes an anchor near
versus far — is unspecified. Against the code that is exact. Distance is
operationalised as `BAND_CEILING[corroboration.class]`, the class is a
string the author writes into the anchor file, and no routine derives it
from anything. `score_anchor` reads it, `score` takes the max over it, and
`anchor_spread` is a difference of two of these constants.

`DL_010` reached the same place from the other side: `anchor.py` refuses
to emit a composite, which is right, and the two numbers it does emit are
functions of three stipulated constants with rationales and no derivation.
A2 is the author naming that gap and proposing a definition for **the
term** rather than for the constants — the more useful half, since a rule
that decides the class turns the constants into an ordering rather than a
measurement.

The candidate: **an anchor is near because it is assemblable.** That is
`constraint-assembly`'s invariant class read as a band, and if it held it
would make the two folders one instrument — the anchor map stops being a
confidence score and becomes a load table, with confidence derived rather
than primary. The note says that would need `anchor.py` rewritten rather
than amended, and is the reason it stays in prose.

**What the note does that matters more than the candidate.** It refuses to
adopt it, and names the reason:

> the convergence was noticed in the same conversation that produced both
> descriptions, which is not independent.

That is `triad-playground` `TP_003`'s shared-bias finding — readers who
share an input agree tightly and the agreement carries no information —
stated by the author about their own convergence, before anything rests on
it. In TP_003 three of four shadows were AI; here the two descriptions are
one author in one session, which is the same structure at n=1.

The falsifier is named and is a search rather than an experiment:
something well-corroborated that is not assemblable, or something
assemblable with thin corroboration. Neither has been looked for, and the
note says so.
