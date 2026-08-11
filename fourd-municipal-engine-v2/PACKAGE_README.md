# 4D Municipal Intelligence Engine

A pure-Python (stdlib-only) toolkit that combines two ideas:

1. **4D Language Lens** — a density-normalized linguistic analysis engine that
   scores text across four manipulation dimensions, with a static engine and a
   genre-calibrated dynamic engine.
2. **Municipal Code tooling** — a translator that converts regulatory legalese
   into plain English and an advanced analysis pipeline that extracts root
   causes, citation graphs, fee structures, and audit metrics from ordinance
   text.

## Install

```bash
pip install .            # from this repo
pip install '.[dev]'     # with pytest for running the test suite
```

Python 3.9+; no runtime dependencies.

## Quickstart

### CLI

```bash
# Human-readable lens report, genre-calibrated for corporate PR
python -m fourd_municipal_engine.cli "We are thrilled to announce the realignment!" \
    --genre corporate_pr

# Deep analysis of an ordinance, machine-readable output
python -m fourd_municipal_engine.cli --file ordinance.txt \
    --genre legal_contract --citation "Section 12.4" --deep-analysis --json
```

Flags: `--genre {general,corporate_pr,legal_contract,technical_report,casual_social}`,
`--deep-analysis` (translator + advanced pipeline), `--citation "Section X.Y"`,
`--json`, `--file PATH`.

### Python API

```python
from fourd_municipal_engine import DynamicFourDLens, Genre
from fourd_municipal_engine.translator.core import MunicipalCodeTranslator
from fourd_municipal_engine.analysis.pipeline import AdvancedAnalysisPipeline

lens = DynamicFourDLens()
sig = lens.analyze("The critical failure was terminated.", genre=Genre.TECHNICAL_REPORT)
print(sig.manipulation_index, sig.normalized_scores)

translator = MunicipalCodeTranslator()
result = translator.translate(ordinance_text, citation="Section 12.4")
result = AdvancedAnalysisPipeline(translator).analyze(result, ordinance_text)
print(result.plain_english_summary, result.fees, result.auditability_score)
```

## Module map

```
fourd_municipal_engine/
├── models/
│   ├── vectors.py      # Genre, GenreProfile, GENRE_PROFILES, ContextRule, VectorSignature, DynamicVectorSignature
│   └── municipal.py    # MunicipalTranslationResult, FeeItem, RegulationReference, AuditMetric,
│                       # Density/Design/Delay/Dollars metrics, TemporalMetadata, FourDMunicipalCodeEntity
├── lens/
│   ├── static.py       # FourDLens — fixed-threshold 4D analyzer
│   └── dynamic.py      # DynamicFourDLens — genre baselines + context rules
├── translator/core.py  # MunicipalCodeTranslator — jargon map, fee & purpose extraction
├── analysis/
│   ├── root_cause.py   # RegulationRootCauseAnalyzer
│   ├── citations.py    # CitationGraph (municipal / federal / state / industry_standard)
│   ├── fees.py         # FeeExplorationEngine (flat + per-sqft + %-of-valuation, project cost calc)
│   ├── audit.py        # AuditEngine (KPI extraction, auditability score)
│   └── pipeline.py     # AdvancedAnalysisPipeline
└── cli.py              # argparse CLI
```

## The four dimensions

**Language lens (D1–D4):**

- **D1 — Agency Routing**: passive voice, nominalizations, expletive subjects —
  how text hides who did what.
- **D2 — Affective Impedance**: amplifiers, honorifics, emotional injectors,
  punctuation intensity — how text manipulates emotional load.
- **D3 — Reality Construction**: reification, binary compression, evidentiality
  weakeners — how text turns abstractions into facts.
- **D4 — Iconic/Graphic Mass**: acronyms, capitalization shifts, punctuation and
  emoji density — visual/orthographic pressure.

