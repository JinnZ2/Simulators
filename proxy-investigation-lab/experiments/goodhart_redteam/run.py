"""Experiment: Goodhart red-team on a decision-used proxy.

Question: if the Slack-latency proxy were used for bonuses, how fast does it
decouple from burnout, and what residual signal still detects gaming?
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from proxy_lab.goodhart import red_team

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

res = red_team()
print(f"baseline proxy-outcome correlation : {res.baseline_correlation}")
print(f"after {res.gaming_latency_periods} periods of gaming pressure: {res.gamed_correlation}")
print(f"fidelity collapse                  : {res.fidelity_collapse}")
print(f"detection surface                  : {res.detection_surface['interpretation']}")
print(f"  variance ratio top decile: {res.detection_surface['variance_ratio_top_decile']:.3f}")
print(f"  slope top-vs-bottom      : {res.detection_surface['slope_top_vs_bottom']:.3f}")

rec = {"experiment_id": "exp-goodhart-001", "kind": "synthetic_ground_truth",
       "setup": {"scenario": "proxy becomes decision target; agents adapt observable only",
                  "n": 3000, "periods": 12, "adapt_rate": 0.35},
       "results": {"baseline_correlation": res.baseline_correlation,
                    "gamed_correlation": res.gamed_correlation,
                    "fidelity_collapse": res.fidelity_collapse,
                    "gaming_latency_periods": res.gaming_latency_periods,
                    "detection_surface": res.detection_surface},
       "timestamp": "2026-08-12T00:00:00Z"}
json.dump(rec, open(os.path.join(OUT, "goodhart-redteam.experiment.json"), "w"), indent=2)
print("record written to outputs/goodhart-redteam.experiment.json")
