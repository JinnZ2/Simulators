# SPDX-License-Identifier: CC0-1.0
"""FWO-15 Build B -- coupling gradient.

STATUS: RECONSTRUCTED 2026-10-04. The original 2026-09-27 spec text was not
recovered; the order (WORK_ORDER_FWO-15_2026-10-04.md) was rebuilt from a
memory object that is not in this tree. If the original surfaces it
SUPERSEDES the order and this module is re-scored against it.

TERMS: "enclosure", "captive" and "domesticated" are used in their
animal-science external-validity sense. No political position is advanced.

QUESTION (order's): behavior before vs after a population's coupling to the
token, timestamped by the instrument that coupled it.

Rules carried from the order and enforced here:
  - a case with no CONFOUNDS column is rejected (CaseRejected);
  - a case whose coupling instrument is undated, or dated without a source,
    goes to the HELD list and never enters the analysis;
  - the pre-coupling record is labelled CONTROL, not prehistory;
  - every render prints the survivor-filter line.

Not rebuilt here (order's SCOPE): the lag count is FWO-11 lag_count.py and
question selection is FWO-9 question_space.py.

  [CHOICE 7] a confound is COINCIDENT when it is undated, or when its date
             (or any year of its range) falls within WINDOW years of the
             coupling year. Any coincident confound makes the case read
             CONFOUNDED_BEYOND_READ.
  [CHOICE 8] the shift reading (VISIBLE / NOT_VISIBLE) is DECLARED by the
             coder with a basis and never inferred from the behavior text.
  [CHOICE 9] precedence: a missing before or after record reads
             NOT_EVALUABLE first; would_read_if_filled is reported beside it
             so a confound is not hidden behind the missing record.
  [CHOICE 10] an explicit empty confound list is admitted and flagged
             NONE_DECLARED; a missing column is rejected.
"""

import sys

ABSENT = "ABSENT"
INSTRUMENTS = ("lease", "permit", "building approval", "tax", "barter-accounting rule", "other")
COMPLETENESS = ("full", "partial", "gradual", ABSENT)
CONFOUND_KINDS = ("never fully outside", "mechanization", "roads", "media", "other")
SHIFTS = ("VISIBLE", "NOT_VISIBLE")
WINDOW = 5

SURVIVOR_LINE = (
    "SURVIVOR FILTER: every case here is a population whose record survived to be read;\n"
    "a population that dissolved on coupling leaves no before/after pair and is absent\n"
    "by construction, not by measurement."
)

CHOICES = {
    7: "a confound is COINCIDENT when undated or within %d years of the coupling year" % WINDOW,
    8: "shift reading is declared with a basis, never inferred from behavior text",
    9: "missing before/after reads NOT_EVALUABLE first; would_read_if_filled reported beside it",
    10: "an explicit empty confound list is admitted and flagged NONE_DECLARED",
}

VERDICTS = ("VISIBLE", "NOT_VISIBLE", "CONFOUNDED_BEYOND_READ", "NOT_EVALUABLE")


class CaseRejected(ValueError):
    """A case the order's rules do not admit at all (not even to HELD)."""


def _years(d):
    """A date field as a (from, to) year pair, or None when it carries no year."""
    if d in (None, ABSENT):
        return None
    s = str(d.get("date") if isinstance(d, dict) else d).strip()
    if len(s) >= 9 and s[:4].isdigit() and s[4] == "-" and s[5:9].isdigit():
        return (int(s[:4]), int(s[5:9]))
    if len(s) >= 4 and s[:4].isdigit():
        return (int(s[:4]), int(s[:4]))
    return None


def validate(case):
    for k in ("population", "coupling_instrument", "coupling_date", "behavior_before",
              "behavior_after", "coupling_completeness"):
        if k not in case:
            raise CaseRejected("%s: field %s missing (write ABSENT, not nothing)" % (case.get("population"), k))
    if "confounds" not in case:
        raise CaseRejected("%s: CONFOUNDS column missing; the order rejects the case" % case.get("population"))
    if case["coupling_instrument"] not in INSTRUMENTS:
        raise CaseRejected("%s: instrument %r not in %s" % (case["population"], case["coupling_instrument"], INSTRUMENTS))
    if case["coupling_instrument"] == "other" and not case.get("instrument_name"):
        raise CaseRejected("%s: instrument 'other' must be named" % case["population"])
    if case["coupling_completeness"] not in COMPLETENESS:
        raise CaseRejected("%s: completeness %r" % (case["population"], case["coupling_completeness"]))
    for c in case["confounds"]:
        if c.get("kind") not in CONFOUND_KINDS:
            raise CaseRejected("%s: confound kind %r" % (case["population"], c.get("kind")))
        if c["kind"] == "other" and not c.get("name"):
            raise CaseRejected("%s: confound 'other' must be named" % case["population"])
    sr = case.get("shift_reading", ABSENT)
    if sr != ABSENT:
        if sr.get("reading") not in SHIFTS or not sr.get("basis"):
            raise CaseRejected("%s: a shift reading needs one of %s and a basis [CHOICE 8]" % (case["population"], SHIFTS))
    return case


