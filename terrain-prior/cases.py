"""cases.py -- derivation entries, morphology profiles, observations.

WHAT IS TRANSCRIBED AND WHAT IS NOT

The five seed derivation entries are transcribed from WORK_ORDER.md.  Every
mechanism string is the order's own words.  Where the order states a bearing
or entanglement value in words that are already a class ("Bearing is absent",
"LOW, and lower than the surface mat suggests", "HIGH -- dense flexible
stems"), the class is marked ORDER_STATED.  Where the order describes a
condition and the class is a reading of that description, it is marked
DECLARED_READING.  Nothing is marked ORDER_STATED that the order does not say.

The order states NO falsifier for four of its five seed entries.  None is
invented here.  falsifier_coverage() counts them.

The order states NO entanglement for four of its five seed entries.  None is
invented here.  class_coverage() counts them.

WHAT IS CONSTRUCTED

* The morphology profiles.  Every number on them is illustrative and no
  threshold in this folder connects a number to a class; pressure_class and
  entanglement_susceptibility are declared, per [CHOICE 2].
* The mechanism-less entry for validation case D.
* Every observation.  No site has been visited, no indicator observed, no
  observer_baseline belongs to a person.

WHAT IS MISSING AND IS NOT SUPPLIED

Validation case C is specified on a BOG and the order ships no bog derivation
entry.  A bog entry is not invented here.  Case C is run on the cattail entry,
which is the order's own low-bearing high-entanglement case, and the
substitution is recorded rather than hidden.

NO EXPECTED VERDICT LIVES IN THIS FILE.  Expected flags and priors are in
test_terrain.py so no case can agree with the module by construction.
"""

ORDER = "transcribed from WORK_ORDER.md"
CONSTRUCTED = "CONSTRUCTED for this folder; not an observation of anything"


# ---------------------------------------------------------------------------
# derivation entries
# ---------------------------------------------------------------------------

PINE = {
    "entry_id": "pine_stand",
    "indicator": "pine stand",
    "aliases": ("pine",),
    "indicator_type": "VEGETATION",
    "mechanism": "litter and duff over root structure; surface soft, "
                 "substrate typically firm",
    "implies_bearing": "substrate typically firm; the duff is not the "
                       "bearing surface",
    "bearing_class": "MODERATE",
    "bearing_class_basis": "DECLARED_READING",
    "implies_entanglement": "",
    "entanglement_class": "NOT_STATED",
    "entanglement_class_basis": "NOT_STATED",
    "two_layer": True,
    # "a sensor reading the top layer gets the bearing exactly backwards" --
    # the top layer is the soft duff, so the surface reading is WORSE than the
    # substrate.  That is the pessimistic direction, and it is why P1 and P2
    # are different checks: two-layer does not imply the dangerous direction.
    "sensor_invert": "PESSIMISTIC",
    "confidence": "NOT_STATED",
    "scope": None,
    "scope_regions": (),
    "falsified_by": None,
    "derived_from": ORDER,
}

CYPRESS = {
    "entry_id": "cypress",
    "indicator": "cypress",
    "aliases": (),
    "indicator_type": "VEGETATION",
    "mechanism": "standing or seasonally standing water, buttressed roots, "
                 "irregular contact geometry",
    "implies_bearing": "standing or seasonally standing water",
    "bearing_class": "LOW",
    "bearing_class_basis": "DECLARED_READING",
    "implies_entanglement": "",
    "entanglement_class": "NOT_STATED",
    "entanglement_class_basis": "NOT_STATED",
    "two_layer": False,
    "sensor_invert": "UNKNOWN",
    "confidence": "NOT_STATED",
    "scope": None,
    "scope_regions": (),
    "falsified_by": None,
    "derived_from": ORDER,
}

HARDWOODS = {
    "entry_id": "mature_hardwoods",
    "indicator": "mature hardwoods",
    "aliases": ("hardwoods", "hardwood stand"),
    "indicator_type": "VEGETATION",
    "mechanism": "sustained drainage over the tree's lifetime; bearing "
                 "inferable from the fact the tree is standing",
    "implies_bearing": "firm; sustained drainage over the tree's lifetime",
    "bearing_class": "HIGH",
    "bearing_class_basis": "DECLARED_READING",
    "implies_entanglement": "",
    "entanglement_class": "NOT_STATED",
    "entanglement_class_basis": "NOT_STATED",
    "two_layer": False,
    "sensor_invert": "UNKNOWN",
    "confidence": "NOT_STATED",
    "scope": None,
    "scope_regions": (),
    "falsified_by": None,
    "derived_from": ORDER,
}

