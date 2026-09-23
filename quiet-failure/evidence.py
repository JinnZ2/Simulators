"""WO-2 -- the Evidence section, parsed and carried.

The order marks its evidence "(fetched, verified)". That is the ORDER'S
verification, not this folder's: the journal host answers 403 to
CONNECT (decomposition.EGRESS), so every finding here is
CARRIED_NOT_VERIFIED. Numbers are extracted as written, with a span
that slices out of the bullet; nothing is restated.

The section makes one flat reading of its own ("the findings existed,
the rejections happened, the reasoning was not recorded. No cost
comparison was made") and this module separates what each bullet
STATES from what the flat reading ADDS -- a bullet reporting "no
documented information" supports "the reasoning was not recorded" and
does not by itself support "no cost comparison was made", which is a
statement about what happened off the record.
Library module: refuses --selftest; the suite is selftest.py.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")

NUM = re.compile(r"\d+(?:\.\d+)?%?")
# markers, composed at call time so this file does not carry the phrases
# it looks for (UNI_010): the bullet states an absence of RECORD ...
RECORD_ABSENT = ("no documented", "no formal", "not recorded")
# ... and the flat reading states an absence of the ACT itself
ACT_ABSENT = ("no cost comparison",)


def section(text=None):
    text = text or open(ORDER, encoding="utf-8").read()
    m = re.search(r"## Evidence that the join is often not even attempted \((.*?)\)\n\n(.*?)\n\n## Open question", text, re.S)
    if not m:
        raise ValueError("Evidence section not found")
    return {"orders_status": m.group(1), "body": m.group(2)}


def findings(text=None):
    """The three case bullets: name, body, numbers as written with spans,
    and whether the bullet itself states an absence of record."""
    sec = section(text)
    bullets = re.findall(r"^- (.*?)(?=\n- |\n\n|\Z)", sec["body"], re.S | re.M)
    out = []
    for b in bullets:
        body = re.sub(r"\s+", " ", b).strip()
        name, _, rest = body.partition(":")
        out.append({"name": name.strip(), "body": body,
                    "status": "CARRIED_NOT_VERIFIED",
                    "orders_status": sec["orders_status"],
                    "numbers_as_written": [{"as_written": m.group(0), "span": [m.start(), m.end()]}
                                           for m in NUM.finditer(body)],
                    "states_record_absent": any(k in body.lower() for k in RECORD_ABSENT)})
    if len(out) != 3:
        raise ValueError("expected three findings, found %d" % len(out))
    return out


def source_line(text=None):
    """The cited source as the order writes it, plus the adjacent
    safety-economics sentence; both carried."""
    sec = section(text)
    cite = re.search(r"\((\w+), ([^,]+), (\d{4})\)", sec["body"])
    adj = re.search(r"Adjacent, same direction: (.*?)\.\s*So\s+(.*?)\.", sec["body"], re.S)
    return {"author": cite.group(1) if cite else "UNPARSED",
            "venue": cite.group(2) if cite else "UNPARSED",
            "year": cite.group(3) if cite else "UNPARSED",
            "adjacent": re.sub(r"\s+", " ", adj.group(1)) if adj else "UNPARSED",
            "so": re.sub(r"\s+", " ", adj.group(2)) if adj else "UNPARSED",
            "status": "CARRIED_NOT_VERIFIED"}


def flat_reading(text=None):
    """The order's own 'Read flat' sentence, split into the clause each
    bullet supports and the clause none of them states."""
    sec = section(text)
    m = re.search(r"Read flat: (.*?)\n\n", sec["body"] + "\n\n", re.S)
    flat = re.sub(r"\s+", " ", m.group(1)) if m else ""
    fs = findings(text)
    supported = [f["name"] for f in fs if f["states_record_absent"]]
    return {"flat": flat,
            "record_absent_clause": {"stated_by_bullets": supported, "n": len(supported), "of": len(fs)},
            "act_absent_clause": {"present_in_flat": any(k in flat.lower() for k in ACT_ABSENT),
                                  "stated_by_bullets": [f["name"] for f in fs if any(k in f["body"].lower() for k in ACT_ABSENT)],
                                  "reading": "absence of record is what the bullets state; absence of the act is the order's reading of the absent record"}}


def render():
    fs = findings()
    src = source_line()
    lines = ["evidence -- parsed from the order, CARRIED (the order's own tag: '%s'; not re-fetched here)" % fs[0]["orders_status"],
             "  source as written: %s, %s, %s  [%s]" % (src["author"], src["venue"], src["year"], src["status"])]
    for f in fs:
        nums = ", ".join("%s @%d-%d" % (n["as_written"], n["span"][0], n["span"][1]) for n in f["numbers_as_written"]) or "none"
        lines.append("  %-16s numbers as written: %-12s states record absent: %s" % (f["name"][:16], nums, f["states_record_absent"]))
    fr = flat_reading()
    lines.append("  flat reading, clause 1 (reasoning not recorded): stated by %d of %d bullets" % (fr["record_absent_clause"]["n"], fr["record_absent_clause"]["of"]))
    lines.append("  flat reading, clause 2 (no cost comparison made): stated by %d bullets; %s" % (len(fr["act_absent_clause"]["stated_by_bullets"]), fr["act_absent_clause"]["reading"]))
    lines.append("  adjacent (carried): %s" % src["adjacent"][:100])
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("library module; run: python3 selftest.py")
        sys.exit(2)
    print(render())
