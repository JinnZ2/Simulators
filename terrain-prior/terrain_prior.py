"""terrain_prior.py -- observed indicator to substrate prior.

Built to WORK_ORDER.md, landed verbatim beside this file.

WHAT THIS IS

An indicator -- a plant, a landform, a piece of flow evidence -- is a record
of the process that produced the site.  This module reads that record and
returns what must have been true for the indicator to be there, as a PRIOR
with a stated mechanism, a stated confidence, a stated scope, and a stated
falsifier.

WHAT THIS IS NOT

It does not plan routes.  It does not rate terrain.  There is no
traversability number anywhere in this file and there cannot be one: the two
output variables are reported separately on two vocabularies that do not
compare, and nothing sums, averages, ranks or orders them against each other.

It is not a species lookup table.  Every entry carries a mechanism, because
the mechanism is what transfers to a region whose species list is different.
An entry without one is UNRATED and generates no prior at all.

PRIOR VERSUS RATING -- the distinction the hard constraints force

    "No terrain rating independent of a morphology profile."

A PRIOR is a statement about the ground and the process that made it.  It is
returned whether or not a morphology was supplied, because it is not a rating.
A VERDICT -- does this platform's contact pressure exceed what this ground
will bear -- is the rating, and it is produced only inside by_morphology, only
when a morphology profile is supplied.  With no morphology the return carries
priors and an empty by_morphology, never a verdict.

CHOICES

Every decision the order leaves open is numbered, printed by --choices, and
cited inline at the site where it takes effect.

LIMITS STATED AT THE TOP, NOT THE BOTTOM

* resolve_entry matches on words.  It is a word list, and a word list deciding
  which derivation applies is the failure mode this repository records as
  T1-1.  The LANDFORM path is context-driven and does not have this problem;
  the VEGETATION path is entered by name and does.  Two intake paths with
  different epistemic standing under one stated rule.
* No pressure threshold in kPa appears anywhere in this file.  The order
  states none, so none is invented: bearing classes and platform pressure
  classes are DECLARED ordinals, and a declared reading is marked as one.
* Nothing here has been checked against a site.
"""

import sys

# ---------------------------------------------------------------------------
# vocabularies
# ---------------------------------------------------------------------------

INDICATOR_TYPES = ("VEGETATION", "LANDFORM", "FLOW_EVIDENCE",
                   "SUBSTRATE_VISIBLE")

POSITIONS = ("UPSTREAM", "DOWNSTREAM", "LATERAL", "NONE", "UNKNOWN")

RECOVERY = ("PASSIVE", "ACTIVE", "NONE")

CONFIDENCE = ("HIGH", "MEDIUM", "LOW", "NOT_STATED")

# [CHOICE 1] the order states bearing as free text ("LOW, and lower than the
# surface mat suggests").  Validation case C requires two morphologies to
# return results that differ in DIRECTION, and a direction comparison needs an
# ordinal.  So an entry carries BOTH: the order's sentence verbatim as value,
# and a declared ordinal class beside it.  The sentence is never parsed.
BEARING_CLASSES = ("VERY_LOW", "LOW", "MODERATE", "HIGH", "NOT_STATED")
ENTANGLEMENT_CLASSES = ("LOW", "MODERATE", "HIGH", "NOT_STATED")

# [CHOICE 2] a platform's pressure is DECLARED as a class on the morphology
# profile and is never derived from contact_pressure or contact_area.  Deriving
# it would require kPa thresholds the order does not supply, and an invented
# threshold would put a number nobody measured inside a bearing verdict.
PRESSURE_CLASSES = ("LOW", "MODERATE", "HIGH")
SUSCEPTIBILITY_CLASSES = ("LOW", "MODERATE", "HIGH")

# [CHOICE 3] the order names the P2 class -- "the standard sensor suite will
# rate this BETTER than it is" -- and names no field.  sensor_invert is a
# declared four-value field; UNKNOWN is kept apart from NONE, because "nobody
# recorded which way the sensors read this" is not "the sensors read it right".
INVERT_DIRECTIONS = ("OPTIMISTIC", "PESSIMISTIC", "NONE", "UNKNOWN")

# [CHOICE 9] how a class got onto an entry: quoted from the order, or read
# into a class by whoever wrote the entry.  Recorded per axis so a class the
# order states and a class somebody read into the order never merge.
CLASS_BASIS = ("ORDER_STATED", "DECLARED_READING", "NOT_STATED")

