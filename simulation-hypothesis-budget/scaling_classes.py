#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
scaling_classes.py - the delivered SCALING_CLASSES.md, checked.

    python3 scaling_classes.py
    python3 scaling_classes.py --selftest

An itemised table of eight computational loads against Lloyd's 10^120 ceiling,
with the structural claim that the cut is SCALING CLASS rather than size, and
a closing observation that nature never pays the exponential.

Four of the eight rows reproduce EXACTLY from the terms stated in them. Three
need a construction the table does not give. One has DRIFTED ten decades since
the previous drop, unremarked, and the drift is invisible from inside the
table because the EXCEEDS column tracks whichever total is used.

The structural claim is right in direction and needs one qualification, and
the qualification makes it sharper rather than weaker: polynomial does not fit
automatically -- N^3 at N = 10^50 is 10^150 -- so the cut is scaling class
CROSSED WITH N, and the exact form is the CROSSOVER. 2^N crosses the ceiling
at N = 399. 3^n crosses at n = 252.

And the closing observation retracts ONE of the three EXCEEDS rows without
saying so. "Exhaustive fold search" is an algorithm nature does not use, and
the text says so in its own last paragraph. The quantum row does NOT retract
the same way -- it prices a substrate, not a method -- and that asymmetry is
the strongest thing in the drop.

Imports budget.py and earth_transitions.py; modifies neither.
stdlib only, Python 3.9.
"""

import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget as B                                              # noqa: E402
import earth_transitions as ET                                  # noqa: E402

CEILING = 120.0     # log10 ops, Lloyd, as delivered and checked at SHB_025

# --- the delivered table ---------------------------------------------------
#
# `construction` is the arithmetic the row's own terms imply, where they imply
# one. `stated_log10` is what the table says.

ROWS = [
    {"row": "turbulence, one ocean, 1e8 yr", "stated_log10": 45.0,
     "construction": None, "verdict": "fits",
     "note": "no grid count, Reynolds number or timestep given; DNS cost "
             "depends on all three and the row cannot be rebuilt from what "
             "is printed"},
    {"row": "all Earth fluid dynamics, 4.5e9 yr", "stated_log10": 100.0,
     "construction": None, "verdict": "fits",
     "note": "same gap. the figure is plausible and is not reproducible"},
    {"row": "N-body accretion, 1e30 bodies", "stated_log10": 67.0,
     "construction": ("direct O(N^2) pairwise = 1e60, times ~1e7 timesteps",
                      60.0 + 7.0), "fitted": True, "verdict": "fits",
     "note": "reproducible under an INFERRED construction. Note the "
             "algorithm choice: a Barnes-Hut tree is N log N = 1e32, "
             "35 decades cheaper. The verdict is robust; the number is a "
             "property of the method"},
    {"row": "quantum many-body, N=100", "stated_log10": 30.0,
     "construction": ("2^100", 100 * math.log10(2)), "verdict": "fits"},
    {"row": "quantum many-body, N=300", "stated_log10": 90.0,
     "construction": ("2^300", 300 * math.log10(2)), "verdict": "fits"},
    {"row": "quantum many-body, N=1000", "stated_log10": 301.0,
     "construction": ("2^1000", 1000 * math.log10(2)),
     "verdict": "EXCEEDS", "stated_excess": 181.0},
    {"row": "ONE protein, exhaustive fold search", "stated_log10": 143.0,
     "construction": ("3^300, Levinthal's three states per bond",
                      300 * math.log10(3)),
     "verdict": "EXCEEDS", "stated_excess": 23.0},
    {"row": "nested phase transitions, 4 classes", "stated_log10": 152.0,
     "construction": None, "verdict": "EXCEEDS", "stated_excess": 32.0,
     "note": "DRIFTED. see drift_check()"},
]


def reproduce():
    out = []
    for r in ROWS:
        d = dict(r)
        if r["construction"] is None:
            d["state"] = "NEEDS_UNSTATED_CONSTRUCTION"
            d["computed_log10"] = None
            d["error_decades"] = None
        elif r.get("fitted"):
            # A construction reverse-engineered from the stated value is not
            # a reproduction: the free parameter (here the timestep count)
            # was chosen to match. Kept separate so the count of genuine
            # reproductions is not inflated by my own back-fitting.
            name, val = r["construction"]
            d["state"] = "CONSTRUCTION_FITTED"
            d["computed_log10"] = val
            d["error_decades"] = 0.0
        else:
            name, val = r["construction"]
            d["state"] = ("REPRODUCES"
                          if abs(val - r["stated_log10"]) < 1.0
                          else "DISAGREES")
            d["computed_log10"] = val
            d["error_decades"] = val - r["stated_log10"]
        out.append(d)
    return out


def excess_column_check():
    """Every EXCEEDS row's second number should be total - ceiling."""
    out = []
    for r in ROWS:
        if r["verdict"] != "EXCEEDS":
            continue
        implied = r["stated_log10"] - CEILING
        out.append({"row": r["row"], "stated_excess": r["stated_excess"],
                    "implied": implied,
                    "consistent": abs(implied - r["stated_excess"]) < 0.5})
    return out


