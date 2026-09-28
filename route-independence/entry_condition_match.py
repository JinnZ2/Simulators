# SPDX-License-Identifier: CC0-1.0
"""entry_condition_match.py -- match entry conditions before transferring a result.

FWO-1. A study's result is transferred to a population only after the
population is shown to meet the study's entry conditions, row by row.
The instrument reports what matched, what did not, and what could not be
evaluated. It does not say whether the transfer is right.

INPUT FILES  (one row per entry condition; `#` comments; blank lines skipped)

    header (optional):   study: NAME        or   population: NAME
    row:                 condition | state | source [| key=value ...]

    state in {DECOUPLED, COUPLED, REMOVED, PRESENT, UNKNOWN}

    DECOUPLED  provision arrives without the recipient's effort or exchange
    COUPLED    provision stops when effort stops
    This is BINARY. A gradient word (PARTLY_DECOUPLED, MOSTLY_COUPLED, a
    number) is refused as INVALID_STATE, never read as one side. High
    consumption with effort-coupling is COUPLED. (OBSERVED, stated by the
    person who raised the case; carried from the work order.)

    Optional marker, any row:  dwellings_held=N
    N > 1 derives DECOUPLED for that row (a body occupies one dwelling at a
    time; holdings past physical occupancy are no longer meeting the need).
    N <= 1 says nothing. A stated state that disagrees with the marker is
    reported as marker_conflict and the marker's reading is used.

    Optional marker, study rows only:  load_bearing=no
    Every study row is load-bearing unless marked. [CHOICE 1]

    A row with an empty source is SOURCED=False and printed as SYNTHETIC.
    The instrument cannot check a source; it can only see whether one is
    stated.

PER ROW      MATCH | MISMATCH | UNKNOWN(reason)
    reason in {study_row_unknown, population_row_unknown,
               population_row_absent}
    A population row the study does not name is listed as extra and
    enters no count.

OVERALL
    TRANSFERABLE       every study row MATCH
    PARTIAL            at least one MATCH and at least one MISMATCH; both
                       lists are returned
    NOT_TRANSFERABLE   no row MATCH, at least one MISMATCH
    NOT_EVALUABLE      any load-bearing row UNKNOWN, or every row UNKNOWN
    PARTIAL and NOT_TRANSFERABLE are kept distinct.

    [CHOICE 1] load-bearing: a load-bearing UNKNOWN row makes the whole
    comparison NOT_EVALUABLE. A row marked load_bearing=no that is UNKNOWN
    is excluded from the tally and listed; it still blocks TRANSFERABLE,
    since "every row MATCH" is not true of it, so a comparison with only
    such rows unresolved reads NOT_EVALUABLE(unknown_rows_block_transferable)
    rather than TRANSFERABLE.

REFUSALS (typed, returned, never raised past the CLI)
    INVALID_STATE(row, value)     gradient or unknown word in the state field
    MALFORMED_ROW(line)           fewer than two fields
    DUPLICATE_CONDITION(name)     the same condition twice in one file
"""

import sys

STATES = ("DECOUPLED", "COUPLED", "REMOVED", "PRESENT", "UNKNOWN")

MATCH = "MATCH"
MISMATCH = "MISMATCH"
UNKNOWN = "UNKNOWN"

TRANSFERABLE = "TRANSFERABLE"
PARTIAL = "PARTIAL"
NOT_TRANSFERABLE = "NOT_TRANSFERABLE"
NOT_EVALUABLE = "NOT_EVALUABLE"
OVERALLS = (TRANSFERABLE, PARTIAL, NOT_TRANSFERABLE, NOT_EVALUABLE)

CHOICES = {
    1: "every study row is load-bearing unless marked load_bearing=no; an "
       "UNKNOWN on a non-load-bearing row is excluded from the tally but "
       "still blocks TRANSFERABLE",
    2: "dwellings_held > 1 derives DECOUPLED and overrides a stated state, "
       "reported as marker_conflict; dwellings_held <= 1 derives nothing",
    3: "a population row the study does not name is listed as extra and "
       "enters no count",
}


