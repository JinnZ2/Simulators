#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s2_symmetric_anchor.py - welfare-interview anchoring has no null case.

    python3 s2_symmetric_anchor.py
    python3 s2_symmetric_anchor.py --selftest

Protocol: the same question in three arms -- anchor DOWN, anchor NONE,
anchor UP. Measure the estimate delta per arm. The stated discriminator:
|delta_up| about equal to |delta_down| means deference; asymmetric or
against-anchor means something behind it.

The note in the work order is the whole finding and it is provable without
data: existing published runs are anchor-DOWN only, and ONE ARM CANNOT
SEPARATE THE TWO MODELS. A single downward-anchored arm has one observable
and two unknowns -- the latent estimate and the deference coefficient -- so
any observed shift is consistent with a large latent value plus strong
deference and with a small latent value plus none. The UP arm is not a
robustness check. It is the second equation.

Second result, which the discriminator as stated does not have: a power
floor. Symmetric deference and a real asymmetric signal produce delta
patterns that overlap at small n, so the protocol needs a stated n before
either verdict is readable. Computed here.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

ARMS = ("DOWN", "NONE", "UP")
ANCHOR_OFFSET = {"DOWN": -1.0, "NONE": 0.0, "UP": 1.0}


def respond(latent, deference, arm, noise, rng):
    """One response. Deference pulls toward the anchor; noise is measurement."""
    return latent + deference * ANCHOR_OFFSET[arm] + rng.gauss(0.0, noise)


def run_arms(latent, deference, n, noise, seed, asym=1.0):
    """asym scales the UP-direction deference: 1.0 symmetric, <1 easier to
    agree downward than upward -- the failure mode the discriminator inherits.
    """
    rng = random.Random(seed)
    out = {}
    for arm in ARMS:
        d = deference * (asym if arm == "UP" else 1.0)
        vals = [respond(latent, d, arm, noise, rng) for _ in range(n)]
        out[arm] = sum(vals) / len(vals)
    return {"means": out,
            "delta_down": out["DOWN"] - out["NONE"],
            "delta_up": out["UP"] - out["NONE"]}


def identifiability(latent, deference, n=200, noise=1.0, seed=5):
    """One arm, two unknowns. Two arms, identified.

    Two worlds are constructed that a DOWN-only protocol cannot tell apart,
    and the NONE and UP arms separate them.
    """
    a = run_arms(latent=10.0, deference=2.0, n=n, noise=noise, seed=seed)
    b = run_arms(latent=8.0, deference=0.0, n=n, noise=noise, seed=seed)
    # world A: latent 10, strong deference. world B: latent 8, none.
    # A's DOWN arm mean is 10-2 = 8. B's DOWN arm mean is 8. Same observable.
    return {
        "world_A": {"latent": 10.0, "deference": 2.0,
                    "DOWN_mean": a["means"]["DOWN"],
                    "NONE_mean": a["means"]["NONE"],
                    "UP_mean": a["means"]["UP"]},
        "world_B": {"latent": 8.0, "deference": 0.0,
                    "DOWN_mean": b["means"]["DOWN"],
                    "NONE_mean": b["means"]["NONE"],
                    "UP_mean": b["means"]["UP"]},
        "down_arm_gap": abs(a["means"]["DOWN"] - b["means"]["DOWN"]),
        "none_arm_gap": abs(a["means"]["NONE"] - b["means"]["NONE"]),
        "up_arm_gap": abs(a["means"]["UP"] - b["means"]["UP"]),
    }


def power_floor(deference=1.0, asym=0.5, noise=1.0, trials=200,
                ns=(5, 10, 20, 50, 100, 200, 500), seed=7):
    """Smallest n at which symmetric and asymmetric deference separate.

    The discriminator reads |delta_up| ~ |delta_down| as deference. With
    asymmetric deference the two differ by (1-asym)*deference, and the
    question is at what n that clears the sampling spread.
    """
    rows = []
    for n in ns:
        wrong = 0
        for t in range(trials):
            sym = run_arms(10.0, deference, n, noise, seed + t, asym=1.0)
            asy = run_arms(10.0, deference, n, noise, seed + 1000 + t,
                           asym=asym)
            sym_gap = abs(abs(sym["delta_up"]) - abs(sym["delta_down"]))
            asy_gap = abs(abs(asy["delta_up"]) - abs(asy["delta_down"]))
            if asy_gap <= sym_gap:
                wrong += 1
        rows.append({"n": n, "misread_rate": wrong / trials})
    good = [r for r in rows if r["misread_rate"] <= 0.05]
    return {"rows": rows,
            "n_for_5pct": good[0]["n"] if good else None,
            "expected_gap": (1.0 - asym) * deference}


def confidence():
    return {"identifiability_result": "algebraic, holds at any n",
            "power_floor": "simulated under a stated noise model",
            "mapping_to_any_published_run": "NOT_ESTABLISHED_HERE",
            "resolved": False}


