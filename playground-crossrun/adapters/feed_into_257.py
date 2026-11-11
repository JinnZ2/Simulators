"""Feed the study-aperture playground's cases into #257, through #257's own public objects.

Runs with relational-playground/ on sys.path. Reads out/perplexity_cases.json,
writes out/p_into_257.json. Same row shape as feed_into_perplexity.py: what
#257 did (`r`), whether the adapter could express the case, whether the
concept that decides the classification has a slot on this side, and every
translation choice named in `mapping`.

The study-aperture instruments are rebuilt here from their captured
parameters (slope/intercept, threshold/offset): those are two-line formulas
and the parameters are data in the export, not logic carried across.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

sys.path.insert(0, common.R257)
from playground import l0, known_answer_gate as gate, anchor  # noqa: E402
from playground.equations import base as eq  # noqa: E402
from playground.equations.base import ModelOutput, from_transfers  # noqa: E402
from playground.uncertainty import Value  # noqa: E402
from playground.continuity import ContinuityMatrix  # noqa: E402
from playground.analysis import coincidence  # noqa: E402

eq.load_all()


def ledger_of(case):
    return case["calls"][0]["args"][0]


def feed_l0(case):
    """BoundaryAccounting -> #257 budget audit. Perplexity's per-account tolerance enters as
    sigma_meas = tol/2, so #257's NOISE band (k_sigma 2) equals that tolerance [declared]."""
    acc = ledger_of(case)
    a = acc["accounts"][0]
    pool = "E"
    b = l0.Budget("energy", pools=[pool], sigma_meas=a["tolerance"] / 2.0)
    budgets = l0.declare(energy=b, **{n: l0.Budget(n, void_reason="not in this case") for n in l0.BUDGETS if n != "energy"})
    s0 = {pool: a["initial"]}
    s1 = {pool: a["final"]}
    for e in a["exchanges"]:
        k = "_%s|energy|%s" % ("in" if e["direction"] == "inflow" else "out", e["label"])
        s1[k] = s1.get(k, 0.0) + e["magnitude"]
    rows, _ = l0.audit(budgets, s0, s1)
    status, why = l0.run_status(rows)
    live = [r for r in rows if r["verdict"] != "VOID"][0]
    unregistered = sorted(set(acc["registered_interventions"]) - {e["registered_by"] for e in a["exchanges"]})
    return dict(r=dict(verdict=live["verdict"], misclosure=live["misclosure"], status=status, status_reason=why),
                adapter_ok=True,
                mapping=["account tolerance %g -> sigma_meas %g (NOISE band = 2 sigma)" % (a["tolerance"], a["tolerance"] / 2),
                         "pool 'E' carries the energy account; each Exchange -> one boundary accumulator"],
                dropped_on_translation=dict(registered_interventions=acc["registered_interventions"],
                                            unregistered_interventions=unregistered,
                                            declared_complete=acc["declared_complete"],
                                            provenances=sorted({e["provenance"] for e in a["exchanges"]} |
                                                               {a["initial_provenance"], a["final_provenance"]})),
                slot=False,
                slot_note="#257's L0 has no intervention registry, no declared-complete flag and no value provenance; "
                          "these decide Perplexity's axis and are dropped on the way in (listed above)")


_N = [0]
Y0_ARMS = (0.0, 1.0, -1.0)
Y0_PRIMARY = 0.0


def instrument_model(inst, y0):
    """Register a one-step #257 model whose step writes the instrument's reading into y.
    The reading enters as a boundary transfer so the L0 table carries it and the gate's
    leak/coef plants have a transfer to act on."""
    _N[0] += 1
    name = "xrun_%s_y%g_%d" % (inst["instrument_id"], y0, _N[0])

    def fn(state, env, rel, ctl, p):
        target = p["slope"] * p["x"] + p["intercept"]
        tr = [("reading", None, "y", target - state["y"])]
        return ModelOutput(from_transfers(tr, ["y"]), transfers=tr)
    eq.register(name, "xrun-instrument", "0", fn, "step", requires=("slope", "intercept", "x"))
    return name


