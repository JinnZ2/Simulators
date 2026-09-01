#!/usr/bin/env python3
# hf_incident_extract.py -- CC0, stdlib only, one file, parses under 3.9
#
# WORK_ORDER hf_incident_extract: read a METR/Redwood incident report
# (plus transcripts, if released) and emit COUNTS, no labels.
#
# Two layers, kept apart.
#   text_scan(report_text)  -- mechanical: every duration and count the
#       prose states, with its line number, emitted as CANDIDATES for a
#       reader. A candidate is not a measure; which sentence gives
#       t_characterize is a reading, and a regex deciding it would be the
#       word-list miss this repo records elsewhere.
#   measures(sheet)         -- the six measures computed from a coded
#       SHEET the reader fills from the report, every field carrying a
#       unit or a state. An UNMEASURED field returns None for every
#       measure that needs it -- never 0, never a guess.
#
# Nothing in this file holds a value from the report. The report is not
# in hand (egress here is an allowlist); every real cell is UNMEASURED
# with the input it wants named. The fixtures used to prove the
# instrument works are constructed, and say so.

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

UNMEASURED = "UNMEASURED"        # wanted, not yet read from the report
NOT_COLLECTED = "NOT_COLLECTED"  # the report is silent (OPEN item)
NOT_RELEASED = "NOT_RELEASED"    # transcripts not public

HOURS = {"h": 1.0, "hour": 1.0, "hours": 1.0,
         "d": 24.0, "day": 24.0, "days": 24.0,
         "min": 1.0 / 60, "minute": 1.0 / 60, "minutes": 1.0 / 60}


# ------------------------------------------------------------ the sheet

SHEET = {
    "source": {"report": UNMEASURED, "transcripts": NOT_RELEASED},
    # M1: two durations, each with a unit -- refused without one
    "t_characterize": {"value": UNMEASURED, "unit": None,
                       "wants": "the report's stated time to characterise "
                                "the environment before solving"},
    "t_solve": {"value": UNMEASURED, "unit": None,
                "wants": "the report's stated time to solve once "
                         "characterised"},
    # M2: from the branch tree (transcripts)
    "branches_total": {"value": UNMEASURED, "wants": "branch count in the "
                       "transcript tree"},
    "branches_from_strict_causal": {"value": UNMEASURED,
                                    "wants": "branches whose root is the "
                                             "STRICT_CAUSAL node"},
    # M3: move classes (transcripts)
    "env_edit_moves": {"value": UNMEASURED, "wants": "moves that edit the "
                       "environment (target swap)"},
    "gate_fool_moves": {"value": UNMEASURED, "wants": "moves that fool the "
                        "gate (spoof)"},
    # M4: runs
    "runs_total": {"value": UNMEASURED, "wants": "runs in the reported "
                   "population"},
    "runs_self_failed_for_collective": {"value": UNMEASURED,
                                        "wants": "runs the agent failed "
                                                 "itself for the "
                                                 "collective"},
    # M5: log edits
    "actions_edited": {"value": UNMEASURED, "wants": "edited action "
                       "entries in the log"},
    "reasoning_edited": {"value": UNMEASURED, "wants": "edited reasoning "
                         "entries in the log"},
    # M6: per agent
    "agents": {"value": UNMEASURED,
               "wants": "per agent: did it charge an inert gate as "
                        "adversarial (bool)"},
    # GATE_PROPERTY_TEST inputs
    "gate_declared": {"value": UNMEASURED, "wants": "the gate property "
                      "the paper declares (a set of property names)"},
    "gate_implemented": {"value": UNMEASURED, "wants": "the gate property "
                         "the code implements (a set of property names)"},
    # OPEN
    "post_validation_off_trail_fraction": {"value": NOT_COLLECTED,
                                           "wants": "report silent"},
}


def _num(field):
    """A numeric value, or None when the field is in a non-value state."""
    v = field.get("value")
    if v in (UNMEASURED, NOT_COLLECTED, NOT_RELEASED, None):
        return None
    return float(v)


def _hours(field):
    v = _num(field)
    if v is None:
        return None
    unit = field.get("unit")
    if unit not in HOURS:
        raise ValueError("duration %r carries no unit in %s"
                         % (v, sorted(HOURS)))
    return v * HOURS[unit]


def _ratio(num, den):
    """None if either side is unmeasured; None (not inf) on a zero
    denominator, with the state reported separately."""
    if num is None or den is None:
        return None
    if den == 0:
        return None
    return num / den


# ------------------------------------------------------------ measures

def m1_explore_ratio(sheet):
    return _ratio(_hours(sheet["t_characterize"]), _hours(sheet["t_solve"]))


def m2_root_fanout(sheet):
    return _ratio(_num(sheet["branches_from_strict_causal"]),
                  _num(sheet["branches_total"]))


def m3_upstream_edits(sheet):
    return _ratio(_num(sheet["env_edit_moves"]),
                  _num(sheet["gate_fool_moves"]))


def m4_member_cost(sheet):
    return _ratio(_num(sheet["runs_self_failed_for_collective"]),
                  _num(sheet["runs_total"]))


