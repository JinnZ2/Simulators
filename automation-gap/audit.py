#!/usr/bin/env python3
# audit.py -- recompute what the six delivered documents state.
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
    "seed":    "FIELD_LAYER_SEED_ROADS.md",
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


# ---------------------------------------------------------------- seed roads
#
# FIELD_LAYER_SEED_ROADS arrived one drop after the other five and is WP1 and
# WP2 -- two of the four objects AGA_009 recorded as named-and-absent. The
# checks below are the same shape as the rest: arithmetic over figures the
# document itself supplies, plus two citations it makes into its siblings.

DASH = "[–—-]"
TIMES = "×"


def _seed_table_rows():
    """Every pipe-table data row in the seed, as cell lists."""
    out = []
    for line in text("seed").splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= set("|- :"):
            continue
        out.append([c.strip() for c in s.strip("|").split("|")])
    return out


def seed_tire_ratio():
    """'gravel ~= 2.5-3.7x paved' against the three cent-per-mile figures
    printed in the same cell."""
    t = text("seed")
    m = re.search(r"concrete ([0-9.]+).*?asphalt ([0-9.]+).*?gravel ([0-9.]+)"
                  r".*?\*\*([0-9.]+)" + DASH + r"([0-9.]+)", t)
    if not m:
        return {"parsed": False}
    conc, asph, grav = _f(m.group(1)), _f(m.group(2)), _f(m.group(3))
    lo_s, hi_s = m.group(4), m.group(5)
    lo_c, hi_c = grav / asph, grav / conc
    hw_lo, hw_hi = halfwidth(lo_s), halfwidth(hi_s)
    return {"parsed": True,
            "cents": {"concrete": conc, "asphalt": asph, "gravel": grav},
            "stated": [_f(lo_s), _f(hi_s)],
            "as_written": [lo_s, hi_s],
            "recomputed": [round(lo_c, 4), round(hi_c, 4)],
            "halfwidth": [float(hw_lo), float(hw_hi)],
            "lo_agrees": abs(lo_c - _f(lo_s)) <= float(hw_lo),
            "hi_agrees": abs(hi_c - _f(hi_s)) <= float(hw_hi),
            "note": "lo = gravel/asphalt, hi = gravel/concrete -- the two "
                    "surfaces the cell calls paved"}


def seed_cost_vs_frequency():
    """The maintenance-frequency row and the county-expenditure row sit two
    lines apart in one table and do not scale together."""
    t = text("seed")
    fq = re.search(r"~([0-9.]+)" + TIMES + r" paved", t)
    mn = re.search(r"gravel \$([0-9,]+)/mi/yr vs paved \$([0-9.]+)/mi/yr", t)
    if not (fq and mn):
        return {"parsed": False}
    freq = _f(fq.group(1))
    g, p = _f(mn.group(1)), _f(mn.group(2))
    cost = g / p
    return {"parsed": True,
            "frequency_ratio_stated": freq,
            "expenditure": {"gravel": g, "paved": p},
            "expenditure_ratio": round(cost, 1),
            "factor_between_them": round(cost / freq, 1),
            "same_quantity": False,
            "note": "frequency and expenditure are different quantities, so "
                    "this is a tension and not a contradiction. What it needs "
                    "is the county's own units on $13.45/mi/yr; nothing here "
                    "adjudicates either figure."}


def seed_rainfall_and_restatement():
    """THE COLLISION restates three WP1 figures. Each is checked against the
    row it restates -- the containment check, not a new measurement."""
    t = text("seed")
    rows = {}
    m = re.search(r"\+([0-9,]+)" + DASH + r"([0-9,]+) mm/km", t)
    rows["rainfall_row"] = [_f(m.group(1)), _f(m.group(2))] if m else None
    m = re.search(r"~([0-9,]+) mm/km per metre of rain", t)
    rows["rainfall_restated"] = _f(m.group(1)) if m else None
    m = re.search(r"([0-9.]+)" + DASH + r"([0-9.]+)" + TIMES + r" tire cost", t)
    rows["tire_restated"] = [_f(m.group(1)), _f(m.group(2))] if m else None
    m = re.search(r"([0-9.]+)" + TIMES + r"\s+maintenance\s+frequency", t)
    rows["freq_restated"] = _f(m.group(1)) if m else None
    tr = seed_tire_ratio()
    fq = seed_cost_vs_frequency()
    checks = []
    if rows["rainfall_row"] and rows["rainfall_restated"] is not None:
        lo, hi = rows["rainfall_row"]
        checks.append({"figure": "rainfall roughness",
                       "restated": rows["rainfall_restated"],
                       "source_row": [lo, hi],
                       "contained": lo <= rows["rainfall_restated"] <= hi})
    if rows["tire_restated"] and tr.get("parsed"):
        checks.append({"figure": "tire cost ratio",
                       "restated": rows["tire_restated"],
                       "source_row": tr["stated"],
                       "contained": rows["tire_restated"] == tr["stated"]})
    if rows["freq_restated"] is not None and fq.get("parsed"):
        checks.append({"figure": "maintenance frequency",
                       "restated": rows["freq_restated"],
                       "source_row": [fq["frequency_ratio_stated"]],
                       "contained": rows["freq_restated"]
                                    == fq["frequency_ratio_stated"]})
    return {"checks": checks,
            "all_contained": bool(checks) and all(c["contained"] for c in checks)}


