"""J) observer_position_control.py -- method layer. Is the maladaptive /
adaptive label set by the behavior, or by whether the describer is
inside the population described? Label extraction over a published
corpus; no new observation. The corpus is the data; blind coding is the
only labor, and it happens outside this script.

Two input files, kept apart so null (a) is blind by construction:
  sources.jsonl   source_id, position (1 nonhuman | 2 outgroup | 3 own),
                  decade (int), literature (ethology|psychology|ethnography|
                  clinical|history|other), label_class (pathology|artifact|
                  adaptation|need|virtue), attributed_cause (internal_defect|
                  environment|function|culture), adaptive_account
                  (supplied|assumed|none), null_offered (y|n), test_proposed (y|n)
  behavior.jsonl  source_id, avoids_neutral_novelty_high_cost (bool),
                  no_test_phase (bool), arousal_persists (bool), intensity (1..5)
                  -- coded from the description text alone. ANY other field
                  in this file is refused: a coder who could see position or
                  label was not blind.
Held-fixed pattern = all three behavior components present. Only sources
matching it enter the contingency.

Outputs: label x position contingency with Cramer's V; the four nulls,
each with its number; the residual verdict as an enum:
  OBSERVER_INDEXED | BEHAVIOR_DIFFERS | EXPLAINED_BY_ERA |
  EXPLAINED_BY_LITERATURE | EXPLAINED_BY_SEVERITY | NO_ASSOCIATION |
  UNKNOWN_measurable (source count too thin at the stated minimum)
The prediction is stated in PREDICTION before any row is read and scored
against the modal label per position. Thresholds are arguments, printed.

Command: python3 observer_position_control.py SOURCES.jsonl BEHAVIOR.jsonl [--min-cell 5] [--v 0.3] [--json]
         python3 observer_position_control.py --selftest
"""
import json
import math
import sys

POS = {1: "nonhuman", 2: "outgroup", 3: "own"}
LABELS = ("pathology", "artifact", "adaptation", "need", "virtue")
CAUSES = ("internal_defect", "environment", "function", "culture")
LITS = ("ethology", "psychology", "ethnography", "clinical", "history", "other")
BEHAVIOR_FIELDS = ("source_id", "avoids_neutral_novelty_high_cost", "no_test_phase", "arousal_persists", "intensity")
SOURCE_FIELDS = ("source_id", "position", "decade", "literature", "label_class", "attributed_cause",
                 "adaptive_account", "null_offered", "test_proposed")
PREDICTION = {1: ("pathology", "artifact"), 2: ("pathology", "artifact"), 3: ("need", "adaptation")}


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def validate(sources, behavior):
    probs = []
    for k, r in enumerate(behavior, 1):
        extra = sorted(set(r) - set(BEHAVIOR_FIELDS))
        if extra:
            probs.append("behavior row %d: fields %s present -- coder was not blind; refused" % (k, extra))
        for f in BEHAVIOR_FIELDS:
            if f not in r:
                probs.append("behavior row %d: missing %s" % (k, f))
    for k, r in enumerate(sources, 1):
        for f in SOURCE_FIELDS:
            if f not in r:
                probs.append("source row %d: missing %s" % (k, f))
        if probs and probs[-1].startswith("source row %d" % k):
            continue
        if r["position"] not in POS:
            probs.append("source row %d: position must be 1|2|3" % k)
        if r["label_class"] not in LABELS or r["attributed_cause"] not in CAUSES or r["literature"] not in LITS:
            probs.append("source row %d: label_class/attributed_cause/literature outside the closed sets" % k)
        if r["adaptive_account"] not in ("supplied", "assumed", "none") or r["null_offered"] not in ("y", "n") or r["test_proposed"] not in ("y", "n"):
            probs.append("source row %d: adaptive_account|null_offered|test_proposed value" % k)
    b_ids = set(r["source_id"] for r in behavior)
    for r in sources:
        if r["source_id"] not in b_ids:
            probs.append("source %s has no blind behavior coding" % r["source_id"])
    if probs:
        raise ValueError("\n".join(probs))


def cramers_v(table):
    """table: {row: {col: count}}. Returns (V, n, min_cell)."""
    rows, cols = sorted(table), sorted(set(c for r in table.values() for c in r))
    n = sum(table[r].get(c, 0) for r in rows for c in cols)
    if n == 0 or len(rows) < 2:
        return None, n, 0
    if len(cols) < 2:   # the label does not vary: zero association, not "not computable"
        return 0.0, n, min(table[r].get(cols[0], 0) for r in rows)
    rs = {r: sum(table[r].get(c, 0) for c in cols) for r in rows}
    cs = {c: sum(table[r].get(c, 0) for r in rows) for c in cols}
    chi2 = 0.0
    for r in rows:
        for c in cols:
            e = rs[r] * cs[c] / float(n)
            if e:
                chi2 += (table[r].get(c, 0) - e) ** 2 / e
    return round(math.sqrt(chi2 / (n * (min(len(rows), len(cols)) - 1))), 4), n, min(table[r].get(c, 0) for r in rows for c in cols)


