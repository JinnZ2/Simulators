#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
m3_energy_ledger.py - compensation gradient vs metabolic gradient.

    python3 m3_energy_ledger.py [--selftest]

Per position: kcal expended (physical + cognitive) and kcal the wage
replaces. Output: the sign and magnitude of the correlation between wage and
kcal, and whether the compensation gradient runs with or against energy draw.

REFERENCE POINTS ARE PARAMETERS, NOT ASSUMPTIONS -- carried from the spec and
not verified here:
  desk day                   ~2000 kcal total expenditure
  heavy physical day         ~4000-5000 kcal
  goal-directed cognition    ~5% above resting brain metabolism
  brain                      ~20% of resting draw
  => desk cognitive increment ~1% of daily total

KNOWN GAP, left visible per the spec: there is NO TERM here for multi-channel
sensory integration load under vibration and noise. Occupational neuroimaging
exists and is field-deployable, and the sampled occupations are sport and
prestige -- pianists, racing drivers, pilots, air traffic controllers. No
farm, fabrication, animal handling or freight data was located. The gap is a
data gap in the same shape as the thing this module set is about, and it is
not filled with an estimate.

stdlib only, CC0.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import _shared as SH                                            # noqa: E402
import m1_tenure_budget as M1                                   # noqa: E402

RESTING_KCAL = 1800.0
BRAIN_SHARE_OF_RESTING = 0.20
COGNITION_INCREMENT = 0.05          # above resting brain metabolism
KCAL_PER_CURRENCY_UNIT = 2.0        # food purchasable per wage unit

# Physical expenditure above resting, per position. Stipulated against the
# spec's reference points.
PHYSICAL_ABOVE_RESTING = {
    "desk_professional": 200.0,
    "freight_driver": 700.0,
    "fabrication": 2100.0,
    "animal_handling": 1900.0,
    "farm_labor": 2800.0,
}

# The unfilled term. Present as a declared field so it renders, per the
# folder rule about visible blanks.
SENSORY_INTEGRATION_LOAD = dict(
    (p, None) for p in PHYSICAL_ABOVE_RESTING)


def cognitive_increment():
    """~5% above resting brain metabolism, brain ~20% of resting draw."""
    return RESTING_KCAL * BRAIN_SHARE_OF_RESTING * COGNITION_INCREMENT


def ledger(position_name, hours_worked):
    phys = PHYSICAL_ABOVE_RESTING[position_name]
    cog = cognitive_increment()
    total = RESTING_KCAL + phys + cog
    wage = [p for p in M1.POSITIONS
            if p["position"] == position_name][0]["wage"]
    replaced = wage * hours_worked * KCAL_PER_CURRENCY_UNIT
    return {"position": position_name, "wage": wage,
            "kcal_resting": RESTING_KCAL, "kcal_physical": phys,
            "kcal_cognitive": cog, "kcal_expended": total,
            "cognitive_share_of_total": cog / total,
            "kcal_replaced_by_wage": replaced,
            "replacement_ratio": replaced / total,
            "sensory_integration_load": SENSORY_INTEGRATION_LOAD[
                position_name]}


def table(hours_worked=8.0):
    return [ledger(p["position"], hours_worked) for p in M1.POSITIONS]


def _corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def gradient(hours_worked=8.0):
    t = table(hours_worked)
    r = _corr([x["wage"] for x in t], [x["kcal_expended"] for x in t])
    return {"correlation_wage_vs_kcal": r,
            "direction": "against energy draw" if r < 0
            else "with energy draw" if r > 0 else "flat",
            "cognitive_share_range":
                (min(x["cognitive_share_of_total"] for x in t),
                 max(x["cognitive_share_of_total"] for x in t)),
            "replacement_ratio_range":
                (min(x["replacement_ratio"] for x in t),
                 max(x["replacement_ratio"] for x in t))}


def robustness(extra_positions=(("surgeon", 90.0, 900.0),
                                ("professional_athlete", 120.0, 4500.0))):
    """How many high-wage high-kcal positions flip the sign?

    The position list is hand-picked, so the sign is a property of the list
    until it is not. This measures how far from a property of the list it is.
    """
    base = table()
    rows = [{"added": "none", "n": len(base),
             "correlation": gradient()["correlation_wage_vs_kcal"]}]
    xs = [x["wage"] for x in base]
    ys = [x["kcal_expended"] for x in base]
    for name, wage, phys in extra_positions:
        xs = xs + [wage]
        ys = ys + [RESTING_KCAL + phys + cognitive_increment()]
        rows.append({"added": name, "n": len(xs), "correlation":
                     _corr(xs, ys)})
    signs = set(r["correlation"] < 0 for r in rows)
    return {"rows": rows, "sign_flips": len(signs) > 1,
            "why": "one high-wage high-expenditure position is enough to "
                   "move the correlation materially, and the second flips "
                   "the sign. The population weight of such positions is not "
                   "represented here at all, which is what would decide it"}


def known_gap():
    return {"missing_term": "multi-channel sensory integration load under "
                            "vibration and noise",
            "positions_with_a_value": sum(
                1 for v in SENSORY_INTEGRATION_LOAD.values() if v is not None),
            "positions_total": len(SENSORY_INTEGRATION_LOAD),
            "instrument_exists": True,
            "sampled_occupations": ["pianists", "racing drivers", "pilots",
                                    "air traffic controllers"],
            "not_located": ["farm", "fabrication", "animal handling",
                            "freight"],
            "note": "the instrument is field-deployable and the sampled "
                    "occupations are sport and prestige. The gap has the "
                    "same shape as the thing this module set is about, and "
                    "it is left as None rather than estimated -- an "
                    "estimated value would enter the correlation and could "
                    "not be told apart from a measured one"}


