# The Instrument Investigation Protocol

Seven phases, applied to any scientific instrument in biology, ecology, or
physics. Each phase ends with an artifact and a grounding grade.

## Phase 1 — Measurand Decomposition
Separate three things that are usually conflated:
- **Measurand**: the quantity of nature you want (forest biomass, species
  presence, ground acceleration)
- **Indication**: what the instrument actually outputs (return intensity
  distribution, sequence reads, shutter events)
- **Bridge model**: the mathematics that maps indication → measurand
  (allometric equations, occupancy models, Green's functions)

The bridge model is where most "measurement error" actually lives.

## Phase 2 — Transduction Chain
Enumerate every physical link from nature to number:
`phenomenon → interaction → transducer → signal conditioning → digitization →
indication`. Grade each link's fidelity and provenance. The chain fidelity is
multiplicative; the weakest physical link caps everything downstream.

## Phase 3 — Model-Dependence Ladder
Classify every number the instrument gives you:
- **M0 direct reading** — indication itself (rarely what you want)
- **M1 calibrated reading** — indication + calibration curve (traceable)
- **M2 model-derived** — requires an empirical model (allometry, occupancy)
- **M3 model-inverted** — requires solving an inverse problem (tomography,
  remote sensing retrievals)
Higher rungs are not "worse science" — but their uncertainty is dominated by
model error, not instrument error, and must be reported as such.

## Phase 4 — Traceability Audit
Walk the calibration chain: instrument → working standard → reference standard
→ SI realization. Note every break: no reference standard exists (many
ecological measurands), chain lapses (expired calibration), or the standard
measures something slightly different (reference libraries built on other
populations/regions).

## Phase 5 — Blindness Mapping
For the instrument, list:
- **Null states**: configurations of nature producing no signal
  (arboreal species under camera traps, deep-soil carbon under LiDAR)
- **Alias states**: different worlds producing the same signal
  (two species with identical barcode regions; cloud vs. aerosol in a band)
- **Saturation states**: where the instrument stops responding linearly
- **Gate states**: where a threshold decision upstream (detection limit,
  PCR cycle cutoff) silently converts "below detection" into "absent"

## Phase 6 — Validation (in strength order)
1. Traceability check (Phase 4) — does the chain hold?
2. Inter-instrument triangulation — do physically different instruments agree?
3. Forward simulation — inject known signals into a simulated chain; recover?
4. Intervention — known change in the world (spike-in, enclosure, controlled
   burn); does the instrument track it?

## Phase 7 — Epistemic Coverage Report
The bottom line: for each aspect of the instrument's claim on nature, its grade
(measured / estimated / assumed), its grounding, and the named experiment or
standard that would upgrade it. Plus the blindness map summary: **what this
instrument cannot see, by construction.**
