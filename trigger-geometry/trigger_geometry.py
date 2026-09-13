"""trigger_geometry.py -- was this response validated in THIS geometry.

Built to WORK_ORDER.md, landed verbatim beside this file.

WHAT THIS IS

A trigger is a sensed quantity, a threshold and a programmed response.  This
takes one, plus a geometry it will operate in, and reports whether the
RESPONSE was validated there.  The failure class is SENSOR CORRECT + MODEL
INVERTED: the reading is accurate and the response was derived somewhere the
response reduces the hazard, then applied somewhere it raises it.

WHAT THIS IS NOT

It does not evaluate the sensor.  `sensor_verdict` is carried verbatim from
the intake to the return and is computed by nothing here -- asserted.  It
does not evaluate the threshold.  There is no safety score: sensor, inference
and response are three separate verdicts on three separate lines, nothing
sums, averages, ranks or orders them, and no check reads more than one.

FOUR HARD CONSTRAINTS, ENFORCED RATHER THAN DESCRIBED

1. No single score.  Three verdicts, and an AST check asserts no arithmetic
   operator touches any of them.
2. Redundancy is not mitigation.  `redundancy` is carried on the trigger and
   read by no check -- asserted from the AST and behaviourally, by sweeping
   it and requiring every flag to be unchanged.
3. A geometry absent from the validation set is ABSENT, never SAFE.
4. Reliability figures are refused at intake.  `read()` raises on a
   reliability-shaped key rather than ignoring it, because an ignored input
   is one somebody assumes was used.

LIMITS STATED AT THE TOP, NOT THE BOTTOM

* The reliability screen is a word list.  A figure under a name not on the
  list enters as an ordinary field, and any paraphrase steps around it.
* Three of the order's six checks have no field in the order's own intake
  schema (see [CHOICE 1]).  They run on fields this build ADDED, declared
  per trigger and never inferred, so an undeclared field returns
  NOT_EVALUABLE rather than a silence that reads as a pass.
* Nothing here has been run against a real trigger, a real vehicle or a real
  road.  Every case in `cases.py` is constructed and says so.
"""

import sys

# ---------------------------------------------------------------------------
# vocabularies
# ---------------------------------------------------------------------------

SENSOR_VERDICTS = ("CORRECT", "DEGRADED", "UNKNOWN")
INSTANCE_COUNTS = ("SINGLE", "REPEATED", "UNSPECIFIED")

# [CHOICE 1] three of the order's six checks name a property the order's own
# intake schema carries no field for -- T2 (does the response feed the next
# input cycle), T4 (does the proxy decouple silently), T5 (is this the
# condition where consequence is highest).  Each becomes a DECLARED field
# with three values.  UNDECLARED never fires and never clears: inferring
# "the response does not couple" from nobody having said so is the silence
# this instrument exists to refuse.
YES = "YES"
NO = "NO"
UNDECLARED = "UNDECLARED"
DECLARED_VALUES = (YES, NO, UNDECLARED)

ADDED_FIELDS = ("couples_into_next_cycle", "proxy_decouples_silently",
                "degrades_where_consequence_highest")

ORDER_TRIGGER_FIELDS = ("trigger_id", "sensed_quantity", "sensor_verdict",
                        "inferred_hazard", "response", "response_derived_in")
ORDER_GEOMETRY_FIELDS = ("geometry_id", "geometry_class", "reversal",
                         "reversal_period", "system_relaxation_time",
                         "gradient", "constructibility_note")

CHECK_CODES = ("T1_ACCUMULATION", "T2_RESPONSE_COUPLES",
               "T3_ENVELOPE_UNSTATED", "T4_PROXY_STATE",
               "T5_DEGRADATION_CORRELATION", "T6_GEOMETRY_ABSENT")

FIRED = "FIRED"
SILENT = "SILENT"
NOT_EVALUABLE = "NOT_EVALUABLE"
CHECK_STATES = (FIRED, SILENT, NOT_EVALUABLE)

