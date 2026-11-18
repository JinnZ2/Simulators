#!/usr/bin/env python3
"""Score one blind reader's response for VOID-12 against the first reader's key.

  python3 score.py response.json [--key key.json] [--json out.json] [--nulls 20000]

Reads: a response (the filled response_template.json) and scoring/key.json.
Reports, in this order:
  1. validation (a response that fails validation is not scored);
  2. blindness status from the attestation (rule fixed in PREREG.md);
  3. the 8 declared pairs: reader tier, key tier, agree / differ;
  4. all 105 term pairs: same-predicate agreement (counts, adjusted Rand index);
  5. slots: per term, reader's slot set against the key's (Jaccard);
  6. references: a Clopper-Pearson 95% interval for k of 8, and three baselines
     (singletons, label-only, and 20000 random regroupings with the key's cluster sizes).
The tier rule is the first reader's own (vocab_branches.relation): same cluster -> MAPS if the two slot sets are equal,
else PARTIAL; different clusters -> HOMONYM if the labels are equal, else NONE. Slot sets are compared
case-insensitively and without regard to order (the generator checks that this gives the same tiers as the first
reader's ordered tuples on the key). Nothing here decides anything; it counts.
"""
import argparse, itertools, json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASES = ("READ_FROM_SOURCE", "NONE_STATED", "DECLARED")
CONF = ("HIGH", "MEDIUM", "LOW")
TIERS = ("MAPS", "PARTIAL", "HOMONYM", "NONE")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def validate(resp, key):
    errs = []
    ids = set(key["terms"])
    got = resp.get("terms")
    if not isinstance(got, dict):
        return ["'terms' missing or not an object"]
    for i in sorted(ids - set(got)):
        errs.append("missing term %s" % i)
    for i in sorted(set(got) - ids):
        errs.append("unknown term %s" % i)
    for i in sorted(ids & set(got)):
        t = got[i]
        if not isinstance(t, dict):
            errs.append("%s: not an object" % i); continue
        if not str(t.get("cluster", "")).strip():
            errs.append("%s: cluster empty" % i)
        if not str(t.get("predicate", "")).strip():
            errs.append("%s: predicate empty" % i)
        if not isinstance(t.get("slots"), list) or not all(isinstance(x, str) for x in t.get("slots", [])):
            errs.append("%s: slots must be a list of strings" % i)
        if t.get("slots_basis") not in BASES:
            errs.append("%s: slots_basis must be one of %s" % (i, "/".join(BASES)))
        if t.get("slots_basis") == "NONE_STATED" and t.get("slots"):
            errs.append("%s: NONE_STATED requires slots []" % i)
        if t.get("confidence") not in CONF:
            errs.append("%s: confidence must be one of %s" % (i, "/".join(CONF)))
        cj = t.get("could_also_join", [])
        if not isinstance(cj, list) or any(x not in ids for x in cj):
            errs.append("%s: could_also_join must list known term ids" % i)
    att = resp.get("attestation", {})
    for q in ("q1_seen_pair_table_with_verdicts", "q2_seen_predicate_sentence_by_someone_else",
              "q3_seen_vocabulary_mapping_or_second_reader_report", "q4_told_how_many_clusters_or_pairs",
              "q5_used_anything_outside_packet", "q6_prior_sessions_about_this_project"):
        if att.get(q) not in ("yes", "no", "unsure"):
            errs.append("attestation %s must be yes / no / unsure" % q)
    for f in ("reader_label", "model_family", "date_utc"):
        if not str(resp.get(f, "")).strip():
            errs.append("%s empty" % f)
    return errs


def blind_status(att):
    q = [att.get(k) for k in ("q1_seen_pair_table_with_verdicts", "q2_seen_predicate_sentence_by_someone_else",
                              "q3_seen_vocabulary_mapping_or_second_reader_report", "q4_told_how_many_clusters_or_pairs")]
    if any(x == "yes" for x in q):
        s = "NOT_BLIND"
    elif all(x == "no" for x in q):
        s = "BLIND"
    else:
        s = "UNCERTAIN"
    flags = [k for k in ("q5_used_anything_outside_packet", "q6_prior_sessions_about_this_project") if att.get(k) in ("yes", "unsure")]
    return s, flags


def slotset(xs):
    return frozenset(x.strip().lower() for x in xs)


def tier(same_cluster, slots_a, slots_b, label_a, label_b):
    if same_cluster:
        return "MAPS" if slotset(slots_a) == slotset(slots_b) else "PARTIAL"
    return "HOMONYM" if label_a == label_b else "NONE"


