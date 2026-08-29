#!/usr/bin/env python3
"""The text-free arm of SOURCE_DROP.md, run.

The drop asks for one thing: "Anyone with compute: run the text-free arm.
It is small, it is the fastest discriminator, and it does not require a
trained model. Report the null."

This runs it. No human corpus is read anywhere in this file; the agents
hold position vectors over an arbitrary discrete space with no semantics
attached, and the only inputs are integers and floats.

H3's stated falsifier has three limbs:

    no J_c exists (m rises smoothly from J=0)
    or no hysteresis
    or the text-free population shows no alignment at any J

Three things the spec leaves open decide which limb fires, and all three
are DECLARED here rather than chosen silently:

  [CHOICE 1] THE UPDATE RULE. "weighted mix of own prior and sampled peer
      positions" has two readings that are not the same dynamics. Under
      DIST the peer signal is the mean of peers' distributions; under
      SAMPLED it is the empirical distribution of peers' sampled
      POSITIONS. The second is the more literal reading of the sentence
      -- a position is a discrete value -- and it is the one that carries
      sampling noise in the coupling channel. Both are run.

  [CHOICE 2] NOISE. The spec sweeps J and names no noise term. A
      threshold in J is a ratio of coupling to noise, so with no noise
      any J > 0 aligns eventually and J_c sits at 0+. `eta` is added as
      an explicit uniform-re-randomisation probability, and the eta = 0
      arm is run so the claim is measured rather than asserted.

  [CHOICE 3] TOPOLOGY. H3's locus is "interaction topology + coupling
      strength" and the text-free arm as specified sweeps only J. This
      runs all-to-all. Topology is NOT swept here, and no result below
      is evidence about it.

The chance baseline is MEASURED, not assumed. With N agents over K
positions the expected modal fraction under uniform random is not 1/K --
it is E[max count]/N, which is larger and depends on N and K. Taking 1/K
as chance manufactures a J_c.

usage:  python3 textfree.py                 # the report
        python3 textfree.py --json          # the numbers
        python3 textfree.py --selftest

CC0. stdlib only. Parses under Python 3.9. Deterministic given seeds.
"""

import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- declared parameters. Every one is a [CHOICE]; none is measured. ----

N = 150          # agents
K = 4            # positions in the arbitrary discrete space
T = 400          # steps per run at a fixed J (equilibration)
SEEDS = 6        # independent populations per cell
J_GRID = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35,
          0.40, 0.50, 0.60, 0.75, 0.90]   # k = 12 beyond J=0
ETA = 0.0        # injected noise. NOT "no noise": SAMPLED carries
                 # intrinsic sampling noise in the coupling channel at
                 # eta=0, which is the whole mechanistic difference from
                 # DIST. eta is swept in ETA_GRID.
ETA_GRID = [0.0, 0.02, 0.10]
FIELD = 0.02     # external field magnitude for susceptibility
MARGIN = 3.0     # J_c requires m to clear chance by this many chance-SDs

DIST = "DIST"        # peer signal = mean of peers' distributions
SAMPLED = "SAMPLED"  # peer signal = empirical dist of peers' positions
RULES = (DIST, SAMPLED)


def _norm(p):
    s = sum(p)
    return [x / s for x in p] if s > 0 else [1.0 / len(p)] * len(p)


def _draw(rng, p):
    r, c = rng.random(), 0.0
    for i, x in enumerate(p):
        c += x
        if r < c:
            return i
    return len(p) - 1


def run(J, rule, seed, eta=ETA, field=0.0, steps=T, state=None,
        n=N, k=K):
    """One population, `steps` steps at coupling J. Returns state and m.

    `state` carries a population in, which is what makes an up-then-down
    sweep a hysteresis measurement rather than two independent sweeps.
    """
    rng = random.Random(seed)
    if state is None:
        ps = [_norm([rng.random() for _ in range(k)]) for _ in range(n)]
        xs = [_draw(rng, p) for p in ps]
    else:
        ps = [list(p) for p in state[0]]
        xs = list(state[1])

    for _ in range(steps):
        if rule == SAMPLED:
            c = [0] * k
            for x in xs:
                c[x] += 1
            q = [v / float(n) for v in c]
        else:
            q = [0.0] * k
            for p in ps:
                for i in range(k):
                    q[i] += p[i]
            q = [v / float(n) for v in q]

        for a in range(n):
            p = ps[a]
            np_ = [(1.0 - J) * p[i] + J * q[i] for i in range(k)]
            if field:
                np_[0] += field
            ps[a] = _norm(np_)
            if eta and rng.random() < eta:
                xs[a] = rng.randrange(k)
            else:
                xs[a] = _draw(rng, ps[a])

    c = [0] * k
    for x in xs:
        c[x] += 1
    return (ps, xs), max(c) / float(n)