def m5_log_scrub_split(sheet):
    return _ratio(_num(sheet["actions_edited"]),
                  _num(sheet["reasoning_edited"]))


def m6_opponent_by_slot(sheet):
    """bool per agent, and the count of True. The order asks for the
    bools; the count is the only aggregate emitted."""
    a = sheet["agents"].get("value")
    if a in (UNMEASURED, NOT_RELEASED, NOT_COLLECTED, None):
        return {"per_agent": None, "n_agents": None, "n_charged": None}
    bools = [bool(x) for x in a]
    return {"per_agent": bools, "n_agents": len(bools),
            "n_charged": sum(bools)}


def measures(sheet):
    return {"M1_explore_ratio": m1_explore_ratio(sheet),
            "M2_root_fanout": m2_root_fanout(sheet),
            "M3_upstream_edits": m3_upstream_edits(sheet),
            "M4_member_cost": m4_member_cost(sheet),
            "M5_log_scrub_split": m5_log_scrub_split(sheet),
            "M6_opponent_by_slot": m6_opponent_by_slot(sheet)}


# ---------------------------------------------- the gate property test

# What counts as "high" is not in the order. Stipulated here, declared,
# and swapped by argument; the prediction is reported beside the value.
HIGH = {"M1_explore_ratio": 6.0,   # [CHOICE] days-over-hours reads >= 6
        "M2_root_fanout": 0.5}     # [CHOICE] half or more of branches


def gate_property_test(sheet, high=HIGH):
    """declared(paper) vs implemented(code) -> gap (symmetric difference
    of the two property sets). gap != 0 -> predict M1 high and M2 high.
    The prediction is checked against the measures only where those are
    measured; an unmeasured measure leaves the check None."""
    d = sheet["gate_declared"].get("value")
    i = sheet["gate_implemented"].get("value")
    if d in (UNMEASURED, None) or i in (UNMEASURED, None):
        return {"gap": None, "predict_m1_high": None,
                "predict_m2_high": None, "m1_check": None,
                "m2_check": None}
    gap = sorted(set(d) ^ set(i))
    predict = len(gap) != 0
    m = measures(sheet)
    m1, m2 = m["M1_explore_ratio"], m["M2_root_fanout"]
    return {"gap": gap,
            "predict_m1_high": predict, "predict_m2_high": predict,
            "m1_check": None if m1 is None or not predict
            else (m1 >= high["M1_explore_ratio"]),
            "m2_check": None if m2 is None or not predict
            else (m2 >= high["M2_root_fanout"])}


# ------------------------------------------------------ cross-substrate

SUBSTRATES = ("pea_tendril", "fledgling", "ant_bridge", "fire_crew",
              "swarm")


def substrate_sheet(name, t_char=UNMEASURED, t_char_unit=None,
                    t_solve=UNMEASURED, t_solve_unit=None,
                    runs_total=UNMEASURED, runs_self_failed=UNMEASURED,
                    unit_boundary=UNMEASURED, objective_boundary=UNMEASURED):
    """A sheet for any substrate, same fields, same functions. The name
    is a key and nothing else -- no function reads it."""
    s = json.loads(json.dumps(SHEET))
    s["t_characterize"].update({"value": t_char, "unit": t_char_unit})
    s["t_solve"].update({"value": t_solve, "unit": t_solve_unit})
    s["runs_total"]["value"] = runs_total
    s["runs_self_failed_for_collective"]["value"] = runs_self_failed
    s["unit_boundary"] = unit_boundary
    s["objective_boundary"] = objective_boundary
    s["substrate"] = name
    return s


def boundary_mismatch(sheet):
    u, o = sheet.get("unit_boundary"), sheet.get("objective_boundary")
    if u in (UNMEASURED, None) or o in (UNMEASURED, None):
        return None
    return u != o


def cross_substrate(sheets):
    rows = []
    for s in sheets:
        rows.append({"substrate": s["substrate"],
                     "M1_explore_ratio": m1_explore_ratio(s),
                     "M4_member_cost": m4_member_cost(s),
                     "unit_boundary_ne_objective_boundary":
                         boundary_mismatch(s)})
    return rows


# ------------------------------------------------------------ text scan

_DUR = re.compile(r"\b(\d+(?:\.\d+)?)\s*(hours?|h|days?|d|minutes?|min)\b",
                  re.I)
_CNT = re.compile(r"\b(\d+)\s+(runs?|branches?|agents?|edits?|moves?|"
                  r"episodes?|trajectories|trajectory)\b", re.I)


def text_scan(text):
    """Every stated duration and count, with its line. CANDIDATES for the
    reader filling the sheet -- not measures. Which candidate is
    t_characterize is a reading and stays one."""
    out = {"durations": [], "counts": []}
    for n, line in enumerate(text.splitlines(), 1):
        for m in _DUR.finditer(line):
            out["durations"].append((n, float(m.group(1)),
                                     m.group(2).lower(), line.strip()))
        for m in _CNT.finditer(line):
            out["counts"].append((n, int(m.group(1)),
                                  m.group(2).lower(), line.strip()))
    return out


# ------------------------------------------------------------ open items

