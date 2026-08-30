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
