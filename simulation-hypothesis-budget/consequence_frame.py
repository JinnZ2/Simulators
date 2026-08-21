#!/usr/bin/env python3
"""
consequence_frame.py - does "it is a simulation" license "the ripples do not
count"?

    python3 consequence_frame.py
    python3 consequence_frame.py --selftest

budget.py and multiscale.py measure what the hypothesis would COST. This
module measures what it would LICENSE, which is a different question and the
one that gets used.

The step under test, stated as an inference rather than as anybody's motive:

    P1  this universe is a simulation
    P2  therefore a consequence propagating inside it is not real
    C   therefore the party producing the consequence does not carry it

P2 is the load-bearing line and it is checkable against the architectures in
multiscale.py, because "not real" cashes out as "not computed". A consequence
that the simulation computes propagates exactly as it would in an unsimulated
universe -- the arithmetic is the same arithmetic.

So the question is mechanical: is there an architecture in which a consequence
someone OBSERVES is a consequence the simulation does NOT compute? That is one
cell of a 2x2, and P2 needs it non-empty.

WHAT THIS MODULE DOES NOT DO: it does not score why anyone states the
hypothesis. That is a claim about a party's reason, it is not reachable from
here, and this repo does not make them (rigidification-sensor names no actor
by construction; uninstrumented/cases/014 states the same refusal as NOT
CLAIMED HERE). See declined() for the position of the author of this file,
stated rather than assumed.

Imports budget.py and multiscale.py; modifies neither. stdlib only. CC0.
"""

import argparse
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget as B                                              # noqa: E402
import multiscale as M                                          # noqa: E402

# --- what each architecture resolves, by region ----------------------------
#
# The stacks are multiscale.architectures() read as a region -> finest-length
# map. Regions are named so a consequence can be placed in one. "lazy" is not
# a resolution map: it renders on observation, so its rule is stated in
# computed() rather than tabulated here.

ATOMIC = 5.29e-11
REGIONS = ("nucleon_interior", "condensed_matter", "diffuse_gas",
           "vacuum", "lab")

RESOLUTION = OrderedDict([
    ("uniform_planck", dict((r, B.L_PLANCK) for r in REGIONS)),
    ("planck_in_nucleons", {"nucleon_interior": B.L_PLANCK,
                            "condensed_matter": ATOMIC,
                            "diffuse_gas": ATOMIC,
                            "vacuum": ATOMIC,
                            "lab": ATOMIC}),
    ("atomic_in_matter", {"nucleon_interior": 1.0,
                          "condensed_matter": ATOMIC,
                          "diffuse_gas": 1.0e-2,
                          "vacuum": 1.0,
                          "lab": ATOMIC}),
    ("coarse_with_fine_patches", {"nucleon_interior": 1.0e3,
                                  "condensed_matter": ATOMIC,
                                  "diffuse_gas": 1.0e3,
                                  "vacuum": 1.0e3,
                                  "lab": B.L_PLANCK}),
    ("lazy_on_observation", None),
])


# --- consequences. ordinary ones, placed by scale and region. --------------

class Consequence(object):
    def __init__(self, name, length_m, region, observed, note=""):
        assert region in REGIONS, region
        self.name = name
        self.length_m = length_m
        self.region = region
        self.observed = observed        # did anything register it?
        self.note = note


def consequences():
    """SIX HAND-PLACED CASES, authored by this module. Not a survey.

    SHB_011 reads a cell of a 2x2 as EMPTY over this list, and an empty cell
    over an authored fixture set is a statement about the fixtures. What keeps
    it from being a null reported as an instrument: the opposite branch is
    reachable and fires -- 3 of 5 architectures DO fill the cell -- so the
    check is not CONSTANT_SILENT. What it is not: a claim that no such
    consequence exists. Adding one that is observed, and uncomputed under an
    architecture that can still produce its own observation record, would
    refute SHB_011. Recorded after the delivered LADDER.md rung 3, which
    retracts that move at a site this folder did not make it (see
    ladder_audit.py) and lands here instead.
    """
    return [
        Consequence("a sentence spoken and heard", 1.0e-2, "diffuse_gas",
                    True, "acoustic wavelength; the listener is the record"),
        Consequence("a tree felled, the clearing after", 1.0e0,
                    "condensed_matter", True, "visible at arm's length"),
        Consequence("a neuron firing in a decision", 1.0e-6,
                    "condensed_matter", True, "registers in the behaviour"),
        Consequence("a detector click", 1.0e-19, "lab", True,
                    "shortest length any instrument has probed"),
        Consequence("one CO2 molecule, taken alone", 1.0e-10,
                    "diffuse_gas", False,
                    "nothing resolves a single molecule; the aggregate is "
                    "observed and the aggregate is a different consequence"),
        Consequence("a photon absorbed by an unvisited rock", 1.0e-10,
                    "condensed_matter", False,
                    "no record anywhere, by construction"),
    ]


