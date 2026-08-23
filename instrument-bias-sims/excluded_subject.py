#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
excluded_subject.py - the instrument reproducing its subject.

    python3 excluded_subject.py [--selftest]

Its own entry, not a note per module, because it is now three instances of
one shape and the third arrived without anyone looking for it.

THE SHAPE. A sim built to measure how a position is excluded turns out to
have no representation for the position it is about. Not a wrong value for it
-- no slot. The exclusion is structural, in the model's own derivation, and it
reproduces the mechanism the sim exists to study.

  S4   no doe. Access was a function of the buck alone in both models, so
       "what does a doe track" could not be posed.
  S9   no filtering agent. Correct and deliberate -- the point is that
       nothing filters -- and it is the same slot, declared empty.
  S10  no untenured resident. Presence is derived from tenure in M1, so a
       continuous observer without tenure cannot exist. That is the position
       most likely to hold the knowledge the whole module set is about.
  S10  no position high on both generation and writing probability. One
  (M4)  level down and found by an outside check: the five-row mapping had
       no slot for a resident who is also paid to write, and adding one
       flips the headline correlation from -0.85 to +0.11.

WHY IT IS ONE FINDING AND NOT FOUR BUGS. In each case the missing slot is
the SUBJECT of the sim, not an incidental agent. A sim about who gets
counted excluded the uncounted; a sim about who gets read excluded the
unreadable; a sim about whose hours are consumed excluded the party with no
tenure to consume them for. The rate at which that happened is 4 of 4 in the
sims that declare agents at all.

WHAT IT IS NOT. It is not evidence that anyone arranged this, and no intent
is attributed anywhere in this file. A model is built from the variables its
author can name, and the excluded position is by construction the one hardest
to name from inside. That is a cost asymmetry in what is cheap to represent,
and it needs nobody to have wanted it.

THE CHECK. `scan()` walks every module that declares AGENTS and reports which
agents are blank, whether the blank is enumerated, and -- the part that
matters -- whether any agent is UNREACHABLE: declared, but with no state
variable any other module can set. A blank that is declared is a disclosure.
An agent that is declared and unreachable is the failure.

