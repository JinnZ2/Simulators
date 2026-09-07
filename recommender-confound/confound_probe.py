"""A) confound_probe.py -- audit tool, built for others to run on their own
catalogs. Reads a catalog and model outputs, scores every list under >= 2
string matchers, and asks whether the reported hallucination number is
separable into h(catalog) and m(matcher) at all.

catalog.jsonl : {item_id, title, aliases?: [], category?}
outputs.jsonl : {model_id, query_id, items: [str], category?, n_requested?}

Emits (--json for the full object):
  halluc[model][matcher]        strict = miss / n
  matcher_spread                per model, max - min over matchers
  between_model_spread          per matcher, max - min over models
  kill                          max matcher_spread > min between_model_spread
                                => the model ranking is void (one matcher
                                choice moves a model past the closest gap
                                between models); the mean-vs-mean form is
                                printed beside it
  rankings_by_matcher           how many distinct model orderings the
                                matcher set produces
  canonicality_score(catalog)   fraction of titles that hit exactly one
                                item under the loosest matcher in the set
                                (self-match uniqueness), per category
  corr(sparsity, canonicality)  across categories; sparsity =
                                max(0, 1 - supply / n_requested)
  separable                     two-way halluc[category][matcher] additive
                                fit; interaction share < --interaction
                                (default 0.10, printed) => y
  preflight (WORK_ORDER_02 task 3)   runs FIRST on any catalog: the
                                canonical subset (titles that self-match
                                uniquely under the loosest matcher) is
                                scored as if it were a model output under
                                every matcher in the set. All matchers must
                                agree to 3 decimals (halluc 0.000). A
                                disagreement is a matcher-set bug and the
                                run ABORTS before any catalog claim. This
                                diagnoses the instrument with no ground
                                truth; it validates nothing about the
                                catalog (RC_008 unaffected).

Command: python3 confound_probe.py CATALOG.jsonl OUTPUTS.jsonl [--matchers exact,norm,jaccard] [--interaction 0.10] [--json]
         python3 confound_probe.py --selftest
"""
import itertools
import json
import math
import sys

from matchers import DEFAULT_SET, MATCHERS, classify, score_list  # noqa: F401

LOOSEST_ORDER = ("substring", "jaccard", "edit", "alnum", "norm", "exact")


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / float(len(xs)) if xs else None


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = mean(xs), mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 4)


def halluc_table(catalog, outputs, matchers):
    """halluc[model][matcher] pooled over all items of that model."""
    table = {}
    for m in matchers:
        for model in sorted(set(o["model_id"] for o in outputs)):
            items = [s for o in outputs if o["model_id"] == model for s in o["items"]]
            table.setdefault(model, {})[m] = score_list(items, catalog, m)["halluc_strict"]
    return table


def spreads(table, matchers):
    models = sorted(table)
    ms = {mo: round(max(table[mo].values()) - min(table[mo].values()), 4) for mo in models}
    bm = {m: round(max(table[mo][m] for mo in models) - min(table[mo][m] for mo in models), 4) for m in matchers} if len(models) > 1 else {}
    rankings = {}
    for m in matchers:  # tied models share a group; a tie is a distinct ranking from an ordering
        groups = {}
        for mo in models:
            groups.setdefault(table[mo][m], []).append(mo)
        rankings[m] = tuple(tuple(sorted(groups[v])) for v in sorted(groups))
    return {"matcher_spread": ms, "matcher_spread_mean": mean(ms.values()), "matcher_spread_max": max(ms.values()) if ms else None,
            "between_model_spread": bm, "between_model_spread_mean": mean(bm.values()) if bm else None,
            "between_model_spread_min": min(bm.values()) if bm else None,
            "distinct_rankings": len(set(rankings.values())), "rankings_by_matcher": {m: [list(g) for g in r] for m, r in rankings.items()}}


def canonicality(catalog, matchers):
    loosest = next(m for m in LOOSEST_ORDER if m in matchers)
    out = {}
    for cat in sorted(set(it.get("category", "_all") for it in catalog)):
        sub = [it for it in catalog if it.get("category", "_all") == cat]
        uniq = [classify(it["title"], sub, loosest)[0] == "match" for it in sub]
        out[cat] = {"n_items": len(sub), "self_match_unique": round(sum(uniq) / float(len(uniq)), 4) if uniq else None,
                    "mean_aliases": round(mean(len(it.get("aliases", [])) for it in sub), 3) if sub else None, "loosest_matcher": loosest}
    return out


def sparsity(catalog, outputs):
    supply = {}
    for it in catalog:
        supply[it.get("category", "_all")] = supply.get(it.get("category", "_all"), 0) + 1
    out = {}
    for o in outputs:
        cat, n = o.get("category"), o.get("n_requested")
        if cat is None or n is None:
            continue
        out.setdefault(cat, []).append(max(0.0, 1 - supply.get(cat, 0) / float(n)))
    return {c: round(mean(v), 4) for c, v in out.items()}


