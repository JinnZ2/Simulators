-- =====================================================================
-- 4D MUNICIPAL CODE REPOSITORY SCHEMA (Simplified Variant v2)
-- No temporal ranges; plain unique constraints; idempotent CREATE style.
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Jurisdictions
CREATE TABLE IF NOT EXISTS jurisdictions (
    jurisdiction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    state_code VARCHAR(2) NOT NULL,
    fips_code VARCHAR(10) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Zoning Districts with 2D Boundaries
CREATE TABLE IF NOT EXISTS zoning_districts (
    zoning_district_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_id UUID NOT NULL REFERENCES jurisdictions(jurisdiction_id) ON DELETE CASCADE,
    district_code VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    boundary GEOMETRY(MultiPolygon, 4326),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_district_per_jurisdiction UNIQUE (jurisdiction_id, district_code)
);
CREATE INDEX IF NOT EXISTS idx_zoning_districts_spatial ON zoning_districts USING gist(boundary);

-- Code Sections
CREATE TABLE IF NOT EXISTS code_sections (
    section_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_id UUID NOT NULL REFERENCES jurisdictions(jurisdiction_id) ON DELETE CASCADE,
    citation VARCHAR(100) NOT NULL,
    title VARCHAR(255),
    raw_text TEXT,
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4D Metrics Table
CREATE TABLE IF NOT EXISTS code_4d_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID UNIQUE NOT NULL REFERENCES code_sections(section_id) ON DELETE CASCADE,
    -- Density
    max_far NUMERIC(6,2),
    max_height_ft NUMERIC(6,2),
    max_units_per_acre NUMERIC(8,2),
    max_lot_coverage_pct NUMERIC(5,2),
    min_lot_size_sqft NUMERIC(10,2),
    -- Design
    setback_front_ft NUMERIC(6,2),
    setback_rear_ft NUMERIC(6,2),
    setback_side_ft NUMERIC(6,2),
    parking_spaces_per_unit NUMERIC(5,2),
    building_codes JSONB DEFAULT '[]'::jsonb,
    -- Delay
    admin_review_days INT,
    public_notice_days INT,
    board_approval_required BOOLEAN DEFAULT FALSE,
    total_lead_time_days INT,
    -- Dollars
    flat_fee_usd NUMERIC(10,2) DEFAULT 0.0,
    sqft_rate_usd NUMERIC(8,4) DEFAULT 0.0,
    valuation_pct NUMERIC(6,4) DEFAULT 0.0,
    fee_formulas JSONB DEFAULT '{}'::jsonb
);

-- Code Section to Zoning District Mapping
CREATE TABLE IF NOT EXISTS code_zoning_junction (
    section_id UUID REFERENCES code_sections(section_id) ON DELETE CASCADE,
    zoning_district_id UUID REFERENCES zoning_districts(zoning_district_id) ON DELETE CASCADE,
    PRIMARY KEY (section_id, zoning_district_id)
);

-- 3D Volumetric Building Envelopes
CREATE TABLE IF NOT EXISTS building_envelopes_3d (
    envelope_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID NOT NULL REFERENCES code_sections(section_id) ON DELETE CASCADE,
    zoning_district_id UUID NOT NULL REFERENCES zoning_districts(zoning_district_id) ON DELETE CASCADE,
    buildable_footprint_2d GEOMETRY(MultiPolygon, 4326),
    envelope_3d GEOMETRY(PolyhedralSurfaceZ, 4326),
    max_height_ft NUMERIC(6,2),
    calculated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_envelope_per_junction UNIQUE (section_id, zoning_district_id)
);
CREATE INDEX IF NOT EXISTS idx_envelopes_3d_spatial ON building_envelopes_3d USING gist(envelope_3d);

-- 3D Extrusion Function
CREATE OR REPLACE FUNCTION fn_generate_3d_building_envelope(
    p_section_id UUID,
    p_zoning_district_id UUID
)
RETURNS VOID AS $$
DECLARE
    v_boundary GEOMETRY;
    v_max_height NUMERIC;
    v_setback_front NUMERIC;
    v_setback_rear NUMERIC;
    v_setback_side NUMERIC;
    v_avg_setback_meters NUMERIC;
    v_footprint_meters GEOMETRY;
    v_extrude_meters NUMERIC;
    v_envelope_3d GEOMETRY;
    v_footprint_4326 GEOMETRY;
BEGIN
    SELECT boundary INTO v_boundary FROM zoning_districts WHERE zoning_district_id = p_zoning_district_id;
    SELECT COALESCE(max_height_ft, 35.0), COALESCE(setback_front_ft, 15.0), COALESCE(setback_rear_ft, 10.0), COALESCE(setback_side_ft, 5.0)
    INTO v_max_height, v_setback_front, v_setback_rear, v_setback_side
    FROM code_4d_metrics WHERE section_id = p_section_id;

    IF v_boundary IS NULL THEN RETURN; END IF;

    v_avg_setback_meters := ((v_setback_front + v_setback_rear + v_setback_side) / 3.0) * 0.3048;
    v_extrude_meters := v_max_height * 0.3048;

    v_footprint_meters := ST_Buffer(ST_Transform(v_boundary, 3857), -v_avg_setback_meters);
    IF ST_IsEmpty(v_footprint_meters) OR v_footprint_meters IS NULL THEN
        v_footprint_meters := ST_Transform(v_boundary, 3857);
    END IF;

    v_envelope_3d := ST_Extrude(v_footprint_meters, 0, 0, v_extrude_meters);
    v_footprint_4326 := ST_Multi(ST_Transform(v_footprint_meters, 4326));
    v_envelope_3d := ST_Transform(v_envelope_3d, 4326);

    INSERT INTO building_envelopes_3d (section_id, zoning_district_id, buildable_footprint_2d, envelope_3d, max_height_ft, calculated_at)
    VALUES (p_section_id, p_zoning_district_id, v_footprint_4326, v_envelope_3d, v_max_height, CURRENT_TIMESTAMP)
    ON CONFLICT (section_id, zoning_district_id)
    DO UPDATE SET buildable_footprint_2d = EXCLUDED.buildable_footprint_2d, envelope_3d = EXCLUDED.envelope_3d, max_height_ft = EXCLUDED.max_height_ft, calculated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Trigger Setup
CREATE OR REPLACE FUNCTION trg_fn_auto_generate_3d_envelope() RETURNS TRIGGER AS $$
BEGIN
    PERFORM fn_generate_3d_building_envelope(NEW.section_id, NEW.zoning_district_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_3d_envelope_generation ON code_zoning_junction;
CREATE TRIGGER trg_3d_envelope_generation
AFTER INSERT OR UPDATE ON code_zoning_junction
FOR EACH ROW EXECUTE FUNCTION trg_fn_auto_generate_3d_envelope();
