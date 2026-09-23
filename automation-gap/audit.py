#!/usr/bin/env python3
# audit.py -- recompute what the five delivered documents state.
# CC0, stdlib only, no network. Parses the delivered files at call time;
# no figure from them is retyped as a literal here (asserted by the suite).
#
# WHAT THIS DOES
#     The drop carries a results matrix, a distribution table, a per-truck
#     input ledger and a set of findings. Each of those is arithmetic over
#     numbers the documents themselves supply. This recomputes them.
#
# WHAT IT DOES NOT DO
#     It checks no claim about the world. Every figure in the drop is
#     CARRIED -- sourced to reporting this environment cannot reach (the
#     egress gate refuses every publisher host) -- and nothing here is
#     evidence for or against mining haulage, humanoid robots, container
#     terminals or any vendor. It checks whether the documents agree with
#     themselves.
#
# usage:
#     python3 audit.py              the findings
#     python3 audit.py --json
#     python3 audit.py --selftest

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _import(relpath, name):
    """Import a module whose folder name is not an identifier."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, relpath))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Shipped precision. IMPORTED, not reimplemented: the repository already
# carries this helper and it is registered in tools/known_answer.py. A second
# copy is the drift this tree has a checker for.
_MS = _import("move-set/move_set_sim_v2.py", "_ms_v2")
halfwidth = _MS._halfwidth
DOC = {
    "gap":     "AUTOMATION_GAP_AUDIT.md",
    "corpus":  "DEMO_CORPUS_AUDIT.md",
    "komatsu": "KOMATSU_AHS_INPUT_SCAFFOLD.md",
    "field":   "FIELD_LAYER_ZERO_BURDEN_SPEC.md",
    "ledger":  "FIELD_LEDGER_001.md",
}
# Records the drop's own vocabulary treats as humanoid, declared here because
# no delivered field carries a form factor. A reader may disagree with a row;
# the finding below is reported per row so a disagreement is locatable.
HUMANOID = ("Optimus", "Figure", "Digit", "Apollo", "Atlas", "NEO",
            "Humanoid Games")
CHECK_ORDER = ("teleop", "metrics", "variation", "envelope",
               "independent", "sustained")


def text(key):
    return open(os.path.join(HERE, DOC[key]), encoding="utf-8").read()


def _rows(md, header_word):
    """Pipe-table rows under the first header containing header_word."""
    out, on = [], False
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|") and header_word in s:
            on = True
            continue
        if on:
            if not s.startswith("|"):
                break
            if set(s) <= set("|- :"):
                continue
            out.append([c.strip() for c in s.strip("|").split("|")])
    return out


def _cell(c):
    """A matrix cell's verdict, with markdown emphasis stripped."""
    return re.sub(r"[*`]", "", c).strip().upper()


# ---------------------------------------------------------------- corpus

def matrix():
    rows = _rows(text("corpus"), "Demo / deployment")
    return [(r[0], [_cell(x) for x in r[1:7]]) for r in rows if len(r) >= 7]


def stated_distribution():
    """The distribution table as the document prints it."""
    out = {}
    for r in _rows(text("corpus"), "| Check |"):
        if len(r) < 5:
            continue
        name = re.sub(r"[*`]", "", r[0]).strip().lower()
        vals = []
        for c in r[1:5]:
            c = c.strip()
            vals.append(0 if c in ("—", "-", "") else int(c))
        out[name] = dict(zip(("PASS", "PARTIAL", "FAIL", "ABSENT"), vals))
    return out


def recomputed_distribution():
    m = matrix()
    out = {}
    for i, key in enumerate(CHECK_ORDER):
        d = {"PASS": 0, "PARTIAL": 0, "FAIL": 0, "ABSENT": 0}
        for _, cells in m:
            v = cells[i]
            if v in d:
                d[v] += 1
        out[key] = d
    return out


