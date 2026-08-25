#!/usr/bin/env python3
"""
record -- the seven-field claim record, and the validator that refuses.

    record.py validate [DIR]        every record, with findings
    record.py path CLAIM_ID [DIR]   the load path, walked upward
    record.py due [DIR] [--on ISO]  claims whose next-check has passed
    record.py --selftest

THE DESIGN MOVE, and everything else follows from it: this schema has no
way to say NOTHING. It only has ways to say "not known, and here is
why". Rule two says no field is optional because optional is how the
domain of validity disappeared -- so a field that cannot be filled is
filled with a stated sentinel (UNTESTED, UNQUANTIFIED, and each carries
a reason), never left out and never left blank. An omission and a known
negative are different states and the schema keeps them apart in every
field that can carry either.

That is the same repair this repository has recorded more than a dozen
times and implemented at construction only a handful, which is the only
point where it is free.

WHAT IS ENFORCED STRUCTURALLY, and it is most of it: intervals that are
not inverted, units that are not blank, a point measurement that has to
say why it is a point, error characteristics that are quantified or
explicitly not, at least one named condition, a parseable clock, parents
that resolve, no cycles, and a collapse statistic from a closed
vocabulary.

WHAT IS ENFORCED LEXICALLY, and it is one field: "stated without
hedges". A word list catches the fluent failure -- reaching for "may",
"appears", "roughly" without noticing -- and any paraphrase steps around
it. That limit is stated here rather than at the bottom, alongside
UNI_009, DF_010 and ACL_017, which are the same limit on other
substrates. The screen is null-tested in both directions.

CC0. stdlib only. Parses under Python 3.9. ASCII only.
"""

import datetime
import json
import os
import re
import sys

# One screen, imported rather than copied. sheet-structure-scan owns it,
# the repository convention is to import the shared instrument so the two
# copies cannot drift, and MF_019 is what copying costs.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "sheet-structure-scan"))
import no_severity  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RECORDS = os.path.join(HERE, "records")

FIELDS = ("assertion", "measurement", "instrument", "domain_of_validity",
          "clock", "derivation", "collapse_record")

# Field 7 states. A point measurement is legal only under COLLAPSED or
# EXACT, and an interval is illegal under EXACT. See _check_collapse.
NOT_COLLAPSED = "NOT_COLLAPSED"
COLLAPSED = "COLLAPSED"
COLLAPSED_UPSTREAM = "COLLAPSED_UPSTREAM"
EXACT = "EXACT"
COLLAPSE_STATES = (NOT_COLLAPSED, COLLAPSED, COLLAPSED_UPSTREAM, EXACT)

# Closed vocabulary for WHICH point, with a named escape. Closed, because
# "a statistic" as free text is how the upper quartile disappears into
# "the value"; with an escape, because uninstrumented/UNI_013 recorded
# what a vocabulary closed on purpose costs when a real case does not
# fit, and the repair it asked for was exactly this.
POINTS = ("mean", "median", "mode", "min", "max",
          "lower_quartile", "upper_quartile", "interquartile_range",
          "percentile", "single_draw", "other")

ERROR_KINDS = ("random", "systematic", "both", "UNQUANTIFIED")

# Hedges. The assertion states the thing; the interval in field 2 carries
# the imprecision. A hedge in field 1 is imprecision stated twice, once
# where it can be measured and once where it cannot.
HEDGES = [
    "may", "might", "could", "possibly", "perhaps", "probably", "likely",
    "unlikely", "seems", "seem", "appears", "appear", "apparently",
    "arguably", "roughly", "approximately", "about", "around", "some",
    "several", "often", "usually", "generally", "typically", "tends",
    "suggests", "suggest", "indicates", "indicate", "presumably",
    "somewhat", "fairly", "rather", "quite", "essentially", "basically",
    "more or less", "or so", "ish",
]
_HEDGE_PATTERNS = [(w, re.compile(r"\b%s\b" % re.escape(w), re.I))
                   for w in HEDGES]

VALID = "VALID"
INVALID = "INVALID"

# Field 5 states. UNDERIVABLE and UNBOUNDED_BY_THIS_TERM are both "no
# date", and they are not the same thing: the first is a term nobody
# measured, the second is a term the result does not depend on.
DERIVED_CLOCK = "DERIVED"
UNDERIVABLE = "UNDERIVABLE"
UNBOUNDED = "UNBOUNDED_BY_THIS_TERM"
ADIABATIC = "ADIABATIC"
SUDDEN = "SUDDEN"
REGIME_UNKNOWN = "REGIME_UNKNOWN"

# A sub-field is either a measured quantity or a stated absence.
UNMEASURED = "UNMEASURED"

