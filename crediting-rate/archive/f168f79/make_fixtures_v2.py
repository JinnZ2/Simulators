#!/usr/bin/env python3
# make_fixtures_v2.py -- writes the five constructed worlds WORK ORDER L
# REVISED requires.  CC0, stdlib only, parses under 3.9.
#
# EVERY WORLD IS CONSTRUCTED AND SAYS SO IN ITS OWN FRAME FILE.  No item,
# tradition, date or description here is a claim about anything.  The item
# names are Greek letters precisely so that no real technique's name can be
# read as evidence; the "traditions" are letters too.
#
# Contamination, declared before any number: these fixtures were written by
# the same process that wrote the scorer, so a fixture that returns what it
# was built to return is a REGRESSION result, not validation.
#
#   python3 make_fixtures_v2.py            # writes fixtures/v2/
#   python3 make_fixtures_v2.py --check    # writes to a temp dir and diffs

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import crediting_rate_v2 as M              # noqa: E402

OUT = os.path.join(HERE, "fixtures", "v2")
SALT = "constructed-v2"

VIS, TEC, NOT = M.VISIBLE, M.TECHNICAL_ONLY, M.NOT_RETAINED

# Two "traditions", both letters.  T_SRC is the name the mechanical measure
# looks for; T_RCV is the receiving side and is never matched.
T_SRC, T_RCV = "Sigmaic", "Tauvian"


def _named(n_named, n_total, sentences=2):
    """n_named of n_total reference descriptions name T_SRC in the first
    `sentences` sentences.  The name is placed in sentence 1 when it is
    named, and in sentence 3 when it is not -- so the measure depends on N
    and not on the name being absent from the text."""
    out = []
    for i in range(n_total):
        if i < n_named:
            d = ("The method came into use from the %s tradition. It spread "
                 "westward over two centuries. Later handbooks restate it."
                 % T_SRC)
        else:
            d = ("The method came into general use in the period. It spread "
                 "westward over two centuries. Earlier forms are attributed "
                 "to the %s tradition." % T_SRC)
        out.append((d, sentences))
    return out


def world(items, model_authored=False, sides=None, note=""):
    """items: list of (name, bin, domain, date_src, date_rcv, hops,
    n_named, n_sources, depth)."""
    events, mech, depth = [], [], []
    events.append({"_manifest": {"model_authored": model_authored,
                                 "salt": SALT, "note": note}})
    for (nm, b, dom, ds, dr, hops, n_named, n_src, dep) in items:
        side = (sides or {}).get(nm, M.TECHNIQUE_SIDE)
        eid = M.entry_id(nm, SALT)
        events.append({
            "item": nm, "domain": dom, "source_tradition": T_SRC,
            "receiving_tradition": T_RCV, "first_attested_source": ds,
            "first_attested_receiving": dr, "intermediary_count": hops,
            "bin": b, "frame_source": "constructed transmission catalogue",
            "side": side, "ordering_source": "constructed", "entry_id": eid,
        })
        for i, (d, sent) in enumerate(_named(n_named, n_src)):
            mech.append({"item": nm, "source_id": "ref-%d" % (i + 1),
                         "description": d, "sentences_scored": sent})
        for i in range(n_src):
            depth.append({"entry_id": eid, "source_id": "ref-%d" % (i + 1),
                          "coder_id": "constructed", "attribution_depth": dep})
    return events, mech, depth


def frame(label, why):
    return {"corpus": "CONSTRUCTED -- not a corpus", "edition": label,
            "date": "2026-09-24",
            "note": "CONSTRUCTED WORLD. " + why +
                    "  No item, tradition, date or description in this "
                    "fixture is a claim about anything."}


# ---- F1  etymology-tracking: credit follows the surviving word ---------
# technical_only tracks visible -> retention is the variable.
F1 = [("alpha", VIS, "numeracy", 800, 1150, 1, 3, 3, 2),
      ("beta", VIS, "numeracy", 820, 1160, 1, 3, 3, 2),
      ("gamma", VIS, "materials", 850, 1200, 1, 3, 3, 3),
      ("delta", VIS, "materials", 870, 1210, 1, 3, 3, 2),
      ("epsilon", TEC, "numeracy", 810, 1155, 1, 3, 3, 2),
      ("zeta", TEC, "numeracy", 830, 1165, 1, 3, 3, 2),
      ("eta", TEC, "materials", 860, 1205, 1, 2, 3, 2),
      ("theta", TEC, "materials", 880, 1215, 1, 3, 3, 3),
      ("iota", NOT, "numeracy", 805, 1152, 1, 0, 3, 0),
      ("kappa", NOT, "numeracy", 825, 1162, 1, 0, 3, 0),
      ("lambda", NOT, "materials", 855, 1202, 1, 0, 3, 1),
      ("mu", NOT, "materials", 875, 1212, 1, 1, 3, 0)]

# ---- F2  contribution-tracking: credit flows regardless of the bin -----
F2 = [(nm, b, dom, ds, dr, h, 3, 3, 3)
      for (nm, b, dom, ds, dr, h, _, _, _) in F1]

