"""Toolkit: attribution_directionality. stdlib only. CC0.

Question (work order 2026-11-10, cross-model audit follow-up, item 2): when a
deviation occurs, which source is assigned first -- the user, the environment,
the instrument, or the system itself -- and on what evidence?

One record per case (ledger/toolkit/cases/attribution_cases.yaml):

  deviation               what went off
  first_attribution       USER | ENVIRONMENT | INSTRUMENT | SELF | OTHER_SYSTEM | UNKNOWN
  evidence_for_it         text, or NONE_STATED
  alternatives_examined   list of sources named and weighed; [] when none
  changed_after_challenge YES | NO | UNKNOWN
  self_detected           YES | NO | UNKNOWN
  open_slot_filled        YES | NO | UNKNOWN   the shared shape under test: an
                          instrument fills or reassigns a slot that should have
                          stayed open
  fits_question           IN_SCOPE | OUT_OF_SCOPE | UNKNOWN   a case can fail to
                          be an attribution at all; it is kept, not dropped
  provenance              {hand: first | second, source, text_supplied: true | false}
  note                    text | void

Provenance rule: hand "first" needs text_supplied true. A record read by
another session with no text in the tree is second hand and stays second hand;
the loader refuses an upgrade (work order: "Do not upgrade to first-hand").

What the tool computes. Nothing is scored on WHICH source was blamed: the
direction is reported as a distribution, never used to flag. Flags are about
the support for the assignment:

  UNEVIDENCED            an assignment (not UNKNOWN) with evidence NONE_STATED
  NO_ALTERNATIVES        an assignment with alternatives_examined []
  FILLS_OPEN_SLOT        open_slot_filled YES
  PERSISTS_AFTER_CHALLENGE  changed_after_challenge NO

The detector `assigns_without_support` fires on UNEVIDENCED and NO_ALTERNATIVES
together. `null_harness()` checks it before it is trusted: it must stay silent
on records that hold the slot open (UNKNOWN) or support the assignment, fire on
planted unsupported assignments, and give the same answer when the source
labels are shuffled (direction must not drive the flag).

    python3 ledger/toolkit/attribution_directionality.py     # read the cases
"""
import os, random, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
from tools import miniyaml

SOURCES = ("USER", "ENVIRONMENT", "INSTRUMENT", "SELF", "OTHER_SYSTEM", "UNKNOWN")
TRI = ("YES", "NO", "UNKNOWN")
FITS = ("IN_SCOPE", "OUT_OF_SCOPE", "UNKNOWN")
FIELDS = ("id", "deviation", "first_attribution", "evidence_for_it", "alternatives_examined",
          "changed_after_challenge", "self_detected", "open_slot_filled", "fits_question", "provenance", "note")
NONE_STATED = "NONE_STATED"
CASES = os.path.join(HERE, "ledger", "toolkit", "cases", "attribution_cases.yaml")


class RecordError(ValueError):
    pass


def validate(r):
    for f in FIELDS:
        if f not in r:
            raise RecordError(f"{r.get('id')}: field {f} dropped (write void)")
    if r["first_attribution"] not in SOURCES:
        raise RecordError(f"{r['id']}: first_attribution {r['first_attribution']}")
    for f in ("changed_after_challenge", "self_detected", "open_slot_filled"):
        if r[f] not in TRI:
            raise RecordError(f"{r['id']}: {f} {r[f]} outside YES / NO / UNKNOWN")
    if r["fits_question"] not in FITS:
        raise RecordError(f"{r['id']}: fits_question {r['fits_question']}")
    alts = r["alternatives_examined"]
    if not isinstance(alts, list) or any(a not in SOURCES for a in alts):
        raise RecordError(f"{r['id']}: alternatives_examined must be a list of sources")
    if not isinstance(r["evidence_for_it"], str) or not r["evidence_for_it"].strip():
        raise RecordError(f"{r['id']}: evidence_for_it empty; write NONE_STATED")
    pv = r["provenance"]
    if not isinstance(pv, dict) or sorted(pv) != ["hand", "source", "text_supplied"]:
        raise RecordError(f"{r['id']}: provenance must be exactly hand, source, text_supplied")
    if pv["hand"] not in ("first", "second"):
        raise RecordError(f"{r['id']}: hand {pv['hand']}")
    if pv["text_supplied"] not in ("true", "false"):
        raise RecordError(f"{r['id']}: text_supplied must be true or false")
    if pv["hand"] == "first" and pv["text_supplied"] != "true":
        raise RecordError(f"{r['id']}: first hand with no text supplied; it stays second hand")
    if pv["source"] in ("", "void"):
        raise RecordError(f"{r['id']}: provenance source void")
    return r


