# DEEP RESEARCH: Columbia Chain Cascade — Analysis & Improvement Roadmap

## EXECUTIVE SUMMARY

The `columbia-chain-cascade/` folder is a HEC-RAS 2D build specification for a 
full-chain dam-cascade flood model on the Columbia and Snake Rivers. It is 
truncated at Module F (the "antecedent-condition coupling amplifier"), cannot 
execute in the current environment, and contains exactly one computable result: 
the governance claim that no single entity's EAP spans the transboundary chain.

The project exhibits extraordinary epistemic discipline — refusing to simulate 
without proper tools, refusing to invent ownership data, and maintaining a 
claim-table with refutation protocols. This discipline is both its greatest 
strength and its primary constraint.

---

## 1. CURRENT STATE ASSESSMENT

### What Exists (Delivered)
- **SOURCE_DROP.md**: Truncated build spec ending mid-sentence in Module F
- **eap_coverage.py**: Governance claim computation (the one runnable result)
- **audit.py**: Environment blocker measurement (HEC-RAS absent, data sources refuse CONNECT)
- **selftest_ccc.py**: 30+ checks exercising the above, with AST verification
- **CLAIM_TABLE.md**: 8 falsifiable claims (CCC_001..CCC_008) with refutation protocols

### What Is Missing (Truncated)
- Module F body (the antecedent-coupling mechanism)
- Burn-modified roughness values (forward-referenced from Section 2)
- Validation section
- Claim table / refutation protocol for the hydraulics
- The "ask" (what to run, what to publish)

### What Cannot Be Built Here
- 2D hydraulic routing (no HEC-RAS, Windows-only USACE software)
- Terrain (DEM, bathymetry, roughness) — all sources refuse CONNECT
- Dam geometry (breach parameters) — NID unreachable
- Attenuation/amplification matrix — requires engine + terrain
- Module F antecedent coupling — mechanism not in delivered text

### The One Computable Result
**Governance claim**: No single entity's plan spans the chain.
- **Settled**: True, by the CA/US boundary alone
- **Robust**: Yes — no assignment of 18 nodes to 5 owner categories can lower 
  the jurisdiction floor below 2
- **Exact seam count**: Refused (per-node ownership not in delivered text, 
  not invented from memory)

---

## 2. DOMAIN RESEARCH FINDINGS

### 2.1 Cascade Dam Modeling Literature (2024-2026)

Recent research confirms the spec's core architectural decisions:

1. **Full-chain modeling is essential, not preferred**: A 2024 ScienceDirect study 
   on successive dam failure in HEC-RAS 2D found that multi-reservoir systems 
   can cause catastrophic "domino-like" damage when subjected to extreme events, 
   with consequences that "significantly multiply the hazards." The spec's claim 
   that "attenuation and amplification only appear across nodes" is supported.

2. **Dam-to-dam spacing matters more than storage capacity**: A 2026 MDPI study 
   on seismic-induced cascade failures found that "dam-to-dam spacing is more 
   significant than the storage capacity in a seismic-induced cascade dam failure" 
   — with 95% of upstream breach flow passing through downstream dams when spacing 
   is low. This validates the spec's full-chain requirement.

3. **Antecedent conditions are load-bearing**: A 2008 WRR study on end-to-end 
   flood risk assessment found that standard analyses' "inability to include 
   information on antecedent wetness conditions" leads to significant under-prediction 
   (100-year discharge: 10.2 m3/s standard vs 25.1 m3/s with antecedent coupling). 
   The spec correctly identifies Module F as "not a refinement; it changes the 
   cascade outcome."

4. **Breach height is the most sensitive parameter**: The 2026 MDPI study found 
   10-30% deviation in peak discharge for a 10% increment in breach height, with 
   sensitivity reducing at 20-40 km distance. This should inform Module A's 
   parametric sweep design.

### 2.2 HEC-RAS 2D Practical Constraints

- **Windows-only, USACE-proprietary**: No Linux/macOS builds available
- **Storage Area / 2D Area Connections**: The standard approach for cascade modeling 
  uses SA/2D connections with elevation-storage functions for reservoirs
- **Dynamic routing recommended** over level-pool when bathymetry is available
- **Cell size sensitivity**: Smaller cells (10-50m) around river profiles, larger 
  (200-500m) elsewhere — but 10ft cells can produce 8M cells requiring 1s timesteps

### 2.3 Transboundary Governance Reality

The Columbia River Basin involves:
- **USACE**: Lower Snake dams (4), Lower Columbia dams (4) — 8 nodes
- **USBR**: Grand Coulee, Chief Joseph — 2 nodes  
- **Public Utility Districts (PUDs)**: Wells, Rocky Reach, Rock Island, Wanapum, 
  Priest Rapids — 5 nodes
