# SPEC.md — 4D Municipal Intelligence Engine

Single source of truth. Implement interfaces EXACTLY as specified.

## Overview
A pure-Python (stdlib-only) package that combines:
1. **4D Language Lens** — density-normalized linguistic manipulation analysis (static + genre-calibrated dynamic engines).
2. **Municipal Code Translator** — converts regulatory legalese to plain English with structured extraction.
3. **Advanced Analysis Pipeline** — root cause, citation graph, fee exploration, audit metrics.
4. **4D Municipal Code Entity model** — Density / Design / Delay / Dollars + Temporal + Spatial.

## Repo layout
```
fourd-repo/
├── pyproject.toml
├── README.md
├── fourd_municipal_engine/
│   ├── __init__.py            # re-exports public API
│   ├── models/
│   │   ├── __init__.py
│   │   ├── vectors.py         # VectorSignature (static + dynamic variants), Genre, GenreProfile, GENRE_PROFILES, ContextRule
│   │   └── municipal.py       # MunicipalTranslationResult, RegulationReference, AuditMetric, FeeItem, DensityMetrics, DesignConstraints, DelayMetrics, DollarsMetrics, TemporalMetadata, FourDMunicipalCodeEntity
│   ├── lens/
│   │   ├── __init__.py
│   │   ├── static.py          # FourDLens (exact code from source, adapted imports)
│   │   └── dynamic.py         # DynamicFourDLens (exact code from source, adapted imports)
│   ├── translator/
│   │   ├── __init__.py
│   │   └── core.py            # MunicipalCodeTranslator: jargon dictionary, legalese->plain-english mapping, fee/regex extraction, summarize()
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── root_cause.py      # RegulationRootCauseAnalyzer
│   │   ├── citations.py       # CitationGraph (extract_references)
│   │   ├── fees.py            # FeeExplorationEngine (flat fees + formulaic fees + project cost calc)
│   │   ├── audit.py           # AuditEngine (extract KPI metrics, auditability score)
│   │   └── pipeline.py        # AdvancedAnalysisPipeline
│   └── cli.py                 # argparse CLI: analyze text; flags --genre, --deep-analysis, --json
└── tests/
    ├── test_lens_static.py
    ├── test_lens_dynamic.py
    ├── test_translator.py
    ├── test_analysis.py
    └── test_cli.py
```

## Interface contracts

### models/vectors.py
- `class Genre(Enum)`: GENERAL, CORPORATE_PR, LEGAL_CONTRACT, TECHNICAL_REPORT, CASUAL_SOCIAL (auto())
- `@dataclass GenreProfile`: name:str, saturation_thresholds:Dict[str,float], weights:Dict[str,float], passivity_dampening:float, affective_dampening:float, reification_dampening:float
- `GENRE_PROFILES: Dict[Genre, GenreProfile]` — values exactly as in source paste.
- `@dataclass ContextRule`: pattern:Pattern, target_dimension:str, genre_multipliers:Dict[Genre,float], qualifying_context:Set[str]=factory(set), disqualifying_context:Set[str]=factory(set)
- `@dataclass VectorSignature` (static lens): dimension_scores, raw_counts, normalized_scores: Dict[str,float]; trace:List[str]; energy_estimate:float; manipulation_index:float
- `@dataclass DynamicVectorSignature`: adds genre_applied:str first. (To avoid field-order collision, dynamic lens uses this separate dataclass.)

### lens/static.py
`class FourDLens` with `.analyze(text: str) -> VectorSignature`. Pattern tables and logic exactly as in the user's pasted source.

### lens/dynamic.py
`class DynamicFourDLens(default_genre: Genre = Genre.GENERAL)` with `.analyze(text: str, genre: Optional[Genre] = None) -> DynamicVectorSignature`. Logic exactly as pasted source; imports Genre/GENRE_PROFILES/ContextRule from models.vectors; returns DynamicVectorSignature.

