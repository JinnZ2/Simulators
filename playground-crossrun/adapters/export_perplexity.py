"""Export the study-aperture playground's own cases, and its own reading of each.

Runs inside study-aperture/experimental (the `playground` package there).
Nothing is retyped: each planted defect and control is executed as shipped,
and the arguments it hands to its own gate are captured on the way in by
wrapping the gate function in the defect module's namespace. The wrapper
calls the original and records; it changes no result.

Output: out/perplexity_cases.json
"""
import dataclasses, enum, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

sys.path.insert(0, common.SA_EXP)
os.chdir(common.SA_EXP)

from playground.validation import planted_defects as PD  # noqa: E402
from playground.validation import system_track_defects as SD  # noqa: E402
from playground.validation import determination_track_defects as DD  # noqa: E402
from playground.failures import Axis, FailureRecord  # noqa: E402

BUF = []


def ser(o):
    if isinstance(o, enum.Enum):
        return o.value
    if dataclasses.is_dataclass(o) and not isinstance(o, type):
        d = {f.name: ser(getattr(o, f.name)) for f in dataclasses.fields(o)}
        d["_type"] = type(o).__name__
        return d
    if isinstance(o, dict):
        return {str(ser(k)): ser(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set, frozenset)):
        return [ser(v) for v in o]
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    if callable(o) and not hasattr(o, "__dict__"):
        return "<callable>"
    if hasattr(o, "__dict__"):
        d = {k: ser(v) for k, v in vars(o).items() if not k.startswith("_")}
        d["_type"] = type(o).__name__
        return d
    return repr(o)


def wrap(mod, name):
    orig = getattr(mod, name)

    def w(*a, **k):
        out = orig(*a, **k)
        BUF.append(dict(fn=name, module=mod.__name__.split(".")[-1], args=ser(list(a)), kwargs=ser(k)))
        return out
    setattr(mod, name, w)


for _m, _names in ((PD, ("l0_closure_gate", "validate_known_answers", "validate_nulls")),
                   (SD, ("return_test", "classify_continuity", "compare_configurations")),
                   (DD, ("establish_sensitivity", "record_non_detection", "claim_absence",
                         "stale_reliance", "check_expiry", "reevaluate"))):
    for _n in _names:
        wrap(_m, _n)


def reading(rec):
    if not isinstance(rec, FailureRecord):
        rec = rec.record
    return dict(axes={a.value: rec.status_for(a).value for a in Axis},
                codes=[dict(axis=f.axis.value, severity=f.severity.value, code=f.code) for f in rec.findings])


def defects():
    rows = []
    for group, defs in (("L0+harness", PD.DEFECTS), ("system-track", SD.SYSTEM_TRACK_DEFECTS),
                        ("determination-track", DD.DETERMINATION_TRACK_DEFECTS)):
        for d in defs:
            BUF.clear()
            rec = d.exercise()
            rows.append(dict(case_id="P-DEF:" + d.defect_id, group=group, kind="planted_defect",
                             description=d.description,
                             expected=[[a.value, s.value] for a, s in d.expected],
                             must_be_untested=[a.value for a in d.must_be_untested],
                             calls=list(BUF), perplexity=reading(rec)))
    return rows


def controls():
    """Controls run in sequence inside one function each; ControlCheck is wrapped
    so the calls made since the previous control are attached to the control they built."""
    rows = []
    for mod, fn in ((PD, "run_control_cases"), (SD, "run_system_track_controls"),
                    (DD, "run_determination_track_controls")):
        orig = mod.ControlCheck

        def cc(*a, _orig=orig, **k):
            c = _orig(*a, **k)
            rows.append(dict(case_id="P-CTRL:" + c.control_id, group=fn, kind="control",
                             description=c.description, calls=list(BUF),
                             perplexity=dict(passed=c.passed, detail=c.detail)))
            BUF.clear()
            return c
        mod.ControlCheck = cc
        BUF.clear()
        getattr(mod, fn)()
        mod.ControlCheck = orig
    return rows


def audits():
    from playground.audits import denominator_process as den, distribution_mean_process as dm
    from playground.equations import measurand_example as me
    rows = []
    for tag, mod in (("P-DEN", den), ("P-MEAN", dm)):
        rep = mod.inspect_process()
        for k, c in rep["cases"].items():
            keep = {kk: c[kk] for kk in ("audited_comparison", "conclusion", "usable_for_selected_target_in_this_case",
                                         "audited_point_difference", "source_moments", "source", "question",
                                         "interchangeability_established", "census") if kk in c}
            rows.append(dict(case_id="%s:%s" % (tag, k), group=mod.__name__.split(".")[-1], kind="audit_case",
                             data=keep, perplexity=dict(axes=c["axis_statuses"])))
    rep = me.inspect_identity()
    for k, c in rep["cases"].items():
        rows.append(dict(case_id="P-MEAS:" + k, group="measurand", kind="audit_case",
                         data=dict(state=c["state"], identity=c["identity"], differing_fields=c["differing_fields"],
                                   previous_output=(c["previous"]["outputs"] or [None])[0],
                                   replacement_output=(c["replacement"]["outputs"] or [None])[0]),
                         perplexity=dict(axes=c["axis_statuses"], state=c["state"])))
    return rows


def cross_system():
    """Two of the shipped cross-class transfer guards, run as shipped. Their asserted
    readings are the native reading of the case; ran records whether they held here."""
    import unittest
    from playground.validation import cross_system as cs, test_cross_system as tcs
    rows = []
    for name, axes, what in (
            ("test_equation_diagnostics_never_transfer_between_classes",
             dict(determination="failed", instrument="untested"),
             "diagnostics (known-answer/null) earned in one system class presented in another"),
            ("test_calibration_cannot_transfer_even_between_dimensionless_surrogates",
             dict(determination="indeterminate", physical="untested"),
             "sensitivity calibration from one class used for an absence claim in another")):
        res = unittest.TextTestRunner(stream=open(os.devnull, "w")).run(
            unittest.defaultTestLoader.loadTestsFromName(name, tcs.CrossSystemTests)
            if hasattr(tcs, "CrossSystemTests") else unittest.defaultTestLoader.loadTestsFromName(
                [n for n in dir(tcs) if n.endswith("Tests") and hasattr(getattr(tcs, n), name)][0] + "." + name, tcs))
        rows.append(dict(case_id="P-XSYS:" + name[5:], group="cross_system", kind="guard_test",
                         description=what, data=dict(classes=[f.system_class for f in cs.fixtures()],
                                                     permutations=20, test=name),
                         perplexity=dict(axes=axes, ran="PASS" if res.wasSuccessful() else "FAIL")))
    return rows


if __name__ == "__main__":
    common.dump("perplexity_cases.json", dict(
        source="study-aperture/experimental/playground", rev=common.git_rev(common.SA_ROOT),
        cases=defects() + controls() + audits() + cross_system()))
    print("exported", len(common.load("perplexity_cases.json")["cases"]), "study-aperture cases")
