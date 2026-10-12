#!/usr/bin/env python3
"""system_efficiency.py - floor-anchored efficiency with theater gap. CC0. stdlib only.

E_real = (after - before) / (sum(hop costs) + sum(join costs))
completion = (after - before) / (target - before)          if target given
reported   = fraction of hops that self-report success
THEATER_GAP = reported - completion  (1.0 = all green, nothing moved)
join_share  = sum(join costs) / total cost

No change in state -> E_real = 0, whatever the activity. Joins are summed, not skipped.
All costs must share one unit or the run refuses.

Input JSON:
{
  "floor":  {"name": "pallets inside building", "unit": "pallets",
             "before": 0, "after": 0, "target": 22},
  "cost_unit": "minutes",
  "hops":  [{"name": "...", "cost": 3, "unit": "minutes", "reported_success": true}],
  "joins": [{"between": "A->B", "cost": 15, "unit": "minutes"}],
  "deadline": {"name": "reefer fuel", "cost": 600, "unit": "minutes"}      # optional
}

Usage:
  system_efficiency.py run case.json
  system_efficiency.py template > case.json
  system_efficiency.py example
  system_efficiency.py selftest
"""
import argparse, json, sys

class UnitError(ValueError):
    pass

def _check_units(case):
    cu = case.get("cost_unit")
    if not cu:
        raise UnitError("cost_unit missing")
    items = case.get("hops", []) + case.get("joins", [])
    if case.get("deadline"):
        items = items + [case["deadline"]]
    for it in items:
        u = it.get("unit", cu)
        if u != cu:
            raise UnitError(f"'{it.get('name', it.get('between', '?'))}' in {u}, "
                            f"chain declared {cu}: cannot sum")

def analyze(case):
    _check_units(case)
    fl = case["floor"]
    delta = fl["after"] - fl["before"]
    hop_cost = sum(h["cost"] for h in case.get("hops", []))
    join_cost = sum(j["cost"] for j in case.get("joins", []))
    total = hop_cost + join_cost
    e_real = (delta / total) if total > 0 else (0.0 if delta == 0 else float("inf"))

    completion = None
    if fl.get("target") is not None and fl["target"] != fl["before"]:
        completion = delta / (fl["target"] - fl["before"])

    hops = case.get("hops", [])
    reported = (sum(1 for h in hops if h.get("reported_success")) / len(hops)) if hops else None

    gap = None
    if reported is not None and completion is not None:
        gap = reported - max(0.0, min(1.0, completion))

    if delta == 0:
        verdict = "ZERO_NUMERATOR: activity without change in state"
    elif delta < 0:
        verdict = "NEGATIVE: the floor is worse than before"
    elif completion is not None and completion < 1:
        verdict = "PARTIAL: some change, target not reached"
    else:
        verdict = "DELIVERED"
    theater = gap is not None and reported >= 0.8 and gap >= 0.6

    margin = None
    if case.get("deadline"):
        margin = case["deadline"]["cost"] - total

    return {
        "delta_state": delta, "floor_unit": fl.get("unit", ""),
        "hop_cost": hop_cost, "join_cost": join_cost, "total_cost": total,
        "cost_unit": case["cost_unit"],
        "e_real": e_real, "completion": completion,
        "reported_success_rate": reported, "theater_gap": gap,
        "join_share": (join_cost / total) if total else 0.0,
        "verdict": verdict, "theater_flag": theater,
        "deadline_margin": margin,
        "deadline_name": case.get("deadline", {}).get("name"),
    }

def report(case, r):
    cu, fu = r["cost_unit"], r["floor_unit"]
    L = [f"FLOOR: {case['floor']['name']}  before={case['floor']['before']} "
         f"after={case['floor']['after']} target={case['floor'].get('target')} ({fu})",
         f"CHANGE IN STATE: {r['delta_state']} {fu}",
         f"COST: hops={r['hop_cost']} + joins={r['join_cost']} = {r['total_cost']} {cu}"
         f"   (joins are {r['join_share']:.0%} of cost)",
         f"REAL EFFICIENCY: {r['e_real']:.4g} {fu} per {cu}"]
    if r["completion"] is not None:
        L.append(f"COMPLETION: {r['completion']:.0%}")
    if r["reported_success_rate"] is not None:
        L.append(f"SELF-REPORTED SUCCESS: {r['reported_success_rate']:.0%} of hops")
    if r["theater_gap"] is not None:
        L.append(f"THEATER GAP: {r['theater_gap']:.2f}  (reported success minus real completion)")
    if r["deadline_margin"] is not None:
        state = "REMAINING" if r["deadline_margin"] >= 0 else "OVERRUN"
        L.append(f"FLOOR CLOCK ({r['deadline_name']}): {abs(r['deadline_margin'])} {cu} {state}")
    L.append(f"=> {r['verdict']}" + ("  [THEATER: chain reports success, floor did not move]"
                                     if r["theater_flag"] else ""))
    return "\n".join(L)