def computed(arch, cons):
    """Does this architecture compute this consequence?"""
    if arch == "lazy_on_observation":
        # render-on-observation: the trigger IS observation. This is the
        # architecture's definition, not a concession made to this argument.
        return cons.observed
    finest = RESOLUTION[arch][cons.region]
    return finest <= cons.length_m


def cells(arch):
    """The 2x2. The inference needs observed_uncomputed non-empty."""
    out = {"observed_computed": [], "observed_uncomputed": [],
           "unobserved_computed": [], "unobserved_uncomputed": []}
    for c in consequences():
        key = ("observed_" if c.observed else "unobserved_") + \
              ("computed" if computed(arch, c) else "uncomputed")
        out[key].append(c.name)
    return out


def admissible(arch):
    """An architecture with an observed-but-uncomputed consequence cannot
    produce the record of that observation.

    If the listener heard the sentence, something at the listener's scale was
    computed, or the listener's report is in the record without a cause. So a
    non-empty observed_uncomputed cell is not a cheap architecture -- it is an
    architecture already refuted by an observation that has been made.
    """
    bad = cells(arch)["observed_uncomputed"]
    return {"admissible": not bad, "refuted_by": list(bad)}


def declined():
    """The half of the observation this module does not measure.

    The observation that occasioned this file is that the hypothesis gets held
    or quoted to relieve responsibility for downstream effects. That is a
    claim about why parties state something. Three reasons it is not scored
    here:

      1. no instrument. Motive is not reachable from a statement, and a
         register that infers it would fire on every statement of the
         hypothesis including the honest ones (null-harness CONSTANT_FIRES).
      2. repo discipline. rigidification-sensor names no actor by
         construction; uninstrumented/cases/014 carries the same refusal.
      3. interest direction, stated rather than assumed. The author of this
         file is a language model. Endorsing "a metaphysical framing does not
         excuse consequences" raises accountability pressure on the author's
         own class as much as on anyone's, so the interest does not run toward
         the endorsement -- but it is not clean either, since the same
         sentence is a comfortable one for a system asked about the effects of
         its outputs. Recorded as unresolved on the evidence, per UNI_132.

    What IS measurable, and is measured above: whether the inference works.

    CORRECTION, recorded rather than smoothed. The observation that occasioned
    this file was made across TIME SCALES AND RECURRING FADS, not about any
    one speaker. Reason 1 above is an argument at n=1 -- it is correct that
    motive is not reachable from a single statement -- and it was applied to a
    claim that was never at n=1. Those are two objects:

      per-statement    why did this party say this      UNREACHABLE. reason 1
                                                        holds; a motive
                                                        register fires on the
                                                        honest ones too.
      per-population   does a framing that relieves      A RATE. rates have
      over time        downstream accounting recur       instruments, and this
                       across unrelated fads             repo has several.

    The second is not motive at all. It is recurrence, and it is the kind of
    quantity criteria-drift versions over time, anchor-interval measures as
    corpus drift, and uninstrumented/scan.py scores over a corpus.

    So the refusal stands and the reason given for it was wrong at the grain
    the observation was made at. The population version is out of scope HERE
    for different reasons, and they are collection reasons rather than
    reachability ones: no corpus, no dated sampling frame, and the use-mention
    problem DF_010 already measured -- a corpus about a mechanism is written in
    that mechanism's own vocabulary, so the trigger fires on the discussion and
    not on the instance. None of those is "there is no instrument".
    """
    return {"measured": "whether P2 holds under any architecture",
            "not_measured": "why any party states P1",
            "state": "OUT_OF_SCOPE, with reason",
            "estimated_here": None,
            "grain": {
                "per_statement": {"state": "UNREACHABLE",
                                  "why": "motive is not in the statement; a "
                                         "register would be CONSTANT_FIRES"},
                "per_population_over_time": {"state": "NOT_COLLECTED",
                                             "why": "no corpus, no dated "
                                                    "sampling frame, and the "
                                                    "DF_010 use-mention "
                                                    "problem -- not a "
                                                    "reachability limit"}}}