# [CHOICE] below this the neglected term is treated as uncoupled and the
# shelf life is UNBOUNDED_BY_THIS_TERM rather than a very large number.
# A number would sort; a state does not pretend to.
COUPLING_FLOOR = 1e-6


def _quantity(d, name, out, field, units_expected):
    """A sub-field is a value with a basis, or UNMEASURED with a reason.

    Returns the float, or None when it is a stated absence, and appends
    a finding when it is neither.
    """
    q = d.get(name)
    if not isinstance(q, dict):
        out.append(Finding("MISSING_FIELD", "%s.%s" % (field, name),
                           "a value with a basis, or state UNMEASURED "
                           "with a why"))
        return None
    if q.get("state") == UNMEASURED:
        if not str(q.get("why", "")).strip():
            out.append(Finding(
                "CLOCK_NOT_DERIVED", "%s.%s.why" % (field, name),
                "UNMEASURED is a stated value and carries its reason"))
        return None
    v = q.get("value")
    if not isinstance(v, (int, float)):
        out.append(Finding("CLOCK_NOT_DERIVED", "%s.%s.value" % (field, name),
                           "not a number, and not stated UNMEASURED"))
        return None
    if not str(q.get("basis", "")).strip():
        out.append(Finding(
            "CLOCK_NOT_DERIVED", "%s.%s.basis" % (field, name),
            "a derived sub-field carries what it was derived from; "
            "without it the clock is asserted one level down"))
    if units_expected and q.get("units") != units_expected:
        out.append(Finding("CLOCK_NOT_DERIVED", "%s.%s.units" % (field, name),
                           "expected %r, got %r"
                           % (units_expected, q.get("units"))))
    return float(v)


def derive_clock(rec):
    """Field 5, computed from its three sub-fields. Never asserted.

    shelf_life = time_constant / |coupling|

    The coupling is a DIMENSIONLESS elasticity, and it has to be: a raw
    partial derivative carries the units of the result over the units of
    the neglected term, and a time divided by that is not a time. So the
    weighting quantity is (dY/Y)/(dX/X), which is what coupling.py
    measures by perturbation.

    Weak coupling means a fast-moving neglected term does not shorten
    the shelf life, and at zero coupling it does not bound it at all --
    reported as a state, not as a large number.
    """
    c = rec.get("clock")
    if not isinstance(c, dict):
        return {"state": UNDERIVABLE, "why": "no clock field"}
    out = []
    tau = _quantity(c, "time_constant", out, "clock", "years")
    ceil = _quantity(c, "rate_ceiling", out, "clock", "per_year")
    coup = _quantity(c, "coupling", out, "clock", "1")

    regime = REGIME_UNKNOWN
    if tau is not None and ceil is not None and tau > 0:
        regime = ADIABATIC if (1.0 / tau) <= ceil else SUDDEN

    if tau is None or coup is None:
        missing = [n for n, v in (("time_constant", tau), ("coupling", coup))
                   if v is None]
        return {"state": UNDERIVABLE, "regime": regime, "findings": out,
                "missing": missing, "shelf_life_years": None,
                "next_check": None,
                "why": "no date is emitted; %s is not measured"
                       % " and ".join(missing)}
    if abs(coup) < COUPLING_FLOOR:
        return {"state": UNBOUNDED, "regime": regime, "findings": out,
                "shelf_life_years": None, "next_check": None,
                "why": "the result does not depend on the neglected term, "
                       "so that term does not date the claim"}
    shelf = tau / abs(coup)
    nc = None
    m = c.get("measured_on")
    try:
        d0 = datetime.date.fromisoformat(str(m))
        nc = (d0 + datetime.timedelta(days=shelf * 365.2425)).isoformat()
    except (ValueError, TypeError):
        out.append(Finding("CLOCK_NOT_DERIVED", "clock.measured_on",
                           "%r is not an ISO date, so no next check can be "
                           "computed from the shelf life" % m))
    return {"state": DERIVED_CLOCK, "regime": regime, "findings": out,
            "shelf_life_years": shelf, "next_check": nc,
            "why": "time constant %g years / coupling %g" % (tau, abs(coup))}


class Finding(object):
    __slots__ = ("code", "field", "detail")

    def __init__(self, code, field, detail):
        self.code = code
        self.field = field
        self.detail = detail

    def __repr__(self):
        return "%s[%s] %s" % (self.code, self.field, self.detail)

    def as_row(self):
        return [self.code, self.field, self.detail]


def hedges_in(text):
    return [w for w, p in _HEDGE_PATTERNS if p.search(text or "")]


# ------------------------------------------------------------- per field

