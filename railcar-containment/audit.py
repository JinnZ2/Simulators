#!/usr/bin/env python3
"""Reads the delivered folder against its own README, CLAIMS.md and
scripts. Imports the delivered modules and edits nothing; every number
in CLAIM_TABLE.md is computed here. Nothing here is a statement about
any real car, device, line or report.

    python3 audit.py
Refuses --selftest (checks live in selftest_rail.py).
"""

import ast
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "envelope-asymmetry"))
import tenability as T  # noqa: E402
import t_hold as H  # noqa: E402
import detection_loop as D  # noqa: E402
import envelope_score as ES  # noqa: E402

PARAMS = os.path.join(HERE, "params", "example_lines.json")
DELIVERED = ["README.md", "CLAIMS.md", "tenability.py", "t_hold.py", "detection_loop.py", "run_all.py",
             "params/example_lines.json"]


def _coef():
    if not hasattr(_coef, "c"):
        _coef.c = T.calibrate(T.ASSUMPTIONS)
    return _coef.c


def anchor():
    """The calibrated model at its own anchor: each channel lands on its
    anchor by construction; the folder's t_available is their minimum."""
    a = T.ASSUMPTIONS
    r = T.simulate(a["V_intercity_m3"], 1.0, _coef(), a)
    lo, hi = T.ANCHOR_WINDOW_S
    return {"channels": {k: r[v] for k, v in T._KEY.items()}, "t_available": r["t_available_s"],
            "binding_channel": min(T._KEY, key=lambda k: r[T._KEY[k]] if r[T._KEY[k]] is not None else 1e9),
            "inside_window": lo <= r["t_available_s"] <= hi, "anchor_residuals": {k: r[T._KEY[k]] - T.ANCHORS_S[k] for k in T._KEY}}


def volume_scaling(volumes=(60, 80, 100, 120, 160, 200, 240, 320)):
    """Per-channel crossing time against volume, and the local exponent
    d ln t / d ln V for each channel and for the minimum."""
    a = T.ASSUMPTIONS
    rows = {}
    for V in volumes:
        r = T.simulate(float(V), 1.0, _coef(), a)
        rows[V] = {k: r[v] for k, v in T._KEY.items()}
        rows[V]["min"] = r["t_available_s"]
    import math
    expo = {}
    for k in list(T._KEY) + ["min"]:
        pairs = [(V, rows[V][k]) for V in volumes if rows[V][k] is not None]
        ex = []
        for (v1, t1), (v2, t2) in zip(pairs, pairs[1:]):
            ex.append(math.log(t2 / t1) / math.log(v2 / v1))
        expo[k] = (min(ex), max(ex)) if ex else None
    mono = all(rows[v1]["min"] <= rows[v2]["min"] for v1, v2 in zip(volumes, volumes[1:])
               if rows[v1]["min"] is not None and rows[v2]["min"] is not None)
    binding = {V: min(T._KEY, key=lambda k: rows[V][k] if rows[V][k] is not None else 1e9) for V in volumes}
    return {"rows": rows, "exponent_range": expo, "monotone_in_volume": mono, "binding": binding,
            "subway_over_intercity": rows[100]["min"] / rows[160]["min"]}


def containment_form(fracs=(1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.1, 0.05)):
    """tenability.py's t_available against contained fraction at intercity
    volume, beside the linear stretch detection_loop.py applies
    (budget / fraction). The two screens disagree on the functional form."""
    a = T.ASSUMPTIONS
    base = T.simulate(a["V_intercity_m3"], 1.0, _coef(), a)["t_available_s"]
    out = {}
    for f in fracs:
        t = T.simulate(a["V_intercity_m3"], f, _coef(), a)["t_available_s"]
        out[f] = {"tenability": t, "detection_loop_stretch": base / max(f, 1e-3),
                  "ratio_tenability_over_stretch": (t / (base / f)) if t is not None else None}
    never = [f for f in fracs if out[f]["tenability"] is None]
    return {"base": base, "rows": out, "never_crossed_at": never,
            "source_total_s": a["vent_rise_s"] + a["vent_peak_s"] + a["vent_decay_s"]}


