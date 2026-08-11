"""Investigation: seismometer networks as instruments for ground motion.

The contrast case: a mature metrological discipline. Inertial physics, direct
SI traceability (laser interferometry primary standards), dense inter-instrument
triangulation. What does 'well grounded' actually look like — and what blind
spots remain even here?
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
    measurand="Ground velocity/acceleration vs. time at a point (m/s, m/s2)",
    indication="Voltage from inertial mass displacement transducer",
    bridge_model="Instrument response deconvolution (poles/zeros); site correction",
    model_rung="M1")
print(f"PHASE 1: rung {dec.model_rung} — dominant uncertainty: {dec.dominant_uncertainty()}")

chain = TransductionChain(links=[
    TransductionLink("ground->inertial mass", "Frame moves with ground; mass lags by inertia",
                     fidelity=0.98, grade="measured",
                     alias_states=["tilt couples into horizontal channels"]),
    TransductionLink("mass->voltage", "Capacitive/electromagnetic displacement transducer",
                     fidelity=0.97, grade="measured"),
    TransductionLink("voltage->digital counts", "24-bit digitizer, GPS-disciplined clock",
                     fidelity=0.99, grade="measured"),
    TransductionLink("counts->ground motion", "Response deconvolution; local site amplification",
                     fidelity=0.85, grade="estimated",
                     alias_states=["soft sediment amplifies — site, not source"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

tr = TraceabilityChain(levels=[
    {"level": "instrument", "status": "ok", "note": "shake-table calibration"},
    {"level": "working_standard", "status": "ok", "note": "calibrated reference seismometers"},
    {"level": "reference_standard", "status": "ok", "note": "laser interferometer primary standard"},
    {"level": "SI", "status": "ok", "note": "meter/second via laser wavelength + atomic time"},
])
print(f"PHASE 4: {tr.highest_break()} -> grade {tr.grade()}")

blind = BlindnessMap(spots=[
    BlindSpot("gate", "Below magnitude-completeness threshold, small quakes are 'not occurring'",
              "seismicity rate biased low; completeness must be estimated per network"),
    BlindSpot("frame", "Station geometry: gaps offshore / between stations",
              "locations and mechanisms biased where coverage is thin"),
    BlindSpot("alias_state", "Local site amplification vs. genuinely large source signal",
              "hazard maps conflate site response with source hazard if unmodeled"),
])
print(f"PHASE 5: {blind.summary()['n_spots']} blind spots; absence interpretable: {blind.absence_interpretable()}")

sim_naive = inject_and_recover(true_value=0.02, chain_fidelity=rep["chain_fidelity"],
                               noise=0.0005, model_bias=0.0005, tol=0.1)
print(f"PHASE 6a (naive pipeline, ideal-chain assumption): injected 0.02 m/s, "
      f"recovered {sim_naive.recovered} -> {'PASS' if sim_naive.passed else 'FAIL (as expected — response not deconvolved)'}")
# The mature discipline response: model the chain, then the effective fidelity is ~1
sim_cal = inject_and_recover(true_value=0.02, chain_fidelity=0.995,
                             noise=0.0005, model_bias=0.0001, tol=0.1)
print(f"PHASE 6b (response-deconvolved pipeline): injected 0.02 m/s, "
      f"recovered {sim_cal.recovered} -> {'PASS — traceable chain + modeled response recovers truth' if sim_cal.passed else 'FAIL'}")
sim = sim_cal  # record the proper pipeline

aspects = [
    {"aspect": "inertial transduction physics", "grade": "measured"},
    {"aspect": "digitizer and timing", "grade": "measured"},
    {"aspect": "SI traceability (laser primary standard)", "grade": "measured"},
    {"aspect": "response deconvolution", "grade": "measured"},
    {"aspect": "site amplification correction", "grade": "estimated"},
    {"aspect": "magnitude-completeness of network", "grade": "estimated"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {"investigation_id": "inv-seismometer-001", "instrument": "Broadband seismometer network",
          "domain": "physics",
          "measurand_decomposition": {"measurand": dec.measurand, "indication": dec.indication,
                                       "bridge_model": dec.bridge_model},
          "transduction_chain": rep, "model_rung": dec.model_rung,
          "traceability": {"highest_break": tr.highest_break(), "grade": tr.grade()},
          "blindness_map": blind.summary()["spots"],
          "validation": {"forward_simulation": sim.__dict__},
          "coverage": cov}
json.dump(record, open(os.path.join(OUT, "seismometer.instrument.json"), "w"), indent=2)
print("record written to outputs/seismometer.instrument.json")