# the one entry the order writes out in full.
CATTAILS = {
    "entry_id": "cattails",
    "indicator": "cattails",
    "aliases": ("cattail", "reeds", "reed"),
    "indicator_type": "VEGETATION",
    "mechanism": "obligate of saturated or standing shallow water; root mat "
                 "over unconsolidated saturated sediment",
    "implies_bearing": "LOW, and lower than the surface mat suggests",
    "bearing_class": "LOW",
    "bearing_class_basis": "ORDER_STATED",
    "implies_entanglement": "HIGH -- dense flexible stems at limb height, "
                            "bind when displaced",
    "entanglement_class": "HIGH",
    "entanglement_class_basis": "ORDER_STATED",
    "two_layer": True,
    # "lower than the surface mat suggests": the mat is what a surface sensor
    # reads, so the surface reading is BETTER than the ground.  P2 direction.
    "sensor_invert": "OPTIMISTIC",
    "confidence": "HIGH",
    "scope": "temperate wetland margins",
    "scope_regions": ("temperate wetland margin",
                      "upper midwest wetland margin"),
    "falsified_by": "cattails on a drained or filled site; mat over hardpan",
    "derived_from": ORDER,
}

# the load-bearing landform case, and the only entry that needs branches.
BOULDER = {
    "entry_id": "boulder_sorted_streambed",
    "indicator": "boulder",
    "aliases": ("obstruction",),
    "indicator_type": "LANDFORM",
    "mechanism": "the obstruction sorted the sediment; the deposition zone "
                 "behind it is fines dropped from slowed water, poorly "
                 "consolidated",
    "confidence": "NOT_STATED",
    "scope": None,
    "scope_regions": (),
    "falsified_by": None,
    "derived_from": ORDER,
    "context_branches": (
        {
            "when": {"flow_direction_known": True,
                     "position_relative_to_obstruction": "DOWNSTREAM"},
            "implies_bearing": "bearing is absent; fines dropped from slowed "
                               "water, poorly consolidated",
            "bearing_class": "VERY_LOW",
            "bearing_class_basis": "ORDER_STATED",
            "implies_entanglement": "",
            "entanglement_class": "NOT_STATED",
            "entanglement_class_basis": "NOT_STATED",
            "two_layer": False,
            # "the surface reads SMOOTHER AND FINER than the scoured side, so
            # every existing sensor rates it BETTER" -- the order names the
            # direction outright.
            "sensor_invert": "OPTIMISTIC",
            "falsified_by": None,
        },
        {
            "when": {"flow_direction_known": True,
                     "position_relative_to_obstruction": "UPSTREAM"},
            "implies_bearing": "scoured side; fines removed by accelerated "
                               "flow",
            "bearing_class": "MODERATE",
            "bearing_class_basis": "DECLARED_READING",
            "implies_entanglement": "",
            "entanglement_class": "NOT_STATED",
            "entanglement_class_basis": "NOT_STATED",
            "two_layer": False,
            "sensor_invert": "NONE",
            "falsified_by": None,
        },
    ),
}

# CONSTRUCTED.  Validation case D: an entry with an indicator and an
# implication and no mechanism.
NO_MECHANISM = {
    "entry_id": "sedge_tussocks_no_mechanism",
    "indicator": "sedge tussocks",
    "aliases": (),
    "indicator_type": "VEGETATION",
    "implies_bearing": "LOW",
    "bearing_class": "LOW",
    "bearing_class_basis": "DECLARED_READING",
    "implies_entanglement": "MODERATE",
    "entanglement_class": "MODERATE",
    "entanglement_class_basis": "DECLARED_READING",
    "two_layer": False,
    "sensor_invert": "UNKNOWN",
    "confidence": "LOW",
    "scope": None,
    "scope_regions": (),
    "falsified_by": None,
    "derived_from": CONSTRUCTED,
}

ENTRIES = (PINE, CYPRESS, HARDWOODS, CATTAILS, BOULDER, NO_MECHANISM)

BY_ENTRY_ID = dict((e["entry_id"], e) for e in ENTRIES)


# ---------------------------------------------------------------------------
# morphology profiles -- CONSTRUCTED
# ---------------------------------------------------------------------------
# Every number below is illustrative.  No function in this folder converts a
# number here into a class; pressure_class and entanglement_susceptibility are
# declared, per [CHOICE 2], and the numbers are carried so a reader can see
# what the declaration is meant to describe.

MORPH_HIGH_PRESSURE = {
    "platform_id": "small_contact_high_pressure",
    "contact_area": 0.004,
    "contact_pressure": 180.0,
    "n_contacts": 4,
    "swing_profile": "narrow arc, distal link sweeps at stem height",
    "joint_exposure": ["ankle", "knee"],
    "ankle_to_foot_ratio": 1.8,
    "recovery_from_entanglement": "ACTIVE",
    "pressure_class": "HIGH",
    "entanglement_susceptibility": "HIGH",
    "source": CONSTRUCTED,
}

