# WORK_ORDER.md

Delivered 2026-11-10, verbatim (the spec it carried is in SPEC_GPT.md).

---

WORK ORDER — Relational Systems Playground (co-authored, Kavik + Claude + GPT spec, 2026-11-10)
Repo: JinnZ2/Simulators, new folder relational-playground/. Stdlib only, CC0. Draft PR. Merge nothing.
Follow forest-model-ledger/CLAUDE.md METHOD BRIEF (incl. "ask questions, as many as needed, one at a time").

BASE SPEC: GPT "Relational Systems Experimental Playground" (Kavik will paste verbatim) — keep its
6 layers (system, relational, boundary, control, continuity, uncertainty matrices), equation
substitution interface MODEL(state, environment, relationships, controls, parameters), boundary
experiments A–D, applicability record (no ranking), outputs, project structure, constraints, phases.
File the spec verbatim as relational-playground/SPEC_GPT.md, provenance: GPT, 2026-11-10.

ADDITIONS (from method; each a separate commit, labeled):
 1 L0 GATE — every run closes declared budgets (mass/N/C/water/energy as applicable) and reports
   misclosure. A run that fails closure is INCOMPLETE regardless of fit. Energy-family is not
   the only place energy is checked. Boundary audit line per run (what crosses the chosen boundary).
 2 ANCHOR LOOP — frozen, sha-pinned anchor configs; every branch changes ONE thing; RETURN step
   diffs against its anchor; anchor test (closure, seeds, nudges, multi-budget). Reuse forest
   ledger's anchor record + STATUS_MAP.
 3 KNOWN-ANSWER GATE — no equation module or analysis tool trusted until it passes planted-defect
   cases + null-harness (FP=0 / TP=1). Reuse simulators/null-harness and tools/known_answer.py.
 4 EXPIRY — every UNKNOWN / NOT MEASURED carries expiry_condition (VOID allowed, counted as
   "no exit defined"). Add ABSENT_AT_SENSITIVITY(<value>) to the uncertainty statuses.
 5 CLAIM TAGS — results/interpretations tagged OBSERVED / DERIVED / PROPOSED, separate from the
   value statuses (MEASURED…EXCLUDED BY DESIGN).
 6 OBSERVER REGIMES — PERTURBATION / REACTIVITY / STRATEGY as separate fields in the control matrix;
   no cross-system comparison until each system's regime is declared.
 7 EQUATION FAMILIES — add percolation (spatial threshold, spotting parameter) and branching
   process (early stochastic die-out) beside linear/nonlinear/network/energy/boundary/stochastic.
 8 COINCIDENCE CARD — wire divergence-playground/coincidence.py (C1–C6 + none_of_above) into
   analysis/: run on any cross-family agreement.

FIRST EXPERIMENT: port forest-model-ledger run 6 (mass-conserving N model) + runs 7–8 (ODE vs
percolation, spotting) as experiments/model_comparison/forest_fire_regime/. Must reproduce the
logged results; misclosure ~1e-9; convergence at spot 0.2, drought ≥0.5.

DO NOT: rank models, auto-select boundaries, drop failed predictions, fill unknowns.
Report: TOOL NEEDED line (if any) → which additions landed → forest port reproduced? → open questions.
