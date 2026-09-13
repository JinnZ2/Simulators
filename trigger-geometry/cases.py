"""cases.py -- constructed triggers and geometries for trigger_geometry.py.

EVERY CASE HERE IS CONSTRUCTED.  No trigger in this file was read off a real
control unit, no geometry was surveyed, no sensor_verdict was measured, and
no reversal_period or system_relaxation_time is a number anybody recorded.
The reference case is transcribed from the work order's own prose, which is
an operator's account and is carried as such.

NO EXPECTED VERDICT APPEARS IN THIS FILE.  What each case must return lives
in test_trigger.py, so that a case cannot be quietly shaped until it agrees
with the module.

The five validation cases the order fixes are A..E.  The rows after them
exist so that every declared vocabulary member is reached by something --
a member no case reaches cannot be told from one nobody looked for.
"""

# ---------------------------------------------------------------------------
# triggers
# ---------------------------------------------------------------------------

TRIGGERS = {

    # ---- A / B: the order's reference trigger -----------------------------
    # Transcribed from WORK_ORDER.md "Worked case".  The envelope NAMES the
    # serpentine class and was validated on ONE instance of it: see
    # CLAIM_TABLE TG_001 for why case A's stated requirement forces that
    # reading rather than the geometry-absent one.
    "serpentine_brake": {
        "trigger_id": "serpentine_brake",
        "sensed_quantity": "chassis lateral displacement",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "rollover risk",
        "response": "brake",
        "response_derived_in": {
            "geometry_class": ["descending serpentine grade",
                               "single curve, flat"],
            "instance_count": "SINGLE",
            "stated": True,
        },
        "couples_into_next_cycle": "YES",
        "proxy_decouples_silently": "NO",
        "degrades_where_consequence_highest": "NO",
        "redundancy": "single sensor",
        "failure_mode_if_inverted":
            "braking removes momentum from the tractor holding the rig and "
            "transfers load rearward to the trailer, increasing trailer "
            "moment and therefore increasing rollover risk",
        "operator_correction_required":
            "push through -- overpower the trigger; the opposite of what "
            "every safety layer is designed to permit",
        "source": "CONSTRUCTED from WORK_ORDER.md worked case (operator "
                  "account, carried verbatim, verified against nothing)",
    },

    # ---- C: fifth wheel ---------------------------------------------------
    "fifth_wheel_latch": {
        "trigger_id": "fifth_wheel_latch",
        "sensed_quantity": "latch handle position",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "trailer uncoupled",
        "response": "permit departure",
        "response_derived_in": {
            "geometry_class": ["yard coupling, level"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        # the handle reads the handle, not the jaw around the kingpin
        "proxy_decouples_silently": "YES",
        "degrades_where_consequence_highest": "NO",
        "redundancy": "single sensor",
        "failure_mode_if_inverted":
            "handle seated with the jaw closed on nothing; the observable "
            "and the mechanical state part with no signal, and the "
            "consequence is a dropped trailer at road speed",
        "operator_correction_required":
            "pull test against the kingpin, and a visual on the jaw",
        "source": "CONSTRUCTED to the order's validation case C",
    },

    # ---- D: the falsifier -------------------------------------------------
    # Correct sensor, correctly derived response, envelope stated and
    # covering the operating geometry, derived over REPEATED instances.
    "grade_retarder": {
        "trigger_id": "grade_retarder",
        "sensed_quantity": "driveline speed",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "service brake thermal load",
        "response": "engage engine retarder",
        "response_derived_in": {
            "geometry_class": ["sustained descending grade, straight"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        "proxy_decouples_silently": "NO",
        "degrades_where_consequence_highest": "NO",
        "redundancy": "single sensor",
        "failure_mode_if_inverted": None,
        "operator_correction_required": None,
        "source": "CONSTRUCTED to the order's validation case D",
    },

    # ---- E: unstated envelope ---------------------------------------------
    # Nothing declared about where the response came from, and -- the point
    # of the case -- nothing declared about the added fields either.  An
    # absence is not a finding against the trigger.
    "stability_cut": {
        "trigger_id": "stability_cut",
        "sensed_quantity": "yaw rate",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "loss of directional control",
        "response": "cut throttle",
        "response_derived_in": {
            "geometry_class": None,
            "instance_count": "UNSPECIFIED",
            "stated": False,
        },
        "redundancy": "single sensor",
        "failure_mode_if_inverted": None,
        "operator_correction_required": None,
        "source": "CONSTRUCTED to the order's validation case E",
    },

    # ---- reachability: T5, sensor DEGRADED where consequence is highest ----
    "washout_detect": {
        "trigger_id": "washout_detect",
        "sensed_quantity": "optical road-edge return",
        "sensor_verdict": "DEGRADED",
        "inferred_hazard": "shoulder washout",
        "response": "hold lane centre",
        "response_derived_in": {
            "geometry_class": ["two-lane rural, clear air"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        "proxy_decouples_silently": "NO",
        # the washout and the rain that degrades the optics arrive together
        "degrades_where_consequence_highest": "YES",
        "redundancy": "two sensors, agreeing",
        "failure_mode_if_inverted":
            "an availability figure averaged over the envelope reports the "
            "inverse of the truth, because the outage is concentrated in "
            "exactly the conditions the figure is quoted to cover",
        "operator_correction_required":
            "slow to a speed where the road edge is readable by eye",
        "source": "CONSTRUCTED for T5 reachability",
    },

    # ---- reachability: T6, operating class absent from the envelope -------
    # Non-vehicle.  The order's own scope section: the deposition zone
    # downstream of an obstruction, where every sensor rates the surface
    # better than it is.
    "fineness_probe": {
        "trigger_id": "fineness_probe",
        "sensed_quantity": "surface grain size",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "none; fine and smooth reads as consolidated",
        "response": "commit weight",
        "response_derived_in": {
            "geometry_class": ["floodplain overbank deposit"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        "proxy_decouples_silently": "YES",
        "degrades_where_consequence_highest": "NO",
        "redundancy": "three sensors, agreeing",
        "failure_mode_if_inverted":
            "the obstruction sorted the sediment; the deposition zone behind "
            "it is fines dropped from slowed water and reads smoother and "
            "finer than the scoured side, so the correct reading supports "
            "the inverted inference",
        "operator_correction_required":
            "read the flow direction and the obstruction, and stay off the "
            "lee side",
        "source": "CONSTRUCTED from the order's scope section; the same "
                  "shape is worked at length in terrain-prior/",
    },

    # ---- reachability: CHOICE 9, nothing fires and one check never ran ----
    # Non-vehicle.  The order's other named instance: the committed dive.
    "dive_commit": {
        "trigger_id": "dive_commit",
        "sensed_quantity": "closure rate on target",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "intercept failure",
        "response": "commit past the abort point",
        "response_derived_in": {
            "geometry_class": ["open water, single target"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        "proxy_decouples_silently": "NO",
        # nobody has said whether this is the high-consequence condition
        "redundancy": "single sensor",
        "failure_mode_if_inverted":
            "prior sound, commit point wrong; the missing term is a rate, "
            "and the geometry that supplies it is not in the envelope",
        "operator_correction_required": None,
        "source": "CONSTRUCTED from the order's scope section",
    },

    # ---- reachability: sensor UNKNOWN, and T1 not evaluable ---------------
    "culvert_ice": {
        "trigger_id": "culvert_ice",
        "sensed_quantity": "deck surface temperature",
        "sensor_verdict": "UNKNOWN",
        "inferred_hazard": "deck icing",
        "response": "reduce speed",
        "response_derived_in": {
            "geometry_class": ["bridge deck, exposed"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        "proxy_decouples_silently": "NO",
        "degrades_where_consequence_highest": "NO",
        "redundancy": "single sensor",
        "failure_mode_if_inverted": None,
        "operator_correction_required": None,
        "source": "CONSTRUCTED for sensor-verdict and T1 reachability",
    },

    # ---- reachability: T6 NOT_EVALUABLE, envelope stated with no class ----
    # The envelope was stated and does not say WHERE.  Distinct from case E,
    # where nothing was stated at all: here T3 is silent, so T6 is not
    # suppressed, and T6 has nothing to compare against.
    "envelope_no_class": {
        "trigger_id": "envelope_no_class",
        "sensed_quantity": "wheel slip",
        "sensor_verdict": "CORRECT",
        "inferred_hazard": "traction loss",
        "response": "reduce torque",
        "response_derived_in": {
            "geometry_class": None,
            "instance_count": "REPEATED",
            "stated": True,
        },
        "couples_into_next_cycle": "NO",
        "proxy_decouples_silently": "NO",
        "degrades_where_consequence_highest": "NO",
        "redundancy": "single sensor",
        "failure_mode_if_inverted": None,
        "operator_correction_required": None,
        "source": "CONSTRUCTED so T6 NOT_EVALUABLE is reachable",
    },

    # ---- reachability: intake incomplete ----------------------------------
    "partial_trigger": {
        "trigger_id": "partial_trigger",
        "sensed_quantity": "axle load",
        "sensor_verdict": "CORRECT",
        # inferred_hazard and response absent on purpose
        "response_derived_in": {
            "geometry_class": ["weigh station approach"],
            "instance_count": "REPEATED",
            "stated": True,
        },
        "redundancy": "single sensor",
        "source": "CONSTRUCTED for intake-incomplete reachability",
    },
}


# a trigger carrying a reliability-shaped key.  Deliberately NOT in PAIRS:
# read() raises on it, and the test is where the raise is exercised.
REFUSED_TRIGGER = {
    "trigger_id": "refused_by_intake",
    "sensed_quantity": "chassis lateral displacement",
    "sensor_verdict": "CORRECT",
    "inferred_hazard": "rollover risk",
    "response": "brake",
    "response_derived_in": {
        "geometry_class": ["descending serpentine grade"],
        "instance_count": "REPEATED",
        "stated": True,
    },
    "system_availability": 0.9997,
    "source": "CONSTRUCTED to exercise the reliability refusal",
}


# ---------------------------------------------------------------------------
# geometries
# ---------------------------------------------------------------------------

GEOMETRIES = {

    # ---- A: the reference geometry ----------------------------------------
    # Both times unmeasured, as the order's Open section says they will be.
    "driftless_grade": {
        "geometry_id": "driftless_grade",
        "geometry_class": "descending serpentine grade",
        "reversal": True,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.09,
        "constructibility_note":
            "over nine percent, two lanes, continuous serpentine reversals "
            "for the length of the grade -- the only geometry in which "
            "usable road can be built on that topography",
        "source": "CONSTRUCTED from WORK_ORDER.md worked case",
    },

    # ---- B: single curve, flat --------------------------------------------
    "single_curve_flat": {
        "geometry_id": "single_curve_flat",
        "geometry_class": "single curve, flat",
        "reversal": False,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.0,
        "constructibility_note":
            "the test article; one curve, chosen because it is easy to "
            "instrument, not because it is what the road does",
        "source": "CONSTRUCTED to the order's validation case B",
    },

    # ---- C ----------------------------------------------------------------
    "yard_level": {
        "geometry_id": "yard_level",
        "geometry_class": "yard coupling, level",
        "reversal": False,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.0,
        "constructibility_note":
            "flat paved yard; the geometry the coupling check was written "
            "in and the only one it is ever demonstrated in",
        "source": "CONSTRUCTED to the order's validation case C",
    },

    # ---- D ----------------------------------------------------------------
    "straight_descent": {
        "geometry_id": "straight_descent",
        "geometry_class": "sustained descending grade, straight",
        "reversal": False,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.06,
        "constructibility_note":
            "a long straight descent; routed this way because the ridge "
            "allowed it",
        "source": "CONSTRUCTED to the order's validation case D",
    },

    # ---- E ----------------------------------------------------------------
    "ordinary_two_lane": {
        "geometry_id": "ordinary_two_lane",
        "geometry_class": "two-lane rural, clear air",
        "reversal": False,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.01,
        "constructibility_note":
            "unremarkable road; carried so that an unrated return is not "
            "confounded with an unusual geometry",
        "source": "CONSTRUCTED to the order's validation case E",
    },

    # ---- reachability: T5, the high-consequence condition ------------------
    "rural_in_rain": {
        "geometry_id": "rural_in_rain",
        "geometry_class": "two-lane rural, clear air",
        "reversal": False,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.02,
        "constructibility_note":
            "same road as ordinary_two_lane; the water is the condition, "
            "not the geometry, and is carried on the trigger",
        "source": "CONSTRUCTED for T5 reachability",
    },

    # ---- reachability: T6, a class absent from every envelope -------------
    "boulder_lee": {
        "geometry_id": "boulder_lee",
        "geometry_class": "deposition zone, lee of an obstruction",
        "reversal": False,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.0,
        "constructibility_note":
            "the zone exists because the obstruction exists; it is not an "
            "edge case of a floodplain, it is what a floodplain does around "
            "anything that stands in it",
        "source": "CONSTRUCTED for T6 reachability",
    },

    # ---- reachability: both times measured, so the ratio is not None ------
    "reversing_ramp": {
        "geometry_id": "reversing_ramp",
        "geometry_class": "open water, single target",
        "reversal": True,
        "reversal_period": 2.0,
        "system_relaxation_time": 7.0,
        "gradient": None,
        "constructibility_note":
            "a reversing approach; carried so accumulation_ratio has a "
            "value somewhere, and it still gates nothing",
        "source": "CONSTRUCTED so the ratio is reachable",
    },

    # ---- reachability: reversal declared and unknown -----------------------
    "deck_unknown_reversal": {
        "geometry_id": "deck_unknown",
        "geometry_class": "bridge deck, exposed",
        "reversal": None,
        "reversal_period": None,
        "system_relaxation_time": None,
        "gradient": 0.0,
        "constructibility_note":
            "a short exposed deck; whether the input reverses on it has not "
            "been established, and None is recorded rather than False",
        "source": "CONSTRUCTED so T1 NOT_EVALUABLE is reachable",
    },
}


# ---------------------------------------------------------------------------
# pairs
# ---------------------------------------------------------------------------

PAIRS = (
    ("serpentine_brake", "driftless_grade"),        # A
    ("serpentine_brake", "single_curve_flat"),      # B
    ("fifth_wheel_latch", "yard_level"),            # C
    ("grade_retarder", "straight_descent"),         # D
    ("stability_cut", "ordinary_two_lane"),         # E
    ("washout_detect", "rural_in_rain"),            # T5
    ("fineness_probe", "boulder_lee"),            # T6
    ("dive_commit", "reversing_ramp"),              # CHOICE 9, and the ratio
    ("culvert_ice", "deck_unknown_reversal"),       # T1 NOT_EVALUABLE
    ("envelope_no_class", "straight_descent"),      # T6 NOT_EVALUABLE
    ("partial_trigger", "straight_descent"),        # intake incomplete
)

# the order's five validation cases, by pair.  The REQUIREMENTS are in
# test_trigger.py; this is only the naming.
ORDER_CASES = {
    "A": ("serpentine_brake", "driftless_grade"),
    "B": ("serpentine_brake", "single_curve_flat"),
    "C": ("fifth_wheel_latch", "yard_level"),
    "D": ("grade_retarder", "straight_descent"),
    "E": ("stability_cut", "ordinary_two_lane"),
}
