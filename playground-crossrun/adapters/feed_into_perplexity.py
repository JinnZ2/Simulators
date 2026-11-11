"""Feed #257's cases into the study-aperture playground, through its own public objects.

Runs inside study-aperture/experimental. Reads out/r257_cases.json, writes
out/r257_into_p.json. Each row records what the study-aperture build did with
the case (`p`), whether the adapter could express it at all (`adapter_ok`,
`adapter_note`), and whether the concept that decides the classification has
a slot on this side (`slot`, `slot_note`). Every translation choice the
adapter makes is named in `mapping` on the row; nothing is chosen silently.
"""
import dataclasses, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

sys.path.insert(0, common.SA_EXP)
os.chdir(common.SA_EXP)

from playground.failures import Axis, FailureRecord  # noqa: E402
from playground.gates.l0_closure import (BoundaryAccounting, Direction, Exchange, QuantityAccount,  # noqa: E402
                                         ValueProvenance, l0_closure_gate)
from playground.detection.non_detection import NonDetectionObservation, record_non_detection  # noqa: E402
from playground.lifecycle.unknown_expiry import UnknownDetermination  # noqa: E402


def reading(rec):
    if not isinstance(rec, FailureRecord):
        rec = rec.record
    return dict(axes={a.value: rec.status_for(a).value for a in Axis},
                codes=sorted({"%s:%s:%s" % (f.axis.value, f.severity.value, f.code) for f in rec.findings}))


def forest_ledger(case, arm):
    """arm 'as_stated': only what #257 states. #257 has no intervention registry and no
    declared-complete flag, so the registry is empty and completeness is not declared.
    arm 'self_registered': every boundary flux registers itself and the ledger is declared
    complete. That is circular (the ledger vouches for itself) and is kept as a contrast arm."""
    accounts, regs = [], []
    for b, d in sorted(case["data"]["budgets"].items()):
        ex = [Exchange(b, Direction.INFLOW, v, k, ValueProvenance.MODEL, "flux:" + k) for k, v in sorted(d["inflows"].items())]
        ex += [Exchange(b, Direction.OUTFLOW, v, k, ValueProvenance.MODEL, "flux:" + k) for k, v in sorted(d["outflows"].items())]
        regs += ["flux:" + k for k in sorted(d["inflows"]) + sorted(d["outflows"])]
        accounts.append(QuantityAccount(b, d["start"], d["end"], ValueProvenance.SPECIFIED, ValueProvenance.MODEL,
                                        tuple(ex), d["tolerance_257"]))
    if arm == "as_stated":
        return BoundaryAccounting("forest-stand-edge", tuple(accounts), False, ())
    return BoundaryAccounting("forest-stand-edge", tuple(accounts), True, tuple(sorted(set(regs))))


def feed_forest(case):
    arms = {arm: reading(l0_closure_gate(forest_ledger(case, arm)).record) for arm in ("as_stated", "self_registered")}
    leak = "leak" in case["case_id"]
    return dict(p=arms["as_stated"], p_arms=arms, adapter_ok=True,
                mapping=["#257 per-budget tolerance (1e-9 x scale) entered as the absolute account tolerance",
                         "pool start = SPECIFIED (INIT), pool end and every flux = MODEL (simulated, nothing measured)",
                         "VOID budgets (%s) have no account on this side: they are absent, not VOID" % ", ".join(case["data"]["void_budgets"])],
                slot=False,
                slot_note=("declared_complete decides PHYSICAL vs DETERMINATION for an unbalanced ledger; #257 carries no such flag"
                           if leak else "an intervention registry decides whether registration is complete; #257 has none, so 'as_stated' "
                           "reads L0_INTERVENTION_REGISTRY_EMPTY"))


def feed_coincidence(case):
    return dict(p=None, adapter_ok=True, mapping=[], slot=False,
                slot_note="no coincidence card or cross-family agreement object; the nearest object, measurand comparison, needs two "
                          "EquationRuns with declared identity coordinates (#257 declares none: see P-MEAS:both_legacy_declarations_missing, "
                          "comparison-withheld)")


def site_to_bond(case):
    """#257 percolation is SITE percolation with fire spread; the study-aperture family is
    BOND percolation on a FiniteGraph. Declared translation: nodes = every cell, an edge
    between 4-neighbours that are both flammable. Spread dynamics and spotting have no slot."""
    d = case["data"]
    L = d["params"]["L"]
    grid = d["params"]["grid"]
    if grid == "RANDOM":
        grid = [[1 if d["params"]["p_flammable"] >= 1.0 else 0] * L for _ in range(L)]
    nodes = ["c%d_%d" % (i, j) for i in range(L) for j in range(L)]
    edges = []
    for i in range(L):
        for j in range(L):
            for di, dj in ((0, 1), (1, 0)):
                a, b = i + di, j + dj
                if a < L and b < L and grid[i][j] and grid[a][b]:
                    edges.append(("c%d_%d" % (i, j), "c%d_%d" % (a, b)))
    return L, nodes, edges


