#!/usr/bin/env python3
"""
comparative_economics_audit/run.py – Load scenarios, compute profiles, detect anomalies.
CC0. Stdlib only.

Usage:
  python comparative_economics_audit/run.py
  python comparative_economics_audit/run.py --scenario ussr_1985
  python comparative_economics_audit/run.py --compare all
"""

import argparse
import importlib
import json
import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system_profile import SystemProfile

def load_scenario(name: str) -> SystemProfile:
    mod = importlib.import_module(f"scenarios.{name}")
    data = mod.system_profile
    profile = SystemProfile(**{k: v for k, v in data.items()
                               if not k.endswith("_note") and not k.startswith("_")})
    # Reattach notes
    for key, val in data.items():
        if key.endswith("_note") or key.startswith("_"):
            setattr(profile, key, val)
    profile.compute_composites()
    profile.anomaly_flags = profile.detect_anomalies()
    return profile

def compare_all():
    scenarios = ["us_capitalism_2026", "ussr_1985", "arabic_trust_trade"]
    profiles = {name: load_scenario(name) for name in scenarios}

    print("=" * 100)
    print("COMPARATIVE ECONOMIC SYSTEMS FINGERPRINT")
    print("=" * 100)

    # Header
    headers = ["Index"] + list(profiles.keys())
    indices = [
        "SID", "VE_VL", "MSI", "ISR", "BSC", "MM", "OSDI",
        "UFR", "ER", "HHI", "DI", "LWR", "RI",
        "OCDI", "RPI",
        "BEI", "ICD", "NEI", "RTF", "SC"
    ]

    for idx in indices:
        vals = []
        for name, p in profiles.items():
            v = getattr(p, idx, None)
            if v is None:
                vals.append("N/A")
            elif isinstance(v, float) and v == float("inf"):
                vals.append("∞")
            else:
                try:
                    vals.append(f"{v:.2f}")
                except:
                    vals.append(str(v))
        print(f"{idx:<6} " + " | ".join(f"{v:>12}" for v in vals))

    print("\n--- ANOMALY FLAGS ---")
    for name, p in profiles.items():
        if p.anomaly_flags:
            print(f"\n{name}:")
            for flag in p.anomaly_flags:
                print(f"  ⚠️  {flag}")

    print("\n--- EXPLORATION SPACES (UNKNOWN/UNEXPECTED VARIABLES) ---")
    print("""
    UFR_NEGATIVE          : Wealth flows from rich to poor. Expected in gift/redistributive economies.
    DI_INFINITE           : Total power concentration. Expected in single-party or monopoly states.
    OCDI_ZERO_OR_NEGATIVE : Minimal extraction yet system collapsed. Implies non-extraction failure 
                            (bureaucratic entropy, trust collapse, external shock). See USSR 1985.
    OCDI_NEGATIVE         : Value flows toward maintenance faster than extraction. Probable in pure gift 
                            or regenerative economies where status derives from giving.
    LWR_HIGH              : Labor dominates wealth creation. Normal for pre-financialized economies.
    ISR_INFINITE          : Full infrastructure subsidy with no market pricing. Typical in state-socialism.
    RELATIONAL_TRUST_NO_BAILOUT : High relational trust renders BSC misleadingly low; enforcement is social.
    NEGATIVE_EXTRACTION   : Value flows out of holders. NEI > 0 marks gift/reciprocal logic.
    BUREAUCRATIC_ENTROPY  : Coordination cost dominates. BEI > 0.5 signals price-signal failure.
    """)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario")
    parser.add_argument("--compare", choices=["all"])
    args = parser.parse_args()

    if args.compare == "all":
        compare_all()
    elif args.scenario:
        p = load_scenario(args.scenario)
        print(json.dumps(p.__dict__, default=str, indent=2))
    else:
        compare_all()

if __name__ == "__main__":
    main()