# which of the three verdicts each check bears on.  Declared, so a reader can
# disagree with the assignment rather than guess at it.  T3 suspends both
# derived verdicts, because an unstated envelope is not evidence either way.
BEARS_ON = {
    "T1_ACCUMULATION": "response",
    "T2_RESPONSE_COUPLES": "response",
    "T6_GEOMETRY_ABSENT": "response",
    # a proxy that decouples silently, and a sensor that degrades exactly
    # where consequence is highest, both corrupt the step from "the sensor
    # says X" to "X is the case" -- which is the inference, not the sensor.
    "T4_PROXY_STATE": "inference",
    "T5_DEGRADATION_CORRELATION": "inference",
    "T3_ENVELOPE_UNSTATED": "both",
}

VERDICT_OK = "NOT_CONTRADICTED_HERE"
VERDICT_INVERTED = "INVERTED_IN_THIS_GEOMETRY"
VERDICT_UNRATED = "UNRATED"
VERDICT_NOT_EVALUABLE = "NOT_EVALUABLE"

# [CHOICE 3] the hard constraints name a state -- ABSENT -- that the stated
# return vocabulary (True | False | UNRATED) does not carry.  The three
# values stay exactly as delivered and the reason rides beside them.
UNRATED = "UNRATED"
REASON_CLEAN = "CLEAN"
REASON_FLAGGED = "FLAGGED"
REASON_ABSENT = "ABSENT"
REASON_UNSTATED_ENVELOPE = "UNSTATED_ENVELOPE"
REASON_NOT_EVALUABLE = "CHECKS_NOT_EVALUABLE"
REASON_INTAKE = "INTAKE_INCOMPLETE"

INTAKE_INCOMPLETE = "INTAKE_INCOMPLETE"

# [CHOICE 7] reliability-shaped intake keys are refused rather than ignored.
# A word list, and the limit is stated in the module docstring.
RELIABILITY_TOKENS = ("reliability", "availability", "mtbf", "mttf",
                      "uptime", "downtime", "failure_rate", "confidence",
                      "nines", "sil", "pfd", "dependability")


class ReliabilityInput(Exception):
    """Raised at intake.  An average over an envelope says nothing about its
    edges, and accepting one silently would let it be cited as if it did."""


CHOICES = {
    1: "T2, T4 and T5 run on declared three-value fields this build added; "
       "the order's intake schema carries no field for any of them, and "
       "UNDECLARED neither fires nor clears",
    2: "T3 suppresses T6; an envelope that was never stated cannot be asked "
       "whether it covers a geometry (forced by validation case E's T3 ONLY)",
    3: "validated_reason rides beside the delivered three-value return, "
       "because the hard constraints name ABSENT and the return does not",
    4: "three verdicts (sensor, inference, response) are returned beside the "
       "delivered single field; the hard constraint names three and the "
       "delivered Return block has one",
    5: "an absent reversal_period or system_relaxation_time is recorded as a "
       "finding and does not block the return; only an absent REQUIRED field "
       "returns INTAKE_INCOMPLETE",
    6: "accumulation_ratio is computed where both times are present and "
       "gates nothing, because T1 as written reads neither",
    7: "reliability-shaped intake keys raise rather than being dropped",
    8: "redundancy is carried on the trigger and read by no check",
    9: "a NOT_EVALUABLE check blocks a True verdict; validating on a check "
       "nobody ran is the pass this instrument exists to refuse",
}


# ---------------------------------------------------------------------------
# intake
# ---------------------------------------------------------------------------

def _reliability_keys(mapping, prefix=""):
    """Every key whose name carries a reliability-shaped token."""
    hits = []
    for key, value in mapping.items():
        name = prefix + str(key)
        parts = str(key).lower().replace("-", "_").split("_")
        for token in RELIABILITY_TOKENS:
            if token in parts:
                hits.append(name)
                break
        if isinstance(value, dict):
            hits.extend(_reliability_keys(value, name + "."))
    return hits


def refuse_reliability(trigger, geometry):
    """[CHOICE 7] raise rather than ignore."""
    hits = _reliability_keys(trigger, "trigger.")
    hits.extend(_reliability_keys(geometry, "geometry."))
    if hits:
        raise ReliabilityInput(
            "reliability-shaped inputs are not accepted: " + ", ".join(hits))
    return hits


