#!/usr/bin/env python3
"""Score one blind reader's v2 response (two slot lists per term) for VOID-12.
  python3 score_v2.py response.json [--key key_v2.json] [--json out.json]
Reports, in this order:
  1. validation (a failing response is not scored);
  2. blindness status (rule in PREREG.md);
  3. grouping: all 105 term pairs and the adjusted Rand index. This does not depend on slots at all;
  4. for EACH of the two slot meanings, separately:
       a. the 8 declared pairs: reader tier, key tier under that meaning, and the first reading's declared tier beside them;
          the count is out of the pairs the key could determine under that meaning (a pair with an undetermined slot list
          is shown as n/d and is neither a match nor a miss);
       b. per term, reader's set against the key's: equal, or which names are missing and which are extra (n/d where the key
          is undetermined);
       c. two references: nothing grouped, and grouped by label only, under the same key tiers;
It does not combine the two meanings into one number, and it does not say which meaning is right. The tier rule is the first
reader's (same cluster: MAPS if the two slot sets are equal, else PARTIAL; different clusters: HOMONYM if the labels are
equal, else NONE); under 'specific' two terms that each have no tied fields have equal (empty) sets and so MAPS.

Scoring rules a key may name in meta.scoring_rules (key_v2_a1.json names both; key_v2.json names none, so v2 output is
unchanged byte for byte). Source: KEY_V2_AMENDMENT_1.md.
  N1  before comparing slot names, strip one pair of surrounding < > and surrounding backticks (after strip + lowercase)
  C1  per term, beside equal / differ, the set relation of reader to key: equal | reader-superset | reader-subset |
      overlap | disjoint; a superset lists its extras. Reported beside the existing numbers; nothing is combined.
"""
import argparse, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score as S  # noqa: E402
MEANINGS = ("specific", "carried")
RULES = ("N1", "C1")
RELATIONS = ("equal", "reader-superset", "reader-subset", "overlap", "disjoint")

def rules_of(key):
    r = tuple(key.get("meta", {}).get("scoring_rules", ()))
    bad = [x for x in r if x not in RULES]
    if bad:
        raise ValueError("unknown scoring rule(s) in key: %s" % ", ".join(bad))
    return r

def norm_name(x, n1):
    """The scorer's name comparison: strip + lowercase (as score.slotset); under N1 also one pair of <> and backticks."""
    x = x.strip().lower()
    if n1:
        if len(x) >= 2 and x[0] == "`" and x[-1] == "`": x = x[1:-1].strip()
        if len(x) >= 2 and x[0] == "<" and x[-1] == ">": x = x[1:-1].strip()
    return x

def nset(xs, n1):
    return frozenset(norm_name(x, n1) for x in xs)

def relation(r, q):
    """C1: reader set r against key set q."""
    if r == q: return "equal"
    if r > q: return "reader-superset"
    if r < q: return "reader-subset"
    return "overlap" if r & q else "disjoint"

def ntier(same, sa, sb, la, lb, n1):
    if same:
        return "MAPS" if nset(sa, n1) == nset(sb, n1) else "PARTIAL"
    return "HOMONYM" if la == lb else "NONE"

def validate(resp, key):
    errs = []
    ids = set(key["terms"])
    got = resp.get("terms")
    if not isinstance(got, dict):
        return ["'terms' missing or not an object"]
    for i in sorted(ids - set(got)): errs.append("missing term %s" % i)
    for i in sorted(set(got) - ids): errs.append("unknown term %s" % i)
    for i in sorted(ids & set(got)):
        t = got[i]
        if not isinstance(t, dict):
            errs.append("%s: not an object" % i); continue
        if not str(t.get("cluster", "")).strip(): errs.append("%s: cluster empty" % i)
        if not str(t.get("predicate", "")).strip(): errs.append("%s: predicate empty" % i)
        for m in MEANINGS:
            v = t.get("slots_" + m)
            if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
                errs.append("%s: slots_%s must be a list of strings" % (i, m))
            b = t.get("slots_%s_basis" % m)
            if b not in S.BASES:
                errs.append("%s: slots_%s_basis must be one of %s" % (i, m, "/".join(S.BASES)))
            if b == "NONE_STATED" and v:
                errs.append("%s: slots_%s_basis NONE_STATED requires []" % (i, m))
        if t.get("confidence") not in S.CONF: errs.append("%s: confidence must be one of %s" % (i, "/".join(S.CONF)))
        cj = t.get("could_also_join", [])
        if not isinstance(cj, list) or any(x not in ids for x in cj):
            errs.append("%s: could_also_join must list known term ids" % i)
    att = resp.get("attestation", {})
    for q in ("q1_seen_pair_table_with_verdicts", "q2_seen_predicate_sentence_by_someone_else",
              "q3_seen_vocabulary_mapping_or_second_reader_report", "q4_told_how_many_clusters_or_pairs",
              "q5_used_anything_outside_packet", "q6_prior_sessions_about_this_project"):
        if att.get(q) not in ("yes", "no", "unsure"): errs.append("attestation %s must be yes / no / unsure" % q)
    for f in ("reader_label", "model_family", "date_utc"):
        if not str(resp.get(f, "")).strip(): errs.append("%s empty" % f)
    return errs

