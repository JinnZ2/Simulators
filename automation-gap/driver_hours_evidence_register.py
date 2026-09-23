#!/usr/bin/env python3
"""
driver_hours_evidence_register.py  --  CC0 1.0, stdlib only

What this is: a register of what is KNOWN, what is only SELF-REPORTED,
and what is UNMEASURED about long driving days, fatigue, and driver
tenure. Built 2026-09-23 from a search pass. Gaps are the product.

Status scale (one scale for every source, including the operator's own
record):
  OBSERVED    read directly off a primary source, or first-hand record
  SECONDARY   relayed by a secondary source; primary not read
  DERIVED     follows from two or more entries
  PROPOSED    offered for test
  UNMEASURED  no source found that measures it
  UNREAD      source located, content relevant, full text not read

Sampling-frame flags (every source carries one):
  ON_ROAD      interviewed while working -> excludes drivers already out
               (crashed, quit, fired): survivorship
  ADMISSION    self-report where admitting it carried risk
               (inspection station) -> likely UNDERcount of hours
  VENDOR       party reporting benefits from the number
  N_OF_1       single first-hand record
  ARCHIVE      narrative / oral history, not a sample
  TERM_DRIFT   item wording carries two meanings across populations;
               the count mixes them (see TERM NOTES)

Nothing here is a finding about any individual. It is a map of which
questions the record can and cannot answer yet.
"""