Scores are density-normalized per 100 tokens, saturated to [0, 1], and combined
into a weighted **manipulation index** plus a **cognitive energy** estimate. The
dynamic lens re-weights each dimension with genre baselines (a "critical
failure" is benign in a technical report, loaded in corporate PR) via dampening
factors and context rules.

**Municipal code entity (the other 4D):**

- **Density** — FAR, height, units/acre, lot coverage.
- **Design** — setbacks, parking ratios, referenced building codes.
- **Delay** — review days, public notice, board approvals, lead time.
- **Dollars** — flat fees, per-sqft rates, valuation percentages.

plus **Temporal** metadata (effective dates, supersession) and **Spatial**
zoning-district links.

## Roadmap

- **Phase 1 (current)** — operational extraction: legalese translation, fee /
  intent / citation / audit extraction on raw ordinance text.
- **Phase 2** — temporal versioning: track ordinance amendments, supersession
  chains, and effective-date timelines via `TemporalMetadata`.
- **Phase 3** — GIS overlay: join `FourDMunicipalCodeEntity.spatial_zoning_districts`
  to GeoJSON zoning geometries for map-based regulation queries.

## V2: persistence, ETL, integrity & API

V2 adds a database layer, an ingestion pipeline, a campaign-finance integrity
module, and a FastAPI service — all as **optional extras**; the core package
stays stdlib-only.

### Install extras

```bash
pip install -e '.[all]'     # db + api + parser + integrity extras
pip install -e '.[api]'     # fastapi, uvicorn, psycopg2-binary only
```

### Database layout (`db/`)

Two schema variants are provided ("multiple avenues"):

- **`schema_v1_bitemporal.sql`** — full bitemporal design: valid/system time
  `TSTZRANGE` columns with exclusion constraints (btree_gist) preventing
  overlapping district/section versions, plus the 3D building-envelope table
  and trigger function.
- **`schema_v2_simple.sql`** — simplified variant: no temporal ranges, plain
  unique constraints; same 3D envelope support.

Plus:

- **`schema_corruption.sql`** — donors, officials, contributions, corporate
  entities/officers, variance applications, official votes, risk scores.
- **`schema_analytics_addendum.sql`** — `root_causes` JSONB + `stated_intent`
  columns on `code_sections`, `regulation_citations` graph, `audit_metrics`,
  and the `calculate_fee()` SQL function.
- **`graph_schema.cypher`** — Neo4j constraints + 2-hop pay-to-play query.
- **`init-db.sql`** — docker entrypoint (v1 schema + corruption + addendum).

### Docker quickstart

```bash
cd db && docker compose up
# API on :8000, PostGIS 16 on :5432 (schema auto-initialized via init-db.sql)
```

### Parser: LLM vs regex dual path

`parser/ordinance_parser.py` (`Ordinance4DParser`) uses OpenAI structured
output when an API key is configured, and falls back to a deterministic regex
extractor otherwise. Both paths return the same payload: `section_data`,
`target_zoning_codes`, `metrics_data` (the 4D metrics), plus V2 keys
`stated_intent`, `root_causes`, and `references`.

### Integrity module

`integrity/entity_resolution.py` matches campaign donors to corporate officers
(rapidfuzz when installed, difflib fallback). `integrity/corruption_risk.py`
computes a **Corruption Risk Index (0–100)**:

```
CRI = 0.35 * temporal   (days contribution->vote: 14/30/60/90/180 -> 100/85/60/40/15/0)
    + 0.25 * magnitude  (FAR/height variance increase, capped at 300%)
    + 0.20 * network    (developer funding share of official's receipts, capped at 20%)
    + 0.20 * recusal    (binary: voted YES with contribution & no recusal)
```

### API endpoints (`fourd_municipal_engine.api.main:app`)

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/api/v1/envelopes/by-district/{zoning_district_id}` | 3D GeoJSON envelope + 4D metrics for a zoning district |
| GET | `/api/v1/envelopes/by-location?lat=&lon=` | Spatial point-intersect envelope lookup |
| GET | `/api/v1/sections/{section_id}/root-causes` | Stored root-cause analysis + stated intent |
| GET | `/api/v1/sections/{section_id}/citations` | Outgoing regulation citation graph edges |
| GET | `/api/v1/fees/calculate?section_id=&sqft=&valuation=` | Dynamic fee breakdown via SQL `calculate_fee()` |
| GET | `/api/v1/audit/intent-compliance?jurisdiction_id=` | Variance-based integrity audit: per-application CRI + aggregate stats |

Run with: `uvicorn fourd_municipal_engine.api.main:app` (set `DATABASE_URL`).

## Tests

```bash
python -m pytest tests/ -q
```

Offline tests (integrity, corruption risk) run on stdlib only; pydantic/API
tests self-skip via `pytest.importorskip` when the extras are not installed.
