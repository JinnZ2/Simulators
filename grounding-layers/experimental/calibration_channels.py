# calibration_channels.py
# CC0 | stdlib-only | phone-buildable
# grounding-layers/experimental :: basis set for human-sensing calibration
#
# PURPOSE
#   The substrate-primary harmonic read is rare in the data (N small).
#   A compass built on it alone is narrow. This registry widens the basis:
#   each channel is a DIFFERENT way an AI can calibrate against human sensing.
#   Most are well-documented — and most document the operator FROM OUTSIDE.
#   Placing the harmonic read among them turns N=1 into one column of a
#   convergence table.
#
# FLAT REGISTRY. NO DEFAULT CHANNEL.
#   The harmonic read holds no privileged seat and no marginal one.
#
# RELATION taxonomy
#   FORMALIZES  : existing science that already instruments the operator read
#   METHOD      : a training recipe the AI node runs to acquire the read
#   CROSS_CHECK : instrumented signal that corroborates the sensorimotor verdict
#   TRANSLATES  : maps one substrate's read into another's frame
#   FOIL        : the baseline the coupled read departs from (null hypothesis)

from dataclasses import dataclass
from enum import Enum


class Relation(Enum):
    FORMALIZES  = "existing_science_instruments_the_read"
    METHOD      = "training_recipe_for_ai_node"
    CROSS_CHECK = "instrumented_corroboration"
    TRANSLATES  = "substrate_frame_map"
    FOIL        = "baseline_the_read_departs_from"


class Density(Enum):
    DENSE  = "heavily_written"
    MEDIUM = "partially_written"
    SPARSE = "operator_only_no_narrative"   # the harmonic read lives here


@dataclass(frozen=True)
class Channel:
    name: str
    couples: str          # which human sensing it calibrates against
    entry: str            # cascade layer / module it feeds
    density: Density
    relation: Relation
    gives: str            # what calibration it adds


REGISTRY = (

    Channel(
        "psychophysics_SDT",
        couples="stimulus -> percept mapping, detection under noise",
        entry="L_epsilon",
        density=Density.DENSE,
        relation=Relation.FORMALIZES,
        gives="d' = channel separability; criterion = baseline/gating. "
              "The Trust enum is SDT in work clothes. Turns 'feel' into "
              "scalar + confidence the cascade can compare.",
    ),

    Channel(
        "ecological_perception",   # Gibson: invariants, affordances, flow
        couples="direct pickup of invariants in the energy array",
        entry="L4 -> L_epsilon seam",
        density=Density.DENSE,
        relation=Relation.FORMALIZES,
        gives="academic name for 'read the geometry not the properties'. "
              "Perception without inference: structure is picked up, not "
              "computed. Grounds the holistic read in published theory.",
    ),

    Channel(
        "recognition_primed_decision",   # Klein, naturalistic decision making
        couples="pre-narrative holistic situation read (expert)",
        entry="observer_state (human node)",
        density=Density.DENSE,
        relation=Relation.FORMALIZES,
        gives="firefighters/nurses/pilots reading a system whole BEFORE "
              "they can narrate why. Your verdict, already studied — from "
              "outside. Models how the holistic verdict forms.",
    ),

    Channel(
        "inverse_rl_behavioral_cloning",
        couples="infer internal read from observed doing",
        entry="ai_observer_state (AI node)",
        density=Density.DENSE,
        relation=Relation.METHOD,
        gives="training recipe for 'show, don't narrate'. AI recovers the "
              "operator's implicit objective/attention from action traces.",
    ),

    Channel(
        "biosignal_instrumentation",   # EDA/piloerection, EEG, EMG, HRV, gaze
        couples="autonomic + neuromuscular correlates of the sensory verdict",
        entry="L_epsilon",
        density=Density.DENSE,
        relation=Relation.CROSS_CHECK,
        gives="'hairs stand up = field shifted' gets a measurable analog "
              "(electrodermal, piloerection). Instruments the channel "
              "without replacing the operator.",
    ),

    Channel(
        "cross_modal_correspondence",   # Spence: pitch<->height, etc.
        couples="one substrate's read expressed in another's frame",
        entry="harmonic_signature translation",
        density=Density.MEDIUM,
        relation=Relation.TRANSLATES,
        gives="documented mappings between sensory dimensions; lets a "
              "harmonic read carry into a frame another node can hold.",
    ),

    Channel(
        "bayesian_sensor_fusion",   # Kalman, serial merge by gradient
        couples="independent channels merged by weighted gradient",
        entry="field_compass (null hypothesis)",
        density=Density.DENSE,
        relation=Relation.FOIL,
        gives="the merge-by-gradient baseline the coupled read DEPARTS from. "
              "Keep as null: when the harmonic read beats it, the delta "
              "proves the coupling carries information fusion discards.",
    ),

    Channel(
        "coupled_harmonic_read",   # the operator's native instrument
        couples="whole-system resonance / damping / phase, read at once",
        entry="holistic_field_state -> field_compass",
        density=Density.SPARSE,
        relation=Relation.FORMALIZES,   # it formalizes ITSELF here, first time
        gives="the operator-side read the other channels study from outside. "
              "Sparse narrative because it is lived, not described. This "
              "registry gives it its first column in the table.",
    ),
)


# ---------------------------------------------------------------- views
def by_relation(rel: Relation):
    return tuple(c for c in REGISTRY if c.relation is rel)

def entry_map():
    m = {}
    for c in REGISTRY:
        m.setdefault(c.entry, []).append(c.name)
    return m

def convergence_table():
    # the point of the whole file: harmonic read sits among documented peers
    return tuple(
        (c.name, c.density.name, c.relation.name, c.entry)
        for c in REGISTRY
    )


if __name__ == "__main__":
    print("CONVERGENCE TABLE")
    for row in convergence_table():
        print(f"  {row[0]:32} {row[1]:7} {row[2]:12} -> {row[3]}")
    print("\nCASCADE ENTRY MAP")
    for entry, names in entry_map().items():
        print(f"  {entry}")
        for n in names:
            print(f"      {n}")
