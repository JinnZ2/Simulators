#!/usr/bin/env python3
"""
tenability.py - how t_available moves with car volume and containment fraction.

Well-mixed single-zone cabin, three hazard channels (CO dose, convective heat,
optical density). Each channel's source coefficient is CALIBRATED to a published
anchor from FSRI 2026 at intercity volume, uncontained:

    visibility lost      < 4 min          -> anchor 230 s
    tenability window    3:37 - 7:08      -> CO dose anchor 322 s (midpoint)
    thermal              in-window        -> anchor 400 s

After calibration the model reproduces those published facts by construction.
Everything downstream - volume scaling, containment fraction - is a RATIO
against that anchor, not an independent prediction.

Not valid for absolute prediction. See README envelope section.

stdlib only. CC0.
"""

import argparse
import json

ASSUMPTIONS = {
    "V_intercity_m3": 160.0,      # single-level intercity commuter car, interior
    "V_subway_m3": 100.0,         # typical heavy-rail metro car, interior
    "vent_rise_s": 20.0,          # ramp to peak vent-gas rate, from ignition
    "vent_peak_s": 90.0,          # duration at peak
    "vent_decay_s": 180.0,        # decay back to zero
    "air_change_per_hr": 2.0,     # doors closed, HVAC running, leakage
    "CO_incap_ppm_min": 35000.0,  # dose proxy: ppm-minutes to incapacitation
    "temp_incap_C": 120.0,        # convective incapacitation threshold
    "OD_incap_per_m": 0.20,       # optical density blocking wayfinding
}

ANCHORS_S = {"od": 230.0, "co": 322.0, "temp": 400.0}
ANCHOR_WINDOW_S = (217.0, 428.0)          # 3:37 - 7:08, published
DT = 0.5
T_MAX = 3600.0

_KEY = {"co": "t_CO_dose_s", "temp": "t_thermal_s", "od": "t_visibility_s"}


def vent_rate(t, a):
    """Normalised vent-gas source strength 0..1, trapezoid from ignition."""
    r, p, d = a["vent_rise_s"], a["vent_peak_s"], a["vent_decay_s"]
    if t < 0:
        return 0.0
    if t < r:
        return t / r
    if t < r + p:
        return 1.0
    if t < r + p + d:
        return 1.0 - (t - r - p) / d
    return 0.0


def simulate(volume_m3, contained_fraction, coef, a=ASSUMPTIONS):
    """
    contained_fraction: fraction of vent gas reaching the cabin.
                        1.0 = no containment, 0.05 = 95% vented outboard.
    coef: {"co":, "temp":, "od":} calibrated source coefficients.
    Returns per-channel crossing times and t_available, in seconds.
    """
    lam = a["air_change_per_hr"] / 3600.0
    co_ppm = od = dose = 0.0
    temp_C = 20.0
    t_co = t_temp = t_od = None
    t = 0.0
    while t < T_MAX:
        s = vent_rate(t, a) * contained_fraction / volume_m3
        co_ppm += (coef.get("co", 0.0) * s - lam * co_ppm) * DT
        temp_C += (coef.get("temp", 0.0) * s - lam * (temp_C - 20.0)) * DT
        od += (coef.get("od", 0.0) * s - lam * od) * DT
        dose += co_ppm * (DT / 60.0)
        if t_co is None and dose >= a["CO_incap_ppm_min"]:
            t_co = t
        if t_temp is None and temp_C >= a["temp_incap_C"]:
            t_temp = t
        if t_od is None and od >= a["OD_incap_per_m"]:
            t_od = t
        t += DT
    times = [x for x in (t_co, t_temp, t_od) if x is not None]
    return {"t_CO_dose_s": t_co, "t_thermal_s": t_temp,
            "t_visibility_s": t_od,
            "t_available_s": min(times) if times else None}


def _channel_time(channel, c, a):
    """Crossing time for one channel alone, at anchor conditions."""
    r = simulate(a["V_intercity_m3"], 1.0, {channel: c}, a)
    return r[_KEY[channel]]


def calibrate(a=ASSUMPTIONS, anchors=ANCHORS_S):
    """
    Bisect each channel's coefficient so its crossing time hits its anchor at
    intercity volume, uncontained. Crossing time is monotone decreasing in the
    coefficient, so bisection is well posed. Geometric midpoint because the
    plausible span covers many decades.
    """
    coef = {}
    for ch, target in anchors.items():
        lo, hi = 1e-3, 1e12
        for _ in range(120):
            mid = (lo * hi) ** 0.5
            t = _channel_time(ch, mid, a)
            if t is None or t > target:
                lo = mid
            else:
                hi = mid
        coef[ch] = (lo * hi) ** 0.5
    return coef


def fmt(s):
    if s is None:
        return "never"
    return "%d:%02d" % (int(s) // 60, int(s) % 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", type=float, default=None, help="cabin m3")
    ap.add_argument("--contained", type=float, default=None,
                    help="fraction of vent gas reaching cabin, 0..1")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    a = ASSUMPTIONS
    coef = calibrate(a)

    if args.volume is not None and args.contained is not None:
        r = simulate(args.volume, args.contained, coef, a)
        if args.json:
            print(json.dumps({"volume_m3": args.volume,
                              "contained_fraction": args.contained,
                              "coef": coef, **r}, indent=2))
        else:
            print("t_available %s   (vis %s / CO %s / thermal %s)" % (
                fmt(r["t_available_s"]), fmt(r["t_visibility_s"]),
                fmt(r["t_CO_dose_s"]), fmt(r["t_thermal_s"])))
        return

    print("calibrated to published anchors, intercity volume, uncontained:")
    print("  visibility %s | CO dose %s | thermal %s"
          % (fmt(ANCHORS_S["od"]), fmt(ANCHORS_S["co"]), fmt(ANCHORS_S["temp"])))
    print("  published tenability window %s - %s\n"
          % (fmt(ANCHOR_WINDOW_S[0]), fmt(ANCHOR_WINDOW_S[1])))

    fracs = [1.00, 0.50, 0.20, 0.05, 0.01]
    print("t_available (mm:ss), cabin volume x fraction of vent gas reaching cabin")
    print("%-18s" % "" + "".join("%9s" % ("%.0f%%" % (f * 100)) for f in fracs))
    rows = {}
    for v, name in [(a["V_intercity_m3"], "intercity"),
                    (a["V_subway_m3"], "subway")]:
        line = "%-18s" % ("%s %.0f m3" % (name, v))
        rows[name] = []
        for f in fracs:
            t = simulate(v, f, coef, a)["t_available_s"]
            rows[name].append(t)
            line += "%9s" % fmt(t)
        print(line)

    ic, sw = rows["intercity"][0], rows["subway"][0]
    if ic and sw:
        print("\nvolume effect, uncontained: subway t_available is %.0f%% of "
              "intercity" % (100.0 * sw / ic))
        print("published findings are therefore a FLOOR for subway application.")
    print("\ncontainment effect, subway: %s at 100%% -> %s at 5%%"
          % (fmt(rows["subway"][0]), fmt(rows["subway"][3])))
    print("the fire still happens. it is not in the air people are breathing.")


if __name__ == "__main__":
    main()