CHECK_CODES = ("P1_TWO_LAYER", "P2_SENSOR_INVERT", "P3_MORPH_SPLIT",
               "P4_OUT_OF_SCOPE", "P5_NO_MECHANISM")

# bearing verdict vocabulary
WITHIN = "WITHIN"
EXCEEDS = "EXCEEDS"
VERDICT_NOT_EVALUABLE = "NOT_EVALUABLE"

# entanglement verdict vocabulary -- deliberately a DIFFERENT vocabulary, so
# no caller can put a bearing verdict and an entanglement verdict on one axis.
CLEARS = "CLEARS"
BINDS = "BINDS"

# why no prior was returned
NO_ENTRY = "NO_ENTRY"
UNRATED_NO_MECHANISM = "UNRATED_NO_MECHANISM"
NO_CONTEXT_BRANCH = "NO_CONTEXT_BRANCH"
INTAKE_INCOMPLETE = "INTAKE_INCOMPLETE"
NO_PRIOR_REASONS = (NO_ENTRY, UNRATED_NO_MECHANISM, NO_CONTEXT_BRANCH,
                    INTAKE_INCOMPLETE)

# [CHOICE 5] region is a scope field.  Three states, because "observed outside
# the entry's stated scope" and "nobody wrote down where this was observed"
# are different findings and only the first is P4.
REGION_IN_SCOPE = "IN_SCOPE"
REGION_OUT_OF_SCOPE = "OUT_OF_SCOPE"
REGION_UNSTATED = "REGION_UNSTATED"
REGION_STATES = (REGION_IN_SCOPE, REGION_OUT_OF_SCOPE, REGION_UNSTATED)

# which platform pressure classes a given bearing class will carry.
SUPPORTS = {
    "VERY_LOW": (),
    "LOW": ("LOW",),
    "MODERATE": ("LOW", "MODERATE"),
    "HIGH": ("LOW", "MODERATE", "HIGH"),
}

# which platform susceptibilities a given entanglement class lets through.
TOLERATES = {
    "LOW": ("LOW", "MODERATE", "HIGH"),
    "MODERATE": ("LOW", "MODERATE"),
    "HIGH": ("LOW",),
}

# the morphology fields any check in this module reads.  The order specifies
# eight; two are read.  See morphology_fields_reaching_a_check().
MORPHOLOGY_FIELDS_READ = ("pressure_class", "entanglement_susceptibility")

MORPHOLOGY_FIELDS_ORDER = ("platform_id", "contact_area", "contact_pressure",
                           "n_contacts", "swing_profile", "joint_exposure",
                           "ankle_to_foot_ratio",
                           "recovery_from_entanglement")

CHOICES = {
    1: "bearing and entanglement carry a declared ordinal class beside the "
       "order's verbatim sentence; the sentence is never parsed",
    2: "platform pressure class is declared on the morphology profile and "
       "never derived from contact_pressure or contact_area",
    3: "sensor_invert is a declared four-value entry field; UNKNOWN is kept "
       "apart from NONE",
    4: "context_branches let one entry carry a prior that only holds under a "
       "stated context; the order's entry schema has no field for it and its "
       "own validation target needs one",
    5: "region_state has three values; REGION_UNSTATED is not P4",
    6: "resolve_entry matches normalised words against entry indicator and "
       "aliases, longest match wins, and does not read region",
    7: "by_morphology is added to the return; the order's return block has "
       "one bearing_prior and its hard constraints require a verdict per "
       "morphology",
    8: "P5 returns early with no prior on either axis, not a prior carrying "
       "a flag",
    9: "class_basis is recorded per axis so a class quoted from the order is "
       "distinguishable from one read into a class here",
    10: "the boulder deposition zone is entered at VERY_LOW, from the order's "
        "derivation text 'Bearing is absent', not at LOW from its validation "
        "case; the two rungs disagree for a low-pressure platform and "
        "boulder_rung_divergence() computes the disagreement",
}


# ---------------------------------------------------------------------------
# intake
# ---------------------------------------------------------------------------

def normalize(text):
    """Lowercase word tokens.  No stemming, no synonyms, no inference."""
    out = []
    word = []
    for ch in str(text).lower():
        if ch.isalnum():
            word.append(ch)
        elif word:
            out.append("".join(word))
            word = []
    if word:
        out.append("".join(word))
    return out


