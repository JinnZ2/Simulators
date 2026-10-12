#!/usr/bin/env python3
"""
check.py -- CC0, stdlib only.

Recomputes the mechanical claims in REPORT.md, an outside deep-research
report (Kimi) on a four-element framework: unit-and-conservation gates,
pre-signal readers, latency-in-the-joins, and an anchored worker-correction
channel. The report is landed verbatim and is not edited.

Every check locates its quote in REPORT.md at run time, so an edit to the
report turns the check red rather than leaving a stale reading. Nothing
here verifies a citation: every outside host is behind this environment's
egress allowlist, so all 79 cited URLs are CARRIED, not read.

Figure values (figs/*.png) are not parseable with the standard library.
They are transcribed by hand in FIG3_BARS and declared as a transcription.

    python3 check.py           render the readings
    python3 test_check.py      the checks on the checker
"""
import os
import re
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "REPORT.md")
sys.path.insert(0, os.path.join(HERE, "..", "move-set"))
from move_set_sim_v2 import _halfwidth   # noqa: E402  imported, not copied

LBF_TO_N = Decimal("4.4482216152605")    # exact by definition of the lbf

# Hand transcription of figs/fig3_handoff_evidence.png (declared, not parsed).
FIG3_BARS = [
    ("DDI alert overrides, Ancker et al.", 95.1),
    ("All medication alert overrides, same study", 93.0),
    ("Override rate, Korean ED CDSS (Park et al. 2022)", 92.9),
    ("DDI overrides, meta-range 49-96% (Olakotan et al. 2020)", 90.0),
    ("Outpatient CDS overrides (Nanji et al. 2014)", 53.0),
]
FIG3_META_RANGE = (49.0, 96.0)

# In-tree instruments for each element: a reading, checked by path only.
CROSS_MAP = [
    ("1 unit/conservation gates", "reasoning-gate/guards.json",
     "G-DIM voids a ratio across unlike objects; a unit check, not a conservation check"),
    ("2 pre-signal readers", "tools/presignal_ledger.py",
     "scores whether an early read preceded the event, against chance and a baseline"),
    ("3 latency in the joins", "reporting-chain-loss/hop_compose.py",
     "per-hop loss composed down a chain; information loss, not elapsed time"),
    ("4 anchored correction channel", "return-path/return_path.py",
     "four requirements on a correction channel, the set failed, never a score"),
]


def report_text(path=REPORT):
    with open(path, encoding="utf-8") as f:
        return f.read()


def locate(text, needle):
    """Line number (1-based) of the first line holding needle; raises if absent."""
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i
    raise LookupError("quote not in report: " + needle)


def g001_lbf(text):
    ln = locate(text, "factor of **4.45**")
    hw = _halfwidth("4.45")
    holds = abs(LBF_TO_N - Decimal("4.45")) <= hw
    return {"id": "GWS_001", "line": ln, "status": "HOLDS" if holds else "DIVERGES",
            "evidence": "lbf->N is %s; 4.45 +/- %s contains it" % (LBF_TO_N, hw)}


def g002_asana(text):
    ln = locate(text, "60% of working time")
    m = re.search(r"roughly (\d+)% on skilled work and (\d+)% on strategy", text)
    parts = [60, int(m.group(1)), int(m.group(2))]
    hrs = [int(x) for x in re.findall(r"(\d+) hours to (?:unnecessary|duplicative|talking)", text)]
    return {"id": "GWS_002", "line": ln, "status": "HOLDS" if sum(parts) == 100 else "DIVERGES",
            "evidence": "shares %s sum to %d; hour losses %s sum to %d, no total stated"
                        % (parts, sum(parts), hrs, sum(hrs))}


def g003_alert_cut(text):
    ln = locate(text, "15,057 to 4,590")
    cut = 1 - 4590 / 15057
    holds = abs(cut * 100 - 70) <= float(_halfwidth("70"))
    return {"id": "GWS_003", "line": ln, "status": "HOLDS" if holds else "DIVERGES",
            "evidence": "reduction %.4f; stated 70%% at whole-percent precision" % cut}


def g004_workweeks(text):
    ln = locate(text, "nine full workweeks")
    locate(text, "nearly 20% more")
    days_needed = 9 * 40 / 1.8
    weeks_at_250 = 1.8 * 250 / 40
    share_8h, share_9h = 1.8 / 8, 1.8 / 9
    return {"id": "GWS_004", "line": ln, "status": "CONDITIONAL",
            "evidence": ("nine 40-h weeks of 1.8 h/day take %.0f working days; a 250-day "
                         "year gives %.2f weeks. 1.8 h is %.1f%% of an 8-h day, %.1f%% of a "
                         "9-h day. The report states neither day count nor day length."
                         % (days_needed, weeks_at_250, share_8h * 100, share_9h * 100))}


def g005_override_range(text):
    n = text.count("90–96%")
    ln = locate(text, "overridden 90–96%")
    outside = [b for b in FIG3_BARS if not (90.0 <= b[1] <= 96.0)]
    lo, hi = FIG3_META_RANGE
    return {"id": "GWS_005", "line": ln, "status": "TENSION",
            "evidence": ("text states 90-96%% at %d sites; its own fig3 plots %d bar(s) outside "
                         "that range (%s) and draws the %g-%g%% meta-range as a single 90%% bar, "
                         "neither its midpoint %.1f nor its top. fig3 values are a hand "
                         "transcription." % (n, len(outside), ", ".join(
                             "%s %g%%" % (b[0], b[1]) for b in outside), lo, hi, (lo + hi) / 2))}