def _need(rec, field, out):
    """Rule two, at the top level. Absent is not a value."""
    if field not in rec:
        out.append(Finding("MISSING_FIELD", field,
                           "no field is optional; a value that cannot be "
                           "known is stated as a sentinel with a reason"))
        return False
    return True


def _check_assertion(rec, out):
    a = rec.get("assertion")
    if not isinstance(a, str) or not a.strip():
        out.append(Finding("EMPTY_VALUE", "assertion", "blank"))
        return
    hs = hedges_in(a)
    if hs:
        out.append(Finding(
            "HEDGE_IN_ASSERTION", "assertion",
            "hedges present (%s); the interval in field 2 carries the "
            "imprecision" % ", ".join(hs)))


def _check_measurement(rec, out):
    m = rec.get("measurement")
    if not isinstance(m, dict):
        out.append(Finding("EMPTY_VALUE", "measurement", "not a mapping"))
        return
    for k in ("lo", "hi", "units"):
        if k not in m:
            out.append(Finding("MISSING_FIELD", "measurement.%s" % k,
                               "an interval is lo, hi and units"))
    lo, hi = m.get("lo"), m.get("hi")
    if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
        if lo > hi:
            out.append(Finding("INTERVAL_INVERTED", "measurement",
                               "lo %r is above hi %r" % (lo, hi)))
    u = m.get("units")
    if not isinstance(u, str) or not u.strip():
        out.append(Finding(
            "UNITS_BLANK", "measurement.units",
            "dimensionless is a value and is written as such, not left "
            "blank"))


def _check_instrument(rec, out):
    i = rec.get("instrument")
    if not isinstance(i, dict):
        out.append(Finding("EMPTY_VALUE", "instrument", "not a mapping"))
        return
    if not str(i.get("name", "")).strip():
        out.append(Finding("EMPTY_VALUE", "instrument.name", "blank"))
    err = i.get("error")
    if not isinstance(err, dict):
        out.append(Finding(
            "ERROR_NOT_CHARACTERISED", "instrument.error",
            "field 3 is what produced the measurement AND its known error "
            "characteristics; the second half is not optional"))
        return
    kind = err.get("kind")
    if kind not in ERROR_KINDS:
        out.append(Finding("ERROR_NOT_CHARACTERISED", "instrument.error.kind",
                           "one of %s" % ", ".join(ERROR_KINDS)))
        return
    if kind == "UNQUANTIFIED":
        if not str(err.get("why", "")).strip():
            out.append(Finding(
                "ERROR_NOT_CHARACTERISED", "instrument.error.why",
                "UNQUANTIFIED is a stated value and carries its reason; "
                "without one it is an omission wearing a sentinel"))
    elif not str(err.get("magnitude", "")).strip():
        out.append(Finding("ERROR_NOT_CHARACTERISED",
                           "instrument.error.magnitude",
                           "a characterised error has a magnitude"))


def _check_domain(rec, out):
    d = rec.get("domain_of_validity")
    if not isinstance(d, dict):
        out.append(Finding("EMPTY_VALUE", "domain_of_validity",
                           "not a mapping"))
        return
    conds = d.get("conditions")
    if not isinstance(conds, list) or not conds:
        out.append(Finding(
            "NO_CONDITIONS", "domain_of_validity.conditions",
            "at least one named condition under which the measurement was "
            "taken; this is the field that gets stripped"))
    else:
        for n, c in enumerate(conds):
            if not isinstance(c, dict) or not str(c.get("name", "")).strip() \
                    or not str(c.get("value", "")).strip():
                out.append(Finding("NO_CONDITIONS",
                                   "domain_of_validity.conditions[%d]" % n,
                                   "each condition is a name and a value"))
    if "outside_this" not in d:
        out.append(Finding(
            "MISSING_FIELD", "domain_of_validity.outside_this",
            "what is known to happen outside the conditions; UNTESTED is "
            "a legal value and an omission is not"))
    elif not str(d.get("outside_this", "")).strip():
        out.append(Finding("EMPTY_VALUE", "domain_of_validity.outside_this",
                           "blank; write UNTESTED"))


def _check_clock(rec, out):
    """Rule 3: a clock asserted rather than derived does not validate."""
    c = rec.get("clock")
    if not isinstance(c, dict):
        out.append(Finding("EMPTY_VALUE", "clock", "not a mapping"))
        return
    for banned in ("holds_for", "next_check", "shelf_life", "shelf_life_years"):
        if banned in c:
            out.append(Finding(
                "CLOCK_ASSERTED", "clock.%s" % banned,
                "the clock is derived from time_constant, rate_ceiling and "
                "coupling; a literal here is the field the schema exists to "
                "protect being written by hand"))
    n = c.get("neglected_term")
    if not isinstance(n, dict) or not str(n.get("held_fixed", "")).strip():
        out.append(Finding(
            "CLOCK_NOT_DERIVED", "clock.neglected_term.held_fixed",
            "what did this claim hold fixed; the time constant is a "
            "property of that thing and cannot be stated without it"))
    if "measured_on" not in c:
        out.append(Finding("MISSING_FIELD", "clock.measured_on",
                           "the anchor a next check is computed from"))
    out.extend(derive_clock(rec).get("findings", []))


