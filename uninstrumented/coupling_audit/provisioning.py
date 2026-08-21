#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
# To the extent possible under law, the authors have waived all copyright and
# related or neighboring rights to this file.
"""
provisioning.py - the discriminating test, and a unit for coupling strength.

    python3 provisioning.py --resolution   # which tissue can ask the question
    python3 provisioning.py --cases        # the delivered cases, scored
    python3 provisioning.py --amplitude    # coupling strength as a number
    python3 provisioning.py --report
    python3 provisioning.py --selftest

audit.py records whether a MODEL applies its coupling machinery evenly. This
module is about the other end: whether the coupling itself is MEASURABLE in a
given body of evidence, and what would separate it from the explanations
already standing in the literature.

THREE HYPOTHESES for isotopic spread in an archaeological animal assemblage:

  MOBILITY          people and/or animals moved along a coast or a range, so
                    a site aggregates individuals formed elsewhere
  BREED_OR_STATUS   the site held two or more classes of animal, each
                    internally consistent, provisioned differently
  VARIABLE_COUPLING one class, switching draw -- provisioned when supply
                    allows, re-coupled to its own foraging envelope when it
                    does not, re-imported when supply returns

They predict different SIGNATURES, and the signatures are separable -- but
only in a tissue that resolves sub-annually. Bone collagen averages years, so
a within-year switch is averaged away BEFORE the sample is taken and the
spread presents as between-individual. That is a resolution pairing in the
`reasoning-gate` G-RES sense: instrument x margin <= feature.

WHAT IS DELIVERED AND WHAT IS NOT. Every case and citation below arrives from
the delivered material and is marked MODEL_SEEDED. None was independently
verified here, no isotope value was computed here, and the tissue averaging
windows are DECLARED PARAMETERS, not measurements. What this module computes
is which hypotheses a given evidence configuration can separate, which is a
property of the design rather than of the past.

stdlib only, parses under Python 3.9.
"""

import argparse
import sys

HYPOTHESES = ("MOBILITY", "BREED_OR_STATUS", "VARIABLE_COUPLING")

# The signature each hypothesis predicts. `within_individual` is the axis that
# separates VARIABLE_COUPLING from the other two, and it is the axis a
# years-averaging tissue destroys.
SIGNATURES = {
    "MOBILITY": {
        "within_individual_spread": False,
        "between_individual_spread": True,
        "covaries_with_strontium": True,
        "phased_to_season": False,
        "note": "a spatial signal. strontium should co-vary with the "
                "carbon/nitrogen spread, because the individuals formed in "
                "different places",
    },
    "BREED_OR_STATUS": {
        "within_individual_spread": False,
        "between_individual_spread": True,
        "covaries_with_strontium": False,
        "phased_to_season": False,
        "note": "two or more classes at one site. spread is BETWEEN "
                "individuals and each individual is internally consistent",
    },
    "VARIABLE_COUPLING": {
        "within_individual_spread": True,
        "between_individual_spread": True,
        "covaries_with_strontium": False,
        "phased_to_season": True,
        "note": "one class with a switching draw. spread is WITHIN the "
                "individual, sequential, phased to season -- the same animal "
                "moving between provisioned and foraged intake",
    },
}

# DECLARED PARAMETERS. Order-of-magnitude averaging windows for each tissue,
# in days. Not measured here; stated so the resolution check is auditable and
# so a reader who disagrees can change one number and re-run.
TISSUES = {
    "bone_collagen": {
        "averaging_days": 1095.0,       # years; longer in large-bodied taxa
        "sequential": False,
        "note": "turnover integrates years of intake into one value. a "
                "within-year switch is averaged away before sampling",
    },
    "incremental_dentine": {
        "averaging_days": 30.0,
        "sequential": True,
        "note": "sampled along the tooth: a time series of one individual's "
                "intake during tooth formation",
    },
    "sequential_enamel": {
        "averaging_days": 30.0,
        "sequential": True,
        "note": "d18O and d13C sampled along the growth axis; established in "
                "cattle since the 1990s and validated by a controlled "
                "feeding experiment with a known diet switch",
    },
}

SEASONAL_SWITCH_DAYS = 180.0   # the feature being resolved: one season
G_RES_MARGIN = 2.0             # instrument x margin <= feature


class GeometryNotDeclared(Exception):
    pass


# --- the resolution pairing ------------------------------------------------