def volume_vs_containment():
    """RC_002: the volume effect (100 vs 160 m3) against the containment
    effect (1.0 -> 0.5, the largest fraction step before 'never')."""
    a = T.ASSUMPTIONS
    t160 = T.simulate(160.0, 1.0, _coef(), a)["t_available_s"]
    t100 = T.simulate(100.0, 1.0, _coef(), a)["t_available_s"]
    t160_half = T.simulate(160.0, 0.5, _coef(), a)["t_available_s"]
    t160_fifth = T.simulate(160.0, 0.2, _coef(), a)["t_available_s"]
    return {"volume_ratio_100_over_160": t100 / t160, "containment_ratio_half": (t160_half / t160) if t160_half else None,
            "containment_at_0_2": t160_fifth}


def hold_requirements():
    with open(PARAMS) as fh:
        cfg = json.load(fh)
    lat = cfg["latencies"]
    out = {}
    for line in cfg["lines"]:
        out[line["name"]] = {"%s_%s" % (m, p): H.required_hold(line, lat, m, p)["t_hold_required_s"]
                             for m in ("sensor", "visual") for p in ("run", "stop")}
    src = open(os.path.join(HERE, "t_hold.py"), encoding="utf-8").read()
    return {"lines": out, "offgas_key_read_by_t_hold": "offgas_to_flame_s" in src,
            "default_margin": 1.5 if "default=1.5" in src else None,
            "clear_dominates_worst": {n: (H.required_hold(l, lat, "visual", "stop")["clear_s"]
                                          / H.required_hold(l, lat, "visual", "stop")["t_hold_required_s"])
                                      for n, l in ((l["name"], l) for l in cfg["lines"])}}


def detection_by_egress(trials=4000, seed=1):
    """RC_005 as a function of the egress-action mean: where detection
    stops mattering is set by egress time against the budget."""
    out = {}
    for mean in (120, 240, 360, 480, 600, 900):
        p = dict(D.DEFAULTS, egress_action_mean_s=float(mean), egress_action_sd_s=0.375 * mean)
        v = D.run_arm("visual", trials, 1.0, p, seed)["p_cleared"]
        s = D.run_arm("sensor", trials, 1.0, p, seed)["p_cleared"]
        c = D.run_arm("visual", trials, 0.2, p, seed)["p_cleared"]
        out[mean] = {"visual": v, "sensor": s, "visual_contained_0_2": c, "detection_gain": s - v, "containment_gain": c - v}
    return out


def shift_arithmetic():
    """The sensor arm's gain in the model is one number: the mean lead
    (offgas-to-flame + visual latency - sensor latency)."""
    p = D.DEFAULTS
    return {"mean_lead_s": p["offgas_to_flame_mean_s"] + p["visual_detect_mean_s"] - p["sensor_detect_mean_s"],
            "tunnel_egress_mean_s": 900.0, "budget_mean_s": p["t_available_mean_s"],
            "tunnel_deficit_before_detection_s": 900.0 + p["crew_decide_mean_s"] + p["visual_detect_mean_s"] - p["t_available_mean_s"]}


def envelope_of_readme():
    """The README's envelope block scored with the sibling instrument, as
    a declared coding of one document. E5 asks for a number and the block
    says 'none applied'; E6 names no party."""
    text = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    row = {"doc_id": "railcar-containment/README.md", "arm": "A", "vendor": "n/a", "host_domain": "rail transit",
           "doc_type": "sim README", "doc_words": len(text.split()), "E1": 1, "E2": 1, "E3": 1, "E4": 1, "E5": 0, "E6": 0,
           "envelope_score": 4, "structural_absence": False, "coder": "audit.py (declared reading)"}
    return {"row": row, "valid": ES.validate_rows([row]) == [],
            "margin_in_readme": "none applied" in text, "margin_in_t_hold": hold_requirements()["default_margin"]}


