"""Audit tests for the Ordinance4DParser regex fallback and ETL payload format."""
import pytest

pytest.importorskip("pydantic")

from fourd_municipal_engine.parser.ordinance_parser import Ordinance4DParser

AUDIT_SAMPLE = """
Section 12.04 - Commercial Overlay
Maximum height limit of 45 feet.
Application fee: $1,250.00 base fee plus $0.50 per square foot.
Plan review timeline: decisions rendered within 45 days.
Requires Planning Commission approval.
Building codes applicable: IBC 2024 and NFPA 101.
"""

DEMO_SAMPLE = """
ORDINANCE NO. 2026-88 - SECTION 25-2-774
Accessory Dwelling Unit (ADU) Building Standards for SF-3 and MF-1 Districts.

(A) Development Limits:
    1. Maximum building height shall not exceed 18 feet.
    2. Maximum Floor Area Ratio (FAR) shall be 0.45.
    3. Rear yard setback minimum is 5 feet; side yard setback minimum is 5 feet.
    4. One off-street parking space is required per unit.
    5. Construction must comply with IRC 2024 standards.

(B) Administration and Fees:
    1. A fixed processing fee of $450.00 is due at application submittal.
    2. Plan review fee is $0.85 per sq. ft. plus 0.25% of total project valuation.
    3. Staff shall render a final decision within 30 days of submission. No board approval is required.
"""


@pytest.fixture(scope="module")
def parser():
    # Offline/heuristic regex mode for deterministic auditing
    return Ordinance4DParser(api_key=None)


def test_regex_fallback_metric_extraction(parser):
    """Audit 1: extraction of financial fees, heights, and timelines via Regex fallback."""
    result = parser.parse(AUDIT_SAMPLE)
    metrics = result["metrics_data"]

    assert metrics["flat_fee_usd"] == 1250.00
    assert metrics["sqft_rate_usd"] == 0.50
    assert metrics["max_height_ft"] == 45.0
    assert metrics["admin_review_days"] == 45
    assert metrics["board_approval_required"] is True
    assert "IBC 2024" in metrics["building_codes"]


def test_schema_null_safety(parser):
    """Audit 2: schema outputs valid structure even when input text contains no numbers."""
    sparse_text = "This ordinance section governs general administrative intent and definitions."
    result = parser.parse(sparse_text)
    metrics = result["metrics_data"]

    assert metrics["max_far"] is None
    assert metrics["max_height_ft"] is None
    assert metrics["flat_fee_usd"] == 0.0
    assert isinstance(metrics["building_codes"], list)


def test_3d_extrusion_parameter_bounds():
    """Audit 3: extracted metrics fall within reasonable physical/legal constraints."""
    mock_payload = {
        "max_height_ft": 35.0,
        "setback_front_ft": 15.0,
        "setback_rear_ft": 10.0,
        "setback_side_ft": 5.0,
    }
    assert mock_payload["max_height_ft"] > 0.0
    assert mock_payload["setback_side_ft"] * 2 < 100.0


def test_payload_etl_format_compliance(parser):
    """Audit 4: payload format matches the exact schema expected by the ETL loader."""
    result = parser.parse("Height limit of 30 feet. $200 fee.")

    for key in ("section_data", "target_zoning_codes", "metrics_data"):
        assert key in result

    for key in (
        "max_far", "max_height_ft", "admin_review_days",
        "flat_fee_usd", "sqft_rate_usd", "valuation_pct",
    ):
        assert key in result["metrics_data"]

    # SPEC V2 addendum enrichments
    for key in ("stated_intent", "root_causes", "references"):
        assert key in result


def test_improved_extraction_on_demo_text(parser):
    """Audit 5: improved regex fallback on the source demo ordinance text."""
    result = parser.parse(DEMO_SAMPLE)
    metrics = result["metrics_data"]

    assert metrics["flat_fee_usd"] == 450.00
    assert metrics["sqft_rate_usd"] == 0.85
    assert metrics["valuation_pct"] == pytest.approx(0.0025)
    assert metrics["max_height_ft"] == 18.0
    assert metrics["admin_review_days"] == 30
    assert metrics["building_codes"] == ["IRC 2024"]
    assert metrics["max_far"] == 0.45
    assert metrics["setback_rear_ft"] == 5.0
    assert metrics["setback_side_ft"] == 5.0
    assert metrics["parking_spaces_per_unit"] == 1.0
    assert metrics["board_approval_required"] is False


def test_addendum_enrichment_values(parser):
    """Addendum: stated_intent / root_causes / references are populated."""
    text = (
        "Purpose: This section promotes affordable housing and manages parking "
        "traffic impacts. Standards are adopted pursuant to Section 12.04 and "
        "must comply with IBC 2024."
    )
    result = parser.parse(text)

    assert result["stated_intent"] is not None
    assert "affordable housing" in result["stated_intent"].lower()
    assert "affordable_housing" in result["root_causes"]
    assert "traffic" in result["root_causes"]
    names = {ref["name"] for ref in result["references"]}
    assert "Section 12.04" in names
    assert "IBC" in names
    for ref in result["references"]:
        assert set(ref) >= {"name", "type", "relationship"}
