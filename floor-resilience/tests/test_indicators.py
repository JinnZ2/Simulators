import math

import pytest

from floor_resilience import indicators as ind
from floor_resilience import scrap
from floor_resilience.stress import power, software

CFG = ind.load_config()


def _run(make, raw):
    site = make(raw)
    sc = scrap.reclassify(site)
    pw = power.run(site)
    kos = software.all_knockouts(site)
    return {i.id: i for i in ind.assess(site, CFG, sc, pw, kos).indicators}, site


def test_empty_site_scores_nothing_but_never_crashes(make):
    out, _ = _run(make, {})
    assert len(out) == 12
    for i in out.values():
        assert i.score is None and i.confidence == 0 and i.tag
        assert i.explanation.startswith("No data:") and i.plain
    a = ind.assess(make({}), CFG)
    assert a.overall is None and a.weakest == [] and len(a.unscored) == 12


def test_every_scored_indicator_has_confidence_and_tag(example):
    a = ind.assess(example, CFG, scrap.reclassify(example), power.run(example),
                   software.all_knockouts(example))
    for i in a.indicators:
        assert i.tag and 0 <= i.confidence <= 1
        if i.score is not None:
            assert 0 <= i.score <= 4 and i.confidence > 0
    assert "EXAMPLE" in a.indicators[0].tag


def test_band_rules():
    assert ind.band(0.9, {"higher_better": [0.2, 0.4, 0.6, 0.8]}) == 4
    assert ind.band(0.1, {"higher_better": [0.2, 0.4, 0.6, 0.8]}) == 0
    assert ind.band(0, {"lower_better": [0, 1, 3, 5]}) == 4
    assert ind.band(6, {"lower_better": [0, 1, 3, 5]}) == 0


def test_score_without_tag_is_refused():
    with pytest.raises(ValueError):
        ind.Indicator("I1", "x", 1.0, 2, 1.0, "", "e")


def test_i2_i3_i9_i10_i11(make):
    out, _ = _run(make, {
        "safety": [{"origin": "worker_reported"}] * 3 + [{"origin": "incident_driven"}] + [{"origin": "regulation"}],
        "maintenance": [{"year": 2021, "repairs_inhouse": 90, "repairs_outsourced": 10},
                        {"year": 2023, "repairs_inhouse": 50, "repairs_outsourced": 50}],
        "repair_attribution": [{"who_fixed": "a", "who_wrote_up": "b"},
                               {"who_fixed": "a", "who_wrote_up": "a"}, {"who_fixed": "a"}],
        "oversight": [{"year": 2020, "inspectors": 1, "supervisors": 1, "direct_operators": 20},
                      {"year": 2022, "inspectors": 3, "supervisors": 1, "direct_operators": 20}],
        "automation": [{"experienced_operators_involved": True}, {"experienced_operators_involved": False},
                       {"id": "unknown"}],
    })
    assert out["I2"].value == pytest.approx(0.75) and out["I2"].score == 3
    assert out["I3"].value == pytest.approx(-0.2) and out["I3"].score == 0
    assert out["I9"].value == pytest.approx(0.5) and out["I9"].score == 1
    assert out["I10"].value == pytest.approx(0.05) and out["I10"].score == 0
    assert out["I11"].value == pytest.approx(0.5) and out["I11"].confidence == pytest.approx(2 / 3, abs=1e-3)


def test_i4_turnover(make):
    out, _ = _run(make, {"machines": [
        {"id": "a", "expected_service_life_years": 10, "replacements_per_year": 0.1},
        {"id": "b", "expected_service_life_years": 10, "replacements_per_year": 0.3},
        {"id": "c"}]})
    assert out["I4"].value == pytest.approx(2.0) and out["I4"].score == 1
    assert out["I4"].confidence == pytest.approx(2 / 3, abs=1e-3)


