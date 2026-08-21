#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
earth_transitions.py - the delivered EARTH_TRANSITIONS.md, checked.

    python3 earth_transitions.py
    python3 earth_transitions.py --selftest

A count of Earth's phase transitions against Lloyd's ceiling, delivered from
outside this folder, and carrying its own correction: the eight "major
transitions" are LABELS, each a coarse-grained envelope over nested
transitions at every scale inside it.

THE STRUCTURAL POINT IS RIGHT AND SHARP, and nothing below disputes it. What
is checked is the arithmetic, because the arithmetic is what produces the
headline.

Three things came back:

  1. THE CEILING CHECKS OUT from inside this folder, by an independent route.
     budget.py's Margolus-Levitin machinery, pointed at the universe's
     mass-energy over its age, gives 10^122.9 ops against Lloyd's 10^120.
  2. THE FIRST-PASS NUMBER IS REPRODUCIBLE, and the eight labels are not what
     produce it. atoms x Planck ticks = 10^110.5. The factor of 8 adds 0.9
     decades to a 110-decade number.
  3. THE HEADLINE NEEDS A DOUBLE-COUNT. 1e52 is a MULTIPLIER, not a total
     (110 + 52 - 120 = 42, exactly). But multiplying a per-tick STEPPING cost
     by a TRANSITION count prices the same physics twice. Under either
     coherent cost model separately, Planck-resolved Earth FITS.