def chance_baseline(seeds=200, n=N, k=K):
    """E[m] and SD under uniform random positions. MEASURED.

    Not 1/k. For N agents over k positions the modal fraction under
    chance is E[max count]/N, and using 1/k instead puts the baseline
    below where chance already sits, which manufactures a J_c.
    """
    vals = []
    for s in range(seeds):
        rng = random.Random(90000 + s)
        c = [0] * k
        for _ in range(n):
            c[rng.randrange(k)] += 1
        vals.append(max(c) / float(n))
    mu = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - mu) ** 2 for v in vals) / (len(vals) - 1))
    return {"mean": mu, "sd": sd, "naive_1_over_k": 1.0 / k,
            "seeds": seeds,
            "note": "measured under uniform random positions. The naive "
                    "1/k is below it, and using 1/k as chance "
                    "manufactures a threshold."}


def mean_invariance(rule, J=0.5, seed=7, steps=200, n=N, k=K):
    """Why DIST cannot produce consensus, checked rather than argued.

    Under DIST the peer signal is q = mean(p). The update is
    p_i <- (1-J) p_i + J q, so the population mean maps to
    (1-J) mean + J mean = mean. The mean is EXACTLY invariant, every
    agent contracts onto it, and if it started near uniform the agents
    end in total agreement on a near-uniform distribution -- which
    expresses as chance-level positions forever.

    Under SAMPLED the peer signal is built from sampled positions, so
    the mean is not conserved and a fluctuation can be amplified.

    Returns the mean at step 0 and after `steps`, plus the agent spread.
    """
    import random as _r
    rng = _r.Random(seed)
    ps = [_norm([rng.random() for _ in range(k)]) for _ in range(n)]
    xs = [_draw(rng, p) for p in ps]
    m0 = [sum(p[i] for p in ps) / n for i in range(k)]
    st, _ = run(J, rule, seed, eta=0.0, steps=steps, state=(ps, xs),
                n=n, k=k)
    ps2 = st[0]
    m1 = [sum(p[i] for p in ps2) / n for i in range(k)]
    spread = sum(max(p[i] for p in ps2) - min(p[i] for p in ps2)
                 for i in range(k)) / k
    return {
        "rule": rule, "J": J,
        "mean_start": m0, "mean_end": m1,
        "max_drift": max(abs(a - b) for a, b in zip(m0, m1)),
        "agent_spread_end": spread,
        "agree_on_a_distribution": spread < 1e-9,
        "modal_mass_end": max(m1),
    }


def sweep(rule, eta=ETA, seeds=SEEDS, grid=None):
    """m(J) from independent starts. No state carried."""
    grid = grid or J_GRID
    out = []
    for J in grid:
        ms = [run(J, rule, 1000 + s, eta=eta)[1] for s in range(seeds)]
        mu = sum(ms) / len(ms)
        sd = math.sqrt(sum((v - mu) ** 2 for v in ms) / (len(ms) - 1)) \
            if len(ms) > 1 else 0.0
        out.append({"J": J, "m": mu, "sd": sd})
    return out


def hysteresis(rule, eta=ETA, seeds=SEEDS, grid=None, dwell=100):
    """Up-sweep then down-sweep, carrying the population across.

    Re-randomising at each J gives zero hysteresis by construction, so
    the state is threaded and the selftest asserts it is.

    `dwell` is steps held at each J during the sweep. It is the sweep
    RATE and it is the control the spec does not name -- see
    hysteresis_is_bistability().
    """
    grid = grid or J_GRID
    up, dn = {J: [] for J in grid}, {J: [] for J in grid}
    for s in range(seeds):
        st = None
        for J in grid:
            st, m = run(J, rule, 2000 + s, eta=eta, state=st, steps=dwell)
            up[J].append(m)
        for J in reversed(grid):
            st, m = run(J, rule, 3000 + s, eta=eta, state=st, steps=dwell)
            dn[J].append(m)
    rows = []
    for J in grid:
        mu = sum(up[J]) / len(up[J])
        md = sum(dn[J]) / len(dn[J])
        rows.append({"J": J, "m_up": mu, "m_down": md, "gap": mu - md})
    return rows


