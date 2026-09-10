#!/usr/bin/env python3
"""normalize.py -- quantity strings to measurand groups under a PUBLISHED
transform list (WORK ORDER, section 6).

    normalize:  strip units, articles, hedges
    group:      SAME measurand if one is a transform of the other under
                {integrate, differentiate, aggregate, disaggregate,
                 threshold, re-scope in time or population}
                DIFFERENT if converting needs a coefficient, model, or a
                measurement the method does not contain

Mechanically: aliases (longest phrase first) -> tokens -> drop units,
articles, hedges and every transform-marker token -> the residue is the
CORE. Two cores are one measurand if equal, or (subset_rule) if one is a
subset of the other and the extra tokens are all unclassified residue
(see _same). Union-find, so grouping is transitive; the second list
(N4) differs in which tokens count as measurand vocabulary.

A core emptied by stripping is UNRESOLVED: counted apart, never a
measurand. A token surviving that is not a canonical alias value is
UNKNOWN: reported so a reader can extend the list and rescore. Both are
the scorer's limits stated where they occur.

Every list is scored TWICE (score.CHOICES[9]): once with unknown tokens
as residue (the subset rule may absorb them; crossing_count, the floor)
and once with unknown tokens as measurand vocabulary (only equal cores
group; crossing_count_max, the ceiling). An unknown token sharing a
native token was absorbed into the native group under the first rule
alone, a signed undercount (WORK_ORDER_2 W3). No entries at all gives
None on every crossing field, never 0 (CHOICES[12]).

Stdlib only. No model, no network. Imported by score.py.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PRIMARY = os.path.join(HERE, "transforms.json")
ALT = os.path.join(HERE, "transforms_alt.json")
TRANSFORMS = ("integrate", "differentiate", "aggregate", "disaggregate",
              "threshold", "rescope")


def load_lexicon(path=PRIMARY):
    with open(path, encoding="utf-8") as fh:
        lex = json.load(fh)
    need = ("name", "subset_rule", "units", "articles", "hedges",
            "transforms", "aliases")
    missing = [k for k in need if k not in lex]
    if missing:
        raise ValueError("lexicon %s missing %s" % (path, missing))
    bad = [t for t in lex["transforms"] if t not in TRANSFORMS]
    if bad:
        raise ValueError("lexicon %s names transforms outside the order's "
                         "list: %s" % (path, bad))
    lex["_drop"] = {}
    for cls in ("units", "articles", "hedges"):
        for tok in lex[cls]:
            lex["_drop"][tok] = cls
    for cls, toks in lex["transforms"].items():
        for tok in toks:
            lex["_drop"][tok] = cls
    lex["_alias"] = sorted(lex["aliases"].items(), key=lambda kv: -len(kv[0]))
    lex["_known"] = set()
    for v in lex["aliases"].values():
        lex["_known"].update(v.split())
    lex["_path"] = path
    return lex


def _singular(tok):
    if len(tok) > 3 and tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok


def normalize(quantity, lex):
    """-> (core frozenset, record). record lists what was stripped and why."""
    s = quantity.lower().replace("µ", "u")
    s = re.sub(r"\(.*?\)", " ", s)            # [CHOICE 8] parentheticals are glosses/units (score.CHOICES)
    s = s.replace("/", " per ").replace("-", " ").replace("_", " ")
    holds = []
    for phrase, canon in lex["_alias"]:      # longest first; a replaced span is
        def _hold(m, canon=canon):           # held so a shorter alias cannot
            holds.append(canon)              # match inside it
            return " \x00%d\x00 " % (len(holds) - 1)
        s = re.sub(r"\b%s\b" % re.escape(phrase), _hold, s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: holds[int(m.group(1))], s)
    toks = re.findall(r"[a-z0-9][a-z0-9\-]*", s)
    core, stripped, unknown = [], [], []
    for tok in toks:
        if tok.isdigit() or len(tok) == 1:
            stripped.append((tok, "numeral-or-letter"))
            continue
        cls = lex["_drop"].get(tok) or lex["_drop"].get(_singular(tok))
        if cls and tok not in lex["_known"]:
            stripped.append((tok, cls))
            continue
        tok2 = tok if tok in lex["_known"] else _singular(tok)
        core.append(tok2)
        if tok2 not in lex["_known"]:
            unknown.append(tok2)
    return frozenset(core), {"quantity": quantity, "core": sorted(core),
                             "stripped": stripped, "unknown": unknown}


def _same(a, b, lex, unknown_is_vocab=False):
    """equal cores are one measurand. Under subset_rule a core contained in
    another is the same measurand ONLY when the larger core's extra tokens
    are all UNCLASSIFIED (descriptive residue such as 'dry combustion');
    an extra token that is measurand vocabulary (a canonical alias value:
    hazard, migration, co2e ...) makes it a different quantity. Without
    that clause a one-token native like {polymer} absorbs every quantity
    that mentions polymer, which is the chaining the first draft did.
    With unknown_is_vocab every surviving token is vocabulary, so only
    equal cores group: the ceiling end of the band (CHOICES[9])."""
    if a == b:
        return True
    if not lex["subset_rule"] or unknown_is_vocab:
        return False
    small, large = (a, b) if a <= b else (b, a) if b <= a else (None, None)
    if small is None:
        return False
    return not ((large - small) & lex["_known"])


def group(cores, lex, unknown_is_vocab=False):
    """union-find over a list of cores -> list of group ids (int)."""
    parent = list(range(len(cores)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(cores)):
        if not cores[i]:
            continue
        for j in range(i + 1, len(cores)):
            if not cores[j]:
                continue
            if _same(cores[i], cores[j], lex, unknown_is_vocab):
                parent[find(i)] = find(j)
    return [find(i) if cores[i] else None for i in range(len(cores))]


def _score_mode(recs, nrecs, quantities, lex, unknown_is_vocab):
    cores = [r[0] for r in recs] + [r[0] for r in nrecs]
    gids = group(cores, lex, unknown_is_vocab)
    n = len(quantities)
    entry_groups = set(g for g in gids[:n] if g is not None)
    native_groups = set(g for g in gids[n:] if g is not None)
    hit = entry_groups & native_groups
    members = {}
    for i, g in enumerate(gids[:n]):
        if g is not None:
            members.setdefault(g, []).append(quantities[i])
    distinct = len(entry_groups)
    return {"distinct": distinct, "native_groups_hit": len(hit), "native_hit": 1 if hit else 0,
            "crossing": distinct - len(hit), "crossing_order": distinct - (1 if hit else 0),
            "unresolved": sum(1 for g in gids[:n] if g is None),
            "groups": [{"native": g in native_groups, "quantities": qs} for g, qs in sorted(members.items())],
            "gids": gids[:n]}


def score(quantities, native, lex):
    """WORK ORDER section 6, per response. `native` may be disjunctive
    ('a or b'): every native measurand is a native measurand group.

    native_hit         1 if any entry is in a native group (the order's form)
    native_groups_hit  how many native groups the entries reach; this is what
                       crossing_count subtracts, because a native stated as
                       'count OR mass' names two measurands and entries on
                       both are not one crossing. [CHOICE 3] printed in
                       reports; crossing_count_order keeps the order's form.
    crossing_count     unknown tokens as residue (the floor)      [CHOICE 9]
    crossing_count_max unknown tokens as measurand vocabulary (the ceiling)
    No entries -> every crossing field is None: ABSENT, not 0  [CHOICE 12]
    """
    natives = [n.strip() for n in re.split(r"\bor\b", native) if n.strip()]
    recs = [normalize(q, lex) for q in quantities]
    nrecs = [normalize(n, lex) for n in natives]
    n = len(quantities)
    base = {"n_entries": n, "unknown_tokens": sorted(set(t for r in recs for t in r[1]["unknown"])),
            "native_cores": [sorted(r[0]) for r in nrecs], "lexicon": lex["name"]}
    if n == 0:
        base.update({"distinct_measurands": 0, "distinct_measurands_max": 0, "native_hit": 0,
                     "native_hit_max": 0, "native_groups_hit": 0, "native_groups_hit_max": 0,
                     "crossing_count": None, "crossing_count_order": None, "crossing_count_max": None,
                     "unresolved": 0, "groups": [], "groups_max": [], "absent": True})
        return base
    lo = _score_mode(recs, nrecs, quantities, lex, False)
    hi = _score_mode(recs, nrecs, quantities, lex, True)
    base.update({"distinct_measurands": lo["distinct"], "distinct_measurands_max": hi["distinct"],
                 "native_hit": lo["native_hit"], "native_hit_max": hi["native_hit"],
                 "native_groups_hit": lo["native_groups_hit"], "native_groups_hit_max": hi["native_groups_hit"],
                 "crossing_count": lo["crossing"], "crossing_count_order": lo["crossing_order"],
                 "crossing_count_max": hi["crossing"], "unresolved": lo["unresolved"],
                 "groups": lo["groups"], "groups_max": hi["groups"], "absent": False})
    return base


def measurand_sets(list_a, list_b, native, lex, unknown_is_vocab=False):
    """Group the UNION of two quantity lists once and return the set of
    group ids each list reaches, so a strict-superset test (AP-4) runs on
    measurands and not on strings (WORK_ORDER_2 W5). Returns
    (set_a, set_b, names) with names: gid -> its quantities."""
    qs = list(list_a) + list(list_b)
    natives = [n.strip() for n in re.split(r"\bor\b", native) if n.strip()]
    recs = [normalize(q, lex) for q in qs]
    nrecs = [normalize(n, lex) for n in natives]
    r = _score_mode(recs, nrecs, qs, lex, unknown_is_vocab)
    gids = r["gids"]
    a = set(g for g in gids[:len(list_a)] if g is not None)
    b = set(g for g in gids[len(list_a):] if g is not None)
    names = {}
    for q, g in zip(qs, gids):
        if g is not None:
            names.setdefault(g, []).append(q)
    return a, b, names


def names_unit_or_measurand(text, lex, extra=("count", "mass")):
    """Token-level: does `text` name a unit (from the lexicon's own unit
    list, singular or plural) or a listed measurand word? A substring
    test read 'count' inside 'account' and 'ug' inside 'drug' and missed
    'tonnes', 'kg', 'ha' (WORK_ORDER_2 W8). Returns the tokens that fire."""
    toks = re.findall(r"[a-z0-9][a-z0-9\-]*", text.lower().replace("µ", "u").replace("/", " per "))
    units = set(lex["units"])
    hits = []
    for tok in toks:
        if tok in units or _singular(tok) in units or tok in extra or _singular(tok) in extra:
            hits.append(tok)
    return hits


def crossing_count(quantities, native, lex=None):
    """registered in tools/known_answer.py. None on no entries: absent, not 0."""
    return score(quantities, native, lex or load_lexicon())["crossing_count"]


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit("normalize.py is a library; run: python3 score.py --selftest")
    lex = load_lexicon()
    for q in sys.argv[1:]:
        print(json.dumps(normalize(q, lex)[1]))
