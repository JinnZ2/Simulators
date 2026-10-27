import math

import numpy as np
import pytest

from floor_resilience import drain_sim as ds

# Reference numbers: the published JS model (skill-drain-simulator/index.html),
# run headless in node with its own defaults, 2026-10-23.
JS_A = dict(base=978.3333333333334, scrap60=1446, change=0.4780238500851788,
            vets60=5, insp60=4, outs60=5.175, ind=10, alarm=24)
JS_B = dict(base=921.3333333333334, scrap60=990, change=0.0745296671490594,
            vets60=10.4, insp60=3, ind=11, alarm=None)
# JS at 2000 runs, three seed bases: months 49-60 mean scrap change and veterans.
JS_LATE = {"A": (0.4806, 5.232), "B": (0.0919, 10.187)}


def test_mulberry32_matches_js_first_draws():
    # first three values of the JS rng(1000), computed in node
    r = ds.Mulberry32(1000)
    got = [r.random() for _ in range(3)]
    assert got == pytest.approx([0.7951949068810791, 0.8276879135519266, 0.6915161057841033], abs=1e-15)


@pytest.mark.parametrize("params,ref", [(ds.plant_a(), JS_A), (ds.plant_b(), JS_B)])
def test_js_replay_reproduces_published_numbers_exactly(params, ref):
    r = ds.simulate(params, seed=1000, rng="js")
    assert r.base == pytest.approx(ref["base"], abs=1e-9)
    assert r.scrap[-1] == pytest.approx(ref["scrap60"], abs=1e-9)
    assert r.scrap_change == pytest.approx(ref["change"], abs=1e-12)
    assert r.vets[-1] == pytest.approx(ref["vets60"], abs=1e-9)
    assert r.inspectors[-1] == ref["insp60"]
    assert r.indicator_month == ref["ind"]
    assert r.alarm_month == ref["alarm"]


def test_acceptance_targets_section5():
    """Work order: A ~ +48 %, B ~ +7 %, lead ~ 14 months (+-20 %).

    Met exactly by the published draw (rng='js', seed 1000). The numpy port is
    checked against the converged model instead (next test), because at 40
    runs the JS model's own seed spread is A sd 6 pp, B sd 4 pp, lead sd 6 mo.
    """
    a = ds.simulate(ds.plant_a(), rng="js")
    b = ds.simulate(ds.plant_b(), rng="js")
    assert a.scrap_change == pytest.approx(0.48, rel=0.2)
    assert b.scrap_change == pytest.approx(0.07, rel=0.2)
    assert a.lead_time == pytest.approx(14, rel=0.2)


@pytest.mark.parametrize("name,params", [("A", ds.plant_a(runs=2000)), ("B", ds.plant_b(runs=2000))])
def test_numpy_port_matches_converged_js(name, params):
    r = ds.simulate(params, seed=1, rng="numpy")
    late = r.scrap[48:].mean() / r.base - 1
    js_change, js_vets = JS_LATE[name]
    assert late == pytest.approx(js_change, abs=0.02)
    assert r.vets[48:].mean() == pytest.approx(js_vets, abs=0.15)


def test_seeded_and_reproducible():
    a1 = ds.simulate(ds.plant_a(runs=5), seed=3)
    a2 = ds.simulate(ds.plant_a(runs=5), seed=3)
    a3 = ds.simulate(ds.plant_a(runs=5), seed=4)
    assert np.array_equal(a1.scrap, a2.scrap)
    assert not np.array_equal(a1.scrap, a3.scrap)


def test_reserve_and_hands_on_lower_scrap():
    a = ds.simulate(ds.plant_a(runs=300), seed=2)
    b = ds.simulate(ds.plant_b(runs=300), seed=2)
    assert b.scrap[-12:].mean() < a.scrap[-12:].mean()
    assert b.vets[-1] > a.vets[-1]


def test_no_drift_no_failure_gives_zero_scrap_and_no_alarm():
    r = ds.simulate(ds.Params(runs=3, drift_rate=0.0, fail_rate=0.0), seed=1)
    assert r.scrap.sum() == 0
    assert r.alarm_month is None and r.lead_time is None
    assert math.isnan(r.scrap_change)


def test_summary_and_bad_inputs():
    s = ds.simulate(ds.plant_a(runs=3)).summary()
    assert set(s) >= {"scrap_change", "lead_time_months", "catchable_share_month_end"}
    with pytest.raises(ValueError):
        ds.simulate(ds.Params(screen="essay"))
    with pytest.raises(ValueError):
        ds.simulate(ds.Params(runs=1), rng="dice")


def test_start_from_site(make):
    site = make({"name": "s", "hiring": {"screen_type": "working_shift"},
                 "operators": [{"tenure_months": 240, "retiring_within_months": 6},
                               {"tenure_months": 200, "reserve": True},
                               {"tenure_months": 3}, {"tenure_months": 1},
                               {"name": "gone", "tenure_months": 300, "left_date": "2024-01-01"}]})
    floor, p, notes = ds.floor_from_site(site, ds.Params())
    assert p.n_operators == 4 and p.screen == "hands_on" and p.reserve == 1
    assert floor.retire[0] == 6 and math.isinf(floor.retire[1])
    assert floor.skill[0] > 0.7 and floor.skill[3] < 0.1
    r = ds.simulate(ds.Params(runs=5), site=site)
    assert r.source == "site: s" and len(r.scrap) == 60


def test_site_without_tenure_or_screen_notes(make):
    site = make({"operators": [{"name": "x"}, {"tenure_months": 100}]})
    _, p, notes = ds.floor_from_site(site, ds.Params())
    assert any("no tenure" in n for n in notes)
    assert any("screen unknown" in n for n in notes)
    with pytest.raises(ValueError):
        ds.floor_from_site(make({}), ds.Params())


def test_js_mode_accepts_site_floor(make):
    site = make({"operators": [{"tenure_months": 100}] * 4 + [{"tenure_months": 2}] * 4})
    r = ds.simulate(ds.Params(runs=2, months=12), rng="js", site=site)
    assert len(r.scrap) == 12
