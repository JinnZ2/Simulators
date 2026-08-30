#!/usr/bin/env python3
# selftest_oir.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises pipeline.py, ensembles.py and audit.py.
#
# The load-bearing checks are the two the spec turns on: the falsifiable
# condition FIRES (flipping -> empty) and does not always fire (stable ->
# rules); and step 3 is a MISS filter that is BLIND to false alarms,
# which is the finding.

import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P  # noqa: E402
import ensembles as ENS  # noqa: E402
import audit as A  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    doc = io.open(os.path.join(HERE, "SOURCE_DROP.md"),
                  encoding="utf-8").read()

    # ---- step 2: t_wet is the first threshold crossing, INF if never
    lm = P.Landmark("x", 2.0)
    field = {"r": {"x": [0.0, 1.0, 2.0, 5.0]}}
    chk("t_wet is the first crossing", P.t_wet(field, lm, "r") == 2)
    field2 = {"r": {"x": [0.0, 1.0, 1.5]}}
    chk("t_wet is INF when never crossed",
        P.t_wet(field2, lm, "r") == P.INF)

    # ---- step 3: the falsifiable condition, both directions
    f = A.falsifiable_fires()
    chk("flipping ensemble returns empty output", f["flipping_empty"])
    chk("stable ensemble returns rules", f["stable_nonempty"])
    chk("so the pipeline is not CONSTANT_FIRES", f["honest"])
    # and the spec states empty output is valid
    chk("the spec says empty output is honest",
        "Empty output is a valid, honest result" in " ".join(doc.split()))

    # ---- the ordinal bet: order stable, magnitude not
    ls, fs, rs, h, _m = ENS.stable()
    stable = P.stable_pairs(ls, fs, rs)
    chk("all three pairs are stable in the stable ensemble",
        len(stable) == 3)
    lb = P.lead(ls[0], ls[2], fs, rs)     # bridge -> house
    chk("the lead is a band, not a point", lb["p90"] > lb["min"])
    chk("the band is wide (magnitude varies)",
        lb["p90"] - lb["min"] >= lb["min"])

    # ---- plan against the short end: card uses min/p10, never median
    src = io.open(os.path.join(HERE, "pipeline.py"), encoding="utf-8").read()
    card_fn = src.split("def build_card")[1].split("\ndef ")[0]
    chk("the card uses the short end (min)", '["min"]' in card_fn)
    chk("the card does not use the median (p50)", '["p50"]' not in card_fn)

    # ---- RESULT: step 3 is a MISS filter, blind to false alarms
    fa = A.false_alarm_blindness()
    chk("a stable-order trigger is kept by step 3",
        fa["trigger_kept_by_step3"])
    chk("its miss rate is ~0 (step 3 forces it)", fa["miss_rate"] == 0.0)
    chk("its false-alarm rate is high (step 3 does not constrain it)",
        fa["false_alarm_rate"] and fa["false_alarm_rate"] >= 0.4)
    chk("so step 3 keeps a trigger that cries wolf",
        fa["false_alarm"] > 0 and fa["trigger_kept_by_step3"])

    # ---- reliability(): both error rates, and their asymmetry
    lms, field3, runs, hh, _mt = ENS.false_alarm_heavy()
    trig = [x for x in lms if x.id == "upstream_culvert"][0]
    rel = P.reliability(trig, hh, field3, runs)
    chk("reliability reports a miss rate", rel["miss_rate"] is not None)
    chk("and a false-alarm rate", rel["false_alarm_rate"] is not None)
    chk("the false alarms outnumber-or-equal misses here",
        rel["false_alarm"] >= rel["miss"])
    # null: a trigger identical to the hazard has neither error
    self_rel = P.reliability(hh, hh, field3, runs)
    chk("a trigger identical to the hazard has zero false alarms",
        self_rel["false_alarm"] == 0 and self_rel["miss"] == 0)

    # ---- the card carries the REL line the spec's card omits
    r = P.derive(lms, field3, runs, household=hh, movement_time=1)
    card = P.build_card(r["card_rule"])
    chk("the built card carries a false-alarm rate", "false-alarm rate" in card)
    chk("the spec's own card template does NOT",
        "false-alarm" not in doc and "false alarm" not in doc)

    # ---- step 5: route coupling -- trigger upstream of the door
    chk("the trigger is not the household",
        r["card_rule"]["trigger"] != "household")
    chk("the trigger wets before the route closes",
        r["card_rule"]["trigger_wets_by"]
        <= r["card_rule"]["t_route_short"])

    # ---- over-strict tie handling, the safe direction
    st = A.strict_tie_handling()
    chk("strict sign-invariance drops a tied pair",
        not st["strict_keeps_it"])
    chk("the weak order would have kept it", st["weak_would_keep_it"])
    chk("so the criterion is over-strict (drops, never invents)",
        st["over_strict"])

    # ---- neither-wet runs excluded
    nw = A.neither_wet_excluded()
    chk("a neither-wet run is excluded from the pair check",
        nw["neither_run_excluded"])
    chk("and the pair stays stable on informative runs",
        nw["pair_still_stable"])

    # ---- the router is an input; nothing runs a solver, nothing is real
    allsrc = src + io.open(os.path.join(HERE, "ensembles.py"),
                           encoding="utf-8").read() + \
        io.open(os.path.join(HERE, "audit.py"), encoding="utf-8").read()
    import re as _re
    chk("no hydraulic solver is imported or called",
        not _re.search(r"\bhec\b|\bHEC-RAS\b", allsrc, _re.I)
        and not _re.search(r"\bsolve\s*\(", allsrc))
    chk("the depth field is consumed, not computed -- t_wet reads a series",
        "series[" in src or "for t, d in enumerate(series)" in src)
    # ensembles declare themselves synthetic
    ens = io.open(os.path.join(HERE, "ensembles.py"), encoding="utf-8").read()
    chk("the ensembles declare they are synthetic",
        "SYNTHETIC" in ens and "NOTHING HERE IS A REAL PLACE" in ens)

    # ---- the reports
    out = A.render()
    one = " ".join(out.split())
    chk("the audit states the router is an input",
        "router output is an" in one)
    chk("it names the finding as false-alarm blindness",
        "BLIND TO FALSE ALARMS" in out)
    chk("it states nothing is a real community",
        "not a real community" in one or "Nothing is a real" in one)
    chk("it marks the over-strict criterion a containment",
        "containment" in one)

    # ---- both auxiliaries refuse --selftest
    for mod in ("pipeline.py", "audit.py"):
        rr = subprocess.run([sys.executable, os.path.join(HERE, mod),
                             "--selftest"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, rr.returncode == 2)
        chk("%s names where its checks live" % mod,
            b"selftest_oir.py" in rr.stderr)

    # ---- the no-severity screen, with two DECLARED subject-word
    # exemptions measured by the three-arm harness. `alarm` and `error`
    # are the finding's own vocabulary -- the finding IS that the card
    # omits the false-ALARM rate and the ERROR rates -- and cannot be
    # stated without the tokens. Everything else is reworded.
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    import re as _re2
    EXEMPT = ("alarm", "error")
    chk("two subject-word exemptions", len(EXEMPT) == 2)
    masked = out
    for wd in EXEMPT:
        masked = _re2.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), masked)
    chk("the audit report is clean apart from the exemptions",
        not no_severity.hits(masked))
    fired = set(w for _n, w, _l in no_severity.hits(out))
    chk("and the exemptions are the only tokens that fire",
        fired == set(EXEMPT))
    pmask = out + "\nthis design is broken and the result is invalid\n"
    for wd in EXEMPT:
        pmask = _re2.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), pmask)
    chk("a planted violation is still caught through the exemptions",
        bool(no_severity.hits(pmask)))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
