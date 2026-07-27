# rigidification_sensor.py — measures reversibility, not harm.
# CC0. stdlib only. phone-buildable. imports harm.py and simulator.py.
#
# Concretely instantiates a credit-insurance node chain,
# runs the dynamical model, and populates the OPEN falsifier
# values from the rigidification_sensor spec.
#
# names_no: [actor, motive, plan].  Reports shape and rate.

from harm import System, Node, Coupling
import simulator

# ----------------------------------------------------------------------
# 1. Extended simulation that tracks per‑node regen and (optionally)
#    adds a slow regeneration term so the system can recover,
#    making the "outpaces regeneration" claim actually falsifiable.
# ----------------------------------------------------------------------

def run_with_tracking(system, ticks=20, erosion=1.0, regen_rate=0.0):
    """
    Like simulator.run() but also records per‑node regen every tick.
    If regen_rate > 0, each node regenerates capacity up to its initial
    value after erosion — providing a true null hypothesis for claim_001.
    """
    regen0 = {n: nd.regen for n, nd in system.nodes.items()}
    trace = []
    regen_history = {n: [] for n in system.nodes}
    locked_at = None

    for t in range(ticks):
        exported, induced = simulator.step(system, erosion)

        continuation = sum(exported.values())
        reversal = sum(regen0[n] - nd.regen for n, nd in system.nodes.items())
        dof = sum(1 for n, nd in system.nodes.items() if nd.regen > nd.draw)

        # --- regeneration (if enabled) ---
        if regen_rate > 0:
            for n, nd in system.nodes.items():
                nd.regen = min(regen0[n], nd.regen + regen_rate)

        # record per‑node regen *after* this tick's erosion + regeneration
        for n, nd in system.nodes.items():
            regen_history[n].append(nd.regen)

        prev = trace[-1] if trace else None
        d_cont = continuation - prev["continuation"] if prev else continuation
        d_rev = reversal - prev["reversal"] if prev else reversal

        row = {
            "t": t,
            "dof": dof,
            "continuation": round(continuation, 4),
            "reversal": round(reversal, 4),
            "d_continuation": round(d_cont, 4),
            "d_reversal": round(d_rev, 4),
        }
        trace.append(row)

        if locked_at is None and reversal > continuation and d_rev > d_cont:
            locked_at = t

    return {"trace": trace, "locked_at": locked_at, "regen_history": regen_history}


# ----------------------------------------------------------------------
# 2. Concrete credit‑insurance node
# ----------------------------------------------------------------------

def credit_insurance_system():
    """
    A small chain:
      A (insurer)       : slight deficit, exports to reinsurer
      B (reinsurer)     : balanced, but sensitive to arriving cost
      C (capital mkts)  : initial surplus, absorbs but erodes

    Couplings are amplifying (sensitivity > 1), so a local deficit
    inflates downstream — the §1 shape.
    """
    nodes = {
        "A": Node(draw=3.0, regen=2.5),   # deficit 0.5
        "B": Node(draw=2.0, regen=2.0),   # barely balanced
        "C": Node(draw=1.0, regen=1.5),   # surplus 0.5
    }
    couplings = [
        Coupling("A", "B", transfer=1.0, sensitivity=1.5),
        Coupling("B", "C", transfer=1.0, sensitivity=2.0),
    ]
    return System(nodes, couplings)


# ----------------------------------------------------------------------
# 3. Tell extraction and falsifier computation
# ----------------------------------------------------------------------