MORPH_LOW_PRESSURE = {
    "platform_id": "broad_contact_low_pressure",
    "contact_area": 0.090,
    "contact_pressure": 12.0,
    "n_contacts": 6,
    "swing_profile": "wide arc, shrouded links",
    "joint_exposure": [],
    "ankle_to_foot_ratio": 0.6,
    "recovery_from_entanglement": "PASSIVE",
    "pressure_class": "LOW",
    "entanglement_susceptibility": "LOW",
    "source": CONSTRUCTED,
}

MORPHOLOGIES = (MORPH_HIGH_PRESSURE, MORPH_LOW_PRESSURE)
BOTH = MORPHOLOGIES


# ---------------------------------------------------------------------------
# observations -- all CONSTRUCTED
# ---------------------------------------------------------------------------

BASELINE = ("CONSTRUCTED: no person holds this prior and no period is "
            "claimed")


def _obs(obs_id, itype, indicator, region, context=None,
         baseline=BASELINE):
    return {
        "obs_id": obs_id,
        "indicator_type": itype,
        "indicator": indicator,
        "context": context or {},
        "region": region,
        "observer_baseline": baseline,
        "source": CONSTRUCTED,
    }


# A -- the order's stated validation target for the whole instrument.
A_BOULDER = _obs(
    "A_boulder", "LANDFORM", "large boulder in a dry streambed",
    "driftless dry streambed",
    {"flow_direction_known": True,
     "position_relative_to_obstruction": "DOWNSTREAM",
     "season": "late summer",
     "recent_precipitation": "none in fourteen days",
     "slope": 0.02})

# B -- two-layer.
B_PINE = _obs("B_pine", "VEGETATION", "mature pine stand",
              "temperate conifer forest")

# C -- morphology split.  Run on cattails; see the module docstring.
C_SPLIT = _obs("C_split", "VEGETATION", "cattail stand at the bog margin",
               "upper midwest wetland margin")

# D -- falsifier: no mechanism.
D_NO_MECHANISM = _obs("D_no_mechanism", "VEGETATION", "sedge tussocks",
                      "upper midwest wetland margin")

# E -- out of scope.
E_OUT_OF_SCOPE = _obs("E_out_of_scope", "VEGETATION", "cattails",
                      "arid interior basin")

# reachability observations, not in the order.
F_BOULDER_NO_BRANCH = _obs(
    "F_no_branch", "LANDFORM", "large boulder in a dry streambed",
    "driftless dry streambed",
    {"flow_direction_known": False,
     "position_relative_to_obstruction": "UNKNOWN"})

G_BOULDER_UPSTREAM = _obs(
    "G_upstream", "LANDFORM", "large boulder in a dry streambed",
    "driftless dry streambed",
    {"flow_direction_known": True,
     "position_relative_to_obstruction": "UPSTREAM"})

H_NO_ENTRY = _obs("H_no_entry", "VEGETATION", "lichen crust on bare rock",
                  "alpine fellfield")

I_INTAKE = {
    "obs_id": "I_intake",
    "indicator_type": "VEGETATION",
    "indicator": "cattails",
    "context": {},
    "region": "upper midwest wetland margin",
    "source": CONSTRUCTED,
}

J_CYPRESS_NO_MORPH = _obs("J_cypress", "VEGETATION", "cypress",
                          "gulf coastal swamp")

K_HARDWOODS = _obs("K_hardwoods", "VEGETATION", "mature hardwoods",
                   "temperate mixed forest")

OBSERVATIONS = (A_BOULDER, B_PINE, C_SPLIT, D_NO_MECHANISM, E_OUT_OF_SCOPE,
                F_BOULDER_NO_BRANCH, G_BOULDER_UPSTREAM, H_NO_ENTRY,
                I_INTAKE, J_CYPRESS_NO_MORPH, K_HARDWOODS)

BY_ID = dict((o["obs_id"], o) for o in OBSERVATIONS)

# which morphology profiles are supplied with which observation.
# J is deliberately absent from this map: a prior with no morphology returns
# no verdict, which is the prior/rating distinction the hard constraints force.
MORPHOLOGIES_FOR = {
    "A_boulder": BOTH,
    "B_pine": (MORPH_HIGH_PRESSURE,),
    "C_split": BOTH,
    "D_no_mechanism": BOTH,
    "E_out_of_scope": BOTH,
    "F_no_branch": BOTH,
    "G_upstream": BOTH,
    "H_no_entry": BOTH,
    "I_intake": BOTH,
    "K_hardwoods": (MORPH_HIGH_PRESSURE,),
}

# the order's validation set, by obs_id.
ORDER_CASES = ("A_boulder", "B_pine", "C_split", "D_no_mechanism",
               "E_out_of_scope")