def held_reason(case):
    """Why a case stays out of the analysis, or None if it enters."""
    d = case["coupling_date"]
    if d == ABSENT or _years(d) is None:
        return "coupling instrument undated"
    if not isinstance(d, dict) or not d.get("source"):
        return "coupling date stated without a source"
    return None


def coincident(case):
    """Confounds that cannot be separated from the coupling by time [CHOICE 7]."""
    y = _years(case["coupling_date"])[0]
    out = []
    for c in case["confounds"]:
        r = _years(c.get("date", ABSENT))
        if r is None or (r[0] - WINDOW <= y and r[1] + WINDOW >= y):
            out.append(c)
    return out


def read_case(case):
    hits = coincident(case)
    would = "CONFOUNDED_BEYOND_READ" if hits else None
    if would is None:
        sr = case.get("shift_reading", ABSENT)
        would = sr["reading"] if sr != ABSENT else "NOT_EVALUABLE"
    if case["behavior_before"] == ABSENT or case["behavior_after"] == ABSENT:
        verdict = "NOT_EVALUABLE"
    else:
        verdict = would
    return {
        "population": case["population"],
        "instrument": case["coupling_instrument"] if case["coupling_instrument"] != "other" else case["instrument_name"],
        "year": _years(case["coupling_date"])[0],
        "control": "CONTROL: " + (case["behavior_before"]["field"] if case["behavior_before"] != ABSENT else "ABSENT"),
        "treatment": case["behavior_after"]["field"] if case["behavior_after"] != ABSENT else "ABSENT",
        "coincident_confounds": [c.get("name") or c["kind"] for c in hits],
        "confounds_flag": "NONE_DECLARED" if not case["confounds"] else "",
        "verdict": verdict,
        "would_read_if_filled": would,
    }


def run(cases):
    rejected, held, entered = [], [], []
    for c in cases:
        try:
            validate(c)
        except CaseRejected as e:
            rejected.append(str(e))
            continue
        why = held_reason(c)
        if why:
            held.append((c["population"], why))
        else:
            entered.append(read_case(c))
    groups = {}
    for r in entered:
        groups.setdefault((r["instrument"], r["year"]), []).append(r["population"])
    shared = {k: v for k, v in groups.items() if len(v) > 1}
    return {"rejected": rejected, "held": held, "entered": entered, "shared_dates": shared}


