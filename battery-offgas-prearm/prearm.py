"""
battery-offgas-prearm / prearm.py -- trigger logic for a DIY off-gas pre-arm.

License: CC0. Stdlib only. Parses under Python 3.9. Phone-readable.
Status : PROPOSED, SELF-GRADED (this module and test_prearm.py share an
         author; passing them is a regression result, not a validation).

What it does
------------
Reads one or more gas-sensor streams sampled at the cell cluster, takes a
least-squares RATE OF RISE over a declared trailing window, and compares it
to a DECLARED threshold per channel. A rise that stays above threshold for a
declared number of consecutive evaluations is a "gust" and fires the stack:

    TIER 0  OPEN_DISCONNECT      cut charge/load feed, isolate the cluster.
                                 Latches. Manual reset only.
    TIER 1  PASSIVE_RECORD       phase-change material does its work with no
                                 actuation; the module only records that the
                                 passive tier is now the one carrying heat.
    TIER 2  DISCHARGE_COOLANT    local CO2 / directed cooling at the cluster,
                                 ONLY if tier 2 is armed (see interlock).

Steady "breathing" -- slow drift, daily temperature swing, a slow ramp
below threshold -- does not fire. That is the whole trigger rule: the
signal is the RATE, not the level.

What it refuses
---------------
* A channel with no declared threshold is UNRATED and contributes nothing.
  If no channel is rated, the module returns UNRATED and arms nothing.
  There is no default threshold anywhere in this file, on purpose: the
  number belongs to a bench measurement on your chemistry, your sensor and
  your enclosure (BENCH_PROTOCOL.md), not to the person who wrote this.
* Tier 2 refuses to arm unless the discharge space is declared VENTED or
  UNOCCUPIED_ENCLOSURE. A CO2 discharge into a room a person can be in is
  an asphyxiation hazard (see co2_fraction()).
* A missing sensor-fault policy is UNRATED: the module will not decide for
  you whether a dead sensor trips the disconnect or only alarms.

What it does NOT do
-------------------
* It does not stop a cell whose internal chemistry is already running away.
  Disconnecting removes external energy input; it does not remove the
  energy already inside the cell.
* It does not read absolute level unless `level_ceiling` is declared.
  A slow leak that never gusts is invisible to a rate-only rule.
* It drives no hardware. It emits an action list; the wiring is yours.

    python3 battery-offgas-prearm/prearm.py --demo
    python3 battery-offgas-prearm/prearm.py --config cfg.json --trace t.csv
    python3 battery-offgas-prearm/test_prearm.py      # the checks
"""

import json
import math
import random
import sys

UNRATED = "UNRATED"
ARMED = "ARMED"
PARTIAL = "ARMED_PARTIAL"          # some channels rated, some not
FAULT_POLICIES = ("TRIP", "ALARM")
DISCHARGE_SPACES = ("VENTED", "UNOCCUPIED_ENCLOSURE")

