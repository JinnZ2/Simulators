# Instrument Epistemology

**How do we know what we know about the natural world — and what did the
instrument have to do with it?**

Every fact we hold about biology, ecology, and physics arrives through an
instrument: a thermometer, a LiDAR unit, a camera trap, an eDNA assay, a
seismometer. Each of those is, formally, a **proxy**: an unobservable natural
quantity (the measurand) mapped to an observable signal (the indication) through
a physical transduction chain plus a model. This repo applies the
proxy-investigation method — decomposition, grounding chains, instrument
characterization, validity threats, synthetic validation, calibration, coverage —
to scientific instruments themselves.

> The instrument does not just *reveal* nature. It *defines what of nature can
> be seen at all.* Every instrument carries an observational blindness map —
> and the map is rarely printed on the box.

## The Core Questions This Repo Asks of Any Instrument

1. **Measurand vs. indication** — what do you *want* to know, and what does the
   device *actually* respond to? (They are never the same thing.)
2. **Transduction chain** — every physical link from nature to number, and each
   link's fidelity and provenance.
3. **Model dependence** — which parts of the "measurement" are actually outputs
   of a model (allometric equations, inversion algorithms, reference libraries)?
4. **Traceability** — is there an unbroken calibration chain to a reference
   standard (the SI pyramid), or does the chain break somewhere?
5. **Observational blindness** — what states of the world produce *no signal* or
   the *wrong signal* in this instrument? What is structurally invisible?
6. **Theory-ladenness** — what must you already believe about the world for the
   reading to mean what you think it means?

## The Hard Problem (and how we handle it)

In the proxy lab, synthetic worlds provide an answer key. Nature provides none.
The strategies here, in order of strength:

- **Metrological traceability** — unbroken chain to SI definitions via reference
  standards (strongest; G1)
- **Inter-instrument triangulation** — two physically *different* instruments
  agreeing on the same measurand constrains both
- **Forward simulation** — simulate the physics of the transduction chain;
  inject known signals; check recovery (the synthetic method, one level down)
- **Intervention** — change the world deliberately (enclosure experiments,
  spike-ins, controlled burns) and check the instrument tracks the *known* change

## Layout

```
docs/
  protocol.md                  ← the instrument investigation protocol
  traceability-and-blindness.md← the SI pyramid, model-dependence ladder, blindness taxonomy
schemas/
  instrument.schema.json       ← instrument investigation record
src/instrum/
  measurand.py                 ← measurand/indication decomposition
  transduction.py              ← physical chain model + weakest link
  traceability.py              ← SI traceability chain checker
  blindness.py                 ← observational blindness mapping
  simulation.py                ← forward-simulated physics validation
  coverage.py                  ← epistemic coverage report
experiments/
  lidar_biomass/               ← airborne LiDAR → forest biomass (heavy model dependence)
  edna_biodiversity/           ← eDNA metabarcoding → species presence (PCR bias, library gaps)
  camera_trap_density/         ← camera traps → population density (detection probability)
  satellite_sst/               ← IR radiometry → SST (M3 inversion, real SI chain via buoys)
  isotope_diet/                ← IRMS isotopes → diet reconstruction (traceable ratio, model-bound diet)
  seismometer/                 ← seismometer networks → ground motion (the well-grounded contrast case)
  comparative_report/          ← cross-instrument analysis: what separates knowing from estimating
outputs/
tests/
```

## Quickstart

```bash
python3 experiments/lidar_biomass/run.py
python3 experiments/edna_biodiversity/run.py
python3 experiments/camera_trap_density/run.py
python3 experiments/satellite_sst/run.py
python3 experiments/isotope_diet/run.py
python3 experiments/seismometer/run.py
python3 experiments/comparative_report/run.py
python3 -m pytest tests/ -q
```

## Lineage

Method from `proxy-investigation-lab`; consumption targets are GDPRF knowledge
graphs and MSIAF environmental audits. The difference: here the "target
variable" is nature itself, and the honest answer to "how do we know?" is always
a chain — physical, mathematical, and institutional — never a single device.
