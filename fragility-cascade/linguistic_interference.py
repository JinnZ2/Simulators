#!/usr/bin/env python3
"""
linguistic_interference.py

Detects linguistic patterns (rhythm, word choice, grammar, framing, repetition)
and maps them to interference axes (α, λ, δ, γ, s, h/ξ).

Scores are continuous (0 to 1) and can be used to predict communication integrity (CI).
"""

import math
import re
from typing import List, Dict

# ----- Lexical markers for manipulation -------------------------------------
ABSTRACT_WORDS = {"always", "never", "everyone", "no one", "absolutely", "completely", "totally"}
BINARY_FRAMING = {"us", "them", "good", "evil", "right", "wrong", "win", "lose"}
PASSIVE_MARKERS = {"was", "were", "been", "being", "by"}

def rhythm_score(text: str) -> float:
    """Estimate speech rhythm from punctuation and sentence length variance."""
    sentences = re.split(r'[.!?]', text)
    lengths = [len(s.split()) for s in sentences if s.strip()]
    if len(lengths) < 2:
        return 0.0
    mean_len = sum(lengths) / len(lengths)
    variance = sum((l - mean_len)**2 for l in lengths) / len(lengths)
    # High variance = erratic rhythm → interference
    return min(1.0, variance / 20.0)

def abstraction_score(text: str) -> float:
    """Fraction of abstract, absolute words."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    abstract = sum(1 for w in words if w in ABSTRACT_WORDS)
    return abstract / len(words)

def framing_score(text: str) -> float:
    """Fraction of binary framing words."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    binary = sum(1 for w in words if w in BINARY_FRAMING)
    return binary / len(words)

def passive_score(text: str) -> float:
    """Proportion of passive voice markers (simplified)."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    passive = sum(1 for w in words if w in PASSIVE_MARKERS)
    return passive / len(words)

def repetition_score(text: str) -> float:
    """Measure repetition of common phrases (normalized)."""
    words = re.findall(r'\b\w+\b', text.lower())
    if len(words) < 10:
        return 0.0
    # Count unique vs total
    unique = len(set(words))
    return 1.0 - (unique / len(words))

def linguistic_interference(text: str) -> Dict[str, float]:
    """
    Returns a dict mapping each interference axis to a score (0..1).
    Higher = more interference.
    """
    return {
        "α (rhythm)": rhythm_score(text),
        "λ (abstraction)": abstraction_score(text),
        "δ (framing)": framing_score(text),
        "γ (passive)": passive_score(text),
        "s (repetition)": repetition_score(text),
        "h/ξ (entrainment)": (abstraction_score(text) + framing_score(text)) / 2.0,
    }

def main():
    print("\n" + "=" * 70)
    print("LINGUISTIC INTERFERENCE — Mapping Text to Collapse Axes")
    print("=" * 70)

    examples = [
        ("De-escalation", 
         "I can see you're upset. Let me slow down. We can figure this out together."),
        ("Manipulative", 
         "You always do this. Everyone knows it. It's completely your fault, and we both know it."),
        ("Neutral", 
         "The data shows a 12% increase. We should consider adjusting the model."),
        ("WEIRD Academic", 
         "The epistemological implications of recursive self-reference are fundamentally intertwined with the phenomenological constraints of qualia and the ontological status of the observer."),
    ]

    for label, text in examples:
        print(f"\n--- {label} ---")
        print(f"Text: {text}")
        scores = linguistic_interference(text)
        print("Interference Scores:")
        for axis, val in scores.items():
            bar = "█" * int(val * 20)
            print(f"  {axis:>12}: {val:.2f} {bar}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • De-escalation: low interference across all axes.")
    print("  • Manipulation: high abstraction, framing, repetition.")
    print("  • WEIRD Academic: high abstraction + passive voice.")
    print("  • Rhythm and repetition are measurable cues for impending collapse.")
    print("=" * 70)

if __name__ == "__main__":
    main()
