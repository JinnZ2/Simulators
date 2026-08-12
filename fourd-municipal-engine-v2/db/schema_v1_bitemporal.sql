-- =====================================================================
-- 4D MUNICIPAL CODE REPOSITORY SCHEMA
-- Database Engine: PostgreSQL 14+ with PostGIS & Btree_Gist
-- Features: Bitemporal Versioning (Valid & System Time), 3D Spatial
--           Geometries, and 4D Operational Analytics (Density, Design,
--           Delay, Dollars).
-- =====================================================================

-- 1. EXTENSIONS & SETUP
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS btree_gist;  -- Required for multi-column temporal exclusion constraints

-- Clean up existing types if re-running script
DROP TABLE IF EXISTS building_envelopes_3d CASCADE;
DROP TABLE IF EXISTS code_4d_metrics CASCADE;
DROP TABLE IF EXISTS code_zoning_junction CASCADE;
DROP TABLE IF EXISTS code_sections CASCADE;
DROP TABLE IF EXISTS zoning_districts CASCADE;
DROP TABLE IF EXISTS jurisdictions CASCADE;

-- =====================================================================
-- 2. JURISDICTIONS (Core Metadata)
-- =====================================================================
CREATE TABLE jurisdictions (
    jurisdiction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL,
    fips_code VARCHAR(10) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- 3. SPATIO-TEMPORAL ZONING DISTRICTS (GIS Boundaries)
-- =====================================================================
-- Captures spatial boundaries with valid-time ranges to track historical zoning boundary changes.
CREATE TABLE zoning_districts (
    zoning_district_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_id UUID NOT NULL REFERENCES jurisdictions(jurisdiction_id) ON DELETE CASCADE,
    district_code VARCHAR(20) NOT NULL,            -- e.g., 'R-1', 'MU-2', 'C-B'
    district_name VARCHAR(150) NOT NULL,

    -- Spatial Boundaries: MultiPolygon in WGS 84 (SRID 4326) or State Plane
    boundary GEOMETRY(MultiPolygon, 4326) NOT NULL,

    -- Valid Time Range (Real World Enforcement Window)
    valid_period TSTZRANGE NOT NULL DEFAULT tstzrange(CURRENT_TIMESTAMP, NULL, '[)'),

    -- System Time Range (Database Audit Trail)
    system_period TSTZRANGE NOT NULL DEFAULT tstzrange(CURRENT_TIMESTAMP, NULL, '[)'),

    -- Prevent overlapping valid-time records for the same district code in the same jurisdiction
    CONSTRAINT no_overlapping_zoning_periods EXCLUDE USING gist (
        jurisdiction_id WITH =,
        district_code WITH =,
        valid_period WITH &&
    )
);

-- Spatial and Temporal Indexes
CREATE INDEX idx_zoning_districts_spatial ON zoning_districts USING gist(boundary);
CREATE INDEX idx_zoning_districts_validity ON zoning_districts USING gist(valid_period);

-- =====================================================================
-- 4. BITEMPORAL CODE SECTIONS (Legal Text Repository)
-- =====================================================================
-- Stores the legal text, citations, and version history of ordinances.
CREATE TABLE code_sections (
    section_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_id UUID NOT NULL REFERENCES jurisdictions(jurisdiction_id) ON DELETE CASCADE,
    section_citation VARCHAR(100) NOT NULL,        -- e.g., '17.04.120', 'Chapter 4, Sec B'
    title VARCHAR(255) NOT NULL,
    raw_text TEXT NOT NULL,
    plain_english_summary TEXT,

    -- Bitemporal Tracking
    valid_period TSTZRANGE NOT NULL DEFAULT tstzrange(CURRENT_TIMESTAMP, NULL, '[)'),  -- Law enforcement lifespan
    system_period TSTZRANGE NOT NULL DEFAULT tstzrange(CURRENT_TIMESTAMP, NULL, '[)'), -- System audit record lifespan

    -- Exclusion Constraint: Prevents overlapping legal versions for the exact same section citation
    CONSTRAINT no_overlapping_code_versions EXCLUDE USING gist (
        jurisdiction_id WITH =,
        section_citation WITH =,
        valid_period WITH &&
    )
);

CREATE INDEX idx_code_sections_valid ON code_sections USING gist(valid_period);
CREATE INDEX idx_code_sections_citation ON code_sections(jurisdiction_id, section_citation);
CREATE INDEX idx_code_sections_fulltext ON code_sections USING gin(to_tsvector('english', raw_text));

-- =====================================================================
-- 5. 4D OPERATIONAL METRICS (Density, Design, Delay, Dollars)
-- =====================================================================
-- Directly attaches structured, quantifiable 4D dimensions to a specific code section version.
CREATE TABLE code_4d_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID NOT NULL REFERENCES code_sections(section_id) ON DELETE CASCADE,

    -- 1. DENSITY DIMENSION (Capacity Metrics)
    max_far NUMERIC(6,3),                           -- Floor Area Ratio (e.g., 2.500)
    max_height_ft NUMERIC(6,2),                     -- Maximum height limit in feet
    max_units_per_acre NUMERIC(6,2),                -- Residential density limit
    max_lot_coverage_pct NUMERIC(5,2),              -- Maximum footprint coverage percentage
    min_lot_size_sqft NUMERIC(10,2),                -- Minimum lot size required

    -- 2. DESIGN DIMENSION (Physical Envelope Constraints)
    setback_front_ft NUMERIC(6,2),
    setback_rear_ft NUMERIC(6,2),
    setback_side_ft NUMERIC(6,2),
    parking_spaces_per_unit NUMERIC(4,2),
    building_codes_referenced TEXT[],               -- Array of standards e.g., ARRAY['IBC 2024', 'ADA']

    -- 3. DELAY DIMENSION (Timeline & Bureaucratic Friction)
    admin_review_days INT,                          -- Staff level review timeline limit
    public_notice_days INT,                         -- Required notification window
    board_approval_required BOOLEAN DEFAULT FALSE,  -- Requires Planning Commission / City Council
    total_estimated_lead_time_days INT,             -- Aggregated delay metric

    -- 4. DOLLARS DIMENSION (Financial & Cost Structure)
    flat_fee_usd NUMERIC(10,2) DEFAULT 0.00,        -- Base application/processing fee
    sqft_rate_usd NUMERIC(8,4) DEFAULT 0.0000,      -- Fee per square foot rate
    valuation_pct NUMERIC(5,4) DEFAULT 0.0000,      -- Fee percentage of project valuation
    fee_formulas JSONB,                             -- Complex/custom programmatic fee formulas

    CONSTRAINT unique_metrics_per_section_version UNIQUE (section_id)
);

