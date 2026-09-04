#!/usr/bin/env python3
"""The envelope-score instrument and the two tests the protocol builds
on it, computed from a JSONL of coded records in the protocol's schema.
No document is coded here: no vendor documentation site and no filing
registry answers from this environment, and no row is invented. With no
rows every reading prints undetermined.

    python3 envelope_score.py                       # unfilled
    python3 envelope_score.py --rows RECORDS.jsonl
    python3 envelope_score.py --domains             # T4 pre-registration hash

[CHOICE 1] the agreement statistic the 0.7 gate reads: both percent
agreement and Cohen's kappa are computed; the gate reads KAPPA.
[CHOICE 2] "A >> B" is a paired mean difference of at least 1.0 marker;
[CHOICE 3] with a two-sided exact sign test at p < 0.05.
Refuses --selftest (checks live in selftest_env.py).
"""

import argparse
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "effective-redundancy-audit"))
sys.path.insert(0, os.path.join(ROOT, "sim-span"))
from effective_redundancy import cohen_kappa  # noqa: E402
from three_column import ols  # noqa: E402

MARKERS = ("E1", "E2", "E3", "E4", "E5", "E6")
REQUIRED = ("doc_id", "arm", "vendor", "host_domain", "doc_type", "doc_words") + MARKERS + (
    "envelope_score", "structural_absence", "coder")
OPTIONAL = ("pair_id", "test", "filing_period", "domain_inferable")
GATE = 0.7
MARGIN = 1.0      # [CHOICE 2]
ALPHA = 0.05      # [CHOICE 3]
DOUBLE_CODE_SHARE = 0.20


def validate_rows(rows):
    """Refusals, not repairs: a stored score that disagrees with its
    markers, a structural absence carrying a marker, a marker outside
    {0, 1}, an arm outside A|B."""
    findings = []
    for i, r in enumerate(rows):
        missing = [k for k in REQUIRED if k not in r]
        if missing:
            findings.append("row %d: missing %s" % (i, missing))
            continue
        if r["arm"] not in ("A", "B"):
            findings.append("row %d: arm %r" % (i, r["arm"]))
        if any(r[m] not in (0, 1) for m in MARKERS):
            findings.append("row %d: marker outside {0,1}" % i)
        if r["envelope_score"] != sum(r[m] for m in MARKERS):
            findings.append("row %d: envelope_score %s is not the marker sum %d" % (i, r["envelope_score"], sum(r[m] for m in MARKERS)))
        if r["structural_absence"] and any(r[m] for m in MARKERS):
            findings.append("row %d: structural absence with a marker present" % i)
        if not isinstance(r["doc_words"], int) or r["doc_words"] < 0:
            findings.append("row %d: doc_words %r" % (i, r["doc_words"]))
        if not r["structural_absence"] and r["doc_words"] == 0:
            findings.append("row %d: zero words on a document that exists" % i)
    return findings


def per_1000(row):
    """T1 secondary outcome. None on a document with no words."""
    return (1000.0 * row["envelope_score"] / row["doc_words"]) if row["doc_words"] else None


def agreement(rows):
    """Inter-rater agreement over doc_ids coded by two coders: percent
    and kappa per marker and pooled. Both printed; the gate reads one."""
    by_doc = {}
    for r in rows:
        by_doc.setdefault(r["doc_id"], []).append(r)
    double = {d: rs for d, rs in by_doc.items() if len(rs) >= 2}
    n_docs = len(by_doc)
    if not double:
        return {"double_coded": 0, "docs": n_docs, "share": 0.0 if n_docs else None, "percent": None, "kappa": None, "per_marker": {}}
    c1, c2, per = [], [], {}
    for m in MARKERS:
        a = [rs[0][m] for rs in double.values()]
        b = [rs[1][m] for rs in double.values()]
        per[m] = {"percent": sum(1 for x, y in zip(a, b) if x == y) / len(a), "kappa": cohen_kappa(a, b)}
        c1 += a
        c2 += b
    return {"double_coded": len(double), "docs": n_docs, "share": len(double) / n_docs,
            "percent": sum(1 for x, y in zip(c1, c2) if x == y) / len(c1), "kappa": cohen_kappa(c1, c2), "per_marker": per}


