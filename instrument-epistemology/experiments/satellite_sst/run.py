"""Investigation: satellite infrared radiometry as an instrument for sea-surface
temperature (SST).

Physics/M3 case: an inverse problem — radiance at top-of-atmosphere must be
inverted through an atmospheric correction model. Contrast with the ecology
cases: a real traceability chain EXISTS (buoy network), but the inversion
priors dominate the error budget.
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
    measurand="Sea-surface skin temperature (K)",
    indication="Top-of-atmosphere radiance counts in thermal IR bands",
    bridge_model="Radiative transfer inversion with atmospheric (water vapor, aerosol) correction priors",
    model_rung="M3")
print(f"PHASE 1: rung {dec.model_rung} — dominant uncertainty: {dec.dominant_uncertainty()}")

chain = TransductionChain(links=[
    TransductionLink("ocean->emission", "Planck emission from the skin layer (~10 microns)",
                     fidelity=0.99, grade="measured"),
    TransductionLink("emission->TOA radiance", "Atmospheric absorption/emission en route",
                     fidelity=0.7, grade="estimated",
                     alias_states=["water vapor and aerosols mimic temperature changes"]),
    TransductionLink("radiance->counts", "Detector response, digitization",
                     fidelity=0.97, grade="measured"),
    TransductionLink("counts->SST (inversion)", "Radiative transfer retrieval with prior atmospheres",
                     fidelity=0.75, grade="estimated",
                     alias_states=["wrong vapor prior = wrong temperature"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

tr = TraceabilityChain(levels=[
    {"level": "instrument", "status": "ok", "note": "on-board blackbody calibration"},
    {"level": "working_standard", "status": "ok", "note": "drifting buoy network intercomparison"},
    {"level": "reference_standard", "status": "ok", "note": "buoy thermistors traceable to ITS-90"},
    {"level": "SI", "status": "ok", "note": "kelvin via ITS-90 realization"},
])
print(f"PHASE 4: {tr.highest_break()} -> grade {tr.grade()}")

blind = BlindnessMap(spots=[
    BlindSpot("null_state", "Cloud cover blocks the surface entirely — IR sees cloud tops",
              "SST maps have systematic gaps exactly in stormy/dynamic regions"),
    BlindSpot("alias_state", "Diurnal warm skin layer vs. true bulk SST under low wind",
              "skin-bulk difference up to several K misread as spatial variation"),
    BlindSpot("saturation", "Detector saturates over very hot surfaces (fires)",
              "not an SST issue but corrupts adjacent pixels"),
])
print(f"PHASE 5: {blind.summary()['n_spots']} blind spots; absence interpretable: {blind.absence_interpretable()}")

sim = inject_and_recover(true_value=290.0, chain_fidelity=rep["chain_fidelity"],
                         noise=0.3, model_bias=1.5, tol=0.05)
print(f"PHASE 6: injected 290 K, recovered {sim.recovered} K "
      f"(error {sim.recovery_error:.4f}) -> {'RECOVERY PASS' if sim.passed else 'RECOVERY FAIL: inversion without correct atmospheric priors is systematically wrong'}")

aspects = [
    {"aspect": "detector calibration (on-board blackbody)", "grade": "measured"},
    {"aspect": "SI traceability via buoy network", "grade": "measured"},
    {"aspect": "atmospheric absorption physics", "grade": "estimated"},
    {"aspect": "inversion prior realism", "grade": "assumed"},
    {"aspect": "skin-bulk temperature conversion", "grade": "estimated"},
    {"aspect": "cloud-gap sampling bias", "grade": "estimated"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {"investigation_id": "inv-sst-001", "instrument": "Satellite thermal IR radiometer",
          "domain": "physics",
          "measurand_decomposition": {"measurand": dec.measurand, "indication": dec.indication,
                                       "bridge_model": dec.bridge_model},
          "transduction_chain": rep, "model_rung": dec.model_rung,
          "traceability": {"highest_break": tr.highest_break(), "grade": tr.grade()},
          "blindness_map": blind.summary()["spots"],
          "validation": {"forward_simulation": sim.__dict__},
          "coverage": cov}
json.dump(record, open(os.path.join(OUT, "satellite-sst.instrument.json"), "w"), indent=2)
print("record written to outputs/satellite-sst.instrument.json")
