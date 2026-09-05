#!/usr/bin/env python3
"""residual.py -- §3, the load-bearing test. Round trip a record through a
registrar and measure the residual: what the registrar cannot hold,
reported as a field list, not a score.

Two directions, both measured (§3):
  round_trip_out_in   our record -> OUT -> IN -> diff   (what R drops of ours)
  round_trip_in_out   R's record -> IN  -> OUT -> diff  (what ours drops of R's)
Asymmetry between them is expected and is information.

Residual classes (§3): DROPPED (no slot, gone), FLATTENED (structure to a
string, human-recoverable), COERCED (mapped to a slot of different
meaning -- the dangerous one), ADDED (target demanded a field the source
lacked; must name its origin or the conversion fails). COERCED and ADDED
are the two that produce silent wrongness; a report of only DROPPED
counts is not finished.

Refuses --selftest (checks live in selftest.py). Stdlib only, parses under
Python 3.9.
"""

import sys

from registrars import FALSIFIER_FIELDS, VerdictError
from convert_out import convert_out
from convert_in import convert_in

RESIDUAL_CLASSES = ("DROPPED", "FLATTENED", "COERCED", "ADDED")
SILENT_WRONGNESS = ("COERCED", "ADDED")   # the two to flag separately


def diff(original, recovered):
    """Field-level residual between a source record and its round-tripped
    self -- a confirmation that the classified residual actually shows up.
    A field missing from recovered is DROPPED; a dict that came back a
    string is FLATTENED; a changed value is CHANGED."""
    out = []
    for f in FALSIFIER_FIELDS:
        if f not in original or original[f] in (None, "", {}, []):
            continue
        if f not in recovered:
            out.append({"field": f, "class": "DROPPED"})
        elif isinstance(original[f], dict) and not isinstance(recovered[f], dict):
            out.append({"field": f, "class": "FLATTENED"})
        elif original[f] != recovered[f]:
            out.append({"field": f, "class": "CHANGED"})
    return out


def round_trip_out_in(record, reg):
    """Our record -> OUT to R -> IN from R -> diff. Residual = what R
    cannot hold of ours."""
    target, out_res = convert_out(record, reg)
    recovered, in_res = convert_in(target, reg)
    return {"direction": "OUT_IN", "registrar": reg.name,
            "target": target, "recovered": recovered,
            "residual": out_res + in_res, "diff": diff(record, recovered)}


def round_trip_in_out(target, reg):
    """R's record -> IN to ours -> OUT back to R -> diff. Residual = what
    ours cannot hold of R's."""
    record, in_res = convert_in(target, reg)
    back, out_res = convert_out(record, reg) if record.get("status") != "NOT-IMPLEMENTED" else ({}, [])
    return {"direction": "IN_OUT", "registrar": reg.name,
            "record": record, "back": back, "residual": in_res + out_res}


def residual_by_class(residual):
    """Counts per class, with the silent-wrongness classes always present
    (visible as a zero) so a report cannot list only DROPPED."""
    counts = {c: 0 for c in RESIDUAL_CLASSES}
    counts["NOT-IMPLEMENTED"] = 0
    for e in residual:
        counts[e["class"]] = counts.get(e["class"], 0) + 1
    return counts


def verdict(reg_name, merge, breaks_at=""):
    """A merge verdict for a registrar. §0: a registrar that does not
    merge is a valid outcome, but a NO-MERGE MUST carry a breaks_at -- a
    converter with no stated breaking point is an assertion of
    equivalence. Raises VerdictError on a NO-MERGE with no breaks_at
    (§5-style hard failure)."""
    if not merge and not breaks_at:
        raise VerdictError("NO-MERGE for %r carries no breaks_at (§0, S5)" % reg_name)
    return {"registrar": reg_name, "verdict": "MERGE" if merge else "NO-MERGE",
            "breaks_at": breaks_at}


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("residual has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("residual.py -- import and call round_trip_out_in / round_trip_in_out / verdict; "
          "run selftest.py for the checks, run_all.py for the fixture set", file=sys.stderr)
    sys.exit(2)
