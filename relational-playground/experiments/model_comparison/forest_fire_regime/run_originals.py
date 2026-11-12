"""PART 3. The original run 6, 7, 8 code, ported, beside the rebuild.

    python3 run_originals.py          # writes out/part3.json and RESULTS_ORIGINALS.txt

Targets and rules: PREREG_ORIGINALS.md (committed before originals.py).
Two branches are kept: ORIGINAL (this file) and REBUILD (run.py part 2, read
from out/part2.json; not re-run and not changed here). Nothing is ranked.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
for p in (ROOT, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
import originals as O
from playground import l0
from playground.analysis import coincidence as cc
from playground.reporting import claims as cl
from playground.equations.branching_math import extinction_probability

H = float.fromhex
WINDOW, C6_TOL, SEEDS = 0.05, 0.02, tuple(range(4, 24))
SMALL = 0.05      # a replicate that burned under 5% of the vegetation; set after the seed spread was seen, so descriptive only
DECLARED = "PREREG_ORIGINALS.md, committed before originals.py"
P3 = lambda x, n=3: "%.*f" % (n, x)


def check(name, ok, got, want):
    return dict(target=name, reading="MET" if ok else "MISSED", got=got, want=want)


def part3():
    with open(os.path.join(HERE, "fixtures", "originals_expected.json")) as f:
        fx = json.load(f)
    out = dict(reference=dict(numpy=fx["numpy_version"], scipy=fx["scipy_version"], sources=fx["sources"]), targets=[])
    T = out["targets"]

    # ---- run 7
    r7 = O.run7()
    e7 = fx["run_7"]
    dg = max(max(abs(a["grid_mean"] - H(b["grid_mean"])), abs(a["grid_sd"] - H(b["grid_sd"]))) for a, b in zip(r7, e7))
    do = max(abs(a["ode"] - H(b["ode"])) for a, b in zip(r7, e7))
    T.append(check("O7 grid mean and sd, 11 droughts, within 1e-12", dg <= 1e-12, "max difference %.3g" % dg, "<= 1e-12"))
    T.append(check("O7 ODE fraction within 1e-9", do <= 1e-9, "max difference %.3g" % do, "<= 1e-9"))
    for r in r7:
        r["ode_over_grid"] = r["ode"] / r["grid_mean"] if r["grid_mean"] > 0 else None
    out["run_7"] = r7

    # ---- run 8
    r8 = O.run8()
    e8 = fx["run_8"]
    d8 = max(max(abs(c["mean"] - H(d["mean"])), abs(c["sd"] - H(d["sd"]))) for a, b in zip(r8, e8) for c, d in zip(a["cells"], b["cells"]))
    do8 = max(abs(a["ode"] - H(b["ode"])) for a, b in zip(r8, e8))
    T.append(check("O8 mean and sd, 5 droughts x 4 spot levels, within 1e-12", d8 <= 1e-12, "max difference %.3g" % d8, "<= 1e-12"))
    T.append(check("O8 ODE fraction within 1e-9", do8 <= 1e-9, "max difference %.3g" % do8, "<= 1e-9"))
    out["run_8"] = r8

    # ---- run 6
    st = O.run6_structure()
    e6 = fx["run_6"]
    old = O.run6_old(st)
    want_old = [H(e6["old_misclosure"][i]) for i in (0, 1, 5, 10, -1)]
    got_old = [old[i] for i in (0, 1, 5, 10, -1)]
    T.append(check("O6 OLD misclosure at the five printed checkpoints, 3 decimals", [P3(x) for x in got_old] == [P3(x) for x in want_old],
                   [P3(x) for x in got_old], [P3(x) for x in want_old]))
    r6 = dict(old_checkpoints=got_old, conserved={})
    fires_ok, stats_ok, fires_got, fires_want, worst = True, True, [], [], 0.0
    for thr in (0.6, 0.3, 0.5, 0.8, 1.2):
        c = O.run6_conserved(thr, struct=st)
        s, e = O.run6_stats(c["B"]), e6["conserved"][repr(thr)]
        mis_max = max(abs(x) for x in c["mis"])
        fires_got.append(c["fires"]); fires_want.append(e["fires"])
        fires_ok &= c["fires"] == e["fires"]
        for k, nd in (("B_mean", 3), ("swing", 3), ("tree_share", 2), ("Ls_min", 2), ("Ls_max", 2)):
            stats_ok &= P3(s[k], nd) == P3(H(e[k]), nd)
            worst = max(worst, abs(s[k] - H(e[k])))
        b = c["boundary"]
        scale = b["dep"] + b["fix"] + b["leach"] + b["volat"]
        r6["conserved"][repr(thr)] = dict(fires=c["fires"], stats=s, mis_max=mis_max, mis_max_numpy=H(e["mis_max"]), boundary=b,
                                          l0=dict(budget="N", misclosure_max=mis_max, tolerance=l0.REL_TOL * scale,
                                                  verdict=l0.verdict(mis_max, scale),
                                                  how="playground l0.verdict on the run's own checkpoint audit (31 checkpoints); "
                                                      "not the runner's per-transfer table: this model is not registered through the substitution interface"))
        if thr == 0.6:
            T.append(check("O6 CONSERVED max |misclosure| below 1e-8", mis_max < 1e-8, "%.16e (numpy run %.16e)" % (mis_max, H(e["mis_max"])), "< 1e-8"))
    T.append(check("O6 fires at fire_thr 0.6 / 0.3 / 0.5 / 0.8 / 1.2, exact", fires_ok, fires_got, fires_want))
    T.append(check("O6 late biomass mean, swing, tree share, Ls range, sweep columns at printed precision", stats_ok,
                   "largest difference from the numpy run %.3g" % worst, "equal at printed precision"))
    b_old = l0.verdict(old[-1], 1.0)
    r6["old_l0"] = dict(budget="N", misclosure_last_checkpoint=old[-1], verdict=b_old,
                        how="playground l0.verdict on the run's own audit; scale 1.0 N unit")
    out["run_6"] = r6

    # ---- rebuild beside original
    with open(os.path.join(HERE, "out", "part2.json")) as f:
        p2 = json.load(f)
    reb0 = {round(r["drought"], 2): r for r in p2["table"]["spot_0.00"]}
    reb2 = {round(r["drought"], 2): r for r in p2["table"]["spot_0.20"]}
    f1 = []
    for r in r7:
        d = round(r["drought"], 2)
        rb = reb0.get(d)
        f1.append(dict(drought=d, original_ode=r["ode"], original_grid=r["grid_mean"], original_ratio=r["ode_over_grid"],
                       rebuild_ode=rb["ode"] if rb else None, rebuild_grid=rb["grid_mean"] if rb else None,
                       rebuild_ratio=rb["ode_over_grid"] if rb else None))
    out["F1"] = dict(rule="ODE / grid by drought for both branches; no single number", rows=f1,
                     note="ratios at grid means of a few cells are noise-dominated (original: 12 reps, one seed)")
    f3 = []
    for row in r8:
        cell = [c for c in row["cells"] if c["spot"] == 0.2][0]
        gap = abs(cell["mean"] - row["ode"])
        rb = reb2.get(round(row["drought"], 2))
        f3.append(dict(drought=row["drought"], original_grid=cell["mean"], original_sd=cell["sd"], original_ode=row["ode"], original_gap=gap,
                       original_inside=gap <= WINDOW, rebuild_gap=rb["abs_gap"] if rb else None, rebuild_inside=rb["inside_window"] if rb else None))
    spread = {}
    for dr in (0.5, 0.6, 0.7):
        spread[dr] = []
    reps_all = {dr: [] for dr in spread}
    for seed in SEEDS:
        rng = O.ns.default_rng(seed)
        for dr in (0.5, 0.6, 0.7):
            p = 0.2 + 0.75 * dr
            keep = []
            m, _sd = O.run8_burn(rng, 0.8, p, 0.2, keep=keep)
            spread[dr].append(m - O.ode_fraction(0.8, p))
            reps_all[dr].extend(keep)
    sp = []
    for dr, v in spread.items():
        reps = reps_all[dr]
        small = [x for x in reps if x < SMALL]
        large = [x for x in reps if x >= SMALL]
        m = math.fsum(v) / len(v)
        sd = math.sqrt(math.fsum((x - m) ** 2 for x in v) / (len(v) - 1))
        sp.append(dict(drought=dr, seeds=len(v), mean_signed_gap=m, sd_over_seeds=sd, min=min(v), max=max(v),
                       inside_window=sum(1 for x in v if abs(x) <= WINDOW), replicates=len(reps), replicates_below_small=len(small),
                       branching_dieout=extinction_probability(4 * (0.2 + 0.75 * dr) * 0.8),
                       mean_of_the_rest=math.fsum(large) / len(large) if large else None,
                       rest_minus_ode=(math.fsum(large) / len(large) - O.ode_fraction(0.8, 0.2 + 0.75 * dr)) if large else None))
    seed4_small = 0
    rng4 = O.ns.default_rng(4)
    for dr in O.RUN8_DROUGHTS:                    # the full run 8 sequence, so these are run 8's own replicates
        for s in O.RUN8_SPOTS:
            keep = []
            O.run8_burn(rng4, 0.8, 0.2 + 0.75 * dr, s, keep=keep)
            if s == 0.2 and dr in (0.5, 0.6, 0.7):
                seed4_small += sum(1 for x in keep if x < SMALL)
    out["F3"] = dict(seed4_small="%d of 30 under 5%%" % seed4_small,
                     window=WINDOW, window_declared=DECLARED + "; the original run declared none", rows=f3, seed_spread=sp,
                     seed_spread_note="original design (L 100, 10 reps, spot 0.2) on seeds 4..23, three droughts only, so the draw "
                                      "sequence for seed 4 is not the one the full run 8 used; a hand-written seed loop, not a multi-seed tool")

    # ---- coincidence cards: evidence entered, no slot set
    design = ("design differences, original vs rebuild: grid L 100 (run 8) / 120 (run 7) vs 64; reps 10 / 12 vs 40; ignition at the centre vs "
              "left edge; ODE z = 1 - exp(-4 p d z) vs the rebuild's mean field of its own grid rules; seeds 3 and 4 vs the rebuild's. "
              "'design' is not one of the card's five causes; recorded as evidence text only")
    c1 = cc.open_card("CC_F1_ode_grid_ratio", "ODE / grid ratio differs between branches (original 62 at drought 0.5; rebuild max %.1f)" %
                      max(r["rebuild_ratio"] for r in f1 if isinstance(r["rebuild_ratio"], float)),
                      "rebuild does not show the logged feature; the divergence between two builds of one comparison is data")
    c3 = cc.open_card("CC_F3_grid_onto_ode", "grid at spot 0.2 near the ODE at drought >= 0.5: original inside 0.05 at 3 of 3 points; "
                      "rebuild outside at 0.50 (gap %.4f), inside from 0.55" % reb2[0.5]["abs_gap"],
                      "a convergence seen in one toy, read by eye, is a candidate; two builds disagree at one point")
    gap_o = [r for r in f3 if r["drought"] == 0.5][0]["original_gap"]
    cc.run_c6(c3, "abs(grid - ODE) at spot 0.2, drought 0.5", C6_TOL, DECLARED, by_config=dict(original=gap_o, rebuild=reb2[0.5]["abs_gap"]))
    c3["c_tests"]["C3"] = "VOID for the original: no window was declared before the numbers were seen (read by eye). The 0.05 window is applied afterwards."
    c3["c_tests"]["C2"] = "NOT RUN: the chance of one (spot, drought) cell landing inside the window is not known; 20 cells were looked at"
    c3["c_tests"]["C5"] = "NOT RUN: no persistence tolerance was declared in PREREG_ORIGINALS.md"
    for c in (c1, c3):
        c["evidence_entered"] = dict(
            statistical="original: one seed, 10-12 reps. Seed spread of (grid - ODE) at spot 0.2 over 20 seeds: " +
                        "; ".join("drought %.1f mean %+.4f sd %.4f, %d of %d inside 0.05" % (s["drought"], s["mean_signed_gap"], s["sd_over_seeds"], s["inside_window"], s["seeds"]) for s in sp),
            numerical="the stdlib port equals the numpy run within %.1g on every grid mean and sd, so the original's numbers do not depend on numpy vs plain arithmetic; a grid burn has no step size" % max(dg, d8),
            design=design)
        c["reading"] = cc.read(c)[0]
    out["cards"] = [c1, c3]
    out["claims"] = cl.check([
        cl.claim("the port reproduces the delivered code's results (targets table)", "DERIVED", "run_originals.py against fixtures/originals_expected.json"),
        cl.claim("the delivered code is what ran chat-side on 2026-11-10", "OBSERVED", "source: chat side, 2026-11-11; filed verbatim, sha256 in the fixture"),
        cl.claim("which of statistical / numerical / design explains the rebuild-original difference", "PROPOSED", "evidence entered on two OPEN cards; no slot set"),
    ])
    return out


def render(p):
    o = ["PART 3  original run 6, 7, 8 code, ported to the standard library",
         "  reference: delivered files run on numpy %s, scipy %s (fixtures/originals_expected.json)" % (p["reference"]["numpy"], p["reference"]["scipy"]),
         "  targets (PREREG_ORIGINALS.md): %d of %d MET" % (sum(1 for t in p["targets"] if t["reading"] == "MET"), len(p["targets"]))]
    for t in p["targets"]:
        o.append("    %-6s %s" % (t["reading"], t["target"]))
        o.append("           got %s ; want %s" % (t["got"], t["want"]))
    o.append("  run 6, N budget read by the playground's L0 rule:")
    c = p["run_6"]["conserved"]["0.6"]
    o.append("    CONSERVED  %s  max |misclosure| %.3e (tolerance %.3e)  fires %d" % (c["l0"]["verdict"], c["mis_max"], c["l0"]["tolerance"], c["fires"]))
    o.append("    OLD        %s  misclosure %.3f at the last checkpoint" % (p["run_6"]["old_l0"]["verdict"], p["run_6"]["old_l0"]["misclosure_last_checkpoint"]))
    o.append("    fires by fire_thr: " + "  ".join("%s: %d" % (k, v["fires"]) for k, v in p["run_6"]["conserved"].items()))
    o.append("  F1  ODE / grid by drought (no spotting) -- two branches, both kept")
    o.append("    drought   ORIGINAL ode  grid    ratio      REBUILD ode  grid    ratio")
    R = lambda x: "%8.1f" % x if isinstance(x, float) else "   undef"
    V = lambda x: "%.3f" % x if isinstance(x, float) else "  -- "
    for r in p["F1"]["rows"]:
        o.append("    %5.2f     %s        %s  %s    %s        %s  %s" % (r["drought"], V(r["original_ode"]), V(r["original_grid"]), R(r["original_ratio"]),
                                                                    V(r["rebuild_ode"]), V(r["rebuild_grid"]), R(r["rebuild_ratio"])))
    o.append("    " + p["F1"]["note"])
    o.append("  F3  |grid - ODE| at spot 0.2, window %.2f (declared after the original ran; the original declared none)" % p["F3"]["window"])
    o.append("    drought   ORIGINAL grid  sd     ode    gap     inside   REBUILD gap  inside")
    for r in p["F3"]["rows"]:
        o.append("    %4.1f      %.3f          %.3f  %.3f  %.4f  %-6s   %s      %s" % (
            r["drought"], r["original_grid"], r["original_sd"], r["original_ode"], r["original_gap"], "yes" if r["original_inside"] else "no",
            "%.4f" % r["rebuild_gap"] if r["rebuild_gap"] is not None else "  --  ",
            "--" if r["rebuild_inside"] is None else ("yes" if r["rebuild_inside"] else "no")))
    o.append("    seed spread, original design, seeds 4..23 (grid - ODE, signed):")
    for s in p["F3"]["seed_spread"]:
        o.append("      drought %.1f  mean %+.4f  sd over seeds %.4f  range %+.4f .. %+.4f  inside 0.05: %d of %d" % (
            s["drought"], s["mean_signed_gap"], s["sd_over_seeds"], s["min"], s["max"], s["inside_window"], s["seeds"]))
        o.append("                   replicates that burned under 5%%: %d of %d (%.3f) ; mean of the rest minus ODE %+.4f" % (
            s["replicates_below_small"], s["replicates"], s["replicates_below_small"] / s["replicates"], s["rest_minus_ode"]))
        o.append("                   branching family, Poisson(R = 4 p d) offspring, die-out from one ignition: %.3f" % s["branching_dieout"])
    o.append("      the 5% cut was set after the spread was seen: a description, not a test. In run 8 itself (seed 4)")
    o.append("      every one of the 30 replicates at these three droughts burned more than 5%%: %s" % p["F3"]["seed4_small"])
    o.append("  coincidence cards (evidence entered, no slot set):")
    for c in p["cards"]:
        o.append("    %s  %s" % (c["id"], c["reading"]))
        for k in ("statistical", "numerical", "design"):
            o.append("      %-11s %s" % (k, c["evidence_entered"][k]))
        c6 = c["c_tests"]["C6"]
        if isinstance(c6, dict):
            o.append("      C6 by_config  spread %.4f against tolerance %.2f -> numerical_artifact flag %s (the two configs also differ in design)" % (
                c6["config_spread"], c6["stability_tol"], c6["numerical_artifact"]))
    o.append("      family swap run: playground branching_math.extinction_probability (registered). The grid gives a cell at most")
    o.append("      4 offspring, not Poisson, so that family as built is not the grid's; its die-out is printed beside the count, not fitted to it.")
    o.append("  F1 note: the delivered correction quotes 478 / 321 / 62 from the 3-decimal columns; unrounded the ratios are the ORIGINAL column above.")
    o.append("  TRIGGER: the seed spread is an unexpected deviation from run 8's single-seed reading. Full toolbox owed; see NEEDS_TOOL.md.")
    o.append("  F3 stays CANDIDATE. Nothing here ranks the two branches.")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("run_originals.py has no selftest; run: python3 selftest_originals.py")
        sys.exit(2)
    p = part3()
    with open(os.path.join(HERE, "out", "part3.json"), "w") as f:
        json.dump(p, f, indent=1, sort_keys=True, default=str)
        f.write("\n")
    text = render(p)
    with open(os.path.join(HERE, "RESULTS_ORIGINALS.txt"), "w") as f:
        f.write(text)
    sys.stdout.write(text)
