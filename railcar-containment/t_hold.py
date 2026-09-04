#!/usr/bin/env python3
"""
t_hold.py - derive the containment hold-time REQUIREMENT from line geometry.

The design number the FSRI study did not have to state, because egress time was
declared out of scope:

    t_hold  >=  max( time from detection to all occupants clear )  over the line

This is a specification, not a judgement call. It is different for a metro with
900 m station spacing than for a 4 km tunnel run, and that difference is knowable
from timetable and track data alone - no fire testing required.

Two egress policies are compared:
    RUN     detect -> continue to next station -> doors -> platform clear
    STOP    detect -> stop where you are -> doors -> tunnel walkout

stdlib only. CC0.
"""

import argparse
import json
import math


def run_time_s(distance_m, speed_mps):
    """Time to close the worst-case distance at line speed, plus braking."""
    brake_pad = 8.0                      # approach and stop allowance
    return distance_m / speed_mps + brake_pad


def stop_time_s(speed_mps, decel_mps2):
    """Time to bring the train to a stand from line speed."""
    return speed_mps / decel_mps2


def required_hold(line, lat, detect_mode="sensor", policy="run"):
    detect = lat["sensor_detect_s"] if detect_mode == "sensor" \
        else lat["visual_detect_s"]
    decide = lat["crew_decide_s"]

    if policy == "run":
        move = run_time_s(line["max_run_to_egress_m"], line["line_speed_mps"])
        clear = line["platform_clear_s"]
    else:
        move = stop_time_s(line["line_speed_mps"], line["decel_mps2"])
        clear = line["tunnel_walkout_s"] if line["underground"] \
            else line["platform_clear_s"]

    total = detect + decide + move + line["door_release_s"] + clear
    return {
        "detect_s": detect, "decide_s": decide, "move_s": round(move, 1),
        "door_s": line["door_release_s"], "clear_s": clear,
        "t_hold_required_s": round(total, 1),
    }


def fmt(s):
    return "%d:%02d" % (int(s) // 60, int(s) % 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", default="params/example_lines.json")
    ap.add_argument("--margin", type=float, default=1.5,
                    help="design margin multiplier applied to the requirement")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    with open(args.lines) as f:
        cfg = json.load(f)
    lat = cfg["latencies"]

    out = []
    for line in cfg["lines"]:
        row = {"line": line["name"]}
        for mode in ("sensor", "visual"):
            for policy in ("run", "stop"):
                r = required_hold(line, lat, mode, policy)
                row["%s_%s" % (mode, policy)] = r["t_hold_required_s"]
                row["%s_%s_breakdown" % (mode, policy)] = r
        out.append(row)

    if args.json:
        print(json.dumps({"margin": args.margin, "results": out}, indent=2))
        return

    print("REQUIRED CONTAINMENT HOLD TIME, by line and egress policy")
    print("margin multiplier applied: %.2fx\n" % args.margin)
    hdr = "%-22s %12s %12s %12s %12s" % (
        "line", "sensor/RUN", "sensor/STOP", "visual/RUN", "visual/STOP")
    print(hdr)
    print("-" * len(hdr))
    for row in out:
        print("%-22s %12s %12s %12s %12s" % (
            row["line"],
            fmt(row["sensor_run"] * args.margin),
            fmt(row["sensor_stop"] * args.margin),
            fmt(row["visual_run"] * args.margin),
            fmt(row["visual_stop"] * args.margin)))

    print("\nbreakdown, worst case on each line (visual detection, STOP policy):")
    for row in out:
        b = row["visual_stop_breakdown"]
        print("  %-22s detect %ss + decide %ss + move %ss + door %ss + clear %ss"
              % (row["line"], b["detect_s"], b["decide_s"], b["move_s"],
                 b["door_s"], b["clear_s"]))

    print("\nREADING")
    print("  the spread between sensor/RUN and visual/STOP is the design space.")
    print("  detection latency and egress policy move the requirement more than")
    print("  any property of the device does. neither is a device restriction.")


if __name__ == "__main__":
    main()
