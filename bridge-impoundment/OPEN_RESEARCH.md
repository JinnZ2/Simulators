---

## CLAIM_TABLE_v2.md

Claims about the delivered bridge-impoundment/ folder, about what a Python stdlib environment can establish concerning it, and about the scaffold-as-deliverable pattern it inherits from the flood family.

This is a scaffold, not a study. No real bridge appears anywhere in this folder. No NBI inventory pass is run. No HEC-RAS backwater or release modeling is performed. What is delivered is the parameter schema, the three-state clog flag, the initiator interface contract, the mass-balance arithmetic, and both falsifier evaluators—the structure the gap's deliverable supports without data.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `BI_001` | The entry is for a register this repository does not hold. OPEN_QUESTIONS.md, SCOPE_BOUNDARY.md, Gap 14, Gap 2, and the sediment-debris-biological-loop marker exist nowhere in this tree, while all four repo-facing references resolve—CCC_007, Module F, the operator swap, and the Columbia/Snake node list. The deliverable itself (bridge_impoundment.py) exists as the scaffold, not the study. | SUPPORTED |
| `BI_002` | "Module F already proves" carries two drifts; its substance is right. The showing lives in the sibling (reservoir-chain-coupling), not the truncated Module F (CCC_001). "Proves" overstates—the FIRM layer holds on constructed chains; the real-chain question is open. The sentence's substance—a bridge evaluated only against its own design flood is the single-event evaluation error—survives both corrections. | SUPPORTED |
| `BI_003` | The sign caveat is enforceable structurally, and is enforced. The drop's sharpest rule—do not import the protective finding into the release scenario—arrives in the prose before any code. Built as structure: no function on the release path takes a shielding or reduction parameter (asserted over signatures), and the successive-bridge finding is representable only as a StandingStructureRecord whose to_initiator() raises. | SUPPORTED |
| `BI_004` | The initiator interface is checkable at the design layer. A breach initiator and a bridge-release initiator carry identical key sets; a widened dict fails the check (same_interface). Showing comparability on the engine remains the routing run this environment cannot perform. | SUPPORTED |
| `BI_005` | The conservation arithmetic is one-sided. Peak-outflow gain equals accumulation time over release time, above one exactly when the release is faster. Debris load gain is at least one by construction. A slow release attenuates; a fast release amplifies. | SUPPORTED |
| `BI_006` | Both falsifiers are three-valued. Constructed data closes the gap in both directions; an unknown input never closes it. On the real chain every cell is UNMEASURED; the data hosts in the carried allowlist-refusal state; no value supplied from memory into a flood-safety artifact. | SUPPORTED |
| `BI_007` | The drop arrives with its own citation hedge—"located by search, not asserted"—the first in the flood family to carry its negative-provenance note itself. | SUPPORTED |
| `BI_008` | SOURCE_DROP_V2.md is a verified pure insertion. The fragment comes from the delivery sheet, appears once, and removing it reproduces v1 byte-for-byte. The placement is a declared [CHOICE] since the instruction names the section, not the byte offset. | SUPPORTED |
| `BI_009` | Fjærland 2004 measures the RELEASE half only. Moraine-dammed lake breach → 240,000 m³ debris flow, post-event morphology in hand. "Clog" does not occur in the fragment. Mechanism kin, configuration differs—the sibling entry's own CONFIGURATION NOTE discipline applied to this folder's new source. | SUPPORTED |
| `BI_010` | The NVE GLOF register is a query-vocabulary-bounded null. It serves English and never ranks on an English query because the phenomenon indexes under jøkulhlaup / skred and the institution under NVE. "Long series = the instrument for a slow rate" names why a register beats event studies on a rate question. | SUPPORTED |
| `BI_011` | The parameter schema refuses values marked UNMEASURED. A parameter with knowledge_state="UNMEASURED" and a non-None value raises. Every parameter carries a moves_it string naming what would move it—a constructor rule rather than a review item. | SUPPORTED |
| `BI_012` | The clog flag has three states, never two. FLAG at or under the carried 10 m threshold, CLEAR above, UNMEASURED when spacing is unknown—an unknown spacing is not a clear span. | SUPPORTED |
| `BI_013` | The delivered code is stdlib-only. bridge_impoundment.py, audit.py, selftest_bi.py, and addendum_audit.py import only from the Python standard library. Phone-buildable, parses under 3.9. | SUPPORTED |
| `BI_014` | The CLIs refuse --selftest rather than exiting 0. No no_severity exemptions—every screen hit was reworded. | SUPPORTED |
| `BI_015` | The folder produces no real-world bridge data. No real bridge appears anywhere. The NBI inventory pass, debris-supply coupling, HEC-RAS backwater and release modeling, and the routing run are the study—they need the reading room and the engine this environment does not have. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the bridge-impoundment framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. NBI INVENTORY PASS — Bridge Spacing and Geometry

