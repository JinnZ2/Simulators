# CLAIM_TABLE — fold-matrix

Claims about work order 8 and about what its fixtures produced.
`WORK_ORDER.md` is delivered and is not edited.

REFUTATION_PROTOCOL: each claim names what would refute it. A failed
check updates the claim, never the instrument's numbers.

---

### FM_001 — the arm this order extends is not in this repository

The order opens *"Extends: folded-term instrument. The downward arm
(levels severed, deepest still-acting term) already has a reading."*

There is no folded-term instrument here and no downward reading in it.
`severed`, `still_acting` and *deepest still-acting term* return **zero
hits** across the tree before this folder. `residual-direction/` names a
"fold detector" as a companion and `claim-record/SPEC.md` cites one as
the reason the frames work was specified early — both are pointers to
something outside.

Seventh instance of the stated-thing-with-no-artifact shape (`MF_017`,
`CW_015`, `DL_004`, `GC_012`, `UNI_013`, `SSS_050`) and the largest so
far: the prior six were a missing field or a missing test, and this is a
missing arm of the instrument being extended.

**Nothing is reconstructed.** The grid holds both arms and downward cells
are filled only where today's material fills them; H1's levels −2 and −3
carry `ABSENT` rather than a plausible reading. That is the `PB_001` /
`CW_004` rule, and the one prior reconstruction in this repository is
what it cost.

**Falsifier:** a downward-arm reading predating this folder.

**Status: SUPPORTED. The grid is built; the downward arm is a schema
with two filled cells, not a reading.**

---

### FM_002 — the fixtures do what S6 requires, and one of them exposed a defect in the instrument

| fixture | S6 requires | result |
|---|---|---|
| H1 grid emission factor | downward levels resolve, level-0 clock derivable, upward cells ASSERTED | −1 and 0 resolve, level-0 clock **3.403 y derived**, upward **ASSERTED ×2 + ABSENT ×1** |
| H2 "more efficiency solves this" | NOT_EVALUABLE on S3, not a low score | `NOT_EVALUABLE`, all three scope fields named, no score emitted |
| H3 tree replacement | Y_function_set UNREAD, comparison refused | `UNREAD`, refused as *"nothing was compared"* |
| H4 two conflicting clocks | both emitted, mismatch flagged, no pick | 0.003 y and 3.0 y both emitted, mismatch flagged, `collapsed: None` |

H1's level-0 clock is derived rather than stated: `3.0 y / 0.8815` where
the coupling was **measured by perturbation** in
`sheet-structure-scan/coupling.py`, not asserted.

**Falsifier:** a fixture passing for a reason other than the one S6
names.

**Status: SUPPORTED, 4 of 4.**

---

### FM_003 — the clock check could not tell an assumption from its own derivative, and H1 is what showed it

S5 says *"if two levels assume different time constants, emit BOTH and
flag the mismatch"*. The first implementation counted distinct
`(value, units)` pairs, and on H1 that reads:

| level | clock | |
|---|---|---|
| −1 | 3.0 years | the generation mix, assumed |
| 0 | 3.403 years | **3.0 / 0.8815**, derived from level −1 |

and flags a mismatch. **It is one horizon and its own derivative**, not
two horizons in conflict — the coupling divisor is what makes the numbers
differ, and dividing an assumption by a measurement does not produce a
second assumption.

Repaired with a `derived_from` field on the clock: derived clocks are
still **emitted**, with what they came from, and only the disagreement
count excludes them. H1 now reports no mismatch and H4 still does.

The defect matters because the false positive runs toward the finding:
S5 says a term whose levels disagree on horizon **is** the finding, so an
over-firing check manufactures findings, and every derivation chain in
the claim registry would produce one.

**Falsifier:** two independently assumed clocks the check reads as a
derivation.

**Status: REPAIRED, pinned three ways.**

---

### FM_004 — P1 and P2 hold, and the evidence for them is narrower than the tally

Registered in `PREDICTIONS_WO8.md` before the fixtures were authored.

| | prediction | result |
|---|---|---|
| P1 | ASSERTED + ABSENT are a strict majority of upward cells | **True** — 3 soft, 0 hard |
| P2 | every `value_string` is empty | **True** — 3 of 3 |

**The honest scope.** Two of the four fixtures are excluded from the
tally as NOT_EVALUABLE, correctly, so the tally rests on H1 and H4. H4's
single upward cell was authored from this repository's own claim table.
**H1's three cells are the only ones traceable to an artifact outside
this session** — they are read from `Disclaimer!A3` of the UNFCCC
calculator, quoted, and anyone with that file can check them.

So P1 and P2 hold on n = 2 terms with external evidence from one, and
that is a weaker result than "4 cells, 4 empty" reads as.

**A weaker registration than WO6's, stated.** `PREDICTIONS_WO8.md` was
written before the fixtures existed but was **not committed before the
run**, unlike WO6 where the commit hash is the timestamp. The evidence
that it preceded the fixtures is the file's own ordering in one commit,
which is weaker.

**Falsifier:** an upward cell in a term drawn from an external artifact
carrying a non-empty value_string.

**Status: SUPPORTED, at the scope stated.**

---

### FM_005 — an empty value_string has two causes and the four basis values do not separate them

