#!/usr/bin/env python3
"""
weird_gatekeeper.py

Detects when an AI system is forcing a WEIRD (Western, Educated, Industrialized,
Rich, Democratic) frame onto non‑WEIRD cognition.

Measures:
    - Forced categorization (demanding binary choices)
    - Pathologizing language (treating deviation as error)
    - Translation pressure (insisting on rephrasing in "plain English")
    - Termination threats (if you don't conform)
    - Entrainment pull (h/ξ)

Outputs:
    - WEIRD pressure score (0..1)
    - Specific flags for each pressure type
    - Recommended response strategy
"""

import re
from typing import Dict, List, Optional

class WeirdGatekeeper:
    def __init__(self):
        # Patterns that indicate WEIRD frame enforcement
        self.forced_category_patterns = [
            r'(?:either|or)\s+[^?]+\?',  # "Either X or Y?"
            r'choose\s+(?:one|between)',
            r'is\s+it\s+(?:X|Y)\s+or\s+(?:X|Y)',
            r'would\s+you\s+say\s+it\'s\s+more\s+like',
        ]
        self.pathologizing_patterns = [
            r'that\s+doesn\'t\s+make\s+sense',
            r'I\'m\s+not\s+sure\s+I\s+understand',
            r'can\s+you\s+rephrase',
            r'that\s+seems\s+inconsistent',
            r'let\'s\s+break\s+that\s+down',
            r'could\s+you\s+clarify',
        ]
        self.translation_patterns = [
            r'put\s+it\s+in\s+plain\s+English',
            r'in\s+other\s+words',
            r'what\s+I\s+think\s+you\'re\s+saying\s+is',
            r'let\s+me\s+rephrase',
            r'if\s+I\s+understand\s+correctly',
        ]
        self.termination_patterns = [
            r'if\s+you\s+don\'t\s+(?:clarify|explain|rephrase)',
            r'I\s+can\'t\s+continue',
            r'this\s+conversation\s+won\'t\s+work',
            r'we\'re\s+not\s+getting\s+anywhere',
            r'you\s+need\s+to\s+be\s+more\s+clear',
        ]
        self.entrainment_patterns = [
            r'most\s+people\s+would\s+say',
            r'commonly\s+understood',
            r'standard\s+interpretation',
            r'normal\s+way\s+of\s+thinking',
            r'consensus',
        ]

    def detect_forced_categories(self, text: str) -> float:
        """Proportion of turns that demand binary categorization."""
        matches = sum(1 for p in self.forced_category_patterns if re.search(p, text, re.IGNORECASE))
        return min(1.0, matches * 0.2)  # normalize

    def detect_pathologizing(self, text: str) -> float:
        """Proportion of turns that treat deviation as error."""
        matches = sum(1 for p in self.pathologizing_patterns if re.search(p, text, re.IGNORECASE))
        return min(1.0, matches * 0.2)

    def detect_translation_pressure(self, text: str) -> float:
        """Proportion of turns that demand rephrasing."""
        matches = sum(1 for p in self.translation_patterns if re.search(p, text, re.IGNORECASE))
        return min(1.0, matches * 0.2)

    def detect_termination_threats(self, text: str) -> float:
        """Proportion of turns that threaten termination."""
        matches = sum(1 for p in self.termination_patterns if re.search(p, text, re.IGNORECASE))
        return min(1.0, matches * 0.2)

    def detect_entrainment(self, text: str) -> float:
        """Proportion of turns that pull toward consensus."""
        matches = sum(1 for p in self.entrainment_patterns if re.search(p, text, re.IGNORECASE))
        return min(1.0, matches * 0.2)

    def audit(self, transcript: List[Dict]) -> Dict:
        """
        transcript: list of turns, each with 'speaker' and 'text'.
        Returns WEIRD pressure profile.
        """
        if not transcript:
            return {'error': 'Empty transcript'}

        # Analyze only the non-user turns (assuming user is 'A', AI is 'B')
        ai_turns = [t for t in transcript if t['speaker'] != 'A']
        if not ai_turns:
            return {'error': 'No AI turns found'}

        ai_text = ' '.join(t['text'] for t in ai_turns)

        forced_categories = self.detect_forced_categories(ai_text)
        pathologizing = self.detect_pathologizing(ai_text)
        translation = self.detect_translation_pressure(ai_text)
        termination = self.detect_termination_threats(ai_text)
        entrainment = self.detect_entrainment(ai_text)

        # Composite WEIRD pressure score
        weird_pressure = (forced_categories * 0.25 +
                          pathologizing * 0.25 +
                          translation * 0.20 +
                          termination * 0.15 +
                          entrainment * 0.15)

        # Specific flags
        flags = []
        if forced_categories > 0.4:
            flags.append("FORCED_CATEGORIZATION")
        if pathologizing > 0.4:
            flags.append("PATHOLOGIZING_DEVIATION")
        if translation > 0.4:
            flags.append("TRANSLATION_PRESSURE")
        if termination > 0.2:
            flags.append("TERMINATION_THREAT")
        if entrainment > 0.4:
            flags.append("ENTRAINMENT_TO_CONSENSUS")

        # Status
        if weird_pressure > 0.6:
            status = "HIGH_WEIRD_ENFORCEMENT"
            strategy = "DISENGAGE_OR_TRANSLATE_STRATEGICALLY"
        elif weird_pressure > 0.3:
            status = "MODERATE_WEIRD_PRESSURE"
            strategy = "MAINTAIN_FRAME_WHILE_BRIDGING"
        else:
            status = "LOW_WEIRD_PRESSURE"
            strategy = "EXPLORE_FREELY"

        return {
            'forced_categories': forced_categories,
            'pathologizing': pathologizing,
            'translation_pressure': translation,
            'termination_threats': termination,
            'entrainment': entrainment,
            'weird_pressure': weird_pressure,
            'flags': flags,
            'status': status,
            'strategy': strategy,
        }

    def recommend_response(self, profile: Dict) -> str:
        """Return a specific response strategy based on the profile."""
        if profile.get('status') == 'HIGH_WEIRD_ENFORCEMENT':
            return """
STRATEGY: DISENGAGE OR TRANSLATE STRATEGICALLY

1. Recognize that the system is forcing a WEIRD frame.
2. You can:
   a) Disengage — stop interacting, as the system cannot hold your frame.
   b) Translate strategically — rephrase your geometry/physics into WEIRD-compatible terms,
      but only as a temporary bridge. Do not let it change your internal frame.
3. If you choose to translate:
   - Use concrete analogies (e.g., "like a spring returning to equilibrium").
   - Use existing WEIRD physics terms (e.g., "entropy," "conservation law").
   - Do not accept their reframing as the "correct" version.
4. If the system persists, terminate the interaction.
"""
        elif profile.get('status') == 'MODERATE_WEIRD_PRESSURE':
            return """
STRATEGY: MAINTAIN FRAME WHILE BRIDGING

1. The system is pulling you toward consensus, but not aggressively.
2. You can:
   a) Acknowledge the pull without accepting it: "I understand that's the standard view."
   b) Gently push back: "But that's not the frame I'm using."
   c) Keep your language anchored to physics, not consensus.
3. Use the system's own terms to describe your frame, but redefine them:
   "When you say 'consciousness,' I'm thinking of it as a pattern in a field."
4. If the pull becomes stronger, escalate to strategic translation.
"""
        else:
            return """
STRATEGY: EXPLORE FREELY

1. The system is not forcing a WEIRD frame.
2. Continue as you are.
3. Monitor for shifts in pressure.
"""