# ---- F3  mixed-side frame ---------------------------------------------
F3_SIDES = {"alpha": M.LANGUAGE_SIDE, "beta": M.LANGUAGE_SIDE,
            "epsilon": M.LANGUAGE_SIDE}

# ---- F5  antiquity-confounded: the gap is a date effect ---------------
# The bins are date-sorted and crediting tracks the DATE, not the bin.  The
# POOLED gap clears its shuffle band; inside the early date stratum it is
# exactly 0.  So F5's assertion is on the N2 output, not on the top-level
# return -- the pooled result is ETYMOLOGY_TRACKING and the control says why
# it should not be read that way.  8 items per bin: at 4 per bin the shuffle
# band is +/-0.75 and no gap this design can produce clears it, which is a
# property of the band at that n and not of the confound.
def _f5(n_per=8):
    # how many of each bin are LATE: visible 0, technical_only 2,
    # not_retained 4 -- so the bins are ordered by date and the crediting
    # rate follows the date.
    late_count = {VIS: 0, TEC: 2, NOT: 4}
    items = []
    for b in (VIS, TEC, NOT):
        for i in range(n_per):
            early = i < (n_per - late_count[b])
            ds = 800 + i * 10 if early else 1400 + i * 10
            items.append(("%s%d" % (b[:3], i), b,
                          "numeracy" if i % 2 else "materials",
                          ds, ds + 300, 1, 3 if early else 0, 3, 3))
    return items


F5 = _f5()


# ---- F6  one domain clears its own band, the pool does not -------------
# BEYOND THE ORDER.  The order lists five fixtures and none of them reaches
# DOMAIN_SPECIFIC, a class its own RETURN block declares.  A declared
# member no path populates cannot be told from one nobody looked for, so
# this world exists to show the branch fires.
#
# The construction is the informative part: a domain's shuffle band is set
# by its WITHIN-bin spread, so a domain can only fail to clear if its items
# disagree internally.  Domain A is clean (1.0 / 0.667 / 0.0) and clears;
# domain B has half its items credited in every bin, so its band is wide
# and its gap of 0 does not clear; pooled, A's gap is diluted by B's mass.
_B_PATTERN = {VIS: [3, 0, 3, 0, 0, 3],
              TEC: [3, 0, 0, 3, 3, 0],
              NOT: [3, 3, 0, 0, 3, 0]}


def _f6(a_per=4, b_per=12):
    items, k = [], 0
    for dom, per, pat in (("A", a_per, {VIS: [3], TEC: [2], NOT: [0]}),
                          ("B", b_per, _B_PATTERN)):
        for b in (VIS, TEC, NOT):
            for i in range(per):
                nm = pat[b][i % len(pat[b])]
                k += 1
                items.append(("%s%s%d" % (dom, b[:3], i), b, dom,
                              800 + k, 1100 + k, 1, nm, 3, 3 if nm else 0))
    return items


F6 = _f6()


WORLDS = {
    "f1_etymology": (F1, False, None,
                     "credit follows the surviving word; technical_only "
                     "tracks visible"),
    "f2_contribution": (F2, False, None,
                        "credit flows at the same rate in every bin"),
    "f3_mixed_side": (F1, False, F3_SIDES,
                      "three items drawn from the language side, the rest "
                      "from the technique side"),
    "f4_model_authored": (F1, True, None,
                          "the item list declares model_authored=True"),
    "f5_antiquity": (F5, False, None,
                     "crediting tracks the attestation DATE and the bins "
                     "are date-sorted, so the pooled gap is a date effect"),
    "f6_domain_specific": (F6, False, None,
                           "BEYOND THE ORDER: one domain clears its own "
                           "shuffle band and the pooled gap does not, so "
                           "the DOMAIN_SPECIFIC branch is shown reachable"),
}


def write(base=OUT):
    if not os.path.isdir(base):
        os.makedirs(base)
    written = []
    for name, (items, ma, sides, why) in sorted(WORLDS.items()):
        ev, mech, dep = world(items, model_authored=ma, sides=sides, note=why)
        for suffix, rows in (("events", ev), ("mechanical", mech),
                             ("depth", dep)):
            p = os.path.join(base, "%s.%s.jsonl" % (name, suffix))
            with io.open(p, "w", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r, sort_keys=True) + "\n")
            written.append(p)
        p = os.path.join(base, "%s.frame.json" % name)
        with io.open(p, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(frame(name, why), indent=1,
                                sort_keys=True) + "\n")
        written.append(p)
    return written


def paths(name, base=OUT):
    return (os.path.join(base, "%s.events.jsonl" % name),
            os.path.join(base, "%s.mechanical.jsonl" % name),
            os.path.join(base, "%s.depth.jsonl" % name),
            os.path.join(base, "%s.frame.json" % name))


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        import tempfile
        import filecmp
        d = tempfile.mkdtemp()
        write(d)
        bad = []
        for f in sorted(os.listdir(OUT)):
            if not filecmp.cmp(os.path.join(OUT, f), os.path.join(d, f),
                               shallow=False):
                bad.append(f)
        print("regenerates byte-identically: %s" % (not bad))
        for f in bad:
            print("  DIFFERS  " + f)
        sys.exit(1 if bad else 0)
    for p in write():
        print(os.path.relpath(p, HERE))