def pair_tiers(key, clusters, slots):
    out = []
    for p in key["pairs"]:
        a, b = p["left"], p["right"]
        out.append(tier(clusters[a] == clusters[b], slots[a], slots[b], key["terms"][a]["label"], key["terms"][b]["label"]))
    return out


def ari(ca, cb):
    """Adjusted Rand index of two labelings given as parallel lists."""
    n = len(ca)
    c2 = lambda x: x * (x - 1) / 2
    tab = {}
    for x, y in zip(ca, cb):
        tab[(x, y)] = tab.get((x, y), 0) + 1
    ra, rb = {}, {}
    for (x, y), v in tab.items():
        ra[x] = ra.get(x, 0) + v; rb[y] = rb.get(y, 0) + v
    s_ij = sum(c2(v) for v in tab.values()); s_a = sum(c2(v) for v in ra.values()); s_b = sum(c2(v) for v in rb.values())
    exp = s_a * s_b / c2(n)
    mx = (s_a + s_b) / 2
    return 1.0 if mx == exp else (s_ij - exp) / (mx - exp)


def cp_interval(k, n, alpha=0.05):
    """Clopper-Pearson two-sided interval for k successes in n trials, by bisection on the binomial tail."""
    def cdf(x, p):   # P(X <= x)
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, x + 1))
    def bisect(pred):   # smallest p in [0,1] with pred(p) true; pred is monotone false -> true
        lo, hi = 0.0, 1.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if pred(mid): hi = mid
            else: lo = mid
        return (lo + hi) / 2
    low = 0.0 if k == 0 else bisect(lambda p: 1 - cdf(k - 1, p) >= alpha / 2)
    high = 1.0 if k == n else bisect(lambda p: cdf(k, p) <= alpha / 2)
    return low, high


def key_clusters(key):
    return {i: t["cluster"] for i, t in key["terms"].items()}


def key_slots(key):
    return {i: t["slots"] for i, t in key["terms"].items()}


def baselines(key):
    ids = sorted(key["terms"])
    ks = key_slots(key)
    key_t = [p["key_tier"] for p in key["pairs"]]
    single = {i: "s" + i for i in ids}
    label = {i: key["terms"][i]["label"] for i in ids}
    out = {}
    for name, cl in (("singletons", single), ("label_only", label)):
        t = pair_tiers(key, cl, ks)
        out[name] = {"tier_agree": sum(a == b for a, b in zip(t, key_t)),
                     "ari": ari([cl[i] for i in ids], [key["terms"][i]["cluster"] for i in ids])}
    return out


def null_distribution(key, n, seed=1):
    """Random regroupings: permute the key's cluster labels over the terms (same cluster sizes), slots as in the key."""
    ids = sorted(key["terms"])
    kc = [key["terms"][i]["cluster"] for i in ids]
    ks = key_slots(key)
    key_t = [p["key_tier"] for p in key["pairs"]]
    rng = random.Random(seed)
    agree, aris = [], []
    for _ in range(n):
        perm = kc[:]
        rng.shuffle(perm)
        cl = dict(zip(ids, perm))
        t = pair_tiers(key, cl, ks)
        agree.append(sum(a == b for a, b in zip(t, key_t)))
        aris.append(ari(perm, kc))
    return agree, aris