def tiers_under(key, clusters, slots_of, m):
    """Tier of each declared pair given clusters and a {id: list or None} map; None if a needed list is undetermined."""
    n1 = "N1" in rules_of(key)
    out = []
    for p in key["pairs"]:
        a, b = p["left"], p["right"]
        same = clusters[a] == clusters[b]
        sa, sb = slots_of[a], slots_of[b]
        if same and (sa is None or sb is None):
            out.append(None)
        else:
            out.append(ntier(same, sa or [], sb or [], key["terms"][a]["label"], key["terms"][b]["label"], n1))
    return out

def score(resp, key):
    rules = rules_of(key)
    n1, c1 = "N1" in rules, "C1" in rules
    ids = sorted(key["terms"])
    cl = {i: str(resp["terms"][i]["cluster"]).strip() for i in ids}
    kc = {i: key["terms"][i]["cluster"] for i in ids}
    tp = fp = fn = tn = 0
    diff = []
    for a, b in itertools.combinations(ids, 2):
        rs, ks = cl[a] == cl[b], kc[a] == kc[b]
        if rs and ks: tp += 1
        elif rs: fp += 1; diff.append(("reader joins, key does not", a, b))
        elif ks: fn += 1; diff.append(("key joins, reader does not", a, b))
        else: tn += 1
    out = {"reader_label": resp["reader_label"], "model_family": resp["model_family"], "date_utc": resp["date_utc"],
           "blind_status": S.blind_status(resp["attestation"])[0], "attestation_flags": S.blind_status(resp["attestation"])[1],
           "term_pairs": {"both_join": tp, "reader_only": fp, "key_only": fn, "neither": tn, "total": tp + fp + fn + tn},
           "ari": round(S.ari([cl[i] for i in ids], [kc[i] for i in ids]), 3), "term_pair_differences": diff,
           "clusters_reader": len(set(cl.values())), "clusters_key": len(set(kc.values())), "meanings": {}, "flags": []}   # flags: reserved, empty
    if rules:
        out["key_version"] = key["meta"].get("v"); out["scoring_rules"] = list(rules)
    single = {i: "s" + i for i in ids}
    label = {i: key["terms"][i]["label"] for i in ids}
    for m in MEANINGS:
        kslots = {i: key["terms"][i]["slots_" + m] for i in ids}
        rslots = {i: resp["terms"][i]["slots_" + m] for i in ids}
        ktier = [p["key_tier_" + m] for p in key["pairs"]]
        rtier = tiers_under(key, cl, rslots, m)
        rows = []
        for p, kt, rt in zip(key["pairs"], ktier, rtier):
            rows.append({"pair": p["pair_label"], "reader": rt, "key": kt, "first_reading_declared": p["key_tier"],
                         "agree": None if kt is None else rt == kt})
        det = [r for r in rows if r["agree"] is not None]
        k, n = sum(r["agree"] for r in det), len(det)
        lo, hi = S.cp_interval(k, n) if n else (0.0, 1.0)
        base = {}
        for name, c in (("singletons", single), ("label_only", label)):
            t = tiers_under(key, c, kslots, m)
            base[name] = sum(1 for a, b in zip(t, ktier) if b is not None and a == b)
        srows = []
        for i in ids:
            r = nset(rslots[i], n1)
            if kslots[i] is None:
                row = {"id": i, "label": key["terms"][i]["label"], "status": "n/d", "missing": [], "extra": sorted(r), "reader_basis": resp["terms"][i]["slots_%s_basis" % m]}
                if c1: row["relation"] = "n/d"
                srows.append(row)
                continue
            q = nset(kslots[i], n1)
            row = {"id": i, "label": key["terms"][i]["label"], "status": "equal" if r == q else "differ",
                   "missing": sorted(q - r), "extra": sorted(r - q), "reader_basis": resp["terms"][i]["slots_%s_basis" % m]}
            if c1: row["relation"] = relation(r, q)
            srows.append(row)
        sdet = [s for s in srows if s["status"] != "n/d"]
        out["meanings"][m] = {"pairs": rows, "tier_agree": k, "n_determined": n, "n_pairs": len(rows),
                              "cp95": [round(lo, 3), round(hi, 3)], "baselines": base, "slots": srows,
                              "slots_equal": sum(s["status"] == "equal" for s in sdet), "slots_determined": len(sdet)}
        if c1:
            out["meanings"][m]["relations"] = {k2: sum(s["relation"] == k2 for s in sdet) for k2 in RELATIONS}
    return out

