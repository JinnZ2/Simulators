import datetime as dt

import pytest

from floor_resilience import eld, reserve
from floor_resilience.schema import ReserveInputs, build_site, load_site


def test_missing_everything_never_crashes(tmp_path):
    for raw in (None, [], "text", {}):
        site, gaps = build_site(raw)
        assert site.operators == []
    p = tmp_path / "empty.yaml"
    p.write_text("")
    site, gaps = load_site(p)
    assert gaps and site.machines == []
    site, gaps = load_site(tmp_path / "nope.yaml")
    assert "could not read" in gaps[0]
    bad = tmp_path / "bad.yaml"
    bad.write_text("a: [unclosed")
    assert "could not read" in load_site(bad)[1][0]


def test_bad_rows_dropped_and_reported():
    site, gaps = build_site({
        "scrap": [{"date": "2025-01-01", "units": 5}, {"date": "not a date"}, {"units": 3}],
        "machines": "should be a list",
        "hiring": {"screen_type": "essay"},
        "name": ["not", "a", "string"],
    })
    assert len(site.scrap) == 1
    assert any("scrap[1]" in g for g in gaps) and any("scrap[2]" in g for g in gaps)
    assert any("machines: expected a list" in g for g in gaps)
    assert any("hiring: dropped" in g for g in gaps)
    assert any("name/example ignored" in g for g in gaps)


def test_unknown_fields_reported_and_nested_spelling_accepted():
    site, gaps = build_site({
        "workforce": {"operators": [{"name": "a", "tenur_months": 3}]},
        "safety": {"rules": [{"origin": "regulation"}]},
        "automation": {"projects": [{"experienced_operators_involved": True}]},
        "fleet": {"drivers": [{"id": "t1"}]},
        "power_budget": {"minimal_kw": 5, "volts": 240},
        "weather": "sunny",
    })
    assert site.operators[0].name == "a" and len(site.safety) == 1
    assert len(site.automation) == 1 and len(site.drivers) == 1
    assert any("tenur_months" in g for g in gaps)
    assert any("volts" in g for g in gaps)
    assert any("weather" in g for g in gaps)


def test_reserve_cost_full_and_partial():
    full = reserve.cost(ReserveInputs(size=3, wage_cost_per_operator_year=60000,
                                      reserve_output_value_per_year=100000, outage_days=10,
                                      daily_output_value=50000, outage_probability_per_year=0.2,
                                      share_of_outage_avoided=0.5))
    assert full.wage_cost == 180000 and full.premium == 80000
    assert full.expected_avoided_loss == pytest.approx(50000)
    assert full.ratio == pytest.approx(0.625) and full.assumed == [] and full.missing == []
    part = reserve.cost(ReserveInputs(outage_days=5))
    assert part.premium is None and part.expected_avoided_loss is None and part.ratio is None
    assert "size" in part.missing and "daily_output_value" in part.missing
    assert part.assumed  # share avoided defaulted
    free = reserve.cost(ReserveInputs(size=1, wage_cost_per_operator_year=10,
                                      reserve_output_value_per_year=50, outage_days=1,
                                      daily_output_value=1, outage_probability_per_year=1))
    assert free.premium < 0 and free.ratio is None
    assert "PROPOSED" in reserve.POLICY_NOTE


def test_eld_readiness(make):
    site = make({"drivers": [
        {"id": "old", "start_year": 2010, "has_kept_paper_logs_in_cab": True},
        {"id": "new-drill", "start_year": 2020, "has_kept_paper_logs_in_cab": False,
         "completed_week_long_paper_drill": True},
        {"id": "new-none", "start_year": 2021, "has_kept_paper_logs_in_cab": False,
         "completed_week_long_paper_drill": False},
        {"id": "unknown", "start_year": 2017},
        {"start_year": None},
    ]})
    r = eld.run(site)
    assert (r.drivers, r.able, r.not_able, r.unknown) == (5, 2, 1, 2)
    assert r.able_share == pytest.approx(2 / 3) and r.confidence == pytest.approx(3 / 5)
    assert r.flagged == ["new-none"]          # 2017 starts before the compliance date
    assert r.no_start_year == 1
    assert eld.run(make({})).able_share is None


def test_eld_rules_are_marked_unverified():
    rules = eld.load_rules()
    assert rules["status"] == "NOT_VERIFIED_AGAINST_PRIMARY_TEXT"
    assert rules["mandate"]["compliance_date"] == dt.date(2017, 12, 18)
    assert {r["id"] for r in rules["rules"]} >= {"reconstruct", "carrier_repair"}
