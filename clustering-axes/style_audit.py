#!/usr/bin/env python3
"""Checks on the delivered `style_index.py` and `ROUTES.md`.

The module is imported and the routes document is read; neither is
modified.

The design constraint is the right one and is the point of the folder:
**no model in the measurement loop**, because the work it is aimed at
scores its clustering variable with a zero-shot classifier and so
cannot separate *agents cluster on X* from *the scorer reads X*.
Everything checked here is downstream of that, and none of it disputes
it.

What this measures, on text already in this repository, since no agent
corpus is reachable from here:

  SCALE       what the shipped `--delta` command actually computes,
              feature by feature, as a share of the distance
  KEY SET     whether two style vectors live in the same feature space
  EDGES       empty input, one word, no punctuation
  COUNT       the routes document's stated "159 countable features"

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import style_index as S  # noqa: E402

ROUTES = os.path.join(HERE, "ROUTES.md")

# Text already in this tree. Not agent posts -- no agent corpus is
# reachable from here, and that is stated rather than worked around.
# What these are good for is the SHAPE of the instrument's output,
# which is a property of the code and not of the corpus.
SAMPLES = ["README.md", "CLAUDE.md", "clustering-axes/ROUTES.md",
           "PREAMBLE.md", "PROTOCOL.md"]


def _read(rel, limit=6000):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8", errors="replace").read()[:limit]


def vectors():
    out = {}
    for rel in SAMPLES:
        t = _read(rel)
        if t:
            out[rel] = S.style_vector(t)
    return out


def contribution(a, b):
    """Per-feature share of the no-corpus L1 distance, largest first."""
    keys = sorted(set(a) & set(b))
    rows = sorted(((abs(a[k] - b[k]), k) for k in keys), reverse=True)
    tot = sum(c for c, _k in rows) or 1e-12
    return [(k, c, c / tot) for c, k in rows], tot, len(keys)


def block_of(key):
    if key.startswith("fw_"):
        return "function words"
    if key.startswith("p_"):
        return "punctuation"
    if key.startswith("t_"):
        return "trigrams"
    if key in ("mean_word_len", "mean_sent_len", "sent_len_sd",
               "mean_line_len"):
        return "UNNORMALISED shape"
    return "other rates"


def block_shares(a, b):
    rows, _tot, _n = contribution(a, b)
    out = {}
    for k, _c, sh in rows:
        out[block_of(k)] = out.get(block_of(k), 0.0) + sh
    return out


def key_overlap(vs):
    """Do two vectors live in the same feature space?"""
    names = sorted(vs)
    out = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = set(vs[names[i]]), set(vs[names[j]])
            out.append({"pair": (names[i], names[j]), "a": len(a),
                        "b": len(b), "shared": len(a & b),
                        "union": len(a | b)})
    return out


def corpus_shares(vs):
    """The same contribution split, with the corpus z-normalisation on.

    This is the constructive half: the delivered `delta` DOES take a
    corpus, and with one the shape features stop dominating. The gap is
    not in the function, it is that the CLI never passes one.
    """
    names = sorted(vs)
    corpus = [vs[n] for n in names]
    a, b = vs[names[0]], vs[names[1]]
    keys = sorted(set(a) & set(b))
    rows = []
    for k in keys:
        col = [c.get(k, 0.0) for c in corpus]
        m = sum(col) / len(col)
        s = S._sd(col) or 1e-9
        rows.append((k, abs((a[k] - m) / s - (b[k] - m) / s)))
    tot = sum(c for _k, c in rows) or 1e-12
    out = {}
    for k, c in rows:
        out[block_of(k)] = out.get(block_of(k), 0.0) + c / tot
    return out


def edges():
    """Inputs a real crawl will contain."""
    cases = {
        "empty": "",
        "one word": "hello",
        "one char": "x",
        "no punctuation": "the quick brown fox jumps over the lazy dog",
        "only punctuation": "!!! ??? ...",
        "only newlines": "\n\n\n",
        "unicode": "你好 世界 — …",
    }
    out = {}
    for name, t in cases.items():
        try:
            v = S.style_vector(t)
            out[name] = {"ok": True, "features": len(v),
                         "finite": all(isinstance(x, float) or
                                       isinstance(x, int) for x in v.values())}
        except Exception as exc:                          # noqa: BLE001
            out[name] = {"ok": False,
                         "error": "%s: %s" % (type(exc).__name__, exc)}
    return out


def cli(args):
    p = subprocess.run([sys.executable, os.path.join(HERE, "style_index.py")]
                       + args, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=120)
    return p.returncode, p.stdout.decode("utf8", "replace")


def routes_facts():
    """Statements in ROUTES.md that are checkable against the module."""
    txt = open(ROUTES, encoding="utf-8").read()
    stated = re.search(r"(\d+) countable features", txt)
    long_text = _read("CLAUDE.md")
    return {
        "stated_features": int(stated.group(1)) if stated else None,
        "observed_on_long_text": len(S.style_vector(long_text)) if long_text
        else None,
        "observed_on_short_text": len(S.style_vector("the cat sat")),
        "func_words": len(S.FUNC),
        "punct_marks": len(S.PUNCT),
        "trigram_slots": 40,
        "claims_burrows": "Burrows's Delta" in txt,
    }


# ------------------------------------------------------------- report

def render():
    out = []
    out.append("STYLE INDEX AUDIT")
    out.append("the module is imported and the routes document read;")
    out.append("neither is modified")
    out.append("")
    out.append("No agent corpus is reachable from here. Everything below")
    out.append("is measured on text already in this repository, and every")
    out.append("finding is a property of the instrument rather than of")
    out.append("any corpus.")
    out.append("")

    rf = routes_facts()
    out.append("1. THE STATED FEATURE COUNT HOLDS, AS A CEILING")
    out.append("   ROUTES.md states %s countable features."
               % rf["stated_features"])
    out.append("   observed on a long text: %d" % rf["observed_on_long_text"])
    out.append("     %d function words + %d punctuation + %d trigram slots"
               % (rf["func_words"], rf["punct_marks"], rf["trigram_slots"]))
    out.append("     + 17 shape and rate features = %d"
               % (rf["func_words"] + rf["punct_marks"] + 40 + 17))
    out.append("   observed on `the cat sat`: %d"
               % rf["observed_on_short_text"])
    out.append("   The trigram block is `most_common(40)`, so a text with")
    out.append("   fewer than 40 distinct trigrams yields fewer features.")
    out.append("   159 is the ceiling, reached by any text of ordinary")
    out.append("   length, and not a constant.")
    out.append("")

    vs = vectors()
    names = sorted(vs)
    out.append("2. WHAT THE SHIPPED COMMAND ACTUALLY MEASURES")
    a, b = vs[names[0]], vs[names[1]]
    rows, tot, nk = contribution(a, b)
    out.append("   %s vs %s, no corpus -- the only path `--delta` takes:"
               % (names[0], names[1]))
    out.append("     shared features %d, total L1 %.4f" % (nk, tot))
    for k, c, sh in rows[:5]:
        out.append("     %-16s %10.4f  %5.1f%%   [%s]"
                   % (k, c, 100 * sh, block_of(k)))
    bs = block_shares(a, b)
    out.append("   by block:")
    for blk in sorted(bs, key=lambda x: -bs[x]):
        out.append("     %-22s %6.2f%%" % (blk, 100 * bs[blk]))
    out.append("")
    out.append("   The function-word profile is the topic-blind core the")
    out.append("   whole design rests on. Under the shipped command it is")
    out.append("   under one part in forty against four features carried")
    out.append("   in their raw units -- characters and words per sentence.")
    out.append("")

    out.append("3. THE CORPUS PATH REVERSES IT, AND THE CLI NEVER TAKES IT")
    cs = corpus_shares(vs)
    out.append("   same pair, z-normalised over %d vectors:" % len(vs))
    for blk in sorted(cs, key=lambda x: -cs[x]):
        out.append("     %-22s %6.2f%%" % (blk, 100 * cs[blk]))
    out.append("   `delta(a, b, corpus=...)` is implemented and correct.")
    out.append("   `main()` calls `delta(vecs[0], vecs[1])` with no third")
    out.append("   argument, so the documented command never reaches it.")
    out.append("")

    out.append("4. TWO VECTORS DO NOT SHARE A FEATURE SPACE")
    for r in key_overlap(vs)[:6]:
        out.append("     %-28s %-28s a=%d b=%d shared=%d union=%d"
                   % (os.path.basename(r["pair"][0])[:28],
                      os.path.basename(r["pair"][1])[:28],
                      r["a"], r["b"], r["shared"], r["union"]))
    out.append("   `delta` averages over `set(a) & set(b)`, and the")
    out.append("   trigram block is per-text, so the denominator changes")
    out.append("   with the pair. d(a,b) and d(a,c) average over")
    out.append("   different feature sets.")
    out.append("")

    out.append("5. EDGES")
    for name, r in sorted(edges().items()):
        out.append("     %-18s %s" % (name, "%d features" % r["features"]
                                      if r["ok"] else r["error"][:48]))
    out.append("")

    out.append("6. CLI")
    tmp = os.path.join(HERE, "samples", "_probe_a.txt")
    tmp2 = os.path.join(HERE, "samples", "_probe_b.txt")
    open(tmp, "w").write("The cat sat on the mat. It was a fine day.\n")
    open(tmp2, "w").write("- one\n- two\n- three\n")
    try:
        for args, label in (([tmp], "one file"),
                            ([tmp, tmp2, "--delta"], "two files --delta"),
                            ([tmp, "--delta"], "one file --delta"),
                            (["nosuch.txt"], "missing file"),
                            ([], "no argument")):
            rc, o = cli(args)
            last = [x for x in o.strip().split("\n") if x.strip()]
            out.append("     %-22s rc=%-3s %s"
                       % (label, rc, (last[-1] if last else "(no output)")[:44]))
    finally:
        for f in (tmp, tmp2):
            if os.path.exists(f):
                os.remove(f)
    return "\n".join(out)


# ------------------------------------------------------------ selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- 1. the stated count
    rf = routes_facts()
    chk("ROUTES.md states a feature count", rf["stated_features"] == 159)
    chk("the count holds on a long text",
        rf["observed_on_long_text"] == 159)
    chk("the blocks add to it",
        rf["func_words"] + rf["punct_marks"] + 40 + 17 == 159)
    chk("a short text yields fewer",
        rf["observed_on_short_text"] < 159)
    chk("the shortfall is entirely trigrams",
        rf["observed_on_short_text"] ==
        159 - 40 + sum(1 for k in S.style_vector("the cat sat")
                       if k.startswith("t_")))

    # -- 2. scale domination, on a constructed pair with a known answer
    a = S.style_vector("It is a fact. It is a fact. It is a fact.\n")
    b = S.style_vector("It is a fact and it is a fact and it is a fact "
                       "and it is a fact and so on at length.\n")
    bs = block_shares(a, b)
    chk("unnormalised shape dominates a constructed pair",
        bs.get("UNNORMALISED shape", 0) > 0.5)
    chk("function words are a small share of it",
        bs.get("function words", 1.0) < 0.2)

    vs = vectors()
    chk("the repo samples load", len(vs) >= 3)
    names = sorted(vs)
    # Across EVERY pair, not one. The first version fixed a threshold
    # from a single observation ("under one percent") and went red on
    # the next pair at 2.15%. A threshold read off one pair is that
    # pair, not a property.
    shares = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            shares.append(block_shares(vs[names[i]], vs[names[j]]))
    chk("unnormalised shape dominates every real pair",
        all(x.get("UNNORMALISED shape", 0) > 0.85 for x in shares))
    chk("the topic-blind core is a small minority on every pair",
        all(x.get("function words", 1.0) < 0.10 for x in shares))
    chk("shape outweighs function words by at least an order of "
        "magnitude on every pair",
        all(x.get("UNNORMALISED shape", 0)
            > 10 * x.get("function words", 1.0) for x in shares))

    # -- 3. the corpus path is implemented, correct, and unreachable
    cs = corpus_shares(vs)
    chk("z-normalisation removes the domination",
        all(cs.get("UNNORMALISED shape", 1.0)
            < x.get("UNNORMALISED shape", 0) for x in shares))
    src = open(os.path.join(HERE, "style_index.py"), encoding="utf-8").read()
    chk("main calls delta with two arguments only",
        re.search(r"delta\(vecs\[0\],\s*vecs\[1\]\)", src) is not None)
    # AST, not regex. The first version matched `def delta(a, b,
    # corpus=None)` -- the DEFINITION -- as a callsite, which is
    # fold-matrix FM_043's `<-`-in-a-format-string a second time: a
    # pattern matching the wrong syntactic role.
    import ast as _ast
    _tree = _ast.parse(src)
    _calls = [nd for nd in _ast.walk(_tree)
              if isinstance(nd, _ast.Call)
              and getattr(nd.func, "id", None) == "delta"]
    chk("delta is called somewhere in the module", bool(_calls))
    chk("no callsite passes a corpus",
        all(len(nd.args) < 3 and not any(kw.arg == "corpus"
                                         for kw in nd.keywords)
            for nd in _calls))
    # ...and the detector must be able to say yes.
    _probe = _ast.parse("delta(a, b, corpus=c)\n")
    chk("the callsite detector fires on a real corpus call",
        any(any(kw.arg == "corpus" for kw in nd.keywords)
            for nd in _ast.walk(_probe) if isinstance(nd, _ast.Call)))
    chk("delta with a corpus differs from delta without one",
        abs(S.delta(vs[names[0]], vs[names[1]],
                    [vs[n] for n in names])
            - S.delta(vs[names[0]], vs[names[1]])) > 1e-6)

    # -- 4. feature spaces differ
    ov = key_overlap(vs)
    chk("at least one pair does not share every feature",
        any(r["shared"] < r["union"] for r in ov))
    chk("the difference is in the trigram block",
        all(set(k for k in vs[r["pair"][0]] if not k.startswith("t_"))
            == set(k for k in vs[r["pair"][1]] if not k.startswith("t_"))
            for r in ov))

    # -- 5. edges: nothing raises, and empty input is handled
    e = edges()
    chk("no edge case raises", all(r["ok"] for r in e.values()))
    chk("empty input returns a vector", e["empty"]["features"] > 0)
    chk("a one-character text returns a vector", e["one char"]["ok"])
    chk("every value is a number", all(r.get("finite", False)
                                       for r in e.values() if r["ok"]))

    # -- 6. CLI
    tmp = os.path.join(HERE, "samples", "_st_a.txt")
    open(tmp, "w").write("The cat sat on the mat.\n")
    try:
        rc, o = cli([tmp])
        chk("one file exits 0 and emits JSON", rc == 0 and o.strip()[0] == "{")
        rc, o = cli([tmp, "--delta"])
        chk("--delta with one file silently emits the vector instead "
            "of a delta", rc == 0 and "delta" not in json.loads(o))
        rc, o = cli(["nosuch_xyz.txt"])
        chk("a missing file raises rather than reporting",
            rc != 0 and "FileNotFoundError" in o)
        rc, o = cli([])
        chk("no argument emits an empty object, not usage",
            rc == 0 and json.loads(o) == {})
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    # -- the module is model-free, which is the whole design constraint
    chk("no network or model import anywhere in the module",
        not re.search(r"\b(requests|urllib|http|openai|torch|transformers|"
                      r"numpy|sklearn)\b", src))
    chk("the module imports only the standard library",
        set(re.findall(r"^import (\w+)", src, re.M))
        <= {"json", "math", "re", "sys"})

    txt = render()
    chk("render names all six sections",
        all(("%d." % i) in txt for i in range(1, 7)))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b_ in bad:
        print("  FAILED", b_)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