def gate(agr, statistic="kappa"):
    """[CHOICE 1]. Returns (proceed, reason)."""
    v = agr.get(statistic)
    if v is None:
        return False, "no double-coded document: agreement not measured"
    if agr["share"] < DOUBLE_CODE_SHARE:
        return False, "double-coded share %.2f below %.2f" % (agr["share"], DOUBLE_CODE_SHARE)
    if v < GATE:
        return False, "%s %.3f below %.1f: instrument underspecified" % (statistic, v, GATE)
    return True, "%s %.3f" % (statistic, v)


def sign_test(diffs):
    """Two-sided exact binomial on the non-zero signs. None when no
    non-zero difference exists."""
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    n = pos + neg
    if n == 0:
        return None
    k = min(pos, neg)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def pairs(rows):
    by = {}
    for r in rows:
        if r.get("pair_id") is not None:
            by.setdefault(r["pair_id"], {})[r["arm"]] = r
    return {k: v for k, v in by.items() if "A" in v and "B" in v}


def test1(rows):
    """Paired difference on total score, per-marker deltas, the E6
    reading, and both accountings of structural absence."""
    ps = pairs(rows)
    if not ps:
        return {"pairs": 0, "reading": "undetermined", "reason": "no complete A/B pair"}
    out = {"pairs": len(ps), "min_pairs_met": len(ps) >= 30}
    absent = [k for k, v in ps.items() if v["B"]["structural_absence"] or v["A"]["structural_absence"]]
    out["structural_absence_rate_B"] = sum(1 for v in ps.values() if v["B"]["structural_absence"]) / len(ps)
    for label, keep in (("all_pairs", list(ps)), ("documents_only", [k for k in ps if k not in absent])):
        diffs = [ps[k]["A"]["envelope_score"] - ps[k]["B"]["envelope_score"] for k in keep]
        d = {"n": len(diffs), "mean_diff": (sum(diffs) / len(diffs)) if diffs else None, "sign_p": sign_test(diffs)}
        d["per_marker"] = {m: (sum(ps[k]["A"][m] - ps[k]["B"][m] for k in keep) / len(keep)) if keep else None for m in MARKERS}
        d["reading"] = reading1(d, ps, keep)
        out[label] = d
    return out


def reading1(d, ps, keep):
    if d["mean_diff"] is None:
        return "undetermined"
    e6 = [ps[k][arm]["E6"] for k in keep for arm in ("A", "B")]
    flat = len(set(e6)) == 1
    if abs(d["mean_diff"]) < MARGIN:
        return "KILL: A ~ B, loop insufficient"
    if d["mean_diff"] >= MARGIN and (d["sign_p"] is not None and d["sign_p"] < ALPHA):
        if flat and e6[0] == 0:
            return "SPLIT: A > B, E6 flat at 0 -- loop drives scope, not signature"
        if flat and e6[0] == 1:
            return "A > B, E6 flat at 1 -- every document names a party; the split reading does not apply"
        return "SUPPORTED: A >> B paired"
    return "A > B at margin, sign test not below alpha: undetermined"


def test2(rows):
    """Between-group rates on E1/E2/E4 inside one filing period, with the
    template kill read as zero variance across every marker."""
    a = [r for r in rows if r["arm"] == "A"]
    b = [r for r in rows if r["arm"] == "B"]
    if not a or not b:
        return {"reading": "undetermined", "reason": "an arm is empty", "n_A": len(a), "n_B": len(b)}
    periods = {r.get("filing_period") for r in a + b}
    if len(periods) != 1 or None in periods:
        return {"reading": "REFUSED", "reason": "filing_period not constant or not recorded: %s" % sorted(map(str, periods))}
    rates = {m: {"A": sum(r[m] for r in a) / len(a), "B": sum(r[m] for r in b) / len(b)} for m in MARKERS}
    zero_variance = all(len({r[m] for r in a + b}) == 1 for m in MARKERS)
    if zero_variance:
        reading = "KILL, informative: zero variance on every marker -- re-target to the document class the host industry requires alongside the filing"
    elif all(rates[m]["A"] > rates[m]["B"] for m in ("E1", "E2", "E4")):
        reading = "SUPPORTED: A > B on E1, E2, E4 inside one regime"
    elif all(abs(rates[m]["A"] - rates[m]["B"]) < 0.1 for m in ("E1", "E2", "E4")):
        reading = "A ~ B: regime dominates, host domain does not reach the filing layer"
    else:
        reading = "mixed across E1/E2/E4: undetermined"
    return {"n_A": len(a), "n_B": len(b), "min_n_met": min(len(a), len(b)) >= 50, "rates": rates,
            "zero_variance": zero_variance, "reading": reading}