def distribution_agrees():
    """Recomputed vs stated, matched by row ORDER (the stated rows carry
    prose labels, not the matrix's column keys)."""
    stated = list(stated_distribution().items())
    recomp = list(recomputed_distribution().items())
    rows, ok = [], True
    for (sname, sv), (rname, rv) in zip(stated, recomp):
        agree = sv == rv
        ok = ok and agree
        rows.append({"stated_label": sname, "column": rname,
                     "stated": sv, "recomputed": rv, "agrees": agree,
                     "row_total": sum(rv.values())})
    return {"all_agree": ok and len(stated) == len(recomp), "rows": rows,
            "n_records": len(matrix())}


def perfect_records():
    return [n for n, c in matrix() if all(v == "PASS" for v in c)]


def humanoid_failure_counts():
    """F1 states every humanoid record fails at least three checks.
    A 'failure' here is any cell that is not PASS -- the reading most
    favourable to the claim, since PARTIAL and ABSENT both count."""
    out = []
    for name, cells in matrix():
        if any(h.lower() in name.lower() for h in HUMANOID):
            n = len([v for v in cells if v != "PASS"])
            out.append({"record": name, "non_pass": n,
                        "cells": dict(zip(CHECK_ORDER, cells))})
    return sorted(out, key=lambda r: r["non_pass"])


def f1_at_least_three():
    rows = humanoid_failure_counts()
    under = [r for r in rows if r["non_pass"] < 3]
    return {"claim": "every humanoid record fails at least three",
            "holds": not under, "n_humanoid": len(rows),
            "counterexamples": under}


def deployment_class_independence():
    """F2: metric-carrying deployment class, independent evaluation 0 of 4."""
    m = dict(matrix())
    named = [n for n in m
             if any(k in n for k in ("Figure 02", "Digit", "Aurora", "Stretch"))]
    ind = {n: m[n][CHECK_ORDER.index("independent")] for n in named}
    var = {n: m[n][CHECK_ORDER.index("variation")] for n in named}
    return {"records": named,
            "independent_pass": len([v for v in ind.values() if v == "PASS"]),
            "variation_pass": len([v for v in var.values() if v == "PASS"]),
            "independent": ind, "variation": var}


# ---------------------------------------------------------------- komatsu

NUM = r"([0-9][0-9,]*(?:\.[0-9]+)?)"


def _f(s):
    return float(s.replace(",", ""))


def komatsu_numbers():
    t = text("komatsu")
    g = {}
    g["_raw"] = {}
    m = re.search(r"Usable hours/yr \| " + NUM + r" \| " + NUM, t)
    g["hours_manned"], g["hours_ahs"] = _f(m.group(1)), _f(m.group(2))
    g["_raw"]["hours_manned"], g["_raw"]["hours_ahs"] = m.group(1), m.group(2)
    m = re.search(r"hours/truck \| ~" + NUM + r".*?\| ~" + NUM, t)
    g["humanhours_manned"], g["humanhours_ahs"] = _f(m.group(1)), _f(m.group(2))
    m = re.search(r"Mean speed \| 1\.00. \| " + NUM, t)
    g["speed_ahs"] = _f(m.group(1)); g["_raw"]["speed_ahs"] = m.group(1)
    m = re.search(r"Throughput/truck-year \| 1\.00. \| ~" + NUM, t)
    g["throughput_ahs"] = _f(m.group(1)); g["_raw"]["throughput_ahs"] = m.group(1)
    m = re.search(r"unit throughput\*\* \| \*\*" + NUM + r"\*\* \| \*\*" + NUM, t)
    g["hpu_manned"], g["hpu_ahs"] = _f(m.group(1)), _f(m.group(2))
    g["_raw"]["hpu_manned"], g["_raw"]["hpu_ahs"] = m.group(1), m.group(2)
    m = re.search(r"unit throughput\*\* \|.*?\(.(\d+)%\)", t)
    g["hpu_drop_pct"] = _f(m.group(1)); g["_raw"]["hpu_drop_pct"] = m.group(1)
    m = re.search(r"Tire & brake consumption \| 1\.00. \| " + NUM + r". \(\+" + NUM + r"% life\)", t)
    g["tire_factor"], g["tire_life_gain_pct"] = _f(m.group(1)), _f(m.group(2))
    g["_raw"]["tire_factor"] = m.group(1)
    m = re.search(r"tire replacement at " + NUM + r"\s*[–—-]\s*" + NUM + r" h vs " + NUM + r" h", t)
    g["tire_lo"], g["tire_hi"], g["tire_base"] = (_f(m.group(1)), _f(m.group(2)),
                                                  _f(m.group(3)))
    m = re.search(r"\(\+" + NUM + r"%\)\s*\| Whittle", t)
    g["hours_gain_pct"] = _f(m.group(1)) if m else None
    g["_raw"]["hours_gain_pct"] = m.group(1) if m else None
    return g