def resolves(tissue, feature_days=SEASONAL_SWITCH_DAYS, margin=G_RES_MARGIN):
    """Can this tissue resolve a switch on this timescale?

    G-RES: instrument resolution x margin must not exceed the feature. Returns
    the pair rather than a bare bool, so the decision is inspectable.
    """
    if tissue not in TISSUES:
        raise KeyError(tissue)
    t = TISSUES[tissue]
    need = t["averaging_days"] * margin
    return {
        "tissue": tissue,
        "averaging_days": t["averaging_days"],
        "margin": margin,
        "required_below": feature_days,
        "instrument_times_margin": need,
        "resolves": need <= feature_days,
        "sequential": t["sequential"],
        "shortfall_factor": need / feature_days,
    }


def separable(tissue):
    """Which hypotheses can this tissue tell apart?

    VARIABLE_COUPLING is separated from the other two ONLY by the
    within-individual axis, which needs a sequential tissue that resolves the
    switch. Without it the coupling hypothesis is not refuted -- it is
    unaskable, which is a different state and the one worth naming.
    """
    r = resolves(tissue)
    ok = r["resolves"] and r["sequential"]
    return {
        "tissue": tissue,
        "separates_variable_coupling": ok,
        "separates_mobility_from_status": True,  # strontium, either tissue
        "state": "SEPARABLE" if ok else "UNASKABLE_IN_THIS_TISSUE",
        "why": ("sequential sampling resolves the within-individual axis"
                if ok else
                "the within-individual axis is averaged away before sampling; "
                "the spread can only present as between-individual, so the "
                "coupling hypothesis cannot fail here. Not refuted -- "
                "unasked."),
    }


# --- coupling strength as a number -----------------------------------------

def amplitude_reading(permil_range, geometry=None):
    """Intra-tooth amplitude as a coupling-strength measurement.

    Flat = fixed draw. High amplitude = supply-coupled. This is what turns the
    audit's coupling field from Y/N into a quantity, at least for
    archaeological cases.

    REFUSES without a declared sampling geometry. Dentine sample geometry
    changes the intra-tooth pattern, so amplitude is partly a methods
    artifact and a comparison across studies that does not state geometry is
    comparing two different instruments. The refusal is the same shape as
    audit.py's requirement that machinery be named in the model's own
    vocabulary: a number whose instrument is undeclared is not yet a reading.
    """
    if not geometry:
        raise GeometryNotDeclared(
            "sampling geometry must be declared before an intra-tooth "
            "amplitude is comparable. Geometry changes the pattern, so an "
            "amplitude without it is a number from an unnamed instrument. "
            "State increment width, orientation and count.")
    if permil_range is None:
        return {"amplitude_permil": None, "reading": "NOT_MEASURED",
                "geometry": geometry,
                "why": "no amplitude reported. distinct from a flat series, "
                       "which is a measurement"}
    if permil_range < 0:
        raise ValueError("amplitude cannot be negative")
    if permil_range < 1.0:
        reading = "FLAT_FIXED_DRAW"
    elif permil_range < 2.0:
        reading = "INTERMEDIATE"
    else:
        reading = "HIGH_SUPPLY_COUPLED"
    return {"amplitude_permil": permil_range, "reading": reading,
            "geometry": geometry,
            "why": "thresholds are CONVENTIONAL, set against the delivered "
                   "Vinca-Belo brdo cattle range of 0.7 to 2.4 permil within "
                   "one herd. They are a scale for that corpus and are not "
                   "calibrated against a controlled feeding experiment here."}


# --- the calibration, and what the method has already been pointed at ------

CALIBRATION = {
    "study": "Balasse et al., controlled feeding experiment",
    "what_was_known": "a C3-to-C4 diet switch, plus weaning",
    "recovered_from_intra_tooth_variation": True,
    "why_it_matters": "the discriminator is not merely plausible -- a known "
                      "switch was recovered from intra-tooth variation under "
                      "controlled conditions. That is a positive control in "
                      "the null-harness sense, and it exists for caprines "
                      "and cattle and not for dogs.",
}

