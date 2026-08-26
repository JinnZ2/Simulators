#!/usr/bin/env python3
# style_index.py  -- CC0, stdlib only, phone-buildable
#
# Style vector for a text sample. NO MODEL IN THE MEASUREMENT LOOP.
#
# Reason for the constraint: the existing agent-clustering work scores
# the clustering variable with a model (zero-shot classifier reading
# linguistic features). That makes the instrument a model, so it
# inherits whatever that model correlates with, and the study cannot
# distinguish "agents cluster on X" from "the scorer reads X".
#
# Everything here is countable. A different lab with a different model
# gets the same numbers off the same text.
#
# usage:  python3 style_index.py sample.txt
#         python3 style_index.py a.txt b.txt --delta

import json
import math
import re
import sys
from collections import Counter

# Function words carry authorial style and almost no topic. This is the
# Burrows's Delta feature set -- established, pre-existing, model-free.
FUNC = """a about all also an and any are as at be been but by can could do
down for from had has have he her his how i if in into is it its me more most
my no not of on one only or other our out over she should so some such than
that the their them then there these they this those through to too up very
was we were what when where which who will with would you your""".split()

PUNCT = list(".,;:!?—-()[]\"'/&*#…")


def _tok(t):
    return re.findall(r"[a-z']+", t.lower())


def style_vector(text):
    toks = _tok(text)
    n = len(toks) or 1
    lines = text.splitlines() or [""]
    sents = [s for s in re.split(r"[.!?]+", text) if s.strip()] or [""]
    words = text.split() or [""]
    chars = len(text) or 1
    tri = Counter(text.lower()[i:i + 3] for i in range(len(text) - 2))

    v = {}
    # 1. function-word profile -- the topic-blind core
    fw = Counter(w for w in toks if w in FUNC)
    for w in FUNC:
        v[f"fw_{w}"] = fw[w] / n
    # 2. shape
    v["mean_word_len"] = sum(len(w) for w in words) / len(words)
    v["mean_sent_len"] = sum(len(s.split()) for s in sents) / len(sents)
    v["sent_len_sd"] = _sd([len(s.split()) for s in sents])
    v["mean_line_len"] = sum(len(l) for l in lines) / len(lines)
    v["ttr"] = len(set(toks)) / n
    v["hapax_rate"] = sum(1 for c in Counter(toks).values() if c == 1) / n
    # 3. surface marks
    for p in PUNCT:
        v[f"p_{p}"] = text.count(p) / chars
    v["caps_rate"] = sum(1 for c in text if c.isupper()) / chars
    v["digit_rate"] = sum(1 for c in text if c.isdigit()) / chars
    v["nonascii_rate"] = sum(1 for c in text if ord(c) > 127) / chars
    v["newline_rate"] = text.count("\n") / chars
    v["blankline_rate"] = sum(1 for l in lines if not l.strip()) / len(lines)
    # 4. formatting habits -- markup is a style choice, not a topic
    v["bullet_rate"] = sum(1 for l in lines if l.lstrip()[:2] in ("- ", "* ")) / len(lines)
    v["numlist_rate"] = sum(1 for l in lines if re.match(r"\s*\d+[.)] ", l)) / len(lines)
    v["fence_rate"] = text.count("```") / max(len(lines), 1)
    v["hashtag_rate"] = len(re.findall(r"#\w", text)) / n
    v["mention_rate"] = len(re.findall(r"@\w", text)) / n
    v["url_rate"] = len(re.findall(r"https?://", text)) / n
    # 5. character trigrams -- catches rhythm no word list reaches
    for g, c in tri.most_common(40):
        v[f"t_{g}"] = c / max(len(text) - 2, 1)
    return v


def _sd(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def delta(a, b, corpus=None):
    """
    Burrows's Delta: mean absolute difference in z-scores over shared
    features. corpus = list of style vectors used for the z-normalization.
    With no corpus, falls back to raw L1 -- weaker, still model-free.
    """
    keys = sorted(set(a) & set(b))
    if not corpus:
        return sum(abs(a[k] - b[k]) for k in keys) / max(len(keys), 1)
    out = 0.0
    for k in keys:
        col = [c.get(k, 0.0) for c in corpus]
        m = sum(col) / len(col)
        s = _sd(col) or 1e-9
        out += abs((a[k] - m) / s - (b[k] - m) / s)
    return out / max(len(keys), 1)


def main(argv):
    paths = [p for p in argv[1:] if not p.startswith("--")]
    vecs = [style_vector(open(p, encoding="utf-8", errors="replace").read())
            for p in paths]
    if "--delta" in argv and len(vecs) == 2:
        print(json.dumps({"delta": delta(vecs[0], vecs[1])}, indent=2))
    else:
        print(json.dumps(dict(zip(paths, vecs)), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
