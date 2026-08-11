"""Tests for the advanced analysis modules and pipeline."""
from fourd_municipal_engine.analysis.audit import AuditEngine
from fourd_municipal_engine.analysis.citations import CitationGraph
from fourd_municipal_engine.analysis.fees import FeeExplorationEngine
from fourd_municipal_engine.analysis.pipeline import AdvancedAnalysisPipeline
from fourd_municipal_engine.analysis.root_cause import RegulationRootCauseAnalyzer
from fourd_municipal_engine.translator.core import MunicipalCodeTranslator

SAMPLE_ORDINANCE = (
    "Purpose: to improve water quality and reduce stormwater runoff hazard.\n"
    "\n"
    "Section 1. Pursuant to Section 12.4 and under the Clean Water Act, all "
    "structures shall comply with the IBC and NFPA 13. The applicant shall pay "
    "a filing fee of $250.00, a plan review fee of $0.50 per square foot, and "
    "a construction fee of 1.5% of project valuation. The city shall reduce "
    "stormwater runoff by 20% no later than December 31, 2030 and shall issue "
    "an annual report on compliance."
)


def test_root_cause_categories_detected():
    causes = RegulationRootCauseAnalyzer().analyze(SAMPLE_ORDINANCE)
    assert "environmental" in causes
    assert "public_safety" in causes  # 'hazard' keyword


def test_citations_classified():
    refs = CitationGraph().extract_references(SAMPLE_ORDINANCE)
    by_type = {}
    for ref in refs:
        by_type.setdefault(ref.type, []).append(ref.name)
    assert "Section 12.4" in by_type.get("municipal", [])
    assert any(
        "Clean Water Act" in name for name in by_type.get("federal", [])
    )
    assert "IBC" in by_type.get("industry_standard", [])
    assert "NFPA" in by_type.get("industry_standard", [])


def test_fee_engine_formula_extraction():
    fees = FeeExplorationEngine().extract(SAMPLE_ORDINANCE)
    formulas = {fee.formula for fee in fees}
    assert "per_square_foot" in formulas
    assert "valuation_pct" in formulas
    flat_amounts = [fee.amount for fee in fees if fee.amount is not None]
    assert 250.0 in flat_amounts


def test_fee_engine_calculate_total():
    engine = FeeExplorationEngine()
    fees = engine.extract(SAMPLE_ORDINANCE)
    total = engine.calculate_total(
        fees, {"square_feet": 2000, "valuation": 300000}
    )
    # 250.00 flat + 0.50 * 2000 sqft + 1.5% * 300000 valuation
    expected = 250.0 + 0.50 * 2000 + 0.015 * 300000
    assert abs(total - expected) < 1e-6


def test_audit_metrics_and_score_bounds():
    engine = AuditEngine()
    metrics = engine.extract_metrics(SAMPLE_ORDINANCE)
    descriptions = [m.metric_description for m in metrics]
    assert any("reduce" in d and "stormwater runoff" in d for d in descriptions)
    assert any("compliance deadline" in d for d in descriptions)
    assert any("annual reporting" in d for d in descriptions)

    score = engine.auditability_score(metrics, SAMPLE_ORDINANCE)
    assert 0.0 <= score <= 1.0
    assert score > 0.0
    assert engine.auditability_score([], SAMPLE_ORDINANCE) == 0.0


def test_pipeline_fills_all_fields():
    translator = MunicipalCodeTranslator()
    result = translator.translate(SAMPLE_ORDINANCE, citation="Section 1")
    result = AdvancedAnalysisPipeline(translator).analyze(
        result, SAMPLE_ORDINANCE
    )
    assert result.section_citation == "Section 1"
    assert result.plain_english_summary
    assert result.fees
    assert any(f.formula for f in result.fees)  # formulaic fees merged in
    assert result.root_causes
    assert result.stated_intent
    assert result.interconnected_regulations
    assert result.audit_metrics
    assert 0.0 < result.auditability_score <= 1.0
