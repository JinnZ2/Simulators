"""Worked investigation: Weigh-In-Motion axle-load sensor as a proxy for
pavement fatigue consumption (MSIAF multimodal-infrastructure model).

Expectation: this should ground at G1 — the observable is a direct physical
measurement of the load that causes the fatigue.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from proxy_lab.decompose import Decomposition
from proxy_lab.grounding import ChainLink, GroundingChain
from proxy_lab.synthetic import make_world, estimate_instrument, recovery_score
from proxy_lab.calibration import calibrate
from proxy_lab.coverage import coverage_report

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

dec = Decomposition(
    target_variable="Cumulative pavement fatigue consumption (fraction of design life used)",
    observable_metric="Piezoelectric WIM sensor axle-load spectrum (kN per axle, continuous)",
    claimed_mapping="Fourth-power law: fatigue consumption ~ sum(axle_load^4); WIM measures the load directly",
    alternative_constructs=["static point-load damage from idling queues (different failure mode)",
                            "subgrade moisture weakening (load-independent)"])
print("PHASE 1:", dec.redefinition_risk())

chain = GroundingChain(links=[
    ChainLink("load->fatigue", "AASHTO fourth-power damage law; lab-verified mechanistic-empirical model",
              fidelity=0.9, grade="measured",
              alternative_causes=["freeze-thaw cycles", "subgrade washout bypass load channel"]),
    ChainLink("fatigue->sensor", "Piezoelectric element converts dynamic axle pressure to charge signal",
              fidelity=0.96, grade="measured",
              alternative_causes=["temperature drift", "sensor aging -> recalibration schedule"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

world = make_world(n=5000, true_bias=0.02, true_noise=0.05,
                   confounder_leak=0.1, alt_cause_weight=0.05, seed=31)
est = estimate_instrument(world)
rec = recovery_score(world, est)
print(f"PHASE 5: recovered bias {est['estimated_bias']:.3f} (true 0.02), "
      f"noise {est['estimated_noise']:.3f} (true 0.05) -> "
      f"{'RECOVERY PASS' if rec['passed'] else 'RECOVERY FAIL'}")

rng = np.random.default_rng(41)
raw = np.clip(world.latent + rng.normal(0.03, 0.06, len(world.latent)), 0, 1)
labels = (world.latent > 0.7).astype(float)
cal = calibrate(raw, labels, method="isotonic")
print(f"PHASE 6: ECE {cal['ece_before']} -> {cal['ece_after']} "
      f"({'IMPROVED' if cal['improved'] else 'NO GAIN'})")

aspects = [
    {"aspect": "axle-load measurement (piezo sensor)", "grade": "measured", "grounding_level": "G1",
     "upgrade_path": "none needed; scheduled recalibration vs. reference weighbridge"},
    {"aspect": "load->fatigue law (4th power)", "grade": "measured", "grounding_level": "G2",
     "upgrade_path": "site-specific falling-weight-deflectometer validation"},
    {"aspect": "instrument bias/noise values", "grade": "measured", "grounding_level": "G1",
     "upgrade_path": "none needed"},
    {"aspect": "non-load failure modes (moisture, freeze-thaw)", "grade": "estimated", "grounding_level": "G3",
     "upgrade_path": "fuse WIM with soil-moisture sensors for full failure-mode coverage"},
    {"aspect": "calibration of fatigue-consumption scores", "grade": "measured", "grounding_level": "G2",
     "upgrade_path": "expand core-sample verification set"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {
    "investigation_id": "inv-wim-pavement-001",
    "proxy_candidate": {"target_variable": dec.target_variable,
                        "observable_metric": dec.observable_metric,
                        "claimed_mapping": dec.claimed_mapping},
    "phases": {"decomposition": {"alternative_constructs": dec.alternative_constructs},
               "grounding_chain": rep,
               "instrument": {"post_experiment": {"bias": est["estimated_bias"], "noise": est["estimated_noise"]},
                              "synthetic_recovery": rec},
               "validity_threats": [{"threat": "load-independent failure modes", "severity": "medium"},
                                     {"threat": "sensor drift", "severity": "low (recalibration scheduled)"}],
               "experiments": ["exp-synth-wim-001"],
               "calibration": cal},
    "coverage": cov,
}
json.dump(record, open(os.path.join(OUT, "wim-pavement.investigation.json"), "w"), indent=2)
print("record written to outputs/wim-pavement.investigation.json")