# Published applications measuring the switch directly, as delivered.
# `commodity_species` is the field the cross-species extension turns on.
PUBLISHED_APPLICATIONS = [
    {"site": "Tana del Barletta, Ligurian Prealps",
     "taxa": ["cattle", "sheep/goat"], "commodity_species": True,
     "what": "intra-tooth series, Late Neolithic to Early Bronze Age"},
    {"site": "Vinca-Belo brdo (PLOS One)",
     "taxa": ["cattle"], "commodity_species": True,
     "what": "cattle intra-tooth d13C amplitude 0.7 to 2.4 permil within one "
             "assemblage -- some nearly flat, others roughly 3x the range"},
    {"site": "Schipluiden, Netherlands",
     "taxa": ["cattle", "red deer", "suids"], "commodity_species": True,
     "what": "d13C lower than expected in some cattle but not in red deer or "
             "suids from the same site; read as leafy fodder"},
    {"site": "Indus Civilisation herds",
     "taxa": ["cattle", "caprines"], "commodity_species": True,
     "what": "sequential multi-isotope husbandry and seasonal mobility"},
    {"site": "Ksizovo-1 forest-steppe",
     "taxa": ["herd animals"], "commodity_species": True,
     "what": "sequential multi-isotope husbandry and seasonal mobility"},
    {"site": "Perdigoes, southern Portugal",
     "taxa": ["sheep", "goat"], "commodity_species": True,
     "what": "seasonal fodder supplementation invoked to explain the "
             "patterns"},
]


def cross_species_readout():
    """The author's stated extension, and what the corpus does and does not say.

    STATED BY THE AUTHOR, UNTESTED: the same coupling is predicted for
    chickens, cattle, yak and buffalo -- household draw tracks surplus while
    protection is held constant through the switch -- and in species with a
    commodity output the switching is ALREADY measured seasonally per
    individual, "because no one had to argue about whether the animal
    counted."

    The count below is consistent with that and does NOT establish it. A
    correlation between commodity status and measurement maturity has other
    live explanations -- sample availability, tooth size and enamel thickness,
    which agricultural-research funding lines exist. What the count does show
    is that the asymmetry is real and large, which is the part that was in
    question.

    Worth naming: this is the same gate as the FAO LEAP / GLEAM entry in
    entries.py, seen from the other side. There the gate is `market_output`
    and it keeps companion animals out of the water accounting. Here the same
    line is why the measurement exists at all for cattle.
    """
    apps = PUBLISHED_APPLICATIONS
    commodity = [a for a in apps if a["commodity_species"]]
    dog_seq = sum(c["n_sequential"] or 0 for c in CASES
                  if "dog" in c["case_id"].lower()
                  or "canid" in c["case_id"].lower()
                  or "Arroyo" in c["case_id"])
    return {
        "published_applications": len(apps),
        "on_commodity_species": len(commodity),
        "on_companion_species": len(apps) - len(commodity),
        "dog_sequential_individuals": dog_seq,
        "claim_status": "STATED_BY_AUTHOR_UNTESTED",
        "count_establishes": "that the asymmetry is real and large",
        "count_does_not_establish": "that commodity status is its cause",
        "same_gate_as": "entries.py -- FAO LEAP / GLEAM, gate market_output",
    }


# --- the delivered cases ---------------------------------------------------
#
# MODEL_SEEDED. Delivered material, one pass, not independently verified here.
# `standing_explanation` is what the cited work concluded; `also_fits` records
# whether the coupling hypothesis predicts the same observation, which is the
# whole point -- two hypotheses fitting one observation is not agreement.

