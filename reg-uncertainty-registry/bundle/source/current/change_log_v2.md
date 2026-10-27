# Change Log — v1 → v2 (WORK ORDER v2)

Every recode and substantive change, with reason. Files affected: `coded_decisions_v2.csv` (dataset), `annex_a_regrading_v2.csv` (grading), `direction_of_uncertainty_report_v2.md` (report), `regulatory_uncertainty_standard_v02.md` (standard), charts 2/4/5.

## Dataset recodes (`coded_decisions_v2.csv`)

| ID | Field | v1 | v2 | Reason (work-order fix) |
|---|---|---|---|---|
| C10 | cost_bearer | public | sponsor | Fix 3: a sponsor exists (Bayer); caution cost falls on the registrant. |
| A06 | cost_bearer | public | sponsor | Fix 3: a sponsor exists (Merck). |
| B03 | cost_bearer | public | sponsor | Fix 3: sponsor exists (countermeasure manufacturers); human-efficacy requirement would kill programs. |
| C08 | direction | hold | go_ahead | Fix 4: direction coded **relative to the cost-bearer**. Declining to require monitoring relieves utilities → permissive toward them. Action verb ("declined to monitor") preserved in note. |
| D02 | direction | hold | warn | Fix 4: coded on **final outcome** — 1977 moratorium kept saccharin on market with a warning label. The ban attempt is logged as an agency action in the note and in the forcing analysis. |
| — | new row E01 | — | added | Fix 10: night shift work — IARC Vol. 124 Group 2A (2020) ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)), Denmark compensation (K-flag: search backend unavailable at revision time), no US OSHA standard. Exposure-coding note requires rotation pattern (permanent night / forward / backward / weekly flip), not ever/never. |
| B05 | (grading only) | U1 | U3 | Fix 7: M2 applied consistently — animal-only evidence ⇒ at least U3. Dataset keeps record-stated uncertainty=low; the U3 grade applies in RUS-0.2 grading. |

## Statistical consequences

- Bivariate test (v2): restrictive 7/31 concentrated-bearer vs 0/2 diffuse-bearer, Fisher p = 1.00 (v1: 9/27 vs 0/5, p = 0.29). High-uncertainty subset: 3/20 vs 0/2, p = 1.00. Excluding statute-compelled: 2/25 vs 0/2, p = 1.00. The bivariate "pattern absent" result **strengthens**.
- Structural finding (new): after Fix 3, the diffuse-cost-bearer configuration occurs in only 2 of 33 decisions — the configuration the naive hypothesis needs barely exists in practice.

## Forcing-analysis reconciliation (Fix 5)

