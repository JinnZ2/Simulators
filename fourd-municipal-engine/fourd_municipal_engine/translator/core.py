"""Municipal Code Translator: converts regulatory legalese to plain English.

Extracts flat fees and stated purpose/intent blocks from ordinance text.
"""
import re
from typing import List

from fourd_municipal_engine.models.municipal import FeeItem, MunicipalTranslationResult


class MunicipalCodeTranslator:
    """Translate municipal legalese into plain English with structured extraction."""

    JARGON_MAP = {
        "hereinafter": "from now on",
        "pursuant to": "under",
        "shall": "must",
        "commence": "start",
        "terminate": "end",
        "utilize": "use",
        "notwithstanding": "despite",
        "aforementioned": "mentioned earlier",
        "heretofore": "until now",
        "thereof": "of it",
        "whereas": "given that",
        "in the event that": "if",
        "prior to": "before",
        "subsequent to": "after",
        "remuneration": "pay",
        "abatement": "reduction",
        "encumbrance": "burden/lien",
        "per annum": "per year",
        "null and void": "invalid",
        "egress": "exit",
        "domicile": "home",
        "therein": "in it",
        "hereby": "by this",
    }

    def __init__(self) -> None:
        self.re_fees = re.compile(r"\$[\d,]+(?:\.\d{2})?")
        self.re_citation = re.compile(
            r"(?:pursuant to|per|under)\s+"
            r"((?:(?:Section|Chapter|Title|Article|Ordinance)\s+[0-9A-Z.\-]+)"
            r"|(?:the\s+[A-Za-z ]+Act))",
            re.IGNORECASE,
        )
        self.re_purpose = re.compile(
            r"(?:Purpose|Intent|Legislative findings)[:.\s]+(.+?)(?:\n\n|\n[A-Z])",
            re.IGNORECASE | re.DOTALL,
        )
        self._jargon_patterns = [
            (re.compile(r"\b" + re.escape(jargon) + r"\b", re.IGNORECASE), jargon)
            for jargon in sorted(self.JARGON_MAP, key=len, reverse=True)
        ]

    def _replace_jargon(self, text: str) -> str:
        for pattern, jargon in self._jargon_patterns:
            replacement = self.JARGON_MAP[jargon]

            def _sub(match, repl=replacement):
                matched = match.group(0)
                if matched[:1].isupper():
                    return repl[:1].upper() + repl[1:]
                return repl

            text = pattern.sub(_sub, text)
        return text

    def _extract_fees(self, text: str) -> List[FeeItem]:
        fees = []
        for match in self.re_fees.finditer(text):
            raw = match.group(0)
            amount = float(raw[1:].replace(",", ""))
            # capture surrounding context for a readable description
            start = max(0, match.start() - 60)
            end = min(len(text), match.end() + 60)
            context = " ".join(text[start:end].split())
            fees.append(FeeItem(description=context, amount=amount))
        return fees

    def _extract_intent(self, text: str) -> str:
        match = self.re_purpose.search(text)
        if match:
            return " ".join(match.group(1).split()).strip()
        return ""

    def translate(self, text: str, citation: str = "") -> MunicipalTranslationResult:
        summary = self._replace_jargon(text)
        fees = self._extract_fees(text)
        intent = self._extract_intent(text)
        return MunicipalTranslationResult(
            section_citation=citation,
            raw_text=text,
            plain_english_summary=summary,
            fees=fees,
            stated_intent=intent,
        )
