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
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
