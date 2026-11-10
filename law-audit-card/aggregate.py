"""aggregate.py -- two counts over the seed cards. CC0, stdlib only.

PROPOSED | ILLUSTRATIVE. The denominator is the seed set in cards/, chosen
because the tree already held material on those laws. It is not a sample of
laws, and neither count is a rate about laws.

  tested_any              last_tested is not VOID
  tested_against_purpose  tested, stated_purpose is not VOID, and the test's
                          measurand is DECLARED to match that purpose
                          (last_tested.value.matches_purpose is true)

Per card the purpose reading is one of
  NOT_TESTED              last_tested VOID
  AGAINST_PURPOSE         as above
  OTHER_MEASURAND         matches_purpose declared false
  UNRESOLVED              tested, but stated_purpose is VOID or the match is
                          not declared; the tool does not infer a match

Usage: python3 aggregate.py [CARDS_DIR]
"""
import glob
import os
import sys

import card

HERE = os.path.dirname(os.path.abspath(__file__))


def purpose_reading(c):
    lt = c["last_tested"]
    if lt["tag"] == "VOID":
        return "NOT_TESTED", "last_tested VOID"
    if c["stated_purpose"]["tag"] == "VOID":
        return "UNRESOLVED", "stated_purpose VOID"
    m = lt["value"].get("matches_purpose")
    if m is True:
        return "AGAINST_PURPOSE", "measurand declared to match stated_purpose"
    if m is False:
        return "OTHER_MEASURAND", "measurand declared not to match stated_purpose"
    return "UNRESOLVED", "measurand-to-purpose match not declared"


def count(cards_dir=os.path.join(HERE, "cards")):
    rows = []
    for p in sorted(glob.glob(os.path.join(cards_dir, "*.json"))):
        c = card.read(card.load(p))
        state, why = purpose_reading(c)
        rows.append({"id": c["id"], "reading": state, "why": why})
    tested = [r for r in rows if r["reading"] != "NOT_TESTED"]
    return {"n": len(rows), "tested_any": len(tested),
            "tested_against_purpose": sum(1 for r in rows if r["reading"] == "AGAINST_PURPOSE"),
            "unresolved": sum(1 for r in rows if r["reading"] == "UNRESOLVED"),
            "rows": rows, "label": "ILLUSTRATIVE: seed cards only, not a sample"}


def render(r):
    L = ["# law-audit-card aggregate | ILLUSTRATIVE | seed cards only, not a sample",
         "tested_any (last_tested != VOID): %d of %d seed cards" % (r["tested_any"], r["n"]),
         "tested_against_purpose (purpose stated, measurand declared to match): %d of %d seed cards"
         % (r["tested_against_purpose"], r["n"]),
         "unresolved (tested, purpose or match not established): %d" % r["unresolved"]]
    L += ["  %-28s %-16s %s" % (x["id"], x["reading"], x["why"]) for x in r["rows"]]
    return "\n".join(L)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) > 1 or (a and a[0].startswith("-")):
        print("usage: python3 aggregate.py [CARDS_DIR]   (checks: python3 tests/test_card.py)")
        sys.exit(2)
    print(render(count(*a)))
