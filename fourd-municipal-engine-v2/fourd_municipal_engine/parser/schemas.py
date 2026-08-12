"""Pydantic schemas for structured 4D ordinance metric extraction.

pydantic is an optional dependency of this package; importing this module
without it raises an ImportError with an install hint.
"""
from typing import Dict, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover - exercised only without pydantic
    raise ImportError(
        "pydantic is required for the parser module. "
        "Install with `pip install fourd-municipal-engine[parser]`."
    ) from exc


class DensityMetricsModel(BaseModel):
    max_far: Optional[float] = Field(None, description="Maximum Floor Area Ratio (e.g., 0.40, 2.5)")
    max_height_ft: Optional[float] = Field(None, description="Maximum height limit in feet")
    max_units_per_acre: Optional[float] = Field(None, description="Maximum residential units allowed per acre")
    max_lot_coverage_pct: Optional[float] = Field(None, description="Maximum lot coverage as a percentage (0-100)")
    min_lot_size_sqft: Optional[float] = Field(None, description="Minimum lot size required in square feet")


class DesignMetricsModel(BaseModel):
    setback_front_ft: Optional[float] = Field(None, description="Minimum front yard setback in feet")
    setback_rear_ft: Optional[float] = Field(None, description="Minimum rear yard setback in feet")
    setback_side_ft: Optional[float] = Field(None, description="Minimum side yard setback in feet")
    parking_spaces_per_unit: Optional[float] = Field(None, description="Required parking spaces per unit")
    building_codes: List[str] = Field(default_factory=list, description="Referenced codes (e.g., ['IBC 2024', 'IRC 2021'])")


class DelayMetricsModel(BaseModel):
    admin_review_days: Optional[int] = Field(None, description="Administrative/staff review timeframe in days")
    public_notice_days: Optional[int] = Field(None, description="Public notice/hearing notification window in days")
    board_approval_required: bool = Field(False, description="True if Planning Commission/Council approval is required")
    total_lead_time_days: Optional[int] = Field(None, description="Total aggregated processing lead time in days")


class DollarMetricsModel(BaseModel):
    flat_fee_usd: float = Field(0.0, description="Base flat application or permit fee in USD")
    sqft_rate_usd: float = Field(0.0, description="Fee per square foot in USD (e.g., $0.75/sq ft -> 0.75)")
    valuation_pct: float = Field(0.0, description="Fee as a percentage of project valuation (e.g., 0.5% -> 0.005)")
    fee_formulas: Dict[str, str] = Field(default_factory=dict, description="Custom or formulaic fees (e.g., {'environmental_surcharge': 'base * 0.10'})")


class FourDOrdinanceMetricsSchema(BaseModel):
    """Unified 4D metrics schema for ordinance text parsing."""
    citation: Optional[str] = Field(None, description="Section or ordinance citation (e.g., '17.04.120')")
    title: Optional[str] = Field(None, description="Title or heading of the ordinance section")
    summary: Optional[str] = Field(None, description="1-2 sentence plain English summary")
    target_zoning_codes: List[str] = Field(default_factory=list, description="List of zoning codes impacted (e.g., ['SF-3', 'MF-2'])")

    density: DensityMetricsModel
    design: DesignMetricsModel
    delay: DelayMetricsModel
    dollars: DollarMetricsModel