def confidence():
    return {"cognitive_increment": "derived from the spec's reference "
                                   "points, which are carried and not "
                                   "verified here",
            "physical_values": "stipulated against the spec's 2000 / "
                               "4000-5000 kcal anchors",
            "correlation_sign": "a property of the position list, and the "
                                "robustness sweep says how much of one",
            "sensory_integration_term": "ABSENT. see known_gap()",
            "resolved": False}


def breaks():
    return [
        "THE SENSORY INTEGRATION TERM IS ABSENT for every position, and the "
        "positions it would most affect -- freight, fabrication, animal "
        "handling -- are exactly the ones no located study samples. It is "
        "left None rather than estimated, because an estimate would enter "
        "the correlation and could not be told apart from a measurement",
        "THE CORRELATION SIGN IS A PROPERTY OF THE POSITION LIST. Adding two "
        "high-wage high-expenditure positions flips it. What would settle it "
        "is the population weight of such positions, which is not "
        "represented here",
        "kcal_replaced_by_wage uses a flat conversion, so the replacement "
        "ratio is a restatement of the wage and carries no information the "
        "wage column does not",
        "physical expenditure is position-fixed. Within-position variation "
        "is larger than some between-position gaps in any real data",
        "the cognitive increment comes out near 1 percent of daily total, "
        "which makes it almost irrelevant to the correlation. If the spec's "
        "reference points are wrong in that direction the whole readout "
        "changes, and nothing here checks them",
    ]


def report():
    L = ["M3 -- ENERGY LEDGER", "=" * 72, ""]
    L.append("  cognitive increment: %.1f kcal/day (%.0f x %.2f x %.2f)"
             % (cognitive_increment(), RESTING_KCAL, BRAIN_SHARE_OF_RESTING,
                COGNITION_INCREMENT))
    L.append("")
    L.append("  %-20s %-8s %-11s %-11s %-11s %s"
             % ("position", "wage", "kcal exp", "cog share", "replaced",
                "sensory load"))
    for r in table():
        L.append("  %-20s %-8.1f %-11.0f %-11.4f %-11.0f %s"
                 % (r["position"], r["wage"], r["kcal_expended"],
                    r["cognitive_share_of_total"],
                    r["kcal_replaced_by_wage"],
                    "[BLANK]" if r["sensory_integration_load"] is None
                    else r["sensory_integration_load"]))
    L.append("")
    g = gradient()
    L.append("  correlation, wage vs kcal expended: %+.3f"
             % g["correlation_wage_vs_kcal"])
    L.append("  the compensation gradient runs %s" % g["direction"])
    L.append("  cognitive share of daily total: %.2f%% to %.2f%%"
             % (100 * g["cognitive_share_range"][0],
                100 * g["cognitive_share_range"][1]))
    L.append("")
    L.extend(SH.wrap("The cognitive increment lands near one percent of the "
                     "daily total, which is what the spec's reference points "
                     "imply and is small enough to be irrelevant to the "
                     "correlation. So the gradient here is set almost "
                     "entirely by physical expenditure.", "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    rb = robustness()
    L.append("  ROBUSTNESS -- the sign is a property of the position list")
    L.append("")
    L.append("  %-26s %-6s %s" % ("added", "n", "correlation"))
    for r in rb["rows"]:
        L.append("  %-26s %-6d %+.3f" % (r["added"], r["n"],
                                         r["correlation"]))
    L.append("")
    L.append("  sign flips: %s" % rb["sign_flips"])
    L.extend(SH.wrap(rb["why"], "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    kg = known_gap()
    L.append("  KNOWN GAP, LEFT VISIBLE")
    L.append("")
    L.append("    missing term        %s" % kg["missing_term"])
    L.append("    positions with a value  %d of %d"
             % (kg["positions_with_a_value"], kg["positions_total"]))
    L.append("    instrument exists   %s" % kg["instrument_exists"])
    L.append("    sampled             %s" % ", ".join(
        kg["sampled_occupations"]))
    L.append("    not located         %s" % ", ".join(kg["not_located"]))
    L.append("")
    L.extend(SH.wrap(kg["note"], "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("the cognitive increment lands near 1 percent of a desk day's total",
       0.005 < cognitive_increment() / ledger("desk_professional", 8)
       ["kcal_expended"] < 0.02)
    ck("a heavy physical day lands in the spec's 4000-5000 band",
       4000 <= ledger("farm_labor", 8)["kcal_expended"] <= 5000)
    ck("a desk day lands near the spec's 2000",
       1900 <= ledger("desk_professional", 8)["kcal_expended"] <= 2100)

    g = gradient()
    ck("the compensation gradient runs against energy draw on this list",
       g["correlation_wage_vs_kcal"] < -0.5)
    ck("and the direction is reported as a graded term, not a verdict",
       g["direction"] in ("against energy draw", "with energy draw", "flat"))

    rb = robustness()
    ck("the sign flips when high-wage high-expenditure positions are added, "
       "so it is a property of the list",
       rb["sign_flips"] is True)
    ck("and what would settle it is named",
       "population weight" in rb["why"])

    kg = known_gap()
    ck("the sensory integration term is absent for every position",
       kg["positions_with_a_value"] == 0)
    ck("it is None rather than zero, so absent and measured-as-zero do not "
       "share a value",
       all(v is None for v in SENSORY_INTEGRATION_LOAD.values()))
    ck("it renders as [BLANK] in the report", "[BLANK]" in report())
    ck("the sampled-occupations asymmetry is recorded",
       len(kg["sampled_occupations"]) > 0 and len(kg["not_located"]) > 0)

    ck("the absent term leads the breaks list", "ABSENT" in breaks()[0])
    ck("confidence records the term as absent",
       "ABSENT" in confidence()["sensory_integration_term"])
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "KNOWN GAP" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "M3"))