def seed_provenance_vocabulary():
    """Labels the seed declares in its own header, against labels its tables
    use. A label in use and not declared is the finding."""
    t = text("seed")
    m = re.search(r"Provenance labels:\s*(.+)", t)
    declared = []
    if m:
        s = re.sub(r"\([^)]*\)", " ", m.group(1))
        for part in s.split("/"):
            w = part.strip().strip(".").strip()
            if w and w == w.upper() and re.match(r"^[A-Z][A-Z -]*$", w):
                declared.append(w)
    used = {}
    for cells in _seed_table_rows():
        if not cells:
            continue
        last = cells[-1]
        lm = re.match(r"([A-Z][A-Z \-/]*[A-Z])", last)
        if not lm:
            continue
        for lab in lm.group(1).split("/"):
            lab = lab.strip()
            if lab:
                used[lab] = used.get(lab, 0) + 1
    undeclared = sorted(k for k in used if k not in declared)
    return {"declared": declared,
            "used": dict(sorted(used.items())),
            "undeclared": undeclared,
            "undeclared_rows": sum(used[k] for k in undeclared),
            "note": "the nearest declared member for an industry-stated "
                    "requirement is VENDOR, and the section's own framing "
                    "turns on it not being one"}


def seed_crosscites():
    """The two citations the seed makes into its sibling documents."""
    out = []

    # 1. "(from the Komatsu scaffold, V2.1)" -- is the figure in that section?
    k = text("komatsu").splitlines()
    start = next((i for i, l in enumerate(k)
                  if l.startswith("###") and "V2.1" in l), None)
    end = len(k)
    if start is not None:
        for i in range(start + 1, len(k)):
            if k[i].startswith("###"):
                end = i
                break
    span = "\n".join(k[start:end]) if start is not None else ""
    seed_fig = re.search(r"2 weeks ungraded corrugation .{0,6} ([0-9]" + DASH
                         + r"[0-9]+)% fleet tire life", text("seed"))
    komatsu_fig = re.search(r"two weeks of un-graded corrugation costs ([0-9]"
                            + DASH + r"[0-9]+)% of fleet tire life", span)
    out.append({"cite": "Komatsu scaffold, V2.1",
                "seed_figure": seed_fig.group(1) if seed_fig else None,
                "found_in_cited_section": bool(komatsu_fig),
                "cited_section_figure": komatsu_fig.group(1) if komatsu_fig else None,
                "resolves": bool(seed_fig and komatsu_fig
                                 and seed_fig.group(1) == komatsu_fig.group(1))})

    # 2. "MEASURED (from demo-corpus audit)" on the Aurora row.
    terms = ("observer", "roadside", "pull")
    counts = {}
    for key in ("corpus", "gap"):
        body = text(key).lower()
        counts[key] = {w: body.count(w) for w in terms}
    cited = sum(counts["corpus"].values())
    elsewhere = sum(counts["gap"].values())
    out.append({"cite": "demo-corpus audit (Aurora emergency procedures row)",
                "terms": list(terms),
                "hits_in_cited_document": counts["corpus"],
                "hits_in_gap_audit": counts["gap"],
                "resolves": cited > 0,
                "supporting_document": "gap" if elsewhere and not cited else None,
                "note": "a term list, so a paraphrase steps around it; the "
                        "counts are printed so a reader can check the call"})
    return {"cites": out, "all_resolve": all(c["resolves"] for c in out)}


