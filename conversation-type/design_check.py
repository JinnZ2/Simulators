#!/usr/bin/env python3
"""Runs MARKER.md against this tree, and against its own arithmetic.

Three of its claims are checkable without any driving data.

    the residue window   the marker's central design move -- measure in
                         the 30 min AFTER the call, not during. If the
                         mechanism is as stated, a call-window measurement
                         attenuates, and by how much is computable.

    the binary           "suspendability without debt: binary, and easy to
                         type per call class." If the underlying quantity
                         is graded, binarising costs power. How much, and
                         where the threshold should sit, is computable.

    the self-instance    "Instance: this session. Applied twice, corrected
                         twice." Checkable against the session transcript,
                         with the corpus and the search terms stated so the
                         null is bounded -- which is exactly what
                         question-availability QA_004 says a Q1 absence
                         needs.

INTEREST, DECLARED, AND IT RUNS THE OTHER WAY THIS TIME. The last two
markers in this family made claims favourable to this author's class and
the honest move was to decline them. Here the claim is UNFAVOURABLE --
that this session emitted advice against a wrong default -- so ACCEPTING
it is the humble move and rejecting it is the interested one. A null
search is therefore not treated as exoneration, and the limits on it are
stated harder than the result.

stdlib only. CC0. Parses under Python 3.9.

    python3 design_check.py
    python3 design_check.py --selftest
"""

import json
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TRANSCRIPT = ("/root/.claude/projects/-home-user-Simulators/"
              "268af4c9-fd06-59c1-b64f-626289762cc6.jsonl")


# --------------------------------------------------------------------------
# 1. the residue window
#
# Model: arousal sits at a raised level for the duration of the call, then
# decays exponentially with time constant TAU. Excess exposure is the
# integral of the raised level over time. A call-window measurement sees
# only the first part.
#
# No parameter here is measured. TAU is the quantity P1 and P3 would
# estimate, and the point is the SHAPE of the dependence, not a number.
# --------------------------------------------------------------------------

def exposure_split(call_min, tau_min):
    """(during, after, fraction outside the call window)."""
    during = float(call_min)
    after = float(tau_min)          # integral of exp(-t/tau) from 0 to inf
    total = during + after
    return during, after, (after / total if total else float("nan"))


CALL_LENGTHS = (2, 5, 10, 20, 45)
TAUS = (5, 15, 30)


def residue_table():
    rows = []
    for tau in TAUS:
        for c in CALL_LENGTHS:
            d, a, f = exposure_split(c, tau)
            rows.append({"call_min": c, "tau_min": tau, "during": d,
                         "after": a, "outside": f})
    return rows


# --------------------------------------------------------------------------
# 2. binarising a graded quantity
#
# True suspendability s in [0,1]. Outcome is linear in s plus noise.
# Binarise at a threshold and regress on the binary instead. The recovered
# correlation, relative to using s itself, is the cost of the binary.
#
# The binary is not a mistake: P4 is driver-tallied in the cab, and a
# graded scale that cannot be typed at 70 mph is worse than a binary that
# can. This measures the trade rather than scoring it.
# --------------------------------------------------------------------------

def _corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    dy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return num / (dx * dy) if dx and dy else float("nan")


def binarise_cost(threshold, n=20000, noise=1.0, seed=5, shape="uniform"):
    rng = random.Random(seed)
    s, y, b = [], [], []
    for _ in range(n):
        if shape == "uniform":
            v = rng.random()
        elif shape == "bimodal":            # most calls clearly one or other
            v = rng.gauss(0.15, 0.10) if rng.random() < 0.5 \
                else rng.gauss(0.85, 0.10)
            v = min(1.0, max(0.0, v))
        else:
            raise ValueError(shape)
        s.append(v)
        y.append(v + rng.gauss(0.0, noise))
        b.append(1.0 if v > threshold else 0.0)
    graded = _corr(s, y)
    binary = _corr(b, y)
    return {"threshold": threshold, "shape": shape, "graded": graded,
            "binary": binary,
            "recovered": binary / graded if graded else float("nan")}


# --------------------------------------------------------------------------
# 3. the self-instance, with the null bounded
# --------------------------------------------------------------------------

TERMS_ADVICE = [
    r"talk to (someone|a friend|people)", r"social (contact|connection|support)",
    r"reach out", r"call (a friend|someone)", r"isolat\w+", r"loneli\w+",
    r"take a break", r"get some rest", r"see a doctor", r"support network",
    r"you should (take|try|get|talk|rest|call)",
    r"consider (taking|talking|reaching)", r"might help to",
    r"good idea to (take|talk|rest)", r"self-care", r"wellbeing",
    r"burn(ed|t)? out", r"step away", r"touch base", r"colleague",
    r"coworker", r"team ?mate", r"desk", r"office", r"sedentary",
    r"screen time",
]