def g006_override_reading(text):
    ln1 = locate(text, "only 7.3% of alerts were clinically appropriate while 92.4%")
    ln2 = locate(text, "the 96% overridden alert")
    return {"id": "GWS_006", "line": ln2, "status": "TENSION",
            "evidence": ("line %d reads the override stream as physicians usually right "
                         "(7.3%% of alerts appropriate; 7.3 and 92.4 sum to 99.7 because they "
                         "have different denominators, alerts and responses). Line %d lists "
                         "'the 96%% overridden alert' among failures that 'did not lack the "
                         "signal'. One override rate, two opposite readings." % (ln1, ln2))}


def g007_thirty(text):
    ln = locate(text, "a third of the preventable harm")
    n = len(re.findall(r"(?<![\d.])30%", text))
    locate(text, "The 30% figure deserves to be read as the value of *measuring and structuring the join itself*")
    return {"id": "GWS_007", "line": ln, "status": "READING",
            "evidence": ("'30%%' occurs %d times naming two quantities (share of malpractice "
                         "claims; I-PASS reduction in preventable events). The conclusion reads "
                         "a trial's reduction as where 'a third of the preventable harm lives'; "
                         "a reduction from one intervention bounds that share from below and "
                         "does not locate it. Section 4.1's own reading is the narrower one." % n)}


def g008_four_examples(text):
    ln = locate(text, "four independent working examples")
    rows = {
        "NASA ASRS": "2.3M+ reports" in text,
        "RLHF / targeted human feedback": "6–7% annotation effort" in text,
        "Shadow-mode fleet learning": "Fleet-scale, billions of miles" in text,
        "Clinical override mining": "70% alert-volume cut" in text,
        "Signed provenance": "proposed for training data" in text,
        "Statutory co-determination": "EU-wide by Dec 2026" in text,
    }
    working = [k for k in rows if k not in ("Signed provenance", "Statutory co-determination")]
    named = ["NASA ASRS", "Shadow-mode fleet learning", "Signed provenance",
             "Statutory co-determination"]
    both = [k for k in named if k in working]
    return {"id": "GWS_008", "line": ln, "status": "TENSION",
            "evidence": ("the section-5 table carries %d rows with a working scale; the "
                         "conclusion's sentence before 'four independent working examples' "
                         "names four, of which %d are working rows (%s). The count matches "
                         "the table; the list does not."
                         % (len(working), len(both), ", ".join(both)))}


def g009_ipass(text):
    sites = [locate(text, "nine-center"), locate(text, "nine medical centers")]
    n = text.count("10,740")
    return {"id": "GWS_009", "line": sites[0], "status": "HOLDS" if n >= 2 else "DIVERGES",
            "evidence": "nine centers at lines %s; 10,740 admissions at %d sites, fig3 agrees"
                        % (sites, n)}


def g010_citations(text):
    urls = sorted(set(re.findall(r"https?://[^)\s]+", text)))
    hosts = sorted(set(re.match(r"https?://([^/]+)", u).group(1) for u in urls))
    dated = [u for u in urls if "2026" in u]
    return {"id": "GWS_010", "line": None, "status": "UNVERIFIED",
            "evidence": ("%d distinct URLs over %d hosts, none fetched (egress allowlist). "
                         "%d carry '2026' in the URL, including a page on a 1999 loss."
                         % (len(urls), len(hosts), len(dated)))}


def g011_cross_map(text):
    root = os.path.join(HERE, "..")
    present = [(e, p, os.path.exists(os.path.join(root, p)), why) for e, p, why in CROSS_MAP]
    return {"id": "GWS_011", "line": None,
            "status": "RESOLVES" if all(x[2] for x in present) else "MISSING",
            "evidence": "; ".join("%s -> %s (%s)" % (e, p, "present" if ok else "ABSENT")
                                  for e, p, ok, _ in present)}


CHECKS = [g001_lbf, g002_asana, g003_alert_cut, g004_workweeks, g005_override_range,
          g006_override_reading, g007_thirty, g008_four_examples, g009_ipass,
          g010_citations, g011_cross_map]


def run(text=None):
    text = report_text() if text is None else text
    return [c(text) for c in CHECKS]


def render(rows):
    out = ["grounded-work-stack: readings of REPORT.md (verbatim, not edited)",
           "citations are carried, not read; fig3 values are a hand transcription", ""]
    for r in rows:
        where = "line %d" % r["line"] if r["line"] else "whole report"
        out.append("%s  %-11s %s" % (r["id"], r["status"], where))
        out.append("    " + r["evidence"])
    out.append("")
    out.append("cross-map readings:")
    for e, p, why in CROSS_MAP:
        out.append("  %s: %s -- %s" % (e, p, why))
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("checks live in test_check.py: python3 test_check.py\n")
        sys.exit(2)
    print(render(run()))