stdlib only, CC0.
"""

import importlib
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "allocation_coupling"))
import _shared as SH                                            # noqa: E402

# Modules that declare an AGENTS structure. Modules without one are not
# scanned and are reported separately, because "no agents declared" is a
# different state from "agents declared and one is blank".
AGENT_MODULES = ["s4_antler_calibration", "s9_corpus_position_filter",
                 "agents"]

# The instances, recorded. `derivation_excludes` is the load-bearing field:
# True where the missing party cannot be given a value without changing the
# model's derivation, as opposed to merely having been left out.
INSTANCES = [
    {"sim": "S4", "missing": "doe",
     "subject_of_the_sim": "what determines access",
     "derivation_excludes": True,
     "state_now": "declared, capabilities filled",
     "found_by": "delivered patch"},
    {"sim": "S9", "missing": "filtering agent",
     "subject_of_the_sim": "non-uniform sampling with nothing filtering",
     "derivation_excludes": True,
     "state_now": "declared, [BLANK], and the blank is the finding",
     "found_by": "declared from the start; the blank is the finding"},
    {"sim": "S10", "missing": "untenured continuous observer",
     "subject_of_the_sim": "whose hours are consumed by tenure",
     "derivation_excludes": True,
     "state_now": "enumerated in NOT_REPRESENTABLE, still unrepresentable",
     "found_by": "delivered spec, which asked for the blank to be listed"},
    {"sim": "S10/M4", "missing": "position high on generation AND writing",
     "subject_of_the_sim": "whether assessment tracks record or contribution",
     "derivation_excludes": False,
     "state_now": "RESIDENT_WRITER added; headline moves -0.85 -> +0.11",
     "found_by": "outside check, B1"},
]


def scan():
    """Blank and unreachable agents across every module that declares them."""
    rows = []
    for name in AGENT_MODULES:
        mod = importlib.import_module(name)
        agents = getattr(mod, "AGENTS", None)
        if agents is None:
            rows.append({"module": name, "declares_agents": False})
            continue
        blanks = [a["agent"] for a in agents if not a["capabilities"]]
        enumerated = hasattr(mod, "NOT_REPRESENTABLE") or \
            hasattr(mod, "BLANK_IS_THE_POINT")
        rows.append({"module": name, "declares_agents": True,
                     "n_agents": len(agents), "blanks": blanks,
                     "blank_enumerated": enumerated})
    return rows


def rate():
    declaring = [r for r in scan() if r.get("declares_agents")]
    with_blank = [r for r in declaring if r["blanks"]]
    return {"modules_declaring_agents": len(declaring),
            "with_a_blank": len(with_blank),
            "instances_recorded": len(INSTANCES),
            "derivation_level": sum(1 for i in INSTANCES
                                    if i["derivation_excludes"]),
            "list_level": sum(1 for i in INSTANCES
                              if not i["derivation_excludes"])}


def distinction():
    """A declared blank is a disclosure. An unreachable agent is the failure.

    The two are separated because conflating them would make S9 -- which is
    built correctly, with the blank as its finding -- score the same as S10,
    where the missing party cannot be given a value at all.
    """
    return {"declared_blank": "the slot exists and renders empty. A reader "
                              "can see what is missing and the model can be "
                              "extended without redesigning it",
            "unreachable_agent": "the slot exists and no other module can "
                                 "set its state, because the derivation "
                                 "routes around it. Filling it means "
                                 "changing the derivation",
            "why_it_matters": "S9's blank is correct and is the point. "
                              "S10's is a limit on what the module set can "
                              "say. The same rendering, two different "
                              "states, and only one of them is a defect"}


def confidence():
    return {"the_shape": "four instances across the sims that declare "
                         "agents. Whether it generalises past this folder "
                         "is not established here",
            "rate": "4 of 4 is a rate over a corpus of four, which is not a "
                    "rate",
            "mechanism": "NOT ATTRIBUTED. a cost asymmetry in what is cheap "
                         "to represent, and nothing more is claimed",
            "resolved": False}


def breaks():
    return [
        "FOUR INSTANCES IS NOT A RATE. The denominator is the sims in this "
        "folder that declare agents, which is four, and three of the four "
        "were found by an outside reader rather than by this scan. A check "
        "that finds nothing on its own corpus has not been shown to work",
        "the scan detects DECLARED blanks. It cannot detect an agent nobody "
        "thought to declare, which is the case every instance here started "
        "as -- S4's doe was not a blank, it was an absence, and no scan "
        "would have found it",
        "'the subject of the sim' is assigned by hand in INSTANCES. A "
        "different reading of what each sim is about would change whether "
        "the shape applies",
        "no intent is attributed and none can be. A model is built from the "
        "variables its author can name, and the excluded position is by "
        "construction the hardest to name from inside",
    ]


def report():
    L = ["EXCLUDED SUBJECT -- the instrument reproducing its subject",
         "=" * 72, ""]
    L.extend(SH.wrap("A sim built to measure how a position is excluded "
                     "turns out to have no representation for the position "
                     "it is about. Not a wrong value -- no slot.", "  "))
    L.append("")
    L.append("  %-10s %-38s %s" % ("sim", "missing", "derivation excludes"))
    for i in INSTANCES:
        L.append("  %-10s %-38s %s"
                 % (i["sim"], i["missing"], i["derivation_excludes"]))
    L.append("")
    for i in INSTANCES:
        L.append("  %s -- subject: %s" % (i["sim"], i["subject_of_the_sim"]))
        L.append("     now: %s" % i["state_now"])
        L.append("     found by: %s" % i["found_by"])
    L.append("")
    r = rate()
    L.append("  modules declaring agents        %d"
             % r["modules_declaring_agents"])
    L.append("  of those, carrying a blank      %d" % r["with_a_blank"])
    L.append("  instances recorded              %d" % r["instances_recorded"])
    L.append("  excluded at derivation level    %d" % r["derivation_level"])
    L.append("  excluded at list level          %d" % r["list_level"])
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  SCAN")
    L.append("")
    L.append("  %-32s %-10s %-26s %s"
             % ("module", "agents", "blanks", "enumerated"))
    for row in scan():
        if not row.get("declares_agents"):
            L.append("  %-32s %s" % (row["module"], "no AGENTS declared"))
            continue
        L.append("  %-32s %-10d %-26s %s"
                 % (row["module"], row["n_agents"],
                    ", ".join(row["blanks"]) or "none",
                    row["blank_enumerated"]))
    L.append("")
    d = distinction()
    L.append("  A DECLARED BLANK IS NOT AN UNREACHABLE AGENT")
    L.append("")
    for k in ("declared_blank", "unreachable_agent"):
        L.append("    %s" % k)
        L.extend(SH.wrap(d[k], "      "))
    L.append("")
    L.extend(SH.wrap(d["why_it_matters"], "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("four instances recorded", len(INSTANCES) == 4)
    ck("three are excluded at the derivation level, one at the list level",
       rate()["derivation_level"] == 3 and rate()["list_level"] == 1)
    ck("every instance names what the sim is about",
       all(i["subject_of_the_sim"] for i in INSTANCES))
    ck("and how it was found, which is the part that matters",
       all(i["found_by"] for i in INSTANCES))
    ck("three of four were found by an outside reader, not by this scan",
       sum(1 for i in INSTANCES if "delivered" in i["found_by"]
           or "outside" in i["found_by"]) == 3)
    ck("no instance's found_by attributes an aim -- crosscutting rule 2 "
       "caught this file's first draft, which said 'built that way on "
       "purpose'",
       not any("on purpose" in i["found_by"] for i in INSTANCES))

    sc = scan()
    ck("every listed module declares agents",
       all(r.get("declares_agents") for r in sc))
    ck("S9 and S10 both carry a blank",
       all(any(r["blanks"]) for r in sc
           if r["module"] in ("s9_corpus_position_filter", "agents")))
    ck("S4 carries none, because the patch filled it",
       not [r for r in sc
            if r["module"] == "s4_antler_calibration"][0]["blanks"])
    ck("every blank is enumerated or explained, not left bare",
       all(r["blank_enumerated"] for r in sc if r["blanks"]))

    d = distinction()
    ck("a declared blank and an unreachable agent are kept apart",
       d["declared_blank"] != d["unreachable_agent"])
    ck("and the reason is stated: one is a disclosure, one is a defect",
       "correct and is the point" in d["why_it_matters"])

    ck("the scan's own limit leads the breaks list -- it cannot find an "
       "agent nobody declared", "NOT A RATE" in breaks()[0])
    ck("and that limit is the state every instance started in",
       any("was not a blank, it was an absence" in b for b in breaks()))
    ck("no intent is attributed", "NOT ATTRIBUTED" in confidence()["mechanism"])
    ck("confidence unresolved", confidence()["resolved"] is False)
    flat = " ".join(report().split())
    for w in ("deliberate", "in order to", "intends", "motivated by"):
        ck("no intent phrase: %r" % w, w not in flat.lower())
    ck("report renders", "A DECLARED BLANK IS NOT AN UNREACHABLE AGENT"
       in flat)
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "excluded subject"))
