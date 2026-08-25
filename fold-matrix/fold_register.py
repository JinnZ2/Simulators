#!/usr/bin/env python3
# fold_register.py  -- CC0, stdlib only, phone-buildable
#
# Folded-term register + document scanner.
#
# A folded term is a compact matrix wearing the costume of a scalar.
# The register does NOT score documents. It emits the grid cells that
# must be filled before the term can be read as a variable at all.
# Unfilled cells stay None. None is the finding, not a missing value.
#
# usage:  python3 fold_register.py doc.txt
#         python3 fold_register.py --grid efficiency
#         python3 fold_register.py --list

import json
import re
import sys

UNFILLED = None          # refused, not zero
KAVIK = "kavik"          # term she named
CAND = "candidate"       # proposed for her to cut or keep

# ---------------------------------------------------------------------
# GRID: every folded term is severed on two axes, independently.
# Depth is a grid, not a number.
# ---------------------------------------------------------------------

GRID_CELLS = {
    # DOWNWARD -- toward substrate. Leaves a trail; was derived once.
    "D1_resolves_to": "What physical/countable quantity does this term resolve to?",
    "D2_deepest_quantified": "Deepest quantity THIS DOCUMENT SET actually computes. "
                             "Not the deepest that exists. Stop here.",
    "D3_levels_severed": "Levels between D1 and D2 that are asserted, not carried.",

    # UPWARD -- toward the purpose. Never derived. Worse instrumented.
    "U1_goal_stated": "Is a goal stated anywhere, in an artifact? "
                      "Highest stated artifact = upward stop.",
    "U2_relation_measured": "Was the term->goal relation MEASURED, or asserted at adoption?",
    "U3_sign": "Sign of that relation. Assumed positive counts as UNFILLED.",
    "U4_magnitude": "Magnitude of that relation, with units.",

    # CLOCK -- one per level, not one per claim.
    "C1_horizon_per_level": "Time frame declared at EACH level, or one clock "
                            "assumed to cover all of them?",

    # SCOPE -- what the objective dropped.
    "S1_boundary": "Measured over what boundary?",
    "S2_function_set": "Functions outside the objective, enumerated? "
                       "If not, replacement inference is invalid on structure alone.",
}

# ---------------------------------------------------------------------
# REGISTER
# ---------------------------------------------------------------------

REGISTER = {
    "money": {
        "source": KAVIK,
        "substitutes_for": "skill + time + labor",
        "sign_storage": "signed",
        "residual_tell": "false cutoff -- 'we don't have the money' closes the "
                         "equation before the other side (time/skill/labor) is read",
        "counter_case": "Ford demonstration stage: process proved on recycled and "
                        "fabricated machines BEFORE backers. Money followed proof.",
    },
    "procedure": {
        "source": KAVIK,
        "substitutes_for": "doing",
        "sign_storage": "unsigned_positive",
        "residual_tell": "abstraction stacks on abstraction; compounds with money "
                         "as a second focal point, so neither level is readable",
        "counter_case": UNFILLED,
    },
    "regulation": {
        "source": KAVIK,
        "substitutes_for": "enforcement of the procedure->money link",
        "sign_storage": "unsigned_positive",
        "residual_tell": "adds a folded term rather than a measurable one",
        "counter_case": "building code exists because the builder won't live in it; "
                        "self-builder has the consequence built in",
    },
    "optimization": {
        "source": KAVIK,
        "substitutes_for": "a chosen objective + a trajectory + a scope, all dropped",
        "sign_storage": "unsigned_positive",
        "residual_tell": "each folded term carries its own dependency tree; folding "
                         "the top makes the whole compound unreadable, not one level",
        "counter_case": "no organism optimizes one thing to the exclusion of itself. "
                        "Single-objective maximizers are ABSENT from the observed "
                        "set, not rare. Failure mode is a TRUNCATED optimizer.",
    },
    "efficiency": {
        "source": KAVIK,
        "substitutes_for": "output/input under an unstated boundary and horizon",
        "sign_storage": "unsigned_positive",
        "residual_tell": "quoted scope-free, so it reads as a property of the thing "
                         "rather than of a chosen measurement frame",
        "counter_case": "'AI more efficient than trees, therefore trees redundant' "
                        "-- comparison against a function set never enumerated",
    },

    # ---- candidates: same signature, not yet cut by Kavik ----
    "merit": {
        "source": CAND,
        "substitutes_for": "a measurement chain that has lost its referent",
        "sign_storage": "unsigned_positive",
        "residual_tell": "register passes as evidence; marker keeps value in one "
                         "domain and loses it in another with no measurement behind either",
        "counter_case": UNFILLED,
    },
    "experience": {
        "source": CAND,
        "substitutes_for": "accumulated hours + continuity + transfer, none checked",
        "sign_storage": "unsigned_positive",
        "residual_tell": "origin claim grants present-tense standing with no decay "
                         "check; hours count as formation in some fields, nothing in others",
        "counter_case": UNFILLED,
    },
    "safety": {
        "source": CAND,
        "substitutes_for": "hazard x exposure x consequence, over an unstated population",
        "sign_storage": "unsigned_positive",
        "residual_tell": "severity language baked into the variable name, so "
                         "direction is asserted rather than measured",
        "counter_case": UNFILLED,
    },
    "risk": {
        "source": CAND,
        "substitutes_for": "probability x magnitude over an unstated denominator",
        "sign_storage": "unsigned_negative",
        "residual_tell": "denominator omitted; ranking survives even when the "
                         "exposure base is unknown",
        "counter_case": UNFILLED,
    },
    "productivity": {
        "source": CAND,
        "substitutes_for": "output per unit input, inputs selectively counted",
        "sign_storage": "unsigned_positive",
        "residual_tell": "uncounted inputs migrate to whoever is furthest from "
                         "the median case",
        "counter_case": UNFILLED,
    },
    "quality": {
        "source": CAND,
        "substitutes_for": "conformance to a spec that is itself unstated",
        "sign_storage": "unsigned_positive",
        "residual_tell": "conformance and fitness collapsed into one word",
        "counter_case": UNFILLED,
    },
    "performance": {
        "source": CAND,
        "substitutes_for": "score on a benchmark + the benchmark's own construction",
        "sign_storage": "unsigned_positive",
        "residual_tell": "the instrument only measures where it was built to look; "
                         "off-benchmark behavior scores as off-task and is trained out",
        "counter_case": UNFILLED,
    },
    "capacity": {
        "source": CAND,
        "substitutes_for": "peak force, quoted where sustained work capacity is meant",
        "sign_storage": "unsigned_positive",
        "residual_tell": "peak and sustained welded into one number",
        "counter_case": UNFILLED,
    },
    "resources": {
        "source": CAND,
        "substitutes_for": "a stock and a flow, welded",
        "sign_storage": "unsigned_positive",
        "residual_tell": "a depleting buffer counted as supply, so the aggregate "
                         "metric holds flat right up to the inelastic transition",
        "counter_case": UNFILLED,
    },
    "compliance": {
        "source": CAND,
        "substitutes_for": "whether the stated relation still holds; substituted "
                           "with whether the form was filed",
        "sign_storage": "unsigned_positive",
        "residual_tell": "instrument cannot report its own failure -- a filed form "
                         "and a working control return the same value",
        "counter_case": UNFILLED,
    },
    "growth": {
        "source": CAND,
        "substitutes_for": "rate of change of an aggregate whose composition is folded",
        "sign_storage": "unsigned_positive",
        "residual_tell": "composition shift invisible; sign asserted by the word",
        "counter_case": UNFILLED,
    },
    "impact": {
        "source": CAND,
        "substitutes_for": "a counterfactual that was never run",
        "sign_storage": "unsigned_positive",
        "residual_tell": "no baseline arm; attribution and correlation collapsed",
        "counter_case": UNFILLED,
    },
}

