#!/usr/bin/env python3
"""M1-M8 and S1-S3, parsed from the delivered coding scheme.

This is the companion scheme `revision-mechanism` recorded as
named-and-absent (its RM_008). It landed, so it is parsed here rather
than retyped, and that folder imports it from here instead of
describing its absence.

Nothing in this file is a claim about any community, valley, or body of
knowledge. It is a vocabulary read out of a delivered document.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DROP = os.path.join(HERE, "SOURCE_DROP.md")

MECHANISM = "M"
STORY = "S"


def _doc():
    return open(DROP, encoding="utf-8").read()


def _block():
    return _doc().split("## Coding scheme")[1].split("## Measures")[0]


def components():
    """M1..M8 -> (label, gloss). Parsed, not retyped."""
    out = {}
    cur = None
    for ln in _block().split("\n"):
        m = re.match(r"^    (M[1-8])\s{2,}(\S.*?)\s{2,}(\S.*)$", ln)
        if m:
            cur = m.group(1)
            out[cur] = {"label": m.group(2).strip(),
                        "gloss": m.group(3).strip()}
            continue
        m2 = re.match(r"^    (M[1-8])\s{2,}(\S.*)$", ln)
        if m2:
            cur = m2.group(1)
            out[cur] = {"label": m2.group(2).strip(), "gloss": ""}
            continue
        if cur and re.match(r"^\s{20,}\S", ln):
            out[cur]["gloss"] = (out[cur]["gloss"] + " "
                                 + ln.strip()).strip()
        elif ln.strip() == "":
            cur = None
    return out


def story_codes():
    """S1..S3 -> gloss."""
    out = {}
    for ln in _block().split("\n"):
        m = re.match(r"^    (S[1-3])\s{2,}(\S.*)$", ln)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def chain_positions():
    """C0..C3+ as delivered, in order."""
    body = _doc().split("chain position:")[1].split("Cohort is defined")[0]
    out = []
    for ln in body.split("\n"):
        m = re.match(r"^\s+(C\d\+?)\s{2,}(\S.*)$", ln)
        if m:
            out.append({"position": m.group(1), "gloss": m.group(2).strip()})
    return out


COMPONENTS = components()
STORY_CODES = story_codes()
CHAIN = chain_positions()

# The two components the design's own headline comparison turns on.
COUPLING = "M8"      # "the coupling component", named so in the drop
ACTION = "M7"        # the ACTION rule
MECHANISM_STATED = "M3"


def _render():
    """The parsed scheme, so a reader can see what was taken from the drop."""
    out = ["THE DELIVERED CODING SCHEME, AS PARSED", ""]
    out.append("  %d M-components" % len(COMPONENTS))
    for k in sorted(COMPONENTS):
        out.append("    %-4s %s" % (k, COMPONENTS[k]["label"]))
    out.append("")
    out.append("  %d story codes" % len(STORY_CODES))
    for k in sorted(STORY_CODES):
        out.append("    %-4s %s" % (k, STORY_CODES[k]))
    out.append("")
    out.append("  %d chain positions" % len(CHAIN))
    for c in CHAIN:
        out.append("    %-4s %s" % (c["position"], c["gloss"]))
    out.append("")
    out.append("  Nothing here is reconstructed. Every line above is read")
    out.append("  out of SOURCE_DROP.md at import; an edit there and not")
    out.append("  here turns selftest_power.py red.")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        # A silent exit 0 here would be a pass on an invocation that runs
        # nothing -- the DL_005 / CC_006 shape. This module is a parser
        # with no checks of its own; its checks live next door, and it
        # says so rather than accepting the flag.
        sys.stderr.write(
            "scheme.py has no checks of its own. It is the parser; the "
            "checks that exercise it live in selftest_power.py.\n"
            "    python3 transmission-decay/selftest_power.py\n")
        sys.exit(2)
    print(_render())
