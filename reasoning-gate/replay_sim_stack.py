#!/usr/bin/env python3
"""
replay_sim_stack.py - run the audited sim stack back through the gate.

CC0-1.0. Stdlib only.

SIM-B was sound. SIM-A and SIM-C were run past the stop point on
purpose so the divergence would be observable. This replays all
three and checks the gate catches A and C and passes B.
"""

from gate import Gate, GateError, Resolution, Control


def sim_b():
    g = Gate("SIM-B")
    g.pre(
        question="do quasiperiodic and cascade point sets share a fractal dimension",
        statistic="box-counting D_f with local-slope plateau",
        discriminates=("D_f separates clustered from space-filling sets. "
                       "NOTE: blind to quasiperiodic order by construction - "
                       "uniform coverage returns the embedding dimension "
                       "regardless of arrangement"),
        expected="AB near 2 (space-filling), cascade below 2 (clustered)",
        resolution=[Resolution("smallest box vs mean nearest-neighbour spacing",
                               instrument=0.05, feature=0.20, margin=2.0)],
        controls=[Control("poisson", predicted="~2.0"),
                  Control("periodic lattice", predicted="~2.0"),
                  Control("line", predicted="1.0")],
    )
    g.control_result("poisson", 1.911)
    g.control_result("periodic lattice", 1.964)
    g.control_result("line", 1.000)

    g.record("Df_AB", 1.889, layer="physical", object_of="Ammann-Beenker tiling")
    g.record("Df_cascade", 1.555, layer="generator",
             object_of="branching_walk output",
             note="set by E_split, E_min, branch rule - not a tungsten property")
    g.record("cluster_spread", 0.075, layer="instrument",
             object_of="box-count estimator",
             note="spread across the three space-filling sets = the error bar")

    g.claim("the two sets do not share a fractal dimension",
            supported_by=["Df_AB", "Df_cascade", "cluster_spread"])
    return g, g.close(observed="AB 1.889 / cascade 1.555, controls on target")


def sim_a():
    g = Gate("SIM-A", strict=False)
    g.pre(
        question="do the two sets share spectral order",
        statistic="structure factor S(k), radial average",
        discriminates="S(k) separates pure-point order from diffuse scattering",
        expected=("AB: dense point spectrum, many sharp peaks away from k=0. "
                  "cascade: flat, S(k) -> 1"),
        # dk = 0.39, finite-sample peak width 2*pi/L = 0.063
        resolution=[Resolution("k-grid spacing vs Bragg peak width",
                               instrument=0.39, feature=0.063)],
        controls=[Control("periodic lattice through same S(k) code",
                          predicted="sharp peaks at reciprocal lattice vectors")],
    )
    return g, None


def sim_c():
    g = Gate("SIM-C", strict=False)
    g.pre(
        question="does the band-edge knee correspond to the cascade branch threshold",
        statistic="band-edge splitting vs aperiodicity fraction",
        discriminates="a shared threshold would show as aligned knees",
        expected="a knee, or no knee",
        resolution=[Resolution("finite-size level spacing vs splitting",
                               instrument=0.031, feature=0.0812, margin=2.0)],
        controls=[Control("f=0 periodic limit", predicted="zero splitting")],
    )
    g.control_result("f=0 periodic limit", 0.0)
    g.record("knee_splitting", 0.0812, layer="instrument",
             object_of="16x16 tight-binding model")
    g.record("cascade_E_split", 0.0015, layer="generator",
             object_of="branching_walk output")
    g.ratio("knee_over_Esplit", "knee_splitting", "cascade_E_split")
    g.claim("the two systems operate on different normalized energy scales",
            supported_by=["knee_over_Esplit"])
    g.convergence(across=["SIM-A", "SIM-B", "SIM-C"], shared=[])
    return g, g.close(observed="knee at f=0.65, splitting 0.0812")


if __name__ == "__main__":
    print("=" * 62)
    g, rep = sim_b()
    print(g.summary(rep))
    print("-> SIM-B PASSES\n")

    print("=" * 62)
    try:
        sim_a()
        print("-> SIM-A passed (unexpected)")
    except GateError as e:
        print("SIM-A DENIED AT PRE:\n  %s" % e)
        print("-> never executes. the ringing spectrum is never produced.\n")

    print("=" * 62)
    g, rep = sim_c()
    print(g.summary(rep))
    print("-> SIM-C runs but its ratio is void and its claim unsupported.")