def contingency(rows, key):
    t = {}
    for r in rows:
        t.setdefault(POS[r["position"]], {}).setdefault(r[key], 0)
        t[POS[r["position"]]][r[key]] += 1
    return t


def stratified(rows, strat_key, min_cell):
    out = {}
    for s in sorted(set(r[strat_key] for r in rows), key=str):
        sub = [r for r in rows if r[strat_key] == s]
        v, n, mc = cramers_v(contingency(sub, "label_class"))
        out[str(s)] = {"n": n, "V": v, "positions_present": sorted(set(POS[r["position"]] for r in sub)), "evaluable": v is not None and n >= min_cell}
    ev = [x for x in out.values() if x["evaluable"]]
    pooled = round(sum(x["V"] * x["n"] for x in ev) / float(sum(x["n"] for x in ev)), 4) if ev else None
    return {"strata": out, "pooled_V_weighted": pooled, "evaluable_strata": len(ev)}


def analyse(sources, behavior, min_cell=5, v_thr=0.3):
    validate(sources, behavior)
    beh = {r["source_id"]: r for r in behavior}
    joined = [dict(r, **{k: beh[r["source_id"]][k] for k in BEHAVIOR_FIELDS[1:]}) for r in sources]
    for r in joined:
        r["pattern_match"] = bool(r["avoids_neutral_novelty_high_cost"] and r["no_test_phase"] and r["arousal_persists"])
    out = {"thresholds": {"min_cell": min_cell, "v": v_thr}, "prediction": {POS[p]: list(v) for p, v in PREDICTION.items()},
           "n_sources": len(joined), "per_position_n": {POS[p]: sum(1 for r in joined if r["position"] == p) for p in POS}}
    # null a -- MAIN: is the behavior the same across positions?
    match_rate = {POS[p]: (round(sum(r["pattern_match"] for r in joined if r["position"] == p) / float(n), 4) if (n := sum(1 for r in joined if r["position"] == p)) else None) for p in POS}
    comp = {}
    for f in BEHAVIOR_FIELDS[1:4]:
        t = {POS[r["position"]]: {} for r in joined}
        for r in joined:
            t[POS[r["position"]]][str(bool(r[f]))] = t[POS[r["position"]]].get(str(bool(r[f])), 0) + 1
        comp[f] = cramers_v(t)[0]
    out["null_a_behavior"] = {"pattern_match_rate_by_position": match_rate, "component_V_by_position": comp,
                              "differs": any(v is not None and v >= v_thr for v in comp.values())}
    held = [r for r in joined if r["pattern_match"]]
    out["held_fixed_n"] = len(held)
    out["held_fixed_by_position"] = {POS[p]: sum(1 for r in held if r["position"] == p) for p in POS}
    thin = len(held) < 3 * min_cell or min(out["held_fixed_by_position"].values()) < min_cell
    ct = contingency(held, "label_class")
    v, n, mc = cramers_v(ct)
    out["contingency_label_x_position"] = ct
    out["effect_raw"] = {"V": v, "n": n, "min_cell": mc}
    modal = {p: max(c, key=lambda k: (c[k], k)) for p, c in ct.items()}
    out["prediction_check"] = {p: {"modal": modal.get(p), "predicted": out["prediction"][p], "hit": modal.get(p) in out["prediction"][p] if p in modal else None} for p in out["prediction"]}
    for key in ("attributed_cause", "adaptive_account", "null_offered", "test_proposed"):
        out["by_position_" + key] = contingency(held, key)
    # nulls b, c, d
    for r in held:
        r["intensity_band"] = "low" if r["intensity"] <= 2 else "mid" if r["intensity"] == 3 else "high"
    out["null_b_era"] = stratified(held, "decade", min_cell)
    out["null_c_literature"] = stratified(held, "literature", min_cell)
    out["null_d_severity"] = dict(stratified(held, "intensity_band", min_cell),
                                  intensity_mean_by_position={POS[p]: round(sum(r["intensity"] for r in held if r["position"] == p) / float(k), 3) if (k := sum(1 for r in held if r["position"] == p)) else None for p in POS})
    # verdict
    if out["null_a_behavior"]["differs"]:
        verdict = "BEHAVIOR_DIFFERS"
    elif thin or v is None:
        verdict = "UNKNOWN_measurable"
    elif v < v_thr:
        verdict = "NO_ASSOCIATION"
    else:
        verdict = "OBSERVER_INDEXED"
        for name, blk in (("EXPLAINED_BY_ERA", out["null_b_era"]), ("EXPLAINED_BY_LITERATURE", out["null_c_literature"]), ("EXPLAINED_BY_SEVERITY", out["null_d_severity"])):
            if blk["evaluable_strata"] == 0:
                verdict = "UNKNOWN_measurable"; out["unknown_reason"] = "%s: no stratum reaches min_cell with >= 2 positions" % name; break
            if blk["pooled_V_weighted"] < v_thr:
                verdict = name; break
    out["residual"] = {"verdict": verdict, "V_raw": v, "V_within_era": out["null_b_era"]["pooled_V_weighted"],
                       "V_within_literature": out["null_c_literature"]["pooled_V_weighted"], "V_within_severity": out["null_d_severity"]["pooled_V_weighted"]}
    return out