def validate_observation(observation):
    """Return (missing, invalid).  Nothing is guessed and nothing defaulted."""
    missing = []
    invalid = []
    for field in ("obs_id", "indicator_type", "indicator", "region",
                  "observer_baseline"):
        if field not in observation:
            missing.append(field)
    if "indicator_type" in observation:
        if observation["indicator_type"] not in INDICATOR_TYPES:
            invalid.append("indicator_type")
    context = observation.get("context", {})
    if not isinstance(context, dict):
        invalid.append("context")
        context = {}
    pos = context.get("position_relative_to_obstruction")
    if pos is not None and pos not in POSITIONS:
        invalid.append("context.position_relative_to_obstruction")
    fdk = context.get("flow_direction_known")
    if fdk is not None and not isinstance(fdk, bool):
        invalid.append("context.flow_direction_known")
    return missing, invalid


def validate_entry(entry):
    """Return (missing, invalid) for a derivation entry."""
    missing = []
    invalid = []
    for field in ("entry_id", "indicator"):
        if field not in entry:
            missing.append(field)
    if entry.get("confidence", "NOT_STATED") not in CONFIDENCE:
        invalid.append("confidence")
    if entry.get("bearing_class", "NOT_STATED") not in BEARING_CLASSES:
        invalid.append("bearing_class")
    if entry.get("entanglement_class", "NOT_STATED") not in \
            ENTANGLEMENT_CLASSES:
        invalid.append("entanglement_class")
    if entry.get("sensor_invert", "UNKNOWN") not in INVERT_DIRECTIONS:
        invalid.append("sensor_invert")
    for field in ("bearing_class_basis", "entanglement_class_basis"):
        if entry.get(field, "NOT_STATED") not in CLASS_BASIS:
            invalid.append(field)
    return missing, invalid


def validate_morphology(morphology):
    """Return (missing, invalid) for a morphology profile."""
    missing = []
    invalid = []
    if "platform_id" not in morphology:
        missing.append("platform_id")
    # [CHOICE 2] both are required and neither is computed from the order's
    # numeric fields.
    for field in ("pressure_class", "entanglement_susceptibility"):
        if field not in morphology:
            missing.append(field)
    if morphology.get("pressure_class") is not None and \
            morphology.get("pressure_class") not in PRESSURE_CLASSES:
        invalid.append("pressure_class")
    if morphology.get("entanglement_susceptibility") is not None and \
            morphology.get("entanglement_susceptibility") not in \
            SUSCEPTIBILITY_CLASSES:
        invalid.append("entanglement_susceptibility")
    rec = morphology.get("recovery_from_entanglement")
    if rec is not None and rec not in RECOVERY:
        invalid.append("recovery_from_entanglement")
    return missing, invalid


def has_mechanism(entry):
    """A mechanism is a non-empty string.  Nothing else counts as one."""
    mech = entry.get("mechanism")
    return isinstance(mech, str) and mech.strip() != ""


# ---------------------------------------------------------------------------
# resolution
# ---------------------------------------------------------------------------

def resolve_entry(observation, entries):
    """Pick the derivation entry for an observation, or None.

    [CHOICE 6] matching is on normalised words: an entry matches when every
    word of its indicator -- or of one of its aliases -- appears among the
    observation's words.  Longest match wins; a tie returns None rather than
    picking one.

    REGION IS NOT READ HERE.  That is the hard constraint "region is a scope
    field, never a lookup key", and it is the one thing in this function that
    is a design decision rather than a convenience.  The cost is stated in the
    module docstring: what is left to enter a VEGETATION derivation by is the
    indicator's NAME, which is a word list, and a word list is exactly what
    fails in a region whose species list differs.  The LANDFORM path does not
    have this problem because its entry is reached through context (flow
    direction plus an obstruction), not through a name.
    """
    words = set(normalize(observation.get("indicator", "")))
    itype = observation.get("indicator_type")
    best = []
    best_len = 0
    for entry in entries:
        if entry.get("indicator_type") is not None and \
                entry.get("indicator_type") != itype:
            continue
        candidates = [entry.get("indicator", "")]
        candidates.extend(entry.get("aliases", ()))
        for candidate in candidates:
            toks = normalize(candidate)
            if not toks:
                continue
            if set(toks) <= words:
                if len(toks) > best_len:
                    best = [entry]
                    best_len = len(toks)
                elif len(toks) == best_len and entry not in best:
                    best.append(entry)
                break
    if len(best) == 1:
        return best[0]
    return None


