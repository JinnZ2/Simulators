# SPDX-License-Identifier: CC0-1.0
"""
Checks for the machine-facing record format: the seven rules, the six
acceptance criteria, and the bisection structure verdicts null-tested in all
four directions.

    python3 machine-record-format/selftest_mrf.py

Prints `selftest: N checks, M failed` and exits non-zero on any failure.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import base_entry as be           # noqa: E402
import views as vw                # noqa: E402
import aggregate as ag            # noqa: E402
import entry_store as es          # noqa: E402
import bisect_structure as bs     # noqa: E402
import test_case as tc            # noqa: E402
import rule8_cases as r8          # noqa: E402

_checks = 0
_failed = 0


def ok(cond, label):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        print("  FAIL: %s" % label)


def raises(exc, fn, label):
    global _checks, _failed
    _checks += 1
    try:
        fn()
    except exc:
        return
    except Exception as ex:          # noqa: BLE001
        _failed += 1
        print("  FAIL: %s (raised %s, wanted %s)"
              % (label, type(ex).__name__, exc.__name__))
        return
    _failed += 1
    print("  FAIL: %s (did not raise)" % label)


S = be.State
B = be.Boundary


def entry(eid, joules, status=be.MEASURED, boundary=None, exposure=10.0,
          release="2026-01-01", period="2026", unit="person-hours"):
    if status in be.ABSENT:
        exposure = None            # an all-absent entry carries no measured column
    return be.write_base_entry(
        entry_id=eid,
        input_state=S("ore", 100.0, "kg"),
        output_state=S("metal", 5.0, "kg"),
        exposure=exposure, exposure_unit=unit, joules_in=joules,
        period=period, observation_method="meter", provenance="constructed",
        status=status, release_date=release,
        boundary=boundary if boundary is not None
        else B(("extraction",), ("transport",), "gate-to-gate"))


# --------------------------------------------------------------------------
print("Rule 1 -- base entries are transformations, not categories:")
ok(not be.has_category_field(), "BaseEntry has no category field")
raises(be.CategoryInBasePath,
       lambda: be.write_base_entry(entry_id="x", category="mining",
                                   input_state=S("a", 1.0, "kg"),
                                   output_state=S("b", 1.0, "kg"),
                                   exposure_unit="person-hours",
                                   period="2026", status=be.MEASURED,
                                   joules_in=1.0),
       "write path refuses a 'category' keyword")
raises(be.CategoryInBasePath,
       lambda: be.write_base_entry(entry_id="x", naics="212",
                                   input_state=S("a", 1.0, "kg"),
                                   output_state=S("b", 1.0, "kg"),
                                   exposure_unit="person-hours",
                                   period="2026", status=be.MEASURED,
                                   joules_in=1.0),
       "write path refuses a 'naics' keyword")
e_ok = entry("e1", 100.0)
ok(e_ok.entry_id == "e1" and e_ok.joules_in == 100.0, "a transformation entry writes")

# --------------------------------------------------------------------------
print("Rule 2 / acceptance #1 -- views are parallel; base read under a later view:")
reg = vw.ViewRegistry()
e1 = entry("e1", 100.0)
e2 = entry("e2", 200.0)
# entries exist first, with NO view
ok(reg.view_ids() == [], "no view is required or canonical at write time")
# a view added LATER maps the already-written entries, no rewrite
reg.add_view(vw.View("v_naics", "NAICS_2017", "industry classifier",
                     ("", ""), {"e1": "212", "e2": "212"}))
reg.add_view(vw.View("v_task", "ONET_taskclass", "task analyst",
                     ("", ""), {"e1": "extract", "e2": "refine"}))
ok(reg.get("v_naics").label("e1") == "212", "later view labels an existing base entry")
ok(reg.labels_for("e1") == {"v_naics": "212", "v_task": "extract"},
   "an entry carries every view's label side by side, none privileged")
# the base entries are unchanged objects -- no rewrite happened
ok(e1.joules_in == 100.0 and not be.has_category_field(),
   "base entries are not rewritten by adding a view")
reg.retire_view("v_task")
ok(reg.labels_for("e1") == {"v_naics": "212"}, "retiring a view leaves the base intact")

# --------------------------------------------------------------------------
print("Rule 3 / acceptance #2 -- aggregation is a read op; recompute matches:")
reg2 = vw.ViewRegistry()
reg2.add_view(vw.View("v", "metabolic_class", "energy analyst", ("", ""),
                      {"a": "hot", "b": "hot", "c": "cold"}))
ents = [entry("a", 100.0), entry("b", 50.0), entry("c", 30.0)]
spec = ag.AggregateSpec("sum_by_class", "v", ag.SUM)
r1 = ag.compute(spec, ents, reg2, base_version=1)
r2 = ag.compute(spec, ents, reg2, base_version=1)
ok(r1.by_label()["hot"].value == 150.0, "sum over 'hot' group = 150")
ok(r1.by_label()["cold"].value == 30.0, "sum over 'cold' group = 30")
ok([g.value for g in r1.groups] == [g.value for g in r2.groups],
   "recompute from base+spec matches (acceptance #2)")
ok(r1.derived is True, "an aggregate is marked derived, never the record")
cache = ag.AggregateCache()
c1 = cache.cached_or_compute(spec, ents, reg2, 1)
ok(cache.has("sum_by_class", 1), "cache is keyed to spec + base_version")
ok(not cache.has("sum_by_class", 2), "a different base_version is a cache miss")
mean_spec = ag.AggregateSpec("mean", "v", ag.MEAN, denominator="measured_count")
rm = ag.compute(mean_spec, ents, reg2, 1)
ok(abs(rm.by_label()["hot"].value - 75.0) < 1e-9, "mean over 'hot' = 75")
rate_spec = ag.AggregateSpec("rate", "v", ag.RATE, denominator="exposure")
rr = ag.compute(rate_spec, ents, reg2, 1)
ok(abs(rr.by_label()["hot"].value - (150.0 / 20.0)) < 1e-9,
   "rate = joules/exposure = 150/20 per 'hot'")
raises(ValueError,
       lambda: ag.compute(ag.AggregateSpec("r", "v", ag.RATE), ents, reg2, 1),
       "rate with no declared denominator is refused (Rule 5)")

# --------------------------------------------------------------------------
print("Rule 4 / acceptance #4 -- vintages retained; prior version retrievable:")
store = es.EntryStore()
store.write(entry("m", 100.0, release="2026-01-15"))
store.write(entry("m", 120.0, release="2026-03-15"))   # a revision
ok(len(store.versions("m", "2026")) == 2, "both vintages retained, not overwritten")
ok(store.latest("m", "2026").joules_in == 120.0, "latest vintage is the revision")
ok(store.as_of("m", "2026", "2026-02-01").joules_in == 100.0,
   "the vintage current as of an earlier date is the original (acceptance #4)")
ok(store.as_of("m", "2026", "2026-01-01") is None,
   "before first publication, as_of is None (not a fabricated zero)")
ok(store.base_version() == 2, "base_version bumps on every write")
raises(es.MissingReleaseDate,
       lambda: store.write(entry("n", 1.0, release="")),
       "a vintage with no release_date is refused")

# --------------------------------------------------------------------------
print("Rule 5 / acceptance #3 -- boundary always; mismatched sums refused:")
und = entry("u", 100.0, boundary=B())      # undeclared boundary
ok(not und.comparable(), "an undeclared-boundary entry is not comparable")
same_b = B(("extraction",), ("transport",), "gate-to-gate")
other_b = B(("extraction", "transport"), (), "cradle-to-gate")
reg3 = vw.ViewRegistry()
reg3.add_view(vw.View("v", "one", "f", ("", ""),
                      {"p": "g", "q": "g", "r": "g"}))
match = [entry("p", 100.0, boundary=same_b), entry("q", 50.0, boundary=same_b)]
ok(ag.compute(ag.AggregateSpec("s", "v", ag.SUM), match, reg3, 1)
   .by_label()["g"].value == 150.0, "entries with matching boundaries sum")
mixed = [entry("p", 100.0, boundary=same_b), entry("r", 50.0, boundary=other_b)]
raises(be.BoundaryMismatch,
       lambda: ag.compute(ag.AggregateSpec("s", "v", ag.SUM), mixed, reg3, 1),
       "mismatched boundaries refuse to sum without a reconciliation")
recon = [be.Reconciliation(same_b.key(), other_b.key(), 0.0, "declared equal")]
ok(ag.compute(ag.AggregateSpec("s", "v", ag.SUM), mixed, reg3, 1, recon)
   .by_label()["g"].value == 150.0, "a declared reconciliation permits the sum")
und_group = [entry("p", 100.0, boundary=same_b), entry("r", 50.0, boundary=B())]
raises(be.UndeclaredBoundary,
       lambda: ag.compute(ag.AggregateSpec("s", "v", ag.SUM), und_group, reg3, 1),
       "an undeclared boundary in scope raises, not silently included")

# --------------------------------------------------------------------------
print("Rule 6 -- no conversion between exposure classes:")
raises(be.ExposureConversion, lambda: be.convert_exposure(10.0, "person-hours",
                                                          "animal-hours"),
       "convert_exposure raises")
raises(ValueError,
       lambda: be.write_base_entry(entry_id="z",
                                   input_state=S("a", 1.0, "kg"),
                                   output_state=S("b", 1.0, "kg"),
                                   exposure_unit="widget-hours",
                                   period="2026", status=be.MEASURED,
                                   joules_in=1.0),
       "an unknown exposure class is refused")

# --------------------------------------------------------------------------
print("Rule 7 / acceptance #5 -- unmeasured and measured_zero never collapse:")
z = entry("z", 0.0, status=be.MEASURED_ZERO)
u = entry("u", None, status=be.UNMEASURED_NO_INSTRUMENT)
ok(z.numeric_joules() == 0.0, "measured_zero enters a fold as 0.0")
ok(u.numeric_joules() is None, "unmeasured enters a fold as None, never 0.0")
reg4 = vw.ViewRegistry()
reg4.add_view(vw.View("v", "one", "f", ("", ""),
                      {"z": "g", "u": "g", "m": "g"}))
mixed7 = [entry("z", 0.0, status=be.MEASURED_ZERO),
          entry("u", None, status=be.UNMEASURED_NO_INSTRUMENT),
          entry("m", 40.0)]
r7 = ag.compute(ag.AggregateSpec("s", "v", ag.SUM), mixed7, reg4, 1)
g = r7.by_label()["g"]
ok(g.value == 40.0, "sum counts measured (40) + measured_zero (0), not the unmeasured")
ok(g.n_measured == 1 and g.n_measured_zero == 1 and g.n_unmeasured_no_instrument == 1,
   "the three states are counted apart in the result")
allabsent = [entry("u", None, status=be.UNMEASURED_OUT_OF_SCOPE)]
reg5 = vw.ViewRegistry(); reg5.add_view(vw.View("v", "one", "f", ("", ""), {"u": "g"}))
ra = ag.compute(ag.AggregateSpec("s", "v", ag.SUM), allabsent, reg5, 1)
ok(ra.by_label()["g"].value is None and ra.by_label()["g"].flag == ag.NOT_COMPUTABLE,
   "an all-absent group is NOT_COMPUTABLE, never 0.0")

# --------------------------------------------------------------------------
print("Diagnostic / acceptance #6 -- structure verdict before any locus:")
# span = a methodology registry (ordered change ids). test(subspan) = signal
# present. Null-test all four structures.
span = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]

def single(sub):          # signal iff c5 is in scope -> a single locus
    return "c5" in sub
v_single = bs.structure_verdict(span, single)
ok(v_single.structure == bs.SINGLE_LOCUS, "single-locus span -> SINGLE_LOCUS")
loc = bs.locate(span, single)
ok(bs.address(loc) == "c5", "locate resolves the address to c5")

def both(sub):            # signal iff any of c2 (left) or c7 (right)
    return "c2" in sub or "c7" in sub
v_both = bs.structure_verdict(span, both)
ok(v_both.structure == bs.NOT_A_LOCUS, "both-halves span -> NOT_A_LOCUS")
raises(bs.AddressFromNonLocus, lambda: bs.address(bs.locate(span, both)),
       "an address is refused from a both-sides run")

def neither(sub):         # signal iff BOTH c2 and c7 are present (needs both halves)
    return "c2" in sub and "c7" in sub
v_neither = bs.structure_verdict(span, neither)
ok(v_neither.structure == bs.MEASURING_SOMETHING_ELSE,
   "whole-but-neither-half -> MEASURING_SOMETHING_ELSE")

_flip = {"n": 0}
def migrating(sub):
    _flip["n"] += 1
    return _flip["n"] % 2 == 0
v_nd = bs.structure_verdict(span, migrating)
ok(v_nd.structure == bs.NONDETERMINISTIC, "migrating test -> NONDETERMINISTIC")
raises(bs.AddressFromNonLocus, lambda: bs.address(v_nd),
       "an address is refused from a nondeterministic run")
ok(bs.structure_verdict([], single).structure == bs.EMPTY_SPAN, "empty span verdict")
ok(bs.structure_verdict(["c5"], single).structure == bs.SINGLE_ELEMENT_SPAN,
   "single-element carrying span verdict")

# --------------------------------------------------------------------------
print("Rule 8 (v2) -- no payment field in the base layer:")
ok(not be.has_payment_field(), "BaseEntry has no payment/compensation field")
for k in ("paid", "unpaid", "wage", "compensation", "salary"):
    raises(be.PaymentInBasePath,
           lambda k=k: be.write_base_entry(
               entry_id="p", input_state=S("a", 1.0, "kg"),
               output_state=S("b", 1.0, "kg"), exposure_unit="person-hours",
               period="2026", status=be.MEASURED, joules_in=1.0, **{k: True}),
           "write path refuses a %r keyword" % k)
# payment enters ONLY as a Rule 2 view, dated like any other view
payreg = vw.ViewRegistry()
payreg.add_view(vw.View("v_pay", "payment_record", "payroll analyst",
                        ("2026-01-01", ""),
                        {"barn_community": "unpaid", "barn_contract": "paid"}))
paidgroups = payreg.group_by("v_pay", ["barn_community", "barn_contract"])
ok(set(paidgroups) == {"paid", "unpaid"},
   "payment lives in a view (Rule 2), separating paid from unpaid there")

# --------------------------------------------------------------------------
print("acceptance #7 -- a paid-only aggregate needs a view + boundary exclusion:")
# there is no base-field route to 'paid' -- the only route is the view above,
# and selecting one of its labels is a boundary exclusion the reader declares.
ok(not (set(f.name for f in __import__("dataclasses").fields(be.BaseEntry))
        & set(be._PAYMENT_KEYS)),
   "no base field can carry payment; the paid subset exists only via the view")
# a paid subset exists only via the payment view above; selecting one of its
# labels is a boundary exclusion the reader must declare (Rule 5).
ce = r8._run_case_a()   # writes barn_community / barn_contract on identical footing
ok(ce["no_payment_field"] and ce["payment_field_refused"],
   "the two barn entries carry no payment field and refuse one")

# --------------------------------------------------------------------------
print("test-case format (v2) -- tests / does_not_test / why_not REQUIRED:")
good = tc.TestCase("g", "establishes X", "does not establish Y",
                   "because Z blocks it")
tc.validate_case(good)
ok(good.citable(), "a complete case is citable")
raises(tc.IncompleteCase,
       lambda: tc.validate_case(tc.TestCase("bad", "establishes X", "", "")),
       "a case with no does_not_test is refused (must not be cited)")
raises(tc.IncompleteCase,
       lambda: tc.validate_case(tc.TestCase("bad2", "", "not Y", "because")),
       "a case with no tests is refused")

# --------------------------------------------------------------------------
print("Rule 8 cases A / B / C -- each tests a DIFFERENT thing:")
for case in r8.CASES:
    tc.validate_case(case)          # each carries the required triple
    ok(case.citable(), "%s is citable (carries the triple)" % case.name)
# they are not merged: the three does_not_test fields are distinct
dnt = {c.does_not_test for c in r8.CASES}
ok(len(dnt) == 3, "the three cases have distinct does_not_test boundaries")

# Case A -- Rule 8 end to end
a = r8.CASE_A.run()
ok(a["both_present"] and a["summable_joules"] == 8.0e8 + 7.0e8,
   "Case A: both entries present and summable on identical footing")
ok(a["no_payment_field"] and a["payment_field_refused"],
   "Case A: neither carries a payment field; one is refused")

# Case B -- strong output, absent exposure, efficiency not computable
b = r8.CASE_B.run()
ok(b["accepted_with_absent_exposure"], "Case B: entry accepted despite absent exposure")
ok(b["exposure_value_is_none"], "Case B: absent exposure is None, not fabricated")
ok(b["ratio_flag"] == ag.NOT_COMPUTABLE, "Case B: efficiency ratio is NOT_COMPUTABLE")
ok(b["durability_readable"] == 750.0, "Case B: the output column reads regardless")

# Case C -- labor-unit comparison without conversion
c = r8.CASE_C.run()
ok(c["compared_on_native_unit"] == 9200.0, "Case C: compared on native labor units")
ok(c["same_exposure_class"], "Case C: same exposure class, no cross-class step")
ok(c["convert_raises"], "Case C: conversion to a monetary unit raises (Rule 6)")

# Case B forces per-column Rule 7: an entry-level status cannot say
# "output measured, exposure absent" -- column_status can.
mixed_col = be.write_base_entry(
    entry_id="mc", input_state=S("a", 1.0, "kg"),
    output_state=S("b", 1.0, "kg"), exposure=None, exposure_unit="person-hours",
    joules_in=500.0, period="2026", observation_method="m",
    provenance="c", status=be.MEASURED,
    boundary=be.Boundary(("x",), ("y",), "r"), release_date="2026-01-01",
    column_status={"exposure": be.UNMEASURED_NO_INSTRUMENT})
ok(mixed_col.numeric_joules() == 500.0 and mixed_col.exposure_value() is None,
   "per-column status: joules measured while exposure absent, in one entry")
raises(ValueError,
       lambda: be.write_base_entry(
           entry_id="bad", input_state=S("a", 1.0, "kg"),
           output_state=S("b", 1.0, "kg"), exposure=42.0,
           exposure_unit="person-hours", joules_in=1.0, period="2026",
           observation_method="m", provenance="c", status=be.MEASURED,
           boundary=be.Boundary(("x",), ("y",), "r"), release_date="2026-01-01",
           column_status={"exposure": be.UNMEASURED_NO_INSTRUMENT}),
       "an absent column carrying a number is refused (not estimated)")

# --------------------------------------------------------------------------
print("v2 demo -- no_severity three-arm exemption (delivered case text):")
import demo_v2                      # noqa: E402
import no_severity as nosev         # noqa: E402
_text = demo_v2.render()
_exempt = demo_v2._declared_exemption()
# arm 1: masked (exempt tokens removed) -> the render is clean
_masked = _text
for w in _exempt:
    _masked = __import__("re").sub(r"\b%s\b" % w, "X", _masked, flags=__import__("re").I)
ok(nosev.check(_masked)[0], "arm 1: render is clean once the exempt token is masked")
# arm 2: the exempt token is the ONLY firer on the unmasked render
_firers = {w.lower() for (_l, w, _s) in nosev.hits(_text)}
ok(_firers == {x.lower() for x in _exempt},
   "arm 2: the declared exemption is exactly the set of firers")
# arm 3: each exempt token appears in a delivered case string
_delivered = " ".join(c.tests + " " + c.does_not_test + " " + c.why_not
                      for c in r8.CASES).lower()
ok(all(w.lower() in _delivered for w in _exempt),
   "arm 3: every exempt token is in the delivered case text")
# arm 3b: a planted banned word is still caught through the exemption
ok(not nosev.check(_masked + "\nthis is wrong")[0],
   "arm 3b: a planted banned word is caught through the exemption")

# --------------------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