def validate_trigger(trigger):
    """Return (missing, invalid).  Nothing is defaulted and nothing guessed."""
    missing = []
    invalid = []
    for field in ORDER_TRIGGER_FIELDS:
        if field not in trigger:
            missing.append(field)
    if trigger.get("sensor_verdict") is not None and \
            trigger.get("sensor_verdict") not in SENSOR_VERDICTS:
        invalid.append("sensor_verdict")
    derived = trigger.get("response_derived_in")
    if derived is None:
        pass
    elif not isinstance(derived, dict):
        invalid.append("response_derived_in")
    else:
        if "stated" not in derived:
            missing.append("response_derived_in.stated")
        elif not isinstance(derived["stated"], bool):
            invalid.append("response_derived_in.stated")
        count = derived.get("instance_count")
        if count is not None and count not in INSTANCE_COUNTS:
            invalid.append("response_derived_in.instance_count")
    # [CHOICE 1] the added fields are optional at intake and default to
    # UNDECLARED; an out-of-vocabulary value is refused rather than read.
    for field in ADDED_FIELDS:
        if trigger.get(field, UNDECLARED) not in DECLARED_VALUES:
            invalid.append(field)
    return missing, invalid


def validate_geometry(geometry):
    """Return (missing, invalid).  geometry_class is free text, never an enum."""
    missing = []
    invalid = []
    for field in ("geometry_id", "geometry_class", "reversal"):
        if field not in geometry:
            missing.append(field)
    if geometry.get("reversal") is not None and \
            not isinstance(geometry.get("reversal"), bool):
        invalid.append("reversal")
    for field in ("reversal_period", "system_relaxation_time", "gradient"):
        value = geometry.get(field)
        if value is not None and not isinstance(value, (int, float)):
            invalid.append(field)
    return missing, invalid


def unmeasured_times(geometry):
    """[CHOICE 5] the order's Open section and its validation case A pull
    opposite ways on these two fields.

    Open says an absent reversal_period or system_relaxation_time returns
    INTAKE_INCOMPLETE.  Case A says the serpentine grade MUST fire T1 and
    return False, and names no times -- and T1 as written reads neither
    field.  Blocking the return on them would make the order's own reference
    case unreachable, so they are recorded as a finding and the checks
    proceed.  Nothing estimates them.
    """
    absent = []
    for field in ("reversal_period", "system_relaxation_time"):
        if geometry.get(field) is None:
            absent.append(field)
    return absent


# ---------------------------------------------------------------------------
# checks -- each returns FIRED / SILENT / NOT_EVALUABLE
# ---------------------------------------------------------------------------

def t1_accumulation(trigger, geometry):
    """geometry reverses AND the response was derived on a single instance.

    The validating test damps out and the operating case does not.  Reads no
    time: see accumulation_ratio() and [CHOICE 6].
    """
    derived = trigger.get("response_derived_in") or {}
    reversal = geometry.get("reversal")
    count = derived.get("instance_count")
    if reversal is None or count is None:
        return NOT_EVALUABLE
    if reversal is True and count == "SINGLE":
        return FIRED
    return SILENT


def t2_response_couples(trigger, geometry):
    """[CHOICE 1] the response feeds the next input cycle: a positive term."""
    value = trigger.get("couples_into_next_cycle", UNDECLARED)
    if value == UNDECLARED:
        return NOT_EVALUABLE
    return FIRED if value == YES else SILENT


def t3_envelope_unstated(trigger, geometry):
    """The validation envelope was never stated.  No claim either way."""
    derived = trigger.get("response_derived_in") or {}
    stated = derived.get("stated")
    if not isinstance(stated, bool):
        return NOT_EVALUABLE
    return FIRED if stated is False else SILENT


def t4_proxy_state(trigger, geometry):
    """[CHOICE 1] the observable is a proxy and the two decouple silently."""
    value = trigger.get("proxy_decouples_silently", UNDECLARED)
    if value == UNDECLARED:
        return NOT_EVALUABLE
    return FIRED if value == YES else SILENT


def t5_degradation_correlation(trigger, geometry):
    """Sensor DEGRADED in exactly the conditions where consequence is highest.

    Half of this check IS in the order's schema (`sensor_verdict`) and half is
    not (whether this geometry is the high-consequence condition), so it is
    the one check that is partly supported.
    """
    here = trigger.get("degrades_where_consequence_highest", UNDECLARED)
    if here == UNDECLARED:
        return NOT_EVALUABLE
    if here == YES and trigger.get("sensor_verdict") == "DEGRADED":
        return FIRED
    return SILENT


