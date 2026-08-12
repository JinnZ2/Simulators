"""Advanced analysis pipeline: chains all analyzers over a translation result."""
from typing import Set, Tuple

from fourd_municipal_engine.analysis.audit import AuditEngine
from fourd_municipal_engine.analysis.citations import CitationGraph
from fourd_municipal_engine.analysis.fees import FeeExplorationEngine
from fourd_municipal_engine.analysis.root_cause import RegulationRootCauseAnalyzer
from fourd_municipal_engine.models.municipal import MunicipalTranslationResult


class AdvancedAnalysisPipeline:
    """Layer advanced analytics on top of the core translator's result."""

    def __init__(self, translator) -> None:
        self.translator = translator
        self.root_cause_analyzer = RegulationRootCauseAnalyzer(
            getattr(translator, "JARGON_MAP", None)
        )
        self.citation_graph = CitationGraph()
        self.fee_engine = FeeExplorationEngine()
        self.audit_engine = AuditEngine()

    def analyze(
        self, result: MunicipalTranslationResult, raw_text: str
    ) -> MunicipalTranslationResult:
        result.root_causes = self.root_cause_analyzer.analyze(raw_text)
        result.interconnected_regulations = self.citation_graph.extract_references(
            raw_text
        )
        if not result.stated_intent:
            result.stated_intent = self.translator._extract_intent(raw_text)
        result.audit_metrics = self.audit_engine.extract_metrics(raw_text)
        result.auditability_score = self.audit_engine.auditability_score(
            result.audit_metrics, raw_text
        )

        # Merge translator flat fees with engine's flat + formulaic fees,
        # deduping by (description, amount).
        explored = self.fee_engine.extract(raw_text)
        merged = list(result.fees)
        seen: Set[Tuple[str, object]] = {
            (f.description, f.amount) for f in merged
        }
        for fee in explored:
            key = (fee.description, fee.amount)
            if key not in seen:
                seen.add(key)
                merged.append(fee)
        result.fees = merged

        return result