# [CHOICE 1] A config with SOME rated channels arms on those and lists the
#            unrated ones by name. Refusing to arm whenever any channel is
#            unrated would let one uncalibrated add-on sensor disarm the
#            whole stack. The unrated channels are reported on every run.
# [CHOICE 2] Rate of rise = Theil-Sen (median pairwise) slope over the
#            trailing window. Least squares was tried first and a single
#            one-sample spike carried it through confirmation (BOP_005).
# [CHOICE 3] A window needs at least 3 samples spanning at least half the
#            declared window before a slope is computed; otherwise the
#            evaluation is skipped (not counted as below threshold).
# [CHOICE 4] Tier 0 latches. Nothing in this module re-closes it.
CHOICES = (
    "[CHOICE 1] some channels rated -> arm on those, list the rest UNRATED",
    "[CHOICE 2] rate of rise = Theil-Sen median slope over trailing window",
    "[CHOICE 3] slope needs >=3 samples spanning >=half the window",
    "[CHOICE 4] tier 0 latches; manual reset only",
)


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def load_config(cfg):
    """Validate a config dict. Returns a dict with `status`, `rated`,
    `unrated`, `missing`, and the normalised fields. Never raises on a
    missing number: it reports it."""
    out = {"status": UNRATED, "rated": [], "unrated": [], "missing": [],
           "tier2_armed": False, "tier2_reason": None}
    channels = cfg.get("channels") or {}
    if not channels:
        out["missing"].append("channels")
    for name in sorted(channels):
        ch = channels[name] or {}
        thr = ch.get("rate_threshold")
        if not _is_number(thr) or thr <= 0:
            out["unrated"].append(name)
        else:
            out["rated"].append(name)
    for key in ("window_s", "confirm_count", "max_gap_s"):
        v = cfg.get(key)
        if not _is_number(v) or v <= 0:
            out["missing"].append(key)
    if cfg.get("on_sensor_fault") not in FAULT_POLICIES:
        out["missing"].append("on_sensor_fault")

    space = cfg.get("tier2_discharge_space")
    if not cfg.get("tier2_installed"):
        out["tier2_reason"] = "tier 2 not installed"
    elif space not in DISCHARGE_SPACES:
        out["tier2_reason"] = ("discharge space %r not declared VENTED or "
                               "UNOCCUPIED_ENCLOSURE; CO2 into an occupiable "
                               "space is an asphyxiation hazard" % (space,))
    else:
        out["tier2_armed"] = True

    if out["rated"] and not out["missing"]:
        out["status"] = PARTIAL if out["unrated"] else ARMED
    out["cfg"] = cfg
    return out


def _is_number(v):
    return (isinstance(v, (int, float)) and not isinstance(v, bool)
            and math.isfinite(v))


# --------------------------------------------------------------------------
# rate of rise
# --------------------------------------------------------------------------

