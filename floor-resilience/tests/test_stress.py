import pytest

from floor_resilience.stress import power, software, vendor


def _m(i, **kw):
    return {"id": i, **kw}


def test_power_cells_statuses_and_people(make):
    site = make({
        "operators": [{"name": "Gene", "can_run_manual": ["press"]},
                      {"name": "Gone", "can_run_manual": ["mill"], "left_date": "2024-01-01"}],
        "machines": [
            _m("press", manual_mode="partial", power_draw_kw=10),
            _m("mill", manual_mode="full", power_draw_kw=20),
            _m("cnc", manual_mode="none", power_draw_kw=30,
               power={"intermittent": {"runs": False, "rehome_after_dropout": True,
                                       "last_tested": "never"}}),
            _m("hand", power_draw_kw=0),
            _m("blank"),
        ]})
    r = power.run(site)
    cell = {(c.machine, c.state): c for c in r.cells}
    assert cell["press", "none"].status == "MANUAL" and cell["press", "none"].who_can_run == ["Gene"]
    assert cell["mill", "none"].status == "MANUAL_NO_ONE"      # the only person left
    assert cell["cnc", "none"].status == "STOPS"
    assert cell["cnc", "intermittent"].rehome_after_dropout is True
    assert cell["cnc", "intermittent"].last_tested == "never"
    assert cell["press", "intermittent"].last_tested == "not recorded"
    assert cell["hand", "none"].status == "RUNS"
    assert cell["blank", "none"].status == "UNKNOWN"
    assert r.never_tested == 1
    assert 0 < r.confidence < 1
    assert r.ready_share == pytest.approx(
        sum(c.status in power.READY for c in r.cells if c.status != "UNKNOWN")
        / sum(c.status != "UNKNOWN" for c in r.cells))


def test_load_shed_greedy_by_priority():
    from floor_resilience.schema import Machine
    ms = [Machine(id="a", priority=2, power_draw_kw=30), Machine(id="b", priority=1, power_draw_kw=25),
          Machine(id="c", priority=3, power_draw_kw=10), Machine(id="d", power_draw_kw=5),
          Machine(id="e", priority=1)]
    plan = power.load_shed(ms, 40)
    assert plan.keep == ["b", "c", "d"] and plan.shed == ["a"] and plan.unknown_draw == ["e"]
    assert plan.used_kw == 40
    assert power.load_shed(ms, None).keep == []


def test_minimal_state_uses_the_plan(make):
    site = make({"power_budget": {"minimal_kw": 15},
                 "machines": [_m("keep", priority=1, power_draw_kw=10, manual_mode="none"),
                              _m("shed", priority=2, power_draw_kw=10, manual_mode="none")]})
    cell = {(c.machine, c.state): c for c in power.run(site).cells}
    assert cell["keep", "minimal"].status == "RUNS"
    assert cell["shed", "minimal"].status == "STOPS"


def test_empty_site_power(make):
    r = power.run(make({}))
    assert r.cells == [] and r.ready_share is None and r.confidence == 0


GRAPH = {
    "software_layers": [
        {"id": "php", "kind": "php_portal", "version": "8.1.31"},
        {"id": "mes", "depends_on": ["php"]},
        {"id": "sched", "depends_on": ["mes"]},
        {"id": "hmi"},
    ],
    "machines": [_m("press", software_layers=["sched"], manual_mode="none"),
                 _m("lathe", software_layers=["hmi"], manual_mode="partial"),
                 _m("saw", software_layers=["php"], manual_mode="full"),
                 _m("odd", software_layers=["ghost"])],
    "functions": [{"id": "tickets", "layers": ["php"], "bridge": "paper tickets"},
                  {"id": "pressing", "machines": ["press"]},
                  {"id": "turning", "machines": ["lathe"]},
                  {"id": "cutting", "machines": ["saw"]}],
}


def test_downstream_is_transitive(make):
    site = make(GRAPH)
    assert software.downstream(site, "php") == ["mes", "php", "sched"]
    assert software.downstream(site, "hmi") == ["hmi"]


