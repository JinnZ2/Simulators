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
| `ledger.py` | delivered, verbatim |
| `anchor.py` | delivered drop 3, verbatim — companion; selftest 14/14 |
| `anchors/` | not delivered — no anchor map has been recorded |
| `shapes/hierarchy-cut-generation.json` | delivered drop 2, verbatim — 30 domains, 0 read, asserted coverage 0.61 |
| `README.md`, `CLAIM_TABLE.md` | not delivered |
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
| DL_002 | The reservation is defined as capping reported headroom and nothing applies it: `ceiling` is computed, returned, printed, and read by nothing; coverage may exceed it with no readout saying so | a headroom field, or a flag when coverage exceeds the ceiling | SUPPORTED |
| DL_003 | `coverage` puts `mixed` in the denominator and not the numerator, so all-break and all-mixed both return 0.00 | a footer clause naming what the denominator includes, or a separate ratio | SUPPORTED |
| DL_004 | `detail()` reads `criterion_fixed_in_advance` and `open`; `SKELETON` carries neither, so `--new` never prompts for the pre-registration guard — `CW_015` repeated in a second folder | either field entering `SKELETON` | SUPPORTED |
| DL_006 | The first shape instances the tool's own argument: an asserted 0.61 sits beside a derived `--`, and `detail()` prints "ledger not yet populated" rather than substituting the asserted value or a zero | the derived column filling in and disagreeing with 0.61 | SUPPORTED (holds) |
| DL_007 | The shape names which of `category-weld/welds/hierarchy.json`'s five senses it runs on, and pre-classifies two domains by sense before reading — the first time in this drop family that a stated cross-folder precondition is met | — | SUPPORTED (holds) |
| DL_008 | `anchor.py` keeps `unrouted` and `absent_established` apart and states that collapsing them "loses the distinction the map exists for" — the fifth instance of this repair in the family and the first implemented, counted separately and restated in the output | the two collapsing anywhere in the readout | SUPPORTED (holds) |
| DL_009 | `target_band` and `corroboration.class` are both described as band-setting; only the second reaches any document-level readout, and `target_band` is computed, printed per anchor, and aggregated by nothing | `target_band` entering a document-level field | SUPPORTED |
| DL_010 | The refusal to emit a composite is real and selftest-enforced; the two numbers it does emit (`ceiling`, `anchor_spread`) are functions of three stipulated constants with rationales and no derivation, and unlike `HANDOFF_CEILING` this is not disclosed | a derivation for 0.30 / 0.80 / 0.99, or a disclosure line | SUPPORTED |
| DL_005 | With no `shapes/` directory the tool prints a well-formed report with zero rows and exits 0, where all three sibling scorers refuse on stderr with rc 1 | the empty state refusing, or saying it is empty | SUPPORTED |

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
