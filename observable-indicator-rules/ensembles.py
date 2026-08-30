#!/usr/bin/env python3
# ensembles.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# SYNTHETIC router outputs, constructed to exercise the pipeline. The
# router (2D unsteady solve) is the non-phone term the spec names and is
# not run here; these are the fields it WOULD emit, authored by hand so
# ground truth (which orderings are stable, where the false alarms are)
# is known.
#
# NOTHING HERE IS A REAL PLACE. Landmark ids are generic feature types,
# depths are integers on an arbitrary scale, timesteps are indices. No
# coordinate, no community, no drainage is real, and no number below is
# a measurement.
#
# Each builder returns (landmarks, field, runs, household, movement_time)
# where field[run][landmark_id] = a depth time series (depth per step).

from pipeline import Landmark, INF   # noqa: F401


def _series(wet_at, n=12, rise=5.0):
    """A depth series that is 0 until `wet_at`, then rises past any
    reasonable threshold. wet_at=None means never wets."""
    if wet_at is None:
        return [0.0] * n
    return [0.0 if t < wet_at else rise for t in range(n)]


# All landmarks use visible_when = 1.0, so a series that reaches `rise`
# (5.0) at step w has t_wet = w. This keeps t_wet == wet_at, so the
# constructed ordering is transparent.
def _lm(lid, is_route=False):
    return Landmark(lid, visible_when=1.0, is_route=is_route)


def stable():
    """Ordering invariant, MAGNITUDE wildly varying. The spec's central
    bet: the sequence survives where the numbers do not. bridge always
    wets before bend always wets before the house, in every run, but the
    absolute times and gaps differ 5x across runs."""
    bridge = _lm("county_rd_bridge")
    bend = _lm("river_bend", is_route=True)   # on the route out
    house = _lm("household")
    lms = [bridge, bend, house]
    # (bridge, bend, house) wetting steps per run -- order fixed, gaps vary
    runs_spec = {
        "r1": (1, 2, 3),
        "r2": (1, 4, 9),
        "r3": (2, 3, 4),
        "r4": (1, 6, 11),
        "r5": (2, 5, 8),
    }
    field = {}
    for r, (b, e, h) in runs_spec.items():
        field[r] = {"county_rd_bridge": _series(b),
                    "river_bend": _series(e),
                    "household": _series(h)}
    return lms, field, list(runs_spec), house, 1


def flipping():
    """Every pair's order flips across the ensemble. Step 3 must return
    NOTHING -- the spec's falsifiable condition. Observable indicators
    are not derivable for this field, and empty output is the honest
    result."""
    a = _lm("landmark_a")
    b = _lm("landmark_b", is_route=True)
    h = _lm("household")
    lms = [a, b, h]
    runs_spec = {
        "r1": (1, 2, 3),    # a<b<h
        "r2": (3, 2, 1),    # h<b<a  -- every pair reversed
        "r3": (2, 1, 3),    # b<a<h  -- a,b flipped again
    }
    field = {}
    for r, (av, bv, hv) in runs_spec.items():
        field[r] = {"landmark_a": _series(av), "landmark_b": _series(bv),
                    "household": _series(hv)}
    return lms, field, list(runs_spec), h, 1


def false_alarm_heavy():
    """The finding. A trigger whose ORDER relative to the household is
    perfectly stable (trigger always wets before the house WHEN the
    house wets), so step 3 keeps it -- but which ALSO wets in many runs
    where the house never floods. Step 3 is blind to those false alarms
    (a dry house reads as trigger-before-house, the same sign as a true
    positive), so the pipeline keeps the trigger and the spec's card
    would carry a clean lead band with no hint that the trigger cries
    wolf half the time."""
    trigger = _lm("upstream_culvert")
    bend = _lm("river_bend", is_route=True)
    house = _lm("household")
    lms = [trigger, bend, house]
    # runs where the house floods: trigger before house before/around bend
    tp_runs = {
        "tp1": (1, 2, 3),
        "tp2": (1, 3, 4),
        "tp3": (2, 3, 5),
        "tp4": (1, 2, 4),
    }
    # runs where the house does NOT flood but the trigger DOES (false
    # alarms). The bend may or may not wet; the house never does.
    fa_runs = {
        "fa1": (1, None, None),
        "fa2": (2, 5, None),
        "fa3": (1, None, None),
        "fa4": (2, 4, None),
    }
    field = {}
    for r, (tv, ev, hv) in dict(tp_runs, **fa_runs).items():
        field[r] = {"upstream_culvert": _series(tv),
                    "river_bend": _series(ev),
                    "household": _series(hv)}
    runs = list(tp_runs) + list(fa_runs)
    return lms, field, runs, house, 1