def _check_derivation(rec, out):
    d = rec.get("derivation")
    if not isinstance(d, dict):
        out.append(Finding("EMPTY_VALUE", "derivation", "not a mapping"))
        return
    ps = d.get("parents")
    if not isinstance(ps, list):
        out.append(Finding("MISSING_FIELD", "derivation.parents",
                           "a list, empty for a stated root"))
        return
    if not ps and not str(d.get("root_reason", "")).strip():
        out.append(Finding(
            "ROOT_UNEXPLAINED", "derivation.root_reason",
            "an empty parent list is a claim to be a root and carries its "
            "reason; without one it cannot be told from parents that were "
            "never recorded"))


def _check_collapse(rec, out):
    c = rec.get("collapse_record")
    m = rec.get("measurement") if isinstance(rec.get("measurement"), dict) \
        else {}
    if not isinstance(c, dict):
        out.append(Finding("EMPTY_VALUE", "collapse_record", "not a mapping"))
        return
    state = c.get("state")
    if state not in COLLAPSE_STATES:
        out.append(Finding("MISSING_FIELD", "collapse_record.state",
                           "one of %s" % ", ".join(COLLAPSE_STATES)))
        return
    if state == COLLAPSED:
        if not str(c.get("from", "")).strip():
            out.append(Finding("COLLAPSE_POINT_UNNAMED", "collapse_record.from",
                               "what distribution was reduced"))
        if c.get("point") not in POINTS:
            out.append(Finding("COLLAPSE_POINT_UNNAMED",
                               "collapse_record.point",
                               "which point, from %s" % ", ".join(POINTS)))
        elif c.get("point") == "other" and not str(c.get("point_name", "")) \
                .strip():
            out.append(Finding("COLLAPSE_POINT_UNNAMED",
                               "collapse_record.point_name",
                               "'other' names the statistic it is"))
        if not str(c.get("why", "")).strip():
            out.append(Finding("COLLAPSE_POINT_UNNAMED", "collapse_record.why",
                               "why that point and not another"))
    if state == COLLAPSED_UPSTREAM:
        # A point that arrived as a point from a source that did not say
        # what it collapsed. Distinct from COLLAPSED, where the statistic
        # is known, and from EXACT, where there was nothing to collapse.
        # The three fixtures separate exactly here: the hotel source
        # states "upper quartile", the Palestine value is a mean computed
        # in the workbook itself, and the grid dataset says neither.
        for k in ("source", "what_is_unstated"):
            if not str(c.get(k, "")).strip():
                out.append(Finding(
                    "COLLAPSE_POINT_UNNAMED", "collapse_record.%s" % k,
                    "a point taken from a source that did not state its "
                    "statistic names the source and what is unstated"))
    if state == EXACT and not str(c.get("basis", "")).strip():
        out.append(Finding("COLLAPSE_POINT_UNNAMED", "collapse_record.basis",
                           "why the quantity is exact rather than estimated"))

    # The coupling between fields 2 and 7. A point that does not say why
    # it is a point is the failure this field exists for.
    lo, hi = m.get("lo"), m.get("hi")
    if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
        if lo == hi and state == NOT_COLLAPSED:
            out.append(Finding(
                "POINT_WITHOUT_BASIS", "collapse_record.state",
                "the measurement is a point and field 7 says nothing was "
                "collapsed and nothing is exact; a point arrives either "
                "from a distribution or from a count"))
        if lo == hi and state == COLLAPSED_UPSTREAM:
            pass  # legal: that is what an upstream point is
        if lo != hi and state == EXACT:
            out.append(Finding(
                "INTERVAL_MARKED_EXACT", "collapse_record.state",
                "an interval was reported and field 7 claims an exact "
                "quantity"))


_CHECKS = {
    "assertion": _check_assertion,
    "measurement": _check_measurement,
    "instrument": _check_instrument,
    "domain_of_validity": _check_domain,
    "clock": _check_clock,
    "derivation": _check_derivation,
    "collapse_record": _check_collapse,
}


# ------------------------------------------------------------- registry