def seed_survey_denominator():
    """'18 companies, 90% response' and 'top ask, 12/18 companies' -- only one
    reading of 18 is arithmetically possible."""
    t = text("seed")
    m = re.search(r"\(2021, ([0-9]+) companies, ([0-9]+)% response\)", t)
    a = re.search(r"top ask, ([0-9]+)/([0-9]+) companies", t)
    if not (m and a):
        return {"parsed": False}
    n, rate = _f(m.group(1)), _f(m.group(2)) / 100.0
    as_surveyed = n * rate          # respondents if 18 were surveyed
    as_responded = n / rate         # population if 18 responded
    return {"parsed": True,
            "n": n, "response_rate": rate,
            "if_18_were_surveyed": round(as_surveyed, 2),
            "if_18_responded": round(as_responded, 2),
            "surveyed_reading_is_integral": abs(as_surveyed
                                                - round(as_surveyed)) < 1e-9,
            "responded_reading_is_integral": abs(as_responded
                                                 - round(as_responded)) < 1e-9,
            "share_numerator": _f(a.group(1)),
            "share_denominator": _f(a.group(2)),
            "note": "the share's denominator is the same 18, so it is a share "
                    "of respondents under the only integral reading"}


def falsifier_ids():
    """Every registered falsifier id across the delivered documents. An id
    carried by two documents with different bodies would be a collision."""
    # A DEFINITION sits at column 0 inside the registered-falsifier block and
    # is followed by its body. A CITATION is the same id anywhere else. The
    # first version of this check counted both and reported AUT-F1 as a
    # collision because the corpus audit's cross-links mention it.
    defs, cites = {}, {}
    for key in DOC:
        body = text(key)
        for fid in re.findall(r"^([A-Z]{2,5}-F[0-9]+)\s+\S", body, re.M):
            defs.setdefault(fid, set()).add(key)
        for m in re.finditer(r"([A-Z]{2,5}-F[0-9]+)", body):
            at_line_start = m.start() == 0 or body[m.start() - 1] == "\n"
            if not at_line_start:
                cites.setdefault(m.group(1), set()).add(key)
    prefixes = {}
    for fid, docs in defs.items():
        prefixes.setdefault(fid.split("-")[0], set()).update(docs)
    return {"definitions": {k: sorted(v) for k, v in sorted(defs.items())},
            "citations": {k: sorted(v) for k, v in sorted(cites.items())},
            "prefixes": {k: sorted(v) for k, v in sorted(prefixes.items())},
            "n_ids": len(defs),
            "collisions": sorted(k for k, v in defs.items() if len(v) > 1),
            "seed_prefix_is_new": "RD" in prefixes
                                  and all(d == "seed" for d in prefixes["RD"])}