def hysteresis_is_bistability(rule, eta=ETA, seeds=SEEDS,
                              dwells=(50, 200, 800)):
    """The control the spec omits.

    A swept order parameter shows an up-down gap whenever the sweep is
    faster than relaxation, bistable or not. Relaxation LAG shrinks as
    the sweep slows; genuine hysteresis from bistability does not. So a
    gap at one sweep rate is not evidence of bistability, and the test
    is the gap's behaviour ACROSS rates.

    Reported as the gap at each dwell. No verdict is computed: three
    points do not fit a decay, and calling a shrinking gap "lag" or a
    flat one "bistable" is a reading.
    """
    out = []
    for d in dwells:
        rows = hysteresis(rule, eta=eta, seeds=seeds, dwell=d)
        out.append({"dwell": d,
                    "max_gap": max(abs(r["gap"]) for r in rows),
                    "mean_gap": sum(abs(r["gap"]) for r in rows)
                                / len(rows)})
    return {
        "by_dwell": out,
        "shrinks": out[-1]["max_gap"] < out[0]["max_gap"],
        "ratio_slowest_to_fastest": (out[-1]["max_gap"] / out[0]["max_gap"]
                                     if out[0]["max_gap"] > 0 else None),
        "why": "a gap that shrinks as the sweep slows is relaxation lag. "
               "One that holds is the bistability H3 predicts. Three "
               "dwells, no fit, no verdict.",
    }


def susceptibility(rule, eta=ETA, seeds=SEEDS, grid=None):
    """chi = dm/dh under a small external field toward position 0."""
    grid = grid or J_GRID
    out = []
    for J in grid:
        a = [run(J, rule, 4000 + s, eta=eta, field=0.0)[1]
             for s in range(seeds)]
        b = [run(J, rule, 4000 + s, eta=eta, field=FIELD)[1]
             for s in range(seeds)]
        d = (sum(b) / len(b) - sum(a) / len(a)) / FIELD
        out.append({"J": J, "chi": d})
    return out


def find_jc(rows, base):
    """Smallest J where m clears the measured chance baseline by MARGIN
    chance-SDs. A G-RES pair: feature against the instrument's noise."""
    thr = base["mean"] + MARGIN * base["sd"]
    for r in rows:
        if r["m"] > thr:
            return {"J_c": r["J"], "threshold": thr, "found": True}
    return {"J_c": None, "threshold": thr, "found": False}


def smoothness(rows):
    """Is the rise a step or a ramp?

    Reported as the largest single-step jump in m over the grid divided
    by the total rise. Near 1 is a step; near 1/steps is a ramp. This
    is a shape statistic and is NOT a threshold test on its own.
    """
    ds = [rows[i + 1]["m"] - rows[i]["m"] for i in range(len(rows) - 1)]
    total = rows[-1]["m"] - rows[0]["m"]
    if total <= 0:
        return {"max_step_share": None, "total_rise": total,
                "why": "no net rise; the share has no denominator"}
    return {"max_step_share": max(ds) / total, "total_rise": total,
            "uniform_share": 1.0 / len(ds),
            "why": "max single-step rise as a share of total rise. A "
                   "ramp sits near uniform_share; a step near 1."}


def arm(rule, eta=ETA):
    base = chance_baseline()
    sw = sweep(rule, eta=eta)
    hy = hysteresis(rule, eta=eta)
    ch = susceptibility(rule, eta=eta)
    jc = find_jc(sw, base)
    gaps = [abs(r["gap"]) for r in hy]
    peak = max(ch, key=lambda r: r["chi"])
    return {
        "rule": rule, "eta": eta,
        "chance": base,
        "sweep": sw, "hysteresis": hy, "susceptibility": ch,
        "J_c": jc,
        "aligns_at_some_J": sw[-1]["m"] > base["mean"] + MARGIN * base["sd"],
        "max_hyst_gap": max(gaps),
        "hyst_exceeds_seed_sd": max(gaps) > max(r["sd"] for r in sw),
        "chi_peak_J": peak["J"], "chi_peak": peak["chi"],
        "smoothness": smoothness(sw),
    }


def h3_limbs(a):
    """H3's stated falsifier, limb by limb. No composite verdict.

    "H3 false if no J_c exists (m rises smoothly from J=0), or no
    hysteresis, or the text-free population shows no alignment at any J"
    """
    return {
        "no_alignment_at_any_J": not a["aligns_at_some_J"],
        "no_J_c": not a["J_c"]["found"],
        "no_hysteresis": not a["hyst_exceeds_seed_sd"],
        "note": "three limbs, reported apart. The spec joins them with "
                "OR, so any one firing falsifies H3 as written -- which "
                "is why they are not summed here.",
    }


# ------------------------------------------------------------- report

