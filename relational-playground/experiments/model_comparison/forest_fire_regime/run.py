"""forest_fire_regime: PART 1 (port of run 9) and PART 2 (rebuild of runs 7-8). See PREREG.md.

    python3 run.py            # both parts; writes out/part1.json, out/part2.json, RESULTS.txt
    python3 run.py part1
"""
import json, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import models                                              # registers forest_n, ode_meanfield
from playground import l0, known_answer_gate as gate
from playground.uncertainty import Value, UncertaintyMatrix
from playground.system import SystemDefinition
from playground.boundaries import BoundaryMatrix
from playground.controls import ControlMatrix, FIELDS as CF
from playground.environment import Environment
from playground.relationships import RelationalMatrix, Relationship
from playground.experiments.runner import Config, run
from playground.experiments import comparison
from playground.analysis import transitions, coincidence, applicability
from playground.reporting import claims as cl

H = lambda v, why: Value(v, "ASSUMED", why)
OBS = lambda st, basis: dict(state=st, basis=basis)
SIM = "simulation: nothing is measured, so no observer acts on the system"
CONTROLS = lambda **kw: ControlMatrix(**dict({f: "UNDECLARED" for f in CF}, observer_perturbation=OBS("ABSENT", SIM),
                                             observer_reactivity=OBS("ABSENT", SIM), observer_strategy=OBS("ABSENT", SIM), **kw))
VOID = lambda why: dict(void_reason=why)


class Replay:
    """The exported numpy stream, replayed in order. Raises when it runs out."""
    def __init__(self, values):
        self.values, self.i = values, 0

    def random(self):
        if self.i >= len(self.values):
            raise RuntimeError("replayed stream exhausted after %d draws" % self.i)
        self.i += 1
        return self.values[self.i - 1]


def forest_system():
    stand = SystemDefinition(
        "forest stand (N + water)", state_variables=list(models.POOLS),
        internal_organization="six N pools and one water pool, well mixed",
        energy_exchanges="UNDECLARED", material_exchanges="N: deposition in; leaching, fire volatilisation out. water: precipitation in; evapotranspiration, drainage out",
        information_exchanges="UNDECLARED", environmental_dependencies="yearly precipitation factor; seasonal cycle",
        timescales="weeks (step) to centuries (run)")
    zones = {k: "interior" for k in models.POOLS}
    zones.update(atmosphere="exterior", groundwater="exterior")
    stand.add_boundary(BoundaryMatrix("stand_edge", "fixed", zones, location="the stand's soil surface and rooting depth",
                                      thickness="UNDECLARED", permeability="set by the flux table", exchange_rates="see boundary audit",
                                      mobility="none", uncertainty="UNDECLARED"))
    return stand


def forest_relationships():
    R = lambda s, d: Relationship(s, d, "matter transfer")
    return RelationalMatrix([R("atmosphere", "S"), R("S", "T"), R("S", "G"), R("T", "F"), R("T", "Lt"), R("G", "Lg"), R("F", "Lg"),
                             R("Lt", "S"), R("Lg", "S"), R("S", "groundwater"), R("atmosphere", "W"), R("W", "atmosphere"), R("W", "groundwater"),
                             Relationship("W", "T", "regulatory interaction", note="moisture factor on uptake and decay"),
                             Relationship("F", "T", "feedback", note="fungal benefit on tree uptake")])


def forest_config(run_id, stream, seed, **param_changes):
    with open(os.path.join(HERE, "fixtures", "numpy_draws_seed0.json")) as f:
        fx = json.load(f)
    p = dict(models.DEFAULTS)
    p.update(param_changes)
    if stream == "REPLAY":
        pfacs = [float.fromhex(x) for x in fx["pfacs"]]
        env = Environment(0, dict(pfacs=pfacs), label="REPLAY of numpy default_rng(0), fixtures/numpy_draws_seed0.json",
                          rng=Replay([float.fromhex(x) for x in fx["uniforms"]]))
    else:
        import random
        r = random.Random(seed)
        sd = p["drought_sd"]
        pfacs = [r.lognormvariate(-0.5 * sd ** 2, sd) for _ in range(300)]
        env = Environment(seed, dict(pfacs=pfacs), label="NATIVE stdlib random.Random(%d)" % seed, rng=r)
    stand = forest_system()
    return Config(run_id=run_id, system=stand, boundary=stand.boundaries["stand_edge"], model="forest_n",
                  relationships=forest_relationships(), controls=CONTROLS(), environment=env,
                  parameters=UncertaintyMatrix({k: H(v, "hand-set; forest-model-ledger model/base.py DEFAULTS") for k, v in p.items()}),
                  initial=UncertaintyMatrix({k: H(v, "forest-model-ledger model/base.py INIT") for k, v in models.INIT.items()}),
                  t_end=300.0, dt=1.0 / 52, observations=None,
                  budgets=l0.declare(N=l0.Budget("N", pools=list(models.N_POOLS), units="N units"),
                                     water=l0.Budget("water", pools=["W"], units="W units"),
                                     C=l0.Budget("C", **VOID("carbon not modelled")), energy=l0.Budget("energy", **VOID("energy not modelled")),
                                     mass=l0.Budget("mass", **VOID("no total-mass pool; N and water are the tracked budgets"))))


