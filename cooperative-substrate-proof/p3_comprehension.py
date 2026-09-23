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
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