def certify_instrument(inst, ka_cases, y0):
    name = instrument_model(inst, y0)
    it = iter(range(10 ** 6))

    def builder(rng):
        c = ka_cases[next(it) % len(ka_cases)]
        x = dict(c["inputs"])["x"]
        return dict(model=name, params=dict(slope=inst["slope"], intercept=inst["intercept"], x=x),
                    initial=dict(y=y0), t_end=1.0, dt=1.0, live=dict(mass=["y"]), output="y",
                    expected=dict(c["expected"])["y"], tol=dict(c["tolerances"])["y"])
    if ka_cases:
        gate.add_builder(name, builder)
    t = gate.certify(name, gate.default_make_config)
    return name, t


def feed_ka(case):
    call = [c for c in case["calls"] if c["fn"] == "validate_known_answers"][0]
    inst, cases = call["args"][0], call["args"][1]
    arms = {}
    for y0 in Y0_ARMS:
        _, t = certify_instrument(inst, cases, y0)
        arms["y0=%g" % y0] = dict(trusted=t["trusted"], harness=t.get("harness"), evidence=t["evidence"], FP=t.get("FP"), TP=t.get("TP"))
    return dict(r=arms["y0=%g" % Y0_PRIMARY], r_arms=arms,
                adapter_ok=True,
                mapping=["LinearInstrument(slope, intercept) -> one-step #257 model writing slope*x+intercept into y",
                         "each Perplexity known-answer case -> a #257 builder draw (cycled; the gate always takes 12)",
                         "the gate then plants leak/coef defects on top -- planted on the instrument, not on the case",
                         "[CHOICE] a static instrument has no start state in #257's dynamic-model gate, so the adapter "
                         "supplies one; y0 in {0, 1, -1} is run and y0=0 is primary. The gate's 'coef' plant scales the "
                         "transfer by 1.1, so it moves nothing on any case whose required flux (answer - y0) is zero: "
                         "y0=0 blinds it on the x=0 case, y0=1 on the x=1 case, y0=-1 on none. The gate verdict on a clean "
                         "instrument is therefore a property of this adapter choice -- coded ADAPTER, not read as a result"],
                slot=True, slot_note=None)


def feed_null(case):
    call = [c for c in case["calls"] if c["fn"] == "validate_nulls"][0]
    inst, nulls = call["args"][0], call["args"][1]
    det = lambda c, i=inst: abs(i["slope"] * dict(c["inputs"])["x"] + i["intercept"] - dict(c["expected_outputs"])["y"]) \
        > dict(c["tolerances"])["y"] if "expected_outputs" in c else None
    keys = sorted(nulls[0]) if nulls else []
    try:
        gate.add_tool("xrun_null_%s" % inst["instrument_id"], nulls, [], det)
        t = gate.certify_tool("xrun_null_%s" % inst["instrument_id"])
        r = dict(form="RECORD", trusted=t["trusted"], harness=t["harness"])
    except ZeroDivisionError as e:
        r = dict(form="CRASH", error="ZeroDivisionError in certify_tool: %s" % e)
    return dict(r=r, adapter_ok=True, mapping=["null cases -> certify_tool nulls; signals = [] (Perplexity's null harness has none)",
                                               "detector = |instrument(x) - stated null output| > tolerance; null case keys %s" % keys],
                slot=False, slot_note="#257's tool gate has no null-only mode: TP divides by len(signals)")


