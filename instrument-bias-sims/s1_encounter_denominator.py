#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s1_encounter_denominator.py - event-sampled observation reconstructs a false
baseline.

    python3 s1_encounter_denominator.py
    python3 s1_encounter_denominator.py --selftest

N dyads on a continuous timeline. Two observers see the same system:

  A  continuous (resident). samples every tick.
  B  event-triggered (visitor / camera / mortality table). samples only when
     something is happening.

The claim under test: at low contested_fraction f, B reports a competitive
system that is >95% null time.

WHERE IT BREAKS, stated before the result. A pure event trigger excludes NULL
by definition, so at duty_cycle 0 the headline is close to analytic rather
than empirical -- the sim is showing the size of a bias it built in. Two
things are not analytic and are what the module is for: how the distortion
scales with f, and what the mortality weighting does on top of it. A
duty_cycle parameter is included so B can be made to converge on A, which is
the check that the result is a statement about the SAMPLING RULE and not
about observers.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import argparse
import random
import sys

STATES = ("NULL", "BOUNDARY_TEST", "CONCEDE", "ESCALATE")

# Relative weights within contested time, and the cost carried by each state.
# Cost is a magnitude, not a valuation: it is what a mortality table records.
CONTESTED_MIX = {"BOUNDARY_TEST": 0.80, "CONCEDE": 0.19, "ESCALATE": 0.01}
STATE_COST = {"NULL": 0.0, "BOUNDARY_TEST": 1.0, "CONCEDE": 0.5,
              "ESCALATE": 100.0}


def timeline(n_dyads, ticks, f, seed):
    """Ground truth: a state per dyad per tick."""
    rng = random.Random(seed)
    keys = list(CONTESTED_MIX)
    wts = [CONTESTED_MIX[k] for k in keys]
    out = []
    for _ in range(n_dyads):
        row = []
        for _ in range(ticks):
            if rng.random() < f:
                row.append(rng.choices(keys, weights=wts, k=1)[0])
            else:
                row.append("NULL")
        out.append(row)
    return out


def observe_continuous(tl):
    counts = dict((s, 0) for s in STATES)
    for row in tl:
        for s in row:
            counts[s] += 1
    total = sum(counts.values())
    return {"counts": counts,
            "composition": dict((s, counts[s] / total) for s in STATES),
            "n_samples": total}


def observe_event(tl, duty_cycle=0.0, mortality_weighted=False, seed=0):
    """B samples on trigger, plus an optional duty cycle of blind sampling.

    duty_cycle 0.0  = pure event trigger, NULL never sampled
    duty_cycle 1.0  = samples everything, converges on A
    mortality_weighted = sample probability proportional to STATE_COST, which
                         is what a mortality table or an incident report is
    """
    rng = random.Random(seed)
    counts = dict((s, 0) for s in STATES)
    maxcost = max(STATE_COST.values())
    for row in tl:
        for s in row:
            if s == "NULL":
                if rng.random() < duty_cycle:
                    counts[s] += 1
                continue
            if mortality_weighted:
                if rng.random() < STATE_COST[s] / maxcost:
                    counts[s] += 1
            else:
                counts[s] += 1
    total = sum(counts.values())
    if total == 0:
        return {"counts": counts, "composition": None, "n_samples": 0,
                "state": "NO_SAMPLES"}
    return {"counts": counts,
            "composition": dict((s, counts[s] / total) for s in STATES),
            "n_samples": total, "state": "OK"}


def sweep(f_values, n_dyads=40, ticks=400, seed=11):
    rows = []
    for f in f_values:
        tl = timeline(n_dyads, ticks, f, seed)
        a = observe_continuous(tl)
        b = observe_event(tl, duty_cycle=0.0, seed=seed)
        bm = observe_event(tl, duty_cycle=0.0, mortality_weighted=True,
                           seed=seed)
        rows.append({
            "f": f,
            "true_null_share": a["composition"]["NULL"],
            "B_null_share": b["composition"]["NULL"] if b["composition"]
            else None,
            "true_escalate_share": a["composition"]["ESCALATE"],
            "B_escalate_share": b["composition"]["ESCALATE"]
            if b["composition"] else None,
            "B_mortality_escalate_share": bm["composition"]["ESCALATE"]
            if bm["composition"] else None,
            "B_samples": b["n_samples"],
            "B_mortality_samples": bm["n_samples"],
        })
    return rows


def duty_convergence(f=0.02, duties=(0.0, 0.01, 0.1, 0.5, 1.0),
                     n_dyads=40, ticks=400, seed=11):
    """The check that this is about the sampling rule, not about B."""
    tl = timeline(n_dyads, ticks, f, seed)
    a = observe_continuous(tl)
    out = []
    for d in duties:
        b = observe_event(tl, duty_cycle=d, seed=seed)
        err = abs(b["composition"]["NULL"] - a["composition"]["NULL"])
        out.append({"duty_cycle": d, "B_null_share": b["composition"]["NULL"],
                    "abs_error_vs_A": err})
    return {"true_null_share": a["composition"]["NULL"], "rows": out}


def confidence():
    """Reported separately from the pattern, and not resolved.

    The pattern is a numeric consequence of the sampling rule and is as solid
    as the rule. Whether any named real observer samples this way is a
    separate question this module does not touch.
    """
    return {"pattern": "arithmetic consequence of the declared sampling rule",
            "mapping_to_any_real_observer": "NOT_ESTABLISHED_HERE",
            "resolved": False}