# --- the drifted row -------------------------------------------------------

def drift_check():
    """The nested-transitions row against the previous drop and this folder.

    EARTH_TRANSITIONS.md gave 1e162 for stepping x nesting and this table
    gives 1e152 for the same object, with no note. earth_transitions.py's
    coherent cost models give neither. The row is internally consistent at
    BOTH values because the EXCEEDS column is computed from whichever total
    is used, so the drift cannot be seen from inside the table.
    """
    models = {m["model"]: m["log10"] for m in ET.cost_models()}
    return {
        "this_table": 152.0,
        "previous_drop": 162.5,
        "drift_decades": 162.5 - 152.0,
        "coherent_models_here": {
            "event-driven, nested": models["event-driven, nested"],
            "uniform Planck stepping": models["uniform Planck stepping"]},
        "matches_any_coherent_model": any(
            abs(v - 152.0) < 1.0 for v in models.values()),
        "why_invisible": "the EXCEEDS column is total minus ceiling, so it "
                         "moves with the total and the row stays internally "
                         "consistent at any value. A second reader is the "
                         "only thing that catches it",
    }


# --- the structural claim --------------------------------------------------

def crossover(base):
    """The N at which base^N reaches the ceiling. The exact form of the claim."""
    return CEILING / math.log10(base)


def polynomial_counterexample():
    """'everything polynomial FITS' is not general, and the fix is one clause.

    The claim holds for the N's in the table and not for all N. Pairwise
    interactions among Earth's atoms fit; triple-wise do not, at the same N,
    with the same polynomial class.
    """
    n_earth_atoms = math.log10(ET.earth_atoms())
    return [
        {"N_log10": n_earth_atoms, "k": 2, "cost_log10": 2 * n_earth_atoms},
        {"N_log10": n_earth_atoms, "k": 3, "cost_log10": 3 * n_earth_atoms},
    ]


def crossover_table():
    return [
        {"form": "2^N  (quantum many-body, d=2)", "crosses_at": crossover(2),
         "units": "components"},
        {"form": "3^n  (conformation search)", "crosses_at": crossover(3),
         "units": "residues"},
        {"form": "N^2  (pairwise)", "crosses_at": 10.0 ** (CEILING / 2),
         "units": "bodies"},
        {"form": "N^3  (triple-wise)", "crosses_at": 10.0 ** (CEILING / 3),
         "units": "bodies"},
    ]


# --- what the closing paragraph does to the table --------------------------