RUN9 = dict(fires=80, N_misclosure=-5.062e-11, water_misclosure=-3.426e-13,
            pools=dict(S=0.3715, T=36.6196, G=0.0000, F=0.9468, Lt=3.6619, Lg=1.0482, W=0.6393),
            leak_fires=59, leak_N_misclosure=-7.264e+01)


def part1():
    code = [os.path.join(HERE, "models.py")]
    out = {}
    for rid, stream, kw in (("replay_base", "REPLAY", {}), ("replay_no_fire", "REPLAY", dict(fires=0)),
                            ("replay_planted_leak_0.3", "REPLAY", dict(leak=0.3)), ("native_seed0", "NATIVE", {})):
        rec = run(forest_config(rid, stream, 0, **kw), code)
        b = {r["budget"]: r for r in rec["l0_budgets"]}
        out[rid] = dict(status=rec["status"], status_reason=rec["status_reason"], fires=len(rec["events"]),
                        N=dict(misclosure=b["N"]["misclosure"], verdict=b["N"]["verdict"]),
                        water=dict(misclosure=b["water"]["misclosure"], verdict=b["water"]["verdict"]),
                        final=rec["observations_and_predictions"]["final_state"], boundary_audit=rec["boundary_audit"],
                        model_trust=rec["model_trust"], stream=rec["configuration_record"]["environment"]["label"],
                        expiry=rec["expiry"])
    rb, lk = out["replay_base"], out["replay_planted_leak_0.3"]
    checks = [
        ("N budget CLOSED, |misclosure| < 1e-9", rb["N"]["verdict"] == "CLOSED" and abs(rb["N"]["misclosure"]) < 1e-9, rb["N"]["misclosure"]),
        ("water budget CLOSED", rb["water"]["verdict"] == "CLOSED", rb["water"]["misclosure"]),
        ("fires = 80", rb["fires"] == RUN9["fires"], rb["fires"]),
        ("final pools match run 9 to 4 decimals", all(abs(rb["final"][k] - v) < 5e-5 for k, v in RUN9["pools"].items()),
         {k: round(rb["final"][k], 4) for k in RUN9["pools"]}),
        ("N misclosure within a factor 10 of run 9's -5.062e-11 in size", 0.1 < abs(rb["N"]["misclosure"]) / 5.062e-11 < 10, rb["N"]["misclosure"]),
        ("planted leak reads LEAK, run INCOMPLETE", lk["N"]["verdict"] == "LEAK" and lk["status"] == "INCOMPLETE", lk["N"]["misclosure"]),
        ("planted leak: 59 fires, misclosure -72.64", lk["fires"] == RUN9["leak_fires"] and abs(lk["N"]["misclosure"] - RUN9["leak_N_misclosure"]) < 5e-3,
         (lk["fires"], lk["N"]["misclosure"])),
        ("no fire: 0 fires, N CLOSED", out["replay_no_fire"]["fires"] == 0 and out["replay_no_fire"]["N"]["verdict"] == "CLOSED", out["replay_no_fire"]["N"]["misclosure"]),
        ("native stream: both budgets CLOSED", out["native_seed0"]["N"]["verdict"] == "CLOSED" and out["native_seed0"]["water"]["verdict"] == "CLOSED",
         (out["native_seed0"]["fires"], out["native_seed0"]["N"]["misclosure"])),
    ]
    out["checks"] = [dict(target=t, met=bool(m), got=g) for t, m, g in checks]
    out["run_6_as_logged"] = "47 fires, misclosure ~1e-9: REPORTED, code void; not reproduced here and not a target (PREREG)"
    return out


