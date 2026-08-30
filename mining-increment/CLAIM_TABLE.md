# mining-increment — claims

REFUTATION_PROTOCOL: a failed check updates the claim, never the
instrument. The delivered `SOURCE_DROP.md` is verbatim and is edited by
nothing here. Findings dated 2026-08-30.

## MI_001 — the coupling pair closed from the other side, within the session

GAP 15 landed naming Gap 14 as absent from this tree; Gap 14 then
arrived — so the pair the two entries forbid treating as independent
now couples in-tree from both ends, and **the first clause of
`BI_001`'s falsifier fired** ("any of the five absent artifacts landing
in this tree"). That claim is updated forward, not rewritten: it rated
the tree as it stood at its audit, and its update note records the
arrival. Resolved here by existence: Module F, the Columbia/Snake node
list, and GAP 15 by content (the sibling folder's SOURCE_DROP header).
Still absent: the register, `SCOPE_BOUNDARY.md`, `knowledge_state.py`,
`contributing_inflow.py`, Gap 1, Gap 2. The interface the deliverable
is specified against (`contributing_inflow.py`) is among the absent —
so the interface equation is built here from the drop's own line, and
plugging into the real module is the student's step.

**Falsifier:** any remaining absent artifact landing — which is the
intended path, and what happened to this claim's sibling.

## MI_002 — the headline knowledge state is contradicted by the drop's own appendix

The headline: *"Knowledge state: NOT_STUDIED (the coupling term)"*,
and §"Why different": *"the connecting term is unstudied on both sides
of the silo boundary."* The trailing section then lists the Kuye-basin
record doing exactly the connection: CWIM incorporates
InSAR-identified subsidence areas *as a boundary condition* in a
coupled surface-water/groundwater model (*"this is a BASIN-SCALE
carry"*), the Kuye coupling model feeds three-zone theory into the
groundwater calculation, and streamflow reduction is *"measured, basin
scale."* Both statements are in the delivered text. The reading that
survives both is the one the TRANSFER CAVEAT already frames: the
coupling term is UNDER_STUDY in the coal-basin record and
NOT_STUDIED **for this basin and rock** — the section's own title
("what the Chinese work has that the Western record didn't") says the
narrower thing; the headline says the wider one. Recorded, not decided
for the author: the fix is one parenthetical in the headline.

**Falsifier:** a reading of the CWIM row under which subsidence-as-
boundary-condition is not the coupling term. The row's own arrow
("a BASIN-SCALE carry, not a subsurface-only study") is the drop
classifying it.

**UPDATE 2026-08-30 (addressed forward):** the revision
(`SOURCE_DROP_V2.md`) resolves the tension in a stronger form than
this claim's suggested parenthetical — the headline stands and its
*referent* is defined one paragraph down: what no record carries is
reservoir pool loading on a multi-dam surface chain, the two existing
carries stopping one node short of each other. The sentence this
finding keyed on is gone, and the appendix is promoted to a primary
source table. Checked in `revision_audit.py`; the claim keeps its
rating on the text it rated.

## MI_003 — the drop's provenance flag is contained, and stronger than its sibling's

Two of the drop's own citations are flagged unconfirmed by name
("Padhy et al. 2026", "Piao et al. 2024"), each with the reason, an
anchor substituted (the Knothe form, full DOI, confirmed), and an
explicit instruction — *"do not publish 'Padhy 2026' or 'Piao 2024' as
given."* Checked by containment: both flagged names occur **only
inside the flag that disclaims them**, so nothing in the delivered
text builds on either. This is per-citation negative provenance with
anchors — stronger than GAP 15's blanket hedge, and the `UNI_029`
negative-provenance record from the author's side, now with named
items. The module follows the instruction: `knothe()` is the anchor,
`mmf()` is carried as ALTERNATIVE with unverified attribution, and
neither flagged name appears in any code file here.

**Falsifier:** a flagged name appearing outside the flag, or an
equation here resting on either. The containment count runs on every
selftest.

## MI_004 — the transfer caveat is enforced structurally, second in a row

Method step 2's rule — *"mark the imported parameter UNDEFINED rather
than applying it"* — is a code path: an `ImportedParam` applied to a
basin whose transfer is neither the study basin nor established
returns the string `UNDEFINED`, a refuted transfer returns the same,
and establishing or refuting takes a basis. The two carried porosity
deltas (+7.42%, +19.25%) enter against their coal-basin study and
return UNDEFINED for the Columbia/Snake chain today. Second
consecutive gap whose sharpest rule arrived in delivered prose before
any code and got built as structure rather than caution (GAP 15's sign
caveat; the `DLA_006` designed-in class) — and the falsifier evaluator
refuses to read UNDEFINED as a low value, so an unapplied import can
never close the gap.

**Falsifier:** an unestablished application returning a number. The
gate is exercised in both directions by the selftest.

## MI_005 — the stock/flow separation is a schema, not a caution

Method step 4 forbids a subsurface storage change and a surface flow
change sharing a variable name (Gap 1's rule; `category-weld`'s
mechanism from the prevention side). Built: the water-balance link is
one record with two distinct required fields —
`storage_side_infiltration_capacity_delta` and
`flow_side_runoff_coefficient_delta` — plus its basis, and no function
in the module returns a single scalar for the pair. A None on either
side is legal and means unmeasured on that side, which is a different
statement from the sides sharing a name.

**Falsifier:** a function here collapsing the pair to one number.
The field names are the check.

## MI_006 — the equations' stated properties hold by arithmetic

The drop says the Knothe and MMF forms share W(0) = 0 and the W₀
asymptote — computed, both hold; Knothe is monotone on a sample; the
strain integral is dimensionally length and a constant profile
returns depth × strain exactly. The forms are carried per the drop's
own instruction: Knothe as the anchor (confirmed, DOI on record), MMF
as the alternative pending its real citation. Nothing here is a
statement about any overburden.

**Falsifier:** either shared property failing at any admissible
parameter set. The check is a limit computation.

## MI_007 — the falsifiers encode three-valued, and the transfer one has three outcomes

The primary falsifier (every increment below 1% AND no rim
intersection) closes on constructed data, stands on a reaching
increment or a rim hit, and returns UNMEASURED on any unknown — an
UNDEFINED import included. The secondary is the **first falsifier in
this family with three outcomes by the drop's own text**: transfer
refuted everywhere → `GAP_NARROWS` (the imports revert to UNDEFINED
and the question becomes *what is the delta for this rock*), any
transfer established → stands, nothing yet examined → UNMEASURED.
A falsifier whose firing narrows a gap instead of closing it is a
different instrument from the family's close/stand pairs, and the
drop specified it. On the real chain both return UNMEASURED: every
cell is unmeasured, the data hosts sit in the carried allowlist-refusal
state (the probe itself was blocked in the landing session — noted in
`audit.py`, not glossed as a measurement), and nothing is supplied
from memory.

**Falsifier:** for the encoding — an unreachable branch (all eight
are exercised). For the gap — the MRDS/InSAR passes the method names.

## MI_008 — the literature rows are carried; the schema is imported, not copied (UNVERIFIED where carried)

All table rows and the CWIM/Kuye rows are carried and unverifiable
from here (publisher hosts in the carried allowlist-refusal state;
`ANC_010`/`MS_004` status), with
the drop's own CITATION STATUS naming the resolution as the student's
step zero. The parameter schema is **imported from
`bridge-impoundment`** rather than copied — both gaps state the
identical deliverable condition, so there is one constructor for it in
the tree, per the no-copies convention (`MF_019`'s lesson). Nothing in
`MI_001..MI_007` rests on any carried row's value; the two numbers
that enter code (the porosity deltas) sit behind the transfer gate and
currently reach no basin.

**Falsifier:** any carried row failing against its named source —
which adjusts the row per the drop's citation status, not these
claims.

## MI_009 — the revision resolves MI_002 by defining the term, not hedging the headline

`SOURCE_DROP_V2.md` lands verbatim beside v1 (both stay). The sentence
`MI_002` keyed on — *"the connecting term is unstudied on both sides
of the silo boundary"* — is gone from v2; in its place the carries are
stated precisely (*"The two carries stop one node short of each
other, and neither reaches a cascade"*), the headline stands with its
referent defined one paragraph down (what no record carries is
**reservoir pool loading on a multi-dam surface chain**), and the
trailing appendix is promoted to a primary source table (*"Entered as
peer sources, primary"* — *"primary, not alternative"* in the
heading). The repair is stronger than the audit's one-parenthetical
suggestion — the `UNI_085` shape, the actual fix beating the proposed
one, arriving in this folder one drop after the finding.

**Falsifier:** the keyed sentence surviving in v2, or the referent
left undefined. Both are string checks on the delivered text.

## MI_010 — the READ CEILING is a per-source read-depth declaration, and the scaffold honors it

New in v2: *"These are entered from English-language abstracts and
citation metadata. The CWIM boundary-condition formulation — the exact
thing that would plug into `mining_increment.py` — is not visible at
that depth… This is a capability limit on the audit, not an open
question about the work."* A source's load-bearing content sitting
below the depth it was read at is a distinct epistemic state — not
carried-and-unverified (the row IS verified at abstract depth), not
absent — and the entry declares it per source with the retrieval step
routed into the method. The family's absent-vs-known-negative repair
applied to citation depth, from the author's side. Checked here in
both directions: the declaration's three parts are present, and the
scaffold complies — no CWIM formulation appears in
`mining_increment.py`, so the ceiling is honored rather than silently
exceeded by an invented boundary condition.

**Falsifier:** a CWIM formulation in the scaffold with no full-text
source behind it. The compliance check runs on every selftest.

## MI_011 — the epistemics changed and the arithmetic did not: six sections byte-identical

Verified mechanically across the revision: the subsurface table, the
governing equations with the provenance flag, the citation-status
paragraph, the research question, the method, and the deliverable-
plus-falsifiers are **byte-identical** between v1 and v2 — while the
three sections the revision is about (the split paragraph, the
transfer caveat, the why-different opening) all changed, so the diff
check can fail in both directions. The provenance flag re-contains on
v2 (both flagged names only inside the flag; the Knothe DOI present).
The scaffold therefore stands unchanged on an unchanged
specification — a revision that moved the claims and left the
instrument alone, which is what *"the claim updates, never the
instrument"* looks like from the author's side.

**Falsifier:** any invariant section differing, or a changed section
identical. Both lists are pinned.

## MI_012 — the CONFIGURATION NOTE carries the FIRM/SOFT split into the source table

*"The mechanism (stress / seepage / fracture coupling degrading a dam
body) transfers; the configuration does not"* — the
mechanism-versus-instantiation split this family keeps as FIRM/SOFT
(`RCC_007`) arriving inside the author's own source table, applied to
the CMUR dam work (a coal-pillar dam inside a mine is not a surface
impoundment in a cascade). Beside it, two ranking rules stated as
discipline rather than sentiment: the configuration difference *"is
not a reason to rank these sources below an English one"*, and the
transfer caveat's closing — *"The language of the source carries no
weight here; the geology of the basin carries all of it."* The
transfer gate built at v1 is exactly the instrument this rule wants:
transfer is a physics declaration per basin with a basis, and the
source's language has no field.

**Falsifier:** a ranking or weighting anywhere in this folder keyed
to source language. There is none; the gate's only key is the basin.

## MI_013 — the addendum is a verified pure insertion, and the validation case is the known-answer rule arriving in the entry's own text

The pore-pressure addendum landed with an exact placement instruction
(*"insert before 'CONFIGURATION NOTE — not a discount.'"*) and
`SOURCE_DROP_V3.md` is the assembly: the fragment is extracted
mechanically from the delivery sheet (`ADDENDUM_DELIVERY.md`,
verbatim), appears once, sits immediately before the instructed
marker, and removing it reproduces v2 byte-for-byte — checked in
`revision_audit.addendum()`, with a doctored-v3 arm proving the
pure-insertion check can fail. The content: `u` is the term that
drops the factor of safety and is normally a MODELED quantity, and
Bondevik & Sorteberg (2021, `10.5194/hess-25-4147-2021`) record it
*"DURING a debris flow event"* — so the modeled term has, for the
first time in this entry, a measured answer to reproduce. *"A modeled
u that cannot reproduce a measured u on a real event has not earned
its place in the FoS calculation"* is `tools/known_answer.py`'s
standing rule stated by the author about the entry's own load-bearing
term — and the entry routes it itself: *"this is the transfer test in
Method step 2, applied to the pore-pressure term,"* which is the gate
`ImportedParam.establish_transfer` already is. No new code path was
added, because the delivered routing lands on one that exists.

**Falsifier:** for the assembly — `v3.replace(fragment, "") != v2`,
pinned. For the routing — a pore-pressure transfer established
without a basis; the gate raises on that today.

## MI_014 — a third literature enters, and the language-carries-no-weight rule now has three instances

The entry's source table carried two bodies: Chinese basin-scale
carries (primary, per the v2 promotion) and Western textbook methods.
The addendum adds a third — Norwegian instrumented field events, in
English, from a hydrology venue — and the `MI_012` rule (*"The
language of the source carries no weight here; the geology of the
basin carries all of it"*) now binds in both directions: the
Norwegian case enters for its measured `u`, not for being in English,
and its transfer to the Columbia/Snake is exactly as UNDEFINED as the
coal-basin porosity deltas until a per-basin basis is declared — a
rain/snowmelt-triggered debris-flow slope in western Norway is not a
mining-undermined reservoir rim. The scaffold's gate applies
unchanged, which is the check that the rule is structural rather than
rhetorical: three literatures, three languages of origin, one basin
key.

**Falsifier:** any code path or table treating the Norwegian value
as transferred to the chain without an `establish_transfer` basis.
None exists; no `ImportedParam` for `u` is even instantiated,
because the addendum carries a citation, not a coefficient.
