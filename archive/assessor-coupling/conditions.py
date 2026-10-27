"""WO-6, the remedy set as an instrument.

The eight INDEPENDENCE CONDITIONS are parsed out of WORK_ORDER.md at call
time and never retyped. A scoring is a set of DECLARED per-condition
states, one of MET / FAILS / UNVERIFIABLE / UNDECLARED; the instrument
counts them and reports each column, and no composite is emitted. The
hop-1 test (does the assessed pay the assessor) is a separate field and
is never read as any of the eight.

The one scoring shipped is the order's own current-position section,
carried as CARRIED: its source is the order's reading of public
statements, re-verified here against nothing. No organization is named
anywhere in this folder and no field of this record can carry one.

Library module: refuses --selftest; the suite is selftest.py.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")
STATES = ("MET", "FAILS", "UNVERIFIABLE", "UNDECLARED")
DEFENSE_ITEMS = 4  # the order's "common prior defense" lists four


def conditions(text=None):
    """The eight conditions, parsed from the fenced INDEPENDENCE CONDITIONS
    block: id -> (title, gloss). Raises if the block is not there or does
    not hold eight, so a retyped copy cannot drift silently."""
    text = text if text is not None else open(ORDER, encoding="utf-8").read()
    m = re.search(r"```\nINDEPENDENCE CONDITIONS\n(.*?)```", text, re.S)
    if not m:
        raise ValueError("INDEPENDENCE CONDITIONS block not found in the order")
    out = {}
    cur = None
    for line in m.group(1).splitlines():
        head = re.match(r"\s+(\d)\s+(.+)$", line)
        if head and head.group(2).strip().isupper():
            cur = int(head.group(1))
            out[cur] = [head.group(2).strip(), ""]
        elif cur is not None and line.strip():
            out[cur][1] = (out[cur][1] + " " + line.strip()).strip()
    if sorted(out) != list(range(1, 9)):
        raise ValueError("expected conditions 1..8, parsed %s" % sorted(out))
    return {k: tuple(v) for k, v in out.items()}


def defense(text=None):
    """The four items of the common prior defense, parsed from the order."""
    text = text if text is not None else open(ORDER, encoding="utf-8").read()
    m = re.search(r"### The common prior defense\n(.*?)\n## ", text, re.S)
    if not m:
        raise ValueError("common prior defense block not found")
    items = [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ")]
    if len(items) != DEFENSE_ITEMS:
        raise ValueError("expected %d defense items, parsed %d" % (DEFENSE_ITEMS, len(items)))
    return items


def carried_scoring():
    """The order's 'Current position in AI evaluation' as a record. Every
    state is the order's own; source names where it came from. No party
    is named because the order names none."""
    return {
        "subject": "AI evaluation, as a field, no party named",
        "source": "CARRIED: the order's reading of public statements; re-verified against nothing here",
        "hop1_stated": True,
        "states": {1: "UNDECLARED", 2: "UNVERIFIABLE", 3: "FAILS", 4: "FAILS",
                   5: "FAILS", 6: "FAILS", 7: "FAILS", 8: "FAILS"},
        "defense_stated": [True, True, True, True],
    }


def score(record):
    """Counts per state over the eight conditions. A missing condition is
    UNDECLARED; an unknown state is refused. No composite."""
    if not isinstance(record, dict):
        return {"state": "MALFORMED", "why": "record is not a dict"}
    if any(isinstance(v, str) and _looks_named(v) for v in record.values()):
        return {"state": "REFUSED_NAMED_PARTY",
                "why": "the order is NOT ABOUT ANY NAMED ORGANIZATION; a name-shaped subject is refused"}
    states = record.get("states") or {}
    per = {}
    for cid in range(1, 9):
        s = states.get(cid, states.get(str(cid), "UNDECLARED"))
        if s not in STATES:
            return {"state": "MALFORMED", "why": "condition %d carries state %r" % (cid, s)}
        per[cid] = s
    counts = {s: sum(1 for v in per.values() if v == s) for s in STATES}
    hop1 = record.get("hop1_stated")
    return {"state": "SCORED", "per_condition": per, "counts": counts,
            "hop1_stated": hop1 if isinstance(hop1, bool) else "UNDECLARED",
            "hop1_reaches_condition": None,   # the hop-1 test is not one of the eight; asserted
            "met": [c for c, s in per.items() if s == "MET"],
            "fails": [c for c, s in per.items() if s == "FAILS"],
            "unverifiable": [c for c, s in per.items() if s == "UNVERIFIABLE"],
            "undeclared": [c for c, s in per.items() if s == "UNDECLARED"]}


def _looks_named(s):
    """A subject string carrying a registered-entity marker. A word list,
    stated: it refuses obvious names and cannot refuse a paraphrase."""
    return bool(re.search(r"\b(Inc|LLC|Ltd|Corp|GmbH|plc|Foundation|Institute)\b\.?", s))


def defense_effect(record):
    """The common prior defense stated in full moves NO condition: the
    scoring with all four items TRUE and with all four FALSE returns the
    same per-condition states. This is the order's 'true at the transfer
    level and the structure failed anyway' as an invariance."""
    a = dict(record, defense_stated=[True] * DEFENSE_ITEMS)
    b = dict(record, defense_stated=[False] * DEFENSE_ITEMS)
    sa, sb = score(a), score(b)
    if sa.get("state") != "SCORED" or sb.get("state") != "SCORED":
        return {"state": "NOT_EVALUABLE"}
    return {"state": "INVARIANT" if sa["per_condition"] == sb["per_condition"] else "MOVES",
            "conditions_moved": [c for c in range(1, 9) if sa["per_condition"][c] != sb["per_condition"][c]]}


def render(record=None):
    record = record or carried_scoring()
    conds = conditions()
    sc = score(record)
    lines = ["conditions -- WO-6, the eight INDEPENDENCE CONDITIONS as a scorer",
             "  conditions parsed from WORK_ORDER.md at call time; scoring CARRIED from the order",
             "  subject: %s" % record.get("subject"),
             "  source:  %s" % record.get("source"),
             "  hop-1 (assessed pays assessor) stated: %s   -- a routing question, not one of the eight" % sc.get("hop1_stated")]
    if sc["state"] != "SCORED":
        lines.append("  state: %s  %s" % (sc["state"], sc.get("why", "")))
        return "\n".join(lines)
    for cid in range(1, 9):
        lines.append("    %d  %-13s %s" % (cid, sc["per_condition"][cid], conds[cid][0]))
    lines.append("  counts: " + "  ".join("%s %d" % (s, sc["counts"][s]) for s in STATES) + "   (no composite)")
    de = defense_effect(record)
    lines.append("  common prior defense, all four items stated vs none: %s  moved=%s" % (de["state"], de.get("conditions_moved")))
    lines.append("  reading: the defense is stated at the transfer level and the eight are structural; stating")
    lines.append("           it moves none of them, which is the order's finding as an invariance")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("conditions.py is a library; run python3 selftest.py\n")
        return 2
    rec = None
    if "--record" in argv:
        rec = json.load(open(argv[argv.index("--record") + 1]))
    print(render(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