def komatsu_arithmetic():
    """Every derived cell the ledger marks CONSTRUCTED, recomputed from the
    cells it derives from."""
    g = komatsu_numbers()
    raw = g["_raw"]
    out = []

    def row(name, key, computed, note=""):
        stated = g[key]
        hw = halfwidth(raw.get(key))
        ok = (stated is not None and hw is not None
              and abs(stated - computed) <= float(hw))
        out.append({"quantity": name, "stated": stated,
                    "as_written": raw.get(key), "halfwidth": float(hw) if hw else None,
                    "recomputed": round(computed, 4), "agrees": ok,
                    "note": note})

    row("hours gain %", "hours_gain_pct",
        (g["hours_ahs"] / g["hours_manned"] - 1) * 100,
        "usable-hours delta")
    row("throughput AHS", "throughput_ahs",
        (g["hours_ahs"] / g["hours_manned"]) * g["speed_ahs"],
        "hours x speed")
    row("human hours per unit, manned", "hpu_manned",
        g["humanhours_manned"] / g["hours_manned"],
        "human hours / (usable hours x 1.00)")
    row("human hours per unit, AHS", "hpu_ahs",
        g["humanhours_ahs"] / (g["hours_manned"] * g["throughput_ahs"]),
        "human hours / (manned hours x throughput factor)")
    row("drop %", "hpu_drop_pct",
        (g["hpu_manned"] - g["hpu_ahs"]) / g["hpu_manned"] * 100,
        "from the two stated per-unit figures")
    row("tire factor", "tire_factor",
        1.0 / (1.0 + g["tire_life_gain_pct"] / 100.0),
        "1 / (1 + life gain)")
    return {"all_agree": all(r["agrees"] for r in out), "rows": out,
            "inputs": g}


def tire_range():
    """The +40% life figure against the replacement-hours range it cites."""
    g = komatsu_numbers()
    raw_gain = re.search(r"\(\+([0-9.]+)% life\)", text("komatsu")).group(1)
    lo = (g["tire_lo"] / g["tire_base"] - 1) * 100
    hi = (g["tire_hi"] / g["tire_base"] - 1) * 100
    mid = ((g["tire_lo"] + g["tire_hi"]) / 2 / g["tire_base"] - 1) * 100
    return {"stated_gain_pct": g["tire_life_gain_pct"],
            "range_from_hours_pct": [round(lo, 1), round(hi, 1)],
            "midpoint_pct": round(mid, 1),
            "stated_is_top_of_range": abs(g["tire_life_gain_pct"] - hi)
                                      <= float(halfwidth(raw_gain)),
            "factor_at_stated": round(1 / (1 + g["tire_life_gain_pct"] / 100), 3),
            "factor_at_midpoint": round(1 / (1 + mid / 100), 3)}


# ---------------------------------------------------------------- ledger

def ledger_entries():
    t = text("ledger")
    ids = re.findall(r"^## ENTR(?:Y|IES) ([0-9+ ]+)", t, re.M)
    records = [i.strip() for i in ids]
    return {"headed_entries": records, "n_records": len(records)}


def parked_strike_share():
    """The drop states parked-strike discovery is 2 of 6 entries."""
    t = text("ledger")
    m = re.search(r"parked-strike discovery is now (\d+) of (\d+) entries", t)
    e = ledger_entries()
    return {"stated": [int(m.group(1)), int(m.group(2))] if m else None,
            "headed_entry_records": e["n_records"],
            "headings": e["headed_entries"],
            "denominator_agrees": bool(m) and int(m.group(2)) == e["n_records"]}