**Gap:** The scaffold's clog flag uses a carried 10 m threshold from the Belgium/Germany 2021 floods literature. No inventory pass has been run against the National Bridge Inventory (NBI) to identify which bridges on the Columbia/Snake chain fall at or under this threshold.

**Knowledge state:** NOT_STUDIED

**Research question:** Which bridges on the Columbia/Snake river chain have pier spacing ≤ 10 m, and therefore carry the clogging flag? Which bridges have unknown spacing?

**Disciplines:** Civil engineering, GIS, transportation infrastructure

**Data sources:**

- National Bridge Inventory (NBI) — nbi.fhwa.dot.gov
- State DOT bridge inventories (WA, OR, ID)
- USGS National Hydrography Dataset (NHD) for river alignment

**Method:**

1. Query NBI for all bridges crossing the Columbia and Snake rivers
2. Extract pier spacing (or structure dimensions to estimate it)
3. Apply the 10 m clogging threshold from CLOG_SPACING_M
4. Classify each bridge as FLAG, CLEAR, or UNMEASURED
5. Produce a per-bridge table matching the scaffold's schema

**Expected deliverable:** A completed bridge inventory for the Columbia/Snake chain, with per-bridge clog status and provenance, replacing the UNMEASURED cells.

**Falsifier:** No bridges on the chain have pier spacing ≤ 10 m (then the clogging mechanism is not load-bearing for this chain).

---

### 2. DEBRIS-SUPPLY COUPLING — Upstream Sediment Delivery

**Gap:** The scaffold's debris_budget() expects a debris load input. The upstream debris supply—from landslides, bank erosion, and the sediment-debris-biological loop—is not quantified for any Columbia/Snake reach.

**Knowledge state:** UNKNOWN_ATM (site-specific)

**Research question:** What is the debris supply (volume, size distribution, timing) from upstream reaches to each bridge on the Columbia/Snake chain? How does the sediment-debris-biological loop modulate this supply?

**Disciplines:** Geomorphology, sediment transport, fluvial hydraulics

**Data sources:**

- USGS sediment gaging stations
- Published landslide and bank erosion inventories
- LiDAR and aerial imagery for debris source identification
- The mining-increment/ folder (Gap 14, arrived in the same session)

**Method:**

1. Identify debris sources upstream of each bridge (landslide scars, eroding banks, mining sites)
2. Estimate debris volume and size distribution from source characterization
3. Route debris to the bridge using a simple transport model
4. Incorporate the sediment-debris-biological loop marker
5. Produce a per-bridge debris supply estimate

**Expected deliverable:** A debris-supply table for the Columbia/Snake chain, with per-bridge debris load estimates and provenance.

**Falsifier:** Debris supply to bridges is negligible (< 1 m³ per event) (then debris loading is not load-bearing).

---

### 3. CLOG DYNAMICS — Real Jam Growth vs. Fixed Geometry

**Gap:** The literature notes that prior work used fixed jam geometry; real jams grow during the event. The scaffold does not model jam growth dynamics.

**Knowledge state:** UNDER_STUDY

**Research question:** How does debris jam geometry evolve during a flood event? What is the relationship between jam growth rate, flow velocity, and debris supply?

**Disciplines:** Hydraulic engineering, sediment transport, fluid mechanics

**Data sources:**

- J. Hydraulic Eng. (ASCE, 2024), 150(5) — temporal behavior study
- Published flume and field studies of debris jam formation
- Video and photographic records of bridge clogging events

