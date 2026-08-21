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
