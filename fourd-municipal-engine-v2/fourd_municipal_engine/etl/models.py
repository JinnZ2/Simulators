"""SQLAlchemy ORM models for the 4D municipal PostGIS schema.

sqlalchemy and geoalchemy2 are optional dependencies; importing this module
without them raises an ImportError with an install hint.
"""
import uuid

try:
    from sqlalchemy import Column, String, Float, Integer, Boolean, Text, ForeignKey
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TSTZRANGE, JSONB, ARRAY as PG_ARRAY
    from sqlalchemy.orm import declarative_base, relationship
except ImportError as exc:  # pragma: no cover - exercised only without sqlalchemy
    raise ImportError(
        "sqlalchemy is required for the etl module. "
        "Install with `pip install fourd-municipal-engine[db]`."
    ) from exc

try:
    from geoalchemy2 import Geometry
except ImportError as exc:  # pragma: no cover - exercised only without geoalchemy2
    raise ImportError(
        "geoalchemy2 is required for the etl module. "
        "Install with `pip install fourd-municipal-engine[db]`."
    ) from exc

Base = declarative_base()


class Jurisdiction(Base):
    __tablename__ = "jurisdictions"

    jurisdiction_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    state_code = Column(String(2), nullable=False)
    fips_code = Column(String(10), unique=True)


class ZoningDistrict(Base):
    __tablename__ = "zoning_districts"

    zoning_district_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jurisdiction_id = Column(PG_UUID(as_uuid=True), ForeignKey("jurisdictions.jurisdiction_id", ondelete="CASCADE"), nullable=False)
    district_code = Column(String(20), nullable=False)
    district_name = Column(String(150), nullable=False)
    boundary = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=False)
    valid_period = Column(TSTZRANGE, nullable=False)
    system_period = Column(TSTZRANGE, nullable=False)


class CodeSection(Base):
    __tablename__ = "code_sections"

    section_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jurisdiction_id = Column(PG_UUID(as_uuid=True), ForeignKey("jurisdictions.jurisdiction_id", ondelete="CASCADE"), nullable=False)
    section_citation = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    plain_english_summary = Column(Text)
    valid_period = Column(TSTZRANGE, nullable=False)
    system_period = Column(TSTZRANGE, nullable=False)

    metrics = relationship("Code4DMetrics", back_populates="section", uselist=False, cascade="all, delete-orphan")


class Code4DMetrics(Base):
    __tablename__ = "code_4d_metrics"

    metric_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id = Column(PG_UUID(as_uuid=True), ForeignKey("code_sections.section_id", ondelete="CASCADE"), nullable=False, unique=True)

    # Density
    max_far = Column(Float)
    max_height_ft = Column(Float)
    max_units_per_acre = Column(Float)
    max_lot_coverage_pct = Column(Float)
    min_lot_size_sqft = Column(Float)

    # Design
    setback_front_ft = Column(Float)
    setback_rear_ft = Column(Float)
    setback_side_ft = Column(Float)
    parking_spaces_per_unit = Column(Float)
    building_codes_referenced = Column(PG_ARRAY(Text))

    # Delay
    admin_review_days = Column(Integer)
    public_notice_days = Column(Integer)
    board_approval_required = Column(Boolean, default=False)
    total_estimated_lead_time_days = Column(Integer)

    # Dollars
    flat_fee_usd = Column(Float, default=0.0)
    sqft_rate_usd = Column(Float, default=0.0)
    valuation_pct = Column(Float, default=0.0)
    fee_formulas = Column(JSONB)

    section = relationship("CodeSection", back_populates="metrics")


class CodeZoningJunction(Base):
    __tablename__ = "code_zoning_junction"

    section_id = Column(PG_UUID(as_uuid=True), ForeignKey("code_sections.section_id", ondelete="CASCADE"), primary_key=True)
    zoning_district_id = Column(PG_UUID(as_uuid=True), ForeignKey("zoning_districts.zoning_district_id", ondelete="CASCADE"), primary_key=True)
