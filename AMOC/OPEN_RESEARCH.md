---

## CLAIM_TABLE_v2.md

Claims about the delivered AMOC/ folder, about what a Python stdlib environment can establish concerning it, and about the honest-gap protocol it inherits.

This is a regime-shift trajectory framework, not a forecast. No GCM is run here. No timing claim is emitted. Every output is a response surface or a band—wide where data is missing, narrow where it is supplied. The framework requires only the Python standard library.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `RGS_001` | A no-glacier start makes the transition faster and choppier than any glacial-era analog. Mechanism: loss of meltwater-buffer and permafrost thermal inertia removes damping. The divergence.py module strips analog terms that depended on continental ice, meltwater buffer, and permafrost cycle, flagging what can't be inherited. | SUPPORTED (by module architecture) |
| `RGS_002` | Analog recovery should be discounted. The 8.2ka system recovered because its freshwater pulse was finite (a draining lake). Present loading is Antarctic+Greenland sourced and sustained. divergence.py explicitly flags that recovery is not inheritable. | SUPPORTED (by module logic) |
| `RGS_003` | The collapse zone is under-determined between the two forcing models—Stommel spinodal ≈ 0.22, Kramers spinodal ≈ 0.39 on the nondim axis. This Consensus-Fault band is itself the finding: any single-model timing inside it is overconfident. trajectory.py surfaces model disagreement explicitly. | SUPPORTED (by module architecture) |
| `RGS_004` | Heinrich-class (ENSO-coupled) forcing yields a deeper, higher-variance cold band than 8.2ka-class for the same site, because it carries the amplified-variability signal. carlton_county.py runs both analogs for comparison. | SUPPORTED (by module architecture) |
| `RGS_005` | The Sv→F calibration is the most assumption-laden step in the framework, and it lives in the open. sitespec.ForcingCalibration maps real sverdrups to the nondimensional F axis with declared anchors. Do not read a nondimensional spinodal as a measured sverdrup value without going through it. | SUPPORTED |
| `RGS_006` | Every site datum carries provenance—field_measured / public_dataset / estimate / keeper, plus who, when, and confidence. A missing site datum stays None and is reported as a gap. sitespec.py enforces this. | SUPPORTED |
| `RGS_007` | The framework is forkable. Copy carlton_county.py → my_land.py, replace every Datum with your own measurement + provenance, set now_state, adjust ForcingCalibration anchors, run. | SUPPORTED (by module design) |
| `RGS_008` | The framework is stdlib-only. It imports only from the Python standard library—math, dataclasses, typing, json. No numpy, scipy, pandas, or other external dependency. | SUPPORTED |
| `RGS_009` | The delivered text is complete. Unlike the Columbia cascade spec, this README does not truncate mid-sentence. All modules are present and importable. | SUPPORTED |
| `RGS_010` | Analog numbers are order-of-magnitude scaffolding from published paleoclimate literature, marked proxy_reconstruction. Replace them. baseline.py carries three analogs (Younger Dryas, 8.2ka, Heinrich 1) with confidence and source_class. | SUPPORTED |
| `RGS_011` | Species/biome tolerances are keeper-supplied only. The framework will not invent them. sitespec.py has no built-in biome or species data. | SUPPORTED |
| `RGS_012` | The framework returns response surfaces and honest gaps, never a verdict. response.py returns bands (low, high) or flagged gaps, never point estimates. | SUPPORTED |
| `RGS_013` | Timing is a coupled-systems question this skeleton does not pretend to close. trajectory.py generates ensembles across a forcing range, not a single timeline. | SUPPORTED |
| `RGS_014` | The operator's content is preserved verbatim. The file named site.py in the collaborator's drop was saved as sitespec.py so the import chain resolves; the content is the operator's verbatim text. | SUPPORTED |

---

## UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the AMOC regime-shift framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. SITE CHARACTERIZATION — Soil Thermal Mass Measurement

**Gap:** soil_thermal_mass is a dimensionless parameter (0–1) with no calibration for any specific location.

**Knowledge state:** UNKNOWN_ATM (site-specific)

**Research question:** What is the actual soil thermal mass (thermal buffering capacity) for a given parcel, and how does it affect ecosystem lag under a regime shift?

**Disciplines:** Soil science, geomorphology, heat transfer

