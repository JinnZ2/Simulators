# seam-gaps

Six gaps from one session, 2026-08-31, delivered as WORK ORDER 02.

This is a rendered gap inventory, not a set of findings. Nothing in
this folder claims anything about the world beyond what the delivered
order carries, and every literature fact sits at the status
[`SOURCES.md`](SOURCES.md) records. All six are seam gaps — the order's
own classification: *each sits between two fields whose instruments
code it as the other's problem.*

## Files

- [`WORK_ORDER.md`](WORK_ORDER.md) — the order as delivered, verbatim.
  It arrives with an unterminated code fence around the source
  material; kept as delivered.
- [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) — the six entries, rendered
  per [`../RESEARCH_RENDER.md`](../RESEARCH_RENDER.md). Entries 5 and 6
  are the first worked instances of the DECISION entry type.
- [`SOURCES.md`](SOURCES.md) — per-row status of the source material:
  what arithmetic could check here, what is consistent with the record
  as this environment carried it, what is only carried. Egress
  refusals measured, with timestamps.
- [`verify_sources.py`](verify_sources.py) — the arithmetic, runnable
  (`--selftest`).

## Two readings declared rather than smoothed

**[CHOICE] The blocks are the gaps.** The order announces six gaps
(G-01..G-06) and delivers six source blocks with no per-gap sections.
This render reads the blocks as the gaps, 1:1 in order — supported by
the schema note placing G-05 and G-06 on exactly the two blocks that
are fork-shaped. If the author's own G-list differs, the ids here
yield to it.

**[CHOICE] Placement is noted, not executed.** "Folder placement noted
per gap" is honoured as written: each entry carries a **Placement**
line naming a destination folder with the reason, and nothing was
inserted anywhere. Inserting these into existing folders means editing
delivered documents, and the placements are this render's call rather
than the author's. Moving any entry to its noted folder is one
operation once the author says so. The notes, for scanning:

| entry | noted placement | why |
|---|---|---|
| 1 (G-01) | `question-availability/` | QA_005's half-life instrument is the consumer; the alternative is `term-drift-citation/` |
| 2 (G-02) | `instrument-epistemology/` | a detection floor per instrument is its subject |
| 3 (G-03) | `category-weld/` | the deliverable is a `welds/` entry — the register's first cross-field candidate |
| 4 (G-04) | `proxy-investigation-lab/` | richness → traits → function is a gradeable proxy chain |
| 5 (G-05) | `climate-modeling/` | `StationarityAudit` is this fork's subject in runnable form |
| 6 (G-06) | `instrument-epistemology/` | the discriminator is a triangulation-order question |

## What was checked

The order says *verify before rendering*. Verification reached exactly
as far as `SOURCES.md` states: every publisher host refuses CONNECT
through this environment's egress allowlist (measured), the
load-bearing dates are past this environment's knowledge horizon, so
the checks that ran are internal — the biomass partition closes, the
delivered animal components exceed their own stated total by 0.27
(consistent only at one significant figure; recorded, not
adjudicated), and the SILENT re-read of the radar null is conditional
arithmetic on two carried numbers. `verify_sources.py` computes all of
it.

## Held sibling material

A marker file from the same session sits at
`notes/markers/HELD_2026_08_31.md` — five held items (M-A..M-E) plus
draft G-07/G-08, deliberately NOT rendered, each with its own hold
reason. It cites "G-01's detection floor", which in this render is
entry 2 (G-02) — the first live evidence bearing on the blocks-are-gaps
[CHOICE] above; the ids here yield to the author's list per that
choice, and `notes/check_markers.py` records both readings without
picking. WORK ORDER 03 has since rendered the cluster into
`uninstrumented/` — mechanism first, instances under it — filing G-07
and G-08 there; nothing from it enters this folder, and its own G-01
cross-reference confirms the yield rule's premise a second time (the
author's G-01 is this render's G-02).

CC0.