SOURCES = {
    "S1": dict(
        cite="Braver, Preusser, Preusser, Baum, Beilock, Ulmer (1992). "
             "Long hours and fatigue: a survey of tractor-trailer drivers. "
             "J Public Health Policy 13(3):341-66",
        n="1,249 long-haul drivers", years="Dec 1990 - Apr 1991",
        where="inspection stations, truck stops; CT FL OK OR; 89% response",
        holds=["~3/4 self-report violating hours-of-service",
               "~2/3 routinely exceed weekly max",
               "economic pressure (tight schedules, low pay) named main driver",
               "violators more likely to report falling asleep at wheel "
               "in past month (per IIHS summary)",
               "violator characteristics table exists -- contents UNREAD"],
        status="OBSERVED (abstract) / UNREAD (tables)",
        frame=["ON_ROAD", "ADMISSION", "TERM_DRIFT"]),
    "S2": dict(
        cite="McCartt, Rohrbaugh, Hammer, Fuller (2000). Factors associated "
             "with falling asleep at the wheel among long-distance truck "
             "drivers. Accid Anal Prev 32(4):493-504",
        n="593 long-distance drivers", years="late 1990s",
        where="rest areas + roadside inspections, random selection",
        holds=["47.1% ever fell asleep at the wheel of a truck",
               "25.4% in the past year",
               "predictors include schedules, long hours, night driving "
               "(secondary summary)",
               "six factors from multivariate analysis; per a secondary "
               "review (Brazil, scielo) one factor = OLDER AGE AND MORE "
               "EXPERIENCE as a driver -> predicts MORE 'fell asleep at "
               "the wheel'  [SECONDARY]",
               "abstract wording: 'at the wheel of a truck'; later "
               "citations restate it as 'while driving' (Tandfonline "
               "2017; scielo)  [OBSERVED -- citation-chain conversion]",
               "which item (ever vs past-year) the experience factor "
               "predicted: UNREAD"],
        status="OBSERVED (abstract) / UNREAD (predictor table, item wording)",
        frame=["ON_ROAD", "TERM_DRIFT"]),
    "S11": dict(
        cite="Lin et al. (1994), operational data from a national motor "
             "carrier, as summarised in McCartt et al. 2000",
        n="carrier fleet", years="early 1990s", where="carrier records",
        holds=["total driving time had a greater effect on crash risk "
               "than time of day or driving experience  [SECONDARY]"],
        status="SECONDARY", frame=["ON_ROAD"]),
    "S3": dict(
        cite="Braver, Preusser, Ulmer (1999). How long-haul motor carriers "
             "determine truck driver work schedules: the role of shipper "
             "demands. J Safety Research",
        n="270 of 309 dispatchers", years="late 1990s",
        where="drivers at weigh stations WY + TN; dispatchers by phone",
        holds=["73% of drivers reported working longer than permitted",
               "revenue top factor (75%) in load acceptance"],
        status="OBSERVED (abstract)", frame=["ON_ROAD", "ADMISSION"]),
    "S4": dict(
        cite="IIHS survey, 2003 vs 2004 (in IIHS comment to FMCSA, 2005)",
        n="not stated in excerpt", years="2003-2004",
        where="national survey, pre/post HOS rule change",
        holds=["share of shifts > 10 h rose substantially after 2004 rule",
               "~1/4 took < 10 h off; most of those < 8 h"],
        status="OBSERVED (comment letter excerpt)",
        frame=["ON_ROAD", "ADMISSION"]),
    "S5": dict(
        cite="NSTSCE / Virginia Tech Transportation Institute (2020). "
             "Commercial Motor Vehicle Driver Risk Based on Age and "
             "Driving Experience",
        n="9,000+ CMV drivers, age 21-65, 6 mo - 30 yr experience",
        years="report 2020",
        where="carrier records (crash, moving violation)",
        holds=["< 6 months experience: highest crash likelihood",
               "< 5 years: higher risk than seasoned",
               "improvement plateaus ~10 years",
               "age no independent effect once experience held",
               "authors recommend mentoring by experienced drivers",
               "crash TYPE (fatigue vs other) by tenure: not in relays"],
        status="SECONDARY (law-firm relays; primary report UNREAD)",
        frame=["ON_ROAD"]),
    "S6": dict(
        cite="FMCSA crash-causation analysis (LTCCS-derived), as relayed",
        n="?", years="?", where="?",
        holds=["< 5 yr experience: 41% more likely assigned critical reason"],
        status="SECONDARY (law-firm relay; primary not located)",
        frame=[]),
    "S7": dict(
        cite="Heaton, Browning, Anderson (2008). Identifying variables that "
             "predict falling asleep at the wheel among long-haul truck "
             "drivers. AAOHN Journal 56(9)",
        n="843 long-haul drivers", years="~2005-2008", where="?",
        holds=["predictors incl. demographics, Epworth -- tenure: UNREAD"],
        status="UNREAD", frame=["ON_ROAD"]),
    "S8": dict(
        cite="NIOSH / FMCSA National Survey of Long-Haul Truck Driver "
             "Health and Injury (data 2010, report 2014)",
        n="national sample", years="2010", where="truck stops",
        holds=["hours, sleep, injury, tenure fields likely -- UNREAD"],
        status="UNREAD", frame=["ON_ROAD"]),
    "S9": dict(
        cite="Aurora Innovation releases + trade press (Feb-Mar 2026)",
        n="30 trucks, 10 driverless (Feb 2026)", years="2025-2026",
        where="Sun Belt mapped corridors, terminal to terminal",
        holds=["~1,000 mi Fort Worth-Phoenix in ~15 h, no HOS stop",
               "observer in cab on Paccar trucks",
               "weather constrained Texas ops ~40% of prior year",
               "terminal dwell, human touch-minutes per load: unreported"],
        status="OBSERVED (vendor claims)", frame=["VENDOR"]),
    "S10": dict(
        cite="Operator first-hand record (this register's requester)",
        n="1", years="COVID window; oilfield-exemption era",
        where="COVID relief runs; oilfield multi-stop",
        holds=["1,000-mi round trips under COVID HOS waiver",
               "1,000-mi days under oilfield exemption, MORE stops/day"],
        status="OBSERVED (first-hand)", frame=["N_OF_1"]),
    "Q1": dict(
        cite="Qualitative archive leads (not samples)",
        n="-", years="1970s-2010s", where="-",
        holds=["Ouellet (1994) Pedal to the Metal -- ethnography, UNREAD",
               "Thomas (1979) The Long Haul -- 1970s snapshot, UNREAD",
               "LOC American Folklife Center, Occupational Folklife "
               "Project (1,800+ interviews) -- trucker content UNCONFIRMED",
               "Overdrive 'Faces of the Road' oral histories -- UNREAD",
               "carrier million-mile safe-driver award rosters -- NOT "
               "SEARCHED; tenure-selected by construction"],
        status="UNREAD", frame=["ARCHIVE"]),
}

TERM_NOTES = {
    "fell asleep at the wheel": dict(
        sense_old="pulled over, stopped, slept slumped on the steering "
                  "wheel -- a REST ACT (fatigue managed)",
        sense_new="dozed while the truck was moving -- a HAZARD EVENT "
                  "(fatigue unmanaged)",
        source="operator first-hand: old sense was standard in her "
               "father's era; oilfield usage still carries it  [OBSERVED]",
        effect="a survey counting 'yes' mixes a safety behaviour with "
               "a hazard; the two have OPPOSITE signs for risk  [DERIVED]",
        tenure_bias="if older / oilfield drivers answer in the old sense, "
                    "experienced drivers' 'fatigue' rate is inflated by "
                    "rest acts -> a tenure curve on this item is biased "
                    "FLAT, masking any novice concentration  [DERIVED]",
        fix="read item wording (S1, S2, S7, S8). If it does not say "
            "'while the vehicle was moving', the count is TERM_DRIFT and "
            "cannot be read as hazard prevalence  [PROPOSED]"),
}

