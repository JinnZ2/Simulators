# falsifier-survey

Filed as delivered, 2026-09-05. Instructions for what to do with it are
pending; nothing here has been audited, re-run, or edited. This README is
the only file in the folder not from the drop.

## What arrived, and where it now lives

One zip (`OKComputer_Simulators____falsifier___.zip`, 42 files, 6.4 MB
text) carrying two runs of a falsifier survey under "ADDENDUM 01" (the
adjusted admissibility rule: MEASURED needs quantity + units + how
obtained; SCOPE-DIFFERENT needs reference / maps_to / breaks_at; MISSING
and UNKNOWN emitted explicitly), plus a blind taxonomy sort of the
SCOPE-DIFFERENT transforms.

The whole zip was first filed here (commit `5e81b9d`). Run 2 turned out to
be about two other repositories, so it was split out by the `repo` field
every Run 2 record carries and moved to `falsifier-survey/` in
`Geometric-manifold-` (109 cells) and
`Geometric-to-Binary-Computational-Bridge` (514 cells). The combined Run 2
files as delivered remain in this repo's history at that commit. What
stays here is Run 1, which is about this repository:

```
plan.md                            the orchestrator's plan, BOTH runs (kept
                                   here as the run's root document)
falsifier_survey_report.md         Run 1: this repo, 127 folders, 1765 cells
cell_records.{jsonl,csv}           one row per Run 1 cell
survey/                            Run 1 working set: folder list, extraction
                                   mention list, 8 coder batches, the hit
                                   slice each coder received, validator
```

## What was not checked in

`falsifier_survey_bundle.zip` (1,060,869 bytes, sha256
`f271f4d15ea3a0982084c553931251e815300164271b3be0a5a18f7e6776495d`) was
inside the drop. Extracted and compared: its 30 files are byte-identical
to the same-named files landed here, and it carries nothing the outer set
lacks (the 11 `*_hits.jsonl` files exist only outside it). A binary
duplicate of text already in the tree is not landed; the hash is recorded
so a re-obtained copy can be checked against it (the
`notes/datasets/uploads_2026_08_25.md` arrangement).

## Provenance notes, not findings

- `survey/validate.py` carries absolute paths from the machine
  that ran it (`/mnt/agents/output/...`). Left as delivered.
- Both reports date their run 2026-09-05 against a fresh clone of HEAD.
  Which commit is not recorded in the drop.
- Run 1 excludes `docs/`, `notes/`, `legacy/`, `tests/`, `tools/` as
  meta-directories. Run 2 (now in the other two repos) includes `docs/`.
  The plan states both.
- Coding is from reading, not execution: the Run 1 report says so under
  "Deviations and limitations". Nothing in either report was re-derived
  here.
