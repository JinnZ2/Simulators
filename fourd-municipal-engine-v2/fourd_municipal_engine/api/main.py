"""4D Municipal Ordinance & 3D Spatial Envelope API.

FastAPI application (optional ``api`` extra). Faithful port of the source
envelope service plus the V2 analytics roadmap endpoints:

- GET /health
- GET /api/v1/envelopes/by-district/{zoning_district_id}
- GET /api/v1/envelopes/by-location
- GET /api/v1/sections/{section_id}/root-causes
- GET /api/v1/sections/{section_id}/citations
- GET /api/v1/fees/calculate
- GET /api/v1/audit/intent-compliance

Database access uses psycopg2 with RealDictCursor; the connection string
comes from the DATABASE_URL environment variable.
"""

import os
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor

from fourd_municipal_engine.integrity import CorruptionRiskCalculator

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://municipal_user:spatial_pass_2026@db:5432/municipal_4d",
)

app = FastAPI(
    title="4D Municipal Ordinance & 3D Spatial Envelope API",
    description=(
        "Extracts 4D ordinance metrics, serves PostGIS-calculated 3D "
        "volumetric building envelopes, and exposes V2 analytics "
        "(root causes, citation graph, fee calculator, intent-compliance audit)."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_conn():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------


class Envelope3DResponse(BaseModel):
    envelope_id: str
    section_citation: str
    zoning_district_code: str
    max_height_ft: float
    buildable_footprint_geojson: Dict[str, Any]
    envelope_3d_geojson: Dict[str, Any]
    metrics_4d: Dict[str, Any]


class SpatialLocationQuery(BaseModel):
    latitude: float = Field(..., example=30.2672)
    longitude: float = Field(..., example=-97.7431)


class RootCausesResponse(BaseModel):
    section_id: str
    stated_intent: Optional[str] = None
    root_causes: List[Dict[str, Any]] = []


class CitationRow(BaseModel):
    from_section_id: str
    to_citation: str
    relationship_type: Optional[str] = None


class FeeBreakdownResponse(BaseModel):
    section_id: str
    sqft: float
    valuation: float
    breakdown: List[Dict[str, Any]]
    total_usd: float


class ApplicationRiskResult(BaseModel):
    application_id: str
    status: Optional[str] = None
    contributing_officials: int
    corruption_risk_index: int
    subscores: Dict[str, Any]


class IntentComplianceResponse(BaseModel):
    jurisdiction_id: str
    applications_analyzed: int
    pct_approved: float
    mean_cri: float
    max_cri: int
    applications: List[ApplicationRiskResult]


# ---------------------------------------------------------------------------
# Core service endpoints (source port)
# ---------------------------------------------------------------------------


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "4D Ordinance API"}


@app.get("/api/v1/envelopes/by-district/{zoning_district_id}", response_model=Envelope3DResponse)
def get_envelope_by_district(zoning_district_id: UUID, conn=Depends(get_db_conn)):
    """Fetches the 3D GeoJSON envelope and 4D metrics for a specific Zoning District ID."""
    query = """
        SELECT
            e.envelope_id,
            s.citation AS section_citation,
            z.district_code AS zoning_district_code,
            e.max_height_ft,
            ST_AsGeoJSON(e.buildable_footprint_2d)::json AS buildable_footprint_geojson,
            ST_AsGeoJSON(e.envelope_3d)::json AS envelope_3d_geojson,
            to_jsonb(m.*) - 'metric_id' - 'section_id' AS metrics_4d
        FROM building_envelopes_3d e
        JOIN code_sections s ON e.section_id = s.section_id
        JOIN zoning_districts z ON e.zoning_district_id = z.zoning_district_id
        JOIN code_4d_metrics m ON s.section_id = m.section_id
        WHERE e.zoning_district_id = %s
        LIMIT 1;
    """
    with conn.cursor() as cur:
        cur.execute(query, (str(zoning_district_id),))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="3D Envelope not found for the specified district.")

        row["envelope_id"] = str(row["envelope_id"])
        return row