**Data sources:**

- Field measurements (soil temperature profiles, thermal conductivity)
- USDA NRCS soil surveys
- USGS surficial geology maps
- Published soil thermal properties for analogous lithologies

**Method:**

1. Identify the soil type and lithology for the site
2. Measure or look up thermal conductivity, volumetric heat capacity, and depth
3. Compute thermal diffusivity and damping depth
4. Calibrate the rel_0_1 scale against a reference (e.g., pure quartz sand = 0, peat = 1)
5. Validate against soil temperature time series (if available)

**Expected deliverable:** A calibrated soil_thermal_mass value with provenance (field_measured or public_dataset), replacing the estimate placeholder.

**Falsifier:** Soil thermal mass has no detectable effect on ecosystem lag (then the parameter can be dropped from the framework).

---

### 2. SITE CHARACTERIZATION — Drainage Mapping

**Gap:** drainage is a dimensionless parameter (0–1) with no calibration for any specific location.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What is the actual drainage capacity of a given parcel, and how does it affect precipitation variance amplification under a regime shift?

**Disciplines:** Hydrology, geomorphology, soil science

**Data sources:**

- Field infiltration tests
- USDA NRCS hydrologic soil groups
- USGS topographic and surficial geology maps
- Soil Survey Geographic Database (SSURGO)

**Method:**

1. Identify the hydrologic soil group for the site
2. Measure or estimate infiltration capacity
3. Classify drainage on a 0–1 scale (e.g., 0 = ponded/clay, 1 = well-drained sand/gravel)
4. Validate against storm event runoff observations

**Expected deliverable:** A calibrated drainage value with provenance, replacing the estimate placeholder.

**Falsifier:** Drainage has no detectable effect on precipitation variance amplification (then the parameter can be dropped).

---

### 3. SITE CHARACTERIZATION — Water Table Depth

**Gap:** water_table_m is a missing gap in the Carlton County example (None).

**Knowledge state:** UNKNOWN_ATM (site-specific)

**Research question:** What is the actual depth to water table for a given parcel, and how does it modulate ecosystem response to a regime shift?

**Disciplines:** Hydrology, hydrogeology, ecology

**Data sources:**

- Well logs and groundwater monitoring data (USGS, state agencies)
- Soil Survey Geographic Database (SSURGO)
- Local wetland inventories
- Field measurements (piezometers, wells)

**Method:**

1. Identify nearest monitoring wells or well logs
2. Measure or look up depth to water table (seasonal range)
3. Record minimum, mean, and maximum depths
4. Note seasonal and interannual variability

**Expected deliverable:** A water_table_m value (or range) with provenance, replacing the None gap.

**Falsifier:** Water table depth has no detectable effect on ecosystem response (then it can be dropped from the framework).

---

### 4. ANALOG CALIBRATION — Younger Dryas for Upper Midwest

**Gap:** The Younger Dryas analog is included but not calibrated to Upper Midwest conditions.

**Knowledge state:** NOT_STUDIED

**Research question:** What does the Younger Dryas analog imply for the Upper Midwest specifically, after divergence correction (no ice, no meltwater buffer, no permafrost cycle)?

**Disciplines:** Paleoclimatology, ecology, Quaternary geology

**Data sources:**

- Younger Dryas proxy records from the Upper Midwest (pollen, lake sediments, speleothems)
- North American pollen database (NAPD)
- Published Younger Dryas temperature and precipitation reconstructions for the region

**Method:**

1. Extract Upper Midwest-specific proxy records for the Younger Dryas
2. Compare to the global/northern hemisphere pattern in baseline.py
3. Compute regional scaling factors (temperature, precipitation variance, ecosystem lag)
4. Replace the analog's generic values with region-specific ones
5. Re-run the divergence correction

**Expected deliverable:** A regionally calibrated Younger Dryas analog for the Upper Midwest, with updated transition_decades, nh_cooling_C, and ecosystem_lag_decades.

**Falsifier:** The Upper Midwest shows no detectable Younger Dryas signal (then the analog is not applicable to this region).

---

### 5. ANALOG CALIBRATION — 8.2ka Event for Upper Midwest

**Gap:** The 8.2ka analog is included but not calibrated to Upper Midwest conditions.

**Knowledge state:** NOT_STUDIED

