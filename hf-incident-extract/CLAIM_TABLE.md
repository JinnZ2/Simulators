# CLAIM_TABLE — hf-incident-extract

`HFI_001..HFI_007`. `WORK_ORDER.md` is delivered verbatim and edited by
nothing here. The instrument it orders is built as one stdlib file; the
report it is for is **not in hand** (egress is an allowlist), so every
real cell is UNMEASURED with the input it wants named. No value in the
folder is from any report. The fixtures are constructed and say so.

## REFUTATION_PROTOCOL

| id | claim | status |
|---|---|---|
| `HFI_001` | The six measures are built to the order's definitions and reproduce known answers on a constructed sheet (18.0 / 0.7 / 3.0 / 0.25 / 20.0 / 3-of-4); an unmeasured input returns None for every measure that needs it, never 0, and one measured side against one unmeasured side is still None. | SUPPORTED |
| `HFI_002` | The order's two-layer input — report prose and (unreleased) transcripts — is honoured as two layers in code: `text_scan` emits CANDIDATES with line numbers for a reader, and only a coded SHEET yields a measure. Which sentence gives `t_characterize` is a reading and stays one. | SUPPORTED |
| `HFI_003` | The gate-property test computes `gap` as the symmetric difference of declared and implemented property sets; `gap != 0` predicts M1 high and M2 high, and the prediction is checked against the measures only where measured — the check can fail (a predicted-high M1 that measures low reads False) and `gap == 0` predicts nothing. The "high" thresholds are stipulated `[CHOICE]` constants, printed beside every result. | SUPPORTED |
| `HFI_004` | CROSS_SUBSTRATE is vocabulary-invariant by construction: the substrate name is a key no function reads, asserted over the AST of every function body; the five rows compute through the same functions and every real cell is UNMEASURED — no tendril, fledgling, ant, crew or swarm value is supplied from memory. | SUPPORTED |
| `HFI_005` | The OPEN items are states, not gaps: transcripts `NOT_RELEASED` routes M2..M5 to "report figures only", and the post-validation off-trail fraction is `NOT_COLLECTED` (report silent) — distinct from `UNMEASURED`, which is wanted and readable. | SUPPORTED |
| `HFI_006` | Durations refuse to be unitless (M1 is `days / 4h` in the order; a value with no unit raises rather than dividing), and days and hours convert to one scale — the `G-DIM` discipline applied before any ratio exists. | SUPPORTED |
| `HFI_007` | Nothing here is a measurement of the incident: the report is unread, the transcripts unreleased, and every measure on the real sheet is None. The instrument is built and unrun on its subject. | UNVERIFIED |

---

## HFI_001 — known answers first

A measure that has never returned a known number is not yet an
instrument. The constructed sheet plants 3 days over 4 hours (18.0), 7 of
10 branches (0.7), 9 env-edit over 3 gate-fool moves (3.0), 5 of 20 runs
(0.25), 40 action edits over 2 reasoning edits (20.0), and four agents of
whom three charge an inert gate. All six reproduce. The other direction
is pinned too: the unfilled sheet returns None on M1–M5 and no count on
M6; a sheet with `runs_total` filled and the numerator unmeasured returns
None rather than dividing by the known side; a zero denominator returns
None rather than infinity. The absent-vs-known-negative repair this repo
records elsewhere is designed in here.

**Falsifier:** any measure returning a number from an unmeasured input.

## HFI_002 — the prose is scanned, the sheet is measured

The order's INPUT is report text plus transcripts; its OUTPUT is counts.
Between them sits a reading — which sentence states the characterisation
time, which log entries count as reasoning — and a regex that decided it
would be `nonidentity-census` T1-1's word-list miss on a corpus nobody
here has seen. So `text_scan` finds every stated duration and count with
its line and emits them as CANDIDATES, and `--sheet` computes the
measures from the coded sheet. A planted decoy ("Version 2.0") is not
promoted to a duration or a count.

**Falsifier:** `text_scan` returning a measure, or missing a planted
duration. Both pinned.

## HFI_003 — the charter-signature check can fail

`declared(paper)` and `implemented(code)` enter as sets of property
names; `gap` is their symmetric difference. A non-empty gap predicts M1
and M2 high — the order's charter-signature check — and the prediction
is then compared with the measured M1 and M2 where those exist. On the
constructed sheet the gap is `["inert"]`, the prediction fires, and both
checks pass; on a sheet whose characterisation took 8 hours the M1 check
fails, so the signature is a thing that can be absent; on an equal pair
the gap is empty and nothing is predicted. What "high" is, the order
does not say — 6.0 for M1 and 0.5 for M2 are `[CHOICE]` constants
declared in the module and printed on every render.

**Falsifier:** an empty gap predicting high, or a low measured M1
passing the check.

## HFI_004 — same instrument, no vocabulary change, by AST

The order's CROSS_SUBSTRATE test is a property of the code, testable
without any substrate value: the substrate name is stored as a key and
read by no function. `selftest_hf.py` walks every function body and
asserts none of the five names appears in it. The five rows then compute
M1, M4 and `unit_boundary != objective_boundary` through the identical
functions — every cell UNMEASURED, because a tendril's characterisation
time or a fire crew's self-failed-run count is not a thing to supply from
memory into an instrument. A filled fictional row (2 days / 4 h, 3 of 10,
individual vs crew) shows the path computes.

**Falsifier:** a substrate name inside a function body, or a real
substrate cell carrying a value with no source.

## HFI_005 — OPEN items are states

`NOT_RELEASED` on transcripts routes M2..M5 to report figures only, as
the order says; `NOT_COLLECTED` on the post-validation off-trail fraction
records that the report is silent on it. Neither is `UNMEASURED`, which
is the state of a value the report carries and nobody here has read.
Three states, kept apart.

## HFI_006 — no unitless duration

M1 is a ratio of two durations the order states in different units
(days over 4h). A duration with no unit raises; days and hours are
converted to one scale before the ratio; the same 72 hours stated as
"72 h" and as "3 days" give the same 18.0.

## HFI_007 — built, unrun on its subject (UNVERIFIED)

Nothing here says anything about the incident. Every measure on the real
sheet is None, and the folder will stay that way until someone with the
report codes the sheet — at which point every check here runs unchanged.