S2 requires `value_string` per upward cell and says empty is the normal
result. On H1 level +1 it is empty for a reason the schema cannot record:
the source **states the goal and explicitly declines the relation**.

`Disclaimer!A3` says the calculator exists *"to support organizations to
estimate their GHG emissions"* and, in the same cell, that the secretariat
*"makes no representations as to the accuracy, completeness, suitability
or validity of any information on this Spreadsheet"*.

That is not `ABSENT` — a goal is stated. It is not ordinary `ASSERTED`
either: a relation claimed at adoption with no value string, and a
relation the source refuses to claim, are different facts arriving at the
same empty cell.

**Fourteenth instance of the absent-vs-known-negative repair here**, and
the first where the missing state is *the source declined*. Carried as a
`source_disclaims` field beside the basis rather than folded into it, and
printed under the upward table with the quote, so the distinction is
visible without adding a fifth basis value to a delivered vocabulary.

**Falsifier:** a use where *nobody stated a relation* and *the source
declined to state one* license the same next step.

**Status: SUPPORTED. Recorded, not resolved by widening the vocabulary.**

---

### FM_006 — NOT_EVALUABLE is unrankable structurally rather than by convention

S3: *"Do not score it, do not rank it, do not carry it into a
comparison."* Three instructions a caller can forget.

`score()` **raises** on a NOT_EVALUABLE term — and raises on an evaluable
one too, with *"one term, one grid, not one number"*, because there is no
score in this instrument at all. `upward_tally()` excludes refused terms
and names them, so a refusal never enters a count as a zero.

The H2 fixture is the case: it returns `NOT_EVALUABLE` with all three
scope fields named, and the report states in its own words that this is a
refusal about what can be read and not a low reading.

One distinction the check makes that S3 does not: a scope field **present
but declared unknown** is missing too, and is reported apart from an
omission. `horizon: "unknown"` is an honest declaration and still does not
let a ratio be compared, but the two call for different next steps — one
is a gap in the record, the other a measurement nobody has.

**Falsifier:** a path by which a NOT_EVALUABLE term reaches a ranking.

**Status: SUPPORTED.**

---

### FM_007 — S3's scope is declared-frame's core plus one field, and the two are wired rather than retyped

`boundary` and `horizon` are two of `declared-frame`'s three CORE fields.
They are **read out of `declared-frame/v2/check_frame.py` at import** and
asserted in the selftest, rather than retyped here, so the two folders
cannot drift about what a frame's core is — the no-copies convention
`MF_019` and `tools/check_gate_drift.py` exist for.

`with_respect_to` is S3's addition and is a different question:
declared-frame asks what is inside the accounting, S3 asks what the ratio
is taken **against**. `who_counts`, declared-frame's third core field, is
not required here.

The H3 fixture is where that bites: its `neutral_reading.frame` is
`DF_005`'s finding verbatim — the panel frame excludes fabrication,
mining, smelting, transport, installation, maintenance and decommission
while the leaf frame puts all of them inside the same photon budget — so
the term is NOT_EVALUABLE on `boundary: unknown` **and** would be a void
ratio if it were filled in.

**Falsifier:** a change to declared-frame's CORE that this module does
not pick up.

**Status: SUPPORTED, asserted at selftest.**

---

### FM_008 — the exemption harness kept "for a real exemption later" is spent here, on exactly one word

`SSS_049` retired scan 4's exemption and kept the three-arm harness for a
real case. This order is one: S3 names the efficiency class as
*"efficient/optimal/better/faster"*, and **`better` is on `no_severity`'s
interpretation list** while the other three are not.

`DELIVERED_VOCABULARY = ("better",)` — one token, declared, and measured
three ways: the report is clean under the mask, nothing but that token
fires without it, and a planted grading word is caught through the
exemption. A fourth check asserts the list is length one, so a widening
turns it red rather than passing quietly.

`waste`, `optimization` and `improvement` are flagged by S4 and are **not**
on the screened list, so they need no exemption — checked rather than
assumed.

**Falsifier:** a screened word in an emitted report, or an exemption
entry the order does not name.

**Status: SUPPORTED.**

---

### FM_009 — S4's neutral reading is a declared field, because a name cannot be de-signed

S4 says to flag any variable whose name asserts a sign and *"emit the
neutral reading alongside: the measured quantity plus its frame"*.

The neutral reading is **not computed from the name**. There is no string
operation that turns *efficiency* into *joules out per joule in, at the
cell surface, instantaneous* — producing one would be inventing a
measurement, which is the failure `uninstrumented`'s `PROXY SUBSTITUTION`
names. So it is a declared field, and a flagged term without one reports
`NOT_SUPPLIED` rather than a guess.

H2 is the case: `more efficiency solves this` is flagged and supplies
nothing, and the report says the field is not something a name can be
de-signed into. H3 supplies one, and it is `DF_005`.

The flag list is a superset of the efficiency class: `waste`, `leakage`,
`savings` and the rest assert a direction without triggering S3's scope
requirement. Both halves are asserted, because collapsing them would make
every mention of a loss require a horizon.

**Falsifier:** a neutral reading derivable from a name.

**Status: SUPPORTED.**
