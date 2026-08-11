"""Audit engine: extract measurable KPIs and score regulation auditability."""
import re
from typing import List

from fourd_municipal_engine.models.municipal import AuditMetric


class AuditEngine:
    """Flag metrics mentioned in a regulation and score its auditability."""

    def __init__(self) -> None:
        self.re_reduce = re.compile(
            r"reduce\s+(.+?)\s+by\s+(\d+(?:\.\d+)?%)", re.IGNORECASE
        )
        self.re_increase = re.compile(
            r"increase\s+(.+?)\s+by\s+(\d[\d,]*(?:\.\d+)?%?)", re.IGNORECASE
        )
        self.re_deadline = re.compile(
            r"no later than\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4}"
            r"|\d{1,2}/\d{1,2}/\d{2,4}|[A-Za-z]+\s+\d{4})",
            re.IGNORECASE,
        )
        self.re_report = re.compile(
            r"\b(annual|quarterly|monthly|biennial)\s+report", re.IGNORECASE
        )

    def extract_metrics(self, text: str) -> List[AuditMetric]:
        metrics: List[AuditMetric] = []

        for match in self.re_reduce.finditer(text):
            subject = " ".join(match.group(1).split()).strip()
            metrics.append(
                AuditMetric(
                    metric_description=f"reduce {subject}",
                    target=match.group(2),
                )
            )

        for match in self.re_increase.finditer(text):
            subject = " ".join(match.group(1).split()).strip()
            metrics.append(
                AuditMetric(
                    metric_description=f"increase {subject}",
                    target=match.group(2),
                )
            )

        for match in self.re_deadline.finditer(text):
            metrics.append(
                AuditMetric(
                    metric_description="compliance deadline",
                    target=f"no later than {match.group(1)}",
                )
            )

        for match in self.re_report.finditer(text):
            metrics.append(
                AuditMetric(
                    metric_description=f"{match.group(1).lower()} reporting requirement",
                    target=f"{match.group(1).lower()} report",
                )
            )

        return metrics

    def auditability_score(self, metrics: List[AuditMetric], text: str) -> float:
        """Score in [0, 1] based on measurable targets, deadlines, reporting."""
        if not metrics:
            return 0.0
        score = 0.0
        # measurable numeric targets
        if any(re.search(r"\d", m.target) for m in metrics):
            score += 0.4
        # explicit deadlines
        if any("no later than" in m.target for m in metrics):
            score += 0.3
        # reporting duty (in metrics or raw text)
        if any("report" in m.metric_description for m in metrics) or re.search(
            r"\b(annual|quarterly|monthly|biennial)\s+report", text, re.IGNORECASE
        ):
            score += 0.3
        return min(1.0, score)