# words that trigger a scan hit, mapped to register key
ALIASES = {
    "protocol": "procedure", "process": "procedure", "policy": "regulation",
    "standard": "regulation", "optimize": "optimization",
    "optimized": "optimization", "optimal": "optimization",
    "efficient": "efficiency", "efficiencies": "efficiency",
    "cost": "money", "budget": "money", "funding": "money",
    "qualified": "merit", "talent": "merit", "best": "merit",
    "experienced": "experience", "seasoned": "experience",
    "safe": "safety", "risky": "risk", "productive": "productivity",
    "quality": "quality", "capabilities": "performance",
    "capable": "performance", "throughput": "productivity",
    "scalable": "capacity", "sustainable": "resources",
    "compliant": "compliance", "impactful": "impact",
}


def grid_for(term):
    """Empty grid. Every cell None until a document fills it."""
    rec = REGISTER.get(term)
    if rec is None:
        return None
    return {
        "term": term,
        "source": rec["source"],
        "substitutes_for": rec["substitutes_for"],
        "sign_storage": rec["sign_storage"],
        "residual_tell": rec["residual_tell"],
        "cells": {k: UNFILLED for k in GRID_CELLS},
    }


def scan(text):
    """Find folded terms. Emit unfilled grids. Do not score."""
    hits = {}
    lines = text.splitlines()
    for n, line in enumerate(lines, 1):
        for word in re.findall(r"[A-Za-z]+", line.lower()):
            key = word if word in REGISTER else ALIASES.get(word)
            if key is None:
                continue
            h = hits.setdefault(key, {"grid": grid_for(key), "lines": []})
            if len(h["lines"]) < 12:
                h["lines"].append(n)
    total = len(hits) * len(GRID_CELLS)
    return {
        "folded_terms_found": sorted(hits),
        "occurrences": {k: v["lines"] for k, v in hits.items()},
        "grids": {k: v["grid"] for k, v in hits.items()},
        "cells_total": total,
        "cells_filled": 0,
        "cells_unfilled": total,
        "score": UNFILLED,
        "verdict": "NOT SCORABLE -- grid unfilled. Absence is the reading.",
    }


def main(argv):
    if len(argv) < 2 or argv[1] == "--list":
        for k, v in sorted(REGISTER.items()):
            print(f"{v['source']:9} {k:14} <- {v['substitutes_for']}")
        return 0
    if argv[1] == "--grid":
        g = grid_for(argv[2])
        print(json.dumps(g if g else {"error": "not in register"}, indent=2))
        return 0
    with open(argv[1], encoding="utf-8", errors="replace") as f:
        print(json.dumps(scan(f.read()), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