**Research question:** What does the 8.2ka event imply for the Upper Midwest specifically, given that it is the "best RATE analog"?

**Disciplines:** Paleoclimatology, ecology, Quaternary geology

**Data sources:**

- 8.2ka proxy records from the Upper Midwest
- North American pollen database (NAPD)
- Published 8.2ka temperature and precipitation reconstructions for the region

**Method:**

1. Extract Upper Midwest-specific proxy records for the 8.2ka event
2. Compare to the pattern in baseline.py
3. Compute regional scaling factors
4. Replace the analog's generic values with region-specific ones
5. Re-run the divergence correction

**Expected deliverable:** A regionally calibrated 8.2ka analog for the Upper Midwest.

**Falsifier:** The Upper Midwest shows no detectable 8.2ka signal (then the analog is not applicable).

---

### 6. ANALOG CALIBRATION — Heinrich 1 ENSO Coupling for Upper Midwest

**Gap:** The Heinrich 1 analog is included but not calibrated to Upper Midwest conditions.

**Knowledge state:** NOT_STUDIED

**Research question:** What does the Heinrich 1 (ENSO-coupled) analog imply for the Upper Midwest specifically, under a super-El-Niño-during-loading scenario?

**Disciplines:** Paleoclimatology, ENSO dynamics, Quaternary geology

**Data sources:**

- Heinrich 1 proxy records from the Upper Midwest (if any)
- Published ENSO-teleconnection studies for the region
- Modern ENSO impacts on Upper Midwest climate

**Method:**

1. Identify Heinrich 1 signals in Upper Midwest proxies (if they exist)
2. If none exist, use modern ENSO teleconnections as a proxy
3. Compute expected temperature and precipitation variance under Heinrich-like forcing
4. Replace the analog's generic values with region-specific ones
5. Re-run the divergence correction

**Expected deliverable:** A regionally calibrated Heinrich 1 analog for the Upper Midwest, with explicit uncertainty bounds.

**Falsifier:** Heinrich 1 has no detectable ENSO-teleconnection signal in the Upper Midwest (then the analog is not applicable).

---

### 7. FORCING CALIBRATION — Sv→F Anchors

**Gap:** The ForcingCalibration defaults (sv_at_F0=0.15, sv_at_spinodal=0.50) are order-of-magnitude from published box-model ranges.

**Knowledge state:** UNKNOWN_ATM (literature-dependent)

**Research question:** What are the correct Sv→F calibration anchors for the AMOC freshwater-hosing problem, given the current literature?

**Disciplines:** Physical oceanography, climate dynamics

**Data sources:**

- Published AMOC box-model and GCM freshwater-hosing studies
- IPCC AR6 WG1 (ocean circulation chapter)
- Observational estimates of North Atlantic freshwater flux

**Method:**

1. Conduct a literature review of AMOC freshwater-hosing thresholds
2. Extract the range of Sv values associated with collapse in different models
3. Compute a central estimate and uncertainty range
4. Replace the default anchors with the literature-derived values
5. Document the new anchors and their sources

**Expected deliverable:** An updated ForcingCalibration with literature-derived anchors and a full citation list.

**Falsifier:** The literature shows no consensus on Sv→F mapping (then the calibration remains under-determined, which is itself a finding).

---

### 8. VALIDATION — Historical AMOC Variability Reproduction

**Gap:** No validation section exists for the framework.

**Knowledge state:** NOT_STUDIED

**Research question:** Can the framework reproduce known historical AMOC variability (e.g., the 1970s freshening, the 1990s recovery)?

**Disciplines:** Physical oceanography, climate dynamics, model validation

**Data sources:**

- RAPID array AMOC observations (2004–present)
- Historical hydrographic sections
- Reanalysis products (e.g., ORAS5, GODAS)
- Published AMOC reconstruction time series

**Method:**

1. Extract historical freshwater forcing estimates for the North Atlantic
2. Run the Stommel and Kramers models with those forcings
3. Compare model output to observed AMOC variability (RAPID, hydrographic)
4. Compute error metrics (correlation, RMSE, bias)
5. Document where the models succeed and fail

**Expected deliverable:** A validation report comparing framework output to historical AMOC observations.

**Falsifier:** The models show no correlation with observed AMOC variability (then the framework is not capturing the relevant dynamics).

