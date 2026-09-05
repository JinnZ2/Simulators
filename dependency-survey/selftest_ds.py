#!/usr/bin/env python3
"""Checks for the dependency survey against the seeded CELLS.md, which is
the human-editable data store. Known answers first, both directions.
Writes samples/.

    python3 dependency-survey/selftest_ds.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import survey as S  # noqa: E402
import gaps as G  # noqa: E402
import report as R  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_ds")
    for f in ("survey.py", "gaps.py", "report.py", "run_all.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)

    g = S.grid()
    check("the grid is exactly 25 cells (5 terms x 5 substrates)", len(g) == 25)
    c = S.counts(g)
    check("three cells coded, 22 never-coded UNKNOWN",
          c["UNKNOWN"] == 22 and (c["MEASURED"] + c["MISSING"] + c["SCOPE-DIFFERENT"] + c["scope_incomplete"] + c["measured_no_units"]) == 3)

    # ---- the units rule, both directions
    check("a MEASURED_AS with a slash rate states units; a unitless phrase does not",
          S.has_units("energy intake per unit handling time, J/s") and not S.has_units("cost asymmetry between the parties"))
    check("T1 x S1 is validly MEASURED (J/s)", S.is_valid_measured(g[("T1", "S1")]))
    ok, _ = S.validate({"status": "MEASURED", "measured_as": "a big quantity", "scope_note": "", "provisional": False})
    check("a MEASURED cell whose measured_as states no units is INVALID and downgraded to MISSING",
          not ok and S.effective_status({"status": "MEASURED", "measured_as": "a big quantity"}, False) == "MISSING (downgraded: no units)")

    # ---- ADDENDUM_01: SCOPE-DIFFERENT needs a SCOPE_TRANSFORM, not units
    t3s5 = g[("T3", "S5")]
    check("the seeded T3 x S5 is coded SCOPE-DIFFERENT with a scope_note and no transform, so inadmissible (fails the ADJUSTED rule)",
          t3s5["status"] == "SCOPE-DIFFERENT" and t3s5["scope_note"] and not any(t3s5[f] for f in S.TRANSFORM_FIELDS) and not t3s5["valid"])
    check("its reason names the absent transform fields, and it downgrades to UNKNOWN, counted as scope_incomplete",
          "reference" in t3s5["invalid_reason"] and t3s5["effective_status"] == "UNKNOWN (downgraded: incomplete transform)"
          and ("T3", "S5") in S.scope_incomplete_cells(g) and c["scope_incomplete"] == 1)
    okc, _ = S.validate({"status": "SCOPE-DIFFERENT", "reference": "the drawn accounting boundary", "maps_to": "the same term in S1", "breaks_at": "where an out-of-boundary dependency is load-bearing", "scope_note": ""})
    check("a complete SCOPE_TRANSFORM validates WITHOUT units (the rescope: frame info is not in the quantity's units)", okc)
    oki, _ = S.validate({"status": "SCOPE-DIFFERENT", "reference": "a frame", "maps_to": "a correspondence", "breaks_at": ""})
    check("a SCOPE-DIFFERENT cell missing one transform field is inadmissible (the check is not CONSTANT_FIRES)", not oki)
    check("a SCOPE-DIFFERENT cell downgrades to UNKNOWN, not to MISSING (unlike a no-units MEASURED cell)",
          S.effective_status({"status": "SCOPE-DIFFERENT", "reference": "", "maps_to": "", "breaks_at": ""}, False) == "UNKNOWN (downgraded: incomplete transform)")

    # ---- the gap that falls out of the seed
    gl = G.gaps(g)
    check("exactly one gap: T1 measured in S1, missing in S2", len(gl) == 1 and gl[0]["term"] == "T1" and gl[0]["measured_in"] == "S1" and gl[0]["missing_in"] == "S2")
    check("the gap is PROVISIONAL and OPEN (no transfer stated), carrying the J/s measure on the measured side",
          gl[0]["provisional"] and gl[0]["state"] == "OPEN" and "J/s" in gl[0]["measured_as"])
    check("the transfer question is stated in the target substrate's own units clause", "S2's own units" in gl[0]["transfer_question"])
    # NO-TRANSFER is reachable: a constructed target cell flagged no_transfer flips the gap state
    g2 = dict(g)
    g2[("T1", "S2")] = dict(g[("T1", "S2")], no_transfer=True)
    check("a coded no_transfer flag makes the gap NO-TRANSFER (not CONSTANT)", G.gaps(g2)[0]["state"] == "NO-TRANSFER")
    g3 = dict(g)
    g3[("T1", "S2")] = dict(g[("T1", "S2")], transfer="tokens spent by agent A to block B over tokens spent by B to block A, dimensionless")
    check("a coded transfer answer makes the gap TRANSFER-STATED", G.gaps(g3)[0]["state"] == "TRANSFER-STATED")
    # an invalid MEASURED cell cannot seed a gap as the measured side
    g4 = dict(g)
    g4[("T1", "S1")] = dict(g[("T1", "S1")], measured_as="cost asymmetry, big", valid=False, effective_status="MISSING (downgraded: no units)")
    check("an invalid (no-units) MEASURED cell does not seed a gap", len(G.gaps(g4)) == 0)

    # ---- UNKNOWN kept apart from MISSING
    check("UNKNOWN and MISSING are distinct statuses in the grid",
          g[("T2", "S3")]["status"] == "UNKNOWN" and g[("T1", "S2")]["status"] == "MISSING")

    # ---- renders and the screen
    outs = {"survey": S.render(g), "gaps": G.render(g), "report": R.full_report()}
    check("survey render screens clean (instrument framing only)", not no_severity.hits(outs["survey"]))
    check("gaps render screens clean", not no_severity.hits(outs["gaps"]))
    # the report echoes the delivered T3 x S5 scope_note, which carries "wrong"
    # and "error" verbatim from the order's seed (operator data). Declared
    # exemption, measured with the three-arm harness.
    rep = outs["report"]
    masked = rep.replace("wrong", "not-so").replace("error", "slip")
    check("report render: masked, the screen is clean", not no_severity.hits(masked))
    check("report render: the only firers are the delivered scope_note tokens",
          {w for _, w, _ in no_severity.hits(rep)} == {"wrong", "error"})
    check("report render: a planted word is caught through the exemption",
          {w for _, w, _ in no_severity.hits(masked + "\nthis is broken\n")} == {"broken"})
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "report.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(rep + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
