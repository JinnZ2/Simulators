"""Bridge test suite. Run: python3 -m pytest tests/ -q"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from bridge import Investigation

HERE = os.path.dirname(__file__)
CASE = json.load(open(os.path.join(HERE, "..", "cases", "reefer-trucking.case.json")))

def run_inv():
    inv = Investigation(CASE)
    for link in inv.case["links"]:   # iterate the deep copy, never the shared module-level CASE
        inv.run_link(link)
    agg = inv.aggregate()
    dp = inv.decide(agg)
    return inv, agg, dp

def test_links_all_update():
    inv, agg, dp = run_inv()
    assert len(inv.link_results) == 4
    assert all(0 < r["posterior"] < 1 for r in inv.link_results)

def test_strong_links_beat_weak_links():
    inv, agg, dp = run_inv()
    by_id = {r["link_id"]: r for r in inv.link_results}
    assert by_id["L1"]["posterior"] > by_id["L2"]["posterior"]  # logs beat models
    assert by_id["L3"]["posterior"] > by_id["L4"]["posterior"]

def test_chain_below_weakest_link():
    inv, agg, dp = run_inv()
    assert agg["confidence_gradient"] < agg["weakest_link_bound"]

def test_failed_gate_escalates():
    inv, agg, dp = run_inv()
    assert dp.action.value == "escalate"

def test_uncalibrated_proxies_flagged_in_results():
    inv, agg, dp = run_inv()
    # L2's stop audit and L4's reconstruction use method 'none' -> their links lose fidelity
    by_id = {r["link_id"]: r for r in inv.link_results}
    assert by_id["L2"]["cascade_fidelity"] < 0.6

def test_ledger_integrity():
    inv, agg, dp = run_inv()
    assert inv.ledger.verify_chain() and len(inv.ledger.records) >= 20

def test_end_to_end_script():
    r = subprocess.run("python3 src/run_reefer_case.py", shell=True,
                       cwd=os.path.join(HERE, ".."), capture_output=True, text=True)
    assert r.returncode == 0 and "ESCALATE" in r.stdout and "chain valid: True" in r.stdout