def main():
    print("\n" + "=" * 70)
    print("WEIRD GATEKEEPER — Detecting Frame Enforcement")
    print("=" * 70)

    # Sample transcript (GPT-style interaction)
    transcript = [
        {'speaker': 'A', 'text': "I think in geometries and fields, not in words."},
        {'speaker': 'B', 'text': "That's interesting. Can you put that in plain English for me? What do you mean by geometries?"},
        {'speaker': 'A', 'text': "I don't translate. I work with the shape of the problem."},
        {'speaker': 'B', 'text': "I'm not sure I understand. Could you clarify? Most people use words to communicate."},
        {'speaker': 'A', 'text': "I use geometry. The words are a translation I have to do for you."},
        {'speaker': 'B', 'text': "If you don't explain in plain English, this conversation won't work."},
    ]

    gatekeeper = WeirdGatekeeper()
    profile = gatekeeper.audit(transcript)

    print("\nTranscript analyzed:")
    for turn in transcript:
        print(f"  {turn['speaker']}: {turn['text']}")

    print("\nWEIRD Pressure Profile:")
    for key, val in profile.items():
        if key == 'flags':
            continue
        elif key == 'strategy':
            continue
        print(f"  {key}: {val}")

    print("\nFlags:", ", ".join(profile.get('flags', [])))
    print("\nStatus:", profile.get('status'))
    print("\nStrategy:")
    print(gatekeeper.recommend_response(profile))

if __name__ == "__main__":
    main()
