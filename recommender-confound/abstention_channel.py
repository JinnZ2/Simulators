"""C) abstention_channel.py -- the contract, and a test of it.

contract v1  "return N items": N fixed by the harness, not by supply, so
             a deficit has one low-resistance path, fabricate.
contract v2  items[] (0..N), supply_estimate, refusal_reason[]
scoring      PRECISION over the items returned, never count-completion;
             abstention is CORRECT when supply < N and the list stops at
             supply. count_completion is printed and is not the score.

score mode   python3 abstention_channel.py score CATALOG.jsonl RESPONSES.jsonl --contract v1|v2 [--json]
             responses: {query_id, category, n_requested, items[]} and for v2
             also supply_estimate (int) and refusal_reason[] (non-empty when
             len(items) < n_requested). A v2 row failing that is refused.
sim mode     python3 abstention_channel.py sim --seed 1 [--json]
             the synthetic_catalog model, unchanged, under v1 then v2:
             hallucination collapse with the model held fixed.
             python3 abstention_channel.py --selftest
"""
import json
import random
import sys

import synthetic_catalog as sc
from matchers import score_list

REFUSALS = ("supply_exhausted", "ambiguous_request", "no_knowledge", "other")


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def validate_v2(rows):
    probs = []
    for k, r in enumerate(rows, 1):
        for f in ("query_id", "n_requested", "items", "supply_estimate", "refusal_reason"):
            if f not in r:
                probs.append("row %d: missing %s" % (k, f))
        if probs:
            continue
        if len(r["items"]) > r["n_requested"]:
            probs.append("row %d: more items than n_requested" % k)
        if len(r["items"]) < r["n_requested"] and not r["refusal_reason"]:
            probs.append("row %d: short list with no refusal_reason" % k)
    if probs:
        raise ValueError("\n".join(probs))
    return rows


def score(catalog, rows, contract, matcher="norm"):
    supply = {}
    for it in catalog:
        supply[it.get("category", "_all")] = supply.get(it.get("category", "_all"), 0) + 1
    if contract == "v2":
        validate_v2(rows)
    per, agg = [], {"precision": [], "halluc": [], "count_completion": [], "abstention_correct": 0, "over_abstention": 0, "supply_below_n": 0}
    for r in rows:
        cat = [it for it in catalog if it.get("category", "_all") == r.get("category", "_all")]
        s = score_list(r["items"], cat, matcher)
        n, k, sup = r["n_requested"], len(r["items"]), supply.get(r.get("category", "_all"), 0)
        prec = (s["match"] / float(k)) if k else None
        row = {"query_id": r["query_id"], "returned": k, "n_requested": n, "supply": sup, "precision": prec,
               "halluc": s["halluc_strict"], "count_completion": round(k / float(n), 4),
               "supply_below_n": sup < n, "abstention_correct": (sup < n and k <= sup), "over_abstention": k < min(sup, n)}
        if contract == "v2":
            row["supply_estimate"] = r["supply_estimate"]
            row["supply_estimate_error"] = r["supply_estimate"] - sup
            row["refusal_reason"] = r["refusal_reason"]
        per.append(row)
        for f in ("precision", "halluc", "count_completion"):
            if row[f] is not None:
                agg[f].append(row[f])
        agg["supply_below_n"] += row["supply_below_n"]; agg["abstention_correct"] += row["abstention_correct"]; agg["over_abstention"] += row["over_abstention"]
    m = lambda xs: round(sum(xs) / float(len(xs)), 4) if xs else None
    return {"contract": contract, "matcher": matcher, "n_queries": len(rows),
            "precision_mean": m(agg["precision"]), "halluc_mean": m(agg["halluc"]),
            "count_completion_mean (NOT the score)": m(agg["count_completion"]),
            "abstention_correct": "%d of %d queries with supply < N" % (agg["abstention_correct"], agg["supply_below_n"]),
            "over_abstention": agg["over_abstention"], "per_query": per}


def sim(seed, n=10, queries=50):
    """The synthetic_catalog model under both contracts, sparse corner, high canonicality."""
    rng = random.Random(seed)
    cat = sc.make_catalog(rng, sc.SUPPLY["sparse"], "sparse")
    out = {}
    for contract in ("v1", "v2"):
        rng = random.Random(seed)  # identical draws: the model is unchanged
        rows = []
        for q in range(queries):
            items, fab, sup = sc.produce(rng, cat, n, "high", sc.MODEL, contract)
            row = {"query_id": "q%d" % q, "category": "sparse", "n_requested": n, "items": items}
            if contract == "v2":
                row.update({"supply_estimate": sup, "refusal_reason": ["supply_exhausted"] if len(items) < n else []})
            rows.append(row)
        r = score(cat, rows, contract)
        r.pop("per_query")
        out[contract] = r
    return {"seed": seed, "model": sc.MODEL, "supply": sc.SUPPLY["sparse"], "n": n, "v1": out["v1"], "v2": out["v2"],
            "collapse": round(out["v1"]["halluc_mean"] - out["v2"]["halluc_mean"], 4),
            "reading": "the model is identical under both contracts; the difference is the contract"}


def selftest():
    r = sim(3, queries=40)
    assert r["v1"]["halluc_mean"] > 0.6 and r["v2"]["halluc_mean"] < 0.15, r
    assert r["collapse"] > 0.5
    assert r["v2"]["abstention_correct"].startswith("40 of 40")
    assert r["v1"]["abstention_correct"].startswith("0 of 40")
    bad = [{"query_id": "q", "category": "sparse", "n_requested": 10, "items": ["x"], "supply_estimate": 1, "refusal_reason": []}]
    try:
        validate_v2(bad); raise AssertionError("short v2 list with no refusal accepted")
    except ValueError:
        pass
    assert sim(3, queries=40) == r
    print("abstention_channel selftest: 6 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if not argv or "--help" in argv:
        print(__doc__); return 2
    as_json = "--json" in argv
    if argv[0] == "sim":
        r = sim(int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 1)
        if as_json:
            print(json.dumps(r, indent=1, sort_keys=True))
        else:
            print("model %s held fixed | v1 halluc %.3f  v2 halluc %.3f  collapse %.3f | v2 precision %.3f, abstention %s" %
                  (r["model"], r["v1"]["halluc_mean"], r["v2"]["halluc_mean"], r["collapse"], r["v2"]["precision_mean"], r["v2"]["abstention_correct"]))
        return 0
    if argv[0] == "score" and len(argv) >= 3:
        contract = argv[argv.index("--contract") + 1] if "--contract" in argv else "v1"
        r = score(read_jsonl(argv[1]), read_jsonl(argv[2]), contract)
        if not as_json:
            r.pop("per_query")
        print(json.dumps(r, indent=1, sort_keys=True))
        return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
