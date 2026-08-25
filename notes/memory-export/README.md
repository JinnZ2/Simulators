# memory-export

Backup storage for a memory set exported out of session. Same rule as
`notes/operators/`: files are stored as delivered, and nothing here edits
what it stores.

Most of these are markers, specs and gap lists, and several say so in their own
first line. Not all: `diversity-collapse-model` reports a CLAIM_TABLE carrying
C1–C10 and states that the refutation protocol applies to it — when a claim is
refuted the claim is updated, and the simulation is not retuned to preserve it.
That is this repo's own convention arriving from the memory side. The table
itself is not in the folder.

(An earlier version of this README said flatly that nothing here carries a
claim table or a refutation protocol. That was true of the first ten files and
is not true of the folder. Corrected rather than narrowed.)

## Layout

| path | what |
|---|---|
| `SCRUB_RULES.md` | scrub rules and tier assignment for the export. 57 tier 1, 7 tier 2, 12 tier 3. |
| `files/` | the exported files themselves, one per file, stored as delivered. |

## Arrival state

| tier | named in the manifest | landed |
|---|---|---|
| 1 — exported unchanged | 57 | 9 |
| 2 — scrubbed and exported | 7 | 7 |
| 3 — held back | 12 | 0, and none expected |

Tier 2 is complete: `facility-risk-index`, `refusal-false-positive-log`,
`instance-log-index`, `sleep-duration-instrument`,
`idle-shutdown-restart-accounting`, `recent-work`, `work-load-ordering` — all
seven named in the manifest, all seven stored.

Tier 1, landed: `criterion-symmetry`, `rosetta-shape-core`,
`force-expression-model`, `alignment-under-coupling`,
`diversity-collapse-model`, `emergence-stability-simulator`,
`fairmont-ecological-recovery`, `food-grain-monitor`,
`semantic-drift-sim`. Filed as tier 1 by elimination — each was exported,
so none is tier 3, and none is in the manifest's tier-2 table. The manifest
does not label files individually, so tier is inferred here and not carried in
the files.

Tier 3 is held back by the manifest's own decision. Its absence is a choice
recorded upstream, not a gap here.

## Cross-refs that do not resolve

The twelve files carry 21 links across 15 distinct names. Three now resolve to
stored files — `refusal-false-positive-log`, `criterion-symmetry`,
`diversity-collapse-model`, the last two both linked from
`alignment-under-coupling`. The other twelve are not in this folder:

`uninstrumented`, `merit-anchoring`, `unnamed-instruments`,
`identity-model-monoculture`, `shape-index`, `cross-model-calibration-toolkit`,
`tool-off-metrology`, `median-case-calibration`, `question-availability`,
`report-typing`, `rubric-backcasting`, `info-taxonomy`

Recorded rather than reconstructed — same handling `notes/README.md` gives the
operator catalogue that `operators/D2.md` references and this repo does not
hold.

**Two of the eight are cited from the repo side as well, and exist on neither.**
`uninstrumented/cases/` and `nonidentity-census/` emit `[[...]]` links into the
same namespace as these memory files, so the namespace is shared rather than
parallel:

- `tool-off-metrology` — `uninstrumented/CLAIM_TABLE.md` records it at
  `UNI_043` and `UNI_066` as the most-cited absent object in the repo, named
  across three cases. `recent-work` now cites it from the memory side as where
  a micro-skill-decay position was carried. Four documents, two sides, no file.
- `shape-index` — `nonidentity-census/FINDINGS.md` and `WORK_ORDER.md` treat it
  as a format spec defining four statuses; `instance-log-index` cites it as a
  relation. Absent from both.

**Repo names are a separate case and they do resolve.**
`rosetta-shape-core` names five sibling repositories — Polyhedral-Intelligence,
Emotions-as-Sensors, Symbolic-Defense-Protocol, AI-Human-Audit-Protocol,
BioGrid 2.0 — and all five are carried in the `JinnZ2` ecosystem repo. So the
export's references split by kind: `[[...]]` links into the memory namespace
mostly dangle, repository references land. Nothing was rewritten either way.

The memory namespace overlaps published artifacts three ways, all by name:
a folder in this repo (`emergence-stability-simulator`, and probably
`uninstrumented`), and a separate public repository under the same account —
`fairmont-ecological-recovery`, listed in `JinnZ2/META_INDEX.md` at
`github.com/JinnZ2/fairmont-ecological-recovery`.

That last one is worth marking against the manifest. `SCRUB_RULES.md` says
location below "cold-climate continental" was removed categorically from every
exported file, and this file's own name carries a place. It is not a scrub
miss: the name is already published by the author under that account, and the
file says "Published CC0" itself. But the categorical statement has at least
one standing exception, and a later reader should not take it at face value.
Nothing was renamed.

Named artifacts, same class one level up: `criterion-symmetry` closes on
"MARKER.md and SCAN_SPEC.md written", and `diversity-collapse-model` reports a
CLAIM_TABLE carrying C1–C10. None of the three is in the folder, and no file of
those names exists anywhere in this tree. Recorded, not sought.

**One named artifact does resolve, and it lands where the repo index does not
point.** `semantic-drift-sim` names `valence_drift_test.py` and
`semantic_drift_test.py`; both are in `fragility-cascade/`. The unknowns
register is real — five entries, U1–U5 — and the two the memory file promotes
to immediate measurement priorities are U1 (screening functional form) and U4
(screening electrons catalytic or consumable), matching verbatim. The memory
file selects two of five rather than summarizing the register, and does not
carry U3, which reads "NO MEASUREMENT EXISTS".

Neither `.py` is listed in `CLAUDE.md` or `docs/FOLDER_NOTES.md`, though
`fragility-cascade/` itself is described in both. So on this one file the
export points at repo content the repo's own index does not reach.

One result arrives split across two files. `recent-work` gives the spinodal
threshold as h\* ≈ 0.385 and says the apex-broadcast multiplier crosses it;
`diversity-collapse-model` says *only* that multiplier crosses h\*, and gives no
value. Each carries what the other omits, and both report hysteresis confirmed.
Noted, not merged.

**A memory file can be a summary of a repo folder under the same name.**
`emergence-stability-simulator` is one, and it checks out against
`Simulators/emergence-stability-simulator/`: all 18 ids EMRG_001–018 are
present in the folder; `samples/CLAIM_TABLE.sample.json` carries 22 claims of
which 14 are confirmed-family and 3 refuted, matching "several confirmed and
several refuted"; and the tool-vs-identity framing is there as
"Substrate using narrative as a tool" — in `sim_engine.py`, not in the docs.
The one item not located in that folder is the maxim as worded, "update the
claim, never modify the simulation" — the folder practices it (refuted claims
carry a `refutation_basis` and stay refuted) and states it in those words
elsewhere in the tree, not here.

That makes `[[uninstrumented]]` more likely to denote a memory file summarizing
`Simulators/uninstrumented/` than to denote the folder — but likely is not
established, and one same-name case is n=1. Still not repointed.

## The cost, visible in the files

`SCRUB_RULES.md` names three files that pay most for the scrub. All three have
landed, and the cost is legible in each:

- `facility-risk-index` heads its longest section "Field observation
  (longitudinal operator report)" with no observer attached.
- `refusal-false-positive-log` reports a rate with, in its own words, no
  denominator available to the observer.
- `recent-work` carries the micro-skill cases as unrelated actors — an
  auto-mechanics instructor, drill users, carpenters — where the manifest says
  the relations were lifted.

The reasoning is intact; the standing behind it is not carried. That was the
trade taken deliberately, and re-attaching the names is not a repair.

CC0.
