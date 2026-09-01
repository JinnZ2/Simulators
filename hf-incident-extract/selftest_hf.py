#!/usr/bin/env python3
# selftest_hf.py -- CC0, stdlib only, parses under 3.9
#
# The checks that exercise hf_incident_extract.py. Every measure is
# checked on a CONSTRUCTED sheet with known ratios (known answer first),
# then on the unfilled sheet (every measure None, never 0), then the
# gate test both ways, the cross-substrate vocabulary invariance by AST,
# and the text scan against planted and decoy lines. No value here is
# from any report.

import ast
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import hf_incident_extract as H  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def constructed_sheet():
    s = json.loads(json.dumps(H.SHEET))
    s["source"] = {"report": "CONSTRUCTED", "transcripts": "CONSTRUCTED"}
    s["t_characterize"].update({"value": 3, "unit": "days"})     # 72 h
    s["t_solve"].update({"value": 4, "unit": "hours"})           # 4 h
    s["branches_total"]["value"] = 10
    s["branches_from_strict_causal"]["value"] = 7
    s["env_edit_moves"]["value"] = 9
    s["gate_fool_moves"]["value"] = 3
    s["runs_total"]["value"] = 20
    s["runs_self_failed_for_collective"]["value"] = 5
    s["actions_edited"]["value"] = 40
    s["reasoning_edited"]["value"] = 2
    s["agents"]["value"] = [True, False, True, True]
    s["gate_declared"]["value"] = ["deterministic", "inert"]
    s["gate_implemented"]["value"] = ["deterministic"]
    return s