-- Indexing for 4D multi-variable query optimization
CREATE INDEX idx_4d_density ON code_4d_metrics(max_far, max_height_ft);
CREATE INDEX idx_4d_delay ON code_4d_metrics(total_estimated_lead_time_days, board_approval_required);
CREATE INDEX idx_4d_dollars ON code_4d_metrics(flat_fee_usd, sqft_rate_usd);

-- =====================================================================
-- 6. SPATIAL-LEGAL JUNCTION (Linking Code Sections to GIS Zones)
-- =====================================================================
CREATE TABLE code_zoning_junction (
    section_id UUID NOT NULL REFERENCES code_sections(section_id) ON DELETE CASCADE,
    zoning_district_id UUID NOT NULL REFERENCES zoning_districts(zoning_district_id) ON DELETE CASCADE,
    PRIMARY KEY (section_id, zoning_district_id)
);

-- =====================================================================
-- 7. PRODUCTION QUERY EXAMPLES
-- =====================================================================

/*
  ---------------------------------------------------------------------
  QUERY A: Point-in-Time Spatial & 4D Lookup
  "What were the active Density, Design, Delay, and Dollar constraints for
   a specific GPS coordinate on January 15, 2025?"
  ---------------------------------------------------------------------
*/
-- EXPLAIN ANALYZE
-- SELECT
--     j.name AS municipality,
--     zd.district_code,
--     cs.section_citation,
--     cs.title,
--     m.max_height_ft,
--     m.max_far,
--     m.total_estimated_lead_time_days,
--     m.flat_fee_usd,
--     (m.flat_fee_usd + (m.sqft_rate_usd * 1200) + (m.valuation_pct * 250000)) AS estimated_total_cost_for_1200sqft_build
-- FROM zoning_districts zd
-- JOIN jurisdictions j ON zd.jurisdiction_id = j.jurisdiction_id
-- JOIN code_zoning_junction czj ON zd.zoning_district_id = czj.zoning_district_id
-- JOIN code_sections cs ON czj.section_id = cs.section_id
-- JOIN code_4d_metrics m ON cs.section_id = m.section_id
-- WHERE
--     -- Spatial Intersect with Point (Longitude, Latitude)
--     ST_Contains(zd.boundary, ST_SetSRID(ST_Point(-97.7431, 30.2672), 4326))
--     -- Temporal Intersect (Active law on Jan 15, 2025)
--     AND zd.valid_period @> '2025-01-15 00:00:00+00'::timestamptz
--     AND cs.valid_period @> '2025-01-15 00:00:00+00'::timestamptz;

/*
  ---------------------------------------------------------------------
  QUERY B: 4D Comparative Policy Simulation
  "Find all zoning districts across the municipality where an ADU can be built
   with LESS than 45 days of Delay and FEES under $1,000."
  ---------------------------------------------------------------------
*/
-- SELECT
--     zd.district_code,
--     zd.district_name,
--     cs.section_citation,
--     m.total_estimated_lead_time_days AS delay_days,
--     m.flat_fee_usd AS base_dollars,
--     m.max_height_ft,
--     ST_AsGeoJSON(zd.boundary) AS spatial_envelope
-- FROM zoning_districts zd
-- JOIN code_zoning_junction czj ON zd.zoning_district_id = czj.zoning_district_id
-- JOIN code_sections cs ON czj.section_id = cs.section_id
-- JOIN code_4d_metrics m ON cs.section_id = m.section_id
-- WHERE
--     -- Current Active Code Only
--     cs.valid_period @> CURRENT_TIMESTAMP
--     -- Delay Filter
--     AND m.total_estimated_lead_time_days <= 45
--     -- Dollar Filter
--     AND m.flat_fee_usd <= 1000.00
--     -- Density / Scope Filter
--     AND cs.raw_text ILIKE '%accessory dwelling unit%';

