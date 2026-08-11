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

## Tests

```bash
python -m pytest tests/ -q
```
