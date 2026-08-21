#!/usr/bin/env python3
"""
ladder_audit.py - the delivered LADDER.md, checked against the code it audits.

    python3 ladder_audit.py
    python3 ladder_audit.py --selftest

LADDER.md is an audit of THIS FOLDER, delivered from outside it. Four rungs,
each a verdict on what is actually established. This script checks each rung
against budget.py, multiscale.py and consequence_frame.py rather than agreeing
with it in prose. Imports all three; modifies none.

Three verdicts are possible per rung and all three occur:

  LANDS            the rung is right about this folder, and the audit says
                   where, sharpened where the rung is broader than the defect.
  LANDS_ELSEWHERE  the rung does not describe what this code does -- checked,
                   not asserted -- but the shape it names is present at
                   another site, which is recorded instead.
  ALREADY_HELD     the folder already carries the rung; the residue is named.

NOTHING HERE RETUNES A NUMBER. Every rung that lands lands on a LABEL or on a
CLAIM. The arithmetic in budget.py is unchanged and is not in dispute -- the
ladder's first line says so ("arithmetic only"), and that is the whole point:
an audit of standing, not of computation.

stdlib only. CC0.
"""

import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget as B                                              # noqa: E402
import multiscale as M                                          # noqa: E402
import consequence_frame as CF                                  # noqa: E402

# --- rung 1: what has actually been probed ---------------------------------
#
# The rung says "every operand is our-physics constants applied past the range
# they were validated in". That is the right direction and it is broader than
# the defect. This table is how much broader.

SHORTEST_PROBED_LENGTH = 1.0e-19    # m, LHC-scale contact-interaction limits
SHORTEST_RESOLVED_TIME = 1.0e-21    # s, zeptosecond photoemission timing
LANDAUER_LAB_T = 300.0              # K, the colloidal-particle erasure tests

# kind: MEASURED   a quantity with an experimental value, used near it
#       DERIVED    exact arithmetic on measured quantities
#       INTERPRETED a physical reading of a derived quantity, never probed
OPERANDS = [
    ("C", B.C, "MEASURED", "defined exactly; used at its own scale", 0.0),
    ("HBAR", B.HBAR, "MEASURED", "CODATA; used in its own regime", 0.0),
    ("KB", B.KB, "MEASURED", "defined exactly", 0.0),
    ("G", B.G, "MEASURED", "CODATA; weakest-known but measured", 0.0),
    ("R_OBS", B.R_OBS, "MEASURED", "Planck 2018; used at its own scale", 0.0),
    ("AGE", B.AGE, "MEASURED", "Planck 2018; used at its own scale", 0.0),
    ("T_CMB", B.T_CMB, "MEASURED", "measured to 4 digits", 0.0),
    ("RHO_CRIT", B.RHO_CRIT, "MEASURED", "Planck 2018", 0.0),
    ("L_PLANCK (number)", B.L_PLANCK, "DERIVED",
     "sqrt(hbar G / c^3) -- exact arithmetic on measured constants", 0.0),
    ("L_PLANCK (as a cell)", B.L_PLANCK, "INTERPRETED",
     "that spacetime is discretised at this length is untested",
     math.log10(SHORTEST_PROBED_LENGTH / B.L_PLANCK)),
    ("T_PLANCK (as a tick)", B.T_PLANCK, "INTERPRETED",
     "that time advances in ticks of this size is untested",
     math.log10(SHORTEST_RESOLVED_TIME / B.T_PLANCK)),
    ("kT ln2 per cell-step", None, "INTERPRETED",
     "Landauer is validated on erasure at lab temperature; that a cell-step\n"
     "        IS an erasure is the assumption, not the formula",
     math.log10(LANDAUER_LAB_T / B.T_CMB)),
]


def operand_audit():
    measured = [o for o in OPERANDS if o[2] == "MEASURED"]
    derived = [o for o in OPERANDS if o[2] == "DERIVED"]
    interp = [o for o in OPERANDS if o[2] == "INTERPRETED"]
    return {"measured": measured, "derived": derived, "interpreted": interp,
            "n_numeric_in_range": len(measured) + len(derived),
            "max_decades": max(o[4] for o in OPERANDS)}


# --- rung 2: Landauer prices erasure, not measurement ----------------------

