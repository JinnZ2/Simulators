# WO-REG-1 (consolidated) — Regulatory Uncertainty Registry, pilot

Consolidates WO-REG-1, addendum WO-REG-1a, and new addendum WO-REG-1b (2026-10-19).
If an earlier WO-REG-1 bundle was already loaded, this bundle supersedes its inputs; keep the earlier commits, log the swap as a CHANGE.

## Inputs (this bundle)
- `source/current/` — latest Kimmy (Kimi) research output: report v2, sensitivity addendum v3, RUS-0.2 standard, coded_decisions_v3.csv (33 rows, dual cost-bearer + action/outcome columns), annex_a_regrading_v2.csv, epa_frame_2022.csv, calibration_sweep_v3.csv, change log v1→v3, charts.
- `source/superseded/` — v1 and v2 files, kept for configuration history only. Load as superseded versions; do not grade from them.
- `reviews/REVIEW_v1.md`, `REVIEW_v2.md`, `REVIEW_v3.md` — chat-side reviews, items R1–R14. Treat as findings to adjudicate, not truth.
- `MANIFEST.sha256` — pin these hashes; re-check on every run.

Treat source as SOURCE. Do any other necessary items you find; log each one.

## Goal
A machine-readable registry an AI can query without re-reading prose: no loss of provenance, reasoning chain, cross-reference, or decision authority. Legacy decisions are audited as decided, not assumed correct.

Semantics borrowed from nuclear QA (10 CFR 50 App B / NQA-1 style — verify the mapping, don't assume it):
- design basis → every grade/direction traces to evidence objects
- independent verification → reviewer ≠ originator; tag BLIND / CONTAMINATED-BY-PRIOR
- configuration management → versioned records, pinned hashes, CHANGE record per edit
- corrective action → each review item = one NCR with disposition ACCEPT / REJECT / MODIFY + reason
- graded approach → verification rigor scales with consequence grade
- single-failure check → flag any conclusion resting on one source or one coder

## Part A — schema (JSON Schema + controlled vocabulary)
Objects: EVIDENCE, DECISION, NON_DECISION, ENDPOINT_ABSENCE, OUTCOME, REVERSAL, SUBSTANCE, ENDPOINT, SOURCE, ACTOR, AUTHORITY, CONFLICT, CHANGE, NCR.
Edges: cites, supports, contradicts, supersedes, mirrors (cross-agency), forced_by (statute/court/trial), predicts, closes, reverses, decided_by, recommended_by, overruled, delegated_from, funded_by.
- Status on every claim: OBSERVED / DERIVED / PROPOSED.
- Verification on every source: VERIFIED / CORRECTED / NOT_FOUND / UNREACHABLE.
- Reuse existing IDs where they exist (e.g. EPA CompTox DTXSID, standard endpoint ontologies) — confirm availability; else mint local IDs and log the gap. List every endpoint you could NOT map (the vocabulary decides what is queryable).
- ENDPOINT_ABSENCE example: glyphosate × gut microbiome = NOT_ASSESSED.
- Direction is stored TWICE: as the agency's verb and RELATIVE TO THE COST-BEARER. Store both cost-bearer rules (L and S).
- Consequence is TWO-SIDED in the schema: C_permit and C_restrict, each with P/I/D scores + rationale; C_restrict carries a substitution field (named alternative + its own grade).

### 1a — authority and actors
- ACTOR: actor_id, type (person / office / agency / court / legislature / advisory_committee / sponsor / trade_group / public_interest_litigant / injured_class), name, role_at_time, date_range.
- AUTHORITY chain on every DECISION: statute → regulation → guidance → decision, each with citation; flag UNREACHABLE / NOT_FOUND links.
- CONFLICT: actor_id, type (financial / prior employment / institutional-reputational commitment / funding source), source, verification. Record recusals. No disclosure record = NOT_FOUND, never "no conflict".
- Unrecorded legacy inputs: create the EVIDENCE node anyway, status UNREACHABLE, reason stated. Gaps are nodes, never blanks.

### 1b — reversals (new)
- REVERSAL object links two decisions (or a decision and a court/legislative act): from_direction, to_direction, initiator ACTOR, mechanism (court / legislature / agency under pressure / new evidence / mass-harm litigation), time_to_reversal, harm count at reversal (if documented, else NOT_FOUND).
- Do not encode reversals inside a single row; 510(k) clearance → PMA order is a REVERSAL edge between B00/B00b and B01/B02.

## Part B — load
- Load the 33 coded decisions from `coded_decisions_v3.csv` and the 40 rows of `epa_frame_2022.csv` (case closures as NA direction, not go_ahead).
- Night shift (E01): exposure coded by ROTATION PATTERN (permanent night, forward, backward, weekly day↔night flip), never ever/never.

## Part C — adjudicate reviews as NCRs (R1–R14)
Open items most likely to change results:
- R6 pentachlorophenol: EPA REQUIRED cancellation (epa.gov release "EPA Requires Cancellation of Pentachlorophenol to Protect Human Health") → restrictive, discretionary. Frame C2 is not 34/34; forcing count changes. Fix everywhere "34/34" appears (report v2 §1, §6.2; sensitivity v3 combined statement).
- R7/R13 margin rule asymmetry: add sweep variant M7 = symmetric ±1 tolerance (reviewer computed 14 below floor under M0 + M7).
- R8/R13 no restrictive row with C_restrict > C_permit → "0 over-restrictive" is untestable. Add restrictive-side candidates (Schedule I maintenance of cannabis/psilocybin 1970–2025 with R6 self-sealing; FDA clinical holds / refuse-to-file in a stated window) and rerun.
- R9 substitution risk in C_restrict (PFOA → GenX as reference).
- R10 Coder B pass-2 κ tuned post hoc → report pass 1 (κ 0.45) as reliability.
- R11/R12 framing: "null strengthens" and "permissive in both error directions" are errors — fix wording.
- R14 reversal recoding: C03 glyphosate interim decision (vacated in part 2022, withdrawn) as a permissive reversal; single restrictive-action list (A10 included, forcing coded).
Rerun every statistic after dispositions. "Not testable" is reported as "not testable".

## Part D — RUS-0.3
Two-sided consequence with substitution field; symmetric tolerance as published variant; R6 self-sealing applied; re-grade all rows; report whether one-directional non-conformity survives each variant.

## Part E — tools (Python stdlib only, CC0)
- `validate.py` — schema, vocabulary, edge integrity; `--selftest`
- `symmetry.py` — matched profile, different direction, no named exception → SYMMETRY-FAIL
- `chain.py` — for any DECISION: evidence chain + actor chain + authority chain back to sources, status/verification at each hop; flag single-failure nodes
- `gaps.py` — ENDPOINT_ABSENCE, NON_DECISION, unmapped endpoints, UNREACHABLE authority links, unlocated inputs, missing conflict records
- `who.py` — given ACTOR: every decision, direction, overruled advice; given DECISION: everyone in its chain
- `reversals.py` — reversal table by initiator type, median time_to_reversal by direction (the testable cost-bearer branch: does the bias live at the reversal stage?)
- Pinned hashes re-checked on every run.

## Acceptance
- All selftests pass; counts printed.
- Every number in the revised report reproducible from the registry.
- Change log: every recode with reason and NCR link; addenda logged as WO-REG-1a / WO-REG-1b.
- Second coder on a 10-row subset, contamination probe first, κ per field.
- Branches kept separate: holds / scope-limited / no data / absent. No verdict language; inferences marked.
