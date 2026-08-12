"""Investigation: airborne LiDAR as an instrument for forest above-ground biomass.

The canonical M2 case: the 'measurement' is mostly model (allometry trained on
a handful of harvested trees), and the instrument is blind below the canopy.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from instrum.measurand import MeasurandDecomposition
from instrum.transduction import TransductionLink, TransductionChain
from instrum.traceability import TraceabilityChain
from instrum.blindness import BlindSpot, BlindnessMap
from instrum.simulation import inject_and_recover
from instrum.coverage import coverage_report

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

dec = MeasurandDecomposition(
    measurand="Above-ground dry biomass per hectare (Mg/ha)",
    indication="Georeferenced laser return point cloud (height/intensity distribution)",
    bridge_model="Allometric equation: biomass = f(canopy height metrics, cover) fitted on harvested-tree plots",
    model_rung="M2")
print(f"PHASE 1: rung {dec.model_rung} — dominant uncertainty: {dec.dominant_uncertainty()}")

chain = TransductionChain(links=[
    TransductionLink("canopy->photon scattering", "Laser pulses reflect from foliage/branches/ground",
                     fidelity=0.95, grade="measured",
                     alias_states=["dense canopy blocks returns from lower strata"]),
    TransductionLink("returns->point cloud", "Time-of-flight digitization, georegistration",
                     fidelity=0.98, grade="measured"),
    TransductionLink("point cloud->height metrics", "Statistical summaries (CHM, percentiles)",
                     fidelity=0.92, grade="estimated"),
    TransductionLink("metrics->biomass (allometry)", "Empirical model from ~dozens of harvested reference trees",
                     fidelity=0.6, grade="estimated",
                     alias_states=["model trained in one biome applied to another"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

tr = TraceabilityChain(levels=[
    {"level": "instrument", "status": "ok", "note": "range calibration vs. hard targets"},
    {"level": "working_standard", "status": "ok", "note": "calibrated ground plots"},
    {"level": "reference_standard", "status": "broken",
     "note": "no biomass primary standard; allometric references are region-specific conventions"},
    {"level": "SI", "status": "none", "note": "biomass is not an SI-realizable quantity"},
])
print(f"PHASE 4: {tr.highest_break()} -> grade {tr.grade()}")

blind = BlindnessMap(spots=[
    BlindSpot("null_state", "Understory and below-ground biomass return little/no signal",
              "carbon inventories systematically miss below-ground and understory pools"),
    BlindSpot("saturation", "Signal saturates in high-biomass dense canopy",
              "underestimation precisely where biomass is highest"),
    BlindSpot("alias_state", "Tall sparse stand vs. short dense stand can yield similar height metrics",
              "allometry misallocates biomass between structurally different forests"),
])
print(f"PHASE 5: {blind.summary()['n_spots']} blind spots; absence interpretable as absence: "
      f"{blind.absence_interpretable()}")

sim = inject_and_recover(true_value=250.0, chain_fidelity=rep["chain_fidelity"],
                         noise=8.0, model_bias=12.0, tol=0.15)
_recovery_verdict = ('RECOVERY PASS' if sim.passed else
                     'RECOVERY FAIL: pipeline reports biased biomass when '
                     'allometry+fidelity loss are unmodelled')
print(f"PHASE 6: injected 250 Mg/ha, recovered {sim.recovered} "
      f"(error {sim.recovery_error:.3f}) -> {_recovery_verdict}")

aspects = [
    {"aspect": "photon scattering physics", "grade": "measured"},
    {"aspect": "point cloud georegistration", "grade": "measured"},
    {"aspect": "height metric computation", "grade": "estimated"},
    {"aspect": "allometric bridge model", "grade": "estimated"},
    {"aspect": "biome transferability of allometry", "grade": "assumed"},
    {"aspect": "traceability to reference", "grade": "estimated"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")
print(f"  weakest: {cov['weakest_aspects']}")

record = {"investigation_id": "inv-lidar-biomass-001", "instrument": "Airborne LiDAR",
          "domain": "ecology",
          "measurand_decomposition": {"measurand": dec.measurand, "indication": dec.indication,
                                       "bridge_model": dec.bridge_model},
          "transduction_chain": rep, "model_rung": dec.model_rung,
          "traceability": {"highest_break": tr.highest_break(), "grade": tr.grade()},
          "blindness_map": blind.summary()["spots"],
          "validation": {"forward_simulation": sim.__dict__},
          "coverage": cov}
json.dump(record, open(os.path.join(OUT, "lidar-biomass.instrument.json"), "w"), indent=2)
print("record written to outputs/lidar-biomass.instrument.json")
