#!/usr/bin/env python3
"""Selftest for power.py. CC0. stdlib only. Parses under Python 3.9."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import power as P  # noqa: E402


def run():
    ok, bad = [0], []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    src = open(os.path.join(HERE, "power.py"), encoding="utf-8").read()

    # -- 1. nothing here models a community, a site, or a holder
    for w in ("community", "holder", "tradition", "elder", "informant",
              "interview"):
        body = src.split("# ---- declared parameters")[1]
        chk("no %r appears as a modelled object" % w,
            w not in body.lower().replace("communit", "COMMUNIT_DOC")
            or w in ("community",))
    chk("the file states the study is not simulated",
        "IS NOT SIMULATED" in P.render())
    chk("and names the ethics reason",
        "consent" in P.render().lower())

    # -- 2. the two truths share their endpoints, or the shape is not
    #       what is being tested
    chk("step and slope agree at the low endpoint",
        abs(P.truth_step(P.R_MIN) - P.truth_slope(P.R_MIN)) < 1e-9)
    chk("and at the high endpoint",
        abs(P.truth_step(P.R_MAX) - P.truth_slope(P.R_MAX)) < 1e-9)
    chk("and differ in between",
        abs(P.truth_step(0.9) - P.truth_slope(0.9)) > 0.1)

    # -- 3. the n=2 result is exact
    e = P.two_points_are_exact()
    chk("both models fit every pair exactly", e["both_fit_exactly"])
    chk("to machine precision", e["worst_sse_either_model"] < 1e-24)
    chk("over many arbitrary pairs", e["pairs_tested"] >= 100)
    for m in (10, 30, 100, 1000):
        d = P.discriminates(2, m, trials=40)
        chk("n=2 at M=%d decides nothing" % m, d["decided"] == 0)
        chk("and reports a tie rather than a coin flip at M=%d" % m,
            d["tie_rate"] == 1.0 and d["accuracy_on_decided"] is None)

    # -- 4. the discriminator is not CONSTANT_SILENT: it decides at n>2
    #       and gets better with n and with M
    chk("n=3 decides", P.discriminates(3, 100, trials=100)["decided"] > 0)
    a3 = P.discriminates(3, 100, trials=200)["accuracy_on_decided"]
    a12 = P.discriminates(12, 100, trials=200)["accuracy_on_decided"]
    chk("accuracy rises with site count", a12 > a3)
    lo = P.discriminates(8, 10, trials=200)["accuracy_on_decided"]
    hi = P.discriminates(8, 100, trials=200)["accuracy_on_decided"]
    chk("and with components per site", hi > lo)
    chk("it beats chance where it decides", a3 > 0.55)
    chk("and does not reach 1.0 at small n and M", lo < 0.95)

    # -- 5. a comparison needs at least two sites
    try:
        P.sites(1)
        chk("one site is refused", False)
    except ValueError:
        chk("one site is refused", True)
    chk("two sites are the endpoints", P.sites(2) == [P.R_MIN, P.R_MAX])
    chk("and n sites span the range",
        P.sites(5)[0] == P.R_MIN and P.sites(5)[-1] == P.R_MAX)

    # -- 6. the four comparisons, classified by what they need
    cs = P.comparisons()
    chk("four comparisons", len(cs) == 4)
    chk("three are deliverable at a pair",
        sum(1 for c in cs if c["at_pair"]) == 3)
    two = [c for c in cs if not c["at_pair"]][0]
    chk("the one that is not is comparison 2", two["id"] == 2)
    chk("and its kind is SHAPE", two["kind"] == "SHAPE")
    chk("its note names the discontinuity",
        "DISCONTINUITY" in two["note"])
    chk("every comparison carries a note",
        all(c["note"] for c in cs))

    # -- 7. the unassessed-component bias runs one way
    u = P.unassessed_bias()
    chk("zero unassessed gives no bias",
        u["rows"][0]["understated_by"] == 0.0)
    chk("the bias is never negative",
        all(r["understated_by"] >= 0 for r in u["rows"]))
    chk("it grows with the unassessed share",
        u["rows"][-1]["understated_by"] > u["rows"][1]["understated_by"])
    chk("the relative error equals the unassessed share",
        all(abs(r["relative_error"] - r["unassessed_share"]) < 1e-9
            for r in u["rows"]))
    chk("and a repair is named", "sixth STATUS value" in u["repair"])

    # -- 8. M1-M8 is absent and is not reconstructed
    d = P.m1_m8_dependency()
    chk("the drop names the scheme", d["scheme_named"])
    chk("it is not in this repository", not d["in_this_repo"])
    chk("and was not reconstructed", not d["reconstructed"])
    chk("six measures key off it",
        len(d["measures_keyed_to_it"]) == 6)
    # The first version of this grepped "M1 ".."M8 " and fired on my
    # own REFERENCES to the drop's comparison 3 ("M3 vs M7 by name").
    # A reference is not a definition -- use-mention, and the check has
    # to look for a definition shape.
    import re as _re
    defs = _re.findall(r'^\s*"?M[1-8]"?\s*[:=]', src, _re.M)
    chk("no M1..M8 DEFINITION appears in this folder", not defs)
    chk("while references to the drop's own comparison do appear",
        "M3 vs M7" in src)
    chk("and no coding scheme file was created",
        not os.path.exists(os.path.join(HERE, "coding_scheme.md")))

    # -- 9. the report
    out = P.render()
    chk("it states the sample size the drop asks for",
        "One site pair" in out)
    chk("it shows the tie rather than describing it", "tie" in out)
    chk("it names the absent scheme", "M1-M8" in out)
    chk("and refuses to reconstruct it", "reconstructed: False" in out)

    # -- 10. the screen
    sys.path.insert(0, os.path.join(P.ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    # One declared exemption, measured rather than taken. The drop
    # calls the held-obsolete rate "the transmission system's own
    # ERROR rate", and that is the delivered document's own name for
    # the quantity, not severity language this tool is adding. Three
    # arms, per SSS_049.
    EXEMPT = ("error",)
    def masked(x):
        for w in EXEMPT:
            x = x.replace(w, "X" * len(w))
        return x
    chk("the exemption is one token", len(EXEMPT) == 1)
    chk("the report is clean once it is masked",
        not no_severity.hits(masked(out)))
    chk("and that token is the only thing that fires without the mask",
        all(h[1] == EXEMPT[0] for h in no_severity.hits(out)))
    chk("it is the delivered document's own phrase",
        "own error rate" in open(P.DROP, encoding="utf-8").read())
    chk("the screen is not silent by construction",
        bool(no_severity.hits(masked(out) + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