def parse_rows(text):
    """Parse a study or population file.

    Returns (name, rows, refusals). rows is a list of dicts in file order:
      condition, state, source, sourced, markers (dict), derived_from_marker,
      marker_conflict, load_bearing, line
    refusals is a list of (kind, detail) and is empty when the file is clean.
    A file with any refusal must not be evaluated; the caller decides.
    """
    name = None
    rows = []
    refusals = []
    seen = set()
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith("study:") or low.startswith("population:"):
            name = line.split(":", 1)[1].strip()
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            refusals.append(("MALFORMED_ROW", "line %d: %r" % (lineno, raw.strip())))
            continue
        condition = parts[0]
        state = parts[1].upper()
        source = parts[2] if len(parts) > 2 else ""
        markers = {}
        for extra in parts[3:]:
            if "=" in extra:
                k, v = extra.split("=", 1)
                markers[k.strip()] = v.strip()
        if condition in seen:
            refusals.append(("DUPLICATE_CONDITION", condition))
            continue
        seen.add(condition)
        if state not in STATES:
            refusals.append(("INVALID_STATE",
                             "row %r: %r is not one of %s (binary field; "
                             "gradients are refused)" % (condition, parts[1], "/".join(STATES))))
            continue
        derived = False
        conflict = None
        if "dwellings_held" in markers:
            try:
                held = int(markers["dwellings_held"])
            except ValueError:
                refusals.append(("INVALID_MARKER",
                                 "row %r: dwellings_held=%r is not an integer"
                                 % (condition, markers["dwellings_held"])))
                continue
            if held > 1:
                if state not in ("UNKNOWN", "DECOUPLED"):
                    conflict = "stated %s, marker derives DECOUPLED" % state
                state = "DECOUPLED"
                derived = True
        load_bearing = markers.get("load_bearing", "yes").lower() != "no"
        rows.append({
            "condition": condition,
            "state": state,
            "source": source,
            "sourced": bool(source) and source.upper() != "SYNTHETIC",
            "markers": markers,
            "derived_from_marker": derived,
            "marker_conflict": conflict,
            "load_bearing": load_bearing,
            "line": lineno,
        })
    return name, rows, refusals


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return parse_rows(handle.read())


def match_row(study_row, pop_row):
    """One row. pop_row may be None (absent from the population file)."""
    if pop_row is None:
        return UNKNOWN, "population_row_absent"
    if study_row["state"] == UNKNOWN:
        return UNKNOWN, "study_row_unknown"
    if pop_row["state"] == UNKNOWN:
        return UNKNOWN, "population_row_unknown"
    if study_row["state"] == pop_row["state"]:
        return MATCH, None
    return MISMATCH, None


def evaluate(study_rows, pop_rows):
    """Compare a population against a study, row by row, then overall."""
    by_name = dict((r["condition"], r) for r in pop_rows)
    per_row = []
    hold, fail, unknown_lb, unknown_nlb = [], [], [], []
    for s in study_rows:
        p = by_name.get(s["condition"])
        result, reason = match_row(s, p)
        per_row.append({
            "condition": s["condition"],
            "study_state": s["state"],
            "population_state": p["state"] if p else None,
            "result": result,
            "reason": reason,
            "load_bearing": s["load_bearing"],
            "study_sourced": s["sourced"],
            "population_sourced": p["sourced"] if p else None,
            "derived_from_marker": bool(p and p["derived_from_marker"]),
            "marker_conflict": p["marker_conflict"] if p else None,
        })
        if result == MATCH:
            hold.append(s["condition"])
        elif result == MISMATCH:
            fail.append(s["condition"])
        elif s["load_bearing"]:
            unknown_lb.append(s["condition"])
        else:
            unknown_nlb.append(s["condition"])
    extra = [r["condition"] for r in pop_rows if r["condition"] not in
             set(s["condition"] for s in study_rows)]

    if not study_rows:
        overall, reason = NOT_EVALUABLE, "no study rows"
    elif unknown_lb:
        overall, reason = NOT_EVALUABLE, "load-bearing rows UNKNOWN: " + ", ".join(unknown_lb)
    elif hold and fail:
        overall, reason = PARTIAL, None
    elif fail:
        overall, reason = NOT_TRANSFERABLE, None
    elif unknown_nlb:
        overall, reason = NOT_EVALUABLE, ("unknown_rows_block_transferable: "
                                          + ", ".join(unknown_nlb))
    else:
        overall, reason = TRANSFERABLE, None

    return {
        "overall": overall,
        "reason": reason,
        "hold": hold,
        "fail": fail,
        "unknown_load_bearing": unknown_lb,
        "unknown_not_load_bearing": unknown_nlb,
        "extra_population_rows": extra,
        "rows": per_row,
        "synthetic_rows": [r["condition"] for r in per_row
                           if r["population_sourced"] is False or not r["study_sourced"]],
    }


