# inquiry_engine/register_fermi_claims.py
from inquiry_engine.claim_lifecycle import ClaimLifecycle, ClaimRegistry

FERMI_CLAIMS = [
    {
        "id": "FERMI_001",
        "statement": "Dyson sphere construction is a self-terminating trajectory under any physically plausible energy budget, once full-stack thermodynamic costs and cascade risks from higher-order interactions are included.",
        "falsifier": "Demonstrate a completed Dyson sphere (or equivalent megastructure) with lifecycle EROI > 1, accounting for: (1) embodied energy of all collector elements, (2) launch/deployment energy, (3) maintenance energy against degradation, (4) waste heat management, (5) complexity overhead scaling as population^1.2, and (6) cascade risk from triplet coupling reduction (70% threshold).",
        "test_procedure": {
            "module": "fermi_paradox_audit",
            "function": "run_simulation",
            "args": {"expansion_rate": 0.10, "horizon": 300}
        },
    },
    {
        "id": "FERMI_002",
        "statement": "The Fermi paradox is explained by civilizations that understand the thermodynamic constraint stack choosing not to expand beyond their scale ceiling (SCI > 1).",
        "falsifier": "Find an expanding civilization with SCI < 1 that survives more than 500 years without either collapsing or voluntarily contracting to below its scale ceiling.",
        "test_procedure": None,  # Requires astronomical observation
    },
    {
        "id": "FERMI_003",
        "statement": "Indigenous economic systems (Aboriginal, Ainu, Sámi, Ubuntu, Potlatch) encode the post-filter survival strategy: maintain SCI > 1, keep OCDI negative, preserve relational trust.",
        "falsifier": "Show that any of these systems, when exposed to expansion-capable technology, chose to expand beyond their scale ceiling without external coercion.",
        "test_procedure": None,  # Historical/ethnographic review
    },
]

def register():
    registry = ClaimRegistry()
    for cd in FERMI_CLAIMS:
        claim = ClaimLifecycle(
            claim_id=cd["id"],
            statement=cd["statement"],
            falsifier=cd["falsifier"],
            test_procedure=cd.get("test_procedure"),
        )
        claim.propose(proposed_by="Fermi-Dyson-audit")
        claim.under_review()
        claim.activate()
        registry.add(claim)
    print(f"Registered {len(FERMI_CLAIMS)} Fermi-paradox claims.")

if __name__ == "__main__":
    register()