Imports budget.py for constants; modifies nothing. stdlib only, Python 3.9.
"""

import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget as B                                              # noqa: E402

# --- Earth, declared -------------------------------------------------------

M_EARTH = 5.972e24              # kg
R_EARTH = 6.371e6               # m
AGE_EARTH = 4.54e9 * 3.156e7    # s
M_ATOM_MEAN = 5.0e-26           # kg; ~30 g/mol, Earth's Fe/O/Si/Mg mix

N_LABELS = 8                    # the delivered "eight major transitions"
NESTING_DECADES = 52.0          # the delivered nested multiplier, four classes
LLOYD_CEILING_LOG10 = 120.0     # Lloyd, Computational capacity of the universe

V_EARTH = (4.0 / 3.0) * math.pi * R_EARTH ** 3


def earth_atoms():
    return M_EARTH / M_ATOM_MEAN


def planck_ticks():
    return AGE_EARTH / B.T_PLANCK


def lloyd_check():
    """Reproduce the ceiling from this folder's own machinery.

    Independent route: Margolus-Levitin rate (2E/pi hbar) on the universe's
    mass-energy, integrated over its age. Agreement to a few decades against
    a published figure derived the same way is a check on the folder, not on
    Lloyd.
    """
    e = B.RHO_CRIT * B.C ** 2 * (4.0 / 3.0) * math.pi * B.R_OBS ** 3
    rate = 2.0 * e / (math.pi * B.HBAR)
    ops = rate * B.AGE
    return {"universe_energy_J": e, "ml_rate_ops_per_s": rate,
            "ops_since_t0": ops, "log10": math.log10(ops),
            "lloyd_log10": LLOYD_CEILING_LOG10,
            "gap_decades": math.log10(ops) - LLOYD_CEILING_LOG10,
            "why_not_exact": "budget.py uses all components at rho_crit; "
                             "Lloyd uses matter-only. SHB_006(a) already "
                             "names that convention as a choice worth ~1.3 "
                             "decades, and the rest is accounting detail. "
                             "Order-of-magnitude agreement by a second route "
                             "is the check."}


# --- what construction produces 10^110? ------------------------------------

def constructions():
    a, t = earth_atoms(), planck_ticks()
    return [
        ("labels x atoms", N_LABELS * a,
         "a pure EVENT count: one op per atom per named transition"),
        ("atoms x Planck ticks", a * t,
         "a pure STEPPING count: one op per atom per Planck time, for all "
         "of Earth history. Transitions do not appear in it"),
        ("labels x atoms x ticks", N_LABELS * a * t,
         "both, multiplied"),
    ]


def which_reproduces(target_log10=110.0, tol=1.0):
    return [(name, v, note) for name, v, note in constructions()
            if abs(math.log10(v) - target_log10) <= tol]


def label_contribution():
    """How many decades do the eight labels contribute?"""
    return math.log10(N_LABELS)


# --- the headline, and what reading makes it true --------------------------

def headline_readings():
    """1e52 as a TOTAL and as a MULTIPLIER give opposite verdicts."""
    stepping = math.log10(earth_atoms() * planck_ticks())
    return [
        {"reading": "1e52 is a MULTIPLIER on the stepping count",
         "total_log10": stepping + NESTING_DECADES,
         "verdict_decades": stepping + NESTING_DECADES - LLOYD_CEILING_LOG10,
         "reproduces_delivered_42": abs(
             (stepping + NESTING_DECADES - LLOYD_CEILING_LOG10) - 42.0) < 1.0},
        {"reading": "1e52 is the TOTAL nested transition count",
         "total_log10": NESTING_DECADES,
         "verdict_decades": NESTING_DECADES - LLOYD_CEILING_LOG10,
         "reproduces_delivered_42": False},
    ]


def cost_models():
    """The three internally coherent models, and the mixed one.

    A STEPPING model pays per degree of freedom per timestep and already
    contains every transition that occurs -- nesting adds nothing to its cost.
    An EVENT-DRIVEN model pays per transition and does not step. Multiplying
    them prices the same physics twice.
    """
    a, t = earth_atoms(), planck_ticks()
    nest = 10.0 ** NESTING_DECADES
    out = [
        {"model": "event-driven, labels only", "coherent": True,
         "ops": N_LABELS * a,
         "why": "one op per atom per named transition"},
        {"model": "event-driven, nested", "coherent": True,
         "ops": N_LABELS * a * nest,
         "why": "one op per atom per transition, with the labels unfolded "
                "into their nested transitions -- the delivered correction, "
                "applied to the event count it belongs to"},
        {"model": "uniform Planck stepping", "coherent": True,
         "ops": a * t,
         "why": "one op per atom per Planck time. Every transition that "
                "occurs is already inside this; nesting is free"},
        {"model": "stepping x nesting (as delivered)", "coherent": False,
         "ops": a * t * nest,
         "why": "DOUBLE COUNT. The stepping cost already computes every "
                "transition; multiplying by a transition count charges for "
                "the same physics twice"},
    ]
    for m in out:
        m["log10"] = math.log10(m["ops"])
        m["over_by_decades"] = m["log10"] - LLOYD_CEILING_LOG10
        m["fits"] = m["over_by_decades"] < 0
    return out


def nesting_headroom():
    """How much more nesting would break the coherent event-driven model?

    This is the constructive version of the delivered claim: it does not need
    the double-count, and it names a reachable falsifier -- enumerate more
    transition classes.
    """
    base = math.log10(N_LABELS * earth_atoms())
    return {"event_base_log10": base,
            "nesting_used_decades": NESTING_DECADES,
            "nesting_at_which_it_breaks":
                LLOYD_CEILING_LOG10 - base,
            "headroom_decades":
                LLOYD_CEILING_LOG10 - base - NESTING_DECADES,
            "delivered_says": "four classes only, not exhaustive"}


def resolution_needed_to_fit(include_nesting=False):
    """What timestep fits inside the ceiling, stepping every Earth atom?

    SHB_004 says the resolution knob does more work than any physics. Turning
    it here was expected to show Earth needing a coarse timestep. It does not,
    under pure stepping: the knob has headroom BELOW Planck time. Recorded as
    a check that ran against expectation rather than quietly reframed -- and
    it is the delivered first pass's own result ("uses 10^-10 of the budget.
    it FITS") arriving from this side.

    With the nesting applied as a multiplier -- the delivered mixed model --
    the picture reverses and the required timestep lands in the fraction of a
    second.
    """
    a = earth_atoms()
    budget = 10.0 ** LLOYD_CEILING_LOG10
    if include_nesting:
        budget /= 10.0 ** NESTING_DECADES
    ticks_allowed = budget / a
    dt = AGE_EARTH / ticks_allowed
    return {"ticks_allowed": ticks_allowed,
            "timestep_s": dt,
            "planck_timestep_s": B.T_PLANCK,
            "decades_of_knob": math.log10(dt / B.T_PLANCK),
            "finer_than_planck": dt < B.T_PLANCK,
            "with_nesting": include_nesting}


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
    A("EARTH TRANSITIONS -- the delivered count, checked")
    A("=" * 72)
    A("")
    L.extend(_wrap(
        "The structural point is right and nothing below disputes it: the "
        "eight 'major transitions' are labels, each a coarse-grained "
        "envelope, and pricing the labels is not pricing the transitions. "
        "What is checked is the arithmetic, because the arithmetic is what "
        "produces the headline.", "  "))
    A("")
    A("-" * 72)
    A("")
    lc = lloyd_check()
    A("  1. THE CEILING, CHECKED FROM INSIDE THIS FOLDER")
    A("")
    A("     universe mass-energy      %s J" % B.sci(lc["universe_energy_J"]))
    A("     Margolus-Levitin rate     %s ops/s"
      % B.sci(lc["ml_rate_ops_per_s"]))
    A("     ops since t=0             %s  (10^%.1f)"
      % (B.sci(lc["ops_since_t0"]), lc["log10"]))
    A("     Lloyd, as delivered       10^%.0f" % lc["lloyd_log10"])
    A("     agreement                 within %.1f decades"
      % abs(lc["gap_decades"]))
    L.extend(_wrap(lc["why_not_exact"], "     "))
    A("")
    A("     The ceiling holds. It is the one number in the delivered result")
    A("     this folder can confirm by a route it did not take.")
    A("")
    A("-" * 72)
    A("")
    A("  2. WHAT PRODUCES 10^110 -- and it is not the eight")
    A("")
    A("     Earth atoms                %s" % B.sci(earth_atoms()))
    A("     Planck ticks in 4.54 Gyr   %s" % B.sci(planck_ticks()))
    A("")
    A("     %-26s %-12s %s" % ("construction", "ops", "log10"))
    for name, v, _ in constructions():
        A("     %-26s %-12s %.1f" % (name, B.sci(v, 2), math.log10(v)))
    A("")
    m = which_reproduces()
    A("     reproduces ~10^110 to within a decade: %s"
      % ", ".join(n for n, _, _ in m))
    A("")
    L.extend(_wrap(
        "The eight labels contribute %.1f decades to a 110-decade number. "
        "The count is atoms (%.1f decades) times PLANCK TICKS (%.1f "
        "decades). So the first pass was never really a transition count -- "
        "it was a stepping count, and the resolution assumption supplied "
        "more than half of it."
        % (label_contribution(), math.log10(earth_atoms()),
           math.log10(planck_ticks())), "     "))
    A("")
    L.extend(_wrap(
        "That is SHB_004 on a new substrate: the resolution assumption does "
        "more work than anything else in the argument. It also sharpens the "
        "delivered self-correction rather than undercutting it -- the "
        "correction is worth 52 decades and the thing corrected was worth "
        "0.9.", "     "))
    A("")
    A("-" * 72)
    A("")
    A("  3. THE HEADLINE NEEDS 1e52 TO BE A MULTIPLIER")
    A("")
    for h in headline_readings():
        A("     %s" % h["reading"])
        A("       total 10^%.1f, %s ceiling by %.0f decades"
          % (h["total_log10"],
             "over" if h["verdict_decades"] > 0 else "under",
             abs(h["verdict_decades"])))
        if h["reproduces_delivered_42"]:
            A("       <- reproduces the delivered 1e42")
    A("")
    L.extend(_wrap(
        "110 + 52 - 120 = 42, exactly. So the delivered arithmetic is "
        "consistent under the multiplier reading and 68 decades out under "
        "the other. The text presents 1e52 next to 'nested transitions, "
        "FOUR classes only', which reads as a total. One label is wrong and "
        "the arithmetic is right.", "     "))
    A("")
    A("-" * 72)
    A("")
    A("  4. BUT MULTIPLYING PRICES THE SAME PHYSICS TWICE")
    A("")
    L.extend(_wrap(
        "A STEPPING model pays per degree of freedom per timestep, and every "
        "transition that occurs is already inside that cost -- nesting adds "
        "nothing. An EVENT-DRIVEN model pays per transition and does not "
        "step. They are alternative architectures, and the product of the "
        "two is not a cost.", "     "))
    A("")
    A("     %-36s %-7s %-5s %s"
      % ("cost model", "log10", "cohr", "verdict (decades)"))
    for c in cost_models():
        A("     %-36s %-7.1f %-5s %s"
          % (c["model"], c["log10"], "yes" if c["coherent"] else "NO",
             "fits, %.0f spare" % -c["over_by_decades"]
             if c["fits"] else "OVER by %.0f" % c["over_by_decades"]))
    A("")
    A("     Under every internally coherent model, Planck-resolved Earth")
    A("     FITS. The overshoot appears only in the mixed one.")
    A("")
    A("-" * 72)
    A("")
    nh = nesting_headroom()
    A("  5. THE CONSTRUCTIVE VERSION -- what would make it true")
    A("")
    A("     event-driven base (labels x atoms)   10^%.1f"
      % nh["event_base_log10"])
    A("     nesting used, four classes           %.0f decades"
      % nh["nesting_used_decades"])
    A("     nesting at which the model breaks    %.0f decades"
      % nh["nesting_at_which_it_breaks"])
    A("     headroom remaining                   %.0f decades"
      % nh["headroom_decades"])
    A("")
    L.extend(_wrap(
        "The delivered text says four classes only, not exhaustive. So the "
        "claim becomes true, without any double-count, if the full nesting "
        "is %.0f decades rather than %.0f. That is a reachable falsifier and "
        "a better form of the delivered result: enumerate more transition "
        "classes and the event-driven model breaks on its own."
        % (nh["nesting_at_which_it_breaks"], nh["nesting_used_decades"]),
        "     "))
    A("")
    rn = resolution_needed_to_fit()
    rw = resolution_needed_to_fit(include_nesting=True)
    A("  6. THE KNOB, TURNED UNTIL IT FITS")
    A("     -- and this one ran against expectation")
    A("")
    A("     stepping every atom, no nesting, budget 10^120:")
    A("       timestep affordable      %s s" % B.sci(rn["timestep_s"]))
    A("       Planck time              %s s" % B.sci(rn["planck_timestep_s"]))
    A("       knob                     %.1f decades FINER than Planck"
      % abs(rn["decades_of_knob"]))
    A("")
    L.extend(_wrap(
        "Stepping every Earth atom for 4.54 Gyr inside the universe's whole "
        "ops budget affords a timestep %.1f decades BELOW Planck time. The "
        "knob has headroom in the direction nobody asks for. That is the "
        "delivered first pass's own result -- 'uses 10^-10 of the budget. it "
        "FITS' -- arriving from this side, and it is not what turning the "
        "knob was expected to show."
        % abs(rn["decades_of_knob"]), "     "))
    A("")
    A("     with the delivered nesting applied as a multiplier:")
    A("       timestep affordable      %s s" % B.sci(rw["timestep_s"]))
    A("       knob                     %.0f decades COARSER than Planck"
      % rw["decades_of_knob"])
    A("")
    L.extend(_wrap(
        "Under the mixed model the picture reverses and the affordable "
        "timestep lands at about %.1f of a second -- not Planck time, not "
        "the 10^-21 s anything has ever resolved, but human-scale. So the "
        "delivered claim is equivalently a statement about the CLOCK: it "
        "says a Planck-stepped Earth carrying its full nested transition "
        "count would need a sub-second tick to fit, which is a "
        "contradiction in terms. Stated that way the double-count is "
        "visible without any arithmetic."
        % rw["timestep_s"], "     "))
    A("")
    A("-" * 72)
    A("")
    A("  WHAT IT REACHES, AND WHAT IT DOES NOT")
    A("")
    L.extend(_wrap(
        "Reaches: this is a count over the world's own CONTENTS rather than "
        "over cells, and that is a different kind of bound. Under SHB_011, "
        "every transition that leaves a record must be computed by any "
        "architecture that can produce its own observation record -- mineral "
        "grains, ice cores and fossils are records -- so a content count is "
        "architecture-independent in a way the cell counts of budget.py are "
        "not. That is the strongest thing in the delivered result and it is "
        "not what the delivered result claims.", "     "))
    A("")
    L.extend(_wrap(
        "Does not reach: the hypothesis. Both operands are computed in our "
        "physics about a simulator embedded in our physics, so SHB_003's "
        "frame refusal applies unchanged and this measures self-hosting. And "
        "'four classes' is a floor enumerated by us -- SHB_021 on a second "
        "substrate, the reference class being ours again. The delivered text "
        "reaches that itself: the eight-label count is a map artifact.",
        "     "))
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

    lc = lloyd_check()
    ck("the ceiling reproduces from budget.py's own ML machinery, within a "
       "few decades of the delivered 10^120", abs(lc["gap_decades"]) < 4.0)
    ck("the check is independent of the delivered number, not calibrated to "
       "it", lc["log10"] != LLOYD_CEILING_LOG10)

    ck("Earth atoms land near 10^50",
       49.5 < math.log10(earth_atoms()) < 50.5)
    ck("Planck ticks in Earth history land near 10^60",
       60.0 < math.log10(planck_ticks()) < 61.0)

    m = which_reproduces()
    names = [n for n, _, _ in m]
    ck("atoms x Planck ticks reproduces the delivered 10^110",
       "atoms x Planck ticks" in names)
    ck("the pure event count does NOT reproduce it -- it is 60 decades short",
       "labels x atoms" not in names)
    ck("the eight labels contribute under one decade",
       label_contribution() < 1.0)

    hr = headline_readings()
    mult = [h for h in hr if "MULTIPLIER" in h["reading"]][0]
    tot = [h for h in hr if "TOTAL" in h["reading"]][0]
    ck("the multiplier reading reproduces the delivered 42 decades",
       mult["reproduces_delivered_42"])
    ck("the total reading does not, and is UNDER budget instead",
       not tot["reproduces_delivered_42"] and tot["verdict_decades"] < 0)
    ck("the two readings disagree on the sign of the verdict",
       (mult["verdict_decades"] > 0) != (tot["verdict_decades"] > 0))

    cm = cost_models()
    coherent = [c for c in cm if c["coherent"]]
    mixed = [c for c in cm if not c["coherent"]]
    ck("every internally coherent cost model fits inside the ceiling",
       all(c["fits"] for c in coherent))
    ck("exactly one model is marked incoherent, and it is the one that "
       "overshoots",
       len(mixed) == 1 and not mixed[0]["fits"])
    ck("the incoherent model is the delivered one",
       "as delivered" in mixed[0]["model"])
    ck("the coherent models span a wide range, so 'it fits' is not one "
       "number repeated",
       max(c["log10"] for c in coherent)
       - min(c["log10"] for c in coherent) > 40.0)

    nh = nesting_headroom()
    ck("the constructive falsifier is reachable: more nesting breaks the "
       "event-driven model", nh["headroom_decades"] > 0
       and nh["nesting_at_which_it_breaks"] > NESTING_DECADES)

    rn = resolution_needed_to_fit()
    rw = resolution_needed_to_fit(include_nesting=True)
    ck("pure stepping affords a timestep FINER than Planck time -- the "
       "expectation that the knob needed loosening was wrong, and the check "
       "is kept",
       rn["finer_than_planck"] and rn["decades_of_knob"] < 0)
    ck("with nesting as a multiplier the affordable timestep is coarser "
       "than Planck by tens of decades",
       rw["decades_of_knob"] > 30.0)
    ck("and lands at human scale, which is what makes the mixed model "
       "visibly incoherent", 0.01 < rw["timestep_s"] < 100.0)
    ck("the two directions disagree in sign, so the nesting term is what "
       "flips it",
       (rn["decades_of_knob"] > 0) != (rw["decades_of_knob"] > 0))

    ck("report renders", "prices the same physics twice" in report().lower()
       or "PRICES THE SAME PHYSICS TWICE" in report())
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
