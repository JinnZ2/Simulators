# SPEC V2 ADDENDUM — Persistence, ETL, Parser, API, Integrity Modules

Adds to the existing repo (`fourd-repo`, package `fourd_municipal_engine`). Existing code MUST NOT break; existing 22 tests must keep passing. New heavy deps are OPTIONAL extras — every new Python module must be import-guarded so the core package stays stdlib-only.

## Multiple avenues policy (user instruction)
Where the source paste is ambiguous, implement ALL variants:
- **Schema**: TWO SQL variants — `schema_v1_bitemporal.sql` (valid/system TSTZRANGE + exclusion constraints, btree_gist) and `schema_v2_simple.sql` (no temporal ranges, plain unique constraints). Both include the 3D envelope table + trigger function.
- **Parser**: dual path — LLM structured output (OpenAI) when API key present, deterministic regex fallback otherwise.
- **Entity matching**: rapidfuzz when installed, difflib fallback otherwise.
- **Audit**: Path A (audit_metrics outcome targets) + Path B (variance/CRI-based integrity audit).

## New layout
```
fourd-repo/
├── db/
│   ├── schema_v1_bitemporal.sql      # full bitemporal + PostGIS + 3D envelope + production queries A/B (comments)
│   ├── schema_v2_simple.sql          # simplified variant + 3D envelope
│   ├── schema_corruption.sql         # donors/officials/contributions/entities/officers/variance_applications/official_votes/variance_risk_scores
│   ├── schema_analytics_addendum.sql # root_causes JSONB, stated_intent TEXT cols; regulation_citations; audit_metrics; calculate_fee() SQL fn
│   ├── graph_schema.cypher           # Neo4j constraints + 2-hop pay-to-play detection query (comments)
│   ├── init-db.sql                   # docker entrypoint: v1 schema + corruption + addendum
│   ├── docker-compose.yml            # postgis/postgis:16-3.4 db + api service
│   ├── Dockerfile                    # python:3.11-slim api image
│   └── requirements.txt              # fastapi, uvicorn[standard], psycopg2-binary, sqlalchemy, pydantic, openai, pypdf, geopandas, geoalchemy2, rapidfuzz
├── fourd_municipal_engine/
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── schemas.py                # pydantic models: DensityMetricsModel, DesignMetricsModel, DelayMetricsModel, DollarMetricsModel, FourDOrdinanceMetricsSchema (graceful ImportError -> pydantic optional)
│   │   └── ordinance_parser.py       # Ordinance4DParser (LLM + regex fallback, parse_pdf, parse()->dict payload)
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── models.py                 # SQLAlchemy ORM: Jurisdiction, ZoningDistrict, CodeSection, Code4DMetrics, CodeZoningJunction
│   │   ├── pipeline.py               # Municipal4DETLPipeline (get_or_create_jurisdiction, ingest_gis_shapefile, ingest_ordinance_with_4d_metrics)
│   │   └── batch.py                  # BatchOrdinanceIngestor (ThreadPoolExecutor, ingest_directory)
│   ├── integrity/
│   │   ├── __init__.py               # STDLIB-ONLY (rapidfuzz optional)
│   │   ├── entity_resolution.py      # EntityRecord, EntityNormalizer, EntityResolutionMatcher
│   │   └── corruption_risk.py        # CorruptionRiskCalculator (weights 0.35/0.25/0.20/0.20; subscore functions exactly per source)
│   └── api/
│       ├── __init__.py
│       └── main.py                   # FastAPI app: /health, envelopes by-district/by-location, sections/{id}/root-causes, sections/{id}/citations, fees/calculate, audit/intent-compliance (import-guarded)
└── tests/
    ├── test_parser_regex.py          # regex fallback extraction (from source audit suite) — needs pydantic; skip if missing
    ├── test_entity_resolution.py     # stdlib/difflib path MUST run offline
    ├── test_corruption_risk.py       # full CRI suite from source (9 tests) — stdlib, MUST run offline
    └── test_api_imports.py           # skip-if-missing import smoke tests
```

## Key interface contracts
- `Ordinance4DParser(api_key: Optional[str]=None, model_name="gpt-4o-mini")`; `.parse(input_data: str, is_pdf_path=False) -> Dict` with keys `section_data` {citation,title,raw_text,summary}, `target_zoning_codes`, `metrics_data` (keys per source: max_far, max_height_ft, max_units_per_acre, max_lot_coverage_pct, min_lot_size_sqft, setback_front/rear/side_ft, parking_spaces_per_unit, building_codes, admin_review_days, public_notice_days, board_approval_required, total_lead_time_days, flat_fee_usd, sqft_rate_usd, valuation_pct, fee_formulas). Regex fallback must extract from the source sample: flat fee $450.00, $0.85 per sq ft, 0.25% valuation, 18 ft height, 30 days, IRC 2024. ALSO extend regex fallback to extract: stated_intent (Purpose/Intent block), root_causes (keyword categories — reuse RegulationRootCauseAnalyzer from analysis), cross-references (reuse CitationGraph) and include them in the payload as `stated_intent`, `root_causes`, `references` keys.
- `EntityNormalizer.clean_name(name)->str`; `.parse_person_name(name)->Tuple[str,str]`; `EntityResolutionMatcher(match_threshold=0.88)`; `.calculate_similarity(r1,r2)->float`; `.match_donors_to_officers(donors,officers)->List[Dict]`. rapidfuzz if available else difflib.
- `CorruptionRiskCalculator` — exact subscore logic from source (temporal decay steps 14/30/60/90/180 → 100/85/60/40/15/0; magnitude capped at 300%; network capped at 20%; recusal binary). `calculate_cri(...) -> {"corruption_risk_index": int, "subscores": {...}}`.
- `Municipal4DETLPipeline(session)` methods per source. `BatchOrdinanceIngestor(db_url, openai_api_key=None, max_workers=4)`, `.ingest_directory(directory_path, jurisdiction_name, state_code, fips_code)`.
- FastAPI app `app` in `fourd_municipal_engine.api.main`; DB via `DATABASE_URL` env; endpoints per source + addendum roadmap endpoints. psycopg2 RealDictCursor pattern per source.

## pyproject changes
Add optional extras: `db = [sqlalchemy, psycopg2-binary, geoalchemy2, geopandas]`, `api = [fastapi, uvicorn, psycopg2-binary]`, `parser = [pydantic, openai, pypdf]`, `integrity = [rapidfuzz]`, `all = [...]`. Core install stays dependency-free.

## Test rules
- Offline tests (integrity, corruption_risk) MUST pass with stdlib only.
- pydantic-dependent tests: `pytest.importorskip("pydantic")`.
- API/ETL tests: importorskip; no live DB required.
- `python -m pytest tests/ -q` must be green in an env with only stdlib+pytest (+pydantic if installable).
