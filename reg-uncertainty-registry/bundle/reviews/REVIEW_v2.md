# Review of kimmy_v2 (2026-10-18)

Reviewer: Claude (chat session). Counts re-run from `kimmy_v2/*.csv` (scipy Fisher exact). Tags: VERIFIED = recomputed or checked against a source; CLAIM = reviewer reading.
Supersedes nothing in REVIEW_v1; adjudicate these as new NCRs (WO-REG-1 Part C).

## Accepted from v2 (VERIFIED against files)
- Fixes 1, 2, 3, 4, 5, 7 applied as specified. Bivariate 7/31 vs 0/2, p = 1.00 reproduces. Annex counts reproduce (22 / 6 / 2 / 2 / 1). Change log present, every recode reasoned.
- Frame A now reported as "permissive skew, no contrast group", four rival explanations named. Good.
- BVO reclassified discretionary; court rulings separated. Good.

## R6. Frame C2 sign error — VERIFIED
- Pentachlorophenol (87 FR 6535, Feb 2022) coded `go_ahead` with K-flag "registrant-led". EPA's own release: "EPA Requires Cancellation of Pentachlorophenol to Protect Human Health" — all uses, 5-year phase-out.
  Sources: https://epa.gov/pesticides/epa-requires-cancellation-pentachlorophenol-protect-human-health ; https://fyi.extension.wisc.edu/pat/2022/05/04/epa-to-phase-out-use-of-pentachlorophenol
- Consequence: C2 is not 34/34 permissive. Pentachlorophenol is a restrictive agency action with no court/statute forcing visible → a SECOND discretionary restriction (with BVO). "Lone discretionary exception" must be revised (forcing count becomes 7 of 9 at most).
- Case closures (6 rows) are coded `go_ahead`. They are not decisions on the merits; code NA and exclude from direction counts. Sponsor exit may itself be a hidden restrictive channel (exit in anticipation of EPA demands) — log as a gap, not as permissive.
- Notice-level coding cannot see use cancellations or mitigation inside interim decisions (creosote, chromated arsenicals, permethrin amended). "Registration continued" at notice level is close to tautological. Code at least the decision documents for wood preservatives before claiming direction.
- Structural: C2 has no cost-bearer variation either (sponsor in every row) → same no-contrast limit as Frame A. Say so.

## R7. RUS-0.2 margin rule is still asymmetric — CLAIM
- Below floor by 1 class = non-conforming. Above floor requires ≥ 2 classes AND C_restrict > C_permit to be non-conforming. Tolerance is +1 on one side, 0 on the other. "One-directional non-conformity" is partly produced by this rule.
- Symmetric-tolerance check (±1 conforming both ways, computed from annex_a_regrading_v2.csv): below-floor drops 22 → 14 (A01, A02, A10, B03, B04, C05, C07, D01 move to within-margin). Over-floor stays 0. Direction of the skew survives; its size is rule-dependent. Report both.

## R8. Over-restriction arm has no candidates — VERIFIED
- Rows with C_restrict > C_permit: A01, A02, A06, A07, A08, A09, A10, B03 — all approvals except A08 (R1 withdrawal). No restrictive decision in the sample has C_restrict > C_permit, so R2's over-restrictive test cannot fire on any row. "Zero over-restrictive" is untestable by construction, not a finding.
- Sample drawn from permissive anchors. Add restrictive-side candidates where denial harm is plausible, e.g.: Schedule I maintenance of cannabis/psilocybin 1970–2025 (the research-blocking decision itself, not the 2026 partial reschedule — D01 currently grades the LOOSENING as under-cautious while R6 self-sealing goes unapplied); and any FDA refuse-to-file / clinical holds in a stated window. Then rerun.

## R9. Denial-harm scoring omits substitution risk — CLAIM
- C_restrict is lowered wherever "alternatives exist" (glyphosate, atrazine, aspartame, TiO2, mesh). The alternative's own hazard is not scored. Regrettable substitution is documented in this corpus's own neighbor case: PFOA → GenX (HFPO-DA). Add a substitution axis or a rule: "alternatives exist" requires naming the alternative and its grade.

## R10. Coder B pass 2 was tuned after pass 1 — CLAIM
- The "frozen input rule" was adopted after pass-1 disagreements were inspected. Pass-2 κ = 0.76 is a post-hoc fit, not a reliability estimate. Report pass 1 (κ = 0.45) as the reliability figure; pass 2 as codebook revision. Human independent coder still owed (already acknowledged).

## R11. Framing
- Change log: "bivariate 'pattern absent' result strengthens" (p 0.29 → 1.00). Moving the diffuse cell from n=5 to n=2 removes information; it is a weaker test, not a stronger null. The report body says "nearly uninformative" — make the change log match.
- Night shift: Denmark compensation K-flag — a chat-side search returned a review stating "Monetary compensation has already been paid for such cases in at least one country (Denmark)" (PMC review "Shift Work and Cancer: The Evidence and the Challenge", Dtsch Arztebl). Locate primary Danish source to clear the flag.