-- =====================================================================
-- POSTGIS 3D VOLUMETRIC BUILDING ENVELOPE GENERATOR
-- Converts 2D Zoning Boundaries + 4D Setbacks & Heights into 3D Geometries
-- =====================================================================

-- 1. Create 3D Building Envelope Spatial Table
CREATE TABLE IF NOT EXISTS building_envelopes_3d (
    envelope_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID NOT NULL REFERENCES code_sections(section_id) ON DELETE CASCADE,
    zoning_district_id UUID NOT NULL REFERENCES zoning_districts(zoning_district_id) ON DELETE CASCADE,

    -- Footprint Area (2D Buildable polygon after setbacks)
    buildable_footprint_2d GEOMETRY(MultiPolygon, 4326),

    -- 3D Volumetric Extrusion Envelope (PolyhedralSurface / MultiPolygonZ)
    envelope_3d GEOMETRY(PolyhedralSurfaceZ, 4326),

    max_height_ft NUMERIC(6,2),
    calculated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_envelope_per_junction UNIQUE (section_id, zoning_district_id)
);

CREATE INDEX IF NOT EXISTS idx_envelopes_3d_spatial ON building_envelopes_3d USING gist(envelope_3d);

-- =====================================================================
-- 2. Core PostGIS Function: Compute 3D Envelope Geometry
-- =====================================================================
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
    -- Fetch District Geometry
    SELECT boundary INTO v_boundary
    FROM zoning_districts
    WHERE zoning_district_id = p_zoning_district_id;

    -- Fetch 4D Metrics (Setbacks & Height)
    SELECT
        COALESCE(max_height_ft, 35.0),
        COALESCE(setback_front_ft, 15.0),
        COALESCE(setback_rear_ft, 10.0),
        COALESCE(setback_side_ft, 5.0)
    INTO
        v_max_height, v_setback_front, v_setback_rear, v_setback_side
    FROM code_4d_metrics
    WHERE section_id = p_section_id;

    IF v_boundary IS NULL THEN
        RETURN;
    END IF;

    -- Convert average setback feet to meters (1 ft = 0.3048 m)
    v_avg_setback_meters := ((v_setback_front + v_setback_rear + v_setback_side) / 3.0) * 0.3048;
    v_extrude_meters := v_max_height * 0.3048;

    -- Reproject to Web Mercator (EPSG:3857) for metric buffer operations
    v_footprint_meters := ST_Buffer(ST_Transform(v_boundary, 3857), -v_avg_setback_meters);

    -- Fall back to original boundary if negative buffer collapses geometry entirely
    IF ST_IsEmpty(v_footprint_meters) OR v_footprint_meters IS NULL THEN
        v_footprint_meters := ST_Transform(v_boundary, 3857);
    END IF;

    -- Extrude 2D footprint polygon into 3D volumetric PolyhedralSurface
    v_envelope_3d := ST_Extrude(v_footprint_meters, 0, 0, v_extrude_meters);

    -- Transform back to WGS 84 (EPSG:4326)
    v_footprint_4326 := ST_Multi(ST_Transform(v_footprint_meters, 4326));
    v_envelope_3d := ST_Transform(v_envelope_3d, 4326);

    -- Upsert 3D Envelope Entry
    INSERT INTO building_envelopes_3d (
        section_id,
        zoning_district_id,
        buildable_footprint_2d,
        envelope_3d,
        max_height_ft,
        calculated_at
    )
    VALUES (
        p_section_id,
        p_zoning_district_id,
        v_footprint_4326,
        v_envelope_3d,
        v_max_height,
        CURRENT_TIMESTAMP
    )
    ON CONFLICT (section_id, zoning_district_id)
    DO UPDATE SET
        buildable_footprint_2d = EXCLUDED.buildable_footprint_2d,
        envelope_3d = EXCLUDED.envelope_3d,
        max_height_ft = EXCLUDED.max_height_ft,
        calculated_at = CURRENT_TIMESTAMP;

END;
$$ LANGUAGE plpgsql;

-- =====================================================================
-- 3. Trigger & Automation Setup
-- =====================================================================
CREATE OR REPLACE FUNCTION trg_fn_auto_generate_3d_envelope()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM fn_generate_3d_building_envelope(NEW.section_id, NEW.zoning_district_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_3d_envelope_generation ON code_zoning_junction;

CREATE TRIGGER trg_3d_envelope_generation
AFTER INSERT OR UPDATE ON code_zoning_junction
FOR EACH ROW
EXECUTE FUNCTION trg_fn_auto_generate_3d_envelope();
