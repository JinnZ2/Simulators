"""Worked investigation: 'drayage dwell time' as a proxy for terminal congestion
raising accident risk (MSIAF maritime proxy catalog).

Shorter run — same protocol, different instrument profile.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from proxy_lab.decompose import Decomposition
from proxy_lab.grounding import ChainLink, GroundingChain
from proxy_lab.instruments import Instrument
from proxy_lab.synthetic import make_world, estimate_instrument, recovery_score
from proxy_lab.calibration import calibrate
from proxy_lab.coverage import coverage_report

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

dec = Decomposition(
    target_variable="Terminal congestion-induced systemic accident risk",
    observable_metric="Average drayage dwell time at terminal gates (minutes, daily)",
    claimed_mapping="Positive: congestion -> queue pressure + fatigue + rushed maneuvers -> elevated incident probability",
    alternative_constructs=["terminal under-staffing without congestion",
                            "appointment system misconfiguration",
                            "chassis shortage (equipment, not congestion)"])
print("PHASE 1:", dec.redefinition_risk())

chain = GroundingChain(links=[
    ChainLink("congestion->dwell", "Yard/gate congestion lengthens driver queues",
              fidelity=0.85, grade="measured",
              alternative_causes=["equipment breakdown", "customs holds"]),
    ChainLink("dwell->pressure", "Unpaid queue time creates financial urgency (demurrage clock)",
              fidelity=0.8, grade="estimated",
              alternative_causes=["driver payment structure varies by carrier"]),
    ChainLink("pressure->risk", "Urgency + heat stress + fatigue elevate incident probability",
              fidelity=0.65, grade="estimated",
              alternative_causes=["baseline incident rate varies by terminal design"]),
    ChainLink("risk->measurement", "Dwell logs captured by gate RFID/TOS",
              fidelity=0.95, grade="measured"),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']}")

world = make_world(n=3000, true_bias=0.08, true_noise=0.12,
                   confounder_leak=0.2, alt_cause_weight=0.15, seed=19)
est = estimate_instrument(world)
rec = recovery_score(world, est)
print(f"PHASE 5: recovered bias {est['estimated_bias']:.3f} (true 0.08), "
      f"noise {est['estimated_noise']:.3f} (true 0.12) -> "
      f"{'RECOVERY PASS' if rec['passed'] else 'RECOVERY FAIL'}")

rng = np.random.default_rng(23)
raw_scores = np.clip(world.latent + rng.normal(0.08, 0.18, len(world.latent)), 0, 1)
labels = (world.latent > 0.65).astype(float)
cal = calibrate(raw_scores, labels, method="platt")
print(f"PHASE 6: ECE {cal['ece_before']} -> {cal['ece_after']} "
      f"({'IMPROVED' if cal['improved'] else 'NO GAIN'})")

aspects = [
    {"aspect": "dwell-time capture (RFID/TOS logs)", "grade": "measured", "grounding_level": "G1",
     "upgrade_path": "none needed"},
    {"aspect": "congestion->dwell link", "grade": "measured", "grounding_level": "G2",
     "upgrade_path": "cross-terminal replication"},
    {"aspect": "instrument bias/noise values", "grade": "measured", "grounding_level": "G3",
     "upgrade_path": "verified incident-linked holdout"},
    {"aspect": "dwell->urgency link (payment structure)", "grade": "estimated", "grounding_level": "G3",
     "upgrade_path": "carrier-level compensation audit"},
    {"aspect": "urgency->accident link", "grade": "estimated", "grounding_level": "G3",
     "upgrade_path": "case-control on incidents vs. matched dwell exposure"},
    {"aspect": "demurrage-clock pause confound", "grade": "assumed", "grounding_level": "G4",
     "upgrade_path": "natural experiment at tariff change"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")

record = {
    "investigation_id": "inv-port-dwell-001",
    "proxy_candidate": {"target_variable": dec.target_variable,
                        "observable_metric": dec.observable_metric,
                        "claimed_mapping": dec.claimed_mapping},
    "phases": {"decomposition": {"alternative_constructs": dec.alternative_constructs},
               "grounding_chain": rep,
               "instrument": {"post_experiment": {"bias": est["estimated_bias"], "noise": est["estimated_noise"]},
                              "synthetic_recovery": rec},
               "validity_threats": [{"threat": "equipment-failure confound", "severity": "medium"},
                                     {"threat": "carrier payment heterogeneity", "severity": "medium"}],
               "experiments": ["exp-synth-dwell-001"],
               "calibration": cal},
    "coverage": cov,
}
with open(os.path.join(OUT, "port-dwell-time.investigation.json"), "w") as f:
    json.dump(record, f, indent=2)
print(f"record written to {OUT}")
