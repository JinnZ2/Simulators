WO-REG-1 — Regulatory Uncertainty Registry (pilot, 33 cases)

INPUT: reg_uncertainty_bundle.zip
  kimmy_v1/  = Kimmy (Kimi) deep-research output: report, RUS-0.1 draft standard,
               coded_decisions.csv (n=32), annex_a_regrading.csv, charts
  REVIEW_v1.md = chat-side review: VERIFIED numbers + CLAIM recodes (R1–R5)
Treat kimmy_v1 as SOURCE, REVIEW_v1 as findings to adjudicate — not as truth.
Do any other necessary items you find; log each one.

GOAL: turn this into a machine-readable registry an AI can query without
re-reading prose — no loss of provenance, reasoning chain, or cross-reference.
Semantics borrowed from nuclear QA (10 CFR 50 App B / NQA-1 style — verify
the mapping, don't assume it):
  design basis         → every grade/direction traces to evidence objects
  independent verification → reviewer ≠ originator; tag BLIND / CONTAMINATED-BY-PRIOR
  configuration mgmt   → versioned records, pinned hashes, change record per edit
  corrective action    → each REVIEW finding = one NCR (nonconformance report)
                         with disposition: ACCEPT / REJECT / MODIFY + reason
  graded approach      → verification rigor scales with consequence grade
  single-failure check → flag any conclusion resting on one source or one coder

PART A — schema (JSON Schema + controlled vocabulary file)
  Objects: EVIDENCE, DECISION, NON_DECISION, ENDPOINT_ABSENCE, OUTCOME,
           SUBSTANCE, ENDPOINT, SOURCE, CHANGE, NCR
  Edges:   cites, supports, contradicts, supersedes, mirrors (cross-agency),
           forced_by (statute/court/trial), predicts, closes
  Status on every claim: OBSERVED / DERIVED / PROPOSED
  Verification on every source: VERIFIED / CORRECTED / NOT_FOUND / UNREACHABLE
  Reuse existing IDs where they exist (e.g. EPA CompTox DTXSID, standard
  endpoint ontologies) — confirm availability; if none, mint local IDs and
  log the gap. Endpoint vocabulary is the choke point: a missing term makes a
  gap unqueryable, so list every endpoint you could NOT map.
  ENDPOINT_ABSENCE example: glyphosate × gut microbiome = NOT_ASSESSED.

PART B — load the 32 cases + add night shift (C11 or next free ID)
  Night shift: code exposure by ROTATION PATTERN (permanent night, forward,
  backward, weekly day↔night flip), not ever/never. Sources in REVIEW R5;
  verify each.

PART C — adjudicate REVIEW_v1 as NCRs
  R1 exec-summary 33.3% wording; Frame A has no cost-bearer variation
  R2 diffuse-bin recodes (C10, A06, B03); C08 sign; D02 final outcome
  R3 forcing table 11 vs 9; BVO discretionary
  R4 RUS: add TWO-SIDED consequence (C_permit, C_restrict); M2 vs Red No. 3;
     Annex A not independent
  Rerun stats after dispositions. Report "not testable" as "not testable".

PART D — RUS-0.2
  Two-sided consequence in schema AND grading; re-grade all 33; report
  whether "non-conformity is one-directional" survives.

PART E — tools (Python stdlib only, CC0)
  validate.py      schema + vocabulary + edge integrity; --selftest
  symmetry.py      same evidence profile, different direction, no named
                   exception → SYMMETRY-FAIL list
  chain.py         given any DECISION, print full reasoning chain back to
                   sources with status/verification at each hop; flag
                   single-failure nodes
  gaps.py          list ENDPOINT_ABSENCE + NON_DECISION + unmapped endpoints
  Pinned file hashes re-checked on every run.

ACCEPTANCE
  - all selftests pass; counts printed
  - every number in the revised report reproducible from the registry
  - change log: every recode with reason and NCR link
  - second coder on a 10-row subset, contamination probe first, kappa reported
  - branches kept separate: holds / scope-limited / no data / absent
  - no verdict language; inferences marked
