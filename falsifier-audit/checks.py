#!/usr/bin/env python3
"""checks.py -- A1..A4, each independent, each emitting a research
question. No score, no ranking, no fix. A falsifier may hit several. A
clean pass is information. Heuristics are stated at the callsite; a noisy
check that is cheap to dismiss is acceptable, a silent one is not.
Stdlib only.
"""

import re

import axes as X

WORD = re.compile(r"[a-zA-Z][a-zA-Z_]+")
NUMBER = re.compile(r"[-+]?\d+(?:\.\d+)?%?")

# A1: tokens that name an observable outcome, a quantity, or a threshold.
COMPARISON = ("<", ">", "≤", "≥", "=", "at least", "more than", "less than",
              "below", "above", "exceeds", "under ", "over ", "fewer", "greater")
UNIT_WORDS = frozenset("""units unit ppm ppb kg km hz joule watt ratio fraction probability count
rate percent sigma sd decade decades tokens bits seconds years days hours dollars kcal""".split())
OBSERVABLE = frozenset("""case cases row rows run runs ran cell cells record records document study
fires fired firing returns returned return reads read emits emitted occurs occur exists exist found
measured measure shows showed show produces produced yields gives gave lands landed crosses crossed
matches matched separates separated resolves resolved appears appeared carries carried names named
states stated holds held passes passed fails failed delivered coded scored reaches reached
admit admits admitted refuse refuses refused reverse reversed accept accepts accepted reject rejects
rejected moves moved move flips flip flipped differ differs differed agree agrees disagree disagrees
present absent quoted cited built landed seeds seed seeded produce emit detect detects detected
observe observes observed recovers recovered version versions arm arms edit edits step steps chain
curve series pair panel column session sessions gap gaps threshold value picks picked pick""".split())

# A4: reference / frame / baseline / observer terms that, undeclared, make
# the falsifier frame-bound (the geocentric shape).
REFERENCE_TERMS = ("baseline", "the null", "a null", "chance", "control",
                   "relative to", "against the", "expected", "reference",
                   "compared to", "versus ", " vs ", "the same", "matched")


def _words(s):
    return [w.lower() for w in WORD.findall(s)]


def a1(rec):
    """UNFALSIFIABLE-AS-WRITTEN: no threshold, quantity, or discrete
    observable outcome that could be observed to occur."""
    t = rec["text"]
    low = t.lower()
    has_num = bool(NUMBER.search(t))
    has_cmp = any(c in low for c in COMPARISON)
    ws = set(_words(t))
    has_unit = bool(ws & UNIT_WORDS)
    has_obs = bool(ws & OBSERVABLE)
    if has_num or has_cmp or has_unit or has_obs:
        return None
    return {"check": "A1", "falsifier_id": rec["id"], "text": t,
            "question": "what quantity, in what units, would make this falsifier fail?",
            "detail": "no number, comparison, unit, or observable-outcome word found"}


def a2(rec):
    """CLAIM-TEST DRIFT: load-bearing terms of the falsifier absent from
    the claim it is attached to. Only runs on LOCATED records. Shows
    matched and unmatched terms so a human can dismiss cheaply."""
    if rec["attach_status"] != "LOCATED":
        return None
    STOP = frozenset("""the a an of to in on at by for with from as is are was were be been being it
    its this that these those there here not no nor but if then than so such which who whom whose
    what when where why how all any each both few more most other some own same very can will would
    could and or one two per via would does did done has have had into over under out up down off
    about between through only also would could may might shall""".split())
    fw = [w for w in _words(rec["text"]) if w not in STOP and len(w) > 2]
    cw = set(w for w in _words(rec["attached_to"]) if w not in STOP)
    if len(fw) < 3:
        return None
    matched = [w for w in fw if w in cw]
    unmatched = [w for w in fw if w not in cw]
    share = len(matched) / len(fw)
    if share >= 0.34:            # [CHOICE 1] a third of the falsifier's terms in the claim
        return None
    return {"check": "A2", "falsifier_id": rec["id"], "text": rec["text"],
            "question": "which moved -- the claim or the test? %d of %d falsifier terms appear in the claim"
            % (len(matched), len(fw)),
            "detail": "matched: %s | unmatched: %s" % (", ".join(sorted(set(matched))) or "-", ", ".join(sorted(set(unmatched))[:12]))}


def a4(rec):
    """FIXED-REFERENCE-BODY: an undeclared frame, baseline, observer, or
    reference body. RESCOPE candidates, not narrow candidates."""
    low = rec["text"].lower()
    hit = [term.strip() for term in REFERENCE_TERMS if term in low]
    if not hit:
        return None
    return {"check": "A4", "falsifier_id": rec["id"], "text": rec["text"],
            "question": "what is the reference body here (%s), and what happens to this falsifier if it moves?"
            % ", ".join(sorted(set(hit))),
            "detail": "undeclared reference term(s): %s" % ", ".join(sorted(set(hit)))}


def a3(records):
    """CROSS-REPO INCOMPATIBILITY, computed at corpus level via axes:
    same axis, different repos, incompatible numeric cutoffs."""
    out = []
    for inc in X.incompatibilities(records):
        ids = [r["id"] for r in inc["records"]]
        out.append({"check": "A3", "falsifier_id": "axis:" + inc["axis"], "text": "; ".join(r["text"][:80] for r in inc["records"][:4]),
                    "question": "on axis '%s', repos %s carry different numeric cutoffs; what distinguishes the contexts, and is the difference real or is one cutoff inherited?"
                    % (inc["axis"], ", ".join(inc["repos"])),
                    "detail": "members: " + " | ".join("%s [%s]" % (r["id"], ",".join(r["numbers"])) for r in inc["records"][:8])})
    return out


def per_record(records):
    """A1, A2, A4 over every record; A3 over the corpus. Returns a flat
    list of hits, unaggregated (no score)."""
    hits = []
    for r in records:
        for fn in (a1, a2, a4):
            h = fn(r)
            if h:
                hits.append(h)
    hits.extend(a3(records))
    return hits


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        print("checks has no selftest; run selftest_fa.py", file=sys.stderr)
        sys.exit(2)
    print("checks.py -- A1..A4; import and call per_record(records). "
          "Run selftest_fa.py for the checks.", file=sys.stderr)
    sys.exit(2)