def region_state(observation, entry):
    """[CHOICE 5] three states.  scope_regions is declared on the entry."""
    region = observation.get("region")
    if region is None or str(region).strip() == "":
        return REGION_UNSTATED
    scope_regions = entry.get("scope_regions")
    if not scope_regions:
        return REGION_UNSTATED
    if region in scope_regions:
        return REGION_IN_SCOPE
    return REGION_OUT_OF_SCOPE


def context_branch(observation, entry):
    """Return (branch_or_None, reason).

    [CHOICE 4] the order's own validation target -- the deposition zone behind
    a boulder -- is not a property of the indicator.  A boulder upstream side
    is scoured; the downstream side is fines.  The prior is DIFFERENT on the
    two sides and the entry schema in the order has one implies_bearing field
    and no place to say so.  So an entry may carry context_branches, each with
    a "when" dict of context keys that must all match, and each supplying its
    own bearing/entanglement fields.

    An entry with branches and no matching branch produces NO prior.  Falling
    back to an unconditioned reading would return the scoured-side answer for
    the deposition side, which is the error the case exists to catch.
    """
    branches = entry.get("context_branches")
    if not branches:
        return None, None
    context = observation.get("context", {}) or {}
    for branch in branches:
        when = branch.get("when", {})
        if all(context.get(k) == v for k, v in when.items()):
            return branch, None
    return None, NO_CONTEXT_BRANCH


def _axis(entry, branch, prefix):
    """Read one axis off the branch if it supplies it, else off the entry."""
    source = branch if (branch is not None and
                        (prefix + "_class") in branch) else entry
    return {
        "value": source.get("implies_" + prefix, ""),
        "class": source.get(prefix + "_class", "NOT_STATED"),
        "class_basis": source.get(prefix + "_class_basis", "NOT_STATED"),
        "confidence": source.get("confidence",
                                 entry.get("confidence", "NOT_STATED")),
        "mechanism": entry.get("mechanism", ""),
    }


# ---------------------------------------------------------------------------
# verdicts -- the rating layer, morphology-relative by construction
# ---------------------------------------------------------------------------

def bearing_verdict(bearing_class, pressure_class):
    """WITHIN / EXCEEDS / NOT_EVALUABLE.  Reads no entanglement quantity."""
    if bearing_class == "NOT_STATED" or bearing_class not in SUPPORTS:
        return VERDICT_NOT_EVALUABLE
    if pressure_class not in PRESSURE_CLASSES:
        return VERDICT_NOT_EVALUABLE
    return WITHIN if pressure_class in SUPPORTS[bearing_class] else EXCEEDS


def entanglement_verdict(entanglement_class, susceptibility):
    """CLEARS / BINDS / NOT_EVALUABLE.  Reads no bearing quantity.

    Separate function, separate vocabulary, separate table.  The two verdicts
    are not comparable and nothing in this module puts them on one scale.
    """
    if entanglement_class == "NOT_STATED" or entanglement_class not in \
            TOLERATES:
        return VERDICT_NOT_EVALUABLE
    if susceptibility not in SUSCEPTIBILITY_CLASSES:
        return VERDICT_NOT_EVALUABLE
    return CLEARS if susceptibility in TOLERATES[entanglement_class] else BINDS


# ---------------------------------------------------------------------------
# the read
# ---------------------------------------------------------------------------

def _empty(observation, reason, missing=None, invalid=None, entry_id=None):
    return {
        "obs_id": observation.get("obs_id"),
        "entry_id": entry_id,
        "bearing_prior": None,
        "entanglement_prior": None,
        "by_morphology": [],
        "flags": [],
        "scope": None,
        "region_state": None,
        "derived_from": None,
        "observer_baseline": observation.get("observer_baseline"),
        "falsified_by": None,
        "no_prior_reason": reason,
        "intake_missing": missing or [],
        "intake_invalid": invalid or [],
    }