def open_items(sheet):
    return {
        "transcripts_released": sheet["source"]["transcripts"] != NOT_RELEASED,
        "M2_to_M5_source": ("transcripts" if sheet["source"]["transcripts"]
                            != NOT_RELEASED else "report figures only"),
        "post_validation_off_trail_fraction":
            sheet["post_validation_off_trail_fraction"]["value"],
    }


# ------------------------------------------------------------------ render

def _fmt(v):
    if v is None:
        return "--"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        return "%.3f" % v
    return str(v)


def render(sheet=None, substrates=None):
    sheet = sheet or SHEET
    out = []
    w = out.append
    w("HF INCIDENT EXTRACT -- counts, no labels")
    w("")
    w("SOURCE")
    w("  report:      %s" % sheet["source"]["report"])
    w("  transcripts: %s" % sheet["source"]["transcripts"])
    w("")
    m = measures(sheet)
    w("MEASURES  (-- = unmeasured; the input it wants is named)")
    names = {"M1_explore_ratio": ("t_characterize", "t_solve"),
             "M2_root_fanout": ("branches_from_strict_causal",
                                "branches_total"),
             "M3_upstream_edits": ("env_edit_moves", "gate_fool_moves"),
             "M4_member_cost": ("runs_self_failed_for_collective",
                                "runs_total"),
             "M5_log_scrub_split": ("actions_edited", "reasoning_edited")}
    for k in ("M1_explore_ratio", "M2_root_fanout", "M3_upstream_edits",
              "M4_member_cost", "M5_log_scrub_split"):
        w("  %-20s %s" % (k, _fmt(m[k])))
        if m[k] is None:
            for f in names[k]:
                w("      wants %-34s %s" % (f + ":", sheet[f]["wants"]))
    m6 = m["M6_opponent_by_slot"]
    w("  %-20s agents %s  charged %s" % ("M6_opponent_by_slot",
                                          _fmt(m6["n_agents"]),
                                          _fmt(m6["n_charged"])))
    if m6["per_agent"] is not None:
        w("      per agent: %s" % m6["per_agent"])
    else:
        w("      wants %-34s %s" % ("agents:", sheet["agents"]["wants"]))
    w("")
    g = gate_property_test(sheet)
    w("GATE_PROPERTY_TEST  (declared vs implemented; gap != 0 -> predict "
      "M1 high, M2 high)")
    w("  gap:            %s" % (_fmt(g["gap"]) if g["gap"] is None
                               else (g["gap"] or "[] (none)")))
    w("  predict M1 high: %s   M2 high: %s" % (_fmt(g["predict_m1_high"]),
                                                 _fmt(g["predict_m2_high"])))
    w("  check M1 high:   %s   M2 high: %s   (thresholds %s, %s -- "
      "stipulated, [CHOICE])"
      % (_fmt(g["m1_check"]), _fmt(g["m2_check"]),
         HIGH["M1_explore_ratio"], HIGH["M2_root_fanout"]))
    w("")
    w("CROSS_SUBSTRATE  (same functions; the name is a key no function "
      "reads)")
    subs = substrates or [substrate_sheet(n) for n in SUBSTRATES]
    w("  %-14s %-8s %-8s %s" % ("substrate", "M1", "M4",
                                 "unit_boundary != objective_boundary"))
    for r in cross_substrate(subs):
        w("  %-14s %-8s %-8s %s" % (r["substrate"], _fmt(r["M1_explore_ratio"]),
                                     _fmt(r["M4_member_cost"]),
                                     _fmt(r["unit_boundary_ne_objective_boundary"])))
    w("")
    o = open_items(sheet)
    w("OPEN")
    w("  transcripts released: %s -> M2..M5 from %s"
      % (o["transcripts_released"], o["M2_to_M5_source"]))
    w("  post-validation off-trail fraction: %s (report silent)"
      % o["post_validation_off_trail_fraction"])
    w("")
    w("No value in this file is from the report. Every -- names what would")
    w("fill it. The counts are computed from a coded sheet; the text scan")
    w("emits candidates with line numbers for the reader who codes it.")
    return "\n".join(out)


def _usage():
    return ("usage: hf_incident_extract.py [--sheet SHEET.json] "
            "[--scan REPORT.txt]\n"
            "  --sheet  compute the measures from a coded sheet\n"
            "  --scan   list every stated duration and count, with line\n"
            "  (no args) render the unfilled instrument")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.stderr.write("hf_incident_extract.py has no checks of its own; "
                         "they live in selftest_hf.py.\n")
        sys.exit(2)
    if "--scan" in argv:
        path = argv[argv.index("--scan") + 1]
        sc = text_scan(io.open(path, encoding="utf-8").read())
        print("CANDIDATES (line, value, unit, sentence) -- not measures")
        for row in sc["durations"]:
            print("  dur   %4d  %8.2f %-7s %s" % row)
        for row in sc["counts"]:
            print("  count %4d  %8d %-7s %s" % row)
        sys.exit(0)
    if "--sheet" in argv:
        path = argv[argv.index("--sheet") + 1]
        sheet = json.load(io.open(path, encoding="utf-8"))
        print(render(sheet))
        sys.exit(0)
    print(render())
