# Review of kimmy_v3 (2026-10-19)

Reviewer: Claude (chat session). Counts re-run from `kimmy_v3/coded_decisions_v3.csv`. Tags: VERIFIED / CLAIM as before.
v3 = three robustness upgrades on top of v2. It does not address REVIEW_v2 (R6–R11); those stay open.

## Accepted (VERIFIED)
- Dual cost-bearer rule: Rule L 7/28 vs 0/5, p = 0.559; Rule S 7/31 vs 0/2, p = 1.00. Reproduces. Carrying both columns is the right move.
- Action vs outcome columns: divergent rows A10, C04, D02 reproduce.
- Sweep table counts are internally consistent with the v2 annex (M0 = 22 / 7 / 2 / 0 / 2).

## R12. "Permissive in BOTH error directions" — logic error (CLAIM)
- Going ahead where denial harm is high (aducanumab, donanemab, eteplirsen, molnupiravir) is the side the two-sided standard asks for. That is avoiding the denial error, not committing it.
- An error in the second direction would be RESTRICTING where C_restrict > C_permit. The corpus has no such row (see R8). So the statement reduces to: "where denial harm dominates, decisions still came in one class more permissive than the floor (no conditions attached)." Still one direction. Remove "both error directions" and "stronger and stranger".

## R13. Sweep cannot test the zero — VERIFIED
- Over-restrictive violation requires a restrictive row with C_restrict > C_permit. No such row exists in any variant, because the sweep changes the matrix, not the rows. "0 over-restrictive in every variant" is structurally guaranteed and carries no robustness weight. The addendum's own §3 says the zero is "structurally intelligible" — then it cannot also be evidence. R8 (add restrictive-side candidates: Schedule I maintenance 1970–2025, clinical holds / refuse-to-file in a stated window) still required.
- The sweep never varies the R2 tolerance rule (REVIEW_v2 R7: −1 fails, +1 needs ≥2 and C_restrict > C_permit). Add variant M7: symmetric ±1 tolerance. Reviewer computed below-floor = 14 under M0 + symmetric tolerance.
- "Below floor 15–25" should read 14–25 once M7 is included.

## R14. Reversal asymmetry — keep, but recode and test the mechanism (CLAIM)
- Coding convention produces part of the "zero permissive→restrictive reversals": the 510(k) clearances (B00/B00b) reversed via later separate decisions (B01/B02). A reversal field should link decisions, not live inside one row.
- C03 glyphosate 2020 interim decision: human-health portion vacated by the Ninth Circuit (2022) and the interim decision withdrawn — a permissive action reversed by a court within its lifetime. Check and code.
- Denominator drift: forcing table says 7 of 8 restrictive actions; reversal line says 3 of 9 (A10 added). Use one list. A10's basis (unmet post-market study requirement) is a forcing event of the Makena type; code it.
- MECHANISM BRANCH (new, testable): the speed asymmetry (restrictive reversed in years via court/legislature/pressure; permissive reversed in decades after mass harm) is what the cost-bearer pattern predicts at the REVERSAL stage — concentrated parties have standing, funding and access to contest quickly; diffuse harmed parties must wait for injury to accumulate into litigation. Code for each reversal: initiator (sponsor / trade group / legislature / court on whose petition / public-interest litigant / injured class), time-to-reversal, and harm count at reversal. This may be where the hypothesis is testable when first-decision coding is not.

## Still open from REVIEW_v2
- R6 pentachlorophenol: EPA REQUIRED cancellation (epa.gov release) — C2 is not 34/34; the v3 combined statement repeats "34/34 continuations". Case closures → NA. Notice-level coding limit.
- R7 margin asymmetry (now M7 above). R8 over-restriction candidates. R9 substitution risk in C_restrict. R10 Coder B pass-2 tuned post hoc. R11 change-log framing.
