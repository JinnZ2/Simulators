#!/usr/bin/env python3
"""
ANCHOR MAP
Companion to ledger.py. Stdlib only.

The ledger records how much of a domain space a shape was read across.
Coverage is not the primary term. It resolves position inside a band that
something else already set.

What sets the band is where the shape ANCHORS: what it grounds to, and what
band that anchor already occupies. Anchoring near something that has survived
generational cycles raises the number. Anchoring only to recent work does
not, however many studies there are. Study count adds on top of anchor
proximity; it does not substitute for it.

BANDS — set by the class of support, not by sampling effort.

  none                 0.30   correlations seen across domains with no
                              external body of knowledge behind them.
                              Domain count is irrelevant here.
  external             0.80   corroborated by outside work — studies, field
                              research, long oral tradition, consensus.
                              Capped because it remains one reading of that
                              material.
  cycle_persistent     0.99   held over generational and civilizational
                              cycles, across varied conditions, not
                              overturned. Cannot be bought by reading more.

A shape usually carries several anchors at different distances. The near ones
pull the number up, the far ones hold it down, and the composite is not
computed here. This tool reports the anchors, their distances, and what is
blocking each chain. It does not emit a confidence figure.

PROVENANCE CHAINS

A shape grounded in human construct reaches a near anchor through a chain of
links. A gap in the chain is not fatal and not a discount. It is a routing
problem: the chain does not have to run the expected path, it has to arrive.
So a link carries a routing state, and two states that look identical from
outside are kept distinct:

  routed              a path to the next link exists and is stated
  unrouted            no path found yet. Alternate paths not exhausted.
  absent_established  investigated and the link genuinely does not ground
                      that way. Not a failure — a finding, and its own
                      measurement problem needing instrumentation.

Collapsing unrouted and absent_established into "blocked" loses the
distinction the map exists for.

Usage:
  anchor.py                     table over anchors/
  anchor.py --sense NAME        detail
  anchor.py --blocking NAME     unrouted links only
  anchor.py --new NAME
  anchor.py --jsonl
  anchor.py --selftest
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHORDIR = os.path.join(HERE, "anchors")

NONE = "none"
EXTERNAL = "external"
CYCLE_PERSISTENT = "cycle_persistent"
BAND_CEILING = {NONE: 0.30, EXTERNAL: 0.80, CYCLE_PERSISTENT: 0.99}
BAND_ORDER = (NONE, EXTERNAL, CYCLE_PERSISTENT)

ROUTED = "routed"
UNROUTED = "unrouted"
ABSENT = "absent_established"
STATES = (ROUTED, UNROUTED, ABSENT)


def load(path=ANCHORDIR):
    out = []
    if not os.path.isdir(path):
        return out
    for f in sorted(os.listdir(path)):
        if f.endswith(".json"):
            with open(os.path.join(path, f), encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out


def ratio(n, d):
    return None if not d else round(n / d, 3)


def score_anchor(a):
    chain = a.get("chain", [])
    routed = [l for l in chain if l.get("state") == ROUTED]
    unrouted = [l for l in chain if l.get("state") == UNROUTED]
    absent = [l for l in chain if l.get("state") == ABSENT]
    quantified = [l for l in routed if l.get("quantified") is True]
    corr = a.get("corroboration", {}) or {}
    cls = corr.get("class")
    return {
        "target": a.get("target"),
        "target_band": a.get("target_band"),
        "target_ceiling": BAND_CEILING.get(a.get("target_band")),
        "links": len(chain),
        "routed": len(routed),
        "unrouted": len(unrouted),
        "absent_established": len(absent),
        "chain_routed": ratio(len(routed), len(chain)),
        "chain_quantified": ratio(len(quantified), len(chain)),
        "corroboration_class": cls,
        "corroboration_ceiling": BAND_CEILING.get(cls),
        "study_count": corr.get("study_count"),
        "unrouted_links": [l.get("link") for l in unrouted],
        "absent_links": [l.get("link") for l in absent],
    }


def score(doc):
    anchors = [score_anchor(a) for a in doc.get("anchors", [])]
    classes = [a["corroboration_class"] for a in anchors
               if a["corroboration_class"] in BAND_CEILING]
    best = None
    if classes:
        best = max(classes, key=lambda c: BAND_ORDER.index(c))
    # spread between the nearest and furthest anchor. a shape whose anchors
    # all sit in one band reads differently from one straddling two, even at
    # the same ceiling.
    ceils = [a["corroboration_ceiling"] for a in anchors
             if a["corroboration_ceiling"] is not None]
    spread = None if len(ceils) < 2 else round(max(ceils) - min(ceils), 3)
    fully = [a for a in anchors if a["chain_routed"] == 1.0]
    return {
        "shape": doc.get("shape"),
        "sense": doc.get("sense"),
        "statement": doc.get("statement"),
        "anchors": anchors,
        "anchor_count": len(anchors),
        "ceiling_class": best,
        "ceiling": BAND_CEILING.get(best),
        "anchor_spread": spread,
        "chains_complete": len(fully),
        "unrouted_total": sum(a["unrouted"] for a in anchors),
        "absent_total": sum(a["absent_established"] for a in anchors),
        "asserted": doc.get("asserted_confidence"),
        "open": doc.get("open", []),
    }


def fmt(x):
    if x is None:
        return "--"
    if isinstance(x, float):
        return "%.2f" % x
    return str(x)


def wrap(t, w, ind=""):
    words, lines, cur = str(t).split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > w:
            lines.append(ind + cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(ind + cur)
    return lines


def table(scores):
    hdr = (f"{'shape / sense':<30}{'anch':>6}{'ceil':>6}{'sprd':>6}"
           f"{'done':>6}{'unrt':>6}{'asrt':>6}")
    print(hdr)
    print("-" * len(hdr))
    for s in scores:
        name = "%s / %s" % (s["shape"], s["sense"])
        print(f"{name[:30]:<30}{s['anchor_count']:>6}{fmt(s['ceiling']):>6}"
              f"{fmt(s['anchor_spread']):>6}{s['chains_complete']:>6}"
              f"{s['unrouted_total']:>6}{fmt(s['asserted']):>6}")
    print()
    print("ceil  band ceiling from the strongest corroboration class present.")
    print("sprd  gap between nearest and furthest anchor. non-zero means the")
    print("      number is a composite of anchors at different distances.")
    print("done  anchors whose provenance chain is fully routed.")
    print("unrt  links with no path found yet. Not blockages — unrouted.")
    print("asrt  confidence asserted in the file. Not derived here.")
    print()
    print("No composite figure is emitted. Weighting near against far anchors")
    print("is not specified, and a number produced by guessing at it would be")
    print("less honest than the anchors themselves.")


def detail(s):
    print("SHAPE     %s" % s["shape"])
    print("SENSE     %s" % s["sense"])
    for i, line in enumerate(wrap(s["statement"], 58)):
        print("%-10s%s" % ("" if i else "STATEMENT", line))
    print()
    print("CEILING   %s  (class: %s)" % (fmt(s["ceiling"]), s["ceiling_class"]))
    print("ASSERTED  %s" % fmt(s["asserted"]))
    print("SPREAD    %s" % fmt(s["anchor_spread"]))
    print()
    for a in s["anchors"]:
        print("ANCHOR    %s" % a["target"])
        print("    band          %s (%s)"
              % (a["target_band"], fmt(a["target_ceiling"])))
        print("    corroboration %s (ceiling %s, studies %s)"
              % (a["corroboration_class"], fmt(a["corroboration_ceiling"]),
                 fmt(a["study_count"])))
        print("    chain         %s links: %s routed, %s unrouted, %s absent"
              % (a["links"], a["routed"], a["unrouted"],
                 a["absent_established"]))
        print("    routed        %s   quantified %s"
              % (fmt(a["chain_routed"]), fmt(a["chain_quantified"])))
        for l in a["unrouted_links"]:
            for line in wrap("UNROUTED  " + str(l), 54, "      "):
                print(line)
        for l in a["absent_links"]:
            for line in wrap("ABSENT (established)  " + str(l), 54, "      "):
                print(line)
        print()
    for o in s["open"]:
        print("OPEN")
        for line in wrap(o, 58, "    "):
            print(line)
        print()


def blocking(s, docs):
    print("%s / %s" % (s["shape"], s["sense"]))
    print()
    doc = None
    for d in docs:
        if d.get("shape") == s["shape"] and d.get("sense") == s["sense"]:
            doc = d
    for a in doc.get("anchors", []):
        for l in a.get("chain", []):
            if l.get("state") != UNROUTED:
                continue
            print("ANCHOR %s" % a.get("target"))
            for line in wrap("LINK  " + str(l.get("link")), 58, "  "):
                print(line)
            tried = l.get("paths_attempted") or []
            openp = l.get("paths_open") or []
            print("  attempted: %s" % (", ".join(tried) if tried else "none"))
            print("  open:      %s" % (", ".join(openp) if openp else "none"))
            if l.get("note"):
                for line in wrap(l["note"], 58, "  "):
                    print(line)
            print()
    print("Unrouted is not blocked. An unrouted link means alternate paths")
    print("have not been exhausted. A link that has been investigated and")
    print("does not ground that way is marked absent_established, which is a")
    print("finding requiring its own instrumentation, not a dead end.")


SKELETON = {
    "shape": "", "sense": "", "statement": "",
    "asserted_confidence": None,
    "anchors": [{
        "target": "", "target_band": NONE,
        "corroboration": {"class": NONE, "study_count": None, "note": ""},
        "chain": [{"link": "", "state": UNROUTED, "quantified": False,
                   "paths_attempted": [], "paths_open": [], "note": ""}]
    }],
    "open": []
}


def selftest():
    doc = {
        "shape": "s", "sense": "x", "statement": "t",
        "asserted_confidence": 0.61,
        "anchors": [
            {"target": "thermo", "target_band": CYCLE_PERSISTENT,
             "corroboration": {"class": EXTERNAL, "study_count": 200},
             "chain": [
                 {"link": "a", "state": ROUTED, "quantified": True},
                 {"link": "b", "state": ROUTED, "quantified": False}]},
            {"target": "culture", "target_band": NONE,
             "corroboration": {"class": NONE, "study_count": None},
             "chain": [
                 {"link": "c", "state": UNROUTED},
                 {"link": "d", "state": ABSENT},
                 {"link": "e", "state": ROUTED, "quantified": False}]},
        ]}
    s = score(doc)
    empty = score({"shape": "e", "sense": "y", "anchors": []})
    checks = [
        ("ceiling from strongest class", s["ceiling"] == 0.80),
        ("ceiling class is external", s["ceiling_class"] == EXTERNAL),
        ("spread nonzero across bands", s["anchor_spread"] == 0.5),
        ("complete chains counted", s["chains_complete"] == 1),
        ("unrouted totalled", s["unrouted_total"] == 1),
        ("absent counted separately", s["absent_total"] == 1),
        ("absent not counted as routed",
         s["anchors"][1]["routed"] == 1),
        ("chain routed ratio", s["anchors"][1]["chain_routed"] == 0.333),
        ("quantified over links not routed",
         s["anchors"][0]["chain_quantified"] == 0.5),
        ("asserted carried not derived", s["asserted"] == 0.61),
        ("no composite emitted", "confidence" not in s),
        ("empty gives none not zero", empty["ceiling"] is None),
        ("empty spread none", empty["anchor_spread"] is None),
        ("band ceilings fixed", BAND_CEILING[NONE] == 0.30
         and BAND_CEILING[CYCLE_PERSISTENT] == 0.99),
    ]
    ok = 0
    for n, r in checks:
        print(("PASS" if r else "FAIL"), n)
        ok += bool(r)
    print("\n%d/%d" % (ok, len(checks)))
    return 0 if ok == len(checks) else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--new" in a:
        i = a.index("--new")
        sk = json.loads(json.dumps(SKELETON))
        sk["shape"] = a[i + 1] if len(a) > i + 1 else "unnamed"
        print(json.dumps(sk, indent=2))
        return
    docs = load()
    scores = [score(d) for d in docs]
    if "--jsonl" in a:
        for s in scores:
            print(json.dumps(s))
        return
    for flag in ("--sense", "--blocking"):
        if flag in a:
            i = a.index(flag)
            want = a[i + 1] if len(a) > i + 1 else None
            for s in scores:
                if s["sense"] == want or s["shape"] == want:
                    if flag == "--sense":
                        detail(s)
                    else:
                        blocking(s, docs)
                    return
            print("no sense named %s" % want, file=sys.stderr)
            sys.exit(1)
    table(scores)


if __name__ == "__main__":
    main()