CASES = [
    {
        "case_id": "Harris et al. 2020 -- Labrador Inuit sled dogs",
        "n": 35,
        "n_sequential": 4,
        "tissue": "bone_collagen",
        "observation": "Double Mer Point dogs the most heterogeneous of any "
                       "site",
        "standing_explanation": "MOBILITY -- long-distance movement of people "
                                "and/or animals along the coast",
        "also_fits": ["VARIABLE_COUPLING"],
        "tested_against_each_other": False,
        "same_site_wild_control": False,
        "amplitude_permil": None,
        "geometry_declared": None,
    },
    {
        "case_id": "Arroyo Hondo Pueblo -- 'What Makes a Dog?'",
        "n": 7,
        "n_sequential": 0,
        "tissue": "bone_collagen",
        "observation": "values similarly varied but not in ways one might "
                       "expect; all seven canids from domestic contexts; one "
                       "specimen genetically Canis latrans with isotope "
                       "values in the domestic dog range",
        "standing_explanation": "isotopes reflect variability in human-canid "
                                "relationships, which do not track genetics",
        "also_fits": ["VARIABLE_COUPLING"],
        "tested_against_each_other": False,
        "same_site_wild_control": True,
        "amplitude_permil": None,
        "geometry_declared": None,
    },
    {
        "case_id": "Canine Surrogacy Approach -- Hudson Bay Thule",
        "n": None,
        "n_sequential": 0,
        "tissue": "bone_collagen",
        "observation": "dogs isotopically similar to humans, but mixing "
                       "models put them on a different intake -- a "
                       "systematic offset",
        "standing_explanation": "absorbed as CSA method caution; the "
                                "approach assumes dogs ate what humans ate, "
                                "i.e. that the coupling is fixed",
        "also_fits": ["VARIABLE_COUPLING"],
        "tested_against_each_other": False,
        "same_site_wild_control": False,
        "amplitude_permil": None,
        "geometry_declared": None,
    },
    {
        "case_id": "Vinca-Belo brdo -- cattle intra-tooth (PLOS One)",
        "n": None,
        "n_sequential": None,
        "tissue": "sequential_enamel",
        "observation": "intra-tooth amplitude 0.7 to 2.4 permil within one "
                       "herd -- some individuals nearly flat, others with "
                       "roughly 3x the range",
        "standing_explanation": "husbandry variation within the herd",
        "also_fits": ["VARIABLE_COUPLING"],
        "tested_against_each_other": False,
        "same_site_wild_control": False,
        "amplitude_permil": 2.4,
        "geometry_declared": "as published; increment width not restated in "
                             "the delivered summary",
    },
    {
        "case_id": "Schipluiden -- cattle vs red deer and suids, same site",
        "n": None,
        "n_sequential": None,
        "tissue": "sequential_enamel",
        "observation": "d13C lower than expected in some cattle, NOT in red "
                       "deer or suids from the same site",
        "standing_explanation": "leafy fodder rather than grazing",
        "also_fits": ["VARIABLE_COUPLING"],
        "tested_against_each_other": False,
        "same_site_wild_control": True,
        "amplitude_permil": None,
        "geometry_declared": "as published; not restated in the delivered "
                             "summary",
    },
]


def score_case(c):
    sep = separable(c["tissue"])
    return {
        "case_id": c["case_id"],
        "tissue": c["tissue"],
        "separates_variable_coupling": sep["separates_variable_coupling"],
        "state": sep["state"],
        "standing_explanation": c["standing_explanation"],
        "also_fits": list(c["also_fits"]),
        "tested_against_each_other": c["tested_against_each_other"],
        "same_site_wild_control": c["same_site_wild_control"],
    }


def corpus_readout():
    """The computable findings, such as they are on four delivered cases."""
    scored = [score_case(c) for c in CASES]
    blind = [s for s in scored if not s["separates_variable_coupling"]]
    untested = [s for s in scored if not s["tested_against_each_other"]]
    controls = [s for s in scored if s["same_site_wild_control"]]
    seq_n = sum(c["n_sequential"] or 0 for c in CASES if c["tissue"]
                == "bone_collagen")
    bone_n = sum(c["n"] or 0 for c in CASES if c["tissue"] == "bone_collagen")
    # The delivered text reads "n=35 dogs, plus dentine n=4", which is
    # ambiguous: the four may be a SUBSET of the thirty-five or ADDITIONAL to
    # them. Both denominators are reported rather than one being chosen,
    # because a share computed on an ambiguous denominator is the failure this
    # folder audits for. The two readings differ by less than a percentage
    # point, so the conclusion does not turn on it -- which is worth saying,
    # since it is why the ambiguity can be left open instead of resolved.
    return {
        "cases": len(scored),
        "blind_by_tissue": len(blind),
        "hypotheses_never_tested_against_each_other": len(untested),
        "cases_with_same_site_wild_control": len(controls),
        "canid_bone_collagen_individuals": bone_n,
        "canid_sequential_individuals": seq_n,
        "share_if_subset": seq_n / bone_n if bone_n else None,
        "share_if_additional": seq_n / (bone_n + seq_n) if (bone_n + seq_n)
        else None,
        "denominator_state": "AMBIGUOUS_IN_DELIVERED_TEXT",
    }


# --- the field replacement -------------------------------------------------

