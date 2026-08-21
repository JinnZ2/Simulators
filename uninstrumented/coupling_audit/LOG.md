<!--
SPDX-License-Identifier: CC0-1.0
To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this file.
-->

# LOG

The parent register carries no log file, so this one is local to the
subfolder. Nothing in the parent was restructured or renamed to make room for
it.

## 2026-08-21 — subfolder created

**Added as a subfolder, not as a repo.** It sits alongside the existing
exclusion-mechanism material in `uninstrumented/` rather than beside it at the
repo root. **To be promoted to its own folder only if the entry count grows** —
three entries is a marker, and a marker that never gains a fourth entry should
stay where it is rather than acquire the surface area of a project.

**The audit was run against three models with three hits before the schema was
written.** That ordering is recorded because it bears on how the corpus should
be read: the fields, the verdict labels and the gate vocabulary were derived
from three cases that had already come back positive. `FALSIFIER.md` states
the consequence — a corpus assembled after a hypothesis, by the party holding
it, is not evidence about a base rate. Three cases, not a survey.

**Gate types checked against the parent register's eight mechanisms**, by
importing them rather than copying them (`audit.parent_mechanisms()`). One
gate type — `species` — matches `AUDIT_ASYMMETRY` strongly, so **no candidate
ninth mechanism is claimed**. The other two matches are recorded as PARTIAL
and left unresolved. Separately, the ordinal is already taken: `MECHANISM_09`,
`MECHANISM_10` and `MECHANISM_11` exist as proposals in sibling folders
against the same register of eight.

**One schema addition beyond the specified field list:** `agents_coupled`.
Without it the verdict can only be *declared* by the entry, never *derived*
from the fields, and an entry that declares its own verdict cannot disagree
with itself. `score()` now derives the verdict and reports agreement with the
declared one; on the three seed entries they agree. The addition is what makes
`PRESENT_FIXED` distinguishable from `ABSENT_*` at all — the per-capita carbon
footprint entry is represented-but-uncoupled, which is a state the original
three-set schema could not express.

**Cross-reference added in the parent's `AUDIT_NOTES.md`** rather than in its
`README.md`, since the README is delivered material and the audit notes are
not.

## 2026-08-21 — `provisioning.py` added; OPEN.md items 6 and 6a

Delivered material naming the anthropological/archaeological precedent
(`PROVISIONING REGIME`) landed verbatim as `OPEN.md` item 6, including its own
status line: *not searched to exhaustion; do not record as absent from the
literature — record as not found in one pass.*

`provisioning.py` implements what the delivered material points at: the
discriminating test between `MOBILITY`, `BREED_OR_STATUS` and
`VARIABLE_COUPLING`, plus intra-tooth amplitude as a coupling-strength unit.

**The finding is about the tissue, not about the past.** The within-individual
axis is the only one separating the coupling hypothesis from the other two,
and bone collagen — where most of the delivered dog evidence sits — averages
years, so that axis is destroyed before sampling. G-RES: 12.2× too coarse for
a seasonal feature at a margin of 2. In that tissue the coupling hypothesis
cannot fail, which is `CONSTANT_SILENT` rather than support.

On four delivered cases: 2 blind by tissue, **4 of 4 never tested the standing
explanation against the coupling hypothesis**, 2 carrying a same-site wild
control. Two hypotheses fitting one observation is recorded as a field
(`also_fits`) rather than as agreement.

**One ambiguity left open rather than resolved.** The delivered text reads
"n=35 dogs, plus dentine n=4", which reads either as a subset or as
additional. Both denominators are reported and neither is picked — a share on
an ambiguous denominator is the failure this folder audits for. The two
readings differ by under a percentage point, which is why it can be left open.

**One caveat enforced rather than noted.** `amplitude_reading()` raises
`GeometryNotDeclared` without a stated sampling geometry, because dentine
geometry changes the intra-tooth pattern. Amplitude thresholds are
conventional, scaled to one delivered herd range, and explicitly not
calibrated here.

Nothing in `audit.py` or `entries.py` was modified. The entries' `Y/N`
coupling field is unchanged; `provisioning.py` supplies a unit alongside it
rather than replacing it, since the unit exists only for cases with an
incremental tissue.

## 2026-08-21 — canonical `OPEN.md` sections 6–10; amplitude replaces the boolean

A cleaner version of the anthropology/archaeology material was delivered and
**supersedes** the one-search version landed earlier the same day. Items 6–10
are the delivered text as written. Differences that mattered:

- **two searches, not one** — the status line changed, and the reverse
  direction is now recorded as *"open, and possibly ahead of the record. Not a
  finding."*
- the zooarchaeology name is supplied: **foddering / seasonal fodder
  supplementation**. Two literatures, two names, neither framing it as a
  coupling variable applied across species.
- the caveat is sourced to a **2024 *Journal of Archaeological Science***
  paper, not to an unnamed one.
- the instruction is **replaces**, not *supplements*. The previous LOG entry
  recorded the opposite and was wrong: it said the unit "supplies a unit
  alongside [the boolean] rather than replacing it." `coupling_field_for()`
  now implements the replacement for archaeological cases, with the scope
  limit stated — an incremental tissue and a declared geometry are both
  required, `entries.py` keeps the boolean because there is no tooth in a
  national carbon inventory.

**Added to `provisioning.py`:** the Balasse controlled-feeding calibration as
a first-class object (a positive control that exists for caprines and cattle
and not for dogs); `PUBLISHED_APPLICATIONS` (six sites); a fifth case, the
Canine Surrogacy Approach / Hudson Bay Thule systematic offset absorbed as
method caution; and `cross_species_readout()`.

**The one computable thing in the new material**: 6 of 6 published
applications of the method are on commodity species, 0 on companion species,
against a dog sequential n of about 4. That is consistent with the author's
stated explanation and does not establish it — sample availability, tooth size
and enamel thickness, and funding lines are live alternatives, and the readout
says so in the field names (`count_establishes` /
`count_does_not_establish`). What it does establish is that the asymmetry is
real and large.

**Cross-link worth keeping**: this is entry 3's `market_output` gate seen from
the other side. There it keeps companion animals out of the water accounting;
here the same criterion is why the instrument exists for cattle. One line, two
consequences.

Corpus counts moved with the fifth case: 3 of 5 blind by tissue, **5 of 5**
never tested against the coupling hypothesis, 2 of 5 with a same-site wild
control. Selftest 25/25 → 36/36.
