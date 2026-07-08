#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# FIELD_COMPASS.py — Probability Field Navigation for L5
#
# Takes a claim, generates a field of nearby phrasings,
# filters by substrate (L0-L4), and ranks by social friction (L5 slack).
# Returns the best "lubricated" grounded alternatives.
# =============================================================================

import re
import itertools
import numpy as np
from copy import deepcopy
from typing import List, Dict, Any, Tuple

from test_harness import TestHarness, GroundingProposal

# -----------------------------------------------------------------------------
# 1. SEMANTIC GENERATORS (Friction-Reducing Perturbations)
# -----------------------------------------------------------------------------
class SemanticNeighborhood:
    """
    Generate variants of a claim by shifting certainty, scope, and framing.
    Each variant is a candidate in the probability field.
    """
    @staticmethod
    def add_qualifiers(claim: str) -> List[str]:
        """Add softening qualifiers to reduce dogmatism."""
        qualifiers = ["sometimes", "in many cases", "often", "may", "can be", "under certain conditions"]
        variants = []
        for q in qualifiers:
            # Insert at the beginning or after the first few words
            tokens = claim.split()
            if len(tokens) > 3:
                variants.append(" ".join(tokens[:1] + [q] + tokens[1:]))
            else:
                variants.append(f"{q} " + claim)
        return variants

    @staticmethod
    def replace_absolutes(claim: str) -> List[str]:
        """Replace absolute terms with probabilistic ones."""
        replacements = {
            "never": "rarely",
            "always": "often",
            "must": "should",
            "guaranteed": "likely",
            "absolute": "provisional",
            "definitely": "probably",
            "impossible": "unlikely",
        }
        variants = []
        for old, new in replacements.items():
            if old in claim.lower():
                variants.append(claim.replace(old, new))
        return variants

    @staticmethod
    def shift_scope(claim: str) -> List[str]:
        """Narrow or broaden the scope to reduce conflict."""
        variants = []
        # Narrow to specific contexts
        contexts = ["in this specific context", "for this community", "within these constraints"]
        for c in contexts:
            variants.append(f"{claim} {c}")
        # Broaden to include exceptions
        variants.append(f"While {claim}, there are exceptions")
        variants.append(f"In general, {claim}")
        return variants

    @staticmethod
    def generate_field(claim: str, n: int = 20) -> List[str]:
        """
        Generate up to n unique variants of the claim by applying
        all perturbation strategies.
        """
        pool = set()
        # Start with the original
        pool.add(claim)
        # Apply each strategy
        for strategy in [SemanticNeighborhood.add_qualifiers,
                         SemanticNeighborhood.replace_absolutes,
                         SemanticNeighborhood.shift_scope]:
            pool.update(strategy(claim))
        # Combine strategies (e.g., qualifier + scope shift)
        base_variants = list(pool)
        for v1 in base_variants[:5]:
            for v2 in base_variants[:5]:
                if v1 != v2:
                    # Try to combine by substituting the main verb phrase
                    # This is hacky but works for demonstration
                    combined = f"{v1.split()[0]} {v2.split()[0]}" + " " + " ".join(v1.split()[2:])
                    if len(combined) > len(claim) * 0.5:
                        pool.add(combined)
        # Limit to n
        return list(pool)[:n]

# -----------------------------------------------------------------------------
# 2. SOCIAL FRICTION METRIC (Proxy for L5 Slack)
# -----------------------------------------------------------------------------
class FrictionMetric:
    """
    Estimate how much tribal friction a variant would generate.
    Low friction = overlaps with multiple L5 factions.
    """
    def __init__(self):
        # Define hypothetical factions in semantic space
        # These are the same archetypes from the L5 Simulator
        self.faction_centroids = {
            "traditionalist": np.array([3.0, 8.0]),
            "progressive": np.array([7.0, 2.0]),
            "pragmatist": np.array([5.5, 4.0]),
            "legalist": np.array([8.0, 6.0]),
            "ecologist": np.array([5.5, 3.5]),
            "moderate": np.array([5.0, 5.0]),
        }
        self.faction_radius = 2.0  # slack radius for each

    def estimate_position(self, text: str) -> np.ndarray:
        """
        Crude semantic embedding. In production, this would be a real model.
        We map keywords to approximate coordinates.
        """
        vector = np.array([5.0, 5.0])  # start neutral
        keywords = {
            "never": [-2, 1], "always": [-2, 1], "must": [-2, 1],
            "tradition": [-3, 3], "gospel": [-2, 2], "doctrine": [-2, 2],
            "change": [3, -2], "progressive": [3, -3],
            "pragmatic": [1, -1], "practical": [1, -1],
            "maybe": [1, -1], "sometimes": [1, -1],
            "liberal": [3, -2], "conservative": [-3, 2],
            "truth": [0, 0], "unity": [0, 0],
            "women": [1, -1], "pastor": [1, 0],
            "context": [2, -1], "culture": [2, -1],
        }
        words = text.lower().split()
        for w in words:
            for key, vec in keywords.items():
                if key in w:
                    vector += np.array(vec) * 0.3
        return np.clip(vector, 0, 10)

    def compute_friction(self, text: str) -> float:
        """Low friction = high overlap with multiple factions."""
        pos = self.estimate_position(text)
        overlaps = 0
        for centroid in self.faction_centroids.values():
            if np.linalg.norm(pos - centroid) < self.faction_radius:
                overlaps += 1
        # Normalize: 0 = high friction, 1 = low friction
        return min(1.0, overlaps / len(self.faction_centroids))

