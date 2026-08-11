"""Citation graph: detect references to other regulations in code text."""
import re
from typing import List

from fourd_municipal_engine.models.municipal import RegulationReference


class CitationGraph:
    """Extract and classify references to interconnected regulations."""

    INDUSTRY_STANDARDS = ("IBC", "IRC", "ADA", "NFPA", "IEBC")

    def __init__(self) -> None:
        self.re_citation = re.compile(
            r"(?:pursuant to|per|under)\s+"
            r"((?:(?:Section|Chapter|Title|Article|Ordinance)\s+[0-9A-Z.\-]+)"
            r"|(?:the\s+[A-Za-z ]+Act))",
            re.IGNORECASE,
        )
        self.re_standard = re.compile(r"\b(IBC|IRC|ADA|NFPA|IEBC)\b")

    def _classify(self, name: str) -> str:
        upper = name.upper()
        if any(std in upper for std in self.INDUSTRY_STANDARDS):
            return "industry_standard"
        if re.match(r"(?i)(?:section|chapter|title|article|ordinance)\b", name):
            return "municipal"
        if name.rstrip().lower().endswith("act"):
            if "state" in name.lower():
                return "state"
            return "federal"
        return "municipal"

    def extract_references(self, text: str) -> List[RegulationReference]:
        references: List[RegulationReference] = []
        seen = set()

        for match in self.re_citation.finditer(text):
            name = " ".join(match.group(1).split()).strip()
            if name.lower() in seen:
                continue
            seen.add(name.lower())
            references.append(
                RegulationReference(name=name, type=self._classify(name))
            )

        for match in self.re_standard.finditer(text):
            name = match.group(1)
            if name.lower() in seen:
                continue
            seen.add(name.lower())
            references.append(
                RegulationReference(name=name, type="industry_standard")
            )

        return references