def render(o):
    L = ["reader %s | %s | %s | blindness: %s %s" % (o["reader_label"], o["model_family"], o["date_utc"], o["blind_status"],
                                                      ("(also declared: %s)" % ", ".join(o["attestation_flags"])) if o["attestation_flags"] else "")]
    if o.get("scoring_rules"):
        L.append("key %s | scoring rules %s (KEY_V2_AMENDMENT_1.md)" % (o["key_version"], ", ".join(o["scoring_rules"])))
    t = o["term_pairs"]
    L += ["", "grouping (independent of slots): all %d term pairs: both join %d, reader only %d, key only %d, neither %d; adjusted Rand index %.3f; clusters reader %d, key %d"
          % (t["total"], t["both_join"], t["reader_only"], t["key_only"], t["neither"], o["ari"], o["clusters_reader"], o["clusters_key"])]
    for d, a, b in o["term_pair_differences"]: L.append("   %s: %s %s" % (d, a, b))
    for m in MEANINGS:
        x = o["meanings"][m]
        L += ["", "=== slots_%s ===" % m,
              "declared pairs: %d of %d determined agree with the key (Clopper-Pearson 95%%: %.3f to %.3f); %d pair(s) n/d" % (x["tier_agree"], x["n_determined"], *x["cp95"], x["n_pairs"] - x["n_determined"]),
              "%-46s %-8s %-8s %-8s" % ("pair", "reader", "key", "first reading's declared tier")]
        for r in x["pairs"]:
            L.append("%-46s %-8s %-8s %-8s %s" % (r["pair"], r["reader"] or "n/d", r["key"] or "n/d", r["first_reading_declared"],
                                                  "" if r["agree"] is None else ("agree" if r["agree"] else "DIFFER")))
        L.append("references under this key: nothing grouped %d, label-only %d (of %d determined)" % (x["baselines"]["singletons"], x["baselines"]["label_only"], x["n_determined"]))
        L.append("slot sets equal to the key's: %d of %d determined" % (x["slots_equal"], x["slots_determined"]))
        if "relations" in x:
            L.append("set relation, reader to key (C1, beside the count above): " + ", ".join("%s %d" % (k2, x["relations"][k2]) for k2 in RELATIONS))
        for s in x["slots"]:
            if s["status"] == "equal": continue
            rel = (" [%s]" % s["relation"]) if "relation" in s and s["status"] == "differ" else ""
            L.append("   %s %-24s %-6s missing %s extra %s%s" % (s["id"], s["label"], s["status"], s["missing"] or "-", s["extra"] or "-", rel) if s["status"] == "differ"
                     else "   %s %-24s n/d (key undetermined); reader gave %s" % (s["id"], s["label"], s["extra"] or "[]"))
    if o["flags"]:
        L += ["", "flags:"] + ["   " + f for f in o["flags"]]
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("response"); ap.add_argument("--key", default=os.path.join(HERE, "key_v2.json")); ap.add_argument("--json")
    a = ap.parse_args()
    key, resp = S.load(a.key), S.load(a.response)
    errs = validate(resp, key)
    if errs:
        print("NOT SCORED: response failed validation")
        for e in errs: print("  " + e)
        sys.exit(2)
    o = score(resp, key)
    print(render(o))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f: json.dump(o, f, indent=1)

if __name__ == "__main__":
    main()