def ladder_tool(call):
    inst, rungs = call["args"][0], call["args"][1]
    thr = float(inst["threshold"]) if not isinstance(inst["threshold"], float) else inst["threshold"]

    def reading(x):
        return (x if x >= thr else 0.0) + inst["offset"]
    det = lambda c: abs(reading(dict(c["inputs"])["x"]) - dict(c["null_outputs"])["y"]) > dict(c["tolerances"])["y"]
    nulls = [c for c in rungs if not c["expected_detectable"]]
    sigs = [c for c in rungs if c["expected_detectable"]]
    name = "xrun_ladder_%s_%d" % (inst["instrument_id"], len(rungs))
    try:
        gate.add_tool(name, nulls, sigs, det)
        t = gate.certify_tool(name)
        return dict(form="RECORD", trusted=t["trusted"], harness=t["harness"], FP=t["FP"], TP=t["TP"],
                    limit="NO_SLOT (the tool gate returns FP/TP, never a detection limit)")
    except ZeroDivisionError as e:
        return dict(form="CRASH", error="ZeroDivisionError in certify_tool: %s" % e, n_nulls=len(nulls), n_signals=len(sigs))


def feed_sensitivity(case):
    call = [c for c in case["calls"] if c["fn"] == "establish_sensitivity"][0]
    return dict(r=ladder_tool(call), adapter_ok=True,
                mapping=["ladder rungs expected undetectable -> nulls, expected detectable -> planted signals",
                         "detector = |reading - null output| > tolerance"],
                slot=True, slot_note="#257 grades the detector; it records no limit, no conditions, no effect size")


def feed_nondetection(case):
    """#257's only home for a non-detection is Value(status=ABSENT_AT_SENSITIVITY, sensitivity=...)."""
    nd = [c for c in case["calls"] if c["fn"] == "record_non_detection"][0]
    sens = nd["args"][1]
    limit = sens.get("detection_limit") if isinstance(sens, dict) else None
    try:
        v = Value(None, "ABSENT_AT_SENSITIVITY", "xrun: %s" % case["case_id"], sensitivity=limit)
        r = dict(form="RECORD", accepted=True, label=v.label())
    except ValueError as e:
        r = dict(form="RAISE", accepted=False, refused=str(e)[:160])
    obs = nd["args"][0]
    return dict(r=r, adapter_ok=True,
                mapping=["established detection limit -> Value.sensitivity (None when no sensitivity was established)"],
                dropped_on_translation=dict(effect_size_of_interest=obs.get("effect_size_of_interest"), conditions=obs.get("conditions")),
                slot=False if "below" in case["case_id"] or "mismatch" in case["case_id"] else True,
                slot_note="ABSENT_AT_SENSITIVITY holds one number; no effect size of interest and no scope conditions to compare it with")


def feed_stale(case):
    return dict(r=None, adapter_ok=True, mapping=[], slot=False,
                slot_note="UNKNOWN carries a free-text expiry_condition; there is no expired state and no record of a "
                          "determination resting on an UNKNOWN, so stale reliance cannot be expressed")


def spec_of(case):
    return [c for c in case["calls"] if c["fn"] == "return_test"][0]["args"][0]


def feed_return(case):
    """ReturnTestSpec -> anchor.return_diff. The anchor dict carries only what return_diff reads."""
    sp = spec_of(case)
    a = dict(id=sp["anchor"]["label"], status="anchor", final_state=dict(sp["anchor"]["quantities"]))
    branch = dict(run_id="xrun-return", status="COMPLETE", l0_budgets=[],
                  observations_and_predictions=dict(final_state={q["quantity"]: q["returned"] for q in sp["returned"]}))
    d = anchor.return_diff(a, branch, "return to anchor")
    nc = [row["variable"] for row in d["rows"] if row["delta"] == "NOT COMPARABLE"]
    tol_extra = sorted(set(dict(sp["tolerances"])) - set(a["final_state"]) - set(branch["observations_and_predictions"]["final_state"]))
    return dict(r=dict(rows=[(row["variable"], row["delta"]) for row in d["rows"]], not_comparable=nc),
                adapter_ok=True,
                mapping=["anchor quantities -> anchor final_state; returned values -> branch final_state"],
                dropped_on_translation=dict(expected_return=sp["expected_return"], tolerances=sp["tolerances"],
                                            provenances=sorted({q["provenance"] for q in sp["returned"]}),
                                            tolerances_naming_no_quantity=tol_extra),
                slot=None, slot_note=None)