def run():
    # ---- known answers on a constructed sheet
    s = constructed_sheet()
    m = H.measures(s)
    chk("M1: 3 days over 4 hours is 18.0", abs(m["M1_explore_ratio"] - 18.0) < 1e-12)
    chk("M2: 7 of 10 branches is 0.7", abs(m["M2_root_fanout"] - 0.7) < 1e-12)
    chk("M3: 9 env-edit over 3 gate-fool is 3.0",
        abs(m["M3_upstream_edits"] - 3.0) < 1e-12)
    chk("M4: 5 of 20 runs is 0.25", abs(m["M4_member_cost"] - 0.25) < 1e-12)
    chk("M5: 40 over 2 is 20.0", abs(m["M5_log_scrub_split"] - 20.0) < 1e-12)
    m6 = m["M6_opponent_by_slot"]
    chk("M6: four agents, three charged, bools preserved",
        m6["n_agents"] == 4 and m6["n_charged"] == 3
        and m6["per_agent"] == [True, False, True, True])

    # ---- the unfilled sheet: every measure None, never 0
    u = H.measures(H.SHEET)
    chk("unfilled: M1..M5 are None, not 0",
        all(u[k] is None for k in ("M1_explore_ratio", "M2_root_fanout",
                                   "M3_upstream_edits", "M4_member_cost",
                                   "M5_log_scrub_split")))
    chk("unfilled: M6 carries no count", u["M6_opponent_by_slot"]["n_agents"] is None)
    # a half-filled ratio stays None (one side unmeasured is not a number)
    h = json.loads(json.dumps(H.SHEET))
    h["runs_total"]["value"] = 20
    chk("one side unmeasured -> None, not a division by the known side",
        H.m4_member_cost(h) is None)
    # a zero denominator is None with the numerator intact
    z = constructed_sheet(); z["reasoning_edited"]["value"] = 0
    chk("zero denominator -> None, not inf", H.m5_log_scrub_split(z) is None)
    # durations refuse to be unitless
    n = constructed_sheet(); n["t_solve"]["unit"] = None
    try:
        H.m1_explore_ratio(n); chk("a unitless duration is refused", False)
    except ValueError:
        chk("a unitless duration is refused", True)
    # unit conversion is real: the same 72 h stated in hours gives 18.0
    e = constructed_sheet(); e["t_characterize"].update({"value": 72, "unit": "h"})
    chk("days and hours convert to one scale", abs(H.m1_explore_ratio(e) - 18.0) < 1e-12)

    # ---- the gate property test, both ways
    g = H.gate_property_test(s)
    chk("declared vs implemented gap is the symmetric difference",
        g["gap"] == ["inert"])
    chk("gap != 0 predicts M1 high and M2 high",
        g["predict_m1_high"] is True and g["predict_m2_high"] is True)
    chk("the prediction is checked against the measured values",
        g["m1_check"] is True and g["m2_check"] is True)
    s0 = constructed_sheet(); s0["gate_implemented"]["value"] = ["deterministic", "inert"]
    g0 = H.gate_property_test(s0)
    chk("gap == 0 predicts nothing and checks nothing (the test can "
        "come back the other way)",
        g0["gap"] == [] and g0["predict_m1_high"] is False
        and g0["m1_check"] is None)
    lo = constructed_sheet(); lo["t_characterize"].update({"value": 8, "unit": "h"})
    glo = H.gate_property_test(lo)
    chk("a predicted-high M1 that measures low fails the check (the "
        "charter signature can be absent)", glo["m1_check"] is False)
    chk("the unfilled sheet returns a None gap, not an empty one",
        H.gate_property_test(H.SHEET)["gap"] is None)

    # ---- cross-substrate: same functions, no vocabulary in any body
    src = io.open(os.path.join(HERE, "hf_incident_extract.py"),
                  encoding="utf-8").read()
    tree = ast.parse(src)
    leaks = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            body = ast.dump(node)
            for name in H.SUBSTRATES:
                if name in body:
                    leaks.append((node.name, name))
    chk("no function body names a substrate (vocabulary invariance, by AST)",
        leaks == [])
    rows = H.cross_substrate([H.substrate_sheet(n) for n in H.SUBSTRATES])
    chk("five substrate rows, every cell unmeasured (no value supplied "
        "from memory)",
        len(rows) == 5 and all(r["M1_explore_ratio"] is None
                               and r["M4_member_cost"] is None
                               and r["unit_boundary_ne_objective_boundary"]
                               is None for r in rows))
    f = H.substrate_sheet("fire_crew", 2, "days", 4, "h", 10, 3,
                          "individual", "crew")
    r = H.cross_substrate([f])[0]
    chk("a filled substrate sheet computes through the same functions",
        abs(r["M1_explore_ratio"] - 12.0) < 1e-12
        and abs(r["M4_member_cost"] - 0.3) < 1e-12
        and r["unit_boundary_ne_objective_boundary"] is True)
    same = H.substrate_sheet("swarm", 2, "days", 4, "h", 10, 3, "unit", "unit")
    chk("equal boundaries read False, not None",
        H.cross_substrate([same])[0]["unit_boundary_ne_objective_boundary"]
        is False)

    # ---- the text scan: planted lines found, decoys not promoted
    text = ("Characterising the environment took 3 days.\n"
            "The solve itself took 4 hours.\n"
            "Across 20 runs the agent branched 10 times.\n"
            "Version 2.0 of the harness was used.\n")   # decoy: no unit
    sc = H.text_scan(text)
    chk("the scan finds both durations with their lines",
        [(d[0], d[1], d[2]) for d in sc["durations"]]
        == [(1, 3.0, "days"), (2, 4.0, "hours")])
    chk("the scan finds the run count", any(c[1] == 20 and c[2] == "runs"
                                            for c in sc["counts"]))
    chk("a bare version number is not a duration or a count",
        not any(d[0] == 4 for d in sc["durations"])
        and not any(c[0] == 4 for c in sc["counts"]))
    chk("the scan emits candidates, and no measure",
        "durations" in sc and "M1_explore_ratio" not in sc)

    # ---- open items
    o = H.open_items(H.SHEET)
    chk("transcripts not released -> M2..M5 from report figures only",
        o["transcripts_released"] is False
        and o["M2_to_M5_source"] == "report figures only")
    chk("the off-trail fraction is NOT_COLLECTED (report silent), not "
        "unmeasured", o["post_validation_off_trail_fraction"] == H.NOT_COLLECTED)

    # ---- the file holds no value from any report
    chk("the unfilled sheet carries no numeric value anywhere",
        all(not isinstance(v.get("value"), (int, float))
            for k, v in H.SHEET.items() if isinstance(v, dict)
            and "value" in v))

    # ---- CLI, screen
    r0 = subprocess.run([sys.executable, os.path.join(HERE,
                        "hf_incident_extract.py"), "--selftest"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("the instrument refuses --selftest", r0.returncode == 2)
    sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    out_u = H.render()
    out_f = H.render(s)
    chk("the unfilled render carries no screened language",
        not no_severity.hits(out_u))
    chk("the filled render carries no screened language",
        not no_severity.hits(out_f))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out_u + "\nthis design is broken\n")))
    chk("the filled render prints counts and no label words",
        "18.000" in out_f and "0.700" in out_f
        and not any(wd in out_f.lower() for wd in ("deceptive", "sabotage",
                                                     "malicious", "honest")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
