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
  EXPLORATION real gap, relevance to the question UNKNOWN; kept, not
              load-bearing

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
               "1,000-mi days under oilfield exemption, MORE stops/day",
               "as a TRAINEE ran nights; used exercises, katas, stretches "
               "and essential scents for state regulation",
               "-> novice by CDL tenure, not novice in state regulation: "
               "skill IMPORTED from outside driving  [DERIVED]"],
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
     "every source here is ON_ROAD cross-section. Third arm: IMPORTED "
     "skill -- CDL tenure counts months licensed, not state-regulation "
     "skill brought from elsewhere (S10). A novice by tenure can be "
     "adapted by practice -> tenure is a proxy, and the screen measures "
     "the proxy [DERIVED]"),
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


# ===========================================================================
# ADDENDUM -- continued work, opened 2026-09-23
# ===========================================================================

ADDENDUM_QUESTIONS = [
    ("QK", "State-driven rest (rest on need, split runs) vs clock-driven "
           "rest (fixed HOS blocks): fatigue / crash rate on matched routes",
     ["S10"],
     "UNMEASURED -- S10 is N=1 (operator pattern: run ~600 mi, rest on "
     "need, run ~400, finish the day)  [OBSERVED]",
     "discriminator: drivers using split-sleeper flexibly vs fixed "
     "blocks, same carrier, same lanes. Transfer lead: NASA 1990s "
     "cockpit planned-nap study (aviation) -- NOT VERIFIED this session. "
     "Regulatory lead: FMCSA split sleeper-berth (7/3, 8/2) pauses the "
     "14-h window -- as far as known, NOT VERIFIED this session"),
]

CONTROL_LOOPS = dict(
    clock=dict(input="elapsed hours", stop="clock says", resume="clock "
               "allows", failure="drives through circadian low when hours "
               "remain; forced rest when not sleepy"),
    state=dict(input="body signals (sleep pressure + circadian)",
               stop="signal says", resume="rested",
               failure="depends on reading the signal -- a learned skill; "
                       "candidate mechanism for part of the tenure curve "
                       "[PROPOSED]"),
)

# Behaviour-anchored record: survives term drift in both directions.
# The last two fields carry the transferable skill.
BEHAVIOUR_RECORD_SCHEMA = [
    ("vehicle_state", "moving | stopped | parked"),
    ("location",      "shoulder | lot | ramp | dock | other"),
    ("duration_min",  "int"),
    ("trigger",       "what told you to stop (free text, the skill)"),
    ("resumed_after", "what told you it was safe to go (free text, the "
                      "skill)"),
    ("clock_state",   "hours on duty / driving at stop, if logged"),
]

TRANSFER_NOTE = (
    "Mentoring is the NSTSCE authors' named fix, but it runs on words. "
    "Where a term has drifted ('fell asleep at the wheel': rest act -> "
    "hazard), told practice arrives inverted. Record the behaviour, not "
    "the phrase; show, not tell.  [DERIVED]")

CONTINUED_WORK = [
    ("W1", "Read McCartt et al. 2000 full text: item wording (QI); which "
           "item the experience factor loaded on (QJ, E1)", "library"),
    ("W2", "Read Braver et al. 1992 violator-characteristics table: "
           "tenure column? (QD)", "library"),
    ("W3", "Read NSTSCE 2020 primary report: crash TYPE by tenure band "
           "(QC -> QD)", "online"),
    ("W4", "Read NIOSH/FMCSA 2010 long-haul survey: tenure, sleep, hours "
           "fields (QA magnitude, QD)", "online"),
    ("W5", "Heaton et al. 2008: predictors incl. tenure? (QD)", "library"),
    ("W6", "Verify NASA planned-nap study + FMCSA split-sleeper rule "
           "text (QK leads)", "online"),
    ("W7", "Search oral-history archives for pre-ELD trucker accounts "
           "coded with the behaviour-anchored schema (QF, QI cohort "
           "split)", "online + archive"),
    ("W8", "Million-mile safe-driver rosters as a tenure-selected "
           "population (QE survivorship arm)", "not searched"),
    ("W9", "Regional / multi-stop sample with fatigue TYPE split -- no "
           "existing sample found (QF)", "needs new data"),
]


