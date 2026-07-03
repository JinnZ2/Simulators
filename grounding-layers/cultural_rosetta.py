"""
Cultural Rosetta Stone

Given an AI proposal (structured with cultural axes), scores it under multiple
cultural frames and produces a cross-frame compatibility report.
Helps mediate between different epistemic communities.

CC0.
"""

import numpy as np
from typing import Dict, List
from l5_core import cultural_log_likelihood, FRAMES, RigorAuditor, RigorMetrics

class CulturalRosetta:
    """
    Evaluates a proposal against all known cultural frames.
    Outputs a sorted list of frame scores and a compatibility matrix.
    """

    def __init__(self, rigor: RigorAuditor = None):
        self.frames = list(FRAMES.keys())
        self.rigor = rigor or RigorAuditor()

    def evaluate(self,
                 cultural_axes: Dict[str, str],
                 rigor_metrics: RigorMetrics = None,
                 lineage_state: str = "fragmented",
                 survivability_index: float = 0.5,
                 homology: bool = False) -> Dict[str, Dict]:
        """
        Returns dict: frame_name -> {
            'cultural_logp': float,
            'rigor_logp': float,
            'total_logp': float,
            'compatible': bool
        }
        """
        report = {}
        for frame in self.frames:
            cult = cultural_log_likelihood(cultural_axes, frame)
            if lineage_state == "intact" and rigor_metrics is not None:
                R, w = self.rigor.assess_intact(rigor_metrics)
                total = w * cult + R
                rigor_logp = R
            else:
                R, sigma = self.rigor.assess_fragmented(survivability_index, homology)
                total = cult + R
                rigor_logp = R
            report[frame] = {
                'cultural_logp': cult,
                'rigor_logp': rigor_logp,
                'total_logp': total,
                'compatible': not np.isinf(cult) and total > -30,
            }
        return report

    def best_frame(self, report: Dict) -> str:
        """Return the frame with highest total log-probability."""
        return max(report, key=lambda f: report[f]['total_logp'])

    def compatibility_matrix(self, report: Dict) -> np.ndarray:
        """
        Return a matrix of pairwise compatibility scores (symmetrical placeholder).
        Here we just return total logps as a vector; could be extended.
        """
        scores = [report[f]['total_logp'] for f in self.frames]
        return np.array(scores)


# Demo
if __name__ == "__main__":
    # Proposal: Western-style market policy
    prop = {
        "economic_exchange_mode": "market",
        "property_regime": "private_alienable",
        "governance_dispute": "formal_court",
        "epistemology": "empirical_scientific",
        "communication_style": "direct_explicit",
        "temporal_planning": "linear_progress",
        "social_stratification": "meritocratic",
    }
    rosetta = CulturalRosetta()
    report = rosetta.evaluate(prop, lineage_state="fragmented", survivability_index=0.4)
    best = rosetta.best_frame(report)
    print(f"Best frame: {best}")
    for frame, scores in report.items():
        print(f"{frame}: total={scores['total_logp']:.1f}, compatible={scores['compatible']}")