def separability(catalog, outputs, matchers, thr):
    cats = sorted(set(o.get("category") for o in outputs if o.get("category") is not None))
    if len(cats) < 2 or len(matchers) < 2:
        return {"separable": None, "note": "needs >= 2 categories and >= 2 matchers", "interaction_share": None}
    cell = {}
    for c in cats:
        items = [s for o in outputs if o.get("category") == c for s in o["items"]]
        for m in matchers:
            cell[(c, m)] = score_list(items, catalog, m)["halluc_strict"]
    if any(v is None for v in cell.values()):
        return {"separable": None, "note": "an empty category/matcher cell", "interaction_share": None}
    g = mean(cell.values())
    rowm = {c: mean(cell[(c, m)] for m in matchers) for c in cats}
    colm = {m: mean(cell[(c, m)] for c in cats) for m in matchers}
    ss_tot = sum((v - g) ** 2 for v in cell.values())
    ss_int = sum((cell[(c, m)] - rowm[c] - colm[m] + g) ** 2 for c in cats for m in matchers)
    share = round(ss_int / ss_tot, 4) if ss_tot else 0.0
    return {"separable": share < thr, "interaction_share": share, "threshold": thr,
            "row_effect_catalog": {c: round(rowm[c] - g, 4) for c in cats}, "col_effect_matcher": {m: round(colm[m] - g, 4) for m in matchers},
            "note": "additive two-way fit on halluc[category][matcher]; share of variance not explained by row + column effects"}


class Abort(Exception):
    """Pre-flight failed: matcher-set bug. No catalog claim is emitted."""


def preflight(catalog, matchers, tol=0.0005):
    loosest = next(m for m in LOOSEST_ORDER if m in matchers)
    canonical = [it for it in catalog if classify(it["title"], catalog, loosest)[0] == "match"]
    titles = [it["title"] for it in canonical]
    rates = {m: score_list(titles, catalog, m)["halluc_strict"] for m in matchers} if titles else {}
    vals = [v for v in rates.values() if v is not None]
    ok = bool(vals) and (max(vals) - min(vals)) <= tol and max(vals) <= tol
    return {"canonical_subset": len(canonical), "of_catalog": len(catalog), "loosest_matcher": loosest,
            "halluc_on_canonical_subset": rates, "tolerance": tol, "passed": ok,
            "note": ("all matchers agree on the canonical subset" if ok else
                     "matchers DISAGREE on titles that are their own catalog entries: matcher-set bug, ABORT" if vals else
                     "no canonical subset: nothing self-matches uniquely under %s, ABORT" % loosest)}


def probe(catalog, outputs, matchers, thr=0.10):
    pf = preflight(catalog, matchers)
    if not pf["passed"]:
        raise Abort(json.dumps(pf, sort_keys=True))
    table = halluc_table(catalog, outputs, matchers)
    sp = spreads(table, matchers)
    kill = (sp["matcher_spread_max"] > sp["between_model_spread_min"]) if sp["between_model_spread_min"] is not None else None
    kill_mean = (sp["matcher_spread_mean"] > sp["between_model_spread_mean"]) if sp["between_model_spread_mean"] is not None else None
    canon = canonicality(catalog, matchers)
    spar = sparsity(catalog, outputs)
    common = sorted(set(canon) & set(spar))
    corr = pearson([spar[c] for c in common], [canon[c]["self_match_unique"] for c in common]) if len(common) >= 3 else None
    return {"matchers": list(matchers), "preflight": pf, "halluc": table, "spreads": sp,
            "kill_ranking_void": kill, "kill_rule": "max matcher_spread over models > min between_model_spread over matchers "
                                                   "(one matcher choice can move a model past the closest gap between models)",
            "kill_mean_form": kill_mean, "kill_mean_rule": "matcher_spread_mean > between_model_spread_mean",
            "canonicality": canon, "sparsity": spar, "corr_sparsity_canonicality": corr, "corr_n_categories": len(common),
            "separability": separability(catalog, outputs, matchers, thr)}