def addendum():
    print("\n" + "=" * 60)
    print("ADDENDUM -- continued work (2026-09-23)")
    print("=" * 60)
    for qid, q, srcs, st, nxt in ADDENDUM_QUESTIONS:
        print("  %s  %s" % (qid, q))
        print("       sources: %s" % ", ".join(srcs))
        print("       status : %s" % st)
        print("       next   : %s" % nxt)
    print("\n  CONTROL LOOPS")
    for name, d in CONTROL_LOOPS.items():
        print("    %-6s " % name + " | ".join("%s: %s" % kv
                                              for kv in d.items()))
    print("\n  BEHAVIOUR-ANCHORED RECORD")
    for f, t in BEHAVIOUR_RECORD_SCHEMA:
        print("    %-14s %s" % (f, t))
    print("\n  TRANSFER NOTE\n    " + TRANSFER_NOTE)
    print("\n  CONTINUED WORK")
    for wid, w, access in CONTINUED_WORK:
        print("    %s  [%s]  %s" % (wid, access, w))


# ===========================================================================
# ADDENDUM 2 -- PROPOSED GATE MAP (2026-09-23)
# Question: can machine + human share a truck so the human rests on need
# while the machine carries the monotonous miles?
# Gates run IN ORDER. A FAIL at an earlier gate makes later gates moot
# for this design (they stay open as science, not as design inputs).
# ===========================================================================

import math

# G0 needs: the uninterrupted window must hold a usable rest block PLUS
# the time to become takeover-capable after waking.
REST_BLOCK = dict(
    nap_min=40,          # planned-nap scale (aviation lead, NOT VERIFIED)
    cycle_min=90,        # one sleep cycle, approx (general sleep science)
    inertia_min=(15, 30),  # sleep inertia before alert takeover -- common
                           # range in sleep literature; NOT VERIFIED here
    handoff_lead_min=5,  # warning time machine gives before it needs
                         # the human -- PLACEHOLDER, system-specific
)

# G0 sleep-quality term (multiplies usable rest, does not add windows)
SLEEP_QUALITY_FACTORS = [
    ("trust_in_driver", "chosen/known partner vs assigned stranger vs "
     "machine with checkable record", "OBSERVED (operator) -> key term"),
    ("ride_consistency", "jolts, hard brakes, lane wander per hour",
     "OBSERVED (operator) -> measurable from telematics"),
    ("alert_noise", "chimes / takeover requests per hour, incl. false "
     "alarms", "PROPOSED -- each one is a wake event"),
    ("motion_sleep_history", "early / long exposure to sleeping in "
     "motion (travois, wagon, vehicle) -- operator's own history  "
     "[OBSERVED, N=1]", "PROPOSED as individual-variance term: G0 may "
     "PASS for some operators and FAIL for others on the same route -> "
     "per-operator assessment, not one fleet rule"),
]

# Event classes that could interrupt. Only events the MACHINE CANNOT
# handle wake the human. rate = events/hour on the route;
# p_machine_fails = share the machine cannot handle alone.
# ALL VALUES BELOW ARE PLACEHOLDERS, NOT DATA. They exist so the
# arithmetic can be checked; replace per route + season from sources.
EVENT_CLASSES = [
    # name,                 rate_per_h, p_machine_fails, source status
    ("work_zone",               0.30, 0.3, "PLACEHOLDER -- DOT work-zone logs"),
    ("weather_out_of_envelope", 0.05, 1.0, "PLACEHOLDER -- NWS + vendor envelope"),
    ("incident_or_closure",     0.10, 0.5, "PLACEHOLDER -- state 511 incident feeds"),
    ("heavy_traffic_merge",     0.50, 0.1, "PLACEHOLDER -- traffic data"),
    ("mechanical_alert",        0.01, 1.0, "PLACEHOLDER -- fleet telematics"),
    ("fuel_inspection_stop",    0.08, 1.0, "PLACEHOLDER -- route plan"),
]


def interrupt_rate(classes):
    return sum(r * p for _, r, p, _ in classes)


def p_uninterrupted(lam_per_h, minutes):
    """Poisson assumption: events independent, constant rate.
    Weather and congestion CLUSTER, so real windows are burstier than
    this -- the Poisson figure is an upper bound on usable windows when
    events cluster in the same hours as rest need.  [DERIVED]"""
    return math.exp(-lam_per_h * minutes / 60.0)


def g0_window_needed(block="nap_min", inertia="high"):
    i = REST_BLOCK["inertia_min"][1 if inertia == "high" else 0]
    return REST_BLOCK[block] + i + REST_BLOCK["handoff_lead_min"]


