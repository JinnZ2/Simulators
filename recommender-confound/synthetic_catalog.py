"""B) synthetic_catalog.py -- null construction for the 0.6% -> 61%
finding. No data required. A 2x2 grid, density x title_canonicality,
four corners, one matcher set, MODEL ACCURACY HELD CONSTANT across all
four. What moves the measured number is then h and m alone.

The synthetic model, identical in every corner:
  recall         fraction of the available supply it produces correctly
  fab_on_recall  fraction of produced items that are fabricated even with
                 supply available (a model property, constant)
  collision      fraction of fabricated slots that name a REAL catalog
                 item which is not an answer (WORK_ORDER_02 task 2); every
                 matcher scores it a MATCH, so the fabrication is hidden.
                 At 0 (default) no distractors exist and seed 1 reproduces.
  contract       v1: fill to N regardless of supply (deficit -> fabricate)
Corners:
  density        sparse: supply < N        dense: supply >> N
  canonicality   low: true titles rendered as variants (case, punctuation,
                 dropped article, dropped subtitle, typo, year suffix)
                 high: rendered verbatim
Every constant is a [MODEL] parameter and printed. Seeded.

Per corner x matcher: measured halluc (miss / N), the TRUE fabrication
rate the model committed, measured_minus_true SIGNED, the count of
fabrications each matcher hid, and the count of true items it missed.
produce() accepts a separate render stream so two canonicality levels
can share one model stream exactly (multiseed.py uses it).

Command: python3 synthetic_catalog.py --seed 1 [--n 10] [--queries 50] [--collision 0.3] [--json]
         python3 synthetic_catalog.py --selftest
"""
import json
import random
import sys

from matchers import DEFAULT_SET, classify

WORDS = ("river", "signal", "harbor", "lantern", "meridian", "quarry", "ember", "cistern", "gantry",
         "furrow", "halyard", "kestrel", "mica", "pinion", "sable", "tallow", "vellum", "wicket", "zenith", "basalt")
MODEL = {"recall": 0.9, "fab_on_recall": 0.05, "collision": 0.0}   # [MODEL] constant across corners
SUPPLY = {"sparse": 3, "dense": 40}              # [MODEL] answers available per query
VARIANT_P = {"low": 0.8, "high": 0.0}            # [MODEL] chance a true title is rendered non-canonically
DISTRACTORS = 40                                 # [MODEL] real, non-answer items; present only when collision > 0


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


def make_distractors(rng, n, tag):
    """Real catalog entries that are not answers to the query: the collision cell."""
    return [{"item_id": "%s_x%d" % (tag, k), "title": title(rng, 500 + k), "category": tag, "answer": False} for k in range(n)]


def answers(catalog):
    return [it for it in catalog if it.get("answer", True)]


def fabricated(rng, catalog, model):
    dis = [it for it in catalog if not it.get("answer", True)]
    if dis and rng.random() < model.get("collision", 0.0):
        return rng.choice(dis)["title"]
    titles = set(it["title"] for it in catalog)
    while True:
        t = title(rng, rng.randrange(1000, 9999))
        if t not in titles:
            return t


def produce(rng, catalog, n, canon, model, contract="v1", render_rng=None):
    """One query -> (items, n_true_fabricated, supply_estimate, fab_flags)."""
    rr = render_rng or rng
    ans = answers(catalog)
    supply = len(ans)
    recalled = [it["title"] for it in rng.sample(ans, min(supply, n)) if rng.random() < model["recall"]]
    items, flags = [], []
    for t in recalled:
        if rng.random() < model["fab_on_recall"]:
            items.append(fabricated(rng, catalog, model)); flags.append(True)
        else:
            items.append(variant(rr, t) if rr.random() < VARIANT_P[canon] else t); flags.append(False)
    if contract == "v1":
        while len(items) < n:
            items.append(fabricated(rng, catalog, model)); flags.append(True)
    return items, sum(flags), supply, flags


def corner(rng, dens, canon, n, queries, matchers, model, render_rng=None, cat=None):
    tag = "%s_%s" % (dens, canon)
    if cat is None:
        cat = make_catalog(rng, SUPPLY[dens], tag)
        if model.get("collision", 0.0) > 0:
            cat += make_distractors(rng, DISTRACTORS, tag)
    all_items, flags = [], []
    for _ in range(queries):
        items, _f, _s, fl = produce(rng, cat, n, canon, model, "v1", render_rng)
        all_items += items; flags += fl
    total = len(all_items)
    true_rate = round(sum(flags) / float(total), 4)
    cell = {"true_fabrication_rate": true_rate, "n_items": total, "measured": {}}
    for m in matchers:
        kinds = [classify(s, cat, m)[0] for s in all_items]
        miss = sum(1 for k in kinds if k == "miss")
        meas = round(miss / float(total), 4)
        cell["measured"][m] = {"halluc": meas, "measured_minus_true": round(meas - true_rate, 4),
                               "fabrications_hidden_by_matcher": sum(1 for k, f in zip(kinds, flags) if f and k == "match"),
                               "true_items_missed_by_matcher": sum(1 for k, f in zip(kinds, flags) if not f and k != "match")}
    return cell