TEMPLATE = {
    "floor": {"name": "work actually done", "unit": "units", "before": 0, "after": 0, "target": 1},
    "cost_unit": "minutes",
    "hops": [{"name": "hop 1", "cost": 0, "unit": "minutes", "reported_success": True}],
    "joins": [{"between": "hop 1->hop 2", "cost": 0, "unit": "minutes"}],
    "deadline": {"name": "physical clock", "cost": 0, "unit": "minutes"},
}

# ILLUSTRATIVE numbers. Shape of a dock-delivery case, not a measurement.
EXAMPLE = {
    "floor": {"name": "pallets inside building", "unit": "pallets",
              "before": 0, "after": 0, "target": 22},
    "cost_unit": "minutes",
    "hops": [
        {"name": "store phone AI call 1", "cost": 3, "unit": "minutes", "reported_success": True},
        {"name": "store phone AI call 2", "cost": 3, "unit": "minutes", "reported_success": True},
        {"name": "store phone AI call 3", "cost": 3, "unit": "minutes", "reported_success": True},
        {"name": "store phone AI call 4", "cost": 3, "unit": "minutes", "reported_success": True},
        {"name": "store phone AI call 5", "cost": 3, "unit": "minutes", "reported_success": True},
        {"name": "dock door buzzer", "cost": 5, "unit": "minutes", "reported_success": False},
        {"name": "dispatch call", "cost": 4, "unit": "minutes", "reported_success": True},
        {"name": "dispatch-side AI", "cost": 2, "unit": "minutes", "reported_success": True},
        {"name": "central routing", "cost": 2, "unit": "minutes", "reported_success": True},
    ],
    "joins": [
        {"between": "back-office ring-outs", "cost": 15, "unit": "minutes"},
        {"between": "dispatch -> AI -> central routing", "cost": 45, "unit": "minutes"},
        {"between": "central routing -> human at dock", "cost": 60, "unit": "minutes"},
    ],
    "deadline": {"name": "reefer fuel before cold chain at risk", "cost": 480, "unit": "minutes"},
}

def selftest():
    r = analyze(EXAMPLE)
    assert r["delta_state"] == 0 and r["e_real"] == 0.0
    assert r["verdict"].startswith("ZERO_NUMERATOR")
    assert r["theater_flag"] is True and r["theater_gap"] > 0.8
    assert r["join_share"] > 0.7
    good = json.loads(json.dumps(EXAMPLE))
    good["floor"]["after"] = 22
    g = analyze(good)
    assert g["verdict"] == "DELIVERED" and g["theater_flag"] is False and g["e_real"] > 0
    neg = json.loads(json.dumps(EXAMPLE))
    neg["floor"]["after"] = -3
    assert analyze(neg)["verdict"].startswith("NEGATIVE")
    bad = json.loads(json.dumps(EXAMPLE))
    bad["joins"][0]["unit"] = "dollars"
    try:
        analyze(bad)
        raise AssertionError("mixed units accepted")
    except UnitError:
        pass
    assert "THEATER" in report(EXAMPLE, r)
    print("SELFTEST OK")

def main(argv=None):
    p = argparse.ArgumentParser(description="floor-anchored efficiency with theater gap")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("run").add_argument("path")
    for name in ("template", "example", "selftest"):
        sp.add_parser(name)
    a = p.parse_args(argv)
    if a.cmd == "selftest":
        return selftest()
    if a.cmd == "template":
        print(json.dumps(TEMPLATE, indent=2)); return
    case = EXAMPLE if a.cmd == "example" else json.load(open(a.path))
    try:
        print(report(case, analyze(case)))
    except UnitError as e:
        sys.exit(f"UNIT REFUSAL: {e}")

if __name__ == "__main__":
    main()