def algorithm_vs_physics():
    """Which EXCEEDS rows price a method nature does not use?

    The delivered text answers this itself in its last paragraph -- folding is
    funnelled, not searched; nature never pays the exponential -- and does not
    apply the answer back to the table. Applied, it retracts two of the three
    EXCEEDS rows and leaves the third standing for a reason the text does not
    give.
    """
    return [
        {"row": "ONE protein, exhaustive fold search",
         "prices": "ALGORITHM",
         "retracted_by_the_text": True,
         "why": "the row's own name is 'exhaustive fold search', and the "
                "closing paragraph states that folding is funnelled rather "
                "than searched. So the row prices a brute-force method "
                "nobody claims the physics uses. It exceeds and it does not "
                "bind."},
        {"row": "nested phase transitions, 4 classes",
         "prices": "EVENT COUNT",
         "retracted_by_the_text": False,
         "why": "not an algorithm -- a count of transitions that occurred. "
                "It is not retracted by the funnelling argument, and it is "
                "the row that drifted; see drift_check() and SHB_028, where "
                "the previous drop's version needed a double-count."},
        {"row": "quantum many-body, N=1000",
         "prices": "SUBSTRATE",
         "retracted_by_the_text": False,
         "why": "d^N is the genuine dimension of the state space, not a "
                "search strategy. A CLASSICAL simulator must carry it; a "
                "quantum substrate does not, because the system is its own "
                "simulator. So the row bounds classical simulation of "
                "quantum systems -- Feynman 1982 -- and not simulation as "
                "such. That makes it the strongest row in the table, for a "
                "reason the table does not give."},
    ]


def surviving_bound():
    a = algorithm_vs_physics()
    return {"exceeds_rows": len(a),
            "retracted_by_the_texts_own_resolution":
                sum(1 for r in a if r["retracted_by_the_text"]),
            "still_binding": [r["row"] for r in a
                              if not r["retracted_by_the_text"]],
            "the_one_that_bounds_the_hypothesis":
                [r["row"] for r in a if r["prices"] == "SUBSTRATE"]}


# --- report ----------------------------------------------------------------