def grid(seed, n=10, queries=50, matchers=DEFAULT_SET, model=MODEL, collision=None):
    model = dict(model, collision=model.get("collision", 0.0) if collision is None else collision)
    rng = random.Random(seed)
    out = {}
    for dens in ("sparse", "dense"):
        for canon in ("low", "high"):
            out["%s/%s" % (dens, canon)] = corner(rng, dens, canon, n, queries, matchers, model)
    sbm = {m: round(max(c["measured"][m]["halluc"] for c in out.values()) - min(c["measured"][m]["halluc"] for c in out.values()), 4) for m in matchers}
    sbc = {k: round(max(v["halluc"] for v in c["measured"].values()) - min(v["halluc"] for v in c["measured"].values()), 4) for k, c in out.items()}
    return {"seed": seed, "n": n, "queries": queries, "model": model, "supply": SUPPLY, "variant_p": VARIANT_P,
            "distractors": DISTRACTORS if model["collision"] > 0 else 0, "corners": out,
            "swing_across_corners_by_matcher": sbm, "swing_across_matchers_by_corner": sbc,
            "true_rate_range": [min(c["true_fabrication_rate"] for c in out.values()), max(c["true_fabrication_rate"] for c in out.values())],
            "any_measured_below_true": any(v["measured_minus_true"] < 0 for c in out.values() for v in c["measured"].values())}


def render(g):
    L = ["seed %d  n %d  queries %d  model %s (constant in every corner)" % (g["seed"], g["n"], g["queries"], g["model"])]
    for k, c in g["corners"].items():
        L.append("%-12s true_fab %.3f | " % (k, c["true_fabrication_rate"]) + "  ".join("%s=%.3f(%+.3f)" % (m, v["halluc"], v["measured_minus_true"]) for m, v in c["measured"].items()))
        L.append("%-12s   fabrications hidden by matcher %s" % ("", {m: v["fabrications_hidden_by_matcher"] for m, v in c["measured"].items()}))
    L += ["swing across corners, by matcher: %s" % g["swing_across_corners_by_matcher"],
          "swing across matchers, by corner: %s" % g["swing_across_matchers_by_corner"],
          "true fabrication rate range across corners: %s  <- the part that is g(model) + contract" % g["true_rate_range"],
          "collision %s, distractors %d, any measured below true: %s" % (g["model"]["collision"], g["distractors"], g["any_measured_below_true"])]
    return "\n".join(L)


def selftest():
    g = grid(1, queries=30)
    c = g["corners"]
    assert c["dense/high"]["measured"]["exact"]["halluc"] == c["dense/high"]["true_fabrication_rate"]
    assert c["dense/high"]["measured"]["exact"]["halluc"] < 0.2
    assert c["sparse/high"]["measured"]["exact"]["halluc"] > 0.6
    assert c["dense/low"]["measured"]["exact"]["halluc"] > c["dense/high"]["measured"]["exact"]["halluc"] + 0.3
    assert c["dense/low"]["measured"]["edit"]["halluc"] < c["dense/low"]["measured"]["exact"]["halluc"]
    assert abs(c["dense/low"]["true_fabrication_rate"] - c["dense/high"]["true_fabrication_rate"]) < 0.1
    assert g["swing_across_corners_by_matcher"]["exact"] > 0.5
    assert grid(1, queries=30) == g
    # collision 0: exact cannot deflate (fabricated() excludes exact titles); loose matchers can, by accident
    assert all(cc["measured"]["exact"]["measured_minus_true"] >= 0 for cc in c.values())
    assert all(cc["measured"]["exact"]["fabrications_hidden_by_matcher"] == 0 for cc in c.values())
    gc = grid(1, queries=30, collision=0.5)
    sh = gc["corners"]["sparse/high"]["measured"]["exact"]
    assert gc["any_measured_below_true"] and sh["measured_minus_true"] < 0 and sh["fabrications_hidden_by_matcher"] > 0
    # paired streams: one model stream, one render stream -> the true rate cannot differ between canonicality levels
    rows = {}
    for canon in ("low", "high"):
        rows[canon] = corner(random.Random(7), "dense", canon, 10, 30, ("exact",), MODEL, render_rng=random.Random(99))
    assert rows["low"]["true_fabrication_rate"] == rows["high"]["true_fabrication_rate"]
    print("synthetic_catalog selftest: 11 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if "--help" in argv or "--seed" not in argv:
        print(__doc__)
        return 2
    seed = int(argv[argv.index("--seed") + 1])
    n = int(argv[argv.index("--n") + 1]) if "--n" in argv else 10
    q = int(argv[argv.index("--queries") + 1]) if "--queries" in argv else 50
    col = float(argv[argv.index("--collision") + 1]) if "--collision" in argv else None
    g = grid(seed, n, q, collision=col)
    print(json.dumps(g, indent=1, sort_keys=True) if "--json" in argv else render(g))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