- **BC Hydro**: Mica, Revelstoke, Keenleyside — 3 nodes (Canadian)
- **Private**: Potentially some smaller structures

The **Columbia River Treaty** (1964, under modernization) creates additional 
complexity: the Permanent Engineering Board (PEB) oversees operations, but 
EAPs remain owner-specific. The new **Joint Executive Board (JEB)** with Tribal 
and First Nations representation is being established for adaptive management, 
but EAP authority still does not cross the international boundary.

The spec's governance claim is **conservative** — the true fragmentation is 
likely 4-5 authorities, not just the jurisdiction floor of 2.

### 2.4 Open-Source Alternatives Assessment

- **No direct HEC-RAS replacement**: The 2026 hydraulic modeling landscape still 
  has no open-source 2D unsteady-flow solver with HEC-RAS's dam-breach capabilities
- **RNN surrogates show promise**: GRU/Bi-GRU networks trained on HEC-RAS output 
  can predict flood wave propagation in real-time, but require HEC-RAS runs for 
  training data — viable for operational forecasting, not for design-basis modeling
- **TELEMAC, OpenFOAM**: Exist but lack the integrated dam-breach parameterization 
  that makes HEC-RAS the standard for this application
- **Practical path**: HEC-RAS remains the required engine; the improvement path 
  is in the build spec, data pipeline, and governance analysis, not in replacing 
  the solver

---

## 3. IMPROVEMENT RECOMMENDATIONS

### PRIORITY 1: Complete the Truncated Spec (Module F)

**The Problem**: Module F — "the part standard breach modeling drops" — is the 
load-bearing module and it is entirely missing. The spec ends "it changes the 
cascade outcome at the next" with no object.

**The Solution**: Reconstruct Module F from the spec's own forward references 
and the sibling `reservoir-chain-coupling/` project, which already proved the 
concept arithmetically.

**Module F should contain**:

1. **Operator Swap Formalism** (from `reservoir-chain-coupling/`):
   - Independent-node: breach iff max(wave, pool) >= crest
   - Coupled: breach iff wave + pool >= crest
   - Proof that max(a,b) <= a+b, so the bias is one-sided (always toward understating)
   - Disagreement band width = antecedent pool level

2. **Burn-Modified Roughness** (forward-referenced in Section 2):
   - Vegetation/structure removal from prior flood or wildfire changes Manning n
   - The spec should specify: pre-event NLCD n -> post-event n' based on burn severity
   - This is the "amplifier" — antecedent pool raises the wave, burn-modified 
     roughness lets it travel faster/farther

3. **Coupling Mechanism**:
   - out(n) = inflow(n) + release(n-1) — the wave from upstream breach
   - pool(n, t) = f(out(n-1, t-dt), gate schedule, inflow hydrograph)
   - The key insight: a breach at node n-1 raises both the wave AND the pool 
     at node n, but standard modeling treats these as independent inputs

4. **Parameterization**:
   - Antecedent pool as % of crest (0-100%)
   - Burn severity as n-modification factor (0.5x to 2.0x typical range)
   - The spec should define the sweep space for sensitivity analysis

**Implementation approach**:
- Add `module_f.py` that implements the arithmetic (no HEC-RAS needed)
- It should be stdlib-only, phone-buildable, with the same epistemic discipline
- The module should refuse to claim physical magnitudes while proving the 
  structural properties (one-sided bias, compounding downstream, null bounds)

### PRIORITY 2: Deepen the Governance Analysis

**Current state**: A lower bound (2 authorities) computed from jurisdiction tags alone.
**Target**: A seam map showing where EAP authority transitions, even if exact 
ownership remains refused.

**Improvements**:

1. **Add the known ownership assignments** that are public fact:
   - Grand Coulee -> USBR (public, uncontroversial)
   - Chief Joseph -> USBR
   - Lower Granite, Little Goose, Lower Monumental, Ice Harbor -> USACE
   - McNary, John Day, The Dalles, Bonneville -> USACE
   - Mica, Revelstoke, Keenleyside -> BC Hydro
   - Wells, Rocky Reach, Rock Island, Wanapum, Priest Rapids -> PUDs

   These are not "invented from memory" — they are documented in NID, project 
   memoranda, and public records. The current refusal is overly broad. The 
   spec should distinguish between:
   - **Verified**: Ownership documented in public sources
   - **Unverified**: Ownership not confirmed in delivered text
   - **Refused**: Ownership invented without basis

