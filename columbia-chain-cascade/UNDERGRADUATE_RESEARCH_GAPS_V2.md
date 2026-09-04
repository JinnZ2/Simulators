# UNDERGRADUATE RESEARCH GAPS

## Open questions in the Columbia Chain Cascade spec, organized by discipline

Every gap in this spec is a research question with:
- A **knowledge state** (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A **falsifier** (what would settle it)
- A **data source** (where to look)
- A **method** (how to answer it)
- An **expected deliverable** (what the undergraduate produces)

These are not vague "future work" paragraphs. Each gap is precisely
bounded, checkable, and scoped to a semester or summer of work.

---

## 1. URBAN HYDROLOGY — Contributing Inflow Calibration

**Gap:** The urban runoff increment is parameterized as a dimensionless
fraction (0.0–0.30) but not calibrated for any tributary city.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What is the urban runoff contribution to
antecedent pool levels at Grand Coulee, McNary, and Bonneville from
Spokane, Tri-Cities, and Portland metro respectively?

**Disciplines:** Hydrology, urban planning, remote sensing

**Data sources:**
- NLCD impervious surface raster (USGS)
- USGS gage records for Spokane River, Yakima River, Willamette River
- Naturalized flow estimates from USACE reservoir operations
- Reservoir operating records (pool levels during storm events vs. baseflow)

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- NLCD impervious surface raster (USGS) — **OPEN**; route: mrlc.gov download
- USGS gage records for Spokane River, Yakima River, Willamette River — **OPEN**; route: USGS NWIS
- Naturalized flow estimates from USACE reservoir operations — **OPEN**; route: BPA / USACE modified-flows datasets, published
- Reservoir operating records (pool levels during storm events vs. baseflow) — **OPEN**; route: USACE NWD DataQuery; PUD hydro pages; if a pool series is withheld, records request to the district
<!-- /ADDENDUM -->

**Method:**
1. Extract impervious surface area per tributary watershed from NLCD
2. Compare gage-recorded inflow vs. naturalized flow estimates
3. Compute the urban increment as (gage - naturalized) / naturalized
4. Propagate to reservoir pool level using a simple water balance
5. Validate against known storm events

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** present in the entry (validate against known storm events)
<!-- /ADDENDUM -->

**Expected deliverable:** A calibrated `urban_increment_fraction` for
each tributary city, with uncertainty bounds, added to
`contributing_inflow.py` as a data-driven parameter rather than a
synthetic one.

**Falsifier:** The urban increment is < 1% for all cities (then it is
not load-bearing and can be dropped from the spec).

---

## 2. WILDFIRE HYDROLOGY — Burn-Modified Roughness Calibration

**Gap:** Burn-modified roughness is parameterized as an attenuation
reduction (0.0–0.50) but not calibrated for any fire event in the
Columbia basin.

**Knowledge state:** UNKNOWN_ATM

**Research question:** How does post-wildfire vegetation removal change
Manning n and wave celerity in the Columbia/Snake floodplain?

**Disciplines:** Geomorphology, fire ecology, hydraulic engineering

**Data sources:**
- MTBS (Monitoring Trends in Burn Severity) fire perimeter database
- NIFC (National Interagency Fire Center) incident records
- NLCD land cover pre- and post-fire
- HEC-RAS 2D model runs (or published post-fire hydraulic studies)
- Field Manning n measurements (if available from USACE or state agencies)

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- MTBS (Monitoring Trends in Burn Severity) fire perimeter database — **OPEN**; route: mtbs.gov
- NIFC (National Interagency Fire Center) incident records — **OPEN**; route: NIFC open data
- NLCD land cover pre- and post-fire — **OPEN**; route: mrlc.gov
- HEC-RAS 2D model runs (or published post-fire hydraulic studies) — **GATED**; route: the engine is a free Windows download; the RUNS need terrain and geometry -- route: published post-fire hydraulic studies via a library, USGS OFR series
- Field Manning n measurements (if available from USACE or state agencies) — **UNKNOWN**; route: not established who holds field n for these reaches; ask the state DOT hydraulics section and the USACE district; a documented 'none' is a finding
<!-- /ADDENDUM -->

**Method:**
1. Identify fire events in the Columbia basin since 2000
2. Extract pre- and post-fire NLCD land cover for burned reaches
3. Use standard Manning n lookup tables (Chow 1959, Arcement & Schneider 1989)
4. Compute n_pre and n_post for each burned reach
5. Convert to attenuation reduction factor using a simple routing model
6. Validate against any available post-flood gage records

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** present in the entry (post-flood gage records)
<!-- /ADDENDUM -->

**Expected deliverable:** A burn-severity-to-attenuation-reduction lookup
table, with the `BURN_SEVERITY_MAX` and `ATTENUATION_REDUCTION_MAX`
parameters replaced by calibrated values from real events.

**Falsifier:** Post-fire n change is < 5% (then the amplifier is not
load-bearing).

---

## 3. TRIBAL GOVERNANCE — EAP Coordination Mapping

**Gap:** Tribal sovereign nations are identified as physically relevant
but their EAP coordination with dam owners is NOT_STUDIED.

**Knowledge state:** NOT_STUDIED

**Research question:** What EAP coordination agreements exist between
tribal nations and dam owners in the Columbia basin? What gaps remain?

**Disciplines:** Indigenous studies, public policy, emergency management

**Data sources:**
- Tribal government records (public, via tribal websites or FOIA)
- USACE Emergency Action Plans (public, via USACE districts)
- PUD emergency coordination documents
- Columbia River Treaty Permanent Engineering Board records
- Federal Register notices for EAP updates

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- Tribal government records (public, via tribal websites or FOIA) — **REQUESTABLE**; route: direct request to each nation's emergency-management office AFTER the consultation step; federal FOIA does not reach tribal governments
- USACE Emergency Action Plans (public, via USACE districts) — **GATED**; route: EAPs are commonly withheld as security-sensitive; FOIA to the district, expect redaction; document a refusal (it is a Gap 3 finding)
- PUD emergency coordination documents — **REQUESTABLE**; route: state public-records request (WA PRA) to each PUD
- Columbia River Treaty Permanent Engineering Board records — **OPEN**; route: PEB annual reports, published
- Federal Register notices for EAP updates — **OPEN**; route: federalregister.gov
<!-- /ADDENDUM -->

**Method:**
<!-- ADDENDUM consent -->
0. Before any records request: initiate consultation with each nation's emergency-management or natural-resources office; obtain consent for the study and for publication of its findings; record the terms. Federal FOIA does not reach tribal governments -- requests are direct and voluntary, and a refusal is recorded, never worked around. The Columbia River Treaty's Joint Executive Board (tribal and First Nations representation) is a named route. See the ethics sections of revision-mechanism/ and transmission-decay/.
<!-- /ADDENDUM -->

1. Identify the 6 tribal nations in the flood path (already in the spec)
2. Request or locate EAP coordination agreements for each
3. Map which dams have tribal consultation, which do not
4. Identify "cold seams" — boundaries with no shared planning
5. Compare against the international boundary (the unbridgeable seam)

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** a published dam-tribe MOU the matrix method must classify as coordinated, and a dam with no published agreement it must classify as absent-or-unknown -- both directions
<!-- /ADDENDUM -->

**Expected deliverable:** A tribal-EAP-coordination matrix (dam × tribe,
with status: coordinated, partial, absent, unknown), added to
eap_coverage.py as a governance layer.

**Falsifier:** All 6 tribes have full EAP coordination with all
relevant dam owners (then tribal jurisdiction is not a governance gap).

---

## 4. DAM OWNERSHIP — Seam Map Construction

**Gap:** The exact per-node ownership and seam count is UNKNOWN_ATM.

**Knowledge state:** UNKNOWN_ATM

**Research question:** Who owns each of the 18 dams, and where do EAP
authority transitions occur?

**Disciplines:** Civil engineering, public administration, GIS

**Data sources:**
- National Inventory of Dams (NID) — nid.sec.usace.army.mil
- USACE project design memoranda
- PUD annual reports and regulatory filings
- BC Hydro dam safety reports
- State dam safety office records (WA, OR, ID)

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- National Inventory of Dams (NID) — nid.sec.usace.army.mil — **OPEN**; route: nid.sec.usace.army.mil public download
- USACE project design memoranda — **GATED**; route: FOIA to the district; university depository libraries hold many USACE technical reports
- PUD annual reports and regulatory filings — **OPEN**; route: published by each PUD; FERC eLibrary for license filings
- BC Hydro dam safety reports — **GATED**; route: BC FOI request; BC Hydro water-use-planning documents, some public
- State dam safety office records (WA, OR, ID) — **REQUESTABLE**; route: public-records request: WA Ecology, OR OWRD, ID IDWR
<!-- /ADDENDUM -->

**Method:**
1. Query NID for each dam's owner, operator, and regulatory authority
2. Cross-reference with project design memoranda for verification
3. Handle edge cases (joint ownership, leased facilities, treaty obligations)
4. Construct the seam map: USACE → USBR → PUD → BC Hydro
5. Identify international seams (CA/US) vs. domestic seams

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** one node whose owner the FERC licensing record states openly; the seam map must place it
<!-- /ADDENDUM -->

**Expected deliverable:** A completed node table with per-node owner
assignments, replacing UNKNOWN_ATM with verified values, and a seam map
showing exactly where EAP authority transitions.

**Falsifier:** The ownership is already public and well-documented —
then the gap is closed by data access, not by research.

---

## 5. BREACH HYDROLOGY — Module A Parameterization

**Gap:** Module A (single structure breach) is declared but not
parameterized with Froehlich vs. Xu-Zhang ranges per dam type.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the appropriate breach parameter ranges
(height, width, slope, time to failure) for each of the 18 dams?

**Disciplines:** Dam safety engineering, geotechnical engineering

**Data sources:**
- NID dam type and geometry
- Froehlich (2008) and Xu & Zhang (2009) empirical breach equations
- USACE dam safety inspection reports
- State dam safety office breach analyses
- Published case studies of similar dam types

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- NID dam type and geometry — **OPEN**; route: nid.sec.usace.army.mil
- Froehlich (2008) and Xu & Zhang (2009) empirical breach equations — **GATED**; route: journal paywall; university library, interlibrary loan, author preprints
- USACE dam safety inspection reports — **GATED**; route: FOIA to the district; commonly withheld -- document the refusal
- State dam safety office breach analyses — **REQUESTABLE**; route: public-records request to the state office
- Published case studies of similar dam types — **GATED**; route: library; open-access where available
<!-- /ADDENDUM -->

**Method:**
1. Classify each dam by type (earthfill, concrete gravity, arch, etc.)
2. Apply Froehlich and Xu-Zhang equations with NID geometry
3. Compute parameter ranges (±10% on height, the most sensitive per 2026
   literature)
4. Document sunny-day vs. flood-pool initial conditions
5. Produce a breach parameter table for all 18 nodes

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** a documented historical breach with published Froehlich inputs (the equation paper's own worked case); the table must reproduce it within the equation's stated scatter
<!-- /ADDENDUM -->

**Expected deliverable:** A `breach_params.csv` with per-dam Froehlich
and Xu-Zhang parameters, initial condition variants, and sensitivity
notes, referenced by Module A.

<!-- ADDENDUM schema -->
**Deliverable schema (addendum):** initiator_schemas.py: breach_params.csv, 15 columns
<!-- /ADDENDUM -->

**Falsifier:** All 18 dams have identical breach parameters (then the
18-node sweep collapses to one run).

---

## 6. SEISMIC HAZARD — Module B Ground Motion

**Gap:** Module B mentions "Cascadia M9" but provides no per-node PGA
or PGV values.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the per-node ground motion parameters
for a Cascadia subduction zone M9 event?

**Disciplines:** Seismology, geotechnical engineering, structural engineering

**Data sources:**
- USGS National Seismic Hazard Maps
- PSHA (Probabilistic Seismic Hazard Analysis) for the Pacific Northwest
- Site-specific soil classification (USGS VS30 maps)
- Dam-specific seismic vulnerability assessments (if published)

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- USGS National Seismic Hazard Maps — **OPEN**; route: usgs.gov hazard maps and tools
- PSHA (Probabilistic Seismic Hazard Analysis) for the Pacific Northwest — **OPEN**; route: USGS PSHA products for the Pacific Northwest
- Site-specific soil classification (USGS VS30 maps) — **OPEN**; route: USGS VS30 map service
- Dam-specific seismic vulnerability assessments (if published) — **GATED**; route: FOIA to the district office holding the project file; the dam safety program manager; FERC eLibrary for FERC-licensed PUD dams (open); if refused, document it
<!-- /ADDENDUM -->

**Method:**
1. Extract PGA and PGV for each dam location from USGS hazard maps
2. Adjust for site soil conditions using VS30
3. Compute spectral acceleration at dam-natural-period
4. Define aftershock sequence parameters (delay distribution, damage
   state carry-forward)
5. Produce per-node ground motion time histories or response spectra

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** a USGS NSHM published PGA at a benchmark site; the extraction must return it
<!-- /ADDENDUM -->

**Expected deliverable:** A `seismic_params.csv` with per-dam PGA, PGV,
SA, and aftershock parameters, referenced by Module B.

<!-- ADDENDUM schema -->
**Deliverable schema (addendum):** initiator_schemas.py: seismic_params.csv, 12 columns
<!-- /ADDENDUM -->

**Falsifier:** All nodes experience identical ground motion (then the
"per-node" aspect of Module B is moot).

---

## 7. ATMOSPHERIC RIVER HYDROLOGY — Module C Inflow

**Gap:** Module C mentions "atmospheric-river inflow" but provides no
storm catalog or gate capacity limits.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the design-basis atmospheric river
events for the Columbia basin, and do gate capacity limits make partial
opening insufficient?

**Disciplines:** Meteorology, hydrology, dam operations

**Data sources:**
- NOAA AR (Atmospheric River) scale catalog
- CMIP6 climate model ensemble projections
- USACE reservoir rule curves and gate ratings
- Historical flood records (1948 Vanport, 1964 Christmas flood, etc.)
- SNOTEL snowpack data for rain-on-snow events

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- NOAA AR (Atmospheric River) scale catalog — **OPEN**; route: CW3E / Scripps AR catalog; NOAA PSL
- CMIP6 climate model ensemble projections — **OPEN**; route: ESGF nodes
- USACE reservoir rule curves and gate ratings — **GATED**; route: water control manuals via FOIA to the district; some are published
- Historical flood records (1948 Vanport, 1964 Christmas flood, etc.) — **OPEN**; route: USGS and USACE published reports; NWIS
- SNOTEL snowpack data for rain-on-snow events — **OPEN**; route: NRCS SNOTEL
<!-- /ADDENDUM -->

**Method:**
1. Identify AR4+ events in the Columbia basin historical record
2. Extract inflow hydrographs for each event
3. Compare against gate capacity ratings for each dam
4. Model partial opening scenarios vs. full opening
5. Project climate-change-adjusted hydrographs (CMIP6 ensemble)

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** a documented historical inflow peak (a published USACE flood report) reproduced from the AR catalog plus gage record
<!-- /ADDENDUM -->

**Expected deliverable:** A `hydro_params.csv` with design-basis AR
events, gate capacity analysis, and climate-adjusted variants,
referenced by Module C.

<!-- ADDENDUM schema -->
**Deliverable schema (addendum):** initiator_schemas.py: hydro_params.csv, 12 columns
<!-- /ADDENDUM -->

**Falsifier:** Gate capacity exceeds the largest historical inflow for
all dams (then partial opening is sufficient and the claim is false).

---

## 8. CYBER/CONTROL — Module D Trust Model

**Gap:** Module D is called "the cheapest scenario to run" but provides
no gate-opening time series or SCADA trust model.

**Knowledge state:** UNDEFINED

**Research question:** What is the "operational trust" in SCADA
telemetry during a cyber event, and how fast can manual override respond?

**Disciplines:** Cybersecurity, control systems, human factors

**Data sources:**
- NERC CIP (Critical Infrastructure Protection) standards
- Dam owner SCADA documentation (if publicly available)
- USACE cyber vulnerability assessments
- Human factors research on operator response time
- Published cyber-physical attack case studies

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- NERC CIP (Critical Infrastructure Protection) standards — **OPEN**; route: nerc.com standards
- Dam owner SCADA documentation (if publicly available) — **GATED**; route: not public by design; CEII request through FERC for licensed dams; a refusal is the expected and documentable outcome
- USACE cyber vulnerability assessments — **GATED**; route: FOIA; expect refusal -- document it
- Human factors research on operator response time — **GATED**; route: journal literature; library, ILL
- Published cyber-physical attack case studies — **OPEN**; route: open-access case studies and CISA advisories
<!-- /ADDENDUM -->

**Method:**
1. Define a SCADA trust model (binary/degraded/adversarial)
2. Define gate-opening time series for each scenario (max gates open
   for T hours)
3. Model manual override response time distribution
4. Compute the "compound factor" — how much worse is a cyber event
   during a flood vs. during normal operations?
5. Produce scenario definitions for Module D

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** a documented incident with a published override timeline; the trust model must reproduce its response time
<!-- /ADDENDUM -->

**Expected deliverable:** A `cyber_params.yaml` with trust model states,
gate-opening scenarios, response time distributions, and compound
factors, referenced by Module D.

<!-- ADDENDUM schema -->
**Deliverable schema (addendum):** initiator_schemas.py: cyber_params.yaml, 10 columns
<!-- /ADDENDUM -->

**Falsifier:** Manual override is instantaneous and always successful
(then cyber is not a load-bearing initiator).

---

## 9. COMPOUND EVENTS — Module E Interaction Factor

**Gap:** Module E mentions "B or C as trigger, D as compounding" but
defines no interaction factor.

**Knowledge state:** UNDEFINED

**Research question:** How much worse is a compound event (e.g., seismic
+ cyber) than the sum of its parts?

**Disciplines:** Risk analysis, systems engineering, emergency management

**Data sources:**
- Historical compound events (if any exist for dam cascades)
- Expert elicitation from dam safety engineers
- Published compound risk frameworks (e.g., IPCC AR6)
- Insurance industry compound event models

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- Historical compound events (if any exist for dam cascades) — **UNKNOWN**; route: not established that any documented dam-cascade compound event exists; a search with a stated corpus is the first step
- Expert elicitation from dam safety engineers — **REQUESTABLE**; route: structured elicitation with dam-safety engineers; needs IRB and consent
- Published compound risk frameworks (e.g., IPCC AR6) — **OPEN**; route: IPCC AR6, open
- Insurance industry compound event models — **GATED**; route: commercial; route: published white papers, academic partnerships
<!-- /ADDENDUM -->

**Method:**
1. Define the compound event space (B+D, C+D, B+C+D)
2. Define interaction types (simultaneous, sequential, delayed)
3. Compute or elicit interaction factors for each combination
4. Produce a compound event matrix

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** two independent synthetic events; the interaction factor must return 1.0 within the stated tolerance
<!-- /ADDENDUM -->

**Expected deliverable:** A `compound_matrix.csv` with interaction
factors for all compound event combinations, referenced by Module E.

<!-- ADDENDUM schema -->
**Deliverable schema (addendum):** initiator_schemas.py: compound_matrix.csv, 10 columns
<!-- /ADDENDUM -->

**Falsifier:** All interaction factors = 1.0 (then compound events are
no worse than the sum of parts, and Module E is redundant).

---

## 10. MODEL VALIDATION — 1948 Vanport Flood Reproduction

**Gap:** No validation section exists in the spec.

**Knowledge state:** NOT_STUDIED

**Research question:** Can the model reproduce the 1948 Vanport flood,
the largest historical event on the Columbia River?

**Disciplines:** Hydrology, hydraulic engineering, historical research

**Data sources:**
- USGS gage records from 1948 (Bonneville, The Dalles, etc.)
- Historical newspaper accounts and photographs
- USACE after-action reports
- Dam operating records from 1948
- DEM of 1948 channel conditions (if available)

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- USGS gage records from 1948 (Bonneville, The Dalles, etc.) — **OPEN**; route: NWIS historical daily values
- Historical newspaper accounts and photographs — **OPEN**; route: library newspaper archives; Oregon Historical Society
- USACE after-action reports — **REQUESTABLE**; route: NARA RG 77; district library
- Dam operating records from 1948 — **REQUESTABLE**; route: NARA RG 77; the operating agencies' archives
- DEM of 1948 channel conditions (if available) — **UNKNOWN**; route: not established that a 1948-condition surface exists; USGS historical topographic maps (open) and USACE historical hydrographic surveys at NARA are the route
<!-- /ADDENDUM -->

**Method:**
1. Reconstruct the 1948 hydrograph from gage records
2. Run the model with 1948 conditions (dam geometry, channel, land cover)
3. Compare model output vs. observed stages and times of travel
4. Compute error metrics (peak stage, time to peak, inundation extent)
5. Document discrepancies and their likely causes

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** this gap IS the known answer for the whole spec
<!-- /ADDENDUM -->

**Expected deliverable:** A validation report with 1948 reproduction
results, error analysis, and model adjustment recommendations.

**Falsifier:** The model reproduces 1948 within 20% on peak stage at
Bonneville (then validation passes; if not, the model needs adjustment).

---

## 11. EXPOSURE MAPPING — Population and Critical Facilities

**Gap:** The spec says "overlay exposure on the same sheet" but
provides no method.

**Knowledge state:** NOT_STUDIED

**Research question:** What populations and critical facilities lie in
the velocity bands and time slices of a cascade failure?

**Disciplines:** GIS, demography, emergency management, public health

**Data sources:**
- Census block groups (US Census Bureau)
- National Structure Inventory (NSI) or state equivalents
- Critical facility databases (hospitals, schools, nursing homes)
- FEMA P-2067 critical facility criteria
- Dasymetric redistribution tools (land cover weighted)

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- Census block groups (US Census Bureau) — **OPEN**; route: data.census.gov
- National Structure Inventory (NSI) or state equivalents — **OPEN**; route: USACE NSI 2.0 public
- Critical facility databases (hospitals, schools, nursing homes) — **OPEN**; route: HIFLD open data
- FEMA P-2067 critical facility criteria — **OPEN**; route: fema.gov
- Dasymetric redistribution tools (land cover weighted) — **OPEN**; route: open tools
<!-- /ADDENDUM -->

**Method:**
1. Overlay velocity bands (from HEC-RAS output) on census geography
2. Apply dasymetric redistribution for population accuracy
3. Identify critical facilities in each band
4. Compute time-of-day variation (nighttime residential vs. daytime
   workplace)
5. Apply FEMA velocity-depth consequence thresholds

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** a FEMA-published exposure count for a published flood zone; the overlay must reproduce it
<!-- /ADDENDUM -->

**Expected deliverable:** An exposure table (population and critical
facilities per velocity band per time slice), with temporal variation
and economic consequence estimates.

**Falsifier:** No population or critical facilities in any velocity band
(then the exposure overlay is moot).

---

## 12. DATA PIPELINE — Reproducible Preprocessing

**Gap:** Section 2 lists data sources but provides no pipeline.

**Knowledge state:** NOT_STUDIED

**Research question:** Can the full data pipeline be automated and made
reproducible?

**Disciplines:** Computer science, data engineering, GIS

**Data sources:**
- 3DEP DEM (1m/10m)
- NOAA bathymetry charts
- NLCD land cover
- NID dam geometry
- USACE reservoir surveys

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- 3DEP DEM (1m/10m) — **OPEN**; route: USGS national map
- NOAA bathymetry charts — **OPEN**; route: NOAA charts
- NLCD land cover — **OPEN**; route: mrlc.gov
- NID dam geometry — **OPEN**; route: nid.sec.usace.army.mil
- USACE reservoir surveys — **REQUESTABLE**; route: records request to the district; sedimentation surveys
<!-- /ADDENDUM -->

**Method:**
1. Build a `data_manifest.json` listing every required file, source URL,
   format, and checksum
2. Write preprocessing scripts (gdalwarp for DEM merge,
   whitebox_tools for hydrologic conditioning, NLCD → Manning n lookup)
3. Build a `Makefile` or `build.py` orchestrating the full pipeline
4. Containerize with Docker for reproducibility
5. Document step-by-step execution instructions

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** present in the entry (the falsifier -- reproduce on a second machine)
<!-- /ADDENDUM -->

**Expected deliverable:** A reproducible data pipeline with manifest,
preprocessing scripts, build automation, and documentation.

**Falsifier:** The pipeline cannot be reproduced on a second machine
(then it is not a valid pipeline).

---

## 13. THE OPERATOR SWAP ON REAL TERRAIN

**Gap:** Module F is proved as arithmetic, but the HEC-RAS run on real
terrain is still required.

**Knowledge state:** NOT_STUDIED

**Research question:** Does the operator swap change the breach set for
any real scenario on the Columbia chain?

**Disciplines:** Hydraulic engineering, computational modeling

**Data sources:**
- HEC-RAS 2D (Windows, USACE)
- 3DEP DEM
- NID dam geometry
- Published breach parameters
- Historical inflow hydrographs

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- HEC-RAS 2D (Windows, USACE) — **OPEN**; route: free USACE download; Windows only
- 3DEP DEM — **OPEN**; route: USGS national map
- NID dam geometry — **OPEN**; route: nid.sec.usace.army.mil
- Published breach parameters — **GATED**; route: journal literature; library, ILL
- Historical inflow hydrographs — **OPEN**; route: NWIS; USACE published records
<!-- /ADDENDUM -->

**Method:**
1. Build the HEC-RAS model per the spec (all 18 nodes + estuary)
2. Run Module A (single breach) with both operators:
   - Independent: breach iff max(wave, pool) >= crest
   - Coupled: breach iff wave + pool >= crest
3. Compare breach sets
4. Run with antecedent pool variations (0%, 25%, 50%, 75%, 100%)
5. Document where the operators disagree

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** reservoir-chain-coupling/chain.py: band width equals the antecedent pool on a constructed chain; the terrain run must reproduce it at one synthetic node before any real node is read
<!-- /ADDENDUM -->

**Expected deliverable:** A validation report showing the breach sets
under both operators, with the disagreement band width measured for
real terrain.

**Falsifier:** The operators agree on the breach set for all scenarios
(then Module F is not load-bearing for this chain).

---

<!-- SLOTTED 14 -->
## 14. MINING HYDROLOGY: Subsurface Alteration to Reservoir Loading

**Gap:** `SCOPE_BOUNDARY.md` places mining at the head of its own
example cascade — *"Mining destabilizes slopes -> heavy rain saturates
ground -> landslide enters reservoir -> displacement wave overtops dam"*
— but no gap in the agenda covers it. The subsurface effects are
quantified in the 2024-2025 literature. The term connecting them to
reservoir inflow or dam loading is not.

**Knowledge state:** NOT_STUDIED (the coupling term)
**Input knowledge states:** UNDER_STUDY (the subsurface parameters below)

This split is the whole point of the gap — but state it precisely. The
mining side is measured. The dam side is measured. And the Chinese
literature carries mining FURTHER than the English record does: through
to basin streamflow (Kuye River CWIM) and, separately, through to
dam-body stability (coal-mine underground reservoirs). What no record
carries is either of those to RESERVOIR POOL LOADING on a multi-dam
surface chain. The two carries stop one node short of each other, and
neither reaches a cascade. That remaining seam is a scope error under
`knowledge_state.py`, not an epistemic one.

---

## What is already quantified (do not re-derive)

| Quantity | Measured value | Source |
|---|---|---|
| Surface soil porosity, non-fissure unit | +7.42% vs undisturbed | Land Degradation & Development (Wiley, 2025) |
| Surface soil porosity, fissure unit | +19.25% vs undisturbed | same |
| Porosity driver | volume expansion of pores > 3 mm | same |
| Fracture zone height | 134-183 m, borehole-measured | Int. J. Mining Sci. & Tech. / ScienceDirect (2024) |
| Zone structure | caving / fracture / subsidence, distinct | same |
| Hydraulic conductivity | evolves spatio-temporally with the mining face | same |
| Fissure networks, hard vs weak rock | hard rock extends further vertically, denser interconnection, higher permeability coefficient | Scientific Reports (Nature, 2025) |
| Slope destabilization terms | three distinct: volumetric weight of slide body, strength softening, pore water pressure | Sci. Reports (2024), Thar Coalfield multi-aquifer open pit |
| Failure concentration | where the aquifer is exposed | same |
| Preferential flow | crack density / width / length / connectivity control vadose-zone paths | Water (MDPI, 2025), dual-domain crack-matrix model |

---

## What the basin-scale literature already carries (primary, not alternative)

The table above is the SUBSURFACE side. Separately, work that carries
mining THROUGH to basin hydrology and to dam stability already exists —
predominantly Chinese, because that is where the field has run longest
and where the 2025-2026 record is densest. Entered as peer sources, primary:

| Carry | What it establishes | Source |
|---|---|---|
| mining → basin streamflow / groundwater | InSAR-identified subsidence areas incorporated as a boundary condition in a coupled surface-water / groundwater model (CWIM) | Li, X. et al., J. Hydrol. 659:133243 (2025), 10.1016/j.jhydrol.2025.133243, Kuye River Basin |
| three-zone theory → groundwater impact | caving / fracture / subsidence zones used as the boundary condition feeding a groundwater calculation model | Li et al., River 4(1) (2025), 10.1002/rvr2.70000, Kuye |
| mining → streamflow reduction, quantified | statistical attribution of streamflow loss to mining, basin scale | Sci. China Tech. Sci., 10.1007/s11431-016-0393-4, Kuye |
| mining stress / seepage / fracture → DAM stability | multi-field coupled dam-damage evolution for coal-mine underground reservoir (CMUR) dams | Water 16(13):1856; Sustainability 16:10350 (Shigetai); 2026 review, Du T. et al. |

**PORE-PRESSURE VALIDATION CASE (Norway).** The LEM coupling below has
pore pressure `u` as the term that drops the factor of safety, and `u`
is normally a MODELED quantity. It has been measured in the field
during an actual failure:

| Measurement | What it gives | Source |
|---|---|---|
| groundwater fluctuations recorded DURING a debris flow event, rain- and snowmelt-triggered, western Norway | the pore-pressure term observed in real time rather than inferred after the fact | Bondevik & Sorteberg (2021), Hydrol. Earth Syst. Sci. 25(7):4147–4158, 10.5194/hess-25-4147-2021 |

This is the validation case for Method step 2's transfer test on the
pore-pressure term specifically. A modeled `u` that cannot reproduce a
measured `u` on a real event has not earned its place in the FoS
calculation.

**CONFIGURATION NOTE — not a discount.** The dam in the CMUR work is a
coal-pillar dam INSIDE a mine, not a surface impoundment in a cascade.
The mechanism (stress / seepage / fracture coupling degrading a dam
body) transfers; the configuration does not. And Kuye is a semi-arid
loess basin with a depleting groundwater regime — the transfer to
Columbia hard-rock / gravel is a PHYSICS question about the two basins,
addressed in Method step 2. It is not a reason to rank these sources
below an English one.

**READ CEILING.** These are entered from English-language abstracts and
citation metadata. The CWIM boundary-condition formulation — the exact
thing that would plug into `mining_increment.py` — is not visible at
that depth. Retrieving the full text is a step in the method. This is a
capability limit on the audit, not an open question about the work.

---

## Governing equations (forms verified; two named citations are not)

**SLOPE STABILITY — Limit Equilibrium Method (LEM)**

    FoS = resisting / driving = (c·L + N_eff·tanφ) / (driving shear)
    inputs: cohesion c, unit weight γ, slope height H, friction angle φ,
            pore pressure u
    mining coupling: excavation/blasting raises pore pressure u
      → effective normal stress N_eff = N − u·L falls
      → FoS falls. this is the pore-pressure term the slope literature names.

Method family is textbook (Fellenius, Bishop-simplified, Janbu,
Morgenstern-Price, Spencer, Sarma) and needs no single citation.
Confirmed recent open-pit applications: non-coal open-pit LEM + FLAC3D
(2026); improved Sarma with nonhomogeneous hydraulic boundary conditions
(Sci. Rep. 2025, s41598-025-17972-5, Aynak open-pit copper).

**SUBSIDENCE — time function**

    canonical Knothe (CONFIRMED):
      dW/dt = c·(W₀ − W(t))   →   W(t) = W₀·(1 − e^(−c·t))
      W₀ max subsidence, c overburden mechanical coefficient
      [Zhang, Yan, Tan, Dong 2022, Sci. Rep. 12:18433,
       10.1038/s41598-022-23303-9, Barapukuria coal mine]

    sigmoidal / MMF family (alternative form, as supplied):
      Sₜ = W₀·t^b / (a + t^b)
      a,b geology-dependent; same asymptote Sₜ→W₀, same Sₜ(0)=0.
      one of the benchmarked family (MMF, Weibull, Usher, tanh,
      power-Knothe) in the InSAR time-function literature
      (Remote Sens. 2024, 16:1938)

**STRAIN INTEGRATION (subsidence from a vertical strain profile)**

    S = ∫[h₁→h₂] ε̄ dh
    mean vertical strain integrated over affected depth; dimensionally length.

**PROVENANCE FLAG — two citations could not be confirmed:**

    "Padhy et al. 2026, Springer" (LEM FoS)
      → no such author/paper surfaced. real 2026 open-pit LEM work
        exists; the FoS method is textbook and does not rest on it.
    "Piao et al. 2024, Nature"  (Sₜ = W₀·t^b/(a+t^b))
      → Piao C.D. is a real subsidence researcher (water-conducting
        fracture zones), but this specific paper/formula pairing did
        not surface. the Knothe form above IS confirmed — anchor on it,
        treat the MMF form as an alternative pending its real citation.

    same discipline as the ±10% breach figure: the math is sound, the
    two named attributions are not verified. resolve before a student
    cites them. do not publish "Padhy 2026" or "Piao 2024" as given.

---

**CITATION STATUS: UNVERIFIED-PROVENANCE.** The table rows above were located by
search, not drawn from the source set the module arithmetic was built
from. They confirm the mechanism is quantified; they are not asserted
to be the specific papers behind any equation in this repo. A student
opening this gap resolves the citations against the module arithmetic
as step zero.

**TRANSFER CAVEAT.** The subsurface rows are coal-basin work (China,
Pakistan); the basin-scale carries are loess / coal basins (Kuye). This
is a PHYSICS question about basin conditions — hard-rock and gravel
mining, different overburden, different aquifer structure — not a
discount on the sources. Establishing or refuting transfer is Method
step 2, part of the gap, not a precondition for it. The language of the
source carries no weight here; the geology of the basin carries all of it.

---

**Research question:** Does mining-induced subsurface alteration change
antecedent pool level, reservoir inflow timing, or reservoir-rim slope
stability enough to shift the breach set on the Columbia/Snake chain?

**Disciplines:** Mining engineering, hydrogeology, geomorphology,
geotechnical engineering, dam safety

**Data sources:**
- USGS Mineral Resources Data System (MRDS) — mine locations, commodity, status
- State mining permits and reclamation records (WA, OR, ID, MT, BC)
- USGS groundwater monitoring wells in mined watersheds
- InSAR subsidence products (Sentinel-1, ESA; USGS/JPL ARIA)
- NLCD land cover change over mined parcels
- USGS gage records for tributaries draining mined watersheds
- Reservoir rim stability assessments (USACE, BC Hydro, if published)
- The 2024-2025 subsurface literature above

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- USGS Mineral Resources Data System (MRDS) — mine locations, commodity, status — **OPEN**; route: mrdata.usgs.gov
- State mining permits and reclamation records (WA, OR, ID, MT, BC) — **REQUESTABLE**; route: state agency records request (WA DNR, OR DOGAMI, ID IDL, MT DEQ; BC EMLI)
- USGS groundwater monitoring wells in mined watersheds — **OPEN**; route: NWIS groundwater
- InSAR subsidence products (Sentinel-1, ESA; USGS/JPL ARIA) — **OPEN**; route: ESA Copernicus (Sentinel-1); ARIA products
- NLCD land cover change over mined parcels — **OPEN**; route: mrlc.gov
- USGS gage records for tributaries draining mined watersheds — **OPEN**; route: NWIS
- Reservoir rim stability assessments (USACE, BC Hydro, if published) — **GATED**; route: FOIA to the district office holding the project file; the dam safety program manager; university holdings of USACE technical reports; BC Hydro water-use-planning documents (some public); the FERC licensing record, which is open. IF REFUSED: document it -- a data point on the EAP coverage question in Gap 3
- The 2024-2025 subsurface literature above — **GATED**; route: journal paywall; DOIs are given; library, ILL
<!-- /ADDENDUM -->

**Method:**
1. Inventory mines in the Columbia/Snake contributing watersheds; classify
   by type (open pit, underground, placer, gravel), commodity, and status
2. Establish transfer or refute it: compare host-rock and overburden
   conditions against the coal-basin studies above. Where conditions
   differ materially, mark the imported parameter UNDEFINED rather than
   applying it
3. Measure subsidence extent from InSAR over each mined parcel; where
   subsidence is detected, apply the fissure/non-fissure porosity split
4. Propagate the porosity delta to a runoff-coefficient change via water
   balance. **Name the intermediate quantity explicitly** — do not let a
   subsurface storage change and a surface flow change share a variable
   name (see the stock/flow separation in Gap 1)
5. Convert to an antecedent pool increment using the same interface
   `contributing_inflow.py` uses for urban runoff:
   `pool_effective = pool_natural * (1 + increment_fraction)`
6. Separately, map mined parcels against reservoir rim slopes; flag
   parcels where the aquifer is exposed (the failure concentration
   condition), as candidate displacement-wave sources for Module F
7. Report the increment fraction and the rim-slope flag list with
   uncertainty bounds

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** present in the entry (Bondevik & Sorteberg 2021, measured u)
<!-- /ADDENDUM -->

**Expected deliverable:** A `mining_increment.py` module in the
`contributing_inflow.py` interface, supplying a mining-attributable
pool increment fraction per tributary watershed with uncertainty
bounds, plus a rim-slope candidate list keyed to node. Every parameter
carries a knowledge state and names what would move it.

**Falsifier:** The mining-attributable pool increment is < 1% for all
tributaries AND no mined parcel intersects a reservoir rim slope. Then
the mechanism is not load-bearing for this chain and the gap closes.

**Secondary falsifier (transfer):** The coal-basin porosity and
conductivity findings do not transfer to Columbia-basin host rock.
Then the imported parameters revert to UNDEFINED and the gap narrows to
a measurement problem: what IS the porosity delta for this rock?

---

## Why this gap is different from Gaps 1-13

Gaps 1-13 ask for a value that nobody has measured. This one asks for a
**connection between bodies of measurement that already exist**. The
mining literature does not stop at the aquifer — the Chinese work
carries it to basin streamflow and, separately, to dam-body stability.
But those two carries stop one node short of each other, and neither
reaches a multi-dam surface cascade. The discontinuity is at the
institutional boundary between mining hydrology and cascade dam safety,
which is precisely the condition `SCOPE_BOUNDARY.md` names as a scope
error rather than a knowledge state.

The omission of this gap from the original thirteen is itself an
instance of the mechanism the manifesto describes: *"If a variable is
not in the model, the model shows no sensitivity to it."* The agenda
dropped mining the same way standard breach models drop it. Recording
that here rather than silently patching it is the honest version, and
it is evidence for the thesis rather than against it.

---

<!-- /SLOTTED 14 -->
<!-- SLOTTED 15 -->
## 15. BRIDGE HYDRAULICS: Debris Clog, Impoundment, and Release

**Gap:** `SCOPE_BOUNDARY.md`'s cascade has *"downstream bridge traps
debris"* as an explicit link. The bridge-scour and debris-scour
literature is quantified in the 2024-2025 record. The term the cascade
actually needs — the bridge as a **transient impoundment** that clogs,
ponds, fails, and releases — is not studied. It falls between
transportation engineering and dam safety, and neither field owns it.

**Knowledge state:** NOT_STUDIED (the impoundment/release term)
**Input knowledge states:** UNDER_STUDY (the scour and clogging inputs below)

The scour literature measures damage to a **standing** structure. The
cascade needs the structure's behavior as an **obstruction that fills,
holds water, and then gives way** — a dam-break problem wearing a
bridge's name.

---

## What is already quantified (do not re-derive)

| Quantity | Measured value | Source |
|---|---|---|
| Debris scour amplification, rectangular debris | +42–47% | Scientific Reports (Nature, 2025), s41598-025-34364-x |
| Debris scour amplification, semi-circular | +30–43% | same |
| Debris scour amplification, triangular | lower (upstream positioning partially shields the pier) | same |
| Abutment vs pier scour under debris | abutment scour consistently exceeds pier scour | same |
| Scour hole length increase (buried debris) | +~50% vs pier alone | ResearchGate, buried-debris scour-evolution study |
| Scour hole width increase (buried debris) | +~180% vs pier alone | same |
| Temporal behavior | prior work used fixed jam geometry; real jams grow during the event | J. Hydraulic Eng. (ASCE, 2024), 150(5) |
| Clogging threshold | pier spacing ≤ 10 m substantially increases clogging risk | Water Resources Research (Wiley, 2025), 2024WR039218, Belgium/Germany 2021 floods |
| Successive bridges | upstream bridge reduces downstream pier scour 30–40% (standing-structure case only) | J. Infrastructure Preservation & Resilience (Springer, 2025), s43065-025-00138-y, HEC-RAS |

**CITATION STATUS: located by search, not asserted as the source set the
module arithmetic was built from.** These confirm the mechanism is
quantified; matching them to the repo's equations is step zero for the
student who opens this gap.

---

## Instrumented cascade case and standing record (Norway)

The table above is standing-structure scour. The impoundment/release
term the gap actually needs has a MEASURED analogue — a moraine-dam
breach that produced a debris flow, with post-event morphology in hand:

| Case / record | What it gives | Source |
|---|---|---|
| moraine-dammed lake breach → 240,000 m³ debris flow, erosion and morphology measured | a measured instance of the chained-process shape (impoundment breach → debris flow), not a reconstruction — the same chain the bridge case needs | Breien, De Blasio, Elverhøi & Høeg (2008), Landslides 5(3):271–280, 10.1007/s10346-008-0118-3, Fjærland, western Norway, 8 May 2004 |
| NVE national GLOF event register — pre-1950 events (Liestøl 1956), GLACIORISK to 2003, referenced documentation to 2014, annual updates ("Glaciological investigations in Norway", e.g. Rapport 27/2022) | a continuous instrumented record maintained by the national water and energy directorate — long series is the instrument a slow debris/sediment rate requires | NVE, glacier.nve.no/Glacier/viewer/GLOF/en/ |

**INDEX-TERM NOTE.** The NVE register serves an English page and was
always reachable, but it does not rank on an English-language query
because the phenomenon indexes under `jøkullaup` / `skred` and the
institution under `NVE`. Reaching it required querying the native term
and the institution name directly. This is a retrieval barrier, not a
language barrier — the source is in English. Treat the register as a
DATA SOURCE (tier OPEN), not merely a citation.

**SIGN CAVEAT — carried from the standing-structure table.** The
successive-bridge finding (upstream bridge reduces downstream pier scour
30–40%) is a NEGATIVE interaction term and holds only for standing
structures under sustained flow. It must NOT be carried into the
release case, where the sign is expected to reverse: a failed upstream
impoundment loads the downstream structure rather than shielding it.

**SIGN CAVEAT — do not import the protective finding.** The "successive
bridges" result is a *negative* interaction term — upstream structure
shields downstream structure — which is the **opposite sign** from the
dam chain, where upstream failure amplifies downstream loading. It is
measured for the standing-structure, sustained-flow case only. It says
nothing about a bridge that clogs and fails, and must not be carried
into the release scenario. Testing the release case is the gap.

---

## The unstudied term

    scour literature has:        damage to A standing bridge        (measured)
                                 upstream bridge → downstream scour (measured, protective)
                                 clogging threshold (pier ≤ 10 m)   (measured)

    the cascade needs, and nobody owns:

        CLOG    debris from the upstream failure accumulates on the span
          ↓
        POND    backwater rises; upstream reach inundates
          ↓
        FAIL    span or foundation gives way (scour-driven or overtopping-driven)
          ↓
        RELEASE surge hydrograph + the bridge's own debris load
                delivered to the next downstream node

This is the `sediment-debris-biological-loop` marker applied to a built
obstruction. The debris that clogs the bridge is the **upstream
failure's output**, not an independent input — so the bridge does not
merely pass the cascade along. It **stores and re-releases** it, with
gain, because the jam grows during the event (the ASCE 2024 temporal
finding). A rate with gain, not a static offset.

---

**Research question:** Does a debris-clogged bridge act as a transient
impoundment whose failure changes the downstream breach set or the
exposure timing on the Columbia/Snake chain?

**Disciplines:** Hydraulic engineering, transportation/structural
engineering, dam safety, geomorphology

**Data sources:**
- National Bridge Inventory (NBI, FHWA) — location, pier spacing,
  waterway class, scour-critical rating
- USGS gage records and high-water marks (HWM)
- HEC-RAS 2D bridge routines (blocked-obstruction / perched-weir modes)
- Upstream debris supply sources: landslide inventories, mining rim-slope
  candidates (Gap 14), post-fire debris yield (Gap 2)
- USACE bridge scour and backwater studies
- The 2024-2025 debris-scour and clogging literature above

<!-- ADDENDUM tiers -->
**Access tiers (addendum — carried, not probed; a tier is a label, never a wall):**

- National Bridge Inventory (NBI, FHWA) — location, pier spacing, — **OPEN**; route: FHWA NBI public download
- USGS gage records and high-water marks (HWM) — **OPEN**; route: NWIS; USGS flood event viewer for HWMs
- HEC-RAS 2D bridge routines (blocked-obstruction / perched-weir modes) — **OPEN**; route: free USACE download; Windows only
- Upstream debris supply sources: landslide inventories, mining rim-slope — **OPEN**; route: state landslide inventories (WA DNR, OR DOGAMI); the Gap 14 and Gap 2 outputs
- USACE bridge scour and backwater studies — **GATED**; route: FOIA to the district; state DOT scour-critical files via public-records request
- The 2024-2025 debris-scour and clogging literature above — **GATED**; route: journal paywall; identifiers given; library, ILL
<!-- /ADDENDUM -->

**Method:**
1. Inventory bridges on the Columbia/Snake mainstem and the tributaries
   below dam nodes; flag every span with pier spacing ≤ 10 m (the
   clogging threshold)
2. Estimate debris supply reaching each flagged bridge from upstream
   failure sources. **The debris that clogs is the cascade's output** —
   couple this to Gap 14 (rim slopes) and Gap 2 (post-fire yield), do not
   treat debris supply as an independent parameter
3. Model the clog state (partial → full blockage) and compute backwater
   rise using HEC-RAS bridge/obstruction routines
4. Model the impoundment: pond volume behind the clogged span and the
   upstream inundation footprint
5. Model the release: bridge failure produces a surge hydrograph plus a
   debris load. Feed it to the next downstream node as an **initiator, in
   the same interface a breach hydrograph uses** — this is the `CCC_007`
   comparability requirement (every initiator writes only a hydrograph;
   the routing engine downstream is identical)
6. Test the release case **independently** of the successive-bridge
   protective finding (sign caveat above)
7. Report: which bridges can clog, the backwater/pond envelope, and
   whether the release shifts the downstream breach set

<!-- ADDENDUM known-answer -->
**Known-answer step (addendum):** bridge-impoundment/bridge_impoundment.py: gain above one iff release is faster than fill, on constructed inputs; and the Fjaerland volume as the release-half check
<!-- /ADDENDUM -->

**Expected deliverable:** A `bridge_impoundment.py` module supplying, per
candidate bridge: a clog-probability flag (pier-spacing based), a
backwater/pond envelope, and a release hydrograph in the Module F
initiator interface. Every parameter carries a knowledge state and names
what would move it.

**Falsifier:** No bridge on the chain has pier spacing ≤ 10 m, OR the
maximum clog-induced backwater is below every downstream crest AND the
release hydrograph never shifts the breach set. Then the bridge term is
not load-bearing for this chain and the gap closes.

**Secondary falsifier (coupling):** Debris supply from all upstream
sources is below the clog-forming threshold at every flagged bridge.
Then bridges pass the cascade without storing it, and the loop term
drops — which also tests the coupling to Gaps 2 and 14 directly.

---

## Why this gap is different from Gaps 1-13

Same shape as Gap 14: it connects two bodies of measurement that already
exist — debris-scour hydraulics on one side, dam-break routing on the
other — across the institutional boundary between transportation
engineering and dam safety. Neither field is incomplete on its own
terms. The discontinuity is the seam between them.

And the mechanism it models is the debris loop's own structure: an
obstruction that accumulates its load during the event and releases it
with gain. A bridge evaluated only against its own design flood is the
single-event evaluation error — the same operator swap Module F already
proves. Independent evaluation asks whether the bridge survives its
flood. Coupled evaluation asks what it does when it is already holding
the upstream failure's debris and constricting flow into the next pool.

---

<!-- /SLOTTED 15 -->
## How to Use This Document

Each gap is a **standalone undergraduate research project** — one
semester, one summer, one capstone. The student:

1. Reads the relevant module in the spec
2. Identifies the knowledge state and falsifier
3. Locates the data sources
4. Applies the method
5. Produces the deliverable
6. Updates the spec with their findings (replacing UNKNOWN_ATM with a
   verified value, or confirming the falsifier and closing the gap)

The spec is not a finished product. It is a **living research agenda** —
every gap is an invitation, every falsifier is a challenge, and every
knowledge state is a place where a student can make a real contribution
to dam safety science.

---

## The Bigger Picture

A standard dam-safety spec says: "Here is the answer." This spec says:
"Here is what we know, here is what we don't know, and here is exactly
how to find out." The gaps are not failures. They are the map.

An undergraduate who closes one of these gaps — who calibrates the urban
runoff increment, who maps tribal EAP coordination, who reproduces the
1948 flood — has done real science. They have moved a variable from
UNKNOWN_ATM to a verified value. They have made the model match the
system a little better. They have saved the next researcher from
reinventing the wheel.

That is what this spec is for. Not just to model dams. To model how we
know what we know about dams — and how we find out what we don't.
