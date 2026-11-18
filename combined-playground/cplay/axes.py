"""M3: failure axes, statuses, COVERAGE, and the #257 mapping (COMBINED_SPEC section 2).

Three failure axes (PHYSICAL, INSTRUMENT, DETERMINATION). APPLICABILITY is a field on no
failure axis. COVERAGE is a list of entries beside the axes and never feeds severity (R-A2).

Field restrictions taken from the spec text:
  CRASHED         INSTRUMENT only        ("CRASHED stays an INSTRUMENT status", R-A2)
  OUTSIDE_DOMAIN  APPLICABILITY only     (status table, Q11)
  FAILED          failure axes only      (APPLICABILITY "is not a failure axis", Q11)
  CLOSED_WITHIN   PHYSICAL. On INSTRUMENT / DETERMINATION reading() returns a VOID token, not a
                  Reading: the spec maps CLOSED_WITHIN to PHYSICAL only and says nothing of the
                  other two, so it is neither allowed nor refused (follow-up item 1).

Not defined by the spec, and held VOID: a composite severity across axes; CLOSED_WITHIN on
INSTRUMENT or DETERMINATION.
"""
from collections import namedtuple

from . import tokens as T

AXES = ("PHYSICAL", "INSTRUMENT", "DETERMINATION")
FIELDS = AXES + ("APPLICABILITY",)
STATUSES = ("OK", "FAILED", "INDETERMINATE", "UNTESTED", "CRASHED", "CLOSED_WITHIN", "OUTSIDE_DOMAIN")
COVERAGE_KINDS = ("UNKNOWN", "INFO", "GAP_INSTRUMENT_CRASH")   # TAF unified_audit.py @16285cc l.101

CLOSED_WITHIN_OFF_PHYSICAL = ("section 2 maps CLOSED_WITHIN to PHYSICAL only; its meaning on "
                              "INSTRUMENT / DETERMINATION is not defined")

COMPOSITE_SEVERITY = T.Token("VOID", "section 2 defines per-axis status only; no rule combines axes")


class AxisError(ValueError):
    pass


def _filled(x):
    return isinstance(x, str) and x.strip() != ""


Reading = namedtuple("Reading", "field status reason sigma basis exception path bound")


def reading(field, status, reason=None, sigma=None, basis=None, exception=None, path=None, bound=None):
    if field not in FIELDS:
        raise AxisError("unknown field %r; COVERAGE is not an axis" % (field,))
    if status not in STATUSES:
        raise AxisError("unknown status %r" % (status,))
    if status == "CRASHED" and field != "INSTRUMENT":
        raise AxisError("CRASHED is an INSTRUMENT status (R-A2)")
    if status == "OUTSIDE_DOMAIN" and field != "APPLICABILITY":
        raise AxisError("OUTSIDE_DOMAIN is APPLICABILITY only (Q11)")
    if status == "CLOSED_WITHIN" and field in ("INSTRUMENT", "DETERMINATION"):
        return T.Token("VOID", CLOSED_WITHIN_OFF_PHYSICAL)
    if field == "APPLICABILITY" and status in ("FAILED", "CRASHED", "CLOSED_WITHIN"):
        raise AxisError("APPLICABILITY is not a failure axis (Q11)")
    if status in ("FAILED", "INDETERMINATE", "UNTESTED") and not _filled(reason):
        raise AxisError("%s needs a reason" % status)
    if status == "CRASHED" and not (_filled(exception) and _filled(path)):
        raise AxisError("CRASHED needs exception and path (Q3)")
    if status == "CLOSED_WITHIN":
        if not isinstance(sigma, (int, float)) or isinstance(sigma, bool) or sigma < 0 or not _filled(basis):
            raise AxisError("CLOSED_WITHIN needs a numeric sigma >= 0 and a basis (Q2)")
    if status == "OUTSIDE_DOMAIN" and not _filled(bound):
        raise AxisError("OUTSIDE_DOMAIN needs the bound (Q11)")
    return Reading(field, status, reason, sigma, basis, exception, path, bound)