def test_knockout_hidden_chain_and_bridges(make):
    ko = software.knockout(make(GRAPH), "php")
    m = {x.machine: x for x in ko.machines}
    assert m["press"].status == "STOPS" and m["press"].hidden_chain
    assert m["saw"].status == "BRIDGED_LOCAL" and not m["saw"].hidden_chain
    assert m["lathe"].status == "OK"
    f = {x.function: x for x in ko.functions}
    assert f["tickets"].status == "BRIDGED" and f["tickets"].bridge == "paper tickets"
    assert f["pressing"].status == "STOPS"
    assert f["cutting"].status == "DEGRADED"
    assert ko.hidden_chains == ["press"]
    assert ko.unknown_layers == ["ghost"]


def test_knockout_degraded_and_bridge_share(make):
    site = make(GRAPH)
    ko = software.knockout(site, "hmi")
    f = {x.function: x for x in ko.functions}
    assert f["turning"].status == "DEGRADED"
    kos = software.all_knockouts(site)
    assert len(kos) == 4
    # hits: tickets (bridged) under php; pressing (stops) under php, mes, sched
    assert software.bridge_share(kos) == pytest.approx(1 / 4)
    assert software.bridge_share([]) is None


@pytest.mark.parametrize("version,needle", [
    ("8.1.31", "no patch from the PHP project"),
    ("7.4.33", "no patch from the PHP project"),
    ("8.3.10", "upgrade to 8.3.36"),
    ("8.4.27", "at or above the fixed release"),
    ("8.5.20", "at or above"),
    ("9.0.0", "not in the fixed list"),
    (None, "not recorded"),
    ("eight", "not readable"),
])
def test_php_patch_status(version, needle):
    facts = software.load_php2shell()
    assert needle in software.php_patch_status(version, facts)


def test_php2shell_facts_and_scenario(make):
    facts = software.load_php2shell()
    assert facts["cves"] == ["CVE-2026-109618", "CVE-2026-109619"]
    assert facts["fixed_versions"] == {"8.2": "8.2.35", "8.3": "8.3.36", "8.4": "8.4.27", "8.5": "8.5.12"}
    assert facts["verification"] == "search_result_text"
    sc = software.php2shell_scenario(make(GRAPH))
    assert [c[0] for c in sc.cases] == ["php"]
    assert "no patch" in sc.cases[0][1]
    assert sc.cases[0][2].hidden_chains == ["press"]
    assert software.php2shell_scenario(make({})).cases == []


def test_vendor_flag_over_threshold(make):
    site = make({"machines": [
        _m("a", vendor="X", license_check=True, manual_mode="none", output_share=0.4, repair_knowledge="vendor"),
        _m("b", vendor="X", license_check=True, manual_mode="full", output_share=0.1, repair_knowledge="inhouse"),
        _m("c", vendor="Y", license_check=True, output_share=0.25),
        _m("d", output_share=0.25),
    ]})
    r = vendor.run(site)
    rows = {x.vendor: x for x in r.rows}
    assert rows["X"].line_share == pytest.approx(0.5)
    assert rows["X"].stops_share == pytest.approx(0.4)      # b has full manual mode
    assert rows["X"].flagged and not rows["Y"].flagged       # 0.25 not over 0.30
    assert rows["X"].vendor_held_repair == 1 and rows["X"].inhouse_repair == 1
    assert rows["(vendor not recorded)"].unknown_repair == 1
    assert r.flagged == ["X"] and not r.shares_assumed
    assert vendor.run(site, threshold=0.2).flagged == ["X", "Y"]


def test_vendor_shares_assumed(make):
    r = vendor.run(make({"machines": [_m("a", vendor="X"), _m("b", vendor="Y")]}))
    assert r.shares_assumed and all(x.share_assumed for x in r.rows)
    assert [x.line_share for x in r.rows] == [0.5, 0.5]
    part = vendor.run(make({"machines": [_m("a", vendor="X", output_share=0.7), _m("b", vendor="Y")]}))
    rows = {x.vendor: x for x in part.rows}
    assert rows["Y"].line_share == pytest.approx(0.3) and rows["Y"].share_assumed
    assert not rows["X"].share_assumed
    assert vendor.run(make({})).rows == []
