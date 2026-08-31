# OPEN QUESTIONS

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

**Method:**
1. Extract impervious surface area per tributary watershed from NLCD
2. Compare gage-recorded inflow vs. naturalized flow estimates
3. Compute the urban increment as (gage - naturalized) / naturalized
4. Propagate to reservoir pool level using a simple water balance
5. Validate against known storm events

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

**Method:**
1. Identify fire events in the Columbia basin since 2000
2. Extract pre- and post-fire NLCD land cover for burned reaches
3. Use standard Manning n lookup tables (Chow 1959, Arcement & Schneider 1989)
4. Compute n_pre and n_post for each burned reach
5. Convert to attenuation reduction factor using a simple routing model
6. Validate against any available post-flood gage records

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

**Method:**
1. Identify the 6 tribal nations in the flood path (already in the spec)
2. Request or locate EAP coordination agreements for each
3. Map which dams have tribal consultation, which do not
4. Identify "cold seams" — boundaries with no shared planning
5. Compare against the international boundary (the unbridgeable seam)

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

**Method:**
1. Query NID for each dam's owner, operator, and regulatory authority
2. Cross-reference with project design memoranda for verification
3. Handle edge cases (joint ownership, leased facilities, treaty obligations)
4. Construct the seam map: USACE → USBR → PUD → BC Hydro
5. Identify international seams (CA/US) vs. domestic seams

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

**Method:**
1. Classify each dam by type (earthfill, concrete gravity, arch, etc.)
2. Apply Froehlich and Xu-Zhang equations with NID geometry
3. Compute parameter ranges (±10% on height, the most sensitive per 2026
   literature)
4. Document sunny-day vs. flood-pool initial conditions
5. Produce a breach parameter table for all 18 nodes

**Expected deliverable:** A `breach_params.csv` with per-dam Froehlich
and Xu-Zhang parameters, initial condition variants, and sensitivity
notes, referenced by Module A.

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

**Method:**
1. Extract PGA and PGV for each dam location from USGS hazard maps
2. Adjust for site soil conditions using VS30
3. Compute spectral acceleration at dam-natural-period
4. Define aftershock sequence parameters (delay distribution, damage
   state carry-forward)
5. Produce per-node ground motion time histories or response spectra

**Expected deliverable:** A `seismic_params.csv` with per-dam PGA, PGV,
SA, and aftershock parameters, referenced by Module B.

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

**Method:**
1. Identify AR4+ events in the Columbia basin historical record
2. Extract inflow hydrographs for each event
3. Compare against gate capacity ratings for each dam
4. Model partial opening scenarios vs. full opening
5. Project climate-change-adjusted hydrographs (CMIP6 ensemble)

**Expected deliverable:** A `hydro_params.csv` with design-basis AR
events, gate capacity analysis, and climate-adjusted variants,
referenced by Module C.

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

**Method:**
1. Define a SCADA trust model (binary/degraded/adversarial)
2. Define gate-opening time series for each scenario (max gates open
   for T hours)
3. Model manual override response time distribution
4. Compute the "compound factor" — how much worse is a cyber event
   during a flood vs. during normal operations?
5. Produce scenario definitions for Module D

**Expected deliverable:** A `cyber_params.yaml` with trust model states,
gate-opening scenarios, response time distributions, and compound
factors, referenced by Module D.

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

**Method:**
1. Define the compound event space (B+D, C+D, B+C+D)
2. Define interaction types (simultaneous, sequential, delayed)
3. Compute or elicit interaction factors for each combination
4. Produce a compound event matrix

**Expected deliverable:** A `compound_matrix.csv` with interaction
factors for all compound event combinations, referenced by Module E.

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

**Method:**
1. Reconstruct the 1948 hydrograph from gage records
2. Run the model with 1948 conditions (dam geometry, channel, land cover)
3. Compare model output vs. observed stages and times of travel
4. Compute error metrics (peak stage, time to peak, inundation extent)
5. Document discrepancies and their likely causes

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

**Method:**
1. Overlay velocity bands (from HEC-RAS output) on census geography
2. Apply dasymetric redistribution for population accuracy
3. Identify critical facilities in each band
4. Compute time-of-day variation (nighttime residential vs. daytime
   workplace)
5. Apply FEMA velocity-depth consequence thresholds

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

**Method:**
1. Build a `data_manifest.json` listing every required file, source URL,
   format, and checksum
2. Write preprocessing scripts (gdalwarp for DEM merge,
   whitebox_tools for hydrologic conditioning, NLCD → Manning n lookup)
3. Build a `Makefile` or `build.py` orchestrating the full pipeline
4. Containerize with Docker for reproducibility
5. Document step-by-step execution instructions

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

**Method:**
1. Build the HEC-RAS model per the spec (all 18 nodes + estuary)
2. Run Module A (single breach) with both operators:
   - Independent: breach iff max(wave, pool) >= crest
   - Coupled: breach iff wave + pool >= crest
3. Compare breach sets
4. Run with antecedent pool variations (0%, 25%, 50%, 75%, 100%)
5. Document where the operators disagree

**Expected deliverable:** A validation report showing the breach sets
under both operators, with the disagreement band width measured for
real terrain.

**Falsifier:** The operators agree on the breach set for all scenarios
(then Module F is not load-bearing for this chain).

---

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