class CoverageEntry(namedtuple("CoverageEntry", "kind module input reason missing_path expiry_condition")):
    """All six TAF fields are keyword-required; None is accepted as a passed value, never filled in."""
    __slots__ = ()

    def __new__(cls, *, kind, module, input, reason, missing_path, expiry_condition):
        if kind not in COVERAGE_KINDS:
            raise AxisError("coverage kind %r not in %r" % (kind, COVERAGE_KINDS))
        if not (_filled(module) and _filled(reason)):
            raise AxisError("coverage entry needs module and reason")
        return super().__new__(cls, kind, module, input, reason, missing_path, expiry_condition)


def crash(exc, *, path, module, inputs, expiry_condition):
    """R-A2: a crash is a record -- an INSTRUMENT reading plus a coverage entry, never no row."""
    name = type(exc).__name__
    rd = reading("INSTRUMENT", "CRASHED", reason=str(exc) or name, exception=name, path=path)
    cov = CoverageEntry(kind="GAP_INSTRUMENT_CRASH", module=module, input=inputs,
                        reason="%s: %s" % (name, exc), missing_path=path,
                        expiry_condition=expiry_condition)
    return rd, cov


class Record(object):
    def __init__(self, readings, coverage):
        for f, rd in readings.items():
            if not isinstance(rd, Reading) or rd.field != f:
                raise AxisError("reading for %r must be a Reading on that field" % (f,))
        for c in coverage:
            if not isinstance(c, CoverageEntry):
                raise AxisError("coverage holds CoverageEntry objects only")
        crashed = [rd for rd in readings.values() if rd.status == "CRASHED"]
        gaps = [c for c in coverage if c.kind == "GAP_INSTRUMENT_CRASH"]
        if crashed and not gaps:
            raise AxisError("a CRASHED reading needs its coverage entry (R-A2)")
        self._readings = dict(readings)
        self.coverage = tuple(coverage)

    def get(self, field):
        if field not in FIELDS:
            raise AxisError("unknown field %r" % (field,))
        return self._readings.get(field) or reading(field, "UNTESTED", reason="NO_GATE_READ")  # R-A3

    def severity(self):
        """Per-axis status only. Reads no coverage entry and no APPLICABILITY (R-A2, Q11)."""
        return {f: self.get(f).status for f in AXES}


def map_257(source, **cond):
    """Every reason #257 can emit, mapped per section 2. An unlisted source is refused."""
    if source == "l0.did_not_close":
        if cond.get("declared_complete") is True:                         # R-A1: literal True only
            return reading("PHYSICAL", "FAILED", reason="did not close; ledger declared complete")
        return reading("DETERMINATION", "FAILED", reason="did not close; ledger not declared complete")
    if source == "l0.no_live_budget":
        return reading("DETERMINATION", "UNTESTED", reason="NO_LIVE_BUDGET")
    if source == "l0.noise":
        return reading("PHYSICAL", "CLOSED_WITHIN", reason="misclosure within k sigma",
                       sigma=cond.get("sigma"), basis=cond.get("basis"))
    if source == "certify.untrusted":
        return reading("INSTRUMENT", "FAILED", reason="UNTRUSTED: harness misses plants")
    if source == "certify_tool.raise":
        raise AxisError("a tool raise is a crash record: call crash(), which carries the coverage entry")
    if source == "trust.no_cases":
        return reading("INSTRUMENT", "UNTESTED", reason="KA_NO_CASES")
    if source == "known_answer.circular":
        return reading("INSTRUMENT", "UNTESTED", reason="CIRCULAR_KNOWN_ANSWER")
    if source == "bound.hit":
        return reading("APPLICABILITY", "OUTSIDE_DOMAIN", reason="input beyond a declared bound",
                       bound=cond.get("bound"))
    raise AxisError("no mapping row for #257 source %r (section 2)" % (source,))


Relabeled = namedtuple("Relabeled", "step1_code combined")


def relabel(step1_code, combined):
    """R-A5: the step-1 code is kept; the COMBINED reading sits beside it."""
    if not _filled(step1_code):
        raise AxisError("step-1 code required; rows are not relabelled in place")
    if not isinstance(combined, Reading):
        raise AxisError("combined column takes a Reading")
    return Relabeled(step1_code, combined)