def breaks():
    return [
        "at duty_cycle 0 the headline is near-analytic: an event trigger "
        "excludes NULL by definition, so the sim measures the size of a bias "
        "it built in. What is not analytic is the SCALING with f and the "
        "mortality interaction",
        "the contested mix and the cost table are stipulated. ESCALATE at 1% "
        "of contested time and cost 100 are plausible round numbers, not "
        "measurements, and the mortality result moves with both",
        "a real camera has a duty cycle. duty_convergence() shows B tracking "
        "A as it rises, so the finding is about the sampling rule and not "
        "about a class of observer",
        "no real dyadic dataset is used anywhere in this file",
    ]


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip()); cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def report():
    L = []
    L.append("S1 -- ENCOUNTER DENOMINATOR")
    L.append("=" * 72)
    L.append("")
    L.extend(_wrap("Two observers, one system. A samples every tick. B "
                   "samples only when something is happening.", "  "))
    L.append("")
    L.append("  %-8s %-12s %-12s %-12s %s"
             % ("f", "true null", "B null", "true escl", "B escl"))
    for r in sweep([0.001, 0.005, 0.02, 0.05, 0.1, 0.2]):
        L.append("  %-8.3f %-12.4f %-12.4f %-12.5f %.5f"
                 % (r["f"], r["true_null_share"], r["B_null_share"],
                    r["true_escalate_share"], r["B_escalate_share"]))
    L.append("")
    L.extend(_wrap("B's null share is 0.0000 at every f, by construction. The "
                   "column carrying information is the true one: at f = 0.001 "
                   "the system is 99.9 percent null time and B reports a "
                   "composition with no null in it at all.", "  "))
    L.append("")
    L.append("  MORTALITY-WEIGHTED SECOND PASS")
    L.append("")
    L.append("  %-8s %-14s %-16s %s"
             % ("f", "true escl", "B escl", "B mortality escl"))
    for r in sweep([0.001, 0.02, 0.2]):
        L.append("  %-8.3f %-14.5f %-16.5f %.5f"
                 % (r["f"], r["true_escalate_share"], r["B_escalate_share"],
                    r["B_mortality_escalate_share"]))
    L.append("")
    L.extend(_wrap("Rare high-cost events do dominate the mortality-weighted "
                   "model, and the distortion is a PRODUCT of two factors: "
                   "event triggering removes the null baseline, then cost "
                   "weighting re-weights what is left. Neither alone gives "
                   "the final composition.", "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    dc = duty_convergence()
    L.append("  DUTY CYCLE -- the check that this is about the sampling rule")
    L.append("")
    L.append("  true null share %.4f" % dc["true_null_share"])
    L.append("  %-12s %-14s %s" % ("duty", "B null share", "abs error vs A"))
    for r in dc["rows"]:
        L.append("  %-12.2f %-14.4f %.4f"
                 % (r["duty_cycle"], r["B_null_share"], r["abs_error_vs_A"]))
    L.append("")
    L.extend(_wrap("B converges on A as the duty cycle rises. So the finding "
                   "is a property of the sampling rule and not of a class of "
                   "observer, which is the difference between a measurement "
                   "and a characterisation.", "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    c = confidence()
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k2 in sorted(c):
        L.append("    %-36s %s" % (k2, c[k2]))
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        L.extend(_wrap("- " + b, "    "))
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(lb, c):
        nonlocal f, k
        k += 1
        if not c:
            f += 1
            print("FAIL %s" % lb)

    tl = timeline(20, 200, 0.05, 3)
    a = observe_continuous(tl)
    ck("continuous observer sees every tick", a["n_samples"] == 20 * 200)
    ck("true null share tracks 1-f",
       abs(a["composition"]["NULL"] - 0.95) < 0.03)

    b = observe_event(tl, duty_cycle=0.0, seed=3)
    ck("pure event trigger never samples NULL", b["counts"]["NULL"] == 0)
    ck("and therefore reports zero null share",
       b["composition"]["NULL"] == 0.0)

    s = sweep([0.001, 0.1])
    ck("the claim holds: at low f the true system is >95 percent null while "
       "B reports none",
       s[0]["true_null_share"] > 0.95 and s[0]["B_null_share"] == 0.0)
    ck("and the true null share falls as f rises, so the sweep is not flat",
       s[0]["true_null_share"] > s[1]["true_null_share"])

    hi = sweep([0.02])[0]
    ck("mortality weighting raises the escalate share above the plain event "
       "reading", hi["B_mortality_escalate_share"] > hi["B_escalate_share"])
    ck("and both exceed the truth, so the two distortions compound",
       hi["B_escalate_share"] > hi["true_escalate_share"])

    dc = duty_convergence()
    ck("B converges on A as duty cycle rises",
       dc["rows"][-1]["abs_error_vs_A"] < dc["rows"][0]["abs_error_vs_A"])
    ck("at duty 1.0 B matches A", dc["rows"][-1]["abs_error_vs_A"] < 1e-9)

    ck("an empty trigger set returns NO_SAMPLES rather than a composition",
       observe_event(timeline(2, 50, 0.0, 1))["state"] == "NO_SAMPLES")
    ck("confidence is a separate readout and is not resolved",
       confidence()["resolved"] is False)
    ck("breaks are stated and non-empty", len(breaks()) >= 3)
    ck("report renders", "DUTY CYCLE" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="S1")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
