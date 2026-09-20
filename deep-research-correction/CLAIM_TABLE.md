# CLAIM_TABLE -- deep-research-correction

Permanent ids `DRC_NNN`. These are claims about the CHECKER and its
recomputation of the CORRECTION NOTICE's mechanical items, distinct from the
notice's own `C-n` / `U-n`. Ids are permanent; a refuted claim is updated in
place, never renumbered. Status: SUPPORTED / REFUTED / UNVERIFIED.

The two documents (`Simulators_Last_5_Folders_Deep_Research.md`, the target;
`CORRECTION_NOTICE.md`, the notice) are landed **verbatim** and edited by
nothing here. The checker imports the target read-only and recomputes; the
notice's own scope holds for this folder too: **document integrity and
measurand assignment only, not the repository's instruments and not the
target's suite results.**

| id | status | claim |
|---|---|---|
| DRC_001 | SUPPORTED | **C-1 recomputes from the doc.** The target self-dates its research and its re-execution 2026-09-19, later than the date the notice states it was issued (2026-09-18); a re-execution timestamp later than the date the target was in hand is not a re-execution record. The anchor is the notice's issue date `[CHOICE 1]` — the checker has no independent clock for when the target was in hand. |
| DRC_002 | SUPPORTED | **C-2 is doc-internal arithmetic.** `count_relation(63,157,220)="DISJOINT"` and `count_relation(63,157,157)="NESTED"`: the table's 220 counts the 63 and 157 as non-overlapping while the text states the 63 nested inside the 157 (total 157). Both cannot hold. The TL;DR separately enumerates four values (130,136,211,220) against five named folders. |
| DRC_003 | SUPPORTED | **C-3 is present in the doc.** A citation URL path reads `jul-3026` — July 3026, a future year — so the identifier is unusable as given, though the claim it supports (COBOL fixed-point decimal) is independently sourced in the same sentence. |
| DRC_004 | SUPPORTED | **C-4, LOAD-BEARING, has three parts and all three recompute.** (a) the target's own figures reconcile (550+303=853, ~64%/36%), so the fault is not arithmetic; (b) the local git-author distribution recomputes at HEAD and differs from the target's `main` figures, so the count is a property of who ran the tool, not a stable quantity `[CHOICE 2]`; (c) the structural verdict is `UNPARTITIONED`, computed by `measurand-partition/common.attribution` (imported, not restated) — the contribution residual assigned to the execution-channel identity, four intervening variables unmeasured. |
| DRC_005 | SUPPORTED | **C-5 and C-6 are present in the doc.** Both operator-characterizing clauses ("unusual degree of procedural self-discipline", "independent, outsider research program") and the preference attribution ("the one the repository would presumably prefer") are in the target verbatim. The notice's point is that none is load-bearing for a finding elsewhere. |
| DRC_006 | UNVERIFIED | **C-7 is carried, not reconciled.** The target says ~thirty sibling repositories; the operator's stated figure is 20+. Counting a GitHub account's public repositories requires network egress, which the allowlist refuses `[CHOICE 3]`, so the reconciliation is UNVERIFIED here. |
| DRC_007 | SUPPORTED | **U-1 recomputes against this repository, with one correction to the notice.** The instance-or-class scope of the same-author void is declared nowhere in the tree, so U-1 holds. The notice names the void `VOID_SAME_AUTHOR`; the repository's actual name for it is `VOID_KEY_HOLDER` (revision-survival) — a small correction to the notice, recorded rather than smoothed. |
| DRC_008 | SUPPORTED | **The target's five named folders are a branch-vs-main difference, not a defect.** Four of the five (`substrate-alternative`, `revision-survival`, `move-set`, `notes`) resolve in this checkout; `ledger` does not. The target analysed `main` and this is a working branch, so the miss is a branch difference and the notice's U-2 stands: the suite results are not checkable from here. |
| DRC_009 | UNVERIFIED | **The notice's external citation checks are carried.** The notice reports the Kalai et al. *Nature* 2026 DOI, AbstentionBench and Kadavath arXiv ids as verified against the sources (its V-1..V-3). The egress gate refuses publisher hosts, so this folder verifies none of them; they are the notice's OBSERVED, recorded and not re-checked here. |
| DRC_010 | SUPPORTED | **`count_relation` is not a constant classifier.** Three inputs return three distinct verdicts, and the equal-parts case `(100,100,100)` returns `NEITHER` rather than `NESTED`, pinning the `inner<outer` guard; registered in `tools/known_answer.py` with five cases, the two equal-parts cases pinning the guard and the branch order. |

## What this folder does not establish

- That the target's test-suite results are wrong. They are unchecked here,
  exactly as the notice states (its U-2). The `ledger` folder the target
  names is absent from this branch, so even the folder set differs.
- That the repository's instruments work or do not. The notice does not
  audit them and neither does this.
- Any external citation in the target beyond the three the notice
  spot-checked; those three are the notice's OBSERVED and are carried here,
  not re-verified.
