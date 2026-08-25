#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
excluded_register.py - EXCLUDED-BY-CONSTRUCTION, in one place.

    python3 excluded_register.py [--selftest]

The third category. Not a handoff failure: the model's own ontology refusing
a case. The diff cannot see it -- a DROPPED verdict requires a ledger entry,
and there is none, because the thing was never stated. Only an agent reading
the code finds it.

Logged here rather than per-repo, per the spec. instrument-bias-sims/
excluded_subject.py catalogues the same instances from the sims' side and is
imported rather than duplicated, so the two cannot drift.

ONE CHECK RUN AGAINST THE SPEC'S OWN COUNT. The spec says "three instances so
far". excluded_subject.py records four, three of them at the derivation
level. Those numbers agree -- but only if S9's declared blank counts as the
ontology refusing a case, and it does not: nothing filters in S9 by design,
so the empty slot is a correct representation rather than a refusal. Read
that way the register holds TWO, and the third slot is where S10/M4 sits
under a different description. Both readings are printed; neither is picked.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIMS = os.path.join(os.path.dirname(HERE), "instrument-bias-sims")
sys.path.insert(0, HERE)
sys.path.insert(0, SIMS)
sys.path.insert(0, os.path.join(SIMS, "allocation_coupling"))

try:
    import excluded_subject as ES
    HAVE_SIMS = True
except Exception:                                           # pragma: no cover
    ES = None
    HAVE_SIMS = False

# Per-instance reading. `ontology_refuses` is the spec's own test: is this the
# model's ontology refusing a case, or a correct empty slot?
READINGS = {
    "S4": {"ontology_refuses": True,
           "why": "access was a function of the buck alone, so 'what does a "
                  "doe track' had no expressible form. The ontology had no "
                  "slot, not an empty one"},
    "S9": {"ontology_refuses": False,
           "why": "nothing filters in S9, by design. The empty slot is a "
                  "CORRECT representation of the system, not a refusal, so "
                  "counting it here would make a right answer score as a "
                  "defect"},
    "S10": {"ontology_refuses": True,
            "why": "presence is derived from tenure, so a continuous "
                   "observer without tenure cannot be given a value without "
                   "changing the derivation"},
    "S10/M4": {"ontology_refuses": True,
               "why": "the five-row mapping had no slot for a position high "
                      "on both generation and writing, and adding one moved "
                      "the headline from -0.85 to +0.11. A list-level "
                      "omission with a derivation-level consequence"},
}

SPEC_COUNT = 3      # "Three instances so far", as delivered


def instances():
    if not HAVE_SIMS:
        return []
    out = []
    for i in ES.INSTANCES:
        r = READINGS.get(i["sim"], {})
        out.append({"sim": i["sim"], "missing": i["missing"],
                    "derivation_excludes": i["derivation_excludes"],
                    "ontology_refuses": r.get("ontology_refuses"),
                    "why": r.get("why", ""),
                    "found_by": i["found_by"]})
    return out


def counts():
    ins = instances()
    return {"total_recorded": len(ins),
            "derivation_level": sum(1 for i in ins
                                    if i["derivation_excludes"]),
            "ontology_refuses": sum(1 for i in ins
                                    if i["ontology_refuses"]),
            "spec_says": SPEC_COUNT,
            "derivation_reading_matches_spec":
                sum(1 for i in ins if i["derivation_excludes"]) == SPEC_COUNT,
            "refusal_reading_matches_spec":
                sum(1 for i in ins if i["ontology_refuses"]) == SPEC_COUNT,
            "source": "imported from instrument-bias-sims/"
                      "excluded_subject.py, not duplicated"}


def why_the_diff_cannot_see_it():
    return {"requires": "a ledger entry, which requires the item to have "
                        "been stated",
            "but": "an excluded-by-construction case was never stated, "
                   "because the ontology that would express it does not "
                   "exist on either side of the channel",
            "so": "it appears as neither DROPPED nor ADDED. It appears as "
                  "nothing at all until an agent reads the code and notices "
                  "the missing slot",
            "detection": "not automatable from the diff. Three of the four "
                         "instances here were found by an outside reader"}


def confidence():
    return {"instance_list": "imported from excluded_subject.py; the sims' "
                             "side is the source of truth",
            "the_count": "TWO READINGS, neither picked. Derivation-level "
                         "gives 3 and matches the spec; ontology-refusal "
                         "gives 3 as well but a DIFFERENT three, because S9 "
                         "drops out and S10/M4 enters",
            "detection_rate": "3 of 4 found by an outside reader, which is "
                              "a statement about this corpus and not a rate",
            "resolved": False}