---

### 9. ECOSYSTEM LAG — Species-Specific Tolerances

**Gap:** The framework has no species-specific cold/variance tolerance data.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the cold and variance tolerances of key species (crops, trees, etc.) in a given region, and how do they affect ecosystem lag under a regime shift?

**Disciplines:** Ecology, plant physiology, forestry, agriculture

**Data sources:**

- USDA Plant Hardiness Zone maps
- Published species distribution models
- Agricultural extension records
- Forest inventory and analysis (FIA) data
- Local ecological knowledge (keeper-supplied)

**Method:**

1. Identify key species for the site (crops, timber species, native vegetation)
2. Look up or measure cold tolerance (minimum temperature, frost sensitivity)
3. Look up or measure variance tolerance (interannual variability sensitivity)
4. Compute expected mortality or stress thresholds
5. Incorporate into the ecosystem lag calculation

**Expected deliverable:** A species-tolerance table for the site, with provenance and confidence, added to the framework.

**Falsifier:** All key species have tolerances far outside the projected regime-shift bands (then ecosystem lag is not a concern).

---

### 10. GROWING SEASON — Frost Window Instability

**Gap:** The framework estimates growing season compression but does not model frost-window instability in detail.

**Knowledge state:** NOT_STUDIED

**Research question:** How does increased interannual variability affect the frost-free window, and what is the probability of crop-killing frosts under a regime shift?

**Disciplines:** Agronomy, climatology, risk analysis

**Data sources:**

- NOAA climate divisional data (frost dates, growing season length)
- USDA crop loss data
- Published studies on frost risk under climate change

**Method:**

1. Extract historical frost date time series for the site
2. Compute mean, variance, and trends
3. Model projected changes in frost date distribution under regime shift
4. Compute probability of late spring frost or early fall frost
5. Estimate crop yield impacts

**Expected deliverable:** A frost-window risk assessment for the site, with probability distributions and crop impact estimates.

**Falsifier:** Frost dates show no increase in variability under projected forcing (then frost-window instability is not a concern).

---

### 11. PRECIPITATION — Regional Routing Under Shifted Jet

**Gap:** The framework notes that "regional precip routing under a shifted jet stream" does not map 1:1 from analog ITCZ/monsoon signals.

**Knowledge state:** NOT_STUDIED

**Research question:** How does a shifted jet stream affect precipitation patterns in the Upper Midwest under an AMOC regime shift?

**Disciplines:** Meteorology, climatology, hydrology

**Data sources:**

- CMIP6 model output for AMOC collapse scenarios
- Paleo-precipitation proxies from the Upper Midwest
- NOAA/CPC jet stream and precipitation data

**Method:**

1. Identify projected jet stream shifts under AMOC weakening
2. Extract precipitation response from model ensembles
3. Compare to paleo-precipitation proxies (if available)
4. Compute expected changes in seasonal precipitation, snowpack, and drought frequency

**Expected deliverable:** A regional precipitation routing assessment for the Upper Midwest under AMOC regime shift.

**Falsifier:** The jet stream shows no significant shift under AMOC weakening (then precipitation routing is not a concern).

---

### 12. SEA LEVEL — Local Adjustment

**Gap:** The framework assumes sea_level_rising: True but does not model local sea level adjustment.

**Knowledge state:** NOT_STUDIED

**Research question:** How does regional sea level change under AMOC weakening affect coastal sites (if applicable)?

**Disciplines:** Physical oceanography, coastal geology, sea-level science

**Data sources:**

- Tide gauge records
- Satellite altimetry
- Published sea-level projections under AMOC weakening
- Local land subsidence/uplift rates

**Method:**

1. Extract local sea level rise projections under AMOC weakening
2. Account for regional ocean dynamic sea level (AMOC-induced)
3. Add local vertical land motion
4. Compute projected sea level at the site

**Expected deliverable:** A local sea level projection for the site under AMOC regime shift.

**Falsifier:** Sea level rise under AMOC weakening is negligible at the site (then it can be ignored).

---

### 13. MODEL COMPARISON — Stommel vs. Kramers Disagreement Characterization

**Gap:** The framework reports model disagreement but does not characterize why the two models disagree.

**Knowledge state:** NOT_STUDIED

