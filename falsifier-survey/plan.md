# PLAN — Falsifier survey + taxonomy test over JinnZ2/Simulators

Input: repo clone at /tmp/Simulators (127 survey folders, /tmp/folders.txt)
Rule source: user-pasted ADDENDUM 01 (adjusted admissibility rule + taxonomy test)

## Adjusted rule (from addendum §1) — the coding bar
- MEASURED         → requires MEASURED_AS: quantity + units + how obtained. No units → downgrade.
- SCOPE-DIFFERENT  → requires SCOPE_TRANSFORM: reference / maps_to / breaks_at. Prose note without
                     all three → downgrade to UNKNOWN.
- MISSING          → folder carries no falsifier anywhere. Emitted explicitly.
- UNKNOWN          → falsifier exists but fails its admissibility bar. Emitted explicitly, never silent.
- Report counts SCOPE-DIFFERENT-lacking-complete-transform separately from UNKNOWN (addendum §3).

## Taxonomy test (addendum §2) — hard constraints
- Coders write SCOPE_TRANSFORM only. The candidate kinds (K1 frame / K2 boundary / K3 homonym)
  MUST NOT be shown to coders during coding — sorting must emerge from the transforms.
- Sorting agent derives kinds from the completed transform set; N stated; "one kind" is a result.

## Stage 0 — Mechanical extraction (orchestrator, scripted)
Scan all 127 folders for explicit falsifier material: `Falsifier:` / `Falsifier —` fields in
CLAIM_TABLE.md-style files, standalone FALSIFIER.md, refutation sections, falsifier .py/.json
artifacts. Output: /mnt/agents/output/survey/raw_hits.jsonl  (folder, file, claim_id, raw text).
This guarantees coverage; coders read folder files for context.

## Stage 1 — Coding (8 parallel coder subagents, ~16 folders each)
Each agent receives: adjusted rule (NO kind menu), its folder slice, repo path.
For each folder: one cell per falsifier (or one MISSING cell if none).
Writes /mnt/agents/output/survey/batches/batch_N.jsonl with schema:
  {folder, claim_id, source_file, falsifier_text, status,
   measured_as: {quantity, units, how_obtained} | null,
   scope_transform: {reference, maps_to, breaks_at} | null,
   downgrade_reason | null, notes}
Validation gate: JSONL parses; every folder in slice appears; statuses legal;
MEASURED cells have all 3 measured_as fields; SCOPE-DIFFERENT cells have all 3 transform fields.

## Stage 2 — Taxonomy sort (1 reviewer subagent)
Collect all complete SCOPE_TRANSFORMs. Agent is NOT given K1/K2/K3; it clusters transforms by
what differs (reference body? accounting boundary? the quantity itself?) and proposes a candidate
taxonomy with N stated, plus the "do they sort or stay one thing" verdict.
Cross-check: after kinds are proposed, compare against addendum's named candidates K1/K2/K3 and
report correspondence or divergence.

## Stage 3 — Assembly (orchestrator)
Merge batches → cell_records.jsonl + cell_records.csv. Counts: MEASURED / SCOPE-DIFFERENT /
MISSING / UNKNOWN, plus separate line for SCOPE-DIFFERENT recoded to UNKNOWN (incomplete transform).
Write falsifier_survey_report.md: method, per-folder table, taxonomy section, deviations
(seed-cell analogue: which folders' falsifiers fail their own bar).

## Deliverables (/mnt/agents/output/)
- falsifier_survey_report.md
- cell_records.jsonl, cell_records.csv

---

# PLAN EXTENSION — Run 2: Geometric-manifold- and Geometric-to-Binary-Computational-Bridge

Repos cloned: /tmp/gm (Geometric-manifold-), /tmp/g2b (Geometric-to-Binary-Computational-Bridge)

## Same protocol as Run 1 with these adaptations
- Survey unit = top-level directory + a "(repo root)" unit for root-level markdown.
  Run 1 excluded docs/ as meta; here docs/ carries claim tables and research notes, so it is IN.
- Same adjusted rule (MEASURED_AS / SCOPE_TRANSFORM / MISSING / UNKNOWN), coders blind to kinds.
- Taxonomy sort: blind sort of new SCOPE-DIFFERENT transforms first; then reveal the Run-1
  candidate taxonomy (K1 frame / K2 boundary / K3 homonym / K4 model-substrate calibration gap)
  and ask correspondence + whether the new N changes the verdict.

## Stages
- Stage 0b: scripted extraction over both repos -> survey2/raw_hits_{gm,g2b}.jsonl
- Stage 1b: parallel coding agents sized to extraction volume -> survey2/batches2/*.jsonl
- Stage 1b gate: same validator, folder lists per repo
- Stage 2b: blind sort (if any SCOPE-DIFFERENT cells), then K1-K4 reveal mapping
- Stage 3b: falsifier_survey_report_run2.md + cell_records_run2.jsonl/csv
  (one report covering both repos, per-repo counts sections)
