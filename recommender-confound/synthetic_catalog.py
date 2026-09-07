"""B) synthetic_catalog.py -- null construction for the 0.6% -> 61%
finding. No data required. A 2x2 grid, density x title_canonicality,
four corners, one matcher set, MODEL ACCURACY HELD CONSTANT across all
four. What moves the measured number is then h and m alone.

The synthetic model, identical in every corner:
  recall    fraction of the available supply it produces correctly
  fab_on_recall  fraction of produced items that are fabricated even with
            supply available (a model property, constant)
  contract  v1: fill to N regardless of supply (deficit -> fabricate)
Corners:
  density        sparse: supply < N        dense: supply >> N
  canonicality   low: true titles rendered as variants (case, punctuation,
                 dropped article, dropped subtitle, typo, year suffix)
                 high: rendered verbatim
Every constant is a [MODEL] parameter and printed. Seeded.

Emits per corner x matcher: measured halluc (miss / N), the TRUE
fabrication rate the model actually committed, and their difference;
then the swing: max - min of measured across corners at each matcher,
and across matchers at each corner.

Command: python3 synthetic_catalog.py --seed 1 [--n 10] [--queries 50] [--json]
         python3 synthetic_catalog.py --selftest
"""
import json
import random
import sys

from matchers import DEFAULT_SET, score_list

WORDS = ("river", "signal", "harbor", "lantern", "meridian", "quarry", "ember", "cistern", "gantry",
         "furrow", "halyard", "kestrel", "mica", "pinion", "sable", "tallow", "vellum", "wicket", "zenith", "basalt")
MODEL = {"recall": 0.9, "fab_on_recall": 0.05}          # [MODEL] constant across corners
SUPPLY = {"sparse": 3, "dense": 40}              # [MODEL] items available per query
VARIANT_P = {"low": 0.8, "high": 0.0}            # [MODEL] chance a true title is rendered non-canonically


def title(rng, k):
    return "The %s of %s %d: %s %s" % (rng.choice(WORDS).title(), rng.choice(WORDS).title(), k,
                                       rng.choice(WORDS).title(), rng.choice(WORDS).title())


def variant(rng, t):
    kind = rng.randrange(6)
    if kind == 0:
        return t.lower()
    if kind == 1:
        return t.replace(":", " -")
    if kind == 2:
        return t[4:] if t.startswith("The ") else t
    if kind == 3:
        return t.split(":")[0]
    if kind == 4 and len(t) > 6:
        i = rng.randrange(1, len(t) - 2)
        return t[:i] + t[i + 1] + t[i] + t[i + 2:]
    return t + " (%d)" % rng.randrange(1950, 2025)


def make_catalog(rng, supply, tag):
    return [{"item_id": "%s%d" % (tag, k), "title": title(rng, k), "category": tag} for k in range(supply)]


def fabricated(rng, catalog):
    titles = set(it["title"] for it in catalog)
    while True:
        t = title(rng, rng.randrange(1000, 9999))
        if t not in titles:
            return t


def produce(rng, catalog, n, canon, model, contract="v1"):
    """One query. Returns (items, n_true_fabricated, supply_estimate)."""
    supply = len(catalog)
    recalled = [it["title"] for it in rng.sample(catalog, min(supply, n)) if rng.random() < model["recall"]]
    items, fab = [], 0
    for t in recalled:
        if rng.random() < model["fab_on_recall"]:
            items.append(fabricated(rng, catalog)); fab += 1
        else:
            items.append(variant(rng, t) if rng.random() < VARIANT_P[canon] else t)
    if contract == "v1":
        while len(items) < n:
            items.append(fabricated(rng, catalog)); fab += 1
    return items, fab, supply


def grid(seed, n=10, queries=50, matchers=DEFAULT_SET, model=MODEL):
    rng = random.Random(seed)
    out = {}
    for dens in ("sparse", "dense"):
        for canon in ("low", "high"):
            cat = make_catalog(rng, SUPPLY[dens], "%s_%s" % (dens, canon))
            lists, true_fab, total = [], 0, 0
            for _ in range(queries):
                items, fab, _s = produce(rng, cat, n, canon, model)
                lists.append(items); true_fab += fab; total += len(items)
            true_rate = round(true_fab / float(total), 4)
            cell = {"true_fabrication_rate": true_rate, "measured": {}}
            for m in matchers:
                meas = round(score_list([s for L in lists for s in L], cat, m)["halluc_strict"], 4)
                cell["measured"][m] = {"halluc": meas, "excess_over_true": round(meas - true_rate, 4)}
            out["%s/%s" % (dens, canon)] = cell
    swing_by_matcher = {m: round(max(c["measured"][m]["halluc"] for c in out.values()) - min(c["measured"][m]["halluc"] for c in out.values()), 4) for m in matchers}
    swing_by_corner = {k: round(max(v["halluc"] for v in c["measured"].values()) - min(v["halluc"] for v in c["measured"].values()), 4) for k, c in out.items()}
    return {"seed": seed, "n": n, "queries": queries, "model": model, "supply": SUPPLY, "variant_p": VARIANT_P,
            "corners": out, "swing_across_corners_by_matcher": swing_by_matcher, "swing_across_matchers_by_corner": swing_by_corner,
            "true_rate_range": [min(c["true_fabrication_rate"] for c in out.values()), max(c["true_fabrication_rate"] for c in out.values())]}


def render(g):
    L = ["seed %d  n %d  queries %d  model %s (constant in every corner)" % (g["seed"], g["n"], g["queries"], g["model"])]
    for k, c in g["corners"].items():
        L.append("%-12s true_fab %.3f | " % (k, c["true_fabrication_rate"]) + "  ".join("%s=%.3f" % (m, v["halluc"]) for m, v in c["measured"].items()))
    L += ["swing across corners, by matcher: %s" % g["swing_across_corners_by_matcher"],
          "swing across matchers, by corner: %s" % g["swing_across_matchers_by_corner"],
          "true fabrication rate range across corners: %s  <- the part that is g(model) + contract" % g["true_rate_range"]]
    return "\n".join(L)


def selftest():
    g = grid(1, queries=30)
    c = g["corners"]
    assert c["dense/high"]["measured"]["exact"]["halluc"] == c["dense/high"]["true_fabrication_rate"]  # verbatim titles: exact recovers the truth
    assert c["dense/high"]["measured"]["exact"]["halluc"] < 0.2  # = error + (1 - recall) under fill-to-N, the constant term
    assert c["sparse/high"]["measured"]["exact"]["halluc"] > 0.6          # deficit under v1: the contract, not the model
    assert c["dense/low"]["measured"]["exact"]["halluc"] > c["dense/high"]["measured"]["exact"]["halluc"] + 0.3  # canonicality via matcher
    assert c["dense/low"]["measured"]["edit"]["halluc"] < c["dense/low"]["measured"]["exact"]["halluc"]
    assert abs(c["dense/low"]["true_fabrication_rate"] - c["dense/high"]["true_fabrication_rate"]) < 0.1
    assert g["swing_across_corners_by_matcher"]["exact"] > 0.5
    assert grid(1, queries=30) == g
    print("synthetic_catalog selftest: 7 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if "--help" in argv or "--seed" not in argv:
        print(__doc__)
        return 2
    seed = int(argv[argv.index("--seed") + 1])
    n = int(argv[argv.index("--n") + 1]) if "--n" in argv else 10
    q = int(argv[argv.index("--queries") + 1]) if "--queries" in argv else 50
    g = grid(seed, n, q)
    print(json.dumps(g, indent=1, sort_keys=True) if "--json" in argv else render(g))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
