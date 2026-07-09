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



1. equations.yaml update: Add OCDI₁–OCDI₅, OCDI composite, and RPI with data-source bindings.
2. data/compute_ocdi.py: Fetches the needed series from FRED/BEA and computes the index over a historical range, with sensitivity analysis.
3. audit/ocdi_audit.py: An audit module patterned after eroi_real_time_audit.py that takes current-period data, computes OCDI and RPI, and outputs a verdict: RECOVERABLE, RENTIER_PHASE, or LOCKED_IN.
4. Register in inquiry_engine: Claims like "OCDI crossed 1.0 in year X" become testable hypotheses with falsifiers.

add:

#!/usr/bin/env python3
"""
Register OCDI claims in the inquiry engine for the lifecycle workbench.
Run once to add these claims to claims_registry.json.
CC0.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inquiry_engine.claim_lifecycle import ClaimLifecycle, ClaimRegistry

OCDI_CLAIMS = [
    {
        "id": "OCDI_001",
        "statement": "OCDI crossed 1.0 (rentier phase) before the year 2000.",
        "falsifier": "Show OCDI < 1.0 for all years 1950-2000 using audited data from compute_ocdi.py.",
        "test_procedure": {
            "module": "data.compute_ocdi",
            "function": "run_historical",
            "args": {"start": 1950, "end": 2000}
        },
    },
    {
        "id": "OCDI_002",
        "statement": "The US economy entered the locked-in phase (OCDI > 1.5, RPI > 0) by 2020.",
        "falsifier": "Show OCDI < 1.5 or RPI < 0 for any year 2010-2026 using audited data.",
        "test_procedure": {
            "module": "data.compute_ocdi",
            "function": "run_historical",
            "args": {"start": 2010, "end": 2026}
        },
    },
    {
        "id": "OCDI_003",
        "statement": "OSDI exists without a symmetric OCDI in economic measurement frameworks.",
        "falsifier": "Demonstrate an existing, widely-used index that measures capital extraction intensity relative to substrate maintenance with comparable mathematical rigor to OSDI.",
        "test_procedure": None,  # Manual review claim
    },
    {
        "id": "OCDI_004",
        "statement": "The phase-locked rentier state is irreversible under current institutional arrangements.",
        "falsifier": "Show a sustained decline in OCDI (≥0.2 drop over 5+ years) without a systemic crisis or institutional overhaul.",
        "test_procedure": {
            "module": "data.compute_ocdi",
            "function": "run_historical",
            "args": {"start": 1950, "end": 2026}
        },
    },
]

def register():
    registry = ClaimRegistry()
    for claim_data in OCDI_CLAIMS:
        claim = ClaimLifecycle(
            claim_id=claim_data["id"],
            statement=claim_data["statement"],
            falsifier=claim_data["falsifier"],
            test_procedure=claim_data.get("test_procedure"),
        )
        claim.propose(proposed_by="OCDI-framework-builder")
        claim.under_review()
        claim.activate()
        registry.add(claim)
        print(f"Registered {claim.claim_id}: {claim.statement[:60]}...")
    print(f"\nTotal OCDI claims registered: {len(OCDI_CLAIMS)}")

if __name__ == "__main__":
    register()



    
