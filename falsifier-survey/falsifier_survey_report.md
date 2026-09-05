# FALSIFIER SURVEY — JinnZ2/Simulators

Run under the adjusted admissibility rule of ADDENDUM 01 (SCOPE-DIFFERENT
admissibility, and the taxonomy test). Date of run: 2026-09-05.
Scope: all 127 survey folders of the repository (docs/, notes/, legacy/,
tests/, tools/ excluded as meta-directories). One cell per distinct
falsifier; one explicit MISSING cell per folder stating no falsifier.

## Counts (report.py emission)

```
cells total                                        1765
  MEASURED (complete MEASURED_AS)                  1357
  SCOPE-DIFFERENT (complete SCOPE_TRANSFORM)          9
  UNKNOWN (fails its bar, reason stated)            374
  MISSING (folder states no falsifier)               25
SCOPE-DIFFERENT lacking a complete transform          0
  (separate line per addendum §3: no cell was admitted
   SCOPE-DIFFERENT on a prose scope note; all 9 carry
   reference + maps_to + breaks_at)
distinct falsifiers coded (non-MISSING cells)      1740
folders covered                                   127/127
validation gate                                   0 schema errors
```

## Method

1. **Extraction (scripted).** Three capture modes over every markdown file in
   every folder: pipe-table `falsifier` columns, explicit `Falsifier:` /
   `Falsifier —` prose blocks, and a paragraph-level fallback for other
   mentions. 1,625 raw mentions over 101 folders; 26 folders had no textual
   mention at all. The mention list over-captures by construction; distinct
   falsifiers were enumerated by the coders from the folder files themselves.
2. **Coding (8 parallel coders, adjusted rule only).** Each cell coded:
   - `MEASURED` requires MEASURED_AS: quantity + units + how obtained. Units
     need not be SI — a named count, a verdict label from a named function, a
     ratio, or a boolean from a named test all count, provided the unit is
     stated or unambiguous. No units → downgrade.
   - `SCOPE-DIFFERENT` requires SCOPE_TRANSFORM: reference / maps_to /
     breaks_at. A prose scope note without all three is not admissible →
     UNKNOWN with downgrade reason.
   - `MISSING` emitted explicitly, never silent.
   Per the addendum's constraint on the taxonomy test, coders were **not**
   shown the candidate kinds (K1/K2/K3); they wrote transforms only.
3. **Taxonomy sort (blind).** A separate agent sorted the nine completed
   transforms without any kind menu, then — only after delivering its sort —
   received the addendum's K1/K2/K3 and produced the correspondence mapping.

## Per-folder results