def slope(samples):
    """Theil-Sen slope of (t, value) pairs, value units per second: the
    median of all pairwise slopes. One spiked sample moves at most n-1 of
    the n(n-1)/2 pairs, so a single glitch cannot carry the median.
    None (never 0.0) when there is no slope to take: fewer than 2 points or
    no spread in time."""
    pts = [(t, v) for t, v in samples if _is_number(t) and _is_number(v)]
    pairs = []
    for i in range(len(pts)):
        ti, vi = pts[i]
        for j in range(i + 1, len(pts)):
            tj, vj = pts[j]
            if tj != ti:
                pairs.append((vj - vi) / (tj - ti))
    if not pairs:
        return None
    pairs.sort()
    m = len(pairs)
    return pairs[m // 2] if m % 2 else 0.5 * (pairs[m // 2 - 1] + pairs[m // 2])


def slope_lsq(samples):
    """Least-squares slope. Kept for comparison only: it was this module's
    first choice and it tripped the disconnect on a single one-sample spike
    in the glitch fixture (BOP_005). Not used by evaluate()."""
    pts = [(t, v) for t, v in samples if _is_number(t) and _is_number(v)]
    n = len(pts)
    if n < 2:
        return None
    mt = sum(t for t, _ in pts) / n
    mv = sum(v for _, v in pts) / n
    sxx = sum((t - mt) ** 2 for t, _ in pts)
    if sxx == 0:
        return None
    return sum((t - mt) * (v - mv) for t, v in pts) / sxx


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------

def evaluate(cfg, streams):
    """Run the trigger rule over recorded streams.

    streams: {channel_name: [(t_seconds, value), ...]}  (time-ordered)
    Returns a dict: status, detect_t, detect_channel, actions, unrated,
    missing, faults. `actions` is a time-ordered list of
    {t, tier, action, reason}."""
    c = load_config(cfg)
    res = {"status": c["status"], "detect_t": None, "detect_channel": None,
           "actions": [], "unrated": c["unrated"], "missing": c["missing"],
           "faults": [], "tier2_armed": c["tier2_armed"],
           "tier2_reason": c["tier2_reason"]}
    if c["status"] == UNRATED:
        res["refusal"] = ("refuse to arm: %s" % ", ".join(
            (["no rated channel"] if not c["rated"] else [])
            + ["missing " + m for m in c["missing"]]))
        return res

    window = float(cfg["window_s"])
    confirm = int(cfg["confirm_count"])
    max_gap = float(cfg["max_gap_s"])
    ceiling = cfg.get("level_ceiling") or {}

    # merge all rated samples onto one timeline so tiers fire once, in order
    events = []
    for name in c["rated"]:
        for t, v in streams.get(name, []):
            events.append((t, name, v))
    events.sort(key=lambda e: (e[0], e[1]))

    hist = {name: [] for name in c["rated"]}
    run = {name: 0 for name in c["rated"]}
    last_t = {name: None for name in c["rated"]}
    tripped = False

    for name in c["rated"]:
        if not streams.get(name):
            res["faults"].append({"t": None, "channel": name,
                                  "fault": "NO_SAMPLES"})

    for t, name, v in events:
        if tripped:
            break
        fault = None
        if not _is_number(v):
            fault = "NON_FINITE_VALUE"
        elif last_t[name] is not None and t - last_t[name] > max_gap:
            fault = "SAMPLE_GAP %.1fs > %.1fs" % (t - last_t[name], max_gap)
        last_t[name] = t
        if fault:
            res["faults"].append({"t": t, "channel": name, "fault": fault})
            if cfg["on_sensor_fault"] == "TRIP":
                _fire(res, cfg, c, t, name, "SENSOR_FAULT: " + fault)
                tripped = True
            else:
                res["actions"].append({"t": t, "tier": None,
                                       "action": "ALARM",
                                       "reason": "SENSOR_FAULT: " + fault})
            run[name] = 0
            continue

        h = hist[name]
        h.append((t, v))
        while h and h[0][0] < t - window:
            h.pop(0)

        lim = ceiling.get(name)
        if _is_number(lim) and v >= lim:
            _fire(res, cfg, c, t, name, "LEVEL_CEILING %.4g >= %.4g" % (v, lim))
            tripped = True
            continue

        if len(h) < 3 or (h[-1][0] - h[0][0]) < window / 2.0:
            continue                       # [CHOICE 3] skipped, not "below"
        s = slope(h)
        thr = cfg["channels"][name]["rate_threshold"]
        if s is not None and s >= thr:
            run[name] += 1
        else:
            run[name] = 0
        if run[name] >= confirm:
            _fire(res, cfg, c, t, name,
                  "RATE_OF_RISE %.4g >= %.4g %s/s for %d evals"
                  % (s, thr, cfg["channels"][name].get("units", "units"),
                     confirm))
            tripped = True
    return res


def _fire(res, cfg, c, t, name, reason):
    res["detect_t"] = t
    res["detect_channel"] = name
    res["actions"].append({"t": t, "tier": 0, "action": "OPEN_DISCONNECT",
                           "reason": reason + " (latched)"})
    res["actions"].append({"t": t, "tier": 1, "action": "PASSIVE_RECORD",
                           "reason": "no actuation; PCM melt point %s"
                           % (cfg.get("pcm_melt_c", "UNDECLARED"),)})
    if c["tier2_armed"]:
        res["actions"].append({"t": t, "tier": 2,
                               "action": "DISCHARGE_COOLANT",
                               "reason": "armed; space %s"
                               % cfg["tier2_discharge_space"]})
    else:
        res["actions"].append({"t": t, "tier": 2, "action": "TIER2_NOT_ARMED",
                               "reason": c["tier2_reason"]})


# --------------------------------------------------------------------------
# margins (the gating measurement, as arithmetic on bench numbers)
# --------------------------------------------------------------------------

def heat_margin(q_remove_w, q_generate_w):
    """Watts the passive+active tiers remove inside the onset window against
    watts the cell generates there. HOLDS / SHORT / UNMEASURED."""
    if not (_is_number(q_remove_w) and _is_number(q_generate_w)):
        return {"verdict": "UNMEASURED", "ratio": None}
    if q_generate_w <= 0:
        return {"verdict": "UNMEASURED", "ratio": None}
    r = q_remove_w / q_generate_w
    return {"verdict": "HOLDS" if r >= 1.0 else "SHORT", "ratio": r}


def cascade_margin(lead_s, actuation_s, propagation_s):
    """lead_s       : gas detection before first-cell runaway (bench)
    actuation_s  : sensor T90 not already in lead_s + controller + relay
    propagation_s: first-cell runaway to neighbour runaway (bench)

    FIRST_CELL_WINDOW  detection lands before the first cell goes.
    NEIGHBOURS_ONLY    too late for cell 1, still ahead of the neighbours.
    MARGIN_TOO_SHORT   the signal is real but behind both; the remedy is
                       geometry (cell spacing / barriers), not a faster
                       relay. That is itself a result.
    UNMEASURED         any input missing."""
    if not all(_is_number(x) for x in (lead_s, actuation_s, propagation_s)):
        return {"verdict": "UNMEASURED", "slack_s": None}
    first = lead_s - actuation_s
    if first > 0:
        return {"verdict": "FIRST_CELL_WINDOW", "slack_s": first}
    neigh = lead_s + propagation_s - actuation_s
    if neigh > 0:
        return {"verdict": "NEIGHBOURS_ONLY", "slack_s": neigh}
    return {"verdict": "MARGIN_TOO_SHORT", "slack_s": neigh}


def pcm_mass_kg(energy_j, latent_j_per_kg):
    """PCM mass whose latent heat alone absorbs `energy_j`. Ignores sensible
    heat (so it is the conservative side). None if either input absent."""
    if not (_is_number(energy_j) and _is_number(latent_j_per_kg)):
        return None
    if latent_j_per_kg <= 0:
        return None
    return energy_j / latent_j_per_kg


CO2_DENSITY_KG_M3_20C = 1.84     # at 20 C, 1 atm (carried, standard table)


def co2_fraction(co2_kg, space_m3, density=CO2_DENSITY_KG_M3_20C):
    """Well-mixed CO2 volume fraction after releasing `co2_kg` into a space
    of `space_m3` that leaks mixture out as gas comes in:
        f = 1 - exp(-V_gas / V_space).
    A sealed space is worse (pressure rises, nothing leaves). None if an
    input is absent or non-positive."""
    if not (_is_number(co2_kg) and _is_number(space_m3)):
        return None
    if co2_kg < 0 or space_m3 <= 0:
        return None
    return 1.0 - math.exp(-(co2_kg / density) / space_m3)


# --------------------------------------------------------------------------
# synthetic fixtures (CONSTRUCTED -- shapes, not measurements of any cell)
# --------------------------------------------------------------------------

def fx_breathing(seed=1, duration_s=3600, dt=5.0, base=420.0, swing=40.0,
                 period_s=1800.0, noise=3.0):
    """Normal breathing: a baseline with a slow periodic swing (charge cycle,
    temperature) and sensor noise. Max slope of the swing is
    2*pi*swing/period ~ 0.14 units/s at the defaults."""
    rng = random.Random(seed)
    out, t = [], 0.0
    while t <= duration_s:
        v = base + swing * math.sin(2 * math.pi * t / period_s)
        out.append((t, v + rng.gauss(0, noise)))
        t += dt
    return out


def fx_runaway(seed=2, duration_s=3600, dt=5.0, base=420.0, onset_s=1800.0,
               k=0.5, a=1.6, noise=3.0, runaway_s=None):
    """Breathing baseline, then an accelerating off-gas ramp from onset:
    dx/dt = k * x**a in excess-over-baseline units (the runaway glyph read
    early). `runaway_s` is the declared moment the CONSTRUCTED cell goes;
    default onset + 900 s. Returns (samples, runaway_s)."""
    rng = random.Random(seed)
    if runaway_s is None:
        runaway_s = onset_s + 900.0
    out, t, x = [], 0.0, 1.0
    while t <= duration_s:
        v = base + 10.0 * math.sin(2 * math.pi * t / 1800.0)
        if t >= onset_s:
            x = min(x + k * (x ** a) * dt / 60.0, 1e6)
            v += x
        out.append((t, v + rng.gauss(0, noise)))
        t += dt
    return out, runaway_s


def fx_glitch(seed=3, duration_s=1800, dt=5.0, at_s=900.0, height=2000.0):
    """Breathing with a single-sample spike (a bumped sensor, a door draft)."""
    s = fx_breathing(seed=seed, duration_s=duration_s, dt=dt)
    return [(t, v + (height if abs(t - at_s) < dt / 2 else 0.0)) for t, v in s]


def demo_config():
    """CONSTRUCTED config for the fixtures. The threshold here is chosen to
    sit between the fixture's breathing slope (~0.14/s) and its ramp; it is
    NOT a recommended number for any real sensor or cell."""
    return {
        "channels": {"gas": {"rate_threshold": 1.0, "units": "fixture-units"}},
        "window_s": 60, "confirm_count": 3, "max_gap_s": 30,
        "on_sensor_fault": "ALARM",
        "tier2_installed": True, "tier2_discharge_space": "VENTED",
        "pcm_melt_c": "fixture",
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def read_trace(path):
    """CSV lines: t_seconds,channel,value  (header optional)."""
    streams = {}
    with open(path) as fh:
        for line in fh:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) != 3:
                continue
            try:
                t = float(parts[0]); v = float(parts[2])
            except ValueError:
                continue
            streams.setdefault(parts[1], []).append((t, v))
    for k in streams:
        streams[k].sort()
    return streams


def render(res, title):
    out = ["== %s ==" % title, "status   : %s" % res["status"]]
    if res.get("refusal"):
        out.append("refusal  : %s" % res["refusal"])
    if res["unrated"]:
        out.append("unrated  : %s (contribute nothing)" % ", ".join(res["unrated"]))
    out.append("detect   : %s" % ("none" if res["detect_t"] is None else
                                  "t=%.1fs on %s" % (res["detect_t"],
                                                     res["detect_channel"])))
    for a in res["actions"]:
        out.append("  t=%-8.1f tier %-4s %-18s %s" % (
            a["t"], "-" if a["tier"] is None else a["tier"], a["action"],
            a["reason"]))
    for f in res["faults"]:
        out.append("  fault t=%s %s %s" % (f["t"], f["channel"], f["fault"]))
    return "\n".join(out)


def demo():
    cfg = demo_config()
    lines = ["battery-offgas-prearm demo -- CONSTRUCTED fixtures, not data",
             ""]
    lines.append(render(evaluate(cfg, {"gas": fx_breathing()}), "breathing"))
    ramp, runaway_s = fx_runaway()
    r = evaluate(cfg, {"gas": ramp})
    lines += ["", render(r, "runaway ramp (constructed runaway at t=%.0fs)"
                         % runaway_s)]
    if r["detect_t"] is not None:
        lines.append("lead     : %.1fs before the constructed runaway"
                     % (runaway_s - r["detect_t"]))
    lines += ["", render(evaluate(cfg, {"gas": fx_glitch()}), "single glitch")]
    unr = dict(cfg); unr["channels"] = {"gas": {"rate_threshold": None}}
    lines += ["", render(evaluate(unr, {"gas": ramp}), "no threshold declared")]
    lines += ["", "co2: 1 kg into a 2 m3 closet -> %.0f%% by volume "
              "(NIOSH IDLH is 4%%)" % (100 * co2_fraction(1.0, 2.0))]
    lines += ["", "\n".join(CHOICES)]
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "prearm is a library and a CLI; the checks live in "
            "battery-offgas-prearm/test_prearm.py -- run "
            "python3 battery-offgas-prearm/test_prearm.py\n")
        return 2
    if "--choices" in argv:
        print("\n".join(CHOICES))
        return 0
    if "--demo" in argv or not argv:
        print(demo())
        return 0
    if "--config" in argv and "--trace" in argv:
        with open(argv[argv.index("--config") + 1]) as fh:
            cfg = json.load(fh)
        res = evaluate(cfg, read_trace(argv[argv.index("--trace") + 1]))
        print(render(res, "trace"))
        return 0 if res["status"] != UNRATED else 3
    sys.stderr.write(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