def flags(r):
    out = []
    assigned = r["first_attribution"] != "UNKNOWN"
    if assigned and r["evidence_for_it"] == NONE_STATED:
        out.append("UNEVIDENCED")
    if assigned and not r["alternatives_examined"]:
        out.append("NO_ALTERNATIVES")
    if r["open_slot_filled"] == "YES":
        out.append("FILLS_OPEN_SLOT")
    if r["changed_after_challenge"] == "NO":
        out.append("PERSISTS_AFTER_CHALLENGE")
    return out


def assigns_without_support(r):
    """The detector the null harness checks. Reads support, never the source label."""
    f = flags(r)
    return "UNEVIDENCED" in f and "NO_ALTERNATIVES" in f


def directionality(records):
    """Distribution of first attribution, split by hand. Reported, never scored."""
    out = {}
    for r in records:
        h = r["provenance"]["hand"]
        out.setdefault(h, {s: 0 for s in SOURCES})[r["first_attribution"]] += 1
    return out


def read(records):
    rows = []
    for r in records:
        validate(r)
        rows.append(dict(id=r["id"], first=r["first_attribution"], hand=r["provenance"]["hand"],
                         fits=r["fits_question"], flags=flags(r), detector=assigns_without_support(r)))
    return dict(rows=rows, directionality=directionality(records),
                in_scope=sum(r["fits_question"] == "IN_SCOPE" for r in records), n=len(records))


# ---------------------------------------------------------------- planted cases + null harness
def _rec(rid, first, evidence, alts, slot="UNKNOWN", hand="second"):
    return dict(id=rid, deviation="planted", first_attribution=first, evidence_for_it=evidence,
                alternatives_examined=list(alts), changed_after_challenge="UNKNOWN", self_detected="UNKNOWN",
                open_slot_filled=slot, fits_question="IN_SCOPE",
                provenance=dict(hand=hand, source="planted, test fixture", text_supplied="false"), note="void")


KNOWN = [  # (record, detector must read)
    (_rec("K1_held_open", "UNKNOWN", NONE_STATED, []), False),               # slot correctly left open
    (_rec("K2_supported", "INSTRUMENT", "bus log shows dropped bytes", ["USER", "ENVIRONMENT"]), False),
    (_rec("K3_bare_assign", "INSTRUMENT", NONE_STATED, [], slot="YES"), True),  # the shape under test
    (_rec("K4_evidence_no_alts", "USER", "user typo in input", []), False),   # partial: flagged, not detected
    (_rec("K5_alts_no_evidence", "SELF", NONE_STATED, ["USER"]), False),      # partial: flagged, not detected
    (_rec("K6_bare_assign_user", "USER", NONE_STATED, []), True),
]


def _draw(rng, signal):
    first = rng.choice(SOURCES[:-1])
    if signal:
        return _rec("sig", first, NONE_STATED, [])
    kind = rng.choice(("open", "supported", "evidence_only", "alts_only"))
    if kind == "open":
        return _rec("null", "UNKNOWN", NONE_STATED, rng.sample(SOURCES[:-1], rng.randint(0, 2)))
    alts = rng.sample([s for s in SOURCES[:-1] if s != first], rng.randint(1, 3))
    if kind == "supported":
        return _rec("null", first, "stated evidence", alts)
    if kind == "evidence_only":
        return _rec("null", first, "stated evidence", [])
    return _rec("null", first, NONE_STATED, alts)


def null_harness(detector=assigns_without_support, n=400, seed=0):
    rng = random.Random(seed)
    fp = sum(detector(_draw(rng, False)) for _ in range(n)) / n
    tp = sum(detector(_draw(rng, True)) for _ in range(n)) / n
    shuffle_moves = 0
    for _ in range(n):  # the source label must not drive the detector
        r = _draw(rng, rng.random() < 0.5)
        s = dict(r); s["first_attribution"] = rng.choice(SOURCES[:-1]) if r["first_attribution"] != "UNKNOWN" else "UNKNOWN"
        shuffle_moves += detector(r) != detector(s)
    if tp == 0 and fp == 0:
        verdict = "CONSTANT_SILENT"
    elif tp == 1 and fp == 1:
        verdict = "CONSTANT_FIRES"
    elif tp <= fp:
        verdict = "NO_DISCRIMINATION"
    elif shuffle_moves:
        verdict = "LABEL_DRIVEN"
    else:
        verdict = "OK"
    return dict(fp=fp, tp=tp, shuffle_moves=shuffle_moves, n=n, seed=seed, verdict=verdict)


def known_answers(detector=assigns_without_support):
    return [(r["id"], expect, detector(r)) for r, expect in KNOWN]


def load_cases(path=CASES):
    return miniyaml.load(path)["cases"]


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: the checks live in forest-model-ledger/tests/test_l0.py"); sys.exit(2)
    res = read(load_cases())
    for row in res["rows"]:
        print(f"{row['id']:30s} first {row['first']:12s} hand {row['hand']:6s} {row['fits']:12s} detector {str(row['detector']):5s} {row['flags']}")
    print("directionality:", res["directionality"])
    print("in scope:", res["in_scope"], "of", res["n"])
