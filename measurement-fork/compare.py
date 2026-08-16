#!/usr/bin/env python3
"""
compare.py -- three-way diff. This is the product.

    python3 compare.py systems/<spec>.json

Four cells:

  SOLE REACH        quantity reached by exactly one arm
                    -> what that frame buys

  VOID RATIO        same base name, different quantity
                    (different object_of or normalizer)
                    -> where two designs talk past each other
                       while appearing to agree

  SAME QUANTITY,    identical quantity, different protocol
  DIFFERENT ROUTE   -> conventional result is sound here;
                       usable as-is, no redesign needed

  RESIDUAL          open question no arm generated a probe for
                    -> the growth edge. Nothing measures this yet.

CC0-1.0. stdlib only.
"""
import json
import sys
from collections import defaultdict

from quantities import key, base_key, render
import conventional
import coupling
import widen
import validate

STOP = {"the", "a", "of", "to", "and", "in", "is", "per", "unit", "by"}


def tokens(s):
    txt = "".join(c if c.isalnum() else " " for c in str(s).lower())
    out = set()
    for t in txt.split():
        if t in STOP:
            continue
        out.add(_stem(t))
    return out


def _stem(t):
    if t.endswith("ies") and len(t) > 4:
        return t[:-3] + "y"
    if t.endswith("es") and len(t) > 4:
        return t[:-2]
    if t.endswith("s") and len(t) > 3:
        return t[:-1]
    return t


def coverage(probe_, question):
    """Returns (hits, needed). Graded, not boolean -- a partial match
    is reported as partial rather than resolved in either direction."""
    qt = tokens(question)
    if not qt:
        return 0, 1
    pt = (tokens(probe_["quantity"]["base"])
          | tokens(probe_["quantity"]["normalizer"] or "")
          | tokens(probe_["protocol"])
          | tokens(probe_["reads"]))
    return len(qt & pt), max(2, int(round(0.6 * len(qt))))


def sk(item):
    return tuple("" if x is None else str(x) for x in item[0])


def rule(ch="-"):
    return ch * 66


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    with open(sys.argv[1]) as fh:
        spec = json.load(fh)

    qs = validate.check(spec)
    if qs:
        print("SPEC INCOMPLETE -- run validate.py first\n")
        for q in qs:
            print("  " + q)
        return 1

    arms = {
        "conventional": conventional.generate(spec),
        "coupling": coupling.generate(spec),
        "widen": widen.generate(spec),
    }
    allp = [p for ps in arms.values() for p in ps]

    print(rule("="))
    print("MEASUREMENT FORK  --  %s" % spec["system_id"])
    print(rule("="))
    print(spec["description"])
    print()
    for name, ps in arms.items():
        print("  arm %-14s %2d probes" % (name, len(ps)))
    print()

    by_key = defaultdict(list)
    for p in allp:
        by_key[key(p["quantity"])].append(p)

    by_base = defaultdict(set)
    for p in allp:
        by_base[base_key(p["quantity"])].add(key(p["quantity"]))

    # ---- CELL 1: sole reach ------------------------------------
    print(rule())
    print("SOLE REACH -- reached by exactly one arm")
    print(rule())
    sole = defaultdict(list)
    for k, ps in sorted(by_key.items(), key=sk):
        armset = {p["arm"] for p in ps}
        if len(armset) == 1:
            sole[ps[0]["arm"]].append(ps[0])

    for arm in ("conventional", "coupling"):
        if not sole.get(arm):
            continue
        print("\n  [%s]" % arm)
        for p in sole[arm]:
            print("\n    %s" % render(p["quantity"]))
            print("      reads    %s" % p["reads"])
            print("      blind to %s" % p["blind_to"])

    if sole.get("widen"):
        print("\n  [widen] -- options, not quantities. "
              "mark applies yes|no|unclear:")
        for p in sole["widen"]:
            print("      %s" % p["quantity"]["base"])

    # ---- CELL 2: void ratios -----------------------------------
    print()
    print(rule())
    print("VOID RATIO -- same name, different quantity")
    print(rule())
    found = False
    for base, keys in sorted(by_base.items()):
        if len(keys) < 2:
            continue
        found = True
        print("\n  base name: %s" % base)
        for k in sorted(keys, key=lambda t: tuple("" if x is None else x for x in t)):
            ps = by_key[k]
            print("    %-46s  %s"
                  % (render(ps[0]["quantity"]),
                     ",".join(sorted({p["arm"] for p in ps}))))
        print("    -> these do not compare. A ratio or a "
              "disagreement between")
        print("       them is undefined until the objects are matched.")
    if not found:
        print("\n  none")

    # ---- CELL 3: same quantity, different route ----------------
    print()
    print(rule())
    print("SAME QUANTITY, DIFFERENT ROUTE")
    print(rule())
    found = False
    for k, ps in sorted(by_key.items(), key=sk):
        armset = {p["arm"] for p in ps}
        if len(armset) > 1:
            found = True
            print("\n  %s" % render(ps[0]["quantity"]))
            for p in ps:
                print("    %-12s %s" % (p["arm"], p["protocol"][:44]))
            print("    -> convergent. The conventional number is usable "
                  "here as-is.")
    if not found:
        print("\n  none -- the arms share no quantity at all.")
        print("  That is itself a finding: the designs do not overlap,")
        print("  so no existing result speaks to the coupling questions.")

    # ---- CELL 4: residual --------------------------------------
    print()
    print(rule())
    print("RESIDUAL -- open questions no arm reaches")
    print(rule())
    residual, partial = [], []
    for q in spec.get("open_questions", []):
        full, part = set(), set()
        for p in allp:
            h, need = coverage(p, q)
            if h >= need:
                full.add(p["arm"])
            elif h > 0:
                part.add(p["arm"])
        if full:
            print("  [COVERED %-12s]  %s" % (",".join(sorted(full)), q))
        elif part:
            partial.append((q, sorted(part)))
        else:
            residual.append(q)

    if partial:
        print()
        for q, arms_ in partial:
            print("  [PARTIAL %-12s]  %s" % (",".join(arms_), q))
        print()
        print("  PARTIAL = token overlap below threshold. Either the")
        print("  probe reaches it under a different name, or it does not.")
        print("  Not resolved here. Resolve by hand or rename the")
        print("  open question and re-run.")

    if residual:
        print()
        for q in residual:
            print("  [ NO ARM      ]  %s" % q)
        print()
        print("  %d unreached. This is the growth edge -- either the"
              % len(residual))
        print("  quantity is badly named, or no instrument exists.")
        print("  Both are worth posting.")
    if not residual and not partial:
        print("\n  all open questions reached by at least one arm.")

    print()
    print(rule("="))
    return 0


if __name__ == "__main__":
    sys.exit(main())
