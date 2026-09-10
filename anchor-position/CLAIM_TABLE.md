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
reachable: on one constructed world AP-1/AP-2/AP-3 read SUPPORTED and on a
second AP-1/AP-3/AP-5 read REFUTED, N2 and N3 fire, and a form failure is
counted — so no claim is `CONSTANT_SILENT` and no null `CONSTANT_FIRES`.

*Falsifier:* a claim or null that returns one value on both worlds.
*Status:* SUPPORTED on the fixtures.

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