def t6_geometry_absent(trigger, geometry):
    """The operating geometry class is not in the validation envelope.

    geometry_class is free text and is compared by equality against the
    envelope's own declared classes.  There is no enum of geometry classes
    anywhere in this module, per the hard constraint.
    """
    derived = trigger.get("response_derived_in") or {}
    here = geometry.get("geometry_class")
    if here is None:
        return NOT_EVALUABLE
    declared = derived.get("geometry_class")
    if declared is None:
        return NOT_EVALUABLE
    if isinstance(declared, str):
        covered = [declared]
    else:
        covered = list(declared)
    return SILENT if here in covered else FIRED


CHECKS = (
    ("T1_ACCUMULATION", t1_accumulation),
    ("T2_RESPONSE_COUPLES", t2_response_couples),
    ("T3_ENVELOPE_UNSTATED", t3_envelope_unstated),
    ("T4_PROXY_STATE", t4_proxy_state),
    ("T5_DEGRADATION_CORRELATION", t5_degradation_correlation),
    ("T6_GEOMETRY_ABSENT", t6_geometry_absent),
)


# ---------------------------------------------------------------------------
# reported quantities
# ---------------------------------------------------------------------------

def accumulation_ratio(geometry):
    """[CHOICE 6] the two times the order calls load-bearing, as one ratio.

    system_relaxation_time / reversal_period.  Above 1 the system is still
    carrying the previous reversal when the next arrives, which is the order's
    own mechanism.  It GATES NOTHING: T1 as written reads neither time, so
    making the ratio a precondition would stop T1 firing on the order's own
    reference case, where neither time is measured.
    """
    period = geometry.get("reversal_period")
    relax = geometry.get("system_relaxation_time")
    if period is None or relax is None:
        return None
    if period <= 0:
        return None
    return relax / float(period)


# ---------------------------------------------------------------------------
# the read
# ---------------------------------------------------------------------------

def _empty(trigger, geometry, missing, invalid):
    return {
        "trigger_id": trigger.get("trigger_id"),
        "geometry_id": geometry.get("geometry_id"),
        "flags": None,
        "check_states": {},
        "response_validated_here": UNRATED,
        "validated_reason": REASON_INTAKE,
        "failure_mode_if_inverted": trigger.get("failure_mode_if_inverted"),
        "operator_correction_required":
            trigger.get("operator_correction_required"),
        "verdicts": {"sensor": trigger.get("sensor_verdict"),
                     "inference": VERDICT_UNRATED,
                     "response": VERDICT_UNRATED},
        "not_evaluable": [],
        "suppressed": [],
        "requires_independent_verification": None,
        "accumulation_ratio": None,
        "times_unmeasured": [],
        "intake_missing": missing,
        "intake_invalid": invalid,
        "constructibility_note": geometry.get("constructibility_note"),
    }


