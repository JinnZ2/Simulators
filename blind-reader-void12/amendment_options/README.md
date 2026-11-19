# amendment_options

Evidence for the choice of key v2 amendment 1. Nothing in this folder changes a key, the brief, a scorer, `PREREG.md` or any reading. Nothing here is adopted.

| path | what it is |
|---|---|
| `OPTIONS.md` | the three open choices, the evidence for each labelled SOURCE / RULE / COMPUTED, how much each moves the one filed v2 reading, and a view (labelled as a view) |
| `as_received/KEY_V2_AMENDMENT_1.patch` | the patch exactly as received, sha256 `8ea98d4cd6cc4702b239a626b4f45c54ad1174f209d8a03ce70fe65fa75452bb` |
| `as_received/KEY_V2_AMENDMENT_1_DRAFT.md` | the earlier draft exactly as received, sha256 `b2805ea9e976d15a60bac23f0fd70e634f471d006bbe31ed20cf1d3208762598` |
| `as_received/KEY_V2_AMENDMENT_1_r1.patch` | revision 1 of that patch (R-a, R-b; T10 `[missing_path]`), exactly as made in the Claude Code session, sha256 `dd35fe331ae4fdd6360b5deb5381f95ff4c92ed07b742539875b171932c43108`; superseded by `KEY_V2_AMENDMENT_1.md` (a1) and never adopted; filed 2026-11-19 so the `decide/` re-run instruction ("a tree with the received r1 patch applied") can be followed from this repository |
| `evidence/check_rules.py`, `check_rules_output.txt`, `.json` | applies the amendment's rule tests mechanically to the packet's own sources (numcheck records, cplay constructors, TAF coverage dictionaries) |
| `evidence/build_candidates.py`, `build_candidates_stdout.txt`, `candidate_scores.txt`, `.json` | builds candidate keys on the patched key, scores the filed Claude-v2-A reading under each; the candidate key files are not kept |
| `derive/derive_specific.py`, `derive_specific_output.txt`, `.json` | derives each term's `slots_specific` from the packet's sources by one stated rule (OPTIONS.md section 6), reads no key, compares with three keys afterwards, and runs five mutation checks |
| `decide/CRITERIA.md`, `check_rule_stability.py`, `check_nck.py`, `check_nd.py`, `DECISION_EVIDENCE.md` | criteria committed before the checks (`d7b7687`); the checks and their outputs; the per-item result and recommendation for the rule, N1, C1, ND, K1. Re-run: `SCORER_TREE=<tree with the received r1 patch applied> FORMULA_AUDIT_DIR=<formula-audit checkout> python3 check_nck.py` (the other two need only `FORMULA_AUDIT_DIR`). |

Re-running the derivation (needs a formula-audit checkout whose `numcheck/check.py` matches the packet's; the script checks and stops if not; `COMPARE` is optional and names extra key files to compare with):

```text
FORMULA_AUDIT_DIR=<checkout> COMPARE="name=<path to a key json>" python3 derive/derive_specific.py
```

Re-running the rest:

```text
# 1. the rule checks (formula-audit checkout whose numcheck/check.py has the same sha256 as the packet's; the script checks and stops if not)
FORMULA_AUDIT_DIR=<checkout> python3 evidence/check_rules.py > evidence/check_rules_output.txt

# 2. apply the patch to a scratch copy of main (not to this branch), then
SCORER_DIR=<scratch>/blind-reader-void12/scoring PATCHED_KEY=<scratch>/blind-reader-void12/scoring/key_v2_a1.json \
  python3 evidence/build_candidates.py
```

Limits: one v2 reading exists (Claude-v2-A, the model the amendment was drafted by). Scores under a candidate key show how much a choice matters, not which choice is right.
