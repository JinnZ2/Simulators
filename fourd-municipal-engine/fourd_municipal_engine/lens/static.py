import re
import math
from typing import Dict, List, Tuple, Pattern

from fourd_municipal_engine.models.vectors import VectorSignature


class FourDLens:
    """
    Density-Normalized 4D Language-Aware Lens Engine.
    Analyzes linguistic manipulation vectors across D1-D4.
    """

    # --- Pre-compiled Regular Expressions ---

    # D1: Agency Routing Patterns
    D1_PATTERNS: List[Tuple[str, Pattern]] = [
        ("Passive Voice", re.compile(r'\b(?:was|were|is|are|been|being|be)\s+(\w+(?:ed|en|d|t))\b', re.I)),
        ("Passive Got", re.compile(r'\bgot\s+(\w+(?:ed|en|d|t))\b', re.I)),
        ("Agentless Nominalization", re.compile(r'\b(\w+(?:tion|sion|ment|ance|ence|ability|ization))\b', re.I)),
        ("Middle Voice", re.compile(r'\b(\w+)\s+(?:occurred|happened|took place|transpired)\b', re.I)),
        ("Expletive Subject", re.compile(r'\b(?:there\s+(?:is|are|was|were|has been|have been)|it\s+(?:is|was|seems|appears))\b', re.I)),
    ]

    # D2: Affective Impedance Patterns
    D2_PATTERNS: List[Tuple[str, Pattern]] = [
        ("Positive Amplifier", re.compile(r'\b(?:excellent|outstanding|amazing|incredible|wonderful|delighted|thrilled|exceptional|remarkable|fantastic|regrettable|unfortunate|challenging|difficult|concerned)\b', re.I)),
        ("Honorific Marker", re.compile(r'\b(?:esteemed|honorable|respected|distinguished|sir|madam|dr\.|prof\.)\b', re.I)),
        ("Emotional Injector", re.compile(r'\b(?:sadly|tragically|fortunately|unfortunately|alarmingly|must|urgent|critical|immediate)\b', re.I)),
        ("Punctuation Intensity", re.compile(r'!{1,}')),
        ("Affective Dampening", re.compile(r'\b(?:noted|acknowledged|observed|indicated|reported)\b', re.I)),
    ]

    # D3: Reality Construction Patterns
    D3_PATTERNS: List[Tuple[str, Pattern]] = [
        ("Reification", re.compile(r'\bthe\s+(\w+(?:tion|sion|ment|ity|ness|ance|ence))\s+(?:of|is|was)\b', re.I)),
        ("Binary Compression", re.compile(r'\b(?:either|or|versus|vs\.?|binary|dichotomy|left|right|red|blue|us|them)\b', re.I)),
        ("Evidentiality Weakener", re.compile(r'\b(?:suggests|indicates|appears to|seems to|may|might|could|data\s+shows|studies\s+indicate|research\s+suggests)\b', re.I)),
        ("Countable Reification", re.compile(r'\b(?:a|an|the|one|two|three|several|many|few)\s+(\w+(?:tion|sion|ment|ity))\b', re.I)),
    ]

    # D4: Iconic/Graphic Mass Patterns (Mutually Exclusive Rules)
    D4_PATTERNS: List[Tuple[str, Pattern]] = [
        ("Acronym Mass (3+ Caps)", re.compile(r'\b[A-Z]{3,}\b')),
        ("Capitalization Shift (2 Caps)", re.compile(r'\b[A-Z]{2}\b')),
        ("Title Case String", re.compile(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,}\b')),
        ("Punctuation Mass", re.compile(r'[!?]{2,}|[\.…]{3,}')),
        ("Quoted Mass", re.compile(r'["\'][^"\']+["\']')),
        ("Emoji Density", re.compile(r'[\U0001F300-\U0001F9FF]|:\w+:')),
    ]

    # Density saturation limits per 100 tokens (for normalization)
    SATURATION_THRESHOLDS = {
        'D1_agency': 15.0,
        'D2_affect': 12.0,
        'D3_reality': 12.0,
        'D4_iconic': 8.0,
    }

    def analyze(self, text: str) -> VectorSignature:
        """Runs text through density-normalized 4D analysis."""
        trace = []
        tokens = re.findall(r'\b\w+\b', text)
        token_count = max(len(tokens), 1)  # Prevent zero-division
        scale_factor = 100.0 / token_count # Normalize per 100 tokens

        raw_counts = {
            'D1_agency': self._process_patterns(text, self.D1_PATTERNS, 'D1', trace),
            'D2_affect': self._process_patterns(text, self.D2_PATTERNS, 'D2', trace),
            'D3_reality': self._process_patterns(text, self.D3_PATTERNS, 'D3', trace),
            'D4_iconic': self._process_patterns(text, self.D4_PATTERNS, 'D4', trace),
        }

        # Calculate density scores per 100 tokens
        dimension_scores = {
            k: round(v * scale_factor, 2)
            for k, v in raw_counts.items()
        }

        # Normalize against density saturation limits (0.0 to 1.0)
        normalized_scores = {
            k: min(round(dimension_scores[k] / self.SATURATION_THRESHOLDS[k], 3), 1.0)
            for k in dimension_scores
        }

        # Cognitive Energy Estimate: Entropy over vector distribution + total density
        total_density = sum(dimension_scores.values())
        energy_estimate = self._calculate_cognitive_energy(normalized_scores, total_density)

        # Composite Manipulation Index (Weighted vector field)
        manipulation_index = round(
            (normalized_scores['D1_agency'] * 0.35) +
            (normalized_scores['D2_affect'] * 0.30) +
            (normalized_scores['D3_reality'] * 0.20) +
            (normalized_scores['D4_iconic'] * 0.15),
            3
        )

        return VectorSignature(
            dimension_scores=dimension_scores,
            raw_counts=raw_counts,
            normalized_scores=normalized_scores,
            trace=trace,
            energy_estimate=round(energy_estimate, 2),
            manipulation_index=manipulation_index
        )

    def _process_patterns(self, text: str, patterns: List[Tuple[str, Pattern]], label: str, trace: List[str]) -> float:
        """Executes compiled patterns and logs matches."""
        total_matches = 0.0
        for pattern_name, regex in patterns:
            matches = regex.findall(text)
            if matches:
                count = len(matches)
                total_matches += count
                sample = matches[0] if isinstance(matches[0], str) else matches[0][0]
                trace.append(f"{label}: [{pattern_name}] x{count} -> '{sample}'")
        return total_matches

    def _calculate_cognitive_energy(self, normalized: Dict[str, float], total_density: float) -> float:
        """Calculates cognitive processing overhead based on vector variance and total density."""
        vals = list(normalized.values())
        mean = sum(vals) / len(vals)
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)

        # High friction occurs when density is high OR vector variance is imbalanced
        base_energy = (total_density * 0.05) + (variance * 2.0)
        return base_energy
