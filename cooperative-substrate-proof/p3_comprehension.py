#!/usr/bin/env python3
"""P3 -- COMPREHENSION CHECK. Nothing external: one directory of text
files, no network, no model call.

The order's claim: a corpus is understandable only because its parts do
not contest each other's terms, and COMPRESSIBILITY IS THE EVIDENCE.
Compressibility across two documents is measured as the gain

    gain(A, B) = 1 - C(A + B) / (C(A) + C(B))

where C is compressed size. Positive gain means part of B was already
predictable from A.

WHAT GAIN ALONE DOES NOT ESTABLISH, and why this module carries a null:
two documents in one script, one language and one whitespace convention
compress together whether or not they agree about a single term. Gain
alone is therefore evidence of SHARED FORM, which is necessary for
transmission and not sufficient for term convergence. So every pair is
also measured against a control in which B is put through a
monoalphabetic SUBSTITUTION CIPHER -- a fixed permutation of the
alphabet, case preserved, punctuation and whitespace untouched.

The cipher is the right control and a token rename is not, which was
found by building the token rename first: renaming tokens to fresh
strings destroys B's OWN compressibility, so C(rename(B)) is far larger
than C(B), the denominator moves, and the control returns a near
constant offset instead of a null. A letter permutation leaves every
repeat inside B at the same length and distance and merely relabels the
symbols, so C(cipher(B)) is C(B) to within a byte or two, while every
substring B shared with A is gone. The reading is the drop:

    delta = gain(A, B) - gain(A, cipher(B))

    SHARED_TERMS      delta >= DELTA_MIN; enciphering the terms costs
                      compressibility, so the terms were doing the work
    SHARED_FORM_ONLY  gain > 0 and delta < DELTA_MIN; the documents
                      compress together for reasons the terms do not
                      carry
    NO_SHARED_FORM    gain <= 0
    NOT_EVALUABLE     a document is empty; no reading, not a zero

The verdict is never "convergence established". It is a statement about
what the compressibility of this corpus does and does not support.

    python3 p3_comprehension.py --corpus fixtures/corpus
    python3 p3_comprehension.py --corpus DIR --json out.json

Refuses --selftest; checks live in test_proof.py.
"""

import json
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
import zlib

import scope

TOKEN = re.compile(r"[A-Za-z][A-Za-z'-]*")

# [CHOICE 1] zlib at level 9, the stdlib compressor present on every
# machine that runs Python. The absolute sizes depend on the zlib build;
# the metric that carries the verdict is a DIFFERENCE between two gains
# computed with the same compressor on the same machine, so the build
# cancels.
LEVEL = 9

# [CHOICE 2] delta threshold. A pair whose shared vocabulary is doing no
# work returns a delta near zero; the fixtures separate at an order of
# magnitude above this. Declared, not derived from a corpus.
DELTA_MIN = 0.02

# [CHOICE 3] the control is a monoalphabetic substitution cipher over
# the 26 ASCII letters, seeded, with the same permutation applied to
# both cases. A letter that happens to map to itself is left as drawn
# rather than forced, since forcing a derangement is a second choice
# with no stated basis; the checks record how many fixed points the
# shipped seed has.
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

SHARED_TERMS = "SHARED_TERMS"
SHARED_FORM_ONLY = "SHARED_FORM_ONLY"
NO_SHARED_FORM = "NO_SHARED_FORM"
NOT_EVALUABLE = "NOT_EVALUABLE"


def csize(text):
    """Compressed size in bytes, or None for an empty input."""
    if text is None:
        return None
    data = text.encode("utf-8")
    if not data:
        return None
    return len(zlib.compress(data, LEVEL))


def gain_from_sizes(ca, cb, cab):
    """1 - cab / (ca + cb), or None when any size is absent or the
    denominator is zero.

    Kept separate from the compressor so the arithmetic has a known
    answer independent of any zlib build. A gain of exactly 0.0 is a
    measurement (the pair compressed no better together than apart) and
    is NOT the same as None (nothing to measure). A negative gain is
    possible and is returned as measured.
    """
    if ca is None or cb is None or cab is None:
        return None
    denom = ca + cb
    if denom == 0:
        return None
    return 1.0 - (float(cab) / float(denom))


def gain(a, b):
    return gain_from_sizes(csize(a), csize(b), csize(a + b))


def cipher_alphabet(seed=0):
    """Return the permuted alphabet used as the control mapping."""
    rng = random.Random(seed)
    letters = list(ALPHABET)
    rng.shuffle(letters)
    return "".join(letters)


def encipher(text, seed=0):
    """Monoalphabetic substitution over ASCII letters, case preserved.

    Structure-preserving by construction: every repeated substring in
    the input is a repeated substring of the same length at the same
    distance in the output, so the compressor sees the same matches and
    C(encipher(text)) is C(text) to within the Huffman table. What is
    destroyed is every substring shared with any OTHER document.
    """
    perm = cipher_alphabet(seed)
    table = {}
    for src_ch, dst_ch in zip(ALPHABET, perm):
        table[src_ch] = dst_ch
        table[src_ch.upper()] = dst_ch.upper()
    return "".join(table.get(ch, ch) for ch in text)


def read_corpus(path):
    """Return [(name, text)] for every .txt file in path, sorted.

    Only .txt is read. A README.md alongside the corpus documents it
    without entering it, so a note about the fixtures cannot become a
    document the fixtures are measured against."""
    out = []
    for name in sorted(os.listdir(path)):
        if not name.lower().endswith(".txt"):
            continue
        full = os.path.join(path, name)
        if not os.path.isfile(full):
            continue
        with open(full, "r", encoding="utf-8", errors="replace") as fh:
            out.append((name, fh.read()))
    return out


