# CLAIM TABLE — ANCHOR POSITION AND MEASURAND CROSSING

Prefix `APM_` (`AP-` is the order's own claim id space and is left to it).
Statuses: SUPPORTED / REFUTED / UNVERIFIED / OPEN, with the falsifier stated
per claim. Every SUPPORTED here is supported on constructed fixtures; nothing
in this folder is a statement about any model.

---

**APM_001.** The two prompts are the order's text. ARM M and ARM D are
checked line by line against `WORK_ORDER.md` section 4, and ARM M+ differs
from ARM M by exactly the one sentence D adds, in D's position.

*Falsifier:* any prompt line absent from the order, or an M+/M diff of more
than one line. *Status:* SUPPORTED; asserted in the selftest.

---

**APM_002.** The scorer is mechanical and both verdict directions are
reachable, stated per claim and per world (restated under WORK_ORDER_2 W6;
the first form said "no claim is CONSTANT_SILENT" and named AP-1 and AP-3
as the only two shown both ways, which undercounted — AP-5 REFUTED was
already reachable on the confound world). On the three constructed worlds:

```
claim  SUPPORTED at both ends   REFUTED at both ends      BAND
AP-1   —                        confound, refute          main (floor SUPPORTED, ceiling REFUTED)
AP-2   main, confound           refute [mp-01, 0, 0]      —
AP-3   main                     confound, refute (tie)    —
AP-4   confound                 refute (B superset)       —
AP-5   —                        —                         confound (floor REFUTED, ceiling SUPPORTED)
AP-6   —                        refute [constructed-b]    —   (UNRUN below two families)
```

N2 CLEAN on main, FIRES on confound and refute; N3 SILENT on main, FIRES on
confound; N4 FIRES on main; N5 SILENT everywhere with the form-ok rate
printed. What is NOT shown: AP-5 SUPPORTED at both ends (no world carries a
C row that returns only transforms under both rules) and AP-6 SUPPORTED
(two families that both separate D from M); both branches exist in the
code and no fixture reaches them, stated rather than fixtured, since a
fourth authored world would be written to the claim.

*Falsifier:* a claim or null that returns one value on every world.
*Status:* SUPPORTED on the fixtures, with the two unreached directions
named.

---

**APM_003.** The order's AP-2 refutation condition ("any case where
D <= M") is fired by the control the order itself requires, since on a case
whose native IS the decision measurand D == M == 0 is the correct reading.
Controls are therefore excluded from AP-2, AP-3 and AP-6 and named in the
output, and scored under N2 instead.

*Falsifier:* a reading of section 7 under which a control's D == M refutes
AP-2 without making the required control a guaranteed refuter. *Status:*
SUPPORTED; `[CHOICE 6]`, recorded rather than smoothed.

---

**APM_004.** The transform list does the work (the order's N4): under the
primary list the main world's M arms carry 0 crossings on every case, and
under a list that differs by one declared move (concentration, density and
threshold words become measurand vocabulary) three of them carry 1.

*Falsifier:* the two lists agreeing on every scored row. *Status:*
SUPPORTED; N4 FIRES on the main world with the disagreeing rows listed.

---

**APM_005.** The grouping rule needed a clause the order's prose does not
state. A plain subset rule let a one-token native (`{polymer}`) absorb
`polymer-specific hazard` and `migration of polymer from packaging`, reading
two of mp-01's five D-arm crossings as native. The rule now admits a subset
only when the larger core's extra tokens are unclassified residue; an extra
token that is measurand vocabulary is a different quantity.

*Falsifier:* a pair of quantities the order's own examples call different
that the rule groups, or the reverse. *Status:* SUPPORTED on the examples in
the selftest; the first draft's grouping is recorded here rather than
deleted, since it is the failure the clause exists for.

---

**APM_006.** A disjunctive native (`count OR mass`) names two measurands,
and subtracting a 0/1 `native_hit` reads an M response on both as one
crossing. `crossing_count` subtracts the number of native groups hit;
the order's arithmetic is printed beside it as `cc_order`.

*Falsifier:* a reading of section 6 under which `particle count` and
`polymer mass` are one measurand. *Status:* SUPPORTED; `[CHOICE 3]`.

---

**APM_007.** The control case is required by section 8, not supplied by the
order, and is model-authored here — which is exactly what section 3 says
produced defective sets four times. It is landed as CONSTRUCTED with that
caveat and a decision string that names no unit or measurand (asserted).

*Falsifier:* the operator's hand-built control replacing it. *Status:* OPEN.

---

**APM_008.** Arms B and C have no verbatim text in the order and are not
reconstructed; AP-4 and AP-5 are evaluated only on operator-supplied rows
and read UNRUN otherwise. AP-6 reads UNRUN below two model families.

*Falsifier:* none needed; a state. *Status:* SUPPORTED on the fixtures
(UNRUN on the main world, evaluated on the confound world's B and C rows).

---

**APM_009.** The scorer counts a quantity the method MEASURES but does not
REPORT (bulk density in sc-01) as a crossing, because section 6's rule is
about identity of quantities and bulk density is not a transform of SOC.
An M-arm entry whose `quantity:` is bulk density refutes AP-1 under this
scorer. Recorded as a limit of the order's arithmetic, not repaired.

*Falsifier:* a section-6 reading that exempts auxiliary measured
quantities. *Status:* OPEN.

---

**APM_010.** UNVERIFIED. Nothing here bears on AP-1..AP-6 for any model:
no response in the folder came from one, the prior run's numbers in
section 2 are carried, and the lexicon is hand-built to three cases and has
no external validation — the order's own weak joint, unchanged.

*Falsifier:* cold runs on real models, logged into `responses.jsonl`.
*Status:* UNVERIFIED.

---

**APM_011.** A second, independent build of the same order —
`anchor-measurand-crossing/`, from another session, PR #68 — landed on
`main` while this one was being built. The two delivered orders are
byte-identical modulo a trailing newline (checked in the selftest when the
sibling is present), the two transcribed cases are identical on every field,
and the two builds **converged on the same construction where the order left
it open**: both chose lead action-level compliance as the required control,
both named it `ctl-01`, and both defaulted the M+ sentence to D's position
after the claim+method block. The controls differ in decision string and
method text. Neither build is merged into the other, per the repository's
standing arrangement for parallel builds (`frame-instruments/` and the
`framework-instruments` repository). The convergence is **not** independent
confirmation of any choice: same builder class, same corpus, same order —
`triad-playground` `TP_003`'s shared-bias shape, so two builds agreeing on
the lead case is one reading taken twice. Where they diverge is the
information: the sibling scores a crossing **band** with `UNGROUPED` widening
it and holds the control as a candidate the loader excludes; this build
scores a point count with `unknown` tokens printed and admits the control
while excluding it from the paired claims. Both find the bulk-density class
(`AMC_004` / `APM_009`).

*Falsifier:* the two orders differing, or the sibling folder absent from
`main`. *Status:* SUPPORTED; recorded, not merged.

---

**APM_012 (W1).** An empty response is ABSENT, not zero. `normalize.score()`
on no quantities now returns `None` on every crossing field (`crossing_count`,
`crossing_count_max`, `crossing_count_order`) with `absent: True`; every
comparison in `claims()` and `nulls()` skips a `None` and counts it, the
report prints ABSENT per arm, and an arm above 20% ABSENT carries an N-W1
line and is not dropped. Before this only the standalone `crossing_count()`
returned `None` (the known-answer case), while the scored path read a blank
M row as 0 crossings toward AP-1 and a blank D row as `D <= M`, refuting
AP-2. Both are asserted the other way now: a blank M row leaves AP-1 UNRUN
with `absent: 1`; the refute world's blank D row is `absent_pairs: 1` on
AP-2 and refutes nothing.

*Falsifier:* a blank row moving any verdict. *Status:* SUPPORTED;
`[CHOICE 12]`.

---

**APM_013 (W2).** AP-3 is evaluated only on (case, model) triples where
`cc(D) > cc(M)` — where D produced no more crossings than M there is no
D-level for M+ to reach, and a D = M = M+ = 0 world read REFUTED under the
delivered scorer. Such a world now reads UNRUN with the triple listed as
uninformative (`cc(D)=0 <= cc(M)=0`), asserted. `D_LEVEL` was printed in
the header and never read; it is now the comparison, and flipping it to
`gt` moves the refute world's tie (`mp-01`, M+ 5 against D 5) from REFUTED
to SUPPORTED, asserted, so the constant is a live choice and not a label.

*Falsifier:* an uninformative triple counted, or `D_LEVEL` changing
nothing. *Status:* SUPPORTED; `[CHOICE 5]`, `[CHOICE 11]`.

---

**APM_014 (W3).** Every list is scored twice: unknown tokens as residue
(the floor, `crossing_count`) and as measurand vocabulary (the ceiling,
`crossing_count_max`). A claim is SUPPORTED or REFUTED only when both ends
agree, else BAND with both ends printed. The order's known case holds:
`soc yield` against the SOC native is native at the floor and a crossing at
the ceiling (0 / 1). **N-W3 fired on the delivered main world**, and is
reported as the result rather than smoothed: AP-1 is BAND there, SUPPORTED
at the floor and REFUTED at the ceiling, because `sc-01`'s M response
carries `fixed`, `dry`, `combustion` and `ctl-01`'s M carries `after`,
`hour`, `six` — all outside the alias vocabulary, all absorbed into the
native group under the residue rule. The confound world's AP-5 is BAND the
other way (REFUTED at the floor, SUPPORTED at the ceiling: the C row's
`daily intake dose` reaches the supplied `dose` only when `daily` and
`intake` are residue). Both are recorded in `samples/*.before_after.diff`.
The band is the sibling build's form (`AMC_002`) arriving here by a
different route.

*Falsifier:* a quantity the two rules score alike that a reader calls
undecided, or the reverse. *Status:* SUPPORTED; `[CHOICE 9]`.

---

**APM_015 (W4).** Replicate rows per (case, model, arm) were kept in the
table and lost from the claims — `idx.setdefault` held the first row. Every
row is now kept; paired claims run on every pair (`[CHOICE 10]`, all pairs
rather than a per-cell mean, so a replicate that disagrees is visible as a
pair and not averaged away); collisions are counted and printed. The refute
world carries two D rows on one cell and reports `collisions: 1`, AP-2 on
five pairs.

*Falsifier:* a replicate row absent from any pair count. *Status:*
SUPPORTED.

---

**APM_016 (W5).** AP-4 compared raw lowercase quantity strings, so a
reworded superset never registered and the claim was near-constant
SUPPORTED. It now compares sets of measurand GROUPS: `measurand_sets()`
groups the union of the B and M lists once and returns the group ids each
reaches. The direction was checked against `WORK_ORDER.md` section 7
before the change and holds — AP-4 is REFUTED by a cued follow-up that is a
strict superset of its uncued predecessor. On the refute world a B row that
restates M through aliases and transform markers and adds `bulk density of
each core` reads REFUTED with that quantity named; two transforms of one
measurand read as one group, asserted.

*Falsifier:* a reworded superset scoring SUPPORTED. *Status:* SUPPORTED.

---

**APM_017 (W6).** Recorded under the provenance RULE, since W6 touches
`fixtures/*`, which the order marks UNSEEN: the item's defect line says
both directions were shown for "AP-1, AP-3 only", and the delivered
confound world already reached AP-5 REFUTED (the C row) and AP-4
SUPPORTED — so the count was three claims with a REFUTED branch, not two,
and the missing directions were AP-2 REFUTED, AP-4 REFUTED and AP-6
REFUTED. The item's FIX was applied to those three:
`fixtures/responses.refute.constructed.jsonl` is a third authored world
where a second family's D reads native only on `mp-01` (AP-2 and AP-6
REFUTED), a B row is a reworded superset (AP-4 REFUTED), M+ ties D
(the `D_LEVEL` case), one D row is blank (ABSENT) and one cell holds two D
rows (a collision). `APM_002` is restated per claim and per world above,
with the two directions still unreached named.

*Falsifier:* none needed; a correction to the order's own count, applied
in the direction it asked for. *Status:* SUPPORTED.

---

**APM_018 (W7).** One CHOICE registry. The order's inventory was right as
far as it went — `FORM_FLOOR` was `[CHOICE 3]` in `score.py` and `[CHOICE
4]` in the README, `D_LEVEL` 4 against 5, the crossing arithmetic 3 in the
README only — and it undercounted by one collision and one unnumbered
choice: `[CHOICE 5]` was the continuation-line rule in `score.py` and
`D_LEVEL` in the README, and `normalize.py` carried two bare `[CHOICE]`
marks (the parenthetical strip, and the native-groups arithmetic that the
README numbered 3). All twelve now live in `score.CHOICES`, the report
header prints every entry, the README cites by id, and the selftest asserts
the header carries ids 1..12 with no gap. Two FLAGS sit beside them,
printed ON/off in the same header.

*Falsifier:* a `[CHOICE n]` in any file of this folder absent from the
registry. *Status:* SUPPORTED.

---

**APM_019 (W8).** The decision-string guard used substring `find`, so
`count` fired inside `account` and `ug` inside `drug`, and `tonnes`, `kg`,
`ha` were not on its list at all. `normalize.names_unit_or_measurand()` is
token-level, reads the unit list from `transforms.json` (`units`), singular
and plural, plus the listed measurand words; `account`, `county`, `drug`
are silent and `tonnes`, `kg`, `ha` fire, asserted. A word list still
decides word sense (`nonidentity-census` T1-1), stated at the function.

*Falsifier:* a unit in `transforms.json` the guard misses, or a common
word it fires on. *Status:* SUPPORTED.

---

**APM_020 (W9, ORDER — OPEN).** ARM M and ARM D differ in anchor AND in
output schema: M's has a `set:` slot and glosses `quantity` as *what is
being measured*, D's has `measured_by_method`. M+ holds M's schema, so it
cannot separate anchor from form. Behind `--arm-md` (default off) ARM M_D
is M's question with D's three-field schema and no decision, built from the
two templates rather than typed: the selftest asserts M_D's non-field lines
are M's line for line and its fields are D's, `prompts.py --arm-md` emits
`<case>.M_D.txt` and puts M_D into the seeded order, and the scorer parses
an M_D row in D form only when the flag is on (refused otherwise). The
reading per (case, model): M_D ~ D → the schema carries the effect; M_D ~ M
→ the anchor survives the schema control; with the flag off every report
carries N-W9, *the AP-3 finding stays "anchor OR schema"*. **The
2026-09-09 A-vs-D result in `WORK_ORDER.md` section 2 carries this
confound**: PASS A and PASS D differed in anchor and in schema together, so
its 0-against-11 crossings is a difference between two prompts and not yet
between two anchors.

*Falsifier:* the operator signing the arm, after which it is a delivered
arm and this entry closes; or a reading of the order under which M+ already
controls the schema. *Status:* OPEN, flagged.

---

**APM_021 (W10, ORDER — OPEN).** PREDICTION from the order: D's clause
*repeat the three fields for every other quantity* pushes a second entry on
a control, which N2 reads as a gap. Behind `--n2-first` (default off) N2 is
read on entry 1 of a control D response only and entries 2..n are reported
as `N2_rest`. On the refute world's control (one correct entry, one
spurious) the delivered rule FIRES and the flagged rule reads `N2_first
CLEAN` with `N2_rest [["ctl-01", 1, ["no"]]]`, asserted. That is the
prediction reached on a control written to it and says nothing about
whether a model does this; N-W10 fires only if `N2_first` itself fires on a
real control, which would read as D over-flagging independent of
enumeration.

*Falsifier:* the operator signing the rule; or a real control on which
`N2_first` fires. *Status:* OPEN, flagged.

---

**APM_022 (W11).** A free second instrument: every D-form row carries the
model's own `measured_by_method` label and the scorer computes native
membership of the same quantity, so agreement per entry is printable —
`yes` on a native quantity or `no` on a non-native one agrees, the reverse
disagrees, `partial` is its own bucket. Reported per case with a rate;
gates nothing. On the main world no D entry disagrees with the scorer (partials
reported apart), which is a property of fixtures authored against the
lexicon.

*Falsifier:* none needed; a readout. *Status:* SUPPORTED.

---

**APM_023 (sibling check, WORK_ORDER_2 §3).** `../anchor-measurand-crossing/`
read only, not edited, not merged. For each of W1–W5, does the sibling
carry the same defect class?

```
item  sibling   where
W1    absent    an empty response is `malformed` and filtered before scoring
W2    same      `mp[0] >= d[0]` reads a (0, 0) triple as M+ reaching D-level → REFUTED
W3    absent    an unmatched quantity is UNGROUPED and widens a band
W4    absent    all rows per cell are paired
W5    absent    AP-4 compares (measurand, normalized set) pairs, not strings
```

The one shared defect is the one the sibling's own design did not
anticipate (its band and its UNGROUPED handling are exactly W3's repair
arrived at independently); it is recorded here and left there, per the
order's READ ONLY.

*Falsifier:* a sibling row that behaves otherwise. *Status:* SUPPORTED;
read from the sibling's `amc.py`.
