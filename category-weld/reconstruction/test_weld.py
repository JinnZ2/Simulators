#!/usr/bin/env python3
"""test_weld.py -- synthetic fixtures for the arithmetic in weld.py.

RECONSTRUCTED alongside weld.py. CLAIM_TABLE.md states that max_spread and
bias "are implemented and verified against synthetic fixtures in
test_weld.py"; neither file arrived in the drop, so what is verified below
is the RECONSTRUCTED arithmetic, not the delivered arithmetic. See
AUDIT_NOTES.md CW_001.

Every fixture is a hand-computed number, so a change to weld.py that moves
a readout turns a test red rather than silently moving a claim.

    python3 test_weld.py

stdlib only. CC0.
"""

import sys

import weld

FAILS = []


def eq(got, want, label, tol=1e-12):
    ok = (got is None and want is None) or (
        got is not None and want is not None and abs(got - want) <= tol
    )
    print("  %-52s %s" % (label, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
    if not ok:
        FAILS.append(label)


def is_(got, want, label):
    ok = got == want
    print("  %-52s %s" % (label, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
    if not ok:
        FAILS.append(label)


def term(tracked, comps, cases):
    return {
        "term": "fixture",
        "tracked_by_label": tracked,
        "components": [{"id": c, "name": c, "unit": ""} for c in comps],
        "divergences": cases,
    }


def case(cid, readings):
    return {
        "id": cid,
        "note": "",
        "readings": {
            k: {"before": b, "after": a} for k, (b, a) in readings.items()
        },
    }


print("relative_change")
eq(weld.relative_change(100, 50), -0.5, "halving is -0.5")
eq(weld.relative_change(100, 150), 0.5, "half again is +0.5")
eq(weld.relative_change(100, 100), 0.0, "unmoved is 0.0")
eq(weld.relative_change(-100, -50), 0.5, "denominator is abs(before)")
eq(weld.relative_change(0, 5), None, "before == 0 is undefined, not inf")
eq(weld.relative_change(None, 5), None, "missing before is undefined")
eq(weld.relative_change(5, None), None, "missing after is undefined")

print()
print("case_spread")
s, why = weld.case_spread(case("c", {"a": (100, 50), "b": (100, 90)}))
eq(s, 5.0, "0.5 against 0.1 is a spread of 5")
s, why = weld.case_spread(case("c", {"a": (100, 50), "b": (100, 150)}))
eq(s, 1.0, "equal magnitudes opposite directions spread 1")
s, why = weld.case_spread(case("c", {"a": (100, 50)}))
eq(s, None, "one component is not a spread")
is_(why, "fewer than two quantified components", "  and says why")
s, why = weld.case_spread(case("c", {"a": (100, 50), "b": (100, 100)}))
eq(s, None, "an exactly unmoved component gives no ratio")
is_(why, "a quantified component is exactly unmoved", "  and says why")

print()
print("the limit case the mechanism is built around")
print("  label unmoved, hidden component collapsed -- see AUDIT_NOTES CW_004")
for after in (100.0, 99.0, 99.9, 99.99):
    s, _ = weld.case_spread(case("c", {"label": (100.0, after), "hidden": (100, 50)}))
    print("    label %6.2f -> spread %s" % (after, weld.fmt(s, "%.1f")))

print()
print("bias")
t = term("label", ["label", "hidden"], [
    case("c1", {"label": (100, 100), "hidden": (100, 50)}),
    case("c2", {"label": (100, 100), "hidden": (100, 60)}),
])
eq(weld.score(t)["bias"], 1.0, "two divergences the same way is bias 1")
t = term("label", ["label", "hidden"], [
    case("c1", {"label": (100, 100), "hidden": (100, 50)}),
    case("c2", {"label": (100, 100), "hidden": (100, 150)}),
])
eq(weld.score(t)["bias"], 0.0, "two divergences opposite ways is bias 0")
t = term("label", ["label", "h1", "h2"], [
    case("c1", {"label": (100, 100), "h1": (100, 50), "h2": (100, 150)}),
    case("c2", {"label": (100, 100), "h1": (100, 50), "h2": (100, 40)}),
])
eq(weld.score(t)["bias"], 0.5, "three down one up is bias 0.5")
t = term("label", ["label", "hidden"], [
    case("c1", {"label": (100, 100), "hidden": (100, 50)}),
])
s = weld.score(t)
eq(s["bias"], None, "one observation is withheld, not 1.0")
is_(s["bias_n_obs"], 1, "  and the count is reported")
t = term("label", ["label", "hidden"], [
    case("c1", {"label": (100, 50), "hidden": (100, 50)}),
    case("c2", {"label": (100, 100), "hidden": (100, 50)}),
])
s = weld.score(t)
is_(s["bias_n_obs"], 1, "an exact tie is dropped, not counted as agreement")
eq(s["bias"], None, "  so two cases leave one observation, below the guard")

print()
print("reference substitution")
t = term("label", ["label", "h1", "h2"], [
    case("c1", {"h1": (100, 50), "h2": (100, 90)}),
])
obs = weld.case_directions(t, t["divergences"][0])
is_(len(obs), 1, "tracked component absent, first quantified stands in")
is_(obs[0][1], "reference substituted", "  and the observation is flagged")

print()
print("score on an empty term")
s = weld.score(term("label", ["label"], []))
is_(s["n_cases"], 0, "no cases is n_cases 0")
eq(s["max_spread"], None, "  max_spread undefined")
eq(s["bias"], None, "  bias undefined")

print()
print("score on the delivered terms")
# NOTE: an earlier version asserted n_cases == 4 for every term. That was a
# property of the two seed terms at the time, not of the arithmetic, and the
# third term (hierarchy, 5 cases) broke it. The fixture now checks what it
# was actually for: every delivered term is named and none is quantified.
for t in weld.load_all():
    s = weld.score(t)
    named = len([d for d in t.get("divergences", []) if (d.get("id") or "").strip()])
    is_(s["n_cases"], named, "%s: n_cases matches its named divergences (%d)" % (
        s["term"], named))
    ok_ = s["n_cases"] > 0
    is_(ok_, True, "  %s has at least one named case" % s["term"])
    eq(s["max_spread"], None, "  %s max_spread unquantified" % s["term"])
    eq(s["bias"], None, "  %s bias unquantified" % s["term"])

print()
if FAILS:
    print("%d FAILURE(S)" % len(FAILS))
    for f in FAILS:
        print("  " + f)
    sys.exit(1)
print("all fixtures pass")
