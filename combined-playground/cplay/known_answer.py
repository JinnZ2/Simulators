"""M7: known-answer gate, CIRCULAR_KNOWN_ANSWER, plants and null harness (COMBINED_SPEC section 6;
section 8 rows 9-13).

Built: every case carries its provenance; a provenance naming a declared tested formula or model
makes the case circular, and it counts toward nothing (section 6); zero cases -> INSTRUMENT
UNTESTED (KA_NO_CASES); all-circular -> UNTESTED (CIRCULAR_KNOWN_ANSWER, sources); a raising
check -> CRASHED plus a GAP_INSTRUMENT_CRASH coverage entry (R-A2); each plant names the axis it
should hit; a null-only harness gives a record, with the TP rate None and a reason, not a crash.

Decided (9c item 8): ka_verdict() passes iff every counted case passes and every planted fault is
caught; counts reported, no threshold. Held VOID: the harness-class labels and
their FP / TP thresholds; the ladder method for a detection limit (row 15; see tokens).
Circularity is detected by the declared tested ids appearing in the provenance string; a
provenance that names its source some other way is not caught.
"""
from collections import namedtuple

from . import axes as A
from . import tokens as T


class KAError(ValueError):
    pass


def _filled(x):
    return isinstance(x, str) and x.strip() != ""


class Case(namedtuple("Case", "case_id inputs expected provenance")):
    __slots__ = ()

    def __new__(cls, *, case_id, inputs, expected, provenance):
        if not _filled(case_id) or not _filled(provenance):
            raise KAError("a known-answer case carries an id and its provenance (row 9)")
        return super().__new__(cls, case_id, inputs, expected, provenance)


def circular_source(case, tested):
    for t in tested:
        if t in case.provenance:
            return t
    return None


Result = namedtuple("Result", "reading verdict counted circular passed failed coverage")


def run_cases(cases, *, tested, check, module):
    if not tested or not all(_filled(t) for t in tested):
        raise KAError("declare the tested formula / model ids so circularity can be detected")
    if not cases:
        return Result(A.reading("INSTRUMENT", "UNTESTED", reason="KA_NO_CASES"),
                      T.Token("UNTESTED", "KA_NO_CASES"), (), (), 0, 0, ())
    counted, circular = [], []
    for c in cases:
        src = circular_source(c, tested)
        if src is not None:
            circular.append((c, src))
            continue
        try:
            ok = check(c)
            if not isinstance(ok, bool):
                raise TypeError("check returned %r, not a bool" % (ok,))
        except Exception as exc:  # R-A2: a crash is a record
            rd, cov = A.crash(exc, path="%s.check" % module, module=module,
                              inputs={"case_id": c.case_id, "inputs": c.inputs}, expiry_condition=None)
            return Result(rd, T.Token("CRASHED", "%s on case %s" % (type(exc).__name__, c.case_id)),
                          tuple(counted), tuple(circular), None, None, (cov,))
        counted.append((c, ok))
    if not counted:
        srcs = ", ".join(sorted({s for _, s in circular}))
        why = "CIRCULAR_KNOWN_ANSWER (%s)" % srcs
        return Result(A.reading("INSTRUMENT", "UNTESTED", reason=why), T.Token("UNTESTED", why),
                      (), tuple(circular), 0, 0, ())
    passed = sum(1 for _, ok in counted if ok)
    return Result(None, T.Token("UNTESTED", "pass rule (9c item 8) needs the plant harness: call ka_verdict()"),
                  tuple(counted), tuple(circular), passed, len(counted) - passed, ())


class Plant(namedtuple("Plant", "plant_id expected_axis is_null")):
    __slots__ = ()

    def __new__(cls, *, plant_id, expected_axis, is_null):
        if not _filled(plant_id) or not isinstance(is_null, bool):
            raise KAError("plant needs an id and an explicit is_null")
        if is_null and expected_axis is not None:
            raise KAError("a null plant hits no axis")
        if not is_null and expected_axis not in A.AXES:
            raise KAError("each plant names the axis it should hit (row 10)")
        return super().__new__(cls, plant_id, expected_axis, is_null)


def harness(plants, fired):
    sig = [p for p in plants if not p.is_null]
    nul = [p for p in plants if p.is_null]
    tp = sum(1 for p in sig if fired(p) is True)
    fp = sum(1 for p in nul if fired(p) is True)
    return {
        "tp": tp, "fp": fp, "n_signal": len(sig), "n_null": len(nul),
        "tp_rate": tp / len(sig) if sig else None,
        "tp_rate_reason": None if sig else "NO_SIGNAL_PLANTS",
        "fp_rate": fp / len(nul) if nul else None,
        "fp_rate_reason": None if nul else "NO_NULL_PLANTS",
        "harness_class": T.Token("VOID", "harness-class labels and thresholds not in the spec (row 12)"),
    }


def ka_verdict(result, harness_result):
    """9c item 8: pass iff every counted known-answer case passes AND every planted fault is caught.
    Counts are reported; there is no threshold. Zero cases, all-circular and crash readings pass
    through unchanged; no signal plants -> UNTESTED (nothing planted to catch)."""
    if result.reading is not None:
        return result.reading
    n_cases, n_sig, tp = len(result.counted), harness_result["n_signal"], harness_result["tp"]
    counts = "cases %d/%d, plants caught %d/%d, FP %d" % (result.passed, n_cases, tp, n_sig,
                                                         harness_result["fp"])
    if n_sig == 0:
        return A.reading("INSTRUMENT", "UNTESTED", reason="no planted faults to catch; " + counts)
    if result.passed == n_cases and tp == n_sig:
        return A.reading("INSTRUMENT", "OK", reason=counts)
    return A.reading("INSTRUMENT", "FAILED", reason=counts)