def feed_continuity(case):
    """Return test + configuration comparison -> ContinuityMatrix.read over two states.
    The system criterion is SUPPLIED BY THE ADAPTER (PROPOSED): 'every anchored quantity within
    its declared tolerance of the anchor'. If any anchored quantity has no tolerance the
    criterion is not declarable, so the matrix is left UNDECLARED rather than guessed."""
    sp = spec_of(case)
    anc = dict(sp["anchor"]["quantities"])
    tol = dict(sp["tolerances"])
    ret = {q["quantity"]: q["returned"] for q in sp["returned"]}
    cc = [c for c in case["calls"] if c["fn"] == "compare_configurations"]
    cfg0 = tuple(sorted(map(tuple, cc[0]["args"][0]["entries"]))) if cc else ("persisted",)
    cfg1 = tuple(sorted(map(tuple, cc[0]["args"][1]["entries"]))) if cc else ("persisted",)
    declarable = all(k in tol for k in anc) and all(k in ret for k in anc)
    if declarable:
        crit = lambda s: all(abs(s["q"][k] - anc[k]) <= tol[k] for k in anc)
        m = ContinuityMatrix(crit, lambda s: s["cfg"], basis="xrun: within declared tolerance of the anchor")
    else:
        m = ContinuityMatrix()
    out = m.read([0, 1], [dict(q=anc, cfg=cfg0), dict(q=ret, cfg=cfg1)])
    return dict(r=dict(system_continuity=out["system_continuity"], configuration_continuity=out["configuration_continuity"],
                       recovery_and_reorganization=out["recovery_and_reorganization"]),
                adapter_ok=True,
                mapping=["system_criterion supplied by the adapter: all anchored quantities within tolerance (PROPOSED)",
                         "configuration_of = sorted configuration entries",
                         "criterion left UNDECLARED when any anchored quantity lacks a tolerance or an observation"],
                slot=True, slot_note="#257 splits system continuity and configuration continuity, as Perplexity does; "
                                     "its system criterion is identity ('still the system'), Perplexity's is return-to-anchor")


def feed_measurand(case):
    d = case["data"]
    if not d["previous_output"] or not d["replacement_output"]:
        return dict(r=None, adapter_ok=False, adapter_note="one run produced no output (blocked before calculation); nothing to compare",
                    mapping=[], slot=False, slot_note="no measurand identity in #257")
    po, ro = d["previous_output"]["value"], d["replacement_output"]["value"]
    rows = [dict(model="previous", family="xrun-a", output=po), dict(model="replacement", family="xrun-b", output=ro)]
    res = coincidence.on_agreement(rows, window=1e-9, declared_at="xrun: fixed before reading, exact-equality window")
    return dict(r=dict(state=res["state"], cards=len(res.get("cards", [])), readings=res.get("readings")),
                adapter_ok=True,
                mapping=["two runs -> two families (the runs are different equation revisions)",
                         "agreement window 1e-9 declared before reading: exact agreement only"],
                dropped_on_translation=dict(differing_fields=d["differing_fields"], identity=d["identity"]),
                slot=False, slot_note="no measurand identity: two outputs with one name and one unit are compared; agreement opens a "
                                      "card to be explained instead of voiding the comparison")