**Method:**

1. Extract jam growth rates from the 2024 ASCE study
2. Develop a parameterized jam growth model (volume vs. time)
3. Couple jam growth to flow velocity and debris supply
4. Test sensitivity of the clog flag to jam growth rate
5. Produce a jam-growth module for the scaffold

**Expected deliverable:** A jam_growth.py module that models debris jam evolution during an event, with parameterized growth rates.

**Falsifier:** Jam growth is instantaneous (then fixed geometry is sufficient).

---

### 4. PONDING AND BACKWATER — Impoundment Extent

**Gap:** The scaffold's impoundment_arithmetic() computes peak-outflow gain but does not model the ponding extent or backwater upstream of a clogged bridge.

**Knowledge state:** NOT_STUDIED

**Research question:** How far upstream does a clogged bridge pond water? What is the backwater extent and depth as a function of clog severity and discharge?

**Disciplines:** Hydraulic engineering, open-channel flow, floodplain hydraulics

**Data sources:**

- HEC-RAS models of the Columbia/Snake chain (if available)
- USGS stage-discharge relationships
- Published bridge backwater studies
- The columbia-chain-cascade HEC-RAS build spec

**Method:**

1. Develop a backwater model for a clogged bridge (HEC-RAS or analytical)
2. Compute ponding extent for each bridge under clog conditions
3. Map inundation upstream of each bridge
4. Assess whether ponding triggers upstream dam overtopping or bank failure

**Expected deliverable:** A backwater-ponding module that estimates impoundment extent and depth as a function of clog severity and discharge.

**Falsifier:** Backwater from clogged bridges is negligible (< 0.1 m stage rise) (then ponding is not load-bearing).

---

### 5. BRIDGE FAILURE MODE — Scour vs. Overtopping

**Gap:** The scaffold's release scenario assumes the bridge fails, but does not model which failure mode (scour-driven vs. overtopping-driven) occurs first.

**Knowledge state:** NOT_STUDIED

**Research question:** Under what conditions does a clogged bridge fail by scour versus overtopping? Which failure mode dominates on the Columbia/Snake chain?

**Disciplines:** Geotechnical engineering, structural engineering, hydraulics

**Data sources:**

- Published bridge failure case studies
- NBI scour-critical bridge data
- USGS flood frequency and scour analysis
- HEC-RAS scour modeling outputs

**Method:**

1. Define scour-failure criteria (foundation scour depth > footing depth)
2. Define overtopping-failure criteria (water level > bridge deck + freeboard)
3. Run both failure-mode models for each bridge under clog conditions
4. Determine which mode triggers first for each bridge
5. Produce a failure-mode classification for the chain

**Expected deliverable:** A failure-mode classification for each bridge on the chain, with scour vs. overtopping dominance identified.

**Falsifier:** All bridges fail by the same mode (then the distinction is not load-bearing).

---

### 6. RELEASE HYDROGRAPH — Surge Shape and Timing

**Gap:** The scaffold's impoundment_arithmetic() computes peak-outflow gain but does not model the release hydrograph shape or timing.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the shape and timing of the release hydrograph from a failed clogged bridge? How does it compare to a dam-break hydrograph?

**Disciplines:** Hydraulic engineering, dam safety, flood routing

**Data sources:**

- Published dam-break hydrograph studies
- Bridge failure case studies with hydrograph data
- HEC-RAS modeling of bridge failure scenarios
- The Fjærland 2004 case (moraine-dammed lake breach → debris flow)

**Method:**

1. Develop a release hydrograph model for failed clogged bridges
2. Parameterize the hydrograph by impoundment volume, breach geometry, and debris load
3. Compare to dam-break hydrographs from the columbia-chain-cascade spec
4. Test sensitivity of downstream impacts to hydrograph shape

**Expected deliverable:** A release_hydrograph.py module that generates surge hydrographs for failed clogged bridges.

**Falsifier:** The release hydrograph is identical to a dam-break hydrograph (then the bridge case adds nothing new).

---

### 7. SUCCESSIVE BRIDGE EFFECT — Protective Finding vs. Release Case

