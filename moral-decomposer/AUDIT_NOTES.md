# AUDIT_NOTES — moral-decomposer

Added, not delivered. [`README.md`](README.md),
[`CLAIM_TABLE.md`](CLAIM_TABLE.md) and both files under [`cases/`](cases/)
are the drop as received and are not modified.

    python3 moral_audit.py

## What the drop is

Takes a disagreement presented as moral or ethical and decomposes it into
option-distribution claims plus the frames those claims imply. Three
stages — **option layer** (per party: enters the tally, generates options
or held fixed, decides), **frame layer** (the boundary criterion the
assignments imply, whether documented, whether acquired in development),
**cut count** (further boundary decisions the frame requires, and how many
are documented). The output is the **residue**: what still disagrees once
the lower stages are matched.

Five claims `M1..M5` and a DISCLOSED WEAKNESSES section.

## File status

| file | status |
|------|--------|
| `README.md` | delivered, verbatim |
| `CLAIM_TABLE.md` | delivered, verbatim |
| `cases/animal-standing.json` | delivered, verbatim |
| `cases/means-to-save.json` | delivered, verbatim (uploaded twice, byte-identical) |
| `decompose.py` | **named five times in the README, did not arrive** |
| `moral_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

`decompose.py` is **not reconstructed**. `category-weld` `CW_004` is the
cost of the one time a reconstruction filled a gap of this kind — the
reconstruction's arithmetic choice produced a finding that the delivered
file then refuted — and this README fixes far less of the arithmetic than
that one did. Everything below is read off the delivered case JSON.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| MD_001 | M5's status is entirely a statement about `decompose.py`'s selftest, which did not arrive; on the delivered corpus 0 of 4 residue candidates are live, so nothing in the folder shows the detector can fire | `decompose.py` arriving with the fixture | UNVERIFIED — fifth consecutive drop with this shape |
| MD_002 | `reduces_to: null` carries two opposite meanings — "irreducible, this is the finding" and "not applicable, routed elsewhere" — separated only by an author-set `resolved` boolean | a third value, or a check on `resolved` | SUPPORTED |
| MD_003 | M3's stated asymmetry (3 undocumented cuts vs 0, both cases, opposite file positions) is exact; `terminates` is a separate asserted field and nothing checks it against the cut list | a case where the two disagree and the tool says so | SUPPORTED |
| MD_004 | The README's RUN ORDER requires welded terms decomposed first; 4 welded terms are named across the 2 cases and 0 exist in `category-weld/welds/` | any of the four arriving as a weld file | SUPPORTED — the drop discloses it |
| MD_005 | The no-moral-labels rule holds: 0 of the 22 distinct field names in the delivered schema carry a moral term | a moral term in a field name | SUPPORTED (holds) |
| MD_006 | The drop's own first disclosed weakness is the finding an auditor would lead with, with the mechanism named — the process producing the reductions is the process predicting them | — | SUPPORTED (holds) |

## 1 — MD_001, M5 rests on the missing file

> **M5.** Zero live residue across cases is an absence, not a proof.
>
> *Status:* stated in the tool output and enforced by the schema: the
> selftest includes a fixture with a live residue item, so a non-empty
> residue is representable and the instrument is not rigged toward M1.

Both halves of that status live in `decompose.py`. Neither is in the drop.

M5 is the guard against the folder's central risk — that a decomposer
built to show disagreements reduce will show them reducing. It is the one
claim whose entire content is *the detector can fire*, and it is the one
claim uncheckable from the folder.

    residue candidates in the delivered corpus : 4
    marked resolved                            : 4
    live                                       : 0

0 of 4. `null-harness` grades a detector never shown to fire
`CONSTANT_SILENT`; here the demonstration exists and was not shipped.

Fifth consecutive drop whose status sentence names an absent artifact:
`CW_001` (code, arrived one drop later), `PB_001` (data, arrived exact),
`GC_009` (data, outstanding), `PB_015` (tests, outstanding). The pattern
so far is real and late.

## 2 — MD_002, one null, two meanings

The README's stage description makes `reduces_to: null` the finding:

> **RESIDUE** candidates that reduce to stage 1 or 2 are accounted for.
> Candidates that reduce to neither are the case the instrument exists to
> find.

    case             claim                                    reduces_to  resolved
    animal-standing  the two sides hold different values...   frame       True
    animal-standing  the excluding side simply cares less     option      True
    means-to-save    an irreducible clash between counting... option      True
    means-to-save    both sides accept the presented set...   None        True

The last row is `reduces_to: null` **and** `resolved: true`. Its note says
it is not residue between the sides but agreement between them, routed to
`presented-binary`.

**That reading is right, and it is the most interesting cell in the drop**
— agreement across both sides is where a shared unmeasured assumption
sits, and the case says so in those words. What it costs is the field's
meaning: a null `reduces_to` is now either the finding or its opposite,
and only `resolved` separates them — a boolean the case author sets, with
nothing checking it.

A third value fixes it: `option` / `frame` / `routed` / null, with null
reserved for the finding. Same shape as `PB_012` and `GC_004` — one value
standing for a measurement and for its own absence.

## 3 — MD_003, the asymmetry is exact

    case             side       boundary criterion       cuts  undoc
    animal-standing  admits     capacity to have options    1      0
    animal-standing  excludes   species membership          3      3
    means-to-save    permits    parties are counted, not    3      3
    means-to-save    refuses    a party with option gene    1      0

M3's status is confirmed to the digit, including the position claim — the
3-cut side is second in one case and first in the other.

The status also states its own limit, correctly: *"cut lists are
enumerated by hand, so the count reflects the enumerator, not a survey.
Not a measurement."* That is stronger than it looks — a frame with no
listed cuts scores as terminating, so the readout is `CONSTANT_SILENT` on
any frame nobody enumerated. `terminates` is a separate asserted field
that could contradict the cut list; on all four sides they agree, and
nothing in the schema would catch it if they did not.

## 4 — MD_004, a run order with nothing enforcing it

> Welded terms first. ... List them in `welded_terms` and decompose in
> `category-weld` before trusting the output.

    case             welded term      in category-weld/welds/
    animal-standing  interests        False
    animal-standing  count            False
    means-to-save    means            False
    means-to-save    the few          False

4 named, 0 decomposed. The drop discloses this itself.

`the few` is `presented-binary` B5's *"a few"* under a different article —
the same term now named from a second folder, still with no
`welds/a_few.json` (`PB_009`). **Two folders point at one missing file**,
and the stated run order says the output of both is untrustworthy until it
exists.

Not a defect in the cases: a stated precondition with no schema slot to
check it. The shape recurs — `MF_017`, `CW_015`, `GC_003`.

## 5 — MD_005, the no-moral-labels rule holds

22 distinct field names across both case files; 0 carry a moral term.
`in_tally`, `held_fixed`, `optionality`, `decision_authority`,
`boundary_criterion`, `cuts_required` are positional and directional and
none scores a side.

Cheap to state, expensive to keep, and worth recording as holding. The one
route a moral term could take without tripping the check is a **value**
rather than a key — `position` and `claim` are free text and carry the
dispute's own language. Those are quotations of the parties, not the
instrument's vocabulary, which is the right place for them.

## 6 — MD_006, the weakest part is named by the drop

> Both cases are model-constructed. ... the reductions here were produced
> by the same process that predicts them.

That is the finding an auditor leads with, stated by the author with the
mechanism named. Both `source` fields say it unprompted, and
`animal-standing` goes further — *"Offered, then found to reduce; recorded
with the reduction rather than discarded"* — a candidate counterexample
that failed, kept with its failure. The refutation protocol applied to the
folder's own generated evidence.

What this audit adds is the arithmetic: n=2, both self-produced, 0 live
residue, and the fixture that would show a non-empty residue is
representable is the file that did not arrive. The claim table calls n=2
self-produced "the weakest evidence in the repo" and does not overstate.

## Relation to the rest of the repo

- `category-weld/` — the RUN ORDER's first step. §4; four terms named,
  none decomposed.
- `presented-binary/` — the RUN ORDER's second step, and `means-to-save`
  routes to it explicitly. `the few` ↔ B5's "a few".
- `generation-capacity/` — M4 (`acquired`) links to MECHANISM 10: a
  developmentally acquired frame as an option ceiling rather than a
  position selected from a set.
- `null-harness/` — §1 is the known-signal half missing from a detector.
- `reasoning-gate/` — the three-stage ordering is a pipeline whose later
  stages are only readable if the earlier ones matched, which is `G-LAYER`
  applied to a dispute instead of to a quantity.