def feed_percolation(case):
    from playground.equations.percolation import FiniteGraph, MAX_EDGES, MAX_NODES
    from playground.equations.percolation_example import DECISION, EVIDENCE
    L, nodes, edges = site_to_bond(case)
    srcs = tuple(n for n in nodes if n.endswith("_0"))
    tgts = tuple(n for n in nodes if n.endswith("_%d" % (L - 1)))
    try:
        FiniteGraph(tuple(nodes), tuple(edges), srcs, tgts, DECISION, EVIDENCE)
        ok, note = True, "graph accepted"
    except ValueError as e:
        ok, note = False, "FiniteGraph refused: %s" % e
    return dict(p=dict(refused=not ok, detail=note, nodes=len(nodes), edges=len(edges), bounds=dict(MAX_NODES=MAX_NODES, MAX_EDGES=MAX_EDGES)),
                adapter_ok=ok,
                adapter_note=None if ok else "case does not fit the bounded backend (%d nodes, %d bonds; bounds %d / %d)" % (len(nodes), len(edges), MAX_NODES, MAX_EDGES),
                mapping=["site grid -> bond graph: nodes = all L*L cells, bond between flammable 4-neighbours",
                         "sources = column 0, targets = column L-1 (the lit edge and the far edge)"],
                slot=False, slot_note="fire spread in steps, the burning/burned split and spotting have no slot in a static bond graph")


def feed_branching(case):
    from playground.equations.branching import OffspringLaw, MAX_POPULATION, MAX_INITIAL_POPULATION, MAX_GENERATIONS
    from playground.equations import branching_example as bx
    from playground.equations.adapter import EquationRegistry
    from playground.equations.substitution import execute, ValidationPlan
    from playground.validation.known_answer import KnownAnswerCase
    from playground.validation.null_harness import NullCase
    d = case["data"]
    n0, k, n = d["initial"]["active"], d["params"]["R"], int(d["t_end"])
    active, retired = d["expected"]["active"], d["expected"]["retired"]
    mapping = ["fixed offspring R -> degenerate law ((R, 1),)",
               "#257 active(n) -> expected_population at horizon n",
               "#257 retired + active -> expected_cumulative_population (generations 0..n)",
               "the plan's known-answer case is this same #257 closed form: the run is checked against the answer it is fed (circular)"]
    try:
        law = OffspringLaw(((k, 1),), bx.DECISION, bx.EVIDENCE)
        model = bx.fixture_model(law)
        exp = bx.fixture_experiment(law, initial=n0, generations=n)
        pmf = {active: 1}
        expected = bx.stated_expectation(pmf, k, 0, active, 0, retired + active)
        base = bx.stated_expectation({0: 1}, k, 0, 0, 0, 0)
        plan = ValidationPlan("crossrun-257-closed-form", model.digest(), exp.context.digest(),
                              (KnownAnswerCase.from_maps("r257-%s" % case["case_id"], {"initial": n0, "generations": n}, expected,
                                                         {key: 1e-12 for key in expected}, "#257 known_answer_gate._branching closed form"),),
                              (NullCase.from_maps("no-founders", {"initial": 0, "generations": 0}, base, {key: 0 for key in base},
                                                  "zero cohort"),),
                              tuple((p.name, p.unit) for p in model.inputs), tuple((p.name, p.unit) for p in model.outputs),
                              bx.DECISION, bx.EVIDENCE)
        reg = EquationRegistry()
        reg.register(model)
        run = execute(reg, model.equation_id, model.revision, exp, plan, bx.DECISION)
        outs = {o.name: o.value for o in run.outputs} if run.outputs else {}
        got = dict(expected_population=outs.get("expected_population"), expected_cumulative_population=outs.get("expected_cumulative_population"))
        agree = got["expected_population"] == active and got["expected_cumulative_population"] == retired + active
        return dict(p=dict(run_state=run.state.value, got=got, matches_257_closed_form=agree, **reading(run.record)),
                    adapter_ok=True, mapping=mapping, slot=True, slot_note=None)
    except (ValueError, TypeError) as e:
        why = "%s: %s" % (type(e).__name__, e)
        return dict(p=dict(refused=True, detail=why[:300]), adapter_ok=False,
                    adapter_note="outside the bounded backend (initial <= %d, generations <= %d, population <= %d): n0=%d R=%d n=%d -> %d"
                                 % (MAX_INITIAL_POPULATION, MAX_GENERATIONS, MAX_POPULATION, n0, k, n, active),
                    mapping=mapping, slot=True, slot_note=None)