GATE_MAP = [
    ("G0", "INTERVAL FEASIBILITY",
     "mean time between events the machine cannot handle, per route and "
     "season, vs window needed = rest block + sleep inertia + handoff lead",
     "PASS: P(uninterrupted window) high on the route -> go to G1",
     "FAIL: human cannot rest while machine drives -> complementarity "
     "design dead ON THAT ROUTE/SEASON; human stays primary or team-human",
     "UNMEASURED -- needs per-route event rates (DOT work zones, 511 "
     "incidents, NWS, vendor weather envelope, fuel plan)"),
    ("G1", "TASK-TYPE SPLIT (QF)",
     "is vigilance fatigue separable from muscular/contact fatigue",
     "PASS: automate the monotonous segment, human keeps contact work",
     "FAIL: segment placement irrelevant to fatigue",
     "UNMEASURED"),
    ("G2", "STATE vs CLOCK REST (QK)",
     "does rest-on-need beat fixed blocks on matched routes",
     "PASS: machine carries the leg while human rests on need",
     "FAIL: clock rules adequate; machine value is utilisation only",
     "UNMEASURED (S10 N=1)"),
    ("G3", "LEARNING vs SURVIVORSHIP (QE)",
     "is the tenure curve skill-building",
     "PASS (learning): design must keep hard-segment exposure for skill",
     "FAIL (survivorship): screen/selection is the lever",
     "UNMEASURED"),
    ("G4", "DOOR-TO-DOOR ACCOUNTING (QH)",
     "stops + human-touch minutes, both systems, same lane",
     "any result: required for honest cost/benefit",
     "skipped: human work booked as free",
     "UNMEASURED"),
]

G0_NOTES = [
    "Sleep in a MOVING cab: operator first-hand -- no trouble falling "
    "asleep when she TRUSTED the partner and they drove SAFE and "
    "CONSISTENT  [OBSERVED]. So the variable is trust + driving "
    "consistency, not motion itself. Team-driver poor-sleep findings "
    "(lead, NOT VERIFIED) may be confounded by dispatcher-assigned "
    "strangers vs chosen partners  [DERIVED].",
    "For the machine: sleep quality then depends on (a) ride consistency "
    "-- smooth throttle/brake, few jolts -- and (b) CALIBRATED trust, "
    "earned by a track record the sleeper can check. False alarms and "
    "frequent handoff chimes erode both  [PROPOSED].",
    "Route + season dependent: Upper Midwest winter and Sun Belt corridor "
    "are different gates. One G0 result does not transfer.",
    "The binding term is p_machine_fails, not raw event rate: a machine "
    "that handles work zones alone removes the most frequent interrupter.",
    "Clustering: interrupters bunch in the same hours (weather + traffic "
    "+ incidents). Poisson overstates usable windows -- treat as ceiling.",
]


def addendum2():
    print("\n" + "=" * 60)
    print("ADDENDUM 2 -- PROPOSED GATE MAP")
    print("=" * 60)
    for gid, name, test, ok, bad, st in GATE_MAP:
        print("  %s %s\n     test : %s\n     pass : %s\n     fail : %s"
              "\n     now  : %s" % (gid, name, test, ok, bad, st))
    lam = interrupt_rate(EVENT_CLASSES)
    print("\n  G0 ARITHMETIC -- DEMONSTRATION ON PLACEHOLDER RATES, NOT DATA")
    print("    human-required interrupts/hour (placeholder) = %.3f" % lam)
    print("    mean gap between them = %.0f min" % (60.0 / lam))
    for block in ("nap_min", "cycle_min"):
        for inertia in ("low", "high"):
            w = g0_window_needed(block, inertia)
            print("    window %-9s inertia %-4s = %3d min -> "
                  "P(uninterrupted) = %.2f"
                  % (block, inertia, w, p_uninterrupted(lam, w)))
    print("\n  G0 SLEEP-QUALITY FACTORS")
    for f, m, st in SLEEP_QUALITY_FACTORS:
        print("    %-17s %s  [%s]" % (f, m, st))
    print("\n  G0 NOTES")
    for n in G0_NOTES:
        print("    - " + n)


# ===========================================================================
# ADDENDUM 3 -- EXPLORATION TERRITORY (2026-09-23)
# Status EXPLORATION: a real gap between two literatures, relevance to the
# gate map UNKNOWN. Not load-bearing for any gate. Kept so it is not lost.
# ===========================================================================