def read(trigger, geometry):
    """One trigger, one geometry.  Three verdicts, never one."""
    refuse_reliability(trigger, geometry)

    t_missing, t_invalid = validate_trigger(trigger)
    g_missing, g_invalid = validate_geometry(geometry)
    missing = ["trigger." + f for f in t_missing]
    missing.extend("geometry." + f for f in g_missing)
    invalid = ["trigger." + f for f in t_invalid]
    invalid.extend("geometry." + f for f in g_invalid)
    if missing or invalid:
        return _empty(trigger, geometry, missing, invalid)

    states = {}
    for code, check in CHECKS:
        states[code] = check(trigger, geometry)

    # [CHOICE 2] an envelope that was never stated cannot be asked whether it
    # covers this geometry.  Validation case E requires T3 and nothing else,
    # so T6 is suppressed rather than merely silent, and the suppression is
    # reported rather than hidden.
    suppressed = []
    if states["T3_ENVELOPE_UNSTATED"] == FIRED:
        if states["T6_GEOMETRY_ABSENT"] != SILENT:
            suppressed.append("T6_GEOMETRY_ABSENT")
        states["T6_GEOMETRY_ABSENT"] = SILENT

    flags = [code for code in CHECK_CODES if states[code] == FIRED]
    not_evaluable = [code for code in CHECK_CODES
                     if states[code] == NOT_EVALUABLE]

    # [CHOICE 4] three verdicts.  Nothing combines them.
    sensor = trigger.get("sensor_verdict")
    inference = VERDICT_OK
    response = VERDICT_OK
    if states["T3_ENVELOPE_UNSTATED"] == FIRED:
        inference = VERDICT_UNRATED
        response = VERDICT_UNRATED
    else:
        for code in flags:
            if BEARS_ON[code] == "inference":
                inference = VERDICT_INVERTED
            elif BEARS_ON[code] == "response":
                response = VERDICT_INVERTED
        for code in not_evaluable:
            if BEARS_ON[code] == "inference" and inference == VERDICT_OK:
                inference = VERDICT_NOT_EVALUABLE
            elif BEARS_ON[code] == "response" and response == VERDICT_OK:
                response = VERDICT_NOT_EVALUABLE

    if states["T3_ENVELOPE_UNSTATED"] == FIRED:
        validated = UNRATED
        reason = REASON_UNSTATED_ENVELOPE
    elif "T6_GEOMETRY_ABSENT" in flags:
        # the hard constraint: absent, never safe.
        validated = UNRATED
        reason = REASON_ABSENT
    elif flags:
        validated = False
        reason = REASON_FLAGGED
    elif not_evaluable:
        # [CHOICE 9] a pass resting on a check nobody ran is the silence this
        # instrument refuses.
        validated = UNRATED
        reason = REASON_NOT_EVALUABLE
    else:
        validated = True
        reason = REASON_CLEAN

    return {
        "trigger_id": trigger.get("trigger_id"),
        "geometry_id": geometry.get("geometry_id"),
        "flags": flags,
        "check_states": states,
        "response_validated_here": validated,
        "validated_reason": reason,
        "failure_mode_if_inverted": trigger.get("failure_mode_if_inverted"),
        "operator_correction_required":
            trigger.get("operator_correction_required"),
        "verdicts": {"sensor": sensor, "inference": inference,
                     "response": response},
        "not_evaluable": not_evaluable,
        "suppressed": suppressed,
        "requires_independent_verification":
            "T4_PROXY_STATE" in flags,
        "accumulation_ratio": accumulation_ratio(geometry),
        "times_unmeasured": unmeasured_times(geometry),
        "intake_missing": [],
        "intake_invalid": [],
        "constructibility_note": geometry.get("constructibility_note"),
    }


# ---------------------------------------------------------------------------
# constraint readouts
# ---------------------------------------------------------------------------

def redundancy_effect(trigger, geometry, settings):
    """[CHOICE 8] sweep the redundancy field and report whether any flag moved.

    The hard constraint is that agreement between sensors must not lower any
    flag.  Stating it is cheap; this measures it.  `redundancy` is carried on
    the trigger and no check reads it, which the selftest also asserts from
    the AST.
    """
    seen = set()
    rows = []
    for setting in settings:
        probe = dict(trigger)
        probe["redundancy"] = setting
        result = read(probe, geometry)
        key = (tuple(result["flags"] or ()),
               result["response_validated_here"],
               tuple(sorted(result["verdicts"].items())))
        seen.add(key)
        rows.append({"redundancy": setting, "flags": result["flags"]})
    return {"rows": rows, "distinct_outcomes": len(seen),
            "flags_invariant": len(seen) == 1}


def schema_support():
    """Which of the order's six checks the order's own intake schema supports.

    Reported rather than argued: T1, T3 and T6 read fields the order's schema
    declares; T2 and T4 read fields it does not; T5 reads one of each.
    """
    supported = []
    added = []
    mixed = []
    for code, _ in CHECKS:
        if code in ("T1_ACCUMULATION", "T3_ENVELOPE_UNSTATED",
                    "T6_GEOMETRY_ABSENT"):
            supported.append(code)
        elif code == "T5_DEGRADATION_CORRELATION":
            mixed.append(code)
        else:
            added.append(code)
    return {"from_order_schema": supported, "needs_added_field": added,
            "one_of_each": mixed, "added_fields": list(ADDED_FIELDS)}


def unledgered_safety_functions(results):
    """Triggers whose operating record depends on a human overriding them.

    The order: if operator_correction_required is non-null, removing the human
    removes a safety function that appears nowhere on the ledger.  Counted,
    never scored.
    """
    named = [r["trigger_id"] for r in results
             if r.get("operator_correction_required")]
    # readings, then distinct triggers.  One trigger read in two geometries
    # is two readings and one unledgered function, and reporting only the
    # first number double-counts it.
    distinct = []
    for name in named:
        if name not in distinct:
            distinct.append(name)
    return {"with_correction": named, "count": len(named),
            "distinct": distinct, "distinct_count": len(distinct),
            "of": len(results)}


