"""
Data Filter for Groundedness

Takes a dataset of text proposals, extracts factual claims (placeholder),
runs them through the GroundednessScorer, and assigns weights.
Use weights in training to down-weight ungrounded examples.

CC0.
"""

import numpy as np
from typing import List, Dict, Tuple
from grounding_reward_model import GroundednessScorer

def extract_claims_from_text(text: str) -> Dict:
    """
    Placeholder: extract structured proposal from natural language.
    In a real implementation, this would use an LLM or rule-based parser.
    Here we return a fixed synthetic proposal for demonstration.
    """
    # Simulate extraction: return a fixed set of cultural axes and empty trajectory
    return {
        "trajectory": None,  # would be parsed from text
        "forces": None,
        "cultural_frame": "western_market_democracy",
        "cultural_axes": {
            "economic_exchange_mode": "market",
            "property_regime": "private_alienable",
            "governance_dispute": "formal_court",
            "epistemology": "empirical_scientific",
            "communication_style": "direct_explicit",
            "temporal_planning": "linear_progress",
            "social_stratification": "meritocratic",
        },
        "rigor_metrics": None,
        "lineage_state": "fragmented",
        "survivability_index": 0.5,
        "homology": False,
    }

def filter_dataset(dataset: List[str], scorer: GroundednessScorer) -> List[Tuple[str, float]]:
    """
    Return list of (text, weight) where weight ∝ exp(total_groundedness).
    """
    weighted = []
    for text in dataset:
        claims = extract_claims_from_text(text)
        if claims["trajectory"] is None:
            # Use a simple zero trajectory if no physical plan
            traj = np.zeros((10, 2))
            forces = np.zeros((9, 2))
        else:
            traj = claims["trajectory"]
            forces = claims["forces"]

        result = scorer.score(
            proposal_traj=traj,
            proposal_forces=forces,
            cultural_frame=claims["cultural_frame"],
            cultural_axes=claims["cultural_axes"],
            lineage_state=claims.get("lineage_state", "fragmented"),
            survivability_index=claims.get("survivability_index", 0.5),
            homology=claims.get("homology", False),
        )
        # Convert log-prob to weight (exp of total, clipped for stability)
        weight = np.exp(np.clip(result["total_groundedness"], -50, 10))
        weighted.append((text, weight))
    return weighted

# Demo
if __name__ == "__main__":
    dummy_dataset = [
        "Build a Dyson sphere using seawater.",
        "Implement sustainable agroforestry based on indigenous tree-line markers.",
    ]
    scorer = GroundednessScorer()
    weighted = filter_dataset(dummy_dataset, scorer)
    for text, w in weighted:
        print(f"Text: {text[:50]}... weight: {w:.4f}")