def analyse(system, ticks=20, erosion=1.0, regen_rate=0.0, sweep_K=False):
    """
    Run the system, compute §3 tells, fill in falsifier values for
    claims 001, 002, 003.  If sweep_K is True, vary the sensitivity of
    the B→C coupling and show how locked_at shifts.
    """
    out = run_with_tracking(system, ticks, erosion, regen_rate)
    trace = out["trace"]
    regen_hist = out["regen_history"]

    # --- §3 tells (first-order) ---
    dof_start = trace[0]["dof"]
    dof_end = trace[-1]["dof"]
    dof_lost = dof_start - dof_end

    # --- second-order tell ---
    locked = out["locked_at"]
    if locked is not None:
        L = trace[locked]
        fire_msg = (f"§1 threshold crossed at t={locked}: "
                    f"reversal={L['reversal']} > continuation={L['continuation']} "
                    f"AND d_rev={L['d_reversal']} > d_cont={L['d_continuation']}")
    else:
        fire_msg = "§1 threshold NOT crossed within the window."

    # --- claim_001: variance decline vs regeneration ---
    # variance of regen across nodes over time
    import statistics
    var_series = []
    for t in range(ticks):
        regens = [regen_hist[n][t] for n in system.nodes]
        var_series.append(statistics.variance(regens) if len(regens) > 1 else 0.0)
    # slope of variance (simple linear regression)
    n_ticks = len(var_series)
    if n_ticks > 1:
        x_mean = (n_ticks - 1) / 2.0
        y_mean = sum(var_series) / n_ticks
        num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(var_series))
        den = sum((i - x_mean) ** 2 for i in range(n_ticks))
        var_slope = num / den if den != 0 else 0.0
    else:
        var_slope = 0.0

    # regeneration rate is the amount of capacity recovered per tick
    # (the regen_rate parameter).  A fair comparison: the magnitude of
    # variance decline per tick must exceed the rate at which variance
    # would recover if nodes regenerated in isolation.
    # Here regen_rate is uniform, but we can compute an effective
    # "variance regeneration slope" by running the system in isolation
    # (no coupling) with regen_rate, but that would always push regen
    # to the cap, giving zero variance.  Instead, we note that each node
    # can recover `regen_rate` capacity per tick.  If the variance
    # decline per tick (in absolute value) exceeds a threshold related
    # to regen_rate, the claim holds.  We'll take a simple heuristic:
    # if variance is declining AND the absolute decline per tick is
    # larger than regen_rate, then suppression outpaces regeneration.
    decline_rate = -var_slope
    claim_001_falsifier = {
        "variance_slope": round(var_slope, 6),
        "decline_rate": round(decline_rate, 6),
        "regen_rate": regen_rate,
        "outpaces_regeneration": decline_rate > regen_rate if regen_rate > 0 else "no regeneration modeled",
    }

    # --- claim_003: reversal cost vs continuation cost ---
    # already captured by the locked_at condition; we just need to
    # report the values at the moment of threshold crossing.
    claim_003_falsifier = {
        "locked_at": locked,
        "reversal_at_lock": L["reversal"] if locked is not None else None,
        "continuation_at_lock": L["continuation"] if locked is not None else None,
        "d_rev_at_lock": L["d_reversal"] if locked is not None else None,
        "d_cont_at_lock": L["d_continuation"] if locked is not None else None,
    }

    # --- claim_002: homogenisation rate responds to K ---
    # We'll sweep sensitivity at B->C and record locked_at.
    sweep_results = None
    if sweep_K:
        sweep_results = []
        base_sens = system.couplings[1].sensitivity
        for mult in [0.5, 1.0, 1.5, 2.0, 2.5]:
            # modify the coupling sensitivity
            mod_couplings = [
                Coupling("A", "B", transfer=1.0, sensitivity=1.5),
                Coupling("B", "C", transfer=1.0, sensitivity=base_sens * mult),
            ]
            mod_sys = System(
                {n: Node(nd.draw, nd.regen) for n, nd in system.nodes.items()},
                mod_couplings,
            )
            out_sweep = run_with_tracking(mod_sys, ticks, erosion, regen_rate)
            sweep_results.append({
                "sensitivity_mult": mult,
                "sensitivity_BC": round(base_sens * mult, 2),
                "locked_at": out_sweep["locked_at"],
                "dof_end": out_sweep["trace"][-1]["dof"],
            })
        claim_002_falsifier = {
            "sweep": sweep_results,
            "claim": "locked_at shifts systematically with sensitivity — higher sensitivity brings lock earlier or deeper",
        }
    else:
        claim_002_falsifier = {"sweep": "not performed"}

    return {
        "system": "credit_insurance_chain",
        "ticks": ticks,
        "dof_start": dof_start,
        "dof_end": dof_end,
        "dof_lost": dof_lost,
        "second_order_fire": fire_msg,
        "claim_001": claim_001_falsifier,
        "claim_002": claim_002_falsifier,
        "claim_003": claim_003_falsifier,
        "trace_summary": trace[-1],   # final tick metrics
    }


# ----------------------------------------------------------------------
# 4. Main: run the sensor, print a report, run self-tests
# ----------------------------------------------------------------------

def report():
    sys = credit_insurance_system()
    # Base run with no regeneration (purist model)
    print("=" * 60)
    print("RIGIDIFICATION SENSOR – credit-insurance node")
    print("=" * 60)
    print("\n§0 branch selection:")
    print("  Node: insurer → reinsurer → capital markets.")
    print("  High load, low observability, structural knobs present.")
    print("  No actor-intent branches selected.\n")

    # Run with regeneration rate 0.1 to make claim_001 non-trivial
    print("Running with regeneration rate = 0.1 (so regrowth is possible)...")
    res = analyse(sys, ticks=20, erosion=1.0, regen_rate=0.1, sweep_K=True)

    print(f"DOF: {res['dof_start']} → {res['dof_end']} (lost {res['dof_lost']})")
    print(f"Second‑order tell: {res['second_order_fire']}")
    print(f"\n--- claim_001 (variance decline vs regeneration) ---")
    print(res["claim_001"])
    print(f"\n--- claim_003 (reversal cost) ---")
    print(res["claim_003"])
    print(f"\n--- claim_002 (K sweep) ---")
    for s in res["claim_002"]["sweep"]:
        print(f"  sens={s['sensitivity_BC']:.1f} → locked_at={s['locked_at']}, dof_end={s['dof_end']}")
    print(f"\nFinal tick state: {res['trace_summary']}")
    print("\nAll OPEN values populated. Contest §0 before trusting the numbers.\n")

def _self_test():
    # basic integrity checks
    sys = credit_insurance_system()
    out = run_with_tracking(sys, ticks=5, erosion=1.0, regen_rate=0.0)
    assert "regen_history" in out
    assert all(len(v) == 5 for v in out["regen_history"].values())
    # with regeneration, variance should decline slower
    out_reg = run_with_tracking(sys, ticks=10, erosion=1.0, regen_rate=0.2)
    var0 = out["regen_history"]; var1 = out_reg["regen_history"]
    # not a strong test, just that regeneration avoids zero floor immediately
    # but we can check that locked_at may be later or None.
    res = analyse(sys, ticks=10, erosion=1.0, regen_rate=0.0, sweep_K=False)
    assert res["dof_lost"] >= 0
    print("self-test passed")

if __name__ == "__main__":
    _self_test()
    report()