**Research question:** Why do Stommel and Kramers models give different spinodal values (0.22 vs. 0.39), and what does that tell us about the underlying dynamics?

**Disciplines:** Dynamical systems, physical oceanography, model theory

**Data sources:**

- Stommel (1961) original paper
- Kramers escape-rate theory
- Published comparisons of AMOC box models

**Method:**

1. Derive the mathematical difference between the two models
2. Identify the key assumptions that drive the spinodal difference
3. Test sensitivity of each model to parameter variations
4. Characterize the conditions under which they agree or disagree

**Expected deliverable:** A model-comparison report explaining the Stommel/Kramers disagreement and its implications for AMOC collapse assessment.

**Falsifier:** The models agree under all parameter variations (then the disagreement is an artifact of the default parameters).

---

### 14. UNCERTAINTY QUANTIFICATION — Parameter Sensitivity

**Gap:** The framework has no formal sensitivity analysis for its parameters.

**Knowledge state:** NOT_STUDIED

**Research question:** Which parameters most affect the framework's output, and which are the framework robust to?

**Disciplines:** Sensitivity analysis, uncertainty quantification, computational modeling

**Data sources:**

- The framework's own parameters (config.py-like defaults in each module)
- Published ranges for each parameter

**Method:**

1. Define parameter ranges for all key parameters (Stommel eps, dt, max_t; Kramers D, w0; ForcingCalibration anchors)
2. Run the framework across parameter sweeps
3. Compute sensitivity indices (e.g., Sobol indices) for each output
4. Identify influential vs. non-influential parameters

**Expected deliverable:** A sensitivity analysis report with per-parameter, per-output sensitivity indices.

**Falsifier:** All parameters are equally influential (then sensitivity analysis is not informative).

---

### 15. USER GUIDE — Non-Modeler Translation

**Gap:** The framework is documented for developers but not for non-modeler users (policymakers, farmers, landowners).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the framework's insights be communicated to non-modelers in a way that changes how they think about AMOC risk?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Policy documents on climate risk

**Method:**

1. Translate each module's purpose and output into plain language
2. Develop case studies or scenarios for each analog
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non-modeler audiences
5. Iterate based on feedback

**Expected deliverable:** A non-technical user guide to the AMOC regime-shift framework.

**Falsifier:** Non-modeler audiences find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard AMOC impact practice

Delivered verbatim. CC0.

---

### The Problem

In AMOC impact assessment, things like local soil thermal mass, drainage, water table depth, and species-specific tolerances are not separate from the climate signal. They are direct, material, contributing factors to the regional response. When a GCM says "AMOC weakening causes cooling," that is not a local forecast. It is a large-scale pattern that gets filtered through the local substrate.

The climate system does not care about the resolution of our models. Physics does not isolate a parcel of land from the soil beneath it, the water table below that, or the species that live on it. All of those are part of one continuous system.

When we assess only the large-scale climate signal, we are not simplifying reality—we are assessing a different system than the one that actually exists. And then we are surprised when the real system behaves in ways the projection did not predict.

---

### Six Ways the Connection Gets Lost

#### 1. The "GCM as Oracle" Fallacy

Many impact assessments treat GCM output as a direct forecast for a specific location. If the GCM says "cooling of 2°C," that is treated as the answer.

But GCMs are not oracles. They are coarse-resolution models that smooth over local topography, soil, and vegetation. The 2°C is a large-scale signal. The local response depends on the substrate. If the report says "2°C cooling," it is not false, but it is incomplete. The local substrate was causal too—just not represented.

So "GCM as oracle" often means "We didn't have a downscaling method." That is a modeling limitation, not a physical fact.

#### 2. The "Analog as Template" Fallacy

Many assessments use paleo-analogs as templates—as if the past is a direct map to the future. If the Younger Dryas had 5°C cooling, that is treated as the expected response.

But the starting state is different. The Younger Dryas had continental ice, a meltwater buffer, and an active permafrost cycle. We don't. The analog cannot be inherited whole. If the assessment says "Younger Dryas implies X," it is not false, but it is incomplete. The divergence was causal too—just not accounted for.

So "analog as template" often means "We didn't correct for starting-state differences." That is an omission, not evidence that the differences don't matter.

#### 3. The "Single-Model Certainty" Fallacy

