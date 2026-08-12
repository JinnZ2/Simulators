"""Fee exploration engine: flat + formulaic fee extraction and cost estimation."""
import re
from typing import Dict, List

from fourd_municipal_engine.models.municipal import FeeItem


class FeeExplorationEngine:
    """Extract flat and formulaic fees and compute total project cost."""

    def __init__(self) -> None:
        self.re_flat = re.compile(r"\$([\d,]+(?:\.\d{2})?)")
        self.re_per = re.compile(
            r"\$([\d,]+(?:\.\d{2})?)\s*per\s*(\w+(?:\s+\w+)?)", re.IGNORECASE
        )
        self.re_valuation = re.compile(
            r"([\d.]+)\s*%\s*of\s+(?:project\s+)?valuation", re.IGNORECASE
        )

    @staticmethod
    def _context(text: str, match: re.Match, span: int = 60) -> str:
        start = max(0, match.start() - span)
        end = min(len(text), match.end() + span)
        return " ".join(text[start:end].split())

    def extract(self, text: str) -> List[FeeItem]:
        fees: List[FeeItem] = []
        formula_spans = []

        for match in self.re_valuation.finditer(text):
            pct = float(match.group(1))
            formula_spans.append(match.span())
            fees.append(
                FeeItem(
                    description=self._context(text, match),
                    amount=None,
                    formula="valuation_pct",
                    condition=f"{pct}% of project valuation",
                )
            )

        seen_sqft = False
        for match in self.re_per.finditer(text):
            rate = float(match.group(1).replace(",", ""))
            unit = match.group(2).lower()
            formula_spans.append(match.span())
            if "square" in unit:
                if seen_sqft:
                    continue
                seen_sqft = True
                fees.append(
                    FeeItem(
                        description=self._context(text, match),
                        amount=None,
                        formula="per_square_foot",
                        condition=f"${rate} per square foot",
                    )
                )
            else:
                fees.append(
                    FeeItem(
                        description=self._context(text, match),
                        amount=None,
                        formula=f"per_{unit.replace(' ', '_')}",
                        condition=f"${rate} per {unit}",
                    )
                )

        for match in self.re_flat.finditer(text):
            if any(s <= match.start() < e for s, e in formula_spans):
                continue  # part of a formulaic fee already captured
            amount = float(match.group(1).replace(",", ""))
            fees.append(
                FeeItem(description=self._context(text, match), amount=amount)
            )

        return fees

    def calculate_total(
        self, fees: List[FeeItem], project_params: Dict[str, float]
    ) -> float:
        total = 0.0
        square_feet = project_params.get("square_feet", 0.0)
        valuation = project_params.get("valuation", 0.0)
        for fee in fees:
            if fee.amount is not None:
                total += fee.amount
            elif fee.formula == "per_square_foot":
                rate_match = re.search(r"\$([\d,]+(?:\.\d+)?)", fee.condition)
                if rate_match:
                    total += float(rate_match.group(1).replace(",", "")) * square_feet
            elif fee.formula == "valuation_pct":
                pct_match = re.search(r"([\d.]+)\s*%", fee.condition)
                if pct_match:
                    total += (float(pct_match.group(1)) / 100.0) * valuation
        return total