# questions -> which sources speak to them, current status, next read
QUESTIONS = [
    ("QA", "Did working drivers routinely run long days pre-ELD?",
     ["S1", "S3", "S4", "S10"], "SUPPORTED (self-report; likely undercount)",
     "none needed for existence; magnitude needs S8"),
    ("QB", "Did long hours carry a fatigue signal?",
     ["S1", "S2"], "SUPPORTED (self-report)",
     "keep as its own branch -- do not drop it"),
    ("QC", "Does crash risk fall with tenure?",
     ["S5", "S6"], "SUPPORTED (secondary only)",
     "read S5 primary report"),
    ("QD", "Does the FATIGUE signal fall with tenure?",
     [], "UNMEASURED",
     "S1 violator table; S2 predictor table; S7; S8 tenure fields"),
    ("QE", "Is the tenure curve learning or survivorship?",
     [], "UNMEASURED",
     "within-driver trajectories (same person over years); "
     "every source here is ON_ROAD cross-section"),
    ("QF", "Multi-stop physical vs long-haul monotonous fatigue profile?",
     ["S10"], "UNMEASURED (N=1 only; all samples long-haul)",
     "regional/multi-stop sample with fatigue TYPE split "
     "(vigilance vs muscular vs circadian)"),
    ("QG", "How much of aggregate 'driver fatigue' is carried by "
           "screened-in novices?",
     [], "UNMEASURED",
     "turnover x tenure mix of the pool x fatigue rate by band"),
    ("QH", "Door-to-door stops + human-touch minutes: driverless vs human",
     ["S9", "S10"], "UNMEASURED (vendor omits dwell)",
     "count every stop and touch, both systems, same lane"),
    ("QI", "Did 'fell asleep at the wheel' items measure dozing-while-"
           "moving or pulled-over sleep?",
     ["S1", "S2", "S10"],
     "PARTIAL -- abstract says 'at the wheel'; citing papers convert it "
     "to 'while driving'; questionnaire text still UNREAD",
     "questionnaire text for S1, S2, S7, S8; split by cohort / sector"),
    ("QJ", "Why does experience PREDICT more 'fell asleep at the wheel' "
           "(S2) while crash risk FALLS with experience (S5)?",
     ["S2", "S5", "S10"],
     "UNRESOLVED -- three rival explanations, not yet separable",
     "E1 exposure: 'ever' item grows with years driven -> check "
     "past-year item | E2 age: sleep disorders rise with age -> "
     "control age vs tenure | E3 TERM DRIFT: experienced drivers "
     "answer in the old sense (pulled over, slept) -> item wording + "
     "cohort split. E3 predicts the S2/S5 contradiction; E1 and E2 "
     "predict it only partly"),
]

# propagation rules for readers of this register
RULES = [
    "A SECONDARY figure is not cited as primary until the primary is read.",
    "ON_ROAD samples cannot separate learning from survivorship.",
    "ADMISSION-flagged hours are a floor, not an estimate.",
    "VENDOR numbers omit what the vendor does not book (terminal dwell).",
    "N_OF_1 is OBSERVED, not anecdote: it bounds what is possible, "
    "it does not estimate a rate.",
    "An UNMEASURED cell is a result: it says where the next study goes.",
    "A self-report count is read against the item's WORDING and the "
    "respondent population's sense of the words, not the analyst's.",
]


def main():
    print("DRIVER HOURS / FATIGUE / TENURE -- evidence register\n")
    for k, s in SOURCES.items():
        print("%s  %s" % (k, s["cite"]))
        print("    n=%s | %s | %s" % (s["n"], s["years"], s["where"]))
        print("    status: %s | frame: %s" % (s["status"],
                                             ", ".join(s["frame"]) or "-"))
        for h in s["holds"]:
            print("      - " + h)
        print()
    print("QUESTION MAP")
    for qid, q, srcs, st, nxt in QUESTIONS:
        print("  %s  %s" % (qid, q))
        print("       sources: %s" % (", ".join(srcs) or "none"))
        print("       status : %s" % st)
        print("       next   : %s" % nxt)
    print("\nTERM NOTES")
    for term, t in TERM_NOTES.items():
        print("  '%s'" % term)
        for k in ("sense_old", "sense_new", "source", "effect",
                  "tenure_bias", "fix"):
            print("     %-11s %s" % (k, t[k]))
    print("\nREADING RULES")
    for r in RULES:
        print("  - " + r)
    open_cells = [q for q in QUESTIONS if q[3].startswith("UNMEASURED")]
    print("\n%d of %d questions UNMEASURED." % (len(open_cells),
                                                len(QUESTIONS)))


if __name__ == "__main__":
    main()