@app.get("/api/v1/envelopes/by-location", response_model=Envelope3DResponse)
def get_envelope_by_location(
    lat: float = Query(..., description="Latitude in WGS84"),
    lon: float = Query(..., description="Longitude in WGS84"),
    conn=Depends(get_db_conn),
):
    """Spatial Point Intersect: Finds the zoning district at a GPS coordinate and returns its 3D building envelope."""
    query = """
        SELECT
            e.envelope_id,
            s.citation AS section_citation,
            z.district_code AS zoning_district_code,
            e.max_height_ft,
            ST_AsGeoJSON(e.buildable_footprint_2d)::json AS buildable_footprint_geojson,
            ST_AsGeoJSON(e.envelope_3d)::json AS envelope_3d_geojson,
            to_jsonb(m.*) - 'metric_id' - 'section_id' AS metrics_4d
        FROM zoning_districts z
        JOIN building_envelopes_3d e ON z.zoning_district_id = e.zoning_district_id
        JOIN code_sections s ON e.section_id = s.section_id
        JOIN code_4d_metrics m ON s.section_id = m.section_id
        WHERE ST_Contains(z.boundary, ST_SetSRID(ST_Point(%s, %s), 4326))
        LIMIT 1;
    """
    with conn.cursor() as cur:
        cur.execute(query, (lon, lat))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No zoning district or 3D envelope found at this coordinate.")

        row["envelope_id"] = str(row["envelope_id"])
        return row


# ---------------------------------------------------------------------------
# V2 analytics roadmap endpoints
# ---------------------------------------------------------------------------