def coupling_field_for(case):
    """For archaeological cases, amplitude REPLACES the boolean.

    audit.py records coupling_machinery_present as Y/N, which is the right
    field for a published model: a model either carries a coupling term or it
    does not. For an archaeological case the question is different -- the
    coupling is a property of the animal's intake, not of a document -- and
    intra-tooth amplitude measures it directly. So the boolean is not
    supplemented here, it is replaced, per OPEN.md item 9.

    The replacement has a hard scope. It requires an incremental tissue AND a
    declared geometry, and returns an explicit non-value otherwise, so
    "cannot be measured in this evidence" and "measured and flat" never share
    a value. There is no tooth in a national carbon inventory; entries.py
    keeps the boolean, and that is a scope limit rather than an inconsistency.
    """
    if not TISSUES[case["tissue"]]["sequential"]:
        return {"field": "amplitude", "value": None,
                "state": "NOT_APPLICABLE_TISSUE",
                "why": "amplitude requires an incremental tissue. bone "
                       "collagen returns one value per individual, and one "
                       "value has no amplitude"}
    if not case.get("geometry_declared"):
        return {"field": "amplitude", "value": None,
                "state": "GEOMETRY_NOT_DECLARED",
                "why": "amplitude is partly a protocol artifact; without a "
                       "stated sampling geometry it is not comparable"}
    try:
        r = amplitude_reading(case["amplitude_permil"],
                              geometry=case["geometry_declared"])
    except GeometryNotDeclared:
        return {"field": "amplitude", "value": None,
                "state": "GEOMETRY_NOT_DECLARED", "why": "see above"}
    return {"field": "amplitude", "value": r["amplitude_permil"],
            "state": r["reading"], "why": r["why"]}


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


def resolution_report():
    L = []
    A = L.append
    A("WHICH TISSUE CAN ASK THE QUESTION")
    A("=" * 72)
    A("")
    A("  G-RES pairing: instrument averaging x margin (%.1f) must not exceed"
      % G_RES_MARGIN)
    A("  the feature being resolved -- one season, %.0f days."
      % SEASONAL_SWITCH_DAYS)
    A("")
    A("  %-22s %-9s %-9s %-6s %s"
      % ("tissue", "averages", "x margin", "seq", "resolves"))
    for t in TISSUES:
        r = resolves(t)
        A("  %-22s %-9s %-9s %-6s %s"
          % (t, "%.0f d" % r["averaging_days"],
             "%.0f d" % r["instrument_times_margin"],
             "yes" if r["sequential"] else "no",
             "yes" if r["resolves"] else "NO, %.1fx too coarse"
             % r["shortfall_factor"]))
    A("")
    for t in TISSUES:
        s = separable(t)
        A("  %-22s %s" % (t, s["state"]))
        L.extend(_wrap(s["why"], "    "))
        A("")
    A("-" * 72)
    A("")
    A("  THE THREE SIGNATURES")
    A("")
    A("  %-18s %-8s %-8s %-8s %s"
      % ("hypothesis", "within", "between", "Sr", "seasonal"))
    for h in HYPOTHESES:
        s = SIGNATURES[h]
        A("  %-18s %-8s %-8s %-8s %s"
          % (h,
             "yes" if s["within_individual_spread"] else "no",
             "yes" if s["between_individual_spread"] else "no",
             "yes" if s["covaries_with_strontium"] else "no",
             "yes" if s["phased_to_season"] else "no"))
    A("")
    A("  The `within` column is the only one that separates")
    A("  VARIABLE_COUPLING from the other two, and it is exactly the column")
    A("  a years-averaging tissue removes. In bone collagen the coupling")
    A("  hypothesis cannot fail -- which is not support for it. It is")
    A("  CONSTANT_SILENT, in the null-harness sense, by construction.")
    return "\n".join(L)