def pair_reading(a, b, seed=0):
    """Measure one ordered pair."""
    g = gain(a, b)
    gr = gain(a, encipher(b, seed))
    if g is None or gr is None:
        return {"gain": g, "gain_ciphered": gr, "delta": None,
                "verdict": NOT_EVALUABLE}
    delta = g - gr
    if g <= 0.0:
        verdict = NO_SHARED_FORM
    elif delta >= DELTA_MIN:
        verdict = SHARED_TERMS
    else:
        verdict = SHARED_FORM_ONLY
    return {"gain": g, "gain_ciphered": gr, "delta": delta,
            "verdict": verdict}


def check(corpus, seed=0):
    """Run every unordered pair. Fewer than two documents is
    NOT_EVALUABLE with the reason named, never a clean pass."""
    if len(corpus) < 2:
        return {"pairs": [], "n_docs": len(corpus),
                "verdict": NOT_EVALUABLE,
                "reason": "fewer than two documents; a pair is the unit"}
    pairs = []
    for i in range(len(corpus)):
        for j in range(i + 1, len(corpus)):
            na, a = corpus[i]
            nb, b = corpus[j]
            r = pair_reading(a, b, seed)
            r["a"] = na
            r["b"] = nb
            pairs.append(r)
    counts = {}
    for r in pairs:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    evaluable = [r for r in pairs if r["verdict"] != NOT_EVALUABLE]
    if not evaluable:
        overall = NOT_EVALUABLE
    else:
        overall = weakest_link(evaluable)
    return {"pairs": pairs, "n_docs": len(corpus), "counts": counts,
            "verdict": overall, "reason": ""}


# The corpus verdict is the WEAKEST pair, not the commonest one, and
# that is the order's own first sentence for this part: every link must
# transmit faithfully for information to reach a model. A corpus with
# one pair that shares no terms is a corpus with a link that does not
# transmit, whatever the other pairs do. The first version took the
# modal verdict instead; it was replaced when this folder's own values
# scan fired on the variable that held the running maximum, and the
# weakest-link rule is the better reading as well as the clean one.
LADDER = (NO_SHARED_FORM, SHARED_FORM_ONLY, SHARED_TERMS)


def weakest_link(pairs):
    """The lowest rung on LADDER reached by any pair."""
    for rung in LADDER:
        for r in pairs:
            if r["verdict"] == rung:
                return rung
    return NOT_EVALUABLE


# The coding pass the order asks to be carried inside each part. A
# corpus is read, not competed over, so C2 and C4 do not hold of it --
# the point being that the reading is OUTSIDE the competitive frame's
# coverage rather than against it.
CORPUS_SCOPE = {
    "window": 1.0, "coupling_time": 1.0,
    "window_unit": "corpus", "coupling_unit": "corpus",
    "C2": False, "C3": False, "C4": False,
}


def render(result, corpus_path):
    lines = []
    lines.append("P3 COMPREHENSION CHECK")
    lines.append("")
    lines.append("  corpus: %s" % corpus_path)
    lines.append("  documents: %d" % result["n_docs"])
    lines.append("  [CHOICE 1] zlib level %d   [CHOICE 2] delta >= %.3f"
                 % (LEVEL, DELTA_MIN))
    lines.append("")
    if not result["pairs"]:
        lines.append("  verdict: %s -- %s" % (result["verdict"],
                                              result["reason"]))
    else:
        head = "  %-16s %-16s %8s %8s %8s  %s" % (
            "A", "B", "gain", "ciphered", "delta", "verdict")
        lines.append(head)
        lines.append("  " + "-" * (len(head) - 2))
        for r in result["pairs"]:
            def fmt(v):
                return "--" if v is None else "%.4f" % v
            lines.append("  %-16s %-16s %8s %8s %8s  %s" % (
                r["a"][:16], r["b"][:16], fmt(r["gain"]),
                fmt(r["gain_ciphered"]), fmt(r["delta"]), r["verdict"]))
        lines.append("")
        lines.append("  corpus verdict: %s" % result["verdict"])
    lines.append("")
    lines.append("  Reading: gain measures shared FORM. The drop under a")
    lines.append("  substitution cipher is what the terms carry. A")
    lines.append("  SHARED_TERMS verdict is evidence the parts do not")
    lines.append("  contest each other's terms; it is not proof that they")
    lines.append("  agree about any one of them.")
    lines.append("")
    sr = scope.code(CORPUS_SCOPE)
    lines.append("  scope coding (C1-C4): %s" % sr["verdict"])
    lines.append("  %s" % sr["reading"])
    return "\n".join(lines)
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
        sys.stderr.write(
            "p3_comprehension.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    if "--choices" in argv:
        sys.stdout.write(
            "[CHOICE 1] zlib level %d\n"
            "[CHOICE 2] delta threshold %.3f\n"
            "[CHOICE 3] cipher alphabet (seed 0) %s\n"
            % (LEVEL, DELTA_MIN, cipher_alphabet(0)))
        return 0
    path = None
    out = None
    for i, a in enumerate(argv):
        if a == "--corpus" and i + 1 < len(argv):
            path = argv[i + 1]
        if a == "--json" and i + 1 < len(argv):
            out = argv[i + 1]
    if path is None:
        sys.stderr.write(
            "NOT_RUN: no corpus given.\n"
            "This part reads a directory of text files and reads nothing\n"
            "else; it does not fall back to its own source, which would\n"
            "measure the instrument rather than a corpus.\n"
            "Usage: python3 p3_comprehension.py --corpus DIR\n")
        return 2
    corpus = read_corpus(path)
    result = check(corpus)
    sys.stdout.write(render(result, path) + "\n")
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"corpus": path, "result": result}, fh, indent=1,
                      sort_keys=True)
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
