import datetime as dt

import pytest

from floor_resilience import scrap

CODES = scrap.load_map()


def _rows(machine, month, codes_units, shift="day"):
    return [{"date": f"2025-{month:02d}-10", "machine": machine, "logged_cause_code": c,
             "units": u, "shift": shift} for c, u in codes_units]


def test_default_map_is_the_observed_mapping():
    assert CODES["calibration_drift"]["catchable"] is True
    assert CODES["belt_drive_failure"]["catchable"] is True
    assert CODES["material_jam"]["catchable"] is True
    assert CODES["sudden_fracture"]["catchable"] is False
    assert CODES["power_event"]["catchable"] is False


def test_units_weighted_share_and_unmapped(make):
    site = make({"scrap": _rows("m1", 1, [("calibration_drift", 30), ("power_event", 10),
                                         ("mystery", 50)])})
    r = scrap.reclassify(site)
    assert r.overall.share == pytest.approx(0.75)
    assert r.overall.unmapped == 50
    assert r.unmapped_codes == {"mystery": 50}
    assert r.missing_catch == {"operator who notices dimension creep": 30}
    # unmapped units lower confidence: 40 of 90 mapped, 3 rows of 50
    assert r.confidence == pytest.approx(round(3 / 50 * 40 / 90, 3))


def test_by_machine_shift_month(make):
    rows = (_rows("m1", 1, [("material_jam", 10)], "day")
            + _rows("m2", 2, [("sudden_fracture", 10)], "night"))
    r = scrap.reclassify(make({"scrap": rows}))
    assert r.by_machine["m1"].share == 1 and r.by_machine["m2"].share == 0
    assert r.by_shift["night"].share == 0
    assert list(r.by_month) == ["2025-01", "2025-02"]


def test_no_rows_and_custom_map(make, tmp_path):
    empty = scrap.reclassify(make({}))
    assert empty.overall.share is None and empty.confidence == 0
    p = tmp_path / "m.yaml"
    p.write_text("codes:\n  mystery: {catchable: true, missing_catch: x}\n")
    site = make({"scrap": _rows("m1", 1, [("mystery", 5)])})
    assert scrap.reclassify(site, scrap.load_map(p)).overall.share == 1


def _departure_site(make, after_code, tenure=120, left="2025-04-01"):
    before = []
    for m in (1, 2, 3):
        before += _rows("lathe", m, [("material_jam", 30), ("sudden_fracture", 30)])
    after = []
    for m in (4, 5, 6):
        after += _rows("lathe", m, [(after_code, 30), ("material_jam", 30)])
    ops = [{"name": "Dale", "tenure_months": tenure, "machines": ["lathe"], "left_date": left}]
    return make({"operators": ops, "scrap": before + after})


def test_flag_when_share_rises_after_veteran_leaves(make):
    r = scrap.reclassify(_departure_site(make, "calibration_drift"))
    assert r.checked_departures == 1
    assert len(r.flags) == 1
    f = r.flags[0]
    assert (f.person, f.machine, f.left_date) == ("Dale", "lathe", dt.date(2025, 4, 1))
    assert f.share_before == pytest.approx(0.5) and f.share_after == pytest.approx(1.0)
    assert f.rise == pytest.approx(0.5)


def test_no_flag_when_share_flat_or_not_a_veteran(make):
    flat = scrap.reclassify(_departure_site(make, "sudden_fracture"))
    assert flat.flags == [] and flat.checked_departures == 1
    junior = scrap.reclassify(_departure_site(make, "calibration_drift", tenure=12))
    assert junior.flags == [] and junior.checked_departures == 0


def test_departure_with_too_little_data_is_not_checked(make):
    site = make({"operators": [{"name": "D", "tenure_months": 200, "machines": ["x"],
                                "left_date": "2025-04-01"}],
                 "scrap": _rows("x", 3, [("material_jam", 5)])})
    r = scrap.reclassify(site)
    assert r.checked_departures == 0 and r.flags == []