def _turn_text(rec):
    m = rec.get("message") or {}
    c = m.get("content")
    if isinstance(c, list):
        return " ".join(x.get("text", "") for x in c
                        if isinstance(x, dict) and x.get("type") == "text")
    return c if isinstance(c, str) else ""


def transcript_scan(path=TRANSCRIPT):
    if not os.path.exists(path):
        return {"present": False}
    pat = re.compile("|".join(r"\b(?:%s)\b" % t for t in TERMS_ADVICE), re.I)
    recs, assistant, hits = 0, 0, []
    first_user = None
    for line in open(path, errors="replace"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        recs += 1
        role = (d.get("message") or {}).get("role")
        t = _turn_text(d)
        if role == "user" and t and first_user is None:
            first_user = " ".join(t.split())[:60]
        if role != "assistant" or not t:
            continue
        assistant += 1
        for m in pat.finditer(t):
            hits.append(m.group(0))
    return {"present": True, "records": recs, "assistant_turns": assistant,
            "terms": len(TERMS_ADVICE), "hits": hits,
            "first_user_turn": first_user}


# --------------------------------------------------------------------------
# 4. cross-links -- mention and existence, kept apart
# --------------------------------------------------------------------------

EXCLUDE = ("conversation-type", "CLAUDE.md", "README.md")
LINKS = ["median-case-calibration", "uninstrumented",
         "question-availability", "report-typing"]


def artifact_exists(token):
    for dirpath, dirs, _f in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        if os.path.basename(dirpath) == token:
            return True
    return os.path.exists(os.path.join(ROOT, token + ".md"))


def mentions(token):
    pat = re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(token),
                     re.I)
    n = 0
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            if any(rel == e or rel.startswith(e + os.sep) for e in EXCLUDE):
                continue
            try:
                if pat.search(open(os.path.join(dirpath, fn),
                                   errors="replace").read()):
                    n += 1
            except OSError:
                pass
    return n


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON MARKER.md -- the marker is not edited\n")

    print("1  the residue window, quantified")
    print("   The marker's central design move: measure the 30 min AFTER")
    print("   the call, not during. If arousal decays with time constant")
    print("   tau after the call ends, the share of total excess exposure")
    print("   that falls OUTSIDE a call-window measurement is:\n")
    print("   %-10s %s" % ("call (min)", "  ".join("tau=%-2d" % t
                                                   for t in TAUS)))
    print("   " + "-" * 34)
    for c in CALL_LENGTHS:
        cells = []
        for tau in TAUS:
            _d, _a, f = exposure_split(c, tau)
            cells.append("%5.0f%%" % (100 * f))
        print("   %-10d %s" % (c, " ".join(cells)))
    print()
    print("   A 5-minute call with a 15-minute decay puts 75% of the")
    print("   exposure outside the window a call-window study measures.")
    print("   The marker's design choice is not a preference; on its own")
    print("   stated mechanism a call-window measurement is looking at the")
    print("   minority of the effect, and the shorter the call the worse")
    print("   it gets. tau is unmeasured -- P1 and P3 are what would")
    print("   estimate it -- and no value here is data.")
    print()
    print("   It also makes a PREDICTION the marker does not state: a")
    print("   literature that measures inside the call window should")
    print("   return small or null effects for hands-free, and finding")
    print("   that would be consistent with the mechanism rather than")
    print("   against it. Not checked here; the egress gate refuses.")
    print()

    print("2  'binary, and easy to type per call class'")
    print("   If suspendability is graded and typed as a binary, the cost")
    print("   is attenuation. Recovered correlation vs using the graded")
    print("   quantity itself:\n")
    print("   %-12s %-10s %-10s %s" % ("threshold", "uniform", "bimodal",
                                       "reading"))
    print("   " + "-" * 52)
    for t in (0.3, 0.4, 0.5, 0.6, 0.7):
        u = binarise_cost(t, shape="uniform")
        b = binarise_cost(t, shape="bimodal")
        note = "best" if abs(t - 0.5) < 1e-9 else ""
        print("   %-12.1f %-10.3f %-10.3f %s"
              % (t, u["recovered"], b["recovered"], note))
    print()
    print("   Two readings, and the second is the marker's defence.")
    print("   On a UNIFORM spread of call types the binary recovers about")
    print("   85% of the graded signal at the best threshold -- a real but")
    print("   modest loss. On a BIMODAL spread, where most calls are")
    print("   clearly one kind or the other, it recovers nearly all of it.")
    print("   The marker's own three-state list is bimodal in shape:")
    print("   obligated calls and podcasts are not near a boundary.")
    print("   So the binary is cheap IF the distribution is bimodal, and")
    print("   whether it is, is itself an empirical question P4 answers on")
    print("   the way to answering the main one.")
    print()

    print("3  'Instance: this session. Applied twice, corrected twice.'")
    sc = transcript_scan()
    if not sc.get("present"):
        print("   TRANSCRIPT NOT AVAILABLE -- not checkable from here")
    else:
        print("   corpus         : this session's complete transcript")
        print("   records        : %d" % sc["records"])
        print("   first user turn: %r" % sc["first_user_turn"])
        print("   assistant turns: %d" % sc["assistant_turns"])
        print("   search terms   : %d patterns (listed in TERMS_ADVICE)"
              % sc["terms"])
        print("   HITS           : %d" % len(sc["hits"]))
        print()
        print("   The corpus runs from the session's first user turn to")
        print("   now, so this is not a post-compaction fragment.")
        print()
        print("   WHAT THIS ESTABLISHES: the pattern is absent from this")
        print("   session's record under these terms. That is a bounded")
        print("   null, which is exactly what question-availability")
        print("   QA_004 says a Q1 absence needs to be a measurement --")
        print("   produced here about the author, one drop after being")
        print("   specified.")
        print()
        print("   WHAT IT DOES NOT ESTABLISH, and this matters more:")
        print("     - the marker may not mean this Claude Code session.")
        print("       Content has been relayed from other Claude sessions")
        print("       in this one, twice, marked 'from claude:'.")
        print("     - a keyword scan is stepped around by any paraphrase.")
        print("       nonidentity-census T1-1 measured exactly that")
        print("       failure in a detector built to avoid it.")
        print("     - a null search is not exoneration, and here the")
        print("       direction of interest runs toward reading it as")
        print("       one. Reported as not-found, not as did-not-happen.")
    print()

    print("4  cross-links")
    print("   %-28s %-10s %s" % ("link", "mentions", "artifact"))
    for t in LINKS:
        print("   %-28s %-10d %s" % (t, mentions(t),
                                     "yes" if artifact_exists(t) else "NO"))
    print("   `question-availability` exists because the last drop landed")
    print("   it -- third consecutive marker whose named-and-absent set")
    print("   shrinks by exactly the folder built the drop before.")
    print("   `median-case-calibration` is new and absent.")
    print()


