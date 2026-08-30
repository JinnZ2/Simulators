#!/usr/bin/env python3
"""Selftest for scheme.py and power.py. CC0. stdlib only. 3.9."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import power as P  # noqa: E402
import scheme as S  # noqa: E402


def run():
    ok, bad = [0], []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    src = open(os.path.join(HERE, "power.py"), encoding="utf-8").read()
    doc = S._doc()

    # -- 1. the scheme, parsed and complete
    chk("eight M-components", len(S.COMPONENTS) == 8)
    chk("named M1..M8", sorted(S.COMPONENTS) == ["M%d" % i
                                                 for i in range(1, 9)])
    chk("every one carries a label",
        all(v["label"] for v in S.COMPONENTS.values()))
    chk("every parsed label appears in the delivered text",
        all(v["label"] in doc for v in S.COMPONENTS.values()))
    chk("three S-codes", len(S.STORY_CODES) == 3)
    chk("four chain positions", len(S.CHAIN) == 4)
    chk("the coupling component is named as such in the drop",
        "coupling component" in doc
        and "coupling" in S.COMPONENTS[S.COUPLING]["gloss"])
    chk("M7 is the action rule",
        "ACTION" in S.COMPONENTS[S.ACTION]["label"])
    chk("M3 is the mechanism", "mechanism" in
        S.COMPONENTS[S.MECHANISM_STATED]["label"])

    # -- 2. nothing models a person, a valley, or an account
    body = src.split("# ---- a declared, arbitrary retention profile")[0]
    body = body.split("WHAT THIS FILE IS NOT")[1] if \
        "WHAT THIS FILE IS NOT" in body else body
    for w in ("valley", "informant", "account", "community"):
        chk("no %r is constructed as an object" % w,
            ("%s =" % w) not in src and ("class %s" % w.title())
            not in src)
    chk("the report says the study is not simulated",
        "IS NOT SIMULATED" in P.render())
    chk("and names the extraction hazard",
        "self-defeating" in P.render())
    chk("the retention profile is declared arbitrary",
        "arbitrary and declared" in P.PROFILE_NOTE)
    chk("and explicitly not a prediction",
        "NOT a prediction" in P.PROFILE_NOTE)

    # -- 3. the half-life's resolution
    h = P.halflife_resolution()
    chk("four levels", h["n_levels"] == 4)
    chk("three of them are ordered positions",
        h["ordered_positions"] == 3)
    chk("one is an open catch-all", h["open_bins"] == ["C3+"])
    chk("and its gloss is the absence of a chain",
        "no traceable chain" in h["open_bin_gloss"])
    chk("three intervals are available", h["intervals_available"] == 3)
    chk("the finest statement is an interval, not a value",
        "between" in h["finest_statement"])

    # -- 4. the bracket never interpolates
    b = P.halflife_bracket([8.0, 6.0, 3.0, 1.0])
    chk("a halving is bracketed", b["state"] == "BRACKETED")
    chk("between the two adjacent levels", b["bracket"] == ("C1", "C2"))
    chk("and never interpolated", b["interpolated"] is None)
    chk("with the reason stated",
        "ordinal" in b["why_not_interpolated"])
    flat = P.halflife_bracket([8.0, 8.0, 7.5, 7.0])
    chk("a curve that never halves is not bracketed",
        flat["state"] == "NOT_REACHED_ON_THIS_AXIS")
    chk("and that is not the same as no data",
        flat["state"] != P.halflife_bracket([])["state"])
    chk("no data is its own state",
        P.halflife_bracket([])["state"] == "NO_DATA")

    # -- 5. the three question forms cost differently, and the
    #       ordering of their costs is the finding
    n = 20
    a = P.order_recovery(n, P.PROFILE)["exact_order"]
    f = P.first_to_drop(n, P.PROFILE)["recovered_uniquely"]
    p = P.pair_recovery(n, 0.40, 0.60)["accuracy_on_decided"]
    chk("a pair is cheaper than one-against-seven", p > f)
    chk("which is cheaper than the full order", f > a)
    chk("the full order is out of reach at n=20", a < 0.05)
    chk("and a pair is within reach", p > 0.85)
    # and the ordering of costs holds at another n
    n2 = 40
    chk("the cost ordering holds at n=40",
        P.pair_recovery(n2, 0.40, 0.60)["accuracy_on_decided"]
        > P.first_to_drop(n2, P.PROFILE)["recovered_uniquely"]
        > P.order_recovery(n2, P.PROFILE)["exact_order"])

    # -- 6. the discriminators are not CONSTANT_SILENT or CONSTANT_FIRES
    chk("pair accuracy rises with n",
        P.pair_recovery(80, 0.40, 0.60)["accuracy_on_decided"]
        > P.pair_recovery(5, 0.40, 0.60)["accuracy_on_decided"])
    chk("and with effect size",
        P.pair_recovery(20, 0.35, 0.65)["accuracy_on_decided"]
        > P.pair_recovery(20, 0.45, 0.55)["accuracy_on_decided"])
    chk("full-order recovery rises with n",
        P.order_recovery(160, P.PROFILE)["exact_order"]
        > P.order_recovery(10, P.PROFILE)["exact_order"])
    chk("a zero-gap pair is at chance on decided runs",
        abs(P.pair_recovery(40, 0.5, 0.5)["accuracy_on_decided"]
            - 0.5) < 0.12)
    chk("first_to_drop names the true first",
        P.first_to_drop(20, P.PROFILE)["true_first"]
        == min(P.PROFILE, key=P.PROFILE.get))

    # -- 7. the report
    out = P.render()
    chk("it names every M-component", all(k in out for k in S.COMPONENTS))
    chk("it states the axis resolution", "between C0 and C1" in out)
    chk("it shows the three cost columns", "full 8-order" in out)
    chk("and says the ordering is the expensive form",
        "expensive form" in out)
    chk("it records that the companion scheme landed",
        "named-and-absent" in out)

    # -- 8. the screen
    sys.path.insert(0, os.path.join(P.ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    # --- scheme.py is a parser and refuses --selftest rather than
    # passing silently. A bare exit 0 on an invocation that runs nothing
    # is the DL_005 / CC_006 shape.
    import subprocess
    sp = os.path.join(HERE, "scheme.py")
    r = subprocess.run([sys.executable, sp, "--selftest"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("scheme.py refuses --selftest rather than exiting 0",
        r.returncode == 2)
    chk("and names where its checks live",
        b"selftest_power.py" in r.stderr)
    r2 = subprocess.run([sys.executable, sp],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("bare scheme.py renders the parsed scheme", r2.returncode == 0)
    chk("and the render names every component and chain position",
        all(k.encode() in r2.stdout for k in S.COMPONENTS)
        and all(c["position"].encode() in r2.stdout for c in S.CHAIN))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
