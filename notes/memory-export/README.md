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
| 1 — exported unchanged | 57 | 0 |
| 2 — scrubbed and exported | 7 | 4 |
| 3 — held back | 12 | 0, and none expected |

Tier 2, landed: `facility-risk-index`, `refusal-false-positive-log`,
`instance-log-index`, `sleep-duration-instrument`. Outstanding:
`idle-shutdown-restart-accounting`, `work-load-ordering`, `recent-work`.

Tier 3 is held back by the manifest's own decision. Its absence is a choice
recorded upstream, not a gap here.

## Cross-refs that do not resolve

The landed files carry seven links by name. One resolves —
`refusal-false-positive-log`, which is itself a landed tier-2 file. The other
six are not in this folder:

`uninstrumented`, `merit-anchoring`, `unnamed-instruments`,
`identity-model-monoculture`, `shape-index`, `cross-model-calibration-toolkit`

Recorded rather than reconstructed — same handling `notes/README.md` gives the
operator catalogue that `operators/D2.md` references and this repo does not
hold.

One name collides: `[[uninstrumented]]` is a memory file, and
`Simulators/uninstrumented/` is a folder in this tree. Whether they are the
same material is not established here, and the link was not repointed.

## The cost, visible in the files

`SCRUB_RULES.md` names three files that pay most for the scrub. Two of the
three have landed and the cost is legible in them: `facility-risk-index` heads
its longest section "Field observation (longitudinal operator report)" with no
observer attached, and `refusal-false-positive-log` reports a rate with, in its
own words, no denominator available to the observer. The reasoning is intact;
the standing behind it is not carried.

CC0.