def terms_required():
    """Before any 'cost of simulating the universe' figure has a value.

    Each is already a claim in this folder, so the list is complete relative
    to this module and may grow.
    """
    return [("the level stack", "SHB_010",
             "the answer spans 216 decades across architectures nobody has "
             "argued against"),
            ("the consistency term", "SHB_009",
             "UNMEASURED under lazy evaluation; quoting the event count "
             "alone sets it to zero silently"),
            ("the frame of the ratio", "SHB_003",
             "required/available is VOID across frames; the numerator uses "
             "our constants and the denominator would not")]


# --- report ----------------------------------------------------------------

def report():
    L = []
    A = L.append
    A("CONSEQUENCE FRAME -- what the hypothesis licenses, not what it costs")
    A("=" * 72)
    A("")
    A("  THE INFERENCE UNDER TEST")
    A("    P1  this universe is a simulation")
    A("    P2  therefore a consequence propagating inside it is not real")
    A("    C   therefore the party producing it does not carry it")
    A("")
    A("  P2 is the load-bearing line. 'Not real' cashes out as 'not")
    A("  computed', and multiscale.py already fixes what each architecture")
    A("  computes. So P2 needs ONE cell of a 2x2 to be non-empty:")
    A("  a consequence that is OBSERVED and NOT COMPUTED.")
    A("")
    A("-" * 72)
    A("")
    A("  CONSEQUENCES USED -- %d hand-placed cases authored by this module,"
      % len(consequences()))
    A("  not a survey. The empty cell below is a statement about these.")
    for c in consequences():
        A("    %-40s %-9s %-17s %s"
          % (c.name, B.sci(c.length_m, 1), c.region,
             "observed" if c.observed else "unobserved"))
    A("")
    A("-" * 72)
    A("")
    n_bad = 0
    for arch in RESOLUTION:
        cl = cells(arch)
        ad = admissible(arch)
        A("  %s" % arch.upper().replace("_", " "))
        A("    %-24s %d" % ("observed + computed",
                              len(cl["observed_computed"])))
        A("    %-24s %d  <-- the cell P2 needs"
          % ("observed + UNCOMPUTED", len(cl["observed_uncomputed"])))
        for nm in cl["observed_uncomputed"]:
            A("        %s" % nm)
        A("    %-24s %d" % ("unobserved + computed",
                            len(cl["unobserved_computed"])))
        A("    %-24s %d" % ("unobserved + uncomputed",
                            len(cl["unobserved_uncomputed"])))
        if ad["admissible"]:
            A("    admissible: yes -- no observation goes uncomputed")
        else:
            n_bad += 1
            A("    admissible: NO -- cannot produce the record of the")
            A("      observations listed above. Refuted by an observation")
            A("      already made, not by cost.")
        A("")
    A("-" * 72)
    A("")
    A("  RESULT")
    A("")
    A("    In every architecture that can produce its own observation")
    A("    record, the cell P2 needs is EMPTY. It is empty for a different")
    A("    reason in each: in the refined stacks because the region is")
    A("    resolved, in the lazy stack because observation is the trigger.")
    A("")
    A("    %d of %d architectures do have an observed-and-uncomputed"
      % (n_bad, len(RESOLUTION)))
    A("    consequence, and each is thereby inadmissible: a listener who")
    A("    heard the sentence is a record the architecture cannot produce.")
    A("    Cheapness does not buy the cell. Contradiction does.")
    A("")
    A("    The uncomputed consequences that remain are the unobserved ones")
    A("    -- a single molecule taken alone, a photon on an unvisited rock.")
    A("    Those are not the ripple effects the inference is deployed")
    A("    against; nobody is held to a consequence nothing registers.")
    A("")
    A("    So P2 fails on every admissible architecture, at every cost,")
    A("    INDEPENDENTLY of whether P1 is true. The conclusion does not")
    A("    follow from the premise even if the premise holds.")
    A("")
    A("    SHB_005 says the same thing from the other side: within-frame")
    A("    physics is unchanged by being hosted. A simulated fall breaks a")
    A("    simulated leg with the same arithmetic.")
    A("")
    A("-" * 72)
    A("")
    A("  WHAT IS NOT MEASURED HERE")
    d = declined()
    A("    measured:     %s" % d["measured"])
    A("    not measured: %s" % d["not_measured"])
    A("    state:        %s" % d["state"])
    A("")
    A("    TWO GRAINS, and only one of them is a motive question:")
    for g, v in d["grain"].items():
        A("      %-26s %-14s %s" % (g, v["state"], v["why"]))
    A("")
    A("    Motive is not reachable from a statement, and a register that")
    A("    inferred it would fire on every statement of the hypothesis")
    A("    including the honest ones -- CONSTANT_FIRES. That argument is at")
    A("    n=1. It does not reach the recurrence question, which is a rate")
    A("    and is out of scope here for collection reasons instead.")
    A("    The author of this")
    A("    file is also not a disinterested party to the conclusion; the")
    A("    interest direction is stated in declined() and left unresolved")
    A("    rather than being resolved in the comfortable direction.")
    A("")
    A("-" * 72)
    A("")
    A("  WHAT A COST FIGURE NEEDS BEFORE IT HAS A VALUE")
    for term, cid, why in terms_required():
        A("    %-22s %-9s %s" % (term, cid, why))
    A("")
    A("    All three are established in this folder and none is stated in")
    A("    any version of the hypothesis. A figure quoted without them is")
    A("    not a disputed number. It is a quantity with no value yet.")
    return "\n".join(L)