def render(study_name, pop_name, result):
    lines = ["study:      %s" % (study_name or "(unnamed)"),
             "population: %s" % (pop_name or "(unnamed)"),
             ""]
    for r in result["rows"]:
        tag = r["result"]
        if r["reason"]:
            tag = "%s(%s)" % (tag, r["reason"])
        flags = []
        if not r["study_sourced"]:
            flags.append("study:SYNTHETIC")
        if r["population_sourced"] is False:
            flags.append("population:SYNTHETIC")
        if r["derived_from_marker"]:
            flags.append("derived:dwellings_held")
        if r["marker_conflict"]:
            flags.append("marker_conflict")
        if not r["load_bearing"]:
            flags.append("not_load_bearing")
        lines.append("  %-15s %-10s vs %-10s %-32s %s" % (
            r["condition"], r["study_state"], r["population_state"] or "-",
            tag, " ".join(flags)))
    lines.append("")
    overall = result["overall"]
    if overall == PARTIAL:
        lines.append("overall: PARTIAL  hold=[%s]  fail=[%s]" % (
            ", ".join(result["hold"]), ", ".join(result["fail"])))
    elif result["reason"]:
        lines.append("overall: %s  (%s)" % (overall, result["reason"]))
    else:
        lines.append("overall: %s" % overall)
    if result["unknown_not_load_bearing"] and overall != NOT_EVALUABLE:
        lines.append("  unknown, not load-bearing, excluded from tally: %s"
                     % ", ".join(result["unknown_not_load_bearing"]))
    if result["extra_population_rows"]:
        lines.append("  extra population rows (not counted): %s"
                     % ", ".join(result["extra_population_rows"]))
    if result["synthetic_rows"]:
        lines.append("  rows with an unsourced side (SYNTHETIC): %s"
                     % ", ".join(result["synthetic_rows"]))
    lines.append("")
    lines.append("scope: the instrument checks whether stated entry conditions match;")
    lines.append("       it does not check the stated conditions, and it does not say")
    lines.append("       whether a transfer that matches is sound.")
    return "\n".join(lines)


def render_refusals(label, refusals):
    lines = ["%s: not evaluated, %d refusal(s)" % (label, len(refusals))]
    for kind, detail in refusals:
        lines.append("  %-20s %s" % (kind, detail))
    return "\n".join(lines)


def main(argv):
    args = argv[1:]
    if args == ["--choices"]:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if args == ["--selftest"]:
        sys.stderr.write("library module; run: python3 route-independence/test_route.py\n")
        return 2
    if len(args) != 2:
        sys.stderr.write("usage: entry_condition_match.py STUDY.txt POPULATION.txt\n"
                         "       entry_condition_match.py --choices\n")
        return 2
    s_name, s_rows, s_ref = load(args[0])
    p_name, p_rows, p_ref = load(args[1])
    rc = 0
    if s_ref:
        print(render_refusals("study", s_ref))
        rc = 2
    if p_ref:
        print(render_refusals("population", p_ref))
        rc = 2
    if rc:
        return rc
    print(render(s_name, p_name, evaluate(s_rows, p_rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
