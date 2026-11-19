# Excerpt of P1/cplay/axes.py, original line numbers kept (lines 1-150 of 150). Lines not shown are omitted, not empty.

    1| """M3: failure axes, statuses, COVERAGE, and the #257 mapping (COMBINED_SPEC section 2).
    2| 
    3| Three failure axes (PHYSICAL, INSTRUMENT, DETERMINATION). APPLICABILITY is a field on no
    4| failure axis. COVERAGE is a list of entries beside the axes and never feeds severity (R-A2).
    5| 
    6| Field restrictions taken from the spec text:
    7|   CRASHED         INSTRUMENT only        ("CRASHED stays an INSTRUMENT status", R-A2)
    8|   OUTSIDE_DOMAIN  APPLICABILITY only     (status table, Q11)
    9|   FAILED          failure axes only      (APPLICABILITY "is not a failure axis", Q11)
   10|   CLOSED_WITHIN   PHYSICAL. On INSTRUMENT / DETERMINATION reading() returns a VOID token, not a
   11|                   Reading: the spec maps CLOSED_WITHIN to PHYSICAL only and says nothing of the
   12|                   other two, so it is neither allowed nor refused (follow-up item 1).
   13| 
   14| Decided (9c item 1): no composite severity across axes; severity() is the per-axis vector.
   15| Held VOID: CLOSED_WITHIN on INSTRUMENT or DETERMINATION.
   16| """
   17| from collections import namedtuple
   18| 
   19| from . import tokens as T
   20| 
   21| AXES = ("PHYSICAL", "INSTRUMENT", "DETERMINATION")
   22| FIELDS = AXES + ("APPLICABILITY",)
   23| STATUSES = ("OK", "FAILED", "INDETERMINATE", "UNTESTED", "CRASHED", "CLOSED_WITHIN", "OUTSIDE_DOMAIN")
   24| COVERAGE_KINDS = ("UNKNOWN", "INFO", "GAP_INSTRUMENT_CRASH")   # P3 unified_audit.py @[commit] l.101
   25| 
   26| CLOSED_WITHIN_OFF_PHYSICAL = ("section 2 maps CLOSED_WITHIN to PHYSICAL only; its meaning on "
   27|                               "INSTRUMENT / DETERMINATION is not defined")
   28| 
   29| COMPOSITE_SEVERITY = T.Token("REFUSED", "decided: no composite; severity() reports the per-axis vector "
   30|                              "(9c item 1; pin P1-p3-unknown-axis, P3 [commit] unified_audit.py: UNKNOWN on its own axis; R-A2)")
   31| 
   32| 
   33| class AxisError(ValueError):
   34|     pass
   35| 
   36| 
   37| def _filled(x):
   38|     return isinstance(x, str) and x.strip() != ""
   39| 
   40| 
   41| Reading = namedtuple("Reading", "field status reason sigma basis exception path bound")
   42| 
   43| 
   44| def reading(field, status, reason=None, sigma=None, basis=None, exception=None, path=None, bound=None):
   45|     if field not in FIELDS:
   46|         raise AxisError("unknown field %r; COVERAGE is not an axis" % (field,))
   47|     if status not in STATUSES:
   48|         raise AxisError("unknown status %r" % (status,))
   49|     if status == "CRASHED" and field != "INSTRUMENT":
   50|         raise AxisError("CRASHED is an INSTRUMENT status (R-A2)")
   51|     if status == "OUTSIDE_DOMAIN" and field != "APPLICABILITY":
   52|         raise AxisError("OUTSIDE_DOMAIN is APPLICABILITY only (Q11)")
   53|     if status == "CLOSED_WITHIN" and field in ("INSTRUMENT", "DETERMINATION"):
   54|         return T.Token("VOID", CLOSED_WITHIN_OFF_PHYSICAL)
   55|     if field == "APPLICABILITY" and status in ("FAILED", "CRASHED", "CLOSED_WITHIN"):
   56|         raise AxisError("APPLICABILITY is not a failure axis (Q11)")
   57|     if status in ("FAILED", "INDETERMINATE", "UNTESTED") and not _filled(reason):
   58|         raise AxisError("%s needs a reason" % status)
   59|     if status == "CRASHED" and not (_filled(exception) and _filled(path)):
   60|         raise AxisError("CRASHED needs exception and path (Q3)")
   61|     if status == "CLOSED_WITHIN":
   62|         if not isinstance(sigma, (int, float)) or isinstance(sigma, bool) or sigma < 0 or not _filled(basis):
   63|             raise AxisError("CLOSED_WITHIN needs a numeric sigma >= 0 and a basis (Q2)")
   64|     if status == "OUTSIDE_DOMAIN" and not _filled(bound):
   65|         raise AxisError("OUTSIDE_DOMAIN needs the bound (Q11)")
   66|     return Reading(field, status, reason, sigma, basis, exception, path, bound)
   67| 
   68| 
   69| class CoverageEntry(namedtuple("CoverageEntry", "kind module input reason missing_path expiry_condition")):
   70|     """All six P3 fields are keyword-required; None is accepted as a passed value, never filled in."""
   71|     __slots__ = ()
   72| 
   73|     def __new__(cls, *, kind, module, input, reason, missing_path, expiry_condition):
   74|         if kind not in COVERAGE_KINDS:
   75|             raise AxisError("coverage kind %r not in %r" % (kind, COVERAGE_KINDS))
   76|         if not (_filled(module) and _filled(reason)):
   77|             raise AxisError("coverage entry needs module and reason")
   78|         return super().__new__(cls, kind, module, input, reason, missing_path, expiry_condition)
   79| 
   80| 
   81| def crash(exc, *, path, module, inputs, expiry_condition):
   82|     """R-A2: a crash is a record -- an INSTRUMENT reading plus a coverage entry, never no row."""
   83|     name = type(exc).__name__
   84|     rd = reading("INSTRUMENT", "CRASHED", reason=str(exc) or name, exception=name, path=path)
   85|     cov = CoverageEntry(kind="GAP_INSTRUMENT_CRASH", module=module, input=inputs,
   86|                         reason="%s: %s" % (name, exc), missing_path=path,
   87|                         expiry_condition=expiry_condition)
   88|     return rd, cov
   89| 
   90| 
   91| class Record(object):
   92|     def __init__(self, readings, coverage):
   93|         for f, rd in readings.items():
   94|             if not isinstance(rd, Reading) or rd.field != f:
   95|                 raise AxisError("reading for %r must be a Reading on that field" % (f,))
   96|         for c in coverage:
   97|             if not isinstance(c, CoverageEntry):
   98|                 raise AxisError("coverage holds CoverageEntry objects only")
   99|         crashed = [rd for rd in readings.values() if rd.status == "CRASHED"]
  100|         gaps = [c for c in coverage if c.kind == "GAP_INSTRUMENT_CRASH"]
  101|         if crashed and not gaps:
  102|             raise AxisError("a CRASHED reading needs its coverage entry (R-A2)")
  103|         self._readings = dict(readings)
  104|         self.coverage = tuple(coverage)
  105| 
  106|     def get(self, field):
  107|         if field not in FIELDS:
  108|             raise AxisError("unknown field %r" % (field,))
  109|         return self._readings.get(field) or reading(field, "UNTESTED", reason="NO_GATE_READ")  # R-A3
  110| 
  111|     def severity(self):
  112|         """Per-axis status only. Reads no coverage entry and no APPLICABILITY (R-A2, Q11)."""
  113|         return {f: self.get(f).status for f in AXES}
  114| 
  115| 
  116| def map_257(source, **cond):
  117|     """Every reason #257 can emit, mapped per section 2. An unlisted source is refused."""
  118|     if source == "l0.did_not_close":
  119|         if cond.get("declared_complete") is True:                         # R-A1: literal True only
  120|             return reading("PHYSICAL", "FAILED", reason="did not close; ledger declared complete")
  121|         return reading("DETERMINATION", "FAILED", reason="did not close; ledger not declared complete")
  122|     if source == "l0.no_live_budget":
  123|         return reading("DETERMINATION", "UNTESTED", reason="NO_LIVE_BUDGET")
  124|     if source == "l0.noise":
  125|         return reading("PHYSICAL", "CLOSED_WITHIN", reason="misclosure within k sigma",
  126|                        sigma=cond.get("sigma"), basis=cond.get("basis"))
  127|     if source == "certify.untrusted":
  128|         return reading("INSTRUMENT", "FAILED", reason="UNTRUSTED: harness misses plants")
  129|     if source == "certify_tool.raise":
  130|         raise AxisError("a tool raise is a crash record: call crash(), which carries the coverage entry")
  131|     if source == "trust.no_cases":
  132|         return reading("INSTRUMENT", "UNTESTED", reason="KA_NO_CASES")
  133|     if source == "known_answer.circular":
  134|         return reading("INSTRUMENT", "UNTESTED", reason="CIRCULAR_KNOWN_ANSWER")
  135|     if source == "bound.hit":
  136|         return reading("APPLICABILITY", "OUTSIDE_DOMAIN", reason="input beyond a declared bound",
  137|                        bound=cond.get("bound"))
  138|     raise AxisError("no mapping row for #257 source %r (section 2)" % (source,))
  139| 
  140| 
  141| Relabeled = namedtuple("Relabeled", "step1_code combined")
  142| 
  143| 
  144| def relabel(step1_code, combined):
  145|     """R-A5: the step-1 code is kept; the COMBINED reading sits beside it."""
  146|     if not _filled(step1_code):
  147|         raise AxisError("step-1 code required; rows are not relabelled in place")
  148|     if not isinstance(combined, Reading):
  149|         raise AxisError("combined column takes a Reading")
  150|     return Relabeled(step1_code, combined)