- v1 claimed "11 of 11" restrictive decisions on forcing events against 9 coded restrictive rows — unreconciled. v2: **agency actions only**; court rulings logged separately (NRDC v. EPA 2022 glyphosate vacatur; 8th Cir. 2023 chlorpyrifos vacatur). v2 restrictive agency actions: 7 coded rows + the 1977 saccharin ban attempt (final outcome coded warn). **BVO is reclassified as discretionary** (driven by FDA's own studies, no external forcing) — the v1 chart's "New data" framing overstated the forcing. Corrected finding: **7 of 8 restrictive agency actions ride an external forcing event; BVO is the lone discretionary exception.**

## Report text corrections (Fix 1)

- v1 incorrectly stated FDA "followed … only 33.3% of negative votes." Correct: FDA **followed 66.7% of negative votes** (declined approval in 40/60) and **approved 33.3% anyway** (20/60). Discordance rates (33.3% after NO vs 3.4% after YES; 9.8×; Fisher OR 14.2) were and remain correct. Fixed in executive summary and Section 5.1.

## Frame A reinterpretation (Fix 2)

- Frame A contains **no cost-bearer variation** (the sponsor always bears the caution cost). It is now reported as "**permissive skew, consistent with the pattern, no contrast group**" and moved out of "pattern holds." Rival explanations added: unmet medical need, statutory access mandate, advocacy pressure, PDUFA user-fee dynamics.

## New unselected EPA frame (Fix 9)

- **Frame C2**: all EPA pesticide registration-review interim/final decisions announced in the Federal Register, calendar year 2022 — 5 decision notices (87 FR 5815, 6535, 25266, 48018, 64484), **34 decisions on merits + 6 case closures**, enumerated verbatim in `epa_frame_2022.csv`. Direction coding at notice level (registration continued = permissive toward registrant); document-level mitigation not coded (scope limit stated). Result: 34/34 permissive; restrictive actions in the same window (chlorpyrifos cancellation NOI, DCPA suspension NOI, PFAS-inert removal) logged separately.

## RUS-0.1 → RUS-0.2 (Fix 6)

- Consequence made **two-sided**: C_permit (harm if wrongly allowed) and C_restrict (harm if wrongly blocked — no alternative therapy, essential service, research blocked), each scored P/I/D. Floor column set from the **gap** C_permit − C_restrict. Over-restriction can now be non-conforming when C_restrict > C_permit (bounded margin rule).
- Annex A re-graded (n=33, `annex_a_regrading_v2.csv`): 22 below floor, 6 exact-conform, 2 exceed-floor, 2 statute/judicial exceptions, 1 R5 — **zero over-restrictive non-conformities. One-directional non-conformity survives the two-sided re-grade.** Two flips of note: donanemab (A09) moves to conform (high denial harm), flibanserin (A07) to exceeds-floor.

## Replication claim removed + second coder added (Fix 8)

- v1's statement that the conformity audit "replicates" the population-level result is removed — same coder, same cases; not independent.
- Second-coder exercise: frozen rule-based codebook ("Coder B") applied to a 10-row stratified subset. Pass 1 (fact strings as written): direction agreement 70%, κ = 0.45 — all three disagreements traced to comparator-action verbs in the strings (rulebook attributed the EU ban instead of the US action). Pass 2 (frozen input rule: string names only the US federal action): direction agreement 90%, κ = 0.76; uncertainty agreement 80%, κ = 0.64 (both passes); cost-bearer 100% (κ undefined — no variance in subset). **Limitation marked: Coder B is a programmatic instrument authored by the same researcher; a true independent human coder remains outstanding.**

## Other

- Search backend was unavailable for part of the revision; Denmark-compensation and pentachlorophenol-cancellation details carry K-flags pending re-verification.
- Charts 2, 4, 5 regenerated from v2 data; chart 1 unchanged (its annotations were already correct).

---

# Change Log — v2 → v3 (robustness upgrades, 2026-10-18)

| Change | Detail | Files |
|---|---|---|
| Dual-rule cost-bearer | `cost_bearer_L` (v1 largest-share rule) restored alongside `cost_bearer_S` (v2 rule); both Fisher tests reported (p = 0.559 / 1.000). Null robust to operationalization. | `coded_decisions_v3.csv`, `sensitivity_upgrades_v3.md` |
| Action/outcome split | `action_direction` and `outcome_direction` added; 3 divergent rows (D02, A10, C04), all restrictive→permissive reversals; reversal asymmetry documented. | `coded_decisions_v3.csv` |
| Calibration sweep | 7 matrix variants (M0–M6) computed; below-floor 15–25/33; over-restrictive violations 0 in all variants. One-directional skew not an artifact of cutoffs. | `calibration_sweep_v3.csv`, `img/chart6_sweep.png` |
| New finding recorded | Corpus is permissive in **both** error directions: high-denial-harm cases and high-hazard cases alike resolved go-ahead. | `sensitivity_upgrades_v3.md` §3 |
| Marked limitation added | Sweep varies the matrix, not the per-case P/I/D scores; scorer-level Monte Carlo identified as next layer, not run. | `sensitivity_upgrades_v3.md` §3 |