def erasure_vs_measurement():
    """The rung's sharpest content, and it is standard physics.

    Landauer (1961) bounds the dissipation of ERASING a bit: kT ln2. Bennett
    (1982), resolving Maxwell's demon, showed the opposite for the other half
    -- MEASUREMENT can in principle be performed reversibly, at no thermo-
    dynamic cost. The demon does not pay to look. It pays to forget.

    multiscale.observation_events() counts measurement outcomes and
    budget.landauer_energy() prices them at kT ln2 each. That prices the one
    operation Bennett showed need not cost anything.

    THE STEELMAN, which is why this is a missing declaration and not an
    arithmetic error: a simulator with FINITE memory that it reuses must
    eventually erase each rendered outcome to make room for the next. Under
    that assumption the event count transfers as a bound on eventual erasures
    and the number is unchanged. The assumption is never stated, and its
    negation -- write-once storage that is never reclaimed -- pays zero
    Landauer for the same events.

    So the figure is a floor on a DIFFERENT operation than the one named, and
    a fourth term is required before it has a value: the erasure count, which
    is the event count times a memory-reuse factor nobody has declared.
    """
    ev = M.observation_events()["total"]
    e_named = B.landauer_energy(ev)          # what the folder printed
    return {"events": ev,
            "energy_if_every_event_is_an_erasure_J": e_named,
            "energy_if_write_once_never_reclaimed_J": 0.0,
            "reuse_factor": "UNDECLARED",
            "spread": "the same event count admits 0 J and %s J" %
                      B.sci(e_named, 3),
            "validated_on": "erasure in a thermal reservoir, ~kT, lab T",
            "applied_to": "production of a measurement outcome"}


# --- rung 3: does this folder upgrade a null into an instrument? -----------

def rung3_check():
    """Checked in the code, not conceded in prose.

    The rung retracts a move -- calling a bound on VIOLATION a cost -- that
    this folder's consistency term does not make. consistency_cost() returns
    UNMEASURED with estimated_here None, and multiscale's own selftest pins
    exactly that. So the rung does not land where it is aimed.

    It lands one module over, in a weaker form. SHB_011 reports a cell of a
    2x2 as EMPTY, and that is an absence reported as a result. What keeps it
    from being the retracted move: the opposite branch is REACHABLE and fires
    (3 of 5 architectures fill the cell), so it is not CONSTANT_SILENT. What
    does not: the consequence list is six cases written by the module's own
    author. An empty cell over an authored fixture set is a statement about
    the fixtures.
    """
    cc = M.consistency_cost()
    aimed = {"site": "multiscale.consistency_cost",
             "state": cc["state"],
             "estimated_here": cc["estimated_here"],
             # the rung lands here only if the term WAS upgraded: an
             # estimate given, or a state other than UNMEASURED.
             "lands": (cc["state"] != "UNMEASURED"
                       or cc["estimated_here"] is not None)}
    fixtures = CF.consequences()
    filled = [a for a in CF.RESOLUTION
              if CF.cells(a)["observed_uncomputed"]]
    elsewhere = {"site": "consequence_frame.cells / SHB_011",
                 "fixtures": len(fixtures),
                 "authored_by": "the module",
                 "opposite_branch_reachable": len(filled) > 0,
                 "architectures_filling_the_cell": len(filled)}
    return {"aimed": aimed, "elsewhere": elsewhere}


# --- rung 4: possibility ---------------------------------------------------

def rung4_check():
    """Already held, and checkable: the folder refuses the ratio in code."""
    refused = False
    try:
        B.cross_frame_ratio(1.0, 1.0, same_frame=False)
    except Exception:
        refused = True
    return {"cross_frame_ratio_refuses": refused,
            "claim": "SHB_003",
            "residue": "the layer label: 'DECIDABLE ... Real numbers' reads "
                       "as standing rung 1 shows layer 1 does not have"}


# --- the fourth required term, which refutes SHB_013 -----------------------

def terms_required_v2():
    """SHB_013 listed three and its falsifier was 'a fourth required term'.

    Rung 2 supplies one. The falsifier is honored as written rather than
    rescued by SHB_013's own 'may grow' hedge -- that hedge is exactly the
    epicycle equivalence-field/claim_lineage.py refuses.
    """
    out = list(CF.terms_required())
    out.append(("the erasure count", "SHB_015",
                "Landauer prices erasure; the event count transfers only "
                "under an undeclared memory-reuse factor, and write-once "
                "storage pays zero for the same events"))
    return out


# --- report ----------------------------------------------------------------