@app.get("/api/v1/sections/{section_id}/root-causes", response_model=RootCausesResponse)
def get_section_root_causes(section_id: UUID, conn=Depends(get_db_conn)):
    """Returns the stored root-cause analysis (JSONB) and stated intent for a code section.

    Columns are added by db/schema_analytics_addendum.sql and populated by the
    parser during ingestion.
    """
    query = """
        SELECT section_id, root_causes, stated_intent
        FROM code_sections
        WHERE section_id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (str(section_id),))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Code section not found.")
        return {
            "section_id": str(row["section_id"]),
            "root_causes": row.get("root_causes") or [],
            "stated_intent": row.get("stated_intent"),
        }


@app.get("/api/v1/sections/{section_id}/citations", response_model=List[CitationRow])
def get_section_citations(section_id: UUID, conn=Depends(get_db_conn)):
    """Returns the outgoing citation graph edges (regulation_citations) for a code section."""
    query = """
        SELECT from_section_id, to_citation, relationship_type
        FROM regulation_citations
        WHERE from_section_id = %s
        ORDER BY to_citation;
    """
    with conn.cursor() as cur:
        cur.execute(query, (str(section_id),))
        rows = cur.fetchall()
        return [
            {
                "from_section_id": str(r["from_section_id"]),
                "to_citation": r["to_citation"],
                "relationship_type": r.get("relationship_type"),
            }
            for r in rows
        ]


@app.get("/api/v1/fees/calculate", response_model=FeeBreakdownResponse)
def calculate_fees(
    section_id: UUID = Query(..., description="Code section whose 4D fee metrics apply"),
    sqft: float = Query(..., description="Project square footage"),
    valuation: float = Query(..., description="Project valuation in USD"),
    conn=Depends(get_db_conn),
):
    """Dynamic fee estimation via the SQL calculate_fee() function (schema_analytics_addendum.sql)."""
    query = "SELECT * FROM calculate_fee(%s, %s, %s);"
    with conn.cursor() as cur:
        cur.execute(query, (str(section_id), sqft, valuation))
        rows = cur.fetchall()
        breakdown = [
            {"fee_type": r["fee_type"], "amount_usd": float(r["amount"])} for r in rows
        ]
        total = sum(item["amount_usd"] for item in breakdown)
        return {
            "section_id": str(section_id),
            "sqft": sqft,
            "valuation": valuation,
            "breakdown": breakdown,
            "total_usd": total,
        }


@app.get("/api/v1/audit/intent-compliance", response_model=IntentComplianceResponse)
def audit_intent_compliance(
    jurisdiction_id: str = Query(
        ...,
        description=(
            "Jurisdiction name (public_officials.jurisdiction) or jurisdictions.jurisdiction_id "
            "(matched via jurisdiction name lookup when the bitemporal schema is present)."
        ),
    ),
    conn=Depends(get_db_conn),
):
    """Variance-based integrity audit (Path B of the V2 audit roadmap).

    For each variance application whose deciding officials received campaign
    contributions from the applicant (linked by fuzzy entity resolution upstream
    or exact cleaned-name match here), compute the Corruption Risk Index with
    the integrity module and return per-application CRI plus aggregate stats.

    SQL notes (tables from db/schema_corruption.sql):
      * variance_applications: magnitude metrics (base/requested FAR & height),
        decision_date, status.
      * official_votes: links applications to officials (vote, recusal_filed,
        vote_date).
      * campaign_contributions: donor -> official funding trail.
      * Jurisdiction filter: public_officials.jurisdiction matches the given
        jurisdiction name; a subquery also resolves a jurisdictions row by
        jurisdiction_id so a UUID can be passed instead.
    """
    # Per application, for each official who voted AND received a contribution
    # from a donor whose cleaned name matches the applicant name, expose the
    # inputs needed by CorruptionRiskCalculator.
    query = """
        SELECT
            va.application_id,
            va.status,
            va.base_far,
            va.requested_far,
            va.base_height_ft,
            va.requested_height_ft,
            ov.vote,
            ov.recusal_filed,
            (ov.vote_date - cc.contribution_date) AS days_to_vote,
            cc.amount AS contribution_amount,
            totals.total_amount AS official_total_contributions
        FROM variance_applications va
        JOIN official_votes ov ON ov.application_id = va.application_id
        JOIN public_officials po ON po.official_id = ov.official_id
        JOIN campaign_contributions cc ON cc.official_id = po.official_id
        JOIN campaign_donors cd ON cd.donor_id = cc.donor_id
            AND cd.cleaned_name = UPPER(TRIM(va.applicant_raw_name))
        JOIN (
            SELECT official_id, SUM(amount) AS total_amount
            FROM campaign_contributions
            GROUP BY official_id
        ) totals ON totals.official_id = po.official_id
        WHERE po.jurisdiction = %s
           OR po.jurisdiction = (
               SELECT j.name FROM jurisdictions j
               WHERE j.jurisdiction_id::text = %s
           )
        ORDER BY va.application_id;
    """
    with conn.cursor() as cur:
        cur.execute(query, (jurisdiction_id, jurisdiction_id))
        rows = cur.fetchall()

    # Aggregate contribution rows per application: max CRI inputs.
    by_app: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        app_id = str(row["application_id"])
        entry = by_app.setdefault(
            app_id,
            {
                "application_id": app_id,
                "status": row.get("status"),
                "contributing_officials": 0,
                "cri_inputs": [],
            },
        )
        entry["contributing_officials"] += 1
        total = float(row["official_total_contributions"] or 0)
        amount = float(row["contribution_amount"] or 0)
        funding_share = (amount / total * 100.0) if total > 0 else 0.0
        entry["cri_inputs"].append(
            {
                "days_to_vote": row.get("days_to_vote"),
                "base_far": float(row.get("base_far") or 0),
                "requested_far": float(row.get("requested_far") or 0),
                "base_height": float(row.get("base_height_ft") or 0),
                "requested_height": float(row.get("requested_height_ft") or 0),
                "developer_funding_share_pct": funding_share,
                "voted_yes": (row.get("vote") or "").upper() == "YES",
                "has_contribution": True,
                "recusal_filed": bool(row.get("recusal_filed")),
            }
        )

    applications: List[Dict[str, Any]] = []
    for entry in by_app.values():
        # Use the highest-risk contributing official's inputs per application.
        best = None
        for inputs in entry["cri_inputs"]:
            result = CorruptionRiskCalculator.calculate_cri(**inputs)
            if best is None or result["corruption_risk_index"] > best["corruption_risk_index"]:
                best = result
        applications.append(
            {
                "application_id": entry["application_id"],
                "status": entry["status"],
                "contributing_officials": entry["contributing_officials"],
                "corruption_risk_index": best["corruption_risk_index"],
                "subscores": best["subscores"],
            }
        )

    count = len(applications)
    approved = sum(1 for a in applications if (a["status"] or "").upper() == "APPROVED")
    cris = [a["corruption_risk_index"] for a in applications]
    return {
        "jurisdiction_id": jurisdiction_id,
        "applications_analyzed": count,
        "pct_approved": round(approved / count * 100.0, 2) if count else 0.0,
        "mean_cri": round(sum(cris) / count, 2) if count else 0.0,
        "max_cri": max(cris) if cris else 0,
        "applications": applications,
    }
