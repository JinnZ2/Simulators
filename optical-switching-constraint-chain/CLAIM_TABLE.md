# CLAIM TABLE: optical-switching-constraint-chain

Claims about `SOURCE_DROP.md` (Kimi / OKComputer) and what can be checked
from here. Status is SUPPORTED, REFUTED or UNVERIFIED. "Search depth" means
checked against search-result text, not the primary document.

| id | claim | status | basis | falsifier |
|---|---|---|---|---|
| OSC_001 | The §3.1 stripe-period table and the four §6.2 Δ = 60 crossing sizes reproduce from the stated formulas and parameters, each within 2%. | SUPPORTED | `check.py` sections 1–2 | A different reading of the Kaplan–Gehring form that the report's numbers match more closely. |
| OSC_002 | At the report's own parameters, the stripe period first drops below the 1.5 µm top of its stated spot band at N = 11 (1.06 µm). At N = 10 it is 1.60 µm. The report says the crash comes "precisely at N ≈ 9–10", and the experiment loses deterministic writing at N = 10. | SUPPORTED | `check.py` section 1 | A stated spot scale above 1.6 µm, which the report does not give. |
| OSC_003 | Read as confirmation, the model's agreement with the experiment is a fit, not a test. Over Ms 0.8–1.0 MA/m, Keff 0.3–0.7 MJ/m³ and A 10–20 pJ/m, the crossover against a 1.36 µm spot runs from N = 5 to N = 21. The report's own caveat says the N = 9 period spans 0.13 µm to 2.5 mm. | SUPPORTED | `check.py` envelope; the parameter box is this audit's choice, stated | Independent measurements of Ms, Keff and A for this stack that pin the crossover. |
| OSC_004 | The energy-per-bit values in §7.2 do not follow from the stated fluence, spot and pulse count. The implied absorbed fractions are 0.35, 0.35 and 0.60, and none is stated. | SUPPORTED | `check.py` section 3, disc spot area | A stated absorptance per row, or a spot geometry that reproduces the values. |
| OSC_005 | The UCSD energy row uses 7.6 µJ/cm². The report's own §5 table gives the Co/Pt switching threshold as 1.9–17 mJ/cm², 250–2,237× higher. The 7.6 µJ/cm² value is cited from a different single-shot experiment, not from the UCSD paper. | SUPPORTED | `check.py` section 3; text of §1.2 and §5 | The UCSD paper reporting a µJ/cm²-class fluence. |
| OSC_006 | 6 J/cm³ over a 40×40×20 nm³ cell is 192 aJ, not the stated 120 aJ. The "~24 aJ for a 20-nm-class bit" follows from 6 J/cm³ only for a 20×20×10 nm³ cell. | SUPPORTED | `check.py` section 3 | Kimel & Li stating a lower density or a different cell. The value is carried, not read. |
| OSC_007 | "At a 30 nm bit side every configuration in the figure sits at Δ = 350–1300" holds for the three Co/Pt curves only. The FePt curve in the same figure is at about 8,500. | SUPPORTED | `check.py` section 2; fig2 inspected | — |
| OSC_008 | One bit surviving ten years needs Δ = ln(t/τ₀) = 40.3–42.6 for τ₀ = 10⁻⁹–10⁻¹⁰ s. The §6.4 decision table's "marginal 40–60" band is therefore where a single bit already lasts ten years. The 60 line is a population criterion. | SUPPORTED | `check.py` section 4 | — |
| OSC_009 | Figure references are offset: the text's Figure 1 (phase map) is file `fig6`, and Figures 2–6 are files `fig1`–`fig5`. | SUPPORTED | `check.py` section 5 | — |
| OSC_010 | The report's load-bearing open item holds as a structure: no measured Δ of an optically written bit is cited. The anchor paper exists, but the depinning precedent (arXiv:1312.7301) was not located, and the other roughly 30 citations are unchecked. | UNVERIFIED | `check.py` section 6, search depth | A located Sharrock or decay measurement on an optically written bit, which would close the gap the report names. |