def covariate(rows):
    """T1: score on doc_words and an arm indicator, OLS imported."""
    docs = [r for r in rows if not r["structural_absence"]]
    if len(docs) < 4:
        return {"n": len(docs), "beta": None, "r2": None}
    beta, r2 = ols([float(r["envelope_score"]) for r in docs],
                   [[float(r["doc_words"]) for r in docs], [1.0 if r["arm"] == "A" else 0.0 for r in docs]])
    return {"n": len(docs), "beta": beta, "r2": r2,
            "per_1000_mean": {arm: _mean([per_1000(r) for r in docs if r["arm"] == arm]) for arm in ("A", "B")}}


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return (sum(xs) / len(xs)) if xs else None


def unblindable(rows):
    """T3: fraction of coded documents whose domain was inferable."""
    known = [r for r in rows if r.get("domain_inferable") is not None]
    if not known:
        return {"recorded": 0, "fraction": None}
    return {"recorded": len(known), "fraction": sum(1 for r in known if r["domain_inferable"]) / len(known)}


def domains():
    path = os.path.join(HERE, "domains.json")
    raw = open(path, "rb").read()
    d = json.loads(raw.decode("utf-8"))
    return {"sha256": hashlib.sha256(raw).hexdigest()[:16], "arm_A": d["arm_A_strong_standard"] + d["arm_A_mid_standard"],
            "mid_standard": d["arm_A_mid_standard"], "t4_met": len(d["arm_A_mid_standard"]) >= 2, "registered": d["registered"]}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def render(rows):
    L = ["envelope score -- %d rows" % len(rows)]
    L.append("[CHOICE 1] gate reads kappa; [CHOICE 2] A >> B is a paired mean difference >= %.1f; [CHOICE 3] sign test alpha %.2f" % (MARGIN, ALPHA))
    d = domains()
    L.append("T4 pre-registered domains (sha256 %s, %s): %s; mid-standard %s; requirement met %s" % (
        d["sha256"], d["registered"], d["arm_A"], d["mid_standard"], d["t4_met"]))
    v = validate_rows(rows)
    if v:
        L.append("REFUSED: " + "; ".join(v))
        return "\n".join(L)
    agr = agreement(rows)
    L.append("agreement: double-coded %s of %s (share %s); percent %s; kappa %s" % (
        agr["double_coded"], agr["docs"], _f(agr["share"]), _f(agr["percent"]), _f(agr["kappa"])))
    for m, pm in agr["per_marker"].items():
        L.append("  %s percent %s kappa %s" % (m, _f(pm["percent"]), _f(pm["kappa"])))
    ok, why = gate(agr)
    L.append("gate: %s (%s)" % ("PROCEED" if ok else "REFUSED", why))
    if not ok:
        L.append("test 1: not run -- gate refused;  test 2: not run -- gate refused")
        return "\n".join(L)
    t1 = test1(rows)
    L.append("test 1: %s" % json.dumps(t1, sort_keys=True, default=str))
    L.append("test 2: %s" % json.dumps(test2(rows), sort_keys=True, default=str))
    L.append("T1 covariate: %s" % json.dumps(covariate(rows), sort_keys=True, default=str))
    L.append("T3 unblindable: %s" % json.dumps(unblindable(rows), sort_keys=True))
    return "\n".join(L)


def _f(x):
    return "%.3f" % x if isinstance(x, (int, float)) else "undetermined"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows")
    ap.add_argument("--domains", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("envelope_score has no selftest; run selftest_env.py", file=sys.stderr)
        return 2
    if a.domains:
        print(json.dumps(domains(), indent=1))
        return 0
    rows = load(a.rows) if a.rows else []
    print(render(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
