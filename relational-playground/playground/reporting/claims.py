"""ADDITION 5. Claim tags: how a statement was arrived at. A different axis from
the value statuses (MEASURED ... EXCLUDED BY DESIGN), which say how a number was obtained.

  OBSERVED   read off a supplied observation
  DERIVED    computed here, by code in this tree, from stated inputs
  PROPOSED   an interpretation or a mapping; not tested here
"""
from ..uncertainty import STATUSES

TAGS = ("OBSERVED", "DERIVED", "PROPOSED")


def claim(text, tag, basis):
    if tag in STATUSES:
        raise ValueError("%r is a value status, not a claim tag; the two axes stay apart" % tag)
    if tag not in TAGS:
        raise ValueError("tag %r not in %r" % (tag, TAGS))
    if not basis:
        raise ValueError("a claim needs a basis")
    return dict(text=text, tag=tag, basis=basis)


def check(claims):
    for c in claims:
        if c.get("tag") not in TAGS or not c.get("basis"):
            raise ValueError("untagged or baseless claim: %r" % (c,))
    return claims


def counts(claims):
    return {t: sum(1 for c in claims if c["tag"] == t) for t in TAGS}