| folder | cells | MEASURED | SCOPE-DIFFERENT | UNKNOWN | MISSING |
|---|---|---|---|---|---|
| AMOC | 19 | 15 | 0 | 4 | 0 |
| adaptive-claim-loop | 17 | 17 | 0 | 0 | 0 |
| alignment-under-coupling | 7 | 7 | 0 | 0 | 0 |
| anchor-interval | 14 | 8 | 0 | 6 | 0 |
| antifungal-mechanism-sim | 12 | 6 | 0 | 6 | 0 |
| aperiodic-order-sim-stack | 21 | 19 | 0 | 2 | 0 |
| blame-attribution | 22 | 14 | 0 | 8 | 0 |
| bridge-impoundment | 26 | 22 | 0 | 4 | 0 |
| category-weld | 34 | 27 | 0 | 7 | 0 |
| ch4-four-box | 1 | 0 | 0 | 0 | 1 |
| claim-audits | 1 | 0 | 0 | 0 | 1 |
| claim-record | 30 | 19 | 0 | 11 | 0 |
| claim-refusal-gap | 1 | 0 | 0 | 0 | 1 |
| climate-modeling | 16 | 14 | 0 | 2 | 0 |
| closure-cost | 25 | 22 | 0 | 3 | 0 |
| clustering-axes | 10 | 8 | 0 | 2 | 0 |
| coinage-log | 1 | 0 | 0 | 0 | 1 |
| cold-weather-battery-guide | 1 | 0 | 0 | 0 | 1 |
| columbia-chain-cascade | 60 | 50 | 0 | 10 | 0 |
| condition-scoped-authority | 10 | 9 | 0 | 1 | 0 |
| consensus-anchor | 13 | 9 | 0 | 4 | 0 |
| constraint-assembly | 23 | 20 | 0 | 3 | 0 |
| continuity-audit | 2 | 2 | 0 | 0 | 0 |
| conversation-type | 12 | 9 | 0 | 3 | 0 |
| cooperative-substrate | 26 | 22 | 0 | 4 | 0 |
| corpus-input-gaps | 1 | 1 | 0 | 0 | 0 |
| criteria-drift | 19 | 11 | 0 | 8 | 0 |
| criterion-symmetry | 8 | 6 | 1 | 1 | 0 |
| crossdomain-eval | 1 | 0 | 0 | 0 | 1 |
| custody-verification-band | 9 | 4 | 0 | 5 | 0 |
| declared-frame | 9 | 6 | 0 | 3 | 0 |
| dependency-ledger | 11 | 5 | 0 | 6 | 0 |
| derivation-discarded | 12 | 11 | 0 | 1 | 0 |
| design-basis-ai | 56 | 53 | 0 | 3 | 0 |
| divergence-playground | 11 | 6 | 0 | 5 | 0 |
| domain-ledger | 15 | 13 | 0 | 2 | 0 |
| earth_economics | 11 | 10 | 0 | 1 | 0 |
| effective-redundancy-audit | 8 | 7 | 0 | 1 | 0 |
| emergence-stability-simulator | 32 | 22 | 0 | 10 | 0 |
| encoding-selection | 3 | 3 | 0 | 0 | 0 |
| energy | 11 | 11 | 0 | 0 | 0 |
| engine-boiler-guide | 1 | 0 | 0 | 0 | 1 |
| envelope-asymmetry | 10 | 6 | 0 | 4 | 0 |
| equivalence-field | 3 | 3 | 0 | 0 | 0 |
| evaluation-frame | 11 | 11 | 0 | 0 | 0 |
| experience-ledger | 9 | 5 | 0 | 4 | 0 |
| exploration-engine | 2 | 2 | 0 | 0 | 0 |
| exploration-playground | 1 | 1 | 0 | 0 | 0 |
| extraction-blindness-sim | 7 | 4 | 0 | 3 | 0 |
| field-fabrication-guide | 1 | 0 | 0 | 0 | 1 |
| fold-matrix | 42 | 35 | 0 | 7 | 0 |
| fourd-municipal-engine | 1 | 0 | 0 | 0 | 1 |
| fourd-municipal-engine-v2 | 1 | 0 | 0 | 0 | 1 |
| fragility-cascade | 157 | 150 | 1 | 6 | 0 |
| fuel-independence-guide | 1 | 0 | 0 | 0 | 1 |
| gap-markers | 16 | 13 | 0 | 3 | 0 |
| gdprf-framework | 1 | 0 | 0 | 0 | 1 |
| generation-capacity | 8 | 3 | 0 | 5 | 0 |
| grounding-layers | 76 | 57 | 1 | 18 | 0 |
| handoff-provenance | 1 | 1 | 0 | 0 | 0 |
| held-open-uncertainty | 6 | 6 | 0 | 0 | 0 |
| hf-incident-extract | 4 | 4 | 0 | 0 | 0 |
| household-scope-audit | 12 | 8 | 0 | 4 | 0 |
| incentive-blindspot-sim | 4 | 4 | 0 | 0 | 0 |
| instrument-bias-sims | 11 | 7 | 0 | 4 | 0 |
| instrument-epistemology | 2 | 2 | 0 | 0 | 0 |
| inverseminar | 1 | 0 | 0 | 0 | 1 |
| investigation-sim | 16 | 16 | 0 | 0 | 0 |
| label-position-test | 11 | 9 | 0 | 2 | 0 |
| measurement-fork | 25 | 18 | 0 | 7 | 0 |
| membership-probe | 6 | 6 | 0 | 0 | 0 |
| mining-increment | 16 | 13 | 0 | 3 | 0 |
| model-ecology | 10 | 10 | 0 | 0 | 0 |
| model-provenance | 9 | 8 | 0 | 1 | 0 |
| moral-decomposer | 10 | 9 | 0 | 1 | 0 |
| move-set | 13 | 11 | 0 | 2 | 0 |
| move-set-derivation | 15 | 15 | 0 | 0 | 0 |
| msiaf-framework | 1 | 0 | 0 | 0 | 1 |
| msiaf-gdprf-bridge | 1 | 0 | 0 | 0 | 1 |
| neural-augmentation-audit | 1 | 0 | 0 | 0 | 1 |
| nonidentity-census | 7 | 6 | 0 | 1 | 0 |
| null-harness | 1 | 0 | 0 | 0 | 1 |
| observable-indicator-rules | 9 | 9 | 0 | 0 | 0 |
| observer-exclusion | 18 | 14 | 0 | 4 | 0 |
| open-instrumentation-project | 5 | 3 | 0 | 2 | 0 |
| operator-structure-echo | 1 | 0 | 0 | 0 | 1 |
| photoperiod-claim-harness | 8 | 7 | 0 | 1 | 0 |
| play-sims | 1 | 0 | 0 | 0 | 1 |
| predicate-difference | 1 | 0 | 0 | 0 | 1 |
| presented-binary | 25 | 21 | 0 | 4 | 0 |
| proxy-investigation-lab | 2 | 2 | 0 | 0 | 0 |
| qrng-pair-search | 9 | 6 | 0 | 3 | 0 |
| question-availability | 5 | 4 | 0 | 1 | 0 |
| railcar-containment | 18 | 14 | 0 | 4 | 0 |
| readout-count | 6 | 6 | 0 | 0 | 0 |
| reasoning-dial | 15 | 15 | 0 | 0 | 0 |
| reasoning-gate | 2 | 2 | 0 | 0 | 0 |
| relational | 1 | 0 | 0 | 0 | 1 |
| removal-closure | 3 | 3 | 0 | 0 | 0 |
| report-typing | 16 | 15 | 0 | 1 | 0 |
| research-stability-audit | 8 | 7 | 1 | 0 | 0 |
| reservoir-chain-coupling | 9 | 8 | 0 | 1 | 0 |
| residual-direction | 10 | 5 | 0 | 5 | 0 |
| revision-mechanism | 11 | 5 | 0 | 6 | 0 |
| rigidification-sensor | 3 | 0 | 3 | 0 | 0 |
| scope-bound-shapes | 2 | 2 | 0 | 0 | 0 |
| seam-gaps | 6 | 6 | 0 | 0 | 0 |
| search-substitution | 8 | 5 | 0 | 3 | 0 |
| self-scan | 30 | 28 | 0 | 2 | 0 |
| shape-spec-audit | 17 | 9 | 0 | 8 | 0 |
| sheet-structure-scan | 64 | 46 | 0 | 18 | 0 |
| sim-span | 7 | 6 | 0 | 1 | 0 |
| simulation-hypothesis-budget | 40 | 21 | 0 | 19 | 0 |
| stop-authority | 1 | 0 | 0 | 1 | 0 |
| substrate-emergence | 1 | 0 | 0 | 0 | 1 |
| supplement-placement | 1 | 0 | 0 | 0 | 1 |
| sustained-activation-gate | 6 | 5 | 1 | 0 | 0 |
| term-drift-citation | 1 | 1 | 0 | 0 | 0 |
| thermal-coupling | 2 | 0 | 0 | 2 | 0 |
| thermal-sensor-degradation-audit | 6 | 6 | 0 | 0 | 0 |
| token-minimizer | 1 | 0 | 0 | 0 | 1 |
| transmission-decay | 12 | 8 | 0 | 4 | 0 |
| triad-playground | 11 | 11 | 0 | 0 | 0 |
| uninstrumented | 206 | 124 | 1 | 81 | 0 |
| vector-field-explorer | 1 | 1 | 0 | 0 | 0 |
| voice-attractor-probe | 1 | 0 | 0 | 0 | 1 |
| zero-sum-curriculum-null | 3 | 1 | 0 | 2 | 0 |