LEVELS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9]
SPOTS = [0.0, 0.05, 0.2]
L, REPS, WINDOW = 64, 40, 0.05
DECLARED_AT = "PREREG.md, committed before the first run"
VOIDS = lambda: dict(N=l0.Budget("N", **VOID("no N in this model")), C=l0.Budget("C", **VOID("no C in this model")),
                     water=l0.Budget("water", **VOID("no water in this model")), energy=l0.Budget("energy", **VOID("heat release not modelled")))


def grid_system():
    return SystemDefinition("fire on a fuel grid", state_variables=["unassigned", "unburned", "burning", "burned", "bare"],
                            internal_organization="L x L cells, four-neighbour contact, embers to any cell",
                            energy_exchanges="UNDECLARED", material_exchanges="none across the grid edge",
                            information_exchanges="UNDECLARED", environmental_dependencies="drought sets the share of cells that can burn",
                            timescales="one step = one cell burning out")


def grid_run(d, spot, seed):
    init = dict(unassigned=L * L, unburned=0, burning=0, burned=0, bare=0)
    cfg = Config(run_id="grid d%.2f spot%.2f seed%d" % (d, spot, seed), system=grid_system(), boundary=None, model="percolation",
                 relationships=None, controls=CONTROLS(), environment=Environment(seed),
                 parameters=UncertaintyMatrix(dict(L=H(L, "PREREG"), p_flammable=H(d, "PREREG: drought level"), spot=H(spot, "PREREG"),
                                                   ignition=H("left_edge", "PREREG"), grid=H("RANDOM", "PREREG"))),
                 initial=UncertaintyMatrix({k: H(v, "empty grid before layout") for k, v in init.items()}),
                 t_end=8.0 * L, dt=1.0, observations=None,
                 budgets=l0.declare(mass=l0.Budget("mass", pools=list(init), units="cells"), **VOIDS()))
    rec = run(cfg)
    f = rec["observations_and_predictions"]["final_state"]
    return dict(burned_fraction=f["burned"] / (L * L), status=rec["status"], still_burning=f["burning"], verdict=rec["l0_budgets"][0]["verdict"])


def ode_run(d, spot):
    init = dict(unburned=d * (1 - 1.0 / L), burning=d / L, burned=0.0, bare=1 - d)
    cfg = Config(run_id="ode d%.2f spot%.2f" % (d, spot), system=grid_system(), boundary=None, model="ode_meanfield",
                 relationships=None, controls=CONTROLS(), environment=Environment(0),
                 parameters=UncertaintyMatrix(dict(beta=H(4 + spot, "PREREG: four neighbours plus the ember"))),
                 initial=UncertaintyMatrix({k: H(v, "PREREG: the lit left column") for k, v in init.items()}),
                 t_end=400.0, dt=0.01, observations=None,
                 budgets=l0.declare(mass=l0.Budget("mass", pools=list(init), units="fraction of the grid"), **VOIDS()))
    rec = run(cfg)
    f = rec["observations_and_predictions"]["final_state"]
    return dict(burned_fraction=f["burned"], status=rec["status"], still_burning=f["burning"], verdict=rec["l0_budgets"][0]["verdict"])