def read(observation, entries, morphologies=()):
    """Observation plus derivation set plus zero or more morphologies.

    Returns priors (statements about the ground) always, and verdicts (ratings)
    only per supplied morphology.
    """
    missing, invalid = validate_observation(observation)
    if missing or invalid:
        return _empty(observation, INTAKE_INCOMPLETE, missing, invalid)

    entry = resolve_entry(observation, entries)
    if entry is None:
        return _empty(observation, NO_ENTRY)

    # [CHOICE 8] P5 first, and it returns before any prior is built.  "Entry is
    # UNRATED and must not generate a prior" is not satisfied by a prior with a
    # flag on it: a caller reading bearing_prior["value"] would still act on a
    # correlation with no mechanism.
    if not has_mechanism(entry):
        out = _empty(observation, UNRATED_NO_MECHANISM,
                     entry_id=entry.get("entry_id"))
        out["flags"] = ["P5_NO_MECHANISM"]
        return out

    branch, reason = context_branch(observation, entry)
    if reason == NO_CONTEXT_BRANCH:
        return _empty(observation, NO_CONTEXT_BRANCH,
                      entry_id=entry.get("entry_id"))

    bearing = _axis(entry, branch, "bearing")
    entanglement = _axis(entry, branch, "entanglement")

    flags = []
    two_layer = (branch or {}).get("two_layer", entry.get("two_layer", False))
    if two_layer:
        flags.append("P1_TWO_LAYER")

    invert = (branch or {}).get("sensor_invert",
                                entry.get("sensor_invert", "UNKNOWN"))
    if invert == "OPTIMISTIC":
        flags.append("P2_SENSOR_INVERT")

    rstate = region_state(observation, entry)
    if rstate == REGION_OUT_OF_SCOPE:
        # the order is explicit: flagged, NOT suppressed.
        flags.append("P4_OUT_OF_SCOPE")

    # [CHOICE 7] one verdict pair per morphology.  Never merged, never reduced.
    by_morphology = []
    for morphology in morphologies:
        m_missing, m_invalid = validate_morphology(morphology)
        by_morphology.append({
            "platform_id": morphology.get("platform_id"),
            "bearing_verdict": bearing_verdict(
                bearing["class"], morphology.get("pressure_class")),
            "entanglement_verdict": entanglement_verdict(
                entanglement["class"],
                morphology.get("entanglement_susceptibility")),
            "morphology_missing": m_missing,
            "morphology_invalid": m_invalid,
        })

    verdicts = set(row["bearing_verdict"] for row in by_morphology)
    verdicts.discard(VERDICT_NOT_EVALUABLE)
    if len(verdicts) > 1:
        flags.append("P3_MORPH_SPLIT")

    # flags are a set, rendered in the order the work order lists the checks,
    # so a caller reading the list cannot read an ordering into it.
    flags = [code for code in CHECK_CODES if code in flags]

    return {
        "obs_id": observation.get("obs_id"),
        "entry_id": entry.get("entry_id"),
        "bearing_prior": bearing,
        "entanglement_prior": entanglement,
        "by_morphology": by_morphology,
        "flags": flags,
        "scope": (branch or {}).get("scope", entry.get("scope")),
        "region_state": rstate,
        "derived_from": entry.get("derived_from", entry.get("entry_id")),
        # carried verbatim; read by no check in this module.
        "observer_baseline": observation.get("observer_baseline"),
        "falsified_by": (branch or {}).get("falsified_by",
                                           entry.get("falsified_by")),
        "no_prior_reason": None,
        "intake_missing": [],
        "intake_invalid": [],
    }


# ---------------------------------------------------------------------------
# measurements on the derivation set itself
# ---------------------------------------------------------------------------

def falsifier_coverage(entries):
    """How many entries can say what would disprove them.

    The order: "A prior that cannot say what would disprove it is not
    engineering grade."  Counted, never filled in.
    """
    total = 0
    stated = 0
    for entry in entries:
        total += 1
        fb = entry.get("falsified_by")
        if isinstance(fb, str) and fb.strip() != "":
            stated += 1
            continue
        branches = entry.get("context_branches") or []
        if branches and all(isinstance(b.get("falsified_by"), str) and
                            b.get("falsified_by").strip() != ""
                            for b in branches):
            stated += 1
    return {"stated": stated, "total": total,
            "unstated": total - stated}