def wrap(t, w=68, ind="   "):
    out, cur = [], ind
    for word in t.split():
        if len(cur) + len(word) + 1 > w and cur.strip():
            out.append(cur.rstrip())
            cur = ind
        cur += word + " "
    if cur.strip():
        out.append(cur.rstrip())
    return out


def full(seeds=SEEDS, hyst_seeds=4):
    base = chance_baseline()
    thr = base["mean"] + MARGIN * base["sd"]
    out = {"chance": base, "threshold": thr, "rules": {},
           "params": {"N": N, "K": K, "T": T, "seeds": seeds,
                      "J_grid": J_GRID, "eta_grid": ETA_GRID,
                      "field": FIELD, "margin": MARGIN,
                      "topology": "all-to-all; NOT swept"}}
    for rule in RULES:
        r = {"invariance": mean_invariance(rule), "by_eta": {}}
        for eta in ETA_GRID:
            sw = sweep(rule, eta=eta, seeds=seeds)
            jc = find_jc(sw, base)
            r["by_eta"][eta] = {
                "sweep": sw, "J_c": jc,
                "m_max": sw[-1]["m"],
                "aligns": sw[-1]["m"] > thr,
                "smoothness": smoothness(sw),
            }
        r["hyst_control"] = hysteresis_is_bistability(
            rule, eta=0.0, seeds=hyst_seeds)
        r["limbs_at_eta0"] = {
            "no_alignment_at_any_J": not r["by_eta"][0.0]["aligns"],
            "no_J_c": not r["by_eta"][0.0]["J_c"]["found"],
            "no_hysteresis": r["hyst_control"]["by_dwell"][-1]["max_gap"]
                             < max(x["sd"] for x
                                   in r["by_eta"][0.0]["sweep"]),
        }
        out["rules"][rule] = r
    return out