def case_report():
    L = []
    A = L.append
    A("THE DELIVERED CASES")
    A("=" * 72)
    A("")
    A("  MODEL_SEEDED throughout. One search pass, not independently")
    A("  verified here, and no isotope value computed here.")
    A("")
    for c in CASES:
        s = score_case(c)
        A("  %s" % c["case_id"])
        A("    tissue                 %s" % c["tissue"])
        A("    n / sequential n       %s / %s"
          % (c["n"] if c["n"] is not None else "--",
             c["n_sequential"] if c["n_sequential"] is not None else "--"))
        A("    observation")
        L.extend(_wrap(c["observation"], "      "))
        A("    standing explanation")
        L.extend(_wrap(c["standing_explanation"], "      "))
        A("    also fits              %s" % ", ".join(c["also_fits"]))
        A("    tested against each other  %s"
          % ("yes" if c["tested_against_each_other"] else "NO"))
        A("    same-site wild control %s"
          % ("yes" if c["same_site_wild_control"] else "no"))
        A("    coupling separable     %s" % s["state"])
        A("")
    r = corpus_readout()
    A("-" * 72)
    A("")
    A("  READOUT ON %d DELIVERED CASES -- four cases, not a survey"
      % r["cases"])
    A("")
    A("    blind by tissue                          %d of %d"
      % (r["blind_by_tissue"], r["cases"]))
    A("    hypotheses never tested against each other  %d of %d"
      % (r["hypotheses_never_tested_against_each_other"], r["cases"]))
    A("    cases with a same-site wild control       %d of %d"
      % (r["cases_with_same_site_wild_control"], r["cases"]))
    A("")
    A("    canid individuals, bone collagen         %d"
      % r["canid_bone_collagen_individuals"])
    A("    canid individuals, sequential dentine    %d"
      % r["canid_sequential_individuals"])
    A("    share that can ask it, if a subset       %.1f%%"
      % (100.0 * r["share_if_subset"]))
    A("    share that can ask it, if additional     %.1f%%"
      % (100.0 * r["share_if_additional"]))
    A("    denominator                              %s"
      % r["denominator_state"])
    L.extend(_wrap(
        "The delivered text reads 'n=35 dogs, plus dentine n=4', which "
        "reads either way. Both denominators are reported rather than one "
        "being picked -- a share on an ambiguous denominator is the failure "
        "this folder audits for. Here the two readings differ by less than "
        "a percentage point, which is why the ambiguity can be left open "
        "instead of resolved.",
        "    "))
    A("")
    L.extend(_wrap(
        "So on the delivered dog corpus the discriminating axis exists for "
        "roughly a tenth of the individuals. Every standing explanation "
        "above is compatible with the coupling hypothesis and none was "
        "tested against it -- not because anyone declined to, but because "
        "the tissue carrying most of the data cannot hold the difference.",
        "    "))
    A("")
    L.extend(_wrap(
        "THE CHEAPEST NEXT STEP, and it is already a working design "
        "elsewhere: Schipluiden sampled WILD animals from the SAME SITE as "
        "a baseline -- domesticates deviate, red deer and suids do not, so "
        "the deviation is attributable to household provisioning rather "
        "than to environment. That is a control, in the null-harness "
        "sense. Nobody has pointed it at dogs with a wild-canid control at "
        "the same site. Arroyo Hondo stumbled into one accidentally when a "
        "coyote came back with domestic-dog values, and read it as "
        "evidence that relationships do not track genetics -- which is the "
        "same finding from the other side.",
        "    "))
    return "\n".join(L)