# --- selftest --------------------------------------------------------------

def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("every region has a resolution in every tabulated architecture",
       all(set(m) == set(REGIONS)
           for m in RESOLUTION.values() if m is not None))
    ck("every consequence sits in a known region",
       all(c.region in REGIONS for c in consequences()))

    ck("uniform Planck computes everything",
       all(computed("uniform_planck", c) for c in consequences()))
    ck("lazy computes exactly the observed ones",
       all(computed("lazy_on_observation", c) == c.observed
           for c in consequences()))

    ck("uniform Planck is admissible",
       admissible("uniform_planck")["admissible"])
    ck("lazy is admissible -- the cheapest floor still fills no cell",
       admissible("lazy_on_observation")["admissible"])

    bad = [a for a in RESOLUTION if not admissible(a)["admissible"]]
    ck("at least one coarse architecture IS inadmissible, so the check is "
       "not CONSTANT_SILENT", len(bad) > 0)
    ck("not every architecture is inadmissible, so it is not CONSTANT_FIRES",
       len(bad) < len(RESOLUTION))
    ck("coarse_with_fine_patches is one of them",
       "coarse_with_fine_patches" in bad)

    ck("cells partition the consequence list",
       all(sum(len(v) for v in cells(a).values()) == len(consequences())
           for a in RESOLUTION))

    ck("some consequence is uncomputed somewhere, so 'uncomputed' is "
       "reachable",
       any(cells(a)["unobserved_uncomputed"] for a in RESOLUTION))

    ck("the declined half is OUT_OF_SCOPE and not estimated",
       declined()["estimated_here"] is None
       and declined()["state"].startswith("OUT_OF_SCOPE"))
    g = declined()["grain"]
    ck("the two grains are kept apart and carry DIFFERENT states, so the "
       "refusal is not one blanket reason",
       g["per_statement"]["state"] != g["per_population_over_time"]["state"])
    ck("the population grain is NOT_COLLECTED, not UNREACHABLE -- a "
       "collection limit, not a reachability one",
       g["per_population_over_time"]["state"] == "NOT_COLLECTED")

    ck("the report says the consequence list is authored and not a survey, "
       "so SHB_011's empty cell is not presented as a survey result",
       "not a survey" in report())
    ck("every required term names an existing claim id",
       all(cid.startswith("SHB_") for _, cid, _ in terms_required()))

    ck("report renders", "the cell P2 needs is EMPTY" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