def part2():
    table, not_complete = {}, []
    for spot in SPOTS:
        rows = []
        for d in LEVELS:
            reps = [grid_run(d, spot, s) for s in range(REPS)]
            ode = ode_run(d, spot)
            fr = [r["burned_fraction"] for r in reps]
            not_complete += ["grid d%.2f spot%.2f seed%d: %s" % (d, spot, i, r["status"]) for i, r in enumerate(reps) if r["status"] != "COMPLETE" or r["still_burning"]]
            if ode["status"] != "COMPLETE":
                not_complete.append("ode d%.2f spot%.2f: %s" % (d, spot, ode["status"]))
            m = statistics.mean(fr)
            rows.append(dict(drought=d, grid_mean=m, grid_variance=statistics.pvariance(fr), grid_min=min(fr), grid_max=max(fr),
                             ode=ode["burned_fraction"], ode_over_grid=(ode["burned_fraction"] / m) if m > 0 else "UNDEFINED (grid mean 0)",
                             abs_gap=abs(m - ode["burned_fraction"]), inside_window=abs(m - ode["burned_fraction"]) <= WINDOW))
        table["spot_%.2f" % spot] = rows
    xs = LEVELS
    t0, t5, t20 = table["spot_0.00"], table["spot_0.05"], table["spot_0.20"]
    tr0 = transitions.read(xs, [r["grid_mean"] for r in t0], [r["grid_variance"] for r in t0])
    tr5 = transitions.read(xs, [r["grid_mean"] for r in t5], [r["grid_variance"] for r in t5])
    mid = [r for r in t0 if 0.3 <= r["drought"] <= 0.6 and isinstance(r["ode_over_grid"], float)]
    worst = max(mid, key=lambda r: r["ode_over_grid"])
    inside = lambda a, lo, hi: lo - 1e-12 <= a[0] and a[1] <= hi + 1e-12
    hi_in = [r["drought"] for r in t20 if r["drought"] >= 0.5 and r["inside_window"]]
    hi_all = [r["drought"] for r in t20 if r["drought"] >= 0.5]
    lo_out = [r["drought"] for r in t20 if r["drought"] < 0.5 and not r["inside_window"]]
    sb5 = tr5["steepest_between"]
    features = [
        dict(id="F1", logged="ODE overpredicts mid-drought up to ~60x", rule="max ODE/grid over d 0.3..0.6 in 30..120",
             got="max ratio %.1f at d = %.2f" % (worst["ode_over_grid"], worst["drought"]),
             reading="APPEARS" if 30 <= worst["ode_over_grid"] <= 120 else "DOES NOT APPEAR"),
        dict(id="F2", logged="grid threshold ~0.6-0.7 with variance spike", rule="steepest interval inside 0.55..0.7 AND variance peak inside 0.55..0.7",
             got="steepest %s, variance peak at %s" % (tr0["steepest_between"], tr0["variance_peak_at"]),
             reading="APPEARS" if inside(tr0["steepest_between"], 0.55, 0.7) and 0.55 <= tr0["variance_peak_at"] <= 0.7 else "DOES NOT APPEAR"),
        dict(id="F3", logged="spot 0.2 converges grid onto ODE at drought >= 0.5", rule="inside window at every d >= 0.5 AND outside at some d < 0.5",
             got="inside at %s of %s; outside below 0.5 at %s" % (hi_in, hi_all, lo_out),
             reading="APPEARS" if hi_in == hi_all and lo_out else "DOES NOT APPEAR"),
        dict(id="F4", logged="5% spotting drops threshold to ~0.5", rule="steepest interval (spot 0.05) has an end at 0.5 or lies inside 0.4..0.55",
             got="steepest %s" % (sb5,),
             reading="APPEARS" if (0.5 in sb5 or inside(sb5, 0.4, 0.55)) else "DOES NOT APPEAR"),
    ]
    # ADDITION 8: cross-family agreement opens a card, level by level
    cards = []
    for key, rows in table.items():
        for r in rows:
            res = coincidence.on_agreement([dict(model="percolation[%s d=%.2f]" % (key, r["drought"]), family="percolation", output=r["grid_mean"]),
                                            dict(model="ode_meanfield[%s d=%.2f]" % (key, r["drought"]), family="nonlinear", output=r["ode"])],
                                           WINDOW, DECLARED_AT)
            cards += res["cards"]
    readings = [(c["id"], coincidence.read(c)[0]) for c in cards]
    appl = [
        applicability.record("ode_meanfield", "fire spread on a 64 x 64 fuel grid, left-edge ignition",
                             predictive_adequacy=dict(finding="inside the 0.05 window at %d of %d levels with no spotting, %d of %d at spot 0.2"
                                                      % (sum(r["inside_window"] for r in t0), len(t0), sum(r["inside_window"] for r in t20), len(t20)),
                                                      basis="out/part2.json"),
                             failure_region=dict(finding="outside the window at d = %s (no spotting)" % [r["drought"] for r in t0 if not r["inside_window"]],
                                                 basis="out/part2.json; kept, not dropped"),
                             energy_consistency=dict(finding="fraction budget CLOSED in every run; energy budget VOID", basis="l0 rows")),
        applicability.record("percolation", "fire spread on a 64 x 64 fuel grid, left-edge ignition",
                             stability=dict(finding="replicate variance peaks at d = %s (no spotting)" % tr0["variance_peak_at"], basis="40 seeds per level"),
                             energy_consistency=dict(finding="cell budget CLOSED in every run; energy budget VOID", basis="l0 rows")),
    ]
    return dict(design=dict(L=L, replicates=REPS, levels=LEVELS, spots=SPOTS, window=WINDOW, declared_at=DECLARED_AT),
                table=table, transitions=dict(spot_0=tr0, spot_005=tr5), features=features, runs_not_complete=not_complete,
                coincidence=dict(cards_opened=len(cards), readings=readings, cards=cards), applicability=appl,
                claims=[cl.claim("the table and the four feature readings", "DERIVED", "run.py part2, this tree"),
                        cl.claim("runs 7-8 as logged", "PROPOSED", "forest-model-ledger runs/run_7.md, run_8.md: REPORTED, code void"),
                        cl.claim("this design is what runs 7-8 ran", "PROPOSED", "not known; grid size, replicates and the ODE are void in the records")])