def _wrap(text, indent, width=72):
    words, lines, cur = text.split(), [], indent
    for w in words:
        if len(cur) + len(w) + 1 > width and cur.strip():
            lines.append(cur.rstrip())
            cur = indent + w + " "
        else:
            cur += w + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def report():
    L = []
    A = L.append
    A("SCALING CLASSES -- the delivered table, checked")
    A("=" * 72)
    A("")
    A("  1. REPRODUCING THE ROWS")
    A("")
    for d in reproduce():
        A("     %s" % d["row"])
        A("       stated 10^%-6.0f checked %-8s %s"
          % (d["stated_log10"],
             "--" if d["computed_log10"] is None
             else "10^%.1f" % d["computed_log10"],
             d["state"]))
    A("")
    rep = reproduce()
    ok = [d for d in rep if d["state"] == "REPRODUCES"]
    need = [d for d in rep if d["state"] == "NEEDS_UNSTATED_CONSTRUCTION"]
    L.extend(_wrap(
        "%d of %d rows reproduce exactly from the terms printed in them -- "
        "2^100, 2^300, 2^1000 and 3^300 -- with residuals under a third of "
        "a decade, which is the table rounding to whole decades. %d need a "
        "construction the table does not give: no Reynolds number, grid "
        "count or timestep is printed for the two fluid rows."
        % (len(ok), len(rep), len(need)), "     "))
    A("")
    L.extend(_wrap(
        "The N-body row is marked CONSTRUCTION_FITTED and not counted among "
        "the reproductions. Direct O(N^2) on 10^30 bodies is 10^60, and "
        "10^67 follows only if there are about 10^7 timesteps -- a number "
        "chosen HERE to match the stated value, not printed in the table. A "
        "construction reverse-engineered from the answer is not a check, and "
        "counting it as one would have inflated the reproduction count from "
        "four to five.", "     "))
    A("")
    L.extend(_wrap(
        "Worth naming on the same row: a Barnes-Hut tree makes the same "
        "physics 10^32, thirty-five decades cheaper. The VERDICT is robust "
        "and the NUMBER is a property of the method -- SHB_021 arriving "
        "inside a single row.", "     "))
    A("")
    ec = excess_column_check()
    A("     EXCEEDS columns, checked as total minus ceiling:")
    for e in ec:
        A("       %-38s %-6.0f %s" % (e["row"][:38], e["stated_excess"],
                                      "consistent" if e["consistent"]
                                      else "INCONSISTENT"))
    A("")
    A("-" * 72)
    A("")
    dc = drift_check()
    A("  2. ONE ROW HAS DRIFTED TEN DECADES, UNREMARKED")
    A("")
    A("     nested phase transitions, this table    10^%.0f"
      % dc["this_table"])
    A("     the same object, previous drop          10^%.1f"
      % dc["previous_drop"])
    A("     drift                                   %.1f decades"
      % dc["drift_decades"])
    for k, v in sorted(dc["coherent_models_here"].items()):
        A("     %-38s 10^%.1f" % ("this folder: " + k, v))
    A("     matches any coherent model here         %s"
      % dc["matches_any_coherent_model"])
    A("")
    L.extend(_wrap(dc["why_invisible"], "     "))
    A("")
    A("-" * 72)
    A("")
    A("  3. THE STRUCTURAL CLAIM -- right in direction, one qualification")
    A("")
    pc = polynomial_counterexample()
    A("     'everything polynomial FITS' is not general:")
    for p in pc:
        A("       N = 10^%.0f, N^%d = 10^%.0f   %s"
          % (p["N_log10"], p["k"], p["cost_log10"],
             "fits" if p["cost_log10"] < CEILING else "EXCEEDS"))
    A("")
    L.extend(_wrap(
        "Same N, same polynomial class, opposite verdicts. Pairwise "
        "interactions among Earth's atoms fit; triple-wise do not. So the "
        "cut is scaling class CROSSED WITH N, and the claim holds for the "
        "N's in the table rather than in general.", "     "))
    A("")
    A("     The exact form is the CROSSOVER, and it is sharper:")
    A("")
    A("       %-34s %s" % ("form", "crosses 10^120 at"))
    for c in crossover_table():
        A("       %-34s %s %s"
          % (c["form"],
             ("%.0f" % c["crosses_at"]) if c["crosses_at"] < 1e6
             else B.sci(c["crosses_at"], 2),
             c["units"]))
    A("")
    L.extend(_wrap(
        "Stated that way the delivered claim is exact and stronger. A "
        "quantum system of 399 two-state components exhausts the universe's "
        "entire compute budget. A 252-residue protein does. Pairwise "
        "interactions need 10^60 bodies before they do -- twenty decades "
        "above Earth's atom count -- and that gap between 399 and 10^60 is "
        "the structural result, quantified.", "     "))
    A("")
    A("-" * 72)
    A("")
    A("  4. THE CLOSING PARAGRAPH RETRACTS ONE OF ITS OWN EXCEEDS ROWS")
    A("")
    L.extend(_wrap(
        "The text ends: folding is funnelled, not searched; nature never "
        "pays the exponential; it is in a configuration where the "
        "exponential does not arise. That is correct, and it is not applied "
        "back to the table. Applied:", "     "))
    A("")
    for r in algorithm_vs_physics():
        A("     %s" % r["row"])
        A("       prices: %-12s retracted by the text: %s"
          % (r["prices"], "YES" if r["retracted_by_the_text"] else "no"))
        L.extend(_wrap(r["why"], "       "))
        A("")
    sb = surviving_bound()
    A("     of %d EXCEEDS rows, %d is retracted by the text's own"
      % (sb["exceeds_rows"], sb["retracted_by_the_texts_own_resolution"]))
    A("     resolution. Still binding:")
    for r in sb["still_binding"]:
        A("       %s" % r)
    A("")
    L.extend(_wrap(
        "THE ASYMMETRY IS THE RESULT. The protein row prices an ALGORITHM "
        "and the funnelling argument removes it. The quantum row prices a "
        "SUBSTRATE and the same argument does not touch it: d^N is the real "
        "dimension of the state space, a classical simulator must carry it, "
        "and a quantum one need not because the system is its own simulator. "
        "So the quantum row is the only one in the table that bounds the "
        "hypothesis rather than bounding our method -- and it bounds it in a "
        "specific direction, against a CLASSICAL substrate. That is "
        "Feynman's 1982 argument, and it is the strongest thing in the drop, "
        "for a reason the drop does not state.", "     "))
    A("")
    A("-" * 72)
    A("")
    A("  WHAT SURVIVES")
    A("")
    L.extend(_wrap(
        "Every row priced by what the physical system actually does is "
        "polynomial or a plain event count, and fits. The exponentials enter "
        "through SEARCH, which nature does not perform, or through CLASSICAL "
        "REPRESENTATION of quantum state, which nature does not perform "
        "either. Read that way the table's headline inverts: it is not that "
        "three loads exceed the budget, it is that the two ways of exceeding "
        "it are both artifacts of how WE would compute the answer -- with "
        "one exception, which is a claim about the simulator's substrate and "
        "not about its budget.", "     "))
    A("")
    L.extend(_wrap(
        "That connects to SHB_030 from the other side. A content count binds "
        "any architecture that must produce its own observation record. An "
        "EXPONENTIAL content count does not, unless the exponential is in "
        "the physics rather than in the method -- and the delivered text's "
        "own last line says it is not.", "     "))
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

    rep = reproduce()
    ok = [d for d in rep if d["state"] == "REPRODUCES"]
    ck("four rows reproduce exactly from their own printed terms",
       len(ok) == 4)
    ck("every reproducing row is within a third of a decade -- the "
       "residuals are the table rounding to whole decades",
       all(abs(d["error_decades"]) < 0.35 for d in ok))
    ck("the N-body row is marked CONSTRUCTION_FITTED, not REPRODUCES, "
       "because its free parameter was chosen to match the stated value",
       [d for d in rep if d["row"].startswith("N-body")][0]["state"]
       == "CONSTRUCTION_FITTED")
    ck("no row DISAGREES -- the ones that do not reproduce are missing a "
       "construction, which is a different finding",
       not any(d["state"] == "DISAGREES" for d in rep))
    ck("three rows need an unstated construction",
       sum(1 for d in rep
           if d["state"] == "NEEDS_UNSTATED_CONSTRUCTION") == 3)

    ck("every EXCEEDS column is total minus ceiling",
       all(e["consistent"] for e in excess_column_check()))
    ck("there are three EXCEEDS rows", len(excess_column_check()) == 3)

    dc = drift_check()
    ck("the nested-transitions row has moved ten decades since the previous "
       "drop", abs(dc["drift_decades"] - 10.5) < 1.0)
    ck("and matches no coherent cost model in this folder",
       dc["matches_any_coherent_model"] is False)

    ck("2^N crosses the ceiling at about 399 components",
       398.0 < crossover(2) < 400.0)
    ck("3^n crosses at about 252 residues", 251.0 < crossover(3) < 253.0)
    ck("the delivered 300-residue figure is past the crossover",
       300 > crossover(3))
    ck("the delivered N=300 quantum figure is NOT past it, which is why that "
       "row reads 'fits'", 300 < crossover(2))

    pc = polynomial_counterexample()
    ck("polynomial does not fit automatically -- same N and class, opposite "
       "verdicts",
       any(p["cost_log10"] < CEILING for p in pc)
       and any(p["cost_log10"] >= CEILING for p in pc))

    a = algorithm_vs_physics()
    ck("the three EXCEEDS rows price three different things",
       len({r["prices"] for r in a}) == 3)
    ck("exactly one is retracted by the text's own closing argument",
       sum(1 for r in a if r["retracted_by_the_text"]) == 1)
    ck("the retracted one is the fold search",
       [r["row"] for r in a if r["retracted_by_the_text"]][0].startswith(
           "ONE protein"))
    sb = surviving_bound()
    ck("exactly one row prices a SUBSTRATE, and it is the quantum one",
       len(sb["the_one_that_bounds_the_hypothesis"]) == 1
       and "quantum" in sb["the_one_that_bounds_the_hypothesis"][0])
    ck("two rows still bind after the retraction, so the finding is not "
       "that the whole table dissolves", len(sb["still_binding"]) == 2)

    ck("report renders", "THE ASYMMETRY IS THE RESULT" in report())
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
