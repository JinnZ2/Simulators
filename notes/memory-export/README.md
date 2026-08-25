# memory-export

Backup storage for a memory set exported out of session. Same rule as
`notes/operators/`: files are stored as delivered, and nothing here edits
what it stores.

Nothing here is a simulator. No claim table, no `REFUTATION_PROTOCOL` — these
are markers, specs and gap lists, and several say so in their own first line.

## Layout

| path | what |
|---|---|
| `SCRUB_RULES.md` | scrub rules and tier assignment for the export. 57 tier 1, 7 tier 2, 12 tier 3. |
| `files/` | the exported files themselves, one per file, stored as delivered. |

## Arrival state

| tier | named in the manifest | landed |
|---|---|---|
| 1 — exported unchanged | 57 | 1 |
| 2 — scrubbed and exported | 7 | 7 |
| 3 — held back | 12 | 0, and none expected |

Tier 2 is complete: `facility-risk-index`, `refusal-false-positive-log`,
`instance-log-index`, `sleep-duration-instrument`,
`idle-shutdown-restart-accounting`, `recent-work`, `work-load-ordering` — all
seven named in the manifest, all seven stored.

Tier 1, landed: `criterion-symmetry`. Filed as tier 1 by elimination — it was
exported, so it is not tier 3, and it is not in the manifest's tier-2 table.
The manifest does not label files individually, so tier is inferred here and
not carried in the file.

Tier 3 is held back by the manifest's own decision. Its absence is a choice
recorded upstream, not a gap here.

## Cross-refs that do not resolve

The eight files carry 17 links across 12 distinct names. One resolves —
`refusal-false-positive-log`, itself a stored file. The other eleven are not in
this folder:

`uninstrumented`, `merit-anchoring`, `unnamed-instruments`,
`identity-model-monoculture`, `shape-index`, `cross-model-calibration-toolkit`,
`tool-off-metrology`, `median-case-calibration`, `question-availability`,
`report-typing`, `rubric-backcasting`

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

Named artifacts, same class one level up: `criterion-symmetry` closes on
"MARKER.md and SCAN_SPEC.md written". Neither filename exists anywhere in this
tree. Recorded, not sought.

`[[uninstrumented]]` stays ambiguous rather than settled: a folder of that name
is in this tree, the memory set has a file of that name, and the shared
namespace makes the collision more likely to matter, not less. The link was not
repointed.

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