**Gap:** The literature shows upstream bridge reduces downstream pier scour 30–40% for the standing-structure, sustained-flow case. The scaffold enforces that this protective finding must not be carried into the release scenario—but the release-case effect is unmeasured.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the effect of an upstream bridge that clogs and fails on a downstream bridge? Does it amplify (like a dam cascade) or protect (like the standing-structure case)?

**Disciplines:** Hydraulic engineering, dam safety, risk analysis

**Data sources:**

- The same successive-bridges literature (J. Infrastructure Preservation & Resilience, 2025)
- Fjærland 2004 chained-process case (moraine dam → debris flow)
- HEC-RAS modeling of bridge failure cascades
- The Columbia/Snake chain node list and HEC-RAS build spec

**Method:**

1. Design a release-case experiment: upstream bridge clogs, ponds, fails, releases
2. Model the surge and debris load arriving at the downstream bridge
3. Compare to the standing-structure case (sustained flow, no failure)
4. Measure whether the upstream failure amplifies or protects downstream loading
5. Test the sign caveat empirically

**Expected deliverable:** An empirical or modeled determination of the successive-bridge effect in the release case—amplification, protection, or neutral.

**Falsifier:** The release-case effect is identical to the standing-structure case (then the protective finding can be carried over).

---

### 8. NORWEGIAN INSTRUMENTED CASE — Fjærland 2004 Transferability

**Gap:** The Fjærland 2004 case (moraine-dammed lake breach → 240,000 m³ debris flow) is carried as a measured instance of the chained-process shape. But a moraine dam is not a clogged bridge; the configuration differs.

**Knowledge state:** UNDER_STUDY

**Research question:** What transfers from the Fjærland 2004 case to the bridge-impoundment problem? What does not transfer due to the configuration difference?

**Disciplines:** Geomorphology, hydraulic engineering, case-study methodology

**Data sources:**

- Breien et al. (2008), Landslides 5(3):271-280 — Fjærland 2004
- Published bridge failure case studies
- The CONFIGURATION NOTE discipline from the sibling entry

**Method:**

1. Extract measurable quantities from Fjærland 2004: breach timing, debris volume, flow velocity, erosion morphology
2. Identify which quantities are configuration-dependent (moraine dam vs. bridge)
3. Identify which quantities are mechanism-dependent (impoundment breach → debris flow)
4. Produce a transferability matrix: what transfers, what does not
5. Apply the matrix to bridge-impoundment problem

**Expected deliverable:** A transferability analysis for the Fjærland 2004 case to bridge-impoundment, with configuration-specific adjustments.

**Falsifier:** Nothing transfers from the moraine-dam case to bridge-impoundment (then the case is not informative).

---

### 9. NVE GLOF REGISTER — Rate Estimation

**Gap:** The NVE GLOF register is carried as a standing national record that "serves English and never ranks on an English query." The register contains long series, which is "the instrument for a slow rate." But the rate has not been extracted.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the rate of GLOF (glacial lake outburst flood) events in Norway? How does this rate inform the bridge-impoundment hazard frequency?

**Disciplines:** Glaciology, hydrology, risk analysis

**Data sources:**

- NVE GLOF register: glacier.nve.no/Glacier/viewer/GLOF/en/
- Liestøl 1956 (pre-1950 events)
- GLACIORISK to 2003
- Annual updates in "Glaciological investigations in Norway" (e.g., Rapport 27/2022)

**Method:**

1. Access the NVE GLOF register (English interface available)
2. Extract event dates, locations, magnitudes
3. Compute event rate (events per year) and magnitude-frequency distribution
4. Test whether the rate is slow (as the drop suggests) or faster than expected
5. Apply the rate to bridge-impoundment hazard frequency

**Expected deliverable:** A rate estimate for GLOF events in Norway, with magnitude-frequency distribution and transferability to bridge-impoundment.

**Falsifier:** The register is inaccessible or the rate is not extractable (then the gap remains open).

---

### 10. HEC-RAS BACKWATER AND RELEASE MODELING — The Engine Run

**Gap:** The scaffold's arithmetic is conservation-based. The actual HEC-RAS backwater and release modeling is the study—it needs the engine this environment does not have.

