# Sensitivity & Robustness Upgrades (v3)

**Addendum to `direction_of_uncertainty_report_v2.md` and RUS-0.2 — October 18, 2026**

Implements the three agreed robustness upgrades: dual-rule cost-bearer sensitivity, action-vs-outcome direction columns, and a calibration sweep over the RUS-0.2 decision matrix. Same rules as the parent documents: flat reporting, inference chains marked, no verdict language. Data: `coded_decisions_v3.csv`, `calibration_sweep_v3.csv`.

---

## 1. Dual-rule cost-bearer sensitivity

The v2 recode (Rule S: *code sponsor wherever a sponsor exists*) traded construct validity for coding reliability and shrank the diffuse-bearer cell to n=2. This upgrade reports both operationalizations side-by-side on the same v2 direction coding:

| Operationalization | Concentrated restrictive/permissive | Diffuse restrictive/permissive | Fisher p |
|---|---|---|---|
| **Rule L** (v1: largest-share judgment — pandemic, countermeasure, and public-health contexts coded public) | 7 / 21 | 0 / 5 | 0.559 |
| **Rule S** (v2: sponsor-if-exists) | 7 / 24 | 0 / 2 | 1.000 |

**Finding, stated flat:** the bivariate null is **robust to the operationalization** — neither rule produces support for the naive cost-bearer hypothesis, and neither produces a statistically separable difference. What changes between rules is not the conclusion but the *informativeness*: under Rule L the diffuse cell has 5 observations (still small); under Rule S it has 2. The earlier claim stands in weakened form: the corpus contains too few diffuse-bearer decisions to test the hypothesis's caution condition bivariately under either rule, and this is itself a structural property of the decision space — concentrated cost-bearers are nearly always present. Both codings are now carried in `coded_decisions_v3.csv` (`cost_bearer_L`, `cost_bearer_S`) so any reader can re-run the test under their preferred rule.

## 2. Action vs. outcome direction

Two columns added: `action_direction` (the agency's own move at decision time, relative to the cost-bearer) and `outcome_direction` (the legal status as of October 2026). Three rows diverge, and all three diverge in the same direction:

| ID | Agency action | Outcome (2026) | Reversal mechanism |
|---|---|---|---|
| D02 | decline (1977 ban proposal) | warn | Congress overrode with a moratorium + label ([Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) |
| A10 | decline (2010 proposed withdrawal) | go_ahead | Agency reversed after prescriber/patient outcry; proposal never effectuated |
| C04 | decline (2021 revocation) | warn | Eighth Circuit vacated 2023; tolerances reinstated with partial use retention ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/chlorpyrifos)) |

**Reversal asymmetry, stated flat:** of 9 restrictive agency actions in the corpus, 3 were reversed or overridden toward permissive within the observation window (legislature, agency reversal under pressure, court). Of 24 permissive actions, **zero** were reversed toward restrictive within their decision's lifetime. The corpus does contain permissive→restrictive trajectories — the 510(k) clearances (B00/B00b) that became PMA requirements (B01/B02) — but they arrive as *separate decisions*, 16–20 years later, and only after mass harm and litigation. The asymmetry is real but the two directions run on different clocks: restrictive reversals are fast (years) and juridical; permissive reversals are slow (decades) and harm-driven. *Inference chain marked:* "reversal" is coded from legal status changes; it does not capture partial tightening (label changes, restricted subpopulations), which would soften the zero.

## 3. Calibration sweep on the RUS-0.2 matrix

The published matrix's gap thresholds (G ≥ 3 / 1–2 / 0 / ≤ −1) and U-row floors were chosen, not derived — the strongest attack surface identified in review. Seven variants were computed, spanning maximally lenient to maximally strict combinations of gap-threshold and U3-row calibrations:

![Calibration sweep](img/chart6_sweep.png)

| Variant | Below floor | Conform | Exceeds floor | **Over-restrictive violations** |
|---|---|---|---|---|
| M0 published | 22 | 7 | 2 | **0** |
| M1 lenient gap | 22 | 7 | 2 | **0** |
| M2 strict gap | 23 | 7 | 1 | **0** |
| M3 floor minimized (uniform column) | 21 | 6 | 4 | **0** |
| M4 U3 row relaxed | 16 | 11 | 4 | **0** |
| M5 maximally lenient (M1+M4) | 15 | 12 | 4 | **0** |
| M6 maximally strict (M2+U3 strict) | 25 | 6 | 0 | **0** |

**Finding, stated flat:** the below-floor count ranges from 15 to 25 of 33 (45%–76%) across the full plausibility range of the calibration, and **over-restrictive violations are zero in every variant**. The one-directional skew is therefore **not an artifact of the published cutoffs**: there is no defensible calibration of the standard under which the corpus's non-conformity stops being permissive-leaning. The zero is also structurally intelligible rather than lucky: over-restriction only violates the standard when C_restrict > C_permit (denial hurts more than permission), and every decision in the corpus with that profile was resolved permissively anyway — the high-denial-harm cases (aducanumab, donanemab, molnupiravir, eteplirsen, marijuana research) are precisely the ones that went ahead. That is, the two-sided audit finds the system lenient where denial would hurt *and* lenient where hazard would hurt, which is a stronger and stranger statement than "too permissive": the corpus is permissive in **both** error directions. *Limitation marked:* the sweep varies the matrix but not the per-case P/I/D scores; a scorer-level Monte Carlo (perturbing each axis ±1) is the next layer and is not run here.

## Combined statement for the record

After v2's ten fixes and these three robustness upgrades, the corpus supports three flat statements: (i) the naive cost-bearer hypothesis is bivariately unsupported under either cost-bearer operationalization, and its caution condition is nearly unobserved (2–5 of 33 decisions); (ii) the permissive skew is real and calibration-robust — in the unselected drug frame (33.3% approval after negative votes), in the unselected EPA frame (34/34 continuations), and in the graded audit (15–25 below floor, 0 over, across all variants); (iii) restrictive movement against concentrated cost-bearers is gated by external forcing in 7 of 8 cases, reversed toward permissive in 3 of 9, and never reversed in the opposite direction within a decision's lifetime. What remains undiscriminated is mechanism: cost-bearer, unmet need, access mandate, advocacy, and legal architecture all predict overlapping parts of this pattern, and this corpus cannot rank them.

---

*Addendum, not advice. All artifacts delivered for reproduction.*