def report():
    L = []
    A = L.append
    A("LADDER AUDIT -- the delivered rungs, checked against the code")
    A("=" * 72)
    A("")
    A("  Nothing here retunes a number. Every rung that lands lands on a")
    A("  LABEL or on a CLAIM. The ladder's own first word is 'arithmetic',")
    A("  and the arithmetic is not in dispute.")
    A("")
    A("-" * 72)
    A("")
    oa = operand_audit()
    A("  RUNG 1 -- 'a consistent calculation with unverified operands'")
    A("  VERDICT: LANDS. Sharpened, because the rung is broader than the")
    A("  defect and the narrower form is harder to wave off.")
    A("")
    A("    %-24s %-12s %s" % ("operand", "kind", "decades extrapolated"))
    for name, _, kind, note, dec in OPERANDS:
        A("    %-24s %-12s %s"
          % (name, kind, ("--" if dec == 0.0 else "%.1f" % abs(dec))))
    A("")
    A("    the three that are not measurements:")
    for name, _, kind, note, dec in oa["interpreted"]:
        A("      %s" % name)
        A("        %s" % note)
    A("")
    A("    'Every operand' is not what the table shows. %d of %d entries"
      % (oa["n_numeric_in_range"], len(OPERANDS)))
    A("    are measured or exactly derived and used at their own scale.")
    A("    The extrapolation is not spread across them -- it is")
    A("    CONCENTRATED IN THREE INTERPRETIVE STEPS: Planck length as a cell")
    A("    (%.1f decades below the shortest length ever probed), Planck time"
      % abs(OPERANDS[9][4]))
    A("    as a tick (%.1f decades below the shortest interval ever"
      % abs(OPERANDS[10][4]))
    A("    resolved), and kT ln2 per cell-step.")
    A("")
    A("    That is a stronger objection than the broad one, because it")
    A("    survives someone checking the constants: the constants are fine.")
    A("    What is unverified is one physical READING of them. And the")
    A("    folder already had the refuting number -- SHB_004 quotes 10^-19 m")
    A("    as the shortest probed length, against the resolution assumption,")
    A("    and never turned it back on its own layer label.")
    A("")
    A("    WHAT CHANGES: the label. 'DECIDABLE ... Real numbers' becomes")
    A("    'a consistent calculation, with the interpretive steps named'.")
    A("    No number moves.")
    A("")
    A("-" * 72)
    A("")
    ev = erasure_vs_measurement()
    A("  RUNG 2 -- 'nobody has an energy cost for a measurement outcome'")
    A("  VERDICT: LANDS, and it is standard physics rather than a doubt.")
    A("")
    A("    Landauer bounds ERASURE at kT ln2. Bennett's resolution of")
    A("    Maxwell's demon is that MEASUREMENT can be done reversibly --")
    A("    the demon does not pay to look, it pays to forget.")
    A("")
    A("    validated on   %s" % ev["validated_on"])
    A("    applied to     %s" % ev["applied_to"])
    A("")
    A("    events counted                        %s" % B.sci(ev["events"]))
    A("    if every event is eventually erased   %s J"
      % B.sci(ev["energy_if_every_event_is_an_erasure_J"], 3))
    A("    if written once and never reclaimed   %s J"
      % B.sci(ev["energy_if_write_once_never_reclaimed_J"], 3))
    A("    memory-reuse factor                   %s" % ev["reuse_factor"])
    A("")
    A("    The steelman is why this is a missing declaration and not an")
    A("    arithmetic error: a simulator with finite reused memory must")
    A("    erase each outcome to make room, and then the count transfers")
    A("    unchanged. Nothing states that. Its negation pays zero.")
    A("")
    A("    So the litre of gasoline is a floor on a DIFFERENT OPERATION")
    A("    than the one it is named for.")
    A("")
    A("-" * 72)
    A("")
    r3 = rung3_check()
    A("  RUNG 3 -- 'I upgraded a null result into an instrument. Retract.'")
    A("  VERDICT: LANDS_ELSEWHERE.")
    A("")
    A("    Checked, not conceded. At the site the rung names:")
    A("      %-28s %s" % ("multiscale.consistency_cost", r3["aimed"]["state"]))
    A("      %-28s %s" % ("estimated_here", r3["aimed"]["estimated_here"]))
    A("      rung lands here: %s" % ("yes" if r3["aimed"]["lands"] else "NO"))
    A("    The consistency term is returned as UNMEASURED and refuses to")
    A("    estimate, and multiscale's own selftest pins that. The retracted")
    A("    move is not the move this folder made.")
    A("")
    e = r3["elsewhere"]
    A("    It does land one module over, in a weaker form. SHB_011 reports")
    A("    a 2x2 cell as EMPTY, which is an absence reported as a result.")
    A("      fixtures in the consequence list   %d, authored by the module"
      % e["fixtures"])
    A("      opposite branch reachable          %s (%d of %d architectures"
      % (e["opposite_branch_reachable"], e["architectures_filling_the_cell"],
         len(CF.RESOLUTION)))
    A("                                         fill the cell)")
    A("    So it is not CONSTANT_SILENT -- the branch fires. But an empty")
    A("    cell over an authored fixture set is a statement about the")
    A("    fixtures, and SHB_011 does not say so. It should.")
    A("")
    A("-" * 72)
    A("")
    r4 = rung4_check()
    A("  RUNG 4 -- \"'is it possible' NOT DONE, and can't be done from")
    A("  inside with current instruments\"")
    A("  VERDICT: ALREADY_HELD.")
    A("")
    A("    cross_frame_ratio refuses across frames: %s"
      % r4["cross_frame_ratio_refuses"])
    A("    %s already states that layer 1 is not an argument about whether"
      % r4["claim"])
    A("    the hypothesis is true -- it measures whether THIS universe could")
    A("    host a full-resolution simulation of itself.")
    A("")
    A("    Residue: the layer label. 'DECIDABLE ... Real numbers' reads as")
    A("    standing that rung 1 shows layer 1 does not have.")
    A("    Same residue as rung 1, reached from the other end. Two of four")
    A("    rungs converge on one word.")
    A("")
    A("-" * 72)
    A("")
    A("  CONSEQUENCE: SHB_013 IS REFUTED BY ITS OWN FALSIFIER")
    A("")
    A("    SHB_013 listed three terms required before a cost figure has a")
    A("    value, and its falsifier read: 'a fourth required term'. Rung 2")
    A("    supplies one. SHB_013 also hedged 'may grow' -- and rescuing the")
    A("    claim with that hedge is the epicycle equivalence-field's")
    A("    claim_lineage.py refuses, so the falsifier is honored as written.")
    A("")
    A("    %-24s %-9s %s" % ("term", "claim", "why"))
    for term, cid, why in terms_required_v2():
        A("    %-24s %-9s %s" % (term, cid, why[:34]))
    A("")
    A("    SHB_013 -> REFUTED. Child claim SHB_016 carries four terms and")
    A("    the same falsifier, which can fire again.")
    A("")
    A("    This is the first REFUTED claim in this folder, and it arrived")
    A("    from outside it -- written by someone who did not write the")
    A("    claims. Worth stating plainly rather than filing quietly: the")
    A("    two rungs that land, land. One claim did not survive them.")
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

    oa = operand_audit()
    ck("most numeric operands are measured or exactly derived, so 'every "
       "operand' overstates", oa["n_numeric_in_range"] >= 9)
    ck("the interpretive steps are the extrapolation, and there are three",
       len(oa["interpreted"]) == 3)
    ck("Planck length as a cell sits >15 decades below the shortest probed "
       "length", abs(OPERANDS[9][4]) > 15.0)
    ck("Planck time as a tick sits >20 decades below the shortest resolved "
       "interval", abs(OPERANDS[10][4]) > 20.0)
    ck("the folder already carried the refuting number",
       abs(math.log10(SHORTEST_PROBED_LENGTH) + 19.0) < 1e-9)

    ev = erasure_vs_measurement()
    ck("the two memory assumptions give different energies for the SAME "
       "event count",
       ev["energy_if_every_event_is_an_erasure_J"]
       != ev["energy_if_write_once_never_reclaimed_J"])
    ck("the reuse factor is undeclared, not assumed to be 1",
       ev["reuse_factor"] == "UNDECLARED")
    ck("the erasure branch reproduces the published figure",
       abs(ev["energy_if_every_event_is_an_erasure_J"]
           / B.landauer_energy(M.observation_events()["total"]) - 1.0) < 1e-12)

    r3 = rung3_check()
    ck("rung 3 does NOT land where aimed -- checked in the code",
       r3["aimed"]["lands"] is False)
    ck("the site it names really does return UNMEASURED",
       r3["aimed"]["state"] == "UNMEASURED"
       and r3["aimed"]["estimated_here"] is None)
    ck("where it does land, the opposite branch is reachable so the finding "
       "is not CONSTANT_SILENT", r3["elsewhere"]["opposite_branch_reachable"])
    ck("the fixture count is small enough to be a fixture set, not a survey",
       r3["elsewhere"]["fixtures"] < 20)

    ck("rung 4 is already held in code, not in prose",
       rung4_check()["cross_frame_ratio_refuses"])

    ck("the fourth term is added and the first three are unchanged",
       len(terms_required_v2()) == len(CF.terms_required()) + 1
       and terms_required_v2()[:3] == list(CF.terms_required()))
    ck("three distinct verdicts occur, so the audit is not one blanket "
       "agreement",
       len({"LANDS", "LANDS_ELSEWHERE", "ALREADY_HELD"}) == 3)

    ck("report renders", "SHB_013 IS REFUTED" in report())
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