**Knowledge state:** NOT_STUDIED

**Research question:** What does a HEC-RAS model of a clogged bridge show for backwater, ponding, and release on the Columbia/Snake chain? How do the scaffold's arithmetic predictions compare to the HEC-RAS results?

**Disciplines:** Hydraulic engineering, computational modeling, dam safety

**Data sources:**

- HEC-RAS 2D (Windows, USACE)
- The columbia-chain-cascade HEC-RAS build spec
- 3DEP DEM, NOAA bathymetry, NID dam geometry
- NBI bridge geometry and scour data

**Method:**

1. Build a HEC-RAS model of a selected reach with bridges
2. Model bridge clogging: debris jam geometry, ponding, backwater
3. Model bridge failure: release hydrograph, downstream propagation
4. Compare to the scaffold's arithmetic (gain, debris budget)
5. Document discrepancies and their causes

**Expected deliverable:** A validation report comparing scaffold arithmetic to HEC-RAS results for the bridge-impoundment problem.

**Falsifier:** The scaffold's arithmetic matches HEC-RAS within 10% (then the scaffold is sufficient for planning).

---

### 11. DEBRIS LOAD GAIN — Volume Amplification

**Gap:** The scaffold's debris_budget() computes debris load gain as "at least one by construction," but does not model the volume amplification from scour and erosion during release.

**Knowledge state:** NOT_STUDIED

**Research question:** How much does the debris volume increase during release due to scour and erosion? What is the amplification factor for the Columbia/Snake chain?

**Disciplines:** Sediment transport, geomorphology, hydraulic engineering

**Data sources:**

- Fjærland 2004: 240,000 m³ debris flow (post-event morphology measured)
- Published debris-flow entrainment studies
- USGS sediment transport data
- The scour literature in SOURCE_DROP.md (scour hole length +50%, width +180%)

**Method:**

1. Extract entrainment ratios from published debris-flow studies
2. Apply the scour amplification factors (length +50%, width +180%) to bridge scour
3. Compute debris volume amplification factor
4. Test sensitivity of downstream impacts to debris load gain

**Expected deliverable:** A debris-load-gain module for the scaffold, with amplification factors derived from literature.

**Falsifier:** Debris load gain is < 1.1 (then amplification is not load-bearing).

---

### 12. SEDIMENT-DEBRIS-BIOLOGICAL LOOP — The Marker

**Gap:** The sediment-debris-biological-loop marker is named in the drop but does not exist in this tree. The marker represents the coupling between sediment supply, debris delivery, and biological processes (wood recruitment, beaver dams, vegetation).

**Knowledge state:** UNDEFINED (the marker exists as a concept, not an implementation)

**Research question:** What is the sediment-debris-biological loop, and how does it modulate bridge-impoundment hazard? What are the coupling pathways?

**Disciplines:** Fluvial geomorphology, ecology, forest hydrology

**Data sources:**

- Published literature on large wood recruitment and transport
- Beaver dam and vegetation effects on sediment and debris
- USGS and Forest Service studies on wood in rivers
- The mining-increment/ folder (Gap 14)

**Method:**

1. Define the loop: sediment supply → debris delivery → biological feedback (wood recruitment, beaver dams) → sediment supply
2. Identify the coupling pathways relevant to bridge-impoundment
3. Parameterize each pathway
4. Incorporate the loop into the scaffold
5. Test sensitivity of bridge-impoundment hazard to loop strength

**Expected deliverable:** A sediment_debris_biological_loop.py module defining the loop and its coupling to bridge-impoundment.

**Falsifier:** The loop has no measurable effect on bridge-impoundment hazard (then it is not load-bearing).

---

### 13. SCOUR LITERATURE — Matching the Equations

**Gap:** The drop states: "These confirm the mechanism is quantified; matching them to the repo's equations is step zero for the student who opens this gap."

**Knowledge state:** NOT_STUDIED

**Research question:** How do the scour amplification factors from the 2024–2025 literature map to the scaffold's arithmetic? What is the correct equation for debris scour amplification?

**Disciplines:** Hydraulic engineering, sediment transport, meta-analysis

**Data sources:**

