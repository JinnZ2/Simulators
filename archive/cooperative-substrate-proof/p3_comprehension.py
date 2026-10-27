#!/usr/bin/env python3
"""P3 -- comprehension check. Nothing external. Runs on whatever corpus
the caller can read: files, stdin, or (--self) this folder's own text.

CLAIM UNDER TEST. For information to reach a model every link must
transmit faithfully. A word means something only because speakers
converge on it. A corpus is understandable only because its parts do
not contest each other's terms. COMPRESSIBILITY IS THE EVIDENCE: a
corpus whose parts share a vocabulary compresses better than the same
corpus rewritten so that each part keeps its own internal consistency
but shares no term with any other part.

INSTRUMENT. Split the corpus into parts (one file = one part, or blank
line paragraphs when a single text is given). Both arms replace every
word type with a same-length pseudo-word, so letter-level entropy is
the same in both; the ONLY difference is whether the map is shared:

  shared    one map for the whole corpus: a word type in part A and    -> r_shared
            the same type in part B become the same pseudo-word
  private   one map per part: within-part consistency preserved,        -> r_private
            cross-part sharing destroyed        [CHOICE 2] the null
  r_obs     the raw corpus, reported for reference, not compared
  r_script  each part's characters permuted privately (reported)

r = compressed bytes / raw bytes (zlib level 9). Lower is more
compressible. gap(seed) = r_private - r_shared, PAIRED per seed;
convergence evidence = mean gap > 0, read against the sd of the paired
gaps. [CHOICE 3] margin: mean gap must clear 3 sd of the paired gaps
over N seeds; [CHOICE 4] a corpus under 512 bytes is TOO_SHORT;
[CHOICE 5] a corpus of one part has no cross-part sharing to destroy,
so the null equals the shared arm by construction and the return is
NOT_EVALUABLE, not a pass. A first version compared the private arm to
the raw corpus and read a disjoint-vocabulary corpus as CONVERGENT,
because random pseudo-words compress worse than real words whatever
the sharing; that is why both arms are remapped.

WHAT THIS IS NOT. Compressibility measures redundancy, not meaning. The
check establishes the NECESSARY condition (shared symbols, shared
terms); it cannot establish that the shared terms are understood. A
corpus of one sentence repeated is maximally convergent and says
nothing. That is stated here rather than in a caveat at the bottom.

STATES: CONVERGENT | INDISTINGUISHABLE_FROM_NULL | NOT_EVALUABLE
        | TOO_SHORT | EMPTY
Refuses --selftest (checks live in selftest.py).
"""
import hashlib
import os
import random
import re
import sys
import unicodedata
import zlib

STATES = ("CONVERGENT", "INDISTINGUISHABLE_FROM_NULL", "NOT_EVALUABLE", "TOO_SHORT", "EMPTY")
MARGIN_SD = 3.0        # [CHOICE 3]
MIN_BYTES = 512        # [CHOICE 4]
SEEDS = 12             # [CHOICE 6] seeds for the null spread
TOKEN = re.compile(r"[^\W\d_]+|\d+|[^\w\s]|\s+", re.UNICODE)
ALPHA = "abcdefghijklmnopqrstuvwxyz"


def ratio(data):
    if not data:
        return None
    return len(zlib.compress(data, 9)) / len(data)


def _pseudo(word, part_i, seed):
    """Same-length pseudo-word, deterministic in (word, part, seed).
    Same word in the same part -> same pseudo-word; same word in a
    different part -> a different one. That is the whole null."""
    h = hashlib.sha256(("%d|%d|%s" % (seed, part_i, word)).encode("utf-8")).digest()
    return "".join(ALPHA[h[i % len(h)] % 26] for i in range(len(word)))


def remap(parts, seed, shared):
    """Pseudo-word remap. shared=True uses one map for every part (part
    index held at 0); shared=False gives each part its own map. Digits,
    punctuation and whitespace pass through unchanged in both."""
    out = []
    for i, text in enumerate(parts):
        toks = TOKEN.findall(text)
        pi = 0 if shared else i
        out.append("".join(_pseudo(t, pi, seed) if t[:1].isalpha() else t for t in toks))
    return "\n\n".join(out).encode("utf-8")


def script_null(parts, seed):
    out = []
    for i, text in enumerate(parts):
        rng = random.Random("%d|%d" % (seed, i))
        letters = sorted(set(ch for ch in text if ch.isalpha()))
        perm = letters[:]
        rng.shuffle(perm)
        m = dict(zip(letters, perm))
        out.append("".join(m.get(ch, ch) for ch in text))
    return "\n\n".join(out).encode("utf-8")