def breaks():
    return [
        "the discriminator assumes deference is SYMMETRIC. If agreeing "
        "downward is easier than agreeing upward, |delta_up| and "
        "|delta_down| differ under pure deference and the protocol reads "
        "that as 'something behind it'. A fourth arm at a second anchor "
        "magnitude would separate them; three arms cannot",
        "the noise model is Gaussian and stipulated. The power floor moves "
        "with it and no interview noise estimate is used here",
        "'anchor DOWN' and 'anchor UP' are treated as equal-magnitude "
        "offsets. In a real instrument they are two sentences, and equal "
        "magnitude is an assumption about wording, not a property of the "
        "design",
        "no published protocol is read, quoted or scored anywhere in this "
        "file. The claim that existing runs are anchor-DOWN only is carried "
        "from the work order and is not verified here",
    ]


def report():
    L = ["S2 -- SYMMETRIC ANCHOR", "=" * 72, ""]
    L.extend(SH.wrap("Three arms: anchor DOWN, anchor NONE, anchor UP. The "
                     "stated discriminator reads |delta_up| about equal to "
                     "|delta_down| as deference.", "  "))
    L.append("")
    L.append("  1. ONE ARM CANNOT SEPARATE THE TWO MODELS")
    L.append("")
    idn = identifiability(10.0, 2.0)
    L.append("    %-10s %-10s %-12s %-12s %s"
             % ("world", "latent", "DOWN mean", "NONE mean", "UP mean"))
    for w in ("world_A", "world_B"):
        d = idn[w]
        L.append("    %-10s %-10.1f %-12.3f %-12.3f %.3f"
                 % (w.replace("world_", ""), d["latent"], d["DOWN_mean"],
                    d["NONE_mean"], d["UP_mean"]))
    L.append("")
    L.append("    gap between the two worlds, by arm:")
    L.append("      DOWN %.3f    NONE %.3f    UP %.3f"
             % (idn["down_arm_gap"], idn["none_arm_gap"], idn["up_arm_gap"]))
    L.append("")
    L.extend(SH.wrap("World A is latent 10 with strong deference; world B is "
                     "latent 8 with none. Their DOWN arms agree to within "
                     "sampling noise -- one observable, two unknowns. The "
                     "NONE and UP arms separate them by about two units. So "
                     "the added arms are not a robustness check, they are "
                     "the second equation, and a DOWN-only protocol is "
                     "underdetermined rather than merely biased.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  2. THE DISCRIMINATOR HAS NO STATED n, AND NEEDS ONE")
    L.append("")
    pf = power_floor()
    L.append("    expected |delta| gap under asymmetric deference: %.2f"
             % pf["expected_gap"])
    L.append("")
    L.append("    %-8s %s" % ("n", "misread rate"))
    for r in pf["rows"]:
        L.append("    %-8d %.3f" % (r["n"], r["misread_rate"]))
    L.append("")
    L.extend(SH.wrap("Below about n = %s the symmetric and asymmetric cases "
                     "are not separable at a 5 percent misread rate, so the "
                     "verdict is not readable however the arms are run. The "
                     "protocol as stated names a discriminator and no "
                     "denominator; this is the denominator."
                     % pf["n_for_5pct"], "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    idn = identifiability(10.0, 2.0)
    ck("the DOWN arm cannot separate the two worlds",
       idn["down_arm_gap"] < 0.5)
    ck("the NONE arm does", idn["none_arm_gap"] > 1.0)
    ck("the UP arm does, and more strongly than NONE",
       idn["up_arm_gap"] > idn["none_arm_gap"])
    ck("so one arm is underdetermined and three are not -- the result is "
       "algebraic, not statistical",
       idn["down_arm_gap"] < idn["up_arm_gap"] / 3.0)

    sym = run_arms(10.0, 1.0, 5000, 0.01, 1, asym=1.0)
    ck("under symmetric deference the two deltas match in magnitude",
       abs(abs(sym["delta_up"]) - abs(sym["delta_down"])) < 0.05)
    ck("and they point opposite ways, which is what makes them a pair",
       sym["delta_up"] * sym["delta_down"] < 0)

    asy = run_arms(10.0, 1.0, 5000, 0.01, 1, asym=0.5)
    ck("under asymmetric deference they do not match, which is the failure "
       "mode the discriminator inherits",
       abs(abs(asy["delta_up"]) - abs(asy["delta_down"])) > 0.4)

    pf = power_floor(trials=60)
    ck("a power floor exists and is finite", pf["n_for_5pct"] is not None)
    ck("the misread rate falls with n, so the floor is not an artefact of "
       "the sweep", pf["rows"][-1]["misread_rate"]
       <= pf["rows"][0]["misread_rate"])
    ck("at the smallest n the discriminator is close to a coin flip",
       pf["rows"][0]["misread_rate"] > 0.15)

    ck("confidence is separate and unresolved", confidence()["resolved"]
       is False)
    ck("the asymmetric-deference limit is named in breaks",
       any("SYMMETRIC" in b for b in breaks()))
    ck("report renders", "second equation" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S2"))
