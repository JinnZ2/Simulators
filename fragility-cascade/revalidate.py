#!/usr/bin/env python3
"""
revalidate.py -- re-evaluate a decayed claim: what decayed, and what retest
that actually implies. CC0 / Public Domain. stdlib-only. imports info_taxonomy.

info_taxonomy.staleness() returns a flag. A flag implies one response --
retest everything. But decay is not one thing, and the retest a decayed
claim needs is usually far cheaper than a full re-establishment. Sometimes
it is none at all.

Five axes, each diagnosing a DIFFERENT failure:

    TEMPORAL SCOPE    does the referent move? age is not decay. a constant
                      does not go stale by sitting; a seasonal reading goes
                      stale in months regardless of any half-life.
    SCOPE             was the claim established over a range that includes
                      the conditions it is now applied to?
    METHODOLOGY       is the acquiring mode still sound, superseded, or
                      structurally blind to what the claim asserts?
    UPDATED INFO      has anything arrived since -- corroboration that
                      already refreshes it, or contradiction that aims it?
    PHYSICAL          can it be checked against ground truth directly, and
    AUTHENTICITY      how cheaply? this sets the retest's cost, and whether
                      a retest is possible at all.

The mode table already carries the prescription: every Mode states
stays_fresh_by. Diagnosis routes to it -- or to a DIFFERENT mode when the
method itself was the failure.

BOUNDARY: outputs a retest PLAN (a trajectory), never a new verdict. It does
not re-decide the claim, does not auto-refresh, and does not judge the
method's fit -- where fit requires reading meaning, it surfaces the mode's
blindness and hands the judgment to the operator.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from info_taxonomy import Corpus, Item, MODES

# SEED -- placeholder scales. the STRUCTURE (volatility sets a decay clock
# independent of mode half-life) is the contribution; numbers are operator's.
VOLATILITY_YR: Dict[str, Optional[float]] = {
    "static":   None,     # referent does not move -- age flags are spurious
    "slow":     50.0,
    "seasonal": 0.5,
    "volatile": 0.05,
}


@dataclass
class Envelope:
    """The validity envelope of a claim. Operator-supplied; unrecorded is
    reported LOUD, never assumed fine."""
    key: str
    established_over: Optional[str] = None   # conditions the claim was made under
    applied_to: Optional[str] = None         # conditions it is used under NOW
    referent_volatility: Optional[str] = None
    physical_check: Optional[str] = None     # a direct ground-truth check, if any
    method_superseded_by: Optional[str] = None
    checkable: bool = True                   # False = unfalsifiable as stated


@dataclass
class Axis:
    name: str
    status: str
    finding: str
    implies: str = ""


@dataclass
class Plan:
    key: str
    axes: List[Axis]
    outcome: str          # none | cheap | directed | re_establish | undecidable
    method: str
    cost: str
    notes: List[str] = field(default_factory=list)


# =============================================================================
def diagnose(c: Corpus, key: str, env: Optional[Envelope] = None) -> List[Axis]:
    it = c.items[key]
    m = MODES.get(it.mode)
    age = c.year - (it.refreshed or it.year) if it.year else None
    axes: List[Axis] = []

    # -- 1. TEMPORAL SCOPE: does the referent move at all? -------------------
    if env is None or env.referent_volatility is None:
        axes.append(Axis("temporal_scope", "UNRECORDED",
                         "referent volatility not recorded",
                         "record it -- age alone cannot distinguish a "
                         "constant from a seasonal reading"))
    else:
        vol = env.referent_volatility
        scale = VOLATILITY_YR.get(vol)
        if scale is None:
            axes.append(Axis("temporal_scope", "STATIC",
                             f"referent is {vol} -- does not move with time",
                             "any age-based staleness flag is SPURIOUS here"))
        elif age is not None and age > scale:
            axes.append(Axis("temporal_scope", "EXPIRED",
                             f"referent is {vol} (scale {scale:g}yr), "
                             f"claim age {age}yr",
                             "re-observe -- volatility governs, not half-life"))
        else:
            axes.append(Axis("temporal_scope", "current",
                             f"referent {vol}, age {age}yr within scale"))

    # -- 2. SCOPE: established range vs conditions of current use ------------
    if env is None or env.established_over is None:
        axes.append(Axis("scope", "UNRECORDED",
                         "conditions of establishment not recorded",
                         "a claim with no stated range cannot be shown "
                         "in-range -- re-establish, don't retest"))
    elif env.applied_to and env.applied_to != env.established_over:
        axes.append(Axis("scope", "DRIFTED",
                         f"established over [{env.established_over}], "
                         f"applied to [{env.applied_to}]",
                         "extend the range at current conditions -- a "
                         "narrower job than full re-establishment"))
    else:
        axes.append(Axis("scope", "in_scope",
                         f"applied within [{env.established_over}]"))

    # -- 3. METHODOLOGY: mode sound, superseded, or blind? -------------------
    if m is None:
        axes.append(Axis("methodology", "UNREGISTERED",
                         f"mode '{it.mode}' not in the table",
                         "untraceable -- re-establish"))
    elif env and env.method_superseded_by:
        axes.append(Axis("methodology", "SUPERSEDED",
                         f"method superseded by {env.method_superseded_by}",
                         f"re-acquire via {env.method_superseded_by}"))
    else:
        axes.append(Axis("methodology", "review",
                         f"mode '{it.mode}' is blind to: {m.blind_to}",
                         "operator judges whether that blindness touches "
                         "what this claim asserts"))

    # -- 4. UPDATED INFORMATION: what arrived since? -------------------------
    s = c.support(key)
    newer = [k2 for k2 in s["independent_modes"] if k2 != it.mode]
    if s["contradicted_by"]:
        axes.append(Axis("updated_info", "CONTRADICTED",
                         f"contradicted by {s['contradicted_by']}",
                         "aim the retest at the contradiction, not the "
                         "whole claim"))
    elif len(newer) >= 1:
        axes.append(Axis("updated_info", "CORROBORATED",
                         f"{len(newer)} independent mode(s) since: {newer}",
                         "decay may already be answered without a retest"))
    else:
        axes.append(Axis("updated_info", "none",
                         "nothing independent has arrived since"))

    # -- 5. PHYSICAL AUTHENTICITY: can ground truth settle it, how cheaply? --
    if env and not env.checkable:
        axes.append(Axis("physical_authenticity", "UNFALSIFIABLE",
                         "not checkable against ground truth as stated",
                         "cannot be repaired by retest -- restate it so a "
                         "check could fail, or retire it"))
    elif env and env.physical_check:
        axes.append(Axis("physical_authenticity", "DIRECT",
                         f"direct check available: {env.physical_check}",
                         "cheapest sufficient retest -- run this first"))
    else:
        axes.append(Axis("physical_authenticity", "PROXY_ONLY",
                         "no direct ground-truth check recorded",
                         "retest falls back to the mode's own refresh path"))

    return axes


# =============================================================================
def retest_plan(c: Corpus, key: str, env: Optional[Envelope] = None) -> Plan:
    axes = diagnose(c, key, env)
    st = {a.name: a.status for a in axes}
    it = c.items[key]
    m = MODES.get(it.mode)
    notes: List[str] = []

    # cannot be repaired by retest
    if st["physical_authenticity"] == "UNFALSIFIABLE":
        return Plan(key, axes, "undecidable", "restate or retire",
                    "n/a", ["no check could fail -- retesting cannot resolve it"])
    if st["scope"] == "UNRECORDED" or st["methodology"] == "UNREGISTERED":
        return Plan(key, axes, "re_establish",
                    "establish from scratch, recording the range this time",
                    "full",
                    ["a claim with no stated range or untraceable method "
                     "cannot be repaired by retest"])

    # no retest needed
    if st["temporal_scope"] == "STATIC" and st["updated_info"] != "CONTRADICTED":
        return Plan(key, axes, "none",
                    "no retest -- referent does not move", "zero",
                    ["age-based staleness flag is spurious for a static "
                     "referent; check the applicability range instead"])
    if st["updated_info"] == "CORROBORATED" and st["temporal_scope"] != "EXPIRED" \
            and st["scope"] != "DRIFTED":
        return Plan(key, axes, "none",
                    "no retest -- refreshed by independent corroboration",
                    "zero",
                    ["record the corroborating item as the refresh"])

    # directed
    if st["updated_info"] == "CONTRADICTED":
        method = (env.physical_check if env and env.physical_check
                  else (m.stays_fresh_by if m else "re-acquire"))
        return Plan(key, axes, "directed", method,
                    "direct" if (env and env.physical_check) else "mode-refresh",
                    ["aim at the contradiction; do not re-establish the whole "
                     "claim"])

    # superseded method -> re-acquire through the superseding mode
    if st["methodology"] == "SUPERSEDED":
        return Plan(key, axes, "re_establish",
                    f"re-acquire via {env.method_superseded_by}", "full",
                    ["the method was the failure, not the claim's age"])

    # cheap physical check beats everything else available
    if st["physical_authenticity"] == "DIRECT":
        if st["scope"] == "DRIFTED":
            notes.append("run the check AT the drifted conditions -- that "
                         "extends the range and refreshes in one move")
        return Plan(key, axes, "cheap", env.physical_check, "direct", notes)

    # fall back to the mode's own declared refresh path
    return Plan(key, axes, "cheap" if st["temporal_scope"] == "EXPIRED"
                else "directed",
                m.stays_fresh_by if m else "re-acquire", "mode-refresh",
                notes)


def report(c: Corpus, key: str, env: Optional[Envelope] = None):
    p = retest_plan(c, key, env)
    print(f"\n  [{key}] {c.items[key].claim}")
    print(f"     mode: {c.items[key].mode}   year: {c.items[key].year}")
    for a in p.axes:
        print(f"     {a.name:22s} {a.status:14s} {a.finding}")
        if a.implies:
            print(f"     {'':22s} {'':14s} -> {a.implies}")
    print(f"     PLAN: {p.outcome.upper():13s} cost={p.cost}")
    print(f"           method: {p.method}")
    for n in p.notes:
        print(f"           note: {n}")


# =============================================================================
if __name__ == "__main__":
    c = Corpus(current_year=2026)

    c.add(Item("const.latent_vap", "water latent heat of vaporization "
               "2.26 MJ/kg", "measurement", "numeric", ["physics"],
               "measured_constant", year=1953))
    c.add(Item("code.fill_depth", "county table: 0.5 m imported fill required",
               "rule", "text", ["code", "soil"], "authority", year=1974,
               contradicts=["site.penetrometer"]))
    c.add(Item("site.penetrometer", "240 kPa at 0.5 m",
               "measurement", "instrument_trace", ["soil"], "instrument",
               year=2026))
    c.add(Item("site.moisture", "surface moisture supports compaction",
               "observation", "embodied", ["soil"], "direct_observation",
               year=2025))
    c.add(Item("siting.bench", "never build below the second bench",
               "teaching", "oral", ["siting"], "transmission",
               chain=["grandmother", "mother", "operator"],
               corroborates=["siting.silt"]))
    c.add(Item("siting.silt", "silt lines at first-bench height",
               "observation", "text", ["siting"], "direct_observation",
               year=2025, corroborates=["siting.bench"]))
    c.add(Item("claim.vibes", "the site feels right",
               "claim", "text", ["siting"], "direct_observation", year=2026))

    envs = {
        "const.latent_vap": Envelope("const.latent_vap",
                                     established_over="1 atm, pure water",
                                     applied_to="1 atm, pure water",
                                     referent_volatility="static"),
        "code.fill_depth": Envelope("code.fill_depth",
                                    established_over="1974 materials, equipment, "
                                                     "risk models",
                                    applied_to="2026 site, measured bearing",
                                    referent_volatility="slow",
                                    physical_check="penetrometer at footing depth"),
        "site.moisture": Envelope("site.moisture",
                                  established_over="autumn, post-rain",
                                  applied_to="autumn, post-rain",
                                  referent_volatility="seasonal",
                                  physical_check="hand test at depth"),
        "siting.bench": Envelope("siting.bench",
                                 established_over="this valley, this river",
                                 applied_to="this valley, this river",
                                 referent_volatility="slow"),
        "claim.vibes": Envelope("claim.vibes", checkable=False),
    }

    print("=" * 70)
    print("REVALIDATION -- what decayed, and what retest that implies")
    print("=" * 70)
    for k in ["const.latent_vap", "code.fill_depth", "site.moisture",
              "siting.bench", "claim.vibes"]:
        report(c, k, envs.get(k))

    print("\n" + "=" * 70)
    print("five decayed-looking claims, five DIFFERENT answers:")
    print("  constant   -> no retest. referent doesn't move; age flag spurious.")
    print("  code rule  -> directed. a contradiction arrived; a direct")
    print("                physical check settles it cheaply.")
    print("  moisture   -> expired by VOLATILITY, not half-life. re-observe.")
    print("  teaching   -> no retest. independent mode already corroborated.")
    print("  'vibes'    -> undecidable. no check could fail it -- retesting")
    print("                cannot resolve what was never falsifiable.")
    print("=" * 70)
