-- =====================================================================
-- ANALYTICS ADDENDUM (Idempotent)
-- Adds intent/root-cause columns, citation graph, audit metrics,
-- and a fee calculation function to the 4D municipal code schema.
-- =====================================================================

-- 1. Extend code_sections with intent & root-cause analysis columns
ALTER TABLE code_sections ADD COLUMN IF NOT EXISTS root_causes JSONB DEFAULT '[]'::jsonb;
ALTER TABLE code_sections ADD COLUMN IF NOT EXISTS stated_intent TEXT;

-- 2. Regulation citation graph
CREATE TABLE IF NOT EXISTS regulation_citations (
    from_section_id UUID REFERENCES code_sections(section_id),
    to_citation VARCHAR(200),       -- e.g., 'IBC 2024 § 101.2' or another section_id
    relationship_type VARCHAR(50),  -- 'supersedes', 'requires', 'implements'
    PRIMARY KEY (from_section_id, to_citation)
);

-- 3. Audit / outcome metrics
CREATE TABLE IF NOT EXISTS audit_metrics (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID REFERENCES code_sections(section_id),
    metric_description TEXT,        -- e.g., "Reduce runoff by 30%"
    target_value NUMERIC,
    measured_value NUMERIC,
    data_source VARCHAR(500),       -- URL of open data portal
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4. Fee Exploration Engine: dynamic fee calculator
CREATE OR REPLACE FUNCTION calculate_fee(
    p_section_id UUID,
    p_sqft NUMERIC,
    p_valuation NUMERIC
)
RETURNS TABLE (fee_type TEXT, amount NUMERIC) AS $$
DECLARE
    v_flat_fee NUMERIC;
    v_sqft_rate NUMERIC;
    v_valuation_pct NUMERIC;
BEGIN
    SELECT
        COALESCE(m.flat_fee_usd, 0),
        COALESCE(m.sqft_rate_usd, 0),
        COALESCE(m.valuation_pct, 0)
    INTO v_flat_fee, v_sqft_rate, v_valuation_pct
    FROM code_4d_metrics m
    WHERE m.section_id = p_section_id;

    IF v_flat_fee IS NULL THEN
        RETURN; -- no metrics row for this section
    END IF;

    IF v_flat_fee > 0 THEN
        fee_type := 'flat_fee';
        amount := v_flat_fee;
        RETURN NEXT;
    END IF;

    IF v_sqft_rate > 0 THEN
        fee_type := 'sqft_fee';
        amount := v_sqft_rate * p_sqft;
        RETURN NEXT;
    END IF;

    IF v_valuation_pct > 0 THEN
        fee_type := 'valuation_fee';
        amount := v_valuation_pct * p_valuation;
        RETURN NEXT;
    END IF;

    RETURN;
END;
$$ LANGUAGE plpgsql;