- Scientific Reports (Nature, 2025), s41598-025-34364-x
- ResearchGate buried-debris scour-evolution study
- J. Hydraulic Eng. (ASCE, 2024), 150(5)
- Water Resources Research (Wiley, 2025), 2024WR039218

**Method:**

1. Read each cited paper
2. Extract the amplification factors and equations
3. Map each factor to the scaffold's parameters
4. Propose a unified debris scour amplification equation
5. Test the equation against the cited data

**Expected deliverable:** A unified debris scour amplification module for the scaffold, with literature-derived equations and citations.

**Falsifier:** The literature does not provide enough data to derive an equation (then the gap remains open).

---

### 14. USER GUIDE — Non-Engineer Translation

**Gap:** The scaffold is documented for engineers and researchers but not for non-experts (policymakers, emergency managers, landowners).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the bridge-impoundment framework's insights be communicated to non-experts in a way that changes how they think about bridge failure risk?

**Disciplines:** Science communication, policy, emergency management

**Data sources:**

- The scaffold itself
- Published science communication research
- Emergency management and risk communication literature

**Method:**

1. Translate each scaffold component into plain language
2. Develop case studies or scenarios for bridge-impoundment failure
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non-expert audiences (emergency managers, landowners)
5. Iterate based on feedback

**Expected deliverable:** A non-technical user guide to the bridge-impoundment framework, with case studies and plain-language explanations.

**Falsifier:** Non-experts find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard bridge engineering practice

Delivered verbatim. CC0.

---

### The Problem

In bridge engineering and dam safety, things like debris clog, transient impoundment, and release surge are not separate from the bridge's structural behavior. They are direct, material, contributing factors to the cascade outcome. When a standard practice says those things are "out of scope" or "belong to the other field," that is usually not a scientific finding. It is a boundary choice, a disciplinary division, or a narrow definition of "bridge safety."

The river does not care about our disciplinary boundaries. Physics does not isolate a bridge from the debris that clogs it, the water that ponds behind it, or the surge that follows its failure. All of those are part of one continuous causal system.

When we model only the standing structure under sustained flow, we are not simplifying reality—we are modeling a different system than the one that actually exists. And then we are surprised when the real system behaves in ways the model did not predict.

---

### Six Ways the Connection Gets Lost

#### 1. The "Standing Structure" Fallacy

Many bridge assessments focus on the bridge as a permanent, unchanging structure under sustained flow. If the assessment says "the bridge is safe," that is treated as the answer.

But a bridge in a flood is not permanent and unchanging. It clogs with debris. It ponds water. It fails. The standing-structure case is a different system than the transient-impoundment case. If the assessment says "safe," it is not false for the standing case, but it may be false for the flood case. The transient behavior was causal—just not represented.

So "standing structure" often means "We didn't model the transient behavior." That is a modeling choice, not evidence that bridges don't clog and fail.

#### 2. The "Protective Finding" Import

Many assessments import the successive-bridges protective finding (upstream bridge reduces downstream scour 30–40%) into all scenarios. If the assessment says "upstream bridge protects downstream," that is treated as the answer.

But the protective finding is measured for the standing-structure, sustained-flow case only. It says nothing about a bridge that clogs, ponds, and fails. In the release case, the upstream bridge may amplify downstream loading—the opposite sign. If the assessment imports the protective finding, it may be wrong by the full sign. The sign caveat was causal—just not respected.

So "protective finding import" often means "We assumed the standing case applies to the transient case." That is a transferability error, not evidence that the release case is protective.

#### 3. The "Disciplinary Division" Fallacy

The bridge as a transient impoundment falls between transportation engineering and dam safety—and neither field owns it. Transportation engineers study bridges as structures. Dam safety engineers study dams as impoundments. The clogged bridge is both—and neither.

If the assessment says "out of scope," it is not false for the field's scope, but it may be false for the system. The bridge as transient impoundment was causal—just not owned.

So "disciplinary division" often means "We defined the problem to fit our expertise." That is an institutional boundary, not evidence that the bridge-as-impoundment doesn't exist.

#### 4. The "Fixed Jam Geometry" Fallacy