class Registry(object):
    def __init__(self, records=None):
        self.records = dict(records or {})

    @classmethod
    def load(cls, directory=None):
        directory = directory or RECORDS
        recs = {}
        if os.path.isdir(directory):
            for fn in sorted(os.listdir(directory)):
                if not fn.endswith(".json"):
                    continue
                with open(os.path.join(directory, fn)) as fh:
                    r = json.load(fh)
                recs[r.get("id", fn)] = r
        return cls(recs)

    def validate(self, cid):
        """Rule two field by field, then rule one against the registry."""
        rec = self.records.get(cid)
        out = []
        if rec is None:
            return INVALID, [Finding("PARENT_UNRESOLVED", "id",
                                     "%s is not in the registry" % cid)]
        for f in FIELDS:
            if _need(rec, f, out):
                _CHECKS[f](rec, out)

        # Rule one. An unresolvable parent does not validate, and a cycle
        # is reported as a cycle rather than as recursion.
        d = rec.get("derivation")
        if isinstance(d, dict) and isinstance(d.get("parents"), list):
            for p in d["parents"]:
                if p not in self.records:
                    out.append(Finding(
                        "PARENT_UNRESOLVED", "derivation.parents",
                        "%r does not resolve in this registry" % p))
            cyc = self._cycle(cid)
            if cyc:
                out.append(Finding("PARENT_CYCLE", "derivation.parents",
                                   " -> ".join(cyc)))
        return (VALID if not out else INVALID), out

    def _cycle(self, cid, seen=None, stack=None):
        seen = seen or set()
        stack = stack or []
        if cid in stack:
            return stack[stack.index(cid):] + [cid]
        rec = self.records.get(cid)
        if rec is None:
            return None
        d = rec.get("derivation") or {}
        for p in (d.get("parents") or []):
            got = self._cycle(p, seen, stack + [cid])
            if got:
                return got
        return None

    def path(self, cid, depth=0, seen=None):
        """The load path, walked upward. Field 6's whole purpose."""
        seen = seen or set()
        rec = self.records.get(cid)
        if rec is None:
            return [(depth, cid, "UNRESOLVED")]
        if cid in seen:
            return [(depth, cid, "CYCLE")]
        seen = seen | {cid}
        rows = [(depth, cid, (rec.get("assertion") or "")[:70])]
        for p in ((rec.get("derivation") or {}).get("parents") or []):
            rows.extend(self.path(p, depth + 1, seen))
        return rows

    def due(self, on):
        """Field 5 made operative, from the DERIVED clock.

        A record whose clock is underivable gets no date and is reported
        as such. Emitting a default here is the failure the whole field
        exists to prevent, so there is no branch that can produce one.
        """
        out = []
        for cid, rec in sorted(self.records.items()):
            d = derive_clock(rec)
            shelf = d.get("shelf_life_years")
            nc = d.get("next_check")
            if d["state"] != DERIVED_CLOCK or not nc:
                out.append((cid, d["state"], "-", "-", d.get("regime", "-")))
                continue
            got = datetime.date.fromisoformat(nc)
            out.append((cid, d["state"], "%.2f" % shelf, nc,
                        "DUE" if got <= on else "CURRENT"))
        return out


# ------------------------------------------------------------- rendering

def table(headers, rows):
    widths = [len(h) for h in headers]
    body = [[str(x) for x in r] for r in rows]
    for r in body:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(c))
    fmt = "  ".join("%-" + str(w) + "s" for w in widths)
    out = [fmt % tuple(headers), fmt % tuple("-" * w for w in widths)]
    for r in body:
        out.append((fmt % tuple(r)).rstrip())
    return "\n".join(out)


def render_validate(reg):
    lines = ["claim records -- validation",
             "",
             "Every verdict below is about CONFORMANCE TO THE RECORD",
             "SCHEMA. No column states whether a claim is true, how much",
             "weight a measurement carries, or what to do next, and none",
             "of those is computed here. The reading stays with the",
             "operator, which is the detector's rule.",
             "",
             "records   %d" % len(reg.records),
             "rule 1    a claim with an unresolvable parent does not validate",
             "rule 2    no field is optional; a sentinel carries its reason",
             ""]
    rows = []
    nvalid = 0
    for cid in sorted(reg.records):
        state, findings = reg.validate(cid)
        nvalid += state == VALID
        rows.append([cid, state, len(findings)])
    lines.append(table(["claim", "state", "findings"], rows))
    for cid in sorted(reg.records):
        state, findings = reg.validate(cid)
        if not findings:
            continue
        lines += ["", "%s" % cid]
        lines.append(table(["code", "field", "detail"],
                           [f.as_row() for f in findings]))
    lines += ["", "%d of %d validate." % (nvalid, len(reg.records))]
    return "\n".join(lines)


# ------------------------------------------------------------- selftest

