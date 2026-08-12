# fourd-municipal-engine

Stdlib-only Python package combining a **density-normalized 4D language
lens** with a **municipal-code translator + analysis pipeline**.
Landed from an OKComputer full-repo build. `PACKAGE_README.md` is the
upstream package documentation (install, quickstart, module map,
roadmap). This file explains where the folder sits in the repo, the
two "4D" meanings it juggles, and how to run it.

## Two independent "4D" ontologies, one package

The package deliberately uses "4D" for two different things — not a
naming accident, they are the two lenses the tool combines:

**4D Language Lens (D1–D4)** — analyzes *how text is written*, not
what it says. Each dimension is density-normalized (hits per 100
tokens), saturated to [0, 1], and weighted into a scalar
`manipulation_index` plus a `cognitive_energy` estimate.

- **D1 Agency Routing** — passive voice, nominalizations, expletive
  subjects (hiding who did what).
- **D2 Affective Impedance** — amplifiers, honorifics, punctuation
  intensity (emotional load pressure).
- **D3 Reality Construction** — reification, binary compression,
  evidentiality weakeners (turning abstractions into facts).
- **D4 Iconic / Graphic Mass** — acronyms, capitalization shifts,
  emoji density (visual pressure).

Two engines: `FourDLens` (fixed thresholds) and `DynamicFourDLens`
(re-weights per genre — a "critical failure" is benign in a technical
report, loaded in corporate PR). Genre baselines and context rules
live in `models/vectors.py`; five genres shipped:
`GENERAL`, `CORPORATE_PR`, `LEGAL_CONTRACT`, `TECHNICAL_REPORT`,
`CASUAL_SOCIAL`.

**4D Municipal Code Entity** — analyzes *what an ordinance actually
does*, structured across four regulatory axes plus temporal and
spatial metadata. Fields in `FourDMunicipalCodeEntity`
(`models/municipal.py`):

- **Density** — FAR, height, units/acre, lot coverage.
- **Design** — setbacks, parking ratios, referenced building codes.
- **Delay** — review days, public notice, board approvals, lead time.
- **Dollars** — flat fees, per-sqft rates, valuation percentages.
- **Temporal** — effective / expiration dates, supersession chain.
- **Spatial** — zoning-district links.

## Package modules

| Path | Purpose |
|---|---|
| `models/vectors.py` | `Genre` enum, `GenreProfile`, `GENRE_PROFILES` table, `ContextRule`, `VectorSignature`, `DynamicVectorSignature`. |
| `models/municipal.py` | `MunicipalTranslationResult`, `FeeItem`, `RegulationReference`, `AuditMetric`, `Density`/`Design`/`Delay`/`Dollars` metric dataclasses, `TemporalMetadata`, `FourDMunicipalCodeEntity`. |
| `lens/static.py` | `FourDLens` — fixed-threshold analyzer. |
| `lens/dynamic.py` | `DynamicFourDLens` — genre-calibrated with context rules. |
| `translator/core.py` | `MunicipalCodeTranslator` — 20+ legalese → plain-English jargon map, fee-regex extractor, purpose/intent block extractor. |
| `analysis/root_cause.py` | `RegulationRootCauseAnalyzer` — extracts stated intents (public safety, affordable housing, environmental, traffic, economic development). |
| `analysis/citations.py` | `CitationGraph` — classifies references into `municipal` / `federal` / `state` / `industry_standard`. |
| `analysis/fees.py` | `FeeExplorationEngine` — flat + per-sqft + %-of-valuation + project cost calculator. |
| `analysis/audit.py` | `AuditEngine` — KPI regex ("reduce X by N%", "no later than DATE"), auditability score in [0, 1]. |
| `analysis/pipeline.py` | `AdvancedAnalysisPipeline` — glue that fills a `MunicipalTranslationResult` with root causes, citations, audit metrics, upgraded fees. |
| `cli.py` | `argparse` CLI, entry point `fourd-municipal-engine` / `python -m fourd_municipal_engine.cli`. |

## Install and run

```bash
pip install .            # from fourd-municipal-engine/
pip install '.[dev]'     # add pytest

# Tests (22 total)
python -m pytest tests/ -q

# CLI — language lens, genre-calibrated
python -m fourd_municipal_engine.cli \
  "We are thrilled to announce the realignment!" --genre corporate_pr

# CLI — deep municipal analysis, JSON output
python -m fourd_municipal_engine.cli --file ordinance.txt \
  --genre legal_contract --citation "Section 12.4" --deep-analysis --json
```

## Repo positioning

**Stdlib-only** (Python 3.9+). No numpy, no scipy — the entire lens
pipeline is regex + dataclasses. That means it belongs with the
default-genre packages in this repo, not the exemption cluster
(`energy/`, `play-sims/`, `climate-modeling/`,
`relational/geometric_rag/`, `crossdomain-eval/`).

MIT licensed per the upstream `pyproject.toml`. Repo default is CC0
but a per-file MIT header is compatible (same pattern as `energy/`
modules).

No `CLAIMS.md` / `REFUTATION_PROTOCOL` yet — this is operational
tooling (translator + extractor), not a claim-making artifact of its
own. If it grows into a claim table (e.g. "the density normalization
in D1–D4 is genre-independent within tolerance X"), that lands
alongside the code.

## Sibling in the repo family

- `crossdomain-eval/` — the previous OKComputer drop. Also a Python
  package built from a SPEC.md, but relies on sympy/numpy/scipy and
  ships its own CLI. Same landing shape as this folder
  (`PACKAGE_README.md` preserved, folder README written on top).

## Roadmap (from upstream)

- **Phase 1 (landed)** — operational extraction on raw ordinance text.
- **Phase 2** — temporal versioning: track amendments, supersession
  chains, and effective-date timelines via `TemporalMetadata`.
- **Phase 3** — GIS overlay: join
  `FourDMunicipalCodeEntity.spatial_zoning_districts` to GeoJSON
  zoning geometries for map-based regulation queries.

## Provenance

Source drop: **OKComputer_Build_Full_Repo** zip
(`f99b31e6-OKComputer_Build_Full_Repo.zip`). The drop bundled its own
`SPEC.md`, `plan.md`, and an inner `fourd-municipal-engine.zip` build
alongside the fully-materialized `fourd-repo/` tree. Only the
materialized tree is landed here; the inner zip and top-level `plan.md`
described the build itself and are archived in the source drop, not
the repo. All 22 tests green before and after landing.

MIT (per upstream `pyproject.toml`).