Many models of debris jams use fixed geometry—a jam of a certain size, shape, and porosity. If the model says "the jam causes X backwater," that is treated as the answer.

But real jams grow during the event. Debris accumulates, the jam evolves, the backwater changes. The fixed-geometry model is a different system than the growing-jam system. If the assessment says "backwater is X," it is not false for the fixed case, but it may be false for the real case. The jam growth was causal—just not represented.

So "fixed jam geometry" often means "We assumed the jam doesn't change." That is a modeling simplification, not evidence that jams are static.

#### 5. The "Scour Only" Fallacy

Many assessments of bridge failure focus on scour—the erosion of foundation material. If the assessment says "scour is the failure mode," that is treated as the answer.

But a clogged bridge can fail by overtopping as well—water rises above the deck, the bridge is swept away. The scour-only model misses the overtopping path. If the assessment says "scour is the failure mode," it is not false for the scour case, but it may be false for the overtopping case. The overtopping path was causal—just not represented.

So "scour only" often means "We assumed scour is the only failure mode." That is a failure-mode simplification, not evidence that overtopping doesn't happen.

#### 6. The "No Debris Load" Fallacy

Many models of bridge failure ignore the debris load—the bridge itself becomes debris and is delivered downstream. If the model says "the bridge fails," that is treated as the answer.

But the bridge's debris load is a new source for downstream nodes—a surge of material that can clog the next bridge, damage the next dam, or block the next channel. The no-debris-load model misses the downstream impact. If the assessment says "failure," it is not false for the bridge, but it may be false for the cascade. The debris load was causal—just not represented.

So "no debris load" often means "We stopped at the bridge." That is a cascade boundary, not evidence that the debris doesn't matter.

---

### What This Framework Does Differently

This framework treats the bridge as a transient impoundment—clog, pond, fail, release—as one integrated process. The following components document mechanisms that standard bridge assessment typically drops:

- bridge_impoundment.py — The scaffold: parameter schema (every parameter carries a knowledge state and names what would move it), three-state clog flag (FLAG / CLEAR / UNMEASURED), initiator interface contract (identical key sets across breach and release), mass-balance arithmetic (peak-outflow gain, debris load gain), and both falsifier evaluators (three-valued: constructed data closes, unknown never closes).
- The sign caveat, enforced — No function on the release path takes a shielding or reduction parameter; the protective finding is representable only as a StandingStructureRecord whose to_initiator() raises.
- The Fjærland 2004 case — A measured instance of the chained-process shape (moraine-dammed lake breach → 240,000 m³ debris flow), with configuration split applied: mechanism kin, configuration differs.
- The NVE GLOF register — A standing national record that serves English and never ranks on an English query; long series = the instrument for a slow rate.

---

### The Knowledge-State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the scaffold records its epistemic state rather than excluding it:

State Meaning Example
MEASURED A value is available from field measurement or published data. Fjærland 2004: 240,000 m³ debris flow.
UNDER_STUDY Data collection is in progress; value is provisional. The scour amplification factors from 2024–2025 literature.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. The release-case successive-bridge effect.
UNMEASURED No value is available; the cell is a gap. Per-bridge pier spacing on the Columbia/Snake chain.
CONSTRUCTED The value is synthetic, for testing the scaffold. Test data in samples/.

---

### What Is NOT a Valid Epistemic State

DISCIPLINARY_BOUNDARY is not a valid knowledge state. If a mechanism physically influences the system, excluding it because it belongs to a different field (transportation engineering vs. dam safety) is a scope error, not an epistemic one. The physics does not respect our disciplinary boundaries.

The scaffold refuses to record a mechanism as absent because of field ownership. Instead, it records the mechanism as a gap—a parameter with UNMEASURED status and a moves_it string naming what would move it—and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"Is this within our field's scope?"

But rather:

"Does this mechanism physically influence the system's behavior?"

If the answer is yes, it belongs in the model. End of story.

The river is already interconnected. Our disciplinary boundaries, standing-structure assumptions, and fixed-geometry simplifications are the only things pretending otherwise. And that pretense has cost lives, money, and ecosystems on a scale that we are only beginning to understand.

This framework does not pretend otherwise.
