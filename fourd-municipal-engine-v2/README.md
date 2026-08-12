# fourd-municipal-engine-v2

Second OKComputer drop of the 4D Municipal Intelligence Engine —
extended with persistence, ETL, parser, integrity, and API
subsystems on top of the v1 core. Landed as a **new folder**
alongside `../fourd-municipal-engine/` (v1) so both drops stay
inspectable as delivered.

`PACKAGE_README.md` is the upstream package documentation.
`SPEC.md` is the original v1 spec (unchanged). `SPEC_V2_ADDENDUM.md`
is the new spec for the v2 additions.

## Relationship to v1

- **All v1 core Python files are byte-identical** between v1 and v2.
  The v2 drop did not modify `lens/`, `models/`, `translator/`,
  `analysis/`, or `cli.py`.
- **v2 adds five new subsystems** and four new test files (details
  below).
- **v2 extends `pyproject.toml`** with four optional-extras groups
  (`db`, `api`, `parser`, `integrity`) plus an `all` catch-all. Core
  install stays dependency-free — every heavy dep is import-guarded
  in the module that uses it.
- **All 22 v1 tests still pass** in v2, plus 18 new stdlib-only
  tests (9 corruption risk + 9 entity resolution), plus 2 optional
  tests that skip when their extras aren't installed (parser +
  api-imports). Total: **40 pass, 2 skip** in a stdlib+pytest
  environment.

Both v1 and v2 are preserved in the repo so a reader can diff the
addendum against the base without re-extracting the source zips.

## What the v2 addendum adds

### `db/` — persistence schemas (not auto-loaded)

Two SQL schema variants for the "multiple avenues" policy in the
addendum:

- `schema_v1_bitemporal.sql` — full bitemporal design with
  valid/system TSTZRANGE + exclusion constraints (needs
  `btree_gist`), plus the 3D envelope table + trigger function and
  production queries A/B in comments.
- `schema_v2_simple.sql` — simplified variant without temporal
  ranges, plain unique constraints, same 3D envelope table.
- `schema_corruption.sql` — donors, officials, contributions,
  entities, officers, variance applications, official votes,
  variance risk scores.
- `schema_analytics_addendum.sql` — `root_causes` JSONB column,
  `stated_intent` TEXT column, `regulation_citations` table,
  `audit_metrics` table, `calculate_fee()` SQL function.
- `graph_schema.cypher` — Neo4j constraints + a 2-hop pay-to-play
  detection query in comments.
- `init-db.sql` — docker entrypoint that loads v1 schema +
  corruption + analytics addendum.
- `docker-compose.yml` — `postgis/postgis:16-3.4` db service + api
  service.
- `Dockerfile` — `python:3.11-slim` api image.
- `requirements.txt` — fastapi, uvicorn, psycopg2-binary,
  sqlalchemy, pydantic, openai, pypdf, geopandas, geoalchemy2,
  rapidfuzz.

These are inert schema/config files. Running them requires the
optional dep extras and a PostGIS-enabled database — the package
does not spin them up on install.

### `fourd_municipal_engine/parser/` — ordinance parser (pydantic optional)

- `schemas.py` — pydantic models (`DensityMetricsModel`,
  `DesignMetricsModel`, `DelayMetricsModel`, `DollarMetricsModel`,
  `FourDOrdinanceMetricsSchema`) with a graceful `ImportError`
  fallback so `import fourd_municipal_engine.parser` succeeds
  without pydantic.
- `ordinance_parser.py` — `Ordinance4DParser(api_key,
  model_name="gpt-4o-mini")`. **Dual path**: LLM structured output
  via OpenAI when an API key is present, deterministic regex
  fallback otherwise. `parse(input_data, is_pdf_path=False)`
  returns a `dict` payload with `section_data`,
  `target_zoning_codes`, `metrics_data` (max_far, max_height_ft,
  ..., flat_fee_usd, sqft_rate_usd, valuation_pct, fee_formulas),
  and — extended in v2 — `stated_intent`, `root_causes`,
  `references` reusing the v1 analysis modules.

### `fourd_municipal_engine/etl/` — SQLAlchemy ORM + batch ingestion

- `models.py` — `Jurisdiction`, `ZoningDistrict`, `CodeSection`,
  `Code4DMetrics`, `CodeZoningJunction`.
- `pipeline.py` — `Municipal4DETLPipeline(session)` with
  `get_or_create_jurisdiction`, `ingest_gis_shapefile`,
  `ingest_ordinance_with_4d_metrics`.
