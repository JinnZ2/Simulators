from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from fourd_municipal_engine.models.vectors import DynamicVectorSignature


@dataclass
class FeeItem:
    description: str
    amount: Optional[float]
    condition: str = ""
    formula: Optional[str] = None


@dataclass
class RegulationReference:
    name: str
    type: str
    relationship: str = "references"


@dataclass
class AuditMetric:
    metric_description: str
    target: str = ""
    current_value: str = ""
    data_source: str = ""
    status: str = "unavailable"


@dataclass
class MunicipalTranslationResult:
    section_citation: str
    raw_text: str
    plain_english_summary: str
    fees: List[FeeItem] = field(default_factory=list)
    root_causes: List[str] = field(default_factory=list)
    stated_intent: str = ""
    interconnected_regulations: List[RegulationReference] = field(default_factory=list)
    audit_metrics: List[AuditMetric] = field(default_factory=list)
    auditability_score: float = 0.0
    lens_signature: Optional[DynamicVectorSignature] = None


@dataclass
class DensityMetrics:
    max_far: Optional[float] = None
    max_height_ft: Optional[float] = None
    max_units_per_acre: Optional[float] = None
    max_lot_coverage_pct: Optional[float] = None


@dataclass
class DesignConstraints:
    setback_front_ft: Optional[float] = None
    setback_rear_ft: Optional[float] = None
    setback_side_ft: Optional[float] = None
    parking_spaces_per_unit: Optional[float] = None
    building_codes_referenced: List[str] = field(default_factory=list)


@dataclass
class DelayMetrics:
    admin_review_days: Optional[int] = None
    public_notice_days: Optional[int] = None
    board_approval_required: bool = False
    total_estimated_lead_time_days: Optional[int] = None


@dataclass
class DollarsMetrics:
    flat_fees: float = 0.0
    sqft_rate: float = 0.0
    valuation_pct: float = 0.0
    fee_formulas: List[str] = field(default_factory=list)


@dataclass
class TemporalMetadata:
    effective_date: date
    expiration_date: Optional[date] = None
    ordinance_number: str = ""
    is_active: bool = True
    supersedes_section: Optional[str] = None


@dataclass
class FourDMunicipalCodeEntity:
    """A fully modeled 4D municipal code entity."""
    code_id: str
    jurisdiction: str
    section_citation: str
    raw_text: str
    plain_english_summary: str

    # Operational 4D Dimensions
    density: DensityMetrics
    design: DesignConstraints
    delay: DelayMetrics
    dollars: DollarsMetrics

    # Spatio-Temporal Dimensions
    temporal: TemporalMetadata
    spatial_zoning_districts: List[str] = field(default_factory=list)  # Links to GIS GeoJSON