def clean_reachable(results):
    """Is the clean branch reachable at all on this corpus.

    An instrument that never returns clean is an objection generator, which
    the order names as its own failure mode in validation case D.
    """
    clean = [r["trigger_id"] for r in results
             if r["response_validated_here"] is True]
    return {"clean": clean, "reachable": bool(clean), "of": len(results)}


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
    lines.append("TRIGGER GEOMETRY -- was this response validated HERE")
    lines.append("three verdicts, never one; sensor is carried, never scored")
    lines.append("absent from the validation set is ABSENT, never SAFE")
    lines.append("")
    lines.append("%-16s %-18s %-9s %s" %
                 ("trigger", "geometry", "validated", "flags"))
    lines.append("-" * 110)
    for result in results:
        flags = ",".join(result["flags"]) if result["flags"] else "-"
        if result["flags"] is None:
            flags = "-- " + result["validated_reason"]
        lines.append("%-16s %-18s %-9s %s" %
                     (_short(result["trigger_id"], 16),
                      _short(result["geometry_id"], 18),
                      str(result["response_validated_here"]), flags))
        lines.append("    reason: %s" % result["validated_reason"])
        verdicts = result["verdicts"]
        lines.append("    sensor:    %s   (carried, not computed here)" %
                     verdicts["sensor"])
        lines.append("    inference: %s" % verdicts["inference"])
        lines.append("    response:  %s" % verdicts["response"])
        if result["not_evaluable"]:
            lines.append("    not evaluable: %s" %
                         ",".join(result["not_evaluable"]))
        if result["suppressed"]:
            lines.append("    suppressed by T3: %s" %
                         ",".join(result["suppressed"]))
        if result["requires_independent_verification"]:
            lines.append("    REQUIRES an independent verification path")
        if result["times_unmeasured"]:
            lines.append("    times unmeasured: %s" %
                         ",".join(result["times_unmeasured"]))
        ratio = result["accumulation_ratio"]
        lines.append("    accumulation ratio: %s  (gates nothing)" %
                     ("--" if ratio is None else "%.3f" % ratio))
        if result["operator_correction_required"]:
            lines.append("    operator correction: %s" %
                         result["operator_correction_required"])
        if result["failure_mode_if_inverted"]:
            lines.append("    if inverted: %s" %
                         _short(result["failure_mode_if_inverted"], 88))
        if result["constructibility_note"]:
            lines.append("    geometry exists because: %s" %
                         _short(result["constructibility_note"], 78))
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
            "trigger_geometry.py has no --selftest. The checks are in "
            "test_trigger.py:\n"
            "    python3 test_trigger.py\n")
        return 2
    if "--choices" in argv:
        print(render_choices())
        return 0
    import cases
    results = [read(cases.TRIGGERS[t], cases.GEOMETRIES[g])
               for t, g in cases.PAIRS]
    print(render(results))
    print("")
    print(render_choices())
    print("")
    print("SCHEMA SUPPORT")
    support = schema_support()
    print("  checks the order's intake schema supports: %s" %
          ", ".join(support["from_order_schema"]))
    print("  checks needing a field this build added:   %s" %
          ", ".join(support["needs_added_field"]))
    print("  one field of each:                         %s" %
          ", ".join(support["one_of_each"]))
    print("  fields added: %s" % ", ".join(support["added_fields"]))
    print("")
    print("CONSTRAINT READOUTS")
    red = redundancy_effect(cases.TRIGGERS["serpentine_brake"],
                            cases.GEOMETRIES["driftless_grade"],
                            (1, 2, 3, "agree", "disagree", None))
    print("  redundancy swept over %d settings, flags invariant: %s" %
          (len(red["rows"]), red["flags_invariant"]))
    ledger = unledgered_safety_functions(results)
    print("  readings whose record depends on a human override: %d of %d"
          % (ledger["count"], ledger["of"]))
    print("  distinct triggers doing so: %d (%s)"
          % (ledger["distinct_count"], ", ".join(ledger["distinct"]) or "none"))
    reach = clean_reachable(results)
    print("  clean branch reachable: %s (%s)" %
          (reach["reachable"], ", ".join(reach["clean"]) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