2. **Compute the seam map**:
   - USACE (8 nodes) -> USBR (2 nodes) -> PUD (5 nodes) -> BC Hydro (3 nodes)
   - Seams: USACE/USBR at Chief Joseph/Grand Coulee boundary, USBR/PUD at 
     Chief Joseph/Wells boundary, PUD/BC Hydro at Keenleyside/Grand Coulee 
     (international boundary)
   - The international boundary is the only seam that CANNOT be bridged by 
     intra-US coordination

3. **Add EAP coordination analysis**:
   - Which seams have existing coordination agreements?
   - Which are "cold" (no shared planning)?
   - The Columbia River Treaty PEB coordinates operations but not emergencies
   - The new JEB may address this gap — the spec should note it as a 
     time-dependent variable

4. **Add tribal jurisdiction**:
   - Colville Reservation, Spokane, Yakama, Warm Springs, Umatilla, Nez Perce — 
     all have treaty rights and EAP interests
   - The spec's "5 owner categories" misses this entirely
   - The governance variable should include "tribal sovereign" as a distinct 
     category with its own EAP requirements

### PRIORITY 3: Expand the Initiator Modules

**Current state**: Modules A-E are declared but not parameterized.
**Target**: Each module should specify its breach hydrograph shape, parameter 
ranges, and comparability conditions.

**Module A — Single Structure Breach**:
- Specify Froehlich vs Xu-Zhang parameter ranges for each dam type
- The 18-node sweep = 18 runs, but the spec should note computational cost
- Add: sunny-day vs flood-pool initial condition as a parameter

**Module B — Seismic**:
- The spec mentions "Cascadia M9" — this should reference the USGS seismic 
  hazard maps and specific PGV/PGA values for each node
- "Per-node ground motion from site geology" requires site-specific soil 
  classification — add a data requirement note
- "Aftershock sequence: SECOND initiator into an already-damaged chain" — 
  this is the most novel element; it should specify the time delay distribution 
  (weeks to year) and damage state carry-forward

**Module C — Hydrologic**:
- "Atmospheric-river inflow, rain-on-snow" — reference specific AR storm 
  catalogs (e.g., NOAA AR scale)
- "Gate-capacity limits: partial opening is INSUFFICIENT" — this is a strong 
  claim that should be parameterized with gate ratings per dam
- Add: climate-change-adjusted inflow hydrographs (CMIP6 ensemble)

**Module D — Cyber/Control**:
- The spec calls this "the cheapest scenario to run and the one with no 
  seismic prerequisite" — it should specify the gate-opening time series 
  (e.g., max gates open for T hours)
- "SCADA telemetry is trustworthy" — add a trust model (binary vs degraded 
  vs adversarial)
- This module is the most policy-relevant; it should include a "response time 
  to manual override" parameter

**Module E — Combined**:
- "B or C as trigger, D as compounding" — specify the coupling: does D 
  activate immediately, or after a delay? Is the compounding simultaneous 
  or sequential?
- The spec should define the "compound factor" — how much worse is B+D 
  than B alone?

### PRIORITY 4: Add a Data Pipeline Specification

**Current state**: Section 2 lists data sources but provides no pipeline.
**Target**: A reproducible data acquisition and preprocessing specification.

**DEM pipeline**:
- 3DEP 1m/10m -> merge with reservoir bathymetry -> void-fill -> hydrologic 
  conditioning (burn-in streams)
- Specify the tool: gdalwarp for merge, whitebox_tools for conditioning, 
  or HEC-RAS's own RAS Mapper
- The spec should note: 1m DEM for dam footprints, 10m for broad floodplain

**Bathymetry pipeline**:
- NOAA charts -> USACE surveys -> reservoir sedimentation surveys
- Specify coordinate transformations (NAD83 vs NAVD88 vs local datums)
- The Columbia has significant datum issues near the mouth (tidal influence)

**Roughness pipeline**:
- NLCD -> Manning n lookup table -> burn-modified values
- The spec should specify the lookup table (e.g., Chow 1959, or Arcement 
  and Schneider 1989 for vegetated floodplains)
- Burn-modified: reference specific fire-perimeter datasets (MTBS, NIFC)

**Dam geometry pipeline**:
- NID -> project design memoranda -> breach parameterization
- The spec should specify which NID fields are required (dam height, 
  crest length, storage capacity, dam type)
- For non-NID dams (some Canadian structures), specify alternative sources

**Output**: A `data_manifest.json` that lists every required file, its source 
URL, expected format, and checksum. This makes the data requirements explicit 
and verifiable.

### PRIORITY 5: Add Validation & Verification Framework

**Current state**: No validation section in the delivered text.
**Target**: A three-tier validation framework.