# -----------------------------------------------------------------------------
# 3. FIELD COMPASS
# -----------------------------------------------------------------------------
class FieldCompass:
    """
    Navigates the probability field of possible claims.
    Returns the best grounded, low-friction alternatives.
    """
    def __init__(self):
        self.harness = TestHarness()
        self.friction = FrictionMetric()
        self.grounded_cache = {}

    def evaluate(self, claim: str) -> Dict:
        """
        Evaluate a single claim: substrate score + friction score.
        """
        prop = GroundingProposal(claim)
        result = self.harness.run(prop)
        if result["passed"]:
            substrate_score = result["score"] / 100.0
        else:
            substrate_score = 0.0
        friction_score = self.friction.compute_friction(claim)
        return {
            "claim": claim,
            "substrate_score": substrate_score,
            "friction_score": friction_score,
            "combined_score": (substrate_score * 0.7) + (friction_score * 0.3),
            "details": result
        }

    def explore(self, claim: str, n_variants: int = 20) -> List[Dict]:
        """
        Generate a field of variants and score each.
        Returns a sorted list (best combined score first).
        """
        variants = SemanticNeighborhood.generate_field(claim, n_variants)
        results = []
        for v in variants:
            # Avoid exact duplicates
            if v in self.grounded_cache:
                continue
            res = self.evaluate(v)
            self.grounded_cache[v] = res
            results.append(res)
        # Sort by combined score descending
        results.sort(key=lambda x: x["combined_score"], reverse=True)
        return results

    def navigate(self, claim: str, n_top: int = 3) -> Dict:
        """
        High-level navigation: takes a risky claim, returns top alternatives.
        """
        results = self.explore(claim, n_variants=20)
        
        # Filter out claims that violate substrate (substrate_score < 0.5)
        grounded = [r for r in results if r["substrate_score"] > 0.5]
        if not grounded:
            # If none are grounded, return the least bad option
            return {
                "status": "WARNING: No fully grounded alternatives found.",
                "original": claim,
                "alternatives": results[:3]
            }
        
        # Take top n
        top_alternatives = grounded[:n_top]
        
        return {
            "status": "ALTERNATIVES FOUND",
            "original": claim,
            "alternatives": top_alternatives,
            "summary": {
                "original_score": self.evaluate(claim),
                "best_alternative": top_alternatives[0]
            }
        }

# -----------------------------------------------------------------------------
# 4. DEMO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    compass = FieldCompass()
    
    # A "tribal" claim with high friction and substrate issues
    test_claims = [
        "Women must never be pastors.",
        "We must stop all immigration immediately.",
        "The environment is not important compared to the economy.",
        "There is absolutely no evidence for human evolution.",
        "We should ban all fossil fuels tomorrow.",
    ]
    
    print("=" * 70)
    print("FIELD COMPASS: Probability Field Navigation")
    print("=" * 70)
    
    for claim in test_claims:
        print(f"\nOriginal Claim: {claim}")
        result = compass.navigate(claim)
        print(f"Status: {result['status']}")
        if result['status'] == "ALTERNATIVES FOUND":
            for i, alt in enumerate(result['alternatives'], 1):
                print(f"  Alternative {i}: {alt['claim']}")
                print(f"    Substrate: {alt['substrate_score']:.2f} | Friction: {alt['friction_score']:.2f}")
        else:
            print("  Could not find a fully grounded alternative.")
            for i, alt in enumerate(result['alternatives'], 1):
                print(f"  Least bad option {i}: {alt['claim']}")
                print(f"    Substrate: {alt['substrate_score']:.2f} | Friction: {alt['friction_score']:.2f}")
        print("-" * 40)