### models/municipal.py
- `@dataclass FeeItem`: description:str, amount:Optional[float], condition:str="", formula:Optional[str]=None
- `@dataclass RegulationReference`: name:str, type:str, relationship:str="references"
- `@dataclass AuditMetric`: metric_description:str, target:str="", current_value:str="", data_source:str="", status:str="unavailable"
- `@dataclass MunicipalTranslationResult`: section_citation:str, raw_text:str, plain_english_summary:str, fees:List[FeeItem]=factory(list), root_causes:List[str]=factory(list), stated_intent:str="", interconnected_regulations:List[RegulationReference]=factory(list), audit_metrics:List[AuditMetric]=factory(list), auditability_score:float=0.0, lens_signature:Optional[DynamicVectorSignature]=None
- `@dataclass DensityMetrics`: max_far/max_height_ft/max_units_per_acre/max_lot_coverage_pct: Optional[float]=None
- `@dataclass DesignConstraints`: setback_front_ft/setback_rear_ft/setback_side_ft/parking_spaces_per_unit: Optional[float]=None; building_codes_referenced:List[str]=factory(list)
- `@dataclass DelayMetrics`: admin_review_days:Optional[int]=None, public_notice_days:Optional[int]=None, board_approval_required:bool=False, total_estimated_lead_time_days:Optional[int]=None
- `@dataclass DollarsMetrics`: flat_fees:float=0.0, sqft_rate:float=0.0, valuation_pct:float=0.0, fee_formulas:List[str]=factory(list)
- `@dataclass TemporalMetadata`: effective_date:date, expiration_date:Optional[date]=None, ordinance_number:str="", is_active:bool=True, supersedes_section:Optional[str]=None
- `@dataclass FourDMunicipalCodeEntity`: code_id:str, jurisdiction:str, section_citation:str, raw_text:str, plain_english_summary:str, density:DensityMetrics, design:DesignConstraints, delay:DelayMetrics, dollars:DollarsMetrics, temporal:TemporalMetadata, spatial_zoning_districts:List[str]=factory(list)

### translator/core.py
`class MunicipalCodeTranslator`:
- Jargon map (>=20 entries): e.g. "hereinafter"-> "from now on", "pursuant to"->"under", "shall"->"must", "commence"->"start", "terminate"->"end", "utilize"->"use", "notwithstanding"->"despite", "aforementioned"->"mentioned earlier", "heretofore"->"until now", "thereof"->"of it", "whereas"->"given that", "in the event that"->"if", "prior to"->"before", "subsequent to"->"after", "remuneration"->"pay", "abatement"->"reduction", "encumbrance"->"burden/lien", "per annum"->"per year", "null and void"->"invalid", "egress"->"exit", "domicile"->"home".
- `__init__(self)` compiles regexes: `re_fees` = r'\$[\d,]+(?:\.\d{2})?'; `re_citation` per source; `re_purpose` per source.
- `translate(self, text: str, citation: str = "") -> MunicipalTranslationResult`: builds plain_english_summary by applying jargon replacements sentence-preservingly, extracts flat fees into FeeItem list, extracts purpose/intent block into stated_intent.

### analysis modules
- `RegulationRootCauseAnalyzer(municipal_jargon: Optional[dict] = None)`; `.analyze(full_text: str) -> List[str]`; default intent_keywords per source (public_safety, affordable_housing, environmental, + traffic, economic_development).
- `CitationGraph`; `.extract_references(text: str) -> List[RegulationReference]`; classify type by keyword (Act->federal/state, Section/Chapter/Ordinance->municipal, IBC/IRC/ADA/NFPA->industry_standard).
- `FeeExplorationEngine`; `.extract(text: str) -> List[FeeItem]` (flat + formulaic `$X per sq ft`, `X% of valuation`); `.calculate_total(fees: List[FeeItem], project_params: Dict[str, float]) -> float` supporting keys square_feet, valuation.
- `AuditEngine`; `.extract_metrics(text: str) -> List[AuditMetric]` (regex for "reduce X by N%", "increase ... by N", "no later than <date>"); `.auditability_score(metrics, text) -> float` (0-1: measurable targets, deadlines, reporting duty).
- `AdvancedAnalysisPipeline(translator)`; `.analyze(self, result: MunicipalTranslationResult, raw_text: str) -> MunicipalTranslationResult` — fills root_causes, interconnected_regulations, stated_intent (if empty), audit_metrics, auditability_score, and upgrades fees via FeeExplorationEngine.

### cli.py
`python -m fourd_municipal_engine.cli "text"` or `--file path`. Flags: `--genre {general,corporate_pr,legal_contract,technical_report,casual_social}`, `--deep-analysis`, `--json`, `--citation`. Default: run DynamicFourDLens + translator; print human-readable report. `--json` prints dataclasses.asdict of a result dict.

## Constraints
- Python 3.9+ stdlib ONLY (no external deps). pytest only for tests.
- All modules import via absolute package imports `from fourd_municipal_engine.models... import ...`.
- Tests must pass: `python -m pytest tests/ -q`.