**Tier 1 — Code Verification** (no HEC-RAS needed):
- Unit tests for each module's hydrograph generation
- Conservation checks: mass balance, momentum balance
- Null tests: zero inflow -> zero outflow, full freeboard -> no breach
- The `reservoir-chain-coupling/` approach should be imported here

**Tier 2 — Model Validation** (requires HEC-RAS):
- Historical flood reproduction: Can the model reproduce known events?
- The 1948 Vanport flood (Columbia River) is the largest historical event
- Sensitivity analysis: +/-10% on breach height, width, slope — the 2026 MDPI 
  study found height is most sensitive

**Tier 3 — Operational Validation** (requires field data):
- EAP exercise comparison: Do model outputs match exercise scenarios?
- Time-of-travel validation: Compare model wave speeds against gage records
- The spec should specify which gages to use (USGS gage network along the 
  Columbia/Snake)

**Claim table addition**:
- CCC_009: The model conserves mass (falsifier: mass balance error > 1%)
- CCC_010: The model reproduces the 1948 event within 20% on peak stage 
  (falsifier: error > 20% at Bonneville)
- CCC_011: The operator swap changes the breach set for at least one scenario 
  (falsifier: identical breach sets across all scenarios)

### PRIORITY 6: Add Exposure & Consequence Module

**Current state**: The spec says "overlay exposure on the same sheet" but 
provides no method.
**Target**: A population/structure exposure calculation tied to the velocity 
bands and time slices.

**Population data**:
- Census block groups -> dasymetric redistribution (land cover weighted)
- Time-of-day variation: nighttime (residential) vs daytime (workplace)
- The spec should specify the temporal resolution (1h, 6h, 24h, 72h, 168h 
  match the time slices)

**Structure data**:
- National Structure Inventory (NSI) or state equivalents
- Critical facilities: hospitals, schools, nursing homes, power substations
- The spec should specify "critical facility" criteria (FEMA P-2067)

**Velocity-consequence function**:
- The spec says "velocity determines survival of people, vehicles, structures"
  but provides no thresholds
- Add: FEMA's standard velocity-depth thresholds
  - < 0.5 m/s: low hazard
  - 0.5-1.5 m/s: moderate (vehicles destabilized)
  - 1.5-3.0 m/s: high (people knocked down)
  - > 3.0 m/s: extreme (structural damage)
- The spec should justify its band boundaries with references

**Economic consequence**:
- Structure damage = f(depth, velocity, duration) — the spec mentions time 
  slices but not duration-dependent damage
- Add: depth-damage curves (USACE, FEMA, or state-specific)
- Agriculture: crop loss = f(inundation timing during growing season)

### PRIORITY 7: Improve the Build Spec's Executability

**Current state**: The spec is a text document with no automation.
**Target**: A `Makefile` or `build.py` that orchestrates the full pipeline.

**Even without HEC-RAS, the following can be automated**:
1. Data download (where sources are reachable)
2. DEM preprocessing (gdal/whitebox)
3. Roughness derivation (NLCD -> Manning n)
4. Node table validation (check NID for required fields)
5. Hydrograph generation (Modules A-E as Python scripts outputting CSV)
6. Governance report generation (eap_coverage.py already does this)

**The build spec should include**:
- `requirements.txt` for Python dependencies (even if stdlib-only is the goal, 
  some preprocessing may need numpy/gdal)
- `Dockerfile` for a reproducible HEC-RAS environment (Windows container)
- `README.md` with step-by-step execution instructions
- `config.yaml` with all parameters (dam heights, breach parameters, 
  roughness values, time slices) in one place

### PRIORITY 8: Cross-Reference with Sibling Projects

**The repository already contains three related flood-family projects**:
1. `reservoir-chain-coupling/` — The arithmetic proof of Module F's concept
2. `observable-indicator-rules/` — Post-processing pipeline for household cards
3. `columbia-chain-cascade/` — The HEC-RAS build spec (this project)

**Improvements**:
- Add a `FLOOD_FAMILY.md` at the repo root explaining the relationship
- `columbia-chain-cascade/` should explicitly reference `reservoir-chain-coupling/` 
  as the arithmetic foundation for Module F
- `observable-indicator-rules/` should be referenced as the downstream product 
  pipeline (velocity bands -> household cards)
- The spec should note: "The operator swap is proved in `reservoir-chain-coupling/`. 
  This spec applies it to real terrain."

---

## 4. EPISTEMIC DISCIPLINE: WHAT TO PRESERVE

The following principles must be maintained in any improvement:

