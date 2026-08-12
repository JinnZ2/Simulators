"""Root cause analysis: keyword-classify the problem a regulation targets."""
from typing import Dict, List, Optional


class RegulationRootCauseAnalyzer:
    """Link regulation text to typical root-cause categories via keywords."""

    DEFAULT_INTENT_KEYWORDS: Dict[str, List[str]] = {
        "public_safety": ["fire", "life safety", "egress", "emergency", "hazard"],
        "affordable_housing": [
            "affordable",
            "low-income",
            "density bonus",
            "inclusionary",
            "housing shortage",
        ],
        "environmental": [
            "wetland",
            "endangered species",
            "water quality",
            "emissions",
            "runoff",
            "stormwater",
        ],
        "traffic": ["traffic", "congestion", "parking", "vehicle", "intersection"],
        "economic_development": [
            "economic development",
            "small business",
            "job creation",
            "revitalization",
            "blight",
        ],
    }

    def __init__(self, municipal_jargon: Optional[dict] = None) -> None:
        self.municipal_jargon = municipal_jargon or {}
        self.intent_keywords = dict(self.DEFAULT_INTENT_KEYWORDS)

    def analyze(self, full_text: str) -> List[str]:
        lowered = full_text.lower()
        return [
            category
            for category, keywords in self.intent_keywords.items()
            if any(keyword in lowered for keyword in keywords)
        ]