def _complete():
    """One record that must validate. Without it the null arms below are
    passed by a validator that refuses everything."""
    return {
        "id": "T-OK",
        "assertion": "The reader resolved 825 of 825 formula cells.",
        "measurement": {"lo": 825, "hi": 825, "units": "cells"},
        "instrument": {
            "name": "ElementTree parse of xl/worksheets/*.xml",
            "error": {"kind": "systematic", "magnitude":
                      "array formulas beyond their anchor are not counted"},
        },
        "domain_of_validity": {
            "conditions": [{"name": "file", "value": "one workbook"}],
            "outside_this": "UNTESTED",
        },
        "clock": {
            "measured_on": "2026-08-25",
            "neglected_term": {"name": "reader revision",
                               "held_fixed": "the parser that produced the count"},
            "time_constant": {"value": 1.0, "units": "years",
                              "basis": "one revision per year, stipulated here"},
            "rate_ceiling": {"value": 2.0, "units": "per_year",
                             "basis": "stipulated here"},
            "coupling": {"value": 0.5, "units": "1",
                         "basis": "stipulated here"}},
        "derivation": {"parents": [], "root_reason": "a direct count"},
        "collapse_record": {"state": EXACT, "basis": "a count of elements"},
    }


def _selftest():
    import copy
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("record selftest")

    base = _complete()
    reg = Registry({base["id"]: base})
    ck("a complete record validates", reg.validate("T-OK")[0], VALID)

    # Rule two, one arm per field. A validator that refuses everything
    # passes all seven of these and fails the check above, which is why
    # that check is first.
    for f in FIELDS:
        r = copy.deepcopy(base)
        del r[f]
        st, fs = Registry({r["id"]: r}).validate("T-OK")
        ck("dropping %s is caught" % f,
           (st, any(x.code == "MISSING_FIELD" and x.field == f for x in fs)),
           (INVALID, True))

    def variant(**kw):
        r = copy.deepcopy(base)
        for k, v in kw.items():
            cur = r
            parts = k.split("__")
            for p in parts[:-1]:
                cur = cur[p]
            cur[parts[-1]] = v
        return Registry({r["id"]: r}).validate("T-OK")

    def codes(res):
        return sorted({f.code for f in res[1]})

    ck("a hedge in the assertion is caught",
       codes(variant(assertion="The reader probably resolved most cells.")),
       ["HEDGE_IN_ASSERTION"])
    ck("an inverted interval is caught",
       "INTERVAL_INVERTED" in codes(variant(
           measurement={"lo": 9, "hi": 1, "units": "cells"},
           collapse_record={"state": NOT_COLLAPSED})), True)
    ck("blank units are caught",
       "UNITS_BLANK" in codes(variant(
           measurement={"lo": 1, "hi": 9, "units": "  "},
           collapse_record={"state": NOT_COLLAPSED})), True)

    # The field 2 / field 7 coupling, both directions.
    ck("a point with nothing collapsed and nothing exact is caught",
       "POINT_WITHOUT_BASIS" in codes(variant(
           collapse_record={"state": NOT_COLLAPSED})), True)
    ck("an interval marked exact is caught",
       "INTERVAL_MARKED_EXACT" in codes(variant(
           measurement={"lo": 1, "hi": 9, "units": "cells"})), True)
    ck("a point from a named statistic validates",
       variant(collapse_record={"state": COLLAPSED,
                                "from": "48 per-sheet counts",
                                "point": "upper_quartile",
                                "why": "the reporting convention"})[0], VALID)
    ck("a collapse with no named point is caught",
       "COLLAPSE_POINT_UNNAMED" in codes(variant(
           collapse_record={"state": COLLAPSED, "from": "x", "why": "y"})),
       True)
    ck("an upstream point without its source is caught",
       "COLLAPSE_POINT_UNNAMED" in codes(variant(
           collapse_record={"state": COLLAPSED_UPSTREAM})), True)
    ck("an upstream point that names the source and the gap validates",
       variant(collapse_record={
           "state": COLLAPSED_UPSTREAM,
           "source": "a published dataset",
           "what_is_unstated": "which statistic the point is"})[0], VALID)
    ck("'other' has to name the statistic",
       "COLLAPSE_POINT_UNNAMED" in codes(variant(
           collapse_record={"state": COLLAPSED, "from": "x",
                            "point": "other", "why": "y"})), True)

    ck("an uncharacterised error is caught",
       "ERROR_NOT_CHARACTERISED" in codes(variant(
           instrument__error={"kind": "random"})), True)
    ck("UNQUANTIFIED without a reason is caught",
       "ERROR_NOT_CHARACTERISED" in codes(variant(
           instrument__error={"kind": "UNQUANTIFIED"})), True)
    ck("UNQUANTIFIED with a reason validates",
       variant(instrument__error={"kind": "UNQUANTIFIED",
                                  "why": "no repeat run exists"})[0], VALID)

    ck("no conditions is caught",
       "NO_CONDITIONS" in codes(variant(
           domain_of_validity={"conditions": [], "outside_this": "UNTESTED"})),
       True)
    ck("a missing outside_this is caught",
       "MISSING_FIELD" in codes(variant(
           domain_of_validity={"conditions": [{"name": "a", "value": "b"}]})),
       True)
    ck("UNTESTED outside_this validates",
       variant(domain_of_validity={"conditions": [{"name": "a", "value": "b"}],
                                   "outside_this": "UNTESTED"})[0], VALID)

    # Rule 3. The field the whole thing exists to protect.
    hand = copy.deepcopy(base["clock"])
    hand["next_check"] = "2027-01-01"
    ck("a hand-written next_check does not validate",
       "CLOCK_ASSERTED" in codes(variant(clock=hand)), True)
    hand2 = copy.deepcopy(base["clock"])
    hand2["holds_for"] = "a year"
    ck("a hand-written holds_for does not validate",
       "CLOCK_ASSERTED" in codes(variant(clock=hand2)), True)
    noterm = copy.deepcopy(base["clock"])
    del noterm["neglected_term"]
    ck("a clock with nothing held fixed does not validate",
       "CLOCK_NOT_DERIVED" in codes(variant(clock=noterm)), True)
    nobasis = copy.deepcopy(base["clock"])
    nobasis["time_constant"] = {"value": 1.0, "units": "years"}
    ck("a sub-field with no basis does not validate",
       "CLOCK_NOT_DERIVED" in codes(variant(clock=nobasis)), True)

    # The derivation itself.
    d = derive_clock(base)
    ck("shelf life is the time constant weighted by coupling",
       (d["state"], round(d["shelf_life_years"], 6)), (DERIVED_CLOCK, 2.0))
    ck("and the next check follows from it",
       d["next_check"], "2028-08-24")
    ck("regime is adiabatic when the term moves below the ceiling",
       d["regime"], ADIABATIC)

    fast = copy.deepcopy(base["clock"])
    fast["time_constant"] = {"value": 0.1, "units": "years",
                             "basis": "stipulated"}
    d2 = derive_clock({"clock": fast})
    ck("a faster term shortens the shelf life",
       round(d2["shelf_life_years"], 6), 0.2)
    ck("and crossing the ceiling makes it sudden", d2["regime"], SUDDEN)

    # The rule the drop states outright.
    weak = copy.deepcopy(base["clock"])
    weak["time_constant"] = {"value": 0.01, "units": "years",
                             "basis": "very fast"}
    weak["coupling"] = {"value": 0.0, "units": "1", "basis": "pinned"}
    d3 = derive_clock({"clock": weak})
    ck("weak coupling: a fast term does not shorten the shelf life",
       (d3["state"], d3["next_check"]), (UNBOUNDED, None))

    # The Palestine shape: no clock, and no default emitted.
    nomeas = copy.deepcopy(base["clock"])
    nomeas["time_constant"] = {"state": UNMEASURED,
                               "why": "nobody measured how fast it changes"}
    d4 = derive_clock({"clock": nomeas})
    ck("an unmeasured sub-field yields no date and says why",
       (d4["state"], d4["next_check"], d4["missing"]),
       (UNDERIVABLE, None, ["time_constant"]))
    ck("and the record still validates, because the absence is stated",
       variant(clock=nomeas)[0], VALID)
    nowhy = copy.deepcopy(base["clock"])
    nowhy["time_constant"] = {"state": UNMEASURED}
    ck("UNMEASURED without a reason does not validate",
       "CLOCK_NOT_DERIVED" in codes(variant(clock=nowhy)), True)

    ck("an empty parent list with no reason is caught",
       "ROOT_UNEXPLAINED" in codes(variant(derivation={"parents": []})), True)

    # Rule one.
    child = copy.deepcopy(base)
    child["id"] = "T-CHILD"
    child["derivation"] = {"parents": ["T-MISSING"]}
    st, fs = Registry({base["id"]: base, "T-CHILD": child}).validate("T-CHILD")
    ck("an unresolvable parent does not validate",
       (st, any(f.code == "PARENT_UNRESOLVED" for f in fs)), (INVALID, True))

    child2 = copy.deepcopy(child)
    child2["derivation"] = {"parents": ["T-OK"]}
    ck("a resolvable parent validates",
       Registry({base["id"]: base, "T-CHILD": child2}).validate("T-CHILD")[0],
       VALID)

    a = copy.deepcopy(base)
    a["id"] = "T-A"
    a["derivation"] = {"parents": ["T-B"]}
    b = copy.deepcopy(base)
    b["id"] = "T-B"
    b["derivation"] = {"parents": ["T-A"]}
    st, fs = Registry({"T-A": a, "T-B": b}).validate("T-A")
    ck("a cycle is reported as a cycle, not as recursion",
       (st, any(f.code == "PARENT_CYCLE" for f in fs)), (INVALID, True))

    reg2 = Registry({base["id"]: base, "T-CHILD": child2})
    ck("the load path walks upward",
       [r[1] for r in reg2.path("T-CHILD")], ["T-CHILD", "T-OK"])
    ck("an unresolved parent shows in the path",
       reg2.path("T-CHILD")[-1][2] != "UNRESOLVED", True)

    on = datetime.date(2026, 8, 25)
    ck("a derived future check is CURRENT",
       Registry({base["id"]: base}).due(on)[0][4], "CURRENT")
    past = copy.deepcopy(base)
    past["clock"] = copy.deepcopy(base["clock"])
    past["clock"]["measured_on"] = "2020-01-01"
    ck("a derived past check is DUE",
       Registry({"T-OK": past}).due(on)[0][4], "DUE")
    nod = copy.deepcopy(base)
    nod["clock"] = nomeas
    ck("an underivable clock reports no date, never a default",
       Registry({"T-OK": nod}).due(on)[0][1:4],
       (UNDERIVABLE, "-", "-"))
    ck("an empty registry refuses rather than printing an empty table",
       main(["record.py", "due", os.path.join(HERE, "no_such_dir")]), 2)
    ck("--on's value is not read as a directory",
       main(["record.py", "due", "--on", "2026-08-25"]), 0)

    # The hedge screen, both directions and against substring bleed.
    ck("a hedge-free assertion is clean", hedges_in(
        "The reader resolved 825 of 825 formula cells."), [])
    ck("'maybe' style hedges are caught",
       bool(hedges_in("This may hold")), True)
    ck("'mayor' is not 'may'", hedges_in("The mayor signed it"), [])
    ck("'somewhere' is not 'some'", hedges_in("somewhere"), [])
    ck("'abouts' is not 'about'", hedges_in("thereabouts"), [])

    # The reported constraint: the tool reports structure and does not
    # label a record as wrong. Screened over the emitted report, with the
    # same word list the detector uses.
    rep = render_validate(Registry({base["id"]: base}))
    ck("the emitted report carries no screened word",
       no_severity.check(rep)[0], True)
    ck("and the screen would fire if it drifted",
       no_severity.check(rep + "\nthis record is wrong")[0], False)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