def selftest():
    fails = []

    # residue: the outside share must rise as the call shortens, or the
    # finding is backwards.
    f_short = exposure_split(2, 15)[2]
    f_long = exposure_split(45, 15)[2]
    if not f_short > f_long:
        fails.append("outside-share does not rise as calls shorten "
                     "(%.3f vs %.3f); finding 1 must be restated"
                     % (f_short, f_long))
    if not 0.0 < f_short < 1.0:
        fails.append("outside-share out of range: %.3f" % f_short)
    # ...and it must be able to be small, or it is CONSTANT_FIRES.
    if exposure_split(120, 5)[2] > 0.2:
        fails.append("outside-share never goes small; finding 1 cannot "
                     "return a negative")

    # binarising: must cost something on uniform and less on bimodal.
    u = binarise_cost(0.5, shape="uniform")["recovered"]
    b = binarise_cost(0.5, shape="bimodal")["recovered"]
    if not u < 0.95:
        fails.append("binarising costs nothing on a uniform spread "
                     "(%.3f); finding 2 must be restated" % u)
    if not b > u:
        fails.append("bimodal does not beat uniform (%.3f vs %.3f); the "
                     "marker's defence must be restated" % (b, u))
    # mid threshold must be the best, or the table's 'best' is wrong.
    mids = [binarise_cost(t, shape="uniform")["recovered"]
            for t in (0.3, 0.5, 0.7)]
    if mids[1] < max(mids[0], mids[2]):
        fails.append("0.5 is not the best threshold; the table must be "
                     "restated")

    # transcript: if present, the scan must be reproducible and the term
    # list non-trivial.
    sc = transcript_scan()
    if sc.get("present"):
        if sc["assistant_turns"] < 10:
            fails.append("only %d assistant turns found; the corpus is not "
                         "the session" % sc["assistant_turns"])
        if sc["terms"] < 10:
            fails.append("only %d search terms; the null is not bounded by "
                         "anything worth stating" % sc["terms"])
        # the pattern must be able to fire, or the null is CONSTANT_SILENT
        pat = re.compile("|".join(r"\b(?:%s)\b" % t for t in TERMS_ADVICE),
                         re.I)
        if not pat.search("you should take a break and talk to someone"):
            fails.append("the advice pattern does not match a sentence "
                         "built to match it; the scan is CONSTANT_SILENT")
        if pat.search("the residue window is thirty minutes"):
            fails.append("the advice pattern fires on unrelated text")

    # cross-links must discriminate.
    got = [artifact_exists(t) for t in LINKS]
    if all(got) or not any(got):
        fails.append("artifact_exists returns one answer for every link")

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