def class_coverage(entries):
    """NOT_STATED counts per axis, and the basis split.

    The second output variable the order insists must never be collapsed is
    the one most often left unstated in its own seed set.  Reported, not
    imputed.
    """
    out = {"bearing_not_stated": 0, "entanglement_not_stated": 0,
           "bearing_order_stated": 0, "entanglement_order_stated": 0,
           "total": 0}
    for entry in entries:
        out["total"] += 1
        sources = [entry]
        sources.extend(entry.get("context_branches") or [])
        b_class = "NOT_STATED"
        e_class = "NOT_STATED"
        b_basis = "NOT_STATED"
        e_basis = "NOT_STATED"
        for source in sources:
            if source.get("bearing_class", "NOT_STATED") != "NOT_STATED":
                b_class = source["bearing_class"]
                b_basis = source.get("bearing_class_basis", "NOT_STATED")
            if source.get("entanglement_class", "NOT_STATED") != "NOT_STATED":
                e_class = source["entanglement_class"]
                e_basis = source.get("entanglement_class_basis", "NOT_STATED")
        if b_class == "NOT_STATED":
            out["bearing_not_stated"] += 1
        if e_class == "NOT_STATED":
            out["entanglement_not_stated"] += 1
        if b_basis == "ORDER_STATED":
            out["bearing_order_stated"] += 1
        if e_basis == "ORDER_STATED":
            out["entanglement_order_stated"] += 1
    return out


def morphology_fields_reaching_a_check():
    """Which of the order's eight morphology fields reach any check here.

    NONE of them do.  The order specifies contact_area, contact_pressure,
    n_contacts, swing_profile, joint_exposure, ankle_to_foot_ratio and
    recovery_from_entanglement; every verdict in this module is produced from
    two fields this build ADDED under [CHOICE 2], because the order supplies
    no threshold that turns any of its numbers into a class.  platform_id is
    read, as a label, by nothing that decides anything.

    That is a statement about this build, not about whether the order's fields
    matter.  What it says precisely: the morphology profile as the order
    specifies it cannot produce a verdict without one further declaration, and
    the declaration is doing all the work.
    """
    read_fields = [f for f in MORPHOLOGY_FIELDS_ORDER
                   if f in MORPHOLOGY_FIELDS_READ]
    unread = [f for f in MORPHOLOGY_FIELDS_ORDER
              if f not in MORPHOLOGY_FIELDS_READ]
    return {"read": read_fields, "unread": unread,
            "declared_only": [f for f in MORPHOLOGY_FIELDS_READ
                              if f not in MORPHOLOGY_FIELDS_ORDER]}


def split_is_reachable(observation, entries, morphologies):
    """Does P3 fire anywhere on this observation and this morphology set."""
    result = read(observation, entries, morphologies)
    return "P3_MORPH_SPLIT" in result["flags"]


def region_reaches_no_lookup(observation, entries, other_region):
    """Behavioural check on the hard constraint.

    Re-read the same observation with the region replaced.  If resolution is
    a lookup on region, the entry moves.  It must not.
    """
    a = resolve_entry(observation, entries)
    probe = dict(observation)
    probe["region"] = other_region
    b = resolve_entry(probe, entries)
    return a is b


def boulder_rung_divergence(morphologies):
    """[CHOICE 10] the order says two different things about one prior.

    Its derivation text for the deposition zone reads "Bearing is absent".
    Its validation case A reads "MUST return LOW bearing".  On the ordinal
    ladder those are different rungs, and they do not agree for every
    platform: VERY_LOW supports nothing, LOW supports a low-pressure
    platform.  The entry is built at VERY_LOW because the derivation text is
    the derivation; the disagreement is computed here rather than smoothed,
    so a reader can see which platforms it reaches.
    """
    rows = []
    for morphology in morphologies:
        pressure = morphology.get("pressure_class")
        rows.append({
            "platform_id": morphology.get("platform_id"),
            "as_very_low": bearing_verdict("VERY_LOW", pressure),
            "as_low": bearing_verdict("LOW", pressure),
        })
    return {"rows": rows,
            "platforms_where_rung_matters":
                [r["platform_id"] for r in rows
                 if r["as_very_low"] != r["as_low"]]}


def entanglement_split_has_no_check(observation, entries, morphologies):
    """P3 is specified on bearing only.

    The order's P3 reads "bearing result differs in DIRECTION across two
    supplied morphology profiles".  An entanglement result that differs in
    direction across two profiles fires nothing.  Reported rather than
    repaired, because adding a sixth check would be adding a check the order
    does not have.
    """
    result = read(observation, entries, morphologies)
    verdicts = set(row["entanglement_verdict"] for row in
                   result["by_morphology"])
    verdicts.discard(VERDICT_NOT_EVALUABLE)
    return {"entanglement_verdicts_differ": len(verdicts) > 1,
            "flag_fired": "P3_MORPH_SPLIT" in result["flags"],
            "any_entanglement_check": False}


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------