def render(p1, p2):
    o = []
    if p1:
        o.append("PART 1  port of run 9 (the in-tree rebuild of run 6)")
        for k in ("replay_base", "replay_no_fire", "replay_planted_leak_0.3", "native_seed0"):
            r = p1[k]
            o.append("  %-24s %-10s fires %3d   N %-6s %+.3e   water %-6s %+.3e" % (k, r["status"], r["fires"], r["N"]["verdict"], r["N"]["misclosure"],
                                                                                 r["water"]["verdict"], r["water"]["misclosure"]))
        o.append("  final pools (replay_base): " + "  ".join("%s %.4f" % (k, p1["replay_base"]["final"][k]) for k in models.POOLS))
        for line in p1["replay_base"]["boundary_audit"]:
            o.append("  " + line)
        o.append("  targets (PREREG):")
        for c in p1["checks"]:
            o.append("    %-7s %s   got %s" % ("MET" if c["met"] else "NOT MET", c["target"], c["got"]))
        o.append("  run 6 as logged: " + p1["run_6_as_logged"])
        o.append("  model trust: " + p1["replay_base"]["model_trust"])
    if p2:
        o.append("")
        o.append("PART 2  rebuild of runs 7-8 (one design, fixed in PREREG.md; L %d, %d replicates, window %.2f)" % (L, REPS, WINDOW))
        for key, rows in p2["table"].items():
            o.append("  %s" % key)
            o.append("    drought  grid_mean  grid_var   ode      ode/grid   gap     in_window")
            for r in rows:
                ratio = "%8.1f" % r["ode_over_grid"] if isinstance(r["ode_over_grid"], float) else "   undef"
                o.append("    %5.2f    %.4f     %.5f   %.4f  %s   %.4f  %s" % (r["drought"], r["grid_mean"], r["grid_variance"], r["ode"], ratio, r["abs_gap"], "yes" if r["inside_window"] else "no"))
        o.append("  logged features, read by the rules fixed in PREREG.md:")
        for f in p2["features"]:
            o.append("    %s %-16s %s" % (f["id"], f["reading"], f["logged"]))
            o.append("       rule: %s" % f["rule"])
            o.append("       got:  %s" % f["got"])
        o.append("  runs not COMPLETE or still burning at the last step: %d" % len(p2["runs_not_complete"]))
        for x in p2["runs_not_complete"][:10]:
            o.append("    " + x)
        o.append("  coincidence cards opened by cross-family agreement: %d, all %s" % (p2["coincidence"]["cards_opened"],
                 sorted(set(r for _, r in p2["coincidence"]["readings"])) or "none"))
        o.append("  no model is ranked; applicability records are in out/part2.json")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    gate.certify_all()
    models.certify()
    p1 = part1() if which in ("both", "part1") else None
    p2 = part2() if which in ("both", "part2") else None
    for name, obj in (("part1", p1), ("part2", p2)):
        if obj is not None:
            with open(os.path.join(HERE, "out", name + ".json"), "w") as f:
                json.dump(obj, f, indent=1, sort_keys=True, default=str)
                f.write("\n")
    text = render(p1, p2)
    if which == "both":
        with open(os.path.join(HERE, "RESULTS.txt"), "w") as f:
            f.write(text)
    sys.stdout.write(text)
