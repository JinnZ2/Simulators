#!/usr/bin/env python3
"""P3 -- comprehension check. For one term, a co-occurrence profile per
source document (window +-k), pairwise cosine between sources in pure
Python, the mean as the consistency reading, and the null built in the
same script. Reads a directory of local text files; no introspection,
no network.

    python3 p3_comprehension.py --corpus DIR --term mass --out consistency.json
    python3 p3_comprehension.py --corpus DIR --term mass --null shuffle

`--null shuffle` [CHOICE 3] randomises the term-sense assignment across
sources: each source's profile is replaced by the profile of a random
stand-in token from that source, so the sources are read as if each used
the term for a different sense. `--null permute` shuffles token order
inside each source and rebuilds the term's own profile. Refuses --selftest.
"""

import argparse
import json
import math
import os
import random
import re
import sys
from collections import Counter

TOKEN = re.compile(r"[a-z][a-z'-]*")

# [CHOICE 1] Function words dropped from profiles. A short hand list; the
# null carries the same list, so the contrast does not depend on it.
STOP = set("""a an the and or of to in on at by for with from as is are was were be been being it its
this that these those there here not no nor but if then than so such which who whom whose what when where
why how all any each both few more most other some own same very can will just do does did done has have
had having into over under out up down off about between through during before after above below again
further once only also may might shall would could too s t we our you your they their them he she his her
i my me one two per via et al e g i""".split())

UNCONSTRUCTABLE = ("adversarially encoded corpus: not a corpus; noise. Unconstructable by definition -- "
                   "a text whose parts contest each other's terms has no shared term to profile, so the "
                   "reading is not zero, it is undefined.")


def tokens(text):
    return TOKEN.findall(text.lower())


def profile(toks, term, k, exclude=()):
    """Counts of context tokens within +-k of each occurrence of `term`,
    dropping STOP, the term itself and anything in `exclude`."""
    prof = Counter()
    n = 0
    drop = set(exclude) | {term}
    for i, t in enumerate(toks):
        if t != term:
            continue
        n += 1
        for j in range(max(0, i - k), min(len(toks), i + k + 1)):
            if j != i and toks[j] not in STOP and toks[j] not in drop:
                prof[toks[j]] += 1
    return prof, n


def cosine(a, b):
    if not a or not b:
        return None
    dot = sum(v * b.get(w, 0) for w, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else None


def mean_pairwise(profiles):
    """Mean cosine over pairs; None when fewer than two profiles or every
    pair is undefined."""
    keys = sorted(profiles)
    vals = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            c = cosine(profiles[keys[i]], profiles[keys[j]])
            if c is not None:
                vals.append(c)
    return (sum(vals) / len(vals)) if vals else None, len(vals)


def read_corpus(path, recursive=False):
    """Local .txt/.md files in DIR, keyed by path relative to DIR."""
    out = {}
    walk = os.walk(path) if recursive else [(path, [], os.listdir(path))]
    for root, _, files in walk:
        for f in sorted(files):
            if f.endswith((".txt", ".md")):
                full = os.path.join(root, f)
                with open(full, encoding="utf-8", errors="replace") as fh:
                    out[os.path.relpath(full, path)] = tokens(fh.read())
    return dict(sorted(out.items()))


def observed(corpus, term, k, min_count):
    profiles, counts, excluded = {}, {}, []
    for name, toks in corpus.items():
        p, n = profile(toks, term, k)
        counts[name] = n
        if n >= min_count and p:
            profiles[name] = p
        else:
            excluded.append(name)
    return profiles, counts, excluded


def null_shuffle(corpus, sources, term, k, min_count, reps, seed):
    """[CHOICE 3] per source, a random stand-in token with count >= the
    term's count there (>= min_count when none has), profiled as the term."""
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        profiles = {}
        for name in sources:
            toks = corpus[name]
            c = Counter(t for t in toks if t not in STOP and t != term)
            need = max(min_count, sum(1 for t in toks if t == term))
            pool = [w for w, n in c.items() if n >= need] or [w for w, n in c.items() if n >= min_count]
            if not pool:
                continue
            stand_in = rng.choice(sorted(pool))
            # the original term is excluded from the stand-in's profile:
            # left in, it is shared by every source and lifts the null
            profiles[name], _ = profile(toks, stand_in, k, exclude=(term,))
        m, _ = mean_pairwise(profiles)
        if m is not None:
            vals.append(m)
    return vals


def null_permute(corpus, sources, term, k, reps, seed):
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        profiles = {}
        for name in sources:
            toks = list(corpus[name])
            rng.shuffle(toks)
            profiles[name], _ = profile(toks, term, k)
        m, _ = mean_pairwise(profiles)
        if m is not None:
            vals.append(m)
    return vals


def summarise(vals, obs):
    if not vals:
        return {"reps": 0, "mean": None, "sd": None, "frac_at_or_above_observed": None, "gap_in_sd": None}
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)) if len(vals) > 1 else 0.0
    frac = (sum(1 for v in vals if v >= obs) / len(vals)) if obs is not None else None
    gap = ((obs - m) / sd) if (obs is not None and sd > 0) else None
    return {"reps": len(vals), "mean": m, "sd": sd, "max": max(vals), "frac_at_or_above_observed": frac, "gap_in_sd": gap}