## The taxonomy test — result

Input: the 9 SCOPE-DIFFERENT cells' transforms. Small N expected; this is a
candidate taxonomy with its N stated, not a settled one.

### Blind sort (derived before any menu was shown)

The discriminating question: *where does the mismatch live?*

- **Derived Kind A — domain-boundary mismatch** (same quantity, wrong
  population / unit / extent), N=3: `uninstrumented/UNI_055`
  (species-specific vs category-general threshold),
  `research-stability-audit/AI_DEGRAD_001` (30-day window vs 1-year horizon),
  `criterion-symmetry/RESULTS_F1` (soft member; within-body agreement rate vs
  cross-body adoption fraction).
- **Derived Kind B — model↔substrate calibration gap** (synthetic /
  dimensionless vs physical; no mapping supplied), N=4:
  `rigidification-sensor/claim_001, claim_002, claim_003`,
  `sustained-activation-gate/SG_007 (wet-lab)`.
- **Derived Kind C — frame-of-expression mismatch** (same fact,
  representation/convention/instrument artifact; a conversion exists in
  principle), N=2: `fragility-cascade/FC-1` (reduced-phi4 convention),
  `grounding-layers/GL_L0_004` (external finite-difference vs internal
  inspector value).

Blind verdict: SEVERAL, not one — the breaks have different remedies
(re-scope the domain / supply an absent calibration / convert the
representation).

### Correspondence to the addendum's K1/K2/K3 (mapping done after reveal)

- **K1 frame difference — N=2 clean:** FC-1, GL_L0_004 (derived Kind C).
- **K2 boundary difference — N=1 clean:** AI_DEGRAD_001.
- **K1/K2 straddle — N=1:** UNI_055 (reference population reads as frame or
  boundary; securely in the K1/K2 family, not K3).
- **K3 homonym — N=1:** RESULTS_F1 — the only homonym in the set. Within-body
  agreement rate and cross-body adoption fraction are "properties of
  different objects"; no conversion exists even in principle. The K-menu
  resolves the blind sort's soft-member discomfort: RESULTS_F1 belongs to K3.