def score(resp, key, nulls=20000):
    ids = sorted(key["terms"])
    cl = {i: str(resp["terms"][i]["cluster"]).strip() for i in ids}
    sl = {i: resp["terms"][i]["slots"] for i in ids}
    rt = pair_tiers(key, cl, sl)
    rows = []
    for p, t in zip(key["pairs"], rt):
        rows.append({"pair": p["pair_label"], "left": p["left"], "right": p["right"], "reader": t, "key": p["key_tier"],
                     "agree": t == p["key_tier"],
                     "reader_same_cluster": cl[p["left"]] == cl[p["right"]], "key_same_predicate": p["same_predicate"],
                     "reader_confidence": [resp["terms"][p["left"]]["confidence"], resp["terms"][p["right"]]["confidence"]]})
    k = sum(r["agree"] for r in rows)
    # all 105 term pairs
    tp = fp = fn = tn = 0
    diff = []
    for a, b in itertools.combinations(ids, 2):
        rs = cl[a] == cl[b]
        ks_ = key["terms"][a]["cluster"] == key["terms"][b]["cluster"]
        if rs and ks_: tp += 1
        elif rs: fp += 1; diff.append(("reader joins, key does not", a, b))
        elif ks_: fn += 1; diff.append(("key joins, reader does not", a, b))
        else: tn += 1
    A = ari([cl[i] for i in ids], [key["terms"][i]["cluster"] for i in ids])
    slot_rows = []
    for i in ids:
        r, q = slotset(sl[i]), slotset(key["terms"][i]["slots"])
        j = 1.0 if not r and not q else len(r & q) / len(r | q)
        slot_rows.append({"id": i, "label": key["terms"][i]["label"], "jaccard": round(j, 3), "reader_basis": resp["terms"][i]["slots_basis"],
                          "key_slots_from": key["terms"][i]["slots_from"], "equal": r == q})
    lo, hi = cp_interval(k, len(rows))
    out = {"reader_label": resp["reader_label"], "model_family": resp["model_family"], "date_utc": resp["date_utc"],
           "blind_status": blind_status(resp["attestation"])[0], "attestation_flags": blind_status(resp["attestation"])[1],
           "pairs": rows, "tier_agree": k, "n_pairs": len(rows), "cp95": [round(lo, 3), round(hi, 3)],
           "term_pairs": {"both_join": tp, "reader_only": fp, "key_only": fn, "neither": tn, "total": tp + fp + fn + tn},
           "ari": round(A, 3), "term_pair_differences": diff, "clusters_reader": len(set(cl.values())),
           "clusters_key": len(set(t["cluster"] for t in key["terms"].values())),
           "slots": slot_rows, "baselines": baselines(key)}
    if nulls:
        ag, ar = null_distribution(key, nulls)
        out["null"] = {"n": nulls, "seed": 1, "tier_agree_mean": round(sum(ag) / nulls, 3),
                       "p_tier_agree_ge_observed": round((1 + sum(x >= k for x in ag)) / (nulls + 1), 5),
                       "ari_mean": round(sum(ar) / nulls, 3), "ari_p95": round(sorted(ar)[int(0.95 * nulls)], 3),
                       "p_ari_ge_observed": round((1 + sum(x >= A for x in ar)) / (nulls + 1), 5)}
    return out


def render(o):
    L = ["reader %s | %s | %s | blindness: %s %s" % (o["reader_label"], o["model_family"], o["date_utc"], o["blind_status"],
                                                      ("(also declared: %s)" % ", ".join(o["attestation_flags"])) if o["attestation_flags"] else ""),
         "", "declared pairs: reader tier vs key tier   (%d of %d agree; Clopper-Pearson 95%%: %.3f to %.3f)" % (o["tier_agree"], o["n_pairs"], *o["cp95"]),
         "%-46s %-8s %-8s %s" % ("pair", "reader", "key", "")]
    for r in o["pairs"]:
        L.append("%-46s %-8s %-8s %s" % (r["pair"], r["reader"], r["key"], "agree" if r["agree"] else "DIFFER"))
    t = o["term_pairs"]
    L += ["", "all %d term pairs (same predicate?): both join %d, reader only %d, key only %d, neither %d; adjusted Rand index %.3f; clusters reader %d, key %d"
          % (t["total"], t["both_join"], t["reader_only"], t["key_only"], t["neither"], o["ari"], o["clusters_reader"], o["clusters_key"])]
    for d, a, b in o["term_pair_differences"]:
        L.append("   %s: %s %s" % (d, a, b))
    L += ["", "slots (Jaccard of reader's set and key's set):"]
    for s in o["slots"]:
        L.append("   %s %-24s %.2f  %s  | reader basis %s | key: %s" % (s["id"], s["label"], s["jaccard"], "equal" if s["equal"] else "     ", s["reader_basis"], s["key_slots_from"][:40]))
    b = o["baselines"]
    L += ["", "references: singletons %d of %d (ARI %.3f); label-only %d of %d (ARI %.3f)" % (
        b["singletons"]["tier_agree"], o["n_pairs"], b["singletons"]["ari"], b["label_only"]["tier_agree"], o["n_pairs"], b["label_only"]["ari"])]
    if "null" in o:
        n = o["null"]
        L.append("random regroupings with the key's cluster sizes (%d draws): mean tier agreement %.2f, P(>= observed) %.5f; mean ARI %.3f, 95th percentile %.3f, P(>= observed) %.5f"
                 % (n["n"], n["tier_agree_mean"], n["p_tier_agree_ge_observed"], n["ari_mean"], n["ari_p95"], n["p_ari_ge_observed"]))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("response")
    ap.add_argument("--key", default=os.path.join(HERE, "key.json"))
    ap.add_argument("--json")
    ap.add_argument("--nulls", type=int, default=20000)
    a = ap.parse_args()
    key, resp = load(a.key), load(a.response)
    errs = validate(resp, key)
    if errs:
        print("NOT SCORED: response failed validation")
        for e in errs: print("  " + e)
        sys.exit(2)
    o = score(resp, key, a.nulls)
    print(render(o))
    if a.json:
        json.dump(o, open(a.json, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
