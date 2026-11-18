"""Export relational-playground's (#257) own cases, and its own reading of each.

Runs with relational-playground/ on sys.path (the `playground` package there).
Forest run 9 and the planted leak are read from the experiment's pinned output
(experiments/model_comparison/forest_fire_regime/out/part1.json, written by
run.py); re-running run.py would rewrite #257's tracked files, which this
cross-run does not touch. The known-answer fixtures are regenerated with the
gate's own builders and seed, so the draws are the ones the gate certified on.

Output: out/r257_cases.json
"""
import json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

sys.path.insert(0, common.R257)
FOREST = os.path.join(common.R257, "experiments", "model_comparison", "forest_fire_regime")
sys.path.insert(0, FOREST)

from playground import known_answer_gate as gate, anchor  # noqa: E402
from playground.equations import base as eq  # noqa: E402
from playground.uncertainty import Value, UncertaintyMatrix  # noqa: E402
from playground.controls import ControlMatrix, FIELDS as CF, UNDECLARED  # noqa: E402
import models as forest  # noqa: E402  experiment-local; registers forest_n and ode_meanfield


def forest_cases():
    """Re-integrates each part-1 configuration through #257's own runner.integrate (no file
    is written) so every boundary flux is read at full precision from its accumulator; the
    pinned part1.json prints fluxes at 6 significant figures, which is too coarse for a
    1e-9 closure test on the other side. The pinned verdicts are kept as #257's reading,
    and the recomputed misclosure is checked against them."""
    import run as fr                                   # forest_fire_regime/run.py; its writes sit under __main__
    from playground.experiments import runner
    from playground import l0
    with open(os.path.join(FOREST, "out", "part1.json")) as f:
        p1 = json.load(f)
    rows = []
    for run_id, stream, kw in (("replay_base", "REPLAY", {}), ("replay_no_fire", "REPLAY", dict(fires=0)),
                               ("native_seed0", "NATIVE", {}), ("replay_planted_leak_0.3", "REPLAY", dict(leak=0.3))):
        cfg = fr.forest_config(run_id, stream, 0, **kw)
        model = eq.get(cfg["model"])
        times, states, _ = runner.integrate(model, cfg, cfg["parameters"].resolve(), cfg["initial"].resolve())
        s0, s1 = states[0], states[-1]
        audit_rows, _ = l0.audit(cfg["budgets"], s0, s1)
        r = p1[run_id]
        budgets = {}
        for b in cfg["budgets"].values():
            if not b.live:
                continue
            ins = {k.split("|")[2]: v for k, v in s1.items() if k.startswith("_in|%s|" % b.name)}
            outs = {k.split("|")[2]: v for k, v in s1.items() if k.startswith("_out|%s|" % b.name)}
            row = [x for x in audit_rows if x["budget"] == b.name][0]
            budgets[b.name] = dict(pools=list(b.pools), start=sum(s0[p] for p in b.pools), end=sum(s1[p] for p in b.pools),
                                   inflows=ins, outflows=outs, tolerance_257=row["tolerance"],
                                   misclosure_recomputed=row["misclosure"], misclosure_pinned=r[b.name]["misclosure"],
                                   reproduces=row["misclosure"] == r[b.name]["misclosure"] and row["verdict"] == r[b.name]["verdict"],
                                   verdict_257=r[b.name]["verdict"])
        rows.append(dict(case_id="R-F9:" + run_id, group="forest run 9 port", kind="planted_defect" if "leak" in run_id else "control",
                         description=("planted leak: a term in the N state equation that is not in the transfer table"
                                      if "leak" in run_id else "forest run 9 port, %s" % r["stream"]),
                         data=dict(budgets=budgets, fires=r["fires"], void_budgets=[b.name for b in cfg["budgets"].values() if not b.live]),
                         r257=dict(status=r["status"], status_reason=r["status_reason"],
                                   verdicts={b: r[b]["verdict"] for b in ("N", "water")}, model_trust=r["model_trust"])))
    return rows


def coincidence_cases():
    with open(os.path.join(FOREST, "out", "part2.json")) as f:
        p2 = json.load(f)
    rows = []
    for c in p2["coincidence"]["cards"]:
        rows.append(dict(case_id="R-COIN:" + c["id"], group="forest part 2 coincidence", kind="coincidence",
                         description=c["observation"],
                         data=dict(observed=c["c_tests"]["C3"]["observed"], target=c["c_tests"]["C3"]["target"],
                                   window=c["c_tests"]["C3"]["pre_window"], declared_at=c["c_tests"]["C3"]["declared_at"],
                                   families=["percolation", "nonlinear"]),
                         r257=dict(card="OPEN", slots={k: v["state"] for k, v in c["slots"].items()})))
    return rows


