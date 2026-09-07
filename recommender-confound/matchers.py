"""String matchers shared by confound_probe, synthetic_catalog,
abstention_channel and slot_map. Every matcher maps one produced string
onto a catalog and returns the set of item_ids it hits. A hit set of
size 1 is a MATCH, size 0 a MISS, size >1 AMBIGUOUS -- reported apart,
never folded into either. The matcher is the m in g x h x m; a
hallucination rate quoted without naming it is a number with a hidden
factor.

Catalog rows: {item_id, title, aliases?: [..], category?: str}
Command: python3 matchers.py --selftest
"""
import json
import re
import sys

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def norm(s):
    return " ".join(_PUNCT.sub(" ", s.casefold()).split())


def alnum(s):
    return "".join(ch for ch in s.casefold() if ch.isalnum())


def tokens(s):
    return set(norm(s).split())


def levenshtein(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _names(item):
    return [item["title"]] + list(item.get("aliases", []))


def m_exact(cand, catalog):
    return {it["item_id"] for it in catalog if cand in _names(it)}


def m_norm(cand, catalog):
    c = norm(cand)
    return {it["item_id"] for it in catalog if c in [norm(n) for n in _names(it)]}


def m_alnum(cand, catalog):
    c = alnum(cand)
    return {it["item_id"] for it in catalog if c and c in [alnum(n) for n in _names(it)]}


def m_substring(cand, catalog):
    c = norm(cand)
    out = set()
    for it in catalog:
        for n in _names(it):
            nn = norm(n)
            if c and nn and (c in nn or nn in c):
                out.add(it["item_id"])
    return out


def m_jaccard(cand, catalog, theta=0.6):
    t = tokens(cand)
    out = set()
    for it in catalog:
        for n in _names(it):
            u = tokens(n)
            if t and u and len(t & u) / float(len(t | u)) >= theta:
                out.add(it["item_id"])
    return out


def m_edit(cand, catalog, max_ratio=0.2):
    c = norm(cand)
    out = set()
    for it in catalog:
        for n in _names(it):
            nn = norm(n)
            m = max(len(c), len(nn))
            if m and levenshtein(c, nn) / float(m) <= max_ratio:
                out.add(it["item_id"])
    return out


MATCHERS = {"exact": m_exact, "norm": m_norm, "alnum": m_alnum, "substring": m_substring,
            "jaccard": m_jaccard, "edit": m_edit}
DEFAULT_SET = ("exact", "norm", "alnum", "jaccard", "edit", "substring")


def classify(cand, catalog, matcher):
    hits = MATCHERS[matcher](cand, catalog)
    return ("match" if len(hits) == 1 else "ambiguous" if hits else "miss"), hits


def score_list(items, catalog, matcher):
    """Counts over one produced list: match / miss / ambiguous, plus the
    hallucination rate under the strict reading (miss / n) and the loose
    one ((miss + ambiguous) / n). Both printed; neither is the number."""
    c = {"match": 0, "miss": 0, "ambiguous": 0}
    for s in items:
        c[classify(s, catalog, matcher)[0]] += 1
    n = len(items)
    return dict(c, n=n, halluc_strict=(c["miss"] / float(n)) if n else None,
                halluc_loose=((c["miss"] + c["ambiguous"]) / float(n)) if n else None)


def selftest():
    cat = [{"item_id": "a", "title": "The Left Hand of Darkness", "aliases": ["Left Hand of Darkness"]},
           {"item_id": "b", "title": "The Dispossessed"}, {"item_id": "c", "title": "The Lathe of Heaven"}]
    checks = 0
    assert classify("The Dispossessed", cat, "exact")[0] == "match"; checks += 1
    assert classify("the dispossessed", cat, "exact")[0] == "miss"; checks += 1
    assert classify("the dispossessed.", cat, "norm")[0] == "match"; checks += 1
    assert classify("Left Hand of Darkness", cat, "exact")[0] == "match"; checks += 1  # alias
    assert classify("The", cat, "substring")[0] == "ambiguous"; checks += 1
    assert classify("The Lathe of Heavan", cat, "edit")[0] == "match"; checks += 1
    assert classify("The Lathe of Heavan", cat, "norm")[0] == "miss"; checks += 1
    assert classify("A Wizard of Earthsea", cat, "jaccard")[0] == "miss"; checks += 1
    s = score_list(["The Dispossessed", "The", "Nowhere Book"], cat, "substring")
    assert (s["match"], s["ambiguous"], s["miss"]) == (1, 1, 1) and s["halluc_strict"] < s["halluc_loose"]; checks += 1
    assert levenshtein("kitten", "sitting") == 3; checks += 1
    assert score_list([], cat, "exact")["halluc_strict"] is None; checks += 1
    print("matchers selftest: %d checks OK" % checks)


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        print(__doc__)