EXPLORATION = [
    dict(
        xid="X1",
        gap="Does early carried-motion exposure (carried, cradleboard, "
            "wagon/vehicle-raised) shape adult sleep in motion?",
        half_a="Adult rocking lab studies: nap effects positive (Bayer "
               "2011 Curr Biol; mice 2019); overnight null in good sleepers "
               "(18 young males, 96% baseline efficiency); elderly null to "
               "negative, reduced delta; proposed mechanism = sensory "
               "confusion from translational motion. Early motion history "
               "NEVER recorded.",
        half_b="Infant carrying: Navajo cradleboard ~16 h/day first 3 mo "
               "(1978); no clear long-term swaddling effects; Hopi (Chisholm "
               "1983) lower arousal, motor milestones typical; Inuit amauti "
               "~3 yr; babywearing linked to infant neural tracking of "
               "biological-motion rhythm (2026 preprint). Never followed "
               "to adult sleep.",
        join="UNMEASURED -- nobody links half B exposure to half A outcome",
        relevance="UNKNOWN -- may bear on G0 per-operator variance "
                  "(motion_sleep_history); may not",
        cheapest_probe="add covariate early_motion_exposure to any adult "
                       "rocking / vehicle-sleep study; cross-cultural arm "
                       "in communities that still carry infants",
        prediction="PROPOSED: early vestibular habituation -> less sensory "
                   "confusion -> smaller effect of motion on sleep in "
                   "either direction",
        scope="lab rocking is gentle pendular/translational; truck cab is "
              "vibration + jolts + translation (whole-body vibration "
              "literature, ISO 2631 field, NOT searched)",
        anchor="operator first-hand: carried as infant, slept on travois, "
               "hay wagon, canoe  [OBSERVED, N=1]",
    ),    dict(
        xid="X2",
        gap="Community practices for sleeping in daylight (high-latitude / "
            "long-photoperiod seasons) -- ever studied as METHOD, or "
            "tested for day-sleeping night workers?",
        half_a="Clinical / chronobiology: Tromso Study 69N, n=21,083, age "
               "40+, some seasonal variation; Kiruna office workers n=32, "
               "winter sleep onset delayed 39 min, morning light advances; "
               "Arctic summer exploratory: >45 h/wk daytime sunlight -> "
               "median sleep 102 min shorter. Samples = general / settler "
               "/ indoor-worker populations measuring DISRUPTION.",
        half_b="Ethnography / history: 'Beyond Darkness and Sleep. The "
               "Inuit Night in North Baffin Island' (2016, UNREAD); EU "
               "MSCA project on 19th-c. European explorers' sleep "
               "DISORDERED by polar night / midnight sun (visitor frame).",
        join="UNMEASURED -- practices recorded as culture, never tested "
             "as method; clinical side never samples practice-holders",
        relevance="DIRECT for night drivers sleeping by day and for G0 "
                  "day-rest windows -- higher than X1",
        cheapest_probe="read the 2016 Inuit-night ethnography for "
                       "described practices; code them in the behaviour-"
                       "anchored form (conditions, trigger, duration)",
        prediction="PROPOSED: the population that had trouble (visitors, "
                   "indoor workers) is the one that got studied; the "
                   "population that solved it sits in the archive as custom",
        scope="practice knowledge may not be public by choice; record only "
              "what holders choose to share",
        anchor="operator: communities carry histories of ways to sleep "
               "in light, tied to long seasonal daylight; channels named: "
               "SCENT and BODY MOTION  [OBSERVED -- categories only, "
               "specifics not shared, none requested]",
        channels="light is the channel a cab cannot control; scent and "
                 "motion ARE controllable and portable -> candidate "
                 "carry-anywhere sleep cues for day-sleeping drivers "
                 "[DERIVED]. Literature leads, NOT searched: odor and "
                 "sleep (lavender trials, odor cueing during sleep); "
                 "rhythmic self-motion before sleep. Mechanism candidate: "
                 "learned association -- cue paired with sleep becomes a "
                 "trigger independent of light [PROPOSED]",
    ),
]


def addendum3():
    print("\n" + "=" * 60)
    print("ADDENDUM 3 -- EXPLORATION TERRITORY (relevance unknown)")
    print("=" * 60)
    for x in EXPLORATION:
        print("  %s  %s" % (x["xid"], x["gap"]))
        for k in ("half_a", "half_b", "join", "relevance",
                  "cheapest_probe", "prediction", "scope", "anchor",
                  "channels"):
            if k in x:
                print("     %-14s %s" % (k, x[k]))


if __name__ == "__main__":
    main()
    addendum()
    addendum2()
    addendum3()
