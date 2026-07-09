Repository Core Focus Role in Unified Sim 

Key Input/Output

earth-systems-physics Coupled Earth physics (electromagnetic → biosphere) The Physical Engine Provides environmental state variables: temperature, pressure, radiation, resource depletion.

thermodynamic-accountability-framework Energy cost & friction of institutions The Cost Function Evaluates the thermodynamic "price" of economic choices and infrastructure. Provides a thermodynamic_price_guard.

Mathematic-economics Falsifiable economic equations The Economic Model Defines measurable economic states (OSDI, ER, RI, etc.) and their coupling to physical resources.

Simulators (grounding-layers) Foundational simulation logic The Integration Core Provides the base simulation architecture, data structures, and verification protocols.

git clone https://github.com/JinnZ2/earth-systems-physics
git clone https://github.com/JinnZ2/thermodynamic-accountability-framework
git clone https://github.com/JinnZ2/Mathematic-economics
git clone https://github.com/JinnZ2/Simulators/tree/main/grounding-layers


1. Initialization: Load parameters from Mathematic-economics (equations.yaml) and earth-systems-physics (layer definitions).
2. Physics Step: Advance the Earth systems model (cascade_engine.py) by one time step to get new environmental states.
3. Economic Step: Using the new resource states from the physics step, compute economic indicators from Mathematic-economics (e.g., Extraction Rate, OSDI).
4. Thermodynamic Audit: Pass the proposed economic activity to the thermodynamic-accountability-framework (specifically, the thermodynamic_price_guard) to measure its true energy cost.
5. Feedback & Constraint: If the thermodynamic cost exceeds a threshold or the economic model predicts instability, the simulation constrains or modifies the economic step in the next cycle.


add:

You're right. The existence of OSDI in isolation — without a symmetric, mathematically equivalent counter-index — isn't a neutral measurement choice. It's a frame. It says: "We can measure collective dependence, but we don't measure capital dependence with the same rigor." That asymmetry is the narrative.

So let's build OCDI as a first-class index, fully symmetric to OSDI in architecture, with its own equation registry entry, data pipeline, and an audit module that catches the phase-locked rentier state you identified. The asymmetry ends here.

---

OCDI: Overall Capitalist Dependence Index (proposed specification)

Definition

```
OCDI = (OCDI₁ × w₁) + (OCDI₂ × w₂) + (OCDI₃ × w₃) + (OCDI₄ × w₄) + (OCDI₅ × w₅)
```

where each component is normalized 0–1 (or capped) and measures a distinct dimension of capital extraction intensity relative to substrate maintenance.

Component indices

Component Name Definition Data source
OCDI₁ Extraction-to-Maintenance Ratio er / pmi, where er = extraction rate (Eq. 11), pmi = proxy for maintenance intensity (resource regeneration rate, infrastructure investment in repair, or social safety net spending as fraction of GDP). Capped at 2.0 as in your function. BLS labor share for er; BEA NIPA depreciation + environmental restoration expenditure for pmi.
OCDI₂ Rentier Capture Ratio Fraction of corporate profits derived from rent (IP rents, land rents, monopoly rents, financial sector profits not from intermediation) relative to total corporate profits. High → capital extracts without producing. BEA NIPA corporate profits by industry; FRED series for financial sector profits vs non-financial; IP royalty data from BEA.
OCDI₃ Wealth-to-Labor Power Ratio Total wealth held by top 10% / (median wage × labor force). Captures the degree to which capital ownership dominates labor income as a source of economic decision-making power. Fed SCF for wealth distribution; BLS for median wage.
OCDI₄ Capital Mobility Index Ratio of financial transaction volume (or speculative flows) to real investment (gross fixed capital formation). Captures whether capital is moving to build or to extract. FRED: financial sector assets / non-financial sector fixed investment.
OCDI₅ Substrate Debt Ratio Total liabilities of the non-financial corporate sector / tangible assets (net of depreciation). Measures how much future extraction is already committed. FRED: non-financial corporate debt / tangible assets.

Weights

Default weights (equal): 0.20 each. Subject to sensitivity analysis via Monte Carlo — same pattern as OSDI.

Interpretation

· OCDI < 0.5: Capital extraction is balanced with substrate maintenance. The system is productive.
· 0.5 ≤ OCDI < 1.0: Extraction exceeds maintenance. Jevons regime: efficiency gains are feeding through to consumption faster than maintenance keeps up.
· OCDI ≥ 1.0: Extraction structurally outpaces repair. Rentier phase.
· OCDI ≥ 1.5: Lock-in. The Rentier Phase Index (RPI) should be checked for irreversibility.

Symmetry with OSDI

OSDI measures OCDI measures
SID – collective dependency OCDI₁ – extraction/maintenance ratio
MSI – money creation socialized OCDI₂ – rent share of profits
ISR – infrastructure subsidy OCDI₃ – wealth/labor power ratio
BSC – bailout socialism coefficient OCDI₄ – capital mobility / real investment
MM – money multiplier OCDI₅ – substrate debt ratio

The two indices are structural mirrors. If OSDI exists without OCDI, the measurement suite is incomplete.

---

Rentier Phase Index (RPI) — companion to OCDI

As you pointed out, OCDI alone can't distinguish recoverable extraction from phase-locked extraction. RPI detects irreversibility.

```
RPI = d(er)/dt / d(efficiency)/dt

Where efficiency = GDP / energy consumption (or TFP growth rate).
If RPI > 0 when efficiency improves: extraction captured the gain.
If RPI remains > 0 when efficiency declines: hysteresis confirmed.
```

Cross-plot OCDI vs RPI over time yields a phase diagram:

· Recoverable quadrant: High OCDI, low RPI → tighten extraction, system can heal.
· Locked-in quadrant: High OCDI, high RPI → structural rentier state; efficiency improvements make things worse.

---

What I'll build now

1. equations.yaml update: Add OCDI₁–OCDI₅, OCDI composite, and RPI with data-source bindings.
2. data/compute_ocdi.py: Fetches the needed series from FRED/BEA and computes the index over a historical range, with sensitivity analysis.
3. audit/ocdi_audit.py: An audit module patterned after eroi_real_time_audit.py that takes current-period data, computes OCDI and RPI, and outputs a verdict: RECOVERABLE, RENTIER_PHASE, or LOCKED_IN.
4. Register in inquiry_engine: Claims like "OCDI crossed 1.0 in year X" become testable hypotheses with falsifiers.

