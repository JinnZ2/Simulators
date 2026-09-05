# falsifier-survey

Filed as delivered, 2026-09-05. Instructions for what to do with it are
pending; nothing here has been audited, re-run, or edited. This README is
the only file in the folder not from the drop.

## What arrived

One zip (`OKComputer_Simulators____falsifier___.zip`, 42 files, 6.4 MB
text). Two runs of a falsifier survey under "ADDENDUM 01" (the adjusted
admissibility rule: MEASURED needs quantity + units + how obtained;
SCOPE-DIFFERENT needs reference / maps_to / breaks_at; MISSING and UNKNOWN
emitted explicitly), plus a blind taxonomy sort of the SCOPE-DIFFERENT
transforms.

```
plan.md                            the run plan, both runs
falsifier_survey_report.md         Run 1: this repo, 127 folders, 1765 cells
falsifier_survey_report_run2.md    Run 2: Geometric-manifold- (16 units) and
                                   Geometric-to-Binary-Computational-Bridge
                                   (30 units), 623 cells
cell_records{,_run2}.{jsonl,csv}   one row per cell
survey/                            Run 1 working set: folder list, extraction
                                   mention list, 8 coder batches, validator
survey2/                           Run 2 working set: per-repo folder lists and
                                   mention lists, 3 coder batches, validator
*/batches*/*_hits.jsonl            the extraction slice each coder received
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

- The two `validate*.py` scripts carry absolute paths from the machine
  that ran them (`/mnt/agents/output/...`). Left as delivered.
- Both reports date their run 2026-09-05 against a fresh clone of HEAD.
  Which commit is not recorded in the drop.
- Run 1 excludes `docs/`, `notes/`, `legacy/`, `tests/`, `tools/` as
  meta-directories. Run 2 includes `docs/`. The plan states both.
- Coding is from reading, not execution: the Run 1 report says so under
  "Deviations and limitations". Nothing in either report was re-derived
  here.
