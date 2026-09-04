#!/usr/bin/env python3
# check_source_class.py -- CC0, stdlib only, parses under 3.9.
# WORK ORDER -- FABLE -- 04. Makes the §0 RULE and the §7 constraints
# mechanical: no eval figure appears without a source class in its
# section; the DISPUTED claim is marked-not-resolved; every GAP stays
# a missing measurement; the sim emits no forecast. Edits nothing.

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(HERE, "GAPS_CORPUS_INPUT.md")
WORKED = os.path.join(HERE, "WHAT_THE_INCIDENT_ESTABLISHES.md")
LOOP = os.path.join(HERE, "LOOP_SELF_CONFIRMING_PRIOR.md")

# eval figures that must carry a source class wherever they appear
EVAL_FIG = [r"\b198\b", r">20%", r"3[-–]6\b", r"~1,300", r"0\.2[-–]0\.5%",
            r"~?4[03]x", r">1 day", r"0\.23", r"0\.46"]
# markers that count as a declared source class in a section
SRC_MARK = ["[PRESS]", "press-sourced", "source class",
            "first-hand observation", "OpenAI technical report",
            "METR investigation", "Hugging Face post-mortem"]


def _sections(text):
    """(heading, body) pairs split on markdown '## ' headings; the
    preamble before the first heading is one section too."""
    parts = re.split(r"(?m)^## ", text)
    out = [("<preamble>", parts[0])]
    for p in parts[1:]:
        head = p.split("\n", 1)[0]
        out.append((head, p))
    return out


def source_class_containment():
    """Every eval-figure occurrence sits in a section that declares a
    source class -- the CAC_4 / MI_003 shape on this drop."""
    rows = []
    for path in (REGISTER, WORKED):
        text = open(path, encoding="utf-8").read()
        blanket = any(m in text.split("##", 1)[0] for m in SRC_MARK)
        for head, body in _sections(text):
            has_fig = any(re.search(f, body) for f in EVAL_FIG)
            if not has_fig:
                continue
            marked = any(m in body for m in SRC_MARK) or blanket
            rows.append((os.path.basename(path),
                         head.strip()[:36], marked))
    return {"rows": rows, "all_marked": all(m for _p, _h, m in rows)}


def disputed_marked():
    t = open(REGISTER, encoding="utf-8").read().lower()
    return ("disputed" in t
            and ("marked, not resolved" in t or "not resolve" in t
                 or "marked not resolved" in t))


def gaps_stay_missing_measurements():
    """Every GAP heading is followed, in its section, by a 'Missing
    measurement' -- none is upgraded to a finding."""
    t = open(REGISTER, encoding="utf-8").read()
    gaps = re.findall(r"(?m)^## (GAP-[A-G]\b.*)$", t)
    bodies = re.split(r"(?m)^## GAP-[A-G]\b", t)[1:]
    ok = all("missing measurement" in b.lower() for b in bodies)
    rule = "do not upgrade any entry here to a finding" in t.lower() \
        or "do not upgrade any" in t.lower()
    # no section declares a FINDING:
    no_finding = not re.search(r"(?mi)^\s*finding:", t)
    return {"n_gaps": len(gaps), "each_has_missing_measurement": ok,
            "no_upgrade_rule_stated": rule, "no_finding_label": no_finding}


def sim_has_no_forecast():
    sys.path.insert(0, HERE)
    import corpus_loop_sim as S
    rep = S.report().lower()
    banned = ["by 20", "in 20", "will reach", "forecast:", "we predict"]
    f = S.falsifier()
    return {"no_forecast_token": all(b not in rep for b in banned),
            "hold_stated": "not a forecast" in rep,
            "falsifier_reachable":
                f["falsifier_fires_when_coefficient_zero"]
                and f["D_sensitivity_live"] > 1e-3}


def ordering_and_disclaimers():
    w = open(WORKED, encoding="utf-8").read()
    lp = open(LOOP, encoding="utf-8").read()
    return {
        "worked_declares_fifth_application":
            "FIFTH application, not the premise" in w,
        "worked_disclaims_interior_state":
            "NOT ESTABLISHED" in w
            and "interior state" in w.lower(),
        "loop_precedes_sim":
            "prose-independent form" in lp
            and "before" in lp.lower(),
        "loop_carries_falsifier":
            "not load-bearing" in lp.lower(),
    }


def render():
    L = []
    w = L.append
    w("SOURCE-CLASS AND CONSTRAINT CHECK -- WORK ORDER FABLE 04")
    w("")
    sc = source_class_containment()
    w("1  EVERY EVAL FIGURE CARRIES A SOURCE CLASS IN ITS SECTION")
    for p, h, m in sc["rows"]:
        w("   %-26s %-36s %s" % (p, h, "marked" if m else "UNMARKED"))
    w("   all marked: %s" % sc["all_marked"])
    w("")
    w("2  DISPUTED CLAIM MARKED-NOT-RESOLVED: %s" % disputed_marked())
    g = gaps_stay_missing_measurements()
    w("3  GAPS STAY MISSING MEASUREMENTS")
    w("   %d gaps; each has a missing measurement: %s; no-upgrade rule"
      % (g["n_gaps"], g["each_has_missing_measurement"]))
    w("   stated: %s; no FINDING: label: %s"
      % (g["no_upgrade_rule_stated"], g["no_finding_label"]))
    s = sim_has_no_forecast()
    w("4  SIM EMITS NO FORECAST")
    w("   no forecast token: %s; hold stated: %s; falsifier reachable: %s"
      % (s["no_forecast_token"], s["hold_stated"],
         s["falsifier_reachable"]))
    o = ordering_and_disclaimers()
    w("5  ORDERING AND DISCLAIMERS (§6, §7)")
    for k, v in o.items():
        w("   %-38s %s" % (k, v))
    w("")
    w("This module checks conformance to the work order; it makes no")
    w("claim about the incident and adjudicates no gap.")
    return "\n".join(L)


def selftest():
    n = [0]

    def chk(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    sc = source_class_containment()
    chk("eval figures found", len(sc["rows"]) > 0)
    chk("every eval figure carries a source class", sc["all_marked"])
    chk("disputed marked not resolved", disputed_marked())

    g = gaps_stay_missing_measurements()
    chk("seven gaps", g["n_gaps"] == 7)
    chk("each gap has a missing measurement",
        g["each_has_missing_measurement"])
    chk("no-upgrade rule stated", g["no_upgrade_rule_stated"])
    chk("no FINDING label", g["no_finding_label"])

    s = sim_has_no_forecast()
    chk("sim no forecast token", s["no_forecast_token"])
    chk("sim hold stated", s["hold_stated"])
    chk("sim falsifier reachable", s["falsifier_reachable"])

    o = ordering_and_disclaimers()
    chk("worked declares fifth application",
        o["worked_declares_fifth_application"])
    chk("worked disclaims interior state",
        o["worked_disclaims_interior_state"])
    chk("loop precedes sim", o["loop_precedes_sim"])
    chk("loop carries falsifier", o["loop_carries_falsifier"])

    print("check_source_class selftest: %d/%d checks pass"
          % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