def claims_vs_scripts():
    """What CLAIMS.md attributes to a script, checked against the script."""
    return {
        "RC_001_sign_structural": volume_scaling()["monotone_in_volume"],
        "RC_002_dominates": volume_vs_containment(),
        "RC_005_tunnel": shift_arithmetic(),
    }


def constraints():
    out = {}
    for f in ("tenability.py", "t_hold.py", "detection_loop.py", "run_all.py"):
        src = open(os.path.join(HERE, f), encoding="utf-8").read()
        tree = ast.parse(src)
        mods = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                mods.update(x.name.split(".")[0] for x in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module:
                mods.add(n.module.split(".")[0])
        std = getattr(sys, "stdlib_module_names", None)
        unused = [m for m in mods if src.count(m + ".") == 0 and m not in ("sys", "os")]
        out[f] = {"imports": sorted(mods), "non_stdlib": sorted(m for m in mods if std and m not in std),
                  "imported_unused": unused, "lines": src.count("\n")}
    return out


def render():
    L = ["railcar-containment audit"]
    L.append("delivered files present: %s" % all(os.path.exists(os.path.join(HERE, f)) for f in DELIVERED))
    for f, c in constraints().items():
        L.append("  %-18s imports %s non_stdlib %s unused %s lines %d" % (f, c["imports"], c["non_stdlib"], c["imported_unused"], c["lines"]))
    an = anchor()
    L.append("anchor: channels %s, t_available %s, binding %s, inside window %s, anchor residuals %s" % (
        an["channels"], an["t_available"], an["binding_channel"], an["inside_window"], an["anchor_residuals"]))
    vs = volume_scaling()
    L.append("volume scaling: exponent range per channel %s; monotone %s; subway/intercity %.3f; binding by volume %s" % (
        {k: (round(v[0], 2), round(v[1], 2)) if v else None for k, v in vs["exponent_range"].items()}, vs["monotone_in_volume"],
        vs["subway_over_intercity"], vs["binding"]))
    cf = containment_form()
    L.append("containment form at 160 m3 (base %.1f s, source ends at %.0f s):" % (cf["base"], cf["source_total_s"]))
    for f, r in cf["rows"].items():
        L.append("  f %.2f  tenability %-8s  linear stretch %8.1f  ratio %s" % (
            f, ("%.1f" % r["tenability"]) if r["tenability"] is not None else "never", r["detection_loop_stretch"],
            ("%.2f" % r["ratio_tenability_over_stretch"]) if r["ratio_tenability_over_stretch"] is not None else "undefined"))
    L.append("never crossed at fractions %s" % cf["never_crossed_at"])
    L.append("RC_002 arithmetic: %s" % volume_vs_containment())
    hr = hold_requirements()
    L.append("t_hold (no margin): %s" % hr["lines"])
    L.append("t_hold reads offgas_to_flame_s: %s; default margin %s; clear share of visual/STOP %s" % (
        hr["offgas_key_read_by_t_hold"], hr["default_margin"], {k: round(v, 2) for k, v in hr["clear_dominates_worst"].items()}))
    L.append("detection gain against egress mean (P(clear), 4000 trials):")
    for m, r in detection_by_egress().items():
        L.append("  egress %4d s  visual %.3f  sensor %.3f  contained 0.2 %.3f  detection gain %+.3f  containment gain %+.3f" % (
            m, r["visual"], r["sensor"], r["visual_contained_0_2"], r["detection_gain"], r["containment_gain"]))
    L.append("shift arithmetic: %s" % shift_arithmetic())
    er = envelope_of_readme()
    L.append("README envelope scored with envelope-asymmetry: E1..E6 = %s, score %d, valid %s; margin 'none applied' in README %s, t_hold default margin %s" % (
        [er["row"][m] for m in ES.MARKERS], er["row"]["envelope_score"], er["valid"], er["margin_in_readme"], er["margin_in_t_hold"]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("audit has no selftest; run selftest_rail.py", file=sys.stderr)
        sys.exit(2)
    print(render())