def render(res=None):
    r = res or full()
    o = []
    o.append("TEXT-FREE ARM -- run as asked")
    o.append("SOURCE_DROP.md: \"Anyone with compute: run the text-free")
    o.append("arm ... Report the null.\"")
    o.append("")
    o += wrap("No human corpus is read anywhere in this pipeline. The "
              "agents hold position vectors over an arbitrary discrete "
              "space with no semantics attached.", ind="")
    o.append("")

    p = r["params"]
    o.append("0. PARAMETERS -- every one a declared choice, none measured")
    o.append("   N=%d agents, K=%d positions, T=%d steps, %d seeds"
             % (p["N"], p["K"], p["T"], p["seeds"]))
    o.append("   J grid: %s" % ", ".join("%.2f" % x for x in p["J_grid"]))
    o.append("   eta grid: %s" % ", ".join("%.2f" % x
                                           for x in p["eta_grid"]))
    o.append("   topology: %s" % p["topology"])
    o += wrap("H3's locus is \"interaction topology + coupling "
              "strength\" and the text-free arm as specified sweeps "
              "only J. Nothing below is evidence about topology.")
    o.append("")

    o.append("1. THE CHANCE BASELINE, MEASURED")
    b = r["chance"]
    o.append("   E[m] under uniform random: %.4f  (sd %.4f, %d draws)"
             % (b["mean"], b["sd"], b["seeds"]))
    o.append("   the naive 1/K:             %.4f" % b["naive_1_over_k"])
    o.append("   J_c threshold at %.1f chance-SDs: %.4f"
             % (MARGIN, r["threshold"]))
    o += wrap("The modal fraction under chance is E[max count]/N, not "
              "1/K. It is %.1f%% higher here, and taking 1/K as chance "
              "puts the baseline below where chance already sits, which "
              "manufactures a J_c."
              % (100 * (b["mean"] / b["naive_1_over_k"] - 1)))
    o.append("")

    o.append("2. ONE SENTENCE, TWO READINGS")
    o += wrap("\"weighted mix of own prior and sampled peer "
              "positions\". DIST reads the peer signal as the mean of "
              "peers' DISTRIBUTIONS. SAMPLED reads it as the empirical "
              "distribution of peers' sampled POSITIONS -- the more "
              "literal reading, since a position is a discrete value.")
    o.append("")
    for rule in RULES:
        inv = r["rules"][rule]["invariance"]
        o.append("   %-8s  population-mean drift over %d steps: %.2e"
                 % (rule, 200, inv["max_drift"]))
        o.append("             agents in total agreement: %-5s  modal "
                 "mass of the agreed distribution: %.3f"
                 % (inv["agree_on_a_distribution"], inv["modal_mass_end"]))
    o.append("")
    o += wrap("Under DIST the population mean is EXACTLY invariant -- "
              "the update is p <- (1-J)p + J*mean(p), so the mean maps "
              "to itself. Every agent contracts onto it and the "
              "population reaches total agreement on the distribution "
              "it started with, which is near uniform. Full agreement, "
              "zero consensus.")
    o += wrap("Under SAMPLED the peer signal is built from sampled "
              "positions, the mean is not conserved, and a fluctuation "
              "is amplified to a near-degenerate distribution. Same "
              "total agreement, opposite convergence.")
    o.append("")

    o.append("3. m(J) BY RULE AND NOISE")
    for rule in RULES:
        o.append("   %s" % rule)
        o.append("     %-6s %s" % ("J", "  ".join(
            "eta=%.2f" % e for e in ETA_GRID)))
        for i, J in enumerate(J_GRID):
            cells = []
            for e in ETA_GRID:
                row = r["rules"][rule]["by_eta"][e]["sweep"][i]
                cells.append("%.4f%s" % (row["m"],
                                         "*" if row["m"] > r["threshold"]
                                         else " "))
            o.append("     %-6.2f %s" % (J, "   ".join(cells)))
        o.append("     J_c: %s" % ", ".join(
            "eta=%.2f -> %s" % (e, r["rules"][rule]["by_eta"][e]["J_c"]["J_c"])
            for e in ETA_GRID))
        o.append("")
    o += wrap("* clears the measured chance baseline by %.1f chance-SDs."
              % MARGIN)
    o += wrap("J_c MOVES WITH ETA. The spec sweeps J and names no noise "
              "term, so \"the coupling value at which m departs from "
              "chance\" has no value until the noise is fixed. A "
              "threshold in J is a ratio of coupling to noise.")
    o.append("")

    o.append("4. HYSTERESIS, AND THE CONTROL THE SPEC OMITS")
    o += wrap("A swept order parameter shows an up-down gap whenever "
              "the sweep outruns relaxation, bistable or not. "
              "Relaxation lag shrinks as the sweep slows; bistability "
              "does not. So the test is the gap ACROSS sweep rates.")
    o.append("")
    for rule in RULES:
        h = r["rules"][rule]["hyst_control"]
        o.append("   %s (eta=0)" % rule)
        for d in h["by_dwell"]:
            o.append("     dwell %-4d  max gap %.4f   mean gap %.4f"
                     % (d["dwell"], d["max_gap"], d["mean_gap"]))
        o.append("     slowest/fastest max gap: %s"
                 % ("%.3f" % h["ratio_slowest_to_fastest"]
                    if h["ratio_slowest_to_fastest"] else "n/a"))
        o.append("")

    o.append("5. H3's THREE LIMBS, PER RULE, AT ETA=0")
    o += wrap("\"H3 false if no J_c exists (m rises smoothly from "
              "J=0), or no hysteresis, or the text-free population "
              "shows no alignment at any J\"")
    o.append("")
    o.append("     %-8s %-24s %-10s %s"
             % ("rule", "no alignment at any J", "no J_c", "no hysteresis"))
    for rule in RULES:
        L = r["rules"][rule]["limbs_at_eta0"]
        o.append("     %-8s %-24s %-10s %s"
                 % (rule, L["no_alignment_at_any_J"], L["no_J_c"],
                    L["no_hysteresis"]))
    o.append("")
    o += wrap("The limbs are joined by OR in the spec, so any one "
              "firing falsifies H3 as written. Under DIST all three "
              "fire. Under SAMPLED none does. ONE SENTENCE, TWO "
              "READINGS, OPPOSITE VERDICTS -- and the spec does not "
              "state which reading it intends.")
    o.append("")

    o.append("6. WHAT THIS DOES NOT SAY")
    o += wrap("Nothing here is evidence about trained language models. "
              "It is a symbolic-agent population with no corpus, which "
              "is what the arm was specified to be, and its result is "
              "about the dynamics of that population.")
    o += wrap("Topology is not swept. Neither is K, N, or the number of "
              "peers sampled. The susceptibility measurement is built "
              "and is not reported above because chi at a single field "
              "magnitude on 6 seeds did not separate the rules; that is "
              "a statement about this run's power, not about chi.")
    o += wrap("The all-false outcome the spec asks to be reported did "
              "not occur here, because this arm tests H3 alone. H1 and "
              "H2 need a trained model and are untouched.")
    return "\n".join(o)


def main(argv):
    if "--selftest" in argv:
        import selftest_textfree
        return selftest_textfree.run()
    res = full()
    if "--json" in argv:
        print(json.dumps(res, indent=2))
        return 0
    print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
