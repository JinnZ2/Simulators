"""aggregate.py -- one count over the seed cards. CC0, stdlib only.

PROPOSED | ILLUSTRATIVE. "laws checked against own purpose" = cards whose
last_tested is not VOID. The denominator is the seed set in cards/, chosen
because the tree already held material on those laws. It is not a sample of
laws, and the count is not a rate about laws.

Usage: python3 aggregate.py [CARDS_DIR]
"""
import glob
import os
import sys

import card

HERE = os.path.dirname(os.path.abspath(__file__))


def count(cards_dir=os.path.join(HERE, "cards")):
    cards = [card.read(card.load(p)) for p in sorted(glob.glob(os.path.join(cards_dir, "*.json")))]
    tested = [c["id"] for c in cards if c["last_tested"]["tag"] != "VOID"]
    return {"n": len(cards), "checked_against_own_purpose": len(tested), "ids": tested,
            "label": "ILLUSTRATIVE: seed cards only, not a sample"}


def render(r):
    return ("# law-audit-card aggregate | ILLUSTRATIVE | seed cards only, not a sample\n"
            "laws checked against own purpose (last_tested != VOID): %d of %d seed cards\n"
            "  %s" % (r["checked_against_own_purpose"], r["n"], ", ".join(r["ids"]) or "none"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) > 1 or (a and a[0].startswith("-")):
        print("usage: python3 aggregate.py [CARDS_DIR]   (checks: python3 tests/test_card.py)")
        sys.exit(2)
    print(render(count(*a)))