def test_workforce_indicators(make):
    ops = ([{"tenure_months": 200, "retiring_within_months": 12, "sole_knower_of": ["die change"]},
            {"tenure_months": 100, "sole_knower_of": ["spindle", "shared"]},
            {"tenure_months": 90, "sole_knower_of": ["shared"]}]
           + [{"tenure_months": 6}] * 4 + [{"name": "nt"}]
           + [{"tenure_months": 300, "left_date": "2024-01-01"}])
    out, _ = _run(make, {"operators": ops})
    # I5: 3 veterans of 7 known, 1 retiring -> 2/7
    assert out["I5"].value == pytest.approx(2 / 7)
    assert out["I5"].confidence == pytest.approx(7 / 8, abs=1e-3)
    # I6: die change and spindle are sole; "shared" has two holders
    assert out["I6"].value == 2 and "die change" in out["I6"].explanation
    # I7: 4 new hires / 3 veterans
    assert out["I7"].value == pytest.approx(4 / 3) and out["I7"].score == 2


def test_i6_not_reported_vs_reported_zero(make):
    none, _ = _run(make, {"operators": [{"tenure_months": 10}]})
    assert none["I6"].score is None
    zero, _ = _run(make, {"operators": [{"tenure_months": 10, "sole_knower_of": []}]})
    assert zero["I6"].value == 0 and zero["I6"].score == 4


def test_i7_no_veterans(make):
    out, _ = _run(make, {"operators": [{"tenure_months": 3}]})
    assert math.isinf(out["I7"].value) and out["I7"].score == 0
    out, _ = _run(make, {"operators": [{"tenure_months": 30}]})
    assert out["I7"].value == 0 and out["I7"].score == 4


@pytest.mark.parametrize("job,screen,score,conf", [
    ("hands_on", "written", 0, 1.0), (None, "written", 0, 0.5),
    ("hands_on", "hands_on_trial", 4, 1.0), ("mixed", "interview", 2, 1.0),
    ("written", "written", 4, 1.0),
])
def test_i8_channel_match(make, job, screen, score, conf):
    h = {"screen_type": screen, "first_year_quit_rate": 0.3}
    if job:
        h["job_channel"] = job
    out, _ = _run(make, {"hiring": h})
    assert out["I8"].score == score and out["I8"].confidence == conf
    assert ("ASSUMED" in out["I8"].explanation) == (job is None)


def test_i1_and_i12_from_modules(make):
    out, _ = _run(make, {
        "scrap": [{"date": "2025-01-01", "machine": "m", "logged_cause_code": "material_jam", "units": 9},
                  {"date": "2025-01-02", "machine": "m", "logged_cause_code": "power_event", "units": 1}],
        "operators": [{"name": "p", "can_run_manual": ["m"]}],
        "machines": [{"id": "m", "manual_mode": "full", "power_draw_kw": 5, "software_layers": ["l"]}],
        "software_layers": [{"id": "l"}],
        "functions": [{"id": "f", "layers": ["l"], "bridge": "paper"}],
    })
    assert out["I1"].value == pytest.approx(0.9) and out["I1"].score == 0
    assert out["I12"].value == pytest.approx(1.0) and out["I12"].score == 4


def test_overall_names_weakest_with_ties(make):
    a = ind.assess(make({
        "hiring": {"screen_type": "written", "job_channel": "hands_on"},
        "safety": [{"origin": "incident_driven"}],
        "automation": [{"experienced_operators_involved": False}],
        "repair_attribution": [{"who_fixed": "a", "who_wrote_up": "b"}],
        "oversight": [{"year": 1, "inspectors": 1, "supervisors": 1, "direct_operators": 10},
                      {"year": 2, "inspectors": 1, "supervisors": 0, "direct_operators": 10}],
    }), CFG)
    assert a.overall == pytest.approx(4 / 5)
    assert [i.id for i in a.weakest] == ["I2", "I8", "I9", "I11"]   # four tie at 0


def test_config_override(tmp_path, make):
    p = tmp_path / "c.yaml"
    p.write_text("weights: {I8: 0}\ncuts: {I2: {higher_better: [0.0, 0.0, 0.0, 0.0]}}\n")
    cfg = ind.load_config(p)
    a = ind.assess(make({"hiring": {"screen_type": "written"},
                         "safety": [{"origin": "incident_driven"}]}), cfg)
    assert a.overall == 4.0 and [i.id for i in a.weakest] == ["I2"]
