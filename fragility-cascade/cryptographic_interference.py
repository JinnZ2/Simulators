#!/usr/bin/env python3
"""
cryptographic_interference.py

Measures cryptographic signatures in text and maps them to interference axes.
- Entropy (letter frequency distribution)
- Redundancy (predictability)
- Syntactic structure (n‑gram patterns)
- Steganographic markers (anomalous patterns)
"""

import math
import re
from collections import Counter
from typing import Dict, List

class CryptographicInterference:
    def __init__(self):
        self.english_freq = {
            'e': 0.127, 't': 0.091, 'a': 0.082, 'o': 0.075, 'i': 0.070,
            'n': 0.067, 's': 0.063, 'h': 0.061, 'r': 0.060, 'd': 0.043,
            'l': 0.040, 'c': 0.028, 'u': 0.028, 'm': 0.024, 'w': 0.023,
            'f': 0.022, 'g': 0.020, 'y': 0.020, 'p': 0.019, 'b': 0.015,
            'v': 0.010, 'k': 0.008, 'j': 0.002, 'x': 0.002, 'q': 0.001,
            'z': 0.001
        }

    def shannon_entropy(self, text: str) -> float:
        """Character-level Shannon entropy."""
        text = text.lower()
        if not text:
            return 0.0
        counts = Counter(text)
        total = len(text)
        entropy = 0.0
        for c, n in counts.items():
            p = n / total
            entropy -= p * math.log2(p)
        return entropy

    def redundancy(self, text: str) -> float:
        """Syntactic redundancy (predictability). Simplified: n‑gram repetition."""
        words = re.findall(r'\b\w+\b', text.lower())
        if len(words) < 2:
            return 0.0
        # Count repeated n‑grams (2‑grams)
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        unique = len(set(bigrams))
        total = len(bigrams)
        if total == 0:
            return 0.0
        return 1.0 - (unique / total)

    def entropy_deviation(self, text: str) -> float:
        """Deviation of character frequency from English baseline."""
        text = text.lower()
        counts = Counter(text)
        total = len(text)
        if total == 0:
            return 0.0
        deviation = 0.0
        for c, freq in self.english_freq.items():
            observed = counts.get(c, 0) / total
            deviation += abs(observed - freq)
        # Normalize by baseline sum (≈1.0)
        baseline_sum = sum(self.english_freq.values())
        return min(1.0, deviation / baseline_sum)

    def detect_anomaly(self, text: str) -> float:
        """
        Steganographic marker: sections with unusual entropy or word length.
        """
        # Split into sentences and look for entropy variance
        sentences = re.split(r'[.!?]', text)
        entropies = [self.shannon_entropy(s) for s in sentences if s.strip()]
        if len(entropies) < 2:
            return 0.0
        # High variance → possible steganography
        mean = sum(entropies) / len(entropies)
        variance = sum((e - mean)**2 for e in entropies) / len(entropies)
        return min(1.0, variance / 2.0)

    def interference_profile(self, text: str) -> Dict[str, float]:
        """
        Map cryptographic metrics to interference axes.
        """
        entropy = self.shannon_entropy(text)
        redundancy = self.redundancy(text)
        deviation = self.entropy_deviation(text)
        anomaly = self.detect_anomaly(text)

        # Interpret:
        # - Low entropy + high redundancy → α (scaling collapse)
        # - High entropy + high deviation → s (synthetic accumulation)
        # - High anomaly → λ (kernel drift)
        # - Deviation from English → δ (reciprocity skew)

        return {
            "α (scaling)": 1.0 - min(1.0, entropy / 5.0),  # low entropy → high α
            "λ (kernel)": anomaly,
            "δ (reciprocity)": min(1.0, deviation * 0.5),
            "γ (damping)": min(1.0, redundancy * 0.5),
            "s (synthetic)": min(1.0, (entropy / 5.0) * (1.0 + deviation)),
            "h/ξ (entrainment)": min(1.0, (deviation + redundancy) / 2.0),
        }

def main():
    print("\n" + "=" * 70)
    print("CRYPTOGRAPHIC INTERFERENCE — Entropy, Redundancy, Anomaly")
    print("=" * 70)

    examples = [
        ("Natural English", "The cat sat on the mat. It was a sunny day."),
        ("AI‑Generated", "The cat sat on the mat in a very sunny and bright day."),
        ("Manipulative", "You always do this. Everyone knows it. It's completely your fault."),
        ("Cryptic", "Xyzl mq b kpq. Wkh vhfuhw lv klgghq."),
        ("WEIRD Academic", "The epistemological implications of recursive self-reference are fundamentally intertwined with the phenomenological constraints of qualia."),
    ]

    detector = CryptographicInterference()

    for label, text in examples:
        print(f"\n--- {label} ---")
        print(f"Text: {text[:50]}...")
        entropy = detector.shannon_entropy(text)
        redundancy = detector.redundancy(text)
        deviation = detector.entropy_deviation(text)
        anomaly = detector.detect_anomaly(text)

        print(f"  Entropy: {entropy:.3f} bits/char")
        print(f"  Redundancy: {redundancy:.3f}")
        print(f"  Entropy deviation: {deviation:.3f}")
        print(f"  Anomaly (steganographic): {anomaly:.3f}")

        print("  Interference profile:")
        profile = detector.interference_profile(text)
        for axis, val in profile.items():
            bar = "█" * int(val * 20)
            print(f"    {axis:>12}: {val:.2f} {bar}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Natural English has moderate entropy (~4.0) and low redundancy.")
    print("  • AI‑generated text often has lower entropy and higher redundancy.")
    print("  • Manipulative text has high redundancy and high deviation.")
    print("  • Cryptic text has high entropy and high anomaly.")
    print("  • Cryptographic interference is measurable and maps to collapse axes.")
    print("=" * 70)

if __name__ == "__main__":
    main()
