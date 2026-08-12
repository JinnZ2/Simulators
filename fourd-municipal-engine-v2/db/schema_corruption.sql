-- =====================================================================
-- CORRUPTION / CAMPAIGN-FINANCE DETECTION SCHEMA
-- =====================================================================

-- Enable Spatial & Utility Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- Trigram indexing for fuzzy text lookups

-- =====================================================================
-- 1. CAMPAIGN FINANCE & DONOR REPOSITORY
-- =====================================================================

CREATE TABLE IF NOT EXISTS campaign_donors (
    donor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_name VARCHAR(255) NOT NULL,
    cleaned_name VARCHAR(255) NOT NULL,
    employer VARCHAR(255),
    occupation VARCHAR(255),
    address_street VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_donors_trgm ON campaign_donors USING gin(cleaned_name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS public_officials (
    official_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(100), -- e.g., 'City Council Member', 'Planning Commissioner'
    jurisdiction VARCHAR(100) NOT NULL,
    term_start DATE,
    term_end DATE
);

CREATE TABLE IF NOT EXISTS campaign_contributions (
    contribution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    donor_id UUID NOT NULL REFERENCES campaign_donors(donor_id) ON DELETE CASCADE,
    official_id UUID NOT NULL REFERENCES public_officials(official_id) ON DELETE CASCADE,
    amount NUMERIC(12,2) NOT NULL,
    contribution_date DATE NOT NULL,
    election_cycle INT NOT NULL,
    committee_name VARCHAR(255),
    source_document_url TEXT,
    source_doc_hash VARCHAR(64) -- SHA-256 hash for audit verification
);

CREATE INDEX idx_contributions_date ON campaign_contributions(contribution_date);

-- =====================================================================
-- 2. CORPORATE ENTITY & BENEFICIAL OWNERSHIP SCHEMA
-- =====================================================================

CREATE TABLE IF NOT EXISTS corporate_entities (
    entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_name VARCHAR(255) NOT NULL,
    filing_number VARCHAR(100) UNIQUE,
    entity_type VARCHAR(50), -- e.g., 'LLC', 'LP', 'Inc'
    formation_date DATE,
    registered_agent_name VARCHAR(255),
    principal_address VARCHAR(255),
    state_of_incorporation VARCHAR(2)
);

CREATE INDEX idx_entities_trgm ON corporate_entities USING gin(entity_name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS entity_officers (
    officer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID NOT NULL REFERENCES corporate_entities(entity_id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(100), -- 'Manager', 'Managing Member', 'Director', 'Registered Agent'
    associated_address VARCHAR(255)
);

-- =====================================================================
-- 3. LAND USE, PARCELS & VARIANCE AUDIT TRAIL
-- =====================================================================

CREATE TABLE IF NOT EXISTS variance_applications (
    application_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    applicant_entity_id UUID REFERENCES corporate_entities(entity_id),
    applicant_raw_name VARCHAR(255) NOT NULL,
    parcel_id VARCHAR(100) NOT NULL,
    citation_section VARCHAR(100),
    requested_date DATE NOT NULL,
    decision_date DATE,
    status VARCHAR(50) DEFAULT 'PENDING', -- 'APPROVED', 'DENIED', 'PENDING'

    -- Variance Magnitude Metrics
    base_far NUMERIC(6,2),
    requested_far NUMERIC(6,2),
    base_height_ft NUMERIC(6,2),
    requested_height_ft NUMERIC(6,2),

    source_minutes_url TEXT,
    source_doc_hash VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS official_votes (
    vote_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id UUID NOT NULL REFERENCES variance_applications(application_id) ON DELETE CASCADE,
    official_id UUID NOT NULL REFERENCES public_officials(official_id) ON DELETE CASCADE,
    vote VARCHAR(20) NOT NULL, -- 'YES', 'NO', 'ABSTAIN', 'ABSENT', 'RECUSED'
    recusal_filed BOOLEAN DEFAULT FALSE,
    vote_date DATE NOT NULL
);

-- Calculated Risk Scores Table
CREATE TABLE IF NOT EXISTS variance_risk_scores (
    score_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id UUID UNIQUE NOT NULL REFERENCES variance_applications(application_id) ON DELETE CASCADE,
    corruption_risk_index INT CHECK (corruption_risk_index BETWEEN 0 AND 100),
    temporal_proximity_score NUMERIC(5,2),
    variance_magnitude_score NUMERIC(5,2),
    network_density_score NUMERIC(5,2),
    recusal_flag_score NUMERIC(5,2),
    flagged_reasons JSONB DEFAULT '[]'::jsonb,
    computed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