Many assessments use a single model. If the model says "collapse at 0.3 Sv," that is treated as the answer.

But models disagree. Stommel gives ~0.22; Kramers gives ~0.39 on the nondim axis. The disagreement band is itself a finding: any single-model timing inside it is overconfident. If the assessment says "collapse at 0.3 Sv," it is not false, but it is overconfident. The model disagreement was causal too—just not reported.

So "single-model certainty" often means "We chose one model and ignored the others." That is a preference, not evidence that the chosen model is correct.

#### 4. The "Finite Pulse" Fallacy

Many assessments use the 8.2ka event as a recovery analog. If the 8.2ka system recovered, that is treated as evidence that the current system will recover.

But the 8.2ka pulse was finite—a draining lake. The current loading is Antarctic+Greenland sourced and sustained. Recovery is not guaranteed. If the assessment says "recovery expected," it is not false for 8.2ka, but it may be false for the present. The loading regime was causal—just not the same.

So "finite pulse" fallacy often means "We assumed the past is a direct analog." That is an assumption, not evidence that recovery will happen.

#### 5. The "Soil as Constant" Fallacy

Many impact assessments treat soil properties as constant or ignore them entirely. If the model says "ecosystem lag of 10 years," that is treated as the answer.

But soil thermal mass, drainage, and depth vary enormously across a landscape. A thin till over bedrock has low thermal buffering. A deep organic soil has high buffering. The ecosystem lag depends on the soil. If the assessment says "10 years," it is not false for one soil type, but it may be false for another.

So "soil as constant" often means "We didn't have site-specific soil data." That is a data gap, not evidence that soil doesn't matter.

#### 6. The "Species as Generic" Fallacy

Many impact assessments treat vegetation as generic—"forest," "grassland," "crops." If the model says "forest dieback," that is treated as the answer.

But species have different tolerances. A boreal forest species may be cold-adapted but variance-sensitive. A temperate species may be variance-tolerant but cold-sensitive. The response depends on the species. If the assessment says "forest dieback," it is not false for one species assemblage, but it may be false for another.

So "species as generic" often means "We didn't have species-specific data." That is a data gap, not evidence that species don't matter.

---

### What This Framework Does Differently

This framework treats the site, the analog, and the forcing as one integrated system. The following modules document mechanisms that standard AMOC impact assessment typically drops:

- sitespec.py — The substrate: soil, water table, drainage, growing season. Every field carries provenance. Unknown stays None and is reported as a gap.
- divergence.py — The correction: strips analog terms that depended on a starting state we no longer have, flags what can't be inherited.
- forcing.py — Two models, one interface: Stommel (readable, hysteresis visible) and Kramers (continuous with cascade work). The disagreement between them is surfaced, not hidden.
- response.py — Bands, not points: temperature, precipitation variance, ecosystem lag, growing season pressure. Where a site datum is missing, the band is widened and tagged.
- trajectory.py — The anti-freeze core: ensembles across forcing range and analog set, with cliff zones and model disagreement reported explicitly.

---

### The Knowledge-State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it. The valid states are inherited from the JinnZ2 CONVERGENCE_TABLE_2026:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Soil thermal mass for a specific parcel.
UNDER_STUDY Data collection is in progress; value is provisional. Water table depth seasonal range.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. Species-specific cold tolerance for a local tree species.
UNDEFINED The variable has no agreed definition or measurement protocol. "Drainage" as a dimensionless 0–1 scale.

---

### What Is NOT a Valid Epistemic State

GCM_RESOLUTION is not a valid knowledge state. If a mechanism physically influences the system, excluding it because the GCM is too coarse to resolve it is a modeling limitation, not an epistemic one. The physics does not respect our grid cells.

The framework refuses to record a mechanism as absent because of resolution. Instead, it records the mechanism as a gap—a parameter to be filled by site-specific measurement—and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"What does the GCM say for this grid cell?"

But rather:

"What does this specific patch of ground do when the Atlantic overturning flips?"

If the answer depends on the substrate, the substrate belongs in the assessment. End of story.

The climate system is already interconnected. Our GCMs, analogs, and soil maps are the only things pretending otherwise. And that pretense has cost lives, money, and ecosystems on a scale that we are only beginning to understand.

This framework does not pretend otherwise.