# ------------------------------------------------------------- cli

USAGE = """usage:
  record.py validate [DIR]
  record.py path CLAIM_ID [DIR]
  record.py due [DIR] [--on YYYY-MM-DD]
  record.py --selftest"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print(USAGE)
        return 2
    cmd = argv[1]
    # The value after a flag is not a positional. Without this, `due
    # --on 2026-08-25` read the date as the records directory, loaded
    # nothing, and printed an empty table with rc 0 -- a report whose
    # denominator is zero rendered as though it had one.
    rest, skip = [], False
    for a in argv[2:]:
        if skip:
            skip = False
            continue
        if a.startswith("--"):
            skip = a in ("--on",)
            continue
        rest.append(a)
    if cmd == "validate":
        reg = Registry.load(rest[0] if rest else None)
        if not reg.records:
            sys.stderr.write("no records found in %s\n"
                             % (rest[0] if rest else RECORDS))
            return 2
        out = render_validate(reg)
        print(out)
        clean, _h = no_severity.check(out)
        if not clean:
            sys.stderr.write("\n" + no_severity.report(out, "emitted report")
                             + "\n")
            return 1
        return 0
    if cmd == "path":
        if not rest:
            print(USAGE)
            return 2
        reg = Registry.load(rest[1] if len(rest) > 1 else None)
        for depth, cid, note in reg.path(rest[0]):
            print("%s%s  %s" % ("  " * depth, cid, note))
        return 0
    if cmd == "due":
        on = datetime.date.today()
        if "--on" in argv:
            on = datetime.date.fromisoformat(argv[argv.index("--on") + 1])
        reg = Registry.load(rest[0] if rest else None)
        if not reg.records:
            sys.stderr.write("no records found in %s\n"
                             % (rest[0] if rest else RECORDS))
            return 2
        print("next-check status on %s" % on.isoformat())
        print("shelf life = time constant / |coupling|, both derived")
        print(table(["claim", "clock", "shelf_yr", "next_check", "state"],
                    reg.due(on)))
        return 0
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