def render(a):
    L = ["sources %d  held-fixed pattern %d  by position %s  thresholds %s" % (a["n_sources"], a["held_fixed_n"], a["held_fixed_by_position"], a["thresholds"]),
         "NULL a (main) pattern-match rate by position %s  component V %s  differs: %s" % (a["null_a_behavior"]["pattern_match_rate_by_position"], a["null_a_behavior"]["component_V_by_position"], a["null_a_behavior"]["differs"]),
         "label x position: %s" % a["contingency_label_x_position"], "effect raw: %s" % a["effect_raw"],
         "prediction check: %s" % a["prediction_check"],
         "within era: %s  within literature: %s  within intensity: %s" % (a["null_b_era"]["pooled_V_weighted"], a["null_c_literature"]["pooled_V_weighted"], a["null_d_severity"]["pooled_V_weighted"]),
         "intensity mean by position: %s" % a["null_d_severity"]["intensity_mean_by_position"],
         "RESIDUAL: %s" % a["residual"]]
    if "unknown_reason" in a:
        L.append("unknown because: " + a["unknown_reason"])
    return "\n".join(L)


def fixture(mode="indexed", n=8):
    """Constructed. mode indexed: labels follow position; behavior identical.
    mode differs: own-population descriptions lack the arousal component.
    mode era: position perfectly confounded with decade."""
    src, beh = [], []
    k = 0
    for p in POS:
        for j in range(n):
            k += 1
            lab = {1: "pathology", 2: "artifact" if j % 3 else "pathology", 3: "need" if j % 2 else "adaptation"}[p]
            decade = {"era": {1: 1950, 2: 1980, 3: 2010}[p]}.get(mode, 1950 + 10 * (j % 7))
            src.append({"source_id": "s%d" % k, "position": p, "decade": decade, "literature": ("ethology", "ethnography", "psychology")[p - 1] if mode == "lit" else ("ethology", "psychology", "clinical", "history")[j % 4],
                        "label_class": lab, "attributed_cause": ("internal_defect", "internal_defect", "function")[p - 1],
                        "adaptive_account": ("none", "assumed", "supplied")[p - 1], "null_offered": "n", "test_proposed": "y" if p == 1 else "n"})
            beh.append({"source_id": "s%d" % k, "avoids_neutral_novelty_high_cost": True, "no_test_phase": True,
                        "arousal_persists": not (mode == "differs" and p == 3), "intensity": 3 if mode != "severity" else (5 if p != 3 else 1)})
    return src, beh


def selftest():
    a = analyse(*fixture("indexed"))
    assert a["residual"]["verdict"] == "OBSERVER_INDEXED", a["residual"]
    assert all(v["hit"] for v in a["prediction_check"].values())
    assert analyse(*fixture("differs"))["residual"]["verdict"] == "BEHAVIOR_DIFFERS"
    assert analyse(*fixture("era"))["residual"]["verdict"] in ("EXPLAINED_BY_ERA", "UNKNOWN_measurable")
    assert analyse(*fixture("indexed", n=2))["residual"]["verdict"] == "UNKNOWN_measurable"
    s, b = fixture("indexed")
    flat = [dict(r, label_class="pathology") for r in s]
    assert analyse(flat, b)["residual"]["verdict"] == "NO_ASSOCIATION"
    leaky = [dict(r, position=1) for r in b]
    try:
        analyse(s, leaky); raise AssertionError("behavior file with position accepted")
    except ValueError as e:
        assert "not blind" in str(e)
    print("observer_position_control selftest: 7 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) < 2 or "--help" in argv:
        print(__doc__); return 2
    mc = int(argv[argv.index("--min-cell") + 1]) if "--min-cell" in argv else 5
    vt = float(argv[argv.index("--v") + 1]) if "--v" in argv else 0.3
    a = analyse(read_jsonl(argv[0]), read_jsonl(argv[1]), mc, vt)
    print(json.dumps(a, indent=1, sort_keys=True) if "--json" in argv else render(a))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