# ---------------------------------------------------------------- dates

def doc_dates():
    out = {}
    for k in DOC:
        ds = sorted(set(re.findall(r"20\d\d-\d\d-\d\d", text(k))))
        out[k] = {"dates": ds, "max": ds[-1] if ds else None}
    return out


# ---------------------------------------------------------------- report

def findings():
    return {
        "AGA_001_distribution": distribution_agrees(),
        "AGA_002_perfect_records": perfect_records(),
        "AGA_003_f1_at_least_three": f1_at_least_three(),
        "AGA_004_deployment_class": deployment_class_independence(),
        "AGA_005_komatsu_arithmetic": komatsu_arithmetic(),
        "AGA_006_tire_range": tire_range(),
        "AGA_007_ledger_share": parked_strike_share(),
        "AGA_008_dates": doc_dates(),
    }


def render(f):
    print("AUTOMATION-GAP DROP -- internal recomputation")
    print("Every figure in the drop is CARRIED. Nothing below is evidence")
    print("about the world; it is whether the documents agree with themselves.\n")

    d = f["AGA_001_distribution"]
    print("AGA_001  distribution table vs the matrix (%d records)" % d["n_records"])
    for r in d["rows"]:
        print("    %-26s %-12s %s   total %d"
              % (r["stated_label"][:26], r["column"],
                 "agrees" if r["agrees"] else "DISAGREES", r["row_total"]))
    print("    -> all six columns reconcile: %s\n" % d["all_agree"])

    print("AGA_002  records passing all six: %s\n"
          % (", ".join(f["AGA_002_perfect_records"]) or "none"))

    t = f["AGA_003_f1_at_least_three"]
    print("AGA_003  F1: %s" % t["claim"])
    print("    humanoid records read: %d" % t["n_humanoid"])
    if t["holds"]:
        print("    -> HOLDS\n")
    else:
        print("    -> DOES NOT HOLD. Records failing fewer than three:")
        for c in t["counterexamples"]:
            print("       %-36s %d non-PASS" % (c["record"], c["non_pass"]))
        print()

    dc = f["AGA_004_deployment_class"]
    print("AGA_004  F2 deployment class (%d records)" % len(dc["records"]))
    print("    independent PASS: %d    variation PASS: %d"
          % (dc["independent_pass"], dc["variation_pass"]))
    print("    (both are PASS-counts; ABSENT is not a measured negative)\n")

    k = f["AGA_005_komatsu_arithmetic"]
    print("AGA_005  Komatsu ledger, derived cells recomputed")
    for r in k["rows"]:
        print("    %-32s stated %-8s recomputed %-9s %s"
              % (r["quantity"], r["stated"], r["recomputed"],
                 "agrees" if r["agrees"] else "DISAGREES"))
    print("    -> ledger is internally consistent: %s\n" % k["all_agree"])

    tr = f["AGA_006_tire_range"]
    print("AGA_006  tire life: stated +%g%%, range from its own hours %s, "
          "midpoint +%g%%" % (tr["stated_gain_pct"],
                              tr["range_from_hours_pct"], tr["midpoint_pct"]))
    print("    stated figure is the top of that range: %s"
          % tr["stated_is_top_of_range"])
    print("    consumption factor  at stated %.3f   at midpoint %.3f\n"
          % (tr["factor_at_stated"], tr["factor_at_midpoint"]))

    ls = f["AGA_007_ledger_share"]
    print("AGA_007  field ledger: stated %s; headed entry records %d %s"
          % (ls["stated"], ls["headed_entry_records"],
             "(denominator agrees)" if ls["denominator_agrees"] else "(DISAGREES)"))
    print("    headings: %s\n" % ", ".join(ls["headings"]))

    print("AGA_008  self-dates per document")
    for k2, v in sorted(f["AGA_008_dates"].items()):
        print("    %-9s latest %s" % (k2, v["max"]))
    print()


def main(argv):
    if "--selftest" in argv[1:]:
        import test_audit
        return test_audit.main()
    f = findings()
    print(json.dumps(f, indent=2)) if "--json" in argv[1:] else render(f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