def amplitude_report():
    L = []
    A = L.append
    A("COUPLING STRENGTH AS A NUMBER")
    A("=" * 72)
    A("")
    A("  CALIBRATION -- the positive control exists, for other species")
    A("    %s" % CALIBRATION["study"])
    A("    known: %s" % CALIBRATION["what_was_known"])
    L.extend(_wrap(CALIBRATION["why_it_matters"], "    "))
    A("")
    L.extend(_wrap(
        "Intra-tooth amplitude is a coupling-variability measurement: flat "
        "means a fixed draw, high amplitude means supply-coupled. That "
        "turns audit.py's coupling field from Y/N into a quantity for "
        "archaeological cases -- the first unit this audit has.",
        "  "))
    A("")
    A("  %-12s %s" % ("permil", "reading"))
    for v in (0.5, 0.7, 1.5, 2.4, 3.0):
        r = amplitude_reading(v, geometry="illustrative")
        A("  %-12s %s" % ("%.1f" % v, r["reading"]))
    A("")
    A("  NOT_MEASURED is a separate value from FLAT_FIXED_DRAW. A flat")
    A("  series is a measurement; no series is not.")
    A("")
    A("  THE CAVEAT IS ENFORCED, NOT NOTED.")
    L.extend(_wrap(
        "A 2024 Journal of Archaeological Science paper finds that dentine sample geometry changes the intra-tooth pattern, so "
        "amplitude is partly a methods artifact and a cross-study "
        "comparison that does not state geometry is comparing two "
        "instruments. amplitude_reading() raises GeometryNotDeclared "
        "without one. Same shape as audit.py refusing coupling machinery "
        "that is not named in the model's own vocabulary: a number from an "
        "unnamed instrument is not yet a reading.",
        "    "))
    A("")
    A("  THE FIELD REPLACEMENT, per OPEN.md item 9")
    L.extend(_wrap(
        "For archaeological cases amplitude REPLACES audit.py's boolean "
        "coupling_machinery_present rather than sitting beside it: the "
        "coupling there is a property of an animal's intake, not of a "
        "document. The scope is hard -- it needs an incremental tissue AND "
        "a declared geometry, and returns an explicit non-value otherwise, "
        "so 'cannot be measured in this evidence' and 'measured and flat' "
        "never share a value. There is no tooth in a national carbon "
        "inventory, so entries.py keeps the boolean. That is a scope limit, "
        "not an inconsistency.",
        "    "))
    A("")
    for c in CASES:
        L.extend(_wrap(c["case_id"], "    "))
        A("      -> %s" % coupling_field_for(c)["state"])
    A("")
    A("  THE THRESHOLDS ARE CONVENTIONAL. They are scaled against the")
    A("  delivered Vinca-Belo brdo range (0.7-2.4 permil within one herd)")
    A("  and are not calibrated against a controlled feeding experiment")
    A("  here. The delivered material names one that exists -- Balasse et")
    A("  al., a known C3->C4 switch plus weaning, both recovered from")
    A("  intra-tooth variation -- which is where a real calibration would")
    A("  come from.")
    A("")
    A("-" * 72)
    A("")
    x = cross_species_readout()
    A("  CROSS-SPECIES EXTENSION -- %s" % x["claim_status"])
    A("")
    L.extend(_wrap(
        "The same coupling is predicted for chickens, cattle, yak and "
        "buffalo: the household draw tracks surplus while protection is "
        "held constant through the switch. In species with a commodity "
        "output the switching is already measured seasonally per "
        "individual, because nobody had to argue about whether the animal "
        "counted.",
        "    "))
    A("")
    A("    published applications of the method       %d"
      % x["published_applications"])
    A("      on commodity species                     %d"
      % x["on_commodity_species"])
    A("      on companion species                     %d"
      % x["on_companion_species"])
    A("    dog individuals sampled sequentially       %d"
      % x["dog_sequential_individuals"])
    A("")
    L.extend(_wrap(
        "The count is consistent with the stated claim and does NOT "
        "establish it. A correlation between commodity status and "
        "measurement maturity has other live explanations -- sample "
        "availability, tooth size and enamel thickness, which "
        "agricultural-research funding lines exist. What the count does "
        "show is that the asymmetry is real and large, which is the part "
        "that was in question.",
        "    "))
    A("")
    L.extend(_wrap(
        "This is the same gate as the FAO LEAP / GLEAM entry in entries.py, "
        "seen from the other side. There the gate is `market_output` and it "
        "keeps companion animals out of the water accounting. Here the same "
        "line is why the measurement exists at all for cattle. One "
        "criterion, two consequences: the animal that sells gets both the "
        "ledger entry and the instrument.",
        "    "))
    return "\n".join(L)


def report():
    return "\n\n".join([resolution_report(), "", case_report(), "",
                        amplitude_report()])


# --- selftest --------------------------------------------------------------

