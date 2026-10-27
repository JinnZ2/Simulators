# Review of kimmy_v1 (2026-10-18)

Reviewer: Claude (chat session). Numbers re-run from `kimmy_v1/coded_decisions.csv` with scipy Fisher exact.
Status tags: VERIFIED = re-computed or checked against the file; CLAIM = reviewer reading, not yet checked by a second party.

## R1. Frame A — VERIFIED
- 20/60 approved after negative vote; 5/147 declined after positive vote. OR 14.2, p = 2.1e-8. Matches the report.
- Exec summary wording error: "followed only 33.3% of negative votes" — FDA FOLLOWED 40/60 = 66.7%; it APPROVED ANYWAY 33.3%. (§1 line 15)
- CLAIM: Frame A has no cost-bearer variation (sponsor bears cost of caution in every row) → shows permissive skew, cannot test correlation with cost-bearer. No contrast group. "Pattern holds" overstates; should read "consistent with, no contrast group", with rival explanations listed (unmet need, access mandate, advocacy).

## R2. Coded sample — VERIFIED counts, CLAIM recodes
- As coded: concentrated restrictive 9/27, diffuse 0/5, p = 0.288. Restrictive rows: A04 A08 B01 B02 B05 B06 C04 C08 D02.
- Diffuse bin contains sponsored products: C10 (glyphosate — Bayer), A06 (molnupiravir — Merck), B03 (Animal Rule — countermeasure makers). CLAIM: recode to concentrated.
- C08 (microplastics monitoring declined) coded `hold` = restrictive, but declining monitoring RELIEVES the utility cost-bearer → permissive relative to cost-bearer. Sign flipped. Direction must be coded relative to the cost-bearer, not by verb.
- D02 (saccharin 1977): final outcome = congressional moratorium (permissive). Code on final outcome or carry both stages.
- Recoded (C10/A06/B03 → concentrated; C08, D02 → permissive): 7/30 vs 0/2, p = 1.0. Result: NOT TESTABLE at this n, not "pattern absent".

## R3. Forcing-event table — inconsistency
- §5.5 says "11 of 11 restrictive"; dataset has 9 restrictive rows. Table adds lead 2024 and PFAS 2024 (both coded `warn` = permissive) and the 2022 glyphosate court vacatur (court action, not agency decision); omits C08.
- BVO (B06): basis = FDA's own new rodent studies → discretionary, not external forcing. Contradicts "none was discretionary".

## R4. RUS-0.1 standard
- Consequence grade scores ONLY harm of a wrong permit. Harm of a wrong restriction (no alternative therapy: A02 eteplirsen DMD, A10 midodrine; B03 countermeasures; essential services) is never scored → Annex A finding "non-conformity is one-directional" is partly built into the instrument. The instrument fails its own symmetry audit.
- Fix: two-sided consequence: C_permit and C_restrict, floor set from the difference.
- B05 Red No. 3 graded U1, but M2 says animal-only with unresolved extrapolation ≥ U3. Inconsistent.
- Annex A is described as an independent replication of Frame A; it is the same coder on the same 32 cases → not independent. Single-coder, no kappa.
- KEEP: decision record schema, U4 "never looked" rule, data tickets with sunset, declared statute exceptions, symmetry audit pseudocode, calibration section.

## R5. New case to add — night shift work (sources from chat search 2026-10-17)
- IARC Group 2A (2007; retained 2019, Vol 124): limited human evidence (breast, prostate, colon, rectum), sufficient animal, strong mechanistic.
- Pooled 10 prospective cohorts, 1.4M women: RR 0.99 breast (secondary source; primary believed Travis et al. 2016 JNCI — verify).
- Denmark has paid workers' compensation; Germany requires "general scientific merit"; no US OSHA shift-work standard (reviewer knowledge — verify).
- Exposure coding: cohorts use ever/never night work, which erases rotation pattern (permanent night vs forward/backward rotation vs weekly day↔night flip). Code exposure by rotation pattern.
- Reviewer grade (CLAIM): U3; P3 I3 D1 → C3; one-sided floor D4; two-sided (night work essential) → D2/D3 schedule-design conditions + data ticket. Actual US direction D1. Cost-bearer of caution: employer.