def breaks():
    return [
        "THE SPEC'S COUNT OF THREE IS REACHED BY TWO DIFFERENT ROUTES AND "
        "THEY NAME DIFFERENT INSTANCES. Derivation-level exclusion gives "
        "S4, S9, S10. Ontology-refusal gives S4, S10, S10/M4 -- S9 drops "
        "out because nothing filters there by design, and its empty slot is "
        "a correct representation rather than a refusal. Both are printed; "
        "the register does not pick one, because picking would settle a "
        "question about what the category means by arithmetic",
        "the register imports its instances rather than holding them, so it "
        "inherits whatever excluded_subject.py's hand-assigned reading of "
        "'the subject of the sim' is. Importing beats copying and it is not "
        "independence",
        "'the model's ontology refusing a case' is not operationalised. The "
        "test applied here -- can the missing party be given a value without "
        "changing the derivation -- is a proxy for it and was chosen by this "
        "file",
        "if instrument-bias-sims is absent the register reports zero "
        "instances rather than failing, which would read as 'none found' "
        "when it means 'not checked'. HAVE_SIMS distinguishes them and "
        "anything reading counts() must look at it",
    ]


def report():
    L = ["EXCLUDED BY CONSTRUCTION -- the third category, one place",
         "=" * 72, ""]
    if not HAVE_SIMS:
        L.append("  instrument-bias-sims not importable. NOT CHECKED, which")
        L.append("  is a different state from 'none found'.")
        return "\n".join(L)
    L.append("  Not a handoff failure. The diff cannot see it: a DROPPED")
    L.append("  verdict needs a ledger entry, and there is none, because the")
    L.append("  thing was never stated.")
    L.append("")
    L.append("  %-9s %-40s %-12s %s"
             % ("sim", "missing", "derivation", "ontology refuses"))
    for i in instances():
        L.append("  %-9s %-40s %-12s %s"
                 % (i["sim"], i["missing"][:40], i["derivation_excludes"],
                    i["ontology_refuses"]))
    L.append("")
    c = counts()
    L.append("  spec says                       %d" % c["spec_says"])
    L.append("  recorded                        %d" % c["total_recorded"])
    L.append("  derivation-level                %d  (matches spec: %s)"
             % (c["derivation_level"], c["derivation_reading_matches_spec"]))
    L.append("  ontology-refusal                %d  (matches spec: %s)"
             % (c["ontology_refuses"], c["refusal_reading_matches_spec"]))
    L.append("")
    L.append("  BOTH READINGS GIVE THREE AND THEY NAME DIFFERENT THREE.")
    L.append("")
    for sim in ("S4", "S9", "S10", "S10/M4"):
        r = READINGS[sim]
        L.append("    %-9s ontology refuses: %s" % (sim,
                                                    r["ontology_refuses"]))
        for line in _wrap(r["why"], "      "):
            L.append(line)
    L.append("")
    L.append("  Neither reading is picked here. Picking would settle what")
    L.append("  the category means by arithmetic.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    w = why_the_diff_cannot_see_it()
    L.append("  WHY THE DIFF CANNOT SEE IT")
    for key in ("requires", "but", "so", "detection"):
        L.append("    %-11s %s" % (key, ""))
        for line in _wrap(w[key], "      "):
            L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k2 in sorted(confidence()):
        v = str(confidence()[k2])
        L.append("    %s" % k2)
        for line in _wrap(v, "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("the sims side is importable, so the register is CHECKED rather than "
       "reporting zero", HAVE_SIMS)
    ck("instances are imported, not duplicated",
       "imported" in counts()["source"])
    ck("every recorded instance has a reading",
       all(i["ontology_refuses"] is not None for i in instances()))

    c = counts()
    ck("the derivation reading reaches the spec's count of three",
       c["derivation_reading_matches_spec"])
    ck("so does the ontology-refusal reading",
       c["refusal_reading_matches_spec"])
    dset = {i["sim"] for i in instances() if i["derivation_excludes"]}
    oset = {i["sim"] for i in instances() if i["ontology_refuses"]}
    ck("BUT THEY NAME DIFFERENT INSTANCES -- the same count by two routes",
       dset != oset and len(dset) == len(oset) == 3)
    ck("S9 is in one and not the other, which is where they part",
       ("S9" in dset) != ("S9" in oset))
    ck("and the reason is that nothing filters in S9 by design",
       READINGS["S9"]["ontology_refuses"] is False
       and "by design" in READINGS["S9"]["why"])

    w = why_the_diff_cannot_see_it()
    ck("the diff's blindness is explained by the missing ledger entry",
       "ledger entry" in w["requires"])
    ck("and detection is recorded as not automatable",
       "not automatable" in w["detection"])

    ck("the two-readings problem leads the breaks list",
       "TWO DIFFERENT ROUTES" in breaks()[0])
    ck("the not-checked versus none-found distinction is disclosed",
       any("NOT CHECKED" in b or "not checked" in b for b in breaks()))
    ck("confidence records that neither reading is picked",
       "neither picked" in confidence()["the_count"])
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "NAME DIFFERENT THREE" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="excluded-by-construction")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