def feed_status(case):
    cid = case["case_id"]
    if cid == "R-VAL:absent_at_sensitivity":
        obs = NonDetectionObservation.from_map("r257-absent", {}, effect_size_of_interest=None) \
            if "effect_size_of_interest" in NonDetectionObservation.from_map.__code__.co_varnames else None
        rec = record_non_detection(obs, None)
        return dict(p=reading(rec), adapter_ok=True,
                    mapping=["#257 carries one sensitivity number and no ladder: no SensitivityDetermination can be built without "
                             "inventing one, so sensitivity enters as None", "no effect size of interest and no conditions in #257: None / {}"],
                    slot=False, slot_note="a bounded null here needs an established sensitivity (a ladder), an effect size of interest and "
                                          "matching conditions; #257's ABSENT_AT_SENSITIVITY(<value>) carries the value only")
    if cid == "R-VAL:unknown_with_expiry_text":
        return dict(p=None, adapter_ok=False,
                    adapter_note="UnknownDetermination needs typed ExpiryTriggers (kind in a closed enum); mapping the free-text "
                                 "expiry_condition onto a kind is an interpretation the adapter does not make",
                    mapping=[], slot=True, slot_note="UNKNOWN with expiry triggers exists on both sides; the trigger is typed here, text in #257")
    if cid == "R-VAL:unknown_without_expiry":
        try:
            u = UnknownDetermination(determination_id="r257-u", statement="no exit stated", expiry_triggers=())
            p = dict(accepted=True, state=u.state.value)
        except (ValueError, TypeError) as e:
            p = dict(accepted=False, refused=str(e)[:200])
        return dict(p=p, adapter_ok=True, mapping=["expiry_condition None -> expiry_triggers ()"], slot=True, slot_note=None)
    if cid.startswith("R-CLAIM:"):
        return dict(p=None, adapter_ok=True, mapping=[], slot=False,
                    slot_note="no OBSERVED / DERIVED / PROPOSED claim tag in this playground; ClaimRecord carries state "
                              "(draft/recorded/unknown/retired) and support (none/partial/unknown), and Condition carries a basis "
                              "(selected/assumed/measured/derived) -- a value-provenance axis, not a claim tag")
    if cid == "R-OBS:cross_system_regimes_undeclared":
        from playground.applicability import example
        from playground.applicability.mapping import Domain, assess
        desc, ctx = example.fixture()
        ctx2 = dataclasses.replace(ctx, conditions=tuple(c for c in ctx.conditions if c.domain is not Domain.OBSERVER))
        res = assess(desc, ctx2)
        return dict(p=dict(state=res.state.value if hasattr(res, "state") else None,
                           unresolved=[u for u in res.unresolved if "observer" in u], **reading(res.record)),
                    adapter_ok=True, mapping=["observer coordinate removed from the shipped applicability fixture context"],
                    slot=True, slot_note="one observer coordinate here against three observer regimes in #257: the slot exists at a "
                                         "coarser grain")
    if cid == "R-ANCHOR:two_change_branch":
        return dict(p=None, adapter_ok=True, mapping=[], slot=False,
                    slot_note="no one-change rule on a branch; equation substitution changes one adapter and reruns every gate, but "
                              "nothing counts the changes between a frozen anchor and a run")
    raise KeyError(cid)


def feed_poisson(case):
    return dict(p=None, adapter_ok=False,
                adapter_note="OffspringLaw takes bounded offspring counts (<= 4) with positive integer weights; Poisson(R) has "
                             "unbounded support and irrational probabilities, so it cannot be entered without truncating a tail, "
                             "which the backend is built to refuse",
                mapping=[], slot=True, slot_note="extinction_by_horizon exists here as a finite-horizon quantity; #257 reports "
                                                  "the ultimate die-out root")


def feed(case):
    g = case["group"]
    if g == "forest run 9 port":
        return feed_forest(case)
    if g == "forest part 2 coincidence":
        return feed_coincidence(case)
    if g == "known-answer gate fixture":
        return feed_percolation(case) if "percolation" in case["case_id"] else feed_branching(case)
    if g == "branching die-out":
        return feed_poisson(case)
    return feed_status(case)


if __name__ == "__main__":
    src = common.load("r257_cases.json")
    rows = []
    for c in src["cases"]:
        r = feed(c)
        r.update(case_id=c["case_id"], group=c["group"], kind=c["kind"], description=c["description"], native=c["r257"])
        rows.append(r)
    common.dump("r257_into_p.json", dict(direction="#257 cases -> study-aperture playground", rev=common.git_rev(common.SA_ROOT), rows=rows))
    print("fed", len(rows), "#257 cases into the study-aperture playground")