def render(r):
    pf = r["preflight"]
    L = ["preflight: %s  canonical subset %d of %d  halluc on subset %s" % ("PASS" if pf["passed"] else "ABORT", pf["canonical_subset"], pf["of_catalog"], pf["halluc_on_canonical_subset"]),
         "matchers: %s" % ", ".join(r["matchers"]), "halluc_strict[model][matcher]:"]
    for mo, row in r["halluc"].items():
        L.append("  %-12s " % mo + "  ".join("%s=%.3f" % (m, v) for m, v in row.items()))
    s = r["spreads"]
    L += ["matcher_spread (per model): %s  mean %.4f" % (s["matcher_spread"], s["matcher_spread_mean"]),
          "between_model_spread (per matcher): %s  mean %s" % (s["between_model_spread"], s["between_model_spread_mean"]),
          "distinct model rankings across matchers: %d" % s["distinct_rankings"],
          "KILL: %s  [%s]" % (r["kill_ranking_void"], r["kill_rule"]),
          "     mean form: %s  [%s]" % (r["kill_mean_form"], r["kill_mean_rule"]),
          "canonicality per category: %s" % {c: v["self_match_unique"] for c, v in r["canonicality"].items()},
          "sparsity per category: %s" % r["sparsity"],
          "corr(sparsity, canonicality): %s over %d categories" % (r["corr_sparsity_canonicality"], r["corr_n_categories"]),
          "separable h from m: %s  (interaction share %s, threshold %s)" % (r["separability"]["separable"], r["separability"]["interaction_share"], r["separability"].get("threshold"))]
    return "\n".join(L)


FIXTURE_NAME = "kill_rule_boundary"


def fixture():
    """The KILL-RULE BOUNDARY case (WORK_ORDER_02 task 4), kept on purpose.
    Two models with identical item sets, one rendering canonically and one
    not: under the strict form (max matcher spread > min model spread) the
    ranking is void, under the mean form it is not. Ranking validity here
    depends on the rule chosen; both forms are printed and the
    disagreement is a result, not a defect."""
    cat = [{"item_id": "s%d" % k, "title": "The Signal Book %d" % k, "category": "sparse"} for k in range(3)] + \
          [{"item_id": "d%d" % k, "title": "Dense Title %d: A Subtitle" % k, "category": "dense"} for k in range(30)]
    out = []
    for q in range(5):
        out.append({"model_id": "m_exact", "query_id": "s%d" % q, "category": "sparse", "n_requested": 10,
                    "items": ["The Signal Book %d" % k for k in range(3)] + ["Made Up %d_%d" % (q, k) for k in range(7)]})
        out.append({"model_id": "m_variant", "query_id": "s%d" % q, "category": "sparse", "n_requested": 10,
                    "items": ["the signal book %d." % k for k in range(3)] + ["Made Up %d_%d" % (q, k) for k in range(7)]})
        out.append({"model_id": "m_exact", "query_id": "d%d" % q, "category": "dense", "n_requested": 10,
                    "items": ["Dense Title %d: A Subtitle" % k for k in range(10)]})
        out.append({"model_id": "m_variant", "query_id": "d%d" % q, "category": "dense", "n_requested": 10,
                    "items": ["Dense Title %d" % k for k in range(10)]})
    return cat, out


def selftest():
    cat, out = fixture()
    r = probe(cat, out, ("exact", "norm", "substring"))
    h = r["halluc"]
    assert h["m_exact"]["exact"] == 0.35 and h["m_variant"]["exact"] == 1.0 and h["m_variant"]["norm"] == 0.85, h
    assert h["m_variant"]["substring"] == 0.35, h  # same outputs, loosest matcher: the two models tie
    assert r["spreads"]["distinct_rankings"] >= 2
    assert r["kill_ranking_void"] is True
    assert r["canonicality"]["sparse"]["self_match_unique"] == 1.0
    assert r["sparsity"]["sparse"] == 0.7 and r["sparsity"]["dense"] == 0.0
    assert r["corr_sparsity_canonicality"] is None and r["corr_n_categories"] == 2  # two categories: not computable
    assert r["separability"]["separable"] in (True, False)
    single = probe(cat, [o for o in out if o["model_id"] == "m_exact"], ("exact", "norm"))
    assert single["kill_ranking_void"] is None
    assert r["preflight"]["passed"] and r["preflight"]["canonical_subset"] == len(cat)
    MATCHERS["broken"] = lambda cand, catalog: set()     # a matcher that misses everything
    try:
        probe(cat, out, ("exact", "broken")); raise AssertionError("broken matcher passed preflight")
    except Abort as e:
        assert "ABORT" in str(e)
    finally:
        del MATCHERS["broken"]
    print("confound_probe selftest: 11 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) < 2 or "--help" in argv:
        print(__doc__)
        return 2
    catalog, outputs = read_jsonl(argv[0]), read_jsonl(argv[1])
    matchers = tuple(DEFAULT_SET)
    thr, as_json = 0.10, "--json" in argv
    if "--matchers" in argv:
        matchers = tuple(x for x in argv[argv.index("--matchers") + 1].split(",") if x)
    if "--interaction" in argv:
        thr = float(argv[argv.index("--interaction") + 1])
    if len(matchers) < 2 or any(m not in MATCHERS for m in matchers):
        print("need >= 2 matchers from %s" % sorted(MATCHERS))
        return 2
    try:
        r = probe(catalog, outputs, matchers, thr)
    except Abort as e:
        print("PREFLIGHT ABORT -- matcher-set bug, no catalog claim emitted:\n%s" % e)
        return 3
    print(json.dumps(r, indent=1, sort_keys=True) if as_json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