def feed_mean(case):
    """Distribution -> one Value with an interval; #257 propagates by interval corners."""
    from playground.uncertainty import UncertaintyMatrix
    src = case["data"].get("source") or {}
    atoms = src.get("atoms") or []
    vals = [a["value"] for a in atoms]
    ws = [a["weight"] for a in atoms]
    if not atoms or any(not isinstance(v, (int, float)) for v in vals):
        return dict(r=None, adapter_ok=False, adapter_note="source atoms absent or non-numeric in export", mapping=[], slot=False, slot_note=None)
    lo, hi = min(vals), max(vals)
    if any(w is None for w in ws) or sum(w for w in ws if w) == 0:
        return dict(r=None, adapter_ok=False, adapter_note="weights unknown or zero: no mean to place in a Value",
                    mapping=[], slot=False, slot_note="#257 has no weighted-distribution object")
    mean = sum(v * w for v, w in zip(vals, ws)) / float(sum(ws))
    m = UncertaintyMatrix(dict(X=Value(mean, "ESTIMATED", "xrun: weighted mean", interval=(lo, hi))))
    p = m.propagate(lambda d: d["X"] ** 2, ["X"])
    true_target = sum(v * v * w for v, w in zip(vals, ws)) / float(sum(ws))
    return dict(r=dict(point_at_mean=mean ** 2, interval=(p["low"], p["high"]), true_second_moment=true_target,
                       true_inside_interval=p["low"] <= true_target <= p["high"], flags_information_loss=False),
                adapter_ok=True,
                mapping=["weighted distribution -> Value(mean, interval=(min, max)); target taken as X^2 for every case"],
                slot=False, slot_note="no selected-target / information-loss record; corner propagation reports a range")


def feed_xsys(case):
    """Trust in #257 is keyed by model name alone: certify a model once, read it from any system."""
    t = gate.certify("linear", gate.default_make_config)
    from playground.system import SystemDefinition, FIELDS as SF
    other = SystemDefinition("some-other-class", **{f: "UNDECLARED" for f in SF})
    return dict(r=dict(trust_in_other_system=gate.trust("linear")["trusted"], keyed_by="model name",
                       other_system=other.as_dict().get("name", "some-other-class")),
                adapter_ok=True, mapping=["certify 'linear' once; ask gate.trust('linear') with no system argument (there is none)"],
                slot=False, slot_note="trust has no context/system key; calibration and diagnostics carry to every system")


def feed_den(case):
    return dict(r=None, adapter_ok=True, mapping=[], slot=False,
                slot_note="no cohort-member object and no denominator binding; a rate is a number with an interval")


def feed(case):
    cid = case["case_id"]
    fns = [c["fn"] for c in case.get("calls", [])]
    if cid.startswith("P-MEAS:"):
        return feed_measurand(case)
    if cid.startswith("P-MEAN:"):
        return feed_mean(case)
    if cid.startswith("P-DEN:"):
        return feed_den(case)
    if cid.startswith("P-XSYS:"):
        return feed_xsys(case)
    if "classify_continuity" in fns:
        return feed_continuity(case)
    if "return_test" in fns:
        return feed_return(case)
    if fns == ["l0_closure_gate"]:
        return feed_l0(case)
    if "validate_known_answers" in fns:
        r = feed_ka(case)
        if "validate_nulls" in fns:
            r["r_null"] = feed_null(case)["r"]
        return r
    if "validate_nulls" in fns:
        return feed_null(case)
    if "record_non_detection" in fns:
        return feed_nondetection(case)
    if "establish_sensitivity" in fns:
        return feed_sensitivity(case)
    if "stale_reliance" in fns or "check_expiry" in fns or "reevaluate" in fns:
        return feed_stale(case)
    raise KeyError(cid)


if __name__ == "__main__":
    src = common.load("perplexity_cases.json")
    rows = []
    for c in src["cases"]:
        r = feed(c)
        r.update(case_id=c["case_id"], group=c["group"], kind=c["kind"], description=c.get("description", ""), native=c["perplexity"])
        rows.append(r)
    common.dump("p_into_257.json", dict(direction="study-aperture cases -> #257", rev=common.git_rev(common.SIM_ROOT), rows=rows))
    print("fed", len(rows), "study-aperture cases into #257")