def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("bone collagen cannot resolve a seasonal switch",
       resolves("bone_collagen")["resolves"] is False)
    ck("incremental dentine can",
       resolves("incremental_dentine")["resolves"] is True)
    ck("sequential enamel can",
       resolves("sequential_enamel")["resolves"] is True)
    ck("the shortfall is reported as a factor, not just a bool",
       resolves("bone_collagen")["shortfall_factor"] > 1.0)
    ck("an unknown tissue raises rather than defaulting",
       _raises(lambda: resolves("guesswork"), KeyError))

    ck("coupling is UNASKABLE in bone collagen, not refuted",
       separable("bone_collagen")["state"] == "UNASKABLE_IN_THIS_TISSUE")
    ck("coupling is SEPARABLE in a sequential tissue",
       separable("incremental_dentine")["state"] == "SEPARABLE")
    ck("both states occur, so the check is not constant",
       len({separable(t)["state"] for t in TISSUES}) == 2)

    within = {h: SIGNATURES[h]["within_individual_spread"] for h in HYPOTHESES}
    ck("the within-individual axis separates VARIABLE_COUPLING from both "
       "others -- one yes, two no",
       sum(1 for v in within.values() if v) == 1
       and within["VARIABLE_COUPLING"] is True)
    ck("the between-individual axis separates nothing, which is why the "
       "spread reads as breed or mobility",
       all(SIGNATURES[h]["between_individual_spread"] for h in HYPOTHESES))
    ck("strontium separates MOBILITY from the other two",
       sum(1 for h in HYPOTHESES
           if SIGNATURES[h]["covaries_with_strontium"]) == 1)

    ck("amplitude refuses without declared geometry",
       _raises(lambda: amplitude_reading(2.4), GeometryNotDeclared))
    ck("amplitude reads with geometry",
       amplitude_reading(2.4, geometry="g")["reading"]
       == "HIGH_SUPPLY_COUPLED")
    ck("a flat series reads FLAT_FIXED_DRAW",
       amplitude_reading(0.5, geometry="g")["reading"] == "FLAT_FIXED_DRAW")
    ck("no series is NOT_MEASURED, which is not the same as flat",
       amplitude_reading(None, geometry="g")["reading"] == "NOT_MEASURED")
    ck("a negative amplitude raises",
       _raises(lambda: amplitude_reading(-1.0, geometry="g"), ValueError))

    r = corpus_readout()
    ck("five delivered cases", r["cases"] == 5)
    ck("three of five delivered cases are blind by tissue",
       r["blind_by_tissue"] == 3)
    ck("no delivered case tested the hypotheses against each other",
       r["hypotheses_never_tested_against_each_other"] == r["cases"])
    ck("two delivered cases carry a same-site wild control",
       r["cases_with_same_site_wild_control"] == 2)
    ck("both readings of the ambiguous denominator are reported, and "
       "neither is picked",
       r["denominator_state"] == "AMBIGUOUS_IN_DELIVERED_TEXT"
       and r["share_if_subset"] is not None
       and r["share_if_additional"] is not None)
    ck("the two readings differ by less than a percentage point, so the "
       "conclusion does not turn on the ambiguity",
       abs(r["share_if_subset"] - r["share_if_additional"]) < 0.01)
    ck("the sequential share is small but not zero under either reading",
       0.0 < r["share_if_additional"] <= r["share_if_subset"] < 0.2)
    ck("every case records that the coupling hypothesis also fits, which is "
       "the point -- two hypotheses fitting one observation is not agreement",
       all("VARIABLE_COUPLING" in c["also_fits"] for c in CASES))

    x = cross_species_readout()
    ck("every published application of the method is on a commodity species",
       x["on_commodity_species"] == x["published_applications"]
       and x["on_companion_species"] == 0)
    ck("the asymmetry against dog sequential n is large",
       x["published_applications"] > x["dog_sequential_individuals"])
    ck("the cross-species claim is marked stated-and-untested, not adopted",
       x["claim_status"] == "STATED_BY_AUTHOR_UNTESTED")
    ck("the readout separates what the count shows from what it does not",
       x["count_establishes"] != x["count_does_not_establish"])

    bone_case = [c for c in CASES if c["tissue"] == "bone_collagen"][0]
    ck("amplitude is NOT_APPLICABLE_TISSUE on a bone-collagen case, not "
       "False and not zero",
       coupling_field_for(bone_case)["state"] == "NOT_APPLICABLE_TISSUE")
    seq_no_geo = dict(CASES[0])
    seq_no_geo.update({"tissue": "incremental_dentine",
                       "geometry_declared": None, "amplitude_permil": 2.0})
    ck("amplitude refuses a sequential case with no declared geometry",
       coupling_field_for(seq_no_geo)["state"] == "GEOMETRY_NOT_DECLARED")
    vinca = [c for c in CASES if "Vinca" in c["case_id"]][0]
    ck("the one case with an amplitude and a geometry reads as coupled",
       coupling_field_for(vinca)["state"] == "HIGH_SUPPLY_COUPLED")
    ck("a sequential case with a geometry but no amplitude reads "
       "NOT_MEASURED, distinct from flat",
       coupling_field_for(
           [c for c in CASES if "Schipluiden" in c["case_id"]][0])["state"]
       == "NOT_MEASURED")
    ck("the replacement returns four distinct states across the corpus and "
       "the constructed case, so it is not one value repeated",
       len({coupling_field_for(c)["state"] for c in CASES}
           | {coupling_field_for(seq_no_geo)["state"]}) == 4)

    ck("the calibration is a positive control and is recorded as existing "
       "for caprines and cattle, not for dogs",
       CALIBRATION["recovered_from_intra_tooth_variation"] is True
       and "not for dogs" in CALIBRATION["why_it_matters"])

    ck("report renders", "UNASKABLE_IN_THIS_TISSUE" in report())
    ck("report carries the cross-species readout",
       "STATED_BY_AUTHOR_UNTESTED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


def main():
    ap = argparse.ArgumentParser(description="provisioning discriminator")
    ap.add_argument("--resolution", action="store_true")
    ap.add_argument("--cases", action="store_true")
    ap.add_argument("--amplitude", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.resolution:
        print(resolution_report())
    elif a.cases:
        print(case_report())
    elif a.amplitude:
        print(amplitude_report())
    else:
        print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
