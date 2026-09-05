#!/usr/bin/env python3
"""survey.py -- the term/substrate grid and cell coding for the
cross-substrate dependency survey. The cells live in CELLS.md (data);
this file is the logic. A cell not in CELLS.md is UNKNOWN.

Two admissibility bars, per ADDENDUM_01 (a RESCOPE, not a narrow):
  MEASURED         needs a MEASURED_AS that states units; a cell with no
                   units is not MEASURED and cannot seed a gap.
  SCOPE-DIFFERENT  needs a SCOPE_TRANSFORM (reference / maps_to /
                   breaks_at), NOT units -- frame information is not
                   denominated in the quantity's units. A prose note
                   with none of the three is not admissible and
                   downgrades to UNKNOWN, counted apart from the
                   never-coded UNKNOWN cells.
Both bars keep the table from becoming a vocabulary map.

    python3 survey.py            # the parsed grid, validity flagged
Refuses --selftest (checks live in selftest_ds.py). Stdlib only.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = os.path.join(HERE, "CELLS.md")

TERMS = [
    ("T1", "cost asymmetry"),
    ("T2", "whether the aggregate steers (incentive direction)"),
    ("T3", "what sits inside vs outside the accounting boundary"),
    ("T4", "whether a legitimate other is representable at all"),
    ("T5", "does the accounting stance preserve or destroy the measurement it depends on"),
]
SUBSTRATES = [
    ("S1", "foraging / predation ecology"),
    ("S2", "multiagent AI harnesses"),
    ("S3", "human societies and mutual aid"),
    ("S4", "morality / ethics claims"),
    ("S5", "nation-state sovereignty"),
]
STATUSES = ("MEASURED", "MISSING", "SCOPE-DIFFERENT", "UNKNOWN")
TRANSFORM_FIELDS = ("reference", "maps_to", "breaks_at")

# Units heuristic: a MEASURED_AS "states units" if it carries a slash
# rate, a percent, the word "per", or a whole-word unit. [CHOICE 1] the
# word set. Matched on WORD BOUNDARIES -- a substring test lets "pa"
# match "parties" and "rate" match "operate" (UNI_009 bleed), so a bare
# unit word is required, not a substring.
UNIT_WORDS = frozenset("""joule joules watt watts sec second seconds bit bits byte bytes ppm ppb
kg km metre metres meter meters hz hertz ratio fraction probability count counts dollar dollars
kcal cal calorie calories year years day days hour hours minute minutes pascal kwh percent
dimensionless""".split())
BLOCK = re.compile(r"^##\s+(T\d)\s*x\s*(S\d)\s*$", re.I)
KV = re.compile(r"^([a-z_]+):\s*(.*)$", re.I)
WORD = re.compile(r"[a-z]+")


def has_units(measured_as):
    if not measured_as:
        return False
    low = measured_as.lower()
    if "/" in low or "%" in low:
        return True
    words = WORD.findall(low)
    if "per" in words:
        return True
    return any(w in UNIT_WORDS for w in words)


def parse_cells(path=CELLS):
    """Parse CELLS.md into {(T,S): fields}. Only well-formed blocks are
    read; a block with an unknown status is kept and flagged by validate."""
    cells = {}
    cur = None
    for line in open(path, encoding="utf-8").read().splitlines():
        m = BLOCK.match(line.strip())
        if m:
            cur = (m.group(1).upper(), m.group(2).upper())
            cells[cur] = _blank()
            continue
        if cur is None:
            continue
        kv = KV.match(line.strip())
        if not kv:
            continue
        k, v = kv.group(1).lower(), kv.group(2).strip()
        if k == "status":
            cells[cur]["status"] = v.upper()
        elif k in ("provisional", "no_transfer"):
            cells[cur][k] = v.lower() in ("yes", "true", "1")
        elif k in ("measured_as", "scope_note", "source", "transfer",
                   "reference", "maps_to", "breaks_at"):
            cells[cur][k] = v
    return cells


def _blank(status=None):
    d = {"status": status, "measured_as": "", "scope_note": "", "source": "",
         "provisional": False, "transfer": "", "no_transfer": False}
    for f in TRANSFORM_FIELDS:
        d[f] = ""
    return d


def grid(path=CELLS):
    """All 25 cells, defaulting UNKNOWN, with validity and effective
    status computed."""
    coded = parse_cells(path)
    out = {}
    for t, _ in TERMS:
        for s, _ in SUBSTRATES:
            key = (t, s)
            c = coded.get(key)
            if c is None or c["status"] is None:
                out[key] = dict(_blank("UNKNOWN"), valid=True, invalid_reason="",
                                effective_status="UNKNOWN")
                continue
            valid, reason = validate(c)
            out[key] = dict(c, valid=valid, invalid_reason=reason,
                            effective_status=effective_status(c, valid))
    return out


def validate(cell):
    """Returns (valid, reason). Two admissibility bars, per ADDENDUM_01.
    MEASURED needs units; SCOPE-DIFFERENT needs a complete SCOPE_TRANSFORM
    (reference / maps_to / breaks_at), NOT units."""
    st = cell["status"]
    if st not in STATUSES:
        return False, "status %r is not one of %s" % (st, STATUSES)
    if st == "MEASURED":
        if not cell["measured_as"]:
            return False, "MEASURED requires MEASURED_AS; none given"
        if not has_units(cell["measured_as"]):
            return False, "MEASURED MEASURED_AS states no units; a cell with no units cannot be MEASURED"
    if st == "SCOPE-DIFFERENT":
        absent = [f for f in TRANSFORM_FIELDS if not cell.get(f)]
        if absent:
            return False, ("SCOPE-DIFFERENT requires a complete SCOPE_TRANSFORM "
                           "(reference, maps_to, breaks_at); absent: %s" % ", ".join(absent))
    return True, ""


def effective_status(cell, valid):
    """An admissible cell keeps its status. An inadmissible MEASURED
    downgrades to MISSING (it cannot be the measured side of a gap); an
    inadmissible SCOPE-DIFFERENT downgrades to UNKNOWN (per ADDENDUM_01:
    a scope note with no transform is not admissible), counted apart from
    the never-coded UNKNOWN cells."""
    st = cell["status"]
    if valid:
        return st
    if st == "MEASURED":
        return "MISSING (downgraded: no units)"
    if st == "SCOPE-DIFFERENT":
        return "UNKNOWN (downgraded: incomplete transform)"
    return "%s (inadmissible)" % st


def scope_incomplete_cells(g=None):
    """Cells coded SCOPE-DIFFERENT that lack a complete transform: coded,
    inadmissible, downgraded to UNKNOWN, and reported on their own line."""
    g = g if g is not None else grid()
    return [k for k in sorted(g) if g[k]["status"] == "SCOPE-DIFFERENT" and not g[k]["valid"]]


def is_valid_measured(cell):
    return cell["effective_status"] == "MEASURED" and cell["valid"]


def counts(g=None):
    """Admissible statuses are counted as themselves; an inadmissible
    MEASURED is counted under measured_no_units and an inadmissible
    SCOPE-DIFFERENT under scope_incomplete, so neither is silently folded
    into a valid status or into the never-coded UNKNOWN count."""
    g = g if g is not None else grid()
    out = {"UNKNOWN": 0, "MEASURED": 0, "MISSING": 0, "SCOPE-DIFFERENT": 0,
           "scope_incomplete": 0, "measured_no_units": 0}
    for c in g.values():
        st = c["status"]
        if st == "SCOPE-DIFFERENT":
            out["SCOPE-DIFFERENT" if c["valid"] else "scope_incomplete"] += 1
        elif st == "MEASURED":
            out["MEASURED" if c["valid"] else "measured_no_units"] += 1
        elif st == "MISSING":
            out["MISSING"] += 1
        else:
            out["UNKNOWN"] += 1
    return out


def render(g=None):
    g = g if g is not None else grid()
    L = ["dependency survey grid (5 terms x 5 substrates)"]
    header = "%-4s" % "" + "".join("%-6s" % s for s, _ in SUBSTRATES)
    L.append(header)
    tag = {"MEASURED": "MEAS", "MISSING": "MISS", "SCOPE-DIFFERENT": "SCOPE", "UNKNOWN": "?"}
    for t, _ in TERMS:
        row = "%-4s" % t
        for s, _ in SUBSTRATES:
            c = g[(t, s)]
            mark = tag.get(c["status"], "?")
            if not c["valid"]:
                mark += "*"
            row += "%-6s" % mark
        L.append(row)
    L.append("* = coded but fails its admissibility bar (units for MEASURED, transform for SCOPE-DIFFERENT); see validation")
    inval = [(k, g[k]["invalid_reason"]) for k in sorted(g) if not g[k]["valid"]]
    if inval:
        L.append("validation:")
        for k, reason in inval:
            L.append("  %s x %s -- %s" % (k[0], k[1], reason))
    L.append("counts: %s" % counts(g))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("survey has no selftest; run selftest_ds.py", file=sys.stderr)
        sys.exit(2)
    print(render())