def run(corpus_dir, term, k=8, min_count=2, null=None, reps=200, seed=0, recursive=False):
    corpus = read_corpus(corpus_dir, recursive)
    profiles, counts, excluded = observed(corpus, term.lower(), k, min_count)
    obs, pairs = mean_pairwise(profiles)
    res = {"corpus": corpus_dir, "term": term, "window": k, "min_count": min_count,
           "sources_total": len(corpus), "sources_profiled": len(profiles), "sources_excluded": excluded,
           "term_counts": counts, "pairs": pairs, "consistency_observed": obs,
           "null": None, "unconstructable_row": UNCONSTRUCTABLE}
    if null:
        src = sorted(profiles)
        vals = null_shuffle(corpus, src, term.lower(), k, min_count, reps, seed) if null == "shuffle" \
            else null_permute(corpus, src, term.lower(), k, reps, seed)
        res["null"] = dict(kind=null, seed=seed, **summarise(vals, obs))
    return res


def render(res):
    L = ["P3 comprehension: term %r over %s" % (res["term"], res["corpus"])]
    L.append("sources %d, profiled %d (min_count %d, window +-%d), pairs %d" % (
        res["sources_total"], res["sources_profiled"], res["min_count"], res["window"], res["pairs"]))
    if res["sources_excluded"]:
        L.append("excluded (term below min_count): " + ", ".join(res["sources_excluded"]))
    o = res["consistency_observed"]
    L.append("consistency observed : " + ("%.4f" % o if o is not None else "undefined (fewer than two profiles)"))
    n = res["null"]
    if n:
        L.append("null (%s, %d reps, seed %d): mean %s  sd %s  max %s  frac >= observed %s  gap %s sd" % (
            n["kind"], n["reps"], n["seed"], _f(n["mean"]), _f(n["sd"]), _f(n.get("max")),
            _f(n["frac_at_or_above_observed"]), _f(n["gap_in_sd"], 1)))
    else:
        L.append("null: not run (pass --null shuffle)")
    L.append(res["unconstructable_row"])
    return "\n".join(L)


def _f(x, d=4):
    return ("%%.%df" % d) % x if isinstance(x, (int, float)) else "undefined"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus")
    ap.add_argument("--term")
    ap.add_argument("--window", type=int, default=8)
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--null", choices=["shuffle", "permute"])
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("p3_comprehension has no selftest; run selftest_csp.py", file=sys.stderr)
        return 2
    if not (a.corpus and a.term):
        print("--corpus DIR and --term WORD are required", file=sys.stderr)
        return 2
    res = run(a.corpus, a.term, a.window, a.min_count, a.null, a.reps, a.seed, a.recursive)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1, sort_keys=True)
    print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