def dominant_script_share(text):
    """Share of alphabetic characters in the most common Unicode script
    (first word of the character name). Reported, not gated."""
    counts = {}
    n = 0
    for ch in text:
        if ch.isalpha():
            n += 1
            key = unicodedata.name(ch, "UNKNOWN").split(" ")[0]
            counts[key] = counts.get(key, 0) + 1
    if n == 0:
        return None, None
    top = max(counts, key=counts.get)
    return top, counts[top] / n


def _sd(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def check(parts, seeds=SEEDS):
    parts = [p for p in parts if p and p.strip()]
    raw = "\n\n".join(parts).encode("utf-8")
    base = {"n_parts": len(parts), "raw_bytes": len(raw)}
    if not raw:
        base["state"] = "EMPTY"
        return base
    if len(raw) < MIN_BYTES:
        base.update(state="TOO_SHORT", min_bytes=MIN_BYTES)
        return base
    r_obs = ratio(raw)
    shared = [ratio(remap(parts, s, True)) for s in range(seeds)]
    private = [ratio(remap(parts, s, False)) for s in range(seeds)]
    gaps = [p - q for p, q in zip(private, shared)]
    script = [ratio(script_null(parts, s)) for s in range(seeds)]
    g_mean, g_sd = sum(gaps) / len(gaps), _sd(gaps)
    scr, share = dominant_script_share("".join(parts))
    base.update(r_obs=r_obs, r_shared=sum(shared) / len(shared),
                r_private=sum(private) / len(private), gap=g_mean, gap_sd=g_sd,
                r_script=sum(script) / len(script),
                gap_over_sd=(g_mean / g_sd) if g_sd > 0 else None,
                dominant_script=scr, script_share=share, seeds=seeds)
    if len(parts) < 2:
        base["state"] = "NOT_EVALUABLE"
        base["reason"] = "one part: no cross-part sharing to destroy; private arm equals shared arm by construction"
        return base
    if g_mean > 0 and g_mean > MARGIN_SD * g_sd:
        base["state"] = "CONVERGENT"
    else:
        base["state"] = "INDISTINGUISHABLE_FROM_NULL"
    return base


def render(res, label):
    f = lambda k: ("%.4f" % res[k]) if res.get(k) is not None else "--"
    lines = ["P3 comprehension check  corpus=%s" % label,
             "state          %s" % res["state"],
             "parts %d   raw_bytes %d" % (res["n_parts"], res["raw_bytes"])]
    if "r_obs" in res:
        lines += ["r_obs          %s   (compressed/raw, zlib 9; lower = more compressible; reference only)" % f("r_obs"),
                  "r_shared       %s   pseudo-words, ONE map across parts" % f("r_shared"),
                  "r_private      %s   pseudo-words, one map PER part   [CHOICE 2] the null" % f("r_private"),
                  "gap            %s   = r_private - r_shared, paired per seed; sd %s over %d seeds" % (f("gap"), f("gap_sd"), res["seeds"]),
                  "gap/sd         %s   [CHOICE 3] margin %.1f sd" % (f("gap_over_sd"), MARGIN_SD),
                  "r_script       %s   private script per part (reported)" % f("r_script"),
                  "script         %s  share %s   (reported, not gated)" % (res.get("dominant_script"), f("script_share"))]
    if res.get("reason"):
        lines.append("reason         %s" % res["reason"])
    lines.append("limit: redundancy is a necessary condition for shared meaning, not evidence of it")
    return "\n".join(lines)


def self_corpus():
    here = os.path.dirname(os.path.abspath(__file__))
    parts = []
    for name in sorted(os.listdir(here)):
        if name.endswith((".py", ".md")) and name != "DISPATCH.md":
            with open(os.path.join(here, name), encoding="utf-8") as fh:
                parts.append(fh.read())
    return parts


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("p3_comprehension.py holds no checks; run python3 selftest.py\n")
        return 2
    if "--self" in argv:
        parts, label = self_corpus(), "--self (this folder's .py and .md, DISPATCH.md excluded)"
    elif "--stdin" in argv:
        parts, label = re.split(r"\n\s*\n", sys.stdin.read()), "stdin (blank-line paragraphs as parts)"
    elif "--paths" in argv:
        paths = argv[argv.index("--paths") + 1:]
        parts = []
        for p in paths:
            with open(p, encoding="utf-8", errors="replace") as fh:
                parts.append(fh.read())
        label = "%d files" % len(paths)
    else:
        parts, label = self_corpus(), "--self (default)"
    print(render(check(parts), label))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
