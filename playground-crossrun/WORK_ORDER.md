WORK ORDER — Two-playground cross-run (co-authored, Kavik + Claude, 2026-11-11)
Repos: JinnZ2/study-aperture (experimental/playground, Perplexity, merged) and JinnZ2/Simulators
(relational-playground, draft #257, Claude Code). Branch rule: keep both. Change neither's code.
New folder in Simulators: playground-crossrun/ (draft PR). Stdlib only.

STEP 1 — CROSS-RUN (now)
A Run each playground's own self-check/tests as-is. Report pass counts (baseline).
B Feed each one the OTHER's cases, through thin adapters only (no logic edits):
   - Perplexity's planted defects, L0 cases, known-answer/null cases, cross-system classes,
     measurand/denominator/mean audits → into #257
   - #257's forest run 9 port (+ runs 6–8 originals when filed), leak plant, coincidence cases,
     percolation/branching fixtures → into Perplexity's
C Per case: caught? | classified how? | agree / disagree with the other playground
   Disagreement codes: MISSED (one doesn't detect) | MISCLASSIFIED (detects, different axis/status) |
   NO_SLOT (concept absent — e.g. #257 has no INSTRUMENT vs DETERMINATION split; Perplexity has
   no claim tags/coincidence card) | ADAPTER (adapter couldn't express the case — record, don't force)
D Coincidence card on every agreement (independent builders converging: real shared constraint,
   or shared source/corpus?).
E Concept map: each concept → where it lives in each playground (or VOID).

STEP 2 — COMBINED SPEC (after Kavik reviews step 1; do not build yet)
Draft COMBINED_SPEC.md: per concept, which version is taken and why (cite step-1 evidence),
optimized for AI readers: distinct tokens for every state, no shared labels for different states,
reason fields on every non-verdict. Both originals stay untouched.

STEP 3 — TAF (after step 2 is accepted)
Adopt three-axis failure model (PHYSICAL / INSTRUMENT / DETERMINATION) in TAF unified_audit;
map GAP_INSTRUMENT_CRASH / _UNRECOGNIZED_LABEL → INSTRUMENT, NOT_DETERMINABLE reasons →
DETERMINATION. Not before step 2.

Report step 1: baseline pass counts → disagreement table by code → concept map → anything off.
