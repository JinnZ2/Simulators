#!/usr/bin/env python3
"""
detection_loop.py - does off-gas detection change the outcome, given real latencies?

Monte Carlo over the timeline:

    off-gas onset ---> flaming ---> cabin exposure accumulates
          |
          +-- detection (sensor inside enclosure, or visual smoke in cabin)
                    |
                    +-- crew decision --> egress action --> occupants clear

Outcome measured: whether occupants are clear before t_available is consumed,
and by how much the margin misses when it misses.

The load-bearing asymmetry: FSRI reports devices typically smoked only SECONDS
before igniting. Visual smoke is therefore a late trigger by construction, while
off-gas sensing inside a sealed enclosure fires before flaming.

stdlib only. CC0.
"""

import argparse
import json
import random
import statistics


DEFAULTS = {
    # off-gas venting starts before flaming; short and variable
    "offgas_to_flame_mean_s": 25.0,
    "offgas_to_flame_sd_s": 15.0,
    "offgas_to_flame_min_s": 3.0,

    # sensor inside the enclosure, sampling + threshold + alarm
    "sensor_detect_mean_s": 15.0,
    "sensor_detect_sd_s": 6.0,

    # visual: someone in the cabin notices smoke and reports it
    # measured FROM FLAMING, because that is when cabin smoke appears
    "visual_detect_mean_s": 120.0,
    "visual_detect_sd_s": 60.0,

    "crew_decide_mean_s": 30.0,
    "crew_decide_sd_s": 15.0,

    "egress_action_mean_s": 240.0,   # move to egress point, doors, clear
    "egress_action_sd_s": 90.0,

    # tenability budget from ignition; default is the published mid-window
    "t_available_mean_s": 322.0,
    "t_available_sd_s": 55.0,
}


def trunc_norm(mu, sd, lo=0.0, rng=random):
    for _ in range(50):
        x = rng.gauss(mu, sd)
        if x >= lo:
            return x
    return lo


def one_trial(arm, p, contained_fraction, rng):
    """
    Returns (cleared_bool, margin_s).
    margin_s > 0 means occupants clear with time to spare.
    contained_fraction scales t_available: less gas in cabin, longer budget.
    """
    t_offgas = 0.0
    t_flame = t_offgas + max(p["offgas_to_flame_min_s"],
                             trunc_norm(p["offgas_to_flame_mean_s"],
                                        p["offgas_to_flame_sd_s"], 0.0, rng))

    if arm == "sensor":
        t_detect = t_offgas + trunc_norm(p["sensor_detect_mean_s"],
                                         p["sensor_detect_sd_s"], 0.0, rng)
    else:
        t_detect = t_flame + trunc_norm(p["visual_detect_mean_s"],
                                        p["visual_detect_sd_s"], 0.0, rng)

    t_decide = t_detect + trunc_norm(p["crew_decide_mean_s"],
                                     p["crew_decide_sd_s"], 0.0, rng)
    t_clear = t_decide + trunc_norm(p["egress_action_mean_s"],
                                    p["egress_action_sd_s"], 0.0, rng)

    budget = trunc_norm(p["t_available_mean_s"], p["t_available_sd_s"],
                        30.0, rng)
    # containment stretches the budget; 1.0 = none, 0.05 = 95% vented outboard
    budget = budget / max(contained_fraction, 1e-3)
    deadline = t_flame + budget

    margin = deadline - t_clear
    return (margin > 0.0), margin


def run_arm(arm, trials, contained_fraction, p, seed=1):
    rng = random.Random(seed)
    ok = 0
    margins = []
    for _ in range(trials):
        cleared, m = one_trial(arm, p, contained_fraction, rng)
        ok += 1 if cleared else 0
        margins.append(m)
    margins.sort()
    return {
        "arm": arm,
        "contained_fraction": contained_fraction,
        "p_cleared": ok / trials,
        "margin_median_s": round(statistics.median(margins), 1),
        "margin_p05_s": round(margins[int(0.05 * len(margins))], 1),
        "margin_p95_s": round(margins[int(0.95 * len(margins)) - 1], 1),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--arm", choices=["sensor", "visual", "both"],
                    default="both")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    arms = ["sensor", "visual"] if args.arm == "both" else [args.arm]
    fracs = [1.0, 0.50, 0.20]

    cases = [("station egress", dict(DEFAULTS)),
             ("tunnel walkout", dict(DEFAULTS, egress_action_mean_s=900.0,
                                     egress_action_sd_s=240.0))]

    all_out = {}
    for label, p in cases:
        all_out[label] = [run_arm(a, args.trials, f, p, args.seed)
                          for a in arms for f in fracs]

    if args.json:
        print(json.dumps({"cases": {k: v for k, v in all_out.items()}},
                         indent=2))
        return

    for label, results in all_out.items():
        print("\n=== %s ===   P(occupants clear), %d trials"
              % (label.upper(), args.trials))
        print("%-10s %14s %12s %14s %14s" % (
            "detection", "cabin gas", "P(clear)", "median margin", "p05 margin"))
        print("-" * 68)
        for r in results:
            print("%-10s %13.0f%% %11.3f %13.0fs %13.0fs" % (
                r["arm"], r["contained_fraction"] * 100, r["p_cleared"],
                r["margin_median_s"], r["margin_p05_s"]))
        s = {(r["arm"], r["contained_fraction"]): r["p_cleared"]
             for r in results}
        if ("sensor", 1.0) in s and ("visual", 1.0) in s:
            print("  detection alone:   %.3f -> %.3f"
                  % (s[("visual", 1.0)], s[("sensor", 1.0)]))
        if ("visual", 0.20) in s:
            print("  containment alone: %.3f -> %.3f"
                  % (s[("visual", 1.0)], s[("visual", 0.20)]))
        if ("sensor", 0.20) in s:
            print("  both:              %.3f -> %.3f"
                  % (s[("visual", 1.0)], s[("sensor", 0.20)]))

    print("\nREADING")
    print("  visual detection is measured from FLAMING because that is when")
    print("  cabin smoke appears. devices smoked only seconds before igniting,")
    print("  so the visual arm inherits that lateness by construction.")
    print("  below ~20% cabin gas the model saturates at P=1; that is a model")
    print("  limit, not a safety claim. do not read it as a design margin.")


if __name__ == "__main__":
    main()