- `batch.py` — `BatchOrdinanceIngestor(db_url, openai_api_key=None,
  max_workers=4)` with `ThreadPoolExecutor`-driven
  `ingest_directory` for bulk loads.

Import-guarded on `sqlalchemy` / `geoalchemy2` / `geopandas` — the
module imports fine without them but instantiating a pipeline
raises with a clear message pointing at `pip install .[db]`.

### `fourd_municipal_engine/integrity/` — stdlib-only

- `entity_resolution.py` — `EntityRecord`, `EntityNormalizer`
  (`clean_name`, `parse_person_name`), `EntityResolutionMatcher`
  (`calculate_similarity`, `match_donors_to_officers`).
  **rapidfuzz** when installed, **difflib** fallback otherwise —
  9 tests exercise the difflib path and MUST pass offline.
- `corruption_risk.py` — `CorruptionRiskCalculator` with the exact
  subscore logic from the source: temporal-decay stepped
  (14/30/60/90/180 → 100/85/60/40/15/0), magnitude capped at 300%,
  network capped at 20%, recusal binary. Weights 0.35 / 0.25 /
  0.20 / 0.20. `calculate_cri(...) → {"corruption_risk_index":
  int, "subscores": {...}}`. 9 tests cover the full CRI scenario
  set and MUST pass stdlib-only.

### `fourd_municipal_engine/api/` — FastAPI endpoints (import-guarded)

- `main.py` — FastAPI `app` with `/health`, envelopes
  `by-district` / `by-location`, `sections/{id}/root-causes`,
  `sections/{id}/citations`, `fees/calculate`,
  `audit/intent-compliance`. DB via `DATABASE_URL` env,
  `psycopg2` `RealDictCursor` pattern per source. Skips at test
  time when fastapi is missing.

## Install and run

```bash
# Core install (stdlib only) — v1 features + integrity subsystem
pip install .

# Optional feature groups
pip install '.[db]'         # sqlalchemy + psycopg2 + geoalchemy2 + geopandas
pip install '.[api]'        # fastapi + uvicorn + psycopg2
pip install '.[parser]'     # pydantic + openai + pypdf
pip install '.[integrity]'  # rapidfuzz (falls back to difflib without it)
pip install '.[all]'        # everything

# Tests — 40 pass + 2 skip (skips need pydantic + fastapi)
python -m pytest tests/ -q

# CLI (unchanged from v1)
python -m fourd_municipal_engine.cli "text" --genre corporate_pr
python -m fourd_municipal_engine.cli --file ord.txt --deep-analysis --json
```

## Repo positioning

Core install is **still stdlib-only** — same category as the v1
folder. Only if you install the `db` / `api` / `parser` extras do
heavy deps enter the picture, and every non-core module fails
gracefully without them.

MIT per upstream `pyproject.toml` (compatible-per-file with the
repo's CC0 default, same pattern as `energy/` modules and v1).

No `CLAIMS.md` / `REFUTATION_PROTOCOL` yet — operational tooling,
not a claim-making artifact. The `CorruptionRiskCalculator`
weights (0.35/0.25/0.20/0.20 and the temporal decay steps) are
prime candidates for a future claim table if the module ever
grows one.

## What the addendum's "multiple avenues" policy delivered

The v2 spec called out ambiguities in the source paste and told
the implementation to ship **all variants**:

- **Schema**: bitemporal (`schema_v1_bitemporal.sql`) *and* simple
  (`schema_v2_simple.sql`) landed side-by-side.
- **Parser**: LLM path *and* regex fallback in the same
  `Ordinance4DParser`.
- **Entity matching**: rapidfuzz *and* difflib in the same
  `EntityResolutionMatcher`.
- **Audit**: audit_metrics outcome targets (v1 `AuditEngine`) *and*
  variance/CRI-based integrity audit (v2 `CorruptionRiskCalculator`)
  coexist in different modules.

Symmetric with how the reasoning module in `crossdomain-eval/`
kept both v1 and v2 alongside each other — the honest record of
what was delivered.

## Provenance

Source drop: **OKComputer_Exploring_Addon_Options** zip
(`c4b8b289-OKComputer_Exploring_Addon_Options.zip`). The drop
bundled its own `SPEC.md` (v1), `SPEC_V2_ADDENDUM.md`, `plan.md`,
and an inner `fourd-municipal-engine.zip` build alongside the
fully-materialized `fourd-repo/` tree. Only the materialized tree
is landed here; the inner zip and top-level `plan.md` are
archived in the source drop, not the repo.

40/40 tests green (plus 2 skipped for optional pydantic / fastapi
extras) verified before and after landing.

MIT (per upstream `pyproject.toml`).