def gate_fixtures():
    eq.load_all()
    rows = []
    for name in ("percolation", "branching"):
        rng = random.Random(20261110)            # certify()'s seed; one rng per model, as certify does
        draws = [gate._BUILDERS[name](rng) for _ in range(gate.N_DRAWS)]
        t = gate.certify(name, gate.default_make_config)
        for i, d in enumerate(draws):
            rows.append(dict(case_id="R-KAG:%s-%02d" % (name, i), group="known-answer gate fixture", kind="known_answer",
                             description="%s gate draw %d (clean)" % (name, i), data=d,
                             r257=dict(harness=t["harness"], trusted=t["trusted"], FP=t["FP"], TP=t["TP"])))
    return rows


def status_cases():
    """Shapes #257 accepts, built through its own constructors. Each row is a value or
    claim the #257 record can hold, so the other side can be asked what it makes of it."""
    rows = []
    v = Value(None, "ABSENT_AT_SENSITIVITY", "looked for at this sensitivity, not found", sensitivity=0.05)
    rows.append(dict(case_id="R-VAL:absent_at_sensitivity", group="value status", kind="status",
                     description="ABSENT_AT_SENSITIVITY(0.05): a bounded null, holds no number",
                     data=dict(status=v.status, sensitivity=v.sensitivity, provenance=v.provenance),
                     r257=dict(accepted=True, label=v.label())))
    u = Value(None, "UNKNOWN", "not measured in this tree", expiry_condition="a measured value for K arrives")
    m = UncertaintyMatrix(dict(K=u))
    rows.append(dict(case_id="R-VAL:unknown_with_expiry_text", group="value status", kind="status",
                     description="UNKNOWN with a free-text expiry_condition",
                     data=dict(status=u.status, expiry_condition=u.expiry_condition),
                     r257=dict(accepted=True, expiry_report=m.expiry_report())))
    try:
        Value(None, "UNKNOWN", "x")
        r = dict(accepted=True)
    except ValueError as e:
        r = dict(accepted=False, refused=str(e))
    rows.append(dict(case_id="R-VAL:unknown_without_expiry", group="value status", kind="planted_defect",
                     description="UNKNOWN with no exit stated", data=dict(status="UNKNOWN", expiry_condition=None), r257=r))
    with open(os.path.join(FOREST, "out", "part2.json")) as f:
        claims = json.load(f)["claims"]
    for i, c in enumerate(claims):
        rows.append(dict(case_id="R-CLAIM:part2-%d" % i, group="claim tags", kind="status", description=c["text"],
                         data=c, r257=dict(accepted=True, tag=c["tag"])))
    cm = ControlMatrix(**{f: UNDECLARED for f in CF})
    rows.append(dict(case_id="R-OBS:cross_system_regimes_undeclared", group="observer regimes", kind="planted_defect",
                     description="cross-system comparison requested with all three observer regimes UNDECLARED",
                     data=dict(observer=cm.observer), r257=dict(refused=True, owed=cm.observer_undeclared())))
    try:
        anchor.branch(None, "b", parameter="x", value=1.0, dt=0.1)
        r = dict(refused=False)
    except anchor.AnchorError as e:
        r = dict(refused=True, reason=str(e))
    rows.append(dict(case_id="R-ANCHOR:two_change_branch", group="anchor loop", kind="planted_defect",
                     description="a branch that changes two things against the frozen anchor",
                     data=dict(changes=["parameter x", "config field dt"]), r257=r))
    return rows


def poisson_branching():
    from playground.equations.branching_math import extinction_probability
    rows = []
    for R in (0.8, 1.5, 2.0):
        rows.append(dict(case_id="R-BR:poisson_R%.1f" % R, group="branching die-out", kind="known_answer",
                         description="Poisson(R) offspring; die-out probability is the smallest root of q = exp(R(q-1))",
                         data=dict(R=R, law="poisson"),
                         r257=dict(die_out_probability=extinction_probability(R))))
    return rows


if __name__ == "__main__":
    cases = forest_cases() + coincidence_cases() + gate_fixtures() + status_cases() + poisson_branching()
    common.dump("r257_cases.json", dict(source="Simulators/relational-playground (#257)", rev=common.git_rev(common.SIM_ROOT),
                                        cases=cases))
    print("exported", len(cases), "#257 cases")