- **Outside the menu — N=4:** derived Kind B. K1 and K2 both presuppose that
  quantity identity is established and then re-framed or re-bounded; Kind B
  breaks one step earlier — no mapping establishes quantity identity between
  the synthetic readings and any physical substrate. The menu needs a fourth
  kind: **K4 — model–substrate calibration gap (quantity identity not
  established)**.

### Verdict on the open question

**SCOPE-DIFFERENT is SEVERAL things, not one — and the K1–K3 menu
under-covers the data.** The menu covers 5 of 9 cells; the largest group in
the data (Kind B, 4 of 9) is entirely absent from it. Four distinct failure
modes with four distinct remedies: re-scope (K1/K2), convert (K1 subset),
calibrate (K4), disambiguate (K3, no lesser remedy).

Caveats: (1) N=9; no kind has more than 4 members. (2) Kind B is
single-folder concentrated (3 of 4 from rigidification-sensor), so it may
partly reflect one project's idiom of shipping synthetic demos against OPEN
falsifier values. (3) RESULTS_F1's promotion to K3 is the least anchored
placement. (4) The adjusted rule is **not** shown sufficient as written —
the transforms sorted, so the third status is not a single thing.

## Anatomy of UNKNOWN (374 cells)

Recurring failure shapes reported independently by coders:

- **"A reading under which…" / "an argument that…"** — interpretive
  counterexample shapes naming no quantity (the single largest class;
  concentrated in columbia-chain-cascade, move-set, dependency-ledger,
  residual-direction, divergence-playground, design-basis-ai, fold-matrix).
- **Bare dash / "none" / "none needed" in the falsifier field** — the field
  exists and is empty by declaration (railcar-containment RCT_001/006/007/008,
  envelope-asymmetry ENV_004/005/008/009, transmission-decay TD_001/TD_006,
  revision-mechanism RM_007, qrng Q6, label-position-test LPT_006).
- **Judgment falsifiers with no statistic** — "a reader finds…",
  reader-comprehension tests with no threshold; includes the boilerplate
  user-guide falsifier ("Non-specialists find the guide unhelpful or
  incomprehensible") appearing verbatim in four folders.
- **Existence-of-event falsifiers with no specified check** — "a case
  where…", "a corpus where…", "the engine/data/archive arrives" without a
  named artifact or corpus.
- **Scope-note-only** — zero cells: every SCOPE-DIFFERENT candidate carried a
  complete transform. The addendum's adjusted bar did not have to fire.

## MISSING folders (25)

ch4-four-box, claim-audits, claim-refusal-gap, coinage-log, cold-weather-battery-guide, crossdomain-eval, engine-boiler-guide, field-fabrication-guide, fourd-municipal-engine, fourd-municipal-engine-v2, fuel-independence-guide, gdprf-framework, inverseminar, msiaf-framework, msiaf-gdprf-bridge, neural-augmentation-audit, null-harness, operator-structure-echo, play-sims, predicate-difference, relational, substrate-emergence, supplement-placement, token-minimizer, voice-attractor-probe.

Four declare the absence explicitly in their READMEs (crossdomain-eval,
fourd-municipal-engine, fourd-municipal-engine-v2, play-sims). Two carry a
REFUTATION_PROTOCOL but state no per-claim falsifier (ch4-four-box,
claim-refusal-gap) — the seed-cell analogue of the addendum's forcing case:
the instrument's own rule catches the work-order-shaped folders. Two more
self-describe as not carrying claim tables (gdprf-framework, msiaf-framework).

## Deviations and limitations

- Coding is from reading, not execution: no selftests were run; "how
  obtained" is taken from the text's named instrument.
- Existence-of-named-artifact falsifiers ("the delivered file runs end to
  end") were coded MEASURED with units=boolean by convention, flagged
  per-cell where shallow.
- fragility-cascade's 137 "Refuted if" rows were coded with per-family
  measured_as templates (module, units, pinned sample) rather than
  hand-written per row.
- Coders worked against a fresh clone of HEAD (2026-09-05); the extraction
  mention-list and the coding reads are the same tree.
- Cross-folder duplicate falsifiers (e.g. reasoning-gate RG_F2 =
  aperiodic-order-sim-stack lattice control) were kept as per-folder cells
  with notes — the survey unit is the folder's falsifier, not the claim
  family.

## Files

- `cell_records.jsonl` — one JSON object per cell (full schema incl.
  measured_as / scope_transform sub-objects).
- `cell_records.csv` — flattened table (quantity/units/how_obtained,
  reference/maps_to/breaks_at as columns).
- `survey/raw_hits.jsonl` — the extraction mention list (over-capture
  included, for audit).
- `survey/scope_different_cells.json` — the nine transforms the taxonomy
  test sorted.
- `survey/batches/batch_0..7.jsonl` — per-coder output, pre-merge.