# Seed rows from the order (HERS, all UNCHECKED at delivery). What the 2026-10-04
# searches found is carried in the row; nothing else is supplied. Search-result
# snippets only; full texts sit behind the egress allowlist.
SEEDS = [
    {
        "population": "Amish",
        "coupling_instrument": "other",
        "instrument_name": "lease / permit / building approval (as stated; three named, none dated)",
        "coupling_date": ABSENT,
        "behavior_before": ABSENT,
        "behavior_after": ABSENT,
        "coupling_completeness": ABSENT,
        "confounds": [
            {"kind": "mechanization", "date": ABSENT, "assessed": False},
            {"kind": "roads", "date": ABSENT, "assessed": False},
        ],
        "notes": "searches located DISPUTE dates, not coupling dates: Morristown NY federal suit "
                 "(foxnews), Eau Claire WI state religious waiver (dailyreporter 2015-08-28; a "
                 "DE-coupling instrument, a direction the schema has no field for), Mille Lacs MN "
                 "demand letter dated Aug 24 (year not in snippet). Leases located as mostly "
                 "intra-Amish (amishpedia), no date.",
    },
    {
        "population": "German village groups",
        "coupling_instrument": "other",
        "instrument_name": "not stated",
        "coupling_date": ABSENT,
        "behavior_before": ABSENT,
        "behavior_after": ABSENT,
        "coupling_completeness": ABSENT,
        "confounds": [{"kind": "never fully outside", "date": ABSENT, "assessed": False}],
        "notes": "NOT SEARCHED: population not named to a unit one instrument couples.",
    },
    {
        "population": "Dutch",
        "coupling_instrument": "other",
        "instrument_name": "not stated",
        "coupling_date": ABSENT,
        "behavior_before": ABSENT,
        "behavior_after": ABSENT,
        "coupling_completeness": ABSENT,
        "confounds": [{"kind": "never fully outside", "date": ABSENT, "assessed": False}],
        "notes": "NOT SEARCHED: population not named to a unit one instrument couples.",
    },
    {
        "population": "Indigenous peoples",
        "coupling_instrument": "other",
        "instrument_name": "not stated",
        "coupling_date": ABSENT,
        "behavior_before": ABSENT,
        "behavior_after": ABSENT,
        "coupling_completeness": ABSENT,
        "confounds": [{"kind": "never fully outside", "date": ABSENT, "assessed": False}],
        "notes": "NOT SEARCHED: population not named to a unit one instrument couples.",
    },
    {
        "population": "members of US organized barter exchanges",
        "coupling_instrument": "barter-accounting rule",
        "coupling_date": {
            "date": "1982",
            "source": "Tax Equity and Fiscal Responsibility Act of 1982: barter exchanges treated as "
                      "third-party record keepers, members' transactions reported on Form 1099-B "
                      "(en.wikipedia.org/wiki/Tax_Equity_and_Fiscal_Responsibility_Act_of_1982; "
                      "calt.iastate.edu barter slides, 2015)",
        },
        "behavior_before": ABSENT,
        "behavior_after": ABSENT,
        "coupling_completeness": "partial",
        "completeness_basis": "exchanges with fewer than 100 transactions a year are exempt; informal "
                              "barter outside an exchange is not covered (irs.gov 1099-B instructions)",
        "confounds": [
            {"kind": "never fully outside", "date": ABSENT, "assessed": True,
             "name": "barter income already taxable at fair market value under 26 CFR 1.61-2(d)(1); "
                     "the rule's adoption date was not located (govinfo CFR 2002 edition)"},
            {"kind": "other", "date": ABSENT, "assessed": True,
             "name": "the exchange's own trade credit is a token: trade credits or scrip are credited "
                     "at fair market value (irs.gov 1099-B instructions)"},
            {"kind": "other", "date": "1970-1979", "assessed": True,
             "name": "the population itself grew over the window: modern trade exchanges emerged in "
                     "the US in the late 1970s (trade exchange overview, grokipedia)"},
        ],
        "notes": "The order's line 'barter less constrained 1950s-1970s, then accounted in dollars' "
                 "is not what the located instrument does: barter was already accounted in dollars "
                 "for income tax before 1982; the 1982 rule added third-party REPORTING. One date "
                 "covers every US exchange at once, so the order's shared-date lever holds in form; "
                 "this table carries one population row for it.",
    },
]


def render(out=None, cases=None):
    out = out or sys.stdout
    w = out.write
    res = run(SEEDS if cases is None else cases)
    w("FWO-15 Build B -- coupling gradient\n")
    w("STATUS RECONSTRUCTED 2026-10-04; BUILT, run on the order's seed rows\n")
    w("TERMS: enclosure / captive / domesticated in the animal-science external-validity sense\n")
    w("%s\n\n" % SURVIVOR_LINE)
    w("entered %d   held %d   rejected %d\n" % (len(res["entered"]), len(res["held"]), len(res["rejected"])))
    for r in res["entered"]:
        w("  ENTERED %s | %s %s\n" % (r["population"], r["instrument"], r["year"]))
        w("      %s\n      treatment: %s\n" % (r["control"], r["treatment"]))
        w("      verdict %s   would_read_if_filled %s\n" % (r["verdict"], r["would_read_if_filled"]))
        for c in r["coincident_confounds"]:
            w("      coincident confound: %s\n" % c)
        if r["confounds_flag"]:
            w("      confounds: %s\n" % r["confounds_flag"])
    for pop, why in res["held"]:
        w("  HELD    %s -- %s\n" % (pop, why))
    for r in res["rejected"]:
        w("  REJECTED %s\n" % r)
    if res["shared_dates"]:
        for (inst, year), pops in sorted(res["shared_dates"].items()):
            w("  shared treatment date %s %s: %s\n" % (inst, year, ", ".join(pops)))
    else:
        w("  shared treatment dates: none with more than one population row\n")
    w("not rebuilt: lag count -> FWO-11 lag_count.py; question selection -> FWO-9 question_space.py\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("coupling_gradient: checks live in test_fwo15.py; run python3 test_fwo15.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