def _short(text, width):
    text = "" if text is None else str(text)
    text = text.replace("\n", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    if len(text) <= width:
        return text.ljust(width)
    return text[:width - 3] + "..."


def render(results):
    lines = []
    lines.append("TERRAIN PRIOR -- indicator to substrate prior")
    lines.append("priors are statements about the ground; verdicts are "
                 "ratings and need a morphology")
    lines.append("no traversability score is emitted anywhere")
    lines.append("")
    header = ("%-14s %-14s %-11s %-11s %s" %
              ("obs", "entry", "bearing", "entangle", "flags"))
    lines.append(header)
    lines.append("-" * 118)
    for result in results:
        if result["bearing_prior"] is None:
            bearing = "--"
            entangle = "--"
        else:
            bearing = result["bearing_prior"]["class"]
            entangle = result["entanglement_prior"]["class"]
        flags = ",".join(result["flags"]) if result["flags"] else "-"
        if result["no_prior_reason"]:
            flags = flags + "  NO PRIOR: " + result["no_prior_reason"]
        lines.append("%-14s %-14s %-11s %-11s %s" %
                     (_short(result["obs_id"], 14),
                      _short(result["entry_id"], 14),
                      bearing, entangle, flags))
        for row in result["by_morphology"]:
            lines.append("    %-16s bearing=%-14s entanglement=%s" %
                         (_short(row["platform_id"], 16),
                          row["bearing_verdict"],
                          row["entanglement_verdict"]))
        if result["bearing_prior"] is not None:
            lines.append("    scope: %s [%s]" %
                         (result["scope"], result["region_state"]))
            lines.append("    mechanism: %s" %
                         _short(result["bearing_prior"]["mechanism"], 100))
            lines.append("    falsified_by: %s" %
                         (result["falsified_by"] or "NOT_STATED"))
            lines.append("    observer_baseline: %s" %
                         result["observer_baseline"])
        lines.append("")
    return "\n".join(lines)


def render_choices():
    lines = ["CHOICES -- decisions the work order leaves open", ""]
    for key in sorted(CHOICES):
        lines.append("[CHOICE %d] %s" % (key, CHOICES[key]))
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "terrain_prior.py has no --selftest. The checks are in "
            "test_terrain.py:\n"
            "    python3 test_terrain.py\n")
        return 2
    if "--choices" in argv:
        print(render_choices())
        return 0
    import cases
    results = [read(obs, cases.ENTRIES, cases.MORPHOLOGIES_FOR.get(
        obs["obs_id"], ())) for obs in cases.OBSERVATIONS]
    print(render(results))
    print("")
    print(render_choices())
    print("")
    print("DERIVATION SET")
    fc = falsifier_coverage(cases.ENTRIES)
    print("  falsifier stated: %d of %d  (unstated %d)" %
          (fc["stated"], fc["total"], fc["unstated"]))
    cc = class_coverage(cases.ENTRIES)
    print("  bearing class NOT_STATED:      %d of %d" %
          (cc["bearing_not_stated"], cc["total"]))
    print("  entanglement class NOT_STATED: %d of %d" %
          (cc["entanglement_not_stated"], cc["total"]))
    print("  bearing class quoted from the order:      %d" %
          cc["bearing_order_stated"])
    print("  entanglement class quoted from the order: %d" %
          cc["entanglement_order_stated"])
    brd = boulder_rung_divergence(cases.MORPHOLOGIES)
    print("  [CHOICE 10] platforms where VERY_LOW and LOW disagree: %s" %
          (", ".join(brd["platforms_where_rung_matters"]) or "none"))
    mf = morphology_fields_reaching_a_check()
    print("  order-specified morphology fields reaching a check: %s" %
          (", ".join(mf["read"]) or "none, 0 of %d" %
           len(MORPHOLOGY_FIELDS_ORDER)))
    print("  order-specified fields carried, reaching none: %s" %
          ", ".join(mf["unread"]))
    print("  fields this build added, and every verdict rests on them: %s" %
          ", ".join(mf["declared_only"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
