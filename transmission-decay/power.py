#!/usr/bin/env python3
"""What "run it in one valley" delivers, computed.

SOURCE_DROP.md asks: "Run it in one valley. Publish the component order
and the provenance coding, including the cells you could not fill."

Two things are computable with no field data:

  1  the HALF-LIFE is defined on a four-level ordinal axis whose top
     level is an open catch-all. Its resolution follows from the axis
     and needs no informants.

  2  COMPONENT ORDER is called "the most useful output". Establishing
     an ordering over eight components is a sample-size question, and
     the answer is computable.

WHAT THIS FILE IS NOT
    It does not simulate a valley, an informant, an account, or a
    community. There are no synthetic transmission chains standing in
    for real ones. The only objects are abstract retention
    probabilities and binomial sampling noise; every number below is a
    statement about the DESIGN's arithmetic.

    The study is not run here. It requires fieldwork and collective
    consent, and its own ethics section says a study that extracts a
    decay rate while accelerating the extraction is self-defeating.

usage:  python3 power.py                # the report
        python3 power.py --selftest

CC0. stdlib only. Parses under Python 3.9. Deterministic given seeds.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import scheme as S  # noqa: E402

TRIALS = 300
SEED0 = 8611


# ------------------------------------------------- half-life resolution

def halflife_resolution():
    """The half-life's resolution follows from the axis, not the data.

    "half-life -- chain position at which mechanism score reaches half
    its C0 value". Chain position has four levels and the top one,
    C3+, is defined as "no traceable chain to a witness" -- which is
    the ABSENCE of a chain position rather than a value of one. So the
    axis carries three ordered positions and a catch-all, and a
    half-life read off it can only ever name an interval between two
    adjacent levels.
    """
    levels = [c["position"] for c in S.CHAIN]
    open_bin = [c for c in S.CHAIN if c["position"].endswith("+")]
    return {
        "levels": levels,
        "n_levels": len(levels),
        "ordered_positions": len(levels) - len(open_bin),
        "open_bins": [c["position"] for c in open_bin],
        "open_bin_gloss": open_bin[0]["gloss"] if open_bin else None,
        "intervals_available": len(levels) - 1,
        "finest_statement": "between %s and %s" % (levels[0], levels[1]),
        "why": "a half-life on this axis names an interval between two "
               "adjacent levels and cannot be finer. That is a property "
               "of the axis and no number of informants changes it.",
        "note_on_open_bin": "C3+ is defined as the absence of a "
                            "traceable chain, so treating it as "
                            "position 3 in a fitted curve assigns a "
                            "coordinate to a category that does not "
                            "have one.",
    }


def halflife_bracket(true_scores):
    """Where a half-life falls, given per-position mean scores.

    Returns the bracketing interval, never an interpolated value: the
    axis is ordinal, so interpolating between C1 and C2 asserts a
    metric the design does not have.
    """
    if not true_scores:
        return {"bracket": None, "state": "NO_DATA"}
    half = true_scores[0] / 2.0
    for i in range(1, len(true_scores)):
        if true_scores[i] <= half:
            return {"bracket": (S.CHAIN[i - 1]["position"],
                                S.CHAIN[i]["position"]),
                    "state": "BRACKETED", "half_value": half,
                    "interpolated": None,
                    "why_not_interpolated": "the axis is ordinal. A "
                                            "value between C1 and C2 "
                                            "asserts a metric the "
                                            "design does not define."}
    return {"bracket": None, "state": "NOT_REACHED_ON_THIS_AXIS",
            "half_value": half,
            "why": "the score never halves within the four levels. The "
                   "half-life is outside the axis, not absent."}


# ------------------------------------------------------ component order

def order_recovery(n_per_position, true_retention, trials=TRIALS,
                   seed=SEED0):
    """How often the observed component order matches the true one.

    Each component has a true retention probability at a given chain
    position. n informants are coded; each component is present or
    absent per informant. The observed order is by observed retention.

    Reported three ways, because "the order" is not one question:
      exact       the whole 8-item order recovered
      top_bottom  the first-dropping and last-dropping correctly named
      pair        one named pair correctly ordered
    """
    rng = random.Random(seed)
    keys = sorted(true_retention)
    truth = sorted(keys, key=lambda k: true_retention[k])
    exact = top = 0
    for _ in range(trials):
        obs = {}
        for k in keys:
            p = true_retention[k]
            obs[k] = sum(1 for _ in range(n_per_position)
                         if rng.random() < p) / float(n_per_position)
        got = sorted(keys, key=lambda k: (obs[k], k))
        exact += 1 if got == truth else 0
        top += 1 if (got[0] == truth[0] and got[-1] == truth[-1]) else 0
    return {"n_per_position": n_per_position, "trials": trials,
            "exact_order": exact / float(trials),
            "top_and_bottom": top / float(trials)}


def pair_recovery(n_per_position, p_lo, p_hi, trials=TRIALS,
                  seed=SEED0 + 1):
    """How often a single named pair is ordered correctly.

    This is the form the drop's own headline questions take: does M7
    outlive M3, does M8 drop first. A pair is far cheaper than a full
    ordering and is what the design actually asks.
    """
    rng = random.Random(seed)
    right = ties = 0
    for _ in range(trials):
        a = sum(1 for _ in range(n_per_position) if rng.random() < p_lo)
        b = sum(1 for _ in range(n_per_position) if rng.random() < p_hi)
        if a == b:
            ties += 1
        elif a < b:
            right += 1
    dec = trials - ties
    return {"n_per_position": n_per_position, "gap": p_hi - p_lo,
            "ties": ties, "tie_rate": ties / float(trials),
            "accuracy_on_decided": right / float(dec) if dec else None}


# ---- a declared, arbitrary retention profile. NOT a prediction. ----
#
# Eight probabilities spanning a plausible range so the arithmetic has
# something to run on. They are NOT a claim about which component
# survives -- that is the study's output and inventing it here would be
# answering the question the design exists to ask.

PROFILE = {"M1": 0.85, "M2": 0.70, "M3": 0.55, "M4": 0.65,
           "M5": 0.60, "M6": 0.45, "M7": 0.75, "M8": 0.30}
PROFILE_NOTE = ("arbitrary and declared. Spaced to make the ordering "
                "arithmetic runnable. NOT a prediction about any "
                "component, because which component drops first is the "
                "design's output.")


def first_to_drop(n_per_position, true_retention, trials=TRIALS,
                  seed=SEED0 + 2):
    """How often the truly first-dropping component is observed lowest.

    "If M8 drops first" is not a pair -- it is one component against
    all seven others, so seven comparisons must all land. Reported
    separately from the pair result because it costs much more.
    """
    rng = random.Random(seed)
    keys = sorted(true_retention)
    truth = min(keys, key=lambda k: true_retention[k])
    hit = 0
    for _ in range(trials):
        obs = {}
        for k in keys:
            p = true_retention[k]
            obs[k] = sum(1 for _ in range(n_per_position)
                         if rng.random() < p)
        lo = min(obs.values())
        winners = [k for k in keys if obs[k] == lo]
        hit += 1 if winners == [truth] else 0
    return {"n_per_position": n_per_position,
            "true_first": truth,
            "recovered_uniquely": hit / float(trials),
            "why": "one component against seven others. Seven "
                   "comparisons must all land, and a tie at the bottom "
                   "is not a recovery."}


def n_for_pair(target, gap, ns=(5, 10, 15, 20, 30, 40, 60, 80, 120)):
    for n in ns:
        r = pair_recovery(n, 0.5 - gap / 2.0, 0.5 + gap / 2.0)
        if r["accuracy_on_decided"] is not None \
                and r["accuracy_on_decided"] >= target:
            return {"n": n, "found": True, "row": r}
    return {"n": None, "found": False}


# ------------------------------------------------------------- report

def wrap(t, w=68, ind="   "):
    out, cur = [], ind
    for word in t.split():
        if len(cur) + len(word) + 1 > w and cur.strip():
            out.append(cur.rstrip())
            cur = ind
        cur += word + " "
    if cur.strip():
        out.append(cur.rstrip())
    return out


def render():
    o = []
    o.append("TRANSMISSION DECAY -- what one valley delivers")
    o.append("")
    o += wrap("SOURCE_DROP.md asks: \"Run it in one valley. Publish the "
              "component order and the provenance coding, including the "
              "cells you could not fill.\" This computes which of its "
              "outputs one valley can carry.", ind="")
    o.append("")
    o += wrap("THE STUDY IS NOT RUN AND IS NOT SIMULATED. It requires "
              "fieldwork and collective consent, and its own ethics "
              "section says a study that extracts a decay rate while "
              "accelerating the extraction is self-defeating. No "
              "synthetic valley, informant, account, or transmission "
              "chain stands in for a real one anywhere below. The only "
              "objects are abstract retention probabilities and "
              "binomial noise.", ind="")
    o.append("")

    o.append("0. THE CODING SCHEME, PARSED")
    o.append("   %d M-components, %d S-codes, %d chain positions"
             % (len(S.COMPONENTS), len(S.STORY_CODES), len(S.CHAIN)))
    for k in sorted(S.COMPONENTS):
        o.append("     %-3s %s" % (k, S.COMPONENTS[k]["label"]))
    o += wrap("This is the scheme `revision-mechanism` recorded as "
              "named-and-absent. It landed, so that folder imports it "
              "from here rather than describing its absence, and its "
              "RM_008 closes.")
    o.append("")

    o.append("1. THE HALF-LIFE'S RESOLUTION FOLLOWS FROM THE AXIS")
    h = halflife_resolution()
    o.append("   levels: %s" % ", ".join(h["levels"]))
    o.append("   ordered positions: %d   open catch-all: %s"
             % (h["ordered_positions"], ", ".join(h["open_bins"])))
    o.append("   intervals available: %d" % h["intervals_available"])
    o.append("   finest statement possible: \"%s\"" % h["finest_statement"])
    o += wrap(h["why"])
    o += wrap("AND: " + h["note_on_open_bin"])
    o.append("")

    o.append("2. COMPONENT ORDER IS THE EXPENSIVE FORM OF THE QUESTION")
    o += wrap("The drop calls component order \"the most useful "
              "output\" and then asks two questions that are not "
              "orderings: does M7 outlive M3, and does M8 drop first. "
              "Those cost very different amounts.")
    o.append("")
    o.append("   informants coded per chain position:")
    o.append("   %-6s %-14s %-16s %s"
             % ("n", "full 8-order", "M8 first (1 v 7)", "one named pair"))
    for n in (5, 10, 20, 40, 80, 160):
        a = order_recovery(n, PROFILE)
        b = first_to_drop(n, PROFILE)
        c = pair_recovery(n, 0.40, 0.60)
        o.append("   %-6d %-14.3f %-16.3f %.3f"
                 % (n, a["exact_order"], b["recovered_uniquely"],
                    c["accuracy_on_decided"]))
    o.append("")
    o += wrap("The retention profile behind these is arbitrary and "
              "declared: " + PROFILE_NOTE)
    o.append("")
    o += wrap("Reading across: the full eight-component order is out of "
              "reach at any plausible one-valley sample -- 0.7 percent "
              "at twenty informants per position, and still only about "
              "a third at a hundred and sixty. \"M8 drops first\" is "
              "one component against seven and costs about forty. A "
              "single named pair -- which is the form BOTH of the "
              "drop's headline questions take -- is affordable at ten "
              "to twenty.")
    o.append("")
    o += wrap("So the design's stated most-useful output is the "
              "expensive form, and its own two headline questions are "
              "the cheap form. Someone running one valley can answer "
              "the questions and not the ordering.")
    o.append("")

    o.append("3. WHAT A NAMED PAIR COSTS, BY EFFECT SIZE")
    o.append("   %-6s %s" % ("n", "  ".join("gap=%.2f" % g
                                            for g in (0.10, 0.20, 0.30))))
    for n in (5, 10, 20, 40, 80):
        cells = []
        for g in (0.10, 0.20, 0.30):
            r = pair_recovery(n, 0.5 - g / 2.0, 0.5 + g / 2.0)
            cells.append("%-8.3f" % r["accuracy_on_decided"])
        o.append("   %-6d %s" % (n, "  ".join(cells)))
    o += wrap("A twenty-point retention difference between two named "
              "components is decidable at about ten to twenty "
              "informants per chain position. A ten-point difference "
              "takes eighty.")
    return "\n".join(o)


def main(argv):
    if "--selftest" in argv:
        import selftest_power
        return selftest_power.run()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
