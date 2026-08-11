import re
import math
from typing import Dict, List, Optional, Tuple, Pattern

from fourd_municipal_engine.models.vectors import (
    Genre,
    GENRE_PROFILES,
    ContextRule,
    DynamicVectorSignature,
)


class DynamicFourDLens:
    """
    4D Language Lens with Dynamic Word Interpretation and Genre Baseline Calibration.
    """

    def __init__(self, default_genre: Genre = Genre.GENERAL):
        self.default_genre = default_genre
        self._init_context_rules()

    def _init_context_rules(self):
        """Contextual rules evaluating target terms based on word choice, order, and neighboring tokens."""
        self.context_rules: List[ContextRule] = [
            # 1. "Critical" / "Urgent" / "Fatal" - Mechanical state vs. PR Emotional Injector
            ContextRule(
                pattern=re.compile(r'\b(?:critical|urgent|fatal|severe|failure)\b', re.I),
                target_dimension='D2_affect',
                genre_multipliers={
                    Genre.TECHNICAL_REPORT: 0.1,  # Technical system state -> benign
                    Genre.CORPORATE_PR: 1.8,       # PR urgency injection -> high manipulation
                    Genre.LEGAL_CONTRACT: 0.5,
                    Genre.GENERAL: 1.0
                },
                qualifying_context={'section', 'error', 'temperature', 'failure', 'path', 'state', 'load', 'log', 'threshold'}
            ),

            # 2. "Executed" / "Terminated" - Legal/Tech mechanical execution vs. Human violence/harm
            ContextRule(
                pattern=re.compile(r'\b(?:executed|terminated|dissolved|liquidated)\b', re.I),
                target_dimension='D1_agency',
                genre_multipliers={
                    Genre.LEGAL_CONTRACT: 0.2,    # Standard contractual execution
                    Genre.TECHNICAL_REPORT: 0.2,  # Process lifecycle
                    Genre.CORPORATE_PR: 1.5,      # Euphemistic workforce firing
                    Genre.GENERAL: 1.0
                },
                qualifying_context={'contract', 'agreement', 'process', 'thread', 'function', 'duty', 'asset'}
            ),

            # 3. Normative Modal Deontics ("shall be", "must be") - Legal obligation vs. Rhetorical pressure
            ContextRule(
                pattern=re.compile(r'\b(?:shall|must|is required to)\s+be\s+(\w+(?:ed|en|d|t))\b', re.I),
                target_dimension='D1_agency',
                genre_multipliers={
                    Genre.LEGAL_CONTRACT: 0.2,    # Normative obligation structural standard
                    Genre.CORPORATE_PR: 1.6,       # Unilateral institutional mandate
                    Genre.TECHNICAL_REPORT: 0.5,
                    Genre.GENERAL: 1.0
                }
            ),

            # 4. Agentless Operational Euphemisms ("Realignment", "Optimization", "Restructuring")
            ContextRule(
                pattern=re.compile(r'\b(?:realignment|optimization|restructuring|downsizing|reorganization)\b', re.I),
                target_dimension='D3_reality',
                genre_multipliers={
                    Genre.CORPORATE_PR: 2.0,       # Reification of harm into administrative abstraction
                    Genre.TECHNICAL_REPORT: 0.8,
                    Genre.LEGAL_CONTRACT: 0.6,
                    Genre.GENERAL: 1.2
                }
            )
        ]

        # Base pattern registries (compiled)
        self.D1_BASE = [
            ("Passive Voice", re.compile(r'\b(?:was|were|is|are|been|being|be)\s+(\w+(?:ed|en|d|t))\b', re.I)),
            ("Agentless Nominalization", re.compile(r'\b(\w+(?:tion|sion|ment|ance|ence|ability|ization))\b', re.I)),
            ("Expletive Subject", re.compile(r'\b(?:there\s+(?:is|are|was|were)|it\s+(?:is|was|seems))\b', re.I)),
        ]

        self.D2_BASE = [
            ("Positive Amplifier", re.compile(r'\b(?:excellent|outstanding|amazing|delighted|thrilled|exceptional)\b', re.I)),
            ("Emotional Injector", re.compile(r'\b(?:sadly|tragically|fortunately|alarmingly|immediate)\b', re.I)),
            ("Punctuation Intensity", re.compile(r'!{1,}')),
        ]

        self.D3_BASE = [
            ("Reification", re.compile(r'\bthe\s+(\w+(?:tion|sion|ment|ity|ness))\s+(?:of|is|was)\b', re.I)),
            ("Binary Compression", re.compile(r'\b(?:either|or|versus|vs\.?|binary|us|them)\b', re.I)),
            ("Evidentiality Weakener", re.compile(r'\b(?:suggests|indicates|appears to|seems to|may|might)\b', re.I)),
        ]

        self.D4_BASE = [
            ("Acronym Mass", re.compile(r'\b[A-Z]{3,}\b')),
            ("Punctuation Mass", re.compile(r'[!?]{2,}|[\.…]{3,}')),
            ("Emoji Density", re.compile(r'[\U0001F300-\U0001F9FF]|:\w+:')),
        ]

    def analyze(self, text: str, genre: Optional[Genre] = None) -> DynamicVectorSignature:
        """Analyzes text using genre calibration and context window evaluation."""
        active_genre = genre or self.default_genre
        profile = GENRE_PROFILES[active_genre]
        trace: List[str] = []

        tokens = re.findall(r'\b\w+\b', text)
        token_count = max(len(tokens), 1)
        scale_factor = 100.0 / token_count
        tokens_lower = [t.lower() for t in tokens]

        # Process Base Patterns with Genre Dampening
        raw_counts = {
            'D1_agency': self._scan_base(text, self.D1_BASE, 'D1', trace) * profile.passivity_dampening,
            'D2_affect': self._scan_base(text, self.D2_BASE, 'D2', trace) * profile.affective_dampening,
            'D3_reality': self._scan_base(text, self.D3_BASE, 'D3', trace) * profile.reification_dampening,
            'D4_iconic': self._scan_base(text, self.D4_BASE, 'D4', trace)
        }

        # Apply Contextual N-Gram Rules (Dynamic Word Interpreter)
        self._apply_context_rules(text, tokens_lower, active_genre, raw_counts, trace)

        # Token Density per 100 words
        dimension_scores = {
            k: round(max(0.0, v) * scale_factor, 2)
            for k, v in raw_counts.items()
        }

        # Normalize against Genre-Specific Saturation Thresholds
        normalized_scores = {
            k: min(round(dimension_scores[k] / profile.saturation_thresholds[k], 3), 1.0)
            for k in dimension_scores
        }

        # Calculate Cognitive Processing Energy
        total_density = sum(dimension_scores.values())
        energy_estimate = self._calculate_cognitive_energy(normalized_scores, total_density)

        # Weighted Composite Manipulation Index using Genre Weights
        manipulation_index = round(
            sum(normalized_scores[k] * profile.weights[k] for k in normalized_scores),
            3
        )

        return DynamicVectorSignature(
            genre_applied=profile.name,
            dimension_scores=dimension_scores,
            raw_counts={k: round(v, 2) for k, v in raw_counts.items()},
            normalized_scores=normalized_scores,
            trace=trace,
            energy_estimate=round(energy_estimate, 2),
            manipulation_index=manipulation_index
        )

    def _scan_base(self, text: str, patterns: List[Tuple[str, Pattern]], label: str, trace: List[str]) -> float:
        """Executes base regex passes."""
        hits = 0.0
        for name, regex in patterns:
            matches = regex.findall(text)
            if matches:
                count = len(matches)
                hits += count
                sample = matches[0] if isinstance(matches[0], str) else matches[0][0]
                trace.append(f"{label}: [{name}] x{count} -> '{sample}'")
        return hits

    def _apply_context_rules(self, text: str, tokens_lower: List[str], genre: Genre, raw_counts: Dict[str, float], trace: List[str]):
        """Evaluates N-gram context windows around target words to adjust dimensional scores."""
        token_set = set(tokens_lower)

        for rule in self.context_rules:
            matches = rule.pattern.finditer(text)
            for match in matches:
                word = match.group(0)

                # Check qualifying/disqualifying context within the document token set
                if rule.qualifying_context and not (rule.qualifying_context & token_set):
                    continue  # Context not met
                if rule.disqualifying_context and (rule.disqualifying_context & token_set):
                    continue

                multiplier = rule.genre_multipliers.get(genre, 1.0)
                score_delta = (multiplier - 1.0)
                raw_counts[rule.target_dimension] += score_delta

                trace.append(
                    f"Context Interpreter: Term '{word}' in [{genre.name}] "
                    f"-> Modifying {rule.target_dimension} by {score_delta:+.2f} (x{multiplier})"
                )

    def _calculate_cognitive_energy(self, normalized: Dict[str, float], total_density: float) -> float:
        """Calculates cognitive processing overhead from vector variance and total density."""
        vals = list(normalized.values())
        mean = sum(vals) / len(vals)
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)
        return (total_density * 0.04) + (variance * 2.5)