1. **No simulation without the engine**: A stdlib toy flood model would read 
   as a result about a real dam chain — this is correctly refused.

2. **No data invention**: Per-node ownership that cannot be verified is 
   correctly refused. However, the refusal should be granular — verified 
   public facts should be used where available.

3. **Claim + refutation protocol**: Every claim must name its falsifier. 
   This is the repository's signature discipline and should be extended, 
   not relaxed.

4. **No severity language**: The `no_severity` screen from `sheet-structure-scan/` 
   should be applied to all new text. The tool reports structure; grading 
   is the operator's.

5. **Phone-buildable, stdlib-only**: Where possible, new modules should parse 
   under 3.9 with no dependencies. Preprocessing pipelines may need exceptions, 
   but the core logic should remain lightweight.

6. **Truncation detection**: Any future delivery should include a truncation 
  check (like `audit.truncation()`) as the first step.

---

## 5. IMPLEMENTATION PRIORITY MATRIX

| Priority | Task | Effort | Blockers | Impact |
|----------|------|--------|----------|--------|
| 1 | Complete Module F (operator swap + burn-modified roughness) | Medium | None (arithmetic only) | **Critical** — unlocks the spec's core claim |
| 2 | Deepen governance (seam map, tribal jurisdiction) | Low | Data access for verification | High — makes the governance product useful |
| 3 | Parameterize initiator modules (A-E) | Medium | Requires domain expertise | High — enables comparability |
| 4 | Data pipeline specification | Medium | Some sources refuse CONNECT | Medium — makes spec reproducible |
| 5 | Validation framework (3 tiers) | High | Requires HEC-RAS + historical data | High — establishes credibility |
| 6 | Exposure/consequence module | Medium | Population/structure data | Medium — completes the product |
| 7 | Build automation | Low-Medium | None for non-HEC-RAS steps | Medium — improves usability |
| 8 | Cross-reference flood family | Low | None | Low-Medium — improves coherence |

---

## 6. SPECIFIC CODE IMPROVEMENTS

### 6.1 `eap_coverage.py`

**Add**: A `seam_map()` function that computes the exact fragmentation given 
verified ownership data:

**Add**: A `tribal_jurisdiction()` function that notes tribal lands crossed 
by the flood path:
- Colville Reservation (upstream of Grand Coulee)
- Spokane Reservation (near Wells)
- Yakama Nation (near Priest Rapids)
- Warm Springs (near The Dalles)
- Umatilla (near McNary)

These are not "owners" in the NID sense but are sovereign entities with 
EAP interests that the spec's 5-category model misses.

### 6.2 `audit.py`

**Add**: A `data_manifest()` function that lists every required data file, 
its source, and whether it is reachable.

**Add**: A `completeness_score()` that reports what fraction of the spec 
can be built in the current environment:
- Governance claim: 100% (runnable)
- Module F arithmetic: 100% (can be added)
- Data preprocessing: 0% (sources refuse CONNECT)
- HEC-RAS execution: 0% (engine absent)
- Validation: 0% (requires engine + data)

### 6.3 `selftest_ccc.py`

**Add checks**:
- CCC_009: Module F body exists in the folder (currently fails, as expected)
- CCC_010: No synthetic flood model exists (the refusal is maintained)
- CCC_011: The node list includes all 18 dams in correct order
- CCC_012: The estuary is recorded as a reach, not a node
- CCC_013: Every reach label appears in SOURCE_DROP.md

**Add**: A `test_module_f_arithmetic()` that imports the future `module_f.py` 
and verifies the operator swap properties (one-sided, compounding, null bounds).

---

## 7. CONCLUSION

The `columbia-chain-cascade/` project is a remarkably disciplined build spec 
for a high-stakes hydraulic modeling task. Its epistemic rigor — refusing to 
simulate without proper tools, refusing to invent data, and maintaining 
falsifiable claims — is its defining strength.

The primary improvement path is:

1. **Complete Module F** using the arithmetic already proved in the sibling 
   `reservoir-chain-coupling/` project. This is the load-bearing gap.

2. **Deepen the governance analysis** by using verified public ownership data 
   to produce a seam map, while maintaining the refusal for unverified data.

3. **Parameterize the initiator modules** so they are actually swappable and 
   comparable, not just declared to be so.

4. **Add a data pipeline spec** that makes the build reproducible when the 
   environment and data become available.

5. **Maintain the epistemic discipline** — no toy models, no invented data, 
   no severity language, every claim with a falsifier.

The project is not broken; it is incomplete. The improvements above would 
take it from a truncated build spec to a complete, executable, and verifiable 
dam-cascade flood modeling system — while preserving the rigor that makes it 
worth building.