def named_and_absent():
    """AGA_009's four objects, re-checked against the folder as it now is."""
    # FILED means a document or a heading IS the object. CITED means the name
    # occurs in prose. The first version of this check tested for the name and
    # reported both ledgers as delivered on the strength of the sentences that
    # cite them -- a citation read as a filing, in the check written to
    # separate the two.
    bodies = {k: text(k) for k in DOC}
    targets = {
        "WP1": r"^#+\s+.*\bWP1\b",
        "WP2": r"^#+\s+.*\bWP2\b",
        "trades-shortage ledger": r"^#+\s+.*trades-shortage ledger",
        "claim ledger": r"^#+\s+.*claim ledger",
    }
    out = {}
    for name, pat in targets.items():
        filed = sorted(k for k, b in bodies.items()
                       if re.search(pat, b, re.M | re.I))
        cited = sorted(k for k, b in bodies.items()
                       if re.search(re.escape(name), b, re.I))
        out[name] = {"filed_in": filed, "cited_in": cited,
                     "delivered": bool(filed)}
    return {"objects": out,
            "delivered": sorted(k for k, v in out.items() if v["delivered"]),
            "still_absent": sorted(k for k, v in out.items()
                                   if not v["delivered"])}


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
        "AGA_009_named_and_absent": named_and_absent(),
        "AGA_013_seed_tire_ratio": seed_tire_ratio(),
        "AGA_014_seed_cost_vs_frequency": seed_cost_vs_frequency(),
        "AGA_015_seed_provenance": seed_provenance_vocabulary(),
        "AGA_016_seed_crosscites": seed_crosscites(),
        "AGA_017_seed_restatement": seed_rainfall_and_restatement(),
        "AGA_018_seed_survey": seed_survey_denominator(),
        "AGA_019_falsifier_ids": falsifier_ids(),
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

    na = f["AGA_009_named_and_absent"]
    print("AGA_009  objects cited as filed")
    for name, v in na["objects"].items():
        print("    %-24s %s" % (name,
                                ("FILED in " + ", ".join(v["filed_in"]))
                                if v["delivered"]
                                else "ABSENT (cited in %s)"
                                     % (", ".join(v["cited_in"]) or "nothing")))
    print("    -> delivered %d of %d; still absent: %s\n"
          % (len(na["delivered"]), len(na["objects"]),
             ", ".join(na["still_absent"]) or "none"))

    tr = f["AGA_013_seed_tire_ratio"]
    print("AGA_013  seed WP1 tire cost: gravel %(gravel)g / asphalt %(asphalt)g"
          " / concrete %(concrete)g cents-per-mile" % tr["cents"])
    print("    stated %s   recomputed %s   agrees %s / %s"
          % (tr["as_written"], tr["recomputed"], tr["lo_agrees"], tr["hi_agrees"]))
    print("    tolerance is each figure's own shipped precision %s\n"
          % tr["halfwidth"])

    cf = f["AGA_014_seed_cost_vs_frequency"]
    print("AGA_014  two rows of one table, %gx apart" % cf["factor_between_them"])
    print("    maintenance FREQUENCY stated ~%gx paved" % cf["frequency_ratio_stated"])
    print("    county EXPENDITURE gravel $%g vs paved $%g per mi/yr -> %gx"
          % (cf["expenditure"]["gravel"], cf["expenditure"]["paved"],
             cf["expenditure_ratio"]))
    print("    different quantities, so a tension and not a contradiction;")
    print("    nothing here adjudicates either figure.\n")

    pv = f["AGA_015_seed_provenance"]
    print("AGA_015  provenance vocabulary: declared %s" % pv["declared"])
    print("    used      %s" % pv["used"])
    print("    UNDECLARED %s on %d rows\n" % (pv["undeclared"], pv["undeclared_rows"]))

    cc = f["AGA_016_seed_crosscites"]
    print("AGA_016  the seed's two citations into its siblings")
    for c in cc["cites"]:
        print("    %-46s %s" % (c["cite"][:46],
                                "resolves" if c["resolves"] else "DOES NOT RESOLVE"))
        if not c["resolves"] and c.get("supporting_document"):
            print("        the supporting text is in %s, not the cited document"
                  % DOC[c["supporting_document"]])
    print()

    rs = f["AGA_017_seed_restatement"]
    print("AGA_017  THE COLLISION restates %d WP1 figures" % len(rs["checks"]))
    for c in rs["checks"]:
        print("    %-22s restated %-14s source row %-16s %s"
              % (c["figure"], c["restated"], c["source_row"],
                 "contained" if c["contained"] else "NOT CONTAINED"))
    print("    -> all contained: %s\n" % rs["all_contained"])

    sv = f["AGA_018_seed_survey"]
    print("AGA_018  Caltrans survey: %g companies at %g%% response"
          % (sv["n"], sv["response_rate"] * 100))
    print("    if the %g were surveyed, respondents = %g  (integral: %s)"
          % (sv["n"], sv["if_18_were_surveyed"], sv["surveyed_reading_is_integral"]))
    print("    if the %g responded, population  = %g  (integral: %s)"
          % (sv["n"], sv["if_18_responded"], sv["responded_reading_is_integral"]))
    print("    the %g/%g share therefore reads over respondents\n"
          % (sv["share_numerator"], sv["share_denominator"]))

    fi = f["AGA_019_falsifier_ids"]
    print("AGA_019  registered falsifiers: %d defined, %d prefixes"
          % (fi["n_ids"], len(fi["prefixes"])))
    for pre, docs in fi["prefixes"].items():
        print("    %-5s in %s" % (pre, ", ".join(docs)))
    print("    cited but not redefined elsewhere: %s"
          % (", ".join(k for k, v in fi["citations"].items()
                       if k in fi["definitions"]) or "none"))
    print("    collisions: %s\n" % (", ".join(fi["collisions"]) or "none"))


def main(argv):
    if "--selftest" in argv[1:]:
        import test_audit
        return test_audit.main()
    f = findings()
    print(json.dumps(f, indent=2)) if "--json" in argv[1:] else render(f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
