"""Worked investigation: 'Median Slack response latency outside core hours'
as a proxy for employee burnout.

Phases 1-7 of the protocol, ending in a coverage report + schema-valid record.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from proxy_lab.decompose import Decomposition
from proxy_lab.grounding import ChainLink, GroundingChain
from proxy_lab.instruments import Instrument
from proxy_lab.synthetic import make_world, estimate_instrument, recovery_score
from proxy_lab.calibration import calibrate, expected_calibration_error
from proxy_lab.coverage import coverage_report

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

# --- Phase 1: Decomposition ---
dec = Decomposition(
    target_variable="Employee burnout (operationalized: sustained cognitive-emotional exhaustion scale)",
    observable_metric="Median Slack response latency outside core hours (minutes, weekly median)",
    claimed_mapping="Positive monotone: burnout -> withdrawal behavior -> slower voluntary after-hours response",
    alternative_constructs=["disengagement from employer (not exhaustion)",
                            "boundary-setting / healthy disconnection",
                            "time-zone shifts in team composition"])
print("PHASE 1:", dec.redefinition_risk())

# --- Phase 2: Grounding chain ---
chain = GroundingChain(links=[
    ChainLink("burnout->withdrawal", "Exhaustion reduces voluntary engagement",
              fidelity=0.65, grade="estimated",
              alternative_causes=["healthy boundaries", "job dissatisfaction without exhaustion"]),
    ChainLink("withdrawal->latency", "Withdrawal manifests as slower after-hours replies",
              fidelity=0.7, grade="estimated",
              alternative_causes=["vacation", "focus blocks", "notification settings"]),
    ChainLink("latency->measurement", "Platform logs capture all reply events",
              fidelity=0.95, grade="measured",
              alternative_causes=["mobile vs desktop capture asymmetry"]),
])
rep = chain.report()
print(f"PHASE 2: chain fidelity {rep['chain_fidelity']:.3f}, weakest: {rep['weakest_link']['name']} ({rep['weakest_link']['grade']})")

# --- Phase 3: Instrument model (BEFORE experiments: mostly assumed) ---
inst = Instrument(sensor_type="collaboration_platform_logs",
                  precision=0.9, noise_floor=0.15, systematic_bias=-0.05,
                  precision_source="measured",
                  noise_floor_source="assumed",
                  systematic_bias_source="assumed")
print(f"PHASE 3: SNR at effect 0.35 = {inst.snr(0.35):.2f}; provenance {inst.provenance_summary()}")

# --- Phase 5: Synthetic ground-truth experiment ---
world = make_world(n=4000, true_bias=-0.05, true_noise=0.15,
                   confounder_leak=0.3, alt_cause_weight=0.25, seed=7)
est = estimate_instrument(world)
rec = recovery_score(world, est)
print(f"PHASE 5: pipeline recovered bias {est['estimated_bias']:.3f} (true {world.truth['bias']}), "
      f"noise {est['estimated_noise']:.3f} (true {world.truth['noise']}) -> "
      f"{'RECOVERY PASS' if rec['passed'] else 'RECOVERY FAIL'}")
# upgrade instrument provenance with measured values
inst.noise_floor, inst.systematic_bias = est["estimated_noise"], est["estimated_bias"]
inst.noise_floor_source = inst.systematic_bias_source = "measured"

# --- Phase 6: Calibration ---
# raw (overconfident) fidelity scores per subject vs. verified burnout labels (holdout)
rng = np.random.default_rng(11)
raw_scores = np.clip(world.latent + rng.normal(0.12, 0.2, len(world.latent)), 0, 1)  # systematically high
labels = (world.latent > 0.6).astype(float)
cal = calibrate(raw_scores, labels, method="isotonic")
print(f"PHASE 6: ECE {cal['ece_before']} -> {cal['ece_after']} "
      f"({'IMPROVED' if cal['improved'] else 'NO GAIN'}, n={cal['holdout_n']})")

# --- Phase 4 + 7: threats & coverage ---
aspects = [
    {"aspect": "metric capture (log pipeline)", "grade": "measured", "grounding_level": "G1",
     "upgrade_path": "none needed; periodic pipeline audit"},
    {"aspect": "instrument bias/noise values", "grade": "measured", "grounding_level": "G3",
     "upgrade_path": "larger verified-label holdout (actigraphy-linked)"},
    {"aspect": "burnout->withdrawal mechanism", "grade": "estimated", "grounding_level": "G3",
     "upgrade_path": "longitudinal within-person study; instrument with exogenous workload shocks"},
    {"aspect": "construct redefinition risk", "grade": "assumed", "grounding_level": "G4",
     "upgrade_path": "discriminant validity test vs. boundary-setting scale"},
    {"aspect": "Goodhart pressure under decision use", "grade": "assumed", "grounding_level": "G4",
     "upgrade_path": "red-team: announce metric use, measure gaming latency"},
    {"aspect": "calibration of fidelity scores", "grade": "measured", "grounding_level": "G3",
     "upgrade_path": "expand holdout; recalibrate quarterly (ECE drift watch)"},
]
cov = coverage_report(aspects)
print(f"PHASE 7: grounded fraction {cov['grounded_fraction']:.2f} — {cov['verdict']}")
print(f"  weakest: {cov['weakest_aspects']}")

record = {
    "investigation_id": "inv-burnout-latency-001",
    "proxy_candidate": {"target_variable": dec.target_variable,
                        "observable_metric": dec.observable_metric,
                        "claimed_mapping": dec.claimed_mapping},
    "phases": {"decomposition": {"alternative_constructs": dec.alternative_constructs},
               "grounding_chain": rep,
               "instrument": {"post_experiment": {"bias": est["estimated_bias"], "noise": est["estimated_noise"],
                                                  "provenance": inst.provenance_summary()},
                              "synthetic_recovery": rec},
               "validity_threats": [{"threat": "construct redefinition", "severity": "high"},
                                     {"threat": "Goodhart gaming", "severity": "medium"}],
               "experiments": ["exp-synth-burnout-001"],
               "calibration": cal},
    "coverage": cov,
}
with open(os.path.join(OUT, "burnout-latency.investigation.json"), "w") as f:
    json.dump(record, f, indent=2)
with open(os.path.join(OUT, "burnout-synth.experiment.json"), "w") as f:
    json.dump({"experiment_id": "exp-synth-burnout-001", "kind": "synthetic_ground_truth",
               "setup": {"n": 4000, "true_bias": -0.05, "true_noise": 0.15,
                         "confounder_leak": 0.3, "alt_cause_weight": 0.25},
               "results": {"estimates": est, "recovery": rec},
               "timestamp": "2026-08-12T00:00:00Z"}, f, indent=2)
print(f"records written to {OUT}")
